from pieces_os_client import StreamedIdentifiers, Conversation
from .base_websocket import BaseWebsocket
from ..streamed_identifiers import ConversationsSnapshot
from websocket import WebSocketApp
from typing import Optional, Callable
from ..client import PiecesClient

class ConversationWS(BaseWebsocket):
	def __init__(self, pieces_client: PiecesClient, 
				 on_conversation_update: Optional[Callable[[Conversation], None]] = None,
				 on_conversation_remove: Optional[Callable[[Conversation], None]] = None,
				 on_open_callback: Optional[Callable[[WebSocketApp], None]] = None, 
				 on_error: Optional[Callable[[WebSocketApp, Exception], None]] = None, 
				 on_close: Optional[Callable[[WebSocketApp], None]] = None):
		"""
		Initialize the ConversationWS class.

		:param pieces_client: An instance of PiecesClient.
		:param on_conversation_update: Optional callback for when a conversation is updated.
		:param on_conversation_remove: Optional callback for when a conversation is removed.
		:param on_open_callback: Optional callback for when the WebSocket connection is opened.
		:param on_error: Optional callback for when an error occurs.
		:param on_close: Optional callback for when the WebSocket connection is closed.
		"""
		# Set the pieces_client for ConversationsSnapshot
		ConversationsSnapshot.pieces_client = pieces_client
		
		# Set the update and remove callbacks, defaulting to no-op lambdas if not provided
		ConversationsSnapshot.on_update = on_conversation_update if on_conversation_update else lambda x: None
		ConversationsSnapshot.on_remove = on_conversation_remove if on_conversation_remove else lambda x: None
		
		# Initialize the base WebSocket with the provided callbacks
		super().__init__(pieces_client, ConversationsSnapshot.streamed_identifiers_callback, on_open_callback, on_error, on_close)
	
	@property
	def url(self):
		"""
		Property to get the WebSocket URL for conversations.

		:return: The WebSocket URL for conversations.
		"""
		return self.pieces_client.CONVERSATION_WS_URL

	def on_message(self, ws, message):
		"""
		Handle incoming WebSocket messages.

		:param ws: The WebSocketApp instance.
		:param message: The incoming message as a JSON string.
		"""
		# Parse the incoming message and pass it to the callback
		self.on_message_callback(StreamedIdentifiers.from_json(message))
