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
from .services.cache import results_cache
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

THEME_LIGHT = dbc.themes.BOOTSTRAP
THEME_DARK = dbc.themes.DARKLY


def _reconstruct_simulation_results(data: dict):
    """Reconstruct SimulationResults from serialized dict format."""
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


def _handle_add_remove_action(current_active: list, triggered_id: dict) -> list:
    """Handle add/remove button action for any registry item.

    Returns updated list of active item IDs.
    """
    if current_active is None:
        current_active = []

    item_id = triggered_id['index']
    action = triggered_id['type']

    if 'add-' in action and item_id not in current_active:
        return current_active + [item_id]
    elif 'remove-' in action and item_id in current_active:
        return [i for i in current_active if i != item_id]
    return current_active


def register_callbacks(app):
    """Register all callbacks with the Dash app."""

    # Clientside callback for toggling body class
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

    @app.callback(
        [Output('dark-mode-store', 'data'), Output('theme-stylesheet', 'href')],
        Input('dark-mode-switch', 'value'),
    )
    def update_dark_mode(dark_mode):
        """Update dark mode store and stylesheet based on switch value."""
        if dark_mode is None:
            dark_mode = True
        return dark_mode, THEME_DARK if dark_mode else THEME_LIGHT

    @app.callback(
        Output('clear-cache-btn', 'children'),
        Input('clear-cache-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_cache(n_clicks):
        """Clear the persistent cache."""
        if n_clicks:
            results_cache.clear()
            print("Cache cleared")
        return "Clear Cache"

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
        return _handle_add_remove_action(current_active, ctx.triggered_id)

    @app.callback(
        [Output('available-simulations-list', 'children'), Output('active-simulations-list', 'children')],
        Input('active-simulations-store', 'data'),
    )
    def update_simulation_lists(active_ids):
        """Update both simulation lists when active simulations change."""
        active_ids = active_ids or []
        return _create_available_simulations_list(active_ids), create_active_simulations_list(active_ids)

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
        return _handle_add_remove_action(current_active, ctx.triggered_id)

    @app.callback(
        [Output('available-portfolios-list', 'children'), Output('active-portfolios-list', 'children')],
        Input('active-portfolios-store', 'data'),
    )
    def update_portfolio_lists(active_ids):
        """Update both portfolio lists when active portfolios change."""
        active_ids = active_ids or []
        return _create_available_portfolios_list(active_ids), create_active_portfolios_list(active_ids)

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
        """Run analysis on cross-product of active portfolios x active simulations."""
        import traceback

        empty_grid = [html.P("Run analysis to see results.", className="text-muted text-center")]
        dark_mode = dark_mode if dark_mode is not None else True

        # Handle initial load
        if n_clicks is None:
            empty = create_empty_figure("Add portfolios/simulations and click 'Run Analysis' to start", dark_mode=dark_mode)
            return {}, None, empty_grid, empty_grid, empty_grid, empty_grid, empty

        # Validate inputs
        if not active_portfolios:
            empty = create_empty_figure("Please add at least one portfolio first", dark_mode=dark_mode)
            msg = [html.P("Please add at least one portfolio.", className="text-muted text-center")]
            return {}, None, msg, msg, msg, msg, empty

        if not active_simulations:
            empty = create_empty_figure("Please add at least one simulation first", dark_mode=dark_mode)
            msg = [html.P("Please add at least one simulation.", className="text-muted text-center")]
            return {}, None, msg, msg, msg, msg, empty

        try:
            all_results = {}
            portfolio_names = {pid: registry.get(pid).display_name for pid in active_portfolios}
            simulation_names = {sid: simulation_registry.get(sid).display_name for sid in active_simulations}

            for portfolio_id in active_portfolios:
                for simulation_id in active_simulations:
                    key = f"{portfolio_id}|{simulation_id}"
                    all_results[key] = run_portfolio_analysis(
                        portfolio_id=portfolio_id,
                        simulation_id=simulation_id,
                        initial_amt=initial_amt or DEFAULT_INITIAL_AMT,
                        monthly_cf=monthly_cf or DEFAULT_MONTHLY_CF,
                    )

            # Select first cell by default
            selected_cells = [{'portfolio_id': active_portfolios[0], 'simulation_id': active_simulations[0]}]
            first_key = f"{active_portfolios[0]}|{active_simulations[0]}"

            # Create results grids
            grid_args = (all_results, active_portfolios, active_simulations,
                         portfolio_names, simulation_names, selected_cells, dark_mode)
            grids = [create_results_grid(*grid_args, metric=m)
                     for m in ['cagr', 'sharpe_ratio', 'max_drawdown', 'annual_volatility']]
            grid_fig = create_metrics_grid(all_results[first_key], dark_mode=dark_mode)

            # Serialize results for storage
            serialized_results = _serialize_results(all_results, portfolio_names, simulation_names,
                                                     active_portfolios, active_simulations)

            return serialized_results, selected_cells, [grids[0]], [grids[1]], [grids[2]], [grids[3]], grid_fig

        except Exception as e:
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
        """Handle cell selection with multi-select toggle behavior."""
        if not ctx.triggered_id:
            return no_update, no_update, no_update, no_update, no_update, no_update

        if n_clicks is None or not isinstance(n_clicks, list) or not any(c and c > 0 for c in n_clicks):
            return no_update, no_update, no_update, no_update, no_update, no_update

        if not all_results:
            return no_update, no_update, no_update, no_update, no_update, no_update

        dark_mode = dark_mode if dark_mode is not None else True
        current_selection = current_selection if isinstance(current_selection, list) else []

        try:
            triggered = ctx.triggered_id
            clicked_portfolio = triggered['portfolio']
            clicked_simulation = triggered['simulation']
            key = f"{clicked_portfolio}|{clicked_simulation}"

            if key not in all_results:
                return no_update, no_update, no_update, no_update, no_update, no_update

            new_selection = _compute_new_selection(current_selection, clicked_portfolio, clicked_simulation)

            meta = all_results.get('_meta', {})
            results_for_grid = {k: v for k, v in all_results.items() if k != '_meta'}
            portfolio_names = meta.get('portfolio_names', {})

            # Handle empty selection
            if not new_selection:
                empty_fig = create_empty_figure("Click a cell to view distributions", dark_mode=dark_mode)
                grids = _create_all_grids(results_for_grid, meta, new_selection, dark_mode)
                return new_selection, [grids[0]], [grids[1]], [grids[2]], [grids[3]], empty_fig

            # Build results list for distribution chart
            results_list = []
            for cell in new_selection:
                cell_key = f"{cell['portfolio_id']}|{cell['simulation_id']}"
                if cell_key in all_results:
                    results_obj = _reconstruct_simulation_results(all_results[cell_key])
                    label = portfolio_names.get(cell['portfolio_id'], cell['portfolio_id'])
                    results_list.append((label, results_obj))

            if len(results_list) == 1:
                grid_fig = create_metrics_grid(results_list[0][1], dark_mode=dark_mode)
            else:
                grid_fig = create_multi_metrics_grid(results_list, dark_mode=dark_mode)

            grids = _create_all_grids(results_for_grid, meta, new_selection, dark_mode)
            return new_selection, [grids[0]], [grids[1]], [grids[2]], [grids[3]], grid_fig

        except Exception as e:
            import traceback
            traceback.print_exc()
            return no_update, no_update, no_update, no_update, no_update, no_update

    @app.callback(
        Output({'type': 'collapse-avail-sim', 'index': ALL}, 'is_open'),
        Input({'type': 'toggle-avail-sim', 'index': ALL}, 'n_clicks'),
        State({'type': 'collapse-avail-sim', 'index': ALL}, 'is_open'),
        prevent_initial_call=True
    )
    def toggle_available_simulation_details(n_clicks, is_open_states):
        """Toggle the collapse state of available simulation details."""
        return _toggle_collapse_state(n_clicks, is_open_states,
                                       [s.id for s in simulation_registry.list_all()])

    @app.callback(
        Output({'type': 'collapse-active-sim', 'index': ALL}, 'is_open'),
        Input({'type': 'toggle-active-sim', 'index': ALL}, 'n_clicks'),
        State({'type': 'collapse-active-sim', 'index': ALL}, 'is_open'),
        State('active-simulations-store', 'data'),
        prevent_initial_call=True
    )
    def toggle_active_simulation_details(n_clicks, is_open_states, active_sim_ids):
        """Toggle the collapse state of active simulation details."""
        if not active_sim_ids:
            return no_update
        return _toggle_collapse_state(n_clicks, is_open_states, active_sim_ids)


def _toggle_collapse_state(n_clicks, is_open_states, item_ids):
    """Toggle collapse state for the triggered item."""
    if not ctx.triggered_id or not any(c for c in n_clicks if c):
        return no_update

    triggered_index = ctx.triggered_id['index']
    return [
        (not is_open) if item_id == triggered_index else is_open
        for item_id, is_open in zip(item_ids, is_open_states)
    ]


def _compute_new_selection(current_selection, clicked_portfolio, clicked_simulation):
    """Compute new cell selection based on click rules.

    Rules:
    1. Clicking unselected cell in same column: add to selection (up to 4)
    2. Clicking selected cell: deselect it (toggle off)
    3. Clicking cell in different column: reset selection to just that cell
    """
    current_column = current_selection[0].get('simulation_id') if current_selection else None

    is_already_selected = any(
        cell.get('portfolio_id') == clicked_portfolio and
        cell.get('simulation_id') == clicked_simulation
        for cell in current_selection
    )

    if is_already_selected:
        return [
            cell for cell in current_selection
            if not (cell['portfolio_id'] == clicked_portfolio and
                   cell['simulation_id'] == clicked_simulation)
        ]
    elif clicked_simulation == current_column and len(current_selection) < 4:
        return current_selection + [{'portfolio_id': clicked_portfolio, 'simulation_id': clicked_simulation}]
    else:
        return [{'portfolio_id': clicked_portfolio, 'simulation_id': clicked_simulation}]


def _create_all_grids(results, meta, selected_cells, dark_mode):
    """Create all 4 metric grids."""
    grid_args = (
        results,
        meta.get('active_portfolios', []),
        meta.get('active_simulations', []),
        meta.get('portfolio_names', {}),
        meta.get('simulation_names', {}),
        selected_cells,
        dark_mode
    )
    return [create_results_grid(*grid_args, metric=m)
            for m in ['cagr', 'sharpe_ratio', 'max_drawdown', 'annual_volatility']]


def _serialize_results(all_results, portfolio_names, simulation_names, active_portfolios, active_simulations):
    """Serialize results for storage in dcc.Store."""
    serialized = {}
    for key, res in all_results.items():
        serialized[key] = {
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

    serialized['_meta'] = {
        'portfolio_names': portfolio_names,
        'simulation_names': simulation_names,
        'active_portfolios': active_portfolios,
        'active_simulations': active_simulations,
    }
    return serialized
