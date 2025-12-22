#!/bin/bash

# Exit on error
set -e

# Load environment variables from .env if it exists
if [ -f .env ]; then
    # Use a more robust way to load .env
    export $(grep -v '^#' .env | xargs)
fi

# Check for required variables
if [ -z "$TWS_USERID" ] || [ -z "$TWS_PASSWORD" ]; then
    echo "[Error] TWS_USERID and TWS_PASSWORD must be set in .env"
    exit 1
fi

TRADING_MODE=${TRADING_MODE:-paper}

echo "[Shell] Starting IB Gateway (Mode: $TRADING_MODE)..."
docker compose up -d

# Cleanup function to ensure Docker is stopped
cleanup() {
    echo "[Shell] Cleaning up..."
    docker compose stop # Use stop instead of down to preserve volumes/containers for faster restart
}
trap cleanup EXIT

echo "[Shell] Waiting for IB Gateway to be healthy (this includes 2FA if needed)..."
# Wait for the container to be healthy according to our healthcheck
# This just means the API port is open. Actual login might take longer.
while true; do
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' ib-gateway 2>/dev/null || echo "not-running")
    if [ "$HEALTH" == "healthy" ]; then
        break
    fi
    if [ "$HEALTH" == "unhealthy" ]; then
        echo "[Shell] Gateway became unhealthy. Check logs."
        docker compose logs --tail 20 ib-gateway
        exit 1
    fi
    echo -n "."
    sleep 2
done
echo -e "\n[Shell] Gateway port is open."

# Now wait for the actual login message in the logs
echo "[Shell] Waiting for login confirmation..."
READY=0
for i in {1..60}; do
    if docker logs ib-gateway 2>&1 | grep -qE "Login succeeded|Login has completed"; then
        echo "[Shell] Login successful! Gateway is ready."
        READY=1
        break
    fi
    if docker logs ib-gateway 2>&1 | grep -q "Second Factor Authentication initiated"; then
        echo -n "2FA..."
    else
        echo -n "."
    fi
    sleep 2
done

if [ $READY -eq 0 ]; then
    echo -e "\n[Shell] Error: Gateway failed to authenticate in time."
    exit 1
fi

# Run the strategy
echo "[Shell] Running Python Strategy..."
if command -v uv &> /dev/null; then
    uv run check_positions.py
else
    # Fallback to absolute path if not in PATH
    /home/garg/.local/bin/uv run check_positions.py
fi

echo "[Shell] Strategy complete."
