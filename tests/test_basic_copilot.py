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
