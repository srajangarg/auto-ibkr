"""Simulation registry for extensible Monte Carlo simulation management."""
from dataclasses import dataclass
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from monte_carlo import RFSchedule
from constants import DEFAULT_MC_SIMULATIONS, DEFAULT_MC_YEARS


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


class SimulationRegistry:
    """Registry for all available simulation presets.

    Provides a centralized way to register, retrieve, and list simulations.
    New simulations can be added by calling register() with a SimulationDefinition.
    """

    def __init__(self):
        self._simulations: dict[str, SimulationDefinition] = {}

    def register(self, definition: SimulationDefinition) -> None:
        """Register a simulation definition."""
        if definition.id in self._simulations:
            raise ValueError(f"Simulation '{definition.id}' already registered")
        self._simulations[definition.id] = definition

    def get(self, simulation_id: str) -> SimulationDefinition:
        """Get simulation definition by ID."""
        if simulation_id not in self._simulations:
            raise KeyError(f"Simulation '{simulation_id}' not found")
        return self._simulations[simulation_id]

    def list_all(self) -> List[SimulationDefinition]:
        """List all registered simulations."""
        return list(self._simulations.values())

    def list_by_category(self, category: str) -> List[SimulationDefinition]:
        """List simulations in a specific category."""
        return [s for s in self._simulations.values() if s.category == category]

    def get_dropdown_options(self) -> List[dict]:
        """Get options formatted for Dash dropdown component."""
        return [
            {"label": s.display_name, "value": s.id}
            for s in self._simulations.values()
        ]

    def get_ids(self) -> List[str]:
        """Get list of all simulation IDs."""
        return list(self._simulations.keys())


# Global registry instance
simulation_registry = SimulationRegistry()
