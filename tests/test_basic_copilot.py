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
