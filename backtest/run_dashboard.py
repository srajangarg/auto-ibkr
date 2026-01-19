#!/usr/bin/env python3
"""Entry point for the backtest dashboard."""
import sys
import os

# Ensure proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard.app import create_app


def main():
    """Run the dashboard server."""
    app = create_app(debug=True)
    print("Starting Backtest Dashboard...")
    print("Open http://localhost:8050 in your browser")
    app.run(debug=True, host='0.0.0.0', port=8050)


if __name__ == '__main__':
    main()
