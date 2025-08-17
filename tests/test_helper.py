"""
Tests for NotionHelper class.
"""
import pytest
import os
import json
from unittest.mock import Mock, patch, mock_open, MagicMock
from typing import Dict, Any
import pandas as pd

from notionhelper import NotionHelper


class TestNotionHelper:
    """Test cases for NotionHelper class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_token = "secret_test_token_123"
        self.test_database_id = "test_database_id_123"
        self.test_page_id = "test_page_id_123"
        with patch('notionhelper.helper.Client'):
            self.helper = NotionHelper(self.test_token)

    def test_init(self):
        """Test NotionHelper initialization."""
        assert self.helper.notion_token == self.test_token
        assert hasattr(self.helper, 'notion')

    @patch('notionhelper.helper.Client')
    def test_init_with_client_mock(self, mock_client):
        """Test initialization creates Client with correct token."""
        helper = NotionHelper("test_token")
        mock_client.assert_called_once_with(auth="test_token")

    def test_get_database_success(self):
        """Test successful database retrieval."""
        # Mock response
        mock_response = {
            "id": self.test_database_id,
            "title": [{"text": {"content": "Test Database"}}],
            "properties": {"Name": {"title": {}}}
        }
        self.helper.notion.databases.retrieve.return_value = mock_response

        result = self.helper.get_database(self.test_database_id)

        self.helper.notion.databases.retrieve.assert_called_once_with(database_id=self.test_database_id)
        assert result == mock_response

    def test_get_database_failure(self):
        """Test database retrieval failure."""
        self.helper.notion.databases.retrieve.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="Failed to retrieve database"):
            self.helper.get_database(self.test_database_id)

    def test_new_page_to_db(self):
        """Test adding new page to database."""
        mock_response = {"id": self.test_page_id}
        self.helper.notion.pages.create.return_value = mock_response

        page_properties = {
            "Name": {
                "title": [{"text": {"content": "Test Page"}}]
            }
        }

        result = self.helper.new_page_to_db(self.test_database_id, page_properties)

        expected_call_args = {
            "parent": {"database_id": self.test_database_id},
            "properties": page_properties
        }
        self.helper.notion.pages.create.assert_called_once_with(**expected_call_args)
        assert result == mock_response

    def test_append_page_body(self):
        """Test appending content to page."""
        mock_response = {"object": "list"}
        self.helper.notion.blocks.children.append.return_value = mock_response

        blocks = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Test content"}}]
                }
            }
        ]

        result = self.helper.append_page_body(self.test_page_id, blocks)

        self.helper.notion.blocks.children.append.assert_called_once_with(
            block_id=self.test_page_id,
            children=blocks
        )
        assert result == mock_response

    def test_get_all_page_ids(self):
        """Test retrieving all page IDs from database."""
        mock_response = {
            "results": [
                {"id": "page1"},
                {"id": "page2"},
                {"id": "page3"}
            ]
        }
        self.helper.notion.databases.query.return_value = mock_response

        result = self.helper.get_all_page_ids(self.test_database_id)

        self.helper.notion.databases.query.assert_called_once_with(database_id=self.test_database_id)
        assert result == ["page1", "page2", "page3"]

    def test_get_all_pages_as_json(self):
        """Test retrieving all pages as JSON."""
        mock_response = {
            "results": [
                {
                    "id": "page1",
                    "properties": {
                        "Name": {"title": [{"plain_text": "Test Page 1"}]},
                        "Status": {"status": {"name": "Done"}}
                    }
                }
            ],
            "has_more": False
        }
        self.helper.notion.databases.query.return_value = mock_response

        result = self.helper.get_all_pages_as_json(self.test_database_id)

        expected_result = [mock_response["results"][0]["properties"]]
        assert result == expected_result

    def test_get_all_pages_as_dataframe(self):
        """Test converting pages to DataFrame."""
        mock_response = {
            "results": [
                {
                    "id": "page1",
                    "properties": {
                        "Name": {"type": "title", "title": [{"plain_text": "Test Page"}]},
                        "Status": {"type": "status", "status": {"name": "Done"}},
                        "Number": {"type": "number", "number": 42}
                    }
                }
            ],
            "has_more": False
        }
        self.helper.notion.databases.query.return_value = mock_response

        result = self.helper.get_all_pages_as_dataframe(self.test_database_id)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert "Name" in result.columns
        assert "Status" in result.columns
        assert "Number" in result.columns

    def test_upload_file_not_found(self):
        """Test file upload with non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.helper.upload_file("/non/existent/file.txt")

    @patch('notionhelper.helper.mimetypes.guess_type')
    @patch('notionhelper.helper.os.path.exists')
    @patch('notionhelper.helper.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"test content")
    def test_upload_file_success(self, mock_file, mock_post, mock_exists, mock_guess_type):
        """Test successful file upload."""
        mock_exists.return_value = True
        mock_guess_type.return_value = ("application/pdf", None)
        
        # Mock the two API calls
        first_response = Mock(status_code=200)
        first_response.json.return_value = {"upload_url": "https://upload.url"}
        first_response.raise_for_status.return_value = None
        
        second_response = Mock(status_code=200)
        second_response.json.return_value = {"id": "file_upload_id_123"}
        second_response.raise_for_status.return_value = None
        
        mock_post.side_effect = [first_response, second_response]

        result = self.helper.upload_file("/path/to/test.pdf")

        assert result == {"id": "file_upload_id_123"}
        assert mock_post.call_count == 2

    @patch('notionhelper.helper.requests.patch')
    def test_attach_file_to_page(self, mock_patch):
        """Test attaching file to page."""
        mock_response = {"object": "list"}
        mock_patch.return_value = Mock(json=lambda: mock_response)

        result = self.helper.attach_file_to_page(self.test_page_id, "file_upload_id")

        assert result == mock_response
        mock_patch.assert_called_once()

    @patch('notionhelper.helper.requests.patch')
    def test_embed_image_to_page(self, mock_patch):
        """Test embedding image to page."""
        mock_response = {"object": "block"}
        mock_patch.return_value = Mock(json=lambda: mock_response)

        result = self.helper.embed_image_to_page(self.test_page_id, "file_upload_id")

        assert result == mock_response
        mock_patch.assert_called_once()

    @patch.object(NotionHelper, 'upload_file')
    @patch.object(NotionHelper, 'attach_file_to_page')
    def test_one_step_file_to_page(self, mock_attach, mock_upload):
        """Test one-step file upload and attachment."""
        mock_upload.return_value = {"id": "file_upload_id"}
        mock_attach.return_value = {"object": "list"}

        result = self.helper.one_step_file_to_page(self.test_page_id, "/path/to/file.pdf")

        mock_upload.assert_called_once_with("/path/to/file.pdf")
        mock_attach.assert_called_once_with(self.test_page_id, "file_upload_id")
        assert result == {"object": "list"}

    @patch.object(NotionHelper, 'upload_file')
    @patch.object(NotionHelper, 'embed_image_to_page')
    def test_one_step_image_embed(self, mock_embed, mock_upload):
        """Test one-step image upload and embedding."""
        mock_upload.return_value = {"id": "file_upload_id"}
        mock_embed.return_value = {"object": "block"}

        result = self.helper.one_step_image_embed(self.test_page_id, "/path/to/image.png")

        mock_upload.assert_called_once_with("/path/to/image.png")
        mock_embed.assert_called_once_with(self.test_page_id, "file_upload_id")
        assert result == {"object": "block"}

    @patch.object(NotionHelper, 'upload_file')
    @patch.object(NotionHelper, 'attach_file_to_page_property')
    def test_one_step_file_to_page_property(self, mock_attach_property, mock_upload):
        """Test one-step file upload to page property."""
        mock_upload.return_value = {"id": "file_upload_id"}
        mock_attach_property.return_value = {"object": "page"}

        result = self.helper.one_step_file_to_page_property(
            self.test_page_id, "Files", "/path/to/file.pdf", "Custom Name.pdf"
        )

        mock_upload.assert_called_once_with("/path/to/file.pdf")
        mock_attach_property.assert_called_once_with(
            self.test_page_id, "Files", "file_upload_id", "Custom Name.pdf"
        )
        assert result == {"object": "page"}

    def test_create_database(self):
        """Test database creation."""
        mock_response = {"id": "new_database_id"}
        self.helper.notion.databases.create.return_value = mock_response

        properties = {
            "Name": {"title": {}},
            "Status": {"status": {}}
        }

        result = self.helper.create_database("parent_page_id", "Test Database", properties)

        expected_args = {
            "parent": {"type": "page_id", "page_id": "parent_page_id"},
            "title": [{"type": "text", "text": {"content": "Test Database"}}],
            "properties": properties
        }
        self.helper.notion.databases.create.assert_called_once_with(**expected_args)
        assert result == mock_response

    def test_notion_get_page(self):
        """Test retrieving page with properties and content."""
        mock_page = {
            "id": self.test_page_id,
            "properties": {
                "Name": {"title": [{"plain_text": "Test Page"}]}
            }
        }
        mock_blocks = {
            "results": [
                {"type": "paragraph", "paragraph": {"rich_text": []}}
            ]
        }

        self.helper.notion.pages.retrieve.return_value = mock_page
        self.helper.notion.blocks.children.list.return_value = mock_blocks

        result = self.helper.notion_get_page(self.test_page_id)

        assert "properties" in result
        assert "content" in result
        assert result["properties"] == mock_page["properties"]
        assert len(result["content"]) == 1


class TestNotionHelperIntegration:
    """Integration tests that test multiple components working together."""

    def setup_method(self):
        """Set up for integration tests."""
        self.helper = NotionHelper("test_token")

    @patch.object(NotionHelper, 'upload_file')
    @patch.object(NotionHelper, 'attach_file_to_page')
    def test_file_workflow(self, mock_attach, mock_upload):
        """Test complete file upload and attachment workflow."""
        # Mock file upload
        mock_upload.return_value = {"id": "uploaded_file_id", "name": "test.pdf"}
        
        # Mock file attachment
        mock_attach.return_value = {
            "object": "list",
            "results": [{"type": "file", "file": {"name": "test.pdf"}}]
        }

        # Execute workflow
        upload_result = self.helper.upload_file("/path/to/test.pdf")
        attach_result = self.helper.attach_file_to_page("page_id", upload_result["id"])

        # Verify workflow
        assert upload_result["id"] == "uploaded_file_id"
        assert attach_result["object"] == "list"
        mock_upload.assert_called_once_with("/path/to/test.pdf")
        mock_attach.assert_called_once_with("page_id", "uploaded_file_id")


class TestNotionHelperErrorHandling:
    """Tests for error handling scenarios."""

    def setup_method(self):
        """Set up for error handling tests."""
        self.helper = NotionHelper("test_token")

    @patch('notionhelper.helper.requests.post')
    @patch('notionhelper.helper.os.path.exists')
    def test_upload_file_network_error(self, mock_exists, mock_post):
        """Test file upload with network error."""
        mock_exists.return_value = True
        mock_post.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Error uploading file"):
            self.helper.upload_file("/path/to/test.pdf")

    @patch('notionhelper.helper.requests.post')
    @patch('notionhelper.helper.os.path.exists')
    def test_upload_file_http_error(self, mock_exists, mock_post):
        """Test file upload with HTTP error."""
        mock_exists.return_value = True
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 400 Error")
        mock_post.return_value = mock_response

        with pytest.raises(Exception, match="Error uploading file"):
            self.helper.upload_file("/path/to/test.pdf")


if __name__ == "__main__":
    pytest.main([__file__])