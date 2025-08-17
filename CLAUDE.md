# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NotionHelper is a Python library that provides a convenient interface for interacting with the Notion API. The library simplifies database management, page operations, file handling, and data conversion to Pandas DataFrames.

## Development Commands

### Package Management
- Uses `uv` for dependency management (see `uv.lock`)
- Install dependencies: `uv sync` or `uv sync --extra dev`
- Build package: `uv build`

### Testing
- Full pytest test suite with 21 tests covering all major functionality
- Run tests: `uv run pytest`
- Run with coverage: `uv run pytest --cov=src/notionhelper --cov-report=term-missing`
- Test configuration in `pytest.ini` and `pyproject.toml`
- Install test dependencies: `uv sync --extra test`

## Architecture

### Core Structure
- Main implementation: `src/notionhelper/helper.py`
- Single class `NotionHelper` contains all functionality
- Built on top of `notion-client`, `requests`, and `pandas`

### Key Components

**NotionHelper Class** (`src/notionhelper/helper.py:12`)
- Single entry point for all Notion API interactions
- Handles authentication via token-based auth
- Provides both basic API wrappers and convenience methods

**Database Operations**
- `get_database()` - retrieve database schema
- `create_database()` - create new databases
- `get_all_pages_as_json()` / `get_all_pages_as_dataframe()` - bulk data retrieval with pagination

**Page Operations** 
- `new_page_to_db()` - add pages to databases
- `append_page_body()` - add content blocks to pages
- `notion_get_page()` - retrieve page properties and blocks

**File Operations**
- `upload_file()` - raw file upload to Notion
- `attach_file_to_page()` / `embed_image_to_page()` - attach files/images to pages
- `one_step_*` methods - convenience functions combining upload + attachment

**Data Conversion**
- `get_all_pages_as_dataframe()` - converts Notion data to pandas DataFrame
- Handles 19+ Notion property types (title, status, number, date, etc.)
- Includes pagination support and optional page ID inclusion

### Authentication Pattern
- Requires `NOTION_TOKEN` environment variable
- Token passed to constructor: `NotionHelper(notion_token)`
- Uses notion-client's `Client(auth=token)` for API access

### Dependencies
- `notion-client>=2.4.0` - Official Notion API client
- `pandas>=2.3.1` - DataFrame operations 
- `requests>=2.32.4` - Direct API calls for file operations
- `mimetype>=0.1.5` - File type detection

## Development Notes

- The library uses synchronous operations only
- File uploads use Notion's file upload API with direct HTTP requests
- Pagination is handled automatically in bulk operations
- Property extraction supports most common Notion field types
- Complementary Streamlit app available for JSON construction: https://notioinapiassistant.streamlit.app