from ._streamed_identifiers import StreamedIdentifiersCache
from pieces_os_client import (Asset, 
							AssetsApi,
							AssetApi,
							ClassificationSpecificEnum,
							FormatApi,
							ClassificationGenericEnum,
							Annotation,
							Format,
							Classification,
							Annotations)


from typing import Optional, Union

class AssetSnapshot(StreamedIdentifiersCache):
	def __init__(self,asset_id:str) -> None:
		self._asset_id = asset_id
		self.asset = self.get_asset(asset_id)
		super().__init__()


	def _api_call(self,id):
		asset = self.pieces_client.asset_api.asset_snapshot(id)
		self.on_update(asset)

	@classmethod
	def get_asset(cls,asset_id) -> Optional[Asset]:
		return cls.identifiers_snapshot.get(asset_id)

	def original_classification_specific(self) -> Optional[ClassificationSpecificEnum]:
		if self.asset:
			return self.asset.original.reference.classification.specific

	def edit_asset_original_format(self,data) -> None:
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
		return (
			self.asset.original.reference.classification.generic ==
			ClassificationGenericEnum.Image
		)

	def get_ocr_content(self) -> Optional[str]:
		if not self.asset:
			return
		format = self.get_ocr_format(self.asset)
		if format is None:
			return
		return self.ocr_from_format(format)
	
	@staticmethod
	def get_ocr_format(src: Asset) -> Optional[Format]:
		image_id = src.original.reference.analysis.image.ocr.raw.id if src.original and src.original.reference and src.original.reference.analysis and src.original.reference.analysis.image and src.original.reference.analysis.image.ocr and src.original.reference.analysis.image.ocr.raw and src.original.reference.analysis.image.ocr.raw.id else None
		if image_id is None:
			return None
		return next((element for element in src.formats.iterable if element.id == image_id), None)
	
	@staticmethod
	def ocr_from_format(src: Optional[Format]) -> Optional[str]:
		if src is None:
			return None
		try:
			return src.file.bytes.raw.decode('utf-8')
		except Exception as e:
			Settings.nvim.async_call(Settings.nvim.err_write,'Error in getting image code:', e)
			return None

	@property
	def name(self) -> Optional[str]:
		return self.asset.name if self.asset else "Unnamed snippet"
	
	@staticmethod
	def sort_first_shot():
		pass

	def get_description(self) -> Optional[Annotation]:
		if not self.asset:
			return
		annotations = self.get_annotations
		annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
		for annotation in annotations:
			if annotation.type == "DESCRIPTION":
				return annotation

	def get_annotations(self) -> Optional[Annotations]:
		if not self.asset:
			return
		return self.asset.annotations.iterable

	def delete(self):
		self.pieces_client.assets_api.assets_delete_asset(self._asset_id)
