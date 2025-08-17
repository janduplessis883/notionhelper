# Testing Guide for NotionHelper

This directory contains comprehensive tests for the NotionHelper package using pytest.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest fixtures and configuration
├── test_helper.py       # Main test suite for NotionHelper class
└── README.md           # This file
```

## Running Tests

### Prerequisites

Install test dependencies:

```bash
# Install with test dependencies
uv install --extra test

# Or install dev dependencies (includes testing + linting tools)
uv install --extra dev
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_helper.py

# Run specific test class
pytest tests/test_helper.py::TestNotionHelper

# Run specific test method
pytest tests/test_helper.py::TestNotionHelper::test_get_database_success
```

### Test Coverage

```bash
# Run tests with coverage report
pytest --cov=src/notionhelper

# Generate HTML coverage report
pytest --cov=src/notionhelper --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
```

### Test Markers

Tests are organized with custom markers:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests  
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run only network-related tests
pytest -m network
```

## Test Categories

### Unit Tests (`TestNotionHelper`)
Tests individual methods in isolation with mocked dependencies:
- `test_init()` - Constructor testing
- `test_get_database_success()` - Database retrieval
- `test_new_page_to_db()` - Page creation  
- `test_upload_file_success()` - File upload functionality
- `test_one_step_*()` - Convenience method testing

### Integration Tests (`TestNotionHelperIntegration`) 
Tests multiple components working together:
- `test_file_workflow()` - Complete file upload and attachment process

### Error Handling Tests (`TestNotionHelperErrorHandling`)
Tests error scenarios and exception handling:
- `test_upload_file_network_error()` - Network failure scenarios
- `test_upload_file_http_error()` - HTTP error responses
- `test_get_database_failure()` - API failure handling

## Test Fixtures

The `conftest.py` file provides reusable fixtures:

- `mock_notion_token` - Safe test token
- `notion_helper` - Pre-configured NotionHelper instance
- `sample_database_id` / `sample_page_id` - Test IDs
- `sample_database_schema` - Mock database structure
- `sample_page_properties` - Mock page data
- `sample_blocks` - Mock content blocks
- `temporary_test_file` - Real temporary files for testing
- `mock_requests` - Mocked HTTP requests
- `mock_notion_client` - Fully mocked Notion client

## Mocking Strategy

Tests use comprehensive mocking to avoid real API calls:

1. **Notion Client Mocking**: All `notion-client` interactions are mocked
2. **HTTP Request Mocking**: All `requests` calls are intercepted  
3. **File System Mocking**: File operations use temporary files or mocks
4. **Environment Isolation**: Tests run with safe test tokens

## Configuration

### pytest.ini
Basic pytest configuration with coverage settings.

### pyproject.toml 
Advanced pytest configuration including:
- Test discovery patterns
- Coverage reporting (80% minimum)
- Custom markers
- Warning filters

## Writing New Tests

When adding new tests:

1. **Use appropriate fixtures** from `conftest.py`
2. **Mock external dependencies** (API calls, file system)
3. **Add descriptive docstrings** explaining test purpose
4. **Use proper markers** (`@pytest.mark.unit`, etc.)
5. **Test both success and failure scenarios**
6. **Follow naming convention**: `test_method_name_scenario`

### Example Test Structure

```python
class TestNewFeature:
    """Test cases for new feature."""
    
    def test_new_method_success(self, notion_helper, mock_notion_client):
        """Test successful execution of new method."""
        # Arrange
        mock_notion_client.some_api.return_value = {"success": True}
        
        # Act
        result = notion_helper.new_method("test_param")
        
        # Assert
        assert result["success"] is True
        mock_notion_client.some_api.assert_called_once_with("test_param")
        
    def test_new_method_failure(self, notion_helper, mock_notion_client):
        """Test error handling in new method."""
        # Arrange
        mock_notion_client.some_api.side_effect = Exception("API Error")
        
        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            notion_helper.new_method("test_param")
```

## Continuous Integration

Tests are configured to run automatically via GitHub Actions with:
- Multiple Python versions (3.10+)
- Coverage reporting
- Test result artifacts

## Debugging Tests

```bash
# Run with Python debugger
pytest --pdb

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run with detailed output
pytest -vvv --tb=long
```