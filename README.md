# NotionHelper

![NotionHelper](https://github.com/janduplessis883/notionhelper/blob/master/images/helper_logo.png?raw=true)

`NotionHelper` is a Python library that provides a convenient interface for interacting with the Notion API. It simplifies common tasks such as managing databases, pages, and file uploads, allowing you to integrate Notion's powerful features into your applications with ease.

For help constructing the JSON for the properties, use the [Notion API - JSON Builder](https://notioinapiassistant.streamlit.app) Streamlit app.

## Features

-   **Synchronous Operations**: Uses `notion-client` and `requests` for straightforward API interactions.
-   **Type Safety**: Full type hints for all methods ensuring better development experience and IDE support.
-   **Error Handling**: Robust error handling for API calls and file operations.
-   **Database Management**: Create, query, and retrieve Notion databases.
-   **Page Operations**: Add new pages to databases and append content to existing pages.
-   **File Handling**: Upload files and attach them to pages or page properties with built-in validation.
-   **Pandas Integration**: Convert Notion database pages into a Pandas DataFrame for easy data manipulation.

## Installation

To install `NotionHelper`, you can use `pip`:

```bash
pip install notionhelper
```

This will also install all the necessary dependencies, including `notion-client`, `pandas`, and `requests`.

## Authentication

To use the Notion API, you need to create an integration and obtain an integration token.

1.  **Create an Integration**: Go to [My Integrations](https://www.notion.so/my-integrations) and create a new integration.
2.  **Get the Token**: Copy the "Internal Integration Token".
3.  **Share with a Page/Database**: For your integration to access a page or database, you must share it with your integration from the "Share" menu in Notion.

It is recommended to store your Notion token as an environment variable for security.

```bash
export NOTION_TOKEN="your_secret_token"
```

## Usage

Here is an example of how to use the library:

```python
import os
from notionhelper import NotionHelper
```

### Initialize the NotionHelper class

```python
notion_token = os.getenv("NOTION_TOKEN")

helper = NotionHelper(notion_token)
```

### Retrieve a Database

```python
database_id = "your_database_id"
database_schema = helper.get_database(database_id)
print(database_schema)
```

### Create a New Page in a Database

```python
page_properties = {
    "Name": {
        "title": [
            {
                "text": {
                    "content": "New Page from NotionHelper"
                }
            }
        ]
    }
}
new_page = helper.new_page_to_db(database_id, page_properties)
print(new_page)
```

### Append Content to the New Page

```python
blocks = [
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "Hello from NotionHelper!"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "This content was appended synchronously."
                    }
                }
            ]
        }
    }
]
helper.append_page_body(page_id, blocks)
print(f"Successfully appended content to page ID: {page_id}")
```

### Get all pages as a Pandas DataFrame

```python
  df = helper.get_all_pages_as_dataframe(database_id)
  print(df.head())
```

### Upload a File and Attach to a Page

```python
try:
    file_path = "path/to/your/file.pdf"  # Replace with your file path
    upload_response = helper.upload_file(file_path)
    file_upload_id = upload_response["id"]
    # Replace with your page_id
    page_id = "your_page_id"
    attach_response = helper.attach_file_to_page(page_id, file_upload_id)
    print(f"Successfully uploaded and attached file: {attach_response}")
except Exception as e:
    print(f"Error uploading file: {e}")
```

### Simplified File Operations

NotionHelper provides convenient one-step methods that combine file upload and attachment operations:

#### one_step_image_embed()
Uploads an image and embeds it in a Notion page in a single call, combining what would normally require:
1. Uploading the file
2. Embedding it in the page

```python
page_id = "your_page_id"
image_path = "path/to/image.png"
response = helper.one_step_image_embed(page_id, image_path)
print(f"Successfully embedded image: {response}")
```

#### one_step_file_to_page()
Uploads a file and attaches it to a Notion page in one step, combining:
1. Uploading the file
2. Attaching it to the page

```python
page_id = "your_page_id"
file_path = "path/to/document.pdf"
response = helper.one_step_file_to_page(page_id, file_path)
print(f"Successfully attached file: {response}")
```

#### one_step_file_to_page_property()
Uploads a file and attaches it to a specific Files & Media property on a page, combining:
1. Uploading the file
2. Attaching it to the page property

```python
page_id = "your_page_id"
property_name = "Files"  # Name of your Files & Media property
file_path = "path/to/document.pdf"
file_name = "Custom Display Name.pdf"  # Optional display name
response = helper.one_step_file_to_page_property(page_id, property_name, file_path, file_name)
print(f"Successfully attached file to property: {response}")
```

These methods handle all the intermediate steps automatically, making file operations with Notion much simpler.

## Code Quality

The NotionHelper library includes several quality improvements:

- **Type Hints**: All methods include comprehensive type annotations for better IDE support and code clarity
- **Error Handling**: Built-in validation and exception handling for common failure scenarios
- **Clean Imports**: Explicit imports with `__all__` declaration for better namespace management
- **Production Ready**: Removed debug output and implemented proper error reporting

## Requirements

- Python 3.10+
- notion-client >= 2.4.0
- pandas >= 2.3.1  
- requests >= 2.32.4
- mimetype >= 0.1.5
