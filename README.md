# Pieces Copilot Python SDK

This repository contains the Pieces Copilot SDK, a convenient wrapper around the Pieces OS Client SDK. It simplifies the process of interacting with your applications by providing a more user-friendly interface to the underlying Pieces OS Client SDK.

## Installation

To use the Pieces Copilot SDK in your project, you need to install it via `pip`:

```bash
pip install pieces_copilot_sdk
```

## Requirements

> **You must either have [Pieces OS](https://docs.pieces.app/installation-getting-started/what-am-i-installing) installed on your local machine or have access to a remote instance of Pieces OS to use this SDK.**

## Usage

First, you need to import the SDK and initialize it with your base URL. The base URL will depend on your setup:

- If you are using a local instance of Pieces OS:
  - On macOS/Windows, use `http://localhost:1000`
  - On Linux, use `http://localhost:5323`
- If you are using a remote instance of Pieces OS, use the URL you have set up for that.

Here's how you can initialize the SDK:

```python
from pieces_copilot_sdk import PiecesClient

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})
```

Then, you can use the various methods provided by the SDK to interact with your applications.

## Features

- **Simplified Interaction**: The Pieces Copilot SDK simplifies the interaction with the Pieces OS Client SDK by providing easy-to-use methods for various operations.
- **Manage Conversations**: The SDK provides various methods to manage conversations such as fetching a specific conversation, updating conversation name, and more.
- **Get User Profile Picture**: Retrieve the user's profile picture using the `get_user_profile_picture()` method.

## Methods

### `create_conversation(name=None, first_message=None)`

This method creates a new conversation. It takes an optional name and optional first message as parameters. It returns a dictionary containing the new conversation and the answer to the first message (if provided).

Example usage:

```python
new_conversation = pieces_client.create_conversation(
    name='Hello World Conversation',
    first_message='Hello, world!'
)
```

### `get_conversation(conversation_id, include_raw_messages=False)`

This method retrieves a conversation by its ID. You can choose to include raw messages in the conversation by setting the `include_raw_messages` parameter to `True`. It returns a dictionary representing the Conversation object or `None`.

Example usage:

```python
conversation = pieces_client.get_conversation(
    conversation_id='conversationId',
    include_raw_messages=True
)
```

### `get_conversations()`

This method retrieves all conversations. It returns a list of Conversation objects or `None`.

Example usage:

```python
conversations = pieces_client.get_conversations()
```

### `prompt_conversation(question, conversation_id, regenerate_conversation_name=False)`

This method prompts a conversation with a message. It takes a message string, conversation ID, and an optional flag to regenerate the conversation name (default is `False`). It returns a dictionary containing the text of the answer, the ID of the user query message, and the ID of the bot response message.

If there are previous messages in the conversation, they will be used as context for the new message.

If there is an error, it will return a dictionary containing only the text of the error message.

Example usage:

```python
answer = pieces_client.prompt_conversation(
    message='Hello, world!',
    conversation_id='conversationId'
)
```

### `update_conversation_name(conversation_id)`

This method generates a new name for a specific conversation based on the messages that have been sent. It takes a conversation ID as a parameter. It returns a string representing the updated conversation name or `None`.

Example usage:

```python
updated_name = pieces_client.update_conversation_name(conversation_id='conversationId')
```

### `get_user_profile_picture()`

This method retrieves the user's profile picture. It returns a string representing the URL of the profile picture or `None`.

Example usage:

```python
profile_picture_url = pieces_client.get_user_profile_picture()
```

## Full Example

Here's a full example of how to use all the methods provided by the SDK:

```python
from pieces_copilot_sdk import PiecesClient

# Create an instance of PiecesClient
pieces_client = PiecesClient(
    config={
        'baseUrl': 'http://localhost:1000'
    }
)

# 1. Create a new conversation
conversation_response = pieces_client.create_conversation(
    props={
        "name": "Test Conversation",
        "firstMessage": "Hello, how can I use the API?"
    }
)

# Check if the conversation was created successfully
if conversation_response:
    print("Conversation Created:", conversation_response['conversation'].id)
    print("First Message Response:", conversation_response['answer']['text'])

    # 2. Get the created conversation details
    conversation_id = conversation_response['conversation'].id
    conversation_details = pieces_client.get_conversation(
        conversation_id=conversation_id,
        include_raw_messages=True
    )

    # Access the conversation name using the key
    print("Conversation Name:", conversation_details.get('name'))

    # 3. Ask a question within the created conversation
    question_response = pieces_client.prompt_conversation(
        message="Can you give me an example code snippet?",
        conversation_id=conversation_id
    )
    print("Question Response:", question_response['text'])

# 4. Retrieve all conversations and print their names
all_conversations = pieces_client.get_conversations()
for conversation in all_conversations:
    print("Conversation Name:", conversation.name)

# 5. Get user profile picture
profile_picture = pieces_client.get_user_profile_picture()
print("User Profile Picture URL:", profile_picture)
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before starting.

## License

This project is licensed under the terms of the MIT license.
