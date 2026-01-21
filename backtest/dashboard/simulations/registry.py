"""Simulation registry for extensible Monte Carlo simulation management."""
from dataclasses import dataclass
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import RFSchedule, CrashConfig
from constants import DEFAULT_MC_SIMULATIONS, DEFAULT_MC_YEARS
from ..registry_base import BaseRegistry


@dataclass
class SimulationDefinition:
    """Definition of a Monte Carlo simulation preset for the dashboard.

    Attributes:
        id: Unique identifier for the simulation
        display_name: Human-readable name shown in UI
        description: Brief description of the market scenario
        use_garch: Enable GARCH(1,1) volatility dynamics
        use_erp: Enable equity risk premium modeling
        rf_schedule: Risk-free rate schedule configuration
        num_simulations: Number of Monte Carlo simulations to run
        num_years: Length of each simulation in years
        category: Category for grouping in UI
        crash_config: Optional crash injection configuration
    """
    id: str
    display_name: str
    description: str
    use_garch: bool
    use_erp: bool
    rf_schedule: Optional[RFSchedule]
    num_simulations: int = DEFAULT_MC_SIMULATIONS
    num_years: int = DEFAULT_MC_YEARS
    category: str = "default"
    crash_config: Optional[CrashConfig] = None


# Global registry instance
simulation_registry = BaseRegistry[SimulationDefinition]()
