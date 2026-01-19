"""Dashboard layout definitions."""
from dash import html, dcc
import dash_bootstrap_components as dbc
from .portfolios import registry


def create_layout():
    """Create the main dashboard layout.

    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Backtest Dashboard", className="text-center my-4"),
                html.P(
                    "Compare portfolio strategies with historical and Monte Carlo analysis",
                    className="text-center text-muted mb-4"
                )
            ])
        ]),

        # Controls Row
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Portfolio", className="fw-bold"),
                        dcc.Dropdown(
                            id='portfolio-dropdown',
                            options=registry.get_dropdown_options(),
                            value='qqq_100',
                            clearable=False,
                            className="mb-2"
                        )
                    ], md=3),

                    dbc.Col([
                        html.Label("Initial Investment ($)", className="fw-bold"),
                        dbc.Input(
                            id='initial-amt-input',
                            type='number',
                            value=10000,
                            min=1000,
                            step=1000,
                            className="mb-2"
                        )
                    ], md=2),

                    dbc.Col([
                        html.Label("Monthly Contribution ($)", className="fw-bold"),
                        dbc.Input(
                            id='monthly-cf-input',
                            type='number',
                            value=0,
                            min=0,
                            step=100,
                            className="mb-2"
                        )
                    ], md=2),

                    dbc.Col([
                        html.Label("MC Simulations", className="fw-bold"),
                        dbc.Input(
                            id='mc-simulations-input',
                            type='number',
                            value=500,
                            min=100,
                            max=2000,
                            step=100,
                            className="mb-2"
                        )
                    ], md=2),

                    dbc.Col([
                        html.Label("\u00A0", className="fw-bold"),  # Non-breaking space for alignment
                        dbc.Button(
                            "Run Analysis",
                            id='run-button',
                            color='primary',
                            className='w-100'
                        )
                    ], md=2)
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
                        dcc.Graph(id='summary-table', config={'displayModeBar': False})
                    ])
                ], className="mb-4"),

                # Distribution Charts (2x2 grid)
                dbc.Card([
                    dbc.CardHeader(html.H5("Distribution Analysis", className="mb-0")),
                    dbc.CardBody([
                        html.P(
                            "Red dashed line shows historical result. Histogram shows Monte Carlo distribution.",
                            className="text-muted small mb-3"
                        ),
                        dcc.Graph(id='distributions-grid')
                    ])
                ], className="mb-4"),

                # Detailed metric view
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col(html.H5("Detailed Metric View", className="mb-0"), md=6),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='metric-dropdown',
                                    options=[
                                        {'label': 'CAGR', 'value': 'cagr'},
                                        {'label': 'Max Drawdown', 'value': 'max_drawdown'},
                                        {'label': 'Sharpe Ratio', 'value': 'sharpe_ratio'},
                                        {'label': 'Annual Volatility', 'value': 'annual_volatility'},
                                        {'label': 'Total Value', 'value': 'total_value'}
                                    ],
                                    value='cagr',
                                    clearable=False,
                                    style={'minWidth': '200px'}
                                )
                            ], md=6, className="d-flex justify-content-end")
                        ], align="center")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='detail-distribution')
                    ])
                ])
            ]
        ),

        # Store for results data (allows sharing between callbacks)
        dcc.Store(id='results-store')

    ], fluid=True, className="py-4")
