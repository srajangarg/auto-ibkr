#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Add the current directory to sys.path to allow importing from backtester and constants
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtester import Backtester, DynamicLeveragedPortfolio
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
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    df_final.to_csv(output_file, index=False)
    print(f"Sweep completed. Results saved to {output_file}")

if __name__ == "__main__":
    run_sweep()

