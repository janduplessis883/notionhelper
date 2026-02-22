# Changelog

All notable changes to this project are documented in this file.

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
