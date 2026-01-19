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

# Stable Market + GARCH
simulation_registry.register(SimulationDefinition(
    id="stable_market_garch",
    display_name="Stable Market + GARCH",
    description="Constant 4% RF with GARCH volatility dynamics.",
    use_garch=True,
    use_erp=False,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.04,
        end_rate=0.04
    ),
    category="baseline"
))

# Stable Market + ERP
simulation_registry.register(SimulationDefinition(
    id="stable_market_erp",
    display_name="Stable Market + ERP",
    description="Constant 4% RF with equity risk premium modeling.",
    use_garch=False,
    use_erp=True,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.04,
        end_rate=0.04
    ),
    category="baseline"
))

# Stable Market + GARCH + ERP
simulation_registry.register(SimulationDefinition(
    id="stable_market_garch_erp",
    display_name="Stable Market + GARCH + ERP",
    description="Constant 4% RF with GARCH volatility and equity risk premium.",
    use_garch=True,
    use_erp=True,
    rf_schedule=RFSchedule(
        schedule_type='constant',
        start_rate=0.04,
        end_rate=0.04
    ),
    category="baseline"
))
