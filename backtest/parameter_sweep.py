#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Add the current directory to sys.path to allow importing from backtester and constants
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtester import Backtester, DynamicLeveragedPortfolio
from constants import DATA_FILE, TOTAL_VALUE_COL

def run_simulation(alpha, beta, vol_period, bt):
    TICKER = 'QQQ'
    TARGET_RETURN = 0.12

    portfolio = DynamicLeveragedPortfolio(
        ticker=TICKER,
        alpha=alpha,
        beta=beta,
        target_return=TARGET_RETURN,
        vol_period=vol_period
    )
    
    bt.run(portfolio)
    metrics = portfolio.calculate_metrics()
    
    return {
        'alpha': round(alpha, 4),
        'beta': round(beta, 4),
        'target_return': round(TARGET_RETURN, 4),
        'vol_period': vol_period,
        'total_value': metrics[TOTAL_VALUE_COL],
        'cagr': metrics['CAGR'],
        'max_drawdown': metrics['Max Drawdown'],
        'volatility': metrics['Annual Volatility'],
        'sharpe': metrics['Sharpe Ratio']
    }

def run_sweep():
    bt = Backtester()
    
    # Special Cases
    special_alphas = [1.0, 1.2, 1.5, 2.0]
    special_beta = 0.0
    special_vol_period = '1M'
    
    print(f"Running {len(special_alphas)} special cases...")
    special_results = []
    for alpha in special_alphas:
        res = run_simulation(alpha, special_beta, special_vol_period, bt)
        special_results.append(res)
    
    # Ranges for sweep
    alphas = np.linspace(0.0, 0.3, 4)
    betas = np.linspace(0.4, 0.9, 11)
    vol_periods = ['1M']

    print(f"Running sweep: {len(alphas) * len(betas) * len(vol_periods)} combinations...")
    sweep_results = []
    for alpha in alphas:
        for beta in betas:
            for vol_period in vol_periods:
                res = run_simulation(alpha, beta, vol_period, bt)
                sweep_results.append(res)
    
    # Create DataFrames
    df_special = pd.DataFrame(special_results)
    df_sweep = pd.DataFrame(sweep_results)
    
    # Sort sweep results by sharpe reverse
    df_sweep = df_sweep.sort_values(by='sharpe', ascending=False)
    
    # Combine: special cases at top, then sorted sweep
    df_final = pd.concat([df_special, df_sweep], ignore_index=True)
    
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sweep_results.csv')
    df_final.to_csv(output_file, index=False)
    print(f"Sweep completed. Results saved to {output_file}")

if __name__ == "__main__":
    run_sweep()

