# Copilot
### Method: `ask`

Asks a question to the QGPT model and streams the responses.
by default it will create a new conversation and always use it in the ask.
You can always change the conversation in copilot.chat = BasicChat(chat_id="YOU ID GOES HERE")


**Args:**
- `query` (str): The question to ask.
- `relevant_qgpt_seeds` ([RelevantQGPTSeeds](https://docs.pieces.app/build/reference/python/models/RelevantQGPTSeeds)): Sets the conversation context.


**Yields:**
- `QGPTStreamOutput`: The streamed output from the QGPT model.

**Example:**
```python
from pieces_copilot_sdk import PiecesClient

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

for response in pieces_client.copilot.stream_question("Your question"):
    if response.question:
        answers = response.question.answers.iterable
        for answer in answers:
            print(answer.text,end="")
```

### Method: `question`
Asks a question to the QGPT model and return the responses,
Note: the question is not a part of any conversation.

**Args:**
    query (str): The question to ask.
    relevant_qgpt_seeds (RelevantQGPTSeeds): Context to the model .
    pipeline (Optional[QGPTPromptPipeline]): the pipeline to use.

**returns:**
    [QGPTQuestionOutput](https://docs.pieces.app/build/reference/python/models/QGPTQuestionOutput): The streamed output from the QGPT model.

```python
from pieces_copilot_sdk import PiecesClient

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

text = pieces_client.copilot.question("Your question").answers.iterable[0].text
print(text)
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
