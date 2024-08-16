from typing import Optional, AsyncGenerator
import asyncio
from pieces_os_client import (SeededConversation,
    QGPTStreamInput,
    RelevantQGPTSeeds,
    QGPTQuestionInput,
    QGPTStreamOutput,
    QGPTStreamEnum)
from pieces_copilot_sdk.client import PiecesClient
from pieces_copilot_sdk.websockets import AskStreamWS


class Copilot:
    def __init__(self, pieces_client:PiecesClient):
        self.pieces_client = pieces_client
        self.message_queue = asyncio.Queue()
        self.ask_stream_ws = AskStreamWS(self.pieces_client, self.on_stream_message)
        self.conversation_id = None

    def on_stream_message(self, message:QGPTStreamOutput):
        asyncio.create_task(self.message_queue.put(message))

    async def ask(self,
        query:str,
        relevant_qgpt_seeds:RelevantQGPTSeeds=RelevantQGPTSeeds(iterable=[]),
        conversation_id: Optional[str] = None) -> AsyncGenerator[QGPTStreamOutput, None]:
        self.ask_stream_ws.send_message(
            QGPTStreamInput(
                question=QGPTQuestionInput(
                    relevant=relevant_qgpt_seeds,
                    query=query,
                    application=self.pieces_client.tracked_application.id,
                    model = self.pieces_client.model_id
                ),
                conversation = conversation_id or self._conversation_id,
            )
        )

        while True:
            message:QGPTStreamOutput = await self.message_queue.get()
            if message.status != QGPTStreamEnum.IN_MINUS_PROGRESS: # Loop only while in progress
              yield message
              self._conversation_id = message.conversation # Save the conversation
              break  
            yield message


    # def get_conversation(self, conversation_id: str, include_raw_messages: bool = False) -> dict:
    #     conversation_messages = []

    #     try:
    #         conversation = self.conversation_api.conversation_get_specific_conversation(
    #             conversation=conversation_id,
    #         )

    #         if not include_raw_messages:
    #             return conversation.__dict__

    #         for message_id, index in (conversation.messages.indices or {}).items():
    #             message_response = self.conversation_message_api.message_specific_message_snapshot(
    #                 message=message_id,
    #             )

    #             if (not message_response.fragment or
    #                     not message_response.fragment.string or
    #                     not message_response.fragment.string.raw):
    #                 continue

    #             conversation_messages.append({
    #                 'message': message_response.fragment.string.raw,
    #                 'is_user_message': message_response.role == 'USER',
    #             })

    #         return {
    #             **conversation.__dict__,
    #             'raw_messages': conversation_messages,
    #         }
    #     except Exception as error:
    #         print(f'Error getting conversation: {error}')
    #         return None


    # def ask_question(self, question: str) -> str:
    #     try:
    #         answer = self.qgpt_api.question(
    #             qgpt_question_input={
    #                 'query': question,
    #                 'pipeline': {
    #                     'conversation': {
    #                         'generalizedCodeDialog': {},
    #                     },
    #                 },
    #                 'relevant': {
    #                     'iterable': [],
    #                 }
    #             }
    #         )
    #         return answer.answers.iterable[0].text
    #     except Exception as error:
    #         print(f'Error asking question: {error}')
    #         return 'Error asking question'


    # def prompt_conversation(self, message: str, conversation_id: str, regenerate_conversation_name: bool = False) -> dict:
    #     try:
    #         conversation = self.get_conversation(
    #             conversation_id=conversation_id,
    #             include_raw_messages=True,
    #         )

    #         if not conversation:
    #             return {'text': 'Conversation not found'}

    #         user_message = self.conversation_messages_api.messages_create_specific_message(
    #             seeded_conversation_message={
    #                 # 'role': QGPTConversationMessageRoleEnum.User,
    #                 'role': 'USER',
    #                 'fragment': {
    #                     'string': {
    #                         'raw': message,
    #                     },
    #                 },
    #                 'conversation': {'id': conversation_id},
    #             }
    #         )

    #         relevant_conversation_messages = [
    #             {
    #                 'seed': {
    #                     # 'type': SeedTypeEnum.Asset,
    #                     'type': 'SEEDED_ASSET',
    #                     'asset': {
    #                         'application': self.tracked_application.to_dict(),
    #                         'format': {
    #                             'fragment': {
    #                                 'string': {
    #                                     'raw': msg['message'],
    #                                 },
    #                             },
    #                         },
    #                     },
    #                 }
    #             }
    #             for msg in (conversation.get('raw_messages') or [])
    #         ]

    #         answer = self.qgpt_api.question(
    #             qgpt_question_input={
    #                 'query': message,
    #                 'pipeline': {
    #                     'conversation': {
    #                         'contextualizedCodeDialog': {},
    #                     },
    #                 },
    #                 'relevant': {
    #                     'iterable': relevant_conversation_messages,
    #                 },
    #             }
    #         )

    #         bot_message = self.conversation_messages_api.messages_create_specific_message(
    #             seeded_conversation_message={
    #                 # 'role': QGPTConversationMessageRoleEnum.Assistant,
    #                 'role': 'ASSISTANT',
    #                 'fragment': {
    #                     'string': {
    #                         'raw': answer.answers.iterable[0].text,
    #                     },
    #                 },
    #                 'conversation': {'id': conversation_id},
    #             }
    #         )

    #         if regenerate_conversation_name:
    #             self.update_conversation_name(conversation_id=conversation_id)

    #         return {
    #             'text': answer.answers.iterable[0].text,
    #             'user_message_id': user_message.id,
    #             'bot_message_id': bot_message.id,
    #         }
    #     except Exception as error:
    #         print(f'Error prompting conversation: {error}')
    #         return {'text': 'Error asking question'}

    # def update_conversation_name(self, conversation_id: str) -> str:
    #     try:
    #         conversation = self.conversation_api.conversation_specific_conversation_rename(
    #             conversation=conversation_id,
    #         )
    #         return conversation.name
    #     except Exception as error:
    #         print(f'Error updating conversation name: {error}')
    #         return 'Error updating conversation name'