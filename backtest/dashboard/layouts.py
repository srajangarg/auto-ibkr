"""Dashboard layout definitions."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import DEFAULT_INITIAL_AMT, DEFAULT_MONTHLY_CF
from dash import html, dcc
import dash_bootstrap_components as dbc
from .portfolios import registry
from .simulations import simulation_registry


def create_layout():
    """Create the main dashboard layout."""
    return dbc.Container([
        # Stores
        dcc.Store(id='active-portfolios-store', data=[]),
        dcc.Store(id='active-simulations-store', data=[]),
        dcc.Store(id='all-results-store', data={}),
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
                    dbc.Button("Clear Cache", id='clear-cache-btn', color='secondary', size='sm', outline=True, className="me-3"),
                    dbc.Label("Dark Mode", className="me-2", style={"fontSize": "0.9rem"}),
                    dbc.Switch(id='dark-mode-switch', value=True, className="d-inline-block")
                ], className="d-flex align-items-center justify-content-end mt-4")
            ], md=2)
        ]),

        # Portfolio Manager and Simulation Manager Side by Side
        dbc.Row([
            dbc.Col([
                _create_manager_card(
                    title="Portfolio Manager",
                    available_list_id='available-portfolios-list',
                    active_list_id='active-portfolios-list',
                    initial_available=_create_available_portfolios_list([]),
                )
            ], md=6),
            dbc.Col([
                _create_manager_card(
                    title="MC Simulation Manager",
                    available_list_id='available-simulations-list',
                    active_list_id='active-simulations-list',
                    initial_available=_create_available_simulations_list([]),
                )
            ], md=6)
        ], className="mb-4"),

        # Controls Row
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Initial Investment ($)", className="fw-bold"),
                        dbc.Input(id='initial-amt-input', type='number', value=DEFAULT_INITIAL_AMT,
                                  min=1000, step=1000, className="mb-2")
                    ], md=4),
                    dbc.Col([
                        html.Label("Monthly Contribution ($)", className="fw-bold"),
                        dbc.Input(id='monthly-cf-input', type='number', value=DEFAULT_MONTHLY_CF,
                                  min=0, step=100, className="mb-2")
                    ], md=4),
                    dbc.Col([
                        html.Label("\u00A0", className="fw-bold"),
                        dbc.Button("Run Analysis", id='run-button', color='primary', className='w-100')
                    ], md=4)
                ], align="end")
            ])
        ], className="mb-4"),

        # Loading wrapper for all results
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                # 2D Results Grids Section
                dbc.Card([
                    dbc.CardHeader(html.H5("Results Grid", className="mb-0")),
                    dbc.CardBody([
                        html.P(
                            "Click a cell to view distribution charts for that portfolio x simulation combination. "
                            "Green intensity indicates better performance within each metric.",
                            className="text-muted small mb-3"
                        ),
                        dbc.Row([
                            dbc.Col([
                                html.H6("CAGR", className="text-center mb-2"),
                                html.Div(id='results-grid-cagr', children=_empty_grid_message(),
                                         style={'overflow': 'hidden'})
                            ], md=6, className="mb-3"),
                            dbc.Col([
                                html.H6("Sharpe Ratio", className="text-center mb-2"),
                                html.Div(id='results-grid-sharpe', children=_empty_grid_message(),
                                         style={'overflow': 'hidden'})
                            ], md=6, className="mb-3"),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H6("Max Drawdown", className="text-center mb-2"),
                                html.Div(id='results-grid-drawdown', children=_empty_grid_message(),
                                         style={'overflow': 'hidden'})
                            ], md=6, className="mb-3"),
                            dbc.Col([
                                html.H6("Volatility", className="text-center mb-2"),
                                html.Div(id='results-grid-volatility', children=_empty_grid_message(),
                                         style={'overflow': 'hidden'})
                            ], md=6, className="mb-3"),
                        ])
                    ])
                ], className="mb-4"),

                # Distribution Charts
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


def _create_manager_card(title: str, available_list_id: str, active_list_id: str,
                          initial_available: list) -> dbc.Card:
    """Create a manager card with available and active lists."""
    return dbc.Card([
        dbc.CardHeader(html.H5(title, className="mb-0")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Available", className="fw-bold mb-2"),
                    html.Div(id=available_list_id, children=initial_available)
                ], md=6),
                dbc.Col([
                    html.Label("Active", className="fw-bold mb-2"),
                    html.Div(id=active_list_id, children=[
                        html.P("No items added yet.", className="text-muted")
                    ])
                ], md=6)
            ])
        ])
    ], className="h-100")


def _empty_grid_message() -> list:
    """Return empty grid placeholder message."""
    return [html.P("Run analysis to see results.", className="text-muted text-center")]


def _create_item_list_group(items: list, active_ids: list, item_type: str,
                             add_btn_type: str, remove_btn_type: str,
                             show_details: bool = False, is_active_list: bool = False) -> list:
    """Create a list group for items (portfolios or simulations).

    Args:
        items: List of items to display
        active_ids: List of currently active item IDs
        item_type: Type identifier for collapse IDs (e.g., 'sim', 'portfolio')
        add_btn_type: Button type for add buttons
        remove_btn_type: Button type for remove buttons
        show_details: Whether to show expandable details
        is_active_list: Whether this is the active list (vs available)

    Returns:
        List of Dash components
    """
    if not items:
        empty_msg = "No items added yet." if is_active_list else "No items available."
        return [html.P(empty_msg, className="text-muted")]

    list_items = []
    for item in items:
        is_active = item.id in active_ids

        # Build button
        if is_active_list:
            button = dbc.Button(
                "Remove",
                id={'type': remove_btn_type, 'index': item.id},
                color='danger', size='sm', outline=True, className='w-100'
            )
        else:
            button = dbc.Button(
                "Added" if is_active else "Add",
                id={'type': add_btn_type, 'index': item.id},
                color='secondary' if is_active else 'success',
                size='sm', disabled=is_active, className='w-100'
            )

        # Build name section
        if show_details:
            toggle_type = 'toggle-active-sim' if is_active_list else 'toggle-avail-sim'
            name_content = html.Div([
                html.Strong(item.display_name, className="me-2"),
                html.A(
                    html.Small("▼", className="text-muted"),
                    id={'type': toggle_type, 'index': item.id},
                    href="#", style={"textDecoration": "none", "cursor": "pointer"}
                )
            ])
        else:
            name_content = html.Strong(item.display_name)

        # Build list item content
        content = dbc.Row([
            dbc.Col([
                name_content,
                html.Br() if not show_details else None,
                html.Small(item.description, className="text-muted d-block" if show_details else "text-muted")
            ], width=9),
            dbc.Col([button], width=3, className="d-flex align-items-center")
        ], align="center")

        # Add collapse for details if needed
        if show_details:
            collapse_type = 'collapse-active-sim' if is_active_list else 'collapse-avail-sim'
            list_item = dbc.ListGroupItem([
                content,
                dbc.Collapse(
                    _create_simulation_params_display(item),
                    id={'type': collapse_type, 'index': item.id},
                    is_open=False
                )
            ])
        else:
            list_item = dbc.ListGroupItem(content)

        list_items.append(list_item)

    return [dbc.ListGroup(list_items)]


def _create_available_portfolios_list(active_ids: list) -> list:
    """Create the list of available portfolios with add buttons."""
    return _create_item_list_group(
        items=registry.list_all(),
        active_ids=active_ids,
        item_type='portfolio',
        add_btn_type='add-portfolio-btn',
        remove_btn_type='remove-portfolio-btn',
        show_details=False,
        is_active_list=False
    )


def create_active_portfolios_list(active_ids: list) -> list:
    """Create the list of active portfolios with remove buttons."""
    if not active_ids:
        return [html.P("No portfolios added yet.", className="text-muted")]

    items = []
    for pid in active_ids:
        try:
            items.append(registry.get(pid))
        except KeyError:
            continue

    return _create_item_list_group(
        items=items,
        active_ids=active_ids,
        item_type='portfolio',
        add_btn_type='add-portfolio-btn',
        remove_btn_type='remove-portfolio-btn',
        show_details=False,
        is_active_list=True
    )


def _create_available_simulations_list(active_ids: list) -> list:
    """Create the list of available simulations with add buttons and expandable details."""
    return _create_item_list_group(
        items=simulation_registry.list_all(),
        active_ids=active_ids,
        item_type='sim',
        add_btn_type='add-simulation-btn',
        remove_btn_type='remove-simulation-btn',
        show_details=True,
        is_active_list=False
    )


def create_active_simulations_list(active_ids: list) -> list:
    """Create the list of active simulations with remove buttons and expandable details."""
    if not active_ids:
        return [html.P("No simulations added yet.", className="text-muted")]

    items = []
    for sid in active_ids:
        try:
            items.append(simulation_registry.get(sid))
        except KeyError:
            continue

    return _create_item_list_group(
        items=items,
        active_ids=active_ids,
        item_type='sim',
        add_btn_type='add-simulation-btn',
        remove_btn_type='remove-simulation-btn',
        show_details=True,
        is_active_list=True
    )


def _format_rf_schedule(rf_schedule) -> str:
    """Format RF schedule for display."""
    if rf_schedule is None:
        return "None"

    schedule_type = rf_schedule.schedule_type
    start = f"{rf_schedule.start_rate * 100:.1f}%"
    end = f"{rf_schedule.end_rate * 100:.1f}%"

    if schedule_type == 'constant':
        return f"Constant {start}"
    elif schedule_type in ('increasing', 'decreasing'):
        return f"{start} -> {end}"
    elif schedule_type in ('v_shape', 'inverse_v'):
        mid = f"{rf_schedule.midpoint_rate * 100:.1f}%" if rf_schedule.midpoint_rate else "N/A"
        return f"{start} -> {mid} -> {end}"
    return schedule_type


def _create_simulation_params_display(simulation) -> html.Div:
    """Create the parameter details display for a simulation."""
    params = [
        ("Simulations", str(simulation.num_simulations)),
        ("Years", str(simulation.num_years)),
        ("GARCH", "Yes" if simulation.use_garch else "No"),
        ("ERP", "Yes" if simulation.use_erp else "No"),
        ("RF Schedule", _format_rf_schedule(simulation.rf_schedule)),
    ]

    rows = [
        html.Div([
            html.Small(f"{label}: ", className="text-muted"),
            html.Small(value, className="fw-bold")
        ], className="d-flex justify-content-between")
        for label, value in params
    ]

    return html.Div([
        html.Hr(className="my-2"),
        html.Div(rows, className="small")
    ], className="mt-2")
