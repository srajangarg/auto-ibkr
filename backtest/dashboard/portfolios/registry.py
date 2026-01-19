"""Portfolio registry for extensible portfolio management."""
from dataclasses import dataclass
from typing import Callable, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backtester import BasePortfolio
from ..registry_base import BaseRegistry


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


# Global registry instance
registry = BaseRegistry[PortfolioDefinition]()
