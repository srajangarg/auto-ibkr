"""Portfolio registry for extensible portfolio management."""
from dataclasses import dataclass
from typing import Callable, List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backtester import BasePortfolio


@dataclass
class PortfolioDefinition:
    """Definition of a portfolio for the dashboard.

    Attributes:
        id: Unique identifier for the portfolio
        display_name: Human-readable name shown in UI
        description: Brief description of the strategy
        factory: Callable that returns a fresh portfolio instance
        tickers: List of tickers required for Monte Carlo simulation
        category: Category for grouping in UI (e.g., "static", "dynamic")
    """
    id: str
    display_name: str
    description: str
    factory: Callable[[], BasePortfolio]
    tickers: List[str]
    category: str = "default"


class PortfolioRegistry:
    """Registry for all available portfolios.

    Provides a centralized way to register, retrieve, and list portfolios.
    New portfolios can be added by calling register() with a PortfolioDefinition.
    """

    def __init__(self):
        self._portfolios: dict[str, PortfolioDefinition] = {}

    def register(self, definition: PortfolioDefinition) -> None:
        """Register a portfolio definition."""
        if definition.id in self._portfolios:
            raise ValueError(f"Portfolio '{definition.id}' already registered")
        self._portfolios[definition.id] = definition

    def get(self, portfolio_id: str) -> PortfolioDefinition:
        """Get portfolio definition by ID."""
        if portfolio_id not in self._portfolios:
            raise KeyError(f"Portfolio '{portfolio_id}' not found")
        return self._portfolios[portfolio_id]

    def list_all(self) -> List[PortfolioDefinition]:
        """List all registered portfolios."""
        return list(self._portfolios.values())

    def list_by_category(self, category: str) -> List[PortfolioDefinition]:
        """List portfolios in a specific category."""
        return [p for p in self._portfolios.values() if p.category == category]

    def get_dropdown_options(self) -> List[dict]:
        """Get options formatted for Dash dropdown component."""
        return [
            {"label": p.display_name, "value": p.id}
            for p in self._portfolios.values()
        ]

    def get_ids(self) -> List[str]:
        """Get list of all portfolio IDs."""
        return list(self._portfolios.keys())


# Global registry instance
registry = PortfolioRegistry()
