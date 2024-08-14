from .streamed_identifiers.assets_snapshot import AssetSnapshot

# Friendly wrapper (to avoid interacting with the pieces_os_client models)

class AssetWrapper:
	"""
	A wrapper class for managing assets.
	"""

	def __init__(self, asset_id) -> None:
		"""
		Initialize the AssetWrapper with a given asset ID.

		:param asset_id: The ID of the asset.
		"""
		self.asset_wrapper = AssetSnapshot(asset_id)

	@property
	def raw(self):
		"""
		Retrieve the raw data of the asset.

		:return: The raw data of the asset.
		"""
		return self.asset_wrapper.get_asset_raw()

	def classification(self):
		"""
		Retrieve the classification of the asset.

		:return: The classification value of the asset, or None if not available.
		"""
		c = self.asset_wrapper.original_classification_specific()
		return c.value if c else None

	def edit_content(self, content: str):
		"""
		Edit the content of the asset.

		:param content: The new content to be set for the asset.
		:return: None.
		"""
		self.asset_wrapper.edit_asset_original_format(content)

	def edit_name(self, name: str):
		"""
		Edit the name of the asset.

		:param name: The new name to be set for the asset.
		:return: None.
		"""
		self.asset_wrapper.asset.name = name
		self.asset_wrapper.edit_asset(self.asset_wrapper.asset)

	@property
	def description(self):
		"""
		Retrieve the description of the asset.

		:return: The description text of the asset, or None if not available.
		"""
		d = self.asset_wrapper.get_description()
		return d.text if d else None

	def delete(self):
		"""
		Delete the asset.
		"""
		self.asset_wrapper.delete()

	@property
	def name(self):
		"""
		Retrieve the name of the asset.

		:return: The name of the asset.
		"""
		return self.asset_wrapper.name
