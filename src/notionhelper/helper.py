from typing import Optional, Dict, List, Any, Union
import pandas as pd
import os
import requests
import mimetypes
import json
import re
import time
import logging
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import numpy as np


# NotionHelper can be used in conjunction with the Streamlit APP: (Notion API JSON)[https://notioinapiassistant.streamlit.app]
LOGGER = logging.getLogger(__name__)


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

    append_page_body(page_id, body):
        Appends Notion blocks or raw markdown text to the body of a Notion page.

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

    def __init__(
        self,
        notion_token: str,
        debug: bool = False,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
        request_timeout: float = 30.0,
    ):
        """Initializes the NotionHelper instance with the provided token.

        Parameters:
            notion_token (str): Notion API secret.
            debug (bool): Enables verbose debug logging for API calls.
            max_retries (int): Number of retries for 429/5xx and transient request failures.
            retry_base_delay (float): Base delay (seconds) for exponential backoff.
            request_timeout (float): Timeout (seconds) for HTTP requests.
        """
        self.notion_token = notion_token
        self.debug = debug
        self.max_retries = max(0, max_retries)
        self.retry_base_delay = max(0.1, retry_base_delay)
        self.request_timeout = max(1.0, request_timeout)
        self._supported_block_types = {
            "bookmark",
            "breadcrumb",
            "bulleted_list_item",
            "callout",
            "child_database",
            "child_page",
            "code",
            "column",
            "column_list",
            "divider",
            "embed",
            "equation",
            "file",
            "heading_1",
            "heading_2",
            "heading_3",
            "image",
            "link_preview",
            "link_to_page",
            "numbered_list_item",
            "paragraph",
            "pdf",
            "quote",
            "synced_block",
            "table",
            "table_row",
            "table_of_contents",
            "to_do",
            "toggle",
            "video",
        }

    def _utf16_units(self, value: str) -> int:
        """Returns the number of UTF-16 code units in a string."""
        return len(value.encode("utf-16-le")) // 2

    def _normalize_notion_id(self, value: str, with_hyphens: bool = True) -> Optional[str]:
        """Normalizes a Notion UUID/hex ID to either 32-char or hyphenated UUID format."""
        if not isinstance(value, str):
            return None
        compact = value.strip().replace("-", "")
        if not re.fullmatch(r"[0-9a-fA-F]{32}", compact):
            return None
        compact = compact.lower()
        if not with_hyphens:
            return compact
        return (
            f"{compact[0:8]}-{compact[8:12]}-{compact[12:16]}-"
            f"{compact[16:20]}-{compact[20:32]}"
        )

    def extract_page_id_from_url(self, page_url_or_id: str, with_hyphens: bool = True) -> str:
        """Extracts a Notion page ID from a page URL or raw page ID string.

        Parameters:
            page_url_or_id (str): Notion page URL or raw page ID.
            with_hyphens (bool): Return UUID with hyphens if True, else compact 32-char form.

        Returns:
            str: Normalized Notion page ID.
        """
        direct = self._normalize_notion_id(page_url_or_id, with_hyphens=with_hyphens)
        if direct:
            return direct

        if not isinstance(page_url_or_id, str):
            raise TypeError("page_url_or_id must be a string")

        parsed = urlparse(page_url_or_id.strip())
        candidates: List[str] = []

        # Path is most reliable for shared page URLs
        candidates.extend(
            re.findall(
                r"([0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
                parsed.path,
            )
        )

        # Query params fallback
        query_values = parse_qs(parsed.query)
        for key in ("p", "page_id", "id"):
            for value in query_values.get(key, []):
                candidates.append(value)

        for candidate in candidates:
            normalized = self._normalize_notion_id(candidate, with_hyphens=with_hyphens)
            if normalized:
                return normalized

        raise ValueError("Could not extract a valid Notion page ID from the input")

    def _chunk_text(self, value: str, max_utf16_units: int = 2000) -> List[str]:
        """Splits text into chunks that each fit Notion's UTF-16 length limit."""
        if not value:
            return [""]

        chunks = []
        current_chars: List[str] = []
        current_units = 0

        for char in value:
            char_units = self._utf16_units(char)
            if current_chars and current_units + char_units > max_utf16_units:
                chunks.append("".join(current_chars))
                current_chars = [char]
                current_units = char_units
            else:
                current_chars.append(char)
                current_units += char_units

        if current_chars:
            chunks.append("".join(current_chars))

        return chunks

    def _normalize_rich_text(self, items: Any) -> List[Dict[str, Any]]:
        """Normalizes rich text entries into a Notion-safe text-only representation."""
        if not isinstance(items, list):
            return []

        normalized: List[Dict[str, Any]] = []
        default_annotations = {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        }

        for item in items:
            content = ""
            link_url = None
            annotations = default_annotations.copy()

            if isinstance(item, str):
                content = item
            elif isinstance(item, dict):
                item_annotations = item.get("annotations", {})
                if isinstance(item_annotations, dict):
                    annotations.update(
                        {
                            "bold": bool(item_annotations.get("bold", False)),
                            "italic": bool(item_annotations.get("italic", False)),
                            "strikethrough": bool(item_annotations.get("strikethrough", False)),
                            "underline": bool(item_annotations.get("underline", False)),
                            "code": bool(item_annotations.get("code", False)),
                            "color": item_annotations.get("color", "default") or "default",
                        }
                    )

                text_obj = item.get("text") if isinstance(item.get("text"), dict) else {}
                if item.get("type") == "text" and isinstance(text_obj, dict):
                    text_obj = item["text"]
                    content = text_obj.get("content", "") or item.get("plain_text", "")
                    link_obj = text_obj.get("link")
                    if isinstance(link_obj, dict):
                        link_url = link_obj.get("url")
                else:
                    content = text_obj.get("content", "") or item.get("plain_text", "")

                if item.get("href"):
                    link_url = item.get("href")
            else:
                continue

            if not isinstance(content, str):
                content = str(content)

            for chunk in self._chunk_text(content, 2000):
                text_entry: Dict[str, Any] = {"content": chunk}
                if link_url:
                    text_entry["link"] = {"url": link_url}
                normalized.append(
                    {
                        "type": "text",
                        "text": text_entry,
                        "annotations": annotations.copy(),
                    }
                )

        return normalized

    def _sanitize_notion_block(self, block: Any) -> Optional[Dict[str, Any]]:
        """Sanitizes a single Notion block for the children append API."""
        if not isinstance(block, dict):
            return None

        raw_type = block.get("type")
        if not isinstance(raw_type, str):
            return None

        block_type = raw_type
        if raw_type.startswith("heading_"):
            match = re.match(r"heading_(\d+)$", raw_type)
            if match and int(match.group(1)) > 3:
                block_type = "heading_3"

        if block_type not in self._supported_block_types:
            return None

        block_payload = block.get(raw_type, {})
        if not isinstance(block_payload, dict):
            block_payload = {}

        sanitized_payload: Dict[str, Any] = {}
        for key, value in block_payload.items():
            if key in {"rich_text", "caption"}:
                sanitized_payload[key] = self._normalize_rich_text(value)
            elif key == "children":
                if isinstance(value, list):
                    sanitized_payload[key] = self._sanitize_blocks(value)
            else:
                sanitized_payload[key] = value

        if block_type == "code":
            if not isinstance(sanitized_payload.get("language"), str) or not sanitized_payload.get("language"):
                sanitized_payload["language"] = "plain text"

        return {
            "object": "block",
            "type": block_type,
            block_type: sanitized_payload,
        }

    def _sanitize_blocks(self, blocks: Any) -> List[Dict[str, Any]]:
        """Sanitizes a list of blocks, dropping unsupported or malformed blocks."""
        if not isinstance(blocks, list):
            return []
        sanitized_blocks = []
        for block in blocks:
            sanitized = self._sanitize_notion_block(block)
            if sanitized:
                sanitized_blocks.append(sanitized)
        return sanitized_blocks

    def _plain_text_rich_text(self, value: str) -> List[Dict[str, Any]]:
        """Builds a plain text rich_text array, using the shared normalizer/chunker."""
        return self._normalize_rich_text([{"type": "text", "text": {"content": value}}])

    def _markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        """Converts markdown into a basic list of Notion block objects."""
        lines = markdown.splitlines()
        blocks: List[Dict[str, Any]] = []
        paragraph_lines: List[str] = []

        def flush_paragraph() -> None:
            if not paragraph_lines:
                return
            text = " ".join(part.strip() for part in paragraph_lines if part.strip()).strip()
            paragraph_lines.clear()
            if not text:
                return
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": self._plain_text_rich_text(text)},
                }
            )

        in_code_fence = False
        code_language = "plain text"
        code_lines: List[str] = []

        for line in lines:
            stripped = line.strip()

            if in_code_fence:
                if stripped.startswith("```"):
                    blocks.append(
                        {
                            "object": "block",
                            "type": "code",
                            "code": {
                                "language": code_language,
                                "rich_text": self._plain_text_rich_text("\n".join(code_lines)),
                            },
                        }
                    )
                    in_code_fence = False
                    code_language = "plain text"
                    code_lines = []
                else:
                    code_lines.append(line.rstrip("\n"))
                continue

            fence_match = re.match(r"^```([a-zA-Z0-9_+\- ]*)\s*$", stripped)
            if fence_match:
                flush_paragraph()
                in_code_fence = True
                parsed_language = fence_match.group(1).strip()
                code_language = parsed_language if parsed_language else "plain text"
                code_lines = []
                continue

            if not stripped:
                flush_paragraph()
                continue

            heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if heading_match:
                flush_paragraph()
                level = min(len(heading_match.group(1)), 3)
                text = heading_match.group(2).strip()
                blocks.append(
                    {
                        "object": "block",
                        "type": f"heading_{level}",
                        f"heading_{level}": {"rich_text": self._plain_text_rich_text(text)},
                    }
                )
                continue

            if re.match(r"^([-*_])(?:\s*\1){2,}\s*$", stripped):
                flush_paragraph()
                blocks.append({"object": "block", "type": "divider", "divider": {}})
                continue

            quote_match = re.match(r"^>\s?(.*)$", stripped)
            if quote_match:
                flush_paragraph()
                blocks.append(
                    {
                        "object": "block",
                        "type": "quote",
                        "quote": {"rich_text": self._plain_text_rich_text(quote_match.group(1).strip())},
                    }
                )
                continue

            unordered_match = re.match(r"^[-*+]\s+(.*)$", stripped)
            if unordered_match:
                flush_paragraph()
                blocks.append(
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": self._plain_text_rich_text(unordered_match.group(1).strip())
                        },
                    }
                )
                continue

            ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
            if ordered_match:
                flush_paragraph()
                blocks.append(
                    {
                        "object": "block",
                        "type": "numbered_list_item",
                        "numbered_list_item": {
                            "rich_text": self._plain_text_rich_text(ordered_match.group(1).strip())
                        },
                    }
                )
                continue

            paragraph_lines.append(line)

        if in_code_fence:
            blocks.append(
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": code_language,
                        "rich_text": self._plain_text_rich_text("\n".join(code_lines)),
                    },
                }
            )

        flush_paragraph()
        return blocks

    def _make_request(
        self,
        method: str,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        api_version: str = "2025-09-03",
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Internal helper to make authenticated requests to the Notion API.
        Handles headers, JSON serialization, retries/backoff, and error reporting.
        """
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": api_version,
        }
        response = None
        request_method = method.upper()
        if request_method not in {"GET", "POST", "PATCH"}:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if self.debug:
            LOGGER.debug(
                "Notion request method=%s url=%s params=%s payload_keys=%s",
                request_method,
                url,
                params,
                sorted(payload.keys()) if isinstance(payload, dict) else None,
            )

        for attempt in range(self.max_retries + 1):
            try:
                if request_method == "GET":
                    response = requests.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=self.request_timeout,
                    )
                elif request_method == "POST":
                    response = requests.post(
                        url,
                        headers=headers,
                        data=json.dumps(payload),
                        timeout=self.request_timeout,
                    )
                else:
                    response = requests.patch(
                        url,
                        headers=headers,
                        data=json.dumps(payload),
                        timeout=self.request_timeout,
                    )

                if response.status_code in {429, 500, 502, 503, 504} and attempt < self.max_retries:
                    retry_after = response.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else self.retry_base_delay * (2 ** attempt)
                    except ValueError:
                        delay = self.retry_base_delay * (2 ** attempt)
                    LOGGER.warning(
                        "Transient Notion error status=%s on %s %s. Retrying in %.2fs (attempt %s/%s).",
                        response.status_code,
                        request_method,
                        url,
                        delay,
                        attempt + 1,
                        self.max_retries,
                    )
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                try:
                    return response.json()
                except ValueError:
                    return {}

            except requests.exceptions.RequestException as req_err:
                is_last_attempt = attempt >= self.max_retries
                if not is_last_attempt:
                    delay = self.retry_base_delay * (2 ** attempt)
                    LOGGER.warning(
                        "Request error on %s %s: %s. Retrying in %.2fs (attempt %s/%s).",
                        request_method,
                        url,
                        req_err,
                        delay,
                        attempt + 1,
                        self.max_retries,
                    )
                    time.sleep(delay)
                    continue

                response_body = response.text if response is not None else None
                LOGGER.error(
                    "Notion API request failed method=%s url=%s status=%s error=%s response=%s",
                    request_method,
                    url,
                    response.status_code if response is not None else None,
                    req_err,
                    response_body,
                )

                if response is not None and payload and isinstance(payload.get("children"), list):
                    message = ""
                    try:
                        err_json = response.json()
                        message = err_json.get("message", "") if isinstance(err_json, dict) else ""
                    except ValueError:
                        message = response.text

                    block_index_match = re.search(r"children\[(\d+)\]", message or "")
                    if block_index_match:
                        bad_index = int(block_index_match.group(1))
                        if 0 <= bad_index < len(payload["children"]):
                            LOGGER.error(
                                "Likely failing child block at index %s: %s",
                                bad_index,
                                json.dumps(payload["children"][bad_index], indent=2),
                            )
                raise

        raise RuntimeError("Request retry loop exited unexpectedly")

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

    def _blocks_to_markdown(self, blocks: List[Dict[str, Any]]) -> str:
        """Converts Notion blocks to markdown format.

        Parameters:
            blocks (list): List of block objects from Notion API

        Returns:
            str: Markdown formatted string
        """
        markdown_lines = []

        for block in blocks:
            block_type = block.get("type", "")
            block_data = block.get(block_type, {})

            if block_type == "paragraph":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                if text:
                    markdown_lines.append(text)
                markdown_lines.append("")

            elif block_type == "heading_1":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"# {text}")
                markdown_lines.append("")

            elif block_type == "heading_2":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"## {text}")
                markdown_lines.append("")

            elif block_type == "heading_3":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"### {text}")
                markdown_lines.append("")

            elif block_type == "bulleted_list_item":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"- {text}")

            elif block_type == "numbered_list_item":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"1. {text}")

            elif block_type == "code":
                code_text = self._extract_rich_text(block_data.get("rich_text", []))
                language = block_data.get("language", "")
                markdown_lines.append(f"```{language}")
                markdown_lines.append(code_text)
                markdown_lines.append("```")
                markdown_lines.append("")

            elif block_type == "image":
                image_data = block_data.get("external", {}) or block_data.get("file", {})
                image_url = image_data.get("url", "")
                if image_url:
                    markdown_lines.append(f"![Image]({image_url})")
                    markdown_lines.append("")

            elif block_type == "divider":
                markdown_lines.append("---")
                markdown_lines.append("")

            elif block_type == "quote":
                text = self._extract_rich_text(block_data.get("rich_text", []))
                markdown_lines.append(f"> {text}")
                markdown_lines.append("")

            elif block_type in {"bookmark", "embed", "link_preview"}:
                block_url = block_data.get("url", "")
                if block_url:
                    markdown_lines.append(f"[{block_url}]({block_url})")
                    markdown_lines.append("")

            elif block_type in {"file", "pdf", "video"}:
                media_data = block_data.get("external", {}) or block_data.get("file", {})
                media_url = media_data.get("url", "")
                if media_url:
                    markdown_lines.append(f"[{block_type}]({media_url})")
                    markdown_lines.append("")

        return "\n".join(markdown_lines).strip()

    def _extract_rich_text(self, rich_text_array: List[Dict[str, Any]]) -> str:
        """Extracts and formats rich text from Notion rich_text array.

        Parameters:
            rich_text_array (list): Array of rich text objects

        Returns:
            str: Formatted text with markdown syntax
        """
        result = []

        for text_obj in rich_text_array:
            if not isinstance(text_obj, dict):
                continue

            text_data = text_obj.get("text", {}) if isinstance(text_obj.get("text"), dict) else {}
            content = text_data.get("content", "") or text_obj.get("plain_text", "") or ""
            if not isinstance(content, str):
                content = str(content)

            annotations = text_obj.get("annotations", {})
            href = text_obj.get("href", None)
            if not href:
                link_obj = text_data.get("link")
                if isinstance(link_obj, dict):
                    href = link_obj.get("url")
            if href and not content:
                content = href

            # Apply markdown formatting based on annotations
            if annotations.get("bold"):
                content = f"**{content}**"
            if annotations.get("italic"):
                content = f"*{content}*"
            if annotations.get("strikethrough"):
                content = f"~~{content}~~"
            if annotations.get("code"):
                content = f"`{content}`"
            if href:
                content = f"[{content}]({href})"

            result.append(content)

        return "".join(result)

    def get_page(self, page_id: str, return_markdown: bool = False) -> Dict[str, Any]:
        """Retrieves the JSON of the page properties and an array of blocks on a Notion page given its page_id.

        Parameters:
            page_id (str): The ID of the Notion page
            return_markdown (bool): If True, converts blocks to markdown. If False, returns raw JSON. Defaults to False.

        Returns:
            dict: Dictionary with 'properties' and 'content' (as JSON or markdown string)
        """

        # Retrieve the page properties
        page_url = f"https://api.notion.com/v1/pages/{page_id}"
        page = self._make_request("GET", page_url)

        # Retrieve the block data (content) with pagination
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        content_blocks: List[Dict[str, Any]] = []
        next_cursor = None
        while True:
            params = {"page_size": 100}
            if next_cursor:
                params["start_cursor"] = next_cursor
            blocks = self._make_request("GET", blocks_url, params=params)
            content_blocks.extend(blocks.get("results", []))
            if not blocks.get("has_more"):
                break
            next_cursor = blocks.get("next_cursor")
            if not next_cursor:
                break

        # Extract all properties as a JSON object
        properties = page.get("properties", {})

        # Convert to markdown if requested
        if return_markdown:
            content = self._blocks_to_markdown(content_blocks)
        else:
            content = content_blocks

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

    def trash_page(self, page_id: str) -> Dict[str, Any]:
        """Moves a Notion page to trash."""
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"in_trash": True}
        return self._make_request("PATCH", url, payload)

    def restore_page(self, page_id: str) -> Dict[str, Any]:
        """Restores a Notion page from trash."""
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"in_trash": False}
        return self._make_request("PATCH", url, payload)

    def append_page_body(
        self,
        page_id: str,
        body: Optional[Union[str, List[Dict[str, Any]]]] = None,
        sanitize: bool = True,
        blocks: Optional[List[Dict[str, Any]]] = None,
        batch_size: int = 100,
    ) -> Dict[str, Any]:
        """Appends blocks or markdown text to a Notion page body.

        Parameters:
            page_id (str): The Notion page ID.
            body (str | list[dict]): Raw markdown text or a Notion blocks array.
            sanitize (bool): If True, run block/rich_text sanitization before request.
            blocks (list[dict] | None): Backward-compatible alias for body when passing blocks.
            batch_size (int): Number of child blocks per append request (Notion max is 100).
        """
        if body is None and blocks is not None:
            body = blocks
        elif body is not None and blocks is not None:
            raise ValueError("Provide either body or blocks, not both")
        elif body is None:
            raise ValueError("Either body or blocks must be provided")

        if isinstance(body, str):
            payload_blocks = self._markdown_to_blocks(body)
        elif isinstance(body, list):
            payload_blocks = body
        else:
            raise TypeError("body must be a markdown string or a list of Notion blocks")

        if sanitize:
            payload_blocks = self._sanitize_blocks(payload_blocks)

        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        batch_size = min(batch_size, 100)

        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        if not payload_blocks:
            return {"object": "list", "results": []}

        responses = []
        for start_idx in range(0, len(payload_blocks), batch_size):
            payload = {"children": payload_blocks[start_idx:start_idx + batch_size]}
            responses.append(self._make_request("PATCH", url, payload))

        if len(responses) == 1:
            return responses[0]

        merged_results: List[Dict[str, Any]] = []
        for response in responses:
            if isinstance(response, dict) and isinstance(response.get("results"), list):
                merged_results.extend(response["results"])

        return {
            "object": "list",
            "results": merged_results,
            "batch_count": len(responses),
            "responses": responses,
        }

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
                        title_list = value.get("title", [])
                        row[key] = title_list[0].get("plain_text", "") if title_list else ""
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
