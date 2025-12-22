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

# Wait loop: Gives you 60 seconds to approve login on phone
echo "[Shell] Waiting for API port $TARGET_PORT to open..."
READY=0
for i in {1..30}; do
    if nc -z 127.0.0.1 $TARGET_PORT; then
        echo -e "\n[Shell] Gateway is ready!"
        READY=1
        break
    fi
    echo -n "."
    sleep 2
done

if [ $READY -eq 0 ]; then
    echo -e "\n[Shell] Error: Gateway failed to start or 2FA was not approved in time."
    docker-compose down
    exit 1
fi

# Run the strategy
echo "[Shell] Running Python Strategy..."
python3 check_positions.py

# Cleanup
echo "[Shell] Strategy complete. Stopping Gateway..."
docker-compose down

