from pieces_os_client import StreamedIdentifiers,Conversation
from .base_websocket import BaseWebsocket
from ..streamed_identifiers import ConversationsSnapshot
from websocket import WebSocketApp
from typing import Optional,Callable
from ..client import PiecesClient

class ConversationWS(BaseWebsocket):
	def __init__(self, pieces_client: PiecesClient, 
		on_conversation_update:Optional[Callable[[Conversation],None]] = None,
		on_conversation_remove:Optional[Callable[[Conversation],None]] = None,
		on_open_callback: Optional[Callable[[WebSocketApp], None]] = None, 
		on_error: Optional[Callable[[WebSocketApp, Exception], None]] = None, 
		on_close: Optional[Callable[[WebSocketApp], None]] = None):
		ConversationsSnapshot.pieces_client = pieces_client
		ConversationsSnapshot.on_update = on_conversation_update if on_conversation_update else lambda x:None
		ConversationsSnapshot.on_remove = on_conversation_remove if on_conversation_remove else lambda x:None
		super().__init__(pieces_client, ConversationsSnapshot.streamed_identifiers_callback, on_open_callback, on_error, on_close)
	
	@property
	def url(self):
		return self.pieces_client.CONVERSATION_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))
