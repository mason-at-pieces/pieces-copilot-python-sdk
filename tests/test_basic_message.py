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

    def test_init_valid_id(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.id == "test_message_id"
        self.mock_pieces_client.conversation_message_api.message_specific_message_snapshot.assert_called_once_with(
            message="test_message_id", transferables=True
        )

    def test_init_invalid_id(self):
        self.mock_pieces_client.conversation_message_api.message_specific_message_snapshot.side_effect = Exception("Error")
        with pytest.raises(ValueError, match="Error in retrieving the message"):
            BasicMessage(self.mock_pieces_client, "invalid_id")

    def test_raw_property(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.raw == "Test message content"

    def test_raw_setter(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        message.raw = "New content"
        assert message.message.fragment.string.raw == "New content"
        self.mock_pieces_client.conversation_message_api.message_update_value.assert_called_once_with(
            False, message.message
        )

    def test_role_property(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.role == "USER"

    def test_id_property(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.id == "test_message_id"

    def test_delete_method(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        message.delete()
        self.mock_pieces_client.conversation_messages_api.messages_delete_specific_message.assert_called_once_with(
            "test_message_id"
        )

    def test_annotations_property_none(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.annotations is None

    def test_annotations_property_with_annotations(self):
        mock_annotation = Mock()
        mock_annotation.id = "test_annotation_id"
        self.mock_message.annotations = Mock(iterable=[Mock(id="test_annotation_id")])
        self.mock_pieces_client.annotation_api.annotation_specific_annotation_snapshot.return_value = mock_annotation

        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        annotations = message.annotations

        assert annotations is not None
        assert isinstance(annotations, Annotations)
        assert len(annotations.iterable) == 1
        assert annotations.iterable[0].id == "test_annotation_id"

    def test_description_property_no_annotations(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert message.description is None

    def test_description_property_with_description(self):
        # Create a mock annotation with the correct structure
        mock_annotation = Mock()
        mock_annotation.type = AnnotationTypeEnum.DESCRIPTION
        mock_annotation.text = "Test description"

        # Set up the mock message with annotations
        self.mock_message.annotations = Mock(iterable=[Mock(id="test_annotation_id")])

        # Mock the annotation API call
        self.mock_pieces_client.annotation_api.annotation_specific_annotation_snapshot.return_value = mock_annotation

        # Create the BasicMessage instance
        message = BasicMessage(self.mock_pieces_client, "test_message_id")

        # Replace the message's annotations with our mocked annotations
        message.message.annotations = self.mock_message.annotations

        # Now test the description property
        description = message.description
        print("Returned description:", description)

        assert description == "Test description"

        # Verify that the annotation API was called
        self.mock_pieces_client.annotation_api.annotation_specific_annotation_snapshot.assert_called_once_with("test_annotation_id")

    def test_repr(self):
        message = BasicMessage(self.mock_pieces_client, "test_message_id")
        assert repr(message) == "<BasicMessage(id=test_message_id)>"
