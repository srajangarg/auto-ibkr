#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Add the current directory to sys.path to allow importing from backtester and constants
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtester import Backtester, DynamicLeveragedPortfolio, HybridOptionsPortfolio
from constants import TOTAL_VALUE_COL

def run_simulation(alpha, beta, vol_period, target_return, bt, ticker):
    portfolio = DynamicLeveragedPortfolio(
        ticker=ticker,
        alpha=alpha,
        beta=beta,
        target_return=target_return,
        vol_period=vol_period
    )
    
    bt.run(portfolio)
    metrics = portfolio.calculate_metrics()
    
    return {
        'alpha': round(alpha, 4),
        'beta': round(beta, 4),
        'target_return': round(target_return, 4),
        'vol_period': vol_period,
        'total_value': metrics[TOTAL_VALUE_COL],
        'cagr': metrics['CAGR'],
        'max_drawdown': metrics['Max Drawdown'],
        'volatility': metrics['Annual Volatility'],
        'sharpe': metrics['Sharpe Ratio']
    }

def run_sweep():
    ticker = 'SOXX'
    monthly_cf = 200
    bt = Backtester(monthly_cf=monthly_cf)
    
    # Special Cases
    special_alphas = [1.0, 1.2, 1.5, 2.0]
    special_beta = 0.0
    special_vol_period = '1M'
    special_target_return = 0.13
    
    print(f"Running {len(special_alphas)} special cases for {ticker} (CF: {monthly_cf})...")
    special_results = []
    for alpha in special_alphas:
        res = run_simulation(alpha, special_beta, special_vol_period, special_target_return, bt, ticker)
        special_results.append(res)
    
    # Ranges for sweep
    alphas = np.linspace(0.0, 0.3, 4)
    betas = np.linspace(0.4, 0.9, 11)
    vol_periods = ['1M']
    target_returns = [0.12]

    print(f"Running sweep: {len(alphas) * len(betas) * len(vol_periods) * len(target_returns)} combinations...")
    sweep_results = []
    for alpha in alphas:
        for beta in betas:
            for vol_period in vol_periods:
                for target_return in target_returns:
                    res = run_simulation(alpha, beta, vol_period, target_return, bt, ticker)
                    sweep_results.append(res)
    
    # Create DataFrames
    df_special = pd.DataFrame(special_results)
    df_sweep = pd.DataFrame(sweep_results)
    
    # Sort sweep results by sharpe reverse
    df_sweep = df_sweep.sort_values(by='sharpe', ascending=False)
    
    # Combine: special cases at top, then sorted sweep
    df_final = pd.concat([df_special, df_sweep], ignore_index=True)
    
    filename = f'sweep_results_{ticker}_cf{monthly_cf}.csv'
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', filename)
    df_final.to_csv(output_file, index=False)
    print(f"Sweep completed. Results saved to {output_file}")

def run_options_simulation(options_allocation, moneyness, iv_premium, bt, ticker):
    """Run a single options portfolio simulation."""
    portfolio = HybridOptionsPortfolio(
        ticker=ticker,
        options_allocation=options_allocation,
        moneyness=moneyness,
        iv_premium=iv_premium
    )

    bt.run(portfolio)
    metrics = portfolio.calculate_metrics()

    return {
        'options_allocation': round(options_allocation, 4),
        'moneyness': round(moneyness, 4),
        'iv_premium': round(iv_premium, 4),
        'total_value': metrics[TOTAL_VALUE_COL],
        'cagr': metrics['CAGR'],
        'max_drawdown': metrics['Max Drawdown'],
        'volatility': metrics['Annual Volatility'],
        'sharpe': metrics['Sharpe Ratio']
    }


def run_options_sweep():
    """Sweep over HybridOptionsPortfolio parameters."""
    ticker = 'QQQ'
    monthly_cf = 200
    bt = Backtester(monthly_cf=monthly_cf)

    # Parameter ranges from the plan
    options_allocations = [0.10, 0.15, 0.20, 0.25, 0.30]
    moneynesses = [-0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.20]  # ITM to OTM
    iv_premiums = [1.1, 1.2, 1.3]

    total_combinations = len(options_allocations) * len(moneynesses) * len(iv_premiums)
    print(f"Running options sweep: {total_combinations} combinations for {ticker} (CF: {monthly_cf})...")

    results = []
    for options_allocation in options_allocations:
        for moneyness in moneynesses:
            for iv_premium in iv_premiums:
                res = run_options_simulation(options_allocation, moneyness, iv_premium, bt, ticker)
                results.append(res)

    df = pd.DataFrame(results)
    df = df.sort_values(by='sharpe', ascending=False)

    filename = f'options_sweep_results_{ticker}_cf{monthly_cf}.csv'
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', filename)
    df.to_csv(output_file, index=False)
    print(f"Options sweep completed. Results saved to {output_file}")

    # Print top 10 results
    print("\nTop 10 configurations by Sharpe Ratio:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'options':
        run_options_sweep()
    else:
        run_sweep()

