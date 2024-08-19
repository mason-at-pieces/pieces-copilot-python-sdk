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
from pieces_copilot_sdk.copilot import Copilot
from pieces_copilot_sdk.basic_identifier.asset import BasicAsset
from pieces_copilot_sdk.streamed_identifiers.assets_snapshot import AssetSnapshot
from websockets import *
from pieces_copilot_sdk.client import PiecesClient
from pieces_copilot_sdk.basic_identifier.basic import Basic
from pieces_copilot_sdk.basic_identifier.message import BasicMessage
from pieces_copilot_sdk.basic_identifier.chat import BasicChat
from pieces_copilot_sdk.streamed_identifiers._streamed_identifiers import StreamedIdentifiersCache
from pieces_copilot_sdk.streamed_identifiers.conversations_snapshot import ConversationsSnapshot

class TestBasicChat:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_conversation = Mock(id="test_id", messages=Mock(indices={}), annotations=None)
        self.mock_conversation.name = "Test Conversation"
        ConversationsSnapshot.identifiers_snapshot = {"test_id": self.mock_conversation}
        ConversationsSnapshot.pieces_client = Mock()
