import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import sys

# Add the current directory to sys.path to allow importing constants
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from constants import TOTAL_VALUE_COL
except ImportError:
    # Fallback if constants cannot be imported directly
    TOTAL_VALUE_COL = 'Total Value'

def plot_portfolio_comparison(portfolio_histories, title="Portfolio Performance Comparison", log_y=True):
    """
    Plots the total value and leverage of multiple portfolios over time using Plotly.
    
    Args:
        portfolio_histories (dict): Dictionary mapping portfolio names to their history DataFrames.
                                   Each DataFrame should have TOTAL_VALUE_COL and be indexed by date.
                                   Dynamic portfolios should have a 'Leverage' column.
        title (str): Title for the plot.
        log_y (bool): Whether to use a logarithmic scale for the y-axis.
    """
    # Check if any portfolio has leverage data
    has_leverage = any('Leverage' in df.columns for df in portfolio_histories.values() if not df.empty)
    
    if has_leverage:
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.1,
            subplot_titles=(title, "Strategy Leverage"),
            row_heights=[0.7, 0.3]
        )
    else:
        fig = go.Figure()

    # Track colors to keep them consistent between subplots
    colors = {}
    
    for name, df in portfolio_histories.items():
        if df.empty:
            continue
            
        # Add Total Value trace
        trace = go.Scatter(
            x=df.index,
            y=df[TOTAL_VALUE_COL],
            mode='lines',
            name=name,
            hovertemplate='%{y:$.2f}<extra>' + name + '</extra>'
        )
        
        if has_leverage:
            fig.add_trace(trace, row=1, col=1)
            # Store the color assigned by plotly if possible, or let it auto-assign
            # To ensure matching colors, we can use the default color cycle manually if needed
        else:
            fig.add_trace(trace)

        # Add Leverage trace if it exists
        if has_leverage and 'Leverage' in df.columns:
            # We use the same color for the leverage line as the value line
            # Plotly will automatically match colors if we don't specify, 
            # but to be safe we can use legendgroup
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Leverage'],
                mode='lines',
                name=f"{name} Leverage",
                showlegend=False, # Don't duplicate legend entries
                legendgroup=name,
                hovertemplate='%{y:.2f}x<extra>' + name + ' Leverage</extra>'
            ), row=2, col=1)
            
            # Link the legend group for the value trace as well
            fig.data[-2].legendgroup = name

    fig.update_layout(
        height=1000 if has_leverage else 800,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(t=80, b=50, l=50, r=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Update axes titles and scales
    if has_leverage:
        fig.update_yaxes(title_text="Total Value ($)", type="log" if log_y else "linear", row=1, col=1)
        fig.update_yaxes(title_text="Leverage (x)", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
    else:
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Total Value ($)",
            yaxis_type="log" if log_y else "linear"
        )

    # Add range selector buttons to the bottom x-axis
    xaxis_to_update = "xaxis2" if has_leverage else "xaxis"
    fig.update_layout({
        f"{xaxis_to_update}_rangeselector": dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    })

    fig.show()

if __name__ == "__main__":
    # This block allows testing if run directly
    print("This module is intended to be imported.")
