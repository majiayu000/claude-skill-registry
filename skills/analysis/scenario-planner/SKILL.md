---
name: "scenario-planner"
description: "What-if analysis for construction projects: model different scenarios and their cost/schedule/resource impacts. Compare alternatives and optimize decisions."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📈", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Scenario Planner for Construction

## Overview

Model different project scenarios to understand their impacts on cost, schedule, and resources. Compare alternatives, optimize decisions, and prepare for contingencies.

## Business Case

Construction decisions require understanding trade-offs:
- **Design Alternatives**: Which option is most cost-effective?
- **Schedule Compression**: What's the cost of accelerating?
- **Resource Options**: In-house vs. subcontractor?
- **Risk Scenarios**: What if materials increase 20%?

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from copy import deepcopy

@dataclass
class ScenarioParameter:
    name: str
    base_value: float
    unit: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: str = ""

@dataclass
class Scenario:
    id: str
    name: str
    description: str
    parameters: Dict[str, float]
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ScenarioResult:
    scenario_id: str
    scenario_name: str
    total_cost: float
    total_duration: int  # days
    resource_requirements: Dict[str, float]
    risk_score: float
    key_metrics: Dict[str, float]
    warnings: List[str]
    comparison_to_base: Dict[str, float]

@dataclass
class SensitivityResult:
    parameter: str
    values_tested: List[float]
    cost_impacts: List[float]
    duration_impacts: List[float]
    sensitivity_score: float

class ConstructionScenarioPlanner:
    """Scenario planning and what-if analysis for construction."""

    def __init__(self, base_project: Dict):
        self.base_project = base_project
        self.parameters: Dict[str, ScenarioParameter] = {}
        self.scenarios: Dict[str, Scenario] = {}
        self.results: Dict[str, ScenarioResult] = {}
        self.cost_model: Optional[Callable] = None
        self.duration_model: Optional[Callable] = None
        self._setup_default_parameters()

    def _setup_default_parameters(self):
        """Setup common construction scenario parameters."""
        default_params = [
            ScenarioParameter("labor_rate", 75, "$/hr", 50, 150, "Average labor rate"),
            ScenarioParameter("material_escalation", 0, "%", -10, 30, "Material cost change"),
            ScenarioParameter("productivity_factor", 1.0, "x", 0.5, 1.5, "Labor productivity multiplier"),
            ScenarioParameter("overtime_percentage", 0, "%", 0, 50, "Overtime work percentage"),
            ScenarioParameter("crew_size", 10, "workers", 5, 50, "Average crew size"),
            ScenarioParameter("work_days_per_week", 5, "days", 5, 7, "Working days per week"),
            ScenarioParameter("contingency_percentage", 10, "%", 5, 25, "Cost contingency"),
            ScenarioParameter("weather_delay_days", 0, "days", 0, 60, "Expected weather delays"),
            ScenarioParameter("permit_delay_days", 0, "days", 0, 90, "Expected permit delays"),
            ScenarioParameter("subcontractor_markup", 15, "%", 10, 30, "Subcontractor markup"),
        ]

        for param in default_params:
            self.parameters[param.name] = param

    def add_parameter(self, param: ScenarioParameter):
        """Add custom parameter."""
        self.parameters[param.name] = param

    def set_cost_model(self, model: Callable):
        """Set custom cost calculation model."""
        self.cost_model = model

    def set_duration_model(self, model: Callable):
        """Set custom duration calculation model."""
        self.duration_model = model

    def create_scenario(self, name: str, description: str,
                       parameter_changes: Dict[str, float]) -> Scenario:
        """Create a new scenario with parameter modifications."""
        # Start with base values
        params = {p.name: p.base_value for p in self.parameters.values()}

        # Apply changes
        for param_name, value in parameter_changes.items():
            if param_name in params:
                params[param_name] = value
            else:
                raise ValueError(f"Unknown parameter: {param_name}")

        scenario = Scenario(
            id=f"SCN-{len(self.scenarios) + 1:03d}",
            name=name,
            description=description,
            parameters=params
        )

        self.scenarios[scenario.id] = scenario
        return scenario

    def calculate_cost(self, params: Dict[str, float]) -> float:
        """Calculate total project cost based on parameters."""
        if self.cost_model:
            return self.cost_model(self.base_project, params)

        # Default cost model
        base_cost = self.base_project.get('base_cost', 1000000)

        # Labor adjustments
        labor_factor = params['labor_rate'] / 75  # Normalized to base rate
        productivity_impact = 1 / params['productivity_factor']
        overtime_premium = 1 + (params['overtime_percentage'] / 100 * 0.5)

        labor_cost = base_cost * 0.4 * labor_factor * productivity_impact * overtime_premium

        # Material adjustments
        material_cost = base_cost * 0.35 * (1 + params['material_escalation'] / 100)

        # Equipment and other
        equipment_cost = base_cost * 0.15

        # Subcontractor
        sub_cost = base_cost * 0.1 * (1 + params['subcontractor_markup'] / 100)

        subtotal = labor_cost + material_cost + equipment_cost + sub_cost

        # Contingency
        total = subtotal * (1 + params['contingency_percentage'] / 100)

        return total

    def calculate_duration(self, params: Dict[str, float]) -> int:
        """Calculate project duration based on parameters."""
        if self.duration_model:
            return self.duration_model(self.base_project, params)

        # Default duration model
        base_duration = self.base_project.get('base_duration', 365)

        # Crew size impact
        crew_factor = 10 / params['crew_size']  # Inverse relationship

        # Productivity impact
        productivity_factor = 1 / params['productivity_factor']

        # Work days impact
        workday_factor = 5 / params['work_days_per_week']

        # Overtime compression
        overtime_compression = 1 - (params['overtime_percentage'] / 100 * 0.3)

        calculated_duration = base_duration * crew_factor * productivity_factor * workday_factor * overtime_compression

        # Add delays
        delays = params['weather_delay_days'] + params['permit_delay_days']

        return int(calculated_duration + delays)

    def evaluate_scenario(self, scenario: Scenario) -> ScenarioResult:
        """Evaluate a scenario and calculate results."""
        params = scenario.parameters

        total_cost = self.calculate_cost(params)
        total_duration = self.calculate_duration(params)

        # Calculate resource requirements
        resources = {
            'labor_hours': total_duration * params['crew_size'] * 8 * (params['work_days_per_week'] / 5),
            'peak_workers': params['crew_size'] * (1 + params['overtime_percentage'] / 100 * 0.5),
            'overtime_hours': total_duration * params['crew_size'] * 8 * params['overtime_percentage'] / 100,
        }

        # Calculate risk score (0-100)
        risk_factors = [
            params['overtime_percentage'] / 50 * 20,  # High overtime = higher risk
            (1 - params['productivity_factor']) * 20 if params['productivity_factor'] < 1 else 0,
            params['material_escalation'] / 30 * 15 if params['material_escalation'] > 0 else 0,
            (25 - params['contingency_percentage']) / 20 * 15,  # Low contingency = higher risk
        ]
        risk_score = min(sum(risk_factors), 100)

        # Key metrics
        cost_per_day = total_cost / total_duration
        cost_per_sf = total_cost / self.base_project.get('gross_area', 50000)

        key_metrics = {
            'cost_per_day': cost_per_day,
            'cost_per_sf': cost_per_sf,
            'labor_productivity': resources['labor_hours'] / total_duration,
        }

        # Warnings
        warnings = []
        if params['overtime_percentage'] > 30:
            warnings.append("High overtime may cause burnout and quality issues")
        if params['contingency_percentage'] < 8:
            warnings.append("Low contingency increases risk of budget overrun")
        if params['productivity_factor'] < 0.8:
            warnings.append("Low productivity factor may not be sustainable")

        # Compare to base scenario
        base_params = {p.name: p.base_value for p in self.parameters.values()}
        base_cost = self.calculate_cost(base_params)
        base_duration = self.calculate_duration(base_params)

        comparison = {
            'cost_change_pct': ((total_cost - base_cost) / base_cost) * 100,
            'cost_change_abs': total_cost - base_cost,
            'duration_change_pct': ((total_duration - base_duration) / base_duration) * 100,
            'duration_change_days': total_duration - base_duration,
        }

        result = ScenarioResult(
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            total_cost=total_cost,
            total_duration=total_duration,
            resource_requirements=resources,
            risk_score=risk_score,
            key_metrics=key_metrics,
            warnings=warnings,
            comparison_to_base=comparison
        )

        self.results[scenario.id] = result
        return result

    def run_sensitivity_analysis(self, parameter: str,
                                  values: List[float] = None,
                                  steps: int = 10) -> SensitivityResult:
        """Run sensitivity analysis on a single parameter."""
        if parameter not in self.parameters:
            raise ValueError(f"Unknown parameter: {parameter}")

        param = self.parameters[parameter]

        if values is None:
            min_val = param.min_value or param.base_value * 0.5
            max_val = param.max_value or param.base_value * 1.5
            values = np.linspace(min_val, max_val, steps).tolist()

        base_params = {p.name: p.base_value for p in self.parameters.values()}
        base_cost = self.calculate_cost(base_params)
        base_duration = self.calculate_duration(base_params)

        cost_impacts = []
        duration_impacts = []

        for val in values:
            test_params = base_params.copy()
            test_params[parameter] = val

            cost = self.calculate_cost(test_params)
            duration = self.calculate_duration(test_params)

            cost_impacts.append(((cost - base_cost) / base_cost) * 100)
            duration_impacts.append(((duration - base_duration) / base_duration) * 100)

        # Calculate sensitivity score (range of impact)
        cost_range = max(cost_impacts) - min(cost_impacts)
        duration_range = max(duration_impacts) - min(duration_impacts)
        sensitivity_score = (cost_range + duration_range) / 2

        return SensitivityResult(
            parameter=parameter,
            values_tested=values,
            cost_impacts=cost_impacts,
            duration_impacts=duration_impacts,
            sensitivity_score=sensitivity_score
        )

    def compare_scenarios(self, scenario_ids: List[str] = None) -> pd.DataFrame:
        """Compare multiple scenarios side by side."""
        if scenario_ids is None:
            scenario_ids = list(self.scenarios.keys())

        data = []
        for sid in scenario_ids:
            if sid not in self.results:
                scenario = self.scenarios[sid]
                self.evaluate_scenario(scenario)

            result = self.results[sid]
            data.append({
                'Scenario': result.scenario_name,
                'Total Cost': f"${result.total_cost:,.0f}",
                'Duration (days)': result.total_duration,
                'Cost Change': f"{result.comparison_to_base['cost_change_pct']:+.1f}%",
                'Duration Change': f"{result.comparison_to_base['duration_change_days']:+.0f} days",
                'Risk Score': f"{result.risk_score:.0f}/100",
                'Cost/SF': f"${result.key_metrics['cost_per_sf']:.2f}",
            })

        return pd.DataFrame(data)

    def find_optimal_scenario(self, objective: str = 'cost',
                              constraints: Dict[str, tuple] = None) -> Scenario:
        """Find optimal scenario given objective and constraints."""
        valid_results = []

        for sid, result in self.results.items():
            # Check constraints
            if constraints:
                meets_constraints = True
                if 'max_cost' in constraints and result.total_cost > constraints['max_cost']:
                    meets_constraints = False
                if 'max_duration' in constraints and result.total_duration > constraints['max_duration']:
                    meets_constraints = False
                if 'max_risk' in constraints and result.risk_score > constraints['max_risk']:
                    meets_constraints = False

                if not meets_constraints:
                    continue

            valid_results.append((sid, result))

        if not valid_results:
            return None

        # Sort by objective
        if objective == 'cost':
            valid_results.sort(key=lambda x: x[1].total_cost)
        elif objective == 'duration':
            valid_results.sort(key=lambda x: x[1].total_duration)
        elif objective == 'risk':
            valid_results.sort(key=lambda x: x[1].risk_score)
        elif objective == 'balanced':
            # Normalize and combine metrics
            valid_results.sort(key=lambda x: (
                x[1].total_cost / 1000000 +
                x[1].total_duration / 365 +
                x[1].risk_score / 100
            ))

        return self.scenarios[valid_results[0][0]]

    def generate_report(self) -> str:
        """Generate scenario comparison report."""
        lines = ["# Scenario Analysis Report", ""]
        lines.append(f"**Project:** {self.base_project.get('name', 'Project')}")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Scenarios Analyzed:** {len(self.scenarios)}")
        lines.append("")

        # Comparison table
        lines.append("## Scenario Comparison")
        comparison = self.compare_scenarios()
        lines.append(comparison.to_markdown(index=False))
        lines.append("")

        # Best scenarios
        lines.append("## Optimal Scenarios")

        best_cost = self.find_optimal_scenario('cost')
        if best_cost:
            lines.append(f"- **Lowest Cost:** {best_cost.name}")

        best_duration = self.find_optimal_scenario('duration')
        if best_duration:
            lines.append(f"- **Shortest Duration:** {best_duration.name}")

        best_balanced = self.find_optimal_scenario('balanced')
        if best_balanced:
            lines.append(f"- **Best Balanced:** {best_balanced.name}")

        lines.append("")

        # Detailed results
        lines.append("## Detailed Results")
        for sid, result in self.results.items():
            lines.append(f"\n### {result.scenario_name}")
            lines.append(f"- **Cost:** ${result.total_cost:,.0f} ({result.comparison_to_base['cost_change_pct']:+.1f}%)")
            lines.append(f"- **Duration:** {result.total_duration} days ({result.comparison_to_base['duration_change_days']:+.0f})")
            lines.append(f"- **Risk Score:** {result.risk_score:.0f}/100")

            if result.warnings:
                lines.append("- **Warnings:**")
                for w in result.warnings:
                    lines.append(f"  - ⚠️ {w}")

        return "\n".join(lines)
```

## Quick Start

```python
# Define base project
base_project = {
    'name': 'Office Building',
    'base_cost': 5000000,
    'base_duration': 365,
    'gross_area': 50000
}

# Initialize planner
planner = ConstructionScenarioPlanner(base_project)

# Create scenarios
baseline = planner.create_scenario(
    "Baseline",
    "Standard approach with default parameters",
    {}
)

accelerated = planner.create_scenario(
    "Accelerated Schedule",
    "Faster completion with overtime and larger crew",
    {
        'overtime_percentage': 25,
        'crew_size': 15,
        'work_days_per_week': 6
    }
)

cost_optimized = planner.create_scenario(
    "Cost Optimized",
    "Lower cost with reduced contingency and smaller crew",
    {
        'contingency_percentage': 7,
        'crew_size': 8,
        'subcontractor_markup': 12
    }
)

# Evaluate all scenarios
for scenario in planner.scenarios.values():
    result = planner.evaluate_scenario(scenario)
    print(f"{result.scenario_name}: ${result.total_cost:,.0f}, {result.total_duration} days")

# Compare scenarios
comparison = planner.compare_scenarios()
print(comparison)

# Run sensitivity analysis
sensitivity = planner.run_sensitivity_analysis('material_escalation')
print(f"Material escalation sensitivity: {sensitivity.sensitivity_score:.1f}")

# Generate report
report = planner.generate_report()
print(report)
```

## Dependencies

```bash
pip install pandas numpy
```
