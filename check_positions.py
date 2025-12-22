import asyncio
import os
import logging
import nest_asyncio
from ib_async import IB

# Allow nested event loops for ib_async
nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
TRADING_MODE = os.getenv('TRADING_MODE', 'paper').lower()
DEFAULT_PORT = 4001 if TRADING_MODE == 'live' else 4002
PORT = int(os.getenv('IB_PORT', DEFAULT_PORT))
HOST = os.getenv('IB_HOST', '127.0.0.1')
CLIENT_ID = int(os.getenv('IB_CLIENT_ID', '1'))

async def main():
    ib = IB()
    try:
        logger.info(f"Connecting to Gateway on {HOST}:{PORT} (Mode: {TRADING_MODE}, ClientID: {CLIENT_ID})...")
        await ib.connectAsync(HOST, PORT, clientId=CLIENT_ID)
        logger.info("Connected successfully.")

        # Ensure we have fresh data
        logger.info("Requesting positions...")
        positions = ib.positions()
        
        if not positions:
            logger.info("No active positions found.")
        else:
            logger.info(f"Found {len(positions)} positions:")
            for p in positions:
                logger.info(f" - {p.contract.symbol}: {p.position} shares @ {p.avgCost}")

        # Get Account Summary (Cash/NAV)
        logger.info("Requesting account summary...")
        account_summary = await ib.accountSummaryAsync()
        
        if not account_summary:
             logger.warning("No account summary data available yet.")
        else:
            relevant_tags = {'NetLiquidation', 'TotalCashValue', 'BuyingPower'}
            for item in account_summary:
                if item.tag in relevant_tags:
                    logger.info(f" - {item.tag}: {item.value} {item.currency}")

    except ConnectionRefusedError:
        logger.error(f"Could not connect to IB Gateway at {HOST}:{PORT}. Is it running?")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
    finally:
        if ib.isConnected():
            ib.disconnect()
            logger.info("Disconnected.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")

