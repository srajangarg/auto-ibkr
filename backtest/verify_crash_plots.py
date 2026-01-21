#!/usr/bin/env python3
"""Generate 100 plots of crash scenarios for visual verification."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from monte_carlo import (
    MonteCarloConfig, CrashConfig, generate_monte_carlo_df
)
from backtester import Backtester, DynamicLeveragedPortfolio
from constants import TOTAL_VALUE_COL


def run_crash_simulation_with_history(
    config: MonteCarloConfig,
    seed_offset: int,
    initial_amt: float = 10000,
    monthly_cf: float = 200
) -> pd.DataFrame:
    """Run a single crash simulation and return the portfolio history."""
    df = generate_monte_carlo_df(config, seed_offset=seed_offset, inject_crash_event=True)
    bt = Backtester(df=df, initial_amt=initial_amt, monthly_cf=monthly_cf)
    portfolio = DynamicLeveragedPortfolio('QQQ', alpha=0.0, beta=0.7, target_return=0.12)
    bt.run(portfolio)
    return portfolio.get_history_df()


def main():
    # Configure for 100% crash probability over 5 years
    crash_config = CrashConfig(
        crash_probability=1.0,  # 100% of simulations get a crash
        min_crash_start_days=252,   # Crash starts 1 year from now at earliest
        max_crash_start_days=630,   # Crash starts 2.5 years from now at latest
        min_decline=0.30,  # 30% minimum decline
        max_decline=0.50,  # 50% maximum decline
        min_crash_duration_days=20,  # Crash lasts 20-40 trading days
        max_crash_duration_days=40
    )

    mc_config = MonteCarloConfig(
        num_simulations=100,
        num_days=252 * 5,  # 5 years
        tickers=['QQQ', 'QQQx3'],
        seed=42,
        use_garch=True,
        crash_config=crash_config
    )

    print("Generating 100 crash scenarios...")

    # Run 100 simulations and collect histories
    histories = []
    for i in range(100):
        if (i + 1) % 10 == 0:
            print(f"  Running simulation {i + 1}/100")
        history = run_crash_simulation_with_history(mc_config, seed_offset=i)
        histories.append(history)

    print("Creating plot...")

    # Create a single plot with all 100 trajectories
    fig = go.Figure()

    for i, history in enumerate(histories):
        # Normalize to start at 100 for easier comparison
        values = history[TOTAL_VALUE_COL].values
        normalized = values / values[0] * 100

        fig.add_trace(go.Scatter(
            x=list(range(len(normalized))),
            y=normalized,
            mode='lines',
            line=dict(width=0.5, color='rgba(31, 119, 180, 0.3)'),
            name=f'Sim {i+1}',
            showlegend=False,
            hovertemplate=f'Sim {i+1}<br>Day: %{{x}}<br>Value: %{{y:.1f}}<extra></extra>'
        ))

    # Add median line
    all_values = np.array([h[TOTAL_VALUE_COL].values / h[TOTAL_VALUE_COL].values[0] * 100 for h in histories])
    median_line = np.median(all_values, axis=0)

    fig.add_trace(go.Scatter(
        x=list(range(len(median_line))),
        y=median_line,
        mode='lines',
        line=dict(width=2, color='red'),
        name='Median',
        showlegend=True
    ))

    # Add year markers
    for year in range(1, 6):
        day = year * 252
        if day < len(median_line):
            fig.add_vline(x=day, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_annotation(x=day, y=1.05, yref="paper", text=f"Year {year}", showarrow=False)

    fig.update_layout(
        title="100 Crash Scenarios (5 Years) - 100% Crash Probability<br><sub>30-50% decline within first 2 years, crash duration ~40 days</sub>",
        xaxis_title="Trading Days",
        yaxis_title="Portfolio Value (Normalized to 100, Log Scale)",
        yaxis_type="log",
        height=600,
        width=1000,
        hovermode='closest'
    )

    # Save and show
    fig.write_html("crash_scenarios_100_plots.html")
    print("Saved to crash_scenarios_100_plots.html")
    fig.show()

    # Also create a grid of individual plots (10x10) for detailed inspection
    print("\nCreating 10x10 grid of individual plots...")

    fig_grid = make_subplots(
        rows=10, cols=10,
        subplot_titles=[f"#{i+1}" for i in range(100)],
        horizontal_spacing=0.02,
        vertical_spacing=0.03
    )

    for i, history in enumerate(histories):
        row = i // 10 + 1
        col = i % 10 + 1

        values = history[TOTAL_VALUE_COL].values
        normalized = values / values[0] * 100

        fig_grid.add_trace(
            go.Scatter(
                x=list(range(len(normalized))),
                y=normalized,
                mode='lines',
                line=dict(width=0.8, color='steelblue'),
                showlegend=False
            ),
            row=row, col=col
        )

    fig_grid.update_layout(
        title="100 Crash Scenarios - Individual Plots (10x10 Grid)",
        height=1500,
        width=1500,
        showlegend=False
    )

    # Hide axis labels for cleaner look, use log scale
    fig_grid.update_xaxes(showticklabels=False)
    fig_grid.update_yaxes(showticklabels=False, type="log")

    fig_grid.write_html("crash_scenarios_grid.html")
    print("Saved to crash_scenarios_grid.html")
    fig_grid.show()


if __name__ == "__main__":
    main()
