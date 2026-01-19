"""Dash callbacks for dashboard interactivity."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (
    DEFAULT_INITIAL_AMT,
    DEFAULT_MONTHLY_CF,
    DEFAULT_MC_SIMULATIONS,
)
from dash import Input, Output, State, ALL, ctx, no_update
import dash_bootstrap_components as dbc
from .services.backtest_service import run_portfolio_analysis
from .components.charts import (
    create_metrics_grid,
    create_multi_portfolio_table_data,
    get_datatable_style,
    create_empty_figure,
)
from .layouts import _create_available_portfolios_list, create_active_portfolios_list
from .portfolios import registry

# Theme URLs
THEME_LIGHT = dbc.themes.BOOTSTRAP
THEME_DARK = dbc.themes.DARKLY


def register_callbacks(app):
    """Register all callbacks with the Dash app.

    Args:
        app: Dash application instance
    """

    # Clientside callback for toggling body class (for CSS theming)
    app.clientside_callback(
        """
        function(darkMode) {
            if (darkMode === false) {
                document.body.classList.add('light-mode');
                document.body.classList.remove('dark-mode');
            } else {
                document.body.classList.remove('light-mode');
                document.body.classList.add('dark-mode');
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('dark-mode-store', 'data', allow_duplicate=True),
        Input('dark-mode-switch', 'value'),
        prevent_initial_call='initial_duplicate'
    )

    # Dark mode callback - switch controls store and stylesheet
    @app.callback(
        [
            Output('dark-mode-store', 'data'),
            Output('theme-stylesheet', 'href'),
        ],
        Input('dark-mode-switch', 'value'),
    )
    def update_dark_mode(dark_mode):
        """Update dark mode store and stylesheet based on switch value."""
        if dark_mode is None:
            dark_mode = True  # Default to dark mode
        theme_url = THEME_DARK if dark_mode else THEME_LIGHT
        return dark_mode, theme_url

    # Update DataTable styling when dark mode changes
    @app.callback(
        [
            Output('summary-table', 'style_header'),
            Output('summary-table', 'style_data'),
            Output('summary-table', 'style_data_conditional'),
        ],
        Input('dark-mode-store', 'data'),
    )
    def update_table_style(dark_mode):
        """Update DataTable styling based on dark mode."""
        if dark_mode is None:
            dark_mode = True
        styles = get_datatable_style(dark_mode)
        return styles['style_header'], styles['style_data'], styles['style_data_conditional']

    @app.callback(
        Output('active-portfolios-store', 'data'),
        [
            Input({'type': 'add-portfolio-btn', 'index': ALL}, 'n_clicks'),
            Input({'type': 'remove-portfolio-btn', 'index': ALL}, 'n_clicks'),
        ],
        State('active-portfolios-store', 'data'),
        prevent_initial_call=True
    )
    def update_active_portfolios(add_clicks, remove_clicks, current_active):
        """Update the active portfolios list when add/remove buttons are clicked."""
        if not ctx.triggered_id:
            return no_update

        triggered = ctx.triggered_id
        portfolio_id = triggered['index']
        action = triggered['type']

        if current_active is None:
            current_active = []

        if action == 'add-portfolio-btn' and portfolio_id not in current_active:
            current_active = current_active + [portfolio_id]
        elif action == 'remove-portfolio-btn' and portfolio_id in current_active:
            current_active = [p for p in current_active if p != portfolio_id]

        return current_active

    @app.callback(
        [
            Output('available-portfolios-list', 'children'),
            Output('active-portfolios-list', 'children'),
        ],
        Input('active-portfolios-store', 'data'),
    )
    def update_portfolio_lists(active_ids):
        """Update both portfolio lists when active portfolios change."""
        if active_ids is None:
            active_ids = []

        available_list = _create_available_portfolios_list(active_ids)
        active_list = create_active_portfolios_list(active_ids)

        return available_list, active_list

    @app.callback(
        [
            Output('all-results-store', 'data'),
            Output('selected-portfolio-store', 'data'),
            Output('summary-table', 'data'),
            Output('summary-table', 'columns'),
            Output('summary-table', 'selected_rows'),
            Output('distributions-grid', 'figure'),
        ],
        [Input('run-button', 'n_clicks')],
        [
            State('active-portfolios-store', 'data'),
            State('initial-amt-input', 'value'),
            State('monthly-cf-input', 'value'),
            State('mc-simulations-input', 'value'),
            State('dark-mode-store', 'data'),
        ]
    )
    def run_all_analysis(n_clicks, active_portfolios, initial_amt, monthly_cf, num_simulations, dark_mode):
        """Run analysis on ALL active portfolios when Run is clicked.

        Args:
            n_clicks: Number of button clicks
            active_portfolios: List of active portfolio IDs
            initial_amt: Initial investment amount
            monthly_cf: Monthly contribution
            num_simulations: Number of MC simulations
            dark_mode: Dark mode state

        Returns:
            Tuple of (all_results_store, selected_portfolio, table_data, table_columns, selected_rows, distributions_grid)
        """
        import traceback
        # Default to dark mode if not set
        if dark_mode is None:
            dark_mode = True
        print(f"[Callback] n_clicks={n_clicks}, active_portfolios={active_portfolios}, dark_mode={dark_mode}")

        # Handle initial load - return empty state
        if n_clicks is None:
            print("[Callback] Initial load - returning empty state")
            empty = create_empty_figure("Add portfolios and click 'Run Analysis' to start", dark_mode=dark_mode)
            return {}, None, [], [], [], empty

        # Handle no portfolios added
        if not active_portfolios:
            print("[Callback] No portfolios added")
            empty = create_empty_figure("Please add at least one portfolio first", dark_mode=dark_mode)
            return {}, None, [], [], [], empty

        try:
            # Run analysis for ALL active portfolios
            print(f"[Callback] Running analysis for {len(active_portfolios)} portfolios...")
            all_results = {}
            portfolio_names = {}

            for portfolio_id in active_portfolios:
                print(f"[Callback] Analyzing {portfolio_id}...")
                results = run_portfolio_analysis(
                    portfolio_id=portfolio_id,
                    initial_amt=initial_amt or DEFAULT_INITIAL_AMT,
                    monthly_cf=monthly_cf or DEFAULT_MONTHLY_CF,
                    num_simulations=num_simulations or DEFAULT_MC_SIMULATIONS
                )
                all_results[portfolio_id] = results
                portfolio_names[portfolio_id] = registry.get(portfolio_id).display_name

            print(f"[Callback] All analyses complete.")

            # Select the first portfolio by default
            selected_portfolio = active_portfolios[0]

            # Create the DataTable data and columns
            table_data, table_columns, portfolio_ids = create_multi_portfolio_table_data(
                all_results,
                portfolio_names
            )

            # Create distribution grid for selected portfolio
            grid_fig = create_metrics_grid(all_results[selected_portfolio], dark_mode=dark_mode)

            # Serialize results for storage (convert to dict format)
            serialized_results = {}
            for pid, res in all_results.items():
                serialized_results[pid] = {
                    'summary': res.summary(),
                    'historical': {
                        'cagr': res.historical.cagr,
                        'max_drawdown': res.historical.max_drawdown,
                        'sharpe_ratio': res.historical.sharpe_ratio,
                        'annual_volatility': res.historical.annual_volatility,
                        'total_value': res.historical.total_value,
                        'total_contributions': res.historical.total_contributions,
                    } if res.historical else None,
                    'mc_distributions': {
                        'cagr': [r.cagr for r in res.monte_carlo],
                        'max_drawdown': [r.max_drawdown for r in res.monte_carlo],
                        'sharpe_ratio': [r.sharpe_ratio for r in res.monte_carlo],
                        'annual_volatility': [r.annual_volatility for r in res.monte_carlo],
                        'total_value': [r.total_value for r in res.monte_carlo],
                        'total_contributions': [r.total_contributions for r in res.monte_carlo],
                    } if res.monte_carlo else None,
                    'display_name': portfolio_names[pid]
                }

            print("[Callback] Analysis complete, returning results")
            return serialized_results, selected_portfolio, table_data, table_columns, [0], grid_fig

        except Exception as e:
            print(f"[Callback] ERROR: {e}")
            traceback.print_exc()
            error_fig = create_empty_figure(f"Error: {str(e)}", dark_mode=dark_mode)
            return {}, None, [], [], [], error_fig

    @app.callback(
        [
            Output('selected-portfolio-store', 'data', allow_duplicate=True),
            Output('distributions-grid', 'figure', allow_duplicate=True),
        ],
        Input('summary-table', 'selected_rows'),
        [
            State('summary-table', 'data'),
            State('all-results-store', 'data'),
            State('dark-mode-store', 'data'),
        ],
        prevent_initial_call=True
    )
    def handle_row_selection(selected_rows, table_data, all_results, dark_mode):
        """Handle row selection in the DataTable to update distributions.

        Args:
            selected_rows: List of selected row indices
            table_data: Current table data
            all_results: Serialized results for all portfolios
            dark_mode: Dark mode state

        Returns:
            Tuple of (selected_portfolio, distributions_grid)
        """
        if not selected_rows or not table_data or not all_results:
            return no_update, no_update

        # Default to dark mode if not set
        if dark_mode is None:
            dark_mode = True

        try:
            row_idx = selected_rows[0]
            if row_idx >= len(table_data):
                return no_update, no_update

            # Get the portfolio_id from the selected row
            selected_row = table_data[row_idx]
            new_selected = selected_row.get('portfolio_id')

            if not new_selected or new_selected not in all_results:
                return no_update, no_update

            print(f"[Callback] Row selected: {row_idx}, portfolio: {new_selected}")

            # Reconstruct SimulationResults for the selected portfolio
            from monte_carlo import SimulationResults, BacktestResult

            data = all_results[new_selected]
            historical = BacktestResult(**data['historical']) if data['historical'] else None
            mc_results = []
            if data['mc_distributions']:
                num_sims = len(data['mc_distributions']['cagr'])
                for i in range(num_sims):
                    mc_results.append(BacktestResult(
                        cagr=data['mc_distributions']['cagr'][i],
                        max_drawdown=data['mc_distributions']['max_drawdown'][i],
                        sharpe_ratio=data['mc_distributions']['sharpe_ratio'][i],
                        annual_volatility=data['mc_distributions']['annual_volatility'][i],
                        total_value=data['mc_distributions']['total_value'][i],
                        total_contributions=data['mc_distributions']['total_contributions'][i],
                    ))
            results_obj = SimulationResults(historical=historical, monte_carlo=mc_results)

            # Create distribution grid for the selected portfolio
            grid_fig = create_metrics_grid(results_obj, dark_mode=dark_mode)

            return new_selected, grid_fig

        except Exception as e:
            print(f"[Callback] Error handling row selection: {e}")
            import traceback
            traceback.print_exc()
            return no_update, no_update
