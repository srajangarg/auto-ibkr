# Auto-IBKR: Automated Interactive Brokers Trading

This project implements a "Just-in-Time" (JIT) trading infrastructure designed for **headless Ubuntu servers**. It is optimized for low-frequency strategies (e.g., bi-weekly rebalancing) while minimizing the friction of maintaining an authenticated Interactive Brokers (IBKR) session.

## Architecture

The system uses a JIT lifecycle to handle IBKR's mandatory 2FA and daily/weekly session resets:

1.  **On-Demand Gateway**: Spins up an IB Gateway instance inside a Docker container only when needed.
2.  **Out-of-Band 2FA**: The automation tool (IBC) triggers a push notification to the user's phone (IB Key).
3.  **Python Execution**: Once authenticated, a Python script (`ib_async`) connects to the gateway, executes trades/checks, and disconnects.
4.  **Automatic Shutdown**: The container is stopped immediately after completion to save resources and enhance security.

## Tech Stack

- **Containerization**: [gnzsnz/ib-gateway](https://hub.docker.com/r/gnzsnz/ib-gateway) (bundles IB Gateway, IBC, and Xvfb for headless GUI support).
- **Package Management**: `uv` for fast, reproducible Python environments.
- **Python Library**: `ib_async` (the community-maintained successor to `ib_insync`).
- **Orchestration**: A Bash wrapper (`run_cycle.sh`) that manages the container lifecycle and waits for API port availability.

## Setup

1.  **Configure Credentials**:
    ```bash
    cp env.example .env
    # Edit .env with your TWS_USERID and TWS_PASSWORD
    ```

2.  **Execute a Cycle**:
    ```bash
    ./run_cycle.sh
    ```
    *Note: Watch your phone for the IB Key notification immediately after starting.*

## Files

- `run_cycle.sh`: The master orchestrator.
- `check_positions.py`: Sample script to fetch and print current portfolio positions.
- `docker-compose.yml`: Defines the IB Gateway service.
- `pyproject.toml` / `uv.lock`: Dependency management via `uv`.

## Security Notes

- This setup is designed for **headless environments**. 
- It does **not** store your 2FA secrets; it relies on manual approval via your mobile device to bridge the security gap.
- Port `5900` (VNC) is exposed by default for debugging but should be tunneled via SSH or firewalled in production.

