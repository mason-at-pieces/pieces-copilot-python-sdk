from pieces_os_client import QGPTStreamOutput,QGPTStreamInput
from websocket import WebSocketConnectionClosedException,WebSocketApp

from .base_websocket import BaseWebsocket
from ..client import PiecesClient

from typing import Callable,Optional

class AskStreamWS(BaseWebsocket):
	def __init__(self, pieces_client: PiecesClient,
		on_message_callback: Callable[[QGPTStreamOutput],None], 
		on_open_callback: Optional[Callable[[WebSocketApp], None]] = None, 
		on_error: Optional[Callable[[WebSocketApp, Exception], None]] = None, 
		on_close: Optional[Callable[[WebSocketApp], None]] = None):
		super().__init__(pieces_client, on_message_callback, on_open_callback, on_error, on_close)
	@property
	def url(self):
		return self.pieces_client.ASK_STREAM_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(QGPTStreamOutput.from_json(message))

	
	def send_message(self,message:QGPTStreamInput):
		try:
			if not self.ws:
				raise WebSocketConnectionClosedException()
			self.ws.send(message.to_json())
		except WebSocketConnectionClosedException:
			self.on_open = lambda ws: ws.send(message.to_json()) # Send the message on opening
			self.start() # Start a new websocket since we are not connected to any