from typing import Optional, AsyncGenerator
import asyncio
from pieces_os_client import (SeededConversation,
    QGPTStreamInput,
    RelevantQGPTSeeds,
    QGPTQuestionInput,
    QGPTStreamOutput,
    QGPTStreamEnum)
from pieces_copilot_sdk.basic_identifier.chat import BasicChat
from pieces_copilot_sdk.streamed_identifiers.conversations_snapshot import ConversationsSnapshot
from pieces_copilot_sdk.websockets import AskStreamWS


class Copilot:
    """
    A class to interact with the Pieces Copilot SDK for managing conversations and streaming QGPT responses.
    """

    def __init__(self, pieces_client):
        """
        Initializes the Copilot instance.

        Args:
            pieces_client: The client instance to interact with the Pieces API.
        """
        self.pieces_client = pieces_client
        self.message_queue = asyncio.Queue()
        self.ask_stream_ws = AskStreamWS(self.pieces_client, self._on_stream_message)
        self._chat = None

    def _on_stream_message(self, message: QGPTStreamOutput):
        """
        Callback function to handle incoming stream messages.

        Args:
            message (QGPTStreamOutput): The message received from the stream.
        """
        asyncio.create_task(self.message_queue.put(message))

    async def ask(self,
                  query: str,
                  relevant_qgpt_seeds: RelevantQGPTSeeds = RelevantQGPTSeeds(iterable=[])) -> AsyncGenerator[QGPTStreamOutput, None]:
        """
        Asks a question to the QGPT model and streams the responses.

        Args:
            query (str): The question to ask.
            relevant_qgpt_seeds (RelevantQGPTSeeds): Relevant seeds for the QGPT model.
            chat_id (Optional[str]): The ID of the chat to continue the conversation in.

        Yields:
            QGPTStreamOutput: The streamed output from the QGPT model.
        """
        id = self._chat.id if self._chat else None
        self.ask_stream_ws.send_message(
            QGPTStreamInput(
                question=QGPTQuestionInput(
                    relevant=relevant_qgpt_seeds,
                    query=query,
                    application=self.pieces_client.tracked_application.id,
                    model=self.pieces_client.model_id
                ),
                conversation=id,
            )
        )

        while True:
            message: QGPTStreamOutput = await self.message_queue.get()
            if message.status != QGPTStreamEnum.IN_MINUS_PROGRESS:  # Loop only while in progress
                yield message
                self.chat_id = BasicChat(message.conversation)  # Save the conversation
                break
            yield message

    def chats(self) -> list[BasicChat]:
        """
        Retrieves a list of all chat identifiers.

        Returns:
            list[BasicChat]: A list of BasicChat instances representing the chat identifiers.
        """
        return [BasicChat(id) for id in ConversationsSnapshot.identifiers_snapshot]

    @property
    def chat(self) -> Optional[BasicChat]:
        """
        Gets the current conversation being used in the copilot.

        Returns:
            Optional[BasicChat]: The current chat instance or None if no chat is set.
        """
        return self._chat

    @chat.setter
    def chat(self, chat: Optional[BasicChat]):
        """
        Sets the current conversation to be used in the copilot.

        Args:
            chat (Optional[BasicChat]): The chat instance to set.

        Raises:
            ValueError: If the provided chat is not a valid BasicChat instance.
        """
        if not (chat is None or isinstance(chat, BasicChat)):
            raise ValueError("Not a valid chat")
        self._chat = chat
