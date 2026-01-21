"""Pre-configured Monte Carlo simulation presets.

All presets use GARCH volatility dynamics by default for more realistic simulations.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import RFSchedule, CrashConfig

from .registry import SimulationDefinition, simulation_registry


# Stable Market (Base Case)
# Constant 4% RF with GARCH - baseline for comparison
simulation_registry.register(SimulationDefinition(
    id="stable_market",
    display_name="Stable Market",
    description="Constant 4% RF with GARCH volatility dynamics. Baseline for comparison.",
    use_garch=True,
    use_erp=True,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.04,
        end_rate=0.04
    ),
    category="baseline"
))

# Bubble/Crash Scenarios (constant 4% RF, 5 year horizon)
# x% of simulations have a 30-50% crash within 1-2.5 years, then recover
CRASH_PROBABILITIES = [0.0, 0.10, 0.20, 0.25, 0.33, 0.50, 0.75, 1.0]

for crash_prob in CRASH_PROBABILITIES:
    crash_pct = int(crash_prob * 100)
    simulation_registry.register(SimulationDefinition(
        id=f"bubble_{crash_pct}pct",
        display_name=f"Bubble ({crash_pct}% crash)",
        description=f"Constant 4% RF, {crash_pct}% of sims have 30-50% crash in years 1-2.5, 5Y horizon.",
        use_garch=True,
        use_erp=True,
        rf_schedule=RFSchedule(
            schedule_type='constant',
            start_rate=0.04,
            end_rate=0.04
        ),
        num_years=5,
        category="bubble",
        crash_config=CrashConfig(
            crash_probability=crash_prob,
            min_crash_start_days=252,   # 1 year from now
            max_crash_start_days=630,   # 2.5 years from now
            min_decline=0.30,
            max_decline=0.50,
            min_crash_duration_days=20,
            max_crash_duration_days=40
        ) if crash_prob > 0 else None
    ))
