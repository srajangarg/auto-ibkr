"""Base registry pattern for extensible item management."""
from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar('T')


class BaseRegistry(Generic[T]):
    """Generic registry for managing items by ID.

    Provides a centralized way to register, retrieve, and list items.
    New items can be added by calling register() with an item that has an 'id' attribute.
    """

    def __init__(self):
        self._items: dict[str, T] = {}

    def register(self, item: T) -> None:
        """Register an item."""
        item_id = item.id
        if item_id in self._items:
            raise ValueError(f"Item '{item_id}' already registered")
        self._items[item_id] = item

    def get(self, item_id: str) -> T:
        """Get item by ID."""
        if item_id not in self._items:
            raise KeyError(f"Item '{item_id}' not found")
        return self._items[item_id]

    def list_all(self) -> List[T]:
        """List all registered items."""
        return list(self._items.values())

    def list_by_category(self, category: str) -> List[T]:
        """List items in a specific category."""
        return [item for item in self._items.values() if item.category == category]

    def get_dropdown_options(self) -> List[dict]:
        """Get options formatted for Dash dropdown component."""
        return [
            {"label": item.display_name, "value": item.id}
            for item in self._items.values()
        ]

    def get_ids(self) -> List[str]:
        """Get list of all item IDs."""
        return list(self._items.keys())
