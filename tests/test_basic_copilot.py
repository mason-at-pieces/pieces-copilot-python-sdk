import unittest
from datetime import datetime
from queue import Queue
from unittest.mock import Mock, patch
from typing import Generator
from pieces_os_client import (
    QGPTStreamOutput,
    RelevantQGPTSeeds,
    QGPTQuestionOutput,
    QGPTStreamEnum
)
from pieces_os_client.models.qgpt_prompt_pipeline import QGPTPromptPipeline
from typing import TYPE_CHECKING, Optional, Generator
from pieces_os_client import (SeededConversation,
    QGPTStreamInput,
    RelevantQGPTSeeds,
    QGPTQuestionInput,
    QGPTStreamOutput,
    QGPTStreamEnum,
    QGPTQuestionOutput)
from pieces_os_client.models.qgpt_prompt_pipeline import QGPTPromptPipeline
import sys
import importlib.util
import queue
from typing import Literal, Optional, List, TYPE_CHECKING
from pieces_os_client import Conversation, StreamedIdentifiers, Asset
from abc import ABC, abstractmethod
import threading
import pytest
from unittest.mock import Mock, patch, call
from typing import Literal, Optional, List, TYPE_CHECKING
from abc import ABC, abstractmethod
from pieces_os_client import (
    ApiClient,
    Application,
    Configuration,
    ConversationApi,
    ConversationMessageApi,
    ConversationMessagesApi,
    ConversationsApi,
    QGPTApi,
    UserApi,
    FormatApi,
    ConnectorApi,
    SeededConnectorConnection,
    SeededTrackedApplication,
    AssetApi,
    AssetsApi,
    FragmentMetadata,
    ModelsApi,
    AnnotationApi
)
from typing import Optional,Dict
import platform
import atexit
import sys
import importlib.util
import queue
from typing import Dict, List, Union, Callable, TYPE_CHECKING
from pieces_os_client import Conversation, StreamedIdentifiers, Asset
from abc import ABC, abstractmethod
import threading
from pieces_os_client import Conversation, StreamedIdentifiers, Asset
import threading
from websockets import *
from pieces_copilot_sdk.copilot import Copilot
from pieces_copilot_sdk.client import PiecesClient
from pieces_copilot_sdk.basic_identifier.asset import BasicAsset
from pieces_copilot_sdk.basic_identifier.basic import Basic
from pieces_copilot_sdk.basic_identifier.message import BasicMessage
from pieces_copilot_sdk.basic_identifier.chat import BasicChat
from pieces_copilot_sdk.streamed_identifiers.assets_snapshot import AssetSnapshot
from pieces_copilot_sdk.streamed_identifiers._streamed_identifiers import StreamedIdentifiersCache
from pieces_copilot_sdk.streamed_identifiers.conversations_snapshot import ConversationsSnapshot

class BasicCopilotTest(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_client.tracked_application = Mock(id="mock_app_id")
        self.mock_client.model_id = "mock_model_id"
        self.mock_client.qgpt_api = Mock()
        
        # Define a real BasicChat class for testing
        global BasicChat
        class BasicChat:
            def __init__(self, id):
                self.id = id
        
        self.copilot = Copilot(self.mock_client)

        # Mock ConversationsSnapshot
        self.mock_conversations = patch('__main__.ConversationsSnapshot.identifiers_snapshot', {"test_conversation_id": Mock()}).start()
