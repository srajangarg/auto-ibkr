"""Dash application factory and configuration."""
import dash
import dash_bootstrap_components as dbc

from .layouts import create_layout
from .callbacks import register_callbacks


def create_app(debug: bool = False) -> dash.Dash:
    """Create and configure the Dash application.

    Args:
        debug: Enable debug mode

    Returns:
        Configured Dash application
    """
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        title="Backtest Dashboard",
        update_title="Loading...",
        suppress_callback_exceptions=True
    )

    # Set layout
    app.layout = create_layout()

    # Register callbacks
    register_callbacks(app)

    return app


# Create app instance for imports
app = create_app()

# Expose Flask server for production deployment
server = app.server


if __name__ == '__main__':
    app.run(debug=True, port=8050)
