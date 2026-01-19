"""Dashboard layout definitions."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (
    DEFAULT_INITIAL_AMT,
    DEFAULT_MONTHLY_CF,
)
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from .portfolios import registry
from .simulations import simulation_registry


def create_layout():
    """Create the main dashboard layout.

    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Store for active portfolios (persists client-side)
        dcc.Store(id='active-portfolios-store', data=[]),
        # Store for active simulations (persists client-side)
        dcc.Store(id='active-simulations-store', data=[]),
        # Store for all results keyed by "portfolio_id|simulation_id"
        dcc.Store(id='all-results-store', data={}),
        # Store for selected cells (list of {portfolio_id, simulation_id} dicts for multi-select)
        dcc.Store(id='selected-cell-store', data=[]),

        # Header with dark mode toggle
        dbc.Row([
            dbc.Col([
                html.H1("Backtest Dashboard", className="text-center my-4"),
                html.P(
                    "Compare portfolio strategies with historical and Monte Carlo analysis",
                    className="text-center text-muted mb-4"
                )
            ], md=10),
            dbc.Col([
                html.Div([
                    dbc.Label("Dark Mode", className="me-2", style={"fontSize": "0.9rem"}),
                    dbc.Switch(
                        id='dark-mode-switch',
                        value=True,  # Default to dark mode
                        className="d-inline-block"
                    )
                ], className="d-flex align-items-center justify-content-end mt-4")
            ], md=2)
        ]),

        # Portfolio Manager and Simulation Manager Side by Side
        dbc.Row([
            # Portfolio Manager Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Portfolio Manager", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            # Available Portfolios (left side)
                            dbc.Col([
                                html.Label("Available", className="fw-bold mb-2"),
                                html.Div(
                                    id='available-portfolios-list',
                                    children=_create_available_portfolios_list([])
                                )
                            ], md=6),

                            # Active Portfolios (right side)
                            dbc.Col([
                                html.Label("Active", className="fw-bold mb-2"),
                                html.Div(
                                    id='active-portfolios-list',
                                    children=[
                                        html.P("No portfolios added yet.", className="text-muted")
                                    ]
                                )
                            ], md=6)
                        ])
                    ])
                ], className="h-100")
            ], md=6),

            # MC Simulation Manager Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("MC Simulation Manager", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            # Available Simulations (left side)
                            dbc.Col([
                                html.Label("Available", className="fw-bold mb-2"),
                                html.Div(
                                    id='available-simulations-list',
                                    children=_create_available_simulations_list([])
                                )
                            ], md=6),

                            # Active Simulations (right side)
                            dbc.Col([
                                html.Label("Active", className="fw-bold mb-2"),
                                html.Div(
                                    id='active-simulations-list',
                                    children=[
                                        html.P("No simulations added yet.", className="text-muted")
                                    ]
                                )
                            ], md=6)
                        ])
                    ])
                ], className="h-100")
            ], md=6)
        ], className="mb-4"),

        # Controls Row
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Initial Investment ($)", className="fw-bold"),
                        dbc.Input(
                            id='initial-amt-input',
                            type='number',
                            value=DEFAULT_INITIAL_AMT,
                            min=1000,
                            step=1000,
                            className="mb-2"
                        )
                    ], md=4),

                    dbc.Col([
                        html.Label("Monthly Contribution ($)", className="fw-bold"),
                        dbc.Input(
                            id='monthly-cf-input',
                            type='number',
                            value=DEFAULT_MONTHLY_CF,
                            min=0,
                            step=100,
                            className="mb-2"
                        )
                    ], md=4),

                    dbc.Col([
                        html.Label("\u00A0", className="fw-bold"),  # Non-breaking space for alignment
                        dbc.Button(
                            "Run Analysis",
                            id='run-button',
                            color='primary',
                            className='w-100'
                        )
                    ], md=4)
                ], align="end")
            ])
        ], className="mb-4"),

        # Loading wrapper for all results
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                # 2D Results Grids Section (2x2 layout)
                dbc.Card([
                    dbc.CardHeader(html.H5("Results Grid", className="mb-0")),
                    dbc.CardBody([
                        html.P(
                            "Click a cell to view distribution charts for that portfolio × simulation combination. Green intensity indicates better performance within each metric.",
                            className="text-muted small mb-3"
                        ),
                        # 2x2 grid of metric tables
                        dbc.Row([
                            dbc.Col([
                                html.H6("CAGR", className="text-center mb-2"),
                                html.Div(
                                    id='results-grid-cagr',
                                    children=[html.P("Run analysis to see results.", className="text-muted text-center")]
                                )
                            ], md=6, className="mb-3"),
                            dbc.Col([
                                html.H6("Sharpe Ratio", className="text-center mb-2"),
                                html.Div(
                                    id='results-grid-sharpe',
                                    children=[html.P("Run analysis to see results.", className="text-muted text-center")]
                                )
                            ], md=6, className="mb-3"),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H6("Max Drawdown", className="text-center mb-2"),
                                html.Div(
                                    id='results-grid-drawdown',
                                    children=[html.P("Run analysis to see results.", className="text-muted text-center")]
                                )
                            ], md=6, className="mb-3"),
                            dbc.Col([
                                html.H6("Volatility", className="text-center mb-2"),
                                html.Div(
                                    id='results-grid-volatility',
                                    children=[html.P("Run analysis to see results.", className="text-muted text-center")]
                                )
                            ], md=6, className="mb-3"),
                        ])
                    ])
                ], className="mb-4"),

                # Distribution Charts (2x2 grid)
                dbc.Card([
                    dbc.CardHeader(html.H5("Distribution Analysis", className="mb-0")),
                    dbc.CardBody([
                        html.P(
                            "Orange dashed line shows historical result. Histogram shows Monte Carlo distribution.",
                            className="text-muted small mb-3"
                        ),
                        dcc.Graph(id='distributions-grid')
                    ])
                ])
            ]
        ),

    ], fluid=True, className="py-4")


def _create_available_portfolios_list(active_ids: list) -> list:
    """Create the list of available portfolios with add buttons.

    Args:
        active_ids: List of currently active portfolio IDs

    Returns:
        List of Dash components
    """
    items = []
    for portfolio in registry.list_all():
        is_active = portfolio.id in active_ids
        items.append(
            dbc.ListGroupItem([
                dbc.Row([
                    dbc.Col([
                        html.Strong(portfolio.display_name),
                        html.Br(),
                        html.Small(portfolio.description, className="text-muted")
                    ], width=9),
                    dbc.Col([
                        dbc.Button(
                            "Added" if is_active else "Add",
                            id={'type': 'add-portfolio-btn', 'index': portfolio.id},
                            color='secondary' if is_active else 'success',
                            size='sm',
                            disabled=is_active,
                            className='w-100'
                        )
                    ], width=3, className="d-flex align-items-center")
                ], align="center")
            ])
        )
    return [dbc.ListGroup(items)] if items else [html.P("No portfolios available.", className="text-muted")]


def create_active_portfolios_list(active_ids: list) -> list:
    """Create the list of active portfolios with remove buttons.

    Args:
        active_ids: List of currently active portfolio IDs

    Returns:
        List of Dash components
    """
    if not active_ids:
        return [html.P("No portfolios added yet.", className="text-muted")]

    items = []
    for portfolio_id in active_ids:
        try:
            portfolio = registry.get(portfolio_id)
            items.append(
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col([
                            html.Strong(portfolio.display_name),
                            html.Br(),
                            html.Small(portfolio.description, className="text-muted")
                        ], width=9),
                        dbc.Col([
                            dbc.Button(
                                "Remove",
                                id={'type': 'remove-portfolio-btn', 'index': portfolio_id},
                                color='danger',
                                size='sm',
                                outline=True,
                                className='w-100'
                            )
                        ], width=3, className="d-flex align-items-center")
                    ], align="center")
                ])
            )
        except KeyError:
            continue

    return [dbc.ListGroup(items)] if items else [html.P("No portfolios added yet.", className="text-muted")]


def _format_rf_schedule(rf_schedule) -> str:
    """Format RF schedule for display."""
    if rf_schedule is None:
        return "None"
    schedule_type = rf_schedule.schedule_type
    start = f"{rf_schedule.start_rate * 100:.1f}%"
    end = f"{rf_schedule.end_rate * 100:.1f}%"
    if schedule_type == 'constant':
        return f"Constant {start}"
    elif schedule_type == 'increasing':
        return f"{start} → {end}"
    elif schedule_type == 'decreasing':
        return f"{start} → {end}"
    elif schedule_type in ('v_shape', 'inverse_v'):
        mid = f"{rf_schedule.midpoint_rate * 100:.1f}%" if rf_schedule.midpoint_rate else "N/A"
        return f"{start} → {mid} → {end}"
    return schedule_type


def _create_simulation_params_display(simulation) -> html.Div:
    """Create the parameter details display for a simulation."""
    return html.Div([
        html.Hr(className="my-2"),
        html.Div([
            html.Div([
                html.Small("Simulations: ", className="text-muted"),
                html.Small(f"{simulation.num_simulations}", className="fw-bold")
            ], className="d-flex justify-content-between"),
            html.Div([
                html.Small("Years: ", className="text-muted"),
                html.Small(f"{simulation.num_years}", className="fw-bold")
            ], className="d-flex justify-content-between"),
            html.Div([
                html.Small("GARCH: ", className="text-muted"),
                html.Small("Yes" if simulation.use_garch else "No", className="fw-bold")
            ], className="d-flex justify-content-between"),
            html.Div([
                html.Small("ERP: ", className="text-muted"),
                html.Small("Yes" if simulation.use_erp else "No", className="fw-bold")
            ], className="d-flex justify-content-between"),
            html.Div([
                html.Small("RF Schedule: ", className="text-muted"),
                html.Small(_format_rf_schedule(simulation.rf_schedule), className="fw-bold")
            ], className="d-flex justify-content-between"),
        ], className="small")
    ], className="mt-2")


def _create_available_simulations_list(active_ids: list) -> list:
    """Create the list of available simulations with add buttons and expandable details.

    Args:
        active_ids: List of currently active simulation IDs

    Returns:
        List of Dash components
    """
    items = []
    for simulation in simulation_registry.list_all():
        is_active = simulation.id in active_ids
        collapse_id = f"collapse-avail-{simulation.id}"
        items.append(
            dbc.ListGroupItem([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Strong(simulation.display_name, className="me-2"),
                            html.A(
                                html.Small("▼", className="text-muted"),
                                id={'type': 'toggle-avail-sim', 'index': simulation.id},
                                href="#",
                                style={"textDecoration": "none", "cursor": "pointer"}
                            )
                        ]),
                        html.Small(simulation.description, className="text-muted d-block")
                    ], width=9),
                    dbc.Col([
                        dbc.Button(
                            "Added" if is_active else "Add",
                            id={'type': 'add-simulation-btn', 'index': simulation.id},
                            color='secondary' if is_active else 'success',
                            size='sm',
                            disabled=is_active,
                            className='w-100'
                        )
                    ], width=3, className="d-flex align-items-center")
                ], align="center"),
                dbc.Collapse(
                    _create_simulation_params_display(simulation),
                    id={'type': 'collapse-avail-sim', 'index': simulation.id},
                    is_open=False
                )
            ])
        )
    return [dbc.ListGroup(items)] if items else [html.P("No simulations available.", className="text-muted")]


def create_active_simulations_list(active_ids: list) -> list:
    """Create the list of active simulations with remove buttons and expandable details.

    Args:
        active_ids: List of currently active simulation IDs

    Returns:
        List of Dash components
    """
    if not active_ids:
        return [html.P("No simulations added yet.", className="text-muted")]

    items = []
    for simulation_id in active_ids:
        try:
            simulation = simulation_registry.get(simulation_id)
            items.append(
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Strong(simulation.display_name, className="me-2"),
                                html.A(
                                    html.Small("▼", className="text-muted"),
                                    id={'type': 'toggle-active-sim', 'index': simulation_id},
                                    href="#",
                                    style={"textDecoration": "none", "cursor": "pointer"}
                                )
                            ]),
                            html.Small(simulation.description, className="text-muted d-block")
                        ], width=9),
                        dbc.Col([
                            dbc.Button(
                                "Remove",
                                id={'type': 'remove-simulation-btn', 'index': simulation_id},
                                color='danger',
                                size='sm',
                                outline=True,
                                className='w-100'
                            )
                        ], width=3, className="d-flex align-items-center")
                    ], align="center"),
                    dbc.Collapse(
                        _create_simulation_params_display(simulation),
                        id={'type': 'collapse-active-sim', 'index': simulation_id},
                        is_open=False
                    )
                ])
            )
        except KeyError:
            continue

    return [dbc.ListGroup(items)] if items else [html.P("No simulations added yet.", className="text-muted")]
