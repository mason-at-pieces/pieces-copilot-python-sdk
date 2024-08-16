from pieces_os_client.models.conversation import Conversation
from ..streamed_identifiers import ConversationsSnapshot
from typing import Optional,List
from .basic import Basic
from .message import BasicMessage

class BasicChat(Basic):
	def __init__(self,conversation_id) -> None:
		"""
		Initialize the Chat with a given Conversation ID.

		:param conversation_id: The ID of the asset.
		"""

		self._conversation_id = conversation_id
		self.conversation:Conversation = ConversationsSnapshot.identifiers_snapshot.get(conversation_id)
		if not self.conversation:
			raise ValueError("Conversation not found")

	@property
	def id(self):
		return self.conversation.id

	@property
	def name(self) -> str:
		return self.conversation.name if self.conversation.name else "New Conversation"

	@name.setter
	def name(self,name):
		self.conversation.name = name
		self._edit_conversation(self.conversation)

	def messages(self) -> List[BasicMessage]:
		out = []
		for message_id, index in (self.conversation.messages.indices or {}).items():
			message_response = self._get_message(message_id)
			if index == -1: # Deleted message
				continue
			out.append(BasicMessage(message_response))
		return out

	@staticmethod
	def _get_message(message_id):
		return ConversationsSnapshot.pieces_client.conversation_message_api.message_specific_message_snapshot(message=message_id,transferables=True)
		

	@property
	def annotations(self):
		return getattr(self.conversation.annotations,"iterable",None)

	def delete(self):
		ConversationsSnapshot.pieces_client.conversations_api.conversations_delete_specific_conversation(self.id)

	@staticmethod
	def _edit_conversation(conversation):
		ConversationsSnapshot.pieces_client.conversation_api.conversation_update(False,conversation)



