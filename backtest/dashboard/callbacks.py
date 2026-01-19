"""Dash callbacks for dashboard interactivity."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (
    DEFAULT_INITIAL_AMT,
    DEFAULT_MONTHLY_CF,
)
from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_bootstrap_components as dbc
from .services.backtest_service import run_portfolio_analysis
from .components.charts import (
    create_metrics_grid,
    create_multi_metrics_grid,
    create_results_grid,
    create_empty_figure,
)
from .layouts import (
    _create_available_portfolios_list,
    create_active_portfolios_list,
    _create_available_simulations_list,
    create_active_simulations_list,
)
from .portfolios import registry
from .simulations import simulation_registry

# Theme URLs
THEME_LIGHT = dbc.themes.BOOTSTRAP
THEME_DARK = dbc.themes.DARKLY


def _reconstruct_simulation_results(data: dict):
    """Reconstruct SimulationResults from serialized dict format.

    Args:
        data: Dict with 'historical' and 'mc_distributions' keys

    Returns:
        SimulationResults object
    """
    from monte_carlo import SimulationResults, BacktestResult

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
    return SimulationResults(historical=historical, monte_carlo=mc_results)


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

    # Callback for add/remove simulation buttons
    @app.callback(
        Output('active-simulations-store', 'data'),
        [
            Input({'type': 'add-simulation-btn', 'index': ALL}, 'n_clicks'),
            Input({'type': 'remove-simulation-btn', 'index': ALL}, 'n_clicks'),
        ],
        State('active-simulations-store', 'data'),
        prevent_initial_call=True
    )
    def update_active_simulations(add_clicks, remove_clicks, current_active):
        """Update the active simulations list when add/remove buttons are clicked."""
        if not ctx.triggered_id:
            return no_update

        triggered = ctx.triggered_id
        simulation_id = triggered['index']
        action = triggered['type']

        if current_active is None:
            current_active = []

        if action == 'add-simulation-btn' and simulation_id not in current_active:
            current_active = current_active + [simulation_id]
        elif action == 'remove-simulation-btn' and simulation_id in current_active:
            current_active = [s for s in current_active if s != simulation_id]

        return current_active

    @app.callback(
        [
            Output('available-simulations-list', 'children'),
            Output('active-simulations-list', 'children'),
        ],
        Input('active-simulations-store', 'data'),
    )
    def update_simulation_lists(active_ids):
        """Update both simulation lists when active simulations change."""
        if active_ids is None:
            active_ids = []

        available_list = _create_available_simulations_list(active_ids)
        active_list = create_active_simulations_list(active_ids)

        return available_list, active_list

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
            Output('selected-cell-store', 'data'),
            Output('results-grid-cagr', 'children'),
            Output('results-grid-sharpe', 'children'),
            Output('results-grid-drawdown', 'children'),
            Output('results-grid-volatility', 'children'),
            Output('distributions-grid', 'figure'),
        ],
        [Input('run-button', 'n_clicks')],
        [
            State('active-portfolios-store', 'data'),
            State('active-simulations-store', 'data'),
            State('initial-amt-input', 'value'),
            State('monthly-cf-input', 'value'),
            State('dark-mode-store', 'data'),
        ]
    )
    def run_all_analysis(n_clicks, active_portfolios, active_simulations, initial_amt, monthly_cf, dark_mode):
        """Run analysis on cross-product of active portfolios × active simulations.

        Args:
            n_clicks: Number of button clicks
            active_portfolios: List of active portfolio IDs
            active_simulations: List of active simulation IDs
            initial_amt: Initial investment amount
            monthly_cf: Monthly contribution
            dark_mode: Dark mode state

        Returns:
            Tuple of (all_results_store, selected_cell, 4x results_grids, distributions_grid)
        """
        import traceback
        empty_grid = [html.P("Run analysis to see results.", className="text-muted text-center")]
        # Default to dark mode if not set
        if dark_mode is None:
            dark_mode = True
        print(f"[Callback] n_clicks={n_clicks}, active_portfolios={active_portfolios}, active_simulations={active_simulations}")

        # Handle initial load - return empty state
        if n_clicks is None:
            print("[Callback] Initial load - returning empty state")
            empty = create_empty_figure("Add portfolios/simulations and click 'Run Analysis' to start", dark_mode=dark_mode)
            return {}, None, empty_grid, empty_grid, empty_grid, empty_grid, empty

        # Handle no portfolios added
        if not active_portfolios:
            print("[Callback] No portfolios added")
            empty = create_empty_figure("Please add at least one portfolio first", dark_mode=dark_mode)
            msg = [html.P("Please add at least one portfolio.", className="text-muted text-center")]
            return {}, None, msg, msg, msg, msg, empty

        # Handle no simulations added
        if not active_simulations:
            print("[Callback] No simulations added")
            empty = create_empty_figure("Please add at least one simulation first", dark_mode=dark_mode)
            msg = [html.P("Please add at least one simulation.", className="text-muted text-center")]
            return {}, None, msg, msg, msg, msg, empty

        try:
            # Run analysis for cross-product of portfolios × simulations
            total_runs = len(active_portfolios) * len(active_simulations)
            print(f"[Callback] Running {total_runs} analyses ({len(active_portfolios)} portfolios × {len(active_simulations)} simulations)...")

            all_results = {}
            portfolio_names = {}
            simulation_names = {}

            for portfolio_id in active_portfolios:
                portfolio_names[portfolio_id] = registry.get(portfolio_id).display_name

            for simulation_id in active_simulations:
                simulation_names[simulation_id] = simulation_registry.get(simulation_id).display_name

            for portfolio_id in active_portfolios:
                for simulation_id in active_simulations:
                    key = f"{portfolio_id}|{simulation_id}"
                    print(f"[Callback] Analyzing {key}...")
                    results = run_portfolio_analysis(
                        portfolio_id=portfolio_id,
                        simulation_id=simulation_id,
                        initial_amt=initial_amt or DEFAULT_INITIAL_AMT,
                        monthly_cf=monthly_cf or DEFAULT_MONTHLY_CF,
                    )
                    all_results[key] = results

            print(f"[Callback] All {total_runs} analyses complete.")

            # Select the first cell by default (as a list for multi-select support)
            selected_cells = [{
                'portfolio_id': active_portfolios[0],
                'simulation_id': active_simulations[0]
            }]
            first_key = f"{active_portfolios[0]}|{active_simulations[0]}"

            # Create the 4 results grids (one per metric)
            grid_args = (all_results, active_portfolios, active_simulations,
                         portfolio_names, simulation_names, selected_cells, dark_mode)
            grid_cagr = create_results_grid(*grid_args, metric='cagr')
            grid_sharpe = create_results_grid(*grid_args, metric='sharpe_ratio')
            grid_drawdown = create_results_grid(*grid_args, metric='max_drawdown')
            grid_volatility = create_results_grid(*grid_args, metric='annual_volatility')

            # Create distribution grid for selected cell
            grid_fig = create_metrics_grid(all_results[first_key], dark_mode=dark_mode)

            # Serialize results for storage (convert to dict format)
            serialized_results = {}
            for key, res in all_results.items():
                serialized_results[key] = {
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
                }

            # Store metadata for reconstructing grid
            serialized_results['_meta'] = {
                'portfolio_names': portfolio_names,
                'simulation_names': simulation_names,
                'active_portfolios': active_portfolios,
                'active_simulations': active_simulations,
            }

            print("[Callback] Analysis complete, returning results")
            return serialized_results, selected_cells, [grid_cagr], [grid_sharpe], [grid_drawdown], [grid_volatility], grid_fig

        except Exception as e:
            print(f"[Callback] ERROR: {e}")
            traceback.print_exc()
            error_fig = create_empty_figure(f"Error: {str(e)}", dark_mode=dark_mode)
            err_msg = [html.P(f"Error: {str(e)}", className="text-danger")]
            return {}, None, err_msg, err_msg, err_msg, err_msg, error_fig

    @app.callback(
        [
            Output('selected-cell-store', 'data', allow_duplicate=True),
            Output('results-grid-cagr', 'children', allow_duplicate=True),
            Output('results-grid-sharpe', 'children', allow_duplicate=True),
            Output('results-grid-drawdown', 'children', allow_duplicate=True),
            Output('results-grid-volatility', 'children', allow_duplicate=True),
            Output('distributions-grid', 'figure', allow_duplicate=True),
        ],
        Input({'type': 'grid-cell-btn', 'portfolio': ALL, 'simulation': ALL}, 'n_clicks'),
        [
            State('all-results-store', 'data'),
            State('selected-cell-store', 'data'),
            State('dark-mode-store', 'data'),
        ],
        prevent_initial_call=True
    )
    def handle_cell_selection(n_clicks, all_results, current_selection, dark_mode):
        """Handle cell selection with multi-select toggle behavior.

        Selection rules:
        1. Clicking unselected cell in same column: add to selection (up to 4)
        2. Clicking selected cell: deselect it (toggle off)
        3. Clicking cell in different column: reset selection to just that cell
        4. Max 4 cells can be selected

        Args:
            n_clicks: List of n_clicks for all grid cell buttons
            all_results: Serialized results for all combinations
            current_selection: List of currently selected cells
            dark_mode: Dark mode state

        Returns:
            Tuple of (selected_cells, 4x results_grids, distributions_grid)
        """
        print(f"[Callback] handle_cell_selection triggered. n_clicks={n_clicks}, triggered_id={ctx.triggered_id}")

        # Check if callback was triggered by an actual click
        if not ctx.triggered_id:
            print("[Callback] No triggered_id")
            return no_update, no_update, no_update, no_update, no_update, no_update

        # Check if n_clicks indicates an actual click (buttons start with n_clicks=0)
        if n_clicks is None or not isinstance(n_clicks, list) or not any(c is not None and c > 0 for c in n_clicks):
            print(f"[Callback] No actual click detected. n_clicks={n_clicks}")
            return no_update, no_update, no_update, no_update, no_update, no_update

        if not all_results:
            print(f"[Callback] No results data. all_results type={type(all_results)}")
            return no_update, no_update, no_update, no_update, no_update, no_update

        # Default to dark mode if not set
        if dark_mode is None:
            dark_mode = True

        # Initialize current_selection as list if None or not a list
        if current_selection is None or not isinstance(current_selection, list):
            current_selection = []

        try:
            triggered = ctx.triggered_id
            clicked_portfolio = triggered['portfolio']
            clicked_simulation = triggered['simulation']
            key = f"{clicked_portfolio}|{clicked_simulation}"

            print(f"[Callback] Cell clicked: {clicked_portfolio} × {clicked_simulation}, key={key}")

            if key not in all_results:
                print(f"[Callback] Key {key} not in all_results. Keys: {list(all_results.keys())}")
                return no_update, no_update, no_update, no_update, no_update, no_update

            # Determine the current column (simulation_id) of existing selection
            current_column = None
            if current_selection:
                current_column = current_selection[0].get('simulation_id')

            # Check if clicked cell is already selected
            is_already_selected = any(
                cell.get('portfolio_id') == clicked_portfolio and
                cell.get('simulation_id') == clicked_simulation
                for cell in current_selection
            )

            # Determine new selection based on rules
            if is_already_selected:
                # Rule 2: Toggle off - remove from selection
                new_selection = [
                    cell for cell in current_selection
                    if not (cell['portfolio_id'] == clicked_portfolio and
                           cell['simulation_id'] == clicked_simulation)
                ]
                print(f"[Callback] Toggled off cell, new selection count: {len(new_selection)}")
            elif clicked_simulation == current_column:
                # Rule 1: Same column - add to selection (if under limit of 4)
                if len(current_selection) < 4:
                    new_selection = current_selection + [{
                        'portfolio_id': clicked_portfolio,
                        'simulation_id': clicked_simulation
                    }]
                    print(f"[Callback] Added to selection, new count: {len(new_selection)}")
                else:
                    # At limit, don't change
                    new_selection = current_selection
                    print(f"[Callback] At max selection limit (4), no change")
            else:
                # Rule 3: Different column - reset to just this cell
                new_selection = [{
                    'portfolio_id': clicked_portfolio,
                    'simulation_id': clicked_simulation
                }]
                print(f"[Callback] Different column, reset to single selection")

            # Get metadata for grid recreation
            meta = all_results.get('_meta', {})
            results_for_grid = {k: v for k, v in all_results.items() if k != '_meta'}
            portfolio_names = meta.get('portfolio_names', {})

            # Handle empty selection (show empty state)
            if not new_selection:
                empty_fig = create_empty_figure("Click a cell to view distributions", dark_mode=dark_mode)
                grid_args = (results_for_grid,
                             meta.get('active_portfolios', []),
                             meta.get('active_simulations', []),
                             portfolio_names,
                             meta.get('simulation_names', {}),
                             new_selection, dark_mode)
                grid_cagr = create_results_grid(*grid_args, metric='cagr')
                grid_sharpe = create_results_grid(*grid_args, metric='sharpe_ratio')
                grid_drawdown = create_results_grid(*grid_args, metric='max_drawdown')
                grid_volatility = create_results_grid(*grid_args, metric='annual_volatility')
                print(f"[Callback] Empty selection, showing placeholder")
                return new_selection, [grid_cagr], [grid_sharpe], [grid_drawdown], [grid_volatility], empty_fig

            # Build list of (label, SimulationResults) for distribution chart
            results_list = []
            for cell in new_selection:
                cell_key = f"{cell['portfolio_id']}|{cell['simulation_id']}"
                if cell_key in all_results:
                    data = all_results[cell_key]
                    results_obj = _reconstruct_simulation_results(data)
                    label = portfolio_names.get(cell['portfolio_id'], cell['portfolio_id'])
                    results_list.append((label, results_obj))

            # Create distribution chart (single or multi)
            if len(results_list) == 1:
                grid_fig = create_metrics_grid(results_list[0][1], dark_mode=dark_mode)
            else:
                grid_fig = create_multi_metrics_grid(results_list, dark_mode=dark_mode)

            # Recreate all 4 results grids with the new selection highlighted
            grid_args = (results_for_grid,
                         meta.get('active_portfolios', []),
                         meta.get('active_simulations', []),
                         portfolio_names,
                         meta.get('simulation_names', {}),
                         new_selection, dark_mode)
            grid_cagr = create_results_grid(*grid_args, metric='cagr')
            grid_sharpe = create_results_grid(*grid_args, metric='sharpe_ratio')
            grid_drawdown = create_results_grid(*grid_args, metric='max_drawdown')
            grid_volatility = create_results_grid(*grid_args, metric='annual_volatility')

            print(f"[Callback] Cell selection successful, {len(new_selection)} cells selected")
            return new_selection, [grid_cagr], [grid_sharpe], [grid_drawdown], [grid_volatility], grid_fig

        except Exception as e:
            print(f"[Callback] Error handling cell selection: {e}")
            import traceback
            traceback.print_exc()
            return no_update, no_update, no_update, no_update, no_update, no_update

    # Callback for toggling available simulation details
    @app.callback(
        Output({'type': 'collapse-avail-sim', 'index': ALL}, 'is_open'),
        Input({'type': 'toggle-avail-sim', 'index': ALL}, 'n_clicks'),
        State({'type': 'collapse-avail-sim', 'index': ALL}, 'is_open'),
        prevent_initial_call=True
    )
    def toggle_available_simulation_details(n_clicks, is_open_states):
        """Toggle the collapse state of available simulation details."""
        if not ctx.triggered_id or not any(n_clicks):
            return no_update

        triggered_index = ctx.triggered_id['index']

        # Get the list of all simulation IDs in order
        all_sim_ids = [s.id for s in simulation_registry.list_all()]

        # Toggle only the one that was clicked
        new_states = []
        for i, (sim_id, is_open) in enumerate(zip(all_sim_ids, is_open_states)):
            if sim_id == triggered_index:
                new_states.append(not is_open)
            else:
                new_states.append(is_open)

        return new_states

    # Callback for toggling active simulation details
    @app.callback(
        Output({'type': 'collapse-active-sim', 'index': ALL}, 'is_open'),
        Input({'type': 'toggle-active-sim', 'index': ALL}, 'n_clicks'),
        State({'type': 'collapse-active-sim', 'index': ALL}, 'is_open'),
        State('active-simulations-store', 'data'),
        prevent_initial_call=True
    )
    def toggle_active_simulation_details(n_clicks, is_open_states, active_sim_ids):
        """Toggle the collapse state of active simulation details."""
        if not ctx.triggered_id or not any(c for c in n_clicks if c):
            return no_update

        triggered_index = ctx.triggered_id['index']

        if not active_sim_ids:
            return no_update

        # Toggle only the one that was clicked
        new_states = []
        for i, (sim_id, is_open) in enumerate(zip(active_sim_ids, is_open_states)):
            if sim_id == triggered_index:
                new_states.append(not is_open)
            else:
                new_states.append(is_open)

        return new_states
