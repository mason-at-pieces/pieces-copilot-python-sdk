# BasicChat

## Initialization

```python
chat = BasicChat("Your id goes here")
```

## Methods

### `id`
Gets the ID of the conversation.

**Returns:**
- `str`: The ID of the conversation.

### `name`
Gets the name of the conversation.

**Returns:**
- `str`: The name of the conversation, or "New Conversation" if the name is not set.

### `name = name: str`
Sets the name of the conversation.

**Args:**
- `name` (`str`): The new name of the conversation.

### `messages()`
Retrieves the messages in the conversation.

**Returns:**
- `list`: A list of [`BasicMessage`](./basic_message) instances representing the messages in the conversation.

### `annotations`
Gets the annotations of the conversation.

**Returns:**
- `dict` or `None`: The annotations of the conversation, or `None` if not available.

### `description`
Gets the conversation description.

**Returns:**
- `str`: The description of the conversation.

### `delete()`
Deletes the conversation.

## Example
```python
from pieces_copilot_sdk import PiecesClient

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Initialize a BasicChat instance
chat = pieces_client.copilot.chats()[0]

# Get the ID of the conversation
conversation_id = chat.id
print(f"Conversation ID: {conversation_id}")

# Get the name of the conversation
conversation_name = chat.name
print(f"Conversation Name: {conversation_name}")

# Set a new name for the conversation
chat.name = "Project Discussion"
print(f"Updated Conversation Name: {chat.name}")

# Retrieve the messages in the conversation
messages = chat.messages()
for message in messages:
    print(f"Message: {message.raw}")
    print(f"Message Role: {message.role}")

# Get the annotations of the conversation
annotations = chat.annotations
if annotations:
    print(f"Annotations: {annotations}")
else:
    print("No annotations available.")

# Get the description of the conversation
description = chat.description
print(f"Description: {description}")

# Delete the conversation
chat.delete()
print("Conversation deleted.")
```
