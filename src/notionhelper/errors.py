from typing import Optional


class NotionAPIError(Exception):
    """Base exception for NotionHelper API failures."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        request_path: Optional[str] = None,
        notion_code: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_path = request_path
        self.notion_code = notion_code

    def __str__(self) -> str:
        details = []
        if self.status_code is not None:
            details.append(f"status={self.status_code}")
        if self.request_path:
            details.append(f"path={self.request_path}")
        if self.notion_code:
            details.append(f"code={self.notion_code}")
        suffix = f" ({', '.join(details)})" if details else ""
        return f"{self.message}{suffix}"


class AuthError(NotionAPIError):
    """Authentication or authorization error."""


class RateLimitError(NotionAPIError):
    """Rate limit error."""


class NotFoundError(NotionAPIError):
    """Object not found error."""


class ValidationError(NotionAPIError):
    """Validation or bad request error."""


class TimeoutError(NotionAPIError):
    """Request timeout error."""
