# Pieces Copilot Python SDK Websockets

Pieces depends on websockets in many apis for many reasons the most important reason is to cache the requests.

**All websockets inherit from BaseWebsocket class**

## Common methods between the websockets

1. `.start()`: Start the websocket connection
2. `.close()`: Close the websocket connection
3. `.reconnect()`: Reconnects the websocket connection

## AskStreamWS Websocket

The `AskStreamWS` used in sending messages to the copilot and receiving streamed messages from it

### Args
1. `pieces_client`: 
    - **Type**: `PiecesClient`
    - **Description**: An instance of the `PiecesClient` class that is used to interact with the Pieces Api.
    - **required**: True

2. `on_message_callback`: 
    - **Type**: `Callable[[QGPTStreamOutput], None]`
    - **Description**: A function that gets called whenever a message is sent to the websocket.
    - **Parameter**: It takes one parameter, which is of type [`QGPTStreamOutput`](https://docs.pieces.app/build/reference/python/models/QGPTStreamOutput).
    - **Return Value**: This function does not return any value.
    - **required**: True

3. `on_open_callback`: 
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the websocket connection is opened.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **required**: False

4. `on_error`: 
    - **Type**: `Optional[Callable[[WebSocketApp, Exception], None]]`
    - **Description**: An optional function that gets called when an error occurs in the websocket connection.
    - **Parameters**: 
        - `WebSocketApp`: The websocket application instance where the error occurred.
        - `Exception`: The exception that was raised.
    - **Return Value**: This function does not return any value.
    - **required**: False

5. `on_close`: 
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the websocket connection is closed.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **required**: False

### Special Methods
1. `.send_message`: 
	- **Description**: Send a message to the ask websocket
	- **args**: [QGPTStreamInput](https://docs.pieces.app/build/reference/python/models/QGPTStreamInput)
<!-- # TODO: @Mason I think in the streamed input we have a way to construct it using the pieces client -->

### Example
```python 
from typing import Callable, Optional
from websocket import WebSocketApp, WebSocketConnectionClosedException
from pieces_os_client import QGPTStreamOutput,QGPTStreamInput
from pieces_copilot_sdk import PiecesClient
from pieces_copilot_sdk.websockets import AskStreamWS

pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})


# Define the callback functions
def on_message_callback(output: QGPTStreamOutput):
    print("Message received:", output)

def on_open_callback(ws: WebSocketApp):
    print("WebSocket connection opened")

def on_error_callback(ws: WebSocketApp, error: Exception):
    print("WebSocket error:", error)

def on_close_callback(ws: WebSocketApp):
    print("WebSocket connection closed")

# Create an instance of AskStreamWS
ask_stream_ws = AskStreamWS(
    pieces_client=pieces_client,
    on_message_callback=on_message_callback,
    on_open_callback=on_open_callback,
    on_error=on_error_callback,
    on_close=on_close_callback
)

# Start the WebSocket connection
ask_stream_ws.start()

# Send a message
message = QGPTStreamInput() # TODO Fill this model
ask_stream_ws.send_message(message)
```


## AuthWS WebSocket

The `AuthWS` class is used for managing WebSocket connections to handle Login/Logout events.

### Args

1. **pieces_client**:
    - **Type**: `PiecesClient`
    - **Description**: An instance of the `PiecesClient` class that is used to interact with the Pieces API.
    - **Required**: True

2. **on_message_callback**:
    - **Type**: `Callable[[Optional[UserProfile]], None]`
    - **Description**: A function called when the User login or logout, if the user logged out it will be invoked with `None`
    - **Parameter**: It takes one parameter, which is of type [`UserProfile` ](https://docs.pieces.app/build/reference/python/models/UserProfile)or `None`.
    - **Return Value**: This function does not return any value.
    - **Required**: True

3. **on_open_callback**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is opened.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

4. **on_error**:
    - **Type**: `Optional[Callable[[WebSocketApp, Exception], None]]`
    - **Description**: An optional function that gets called when an error occurs in the WebSocket connection.
    - **Parameters**:
        - `WebSocketApp`: The WebSocket application instance where the error occurred.
        - `Exception`: The exception that was raised.
    - **Return Value**: This function does not return any value.
    - **Required**: False

5. **on_close**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is closed.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

### Example

```python
from typing import Callable, Optional
from websocket import WebSocketApp, WebSocketConnectionClosedException
from pieces_os_client import UserProfile
from pieces_copilot_sdk import PiecesClient
from pieces_copilot_sdk.websockets import AuthWS

# Initialize the PiecesClient
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Define the callback functions
def on_message_callback(user_profile: Optional[UserProfile]):
    if user_profile:
        print("User profile received:", user_profile)
    else:
        print("User logged out!")

def on_open_callback(ws: WebSocketApp):
    print("WebSocket connection opened")

def on_error_callback(ws: WebSocketApp, error: Exception):
    print("WebSocket error:", error)

def on_close_callback(ws: WebSocketApp):
    print("WebSocket connection closed")

# Create an instance of AuthWS
auth_ws = AuthWS(
    pieces_client=pieces_client,
    on_message_callback=on_message_callback,
    on_open_callback=on_open_callback,
    on_error=on_error_callback,
    on_close=on_close_callback
)

# Start the WebSocket connection
auth_ws.start()

```

## HealthWS WebSocket

The `HealthWS` class is used for managing WebSocket checking the connectivity and the Pieces OS Health.

### Args

1. **pieces_client**:
    - **Type**: `PiecesClient`
    - **Description**: An instance of the `PiecesClient` class that is used to interact with the Pieces API.
    - **Required**: True

2. **on_message_callback**:
    - **Type**: `Callable[[str], None]`
    - **Description**: A function called when a health status message is received.
    - **Parameter**: It takes one parameter, which is a string representing the health status message it should be 'OK' if not then there is an issue with Pieces OS.
    - **Return Value**: This function does not return any value.
    - **Required**: True

3. **on_open_callback**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is opened.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

4. **on_error**:
    - **Type**: `Optional[Callable[[WebSocketApp, Exception], None]]`
    - **Description**: An optional function that gets called when an error occurs in the WebSocket connection.
    - **Parameters**:
        - `WebSocketApp`: The WebSocket application instance where the error occurred.
        - `Exception`: The exception that was raised.
    - **Return Value**: This function does not return any value.
    - **Required**: False

5. **on_close**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is closed, Means **Pieces OS is closed**.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

### Example

```python
from typing import Callable, Optional
from websocket import WebSocketApp, WebSocketConnectionClosedException
from pieces_copilot_sdk import PiecesClient
from pieces_copilot_sdk.websockets import HealthWS

# Initialize the PiecesClient
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Define the callback functions
def on_message_callback(message: str):
    print("Health status message received:", message)

def on_open_callback(ws: WebSocketApp):
    print("WebSocket connection opened")

def on_error_callback(ws: WebSocketApp, error: Exception):
    print("WebSocket error:", error)

def on_close_callback(ws: WebSocketApp):
    print("WebSocket connection closed")

# Create an instance of HealthWS
health_ws = HealthWS(
    pieces_client=pieces_client,
    on_message_callback=on_message_callback,
    on_open_callback=on_open_callback,
    on_error=on_error_callback,
    on_close=on_close_callback
)

# Start the WebSocket connection
health_ws.start()
```


## AssetsIdentifiersWS WebSocket

The `AssetsIdentifiersWS` class is used for managing WebSocket connections to monitor asset updates and removals. 
**We already cache the assets by default**

### Args

1. **pieces_client**:
    - **Type**: `PiecesClient`
    - **Description**: An instance of the `PiecesClient` class that is used to interact with the Pieces API.
    - **Required**: True

2. **on_asset_update**:
    - **Type**: `Optional[Callable[[Asset], None]]`
    - **Description**: An optional function that gets called when an asset update message is received.
    - **Parameter**: It takes one parameter, which is an instance of the [`Asset`](https://docs.pieces.app/build/reference/python/models/Asset) class representing the updated asset.
    - **Return Value**: This function does not return any value.
    - **Required**: False

3. **on_asset_remove**:
    - **Type**: `Optional[Callable[[Asset], None]]`
    - **Description**: An optional function that gets called when an asset removal message is received.
    - **Parameter**: It takes one parameter, which is an instance of the [`Asset`](https://docs.pieces.app/build/reference/python/models/Asset) class representing the removed asset.
    - **Return Value**: This function does not return any value.
    - **Required**: False

4. **on_open_callback**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is opened.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

5. **on_error**:
    - **Type**: `Optional[Callable[[WebSocketApp, Exception], None]]`
    - **Description**: An optional function that gets called when an error occurs in the WebSocket connection.
    - **Parameters**:
        - `WebSocketApp`: The WebSocket application instance where the error occurred.
        - `Exception`: The exception that was raised.
    - **Return Value**: This function does not return any value.
    - **Required**: False

6. **on_close**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is closed.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

### Example

```python
from typing import Callable, Optional
from websocket import WebSocketApp
from pieces_copilot_sdk import PiecesClient
from pieces_os_client import Asset
from pieces_copilot_sdk.websockets import AssetsIdentifiersWS

# Initialize the PiecesClient
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Define the callback functions
def on_asset_update(asset: Asset):
    print("Asset updated:", asset)

def on_asset_remove(asset: Asset):
    print("Asset removed:", asset)

def on_open_callback(ws: WebSocketApp):
    print("WebSocket connection opened")

def on_error_callback(ws: WebSocketApp, error: Exception):
    print("WebSocket error:", error)

def on_close_callback(ws: WebSocketApp):
    print("WebSocket connection closed")

# Create an instance of AssetsIdentifiersWS
assets_ws = AssetsIdentifiersWS(
    pieces_client=pieces_client,
    on_asset_update=on_asset_update,
    on_asset_remove=on_asset_remove,
    on_open_callback=on_open_callback,
    on_error=on_error_callback,
    on_close=on_close_callback
)

# Start the WebSocket connection
assets_ws.start()

```


## ConversationWS WebSocket

The `AssetsIdentifiersWS` class is used for managing WebSocket connections to monitor conversations updates and removals. 
**We already cache the assets by default**

### Args

1. **pieces_client**:
    - **Type**: `PiecesClient`
    - **Description**: An instance of the `PiecesClient` class that is used to interact with the Pieces API.
    - **Required**: True

2. **on_conversation_update**:
    - **Type**: `Optional[Callable[[Conversation], None]]`
    - **Description**: An optional function that gets called when a conversation update message is received.
    - **Parameter**: It takes one parameter, which is an instance of the [`Conversation`](https://docs.pieces.app/build/reference/python/models/Conversation) class representing the updated conversation.
    - **Return Value**: This function does not return any value.
    - **Required**: False

3. **on_conversation_remove**:
    - **Type**: `Optional[Callable[[Conversation], None]]`
    - **Description**: An optional function that gets called when a conversation removal message is received.
    - **Parameter**: It takes one parameter, which is an instance of the [`Conversation`](https://docs.pieces.app/build/reference/python/models/Conversation) class representing the removed conversation.
    - **Return Value**: This function does not return any value.
    - **Required**: False

4. **on_open_callback**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is opened.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

5. **on_error**:
    - **Type**: `Optional[Callable[[WebSocketApp, Exception], None]]`
    - **Description**: An optional function that gets called when an error occurs in the WebSocket connection.
    - **Parameters**:
        - `WebSocketApp`: The WebSocket application instance where the error occurred.
        - `Exception`: The exception that was raised.
    - **Return Value**: This function does not return any value.
    - **Required**: False

6. **on_close**:
    - **Type**: `Optional[Callable[[WebSocketApp], None]]`
    - **Description**: An optional function that gets called when the WebSocket connection is closed.
    - **Parameter**: It takes one parameter, which is of type `WebSocketApp`.
    - **Return Value**: This function does not return any value.
    - **Required**: False

### Example

```python
from typing import Callable, Optional
from websocket import WebSocketApp
from pieces_os_client import Conversation
from pieces_copilot_sdk import PiecesClient
from pieces_copilot_sdk.websockets import ConversationWS

# Initialize the PiecesClient
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

# Define the callback functions
def on_conversation_update(conversation: Conversation):
    print("Conversation updated:", conversation)

def on_conversation_remove(conversation: Conversation):
    print("Conversation removed:", conversation)

def on_open_callback(ws: WebSocketApp):
    print("WebSocket connection opened")

def on_error_callback(ws: WebSocketApp, error: Exception):
    print("WebSocket error:", error)

def on_close_callback(ws: WebSocketApp):
    print("WebSocket connection closed")

# Create an instance of ConversationWS
conversation_ws = ConversationWS(
    pieces_client=pieces_client,
    on_conversation_update=on_conversation_update,
    on_conversation_remove=on_conversation_remove,
    on_open_callback=on_open_callback,
    on_error=on_error_callback,
    on_close=on_close_callback
)

# Start the WebSocket connection
conversation_ws.start()
```


## BaseWebsocket

The BaseWebsocket is the main websocket that you can managet your websockets from

`.reconnect_all()`
`.start_all()`
`.close_all()`

**These methods should be used after initlizing the websockets**