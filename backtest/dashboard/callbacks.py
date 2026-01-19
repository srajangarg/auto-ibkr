"""Dash callbacks for dashboard interactivity."""
from dash import Input, Output, State, ALL, ctx, no_update
from .services.backtest_service import run_portfolio_analysis
from .components.charts import (
    create_metrics_grid,
    create_summary_table,
    create_empty_figure,
)
from .layouts import _create_available_portfolios_list, create_active_portfolios_list
from .portfolios import registry


def register_callbacks(app):
    """Register all callbacks with the Dash app.

    Args:
        app: Dash application instance
    """

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
            Output('portfolio-dropdown', 'options'),
            Output('portfolio-dropdown', 'value'),
        ],
        Input('active-portfolios-store', 'data'),
        State('portfolio-dropdown', 'value')
    )
    def update_portfolio_lists(active_ids, current_dropdown_value):
        """Update both portfolio lists and dropdown when active portfolios change."""
        if active_ids is None:
            active_ids = []

        available_list = _create_available_portfolios_list(active_ids)
        active_list = create_active_portfolios_list(active_ids)

        dropdown_options = [
            {'label': registry.get(pid).display_name, 'value': pid}
            for pid in active_ids
            if pid in registry.get_ids()
        ]

        if current_dropdown_value in active_ids:
            dropdown_value = current_dropdown_value
        elif active_ids:
            dropdown_value = active_ids[0]
        else:
            dropdown_value = None

        return available_list, active_list, dropdown_options, dropdown_value

    @app.callback(
        [
            Output('summary-table', 'figure'),
            Output('distributions-grid', 'figure'),
        ],
        [Input('run-button', 'n_clicks')],
        [
            State('portfolio-dropdown', 'value'),
            State('initial-amt-input', 'value'),
            State('monthly-cf-input', 'value'),
            State('mc-simulations-input', 'value'),
        ]
    )
    def update_all_charts(n_clicks, portfolio_id, initial_amt, monthly_cf, num_simulations):
        """Update all dashboard charts when Run is clicked.

        Args:
            n_clicks: Number of button clicks
            portfolio_id: Selected portfolio ID
            initial_amt: Initial investment amount
            monthly_cf: Monthly contribution
            num_simulations: Number of MC simulations

        Returns:
            Tuple of (summary_table, distributions_grid)
        """
        import traceback
        print(f"[Callback] n_clicks={n_clicks}, portfolio={portfolio_id}, initial={initial_amt}, monthly={monthly_cf}, sims={num_simulations}")

        # Handle initial load - return empty figures
        if n_clicks is None:
            print("[Callback] Initial load - returning empty figures")
            empty = create_empty_figure("Add portfolios and click 'Run Analysis' to start")
            return empty, empty

        # Handle no portfolio selected
        if not portfolio_id:
            print("[Callback] No portfolio selected")
            empty = create_empty_figure("Please add a portfolio first")
            return empty, empty

        try:
            # Run analysis
            print("[Callback] Starting analysis...")
            results = run_portfolio_analysis(
                portfolio_id=portfolio_id,
                initial_amt=initial_amt or 10000,
                monthly_cf=monthly_cf or 0,
                num_simulations=num_simulations or 500
            )
            print(f"[Callback] Analysis complete. MC results: {len(results.monte_carlo) if results.monte_carlo else 0}")

            # Create figures
            summary_fig = create_summary_table(results)
            grid_fig = create_metrics_grid(results)

            print("[Callback] Figures created successfully")
            return summary_fig, grid_fig

        except Exception as e:
            # Return error state
            print(f"[Callback] ERROR: {e}")
            traceback.print_exc()
            error_fig = create_empty_figure(f"Error: {str(e)}")
            return error_fig, error_fig
