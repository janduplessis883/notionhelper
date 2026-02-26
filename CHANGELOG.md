# Changelog

All notable changes to this project are documented in this file.

## [0.5.4] - 2026-02-26

### Added
- Optional `notion_blockify` integration for markdown-to-Notion conversion with automatic fallback to the built-in parser.
- Table conversion coverage for markdown import/export and nested-table retrieval in `get_page(..., return_markdown=True)`.

### Changed
- Improved inline markdown parsing in `append_page_body(..., body=str)` to correctly render bold/italic/strikethrough/code/links as Notion rich text annotations.
- Added simple markdown table support in `_markdown_to_blocks`.
- Extended `_blocks_to_markdown` to render Notion `table` blocks back into markdown tables.
- `get_page` now hydrates nested child blocks recursively, enabling table row content to be included in markdown output.

## [0.5.3] - 2026-02-24

### Added
- `trash_page(page_id)` to move pages to Notion trash.
- `restore_page(page_id)` to restore pages from Notion trash.
- Unit tests covering page trash/restore request payloads.

### Changed
- Updated function reference docs for the new page trash APIs.

## [0.5.2] - 2026-02-24

### Added
- Tests for URL-preserving markdown conversion in rich text and URL-based block types.

### Changed
- Improved `_extract_rich_text` to preserve links from `text.link.url` and fallback to `plain_text` when needed.
- Extended `_blocks_to_markdown` URL rendering support for `bookmark`, `embed`, and `link_preview` blocks.

## [0.5.0] - 2026-02-22

### Added
- `append_page_body` now accepts raw Markdown (`str`) in addition to Notion block JSON.
- Optional `blocks=` backward-compatible keyword support for existing callers.
- Automatic batching in `append_page_body` with a default `batch_size=100` to align with Notion child append limits.
- Configurable request behavior via `NotionHelper(..., debug, max_retries, retry_base_delay, request_timeout)`.
- Retry/backoff handling for transient HTTP errors (`429`, `500`, `502`, `503`, `504`) and transient request exceptions.

### Changed
- `get_page` now paginates block-children requests to return full page body content instead of only the first page of blocks.
- API error diagnostics now use structured logging and include targeted failing child block details when available.
- `append_page_body` continues to sanitize payloads by default before writes to reduce Notion 400 validation errors.

## [0.5.1] - 2026-02-22

### Added
- `extract_page_id_from_url(page_url_or_id, with_hyphens=True)` to extract and normalize page IDs from Notion URLs or raw IDs.

### Changed
- Release metadata and lockfile updated for `0.5.1`.
