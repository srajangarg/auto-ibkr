import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def plot_realized_volatility(csv_path, ticker):
    """
    Calculates and plots the rolling 1-month, 2-month, and 3-month annualized realized volatility.
    """
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    # Load data
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.set_index('Date', inplace=True)

    if ticker not in df.columns:
        # Filter out known rate columns to suggest tickers
        rate_cols = ['10Y', '2Y', '3M']
        available_tickers = [c for c in df.columns if c not in rate_cols]
        print(f"Error: Ticker '{ticker}' not found in data.")
        print(f"Available tickers: {available_tickers}")
        return

    # Daily returns (the data in combined_data.csv seems to be daily returns already based on backtester.py)
    returns = pd.to_numeric(df[ticker], errors='coerce').fillna(0)
    
    # Define windows (approx 21 trading days per month)
    windows = {
        '1-Month': 21,
        '2-Month': 42,
        '3-Month': 63
    }
    
    plt.figure(figsize=(14, 7))
    
    for label, window in windows.items():
        # Realized volatility = std dev of returns * sqrt(252) for annualization
        rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)
        plt.plot(rolling_vol * 100, label=f'{label} ({window}d)')

    plt.title(f'Annualized Realized Volatility: {ticker}', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Annualized Volatility (%)', fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # Use a tight layout
    plt.tight_layout()
    
    output_filename = f"volatility_{ticker}.png"
    plt.savefig(output_filename)
    print(f"\nSuccess! Calculated volatility for {ticker}.")
    print(f"Plot saved as: {output_filename}")
    
    # Show last values
    print("\nLatest Realized Volatility (Annualized):")
    for label, window in windows.items():
        last_vol = returns.rolling(window=window).std().iloc[-1] * np.sqrt(252)
        print(f"  {label}: {last_vol*100:.2f}%")

if __name__ == "__main__":
    # Default to QQQ if no ticker provided
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else 'QQQ'
    data_file = "/home/garg/auto-ibkr/backtest/combined_data.csv"
    
    plot_realized_volatility(data_file, target_ticker)

