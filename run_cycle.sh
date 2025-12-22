#!/bin/bash

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Define Ports (must match python script logic)
# 4002 = Paper, 4001 = Live
if [ "$TRADING_MODE" = "live" ]; then
    TARGET_PORT=4001
else
    TARGET_PORT=4002
fi

echo "[Shell] Starting IB Gateway (Mode: ${TRADING_MODE:-paper})... Check your phone for 2FA Notification!"
docker-compose up -d

# Wait loop: Gives you 120 seconds to approve login on phone
echo "[Shell] Waiting for IB Gateway to authenticate (Check your phone)..."
READY=0
for i in {1..60}; do
    # Check logs for successful login message (matches IBC output)
    if docker logs ib-gateway 2>&1 | grep -qE "Login succeeded|Login has completed"; then
        echo -e "\n[Shell] Login successful! Gateway is ready."
        READY=1
        break
    fi
    # Also check if it's still waiting for 2FA to keep the user informed
    if docker logs ib-gateway 2>&1 | grep -q "Second Factor Authentication initiated"; then
        echo -n "2FA..."
    else
        echo -n "."
    fi
    sleep 2
done

if [ $READY -eq 0 ]; then
    echo -e "\n[Shell] Error: Gateway failed to start or 2FA was not approved in time."
    docker-compose down
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

# Cleanup
echo "[Shell] Strategy complete. Stopping Gateway..."
docker-compose down

