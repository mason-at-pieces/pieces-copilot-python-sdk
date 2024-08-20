# BasicMessage

This represents a Copilot chat message to opentain that model you should be using `pieces_client.copilot.chat.messages()` to opentain the messages of the current chat.

## Properties

### `raw_content`

Sets the raw content of the message and updates it in the API.

### `role`

Gets the role of the message.

**Returns:**
- `Literal["USER", "SYSTEM", "ASSISTANT"]`: The role of the message.

### `id`

Gets the ID of the message.

**Returns:**
- `str`: The ID of the message.


## Methods
### `delete`

Deletes the message.

**Example:**
```python
# Delete the message
message.delete()
print("Message deleted.")
```

### Example Usage

```python

from pieces_copilot_sdk import PiecesClient

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Initialize a BasicChat instance
chat = pieces_client.copilot.chats()[0]
messages = chat.messages()

# Set the raw content of the message
message.raw_content = "This is the updated raw content of the message."
print("Raw content updated.")

# Get the role of the message
role = message.role
print(f"Role: {role}")

# Get the ID of the message
message_id = message.id
print(f"Message ID: {message_id}")

# Delete the message
message.delete()
print("Message deleted.")

pieces_client.close()
```
