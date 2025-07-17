# NotionHelper

![NotionHelper]()

`NotionHelper` is a Python library that provides a convenient interface for interacting with the Notion API. It simplifies common tasks such as managing databases, pages, and file uploads, allowing you to integrate Notion's powerful features into your applications with ease.

For help constructing the JSON for the properties, use the [Notion API - JSON Builder](https://notioinapiassistant.streamlit.app) Streamlit app.

![JSON Builder](https://github.com/janduplessis883/notionhelper/blob/master/images/json_builder.png.png?raw=true)

## Features

-   **Synchronous Operations**: Uses `notion-client` and `requests` for straightforward API interactions.
-   **Database Management**: Create, query, and retrieve Notion databases.
-   **Page Operations**: Add new pages to databases and append content to existing pages.
-   **File Handling**: Upload files and attach them to pages or page properties.
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

def main():
    # Initialize the client with your Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        raise ValueError("NOTION_TOKEN environment variable not set.")

    helper = NotionHelper(notion_token)

    # --- Example: Retrieve a Database ---
    database_id = "your_database_id"
    database_schema = helper.get_database(database_id)
    print("Successfully retrieved database schema:")
    # print(database_schema)


    # --- Example: Create a New Page in a Database ---
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
    print(f"Successfully created a new page with ID: {new_page['id']}")
    page_id = new_page['id']

    # --- Example: Append Content to the New Page ---
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


    # --- Example: Get all pages as a Pandas DataFrame ---
    df = helper.get_all_pages_as_dataframe(database_id)
    print("Successfully retrieved pages as a DataFrame:")
    print(df.head())


if __name__ == "__main__":
    main()
