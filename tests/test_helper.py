from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from notionhelper import NotionHelper


def test_init_stores_token_and_default_retry_settings():
    helper = NotionHelper("secret_test_token_123")

    assert helper.notion_token == "secret_test_token_123"
    assert helper.max_retries == 3
    assert helper.request_timeout == 30.0


def test_get_database_uses_request_helper():
    helper = NotionHelper("token")

    with patch.object(NotionHelper, "_make_request", return_value={"id": "db-123"}) as mock_request:
        result = helper.get_database("db-123")

    assert result == {"id": "db-123"}
    assert mock_request.call_args.args[:2] == (
        "GET",
        "https://api.notion.com/v1/databases/db-123",
    )


def test_get_data_source_uses_request_helper():
    helper = NotionHelper("token")

    with patch.object(NotionHelper, "_make_request", return_value={"id": "ds-123"}) as mock_request:
        result = helper.get_data_source("ds-123")

    assert result == {"id": "ds-123"}
    assert mock_request.call_args.args[:2] == (
        "GET",
        "https://api.notion.com/v1/data_sources/ds-123",
    )


def test_notion_search_db_returns_results():
    helper = NotionHelper("token")

    with patch.object(
        NotionHelper,
        "_make_request",
        return_value={"results": [{"id": "page-1"}]},
    ) as mock_request:
        result = helper.notion_search_db("roadmap", filter_object_type="page")

    assert result == [{"id": "page-1"}]
    assert mock_request.call_args.args[0] == "POST"
    assert mock_request.call_args.args[1] == "https://api.notion.com/v1/search"
    assert mock_request.call_args.args[2]["filter"]["value"] == "page"


def test_notion_search_db_rejects_invalid_filter_type():
    helper = NotionHelper("token")

    with pytest.raises(ValueError, match="filter_object_type"):
        helper.notion_search_db("roadmap", filter_object_type="database")


def test_new_page_to_data_source_with_properties_uses_core_api_version():
    helper = NotionHelper("token")
    page_properties = {
        "Name": {"title": [{"text": {"content": "Test Page"}}]},
    }

    with patch.object(NotionHelper, "_make_request", return_value={"id": "page-id"}) as mock_request:
        result = helper.new_page_to_data_source("data-source-id", page_properties)

    assert result == {"id": "page-id"}
    assert mock_request.call_args.args[2]["parent"] == {"data_source_id": "data-source-id"}
    assert mock_request.call_args.kwargs["api_version"] == "2025-09-03"


def test_get_data_source_pages_as_dataframe_builds_dataframe():
    helper = NotionHelper("token")
    pages = iter(
        [
            {
                "id": "page-1",
                "properties": {
                    "Name": {"type": "title", "title": [{"plain_text": "Test Page"}]},
                    "Status": {"type": "status", "status": {"name": "Done"}},
                    "Number": {"type": "number", "number": 42},
                },
            }
        ]
    )

    with patch.object(NotionHelper, "iter_data_source_pages", return_value=pages):
        result = helper.get_data_source_pages_as_dataframe("data-source-id")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.loc[0, "Name"] == "Test Page"
    assert result.loc[0, "Status"] == "Done"
    assert result.loc[0, "Number"] == 42


def test_upload_file_not_found():
    helper = NotionHelper("token")

    with pytest.raises(FileNotFoundError, match="File not found"):
        helper.upload_file("/non/existent/file.txt")


@patch("notionhelper.helper.mimetypes.guess_type")
@patch("notionhelper.helper.os.path.exists")
@patch("notionhelper.helper.requests.post")
@patch("builtins.open", new_callable=mock_open, read_data=b"test content")
def test_upload_file_success(mock_file, mock_post, mock_exists, mock_guess_type):
    helper = NotionHelper("token")
    mock_exists.return_value = True
    mock_guess_type.return_value = ("application/pdf", None)

    first_response = Mock(status_code=200)
    first_response.json.return_value = {
        "id": "file-upload-id",
        "upload_url": "https://upload.url",
    }

    second_response = Mock(status_code=200)
    second_response.json.return_value = {"id": "file_upload_id_123"}

    mock_post.side_effect = [first_response, second_response]

    result = helper.upload_file("/path/to/test.pdf")

    assert result == {"id": "file_upload_id_123"}
    assert mock_post.call_count == 2


@patch.object(NotionHelper, "upload_file")
@patch.object(NotionHelper, "attach_file_to_page")
def test_one_step_file_to_page(mock_attach, mock_upload):
    helper = NotionHelper("token")
    mock_upload.return_value = {"id": "file_upload_id"}
    mock_attach.return_value = {"object": "list"}

    result = helper.one_step_file_to_page("page-id", "/path/to/file.pdf")

    mock_upload.assert_called_once_with("/path/to/file.pdf")
    mock_attach.assert_called_once_with("page-id", "file_upload_id")
    assert result == {"object": "list"}


@patch.object(NotionHelper, "upload_file")
@patch.object(NotionHelper, "embed_image_to_page")
def test_one_step_image_embed(mock_embed, mock_upload):
    helper = NotionHelper("token")
    mock_upload.return_value = {"id": "file_upload_id"}
    mock_embed.return_value = {"object": "block"}

    result = helper.one_step_image_embed("page-id", "/path/to/image.png")

    mock_upload.assert_called_once_with("/path/to/image.png")
    mock_embed.assert_called_once_with("page-id", "file_upload_id")
    assert result == {"object": "block"}


@patch.object(NotionHelper, "upload_file")
@patch.object(NotionHelper, "attach_file_to_page_property")
def test_one_step_file_to_page_property(mock_attach_property, mock_upload):
    helper = NotionHelper("token")
    mock_upload.return_value = {"id": "file_upload_id"}
    mock_attach_property.return_value = {"object": "page"}

    result = helper.one_step_file_to_page_property(
        "page-id",
        "Files",
        "/path/to/file.pdf",
        "Custom Name.pdf",
    )

    mock_upload.assert_called_once_with("/path/to/file.pdf")
    mock_attach_property.assert_called_once_with(
        "page-id",
        "Files",
        "file_upload_id",
        "Custom Name.pdf",
    )
    assert result == {"object": "page"}


@patch("notionhelper.helper.requests.post")
@patch("notionhelper.helper.os.path.exists")
def test_upload_file_network_error(mock_exists, mock_post):
    helper = NotionHelper("token")
    mock_exists.return_value = True
    mock_post.side_effect = Exception("Network error")

    with pytest.raises(Exception, match="Error uploading file"):
        helper.upload_file("/path/to/test.pdf")


@patch("notionhelper.helper.requests.post")
@patch("notionhelper.helper.os.path.exists")
def test_upload_file_http_error(mock_exists, mock_post):
    helper = NotionHelper("token")
    mock_exists.return_value = True
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP 400 Error")
    mock_post.return_value = mock_response

    with pytest.raises(Exception, match="Error uploading file"):
        helper.upload_file("/path/to/test.pdf")
