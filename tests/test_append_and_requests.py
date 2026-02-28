import logging
from unittest.mock import Mock, patch

import pytest
import requests

from notionhelper import NotionHelper, RetryPolicy


def _paragraph_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def test_append_page_body_batches_requests_at_100_children():
    helper = NotionHelper("token")
    blocks = [_paragraph_block(f"line {idx}") for idx in range(205)]

    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"object": "list", "results": [{"id": "a"}]},
            {"object": "list", "results": [{"id": "b"}]},
            {"object": "list", "results": [{"id": "c"}]},
        ]
        response = helper.append_page_body("page-id", blocks)

    assert mock_request.call_count == 3
    first_payload = mock_request.call_args_list[0].args[2]
    second_payload = mock_request.call_args_list[1].args[2]
    third_payload = mock_request.call_args_list[2].args[2]
    assert len(first_payload["children"]) == 100
    assert len(second_payload["children"]) == 100
    assert len(third_payload["children"]) == 5
    assert response["batch_count"] == 3
    assert len(response["results"]) == 3


def test_append_page_body_supports_legacy_blocks_keyword():
    helper = NotionHelper("token")
    blocks = [_paragraph_block("legacy")]

    with patch.object(NotionHelper, "_make_request", return_value={"object": "list"}) as mock_request:
        helper.append_page_body("page-id", blocks=blocks)

    payload = mock_request.call_args.args[2]
    assert payload["children"][0]["type"] == "paragraph"


def test_get_page_paginates_blocks_children_endpoint():
    helper = NotionHelper("token")

    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"properties": {"Name": {"title": []}}},
            {"results": [{"id": "b1"}], "has_more": True, "next_cursor": "cursor-1"},
            {"results": [{"id": "b2"}], "has_more": False, "next_cursor": None},
        ]
        result = helper.get_page("page-id")

    assert result["properties"] == {"Name": {"title": []}}
    assert [block["id"] for block in result["content"]] == ["b1", "b2"]
    assert mock_request.call_args_list[1].kwargs["params"] == {"page_size": 100}
    assert mock_request.call_args_list[2].kwargs["params"] == {
        "page_size": 100,
        "start_cursor": "cursor-1",
    }


def test_get_page_accepts_deprecated_returnmarkdown_alias_with_warning():
    helper = NotionHelper("token")

    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"properties": {"Name": {"title": []}}},
            {"results": [], "has_more": False, "next_cursor": None},
        ]
        with pytest.warns(FutureWarning, match="return_markdown"):
            result = helper.get_page("page-id", returnmarkdown=True)

    assert isinstance(result["content"], str)


def test_get_page_accepts_deprecated_markdownformat_alias_with_warning():
    helper = NotionHelper("token")

    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"properties": {"Name": {"title": []}}},
            {"results": [], "has_more": False, "next_cursor": None},
        ]
        with pytest.warns(FutureWarning, match="return_markdown"):
            result = helper.get_page("page-id", markdownformat=True)

    assert isinstance(result["content"], str)


def test_get_page_raises_on_conflicting_canonical_and_alias_values():
    helper = NotionHelper("token")

    with pytest.warns(FutureWarning, match="return_markdown"):
        with pytest.raises(ValueError, match="Conflicting values"):
            helper.get_page("page-id", return_markdown=True, markdownformat=False)


def test_make_request_retries_on_429_with_retry_after():
    helper = NotionHelper("token", retry_policy=RetryPolicy(max_retries=2, jitter_ratio=0.0))
    retry_response = Mock()
    retry_response.status_code = 429
    retry_response.headers = {"Retry-After": "2"}
    retry_response.text = '{"message":"rate limited"}'

    success_response = Mock()
    success_response.status_code = 200
    success_response.headers = {}
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {"ok": True}

    with patch("notionhelper.helper.requests.patch", side_effect=[retry_response, success_response]) as mock_patch:
        with patch("notionhelper.helper.time.sleep") as mock_sleep:
            result = helper._make_request("PATCH", "https://api.notion.com/v1/test", {"x": 1})

    assert result == {"ok": True}
    assert mock_patch.call_count == 2
    mock_sleep.assert_called_once_with(2.0)


def test_make_request_retries_transient_request_exception():
    helper = NotionHelper(
        "token",
        retry_policy=RetryPolicy(max_retries=1, base_delay=0.5, jitter_ratio=0.0),
    )
    success_response = Mock()
    success_response.status_code = 200
    success_response.headers = {}
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {"ok": True}

    with patch(
        "notionhelper.helper.requests.get",
        side_effect=[requests.exceptions.ConnectionError("boom"), success_response],
    ) as mock_get:
        with patch("notionhelper.helper.time.sleep") as mock_sleep:
            result = helper._make_request("GET", "https://api.notion.com/v1/test")

    assert result == {"ok": True}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(0.5)


def test_debug_logging_emits_request_metadata(caplog):
    helper = NotionHelper("token", debug=True)
    success_response = Mock()
    success_response.status_code = 200
    success_response.headers = {}
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {"ok": True}

    with patch("notionhelper.helper.requests.get", return_value=success_response):
        with caplog.at_level(logging.DEBUG):
            helper._make_request("GET", "https://api.notion.com/v1/test", params={"page_size": 10})

    assert "Notion request method=GET" in caplog.text
