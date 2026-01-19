"""Chart-building functions for the dashboard."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import SimulationResults

# Theme configuration
THEME_CONFIG = {
    'light': {
        'template': 'plotly_white',
        'primary_color': '#0891b2',
        'histogram_color': '#06b6d4',
        'historical_line': '#dc2626',
        'table_header_fill': '#0e7490',
        'table_header_font': '#ffffff',
        'table_cell_fill': '#fafafa',
        'table_cell_font': '#1f2937',
        'table_selected_fill': '#cffafe',
        'table_line_color': '#e5e7eb',
        'annotation_color': '#6b7280',
        'plot_bgcolor': '#ffffff',
        'paper_bgcolor': '#ffffff',
        'grid_color': '#f3f4f6',
        'text_color': '#111827',
    },
    'dark': {
        'template': None,
        'primary_color': '#22d3ee',
        'histogram_color': '#06b6d4',
        'historical_line': '#fb923c',
        'table_header_fill': '#1e293b',
        'table_header_font': '#f1f5f9',
        'table_cell_fill': '#0f172a',
        'table_cell_font': '#e2e8f0',
        'table_selected_fill': '#164e63',
        'table_line_color': '#334155',
        'annotation_color': '#94a3b8',
        'plot_bgcolor': '#0f172a',
        'paper_bgcolor': '#020617',
        'grid_color': '#1e293b',
        'text_color': '#f1f5f9',
    }
}

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
        'higher_is_better': True,
    },
    'annual_volatility': {
        'display_name': 'Annual Volatility',
        'format': '.1%',
        'format_fn': lambda x: f"{x*100:.2f}%",
        'higher_is_better': False,
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

MULTI_SELECT_COLORS = [
    {'fill': 'rgba(6, 182, 212, 0.5)', 'line': '#06b6d4'},
    {'fill': 'rgba(168, 85, 247, 0.5)', 'line': '#a855f7'},
    {'fill': 'rgba(34, 197, 94, 0.5)', 'line': '#22c55e'},
    {'fill': 'rgba(251, 146, 60, 0.5)', 'line': '#fb923c'},
]


def get_theme(dark_mode: bool = False) -> dict:
    """Get theme configuration based on dark mode state."""
    return THEME_CONFIG['dark'] if dark_mode else THEME_CONFIG['light']


def _apply_theme(fig: go.Figure, dark_mode: bool) -> None:
    """Apply theme settings to a Plotly figure."""
    theme = get_theme(dark_mode)

    if dark_mode:
        fig.update_layout(
            paper_bgcolor=theme['paper_bgcolor'],
            plot_bgcolor=theme['plot_bgcolor'],
            font=dict(
                color=theme['text_color'],
                family='Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            ),
        )
        axis_config = dict(
            gridcolor=theme['grid_color'],
            linecolor=theme['table_line_color'],
            tickfont=dict(color=theme['annotation_color']),
            title_font=dict(color=theme['text_color']),
            zerolinecolor=theme['table_line_color'],
        )
        fig.update_xaxes(**axis_config)
        fig.update_yaxes(**axis_config)
    else:
        fig.update_layout(template=theme['template'])


def create_metrics_grid(results: SimulationResults, dark_mode: bool = False) -> go.Figure:
    """Create 2x2 grid of distribution charts for key metrics."""
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
        row, col = i // 2 + 1, i % 2 + 1
        values = results.get_metric_distribution(metric)
        config = METRIC_CONFIG[metric]

        fig.add_trace(
            go.Histogram(
                x=values, nbinsx=30,
                marker_color=theme['histogram_color'],
                opacity=0.7, showlegend=False
            ),
            row=row, col=col
        )

        if results.historical is not None:
            historical_value = getattr(results.historical, metric)
            fig.add_vline(
                x=historical_value, line_dash="dash",
                line_color=theme['historical_line'], line_width=2,
                row=row, col=col
            )

        if config['format'].endswith('%'):
            fig.update_xaxes(tickformat=config['format'], row=row, col=col)

    fig.update_layout(height=600, showlegend=False, margin=dict(l=50, r=50, t=80, b=50))
    _apply_theme(fig, dark_mode)

    if dark_mode:
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(color=theme['text_color'], size=14)

    return fig


def create_multi_metrics_grid(results_list: list, dark_mode: bool = False) -> go.Figure:
    """Create 2x2 grid of overlaid distribution charts for multiple portfolios."""
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
        row, col = i // 2 + 1, i % 2 + 1
        config = METRIC_CONFIG[metric]

        for j, (label, results) in enumerate(results_list):
            color_cfg = MULTI_SELECT_COLORS[j % len(MULTI_SELECT_COLORS)]
            values = results.get_metric_distribution(metric)

            fig.add_trace(
                go.Histogram(
                    x=values, nbinsx=30,
                    marker_color=color_cfg['fill'],
                    marker_line_color=color_cfg['line'],
                    marker_line_width=1, opacity=0.6,
                    name=label, legendgroup=label,
                    showlegend=(i == 0),
                ),
                row=row, col=col
            )

        for j, (label, results) in enumerate(results_list):
            if results.historical is not None:
                historical_value = getattr(results.historical, metric)
                color_cfg = MULTI_SELECT_COLORS[j % len(MULTI_SELECT_COLORS)]
                fig.add_vline(
                    x=historical_value, line_dash="dash",
                    line_color=color_cfg['line'], line_width=2,
                    row=row, col=col
                )

        if config['format'].endswith('%'):
            fig.update_xaxes(tickformat=config['format'], row=row, col=col)

    fig.update_layout(
        height=600, showlegend=True, barmode='overlay',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=50, r=50, t=100, b=50),
    )
    _apply_theme(fig, dark_mode)

    if dark_mode:
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(color=theme['text_color'], size=14)

    return fig


def create_empty_figure(message: str = "No data", dark_mode: bool = False) -> go.Figure:
    """Create an empty figure with a message."""
    theme = get_theme(dark_mode)
    fig = go.Figure()
    fig.add_annotation(
        text=message, xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=16, color=theme['annotation_color'])
    )
    fig.update_layout(height=350, xaxis=dict(visible=False), yaxis=dict(visible=False))

    if dark_mode:
        fig.update_layout(paper_bgcolor=theme['paper_bgcolor'], plot_bgcolor=theme['plot_bgcolor'])
    else:
        fig.update_layout(template=theme['template'], paper_bgcolor='rgba(0,0,0,0)')

    return fig


def _get_color_for_value(value: float, min_val: float, max_val: float, higher_is_better: bool = True) -> str:
    """Get a green color with opacity based on value ranking."""
    if max_val == min_val:
        return 'rgba(34, 197, 94, 0.5)'

    normalized = (value - min_val) / (max_val - min_val)
    if not higher_is_better:
        normalized = 1 - normalized

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
    """Create a 2D clickable grid showing selected metric for each portfolio x simulation."""
    import dash_bootstrap_components as dbc
    from dash import html

    theme = get_theme(dark_mode)
    metric_cfg = METRIC_CONFIG.get(metric, METRIC_CONFIG['cagr'])
    format_fn = metric_cfg['format_fn']
    higher_is_better = metric_cfg.get('higher_is_better', True)

    # Collect MC median values for color scaling
    all_mc_values = []
    for portfolio_id in active_portfolios:
        for sim_id in active_simulations:
            key = f"{portfolio_id}|{sim_id}"
            results = all_results.get(key)
            if results:
                mc_median = _extract_mc_median(results, metric)
                if mc_median is not None:
                    all_mc_values.append(mc_median)

    global_min = min(all_mc_values) if all_mc_values else 0
    global_max = max(all_mc_values) if all_mc_values else 1

    # Build header
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
        header_cells.append(html.Th(simulation_names.get(sim_id, sim_id), style=header_style))

    # Build data rows
    rows = []
    for portfolio_id in active_portfolios:
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

        # Historical value (same for all simulations)
        hist_val = _extract_historical_value(all_results, active_simulations, portfolio_id, metric)
        row_cells.append(html.Td(
            format_fn(hist_val) if hist_val is not None else "N/A",
            style={
                'backgroundColor': theme['table_cell_fill'],
                'color': theme['table_cell_font'],
                'padding': '12px 16px',
                'border': f"1px solid {theme['table_line_color']}",
                'fontWeight': 'bold',
                'textAlign': 'center',
            }
        ))

        # MC median cells
        for sim_id in active_simulations:
            key = f"{portfolio_id}|{sim_id}"
            results = all_results.get(key)
            mc_median = _extract_mc_median(results, metric) if results else None

            bg_color = _get_color_for_value(mc_median, global_min, global_max, higher_is_better) \
                if mc_median is not None else theme['table_cell_fill']

            is_selected = any(
                cell.get('portfolio_id') == portfolio_id and cell.get('simulation_id') == sim_id
                for cell in (selected_cells or [])
            )

            row_cells.append(html.Td(
                dbc.Button(
                    format_fn(mc_median) if mc_median is not None else "N/A",
                    id={'type': 'grid-cell-btn', 'portfolio': portfolio_id, 'simulation': sim_id},
                    n_clicks=0, color='link', className='w-100 h-100',
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

    return dbc.Table(
        [html.Thead(html.Tr(header_cells)), html.Tbody(rows)],
        bordered=True, hover=True, responsive=True,
        style={'backgroundColor': theme['table_cell_fill'], 'marginBottom': '0'}
    )


def _extract_mc_median(results, metric: str):
    """Extract MC median value from results (handles both object and dict formats)."""
    if hasattr(results, 'monte_carlo') and results.monte_carlo:
        values = [getattr(r, metric) for r in results.monte_carlo]
        return np.median(values)
    elif isinstance(results, dict) and results.get('mc_distributions'):
        values = results['mc_distributions'].get(metric, [])
        return np.median(values) if values else None
    return None


def _extract_historical_value(all_results, active_simulations, portfolio_id, metric):
    """Extract historical value for a portfolio (same across all simulations)."""
    for sim_id in active_simulations:
        key = f"{portfolio_id}|{sim_id}"
        results = all_results.get(key)
        if results:
            if hasattr(results, 'historical') and results.historical:
                return getattr(results.historical, metric, None)
            elif isinstance(results, dict) and results.get('historical'):
                return results['historical'].get(metric)
    return None
