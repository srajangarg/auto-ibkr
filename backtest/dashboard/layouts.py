"""Dashboard layout definitions."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (
    DEFAULT_INITIAL_AMT,
    DEFAULT_MONTHLY_CF,
    DEFAULT_MC_SIMULATIONS,
)
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from .portfolios import registry


def create_layout():
    """Create the main dashboard layout.

    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Store for active portfolios (persists client-side)
        dcc.Store(id='active-portfolios-store', data=[]),
        # Store for all portfolio results (after running analysis)
        dcc.Store(id='all-results-store', data={}),
        # Store for selected portfolio (for viewing distributions)
        dcc.Store(id='selected-portfolio-store', data=None),

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

        # Portfolio Manager Section
        dbc.Card([
            dbc.CardHeader(html.H5("Portfolio Manager", className="mb-0")),
            dbc.CardBody([
                dbc.Row([
                    # Available Portfolios (left side)
                    dbc.Col([
                        html.Label("Available Portfolios", className="fw-bold mb-2"),
                        html.Div(
                            id='available-portfolios-list',
                            children=_create_available_portfolios_list([])
                        )
                    ], md=6),

                    # Active Portfolios (right side)
                    dbc.Col([
                        html.Label("Active Portfolios", className="fw-bold mb-2"),
                        html.Div(
                            id='active-portfolios-list',
                            children=[
                                html.P("No portfolios added yet.", className="text-muted")
                            ]
                        )
                    ], md=6)
                ])
            ])
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
                    ], md=3),

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
                    ], md=3),

                    dbc.Col([
                        html.Label("MC Simulations", className="fw-bold"),
                        dbc.Input(
                            id='mc-simulations-input',
                            type='number',
                            value=DEFAULT_MC_SIMULATIONS,
                            min=100,
                            max=2000,
                            step=100,
                            className="mb-2"
                        )
                    ], md=3),

                    dbc.Col([
                        html.Label("\u00A0", className="fw-bold"),  # Non-breaking space for alignment
                        dbc.Button(
                            "Run Analysis",
                            id='run-button',
                            color='primary',
                            className='w-100'
                        )
                    ], md=3)
                ], align="end")
            ])
        ], className="mb-4"),

        # Loading wrapper for all results
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                # Summary Stats Section
                dbc.Card([
                    dbc.CardHeader(html.H5("Summary Statistics", className="mb-0")),
                    dbc.CardBody([
                        html.P(
                            "Click a row to view distribution charts for that portfolio.",
                            className="text-muted small mb-3"
                        ),
                        dash_table.DataTable(
                            id='summary-table',
                            columns=[],
                            data=[],
                            row_selectable='single',
                            selected_rows=[0],
                            merge_duplicate_headers=True,  # Enables hierarchical column headers
                            # Initial styling (will be updated by callback based on dark mode)
                            style_header={
                                'backgroundColor': '#1e293b',
                                'color': '#f1f5f9',
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                                'border': '1px solid #334155',
                                'fontFamily': 'Inter, -apple-system, sans-serif',
                            },
                            style_cell={
                                'textAlign': 'center',
                                'padding': '12px 10px',
                                'fontSize': '13px',
                                'border': '1px solid #334155',
                                'fontFamily': 'Inter, -apple-system, sans-serif',
                            },
                            style_data={
                                'backgroundColor': '#0f172a',
                                'color': '#e2e8f0',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'state': 'selected'},
                                    'backgroundColor': '#164e63',
                                    'border': '1px solid #22d3ee',
                                },
                                {
                                    'if': {'state': 'active'},
                                    'backgroundColor': '#164e63',
                                    'border': '1px solid #22d3ee',
                                },
                            ],
                            style_table={
                                'overflowX': 'auto',
                                'borderRadius': '8px',
                            },
                        )
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
