from unittest.mock import patch

from notionhelper import NotionHelper


def test_markdown_to_blocks_parses_inline_bold_annotations():
    helper = NotionHelper("test-token")
    blocks = helper._markdown_to_blocks("**For Monday morning**")

    assert len(blocks) == 1
    assert blocks[0]["type"] == "paragraph"
    rich_text = blocks[0]["paragraph"]["rich_text"]
    assert rich_text[0]["text"]["content"] == "For Monday morning"
    assert rich_text[0]["annotations"]["bold"] is True


def test_markdown_to_blocks_parses_simple_tables():
    helper = NotionHelper("test-token")
    markdown = "| Name | Owner |\n| --- | --- |\n| Q1 | Jane |\n| Q2 | Bob |"
    blocks = helper._markdown_to_blocks(markdown)

    assert len(blocks) == 1
    table_block = blocks[0]
    assert table_block["type"] == "table"
    assert table_block["table"]["table_width"] == 2
    assert len(table_block["table"]["children"]) == 3


def test_blocks_to_markdown_renders_table_blocks():
    helper = NotionHelper("test-token")
    blocks = [
        {
            "type": "table",
            "table": {
                "children": [
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Name"}, "annotations": {}}],
                                [{"type": "text", "text": {"content": "Owner"}, "annotations": {}}],
                            ]
                        },
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Q1"}, "annotations": {}}],
                                [{"type": "text", "text": {"content": "Jane"}, "annotations": {}}],
                            ]
                        },
                    },
                ]
            },
        }
    ]

    markdown = helper._blocks_to_markdown(blocks)
    assert "| Name | Owner |" in markdown
    assert "| --- | --- |" in markdown
    assert "| Q1 | Jane |" in markdown


def test_get_page_return_markdown_renders_table_children():
    helper = NotionHelper("test-token")
    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"properties": {"Name": {"title": []}}},
            {
                "results": [
                    {
                        "id": "table-1",
                        "type": "table",
                        "has_children": True,
                        "table": {"table_width": 2, "has_column_header": True, "has_row_header": False},
                    }
                ],
                "has_more": False,
                "next_cursor": None,
            },
            {
                "results": [
                    {
                        "id": "row-1",
                        "type": "table_row",
                        "has_children": False,
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Name"}, "annotations": {}}],
                                [{"type": "text", "text": {"content": "Owner"}, "annotations": {}}],
                            ]
                        },
                    },
                    {
                        "id": "row-2",
                        "type": "table_row",
                        "has_children": False,
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Q1"}, "annotations": {}}],
                                [{"type": "text", "text": {"content": "Jane"}, "annotations": {}}],
                            ]
                        },
                    },
                ],
                "has_more": False,
                "next_cursor": None,
            },
        ]
        result = helper.get_page("page-id", return_markdown=True)

    assert "| Name | Owner |" in result["content"]
    assert "| Q1 | Jane |" in result["content"]
