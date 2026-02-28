from unittest.mock import patch

from notionhelper import NotionHelper


def test_parse_datetime_utc_returns_utc_timestamp():
    helper = NotionHelper("token")
    parsed = helper.parse_datetime_utc("2026-03-01T08:00:00-05:00")

    assert parsed is not None
    assert parsed.tzinfo is not None
    assert parsed.isoformat().endswith("+00:00")


def test_normalize_datetime_iso_keeps_date_only_values():
    helper = NotionHelper("token")
    assert helper.normalize_datetime_iso("2026-03-01") == "2026-03-01"


def test_normalize_notion_date_normalizes_to_utc():
    helper = NotionHelper("token")
    normalized = helper.normalize_notion_date(
        {
            "start": "2026-03-01T08:00:00-05:00",
            "end": "2026-03-01T09:00:00-05:00",
            "time_zone": "America/New_York",
        }
    )

    assert normalized["start"] == "2026-03-01T13:00:00Z"
    assert normalized["end"] == "2026-03-01T14:00:00Z"
    assert normalized["time_zone"] == "UTC"


def test_dataframe_datetime_fields_are_normalized_with_utc_defaults():
    helper = NotionHelper("token")
    query_response = {
        "results": [
            {
                "id": "page-1",
                "properties": {
                    "Name": {"type": "title", "title": [{"plain_text": "T1"}]},
                    "Due": {"type": "date", "date": {"start": "2026-03-01T08:00:00-05:00", "end": None, "time_zone": None}},
                    "Created": {"type": "created_time", "created_time": "2026-03-01T08:00:00-05:00"},
                    "Edited": {"type": "last_edited_time", "last_edited_time": "2026-03-01T09:00:00-05:00"},
                },
            }
        ],
        "has_more": False,
        "next_cursor": None,
    }

    with patch.object(NotionHelper, "_make_request", return_value=query_response):
        df = helper.get_data_source_pages_as_dataframe("data-source-id")

    assert df.loc[0, "Due"] == "2026-03-01T13:00:00Z"
    assert df.loc[0, "Created"] == "2026-03-01T13:00:00Z"
    assert df.loc[0, "Edited"] == "2026-03-01T14:00:00Z"
