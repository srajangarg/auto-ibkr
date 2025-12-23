# Fixed Constants
TRADING_DAYS_PER_YEAR = 252
DAYS_PER_YEAR = 365.25 # For CAGR calculation

# File Paths
RATES_FILE = 'backtest/rates.csv'
RETURNS_FILE = 'backtest/returns.csv'
COMBINED_FILE = 'backtest/combined_data.csv'

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
