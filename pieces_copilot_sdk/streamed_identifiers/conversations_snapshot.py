from ..streamed_identifiers import StreamedIdentifiersCache

class ConversationsSnapshot(StreamedIdentifiersCache):
	@classmethod
	def sort_first_shot(cls):
		# Sort the dictionary by the "updated" timestamp
		sorted_conversations = sorted(cls.identifiers_snapshot.values(), key=lambda x: x.updated.value, reverse=True)
		cls.identifiers_snapshot = {conversation.id:conversation for conversation in sorted_conversations}

	def _api_call(self,id):
		self.pieces_client.conversation_get_specific_conversation(id)
