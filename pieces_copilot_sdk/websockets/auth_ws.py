from .base_websocket import BaseWebsocket
from pieces_os_client import UserProfile
import json
from ..client import PiecesClient
from typing import Callable,Optional
from websocket import WebSocketApp

class AuthWS(BaseWebsocket):
	def __init__(self, 
		pieces_client: PiecesClient, 
		on_message_callback: Callable[[Optional[UserProfile]], None],
		on_open_callback: Optional[Callable[[WebSocketApp], None]] = None, 
		on_error: Optional[Callable[[websocket.WebSocketApp, Exception], None]] = None, 
		on_close: Optional[Callable[[websocket.WebSocketApp], None]] = None):
		super().__init__(pieces_client, on_message_callback, on_open_callback, on_error, on_close)
	@property
	def url(self):
		return self.pieces_client.AUTH_WS_URL

	def on_message(self,ws, message):
		try:
			self.on_message_callback(UserProfile.from_json(message))
		except json.decoder.JSONDecodeError:
			self.on_message_callback(None) # User logged out!
