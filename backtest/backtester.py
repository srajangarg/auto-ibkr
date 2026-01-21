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
    SGOV_TICKER,
    DEFAULT_IV_PREMIUM,
    DEFAULT_OPTIONS_ALLOCATION
)
from options_pricing import black_scholes_call, OptionPosition, dte_to_years

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
            'CAGR': round(float(cagr), 6),
            'Max Drawdown': round(float(max_drawdown), 6),
            'Annual Volatility': round(float(volatility), 6),
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

        # Guard against zero/missing volatility - use min_leverage as fallback
        if vol <= 0:
            return self.min_leverage

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


class HybridOptionsPortfolio(BasePortfolio):
    """
    Hybrid portfolio combining equity positions with LEAPS (2-year call options).

    Each monthly rebalance:
    1. Sell all existing LEAPS at current BS value
    2. Allocate (1 - options_allocation) to equity
    3. Buy fresh 2Y LEAPS with remaining options_allocation budget
    """
    VOL_WINDOW = '1M'  # Fixed: use 1-month realized volatility
    LEAPS_DTE = 504    # Fixed: 2 years of trading days
    DEFAULT_VOL = 0.20  # Fallback volatility (20% annualized)
    MIN_IV = 0.15       # Floor IV at 15% (LEAPS rarely trade below this)
    MAX_IV = 2.0        # Cap IV at 200%

    def __init__(self, ticker, options_allocation=DEFAULT_OPTIONS_ALLOCATION,
                 moneyness=0.0, iv_premium=DEFAULT_IV_PREMIUM):
        """
        Args:
            ticker: Base ticker (e.g., 'QQQ')
            options_allocation: Fraction of portfolio in LEAPS (0.0 to 0.5)
            moneyness: Strike as fraction from spot (0.0 = ATM, 0.1 = 10% OTM, -0.1 = 10% ITM)
            iv_premium: Multiplier on realized vol for implied volatility
        """
        super().__init__()
        self.ticker = ticker
        self.options_allocation = options_allocation
        self.moneyness = moneyness
        self.iv_premium = iv_premium

        # Normalized stock price tracking (BS is scale-invariant)
        self.stock_price = 100.0
        self.option_position = None  # OptionPosition or None
        self.current_option_value = 0.0
        self._initialized = False

    def total_value(self):
        """Total portfolio value = equity positions + options value."""
        return sum(self.positions.values()) + self.current_option_value

    def _get_vol(self, row) -> float:
        """Get volatility from row, with fallback."""
        vol_col = f"{self.ticker}_rvol_{self.VOL_WINDOW}"
        vol = row.get(vol_col, 0)
        if vol <= 0:
            return self.DEFAULT_VOL
        return vol

    def _get_iv(self, row) -> float:
        """Calculate implied volatility from realized vol."""
        vol = self._get_vol(row)
        iv = vol * self.iv_premium
        # Floor at MIN_IV (LEAPS rarely trade below 15% IV), cap at MAX_IV
        return max(self.MIN_IV, min(iv, self.MAX_IV))

    def _get_rf_rate(self, row) -> float:
        """Get risk-free rate from row."""
        return row.get(T_BILL_3M_COL, 4.0) / 100.0  # Default 4% if missing

    def _price_option(self, row) -> float:
        """Price current option position using Black-Scholes."""
        if self.option_position is None:
            return 0.0

        T = dte_to_years(self.option_position.current_dte)
        if T <= 0:
            # Expired: return intrinsic value
            intrinsic = max(self.stock_price - self.option_position.strike, 0)
            return intrinsic * self.option_position.quantity

        iv = self._get_iv(row)
        rf = self._get_rf_rate(row)

        call_price = black_scholes_call(
            S=self.stock_price,
            K=self.option_position.strike,
            T=T,
            r=rf,
            sigma=iv
        )
        return call_price * self.option_position.quantity

    def _price_option_fast(self, vol: float, rf: float) -> float:
        """Fast version - takes pre-extracted vol and rf values."""
        if self.option_position is None:
            return 0.0

        T = dte_to_years(self.option_position.current_dte)
        if T <= 0:
            intrinsic = max(self.stock_price - self.option_position.strike, 0)
            return intrinsic * self.option_position.quantity

        # Calculate IV from pre-extracted vol
        iv = vol * self.iv_premium if vol > 0 else self.DEFAULT_VOL * self.iv_premium
        iv = max(self.MIN_IV, min(iv, self.MAX_IV))

        call_price = black_scholes_call(
            S=self.stock_price,
            K=self.option_position.strike,
            T=T,
            r=rf,
            sigma=iv
        )
        return call_price * self.option_position.quantity

    def update_options_value(self, row):
        """
        Called daily by backtester to update options value.
        Updates stock price from daily return, decrements DTE, reprices option.
        """
        # Update stock price from daily return
        daily_return = row.get(self.ticker, 0)
        self.stock_price *= (1 + daily_return)

        # Decrement DTE if we have an option
        if self.option_position is not None:
            self.option_position.current_dte -= 1

        # Reprice option
        self.current_option_value = self._price_option(row)

    def update_options_value_fast(self, daily_return: float, vol: float, rf: float):
        """
        Fast version - takes pre-extracted values instead of row dict.
        Avoids pandas iloc overhead.
        """
        # Update stock price from daily return
        self.stock_price *= (1 + daily_return)

        # Decrement DTE if we have an option
        if self.option_position is not None:
            self.option_position.current_dte -= 1

        # Reprice option using pre-extracted values
        self.current_option_value = self._price_option_fast(vol, rf)

    def rebalance(self, date, row, cash_to_add=0):
        """
        Monthly rebalance:
        1. Value existing options at current BS price (sell)
        2. Calculate total = equity + options_value + new_cash
        3. Allocate (1 - options_allocation) to equity ticker
        4. Buy new 2Y LEAPS with options_allocation budget
        """
        # Initialize stock price on first rebalance
        if not self._initialized:
            self.stock_price = 100.0
            self._initialized = True

        # Step 1: Calculate total portfolio value
        # Options are "sold" at current value
        options_value = self._price_option(row)
        equity_value = sum(self.positions.values())
        total = equity_value + options_value + cash_to_add

        # Step 2: Allocate to equity
        equity_allocation = total * (1 - self.options_allocation)
        self.positions = {self.ticker: equity_allocation}

        # Step 3: Buy new LEAPS
        options_budget = total * self.options_allocation

        if options_budget > 0:
            # Calculate strike price
            strike = self.stock_price * (1 + self.moneyness)

            # Price a single option at 2Y DTE
            T = dte_to_years(self.LEAPS_DTE)
            iv = self._get_iv(row)
            rf = self._get_rf_rate(row)

            single_option_price = black_scholes_call(
                S=self.stock_price,
                K=strike,
                T=T,
                r=rf,
                sigma=iv
            )

            if single_option_price > 0:
                # Buy as many contracts as budget allows (fractional allowed)
                quantity = options_budget / single_option_price
                self.option_position = OptionPosition(
                    strike=strike,
                    initial_dte=self.LEAPS_DTE,
                    current_dte=self.LEAPS_DTE,
                    quantity=quantity
                )
                self.current_option_value = options_budget
            else:
                # Zero option price - move budget to equity
                self.positions[self.ticker] += options_budget
                self.option_position = None
                self.current_option_value = 0.0
        else:
            self.option_position = None
            self.current_option_value = 0.0

    def get_extra_history(self, row):
        """Record extra metrics for history."""
        return self.get_extra_history_fast()

    def get_extra_history_fast(self):
        """Fast version - uses cached values, no row needed."""
        option_value = self.current_option_value
        equity_value = sum(self.positions.values())
        total = equity_value + option_value

        actual_options_pct = option_value / total if total > 0 else 0

        return {
            'Options_Value': option_value,
            'Equity_Value': equity_value,
            'Options_Pct': actual_options_pct,
            'Stock_Price': self.stock_price
        }


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

        # Pre-compute month boundaries for faster checking
        dates = self.df.index
        months = dates.to_period('M')
        month_changes = np.array(months[1:] != months[:-1])

        # Get column indices for faster access
        col_to_idx = {col: i for i, col in enumerate(self.df.columns)}

        # Initial rebalance/allocation
        first_row = self.df.iloc[0]
        portfolio.rebalance(dates[0], cash_to_add=self.initial_amt, row=first_row)

        # Pre-allocate history list with estimated size
        portfolio.history = []

        # Convert to numpy for faster iteration
        data_values = self.df.values
        sgov_idx = col_to_idx.get(SGOV_TICKER, -1)

        for i, date in enumerate(dates):
            # Check for month boundary (skip first row)
            if i > 0 and month_changes[i - 1]:
                portfolio.total_contributions += self.monthly_cf
                # Need row as Series for rebalance
                row = self.df.iloc[i]
                portfolio.rebalance(date, cash_to_add=self.monthly_cf, row=row)

            # Capture value before daily market movement
            val_before = portfolio.total_value()

            # Apply daily returns using dict lookup (faster than Series)
            row_data = data_values[i]
            for asset in portfolio.positions:
                if asset in col_to_idx:
                    portfolio.positions[asset] *= (1 + row_data[col_to_idx[asset]])

            # Update options value if portfolio has options (e.g., HybridOptionsPortfolio)
            # Use cached row_data values instead of iloc for options portfolios
            if hasattr(portfolio, 'update_options_value'):
                daily_return = row_data[col_to_idx.get(portfolio.ticker, 0)] if portfolio.ticker in col_to_idx else 0
                vol_col = f"{portfolio.ticker}_rvol_{portfolio.VOL_WINDOW}"
                vol = row_data[col_to_idx[vol_col]] if vol_col in col_to_idx else 0
                rf = row_data[col_to_idx[T_BILL_3M_COL]] / 100.0 if T_BILL_3M_COL in col_to_idx else 0.04
                portfolio.update_options_value_fast(daily_return, vol, rf)

            total_val = portfolio.total_value()

            # Strategy return for the day
            daily_ret = (total_val / val_before - 1) if val_before != 0 else 0

            # Record snapshot with minimal overhead
            sgov_val = row_data[sgov_idx] if sgov_idx >= 0 else 0
            snapshot = {
                DATE_COL: date,
                TOTAL_VALUE_COL: total_val,
                STRATEGY_RETURN_COL: daily_ret,
                SGOV_TICKER: sgov_val
            }
            # Get extra history if portfolio has custom metrics
            if i == 0 or (i > 0 and month_changes[i - 1]):
                # Only call get_extra_history when we have a row (after rebalance)
                row = self.df.iloc[i]
                snapshot.update(portfolio.get_extra_history(row))
            elif hasattr(portfolio, 'current_leverage'):
                # For dynamic portfolios, record leverage without full row
                snapshot['Leverage'] = portfolio.current_leverage
            elif hasattr(portfolio, 'option_position'):
                # For options portfolios, use cached values (no iloc needed)
                snapshot.update(portfolio.get_extra_history_fast())
            portfolio.history.append(snapshot)

        return portfolio.get_history_df()

if __name__ == "__main__":
    import sys
    import os
    
    # Define Portfolios to Compare
    portfolios = {
        'QQQ': StaticPortfolio({'QQQ': 100}),
        'QQQx2': StaticPortfolio({'QQQ': 50, 'QQQx3': 50}),
        'QQQ_dyn_0.0_0.7': DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12, vol_period='1M'),
        'QQQ_LEAPS_20': HybridOptionsPortfolio('QQQ', options_allocation=0.20, moneyness=0.0),
        'QQQ_LEAPS_30_OTM': HybridOptionsPortfolio('QQQ', options_allocation=0.30, moneyness=0.10),
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