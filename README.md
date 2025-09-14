# NotionHelper

![NotionHelper](https://github.com/janduplessis883/notionhelper/blob/master/images/helper_logo.png?raw=true)

`NotionHelper` is a Python library that provides a convenient interface for interacting with the Notion API, specifically designed to leverage the **Notion API Version 2025-09-03**. It simplifies common tasks such as managing databases, data sources, pages, and file uploads, allowing you to integrate Notion's powerful features into your applications with ease.

For help constructing the JSON for the properties, use the [Notion API - JSON Builder](https://notioinapiassistant.streamlit.app) Streamlit app.

## Features

-   **Synchronous Operations**: Uses `notion-client` and `requests` for straightforward API interactions.
-   **Type Safety**: Full type hints for all methods ensuring better development experience and IDE support.
-   **Error Handling**: Robust error handling for API calls and file operations.
-   **Database & Data Source Management**: Create, retrieve, query, and update Notion databases and their associated data sources.
-   **Page Operations**: Add new pages to data sources and append content to existing pages.
-   **File Handling**: Upload files and attach them to pages or page properties with built-in validation.
-   **Pandas Integration**: Convert Notion data source pages into a Pandas DataFrame for easy data manipulation.
-   **API Version 2025-09-03 Compliance**: Fully updated to support the latest Notion API changes, including the separation of databases and data sources.

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

### Retrieve a Database (Container)

With API version `2025-09-03`, `get_database` now returns the database object, which acts as a container for one or more data sources. To get the actual schema (properties), you need to retrieve a specific data source using `get_data_source`.

```python
database_id = "your_database_id" # ID of the database container
database_object = helper.get_database(database_id)
print(database_object)

# To get the schema of a specific data source within this database:
data_source_id = database_object["data_sources"][0]["id"] # Get the ID of the first data source
data_source_schema = helper.get_data_source(data_source_id)
print(data_source_schema)
```

### Create a New Page in a Data Source

With API version `2025-09-03`, pages are parented by `data_source_id`, not `database_id`. When creating a new page, ensure you use the `data_source_id` of the specific table you want to add the page to.

**Important Note on Property Definitions:** When defining properties for the *schema* of a database or data source, use an empty object `{}` for the property type (e.g., `"My Title Column": {"title": {}}`). However, when defining properties for a *new page* (as shown below), you provide the actual content using rich text arrays or other specific property value objects.

```python
data_source_id = "your_data_source_id" # The ID of the specific data source (table)

page_properties = {
    "Task Name": { # This must match a 'title' property in your data source schema
        "title": [
            {
                "text": {
                    "content": "New Task from NotionHelper"
                }
            }
        ]
    },
    "Status": { # This must match a 'select' property in your data source schema
        "select": {
            "name": "Not Started" # Must be one of the options defined in your data source
        }
    },
    "Due Date": { # This must match a 'date' property in your data source schema
        "date": {
            "start": "2025-12-31"
        }
    }
}
new_page = helper.new_page_to_data_source(data_source_id, page_properties)
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

### Get all pages from a Data Source as a Pandas DataFrame

```python
data_source_id = "your_data_source_id" # The ID of the specific data source (table)
df = helper.get_data_source_pages_as_dataframe(data_source_id)
print(df.head())
```

### Update a Data Source

This example demonstrates how to update the schema (properties/columns), title, icon, or other attributes of an existing data source.

```python
data_source_id = "your_data_source_id" # The ID of the data source to update

# Example 1: Rename a property and add a new one
update_payload_1 = {
    "properties": {
        "Old Property Name": { # Existing property name or ID
            "name": "New Property Name" # New name for the property
        },
        "New Text Property": { # Add a new rich text property
            "rich_text": {}
        }
    }
}
updated_data_source_1 = helper.update_data_source(data_source_id, properties=update_payload_1["properties"])
print(f"Updated data source (rename and add): {updated_data_source_1}")

# Example 2: Update data source title and remove a property
update_payload_2 = {
    "title": [
        {
            "type": "text",
            "text": {
                "content": "Updated Data Source Title"
            }
        }
    ],
    "properties": {
        "Property To Remove": None # Set to None to remove a property
    }
}
updated_data_source_2 = helper.update_data_source(data_source_id, title=update_payload_2["title"], properties=update_payload_2["properties"])
print(f"Updated data source (title and remove): {updated_data_source_2}")

# Example 3: Update a select property's options
update_payload_3 = {
    "properties": {
        "Status": { # Assuming 'Status' is an existing select property
            "select": {
                "options": [
                    {"name": "To Do", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Done", "color": "green"},
                    {"name": "Blocked", "color": "red"} # Add a new option
                ]
            }
        }
    }
}
updated_data_source_3 = helper.update_data_source(data_source_id, properties=update_payload_3["properties"])
print(f"Updated data source (select options): {updated_data_source_3}")
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

## Complete Function Reference

The `NotionHelper` class provides the following methods:

### Database & Data Source Operations
- **`get_database(database_id)`** - Retrieves the database object (container), which includes a list of its data sources.
- **`get_data_source(data_source_id)`** - Retrieves a specific data source, including its properties (schema).
- **`create_database(parent_page_id, database_title, initial_data_source_properties, initial_data_source_title=None)`** - Creates a new database with an initial data source.
- **`update_data_source(data_source_id, properties=None, title=None, icon=None, in_trash=None, parent=None)`** - Updates the attributes of a specified data source.
- **`notion_search_db(query="", filter_object_type="page")`** - Searches for pages or data sources in Notion.

### Page Operations
- **`new_page_to_data_source(data_source_id, page_properties)`** - Adds a new page to a Notion data source with the specified properties.
- **`append_page_body(page_id, blocks)`** - Appends blocks of text to the body of a Notion page.
- **`get_page(page_id)`** - Retrieves the JSON of the page properties and an array of blocks on a Notion page given its page_id.

### Data Retrieval & Conversion
- **`get_data_source_page_ids(data_source_id)`** - Returns the IDs of all pages in a given data source.
- **`get_data_source_pages_as_json(data_source_id, limit=None)`** - Returns a list of JSON objects representing all pages in the given data source, with all properties.
- **`get_data_source_pages_as_dataframe(data_source_id, limit=None, include_page_ids=True)`** - Retrieves all pages from a Notion data source and returns them as a Pandas DataFrame.

### File Operations
- **`upload_file(file_path)`** - Uploads a file to Notion and returns the file upload object
- **`attach_file_to_page(page_id, file_upload_id)`** - Attaches an uploaded file to a specific page
- **`embed_image_to_page(page_id, file_upload_id)`** - Embeds an uploaded image into a page
- **`attach_file_to_page_property(page_id, property_name, file_upload_id, file_name)`** - Attaches a file to a Files & Media property

### One-Step Convenience Methods
- **`one_step_image_embed(page_id, file_path)`** - Uploads and embeds an image in one operation
- **`one_step_file_to_page(page_id, file_path)`** - Uploads and attaches a file to a page in one operation
- **`one_step_file_to_page_property(page_id, property_name, file_path, file_name)`** - Uploads and attaches a file to a page property in one operation

## Requirements

- Python 3.10+
- pandas >= 2.3.1
- requests >= 2.32.4
- mimetype >= 0.1.5
