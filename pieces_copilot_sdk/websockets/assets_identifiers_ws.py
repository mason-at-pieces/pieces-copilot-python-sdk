from typing import Callable,Optional
from pieces_os_client import StreamedIdentifiers,Asset
from ..streamed_identifiers.assets_snapshot import AssetSnapshot
from ..client import PiecesClient
from .base_websocket import BaseWebsocket
from websocket import WebSocketApp


class AssetsIdentifiersWS(BaseWebsocket):
	def __init__(self, pieces_client: PiecesClient, 
		on_asset_update:Optional[Callable[[Asset],None]] = None,
		on_asset_remove:Optional[Callable[[Asset],None]] = None,
		on_open_callback: Optional[Callable[[WebSocketApp], None]] = None, 
		on_error: Optional[Callable[[WebSocketApp, Exception], None]] = None, 
		on_close: Optional[Callable[[WebSocketApp], None]] = None):
		AssetSnapshot.pieces_client = pieces_client
		AssetSnapshot.on_update = on_asset_update if on_asset_update else lambda x:None
		AssetSnapshot.on_remove = on_asset_remove if on_asset_remove else lambda x:None
		super().__init__(pieces_client, AssetSnapshot.streamed_identifiers_callback, on_open_callback, on_error, on_close)
	
	@property
	def url(self):
		return self.pieces_client.ASSETS_IDENTIFIERS_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))
