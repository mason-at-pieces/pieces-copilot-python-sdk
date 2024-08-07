from .base_websocket import BaseWebsocket
import json


class AuthWS(BaseWebsocket):
	@property
	def url(self):
		return self.pieces_client.AUTH_WS_URL

	def on_message(self,ws, message):
		try:
			self.on_message_callback(UserProfile.from_json(message))
		except json.decoder.JSONDecodeError:
			self.on_message_callback(None) # User logged out!
