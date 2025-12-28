#!/usr/bin/env python3
"""
Daily data dump script for backtesting.
Fetches EOD closing prices and volatility measures from yfinance.
Writes returns to returns.csv and volatility measures to risk.csv.
Can be scheduled to run daily at market close via Task Scheduler or cron.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import os
import sys
import logging
from datetime import datetime, timedelta
from fredapi import Fred
from dotenv import load_dotenv
from typing import Optional
from datetime import date

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (
    INVESTABLE_TICKERS,
    RISK_TICKERS,
    DATE_COL,
    TICKER_PRICES_FILE,
    TICKER_RETURNS_FILE,
    TICKER_RISK_FILE,
    DATA_START_DATE
)
from utils.time_utils import get_latest_business_date, get_date_range

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_last_update_date(filepath: str) -> Optional[date]:
    """Get the last update date from existing CSV file."""
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath, index_col=DATE_COL, parse_dates=True)
            return df.index[-1].date()
        except Exception as e:
            logger.warning(f"Could not read {filepath}: {e}")
    return None

def fetch_price_data(tickers: list[str], start_date: date | pd.Timestamp | str, end_date: date | pd.Timestamp | str,
                     interval: str = '1d', column: str = None 
                     ) -> pd.DataFrame:
    """Fetch adjusted closing prices from yfinance."""
    logger.info(f"Fetching price data for {tickers} from {start_date} to {end_date}")
    data = yf.download(tickers, start=start_date, end=end_date, interval=interval, group_by="column")
    if column:
        data = data.xs(column, axis=1, level=0)
    
    # Handle single ticker case (yfinance returns Series instead of DataFrame)
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])
    
    return data

def fetch_vol_measures(vol_tickers: list[str], start_date: date | pd.Timestamp | str, end_date: date | pd.Timestamp | str,
                     interval: str = '1d', column: str = None 
                     ) -> pd.DataFrame:
    """Fetch volatility index data from yfinance."""
    logger.info(f"Fetching volatility measures: {vol_tickers} from {start_date} to {end_date}")
    
    # Load FRED API key from environment
    fred_api_key = os.getenv('FRED_API_KEY')
    if not fred_api_key:
        raise ValueError("FRED_API_KEY not found in environment. Please set it in .env file.")
    
    fred = Fred(api_key=fred_api_key)
    vol_data = pd.DataFrame()
    
    for vol_ticker in vol_tickers:
        data = fred.get_series(vol_ticker, observation_start=start_date, observation_end=end_date)
        data.index = pd.to_datetime(data.index)
        data.index.name = DATE_COL
        
        # Drop 'CLS' from ticker name for cleaner naming (e.g., VIXCLS -> VIX)
        data.name = vol_ticker.replace('CLS', '')
        logger.info(f"Fetched {vol_ticker} -> renamed to {data.name}")

        if vol_data.empty:
            vol_data = data.to_frame()
        else:
            vol_data = pd.concat([vol_data, data], axis=1)
    
    return vol_data

def calculate_returns(price_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate log returns from price data.
    Uses log returns (np.log(price).diff()) which are more robust than percentage returns.
    """
    try:
        # Compute log returns: ln(price_t / price_t-1)
        log_returns = np.log(price_data).diff()
        
        # Drop rows where all values are NaN
        log_returns = log_returns.dropna(how='all')
        
        logger.info(f"Calculated log returns with shape {log_returns.shape}")
        return log_returns
    except Exception as e:
        logger.error(f"Error calculating returns: {e}")
        raise

def update_data_file(data: pd.DataFrame, filepath: str, decimals: int = 6, fill_method: str = None) -> pd.DataFrame:
    """
    Generic function to update a CSV file with new data.
    
    Args:
        data: DataFrame to save
        filepath: Path to save to
        decimals: Number of decimal places to round to
        fill_method: Fill method - 'ffill' for forward fill, 'zero' for fillna(0), None for no fill
    
    Returns:
        Combined DataFrame (existing + new data)
    """
    logger.info(f"Updating {filepath}")
    
    # Round data to specified decimal places
    data = data.round(decimals)
    
    # Load existing file if it exists
    if os.path.exists(filepath):
        existing_df = pd.read_csv(filepath, index_col=DATE_COL, parse_dates=True)
        existing_df.index = pd.to_datetime(existing_df.index)
        logger.info(f"Loaded existing data with {len(existing_df)} rows")
        
        # Combine and remove duplicates (keep newest)
        combined_df = pd.concat([existing_df, data])
        combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
        combined_df = combined_df.sort_index()
    else:
        combined_df = data.sort_index()
        combined_df.index.name = DATE_COL
    
    # Apply fill method
    if fill_method == 'ffill':
        combined_df = combined_df.fillna(method='ffill')
        logger.info("Applied forward fill to data")
    elif fill_method == 'zero':
        combined_df = combined_df.fillna(0)
        logger.info("Filled NaN with 0")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to CSV
    combined_df.to_csv(filepath)
    logger.info(f"Saved {len(combined_df)} rows to {filepath}")
    logger.info(f"Date range: {combined_df.index[0].date()} to {combined_df.index[-1].date()}")
    
    return combined_df

def update_returns_file(returns_data: pd.DataFrame) -> pd.DataFrame:
    """Update returns.csv with log returns (rounded to 6 decimals, NaN not filled)."""
    return update_data_file(returns_data, TICKER_RETURNS_FILE, decimals=6, fill_method=None)

def update_risk_file(vol_data: pd.DataFrame) -> pd.DataFrame:
    """Update risk.csv with volatility measures (rounded to 2 decimals, forward filled)."""
    return update_data_file(vol_data, TICKER_RISK_FILE, decimals=2, fill_method='ffill')

def update_prices_file(price_data: pd.DataFrame) -> pd.DataFrame:
    """Update prices.csv with raw prices (rounded to 2 decimals, forward filled)."""
    return update_data_file(price_data, TICKER_PRICES_FILE, decimals=2, fill_method='ffill')

def main() -> None:
    """Main execution function."""
    try:
        logger.info("Starting daily data dump...")
        
        # Get the latest business date
        latest_business_date = get_latest_business_date()
        logger.info(f"Latest NYSE business date: {latest_business_date}")
        
        # ==================== PRICES ====================
        # Get last prices update date and fetch independently
        last_prices_date = get_last_update_date(TICKER_PRICES_FILE)
        
        if last_prices_date:
            logger.info(f"Last prices update: {last_prices_date}")
            prices_start_date = last_prices_date
        else:
            logger.info(f"No existing prices file found. Will fetch from {DATA_START_DATE}.")
            prices_start_date = pd.Timestamp(DATA_START_DATE)
        
        # Validate date range for prices
        prices_start_date, prices_end_date = get_date_range(prices_start_date, latest_business_date)
        logger.info(f"Fetching prices from {prices_start_date} to {prices_end_date}")
        
        # Fetch and update prices
        price_data = fetch_price_data(INVESTABLE_TICKERS, prices_start_date, prices_end_date, column='Close')
        if price_data.empty:
            logger.warning("No price data fetched. Market may be closed.")
            return
        
        logger.info(f"Fetched {len(price_data)} rows of price data")
        combined_prices = update_prices_file(price_data)
        
        # ==================== RETURNS ====================
        # Compute returns from the combined price data
        logger.info("Computing returns from combined price data")
        returns_data = calculate_returns(combined_prices)
        _ = update_returns_file(returns_data)
        
        # ==================== RISK/VOLATILITY ====================
        # Get last risk update date and fetch independently
        last_risk_date = get_last_update_date(TICKER_RISK_FILE)
        
        if last_risk_date:
            logger.info(f"Last risk update: {last_risk_date}")
            risk_start_date = last_risk_date
        else:
            logger.info(f"No existing risk file found. Will fetch from {DATA_START_DATE}.")
            risk_start_date = pd.Timestamp(DATA_START_DATE)
        
        # Validate date range for risk
        risk_start_date, risk_end_date = get_date_range(risk_start_date, latest_business_date)
        logger.info(f"Fetching volatility from {risk_start_date} to {risk_end_date}")
        
        # Fetch and update volatility measures
        vol_data = fetch_vol_measures(RISK_TICKERS, risk_start_date, risk_end_date)
        
        if vol_data.empty:
            logger.warning("No volatility data fetched.")
        else:
            logger.info(f"Fetched {len(vol_data)} rows of volatility data")
            _ = update_risk_file(vol_data)
        
        logger.info("Daily data dump completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during daily data dump: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
