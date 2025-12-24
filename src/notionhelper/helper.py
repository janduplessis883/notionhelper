from typing import Optional, Dict, List, Any
import pandas as pd
import os
import requests
import mimetypes
import json
from datetime import datetime
import numpy as np


# NotionHelper can be used in conjunction with the Streamlit APP: (Notion API JSON)[https://notioinapiassistant.streamlit.app]


class NotionHelper:
    """
    A helper class to interact with the Notion API.

    Methods
    -------
    __init__():
        Initializes the NotionHelper instance and authenticates with the Notion API.

    _make_request(method, url, payload=None, api_version="2025-09-03"):
        Internal helper to make authenticated requests to the Notion API.

    get_database(database_id):
        Retrieves the database object, which contains a list of data sources.

    get_data_source(data_source_id):
        Retrieves a specific data source, including its properties (schema).

    notion_search_db(query="", filter_object_type="page"):
        Searches for pages or data sources in Notion.

    notion_get_page(page_id):
        Returns the JSON of the page properties and an array of blocks on a Notion page given its page_id.

    create_database(parent_page_id, database_title, initial_data_source_properties, initial_data_source_title=None):
        Creates a new database in Notion with an initial data source.

    new_page_to_db(data_source_id, page_properties):
        Adds a new page to a Notion data source with the specified properties.

    append_page_body(page_id, blocks):
        Appends blocks of text to the body of a Notion page.

    get_all_page_ids(data_source_id):
        Returns the IDs of all pages in a given Notion data source.

    get_all_pages_as_json(data_source_id, limit=None):
        Returns a list of JSON objects representing all pages in the given data source, with all properties.

    get_all_pages_as_dataframe(data_source_id, limit=None):
        Returns a Pandas DataFrame representing all pages in the given data source, with selected properties.

    upload_file(file_path):
        Uploads a file to Notion and returns the file upload object.

    attach_file_to_page(page_id, file_upload_id):
        Attaches an uploaded file to a specific page.

    embed_image_to_page(page_id, file_upload_id):
        Embeds an uploaded image to a specific page.

    attach_file_to_page_property(page_id, property_name, file_upload_id, file_name):
        Attaches a file to a Files & Media property on a specific page.

    update_data_source(data_source_id, properties=None, title=None, icon=None, in_trash=None, parent=None):
        Updates the attributes of a specified data source.
    """

    def __init__(self, notion_token: str):
        """Initializes the NotionHelper instance with the provided token."""
        self.notion_token = notion_token

    def _make_request(self, method: str, url: str, payload: Optional[Dict[str, Any]] = None, api_version: str = "2025-09-03") -> Dict[str, Any]:
        """
        Internal helper to make authenticated requests to the Notion API.
        Handles headers, JSON serialization, and error checking.
        """
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": api_version,
        }
        response = None  # Initialize response to None
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, data=json.dumps(payload))
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, data=json.dumps(payload))
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ NOTION API ERROR DETAILS: {response.text}")
            print(f"HTTP error occurred: {http_err}")
            if response is not None:  # Check if response was assigned before accessing .text
                print(f"Response Body: {response.text}")
            raise
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """Retrieves the schema of a Notion database given its database_id.
        With API version 2025-09-03, this now returns the database object
        which contains a list of data sources. To get the actual schema (properties),
        you need to retrieve a specific data source.

        Parameters
        ----------
        database_id : str
            The unique identifier of the Notion database.

        Returns
        -------
        dict
            A dictionary representing the database object, including its data sources.
        """
        url = f"https://api.notion.com/v1/databases/{database_id}"
        return self._make_request("GET", url)

    def get_data_source(self, data_source_id: str) -> Dict[str, Any]:
        """Retrieves a specific data source given its data_source_id.
        This is used to get the schema (properties) of a data source.

        Parameters
        ----------
        data_source_id : str
            The unique identifier of the Notion data source.

        Returns
        -------
        dict
            A dictionary representing the data source object, including its properties.
        """
        url = f"https://api.notion.com/v1/data_sources/{data_source_id}"
        return self._make_request("GET", url)

    def notion_search_db(self, query: str = "", filter_object_type: str = "page") -> List[Dict[str, Any]]:
        """Searches for pages or data sources in Notion.

        Parameters
        ----------
        query : str
            The search query.
        filter_object_type : str
            The type of object to filter by. Can be "page" or "data_source".

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries representing the search results.
        """
        if filter_object_type not in ["page", "data_source"]:
            raise ValueError("filter_object_type must be 'page' or 'data_source'")

        url = "https://api.notion.com/v1/search"
        payload = {
            "query": query,
            "filter": {
                "value": filter_object_type,
                "property": "object"
            }
        }
        response = self._make_request("POST", url, payload)
        return response.get("results", [])

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieves the JSON of the page properties and an array of blocks on a Notion page given its page_id."""

        # Retrieve the page properties
        page_url = f"https://api.notion.com/v1/pages/{page_id}"
        page = self._make_request("GET", page_url)

        # Retrieve the block data (content)
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        blocks = self._make_request("GET", blocks_url)

        # Extract all properties as a JSON object
        properties = page.get("properties", {})
        content = [block for block in blocks["results"]]

        # Print the full JSON of the properties
        print(properties)

        # Return the properties JSON and blocks content
        return {"properties": properties, "content": content}

    def create_database(self, parent_page_id: str, database_title: str, initial_data_source_properties: Dict[str, Any], initial_data_source_title: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new database in Notion with an initial data source.

        This method creates a new database under a specified parent page with the provided title
        and defines the schema for its initial data source.

        Parameters:
            parent_page_id (str): The unique identifier of the parent page.
            database_title (str): The title for the new database container.
            initial_data_source_properties (dict): A dictionary defining the property schema for the initial data source.
            initial_data_source_title (str, optional): The title for the initial data source. Defaults to database_title.

        Returns:
            dict: The JSON response from the Notion API containing details about the created database and its initial data source.

        Example JSON p[ayload:
            properties = {
                "Mandatory Title": {"title": {}},
                "Description": {"rich_text": {}}
            }
        """
        if initial_data_source_title is None:
            initial_data_source_title = database_title

        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": database_title}}],
            "initial_data_source": {
                "title": [{"type": "text", "text": {"content": initial_data_source_title}}],
                "properties": initial_data_source_properties,
            },
        }
        url = "https://api.notion.com/v1/databases"
        return self._make_request("POST", url, payload)

    def update_data_source(self, data_source_id: str, properties: Optional[Dict[str, Any]] = None, title: Optional[List[Dict[str, Any]]] = None, icon: Optional[Dict[str, Any]] = None, in_trash: Optional[bool] = None, parent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Updates the attributes of a specified data source.

        Parameters:
            data_source_id (str): The unique identifier of the Notion data source to update.
            properties (dict, optional): A dictionary defining the property schema updates for the data source.
                                         Use `{"Property Name": null}` to remove a property.
                                         Use `{"Old Name": {"name": "New Name"}}` to rename.
                                         Use `{"New Property": {"type": "rich_text", "rich_text": {}}}` to add.
            title (list, optional): The new title for the data source.
            icon (dict, optional): The new icon for the data source.
            in_trash (bool, optional): Whether to move the data source to or from the trash.
            parent (dict, optional): The new parent database if moving the data source.

        Returns:
            dict: The JSON response from the Notion API containing details about the updated data source.
        """
        payload = {}
        if properties is not None:
            payload["properties"] = properties
        if title is not None:
            payload["title"] = title
        if icon is not None:
            payload["icon"] = icon
        if in_trash is not None:
            payload["in_trash"] = in_trash
        if parent is not None:
            payload["parent"] = parent

        if not payload:
            raise ValueError("No update parameters provided. Please provide at least one of: properties, title, icon, in_trash, parent.")

        url = f"https://api.notion.com/v1/data_sources/{data_source_id}"
        return self._make_request("PATCH", url, payload)

    def new_page_to_data_source(self, data_source_id: str, page_properties: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a new page to a Notion data source.
        With API version 2025-09-03, pages are parented by data_source_id, not database_id.

        Parameters:
            data_source_id (str): The unique identifier of the Notion data source.
            page_properties (dict): A dictionary defining the properties for the new page.

        Returns:
            dict: The JSON response from the Notion API containing details about the created page.
        """
        payload = {
            "parent": {"data_source_id": data_source_id},
            "properties": page_properties,
        }
        url = "https://api.notion.com/v1/pages"
        return self._make_request("POST", url, payload)

    def append_page_body(self, page_id: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Appends blocks of text to the body of a Notion page."""
        payload = {"children": blocks}
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        return self._make_request("PATCH", url, payload)

    def get_data_source_page_ids(self, data_source_id: str) -> List[str]:
        """Returns the IDs of all pages in a given data source.
        With API version 2025-09-03, this queries a data source, not a database.
        """
        url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
        pages_json = []
        has_more = True
        start_cursor = None

        while has_more:
            payload = {}
            if start_cursor:
                payload["start_cursor"] = start_cursor

            response = self._make_request("POST", url, payload)
            pages_json.extend(response["results"])
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor", None)

        page_ids = [page["id"] for page in pages_json]
        return page_ids

    def get_data_source_pages_as_json(self, data_source_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns a list of JSON objects representing all pages in the given data source, with all properties.
        You can specify the number of entries to be loaded using the `limit` parameter.
        With API version 2025-09-03, this queries a data source, not a database.
        """
        url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
        pages_json = []
        has_more = True
        start_cursor = None
        count = 0

        while has_more:
            payload = {}
            if start_cursor:
                payload["start_cursor"] = start_cursor
            if limit is not None:
                payload["page_size"] = min(100, limit - count) # Max page size is 100

            response = self._make_request("POST", url, payload)
            pages_json.extend([page["properties"] for page in response["results"]])
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor", None)
            count += len(response["results"])

            if limit is not None and count >= limit:
                pages_json = pages_json[:limit]
                break

        return pages_json

    def get_data_source_pages_as_dataframe(self, data_source_id: str, limit: Optional[int] = None, include_page_ids: bool = True) -> pd.DataFrame:
        """Retrieves all pages from a Notion data source and returns them as a Pandas DataFrame.

        This method collects pages from the specified Notion data source, optionally including the page IDs,
        and extracts a predefined set of allowed properties from each page to form a structured DataFrame.
        Numeric values are formatted to avoid scientific notation.

        Parameters:
            data_source_id (str): The identifier of the Notion data source.
            limit (int, optional): Maximum number of page entries to include. If None, all pages are retrieved.
            include_page_ids (bool, optional): If True, includes an additional column 'notion_page_id' in the DataFrame.
                                               Defaults to True.

        Returns:
            pandas.DataFrame: A DataFrame where each row represents a page with columns corresponding to page properties.
                              If include_page_ids is True, an additional column 'notion_page_id' is included.
        """
        # Retrieve pages with or without page IDs based on the flag
        all_pages_data = []
        has_more = True
        start_cursor = None
        count = 0

        url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"

        while has_more:
            payload = {}
            if start_cursor:
                payload["start_cursor"] = start_cursor
            if limit is not None:
                payload["page_size"] = min(100, limit - count) # Max page size is 100

            response = self._make_request("POST", url, payload)
            for page in response["results"]:
                props = page["properties"]
                if include_page_ids:
                    props["notion_page_id"] = page.get("id", "")
                all_pages_data.append(props)

            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor", None)
            count += len(response["results"])

            if limit is not None and count >= limit:
                all_pages_data = all_pages_data[:limit]
                break

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

        for page in all_pages_data:
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
                "Notion-Version": "2025-09-03",
            }
            response = requests.post(create_upload_url, headers=headers, json={})
            response.raise_for_status()
            upload_data = response.json()
            upload_url = upload_data["upload_url"]

            # Step 2: Upload file contents
            with open(file_path, "rb") as f:
                upload_headers = {
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2025-09-03",
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
            "Notion-Version": "2025-09-03",
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
            "Notion-Version": "2025-09-03",
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
            "Notion-Version": "2025-09-03",
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

    def upload_multiple_files_to_property(self, page_id: str, property_name: str, file_paths: List[str]) -> Dict[str, Any]:
        """Uploads multiple files and attaches them all to a single Notion property."""
        file_assets = []

        for path in file_paths:
            if os.path.exists(path):
                # 1. Upload each file individually
                upload_resp = self.upload_file(path)
                file_upload_id = upload_resp["id"]

                # 2. Build the 'files' array for the Notion request
                file_assets.append({
                    "type": "file_upload",
                    "file_upload": {"id": file_upload_id},
                    "name": os.path.basename(path)
                })

        # 3. Update the page property with the full list
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2025-09-03",
        }
        data = {
            "properties": {
                property_name: {
                    "files": file_assets  # This array contains all your files
                }
            }
        }
        response = requests.patch(update_url, headers=headers, json=data)
        return response.json()

    def dict_to_notion_schema(self, data: Dict[str, Any], title_key: str) -> Dict[str, Any]:
        """Converts a dictionary into a Notion property schema for database creation.

        Parameters:
            data (dict): Dictionary containing sample values to infer types from.
            title_key (str): The key that should be used as the title property.

        Returns:
            dict: A dictionary defining the Notion property schema.
        """
        properties = {}

        for key, value in data.items():
            # Handle NumPy types
            if hasattr(value, "item"):
                value = value.item()

            # Debug output to help diagnose type issues
            print(f"DEBUG: key='{key}', value={value}, type={type(value).__name__}, isinstance(bool)={isinstance(value, bool)}, isinstance(int)={isinstance(value, int)}")

            if key == title_key:
                properties[key] = {"title": {}}
            # IMPORTANT: Check for bool BEFORE (int, float) because bool is a subclass of int in Python
            elif isinstance(value, bool):
                properties[key] = {"checkbox": {}}
                print(f"  → Assigned as CHECKBOX")
            elif isinstance(value, (int, float)):
                properties[key] = {"number": {"format": "number"}}
                print(f"  → Assigned as NUMBER")
            else:
                properties[key] = {"rich_text": {}}
                print(f"  → Assigned as RICH_TEXT")

        return properties

    def dict_to_notion_props(self, data: Dict[str, Any], title_key: str) -> Dict[str, Any]:
        """Converts a dictionary into Notion property values for page creation.

        Parameters:
            data (dict): Dictionary containing the values to convert.
            title_key (str): The key that should be used as the title property.

        Returns:
            dict: A dictionary defining the Notion property values.
        """
        notion_props = {}
        for key, value in data.items():
            # Handle NumPy types
            if hasattr(value, "item"):
                value = value.item()

            if key == title_key:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                notion_props[key] = {"title": [{"text": {"content": f"{value} ({ts})"}}]}

            # FIX: Handle Booleans
            elif isinstance(value, bool):
                # Option A: Map to a Checkbox column in Notion
                # notion_props[key] = {"checkbox": value}

                # Option B: Map to a Rich Text column as a string (since you added a rich text field)
                notion_props[key] = {"rich_text": [{"text": {"content": str(value)}}]}

            elif isinstance(value, (int, float)):
                if pd.isna(value) or np.isinf(value): continue
                notion_props[key] = {"number": float(value)}
            else:
                notion_props[key] = {"rich_text": [{"text": {"content": str(value)}}]}
        return notion_props

    def log_ml_experiment(
        self,
        data_source_id: str,
        config: Dict,
        metrics: Dict,
        plots: List[str] = None,
        target_metric: str = "sMAPE",      # Re-added these
        higher_is_better: bool = False,   # to fix the error
        file_paths: Optional[List[str]] = None, # Changed to list
        file_property_name: str = "Output Files"
    ):
        """Logs ML experiment and compares metrics with multiple file support."""
        improvement_tag = "Standard Run"
        new_score = metrics.get(target_metric)

        # 1. Leaderboard Logic (Champions)
        if new_score is not None:
            try:
                df = self.get_data_source_pages_as_dataframe(data_source_id, limit=100)
                if not df.empty and target_metric in df.columns:
                    valid_scores = pd.to_numeric(df[target_metric], errors='coerce').dropna()
                    if not valid_scores.empty:
                        current_best = valid_scores.max() if higher_is_better else valid_scores.min()
                        is_improvement = (new_score > current_best) if higher_is_better else (new_score < current_best)
                        if is_improvement:
                            improvement_tag = f"🏆 NEW BEST {target_metric} (Prev: {current_best:.2f})"
                        else:
                            diff = abs(new_score - current_best)
                            improvement_tag = f"No Improvement (+{diff:.2f} {target_metric})"
            except Exception as e:
                print(f"Leaderboard check skipped: {e}")

        # 2. Prepare Notion Properties
        data_for_notion = metrics.copy()
        data_for_notion["Run Status"] = improvement_tag
        combined_payload = {**config, **data_for_notion}
        title_key = list(config.keys())[0]
        properties = self.dict_to_notion_props(combined_payload, title_key)

        try:
            # 3. Create the row
            new_page = self.new_page_to_data_source(data_source_id, properties)
            page_id = new_page["id"]

            # 4. Handle Plots (Body)
            if plots:
                for plot_path in plots:
                    if os.path.exists(plot_path):
                        self.one_step_image_embed(page_id, plot_path)

            # 5. Handle Multiple File Uploads (Property)
            if file_paths:
                file_assets = []
                for path in file_paths:
                    if os.path.exists(path):
                        print(f"Uploading {path}...")
                        upload_resp = self.upload_file(path)
                        file_assets.append({
                            "type": "file_upload",
                            "file_upload": {"id": upload_resp["id"]},
                            "name": os.path.basename(path),
                        })

                if file_assets:
                    # Attach all files in one request
                    update_url = f"https://api.notion.com/v1/pages/{page_id}"
                    file_payload = {"properties": {file_property_name: {"files": file_assets}}}
                    self._make_request("PATCH", update_url, file_payload)
                    print(f"✅ {len(file_assets)} files attached to {file_property_name}")

            return page_id
        except Exception as e:
            print(f"Log error: {e}")
            return None

    def create_ml_database(self, parent_page_id: str, db_title: str, config: Dict, metrics: Dict, file_property_name: str = "Output Files") -> str:
        """
        Analyzes dicts to create a new Notion Database with the correct schema.
        Uses dict_to_notion_schema() for universal type conversion.
        """
        combined = {**config, **metrics}
        title_key = list(config.keys())[0]

        # Use the universal dict_to_notion_schema() method
        properties = self.dict_to_notion_schema(combined, title_key)

        # Add 'Run Status' if not already present
        if "Run Status" not in properties:
            properties["Run Status"] = {"rich_text": {}}

        # Add the Multi-file property
        properties[file_property_name] = {"files": {}}

        print(f"Creating database '{db_title}' with {len(properties)} columns...")

        response = self.create_database(
            parent_page_id=parent_page_id,
            database_title=db_title,
            initial_data_source_properties=properties
        )

        data_source_id = response.get("initial_data_source", {}).get("id")
        return data_source_id if data_source_id else response.get("id")
