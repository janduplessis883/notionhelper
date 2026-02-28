from typing import Any, Callable, Dict, List, Optional, Protocol
import re

try:
    import notion_blockify  # type: ignore
except ImportError:
    notion_blockify = None


Block = Dict[str, Any]


class ConverterAdapter(Protocol):
    """Adapter interface for markdown/block conversion."""

    def markdown_to_blocks(self, markdown: str) -> List[Block]:
        ...

    def blocks_to_markdown(self, blocks: List[Block]) -> str:
        ...


class InternalConverterAdapter:
    """Internal converter used as fallback for critical block types."""

    def __init__(
        self,
        markdown_to_blocks_fn: Callable[[str], List[Block]],
        blocks_to_markdown_fn: Callable[[List[Block]], str],
    ) -> None:
        self._markdown_to_blocks_fn = markdown_to_blocks_fn
        self._blocks_to_markdown_fn = blocks_to_markdown_fn

    def markdown_to_blocks(self, markdown: str) -> List[Block]:
        return self._markdown_to_blocks_fn(markdown)

    def blocks_to_markdown(self, blocks: List[Block]) -> str:
        return self._blocks_to_markdown_fn(blocks)


class NotionBlockifyAdapter:
    """Primary adapter that tries notion_blockify, then falls back."""

    def __init__(
        self,
        fallback: ConverterAdapter,
        blockify_module: Any = None,
    ) -> None:
        self._fallback = fallback
        self._blockify_module = notion_blockify if blockify_module is None else blockify_module

    def markdown_to_blocks(self, markdown: str) -> List[Block]:
        converted = self._convert_with_blockify(markdown)
        if isinstance(converted, list):
            return converted
        return self._fallback.markdown_to_blocks(markdown)

    def blocks_to_markdown(self, blocks: List[Block]) -> str:
        # Keep reverse conversion stable via whichever renderer the app uses today.
        return self._fallback.blocks_to_markdown(blocks)

    def _convert_with_blockify(self, markdown: str) -> Optional[List[Block]]:
        if self._blockify_module is None:
            return None

        candidates = (
            "markdown_to_notion_blocks",
            "to_notion_blocks",
            "blockify",
            "convert",
        )
        for attr_name in candidates:
            converter = getattr(self._blockify_module, attr_name, None)
            if not callable(converter):
                continue
            try:
                converted = converter(markdown)
            except Exception:
                continue
            blocks = self._normalize_blocks(converted)
            if isinstance(blocks, list) and self._is_well_parsed(markdown, blocks):
                return blocks
        return None

    def _normalize_blocks(self, converted: Any) -> Optional[List[Block]]:
        if isinstance(converted, list):
            return converted
        if isinstance(converted, dict):
            for key in ("blocks", "children", "results"):
                value = converted.get(key)
                if isinstance(value, list):
                    return value
        return None

    def _is_well_parsed(self, markdown: str, converted_blocks: List[Block]) -> bool:
        extracted = self._collect_text(converted_blocks)
        if "**" in markdown and "**" in extracted:
            return False

        looks_like_table = bool(re.search(r"^\s*\|.+\|\s*$", markdown, flags=re.MULTILINE)) and bool(
            re.search(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", markdown, flags=re.MULTILINE)
        )
        if looks_like_table:
            has_table_block = any(isinstance(block, dict) and block.get("type") == "table" for block in converted_blocks)
            if not has_table_block:
                return False
        return True

    def _collect_text(self, blocks: List[Block]) -> str:
        texts: List[str] = []

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                text_obj = value.get("text")
                if isinstance(text_obj, dict):
                    content = text_obj.get("content")
                    if isinstance(content, str):
                        texts.append(content)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(blocks)
        return " ".join(texts)
