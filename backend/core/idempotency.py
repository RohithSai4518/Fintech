"""
Fintech Idempotency Module
Prevents duplicate financial executions (e.g. double-charging, repeat transfers)
via atomic in-flight locking and response caching.
"""

import time
import threading
from typing import Dict, Any, Optional, Tuple


class IdempotencyManager:
    """Thread-safe idempotency manager with TTL expiration and in-flight lock detection."""

    def __init__(self, default_ttl_seconds: int = 86400):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._locks: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._default_ttl = default_ttl_seconds

    def check_or_lock(self, idempotency_key: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Atomically inspects the idempotency key.
        Returns:
            (is_cached, cached_response)
            - If is_cached is True, cached_response contains the past result.
            - If is_cached is False, the key is now reserved/locked for processing.
        Raises:
            RuntimeError if the key is currently actively being processed by a concurrent thread.
        """
        with self._lock:
            self._cleanup_expired()
            now = time.time()

            # Check if cached result exists
            if idempotency_key in self._cache:
                entry = self._cache[idempotency_key]
                if entry["expires_at"] > now:
                    return True, entry["response"]
                else:
                    del self._cache[idempotency_key]

            # Check if currently locked / in-flight
            if idempotency_key in self._locks:
                lock_time = self._locks[idempotency_key]
                # If locked within last 30 seconds, treat as concurrent collision
                if now - lock_time < 30.0:
                    raise RuntimeError(f"Concurrent request in-flight for idempotency key '{idempotency_key}'")

            # Reserve key
            self._locks[idempotency_key] = now
            return False, None

    def store_result(self, idempotency_key: str, response: Dict[str, Any], ttl_seconds: Optional[int] = None) -> None:
        """Stores the execution outcome and releases the in-flight lock."""
        ttl = ttl_seconds or self._default_ttl
        with self._lock:
            self._cache[idempotency_key] = {
                "response": response,
                "expires_at": time.time() + ttl
            }
            if idempotency_key in self._locks:
                del self._locks[idempotency_key]

    def release_lock(self, idempotency_key: str) -> None:
        """Releases an in-flight lock on failure without caching a successful response."""
        with self._lock:
            if idempotency_key in self._locks:
                del self._locks[idempotency_key]

    def _cleanup_expired(self) -> None:
        """Removes expired entries from memory."""
        now = time.time()
        expired_keys = [k for k, v in self._cache.items() if v["expires_at"] <= now]
        for k in expired_keys:
            del self._cache[k]
        
        expired_locks = [k for k, v in self._locks.items() if now - v > 60.0]
        for k in expired_locks:
            del self._locks[k]
