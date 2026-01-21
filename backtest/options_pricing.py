#!/usr/bin/env python3
"""Black-Scholes option pricing and utilities for LEAPS strategy."""

import math
import numpy as np
from dataclasses import dataclass
from constants import TRADING_DAYS_PER_YEAR, DEFAULT_IV_PREMIUM, DEFAULT_IV_SKEW

# Constants for fast normal CDF
_SQRT2 = math.sqrt(2)


def _norm_cdf(x: float) -> float:
    """Fast standard normal CDF using math.erf (much faster than scipy.stats.norm.cdf)."""
    return 0.5 * (1.0 + math.erf(x / _SQRT2))


@dataclass
class OptionPosition:
    """Track an option position."""
    strike: float
    initial_dte: int  # Days to expiration when purchased
    current_dte: int  # Current days to expiration
    quantity: float   # Number of contracts (can be fractional for simulation)


def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculate Black-Scholes call option price.

    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration in years
        r: Risk-free rate (annualized, decimal)
        sigma: Volatility (annualized, decimal)

    Returns:
        Call option price
    """
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        # Handle edge cases
        if T <= 0:
            return max(S - K, 0)  # Intrinsic value at expiration
        return 0.0

    sqrt_T = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    call_price = S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    return call_price


def black_scholes_delta(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculate Black-Scholes call option delta.

    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration in years
        r: Risk-free rate (annualized, decimal)
        sigma: Volatility (annualized, decimal)

    Returns:
        Call option delta (0 to 1)
    """
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        if T <= 0:
            return 1.0 if S > K else 0.0
        return 0.0

    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return _norm_cdf(d1)


def dte_to_years(dte: int) -> float:
    """Convert days to expiration to years."""
    return dte / TRADING_DAYS_PER_YEAR


def adjusted_iv(
    realized_vol: float,
    S: float,
    K: float,
    iv_premium: float = DEFAULT_IV_PREMIUM,
    skew: float = DEFAULT_IV_SKEW
) -> float:
    """
    Adjust realized volatility to implied volatility with smile/skew.

    Models the volatility smile observed in equity options markets:
    - IV premium: implied vol typically exceeds realized vol
    - Skew: OTM puts (ITM calls) have higher IV than ATM
    - Smile: far OTM options have elevated IV (quadratic term)

    Args:
        realized_vol: Historical/realized volatility (annualized, decimal)
        S: Current spot price
        K: Strike price
        iv_premium: Multiplier for realized → implied vol (default 1.2 = 20% premium)
        skew: Skew parameter, negative for typical equity skew (default -0.15)

    Returns:
        Adjusted implied volatility
    """
    if S <= 0 or K <= 0:
        return realized_vol * iv_premium

    # Log-moneyness: negative for ITM calls (K < S), positive for OTM (K > S)
    moneyness = math.log(K / S)

    # Smile adjustment: linear skew + quadratic smile
    # - Skew term: with negative skew, ITM calls (negative moneyness) get higher IV
    # - Smile term: both wings get elevated IV
    smile_adj = 1 + skew * moneyness + 0.5 * moneyness**2

    return realized_vol * iv_premium * smile_adj


if __name__ == "__main__":
    # Test cases to verify Black-Scholes implementation
    print("Black-Scholes Call Option Pricing Tests")
    print("=" * 50)

    # Test 1: ATM option
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.20
    price = black_scholes_call(S, K, T, r, sigma)
    delta = black_scholes_delta(S, K, T, r, sigma)
    print(f"ATM: S={S}, K={K}, T={T}y, r={r}, σ={sigma}")
    print(f"  Price: ${price:.4f}, Delta: {delta:.4f}")
    # Expected: ~$10.45 for ATM 1Y option with 20% vol

    # Test 2: Deep ITM option
    S, K, T, r, sigma = 100, 80, 1.0, 0.05, 0.20
    price = black_scholes_call(S, K, T, r, sigma)
    delta = black_scholes_delta(S, K, T, r, sigma)
    print(f"\nDeep ITM: S={S}, K={K}, T={T}y, r={r}, σ={sigma}")
    print(f"  Price: ${price:.4f}, Delta: {delta:.4f}")
    # Expected: high price (~$23-24), delta close to 1

    # Test 3: Deep OTM option
    S, K, T, r, sigma = 100, 120, 1.0, 0.05, 0.20
    price = black_scholes_call(S, K, T, r, sigma)
    delta = black_scholes_delta(S, K, T, r, sigma)
    print(f"\nDeep OTM: S={S}, K={K}, T={T}y, r={r}, σ={sigma}")
    print(f"  Price: ${price:.4f}, Delta: {delta:.4f}")
    # Expected: low price (~$2-3), delta close to 0.3

    # Test 4: 2Y LEAPS (what we'll use in backtest)
    S, K, T, r, sigma = 100, 100, 2.0, 0.04, 0.25
    price = black_scholes_call(S, K, T, r, sigma)
    delta = black_scholes_delta(S, K, T, r, sigma)
    print(f"\n2Y LEAPS ATM: S={S}, K={K}, T={T}y, r={r}, σ={sigma}")
    print(f"  Price: ${price:.4f}, Delta: {delta:.4f}")

    # Test 5: Expired option (edge case)
    S, K, T, r, sigma = 100, 95, 0.0, 0.05, 0.20
    price = black_scholes_call(S, K, T, r, sigma)
    print(f"\nExpired ITM: S={S}, K={K}, T={T}y")
    print(f"  Price: ${price:.4f} (should be intrinsic: ${max(S-K, 0):.2f})")

    # Test volatility smile/skew
    print("\n" + "=" * 50)
    print("Volatility Smile/Skew Tests")
    print("=" * 50)

    S = 100
    realized_vol = 0.20
    print(f"Spot: ${S}, Realized Vol: {realized_vol:.1%}")
    print(f"IV Premium: {DEFAULT_IV_PREMIUM}, Skew: {DEFAULT_IV_SKEW}\n")

    for K in [80, 90, 100, 110, 120]:
        iv = adjusted_iv(realized_vol, S, K)
        moneyness_pct = (K / S - 1) * 100
        label = "ITM" if K < S else ("ATM" if K == S else "OTM")
        print(f"  K={K} ({label:>3}, {moneyness_pct:+.0f}%): IV = {iv:.2%}")
