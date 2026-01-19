"""Chart-building functions for the dashboard."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import SimulationResults


# ══════════════════════════════════════════════════════════════════════════════
# REFINED DARK THEME - Premium Financial Terminal Aesthetic
# ══════════════════════════════════════════════════════════════════════════════
#
# Color Philosophy:
# - Deep charcoal backgrounds (not bluish-grey) for a premium feel
# - Cyan/teal primary accent - modern, distinctive, high contrast
# - Warm coral for historical markers - draws attention without clashing
# - Subtle gradients in fills for depth
# - High contrast text for readability

THEME_CONFIG = {
    'light': {
        'template': 'plotly_white',
        'primary_color': '#0891b2',        # Cyan-600
        'histogram_color': '#06b6d4',      # Cyan-500
        'historical_line': '#dc2626',      # Red-600
        'table_header_fill': '#0e7490',    # Cyan-700
        'table_header_font': '#ffffff',
        'table_cell_fill': '#fafafa',
        'table_cell_font': '#1f2937',
        'table_selected_fill': '#cffafe',  # Cyan-100
        'table_line_color': '#e5e7eb',
        'annotation_color': '#6b7280',
        'plot_bgcolor': '#ffffff',
        'paper_bgcolor': '#ffffff',
        'grid_color': '#f3f4f6',
        'text_color': '#111827',
    },
    'dark': {
        'template': None,  # We'll use custom layout settings
        'primary_color': '#22d3ee',        # Cyan-400 - vibrant teal
        'histogram_color': '#06b6d4',      # Cyan-500 - rich teal
        'historical_line': '#fb923c',      # Orange-400 - warm coral
        'table_header_fill': '#1e293b',    # Slate-800 - refined dark blue-grey
        'table_header_font': '#f1f5f9',    # Slate-100
        'table_cell_fill': '#0f172a',      # Slate-900 - deep charcoal
        'table_cell_font': '#e2e8f0',      # Slate-200
        'table_selected_fill': '#164e63',  # Cyan-900 - subtle highlight
        'table_line_color': '#334155',     # Slate-700
        'annotation_color': '#94a3b8',     # Slate-400
        'plot_bgcolor': '#0f172a',         # Slate-900
        'paper_bgcolor': '#020617',        # Slate-950 - near black
        'grid_color': '#1e293b',           # Slate-800
        'text_color': '#f1f5f9',           # Slate-100
    }
}


def _apply_dark_theme(fig: go.Figure, theme: dict) -> None:
    """Apply refined dark theme settings to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor=theme.get('paper_bgcolor', 'rgba(0,0,0,0)'),
        plot_bgcolor=theme.get('plot_bgcolor', '#0f172a'),
        font=dict(
            color=theme.get('text_color', '#f1f5f9'),
            family='Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        ),
    )
    fig.update_xaxes(
        gridcolor=theme.get('grid_color', '#1e293b'),
        linecolor=theme.get('table_line_color', '#334155'),
        tickfont=dict(color=theme.get('annotation_color', '#94a3b8')),
        title_font=dict(color=theme.get('text_color', '#cbd5e1')),
        zerolinecolor=theme.get('table_line_color', '#334155'),
    )
    fig.update_yaxes(
        gridcolor=theme.get('grid_color', '#1e293b'),
        linecolor=theme.get('table_line_color', '#334155'),
        tickfont=dict(color=theme.get('annotation_color', '#94a3b8')),
        title_font=dict(color=theme.get('text_color', '#cbd5e1')),
        zerolinecolor=theme.get('table_line_color', '#334155'),
    )


def get_theme(dark_mode: bool = False) -> dict:
    """Get theme configuration based on dark mode state."""
    return THEME_CONFIG['dark'] if dark_mode else THEME_CONFIG['light']


# Metric display configuration
METRIC_CONFIG = {
    'cagr': {
        'display_name': 'CAGR',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%",
        'higher_is_better': True,
    },
    'max_drawdown': {
        'display_name': 'Max Drawdown',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%",
        'higher_is_better': True,  # Less negative (closer to 0) is better, so higher values are better
    },
    'annual_volatility': {
        'display_name': 'Annual Volatility',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%",
        'higher_is_better': False,  # Lower volatility is better
    },
    'sharpe_ratio': {
        'display_name': 'Sharpe Ratio',
        'format': '.2f',
        'format_fn': lambda x: f"{x:.2f}",
        'higher_is_better': True,
    },
    'total_value': {
        'display_name': 'Total Value',
        'format': '$,.0f',
        'format_fn': lambda x: f"${x:,.0f}",
        'higher_is_better': True,
    }
}

# Multi-selection color palette (up to 4 distinct colors for overlaid distributions)
MULTI_SELECT_COLORS = [
    {'fill': 'rgba(6, 182, 212, 0.5)', 'line': '#06b6d4'},    # Cyan
    {'fill': 'rgba(168, 85, 247, 0.5)', 'line': '#a855f7'},   # Purple
    {'fill': 'rgba(34, 197, 94, 0.5)', 'line': '#22c55e'},    # Green
    {'fill': 'rgba(251, 146, 60, 0.5)', 'line': '#fb923c'},   # Orange
]


def create_distribution_chart(
    results: SimulationResults,
    metric: str,
    title: str = None,
    dark_mode: bool = False
) -> go.Figure:
    """Create distribution histogram with historical marker.

    Args:
        results: SimulationResults containing MC and historical data
        metric: Metric name (cagr, max_drawdown, sharpe_ratio, annual_volatility, total_value)
        title: Optional custom title
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure object
    """
    theme = get_theme(dark_mode)
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
        marker_color=theme['histogram_color']
    ))

    # Vertical line for historical result
    if results.historical is not None:
        historical_value = getattr(results.historical, metric)
        fig.add_vline(
            x=historical_value,
            line_dash="dash",
            line_color=theme['historical_line'],
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
        height=350,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Apply theme
    if dark_mode:
        _apply_dark_theme(fig, theme)
    else:
        fig.update_layout(template=theme['template'])

    return fig


def create_metrics_grid(results: SimulationResults, dark_mode: bool = False) -> go.Figure:
    """Create 2x2 grid of distribution charts for key metrics.

    Args:
        results: SimulationResults containing MC and historical data
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure with 2x2 subplots
    """
    theme = get_theme(dark_mode)
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
                marker_color=theme['histogram_color'],
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
                line_color=theme['historical_line'],
                line_width=2,
                row=row, col=col
            )

        # Format axis
        if config['format'].endswith('%'):
            fig.update_xaxes(tickformat=config['format'], row=row, col=col)

    fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Apply theme
    if dark_mode:
        _apply_dark_theme(fig, theme)
        # Update subplot title colors for dark mode
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(color=theme['text_color'], size=14)
    else:
        fig.update_layout(template=theme['template'])

    return fig


def create_multi_metrics_grid(
    results_list: list,
    dark_mode: bool = False
) -> go.Figure:
    """Create 2x2 grid of overlaid distribution charts for multiple portfolios.

    Args:
        results_list: List of tuples (portfolio_name, SimulationResults)
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure with 2x2 subplots with overlaid histograms
    """
    theme = get_theme(dark_mode)
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
        config = METRIC_CONFIG[metric]

        # Add histogram for each portfolio (overlaid)
        for j, (label, results) in enumerate(results_list):
            color_cfg = MULTI_SELECT_COLORS[j % len(MULTI_SELECT_COLORS)]
            values = results.get_metric_distribution(metric)

            fig.add_trace(
                go.Histogram(
                    x=values,
                    nbinsx=30,
                    marker_color=color_cfg['fill'],
                    marker_line_color=color_cfg['line'],
                    marker_line_width=1,
                    opacity=0.6,
                    name=label,
                    legendgroup=label,
                    showlegend=(i == 0),  # Only show legend in first subplot
                ),
                row=row, col=col
            )

        # Add historical lines for each portfolio
        for j, (label, results) in enumerate(results_list):
            if results.historical is not None:
                historical_value = getattr(results.historical, metric)
                color_cfg = MULTI_SELECT_COLORS[j % len(MULTI_SELECT_COLORS)]
                fig.add_vline(
                    x=historical_value,
                    line_dash="dash",
                    line_color=color_cfg['line'],
                    line_width=2,
                    row=row, col=col
                )

        # Format axis
        if config['format'].endswith('%'):
            fig.update_xaxes(tickformat=config['format'], row=row, col=col)

    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(l=50, r=50, t=100, b=50),  # Extra top margin for legend
        barmode='overlay'  # Overlay histograms
    )

    # Apply theme
    if dark_mode:
        _apply_dark_theme(fig, theme)
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(color=theme['text_color'], size=14)
    else:
        fig.update_layout(template=theme['template'])

    return fig


def create_summary_table(results: SimulationResults, dark_mode: bool = False) -> go.Figure:
    """Create formatted table showing summary statistics for a single portfolio.

    Args:
        results: SimulationResults containing MC and historical data
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure with table
    """
    theme = get_theme(dark_mode)
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
            fill_color=theme['table_header_fill'],
            font=dict(color=theme['table_header_font'], size=12),
            align='center',
            height=30,
            line_color=theme['table_line_color']
        ),
        cells=dict(
            values=[rows[h] for h in headers],
            fill_color=theme['table_cell_fill'],
            font=dict(color=theme['table_cell_font'], size=11),
            align='center',
            height=25,
            line_color=theme['table_line_color']
        )
    )])

    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_multi_portfolio_table(
    all_results: dict,
    portfolio_names: dict,
    selected_portfolio_id: str = None,
    dark_mode: bool = False
) -> go.Figure:
    """Create a comparison table with portfolios as rows.

    Table structure:
    - Rows: Each portfolio
    - Columns: Portfolio Name | CAGR (Hist/MC) | Drawdown (Hist/MC) | Sharpe (Hist/MC) | Volatility (Hist/MC)

    Args:
        all_results: Dict mapping portfolio_id -> SimulationResults
        portfolio_names: Dict mapping portfolio_id -> display_name
        selected_portfolio_id: Currently selected portfolio (for highlighting)
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure with table
    """
    theme = get_theme(dark_mode)

    if not all_results:
        empty_fig = go.Figure(data=[go.Table(
            header=dict(values=['No data available']),
            cells=dict(values=[[]])
        )])
        return empty_fig, []

    # Define the metrics we want to show (4 metrics x 2 values each)
    metrics = ['cagr', 'max_drawdown', 'sharpe_ratio', 'annual_volatility']

    # Build header with sub-columns
    headers = ['<b>Portfolio</b>']
    for metric in metrics:
        config = METRIC_CONFIG[metric]
        name = config['display_name']
        headers.extend([f'<b>{name}</b><br>Historical', f'<b>{name}</b><br>MC Median'])

    # Build rows
    portfolio_ids = []
    portfolio_col = []
    metric_cols = {m: {'hist': [], 'mc': []} for m in metrics}

    for portfolio_id, results in all_results.items():
        portfolio_ids.append(portfolio_id)
        portfolio_col.append(portfolio_names.get(portfolio_id, portfolio_id))

        summary = results.summary()
        for metric in metrics:
            config = METRIC_CONFIG[metric]
            fmt = config.get('format_fn', lambda x: f"{x:.4f}")

            if metric in summary:
                stats = summary[metric]
                metric_cols[metric]['hist'].append(fmt(stats.get('historical', 0)))
                metric_cols[metric]['mc'].append(fmt(stats['median']))
            else:
                metric_cols[metric]['hist'].append('N/A')
                metric_cols[metric]['mc'].append('N/A')

    # Assemble cell values in column order
    cell_values = [portfolio_col]
    for metric in metrics:
        cell_values.append(metric_cols[metric]['hist'])
        cell_values.append(metric_cols[metric]['mc'])

    # Row highlighting for selected portfolio
    num_rows = len(portfolio_ids)
    fill_colors = []
    for i, pid in enumerate(portfolio_ids):
        if pid == selected_portfolio_id:
            fill_colors.append(theme['table_selected_fill'])
        else:
            fill_colors.append(theme['table_cell_fill'])

    # Create consistent fill color arrays for each column
    cell_fill_colors = [fill_colors] * len(cell_values)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headers,
            fill_color=theme['table_header_fill'],
            font=dict(color=theme['table_header_font'], size=11),
            align='center',
            height=40,
            line_color=theme['table_line_color']
        ),
        cells=dict(
            values=cell_values,
            fill_color=cell_fill_colors,
            font=dict(color=theme['table_cell_font'], size=11),
            align='center',
            height=35,
            line_color=theme['table_line_color']
        ),
        # Store portfolio_ids in customdata for click handling
        customdata=[portfolio_ids] * len(cell_values)
    )])

    # Calculate height based on number of rows
    table_height = 80 + (num_rows * 40)  # header + rows

    fig.update_layout(
        height=max(150, table_height),
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor=theme.get('paper_bgcolor', 'rgba(0,0,0,0)') if dark_mode else 'rgba(0,0,0,0)'
    )

    return fig, portfolio_ids


def create_multi_portfolio_table_data(
    all_results: dict,
    portfolio_names: dict,
) -> tuple:
    """Create data and columns for a DataTable showing portfolio comparison.

    Table structure:
    - Rows: Each portfolio
    - Columns: Portfolio Name | CAGR (Hist/MC) | Drawdown (Hist/MC) | Sharpe (Hist/MC) | Volatility (Hist/MC)

    Uses hierarchical column headers where metrics are top-level and Hist/MC are sub-headers.

    Args:
        all_results: Dict mapping portfolio_id -> SimulationResults
        portfolio_names: Dict mapping portfolio_id -> display_name

    Returns:
        Tuple of (data_rows, columns, portfolio_ids)
    """
    if not all_results:
        return [], [], []

    # Define the metrics we want to show
    metrics = ['cagr', 'max_drawdown', 'sharpe_ratio', 'annual_volatility']

    # Build columns for DataTable with hierarchical headers
    # Using list format for multi-level headers: ['Top Level', 'Sub Level']
    columns = [
        {'name': ['', 'Portfolio'], 'id': 'portfolio_name'},
    ]
    for metric in metrics:
        config = METRIC_CONFIG[metric]
        name = config['display_name']
        columns.append({'name': [name, 'Hist'], 'id': f'{metric}_hist'})
        columns.append({'name': [name, 'MC'], 'id': f'{metric}_mc'})

    # Build rows
    data_rows = []
    portfolio_ids = []

    for portfolio_id, results in all_results.items():
        portfolio_ids.append(portfolio_id)
        row = {
            'portfolio_id': portfolio_id,  # Hidden ID for selection
            'portfolio_name': portfolio_names.get(portfolio_id, portfolio_id),
        }

        summary = results.summary()
        for metric in metrics:
            config = METRIC_CONFIG[metric]
            fmt = config.get('format_fn', lambda x: f"{x:.4f}")

            if metric in summary:
                stats = summary[metric]
                row[f'{metric}_hist'] = fmt(stats.get('historical', 0))
                row[f'{metric}_mc'] = fmt(stats['median'])
            else:
                row[f'{metric}_hist'] = 'N/A'
                row[f'{metric}_mc'] = 'N/A'

        data_rows.append(row)

    return data_rows, columns, portfolio_ids


def get_datatable_style(dark_mode: bool = False) -> dict:
    """Get DataTable styling based on dark mode state.

    Args:
        dark_mode: Enable dark mode styling

    Returns:
        Dict with style_header, style_cell, style_data, style_data_conditional
    """
    theme = get_theme(dark_mode)

    return {
        'style_header': {
            'backgroundColor': theme['table_header_fill'],
            'color': theme['table_header_font'],
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border': f"1px solid {theme['table_line_color']}",
        },
        'style_cell': {
            'textAlign': 'center',
            'padding': '10px',
            'border': f"1px solid {theme['table_line_color']}",
            'fontSize': '13px',
        },
        'style_data': {
            'backgroundColor': theme['table_cell_fill'],
            'color': theme['table_cell_font'],
        },
        'style_data_conditional': [
            {
                'if': {'state': 'selected'},
                'backgroundColor': theme['table_selected_fill'],
                'border': f"1px solid {theme['primary_color']}",
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': theme['table_selected_fill'],
                'border': f"1px solid {theme['primary_color']}",
            },
        ],
        'style_table': {
            'overflowX': 'auto',
        },
    }


def _get_color_for_value(value: float, min_val: float, max_val: float, higher_is_better: bool = True) -> str:
    """Get a light green color with linear opacity based on value ranking.

    Best value in the range gets full opacity, worst gets transparent.

    Args:
        value: The value to color
        min_val: Minimum value in the range
        max_val: Maximum value in the range
        higher_is_better: If True, high value = high opacity; if False, low value = high opacity

    Returns:
        RGBA color string
    """
    if max_val == min_val:
        return 'rgba(34, 197, 94, 0.5)'  # Medium opacity if all values are the same

    # Normalize to 0-1
    normalized = (value - min_val) / (max_val - min_val)

    # If lower is better, invert so lower values get higher opacity
    if not higher_is_better:
        normalized = 1 - normalized

    # Light green with linear opacity (0.1 to 0.6 range for subtlety)
    opacity = 0.1 + (normalized * 0.5)
    return f'rgba(34, 197, 94, {opacity:.2f})'


def create_results_grid(
    all_results: dict,
    active_portfolios: list,
    active_simulations: list,
    portfolio_names: dict,
    simulation_names: dict,
    selected_cells: list,
    dark_mode: bool = False,
    metric: str = 'cagr'
):
    """Create a 2D clickable grid showing selected metric for each portfolio × simulation combination.

    Grid structure:
    - Column 1: Portfolio name
    - Column 2: Historical value (same for all simulations)
    - Columns 3+: MC median values for each simulation (clickable, color-coded)

    Args:
        all_results: Dict mapping "portfolio_id|simulation_id" -> SimulationResults or dict
        active_portfolios: List of active portfolio IDs (rows)
        active_simulations: List of active simulation IDs (columns)
        portfolio_names: Dict mapping portfolio_id -> display_name
        simulation_names: Dict mapping simulation_id -> display_name
        selected_cells: List of dicts with 'portfolio_id' and 'simulation_id' keys (multi-select)
        dark_mode: Enable dark mode styling
        metric: Which metric to display ('cagr', 'sharpe_ratio', 'max_drawdown', 'annual_volatility')

    Returns:
        Dash Bootstrap Table component with clickable cells
    """
    import dash_bootstrap_components as dbc
    from dash import html
    import numpy as np

    theme = get_theme(dark_mode)
    metric_cfg = METRIC_CONFIG.get(metric, METRIC_CONFIG['cagr'])
    format_fn = metric_cfg['format_fn']
    higher_is_better = metric_cfg.get('higher_is_better', True)

    # First pass: collect all MC median values for global color scaling
    all_mc_values = []
    for portfolio_id in active_portfolios:
        for sim_id in active_simulations:
            key = f"{portfolio_id}|{sim_id}"
            results = all_results.get(key)
            if results:
                # Handle both SimulationResults objects and dict format
                if hasattr(results, 'monte_carlo') and results.monte_carlo:
                    values = [getattr(r, metric) for r in results.monte_carlo]
                    all_mc_values.append(np.median(values))
                elif isinstance(results, dict) and results.get('mc_distributions'):
                    values = results['mc_distributions'].get(metric, [])
                    if values:
                        all_mc_values.append(np.median(values))

    # Global min/max for consistent color scaling
    global_min = min(all_mc_values) if all_mc_values else 0
    global_max = max(all_mc_values) if all_mc_values else 1

    # Build header row: Portfolio | Historical | Simulation1 | Simulation2 | ...
    header_style = {
        'backgroundColor': theme['table_header_fill'],
        'color': theme['table_header_font'],
        'padding': '12px 16px',
        'border': f"1px solid {theme['table_line_color']}",
        'fontWeight': 'bold',
        'textAlign': 'center',
        'minWidth': '100px',
    }
    header_cells = [
        html.Th("Portfolio", style={**header_style, 'minWidth': '120px'}),
        html.Th("Historical", style=header_style),
    ]
    for sim_id in active_simulations:
        header_cells.append(html.Th(
            simulation_names.get(sim_id, sim_id),
            style=header_style
        ))
    header = html.Thead(html.Tr(header_cells))

    # Build data rows
    rows = []
    for portfolio_id in active_portfolios:
        # Portfolio name cell
        row_cells = [html.Td(
            portfolio_names.get(portfolio_id, portfolio_id),
            style={
                'backgroundColor': theme['table_header_fill'],
                'color': theme['table_header_font'],
                'padding': '12px 16px',
                'border': f"1px solid {theme['table_line_color']}",
                'fontWeight': 'bold',
                'textAlign': 'left',
            }
        )]

        # Get historical value (same for all simulations, just grab from first)
        hist_val = None
        for sim_id in active_simulations:
            key = f"{portfolio_id}|{sim_id}"
            results = all_results.get(key)
            if results:
                if hasattr(results, 'historical') and results.historical:
                    hist_val = getattr(results.historical, metric, None)
                elif isinstance(results, dict) and results.get('historical'):
                    hist_val = results['historical'].get(metric)
                if hist_val is not None:
                    break

        hist_text = format_fn(hist_val) if hist_val is not None else "N/A"

        # Historical value cell (not clickable, neutral background)
        row_cells.append(html.Td(
            hist_text,
            style={
                'backgroundColor': theme['table_cell_fill'],
                'color': theme['table_cell_font'],
                'padding': '12px 16px',
                'border': f"1px solid {theme['table_line_color']}",
                'fontWeight': 'bold',
                'textAlign': 'center',
            }
        ))

        # MC median cells for each simulation (clickable, color-coded)
        for sim_id in active_simulations:
            key = f"{portfolio_id}|{sim_id}"
            results = all_results.get(key)

            mc_median = None

            # Extract MC median value
            if results:
                if hasattr(results, 'monte_carlo') and results.monte_carlo:
                    values = [getattr(r, metric) for r in results.monte_carlo]
                    mc_median = np.median(values)
                elif isinstance(results, dict) and results.get('mc_distributions'):
                    values = results['mc_distributions'].get(metric, [])
                    if values:
                        mc_median = np.median(values)

            mc_text = format_fn(mc_median) if mc_median is not None else "N/A"

            # Get background color based on MC median value (using global scaling)
            if mc_median is not None:
                bg_color = _get_color_for_value(mc_median, global_min, global_max, higher_is_better)
            else:
                bg_color = theme['table_cell_fill']

            # Determine if this cell is selected (check against list)
            is_selected = any(
                cell.get('portfolio_id') == portfolio_id and
                cell.get('simulation_id') == sim_id
                for cell in (selected_cells or [])
            )

            row_cells.append(html.Td(
                dbc.Button(
                    mc_text,
                    id={'type': 'grid-cell-btn', 'portfolio': portfolio_id, 'simulation': sim_id},
                    n_clicks=0,
                    color='link',
                    className='w-100 h-100',
                    style={
                        'color': theme['table_cell_font'],
                        'fontWeight': 'bold' if is_selected else 'normal',
                        'fontSize': '14px',
                        'textDecoration': 'none',
                        'padding': '8px 12px',
                        'margin': '0',
                        'display': 'block',
                        'width': '100%',
                    }
                ),
                style={
                    'backgroundColor': bg_color,
                    'border': f"3px solid {theme['primary_color']}" if is_selected else f"1px solid {theme['table_line_color']}",
                    'padding': '0',
                    'textAlign': 'center',
                    'verticalAlign': 'middle',
                }
            ))

        rows.append(html.Tr(row_cells))

    body = html.Tbody(rows)

    # Create table with styling
    table = dbc.Table(
        [header, body],
        bordered=True,
        hover=True,
        responsive=True,
        style={
            'backgroundColor': theme['table_cell_fill'],
            'marginBottom': '0',
        }
    )

    return table


def create_empty_figure(message: str = "No data", dark_mode: bool = False) -> go.Figure:
    """Create an empty figure with a message.

    Args:
        message: Message to display
        dark_mode: Enable dark mode styling

    Returns:
        Plotly Figure with annotation
    """
    theme = get_theme(dark_mode)
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color=theme['annotation_color'])
    )
    fig.update_layout(
        height=350,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    # Apply theme
    if dark_mode:
        fig.update_layout(
            paper_bgcolor=theme.get('paper_bgcolor', '#020617'),
            plot_bgcolor=theme.get('plot_bgcolor', '#0f172a'),
        )
    else:
        fig.update_layout(
            template=theme['template'],
            paper_bgcolor='rgba(0,0,0,0)'
        )
    return fig
