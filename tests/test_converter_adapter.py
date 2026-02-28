from typing import Any, Dict, List
from unittest.mock import patch

from notionhelper import NotionHelper
from notionhelper.converter_adapter import InternalConverterAdapter, NotionBlockifyAdapter


class _StubAdapter:
    def __init__(self, blocks: List[Dict[str, Any]], markdown: str = "stub-markdown") -> None:
        self._blocks = blocks
        self._markdown = markdown

    def markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        return self._blocks

    def blocks_to_markdown(self, blocks: List[Dict[str, Any]]) -> str:
        return self._markdown


def test_default_converter_is_blockify_adapter_with_fallback():
    helper = NotionHelper("test-token")
    assert isinstance(helper._converter_adapter, NotionBlockifyAdapter)


def test_set_converter_adapter_overrides_markdown_to_blocks():
    helper = NotionHelper("test-token")
    helper.set_converter_adapter(_StubAdapter(blocks=[{"type": "paragraph", "paragraph": {"rich_text": []}}]))

    blocks = helper._markdown_to_blocks("# Anything")
    assert blocks == [{"type": "paragraph", "paragraph": {"rich_text": []}}]


def test_get_page_markdown_uses_adapter_renderer():
    helper = NotionHelper("test-token")
    helper.set_converter_adapter(_StubAdapter(blocks=[], markdown="adapter-rendered"))

    with patch.object(NotionHelper, "_make_request") as mock_request:
        mock_request.side_effect = [
            {"properties": {"Name": {"title": []}}},
            {"results": [], "has_more": False, "next_cursor": None},
        ]
        result = helper.get_page("page-id", return_markdown=True)

    assert result["content"] == "adapter-rendered"


def test_blockify_adapter_falls_back_for_bad_table_parse():
    fallback = InternalConverterAdapter(
        markdown_to_blocks_fn=lambda markdown: [{"type": "table", "table": {"table_width": 2}}],
        blocks_to_markdown_fn=lambda blocks: "ok",
    )
    fake_module = type("FakeBlockify", (), {"convert": staticmethod(lambda markdown: [{"type": "paragraph"}])})
    adapter = NotionBlockifyAdapter(fallback=fallback, blockify_module=fake_module)

    markdown = "| Name | Owner |\n| --- | --- |\n| Q1 | Jane |"
    blocks = adapter.markdown_to_blocks(markdown)

    assert blocks[0]["type"] == "table"
