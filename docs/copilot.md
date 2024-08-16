# Copilot
### Method: `ask`

Asks a question to the QGPT model and streams the responses.

**Args:**
- `query` (str): The question to ask.
- `relevant_qgpt_seeds` ([RelevantQGPTSeeds](https://docs.pieces.app/build/reference/python/models/RelevantQGPTSeeds)): Sets the conversation context.


**Yields:**
- `QGPTStreamOutput`: The streamed output from the QGPT model.

**Example:**
```python
import asyncio

async def main():
    async for response in copilot.ask("QUESTION GOES HERE"):
        print("Received response:", response)

asyncio.run(main())
```

### Method: `chats`

Retrieves a list of all chat identifiers.

**Returns:**
- list[[BasicChat](./basic_chat.md)]: A list of [BasicChat](./basic_chat.md) instances representing the chat identifiers.

**Example:**
```python
chat_list = copilot.chats()
for chat in chat_list:
    print(f"Chat ID: {chat.id}, Chat Name: {chat.name}")
```

### Property: `chat` (Getter)

Gets the current conversation being used in the copilot.

**Returns:**
- Optional[[BasicChat](./basic_chat.md)]: The current [BasicChat](./basic_chat.md) instance or `None` if no chat is set.

**Example:**
```python
current_chat = copilot.chat
if current_chat:
    print(f"Current Chat ID: {current_chat.id}")
else:
    print("No chat is currently set.")
```

### Property: `chat` (Setter)

Sets the current conversation to be used in the copilot.

**Args:**
- `chat` (Optional[[BasicChat](./basic_chat.md)]): The [BasicChat](./basic_chat.md) instance to set.

**Raises:**
- `ValueError`: If the provided chat is not a valid [BasicChat](./basic_chat.md)` instance.

**Example:**
```python
new_chat = copilot.chats[0]
try:
    copilot.chat = new_chat
    print("Chat set successfully.")
except ValueError as e:
    print(f"Failed to set chat: {e}")
```
