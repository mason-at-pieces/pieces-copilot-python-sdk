# BasicAsset

## Overview

The `BasicAsset` class provides a way to manage assets with various properties and methods. This document outlines the properties and methods available in the `BasicAsset` class.

## Initialization

```python
asset = BasicAsset("Your id goes here")
```

**Raises**: `ValueError` if the provided ID is invalid.

## Properties

### `id`

Returns the asset ID.

### `raw_content`

Edit the original format of the asset.

**Args**:
- `data`: The new data to be set.

**Raises**:
- `NotImplementedError`: If the asset is an image.

### `is_image`

Check if the asset is an image.

**Returns**: `bool` - `True` if the asset is an image, otherwise `False`.

### `classification`

Get the specific classification of the asset (e.g., `py`).

**Returns**: The classification value of the asset, or `None` if not available.

### `classification` setter

Reclassify an asset


### `name` setter

Edit the name of the asset.

- `name`: The new name to be set for the asset.


### `description`

Retrieve the description of the asset.

**Returns**: The description text of the asset, or `None` if not available.


### `annotations`

Get all annotations of the asset.

**Returns**: Optional[[Annotations](https://docs.pieces.app/build/reference/python/models/Annotations)] - The annotations if available, otherwise `None`.

## Methods

### `delete()`

Delete the asset.

### `create()`

Create a new asset.

**Args**:
- `raw_content` (str): The raw content of the asset.
- `metadata` (Optional[FragmentMetadata]): The metadata of the asset.

**Returns**: `str` - The ID of the created asset.


## Example Usage

```python
from pieces_copilot_sdk import PiecesClient
from pieces_copilot_sdk.basic_identifier import BasicAsset
from pieces_os_client import ClassificationSpecificEnum

# Replace 'your_base_url' with your actual base URL
pieces_client = PiecesClient(config={'baseUrl': 'your_base_url'})

asset = pieces_client.assets()[0]

# Get the asset ID
asset_id = asset.id
print(f"Asset ID: {asset_id}")

# Check if the asset is an image
if asset.is_image:
    print("The asset is an image.")
else:
    print("The asset is not an image.")

# Get and set the asset name
print(f"Current Asset Name: {asset.name}")
asset.name = "Updated Asset Name"
print(f"Updated Asset Name: {asset.name}")

# Retrieve and modify the asset content
content = asset.raw_content
print(f"Original Content: {content}")
asset.raw_content = content + "\n# This is a comment"
print(f"Updated Content: {asset.raw_content}")

# Get the asset classification
classification = asset.classification.value if asset.classification else "None"
print(f"Asset Classification: {classification}")

asset.classification = ClassificationSpecificEnum.SH # Reclassify to shell
print(f"New Classification: {classification}")

# Get the asset description
description = asset.description if asset.description else "No description available."
print(f"Asset Description: {description}")

# Get the asset annotations
annotations = asset.annotations if asset.annotations else "No annotations available."
print(f"Asset Annotations: {annotations}")

# Delete the asset
asset.delete()
print("Asset deleted.")

# Create a new asset
new_asset_id = BasicAsset.create("New Asset content")
print(f"New Asset ID: {new_asset_id}")
pieces_client.close()
```
