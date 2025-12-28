#!/usr/bin/env python3
"""
Time and date utility functions for market-related operations.
Uses pandas_market_calendars (mcal) for accurate NYSE business day calculations.
"""

import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime, timedelta
from typing import Union, Tuple, Optional

# Cache the NYSE calendar
_NYSE_CALENDAR = None

def get_nyse_calendar():
    """Get the NYSE market calendar (cached)."""
    global _NYSE_CALENDAR
    if _NYSE_CALENDAR is None:
        _NYSE_CALENDAR = mcal.get_calendar("NYSE")
    return _NYSE_CALENDAR

def to_timestamp(date_input: Union[str, datetime, pd.Timestamp]) -> pd.Timestamp:
    """
    Convert various date formats to pd.Timestamp.
    
    Args:
        date_input: String (YYYY-MM-DD), datetime, or pd.Timestamp
        
    Returns:
        pd.Timestamp with America/New_York timezone
    """
    if isinstance(date_input, pd.Timestamp):
        ts = date_input
    else:
        ts = pd.Timestamp(date_input)
    
    # Ensure timezone is set to America/New_York
    if ts.tz is None:
        ts = ts.tz_localize("America/New_York")
    else:
        ts = ts.tz_convert("America/New_York")
    
    return ts

def get_latest_business_date(reference_date: Optional[Union[str, datetime, pd.Timestamp]] = None) -> datetime.date:
    """
    Get the latest NYSE business date at or before the reference date.
    
    Args:
        reference_date: Date to check from. Defaults to today.
        
    Returns:
        datetime.date object for the latest NYSE trading day
    """
    if reference_date is None:
        reference_date = pd.Timestamp.now(tz="America/New_York")
    else:
        reference_date = to_timestamp(reference_date)
    
    nyse = get_nyse_calendar()
    
    # Get schedule for the past 10 days to find the latest trading day
    schedule = nyse.schedule(
        start_date=reference_date - pd.Timedelta(days=10),
        end_date=reference_date
    )
    
    if schedule.empty:
        raise ValueError(f"No trading schedule found near {reference_date.date()}")
    
    # Return the last valid trading day
    return schedule.index[-1].date()

def is_business_day(date_input: Union[str, datetime, pd.Timestamp]) -> bool:
    """
    Check if a given date is an NYSE business day.
    
    Args:
        date_input: Date to check
        
    Returns:
        True if it's a business day, False otherwise
    """
    date_ts = to_timestamp(date_input)
    nyse = get_nyse_calendar()
    
    schedule = nyse.schedule(
        start_date=date_ts.date(),
        end_date=date_ts.date()
    )
    
    return not schedule.empty

def get_next_business_day(date_input: Union[str, datetime, pd.Timestamp]) -> datetime.date:
    """
    Get the next NYSE business day after the given date.
    
    Args:
        date_input: Starting date
        
    Returns:
        datetime.date for the next business day
    """
    date_ts = to_timestamp(date_input)
    nyse = get_nyse_calendar()
    
    # Get schedule starting from tomorrow
    schedule = nyse.schedule(
        start_date=date_ts.date() + timedelta(days=1),
        end_date=date_ts.date() + timedelta(days=30)
    )
    
    if schedule.empty:
        raise ValueError(f"No trading days found after {date_ts.date()}")
    
    return schedule.index[0].date()

def get_previous_business_day(date_input: Union[str, datetime, pd.Timestamp]) -> datetime.date:
    """
    Get the previous NYSE business day before the given date.
    
    Args:
        date_input: Starting date
        
    Returns:
        datetime.date for the previous business day
    """
    date_ts = to_timestamp(date_input)
    nyse = get_nyse_calendar()
    
    # Get schedule for the past 30 days
    schedule = nyse.schedule(
        start_date=date_ts.date() - timedelta(days=30),
        end_date=date_ts.date() - timedelta(days=1)
    )
    
    if schedule.empty:
        raise ValueError(f"No trading days found before {date_ts.date()}")
    
    return schedule.index[-1].date()

def get_date_range(
    start_date: Union[str, datetime, pd.Timestamp],
    end_date: Union[str, datetime, pd.Timestamp]
) -> Tuple[datetime.date, datetime.date]:
    """
    Get a valid date range for NYSE business days.
    If start_date is not a business day, returns the next business day.
    If end_date is not a business day, returns the previous business day.
    
    Args:
        start_date: Start date (will be adjusted to next business day if needed)
        end_date: End date (will be adjusted to previous business day if needed)
        
    Returns:
        Tuple of (adjusted_start_date, adjusted_end_date)
    """
    start_ts = to_timestamp(start_date)
    end_ts = to_timestamp(end_date)
    
    nyse = get_nyse_calendar()
    
    # Get the schedule for the full range
    schedule = nyse.schedule(
        start_date=start_ts.date() - timedelta(days=1),
        end_date=end_ts.date() + timedelta(days=1)
    )
    
    if schedule.empty:
        raise ValueError(f"No trading days found in range {start_ts.date()} to {end_ts.date()}")
    
    # Find the first date >= start_date
    valid_start = None
    for trade_date in schedule.index:
        if trade_date.date() >= start_ts.date():
            valid_start = trade_date.date()
            break
    
    # Find the last date <= end_date
    valid_end = None
    for trade_date in reversed(schedule.index):
        if trade_date.date() <= end_ts.date():
            valid_end = trade_date.date()
            break
    
    if valid_start is None or valid_end is None:
        raise ValueError(f"No valid trading days in range {start_ts.date()} to {end_ts.date()}")
    
    return valid_start, valid_end

def get_business_days_between(
    start_date: Union[str, datetime, pd.Timestamp],
    end_date: Union[str, datetime, pd.Timestamp]
) -> list:
    """
    Get all NYSE business days between start_date and end_date (inclusive).
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        List of datetime.date objects for all business days in range
    """
    start_ts = to_timestamp(start_date)
    end_ts = to_timestamp(end_date)
    
    nyse = get_nyse_calendar()
    schedule = nyse.schedule(start_date=start_ts.date(), end_date=end_ts.date())
    
    return [date.date() for date in schedule.index]

def get_business_days_count(
    start_date: Union[str, datetime, pd.Timestamp],
    end_date: Union[str, datetime, pd.Timestamp]
) -> int:
    """
    Count the number of NYSE business days between start_date and end_date (inclusive).
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Number of business days
    """
    return len(get_business_days_between(start_date, end_date))

if __name__ == '__main__':
    # Test examples
    print("Time Utilities Examples:")
    print("-" * 50)
    
    today = datetime.now()
    latest = get_latest_business_date()
    print(f"Latest business date: {latest}")
    
    is_bday = is_business_day('2025-12-26')  # Friday
    print(f"Is 2025-12-26 a business day? {is_bday}")
    
    next_bday = get_next_business_day('2025-12-26')
    print(f"Next business day after 2025-12-26: {next_bday}")
    
    prev_bday = get_previous_business_day('2025-12-29')
    print(f"Previous business day before 2025-12-29: {prev_bday}")
    
    start, end = get_date_range('2025-12-20', '2025-12-31')
    print(f"Date range (2025-12-20 to 2025-12-31): {start} to {end}")
    
    count = get_business_days_count('2025-12-20', '2025-12-31')
    print(f"Business days between 2025-12-20 and 2025-12-31: {count}")
