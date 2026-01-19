"""Dash callbacks for dashboard interactivity."""
from dash import Input, Output, State, no_update, ctx
from .services.backtest_service import run_portfolio_analysis
from .components.charts import (
    create_metrics_grid,
    create_summary_table,
    create_distribution_chart,
    create_empty_figure,
)


def register_callbacks(app):
    """Register all callbacks with the Dash app.

    Args:
        app: Dash application instance
    """

    @app.callback(
        [
            Output('summary-table', 'figure'),
            Output('distributions-grid', 'figure'),
            Output('detail-distribution', 'figure'),
            Output('results-store', 'data')
        ],
        [Input('run-button', 'n_clicks')],
        [
            State('portfolio-dropdown', 'value'),
            State('initial-amt-input', 'value'),
            State('monthly-cf-input', 'value'),
            State('mc-simulations-input', 'value'),
            State('metric-dropdown', 'value')
        ]
    )
    def update_all_charts(n_clicks, portfolio_id, initial_amt, monthly_cf, num_simulations, metric):
        """Update all dashboard charts when Run is clicked.

        Args:
            n_clicks: Number of button clicks
            portfolio_id: Selected portfolio ID
            initial_amt: Initial investment amount
            monthly_cf: Monthly contribution
            num_simulations: Number of MC simulations
            metric: Selected metric for detail view

        Returns:
            Tuple of (summary_table, distributions_grid, detail_chart, store_data)
        """
        import traceback
        print(f"[Callback] n_clicks={n_clicks}, portfolio={portfolio_id}, initial={initial_amt}, monthly={monthly_cf}, sims={num_simulations}")

        # Handle initial load - return empty figures
        if n_clicks is None:
            print("[Callback] Initial load - returning empty figures")
            empty = create_empty_figure("Click 'Run Analysis' to start")
            return empty, empty, empty, None

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
            detail_fig = create_distribution_chart(results, metric or 'cagr')

            # Store portfolio_id for metric dropdown callback
            store_data = {'portfolio_id': portfolio_id}

            print("[Callback] Figures created successfully")
            return summary_fig, grid_fig, detail_fig, store_data

        except Exception as e:
            # Return error state
            print(f"[Callback] ERROR: {e}")
            traceback.print_exc()
            error_fig = create_empty_figure(f"Error: {str(e)}")
            return error_fig, error_fig, error_fig, None

    @app.callback(
        Output('detail-distribution', 'figure', allow_duplicate=True),
        Input('metric-dropdown', 'value'),
        [
            State('portfolio-dropdown', 'value'),
            State('initial-amt-input', 'value'),
            State('monthly-cf-input', 'value'),
            State('mc-simulations-input', 'value')
        ],
        prevent_initial_call=True
    )
    def update_detail_chart(metric, portfolio_id, initial_amt, monthly_cf, num_simulations):
        """Update detailed metric view when metric dropdown changes.

        Uses cached results from previous analysis run.

        Args:
            metric: Selected metric
            portfolio_id: Current portfolio ID
            initial_amt: Initial investment amount
            monthly_cf: Monthly contribution
            num_simulations: Number of MC simulations

        Returns:
            Plotly Figure for the detail distribution
        """
        if not metric:
            return no_update

        try:
            # Get cached results
            results = run_portfolio_analysis(
                portfolio_id=portfolio_id,
                initial_amt=initial_amt or 10000,
                monthly_cf=monthly_cf or 0,
                num_simulations=num_simulations or 500,
                use_cache=True
            )

            return create_distribution_chart(results, metric)

        except Exception as e:
            return create_empty_figure(f"Error: {str(e)}")
