# Caching 

We cache the assets and the conversations for you to use and avoid sending too much requests to Pieces OS (Increasing preformance)

**For Caching to work properly you need to connect its respective websocket**

## AssetSnapshot
### Getting all assets saved

```python
from typing import Callable, Optional
from websocket import WebSocketApp
from pieces_copilot_sdk.websockets import AssetsIdentifiersWS
from pieces_copilot_sdk.streamed_identifiers import AssetSnapshot
from pieces_copilot_sdk import PiecesClient
import time

pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

assets_ws = AssetsIdentifiersWS(pieces_client=pieces_client).start() # Need to connect to the websocket
time.sleep(4) # Wait until all assets is cached 
list(AssetSnapshot.identifiers_snapshot.values()) # return list of Asset
list(AssetSnapshot.identifiers_snapshot.keys()) # return list of str (assets ids)
```
### Using The assets wrapper
The asset wrapper provide many useful functionailty 
	- Edit an asset
	- Delete an asset
	- Creating an asset
	- Get asset raw content
	- Get classification (eg: python)
	- Getting asset description

```python
asset_wrapper = AssetSnapshot(asset_id = "ASSET ID GOES HERE") # Here it should be one from the AssetSnapshot.identifiers_snapshot.items()
classification = asset_wrapper.original_classification_specific()
raw_content = asset_wrapper.get_asset_raw() # The snippet content
asset_wrapper.edit_asset_original_format(data=f"{raw_content} \n My new content goes here") # Here it will edit the asset content
classification = asset_wrapper.original_classification_specific().value # Classification eg. python
description = asset_wrapper.get_description().text
asset_wrapper.delete()
name = asset_wrapper.name
new_asset_id = AssetSnapshot.create("requests.post('URL')",FragmentMetadata(ext="py"))
```


## ConversationSnapshot
```python
from typing import Callable, Optional
from websocket import WebSocketApp
from pieces_copilot_sdk.websockets import ConversationWS
from pieces_copilot_sdk.streamed_identifiers import ConversationSnapshot
from pieces_copilot_sdk import PiecesClient
import time

pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

conversation_ws = ConversationWS(pieces_client=pieces_client).start() # Need to connect to the websocket
time.sleep(4) # Wait until all assets is cached 
(ConversationSnapshot.identifiers_snapshot.values()) # return list of Conversations
list(ConversationSnapshot.identifiers_snapshot.keys()) # return list of str (conversations ids)
```
