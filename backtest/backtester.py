#!/usr/bin/env python3
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
    DATA_FILE,
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
        self.history = []
        self.total_contributions = 0

    def total_value(self):
        return sum(self.positions.values())

    def update_positions(self, returns_row):
        """Applies daily returns to current positions."""
        for asset in self.positions:
            if asset in returns_row:
                self.positions[asset] *= (1 + returns_row[asset])

    def record_snapshot(self, date, daily_ret, row):
        """Records daily state of the portfolio."""
        snapshot = {
            DATE_COL: date,
            TOTAL_VALUE_COL: self.total_value(),
            STRATEGY_RETURN_COL: daily_ret,
            SGOV_TICKER: row[SGOV_TICKER]
        }
        # Allow subclasses to add extra info
        snapshot.update(self.get_extra_history(row))
        self.history.append(snapshot)

    def get_extra_history(self, row):
        """Override to add custom metrics to history."""
        return {}

    def get_history_df(self):
        if not self.history:
            return pd.DataFrame()
        return pd.DataFrame(self.history).set_index(DATE_COL)

    def calculate_metrics(self):
        history_df = self.get_history_df()
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
            TOTAL_VALUE_COL: round(float(total_value), 4),
            'Total Contributions': round(float(self.total_contributions), 4),
            'CAGR': round(float(cagr), 4),
            'Max Drawdown': round(float(max_drawdown), 4),
            'Annual Volatility': round(float(volatility), 4),
            'Sharpe Ratio': round(float(sharpe), 4)
        }

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
    LEVERAGE_THRESHOLD = 1.0
    TICKER_X3_MULTIPLIER = 3.0

    def __init__(self, ticker, alpha, beta, target_return, vol_period = '1M', min_leverage=0.4, max_leverage=2.0):
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
        self.current_leverage = 1.0
        self.min_leverage = min_leverage
        self.max_leverage = max_leverage
        

    def get_desired_leverage(self, row):
        # T-Bill rate as proxy for risk-free rate (RF)
        rf = row[T_BILL_3M_COL] / 100.0
        vol = row.get(f"{self.ticker}_rvol_{self.vol_period}", 0)

        leverage = self.alpha + self.beta * (self.target_return - rf) / (vol**2)
        return max(self.min_leverage, min(self.max_leverage, leverage))

    def rebalance(self, date, row, cash_to_add=0):
        current_total = self.total_value() + cash_to_add

        leverage = self.get_desired_leverage(row)
        self.current_leverage = leverage
        
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
            SGOV_TICKER: current_total * w_sgov
        }

    def get_extra_history(self, row):
        return {'Leverage': self.current_leverage}

class Backtester:
    DEFAULT_INITIAL_AMT = 10000
    DEFAULT_START_DATE = '2005-01-01'

    def __init__(
        self,
        csv_path=DATA_FILE,
        df=None,
        initial_amt=DEFAULT_INITIAL_AMT,
        monthly_cf=0,
        start_date=DEFAULT_START_DATE,
        end_date=None
    ):
        self.initial_amt = initial_amt
        self.monthly_cf = monthly_cf

        if df is not None:
            self.df = self._load_from_dataframe(df)
        else:
            self.df = self._load_from_csv(csv_path, start_date, end_date)

        self.actual_start = self.df.index.min()
        self.actual_end = self.df.index.max()

        self.rate_cols = RATE_COLS
        self.return_cols = [c for c in self.df.columns if c not in self.rate_cols]

        for col in self.return_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        self.df.fillna(0, inplace=True)

    def _load_from_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Load data from a provided DataFrame (e.g., from Monte Carlo)."""
        result = df.copy()
        if not isinstance(result.index, pd.DatetimeIndex):
            if DATE_COL in result.columns:
                result[DATE_COL] = pd.to_datetime(result[DATE_COL])
                result.set_index(DATE_COL, inplace=True)
        return result

    def _load_from_csv(self, csv_path: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Load and filter data from CSV file."""
        if not os.path.exists(csv_path):
            from combine_data import combine_and_convert
            combine_and_convert()

        df = pd.read_csv(csv_path)
        df[DATE_COL] = pd.to_datetime(df[DATE_COL])
        df.sort_values(DATE_COL, inplace=True)

        if start_date:
            df = df[df[DATE_COL] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df[DATE_COL] <= pd.to_datetime(end_date)]

        if df.empty:
            raise ValueError(f"No data found for the given date range: {start_date} to {end_date}")

        df = df.copy()
        df.set_index(DATE_COL, inplace=True)
        return df

    def run(self, portfolio: BasePortfolio):
        portfolio.total_contributions = self.initial_amt
        
        # Initial rebalance/allocation
        portfolio.rebalance(self.df.index[0], cash_to_add=self.initial_amt, row=self.df.iloc[0])
        
        last_month = None
        
        for date, row in self.df.iterrows():
            current_month = (date.year, date.month)
            
            # Rebalance and Cashflow at the start of a new month
            if last_month is not None and current_month != last_month:
                portfolio.total_contributions += self.monthly_cf
                portfolio.rebalance(date, cash_to_add=self.monthly_cf, row=row)
            
            # Capture value before daily market movement (includes any fresh cashflow)
            val_before = portfolio.total_value()
            
            # Apply daily returns
            portfolio.update_positions(row)
            
            total_val = portfolio.total_value()
            
            # Strategy return for the day (excludes impact of cash injections)
            daily_ret = (total_val / val_before - 1) if val_before != 0 else 0
            
            portfolio.record_snapshot(date, daily_ret, row)
            last_month = current_month
            
        return portfolio.get_history_df()

if __name__ == "__main__":
    import sys
    import os
    
    # Define Portfolios to Compare
    portfolios = {
        'QQQ': StaticPortfolio({'QQQ': 100}),      
        'QQQx2': StaticPortfolio({'QQQ': 50, 'QQQx3': 50}),
        'QQQx3': StaticPortfolio({'QQQ': 0, 'QQQx3': 100}),      
        'QQQ_dyn_0.0_0.7': DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12, vol_period='1M'),
    }
    
    all_metrics = {}
    all_histories = {}
    
    # Initialize backtester once
    bt = Backtester()
    print(f"\nRunning backtests from {bt.actual_start.date()} to {bt.actual_end.date()}")
    
    for name, portfolio in portfolios.items():
        history_df = bt.run(portfolio)
        all_histories[name] = history_df
        metrics = portfolio.calculate_metrics()
        all_metrics[name] = metrics
        
    # Convert to DataFrame for tabular display
    comparison_df = pd.DataFrame(all_metrics).astype(object)
    
    # Format the rows for better readability
    format_map = {
        TOTAL_VALUE_COL: lambda x: f"${x:,.2f}",
        'Total Contributions': lambda x: f"${x:,.2f}",
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
    print()
    print(comparison_df)
    print()

    # Plot results
    try:
        from plotting import plot_portfolio_comparison
        plot_portfolio_comparison(all_histories, title=f"QQQ Strategy Comparison ({bt.actual_start.date()} to {bt.actual_end.date()})")
    except ImportError:
        print("Plotly or plotting.py not found. Skipping plot.")
    except Exception as e:
        print(f"Error generating plot: {e}")