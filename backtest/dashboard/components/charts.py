"""Chart-building functions for the dashboard."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import SimulationResults


# Metric display configuration
METRIC_CONFIG = {
    'cagr': {
        'display_name': 'CAGR',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%"
    },
    'max_drawdown': {
        'display_name': 'Max Drawdown',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%"
    },
    'annual_volatility': {
        'display_name': 'Annual Volatility',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%"
    },
    'sharpe_ratio': {
        'display_name': 'Sharpe Ratio',
        'format': '.2f',
        'format_fn': lambda x: f"{x:.2f}"
    },
    'total_value': {
        'display_name': 'Total Value',
        'format': '$,.0f',
        'format_fn': lambda x: f"${x:,.0f}"
    }
}


def create_distribution_chart(
    results: SimulationResults,
    metric: str,
    title: str = None
) -> go.Figure:
    """Create distribution histogram with historical marker.

    Args:
        results: SimulationResults containing MC and historical data
        metric: Metric name (cagr, max_drawdown, sharpe_ratio, annual_volatility, total_value)
        title: Optional custom title

    Returns:
        Plotly Figure object
    """
    values = results.get_metric_distribution(metric)
    config = METRIC_CONFIG.get(metric, {'display_name': metric.replace('_', ' ').title(), 'format': '.4f'})

    if title is None:
        title = f"{config['display_name']} Distribution (n={len(values)})"

    fig = go.Figure()

    # Histogram of MC results
    fig.add_trace(go.Histogram(
        x=values,
        name='Monte Carlo',
        opacity=0.7,
        nbinsx=50,
        marker_color='#636EFA'
    ))

    # Vertical line for historical result
    if results.historical is not None:
        historical_value = getattr(results.historical, metric)
        fig.add_vline(
            x=historical_value,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"Historical: {config.get('format_fn', str)(historical_value)}",
            annotation_position="top"
        )

    # Format x-axis
    if config['format'].startswith('.') and config['format'].endswith('%'):
        fig.update_xaxes(tickformat=config['format'])
    elif config['format'].startswith('$'):
        fig.update_xaxes(tickformat=config['format'])
    else:
        fig.update_xaxes(tickformat=config['format'])

    fig.update_layout(
        title=title,
        xaxis_title=config['display_name'],
        yaxis_title='Count',
        template='plotly_white',
        height=350,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig


def create_metrics_grid(results: SimulationResults) -> go.Figure:
    """Create 2x2 grid of distribution charts for key metrics.

    Args:
        results: SimulationResults containing MC and historical data

    Returns:
        Plotly Figure with 2x2 subplots
    """
    metrics = ['cagr', 'max_drawdown', 'sharpe_ratio', 'annual_volatility']
    titles = [METRIC_CONFIG[m]['display_name'] for m in metrics]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=titles,
        horizontal_spacing=0.12,
        vertical_spacing=0.15
    )

    for i, metric in enumerate(metrics):
        row = i // 2 + 1
        col = i % 2 + 1

        values = results.get_metric_distribution(metric)
        config = METRIC_CONFIG[metric]

        # Add histogram
        fig.add_trace(
            go.Histogram(
                x=values,
                nbinsx=30,
                marker_color='#636EFA',
                opacity=0.7,
                showlegend=False
            ),
            row=row, col=col
        )

        # Add historical line
        if results.historical is not None:
            historical_value = getattr(results.historical, metric)
            fig.add_vline(
                x=historical_value,
                line_dash="dash",
                line_color="red",
                line_width=2,
                row=row, col=col
            )

        # Format axis
        if config['format'].endswith('%'):
            fig.update_xaxes(tickformat=config['format'], row=row, col=col)

    fig.update_layout(
        height=600,
        showlegend=False,
        template='plotly_white',
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig


def create_summary_table(results: SimulationResults) -> go.Figure:
    """Create formatted table showing summary statistics.

    Args:
        results: SimulationResults containing MC and historical data

    Returns:
        Plotly Figure with table
    """
    summary = results.summary()

    if not summary:
        # Return empty table if no results
        return go.Figure(data=[go.Table(
            header=dict(values=['No data available']),
            cells=dict(values=[[]])
        )])

    # Build table data
    headers = ['Metric', 'Historical', 'MC Mean', 'MC Median', '5th %ile', '95th %ile', 'Hist %ile']

    metrics_order = ['cagr', 'max_drawdown', 'sharpe_ratio', 'annual_volatility', 'total_value']
    rows = {h: [] for h in headers}

    for metric in metrics_order:
        if metric not in summary:
            continue

        stats = summary[metric]
        config = METRIC_CONFIG.get(metric, {'display_name': metric, 'format_fn': lambda x: f"{x:.4f}"})
        fmt = config.get('format_fn', lambda x: f"{x:.4f}")

        rows['Metric'].append(config['display_name'])
        rows['Historical'].append(fmt(stats.get('historical', 0)))
        rows['MC Mean'].append(fmt(stats['mean']))
        rows['MC Median'].append(fmt(stats['median']))
        rows['5th %ile'].append(fmt(stats['p5']))
        rows['95th %ile'].append(fmt(stats['p95']))
        rows['Hist %ile'].append(f"{stats.get('historical_percentile', 0):.1f}%")

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headers,
            fill_color='#636EFA',
            font=dict(color='white', size=12),
            align='center',
            height=30
        ),
        cells=dict(
            values=[rows[h] for h in headers],
            fill_color='white',
            font=dict(size=11),
            align='center',
            height=25
        )
    )])

    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


def create_empty_figure(message: str = "No data") -> go.Figure:
    """Create an empty figure with a message.

    Args:
        message: Message to display

    Returns:
        Plotly Figure with annotation
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        template='plotly_white',
        height=350
    )
    return fig
