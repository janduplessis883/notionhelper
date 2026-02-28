from dataclasses import dataclass, field
from typing import Set
import random


@dataclass
class RetryPolicy:
    """Retry policy configuration for Notion API requests."""

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    jitter_ratio: float = 0.2
    timeout: float = 30.0
    retry_statuses: Set[int] = field(default_factory=lambda: {429, 500, 502, 503, 504})
    retry_on_timeout: bool = True
    retry_on_connection_error: bool = True

    def clamp(self) -> "RetryPolicy":
        self.max_retries = max(0, self.max_retries)
        self.base_delay = max(0.1, self.base_delay)
        self.max_delay = max(self.base_delay, self.max_delay)
        self.jitter_ratio = max(0.0, min(self.jitter_ratio, 1.0))
        self.timeout = max(1.0, self.timeout)
        return self

    def compute_delay(self, attempt: int, retry_after: float | None = None) -> float:
        if retry_after is not None and retry_after > 0:
            base = min(retry_after, self.max_delay)
        else:
            base = min(self.base_delay * (2 ** attempt), self.max_delay)
        jitter = random.uniform(0.0, base * self.jitter_ratio) if self.jitter_ratio > 0 else 0.0
        return min(base + jitter, self.max_delay)
