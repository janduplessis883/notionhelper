# Notion 400 Fixes Implemented in Streamlit App

This document captures the fixes implemented to resolve:

`400 validation_error` on `PATCH /v1/blocks/{block_id}/children`

with errors like:

- `body.children[43].code.rich_text[0].text.content.length should be ≤ 2000`

## Problem Summary

The `Write to URL` flow used:

- `notion_blockify.Blockizer().convert(markdown)` to generate blocks
- `NotionHelper.append_page_body(page_id, blocks)` to send payload

`Blockizer` output is close to Notion format, but not always valid for write APIs.  
Notion rejects invalid/malformed fields at append time.

## Root Causes Identified

1. `rich_text` items could be malformed:
- missing required `"type": "text"`
- extra unsupported top-level `"href"` field

2. Unsupported heading levels:
- `heading_4` can be emitted but Notion supports `heading_1..heading_3` only

3. Text-length limit violations:
- Notion enforces max `2000` UTF-16 code units per `rich_text[].text.content`
- naive chunking by Python string length can still exceed Notion length when text contains multi-unit characters (e.g. emoji)

## Fixes Implemented

All changes were implemented in:

`/Users/janduplessis/code/janduplessis883/streamlit-projects/my-notionhelper-app/razor_db_create_new_page.py`

### 1) Block Sanitization Layer

Added `_sanitize_notion_block(block)` and changed `filter_valid_blocks(...)` to sanitize/normalize instead of pass-through.

What this does:
- validates each block has a supported type
- enforces canonical block shape:
  - `{"object":"block","type":"...","<type>":{...}}`
- drops unsupported/malformed blocks instead of sending invalid payload
- recursively sanitizes children where applicable

### 2) Rich Text Normalization

Added `_normalize_rich_text(items)` to rebuild rich_text entries into Notion-safe format.

What this does:
- guarantees each item includes:
  - `"type": "text"`
  - `"text": {"content": "..."}`
- moves links into `text.link.url` when available
- strips unsupported `href` as a top-level field
- normalizes annotations and defaults missing fields safely

### 3) Heading Level Remap

In sanitizer:
- remaps `heading_4+` to `heading_3`

This preserves content while preventing invalid block type errors.

### 4) 2000 Limit Fix (UTF-16 Safe Chunking)

Added:
- `_utf16_units(value)` to count UTF-16 code units
- `_chunk_text(value, 2000)` using UTF-16-aware splitting

Then `_normalize_rich_text(...)` uses this chunker so each generated text fragment satisfies Notion's real length validator.

## Why the Debug “First block” Message Was Misleading

`notionhelper` prints the first block on any 400 response, but the actual failure can be a later block.

In your logs, the true error was explicit:

- `body.children[43].code.rich_text[0].text.content.length ...`

So the `heading_1` block shown first was not necessarily the invalid block.

## Validation Performed

1. `python -m py_compile razor_db_create_new_page.py` passed.
2. Local checks confirmed rich_text chunking now caps each chunk at 2000 UTF-16 units.
3. Heading conversion and normalized payload structure verified on sample markdown.

## Porting Plan for notionhelper (Later)

If you want this in `notionhelper`, best approach is to add an optional preflight sanitizer in `append_page_body`:

1. Add utility module (example: `notionhelper/sanitize.py`) with:
- `sanitize_blocks(blocks: list[dict]) -> list[dict]`
- `normalize_rich_text(...)`
- UTF-16-safe chunking helpers

2. In `append_page_body(...)`:
- sanitize payload before request:
  - `payload = {"children": sanitize_blocks(blocks)}`

3. Improve 400 diagnostics:
- parse Notion `message` and extract `children[index]`
- print that specific failing block (not just block 0)

4. Keep compatibility switch:
- optional arg, e.g. `append_page_body(..., sanitize=True)`

## Suggested Additional Hardening in notionhelper

- Validate `code.language` against Notion-supported language names, fallback to `"plain text"`.
- Add unit tests for:
  - >2000 UTF-16 content
  - emoji/multi-unit characters
  - heading_4 remap
  - malformed rich_text repair
  - nested children sanitization

