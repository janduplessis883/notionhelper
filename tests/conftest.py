"""
Pytest configuration and fixtures for NotionHelper tests.
"""
import pytest
import os
from unittest.mock import Mock, patch
from typing import Dict, Any

from notionhelper import NotionHelper


@pytest.fixture
def mock_notion_token():
    """Fixture providing a mock Notion API token."""
    return "secret_test_token_123456789"


@pytest.fixture
def notion_helper(mock_notion_token):
    """Fixture providing a NotionHelper instance with mocked token."""
    return NotionHelper(mock_notion_token)


@pytest.fixture
def sample_database_id():
    """Fixture providing a sample database ID."""
    return "d7a3b2c1-4e5f-6789-abcd-ef0123456789"


@pytest.fixture
def sample_page_id():
    """Fixture providing a sample page ID."""
    return "p1a2b3c4-5d6e-7f89-0123-456789abcdef"


@pytest.fixture
def sample_database_schema():
    """Fixture providing a sample database schema response."""
    return {
        "object": "database",
        "id": "d7a3b2c1-4e5f-6789-abcd-ef0123456789",
        "title": [
            {
                "type": "text",
                "text": {"content": "Test Database"},
                "plain_text": "Test Database"
            }
        ],
        "properties": {
            "Name": {
                "id": "title",
                "type": "title",
                "title": {}
            },
            "Status": {
                "id": "status",
                "type": "status",
                "status": {
                    "options": [
                        {"id": "1", "name": "Not started", "color": "default"},
                        {"id": "2", "name": "In progress", "color": "blue"},
                        {"id": "3", "name": "Done", "color": "green"}
                    ]
                }
            },
            "Priority": {
                "id": "priority",
                "type": "select",
                "select": {
                    "options": [
                        {"id": "1", "name": "High", "color": "red"},
                        {"id": "2", "name": "Medium", "color": "yellow"},
                        {"id": "3", "name": "Low", "color": "gray"}
                    ]
                }
            },
            "Due Date": {
                "id": "due_date",
                "type": "date",
                "date": {}
            },
            "Number": {
                "id": "number",
                "type": "number",
                "number": {"format": "number"}
            }
        }
    }


@pytest.fixture
def sample_page_properties():
    """Fixture providing sample page properties for testing."""
    return {
        "Name": {
            "title": [
                {
                    "text": {"content": "Test Page Title"}
                }
            ]
        },
        "Status": {
            "status": {"name": "In progress"}
        },
        "Priority": {
            "select": {"name": "High"}
        },
        "Due Date": {
            "date": {"start": "2024-12-31"}
        },
        "Number": {
            "number": 42
        }
    }


@pytest.fixture
def sample_blocks():
    """Fixture providing sample content blocks."""
    return [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Test Heading"},
                        "plain_text": "Test Heading"
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "This is a test paragraph with some content."},
                        "plain_text": "This is a test paragraph with some content."
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "First bullet point"},
                        "plain_text": "First bullet point"
                    }
                ]
            }
        }
    ]


@pytest.fixture
def sample_database_pages():
    """Fixture providing sample database pages response."""
    return {
        "object": "list",
        "results": [
            {
                "id": "page1-id",
                "properties": {
                    "Name": {
                        "type": "title",
                        "title": [{"plain_text": "First Page"}]
                    },
                    "Status": {
                        "type": "status",
                        "status": {"name": "Done"}
                    },
                    "Number": {
                        "type": "number",
                        "number": 10
                    }
                }
            },
            {
                "id": "page2-id",
                "properties": {
                    "Name": {
                        "type": "title",
                        "title": [{"plain_text": "Second Page"}]
                    },
                    "Status": {
                        "type": "status",
                        "status": {"name": "In progress"}
                    },
                    "Number": {
                        "type": "number",
                        "number": 20
                    }
                }
            }
        ],
        "has_more": False,
        "next_cursor": None
    }


@pytest.fixture
def sample_file_upload_response():
    """Fixture providing sample file upload response."""
    return {
        "id": "file_upload_12345",
        "name": "test_document.pdf",
        "upload_url": "https://files.notion.com/upload/12345"
    }


@pytest.fixture
def temporary_test_file(tmp_path):
    """Fixture creating a temporary test file."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is test file content for testing file operations.")
    return str(test_file)


@pytest.fixture
def mock_requests():
    """Fixture providing mocked requests module."""
    with patch('notionhelper.helper.requests') as mock_req:
        # Configure default successful responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_req.post.return_value = mock_response
        mock_req.patch.return_value = mock_response
        yield mock_req


@pytest.fixture
def mock_notion_client():
    """Fixture providing a fully mocked Notion client."""
    with patch('notionhelper.helper.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Configure default responses
        mock_client.databases.retrieve.return_value = {"id": "test_db"}
        mock_client.databases.query.return_value = {"results": [], "has_more": False}
        mock_client.databases.create.return_value = {"id": "new_db"}
        mock_client.pages.create.return_value = {"id": "new_page"}
        mock_client.pages.retrieve.return_value = {"id": "test_page", "properties": {}}
        mock_client.blocks.children.list.return_value = {"results": []}
        mock_client.blocks.children.append.return_value = {"object": "list"}
        
        yield mock_client


# Test environment configurations
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for all tests."""
    # Ensure we're not accidentally using real tokens
    if 'NOTION_TOKEN' in os.environ:
        del os.environ['NOTION_TOKEN']
    
    # Set test-specific environment variables if needed
    os.environ['TESTING'] = '1'
    
    yield
    
    # Cleanup
    if 'TESTING' in os.environ:
        del os.environ['TESTING']


@pytest.fixture
def caplog_info(caplog):
    """Fixture to capture INFO level logs."""
    import logging
    caplog.set_level(logging.INFO)
    return caplog