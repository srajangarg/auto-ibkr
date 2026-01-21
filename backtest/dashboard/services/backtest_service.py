"""Service layer for backtest and Monte Carlo simulations."""
import sys
import os
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import (
    HistoricalConfig,
    MonteCarloConfig,
    RFSchedule,
    SimulationResults,
    run_all,
)
from constants import (
    DEFAULT_INITIAL_AMT,
    DEFAULT_MONTHLY_CF,
    DEFAULT_START_DATE,
)
from ..portfolios.registry import registry
from ..simulations.registry import simulation_registry
from .cache import results_cache


def run_portfolio_analysis(
    portfolio_id: str,
    simulation_id: str = "stable_market",
    initial_amt: float = DEFAULT_INITIAL_AMT,
    monthly_cf: float = DEFAULT_MONTHLY_CF,
    start_date: str = DEFAULT_START_DATE,
    use_cache: bool = True,
    seed: int = 42
) -> SimulationResults:
    """Run historical backtest + Monte Carlo for a portfolio.

    Args:
        portfolio_id: ID of the portfolio from the registry
        simulation_id: ID of the simulation preset from the registry
        initial_amt: Initial investment amount
        monthly_cf: Monthly cash flow contribution
        start_date: Start date for historical backtest
        use_cache: Whether to use cached results
        seed: Random seed for reproducibility

    Returns:
        SimulationResults with historical and monte_carlo results

    Note:
        num_simulations and num_years are now taken from the simulation definition.
    """
    # Get simulation definition first to get num_simulations and num_years
    simulation_def = simulation_registry.get(simulation_id)

    config = {
        'simulation_id': simulation_id,
        'initial_amt': initial_amt,
        'monthly_cf': monthly_cf,
        'num_simulations': simulation_def.num_simulations,
        'num_years': simulation_def.num_years,
        'start_date': start_date,
        'seed': seed
    }

    # Check cache (key includes both portfolio_id and simulation_id via config)
    if use_cache:
        cached = results_cache.get(portfolio_id, config)
        if cached is not None:
            logger.info(f"Cache HIT: {portfolio_id} x {simulation_id}")
            return cached

    # Get portfolio definition
    portfolio_def = registry.get(portfolio_id)

    logger.info(f"Running: {portfolio_def.display_name} x {simulation_def.display_name} "
                f"({simulation_def.num_simulations} sims, {simulation_def.num_years}y)")
    start_time = time.time()

    # Configure
    historical_config = HistoricalConfig(start_date=start_date)
    mc_config = MonteCarloConfig(
        num_simulations=simulation_def.num_simulations,
        num_days=252 * simulation_def.num_years,
        tickers=portfolio_def.tickers,
        seed=seed,
        use_garch=simulation_def.use_garch,
        use_erp=simulation_def.use_erp,
        rf_schedule=simulation_def.rf_schedule,
        crash_config=simulation_def.crash_config
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

    elapsed = time.time() - start_time
    logger.info(f"Completed: {portfolio_def.display_name} x {simulation_def.display_name} in {elapsed:.1f}s")

    # Cache and return
    if use_cache:
        results_cache.set(portfolio_id, config, results)

    return results
