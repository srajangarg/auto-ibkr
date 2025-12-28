"""
Dump model data: correlation, expected returns, and expected volatility.

This module calculates:
1. Correlation: EWM with halflife=2 years from weekly returns
2. Expected Returns: EWM with halflife=0.5 years
3. Expected Std Dev: Historical (EWM hl=0.5 years) and implied volatility
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (
    INVESTABLE_TICKERS,
    RISK_TICKERS,
    TICKER_RETURNS_FILE,
    TICKER_RISK_FILE,
    DATE_COL,
)
from utils.time_utils import get_latest_business_date

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# TODO: improve the volatility prediction model
# Implied volatility mapping
IMPLIED_VOL_MAP = {
    'ETHA': ('VIX', 3.0),
    'IBIT': ('VIX', 2.8),
    'IEF': ('fixed', 0.07),
    'IWM': ('RVX', 1.0),
    'MINT': ('fixed', 0.0),
    'QQQ': ('VXN', 1.0),
    'SPY': ('VIX', 1.0),
    'TLT': ('fixed', 0.14),
    'TQQQ': ('VXN', 3.2),
    'UPRO': ('VIX', 3.2),
    'UWM': ('RVX', 2.1),
}


def calculate_correlation(weekly_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate rolling EWM correlation with halflife=2 years from weekly returns.
    
    Args:
        weekly_returns: Weekly returns DataFrame
    
    Returns:
        Full time series of correlation matrices (MultiIndex DataFrame)
    """
    logger.info("Calculating correlation matrix")
    
    # Calculate EWM correlation (halflife = 2 years = 104 weeks)
    ewm_corr = weekly_returns.ewm(halflife=2*52).corr().dropna(how='all')
    
    logger.info(f"Correlation time series with {len(ewm_corr.index.get_level_values(0).unique())} dates")
    
    return ewm_corr


def expected_historical_returns(weekly_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate historical returns as rolling mean over last 10 years, annualized.
    
    Args:
        weekly_returns: Weekly returns DataFrame
    
    Returns:
        DataFrame with returns for each week and ticker
    """
    logger.info("Calculating historical returns (last 10 years)")
    
    # Rolling mean over last 10 years (52*10 weeks), annualized by 52
    window = 52 * 10
    hist_returns = weekly_returns.rolling(window=window).mean() * 52
    hist_returns.index.name = DATE_COL
    
    logger.info(f"Historical returns time series: {len(hist_returns)} weeks, {len(hist_returns.columns)} tickers")
    
    return hist_returns


def expected_historical_volatility(weekly_returns: pd.DataFrame, risk_measures: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate historical volatility time series: historical (EWM hl=0.5 years) and implied.
    
    Args:
        weekly_returns: Weekly returns DataFrame
        risk_measures: DataFrame with VIX, VXN, RVX columns
    
    Returns:
        DataFrame with <ticker>_hist and <ticker>_impl columns for each week
    """
    logger.info("Calculating historical volatility time series")
    
    # Historical volatility: annualized EWM std (halflife = 0.5 years = 26 weeks), annualized by sqrt(52)
    ewm_std = weekly_returns.ewm(halflife=0.5*52).std() * np.sqrt(52)
    
    exp_vol = pd.DataFrame(index=weekly_returns.index)
    
    # Add historical std columns
    for ticker in weekly_returns.columns:
        exp_vol[f'{ticker}_hist'] = ewm_std[ticker]
    
    # Implied volatility time series
    implied_vol = pd.DataFrame(index=risk_measures.index)
    for ticker, (source, multiplier) in IMPLIED_VOL_MAP.items():
        if source == 'fixed':
            implied_vol[f'{ticker}_impl'] = multiplier
        elif source in ['VIX', 'VXN', 'RVX']:
            if source in risk_measures.columns:
                implied_vol[f'{ticker}_impl'] = (risk_measures[source] / 100) * multiplier
            else:
                logger.warning(f"Risk measure '{source}' not found for {ticker}")
                implied_vol[f'{ticker}_impl'] = np.nan
        else:
            logger.warning(f"Unknown source '{source}' for {ticker}")
            implied_vol[f'{ticker}_impl'] = np.nan
    
    # Align implied vol with weekly returns dates and merge
    implied_vol_aligned = implied_vol.reindex(weekly_returns.index, method='ffill')
    for col in implied_vol.columns:
        exp_vol[col] = implied_vol_aligned[col]
    
    exp_vol.index.name = DATE_COL
    logger.info(f"Historical volatility time series: {len(exp_vol)} weeks, {len(exp_vol.columns)} columns")
    
    return exp_vol


def dump_correlation(weekly_returns: pd.DataFrame, output_dir: str = 'data') -> None:
    """
    Dump correlation time series to parquet.
    
    Args:
        weekly_returns: Weekly returns DataFrame
        output_dir: Directory to save files
    """
    filepath = os.path.join(output_dir, 'correlation.parquet')
    corr_matrix = calculate_correlation(weekly_returns)
    
    os.makedirs(output_dir, exist_ok=True)
    corr_matrix.to_parquet(filepath)
    logger.info(f"Saved correlation matrix to {filepath}")


def dump_expected_returns(weekly_returns: pd.DataFrame, output_dir: str = 'data') -> None:
    """
    Dump historical returns time series to parquet.
    
    Args:
        weekly_returns: Weekly returns DataFrame
        output_dir: Directory to save files
    """
    filepath = os.path.join(output_dir, 'expected_returns.parquet')
    hist_ret = expected_historical_returns(weekly_returns)
    
    os.makedirs(output_dir, exist_ok=True)
    hist_ret.to_parquet(filepath)
    logger.info(f"Saved historical returns to {filepath}")


def dump_expected_volatility(weekly_returns: pd.DataFrame, risk_measures: pd.DataFrame, output_dir: str = 'data') -> None:
    """
    Dump historical volatility time series to parquet.
    
    Args:
        weekly_returns: Weekly returns DataFrame
        risk_measures: DataFrame with VIX, VXN, RVX columns
        output_dir: Directory to save files
    """
    filepath = os.path.join(output_dir, 'expected_volatility.parquet')
    exp_vol = expected_historical_volatility(weekly_returns, risk_measures)
    
    os.makedirs(output_dir, exist_ok=True)
    exp_vol.to_parquet(filepath)
    logger.info(f"Saved historical volatility to {filepath}")


def main() -> None:
    """Main function to dump all model data."""
    logger.info("Starting model data dump")
    
    try:
        # Load data
        logger.info("Loading returns data")
        returns = pd.read_csv(TICKER_RETURNS_FILE, index_col=DATE_COL, parse_dates=True)
        
        logger.info("Loading risk measures data")
        risk_measures = pd.read_csv(TICKER_RISK_FILE, index_col=DATE_COL, parse_dates=True)
        
        # Dump all model data
        weekly_returns = returns.resample('W').sum(min_count=1)
        dump_correlation(weekly_returns)
        dump_expected_returns(weekly_returns)
        dump_expected_volatility(weekly_returns, risk_measures)
        
        logger.info("Model data dump completed successfully")
    
    except Exception as e:
        logger.error(f"Error during model data dump: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
