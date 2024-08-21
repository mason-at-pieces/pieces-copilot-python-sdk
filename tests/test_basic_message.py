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

# Test class
class TestBasicMessage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_pieces_client = Mock()
        self.mock_message = Mock()
        self.mock_message.id = "test_message_id"
        self.mock_message.fragment.string.raw = "Test message content"
        self.mock_message.role.value = "USER"
        self.mock_message.annotations = None

        # Mock the API call
        self.mock_pieces_client.conversation_message_api.message_specific_message_snapshot.return_value = self.mock_message
