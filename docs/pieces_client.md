# PiecesClient
## Snippets ([BasicAsset](./basic_asset.md))
### Creating a Snippet
- Create a snippet 
- returns: [BasicAsset](./basic_asset.md))

```python
from pieces_os_client import FragmentMetadata

content = "import pieces_os_client"
metadata = FragmentMetadata(
    ext="PY"
) # not essential

new_asset = client.create_asset(content, metadata)
print(f"Created asset with ID: {new_asset.id}")
```

### Fetching All Snippets
- Fetch all snippets
- returns: list of [BasicAsset](./basic_asset.md))

```python
assets = client.assets()
for asset in assets:
    print(f"Asset ID: {asset.id}")
```

### Fetching a Specific Asset
- Fetch specific snippet
- returns: [BasicAsset](./basic_asset.md))

```python
asset_id = "some-asset-id"
asset = client.asset(asset_id)
print(f"Fetched asset with ID: {asset.id}")
```

### [Copilot](./copilot.md)

```python
copilot = client.copilot
copilot.ask("How do I use the PiecesClient class?")
```

## Others
### Setting and Getting the Model Name
Note the model name is used in the copilot.ask method by default it is "GPT-3.5-turbo Chat Model"

```python
available_models = client.available_models_names # ["GPT-3.5-turbo Chat Model","GPT-4o Mini Chat Model",....]

print("Available models:", available_models)

print(f"Current model name: {client.model_name}")

client.model_name = "GPT-3.5-turbo Chat Model"
```

