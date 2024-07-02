import pieces_os_client
from pieces_os_client import (
    Application,
    Configuration,
    ConversationApi,
    ConversationMessageApi,
    ConversationMessagesApi,
    ConversationsApi,
    QGPTApi,
    UserApi,
)

class PiecesClient:
    def __init__(self, config: dict, tracked_application: Application = None):
        self.config = Configuration(
            host=config['baseUrl']
        )

        self.api_client = pieces_os_client.ApiClient(self.config)

        self.conversation_message_api = ConversationMessageApi(self.api_client)
        self.conversation_messages_api = ConversationMessagesApi(self.api_client)
        self.conversations_api = ConversationsApi(self.api_client)
        self.conversation_api = ConversationApi(self.api_client)
        self.qgpt_api = QGPTApi(self.api_client)
        self.user_api = UserApi(self.api_client)

        self.tracked_application = tracked_application or Application(
            id='DEFAULT',
            name="OPEN_SOURCE",
            version='0.0.1',
            platform="MACOS",
            onboarded=False,
            privacy="ANONYMOUS",
        )

    @staticmethod
    def application_to_dict(application: Application) -> dict:
        return {
            'id': application.id,
            'name': application.name,
            'version': application.version,
            'platform': application.platform,
            'onboarded': application.onboarded,
            'privacy': application.privacy,
        }

    def create_conversation(self, props: dict = None) -> dict:
        if props is None:
            props = {}

        name = props.get('name', 'New Conversation')
        first_message = props.get('firstMessage')

        try:
            new_conversation = self.conversations_api.conversations_create_specific_conversation(
                seeded_conversation={
                    'name': name,
                    # 'type': ConversationTypeEnum.Copilot,
                    'type': 'COPILOT',
                }
            )

            if first_message:
                answer = self.prompt_conversation(
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

    def get_conversation(self, conversation_id: str, include_raw_messages: bool = False) -> dict:
        conversation_messages = []

        try:
            conversation = self.conversation_api.conversation_get_specific_conversation(
                conversation=conversation_id,
            )

            if not include_raw_messages:
                return conversation.__dict__

            for message_id, index in (conversation.messages.indices or {}).items():
                message_response = self.conversation_message_api.message_specific_message_snapshot(
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
                **conversation.__dict__,
                'raw_messages': conversation_messages,
            }
        except Exception as error:
            print(f'Error getting conversation: {error}')
            return None

    def get_conversations(self) -> list:
        try:
            conversations = self.conversations_api.conversations_snapshot()
            return conversations.iterable or []
        except Exception as error:
            print(f'Error fetching conversations: {error}')
            return []

    def ask_question(self, question: str) -> str:
        try:
            answer = self.qgpt_api.question(
                qgpt_question_input={
                    'query': question,
                    'pipeline': {
                        'conversation': {
                            'generalizedCodeDialog': {},
                        },
                    },
                    'relevant': {
                        'iterable': [],
                    }
                }
            )
            return answer.answers.iterable[0].text
        except Exception as error:
            print(f'Error asking question: {error}')
            return 'Error asking question'

    def prompt_conversation(self, message: str, conversation_id: str, regenerate_conversation_name: bool = False) -> dict:
        try:
            conversation = self.get_conversation(
                conversation_id=conversation_id,
                include_raw_messages=True,
            )

            if not conversation:
                return {'text': 'Conversation not found'}

            user_message = self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message={
                    # 'role': QGPTConversationMessageRoleEnum.User,
                    'role': 'USER',
                    'fragment': {
                        'string': {
                            'raw': message,
                        },
                    },
                    'conversation': {'id': conversation_id},
                }
            )

            relevant_conversation_messages = [
                {
                    'seed': {
                        # 'type': SeedTypeEnum.Asset,
                        'type': 'SEEDED_ASSET',
                        'asset': {
                            'application': PiecesClient.application_to_dict(self.tracked_application),
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

            answer = self.qgpt_api.question(
                qgpt_question_input={
                    'query': message,
                    'pipeline': {
                        'conversation': {
                            'contextualizedCodeDialog': {},
                        },
                    },
                    'relevant': {
                        'iterable': relevant_conversation_messages,
                    },
                }
            )

            bot_message = self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message={
                    # 'role': QGPTConversationMessageRoleEnum.Assistant,
                    'role': 'ASSISTANT',
                    'fragment': {
                        'string': {
                            'raw': answer.answers.iterable[0].text,
                        },
                    },
                    'conversation': {'id': conversation_id},
                }
            )

            if regenerate_conversation_name:
                self.update_conversation_name(conversation_id=conversation_id)

            return {
                'text': answer.answers.iterable[0].text,
                'user_message_id': user_message.id,
                'bot_message_id': bot_message.id,
            }
        except Exception as error:
            print(f'Error prompting conversation: {error}')
            return {'text': 'Error asking question'}

    def update_conversation_name(self, conversation_id: str) -> str:
        try:
            conversation = self.conversation_api.conversation_specific_conversation_rename(
                conversation=conversation_id,
            )
            return conversation.name
        except Exception as error:
            print(f'Error updating conversation name: {error}')
            return 'Error updating conversation name'

    def get_user_profile_picture(self) -> str:
        try:
            user_res = self.user_api.user_snapshot()
            return user_res.user.picture or None
        except Exception as error:
            print(f'Error getting user profile picture: {error}')
            return None
