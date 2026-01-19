"""Dash application factory and configuration."""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from .layouts import create_layout
from .callbacks import register_callbacks

# Theme URLs for switching
THEME_LIGHT = dbc.themes.BOOTSTRAP
THEME_DARK = dbc.themes.DARKLY


def create_app(debug: bool = False) -> dash.Dash:
    """Create and configure the Dash application.

    Args:
        debug: Enable debug mode

    Returns:
        Configured Dash application
    """
    app = dash.Dash(
        __name__,
        external_stylesheets=[THEME_LIGHT],
        title="Backtest Dashboard",
        update_title="Loading...",
        suppress_callback_exceptions=True
    )

    # Wrap layout with theme stylesheet link for dynamic switching
    def serve_layout():
        return html.Div([
            # Dynamic theme stylesheet (start with dark theme)
            html.Link(id='theme-stylesheet', rel='stylesheet', href=THEME_DARK),
            # Store for dark mode state (persisted in localStorage, default True)
            dcc.Store(id='dark-mode-store', storage_type='local', data=True),
            # Main layout
            create_layout()
        ])

    app.layout = serve_layout

    # Register callbacks
    register_callbacks(app)

    return app


# Create app instance for imports
app = create_app()

# Expose Flask server for production deployment
server = app.server


if __name__ == '__main__':
    app.run(debug=True, port=8050)
