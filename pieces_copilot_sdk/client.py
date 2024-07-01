from pieces_os_client import (
    Application,
    Configuration,
    ConversationApi,
    ConversationMessageApi,
    ConversationMessagesApi,
    ConversationsApi,
    ConversationTypeEnum,
    QGPTApi,
    QGPTConversationMessageRoleEnum,
    QGPTQuestionInput,
    SeededConversation,
    SeededConversationMessage,
    UserApi,
)

class PiecesClient:
    def __init__(self, config: dict, tracked_application: Application = None):
        self.config = Configuration(
            host=config['baseUrl']
        )

        self.conversation_messages_api = ConversationMessagesApi(self.config)
        self.conversations_api = ConversationsApi(self.config)
        self.conversation_api = ConversationApi(self.config)
        self.qgpt_api = QGPTApi(self.config)
        self.user_api = UserApi(self.config)

        self.tracked_application = tracked_application or Application(
            id='DEFAULT',
            # name=ApplicationNameEnum.OpenSource,
            name="OPEN_SOURCE",
            version='0.0.1',
            # platform=PlatformEnum.Macos,
            platform="MACOS",
            onboarded=False,
            # privacy=PrivacyEnum.Anonymous,
            privacy="ANONYMOUS",
        )

    async def create_conversation(self, props: dict = None) -> dict:
        if props is None:
            props = {}

        name = props.get('name', 'New Conversation')
        first_message = props.get('firstMessage')

        try:
            seeded_conversation_input = SeededConversation(
                name=name,
                pipeline={
                    'conversation': {
                        'contextualizedCodeDialog': {},
                    },
                },
                type=ConversationTypeEnum.COPILOT,
            )

            new_conversation = await self.conversations_api.conversations_create_specific_conversation(
                seeded_conversation=seeded_conversation_input
            )

            if first_message:
                answer = await self.prompt_conversation(
                    message=first_message,
                    conversation_id=new_conversation.id,
                )

                return {
                    'conversation': new_conversation,
                    'answer': answer
                }

            return {'conversation': new_conversation}
        except Exception as error:
            print(f'Error creating conversation: {error}')
            return None

    async def get_conversation(self, conversation_id: str, include_raw_messages: bool = False) -> dict:
        conversation_messages = []

        try:
            conversation = await self.conversation_api.conversation_get_specific_conversation(
                conversation=conversation_id,
            )

            if not include_raw_messages:
                return conversation

            conversation_message_api = ConversationMessageApi(self.config)
            for message_id, index in (conversation.messages.indices or {}).items():
                message_response = await conversation_message_api.message_specific_message_snapshot(
                    message=message_id,
                )

                if (not message_response.fragment or
                        not message_response.fragment.string or
                        not message_response.fragment.string.raw):
                    continue

                conversation_messages.append({
                    'message': message_response.fragment.string.raw,
                    'is_user_message': message_response.role == 'USER',
                })

            return {
                **conversation,
                'raw_messages': conversation_messages,
            }
        except Exception as error:
            print(f'Error getting conversation: {error}')
            return None

    async def get_conversations(self) -> list:
        try:
            conversations = await self.conversations_api.conversations_snapshot()
            return conversations.iterable or []
        except Exception as error:
            print(f'Error fetching conversations: {error}')
            return []

    async def ask_question(self, question: str) -> str:
        try:
            question_input = QGPTQuestionInput(
                question=question,
                pipeline={
                    'conversation': {
                        'generalizedCodeDialog': {},
                    },
                },
                relevant={
                    'iterable': [],
                },
            )

            answer = await self.qgpt_api.question(
                qgpt_question_input=question_input,
            )
            return answer.answers.iterable[0].text
        except Exception as error:
            print(f'Error asking question: {error}')
            return 'Error asking question'

    async def prompt_conversation(self, message: str, conversation_id: str, regenerate_conversation_name: bool = False) -> dict:
        try:
            conversation = await self.get_conversation(
                conversation_id=conversation_id,
                include_raw_messages=True,
            )

            if not conversation:
                return {'text': 'Conversation not found'}

            seeded_conversation_message_input = SeededConversationMessage(
                role=QGPTConversationMessageRoleEnum.User,
                fragment={
                    'string': {
                        'raw': message,
                    },
                },
                conversation={'id': conversation_id},
            )

            user_message = await self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message=seeded_conversation_message_input,
            )

            relevant_conversation_messages = [
                {
                    'seed': {
                        'type': 'SEEDED_ASSET',
                        'asset': {
                            'application': {
                                **self.tracked_application,
                            },
                            'format': {
                                'fragment': {
                                    'string': {
                                        'raw': msg['message'],
                                    },
                                },
                            },
                        },
                    }
                }
                for msg in (conversation.get('raw_messages') or [])
            ]

            qgpt_question_input = QGPTQuestionInput(
                query=message,
                pipeline={
                    'conversation': {
                        'contextualizedCodeDialog': {},
                    },
                },
                relevant={
                    'iterable': relevant_conversation_messages,
                },
            )

            answer = await self.qgpt_api.question(
                qgpt_question_input=qgpt_question_input,
            )

            seeded_conversation_message_input = SeededConversationMessage(
                role=QGPTConversationMessageRoleEnum.Assistant,
                fragment={
                    'string': {
                        'raw': answer.answers.iterable[0].text,
                    },
                },
                conversation={'id': conversation_id},
            )

            bot_message = await self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message=seeded_conversation_message_input,
            )

            if regenerate_conversation_name:
                await self.update_conversation_name(conversation_id=conversation_id)

            return {
                'text': answer.answers.iterable[0].text,
                'user_message_id': user_message.id,
                'bot_message_id': bot_message.id,
            }
        except Exception as error:
            print(f'Error prompting conversation: {error}')
            return {'text': 'Error asking question'}

    async def update_conversation_name(self, conversation_id: str) -> str:
        try:
            conversation = await self.conversation_api.conversation_specific_conversation_rename(
                conversation=conversation_id,
            )
            return conversation.name
        except Exception as error:
            print(f'Error updating conversation name: {error}')
            return 'Error updating conversation name'

    async def get_user_profile_picture(self) -> str:
        try:
            user_res = await self.user_api.user_snapshot()
            return user_res.user.picture or None
        except Exception as error:
            print(f'Error getting user profile picture: {error}')
            return None
