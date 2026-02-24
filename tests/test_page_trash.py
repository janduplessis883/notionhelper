from unittest.mock import patch

from notionhelper import NotionHelper


def test_trash_page_sets_in_trash_true():
    helper = NotionHelper("test-token")

    with patch.object(NotionHelper, "_make_request", return_value={"id": "page-id", "in_trash": True}) as mock_req:
        result = helper.trash_page("page-id")

    assert result["in_trash"] is True
    mock_req.assert_called_once_with(
        "PATCH",
        "https://api.notion.com/v1/pages/page-id",
        {"in_trash": True},
    )


def test_restore_page_sets_in_trash_false():
    helper = NotionHelper("test-token")

    with patch.object(
        NotionHelper,
        "_make_request",
        return_value={"id": "page-id", "in_trash": False},
    ) as mock_req:
        result = helper.restore_page("page-id")

    assert result["in_trash"] is False
    mock_req.assert_called_once_with(
        "PATCH",
        "https://api.notion.com/v1/pages/page-id",
        {"in_trash": False},
    )
