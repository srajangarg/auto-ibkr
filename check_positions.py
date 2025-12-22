import asyncio
import os
from ib_async import *

# Configuration
# Use 4001 for LIVE, 4002 for PAPER
# We'll try to detect the mode from TRADING_MODE if available
TRADING_MODE = os.getenv('TRADING_MODE', 'paper').lower()
PORT = 4001 if TRADING_MODE == 'live' else 4002
HOST = '127.0.0.1'
CLIENT_ID = 1

async def main():
    ib = IB()
    try:
        print(f"[Python] Connecting to Gateway on {HOST}:{PORT} (Mode: {TRADING_MODE})...")
        await ib.connectAsync(HOST, PORT, clientId=CLIENT_ID)
        print("[Python] Connected successfully.")

        # Ensure we have fresh data
        print("[Python] Requesting positions...")
        positions = ib.positions()
        
        if not positions:
            print("[Python] No active positions found.")
        else:
            print(f"[Python] Found {len(positions)} positions:")
            for p in positions:
                print(f" - {p.contract.symbol}: {p.position} shares @ {p.avgCost}")

        # Get Account Summary (Cash/NAV)
        print("\n[Python] Account Summary:")
        # We need to wait for account summary tags to be filled
        account_summary = ib.accountSummary()
        if not account_summary:
             # If summary is empty immediately, we might need to wait or request it specifically
             # accountSummary() is a list of AccountValue objects that gets updated.
             # For a one-off script, we can just print what's there.
             print(" - No account summary data available yet.")
        else:
            for item in account_summary:
                if item.tag in ['NetLiquidation', 'TotalCashValue', 'BuyingPower']:
                    print(f" - {item.tag}: {item.value} {item.currency}")

    except Exception as e:
        print(f"[Python] Error: {e}")
    finally:
        ib.disconnect()
        print("[Python] Disconnected.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

