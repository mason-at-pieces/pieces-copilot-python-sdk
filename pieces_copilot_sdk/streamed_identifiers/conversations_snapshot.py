from ._streamed_identifiers import StreamedIdentifiersCache

class ConversationsSnapshot(StreamedIdentifiersCache):
	@classmethod
	def sort_first_shot(cls):
		# Sort the dictionary by the "updated" timestamp
		sorted_conversations = sorted(cls.identifiers_snapshot.values(), key=lambda x: x.updated.value, reverse=True)
		cls.identifiers_snapshot = {conversation.id:conversation for conversation in sorted_conversations}

	@classmethod
	def _api_call(cls,id):
		con = cls.pieces_client.conversation_api.conversation_get_specific_conversation(id)
		cls.on_update()
		return con
