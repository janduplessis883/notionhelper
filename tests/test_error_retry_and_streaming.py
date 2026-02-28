from unittest.mock import Mock, patch

import requests

from notionhelper import (
    NotionHelper,
    RetryPolicy,
    AuthError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    TimeoutError,
)


def _mock_response(status_code: int, payload: dict, headers: dict | None = None) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.headers = headers or {}
    response.json.return_value = payload
    response.text = str(payload)
    return response


def test_make_request_raises_auth_error_with_metadata():
    helper = NotionHelper("token", max_retries=0)
    response = _mock_response(401, {"code": "unauthorized", "message": "bad token"})

    with patch("notionhelper.helper.requests.get", return_value=response):
        try:
            helper._make_request("GET", "https://api.notion.com/v1/pages/x")
            assert False, "Expected AuthError"
        except AuthError as err:
            assert err.status_code == 401
            assert err.notion_code == "unauthorized"
            assert err.request_path == "/v1/pages/x"


def test_make_request_raises_validation_notfound_and_ratelimit_errors():
    helper = NotionHelper("token", max_retries=0)
    scenarios = [
        (400, {"code": "validation_error", "message": "bad payload"}, ValidationError),
        (404, {"code": "object_not_found", "message": "missing"}, NotFoundError),
        (429, {"code": "rate_limited", "message": "slow down"}, RateLimitError),
    ]

    for status, payload, expected_exc in scenarios:
        response = _mock_response(status, payload)
        with patch("notionhelper.helper.requests.get", return_value=response):
            try:
                helper._make_request("GET", "https://api.notion.com/v1/test")
                assert False, f"Expected {expected_exc.__name__}"
            except expected_exc as err:
                assert err.status_code == status
                assert err.request_path == "/v1/test"


def test_make_request_timeout_maps_to_structured_timeout_error():
    helper = NotionHelper("token", max_retries=0)
    with patch("notionhelper.helper.requests.get", side_effect=requests.exceptions.Timeout("boom")):
        try:
            helper._make_request("GET", "https://api.notion.com/v1/test")
            assert False, "Expected TimeoutError"
        except TimeoutError as err:
            assert err.request_path == "/v1/test"


def test_make_request_per_call_retry_policy_override():
    helper = NotionHelper("token", max_retries=0)
    retry_response = _mock_response(500, {"code": "internal_server_error", "message": "retry"})
    success_response = _mock_response(200, {"ok": True})
    policy = RetryPolicy(max_retries=1, base_delay=0.1, jitter_ratio=0.0, timeout=5.0, retry_statuses={500})

    with patch("notionhelper.helper.requests.get", side_effect=[retry_response, success_response]) as mock_get:
        with patch("notionhelper.helper.time.sleep") as mock_sleep:
            result = helper._make_request("GET", "https://api.notion.com/v1/test", retry_policy=policy)

    assert result == {"ok": True}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(0.1)


def test_iter_data_source_pages_streams_paginated_results():
    helper = NotionHelper("token")
    responses = [
        {"results": [{"id": "p1"}, {"id": "p2"}], "has_more": True, "next_cursor": "c1"},
        {"results": [{"id": "p3"}], "has_more": False, "next_cursor": None},
    ]

    with patch.object(NotionHelper, "_make_request", side_effect=responses):
        items = list(helper.iter_data_source_pages("data-source-id"))

    assert [item["id"] for item in items] == ["p1", "p2", "p3"]


def test_iter_data_source_page_records_yields_normalized_rows():
    helper = NotionHelper("token")
    page_payload = {
        "results": [
            {
                "id": "page-1",
                "properties": {
                    "Name": {"type": "title", "title": [{"plain_text": "Task"}]},
                    "Due": {"type": "date", "date": {"start": "2026-03-01T08:00:00-05:00", "end": None, "time_zone": None}},
                },
            }
        ],
        "has_more": False,
        "next_cursor": None,
    }

    with patch.object(NotionHelper, "_make_request", return_value=page_payload):
        rows = list(helper.iter_data_source_page_records("data-source-id", utc=True))

    assert rows[0]["notion_page_id"] == "page-1"
    assert rows[0]["Name"] == "Task"
    assert rows[0]["Due"] == "2026-03-01T13:00:00Z"
