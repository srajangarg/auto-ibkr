"""Predefined portfolio configurations."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backtester import StaticPortfolio, DynamicLeveragedPortfolio
from .registry import PortfolioDefinition, registry


# Portfolio 1: QQQ (100%)
registry.register(PortfolioDefinition(
    id="qqq_100",
    display_name="QQQ (100%)",
    description="100% allocation to QQQ (unleveraged)",
    factory=lambda: StaticPortfolio({'QQQ': 100}),
    tickers=['QQQ'],
    category="static"
))

# Portfolio 2: 1.5x Leveraged QQQ
# 75% QQQ + 25% QQQx3 = 0.75*1x + 0.25*3x = 1.5x effective leverage
registry.register(PortfolioDefinition(
    id="qqq_1_5x",
    display_name="1.5x Leveraged QQQ",
    description="75% QQQ + 25% QQQx3 for 1.5x effective leverage",
    factory=lambda: StaticPortfolio({'QQQ': 75, 'QQQx3': 25}),
    tickers=['QQQ', 'QQQx3'],
    category="static"
))

# Portfolio 3: 2x Leveraged QQQ
# 50% QQQ + 50% QQQx3 = 0.5*1x + 0.5*3x = 2x effective leverage
registry.register(PortfolioDefinition(
    id="qqq_2x",
    display_name="2x Leveraged QQQ",
    description="50% QQQ + 50% QQQx3 for 2x effective leverage",
    factory=lambda: StaticPortfolio({'QQQ': 50, 'QQQx3': 50}),
    tickers=['QQQ', 'QQQx3'],
    category="static"
))

# Portfolio 4: Dynamic Leveraged QQQ
# Adjusts leverage based on trailing volatility
registry.register(PortfolioDefinition(
    id="qqq_dynamic",
    display_name="Dynamic Leveraged QQQ",
    description="Volatility-adjusted leverage (alpha=0, beta=0.7, target=12%)",
    factory=lambda: DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12),
    tickers=['QQQ', 'QQQx3'],
    category="dynamic"
))
