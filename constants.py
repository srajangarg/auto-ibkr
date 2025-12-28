import os

# Get the directory where this file (constants.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Fixed Constants
TRADING_DAYS_PER_YEAR = 252
DAYS_PER_YEAR = 365.25 # For CAGR calculation
DATA_START_DATE = '2000-01-01'  # Default start date for historical data

# File Paths
RATES_FILE = os.path.join(BASE_DIR, 'backtest', 'rates.csv')
RETURNS_FILE = os.path.join(BASE_DIR, 'backtest', 'returns.csv')
DATA_FILE = os.path.join(BASE_DIR, 'backtest', 'data', 'combined_data.csv')

# Column Names
DATE_COL = 'Date'
TOTAL_VALUE_COL = 'Total Value'
STRATEGY_RETURN_COL = 'Strategy Return'
SGOV_TICKER = 'SGOV'
T_BILL_3M_COL = '3M'
T_NOTE_2Y_COL = '2Y'
T_BOND_10Y_COL = '10Y'
RATE_COLS = [T_BOND_10Y_COL, T_NOTE_2Y_COL, T_BILL_3M_COL]

# Volatility Calculation
VOLATILITY_WINDOWS = {
    '1M': 21,
    '2M': 42,
    '3M': 63
}


# Investable Tickers
INVESTABLE_TICKERS = ['SPY', 'UPRO', 'QQQ', 'TQQQ', 'MINT', 'IEF', 'TLT', 'ETHA', 'IBIT', 'IWM', 'UWM'] # TODO: check is Fred Api is more stable
RISK_TICKERS = ['VIXCLS', 'VXNCLS', 'RVXCLS']  # VIX for SPY, VXN for QQQ, RVX for IWM
TICKER_PRICES_FILE = os.path.join(BASE_DIR, 'data', 'prices.csv')
TICKER_RETURNS_FILE = os.path.join(BASE_DIR, 'data', 'returns.csv')
TICKER_RISK_FILE = os.path.join(BASE_DIR, 'data', 'risk.csv')
