from pieces_os_client import StreamedIdentifiers
from .base_websocket import BaseWebsocket


class AssetsIdentifiersWS(BaseWebsocket):
	@property
	def url(self):
		return self.pieces_client.ASSETS_IDENTIFIERS_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))
