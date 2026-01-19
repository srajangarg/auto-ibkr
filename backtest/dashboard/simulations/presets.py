"""Pre-configured Monte Carlo simulation presets."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import RFSchedule

from .registry import SimulationDefinition, simulation_registry


# Stable Market (Base Case)
# Constant 4% RF, no dynamics - baseline for comparison
simulation_registry.register(SimulationDefinition(
    id="stable_market",
    display_name="Stable Market",
    description="Constant 4% RF, no dynamics. Baseline for comparison.",
    use_garch=False,
    use_erp=False,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.04,
        end_rate=0.04
    ),
    category="baseline"
))

# Rising Rates
# 1% -> 5% (like 2022-2023 Fed hikes). Tests leverage stress.
simulation_registry.register(SimulationDefinition(
    id="rising_rates",
    display_name="Rising Rates",
    description="1% → 5% (like 2022-2023 Fed hikes). Tests leverage stress.",
    use_garch=True,
    use_erp=True,
    rf_schedule=RFSchedule(
        schedule_type='increasing',
        start_rate=0.01,
        end_rate=0.05
    ),
    category="stress"
))

# Crisis & Recovery (V-Shape)
# V-shaped rates 3% -> 0.5% -> 3% (COVID pattern). Tests volatility spikes.
simulation_registry.register(SimulationDefinition(
    id="crisis_recovery",
    display_name="Crisis & Recovery",
    description="V-shaped rates 3%→0.5%→3% (COVID pattern). Tests volatility spikes.",
    use_garch=True,
    use_erp=True,
    rf_schedule=RFSchedule(
        schedule_type='v_shape',
        start_rate=0.03,
        end_rate=0.03,
        midpoint_rate=0.005
    ),
    category="stress"
))

# Goldilocks
# Steady 2.5% rates, muted volatility. Best-case scenario.
simulation_registry.register(SimulationDefinition(
    id="low_vol_goldilocks",
    display_name="Goldilocks",
    description="Steady 2.5% rates, muted volatility. Best-case scenario.",
    use_garch=False,
    use_erp=False,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.025,
        end_rate=0.025
    ),
    category="optimistic"
))
