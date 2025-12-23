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
4. Generates `combined_data.csv`.

**Note:** `backtester.py` will automatically run `combine_data.py` if `combined_data.csv` is missing.

## Core Components

- `constants.py`: Centralized file for shared constants like file paths, column names, and trading day assumptions.
- `backtester.py`: The main execution script. It defines:
    - `BasePortfolio`: Abstract base class for portfolio management.
    - `StaticPortfolio`: Rebalances to fixed target weights monthly.
    - `DynamicLeveragedPortfolio`: Adjusts leverage based on trailing volatility and target returns.
    - `Backtester`: The engine that iterates through historical data, applies returns, handles monthly cashflows, and calculates performance metrics (CAGR, Sharpe Ratio, Max Drawdown, etc.).

## How to Run

To run the default backtest comparison:

```bash
python backtester.py
```
