from typing import Optional, Dict, List, Any
from notion_client import Client
import pandas as pd
import os
import requests
import mimetypes

# NotionHelper can be used in conjunction with the Streamlit APP: (Notion API JSON)[https://notioinapiassistant.streamlit.app]


class NotionHelper:
    """
    A helper class to interact with the Notion API.

    Methods
    -------
    __init__():
        Initializes the NotionHelper instance and authenticates with the Notion API.

    authenticate():
        Authenticates with the Notion API using a token from environment variables.

    get_database(database_id):
        Fetches the schema of a Notion database given its database_id.

    notion_search_db(database_id, query=""):
        Searches for pages in a Notion database that contain the specified query in their title.

    notion_get_page(page_id):
        Returns the JSON of the page properties and an array of blocks on a Notion page given its page_id.

    create_database(parent_page_id, database_title, properties):
        Creates a new database in Notion under the specified parent page with the given title and properties.

    new_page_to_db(database_id, page_properties):
        Adds a new page to a Notion database with the specified properties.

    append_page_body(page_id, blocks):
        Appends blocks of text to the body of a Notion page.

    get_all_page_ids(database_id):
        Returns the IDs of all pages in a given Notion database.

    get_all_pages_as_json(database_id, limit=None):
        Returns a list of JSON objects representing all pages in the given database, with all properties.

    get_all_pages_as_dataframe(database_id, limit=None):
        Returns a Pandas DataFrame representing all pages in the given database, with selected properties.

    upload_file(file_path):
        Uploads a file to Notion and returns the file upload object.

    attach_file_to_page(page_id, file_upload_id):
        Attaches an uploaded file to a specific page.

    embed_image_to_page(page_id, file_upload_id):
        Embeds an uploaded image to a specific page.

    attach_file_to_page_property(page_id, property_name, file_upload_id, file_name):
        Attaches a file to a Files & Media property on a specific page.
    """

    def __init__(self, notion_token: str):
        """Initializes the NotionHelper instance and authenticates with the Notion API
        using the provided token."""
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """Retrieves the schema of a Notion database given its database_id.

        Parameters
        ----------
        database_id : str
            The unique identifier of the Notion database.

        Returns
        -------
        dict
            A dictionary representing the database schema.
        """
        try:
            response = self.notion.databases.retrieve(database_id=database_id)
            return response
        except Exception as e:
            raise Exception(f"Failed to retrieve database {database_id}: {str(e)}")

    def notion_search_db(
        self, database_id: str, query: str = ""
    ) -> None:
        """Searches for pages in a Notion database that contain the specified query in their title."""
        my_pages = self.notion.databases.query(
            database_id=database_id,
            filter={
                "property": "title",
                "rich_text": {"contains": query},
            },
        )

        page_title = my_pages["results"][0]["properties"]["Code / Notebook Description"]["title"][0]["plain_text"]
        page_url = my_pages["results"][0]["url"]

        page_list = my_pages["results"]
        count = 1
        for page in page_list:
            try:
                print(
                    count,
                    page["properties"]["Code / Notebook Description"]["title"][0]["plain_text"],
                )
            except IndexError:
                print("No results found.")

            print(page["url"])
            print()
            count += 1

        # pprint.pprint(page)

    def notion_get_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieves the JSON of the page properties and an array of blocks on a Notion page given its page_id."""

        # Retrieve the page and block data
        page = self.notion.pages.retrieve(page_id)
        blocks = self.notion.blocks.children.list(page_id)

        # Extract all properties as a JSON object
        properties = page.get("properties", {})
        content = [block for block in blocks["results"]]

        # Print the full JSON of the properties
        print(properties)

        # Return the properties JSON and blocks content
        return {"properties": properties, "content": content}

    def create_database(self, parent_page_id: str, database_title: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new database in Notion.

        This method creates a new database under a specified parent page with the provided title and property definitions.

        Parameters:
            parent_page_id (str): The unique identifier of the parent page.
            database_title (str): The title for the new database.
            properties (dict): A dictionary defining the property schema for the database.

        Returns:
            dict: The JSON response from the Notion API containing details about the created database.
        """

        # Define the properties for the database
        new_database = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": database_title}}],
            "properties": properties,
        }

        response = self.notion.databases.create(**new_database)
        return response

    def new_page_to_db(self, database_id: str, page_properties: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a new page to a Notion database."""

        new_page = {
            "parent": {"database_id": database_id},
            "properties": page_properties,
        }

        response = self.notion.pages.create(**new_page)
        return response

    def append_page_body(self, page_id: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Appends blocks of text to the body of a Notion page."""

        new_blocks = {"children": blocks}

        response = self.notion.blocks.children.append(block_id=page_id, **new_blocks)
        return response

    def get_all_page_ids(self, database_id: str) -> List[str]:
        """Returns the IDs of all pages in a given database."""

        my_pages = self.notion.databases.query(database_id=database_id)
        page_ids = [page["id"] for page in my_pages["results"]]
        return page_ids

    def get_all_pages_as_json(self, database_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns a list of JSON objects representing all pages in the given database, with all properties.
        You can specify the number of entries to be loaded using the `limit` parameter.
        """

        # Use pagination to remove any limits on number of entries, optionally limited by `limit` argument
        pages_json = []
        has_more = True
        start_cursor = None
        count = 0

        while has_more:
            my_pages = self.notion.databases.query(
                **{
                    "database_id": database_id,
                    "start_cursor": start_cursor,
                }
            )
            pages_json.extend([page["properties"] for page in my_pages["results"]])
            has_more = my_pages.get("has_more", False)
            start_cursor = my_pages.get("next_cursor", None)
            count += len(my_pages["results"])

            if limit is not None and count >= limit:
                pages_json = pages_json[:limit]
                break

        return pages_json

    def get_all_pages_as_dataframe(self, database_id: str, limit: Optional[int] = None, include_page_ids: bool = True) -> pd.DataFrame:
        """Retrieves all pages from a Notion database and returns them as a Pandas DataFrame.

        This method collects pages from the specified Notion database, optionally including the page IDs,
        and extracts a predefined set of allowed properties from each page to form a structured DataFrame.
        Numeric values are formatted to avoid scientific notation.

        Parameters:
            database_id (str): The identifier of the Notion database.
            limit (int, optional): Maximum number of page entries to include. If None, all pages are retrieved.
            include_page_ids (bool, optional): If True, includes an additional column 'notion_page_id' in the DataFrame.
                                               Defaults to True.

        Returns:
            pandas.DataFrame: A DataFrame where each row represents a page with columns corresponding to page properties.
                              If include_page_ids is True, an additional column 'notion_page_id' is included.
        """
        # Retrieve pages with or without page IDs based on the flag
        if include_page_ids:
            pages_json = []
            has_more = True
            start_cursor = None
            count = 0
            # Retrieve pages with pagination including the page ID in properties
            while has_more:
                my_pages = self.notion.databases.query(
                    database_id=database_id,
                    start_cursor=start_cursor,
                )
                for page in my_pages["results"]:
                    props = page["properties"]
                    props["notion_page_id"] = page.get("id", "")
                    pages_json.append(props)
                has_more = my_pages.get("has_more", False)
                start_cursor = my_pages.get("next_cursor", None)
                count += len(my_pages["results"])
                if limit is not None and count >= limit:
                    pages_json = pages_json[:limit]
                    break
        else:
            pages_json = self.get_all_pages_as_json(database_id, limit=limit)

        data = []
        # Define the list of allowed property types that we want to extract
        allowed_properties = [
            "title",
            "status",
            "number",
            "date",
            "url",
            "checkbox",
            "rich_text",
            "email",
            "select",
            "people",
            "phone_number",
            "multi_select",
            "created_time",
            "created_by",
            "rollup",
            "relation",
            "last_edited_by",
            "last_edited_time",
            "formula",
            "file",
        ]
        if include_page_ids:
            allowed_properties.append("notion_page_id")

        for page in pages_json:
            row = {}
            for key, value in page.items():
                if key == "notion_page_id":
                    row[key] = value
                    continue
                property_type = value.get("type", "")
                if property_type in allowed_properties:
                    if property_type == "title":
                        row[key] = value.get("title", [{}])[0].get("plain_text", "")
                    elif property_type == "status":
                        row[key] = value.get("status", {}).get("name", "")
                    elif property_type == "number":
                        number_value = value.get("number", None)
                        row[key] = float(number_value) if isinstance(number_value, (int, float)) else None
                    elif property_type == "date":
                        date_field = value.get("date", {})
                        row[key] = date_field.get("start", "") if date_field else ""
                    elif property_type == "url":
                        row[key] = value.get("url", "")
                    elif property_type == "checkbox":
                        row[key] = value.get("checkbox", False)
                    elif property_type == "rich_text":
                        rich_text_field = value.get("rich_text", [])
                        row[key] = rich_text_field[0].get("plain_text", "") if rich_text_field else ""
                    elif property_type == "email":
                        row[key] = value.get("email", "")
                    elif property_type == "select":
                        select_field = value.get("select", {})
                        row[key] = select_field.get("name", "") if select_field else ""
                    elif property_type == "people":
                        people_list = value.get("people", [])
                        if people_list:
                            person = people_list[0]
                            row[key] = {"name": person.get("name", ""), "email": person.get("person", {}).get("email", "")}
                    elif property_type == "phone_number":
                        row[key] = value.get("phone_number", "")
                    elif property_type == "multi_select":
                        multi_select_field = value.get("multi_select", [])
                        row[key] = [item.get("name", "") for item in multi_select_field]
                    elif property_type == "created_time":
                        row[key] = value.get("created_time", "")
                    elif property_type == "created_by":
                        created_by = value.get("created_by", {})
                        row[key] = created_by.get("name", "")
                    elif property_type == "rollup":
                        rollup_field = value.get("rollup", {}).get("array", [])
                        row[key] = [item.get("date", {}).get("start", "") for item in rollup_field]
                    elif property_type == "relation":
                        relation_list = value.get("relation", [])
                        row[key] = [relation.get("id", "") for relation in relation_list]
                    elif property_type == "last_edited_by":
                        last_edited_by = value.get("last_edited_by", {})
                        row[key] = last_edited_by.get("name", "")
                    elif property_type == "last_edited_time":
                        row[key] = value.get("last_edited_time", "")
                    elif property_type == "formula":
                        formula_value = value.get("formula", {})
                        row[key] = formula_value.get(formula_value.get("type", ""), "")
                    elif property_type == "file":
                        files = value.get("files", [])
                        row[key] = [file.get("name", "") for file in files]
            data.append(row)

        df = pd.DataFrame(data)
        pd.options.display.float_format = "{:.3f}".format
        return df

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Uploads a file to Notion and returns the file upload object."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            # Step 1: Create a File Upload object
            create_upload_url = "https://api.notion.com/v1/file_uploads"
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }
            response = requests.post(create_upload_url, headers=headers, json={})
            response.raise_for_status()
            upload_data = response.json()
            upload_url = upload_data["upload_url"]

            # Step 2: Upload file contents
            with open(file_path, "rb") as f:
                upload_headers = {
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                }
                files = {'file': (os.path.basename(file_path), f, mimetypes.guess_type(file_path)[0] or 'application/octet-stream')}
                upload_response = requests.post(upload_url, headers=upload_headers, files=files)
                upload_response.raise_for_status()

            return upload_response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to upload file {file_path}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error uploading file {file_path}: {str(e)}")

    def attach_file_to_page(self, page_id: str, file_upload_id: str) -> Dict[str, Any]:
        """Attaches an uploaded file to a specific page."""
        attach_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "children": [
                {
                    "type": "file",
                    "file": {
                        "type": "file_upload",
                        "file_upload": {
                            "id": file_upload_id
                        }
                    }
                }
            ]
        }
        response = requests.patch(attach_url, headers=headers, json=data)
        return response.json()

    def embed_image_to_page(self, page_id: str, file_upload_id: str) -> Dict[str, Any]:
        """Embeds an uploaded image to a specific page."""
        attach_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "children": [
                {
                    "type": "image",
                    "image": {
                        "type": "file_upload",
                        "file_upload": {
                            "id": file_upload_id
                        }
                    }
                }
            ]
        }
        response = requests.patch(attach_url, headers=headers, json=data)
        return response.json()

    def attach_file_to_page_property(
        self, page_id: str, property_name: str, file_upload_id: str, file_name: str
    ) -> Dict[str, Any]:
        """Attaches a file to a Files & Media property on a specific page."""
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "properties": {
                property_name: {
                    "files": [
                        {
                            "type": "file_upload",
                            "file_upload": {"id": file_upload_id},
                            "name": file_name,
                        }
                    ]
                }
            }
        }
        response = requests.patch(update_url, headers=headers, json=data)
        return response.json()

    def one_step_image_embed(self, page_id: str, file_path: str) -> Dict[str, Any]:
        """Uploads an image and embeds it in a Notion page in one step."""

        # Upload the file
        file_upload = self.upload_file(file_path)
        file_upload_id = file_upload["id"]

        # Embed the image in the page
        return self.embed_image_to_page(page_id, file_upload_id)

    def one_step_file_to_page(self, page_id: str, file_path: str) -> Dict[str, Any]:
        """Uploads a file and attaches it to a Notion page in one step."""

        # Upload the file
        file_upload = self.upload_file(file_path)
        file_upload_id = file_upload["id"]

        # Attach the file to the page
        return self.attach_file_to_page(page_id, file_upload_id)

    def one_step_file_to_page_property(self, page_id: str, property_name: str, file_path: str, file_name: str) -> Dict[str, Any]:
        """Uploads a file and attaches it to a Notion page property in one step."""

        # Upload the file
        file_upload = self.upload_file(file_path)
        file_upload_id = file_upload["id"]

        # Attach the file to the page property
        return self.attach_file_to_page_property(page_id, property_name, file_upload_id, file_name)

    def info(self) -> Optional[Any]:
        """Displays comprehensive library information in a Jupyter notebook.

        Shows:
        - Library name and description
        - Complete list of all available methods with descriptions
        - Version information
        - Optional logo display (if available)

        Returns:
            IPython.display.HTML: An HTML display object or None if IPython is not available.
        """
        try:
            from IPython.display import HTML
            import base64
            import inspect

            # Get logo image data
            logo_path = os.path.join(os.path.dirname(__file__), '../images/helper_logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as image_file:
                    encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                encoded_logo = ""

            # Get all methods and their docstrings
            methods = []
            for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
                if not name.startswith('_'):
                    doc = inspect.getdoc(method) or "No description available"
                    methods.append(f"<li><code>{name}()</code>: {doc.splitlines()[0]}</li>")

            # Create HTML content
            html_content = f"""
            <div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; max-width: 800px; margin: 0 auto; color: #1e293b;">
                <h1 style="color: #1e293b;">NotionHelper Library</h1>
                {f'<img src="data:image/png;base64,{encoded_logo}" style="max-width: 200px; margin: 20px 0; display: block;">' if encoded_logo else ''}
                <p style="font-size: 1.1rem;">A Python helper class for interacting with the Notion API.</p>
                <h3 style="color: #1e293b;">All Available Methods:</h3>
                <ul style="list-style-type: none; padding-left: 0;">
                    {''.join(methods)}
                </ul>
                <h3 style="color: #1e293b;">Features:</h3>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li style="margin-bottom: 8px;">Database querying and manipulation</li>
                    <li style="margin-bottom: 8px;">Page creation and editing</li>
                    <li style="margin-bottom: 8px;">File uploads and attachments</li>
                    <li style="margin-bottom: 8px;">Data conversion to Pandas DataFrames</li>
                </ul>
                <p style="font-size: 0.9rem; color: #64748b;">Version: {getattr(self, '__version__', '1.0.0')}</p>
            </div>
            """
            return HTML(html_content)
        except ImportError:
            print("IPython is required for this functionality. Please install it with: pip install ipython")
            return None
