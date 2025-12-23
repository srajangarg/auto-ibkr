#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Add the current directory to sys.path to allow importing constants
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from constants import (
    TRADING_DAYS_PER_YEAR,
    RATES_FILE,
    RETURNS_FILE,
    DATA_FILE,
    DATE_COL,
    T_BILL_3M_COL,
    T_NOTE_2Y_COL,
    T_BOND_10Y_COL,
    SGOV_TICKER,
    VOLATILITY_WINDOWS
)

def combine_and_convert():
    # Load the datasets
    rates_df = pd.read_csv(RATES_FILE)
    returns_df = pd.read_csv(RETURNS_FILE)

    # Convert Date columns to datetime objects
    rates_df[DATE_COL] = pd.to_datetime(rates_df[DATE_COL])
    returns_df[DATE_COL] = pd.to_datetime(returns_df[DATE_COL])

    # Set Date as index
    rates_df.set_index(DATE_COL, inplace=True)
    returns_df.set_index(DATE_COL, inplace=True)

    # Rename and filter treasury yield columns
    rates_df = rates_df.rename(columns={
        '10Y Treasury Yield': T_BOND_10Y_COL,
        '2Y Treasury Yield': T_NOTE_2Y_COL,
        '3M T-Bill Rate': T_BILL_3M_COL
    })
    # Keep only the renamed columns
    rates_df = rates_df[[T_BOND_10Y_COL, T_NOTE_2Y_COL, T_BILL_3M_COL]]

    # Calculate SGOV daily return from 3M rate (approximate as annual rate / 100 / TRADING_DAYS_PER_YEAR)
    rates_df[SGOV_TICKER] = rates_df[T_BILL_3M_COL] / 100 / TRADING_DAYS_PER_YEAR

    # Convert price levels to daily returns
    # The returns.csv contains price-like levels starting at 10000
    # Daily return = (price_today / price_yesterday) - 1
    daily_returns_df = returns_df.pct_change()

    # Calculate realized volatility for non-leveraged tickers
    # Filter out leveraged tickers (containing 'x2', 'x3', etc.)
    tickers = [col for col in daily_returns_df.columns if not any(x in col.lower() for x in ['x2', 'x3'])]
    
    for ticker in tickers:
        for label, window in VOLATILITY_WINDOWS.items():
            col_name = f"{ticker}_rvol_{label}"
            # Annualized Realized Volatility = std dev of daily returns * sqrt(TRADING_DAYS_PER_YEAR)
            daily_returns_df[col_name] = daily_returns_df[ticker].rolling(window=window).std() * np.sqrt(TRADING_DAYS_PER_YEAR)

    # Combine the dataframes
    combined_df = rates_df.join(daily_returns_df, how='inner')

    # Drop the first row which will have NaN for returns
    combined_df.dropna(inplace=True)

    # Save to a new file
    combined_df.to_csv(DATA_FILE)


if __name__ == "__main__":
    combine_and_convert()

