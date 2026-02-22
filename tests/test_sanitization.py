from unittest.mock import patch

from notionhelper import NotionHelper


def test_append_page_body_sanitizes_heading_and_rich_text():
    helper = NotionHelper("test-token")
    blocks = [
        {
            "type": "heading_4",
            "heading_4": {
                "rich_text": [
                    {"text": {"content": "Title"}, "href": "https://example.com"}
                ]
            },
        }
    ]

    with patch.object(NotionHelper, "_make_request", return_value={"ok": True}) as mock_request:
        helper.append_page_body("page-id", blocks)

    payload = mock_request.call_args.args[2]
    sanitized_block = payload["children"][0]

    assert sanitized_block["type"] == "heading_3"
    assert "heading_3" in sanitized_block
    rich_text = sanitized_block["heading_3"]["rich_text"][0]
    assert rich_text["type"] == "text"
    assert rich_text["text"]["content"] == "Title"
    assert rich_text["text"]["link"]["url"] == "https://example.com"
    assert "href" not in rich_text


def test_normalize_rich_text_chunks_utf16_safely():
    helper = NotionHelper("test-token")
    # 1500 emoji characters => 3000 UTF-16 code units, should chunk into 1000 + 500
    value = "😀" * 1500
    rich_text = helper._normalize_rich_text([{"type": "text", "text": {"content": value}}])

    assert len(rich_text) == 2
    assert helper._utf16_units(rich_text[0]["text"]["content"]) == 2000
    assert helper._utf16_units(rich_text[1]["text"]["content"]) == 1000


def test_sanitize_blocks_drops_unsupported_blocks():
    helper = NotionHelper("test-token")
    blocks = [
        {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "ok"}}]}},
        {"type": "heading_9", "heading_9": {"rich_text": [{"type": "text", "text": {"content": "drop"}}]}},
        {"type": "not_a_real_block", "not_a_real_block": {}},
    ]

    sanitized = helper._sanitize_blocks(blocks)

    assert len(sanitized) == 2
    assert sanitized[0]["type"] == "paragraph"
    assert sanitized[1]["type"] == "heading_3"


def test_append_page_body_accepts_markdown_and_converts_to_blocks():
    helper = NotionHelper("test-token")
    markdown = """# Title

Paragraph text here.

- Item one
1. Item two
> A quote
---
```python
print("hello")
```
"""

    with patch.object(NotionHelper, "_make_request", return_value={"ok": True}) as mock_request:
        helper.append_page_body("page-id", markdown)

    payload = mock_request.call_args.args[2]
    children = payload["children"]
    child_types = [child["type"] for child in children]

    assert child_types == [
        "heading_1",
        "paragraph",
        "bulleted_list_item",
        "numbered_list_item",
        "quote",
        "divider",
        "code",
    ]
    assert children[0]["heading_1"]["rich_text"][0]["text"]["content"] == "Title"
    assert children[1]["paragraph"]["rich_text"][0]["text"]["content"] == "Paragraph text here."
    assert children[-1]["code"]["language"] == "python"


def test_append_page_body_markdown_heading_level_clamps_to_three():
    helper = NotionHelper("test-token")
    markdown = "#### Too Deep"

    with patch.object(NotionHelper, "_make_request", return_value={"ok": True}) as mock_request:
        helper.append_page_body("page-id", markdown)

    payload = mock_request.call_args.args[2]
    assert payload["children"][0]["type"] == "heading_3"
    assert payload["children"][0]["heading_3"]["rich_text"][0]["text"]["content"] == "Too Deep"
