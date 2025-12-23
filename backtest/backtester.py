import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import os
import sys

# Add the current directory to sys.path to allow importing constants
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from constants import (
    TRADING_DAYS_PER_YEAR,
    DAYS_PER_YEAR,
    COMBINED_FILE,
    DATE_COL,
    TOTAL_VALUE_COL,
    STRATEGY_RETURN_COL,
    T_BILL_3M_COL,
    RATE_COLS,
    SGOV_TICKER
)

class BasePortfolio(ABC):
    def __init__(self):
        self.positions = {} # asset_name -> dollar_value

    def total_value(self):
        return sum(self.positions.values())

    def update_positions(self, returns_row):
        """Applies daily returns to current positions."""
        for asset in self.positions:
            if asset in returns_row:
                self.positions[asset] *= (1 + returns_row[asset])

    @abstractmethod
    def rebalance(self, date, cash_to_add=0, row=None):
        """Logic to redistribute current value + extra_cash into self.positions."""
        pass

class StaticPortfolio(BasePortfolio):
    WEIGHT_TOLERANCE = 1e-6

    def __init__(self, target_weights):
        super().__init__()
        # Validate weights
        total_weight = sum(target_weights.values())
        if abs(total_weight - 100) > self.WEIGHT_TOLERANCE:
            raise ValueError(f"Weights must add up to 100%, got {total_weight}")
        self.target_weights = {k: v / 100.0 for k, v in target_weights.items()}

    def rebalance(self, date, cash_to_add=0, row=None):
        current_total = self.total_value() + cash_to_add
        self.positions = {asset: current_total * weight for asset, weight in self.target_weights.items()}

class DynamicLeveragedPortfolio(BasePortfolio):
    LEVERAGE_MIN = 0.5
    LEVERAGE_MAX = 2.0
    LEVERAGE_THRESHOLD = 1.0
    TICKER_X3_MULTIPLIER = 3.0
    SGOV_TICKER = 'SGOV'

    def __init__(self, ticker, alpha, beta, target_return, vol_period):
        """
        Dynamic leverage based on volatility and excess return.
        desired_leverage = alpha + beta * (target_return - RF) / (vol**2)
        """
        super().__init__()
        self.ticker = ticker
        self.ticker3 = f"{ticker}x{int(self.TICKER_X3_MULTIPLIER)}"
        self.alpha = alpha
        self.beta = beta
        self.target_return = target_return
        self.vol_period = vol_period # '1M', '2M', or '3M'

    def rebalance(self, date, cash_to_add=0, row=None):
        current_total = self.total_value() + cash_to_add
        
        if row is None:
            return

        # T-Bill rate as proxy for risk-free rate (RF)
        rf = row[T_BILL_3M_COL] / 100.0
        vol_col = f"{self.ticker}_rvol_{self.vol_period}"
        vol = row.get(vol_col, 0)
        
        if vol > 0:
            leverage = self.alpha + self.beta * (self.target_return - rf) / (vol**2)
        else:
            leverage = self.alpha
            
        # Cut off between LEVERAGE_MIN and LEVERAGE_MAX
        leverage = max(self.LEVERAGE_MIN, min(self.LEVERAGE_MAX, leverage))
        
        # Calculate weights for TICKER, TICKERx3, and SGOV
        if leverage < self.LEVERAGE_THRESHOLD:
            # Only have SGOV if desired_leverage < LEVERAGE_THRESHOLD
            w_ticker = leverage
            w_sgov = self.LEVERAGE_THRESHOLD - leverage
            w_ticker3 = 0.0
        else:
            # For leverage >= LEVERAGE_THRESHOLD, mix TICKER and TICKERx3
            # w_T + w_T3 = 1
            # w_T + TICKER_X3_MULTIPLIER * w_T3 = leverage
            # => (TICKER_X3_MULTIPLIER - 1) * w_T3 = leverage - 1
            w_ticker3 = (leverage - self.LEVERAGE_THRESHOLD) / (self.TICKER_X3_MULTIPLIER - 1.0)
            w_ticker = self.LEVERAGE_THRESHOLD - w_ticker3
            w_sgov = 0.0
            
        self.positions = {
            self.ticker: current_total * w_ticker,
            self.ticker3: current_total * w_ticker3,
            self.SGOV_TICKER: current_total * w_sgov
        }

class Backtester:
    DEFAULT_INITIAL_AMT = 10000
    DEFAULT_START_DATE = '2005-01-01'

    def __init__(self, csv_path, initial_amt, monthly_cf=0, start_date=DEFAULT_START_DATE, end_date=None):
        self.initial_amt = initial_amt  
        self.monthly_cf = monthly_cf
        
        self.df = pd.read_csv(csv_path)
        self.df[DATE_COL] = pd.to_datetime(self.df[DATE_COL])
        self.df.sort_values(DATE_COL, inplace=True)
        
        if start_date:
            self.df = self.df[self.df[DATE_COL] >= pd.to_datetime(start_date)]
        if end_date:
            self.df = self.df[self.df[DATE_COL] <= pd.to_datetime(end_date)]
            
        if self.df.empty:
            raise ValueError(f"No data found for the given date range: {start_date} to {end_date}")
            
        # Store the actual start and end dates used
        self.actual_start = self.df[DATE_COL].min()
        self.actual_end = self.df[DATE_COL].max()
        
        self.df.set_index(DATE_COL, inplace=True)
        
        # Identify return columns (those not in risk-free rates)
        self.rate_cols = RATE_COLS
        self.return_cols = [c for c in self.df.columns if c not in self.rate_cols]
        
        # Ensure all return columns are numeric
        for col in self.return_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        self.df.fillna(0, inplace=True)

    def run(self, portfolio: BasePortfolio):
        total_contributions = self.initial_amt
        
        # Initial rebalance/allocation
        portfolio.rebalance(self.df.index[0], cash_to_add=self.initial_amt, row=self.df.iloc[0])
        
        history = []
        last_month = None
        
        for date, row in self.df.iterrows():
            current_month = (date.year, date.month)
            
            # Rebalance and Cashflow at the start of a new month
            if last_month is not None and current_month != last_month:
                total_contributions += self.monthly_cf
                portfolio.rebalance(date, cash_to_add=self.monthly_cf, row=row)
            
            # Capture value before daily market movement (includes any fresh cashflow)
            val_before = portfolio.total_value()
            
            # Apply daily returns
            portfolio.update_positions(row)
            
            total_val = portfolio.total_value()
            
            # Strategy return for the day (excludes impact of cash injections)
            daily_ret = (total_val / val_before - 1) if val_before != 0 else 0
            
            history.append({
                DATE_COL: date, 
                TOTAL_VALUE_COL: total_val, 
                STRATEGY_RETURN_COL: daily_ret,
                SGOV_TICKER: row[SGOV_TICKER] # Daily RF proxy from combined data
            })
            last_month = current_month
            
        history_df = pd.DataFrame(history).set_index(DATE_COL)
        return history_df, total_contributions

    def calculate_metrics(self, history_df, total_contributions):
        if history_df.empty:
            return {}
            
        total_value = history_df[TOTAL_VALUE_COL].iloc[-1]
        num_years = (history_df.index[-1] - history_df.index[0]).days / DAYS_PER_YEAR
        
        # CAGR (Time-Weighted Return)
        # We use the product of strategy returns to find the total growth of $1
        total_return_factor = (1 + history_df[STRATEGY_RETURN_COL]).prod()
        cagr = (total_return_factor ** (1 / num_years) - 1) if num_years > 0 else 0
        
        # Drawdown (based on actual portfolio value)
        rolling_max = history_df[TOTAL_VALUE_COL].cummax()
        drawdown = (history_df[TOTAL_VALUE_COL] - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Volatility (Annualized strategy returns)
        strategy_returns = history_df[STRATEGY_RETURN_COL]
        volatility = strategy_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
        
        # Sharpe Ratio (Annualized)
        excess_returns = strategy_returns - history_df[SGOV_TICKER]
        sharpe = (excess_returns.mean() / excess_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)) if excess_returns.std() != 0 else 0
        
        return {
            TOTAL_VALUE_COL: total_value,
            'Total Contributions': total_contributions,
            'Total Gain': total_value - total_contributions,
            'CAGR': cagr,
            'Max Drawdown': max_drawdown,
            'Annual Volatility': volatility,
            'Sharpe Ratio': sharpe
        }

if __name__ == "__main__":
    import sys
    import os
    
    # Use the combined file from constants
    csv_file = COMBINED_FILE
    if not os.path.exists(csv_file):
        # Fallback to absolute path or check if it exists relative to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, "combined_data.csv")
        
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        sys.exit(1)
    
    # Simulation Parameters
    params = {
        'initial_amt': Backtester.DEFAULT_INITIAL_AMT,
        # 'monthly_cf': 100,
        # 'start_date': Backtester.DEFAULT_START_DATE,
    }
    
    # Define Portfolios to Compare
    portfolios = {
        'QQQ': StaticPortfolio({'QQQ': 100}),      
        'QQQx1.5': StaticPortfolio({'QQQ': 75, 'QQQx3': 25}),      
        'QQQx2': StaticPortfolio({'QQQ': 50, 'QQQx3': 50}),      
        'QQQx3': StaticPortfolio({'QQQ': 0, 'QQQx3': 100}),      
        'QQQ_Dyn_1M': DynamicLeveragedPortfolio('QQQ', alpha=1.0, beta=0.05, target_return=0.10, vol_period='1M'),
        'QQQ_Dyn_3M': DynamicLeveragedPortfolio('QQQ', alpha=1.0, beta=0.05, target_return=0.10, vol_period='3M'),
    }
    
    all_metrics = {}
    
    # Initialize one backtester just to get actual dates for printing
    temp_bt = Backtester(csv_file, **params)
    print(f"Running backtests from {temp_bt.actual_start.date()} to {temp_bt.actual_end.date()}")
    
    for name, portfolio in portfolios.items():
        bt = Backtester(csv_file, **params)
        results, total_contribs = bt.run(portfolio)
        metrics = bt.calculate_metrics(results, total_contribs)
        all_metrics[name] = metrics
        
    # Convert to DataFrame for tabular display
    comparison_df = pd.DataFrame(all_metrics).astype(object)
    
    # Format the rows for better readability
    format_map = {
        TOTAL_VALUE_COL: lambda x: f"${x:,.2f}",
        'Total Contributions': lambda x: f"${x:,.2f}",
        'Total Gain': lambda x: f"${x:,.2f}",
        'CAGR': lambda x: f"{x*100:.2f}%",
        'Max Drawdown': lambda x: f"{x*100:.2f}%",
        'Annual Volatility': lambda x: f"{x*100:.2f}%",
        'Sharpe Ratio': lambda x: f"{x:.2f}"
    }
    
    # Apply formatting
    for metric, formatter in format_map.items():
        if metric in comparison_df.index:
            comparison_df.loc[metric] = comparison_df.loc[metric].apply(formatter)
            
    # Print the table
    print(comparison_df)
