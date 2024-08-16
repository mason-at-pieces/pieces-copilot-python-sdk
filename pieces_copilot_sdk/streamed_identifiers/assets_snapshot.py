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
	"""

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



	@staticmethod
	def _sort_first_shot():
		"""
		Placeholder method for sorting the first shot.
		"""
		pass
	
