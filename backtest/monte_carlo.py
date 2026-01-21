#!/usr/bin/env python3
"""Monte Carlo simulation module for backtesting."""

import pandas as pd
import numpy as np
import re
from dataclasses import dataclass, field
from typing import Callable, Optional
from functools import lru_cache
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from constants import (
    TRADING_DAYS_PER_YEAR,
    DATA_FILE,
    DATE_COL,
    TOTAL_VALUE_COL,
    T_BILL_3M_COL,
    T_NOTE_2Y_COL,
    T_BOND_10Y_COL,
    SGOV_TICKER,
    VOLATILITY_WINDOWS
)
from backtester import Backtester


# Cache for date ranges to avoid repeated generation
_DATE_RANGE_CACHE: dict[int, pd.DatetimeIndex] = {}


@dataclass
class BacktestResult:
    """Result from a single backtest run."""
    total_value: float
    total_contributions: float
    cagr: float
    max_drawdown: float
    annual_volatility: float
    sharpe_ratio: float
    history_df: Optional[pd.DataFrame] = None


@dataclass
class SimulationResults:
    """Container for all simulation results (historical + Monte Carlo)."""
    historical: Optional[BacktestResult] = None
    monte_carlo: Optional[list[BacktestResult]] = None

    def get_metric_distribution(self, metric: str) -> np.ndarray:
        """Get array of values for a metric across all MC simulations."""
        if self.monte_carlo is None:
            return np.array([])
        return np.array([getattr(r, metric) for r in self.monte_carlo])

    def plot_distribution(self, metric: str, title: str = None, show: bool = True):
        """Plot histogram of MC results with historical as vertical line."""
        try:
            import plotly.graph_objects as go
        except ImportError:
            print("Plotly not installed. Cannot plot distribution.")
            return None

        values = self.get_metric_distribution(metric)
        if len(values) == 0:
            print("No Monte Carlo results to plot.")
            return None

        # Format metric name for display
        metric_display = metric.replace('_', ' ').title()
        if title is None:
            title = f'{metric_display} Distribution (n={len(values)})'

        fig = go.Figure()

        # Add histogram of MC results
        fig.add_trace(go.Histogram(
            x=values,
            name='Monte Carlo',
            opacity=0.7,
            nbinsx=50
        ))

        # Add vertical line for historical result
        if self.historical is not None:
            historical_value = getattr(self.historical, metric)
            fig.add_vline(
                x=historical_value,
                line_dash="dash",
                line_color="red",
                line_width=2,
                annotation_text=f"Historical: {historical_value:.4f}",
                annotation_position="top"
            )

        # Format x-axis based on metric type
        if metric in ['cagr', 'max_drawdown', 'annual_volatility']:
            fig.update_xaxes(tickformat='.1%')
        elif metric == 'sharpe_ratio':
            fig.update_xaxes(tickformat='.2f')

        fig.update_layout(
            title=title,
            xaxis_title=metric_display,
            yaxis_title='Count',
            showlegend=True
        )

        if show:
            fig.show()
        return fig

    def summary(self) -> dict:
        """Get summary statistics for Monte Carlo results."""
        if self.monte_carlo is None or len(self.monte_carlo) == 0:
            return {}

        metrics = ['cagr', 'max_drawdown', 'annual_volatility', 'sharpe_ratio', 'total_value']
        summary = {}

        for metric in metrics:
            values = self.get_metric_distribution(metric)
            summary[metric] = {
                'mean': np.mean(values),
                'median': np.median(values),
                'std': np.std(values),
                'p5': np.percentile(values, 5),
                'p25': np.percentile(values, 25),
                'p75': np.percentile(values, 75),
                'p95': np.percentile(values, 95),
            }
            if self.historical is not None:
                summary[metric]['historical'] = getattr(self.historical, metric)
                # Percentile rank of historical result
                summary[metric]['historical_percentile'] = (values < getattr(self.historical, metric)).mean() * 100

        return summary


@dataclass
class RFSchedule:
    """Risk-free rate schedule configuration.

    Attributes:
        schedule_type: One of 'constant', 'increasing', 'decreasing', 'v_shape', 'inverse_v'
        start_rate: Starting annual risk-free rate (e.g., 0.04 for 4%)
        end_rate: Ending annual rate (used for non-constant schedules)
        midpoint_rate: Rate at midpoint (for v_shape/inverse_v). If None, uses min/max of start/end.
    """
    schedule_type: str = 'constant'
    start_rate: float = 0.04
    end_rate: float = 0.04
    midpoint_rate: Optional[float] = None


@dataclass
class CrashConfig:
    """Configuration for crash injection in Monte Carlo simulations.

    When enabled, a percentage of simulations will experience a market crash
    (30-50% decline) within the crash window, followed by recovery at normal pace.

    Attributes:
        crash_probability: Fraction of simulations that will have a crash (0.0 to 1.0)
        min_crash_start_days: Earliest day crash can start (default: 252 = 1 year)
        max_crash_start_days: Latest day crash can start (default: 630 = 2.5 years)
        min_decline: Minimum decline magnitude (default: 0.30 = 30%)
        max_decline: Maximum decline magnitude (default: 0.50 = 50%)
        min_crash_duration_days: Minimum crash duration (default: 20)
        max_crash_duration_days: Maximum crash duration (default: 40)
    """
    crash_probability: float = 0.0
    min_crash_start_days: int = 252   # 1 year
    max_crash_start_days: int = 630   # 2.5 years
    min_decline: float = 0.30
    max_decline: float = 0.50
    min_crash_duration_days: int = 20
    max_crash_duration_days: int = 40


def generate_rf_path(schedule: RFSchedule, num_days: int) -> np.ndarray:
    """Generate daily risk-free rates following the schedule.

    Args:
        schedule: RFSchedule configuration
        num_days: Number of trading days

    Returns:
        Array of annual risk-free rates for each day
    """
    if schedule.schedule_type == 'constant':
        return np.full(num_days, schedule.start_rate)

    elif schedule.schedule_type == 'increasing':
        return np.linspace(schedule.start_rate, schedule.end_rate, num_days)

    elif schedule.schedule_type == 'decreasing':
        return np.linspace(schedule.start_rate, schedule.end_rate, num_days)

    elif schedule.schedule_type == 'v_shape':
        # Decreasing then increasing (like 2020s: rates fell then rose)
        midpoint = num_days // 2
        mid_rate = schedule.midpoint_rate if schedule.midpoint_rate is not None else min(schedule.start_rate, schedule.end_rate)
        first_half = np.linspace(schedule.start_rate, mid_rate, midpoint)
        second_half = np.linspace(mid_rate, schedule.end_rate, num_days - midpoint)
        return np.concatenate([first_half, second_half])

    elif schedule.schedule_type == 'inverse_v':
        # Increasing then decreasing
        midpoint = num_days // 2
        mid_rate = schedule.midpoint_rate if schedule.midpoint_rate is not None else max(schedule.start_rate, schedule.end_rate)
        first_half = np.linspace(schedule.start_rate, mid_rate, midpoint)
        second_half = np.linspace(mid_rate, schedule.end_rate, num_days - midpoint)
        return np.concatenate([first_half, second_half])

    else:
        raise ValueError(f"Unknown schedule_type: {schedule.schedule_type}")


def inject_crash(
    returns: np.ndarray,
    crash_config: CrashConfig,
    seed: Optional[int] = None,
    warmup_days: int = 0
) -> tuple[np.ndarray, int, int]:
    """Inject a crash event into returns array.

    The crash is modeled as a sharp decline over a random duration,
    distributed across all days in the crash period to achieve the target decline.

    Args:
        returns: Daily returns array
        crash_config: Crash configuration
        seed: Random seed for crash timing and magnitude
        warmup_days: Number of warmup days at the start (crash indices are relative to full array)

    Returns:
        Tuple of (modified returns array, crash_start_idx, crash_end_idx)
    """
    if seed is not None:
        rng = np.random.RandomState(seed)
    else:
        rng = np.random.RandomState()

    # Random crash duration between min and max
    crash_duration = rng.randint(
        crash_config.min_crash_duration_days,
        crash_config.max_crash_duration_days + 1
    )

    # Crash start window (indices relative to full array including warmup)
    min_start = warmup_days + crash_config.min_crash_start_days
    max_start = min(
        warmup_days + crash_config.max_crash_start_days,
        len(returns) - crash_duration
    )

    if min_start >= max_start:
        # Not enough room for crash, use what we can
        min_start = warmup_days
        max_start = max(min_start + 1, len(returns) - crash_duration)

    crash_start = rng.randint(min_start, max_start)

    # Random decline magnitude between min and max
    decline = rng.uniform(crash_config.min_decline, crash_config.max_decline)

    # Calculate daily return needed to achieve total decline over crash duration
    # If we want -40% total: (1 + r)^n = 0.6, so r = 0.6^(1/n) - 1
    target_multiplier = 1 - decline
    daily_crash_return = target_multiplier ** (1 / crash_duration) - 1

    # Replace returns during crash period
    crash_end = crash_start + crash_duration
    returns[crash_start:crash_end] = daily_crash_return

    return returns, crash_start, crash_end


@lru_cache(maxsize=128)
def fit_garch_params(
    ticker: str,
    csv_path: str = DATA_FILE,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """Fit GARCH(1,1) parameters to historical returns.

    Results are cached to avoid repeated fitting.

    Args:
        ticker: Ticker symbol
        csv_path: Path to historical data CSV
        start_date: Optional start date filter (e.g., '2005-01-01')
        end_date: Optional end date filter

    Returns:
        dict: {'omega': x, 'alpha': y, 'beta': z, 'long_run_var': w, 'mu': mean_return}
    """
    try:
        from arch import arch_model
    except ImportError:
        raise ImportError("arch library required for GARCH fitting. Install with: pip install arch")

    df = pd.read_csv(csv_path, index_col=DATE_COL, parse_dates=True)
    if ticker not in df.columns:
        raise ValueError(f"Ticker '{ticker}' not found in historical data")

    # Apply date filtering
    if start_date is not None:
        df = df[df.index >= start_date]
    if end_date is not None:
        df = df[df.index <= end_date]

    daily_returns = df[ticker].dropna() * 100  # arch expects percentage returns

    # Fit GARCH(1,1) model
    model = arch_model(daily_returns, vol='Garch', p=1, q=1, mean='Constant', rescale=False)
    result = model.fit(disp='off')

    omega = result.params['omega']
    alpha = result.params['alpha[1]']
    beta = result.params['beta[1]']
    mu = result.params['mu'] / 100  # Convert back from percentage

    # Long-run variance: omega / (1 - alpha - beta)
    persistence = alpha + beta
    if persistence < 1:
        long_run_var = omega / (1 - persistence) / 10000  # Convert from percentage^2
    else:
        long_run_var = daily_returns.var() / 10000

    return {
        'omega': omega / 10000,  # Convert from percentage^2
        'alpha': alpha,
        'beta': beta,
        'long_run_var': long_run_var,
        'mu': mu
    }


def generate_garch_returns(
    num_days: int,
    mu: float,
    omega: float,
    alpha: float,
    beta: float,
    initial_var: float,
    seed: Optional[int] = None
) -> tuple:
    """Generate returns with GARCH(1,1) volatility dynamics.

    GARCH(1,1): h_t = omega + alpha * epsilon_{t-1}^2 + beta * h_{t-1}

    Args:
        num_days: Number of days to simulate
        mu: Daily mean return (as decimal)
        omega: GARCH constant term (daily variance units)
        alpha: GARCH news/shock coefficient
        beta: GARCH persistence coefficient
        initial_var: Initial variance (daily)
        seed: Random seed

    Returns:
        tuple: (returns_array, volatility_array) - both annualized volatilities
    """
    if seed is not None:
        np.random.seed(seed)

    z = np.random.standard_normal(num_days)
    returns = np.zeros(num_days)
    variances = np.zeros(num_days)

    # Initialize
    variances[0] = initial_var
    returns[0] = mu + np.sqrt(variances[0]) * z[0]

    # Generate path
    for t in range(1, num_days):
        # GARCH variance update
        variances[t] = omega + alpha * (returns[t-1] - mu)**2 + beta * variances[t-1]
        # Ensure variance stays positive
        variances[t] = max(variances[t], 1e-10)
        returns[t] = mu + np.sqrt(variances[t]) * z[t]

    # Annualize volatilities for output
    annualized_vols = np.sqrt(variances * TRADING_DAYS_PER_YEAR)

    return returns, annualized_vols


def recalculate_garch_variances(
    returns: np.ndarray,
    mu: float,
    omega: float,
    alpha: float,
    beta: float,
    initial_var: float
) -> np.ndarray:
    """Recalculate GARCH(1,1) conditional variances given a returns path.

    This is used after crash injection to properly update volatility
    based on the actual returns (including crash).

    Args:
        returns: Daily returns array (already includes crash if injected)
        mu: Daily mean return (as decimal)
        omega: GARCH constant term (daily variance units)
        alpha: GARCH news/shock coefficient
        beta: GARCH persistence coefficient
        initial_var: Initial variance (daily)

    Returns:
        Array of annualized volatilities
    """
    num_days = len(returns)
    variances = np.zeros(num_days)

    # Initialize
    variances[0] = initial_var

    # Recalculate variances based on actual returns
    for t in range(1, num_days):
        variances[t] = omega + alpha * (returns[t-1] - mu)**2 + beta * variances[t-1]
        variances[t] = max(variances[t], 1e-10)

    # Annualize volatilities
    return np.sqrt(variances * TRADING_DAYS_PER_YEAR)


@lru_cache(maxsize=128)
def derive_equity_risk_premium(
    ticker: str,
    csv_path: str = DATA_FILE,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> float:
    """Calculate historical equity risk premium.

    ERP = annualized(mean equity return) - annualized(mean risk-free return)
    Results are cached to avoid repeated CSV reads.

    Args:
        ticker: Equity ticker symbol
        csv_path: Path to historical data CSV
        start_date: Optional start date filter (e.g., '2005-01-01')
        end_date: Optional end date filter

    Returns:
        Annualized equity risk premium as decimal (e.g., 0.05 for 5%)
    """
    df = pd.read_csv(csv_path, index_col=DATE_COL, parse_dates=True)
    if ticker not in df.columns:
        raise ValueError(f"Ticker '{ticker}' not found in historical data")
    if SGOV_TICKER not in df.columns:
        raise ValueError(f"Risk-free ticker '{SGOV_TICKER}' not found in historical data")

    # Apply date filtering
    if start_date is not None:
        df = df[df.index >= start_date]
    if end_date is not None:
        df = df[df.index <= end_date]

    # Get overlapping data
    equity_returns = df[ticker].dropna()
    rf_returns = df[SGOV_TICKER].dropna()
    common_idx = equity_returns.index.intersection(rf_returns.index)

    equity_mean = equity_returns.loc[common_idx].mean() * TRADING_DAYS_PER_YEAR
    rf_mean = rf_returns.loc[common_idx].mean() * TRADING_DAYS_PER_YEAR

    return equity_mean - rf_mean


@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo simulations.

    Attributes:
        num_simulations: Number of MC simulations to run
        num_days: Length of each simulation in trading days
        tickers: List of tickers to simulate
        ticker_params: Override params per ticker {ticker: {'mean_return': x, 'volatility': y}}
        seed: Random seed for reproducibility
        rf_schedule: Risk-free rate schedule (constant, increasing, decreasing, v_shape, inverse_v)
        use_garch: Enable GARCH(1,1) volatility dynamics
        garch_params: Override GARCH params {ticker: {'omega': x, 'alpha': y, 'beta': z, ...}}
        use_erp: If True, equity returns = rf + equity_risk_premium (ties returns to rf)
        ticker_erp: Override ERP per ticker {ticker: erp_value}
        historical_start_date: Start date for deriving params from historical data (default: '2005-01-01')
        crash_config: Optional crash injection configuration
    """
    num_simulations: int = 1000
    num_days: int = 252 * 20  # 20 years
    tickers: list = field(default_factory=list)
    ticker_params: dict = field(default_factory=dict)
    seed: Optional[int] = None
    rf_schedule: RFSchedule = field(default_factory=RFSchedule)  # Defaults to constant 4%
    use_garch: bool = False
    garch_params: dict = field(default_factory=dict)
    use_erp: bool = False
    ticker_erp: dict = field(default_factory=dict)
    historical_start_date: str = '2005-01-01'
    crash_config: Optional[CrashConfig] = None


@dataclass
class HistoricalConfig:
    """Configuration for historical backtest."""
    csv_path: str = DATA_FILE
    start_date: str = '2005-01-01'
    end_date: Optional[str] = None


@lru_cache(maxsize=128)
def derive_params_from_historical(
    ticker: str,
    csv_path: str = DATA_FILE,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> tuple:
    """Extract mean return and volatility from historical data.

    Results are cached to avoid repeated CSV reads.

    Args:
        ticker: Ticker symbol
        csv_path: Path to historical data CSV
        start_date: Optional start date filter (e.g., '2005-01-01')
        end_date: Optional end date filter

    Returns:
        tuple: (annualized_mean_return, annualized_volatility)
    """
    df = pd.read_csv(csv_path, index_col=DATE_COL, parse_dates=True)
    if ticker not in df.columns:
        raise ValueError(f"Ticker '{ticker}' not found in historical data")

    # Apply date filtering
    if start_date is not None:
        df = df[df.index >= start_date]
    if end_date is not None:
        df = df[df.index <= end_date]

    daily_returns = df[ticker].dropna()
    mean_daily = daily_returns.mean()
    std_daily = daily_returns.std()

    # Annualize
    mean_annual = mean_daily * TRADING_DAYS_PER_YEAR
    vol_annual = std_daily * np.sqrt(TRADING_DAYS_PER_YEAR)

    return mean_annual, vol_annual


def _get_cached_date_range(num_days: int) -> pd.DatetimeIndex:
    """Get or create a cached date range for MC simulations."""
    if num_days not in _DATE_RANGE_CACHE:
        start_date = pd.Timestamp('2000-01-01')
        _DATE_RANGE_CACHE[num_days] = pd.bdate_range(start=start_date, periods=num_days)
    return _DATE_RANGE_CACHE[num_days]


def _parse_leveraged_ticker(ticker: str) -> tuple:
    """Parse a ticker to identify if it's leveraged.

    Args:
        ticker: Ticker symbol (e.g., 'QQQ', 'QQQx3', 'SOXXx2')

    Returns:
        tuple: (base_ticker, leverage_factor) or (ticker, 1) if not leveraged
    """
    match = re.match(r'^(.+)x(\d+)$', ticker)
    if match:
        return match.group(1), int(match.group(2))
    return ticker, 1


def generate_monte_carlo_df(
    config: MonteCarloConfig,
    seed_offset: int = 0,
    inject_crash_event: bool = False
) -> pd.DataFrame:
    """Generate synthetic returns DataFrame.

    Supports:
    - Simple GBM (constant volatility) or GARCH(1,1) volatility dynamics
    - Constant or time-varying risk-free rates
    - Equity risk premium modeling (ties equity returns to RF rate)
    - Proper correlation between base and leveraged tickers (e.g., QQQ and QQQx3)
    - Crash event injection (bubble/crash scenarios)

    Args:
        config: Monte Carlo configuration
        seed_offset: Offset added to seed for different simulations
        inject_crash_event: If True and crash_config is set, inject a crash event

    Returns:
        DataFrame with simulated daily returns, same structure as historical data
    """
    seed = (config.seed + seed_offset) if config.seed is not None else None
    if seed is not None:
        np.random.seed(seed)

    # Add warmup period for rolling volatility calculation
    warmup_days = max(VOLATILITY_WINDOWS.values())
    total_days = config.num_days + warmup_days
    tickers = config.tickers

    # Generate RF rate path (including warmup period)
    rf_path = generate_rf_path(config.rf_schedule, total_days)  # Annual rates
    daily_rf = rf_path / TRADING_DAYS_PER_YEAR

    # Identify base tickers and leveraged tickers
    base_tickers = []
    leveraged_tickers = {}  # {ticker: (base_ticker, leverage)}
    for ticker in tickers:
        base, leverage = _parse_leveraged_ticker(ticker)
        if leverage > 1:
            leveraged_tickers[ticker] = (base, leverage)
            if base not in base_tickers and base not in tickers:
                base_tickers.append(base)
        else:
            base_tickers.append(ticker)

    # All tickers we need to generate returns for (base tickers only)
    tickers_to_generate = list(set(base_tickers))

    # Build ticker parameters for base tickers
    params = {}
    garch_params_all = {}
    erp_values = {}

    for ticker in tickers_to_generate:
        # Standard params (mean, vol)
        if ticker in config.ticker_params:
            params[ticker] = config.ticker_params[ticker]
        else:
            mean_ret, vol = derive_params_from_historical(
                ticker, start_date=config.historical_start_date
            )
            params[ticker] = {'mean_return': mean_ret, 'volatility': vol}

        # GARCH params (if enabled)
        if config.use_garch:
            if ticker in config.garch_params:
                garch_params_all[ticker] = config.garch_params[ticker]
            else:
                garch_params_all[ticker] = fit_garch_params(
                    ticker, start_date=config.historical_start_date
                )

        # Equity risk premium (if enabled)
        if config.use_erp:
            if ticker in config.ticker_erp:
                erp_values[ticker] = config.ticker_erp[ticker]
            else:
                erp_values[ticker] = derive_equity_risk_premium(
                    ticker, start_date=config.historical_start_date
                )

    # Generate date index (cached to avoid repeated generation)
    dates = _get_cached_date_range(total_days)

    # Generate returns for base tickers only
    data = {}
    garch_vols = {}  # Store GARCH volatilities for vol columns

    for ticker in tickers_to_generate:
        sigma = params[ticker]['volatility']

        if config.use_garch and ticker in garch_params_all:
            # GARCH volatility dynamics
            gp = garch_params_all[ticker]

            if config.use_erp:
                # ERP: expected return = rf + erp (varies daily with RF)
                erp = erp_values[ticker]
                # Use mean RF for GARCH mu so variance calculation is correct
                # (GARCH variance depends on deviations from mu, so mu must match actual returns)
                mean_rf = np.mean(daily_rf)
                mu_daily_total = erp / TRADING_DAYS_PER_YEAR + mean_rf

                # Generate GARCH returns with total expected return (ERP + mean RF)
                base_returns, vols = generate_garch_returns(
                    num_days=total_days,
                    mu=mu_daily_total,
                    omega=gp['omega'],
                    alpha=gp['alpha'],
                    beta=gp['beta'],
                    initial_var=gp['long_run_var'],
                    seed=seed + hash(ticker) % 10000 if seed else None
                )
                # Adjust returns to have time-varying RF instead of constant mean RF
                # This preserves correct variance while allowing RF to vary over time
                daily_returns = base_returns - mean_rf + daily_rf
            else:
                # Standard GARCH with constant mean
                mu = params[ticker]['mean_return']
                mu_daily = mu / TRADING_DAYS_PER_YEAR
                daily_returns, vols = generate_garch_returns(
                    num_days=total_days,
                    mu=mu_daily,
                    omega=gp['omega'],
                    alpha=gp['alpha'],
                    beta=gp['beta'],
                    initial_var=gp['long_run_var'],
                    seed=seed + hash(ticker) % 10000 if seed else None
                )

            garch_vols[ticker] = vols

        else:
            # Simple GBM (constant volatility)
            sigma_daily = sigma / np.sqrt(TRADING_DAYS_PER_YEAR)

            if config.use_erp:
                # ERP: expected return = rf + erp
                erp = erp_values[ticker]
                mu_daily = erp / TRADING_DAYS_PER_YEAR + daily_rf

                z = np.random.standard_normal(total_days)
                daily_returns = mu_daily + sigma_daily * z
            else:
                # Standard constant mean
                mu = params[ticker]['mean_return']
                mu_daily = mu / TRADING_DAYS_PER_YEAR

                z = np.random.standard_normal(total_days)
                daily_returns = mu_daily + sigma_daily * z

        data[ticker] = daily_returns

    # Inject crash events if configured
    if inject_crash_event and config.crash_config is not None:
        crash_seed = seed + 999999 if seed else None
        for ticker in tickers_to_generate:
            data[ticker], crash_start, crash_end = inject_crash(
                data[ticker],
                config.crash_config,
                seed=crash_seed,
                warmup_days=warmup_days
            )

            # Recalculate GARCH variances to reflect crash impact on volatility
            if config.use_garch and ticker in garch_params_all:
                gp = garch_params_all[ticker]
                if config.use_erp:
                    # Use same mu as generation: ERP + mean_rf (returns include RF)
                    mean_rf = np.mean(daily_rf)
                    mu_daily = erp_values[ticker] / TRADING_DAYS_PER_YEAR + mean_rf
                else:
                    mu_daily = params[ticker]['mean_return'] / TRADING_DAYS_PER_YEAR

                garch_vols[ticker] = recalculate_garch_variances(
                    data[ticker],
                    mu=mu_daily,
                    omega=gp['omega'],
                    alpha=gp['alpha'],
                    beta=gp['beta'],
                    initial_var=gp['long_run_var']
                )

    # Derive leveraged ticker returns from base tickers
    # Leveraged return = leverage * base_return - (leverage - 1) * rf
    # This models daily rebalancing with borrowing at risk-free rate
    for ticker, (base, leverage) in leveraged_tickers.items():
        base_returns = data[base]
        data[ticker] = leverage * base_returns - (leverage - 1) * daily_rf

    # Create DataFrame
    df = pd.DataFrame(data, index=dates)
    df.index.name = DATE_COL

    # Add volatility columns for base tickers
    # Shift by 1 to avoid lookahead bias: vol on day i uses returns through day i-1
    for ticker in tickers_to_generate:
        if config.use_garch and ticker in garch_vols:
            # Use GARCH conditional volatility (already forward-looking by nature)
            df[f"{ticker}_rvol_garch"] = garch_vols[ticker]
            # Also add rolling vol columns (some strategies may still want them)
            for label, window in VOLATILITY_WINDOWS.items():
                col_name = f"{ticker}_rvol_{label}"
                df[col_name] = df[ticker].rolling(window=window).std().shift(1) * np.sqrt(TRADING_DAYS_PER_YEAR)
        else:
            # Rolling realized volatility only
            for label, window in VOLATILITY_WINDOWS.items():
                col_name = f"{ticker}_rvol_{label}"
                df[col_name] = df[ticker].rolling(window=window).std().shift(1) * np.sqrt(TRADING_DAYS_PER_YEAR)

    # Add RF rate columns (daily returns for SGOV, percentages for rate columns)
    df[SGOV_TICKER] = rf_path / TRADING_DAYS_PER_YEAR
    df[T_BILL_3M_COL] = rf_path * 100  # As percentage
    df[T_NOTE_2Y_COL] = rf_path * 100 + 0.5  # Slightly higher spread
    df[T_BOND_10Y_COL] = rf_path * 100 + 1.0  # Higher spread

    # Trim warmup period - volatility columns now have valid data from the start
    df = df.iloc[warmup_days:].copy()

    return df


def run_backtest(
    config: HistoricalConfig,
    portfolio_factory: Callable,
    initial_amt: float = 10000,
    monthly_cf: float = 0
) -> BacktestResult:
    """Run single historical backtest.

    Args:
        config: Historical configuration
        portfolio_factory: Callable that returns a fresh portfolio instance
        initial_amt: Initial investment amount
        monthly_cf: Monthly cash flow

    Returns:
        BacktestResult with metrics and history
    """
    bt = Backtester(
        csv_path=config.csv_path,
        start_date=config.start_date,
        end_date=config.end_date,
        initial_amt=initial_amt,
        monthly_cf=monthly_cf
    )
    portfolio = portfolio_factory()
    bt.run(portfolio)
    metrics = portfolio.calculate_metrics()

    return BacktestResult(
        total_value=metrics[TOTAL_VALUE_COL],
        total_contributions=metrics['Total Contributions'],
        cagr=metrics['CAGR'],
        max_drawdown=metrics['Max Drawdown'],
        annual_volatility=metrics['Annual Volatility'],
        sharpe_ratio=metrics['Sharpe Ratio'],
        history_df=portfolio.get_history_df()
    )


def _run_single_mc_simulation(
    config: MonteCarloConfig,
    portfolio_factory: Callable,
    initial_amt: float,
    monthly_cf: float,
    seed_offset: int
) -> BacktestResult:
    """Run a single MC simulation. Designed for parallel execution."""
    # Determine if this simulation should have a crash
    inject_crash_event = False
    if config.crash_config is not None and config.crash_config.crash_probability > 0:
        # Use seed_offset to deterministically decide if this sim has a crash
        rng = np.random.RandomState((config.seed or 0) + seed_offset + 123456)
        inject_crash_event = rng.random() < config.crash_config.crash_probability

    df = generate_monte_carlo_df(config, seed_offset=seed_offset, inject_crash_event=inject_crash_event)
    bt = Backtester(df=df, initial_amt=initial_amt, monthly_cf=monthly_cf)
    portfolio = portfolio_factory()
    bt.run(portfolio)
    metrics = portfolio.calculate_metrics()

    return BacktestResult(
        total_value=metrics[TOTAL_VALUE_COL],
        total_contributions=metrics['Total Contributions'],
        cagr=metrics['CAGR'],
        max_drawdown=metrics['Max Drawdown'],
        annual_volatility=metrics['Annual Volatility'],
        sharpe_ratio=metrics['Sharpe Ratio'],
        history_df=None
    )


def run_monte_carlo(
    config: MonteCarloConfig,
    portfolio_factory: Callable,
    initial_amt: float = 10000,
    monthly_cf: float = 0,
    verbose: bool = True,
    parallel: bool = True,
    max_workers: Optional[int] = None
) -> list:
    """Run multiple Monte Carlo simulations.

    Args:
        config: Monte Carlo configuration
        portfolio_factory: Callable that returns a fresh portfolio instance
        initial_amt: Initial investment amount
        monthly_cf: Monthly cash flow
        verbose: Print progress
        parallel: Use parallel processing with threads (default True)
        max_workers: Max worker threads (default: min(32, CPU count + 4))

    Returns:
        List of BacktestResult, one per simulation
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import multiprocessing

    if max_workers is None:
        # ThreadPoolExecutor default is min(32, cpu_count + 4)
        max_workers = min(32, multiprocessing.cpu_count() + 4, config.num_simulations)

    if parallel and config.num_simulations > 1:
        # Parallel execution with threads (works with lambdas, numpy releases GIL)
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _run_single_mc_simulation,
                    config, portfolio_factory, initial_amt, monthly_cf, i
                ): i
                for i in range(config.num_simulations)
            }

            completed = 0
            for future in as_completed(futures):
                completed += 1
                if verbose and completed % 100 == 0:
                    print(f"  Completed {completed}/{config.num_simulations} simulations")
                results.append(future.result())

        return results
    else:
        # Sequential execution (fallback)
        results = []
        for i in range(config.num_simulations):
            if verbose and (i + 1) % 100 == 0:
                print(f"  Running simulation {i + 1}/{config.num_simulations}")
            results.append(_run_single_mc_simulation(
                config, portfolio_factory, initial_amt, monthly_cf, i
            ))

        return results


def run_all(
    historical_config: HistoricalConfig,
    mc_config: MonteCarloConfig,
    portfolio_factory: Callable,
    initial_amt: float = 10000,
    monthly_cf: float = 0,
    verbose: bool = True
) -> SimulationResults:
    """Run historical backtest + Monte Carlo simulations.

    Args:
        historical_config: Configuration for historical backtest
        mc_config: Configuration for Monte Carlo simulations
        portfolio_factory: Callable that returns a fresh portfolio instance
        initial_amt: Initial investment amount
        monthly_cf: Monthly cash flow
        verbose: Print progress

    Returns:
        SimulationResults with historical and monte_carlo results
    """
    if verbose:
        print("Running historical backtest...")
    historical = run_backtest(historical_config, portfolio_factory, initial_amt, monthly_cf)

    if verbose:
        print(f"Running {mc_config.num_simulations} Monte Carlo simulations...")
    monte_carlo = run_monte_carlo(mc_config, portfolio_factory, initial_amt, monthly_cf, verbose)

    return SimulationResults(historical=historical, monte_carlo=monte_carlo)


if __name__ == "__main__":
    from backtester import DynamicLeveragedPortfolio, StaticPortfolio

    # Example usage
    historical_config = HistoricalConfig(start_date='2005-01-01')
    mc_config = MonteCarloConfig(
        num_simulations=100,
        num_days=252 * 20,
        tickers=['QQQ', 'QQQx3'],
        seed=42
    )

    def make_portfolio():
        return DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12)

    results = run_all(historical_config, mc_config, make_portfolio, initial_amt=10000, monthly_cf=200)

    print(f"\nHistorical CAGR: {results.historical.cagr:.2%}")
    print(f"MC CAGR (median): {np.median(results.get_metric_distribution('cagr')):.2%}")
    print(f"MC CAGR (5th-95th): {np.percentile(results.get_metric_distribution('cagr'), 5):.2%} - {np.percentile(results.get_metric_distribution('cagr'), 95):.2%}")

    # Print summary
    summary = results.summary()
    print("\n--- Summary ---")
    for metric, stats in summary.items():
        print(f"\n{metric}:")
        print(f"  Historical: {stats.get('historical', 'N/A'):.4f} (percentile: {stats.get('historical_percentile', 'N/A'):.1f}%)")
        print(f"  MC Mean: {stats['mean']:.4f}, Median: {stats['median']:.4f}")
        print(f"  MC 5-95%: [{stats['p5']:.4f}, {stats['p95']:.4f}]")

    # Plot distributions
    results.plot_distribution('cagr', title='CAGR Distribution')
