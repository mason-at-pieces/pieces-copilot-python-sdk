from typing import Literal, Optional
from pieces_os_client.models.conversation_message import ConversationMessage

from ..client import PiecesClient


class BasicMessage:
	def __init__(self,pieces_client:PiecesClient,message:ConversationMessage) -> None:
		self.message = message
		self.pieces_client = pieces_client

	@property
	def raw(self) -> Optional[str]:
		try:
			return self.message.fragment.string.raw
		except: 
			pass

	@raw.setter
	def raw(self,value):
		self.message.fragment.string.raw = value
		self.pieces_client.conversation_message_api.message_specific_message_update(False,self.message)

	@property
	def role(self) -> Literal["USER","SYSTEM","ASSISTANT"]:
		return self.message.role.value

	@property
	def id(self) -> str:
		return self.message.id

	def delete(self):
		self.pieces_client.conversation_messages_api.messages_delete_specific_message(self.message.id)

