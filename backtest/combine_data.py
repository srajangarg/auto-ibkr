import pandas as pd
import numpy as np

def combine_and_convert():
    # Load the datasets
    rates_df = pd.read_csv('backtest/rates.csv')
    returns_df = pd.read_csv('backtest/returns.csv')

    # Convert Date columns to datetime objects
    rates_df['Date'] = pd.to_datetime(rates_df['Date'])
    returns_df['Date'] = pd.to_datetime(returns_df['Date'])

    # Set Date as index
    rates_df.set_index('Date', inplace=True)
    returns_df.set_index('Date', inplace=True)

    # Rename and filter treasury yield columns
    rates_df = rates_df.rename(columns={
        '10Y Treasury Yield': '10Y',
        '2Y Treasury Yield': '2Y',
        '3M T-Bill Rate': '3M'
    })
    # Keep only the renamed columns
    rates_df = rates_df[['10Y', '2Y', '3M']]

    # Calculate SGOV daily return from 3M rate (approximate as annual rate / 100 / 252)
    rates_df['SGOV'] = rates_df['3M'] / 100 / 252

    # Convert price levels to daily returns
    # The returns.csv contains price-like levels starting at 10000
    # Daily return = (price_today / price_yesterday) - 1
    daily_returns_df = returns_df.pct_change()

    # Calculate realized volatility for non-leveraged tickers
    windows = {'1M': 21, '2M': 42, '3M': 63}
    # Filter out leveraged tickers (containing 'x2', 'x3', etc.)
    tickers = [col for col in daily_returns_df.columns if not any(x in col.lower() for x in ['x2', 'x3'])]
    
    for ticker in tickers:
        for label, window in windows.items():
            col_name = f"{ticker}_rvol_{label}"
            # Annualized Realized Volatility = std dev of daily returns * sqrt(252)
            daily_returns_df[col_name] = daily_returns_df[ticker].rolling(window=window).std() * np.sqrt(252)

    # Combine the dataframes
    combined_df = rates_df.join(daily_returns_df, how='inner')

    # Drop the first row which will have NaN for returns
    combined_df.dropna(inplace=True)

    # Save to a new file
    output_path = 'backtest/combined_data.csv'
    combined_df.to_csv(output_path)
    
    print(f"Successfully combined data and saved to {output_path}")
    print("\nFirst few rows of combined data:")
    print(combined_df.head())

if __name__ == "__main__":
    combine_and_convert()

