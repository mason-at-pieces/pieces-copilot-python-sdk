from ._streamed_identifiers import StreamedIdentifiersCache
from pieces_os_client import (
	Asset, 
	AssetsApi,
	AssetApi,
	ClassificationSpecificEnum,
	FormatApi,
	ClassificationGenericEnum,
	Annotation,
	Format,
	Classification,
	Annotations,
	SeededAsset,
	Seed,
	SeededFormat,
	SeededFragment,
	TransferableString,
	FragmentMetadata)


from typing import Optional, Union
class AssetSnapshot(StreamedIdentifiersCache):
	"""
	A class to represent a snapshot of all the cached Assets.
	
	Class attributes:
		identifiers_snapshot (dict): A dictionary where the keys are UUIDs (unique identifiers) and the values are Asset objects.
	
	Attributes:
		_asset_id (str): The ID of the asset.
		asset (Asset): The asset object.
	"""

	def __init__(self, asset_id: str) -> None:
		"""
		Initialize the AssetSnapshot with the given asset ID.

		Args:
			asset_id (str): The ID of the asset.
		"""
		self._asset_id = asset_id
		self.asset = self.get_asset(asset_id)
		super().__init__()

	@classmethod
	def _api_call(cls, id):
		"""
		Make an API call to get the asset snapshot.

		Args:
			id: The ID of the asset.

		Returns:
			The asset snapshot.
		"""
		asset = cls.pieces_client.asset_api.asset_snapshot(id)
		cls.on_update(asset)
		return asset

	@classmethod
	def get_asset(cls, asset_id) -> Optional[Asset]:
		"""
		Get the asset by its ID.

		Args:
			asset_id: The ID of the asset.

		Returns:
			Optional[Asset]: The asset if found, otherwise None.
		"""
		return cls.identifiers_snapshot.get(asset_id)

	def original_classification_specific(self) -> Optional[ClassificationSpecificEnum]:
		"""
		Get the specific classification of the asset (eg: py).

		Returns:
			Optional[ClassificationSpecificEnum]: The specific classification if available, otherwise None.
		"""
		if self.asset:
			return self.asset.original.reference.classification.specific

	def edit_asset_original_format(self, data) -> None:
		"""
		Edit the original format of the asset.

		Args:
			data: The new data to be set.

		Raises:
			AttributeError: If the asset is not found.
			NotImplemented: If the asset is an image.
		"""
		if not self.asset:
			raise AttributeError("Asset not found")
		format_api = self.pieces_client.format_api
		original = format_api.format_snapshot(self.asset.original.id, transferable=True)
		if original.classification.generic == ClassificationGenericEnum.IMAGE:
			raise NotImplemented("Can't edit an image yet")

		if original.fragment.string.raw:
			original.fragment.string.raw = data
		elif original.file.string.raw:
			original.file.string.raw = data
		format_api.format_update_value(transferable=False, format=original)

	def get_asset_raw(self) -> Optional[str]:
		"""
		Get the raw content of the asset.

		Returns:
			Optional[str]: The raw content if available, otherwise None.

		Raises:
			Exception: If unable to get OCR content for an image.
		"""
		if not self.asset:
			return
		if self.is_image():
			content = self.get_ocr_content()
			if content is None:
				raise Exception('Unable to get OCR content')
			return content
		else:
			return (
				self.asset.original.reference.fragment.string.raw or
				self.asset.preview.base.reference.fragment.string.raw or
				''
			)

	def is_image(self) -> bool:
		"""
		Check if the asset is an image.

		Returns:
			bool: True if the asset is an image, otherwise False.
		"""
		return (
			self.asset.original.reference.classification.generic ==
			ClassificationGenericEnum.Image
		)

	def get_ocr_content(self) -> Optional[str]:
		"""
		Get the OCR content of the asset.

		Returns:
			Optional[str]: The OCR content if available, otherwise None.
		"""
		if not self.asset:
			return
		format = self.get_ocr_format(self.asset)
		if format is None:
			return
		return self.ocr_from_format(format)

	@staticmethod
	def get_ocr_format(src: Asset) -> Optional[Format]:
		"""
		Get the OCR format of the asset.

		Args:
			src (Asset): The asset object.

		Returns:
			Optional[Format]: The OCR format if available, otherwise None.
		"""
		image_id = src.original.reference.analysis.image.ocr.raw.id if src.original and src.original.reference and src.original.reference.analysis and src.original.reference.analysis.image and src.original.reference.analysis.image.ocr and src.original.reference.analysis.image.ocr.raw and src.original.reference.analysis.image.ocr.raw.id else None
		if image_id is None:
			return None
		return next((element for element in src.formats.iterable if element.id == image_id), None)

	@staticmethod
	def ocr_from_format(src: Optional[Format]) -> Optional[str]:
		"""
		Extract OCR content from the format.

		Args:
			src (Optional[Format]): The format object.

		Returns:
			Optional[str]: The OCR content if available, otherwise None.
		"""
		if src is None:
			return None
		try:
			return src.file.bytes.raw.decode('utf-8')
		except Exception as e:
			Settings.nvim.async_call(Settings.nvim.err_write, 'Error in getting image code:', e)
			return None

	@property
	def name(self) -> Optional[str]:
		"""
		Get the name of the asset.

		Returns:
			Optional[str]: The name of the asset if available, otherwise "Unnamed snippet".
		"""
		return self.asset.name if self.asset else "Unnamed snippet"

	@staticmethod
	def _sort_first_shot():
		"""
		Placeholder method for sorting the first shot.
		"""
		pass

	def get_description(self) -> Optional[Annotation]:
		"""
		Get the description annotation of the asset.

		Returns:
			Optional[Annotation]: The description annotation if available, otherwise None.
		"""
		if not self.asset:
			return
		annotations = self.get_annotations
		annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
		for annotation in annotations:
			if annotation.type == "DESCRIPTION":
				return annotation

	def get_annotations(self) -> Optional[Annotations]:
		"""
		Get all annotations of the asset.

		Returns:
			Optional[Annotations]: The annotations if available, otherwise None.
		"""
		if not self.asset:
			return
		return self.asset.annotations.iterable

	def delete(self):
		"""
		Delete the asset.
		"""
		self.pieces_client.assets_api.assets_delete_asset(self._asset_id)

	@classmethod
	def create(cls, raw: str, metadata: Optional[FragmentMetadata] = None) -> str:
		"""
		Create a new asset.

		Args:
			raw (str): The raw content of the asset.
			metadata (Optional[FragmentMetadata]): The metadata of the asset.

		Returns:
			str: The ID of the created asset.
		"""
		seed = Seed(
			asset=SeededAsset(
				application=cls.pieces_client.tracked_application,
				format=SeededFormat(
					fragment=SeededFragment(
						string=TransferableString(raw=raw),
						metadata=metadata
					)
				),
				metadata=None
			),
			type="SEEDED_ASSET"
		)

		created_asset_id = cls.pieces_client.assets_api.assets_create_new_asset(transferables=False, seed=seed).id
		return created_asset_id

	@classmethod
	def edit_asset(cls,asset):
		cls.pieces_client.asset_api.asset_update(False,asset)
