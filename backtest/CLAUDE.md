# Backtest Module

This directory contains a backtesting engine for evaluating trading strategies using historical data.

## Data Sources

- `rates.csv`: Historical treasury yields (10Y, 2Y, 3M) downloaded from [testfol.io](https://testfol.io/).
- `returns.csv`: Historical price levels/returns for various tickers (e.g., QQQ, QQQx3) downloaded from [testfol.io](https://testfol.io/). You can use QQQ?L=3 to get the simulated version of 3x leveraged QQQ. I have compared it against TQQQ on the available dates and it tracks very well. Same for SOXX?L=3 and SOXL

## Data Preparation

Before running a backtest, the raw data files need to be combined and processed.
`combine_data.py` performs the following tasks:
1. Merges `rates.csv` and `returns.csv`.
2. Calculates SGOV daily returns from 3M T-Bill rates.
3. Calculates realized volatility for various windows (1M, 2M, 3M) for use in dynamic leverage strategies.
4. Generates `data/combined_data.csv`.

**Note:** `backtester.py` will automatically run `combine_data.py` if `data/combined_data.csv` is missing.

## Core Components

- `constants.py`: Centralized file for shared constants like file paths, column names, and trading day assumptions.
- `backtester.py`: The main execution script. It defines:
    - `BasePortfolio`: Abstract base class for portfolio management.
    - `StaticPortfolio`: Rebalances to fixed target weights monthly.
    - `DynamicLeveragedPortfolio`: Adjusts leverage based on trailing volatility and target returns.
    - `Backtester`: The engine that iterates through historical data, applies returns, handles monthly cashflows, and calculates performance metrics (CAGR, Sharpe Ratio, Max Drawdown, etc.).
- `parameter_sweep.py`: A utility script to find optimal strategy parameters.
    - Runs simulations across ranges of `alpha` and `beta`.
    - Includes "Special Case" configurations for comparison (e.g., fixed leverage benchmarks).
    - Saves results to the `results/` directory for analysis.
- `monte_carlo.py`: Monte Carlo simulation module.
    - `BacktestResult`: Dataclass holding metrics from a single backtest (CAGR, Sharpe, drawdown, etc.).
    - `SimulationResults`: Container with `historical` and `monte_carlo` (list of n results), plus distribution analysis and plotting.
    - `MonteCarloConfig`: Configuration for MC simulations (num_simulations, num_days, tickers, optional param overrides).
    - `HistoricalConfig`: Configuration for historical backtest (csv_path, date range).
    - `RFSchedule`: Risk-free rate schedule (constant, increasing, decreasing, v_shape, inverse_v).
    - `run_all()`: Runs historical backtest + Monte Carlo simulations and returns `SimulationResults`.
    - **Advanced features**:
        - GARCH(1,1) volatility dynamics (`use_garch=True`)
        - Time-varying risk-free rates via `RFSchedule`
        - Equity risk premium modeling (`use_erp=True`): ties equity returns to RF rate

## How to Run

### Default Comparison
To run the default backtest comparison between static and dynamic portfolios:

```bash
python backtester.py
```

### Parameter Sweep
To find optimal parameters for the `DynamicLeveragedPortfolio`:

```bash
python parameter_sweep.py
```

Results will be saved to `backtest/results/sweep_results_<TICKER>_cf<CASHFLOW>.csv`.

### Monte Carlo Simulation
To run Monte Carlo simulations:

```python
from monte_carlo import MonteCarloConfig, RFSchedule, HistoricalConfig, run_all
from backtester import DynamicLeveragedPortfolio

historical_config = HistoricalConfig(start_date='2005-01-01')

mc_config = MonteCarloConfig(
    num_simulations=1000,
    num_days=252 * 20,  # 20 years
    tickers=['QQQ', 'QQQx3'],

    # GARCH(1,1) volatility (auto-fits params from historical data)
    use_garch=True,

    # RF rate schedule: 'constant', 'increasing', 'decreasing', 'v_shape', 'inverse_v'
    rf_schedule=RFSchedule(
        schedule_type='v_shape',  # like 2020s: rates fell then rose
        start_rate=0.04,
        end_rate=0.05,
        midpoint_rate=0.01
    ),

    # Equity Risk Premium: equity_return = rf + ERP
    use_erp=True,

    seed=42
)

def make_portfolio():
    return DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12)

results = run_all(historical_config, mc_config, make_portfolio, initial_amt=10000, monthly_cf=200)

# View summary statistics
print(results.summary())

# Plot distribution of any metric with historical as vertical line
results.plot_distribution('cagr')
```

**Features:**
- **GARCH(1,1)**: Models volatility clustering. Params auto-fit from historical data using `arch` library.
- **RF Schedules**: `constant`, `increasing`, `decreasing`, `v_shape`, `inverse_v`
- **Equity Risk Premium**: When `use_erp=True`, expected equity return = RF + ERP
