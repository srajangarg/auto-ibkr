"""Service layer for backtest and Monte Carlo simulations."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import (
    HistoricalConfig,
    MonteCarloConfig,
    SimulationResults,
    run_all,
)
from ..portfolios.registry import registry
from .cache import results_cache


DEFAULT_INITIAL_AMT = 10000
DEFAULT_MONTHLY_CF = 0
DEFAULT_MC_SIMULATIONS = 500
DEFAULT_MC_YEARS = 20
DEFAULT_START_DATE = '2005-01-01'


def run_portfolio_analysis(
    portfolio_id: str,
    initial_amt: float = DEFAULT_INITIAL_AMT,
    monthly_cf: float = DEFAULT_MONTHLY_CF,
    num_simulations: int = DEFAULT_MC_SIMULATIONS,
    num_years: int = DEFAULT_MC_YEARS,
    start_date: str = DEFAULT_START_DATE,
    use_cache: bool = True,
    seed: int = 42
) -> SimulationResults:
    """Run historical backtest + Monte Carlo for a portfolio.

    Args:
        portfolio_id: ID of the portfolio from the registry
        initial_amt: Initial investment amount
        monthly_cf: Monthly cash flow contribution
        num_simulations: Number of Monte Carlo simulations
        num_years: Length of each simulation in years
        start_date: Start date for historical backtest
        use_cache: Whether to use cached results
        seed: Random seed for reproducibility

    Returns:
        SimulationResults with historical and monte_carlo results
    """
    config = {
        'initial_amt': initial_amt,
        'monthly_cf': monthly_cf,
        'num_simulations': num_simulations,
        'num_years': num_years,
        'start_date': start_date,
        'seed': seed
    }

    # Check cache
    if use_cache:
        cached = results_cache.get(portfolio_id, config)
        if cached is not None:
            return cached

    # Get portfolio definition
    portfolio_def = registry.get(portfolio_id)

    # Configure
    historical_config = HistoricalConfig(start_date=start_date)
    mc_config = MonteCarloConfig(
        num_simulations=num_simulations,
        num_days=252 * num_years,
        tickers=portfolio_def.tickers,
        seed=seed
    )

    # Run
    results = run_all(
        historical_config=historical_config,
        mc_config=mc_config,
        portfolio_factory=portfolio_def.factory,
        initial_amt=initial_amt,
        monthly_cf=monthly_cf,
        verbose=False  # Don't print to console in web app
    )

    # Cache and return
    if use_cache:
        results_cache.set(portfolio_id, config, results)

    return results
