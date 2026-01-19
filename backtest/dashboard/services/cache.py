"""Caching layer for backtest and Monte Carlo results with disk persistence."""
import hashlib
import json
import os
import pickle
from collections import OrderedDict
from typing import Any, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from constants import CACHE_DIR


class ResultsCache:
    """Two-tier cache with disk persistence.

    Cache hierarchy: Memory (fast) -> Disk (persistent) -> Compute

    On startup, loads existing disk cache entries into memory.
    On set, writes to both memory and disk.
    On get, checks memory first, then disk (promoting to memory if found).
    """

    def __init__(self, cache_dir: str = CACHE_DIR):
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._cache_dir = cache_dir
        self._ensure_cache_dir()
        self._load_from_disk()

    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        os.makedirs(self._cache_dir, exist_ok=True)

    def _make_key(self, portfolio_id: str, config: dict) -> str:
        """Create a unique cache key from portfolio ID and config."""
        config_str = json.dumps(config, sort_keys=True)
        config_hash = hashlib.md5(config_str.encode()).hexdigest()[:12]
        return f"{portfolio_id}:{config_hash}"

    def _key_to_filename(self, key: str) -> str:
        """Convert cache key to safe filename."""
        safe_key = key.replace(':', '_')
        return os.path.join(self._cache_dir, f"{safe_key}.pkl")

    def _filename_to_key(self, filename: str) -> str:
        """Convert filename back to cache key."""
        base = os.path.basename(filename)
        if base.endswith('.pkl'):
            base = base[:-4]
        parts = base.rsplit('_', 1)
        if len(parts) == 2 and len(parts[1]) == 12:
            return f"{parts[0]}:{parts[1]}"
        return base.replace('_', ':')

    def _load_from_disk(self) -> None:
        """Load cached entries from disk on startup."""
        if not os.path.exists(self._cache_dir):
            return

        loaded = 0
        for f in os.listdir(self._cache_dir):
            if f.endswith('.pkl'):
                path = os.path.join(self._cache_dir, f)
                try:
                    with open(path, 'rb') as file:
                        data = pickle.load(file)
                    key = self._filename_to_key(path)
                    self._cache[key] = data
                    loaded += 1
                except (pickle.UnpicklingError, EOFError, OSError):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

        if loaded > 0:
            print(f"Loaded {loaded} cached results from disk")

    def _write_to_disk(self, key: str, result: Any) -> None:
        """Write a single cache entry to disk."""
        path = self._key_to_filename(key)
        try:
            with open(path, 'wb') as f:
                pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)
        except (OSError, pickle.PicklingError) as e:
            print(f"Warning: Failed to write cache to disk: {e}")

    def _read_from_disk(self, key: str) -> Optional[Any]:
        """Read a single cache entry from disk."""
        path = self._key_to_filename(key)

        if not os.path.exists(path):
            return None

        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError, OSError):
            try:
                os.remove(path)
            except OSError:
                pass
            return None

    def get(self, portfolio_id: str, config: dict) -> Optional[Any]:
        """Get cached result if available.

        Checks memory first, then disk. Promotes disk hits to memory.
        """
        key = self._make_key(portfolio_id, config)

        # Check memory cache
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]

        # Check disk cache
        result = self._read_from_disk(key)
        if result is not None:
            self._cache[key] = result
            return result

        return None

    def set(self, portfolio_id: str, config: dict, result: Any) -> None:
        """Cache a result to both memory and disk."""
        key = self._make_key(portfolio_id, config)
        self._cache[key] = result
        self._write_to_disk(key, result)

    def clear(self) -> None:
        """Clear both memory and disk cache."""
        self._cache.clear()

        if os.path.exists(self._cache_dir):
            for f in os.listdir(self._cache_dir):
                if f.endswith('.pkl'):
                    try:
                        os.remove(os.path.join(self._cache_dir, f))
                    except OSError:
                        pass

    def size(self) -> int:
        """Return current memory cache size."""
        return len(self._cache)

    def disk_size(self) -> int:
        """Return current disk cache size."""
        if not os.path.exists(self._cache_dir):
            return 0
        return len([f for f in os.listdir(self._cache_dir) if f.endswith('.pkl')])


# Global cache instance
results_cache = ResultsCache()
