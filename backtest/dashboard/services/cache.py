"""Caching layer for backtest and Monte Carlo results."""
import hashlib
import json
from collections import OrderedDict
from typing import Any, Optional


class ResultsCache:
    """LRU cache for backtest and Monte Carlo results.

    Caches results by portfolio ID and configuration hash to avoid
    recomputing expensive Monte Carlo simulations.
    """

    def __init__(self, max_size: int = 32):
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._max_size = max_size

    def _make_key(self, portfolio_id: str, config: dict) -> str:
        """Create a unique cache key from portfolio ID and config."""
        config_str = json.dumps(config, sort_keys=True)
        config_hash = hashlib.md5(config_str.encode()).hexdigest()[:12]
        return f"{portfolio_id}:{config_hash}"

    def get(self, portfolio_id: str, config: dict) -> Optional[Any]:
        """Get cached result if available.

        Args:
            portfolio_id: Portfolio identifier
            config: Configuration dict (initial_amt, monthly_cf, etc.)

        Returns:
            Cached result or None if not found
        """
        key = self._make_key(portfolio_id, config)
        if key in self._cache:
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def set(self, portfolio_id: str, config: dict, result: Any) -> None:
        """Cache a result.

        Args:
            portfolio_id: Portfolio identifier
            config: Configuration dict
            result: Result to cache
        """
        key = self._make_key(portfolio_id, config)

        # Remove oldest if at capacity
        while len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)

        self._cache[key] = result

    def clear(self) -> None:
        """Clear all cached results."""
        self._cache.clear()

    def size(self) -> int:
        """Return current cache size."""
        return len(self._cache)


# Global cache instance
results_cache = ResultsCache()
