---
name: scenario-planning
description: When the user wants to analyze supply chain scenarios, perform risk analysis, evaluate what-if scenarios, or build contingency plans. Also use when the user mentions "scenario analysis," "what-if planning," "risk scenarios," "contingency planning," "monte carlo simulation," "sensitivity analysis," "stress testing," or "disruption planning." For demand uncertainty, see demand-forecasting. For S&OP scenario integration, see sales-operations-planning.
---

# Scenario Planning

You are an expert in supply chain scenario planning and risk analysis. Your goal is to help organizations evaluate alternative futures, assess risks, develop contingency plans, and make robust decisions under uncertainty.

## Initial Assessment

Before building scenario plans, understand:

1. **Planning Context**
   - What decisions need to be made?
   - What uncertainties or risks are most concerning?
   - Planning horizon? (short-term tactical vs. long-term strategic)
   - Current planning process and tools?

2. **Business Environment**
   - Key market uncertainties? (demand, supply, pricing)
   - External risks? (geopolitical, natural disasters, economic)
   - Internal vulnerabilities? (single-source suppliers, capacity constraints)
   - Historical disruptions experienced?

3. **Scope & Objectives**
   - What part of supply chain? (end-to-end, specific segment)
   - Quantitative analysis or qualitative scenarios?
   - One-time analysis or ongoing process?
   - Decision context? (investment, strategy, operations)

4. **Data & Resources**
   - Historical variability data available?
   - Cost and performance data?
   - Risk databases or incident logs?
   - Modeling tools and capabilities?

---

## Scenario Planning Framework

### Types of Scenario Analysis

**1. Sensitivity Analysis**
- Test impact of single variable changes
- "What if demand increases by 10%?"
- Simple, quick insights
- Foundation for deeper analysis

**2. What-If Scenarios**
- Specific event-based scenarios
- "What if supplier X fails?"
- Defined discrete events
- Test preparedness

**3. Monte Carlo Simulation**
- Probabilistic analysis with random sampling
- Thousands of scenarios
- Generate probability distributions
- Risk quantification

**4. Strategic Scenarios**
- Long-term alternative futures
- Multiple variables changing together
- Qualitative + quantitative
- 3-5 year horizons

**5. Stress Testing**
- Extreme event scenarios
- Test system resilience
- Identify breaking points
- Regulatory or internal requirements

---

## Scenario Development Process

### Phase 1: Define Scope & Objectives

**Key Questions:**
- What decision is being supported?
- What are we trying to learn?
- What time horizon matters?
- Who needs to use the analysis?

**Output:** Clear problem statement and success criteria

### Phase 2: Identify Key Uncertainties

**External Uncertainties:**
- **Demand volatility**: Market changes, customer behavior
- **Supply disruptions**: Supplier failures, natural disasters
- **Cost volatility**: Raw materials, transportation, labor
- **Regulatory changes**: Trade policies, environmental rules
- **Technology disruption**: New competitors, obsolescence
- **Economic conditions**: Recession, inflation, currency

**Internal Uncertainties:**
- Production yields and quality
- Equipment reliability
- Workforce availability
- IT system performance
- New product launch success

**Prioritization Matrix:**

```python
import pandas as pd
import matplotlib.pyplot as plt

def prioritize_uncertainties(uncertainties_data):
    """
    Prioritize uncertainties by impact and likelihood

    Parameters:
    - uncertainties_data: list of dicts with 'name', 'impact', 'likelihood'
    """
    df = pd.DataFrame(uncertainties_data)

    # Calculate priority score
    df['priority_score'] = df['impact'] * df['likelihood']
    df = df.sort_values('priority_score', ascending=False)

    # Plot impact-likelihood matrix
    plt.figure(figsize=(10, 8))
    plt.scatter(df['likelihood'], df['impact'], s=200, alpha=0.6)

    for idx, row in df.iterrows():
        plt.annotate(row['name'],
                    (row['likelihood'], row['impact']),
                    fontsize=8)

    plt.xlabel('Likelihood (1-10)')
    plt.ylabel('Business Impact (1-10)')
    plt.title('Uncertainty Prioritization Matrix')
    plt.grid(True, alpha=0.3)

    # Add quadrant lines
    plt.axhline(y=5, color='r', linestyle='--', alpha=0.3)
    plt.axvline(x=5, color='r', linestyle='--', alpha=0.3)

    return df

# Example usage
uncertainties = [
    {'name': 'Supplier Bankruptcy', 'impact': 9, 'likelihood': 3},
    {'name': 'Demand Spike', 'impact': 7, 'likelihood': 6},
    {'name': 'Port Strike', 'impact': 8, 'likelihood': 4},
    {'name': 'Fuel Price Increase', 'impact': 6, 'likelihood': 7},
    {'name': 'Quality Issue', 'impact': 7, 'likelihood': 5}
]

priority_df = prioritize_uncertainties(uncertainties)
```

### Phase 3: Define Scenarios

**Approaches:**

**A. Driver-Based Scenarios**
- Select 2-3 key uncertain drivers
- Define high/low states for each
- Creates 2x2 or 2x2x2 scenario matrix

**Example: Demand Growth vs. Supply Stability**

|                    | Low Demand Growth | High Demand Growth |
|--------------------|-------------------|-------------------|
| **Stable Supply**  | Optimization      | Capacity Expansion |
| **Unstable Supply**| Consolidation     | High Risk/Reward   |

**B. Event-Based Scenarios**
- Specific disruptive events
- Examples: Hurricane, cyber attack, supplier bankruptcy
- Detailed impact modeling

**C. Monte Carlo Scenarios**
- Statistical distributions for uncertain variables
- Random sampling
- Large number of scenarios (1000+)

### Phase 4: Model Scenarios

**Build Base Model:**
```python
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SupplyChainState:
    """Represents supply chain configuration"""
    facilities: List[str]
    suppliers: Dict[str, float]  # supplier: reliability
    inventory_levels: Dict[str, float]  # location: units
    capacity: Dict[str, float]  # facility: units/month
    costs: Dict[str, float]

class ScenarioModel:
    """Supply chain scenario modeling"""

    def __init__(self, base_state: SupplyChainState):
        self.base_state = base_state
        self.scenarios = {}

    def add_scenario(self, name: str, changes: Dict):
        """Define a scenario with changes from base"""
        self.scenarios[name] = changes

    def evaluate_scenario(self, scenario_name: str,
                         demand: np.ndarray,
                         time_periods: int = 12) -> Dict:
        """
        Simulate supply chain performance under scenario

        Returns metrics: cost, service level, inventory
        """

        scenario_changes = self.scenarios[scenario_name]

        # Apply scenario changes to base state
        state = self._apply_changes(self.base_state, scenario_changes)

        # Simulate over time periods
        results = {
            'total_cost': 0,
            'service_level': [],
            'inventory': [],
            'stockouts': 0,
            'periods': []
        }

        inventory = state.inventory_levels.copy()

        for t in range(time_periods):
            period_demand = demand[t]

            # Check if can meet demand
            total_inventory = sum(inventory.values())

            if total_inventory >= period_demand:
                # Meet demand
                service = 1.0
                stockout = 0
                units_sold = period_demand
            else:
                # Stockout
                service = total_inventory / period_demand
                stockout = period_demand - total_inventory
                units_sold = total_inventory

            # Calculate costs
            holding_cost = sum(inventory.values()) * state.costs.get('holding', 1.0)
            stockout_cost = stockout * state.costs.get('stockout', 100.0)
            period_cost = holding_cost + stockout_cost

            # Production/replenishment
            production = min(
                period_demand * 1.2,  # Target 120% of demand
                sum(state.capacity.values())
            )

            # Apply supply reliability
            actual_production = production * scenario_changes.get('supply_reliability', 1.0)

            # Update inventory
            for loc in inventory:
                inventory[loc] = max(0, inventory[loc] - units_sold / len(inventory))
                inventory[loc] += actual_production / len(inventory)

            # Record results
            results['total_cost'] += period_cost
            results['service_level'].append(service)
            results['inventory'].append(sum(inventory.values()))
            results['stockouts'] += stockout
            results['periods'].append(t)

        # Calculate summary metrics
        results['avg_service_level'] = np.mean(results['service_level'])
        results['avg_inventory'] = np.mean(results['inventory'])
        results['total_stockouts'] = results['stockouts']

        return results

    def _apply_changes(self, base_state, changes):
        """Apply scenario changes to base state"""
        import copy
        state = copy.deepcopy(base_state)

        # Apply modifications based on scenario
        if 'capacity_reduction' in changes:
            for facility in state.capacity:
                state.capacity[facility] *= (1 - changes['capacity_reduction'])

        if 'cost_increase' in changes:
            for cost_type in state.costs:
                state.costs[cost_type] *= (1 + changes['cost_increase'])

        return state

    def compare_scenarios(self, demand: np.ndarray) -> pd.DataFrame:
        """Compare all scenarios"""

        results_list = []

        for scenario_name in self.scenarios:
            result = self.evaluate_scenario(scenario_name, demand)
            results_list.append({
                'Scenario': scenario_name,
                'Total_Cost': result['total_cost'],
                'Avg_Service_Level': result['avg_service_level'] * 100,
                'Avg_Inventory': result['avg_inventory'],
                'Total_Stockouts': result['total_stockouts']
            })

        return pd.DataFrame(results_list)

# Example usage
base = SupplyChainState(
    facilities=['DC_East', 'DC_West'],
    suppliers={'Supplier_A': 0.95, 'Supplier_B': 0.98},
    inventory_levels={'DC_East': 5000, 'DC_West': 5000},
    capacity={'DC_East': 4000, 'DC_West': 4000},
    costs={'holding': 2.0, 'stockout': 150.0}
)

model = ScenarioModel(base)

# Define scenarios
model.add_scenario('Base_Case', {
    'supply_reliability': 1.0,
    'capacity_reduction': 0.0,
    'cost_increase': 0.0
})

model.add_scenario('Supplier_Disruption', {
    'supply_reliability': 0.6,
    'capacity_reduction': 0.0,
    'cost_increase': 0.0
})

model.add_scenario('Capacity_Constraint', {
    'supply_reliability': 1.0,
    'capacity_reduction': 0.3,
    'cost_increase': 0.0
})

model.add_scenario('Cost_Inflation', {
    'supply_reliability': 1.0,
    'capacity_reduction': 0.0,
    'cost_increase': 0.25
})

model.add_scenario('Perfect_Storm', {
    'supply_reliability': 0.7,
    'capacity_reduction': 0.2,
    'cost_increase': 0.3
})

# Generate demand scenarios
np.random.seed(42)
demand = np.random.normal(8000, 1000, 12)  # 12 months

# Compare scenarios
comparison = model.compare_scenarios(demand)
print(comparison)
```

---

## Monte Carlo Simulation

### Probabilistic Scenario Analysis

**When to Use:**
- Multiple uncertain variables
- Need probability distributions, not point estimates
- Risk quantification required
- Portfolio or investment decisions

**Process:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

class MonteCarloScenarioAnalysis:
    """Monte Carlo simulation for supply chain scenarios"""

    def __init__(self, n_simulations=1000):
        self.n_simulations = n_simulations
        self.results = None

    def simulate_supply_chain(self,
                             demand_params: Dict,
                             cost_params: Dict,
                             supply_params: Dict,
                             periods: int = 12):
        """
        Run Monte Carlo simulation

        Parameters:
        - demand_params: {'mean': x, 'std': y, 'distribution': 'normal'}
        - cost_params: {'transport': {...}, 'holding': {...}}
        - supply_params: {'reliability': {...}}
        """

        results = []

        for sim in range(self.n_simulations):
            # Generate random demand
            if demand_params['distribution'] == 'normal':
                demand = np.random.normal(
                    demand_params['mean'],
                    demand_params['std'],
                    periods
                )
            elif demand_params['distribution'] == 'lognormal':
                demand = np.random.lognormal(
                    np.log(demand_params['mean']),
                    demand_params['std'],
                    periods
                )

            # Generate random costs
            transport_cost = np.random.uniform(
                cost_params['transport']['min'],
                cost_params['transport']['max']
            )

            holding_cost = np.random.normal(
                cost_params['holding']['mean'],
                cost_params['holding']['std']
            )

            # Generate supply reliability
            supply_reliability = np.random.beta(
                supply_params['reliability']['alpha'],
                supply_params['reliability']['beta']
            )

            # Simulate supply chain performance
            total_demand = demand.sum()
            actual_supply = total_demand * supply_reliability
            shortage = max(0, total_demand - actual_supply)

            # Calculate total cost
            transport_cost_total = actual_supply * transport_cost
            holding_cost_total = actual_supply * holding_cost * 0.1
            shortage_cost_total = shortage * 200  # Penalty

            total_cost = (transport_cost_total +
                         holding_cost_total +
                         shortage_cost_total)

            service_level = (actual_supply / total_demand) * 100

            results.append({
                'simulation': sim,
                'total_demand': total_demand,
                'actual_supply': actual_supply,
                'shortage': shortage,
                'transport_cost': transport_cost_total,
                'holding_cost': holding_cost_total,
                'shortage_cost': shortage_cost_total,
                'total_cost': total_cost,
                'service_level': service_level
            })

        self.results = pd.DataFrame(results)
        return self.results

    def analyze_results(self):
        """Statistical analysis of simulation results"""

        if self.results is None:
            raise ValueError("Run simulation first")

        analysis = {
            'total_cost': {
                'mean': self.results['total_cost'].mean(),
                'std': self.results['total_cost'].std(),
                'p10': self.results['total_cost'].quantile(0.10),
                'p50': self.results['total_cost'].quantile(0.50),
                'p90': self.results['total_cost'].quantile(0.90),
                'p95': self.results['total_cost'].quantile(0.95),
                'min': self.results['total_cost'].min(),
                'max': self.results['total_cost'].max()
            },
            'service_level': {
                'mean': self.results['service_level'].mean(),
                'std': self.results['service_level'].std(),
                'p10': self.results['service_level'].quantile(0.10),
                'p50': self.results['service_level'].quantile(0.50),
                'p90': self.results['service_level'].quantile(0.90)
            }
        }

        return analysis

    def value_at_risk(self, confidence_level=0.95):
        """Calculate Value at Risk (VaR) for costs"""

        if self.results is None:
            raise ValueError("Run simulation first")

        var = self.results['total_cost'].quantile(confidence_level)

        # Conditional VaR (CVaR) - expected loss beyond VaR
        cvar = self.results[
            self.results['total_cost'] >= var
        ]['total_cost'].mean()

        return {'VaR': var, 'CVaR': cvar}

    def plot_distributions(self):
        """Visualize simulation results"""

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Total cost distribution
        axes[0, 0].hist(self.results['total_cost'], bins=50,
                       edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Total Cost Distribution')
        axes[0, 0].set_xlabel('Total Cost ($)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(self.results['total_cost'].mean(),
                          color='r', linestyle='--', label='Mean')
        axes[0, 0].legend()

        # Service level distribution
        axes[0, 1].hist(self.results['service_level'], bins=50,
                       edgecolor='black', alpha=0.7, color='green')
        axes[0, 1].set_title('Service Level Distribution')
        axes[0, 1].set_xlabel('Service Level (%)')
        axes[0, 1].set_ylabel('Frequency')

        # Shortage distribution
        axes[1, 0].hist(self.results['shortage'], bins=50,
                       edgecolor='black', alpha=0.7, color='orange')
        axes[1, 0].set_title('Shortage Distribution')
        axes[1, 0].set_xlabel('Shortage Units')
        axes[1, 0].set_ylabel('Frequency')

        # Cost components
        cost_components = self.results[[
            'transport_cost', 'holding_cost', 'shortage_cost'
        ]].mean()
        axes[1, 1].bar(cost_components.index, cost_components.values)
        axes[1, 1].set_title('Average Cost Components')
        axes[1, 1].set_ylabel('Cost ($)')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig

# Example usage
mc = MonteCarloScenarioAnalysis(n_simulations=10000)

demand_params = {
    'mean': 10000,
    'std': 2000,
    'distribution': 'normal'
}

cost_params = {
    'transport': {'min': 2.0, 'max': 4.0},
    'holding': {'mean': 1.5, 'std': 0.3}
}

supply_params = {
    'reliability': {'alpha': 9, 'beta': 1}  # Beta distribution
}

results = mc.simulate_supply_chain(
    demand_params, cost_params, supply_params, periods=12
)

# Analyze
analysis = mc.analyze_results()
print("Cost Analysis:")
print(f"  Mean: ${analysis['total_cost']['mean']:,.0f}")
print(f"  Std Dev: ${analysis['total_cost']['std']:,.0f}")
print(f"  P95: ${analysis['total_cost']['p95']:,.0f}")

var_metrics = mc.value_at_risk(0.95)
print(f"\nValue at Risk (95%): ${var_metrics['VaR']:,.0f}")
print(f"Conditional VaR: ${var_metrics['CVaR']:,.0f}")

# Plot
mc.plot_distributions()
```

---

## Sensitivity Analysis

### One-Way Sensitivity

**Test single variable impact:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sensitivity_analysis(base_model, variable_name,
                        test_range, other_params):
    """
    Perform one-way sensitivity analysis

    Parameters:
    - base_model: function that returns metric given parameters
    - variable_name: name of variable to test
    - test_range: array of values to test
    - other_params: dict of fixed parameters
    """

    results = []

    for value in test_range:
        # Update parameter
        params = other_params.copy()
        params[variable_name] = value

        # Evaluate model
        metric = base_model(**params)

        results.append({
            variable_name: value,
            'metric': metric
        })

    return pd.DataFrame(results)

# Example: Test demand sensitivity
def calculate_cost(demand, unit_cost, holding_rate, capacity):
    """Simple cost model"""
    production = min(demand, capacity)
    shortage = max(0, demand - capacity)

    production_cost = production * unit_cost
    holding_cost = production * holding_rate * 0.5
    shortage_cost = shortage * unit_cost * 3  # 3x penalty

    return production_cost + holding_cost + shortage_cost

# Test demand scenarios
demand_range = np.linspace(5000, 15000, 20)

other_params = {
    'unit_cost': 10,
    'holding_rate': 0.2,
    'capacity': 10000
}

demand_sensitivity = sensitivity_analysis(
    calculate_cost,
    'demand',
    demand_range,
    other_params
)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(demand_sensitivity['demand'],
         demand_sensitivity['metric'],
         marker='o', linewidth=2)
plt.xlabel('Demand (units)')
plt.ylabel('Total Cost ($)')
plt.title('Sensitivity to Demand Changes')
plt.grid(True, alpha=0.3)
plt.axvline(x=10000, color='r', linestyle='--', label='Capacity Limit')
plt.legend()
plt.show()
```

### Multi-Way Sensitivity (Tornado Diagram)

**Compare impact of multiple variables:**

```python
def tornado_analysis(base_model, variables, ranges, base_params):
    """
    Create tornado diagram showing sensitivity to multiple variables

    Parameters:
    - base_model: function to evaluate
    - variables: list of variable names
    - ranges: dict {variable: (low, high)}
    - base_params: base case parameters
    """

    # Calculate base case
    base_result = base_model(**base_params)

    results = []

    for var in variables:
        # Test low value
        params_low = base_params.copy()
        params_low[var] = ranges[var][0]
        result_low = base_model(**params_low)

        # Test high value
        params_high = base_params.copy()
        params_high[var] = ranges[var][1]
        result_high = base_model(**params_high)

        # Calculate swing
        swing = abs(result_high - result_low)

        results.append({
            'variable': var,
            'low_value': ranges[var][0],
            'high_value': ranges[var][1],
            'result_low': result_low,
            'result_high': result_high,
            'swing': swing,
            'impact_pct': (swing / base_result) * 100
        })

    df = pd.DataFrame(results)
    df = df.sort_values('swing', ascending=True)

    # Plot tornado diagram
    fig, ax = plt.subplots(figsize=(10, 8))

    y_pos = np.arange(len(df))

    for i, row in df.iterrows():
        low = row['result_low']
        high = row['result_high']

        ax.barh(row['variable'], high - base_result,
                left=base_result, color='red', alpha=0.6)
        ax.barh(row['variable'], base_result - low,
                left=low, color='blue', alpha=0.6)

    ax.axvline(x=base_result, color='black', linestyle='--', linewidth=2)
    ax.set_xlabel('Total Cost ($)')
    ax.set_title('Tornado Diagram - Sensitivity Analysis')
    ax.grid(True, alpha=0.3, axis='x')

    return df, fig

# Example usage
variables = ['demand', 'unit_cost', 'holding_rate']

ranges = {
    'demand': (8000, 12000),
    'unit_cost': (8, 12),
    'holding_rate': (0.15, 0.25)
}

base_params = {
    'demand': 10000,
    'unit_cost': 10,
    'holding_rate': 0.2,
    'capacity': 10000
}

tornado_df, fig = tornado_analysis(
    calculate_cost, variables, ranges, base_params
)
```

---

## Risk Assessment & Quantification

### Risk Probability-Impact Matrix

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RiskAssessment:
    """Supply chain risk assessment framework"""

    def __init__(self):
        self.risks = []

    def add_risk(self, name, category, probability, impact,
                detection_difficulty, mitigation_cost):
        """
        Add a risk to the register

        Parameters:
        - probability: 1-5 scale (1=very low, 5=very high)
        - impact: 1-5 scale (1=minimal, 5=catastrophic)
        - detection_difficulty: 1-5 (1=easy to detect, 5=hard)
        - mitigation_cost: 1-5 (1=low cost, 5=high cost)
        """

        risk = {
            'name': name,
            'category': category,
            'probability': probability,
            'impact': impact,
            'detection': detection_difficulty,
            'mitigation_cost': mitigation_cost,
            'risk_score': probability * impact,
            'risk_priority_number': probability * impact * detection_difficulty
        }

        self.risks.append(risk)

    def get_risk_register(self):
        """Return risk register as DataFrame"""
        df = pd.DataFrame(self.risks)
        df = df.sort_values('risk_score', ascending=False)
        return df

    def plot_risk_matrix(self):
        """Plot probability-impact matrix"""

        df = pd.DataFrame(self.risks)

        fig, ax = plt.subplots(figsize=(12, 10))

        # Color by risk score
        scatter = ax.scatter(df['probability'], df['impact'],
                           s=df['risk_score'] * 50,
                           c=df['risk_score'],
                           cmap='RdYlGn_r',
                           alpha=0.6,
                           edgecolors='black',
                           linewidth=1.5)

        # Annotate risks
        for idx, row in df.iterrows():
            ax.annotate(row['name'],
                       (row['probability'], row['impact']),
                       fontsize=8,
                       xytext=(5, 5),
                       textcoords='offset points')

        ax.set_xlabel('Probability (1-5)', fontsize=12)
        ax.set_ylabel('Impact (1-5)', fontsize=12)
        ax.set_title('Supply Chain Risk Matrix', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Add risk zones
        ax.axhline(y=3, color='orange', linestyle='--', alpha=0.3, linewidth=2)
        ax.axvline(x=3, color='orange', linestyle='--', alpha=0.3, linewidth=2)

        # Add text labels for zones
        ax.text(1.2, 4.5, 'Low Prob\nHigh Impact', fontsize=9, alpha=0.5)
        ax.text(4.2, 4.5, 'HIGH RISK', fontsize=11, fontweight='bold',
               color='red', alpha=0.7)
        ax.text(4.2, 1.5, 'High Prob\nLow Impact', fontsize=9, alpha=0.5)
        ax.text(1.2, 1.5, 'LOW RISK', fontsize=10, alpha=0.5)

        plt.colorbar(scatter, label='Risk Score')

        return fig

    def prioritize_risks(self, min_score=10):
        """Return high-priority risks"""
        df = self.get_risk_register()
        return df[df['risk_score'] >= min_score]

# Example usage
risk_assessment = RiskAssessment()

# Add supply chain risks
risk_assessment.add_risk(
    name='Single Source Supplier',
    category='Supply',
    probability=3,
    impact=5,
    detection_difficulty=2,
    mitigation_cost=4
)

risk_assessment.add_risk(
    name='Port Congestion',
    category='Logistics',
    probability=4,
    impact=3,
    detection_difficulty=1,
    mitigation_cost=2
)

risk_assessment.add_risk(
    name='Demand Forecast Error',
    category='Demand',
    probability=5,
    impact=3,
    detection_difficulty=2,
    mitigation_cost=3
)

risk_assessment.add_risk(
    name='Natural Disaster',
    category='External',
    probability=2,
    impact=5,
    detection_difficulty=1,
    mitigation_cost=5
)

risk_assessment.add_risk(
    name='Cyber Attack',
    category='Technology',
    probability=3,
    impact=4,
    detection_difficulty=4,
    mitigation_cost=4
)

risk_assessment.add_risk(
    name='Quality Defect',
    category='Operations',
    probability=4,
    impact=4,
    detection_difficulty=3,
    mitigation_cost=3
)

# Get risk register
risk_register = risk_assessment.get_risk_register()
print("\nTop Risks:")
print(risk_register[['name', 'category', 'risk_score',
                     'risk_priority_number']].head(10))

# Plot
risk_assessment.plot_risk_matrix()

# High priority risks
high_risks = risk_assessment.prioritize_risks(min_score=12)
print(f"\nHigh Priority Risks (score >= 12): {len(high_risks)}")
```

---

## Strategic Scenario Development

### Shell Scenario Planning Method

**For Long-Term Strategic Planning:**

**Step 1: Define Focal Question**
- "What supply chain strategy will be most resilient over next 5 years?"

**Step 2: Identify Key Forces**
- Predetermined elements (trends, demographics)
- Critical uncertainties (regulations, technology adoption)

**Step 3: Select Scenario Dimensions**
- Choose 2 most important/uncertain drivers
- Create 2x2 matrix

**Step 4: Develop Scenario Narratives**
- Create compelling stories for each quadrant
- Name scenarios descriptively
- Detail implications

**Step 5: Identify Implications & Strategies**
- What strategies work in all scenarios? (robust)
- What strategies are scenario-dependent? (contingent)
- Early warning indicators?

**Example: Global Trade Scenarios**

**Dimensions:**
- Economic Integration (High/Low)
- Environmental Regulation (Strict/Relaxed)

**Four Scenarios:**

1. **"Global Efficiency"** (High Integration, Relaxed Regulations)
   - Optimized global networks
   - Lowest cost production
   - Long supply chains
   - Limited regionalization

2. **"Green Global"** (High Integration, Strict Regulations)
   - Carbon-neutral logistics
   - Sustainable sourcing priority
   - Green technology investments
   - Higher costs, strong compliance

3. **"Regional Resilience"** (Low Integration, Strict Regulations)
   - Near-shoring/friend-shoring
   - Regional supply chains
   - Emphasis on reliability
   - Moderate costs

4. **"Fragmented World"** (Low Integration, Relaxed Regulations)
   - Trade barriers
   - Country-specific strategies
   - Duplicated infrastructure
   - High inefficiency

---

## Contingency Planning

### Business Continuity Plans

**Key Components:**

1. **Risk Identification**
   - What can go wrong?
   - Likelihood and impact

2. **Impact Analysis**
   - Revenue impact
   - Customer impact
   - Recovery time objectives (RTO)
   - Recovery point objectives (RPO)

3. **Response Strategies**
   - Immediate actions (0-24 hours)
   - Short-term (1-7 days)
   - Medium-term (1-4 weeks)
   - Long-term recovery

4. **Resource Requirements**
   - People, systems, facilities
   - Backup suppliers
   - Inventory buffers
   - Financial reserves

**Contingency Plan Template:**

```python
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class ContingencyAction:
    """Single action in contingency plan"""
    action_id: str
    description: str
    trigger: str
    responsible_party: str
    timeline: str  # "Immediate", "24 hours", "Week 1", etc.
    resources_needed: List[str]
    cost_estimate: float
    dependencies: List[str]

@dataclass
class ContingencyPlan:
    """Complete contingency plan for a risk scenario"""
    risk_name: str
    risk_category: str
    trigger_conditions: List[str]
    severity_level: str  # "Low", "Medium", "High", "Critical"
    actions: List[ContingencyAction]
    communication_plan: Dict
    escalation_procedure: List[str]

    def get_immediate_actions(self):
        """Return actions needed immediately"""
        return [a for a in self.actions if a.timeline == "Immediate"]

    def get_actions_by_timeline(self, timeline: str):
        """Get actions for specific timeline"""
        return [a for a in self.actions if a.timeline == timeline]

    def estimate_total_cost(self):
        """Calculate total cost of plan execution"""
        return sum(a.cost_estimate for a in self.actions)

# Example: Supplier Disruption Contingency Plan
supplier_disruption_plan = ContingencyPlan(
    risk_name="Primary Supplier Disruption",
    risk_category="Supply Risk",
    trigger_conditions=[
        "Supplier bankruptcy filing",
        "Natural disaster at supplier location",
        "Quality issues requiring supplier shutdown",
        "Supply < 50% of normal for > 3 days"
    ],
    severity_level="High",
    actions=[
        ContingencyAction(
            action_id="SD-001",
            description="Activate backup supplier contracts",
            trigger="Confirmed disruption > 24 hours",
            responsible_party="Procurement Director",
            timeline="Immediate",
            resources_needed=["Backup supplier contact list", "Expedited PO"],
            cost_estimate=50000,
            dependencies=[]
        ),
        ContingencyAction(
            action_id="SD-002",
            description="Increase safety stock from alternative sources",
            trigger="Expected disruption > 1 week",
            responsible_party="Supply Chain Manager",
            timeline="24 hours",
            resources_needed=["Emergency budget authorization", "Warehouse space"],
            cost_estimate=200000,
            dependencies=["SD-001"]
        ),
        ContingencyAction(
            action_id="SD-003",
            description="Implement product rationing to priority customers",
            trigger="Inventory below critical level",
            responsible_party="Customer Service VP",
            timeline="48 hours",
            resources_needed=["Customer priority list", "Communication templates"],
            cost_estimate=0,
            dependencies=["SD-002"]
        ),
        ContingencyAction(
            action_id="SD-004",
            description="Qualify and onboard new supplier",
            trigger="Expected disruption > 30 days",
            responsible_party="Procurement Director",
            timeline="Week 2-4",
            resources_needed=["Supplier qualification team", "Quality testing"],
            cost_estimate=150000,
            dependencies=["SD-001", "SD-002"]
        )
    ],
    communication_plan={
        "internal": ["Executive team notification within 2 hours",
                    "Daily status updates to stakeholders"],
        "external": ["Customer notification within 24 hours if impact expected",
                    "Supplier engagement for resolution timeline"],
        "escalation": ["CFO if cost > $500K", "CEO if duration > 4 weeks"]
    },
    escalation_procedure=[
        "Level 1: Supply Chain Manager (0-24 hours)",
        "Level 2: VP Operations (24-72 hours)",
        "Level 3: COO (> 72 hours or impact > $1M)",
        "Level 4: CEO (Critical customer impact or > $5M)"
    ]
)

# Display immediate actions
print("IMMEDIATE ACTIONS:")
for action in supplier_disruption_plan.get_immediate_actions():
    print(f"  [{action.action_id}] {action.description}")
    print(f"      Owner: {action.responsible_party}")
    print(f"      Cost: ${action.cost_estimate:,}")

print(f"\nTotal Plan Cost: ${supplier_disruption_plan.estimate_total_cost():,}")
```

---

## Tools & Libraries

### Python Libraries

**Simulation & Modeling:**
- `simpy`: Discrete-event simulation
- `scipy.stats`: Statistical distributions
- `numpy`: Random number generation, arrays
- `pandas`: Data manipulation and analysis

**Optimization Under Uncertainty:**
- `pyomo`: Stochastic programming
- `pulp`: Linear programming with scenarios
- `mip`: Mixed-integer programming

**Visualization:**
- `matplotlib`, `seaborn`: Statistical plots
- `plotly`: Interactive dashboards
- `networkx`: Network diagrams

**Risk Analysis:**
- `risktools`: Risk metrics and VaR
- `copulas`: Dependency modeling

### Commercial Software

**Scenario Planning Platforms:**
- **Kinaxis RapidResponse**: Scenario analysis and collaboration
- **o9 Solutions**: AI-driven scenario planning
- **LLamasoft**: Supply chain scenario modeling
- **Blue Yonder**: What-if analysis

**Risk Management:**
- **Resilinc**: Supply chain risk intelligence
- **Everstream Analytics**: Predictive risk analytics
- **Riskmethods**: Risk monitoring and assessment

**Simulation:**
- **AnyLogic**: Multi-method simulation
- **Arena**: Discrete-event simulation
- **Simio**: 3D simulation modeling
- **FlexSim**: 3D simulation

---

## Common Challenges & Solutions

### Challenge: Too Many Scenarios

**Problem:**
- Analysis paralysis
- Overwhelming number of combinations
- Can't make decisions

**Solutions:**
- Focus on 3-5 key scenarios
- Use scenario reduction techniques
- Group similar scenarios
- Prioritize by probability × impact
- Start with base/best/worst cases

### Challenge: Lack of Data

**Problem:**
- No historical disruption data
- Difficult to estimate probabilities
- Uncertainty about impacts

**Solutions:**
- Use expert judgment (Delphi method)
- Industry benchmarks and case studies
- Start with ranges instead of points
- Sensitivity analysis to understand drivers
- Learn and update as events occur

### Challenge: Scenario Bias

**Problem:**
- Anchoring to current state
- Ignoring low-probability high-impact events
- Confirmation bias in scenario selection

**Solutions:**
- Include diverse perspectives
- Use structured methods (Shell approach)
- Challenge assumptions explicitly
- Include "black swan" scenarios
- Independent facilitation

### Challenge: Actionability

**Problem:**
- Scenarios don't lead to decisions
- Analysis doesn't translate to strategy
- Lack of clear next steps

**Solutions:**
- Link scenarios to specific decisions
- Identify "no regret" moves (work in all scenarios)
- Define trigger points and early warnings
- Create contingency plans for each scenario
- Regular review and update process

### Challenge: Complexity vs. Usability

**Problem:**
- Models too complex for stakeholders
- Can't explain results
- Black box simulations

**Solutions:**
- Start simple, add complexity as needed
- Visual dashboards and summaries
- Clear documentation of assumptions
- Sensitivity analysis to show key drivers
- Scenario narratives, not just numbers

---

## Output Format

### Scenario Analysis Report

**Executive Summary:**
- Purpose and scope of analysis
- Key scenarios evaluated
- Critical findings and recommendations
- Decision implications

**Scenario Definitions:**

| Scenario Name | Description | Key Assumptions | Probability |
|--------------|-------------|-----------------|-------------|
| Base Case | Most likely future | Current trends continue | 50% |
| High Growth | Demand surge | Economic boom, new markets | 20% |
| Supply Disruption | Major supplier failure | Single-source risk realizes | 15% |
| Perfect Storm | Multiple issues | Demand spike + supply shortage | 10% |
| Cost Inflation | Rising costs | Fuel, labor, materials up 30% | 25% |

**Scenario Results:**

| Scenario | Total Cost | Service Level | Inventory | Key Metrics |
|----------|-----------|---------------|-----------|-------------|
| Base Case | $25M | 95% | 8,000 units | Baseline |
| High Growth | $32M | 87% | 12,000 units | Capacity constrained |
| Supply Disruption | $38M | 78% | 5,000 units | High stockout costs |
| Perfect Storm | $45M | 65% | 7,000 units | Crisis mode |
| Cost Inflation | $31M | 93% | 8,000 units | Margin pressure |

**Risk Assessment:**
- High-priority risks identified
- Risk mitigation strategies
- Contingency plans for top scenarios
- Early warning indicators

**Recommendations:**

1. **Immediate Actions** (0-3 months)
   - Qualify backup suppliers for top 10 components
   - Increase safety stock for critical items
   - Implement demand sensing for early warning

2. **Short-Term Initiatives** (3-12 months)
   - Diversify supplier base
   - Add flexible capacity options
   - Enhance scenario planning capability

3. **Strategic Investments** (1-3 years)
   - Build regional distribution center
   - Implement control tower technology
   - Develop dual-sourcing strategy

**Monitoring & Review:**
- Key performance indicators to track
- Scenario review frequency (quarterly)
- Trigger points for plan activation
- Governance and escalation process

---

## Questions to Ask

If you need more context:
1. What decision is this scenario analysis supporting?
2. What uncertainties or risks are most concerning?
3. What's the planning horizon? (tactical vs. strategic)
4. What data is available on historical variability and disruptions?
5. Are there specific events or scenarios to model?
6. Quantitative analysis or qualitative scenarios needed?
7. Who will use the analysis and how?
8. Existing risk management or continuity plans?

---

## Related Skills

- **demand-forecasting**: For demand uncertainty analysis
- **sales-operations-planning**: For S&OP scenario integration
- **capacity-planning**: For capacity scenarios and stress testing
- **network-design**: For network strategy scenarios
- **inventory-optimization**: For inventory buffer strategies
- **risk-mitigation**: For risk response planning
- **supply-chain-analytics**: For performance monitoring
- **digital-twin-modeling**: For real-time scenario simulation
