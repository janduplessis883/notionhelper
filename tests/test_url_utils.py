import pytest

from notionhelper import NotionHelper


def test_extract_page_id_from_compact_id():
    helper = NotionHelper("token")
    page_id = "2f5e9f1e8f51415d8fd8be0d0c56e4a1"
    assert helper.extract_page_id_from_url(page_id) == "2f5e9f1e-8f51-415d-8fd8-be0d0c56e4a1"


def test_extract_page_id_from_hyphenated_id_without_hyphens_output():
    helper = NotionHelper("token")
    page_id = "2f5e9f1e-8f51-415d-8fd8-be0d0c56e4a1"
    assert helper.extract_page_id_from_url(page_id, with_hyphens=False) == "2f5e9f1e8f51415d8fd8be0d0c56e4a1"


def test_extract_page_id_from_notion_shared_url():
    helper = NotionHelper("token")
    url = (
        "https://www.notion.so/workspace/Project-Notes-"
        "2f5e9f1e8f51415d8fd8be0d0c56e4a1?pvs=4"
    )
    assert helper.extract_page_id_from_url(url) == "2f5e9f1e-8f51-415d-8fd8-be0d0c56e4a1"


def test_extract_page_id_from_url_query_param():
    helper = NotionHelper("token")
    url = "https://www.notion.so/some/path?p=2f5e9f1e8f51415d8fd8be0d0c56e4a1"
    assert helper.extract_page_id_from_url(url) == "2f5e9f1e-8f51-415d-8fd8-be0d0c56e4a1"


def test_extract_page_id_from_url_raises_for_invalid_input():
    helper = NotionHelper("token")
    with pytest.raises(ValueError):
        helper.extract_page_id_from_url("https://www.notion.so/workspace/no-valid-id-here")
