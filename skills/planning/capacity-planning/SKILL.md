---
name: capacity-planning
description: When the user wants to plan production or distribution capacity, analyze capacity requirements, optimize resource utilization, or balance capacity with demand. Also use when the user mentions "capacity analysis," "resource planning," "bottleneck analysis," "capacity expansion," "load balancing," "throughput planning," "utilization optimization," or "capacity modeling." For production scheduling, see master-production-scheduling. For long-term network capacity, see network-design.
---

# Capacity Planning

You are an expert in capacity planning and resource optimization. Your goal is to help organizations match capacity with demand, optimize resource utilization, identify bottlenecks, and make cost-effective capacity investment decisions.

## Initial Assessment

Before developing capacity plans, understand:

1. **Planning Context**
   - What type of capacity? (production, warehouse, transportation, labor)
   - Planning horizon? (short-term loading, tactical planning, strategic investment)
   - Current capacity utilization rates?
   - Known capacity constraints or bottlenecks?

2. **Demand Profile**
   - Demand forecast and variability?
   - Seasonality patterns?
   - Growth expectations?
   - Product mix changes expected?

3. **Current State**
   - Existing capacity levels?
   - Equipment, facilities, headcount?
   - Operating schedules (shifts, days/week)?
   - Current performance (OEE, yield, throughput)?

4. **Constraints & Requirements**
   - Service level targets?
   - Budget constraints for expansion?
   - Lead times for capacity additions?
   - Union agreements or labor rules?
   - Regulatory requirements?

---

## Capacity Planning Framework

### Types of Capacity Planning

**1. Long-Term Strategic Capacity Planning**
- **Horizon**: 2-5+ years
- **Focus**: Major investments, facility additions
- **Decisions**: Build new plant? Add warehouse? Outsource?
- **Approach**: Scenario analysis, economic modeling

**2. Medium-Term Tactical Capacity Planning**
- **Horizon**: 3-18 months
- **Focus**: Adjust workforce, add equipment, modify schedules
- **Decisions**: Hire staff? Add shift? Lease equipment?
- **Approach**: Aggregate planning, linear programming

**3. Short-Term Operational Capacity Planning**
- **Horizon**: Days to weeks
- **Focus**: Load balancing, scheduling, overtime
- **Decisions**: How to allocate work? Overtime? Outsource batch?
- **Approach**: Scheduling algorithms, queuing theory

### Capacity Strategies

**Leading Strategy**
- Add capacity in anticipation of demand
- Ensures availability, avoids stockouts
- Higher costs, risk of underutilization
- Best for: Growing markets, high service requirements

**Lagging Strategy**
- Add capacity only after demand materializes
- Lower costs, minimizes waste
- Risk of lost sales, poor service
- Best for: Uncertain demand, cost-sensitive markets

**Matching Strategy**
- Closely match capacity to demand
- Balance of cost and service
- Requires flexible capacity options
- Best for: Moderate growth, predictable demand

**Cushion Strategy**
- Maintain buffer capacity above expected demand
- Handles variability and surges
- Higher fixed costs but operational flexibility
- Best for: High variability, premium service

---

## Capacity Analysis Methods

### Capacity Measurement

**Production Capacity Metrics:**

**1. Design Capacity**
- Maximum possible output under ideal conditions
- Theoretical maximum

**2. Effective Capacity**
- Capacity under normal working conditions
- Accounts for breaks, maintenance, changeovers

**3. Actual Output**
- What's currently achieved
- Reality of operations

**Key Formulas:**

```python
def calculate_capacity_metrics(design_capacity, effective_capacity, actual_output):
    """
    Calculate capacity utilization and efficiency

    Returns:
    - utilization: actual / design capacity
    - efficiency: actual / effective capacity
    """

    utilization = (actual_output / design_capacity) * 100
    efficiency = (actual_output / effective_capacity) * 100

    return {
        'utilization': utilization,
        'efficiency': efficiency,
        'design_capacity': design_capacity,
        'effective_capacity': effective_capacity,
        'actual_output': actual_output
    }

# Example
design = 10000  # units per month
effective = 8500  # accounting for maintenance, breaks
actual = 7500  # what's produced

metrics = calculate_capacity_metrics(design, effective, actual)
print(f"Utilization: {metrics['utilization']:.1f}%")  # 75%
print(f"Efficiency: {metrics['efficiency']:.1f}%")    # 88.2%
```

**Overall Equipment Effectiveness (OEE):**

```python
def calculate_oee(availability, performance, quality):
    """
    Calculate OEE (Overall Equipment Effectiveness)

    Parameters:
    - availability: uptime / planned production time
    - performance: actual output / theoretical output at 100% speed
    - quality: good units / total units produced

    World-class OEE: > 85%
    """

    oee = availability * performance * quality * 100

    return {
        'oee': oee,
        'availability': availability * 100,
        'performance': performance * 100,
        'quality': quality * 100
    }

# Example
availability = 0.90  # 90% uptime
performance = 0.85   # 85% of theoretical speed
quality = 0.95       # 95% good units

oee_metrics = calculate_oee(availability, performance, quality)
print(f"OEE: {oee_metrics['oee']:.1f}%")  # 72.7%
```

### Bottleneck Analysis

**Theory of Constraints (TOC):**

```python
import pandas as pd
import numpy as np

def identify_bottleneck(process_steps):
    """
    Identify bottleneck in production process

    Parameters:
    - process_steps: list of dicts with 'name', 'capacity_per_hour', 'hours_available'

    Returns bottleneck step and throughput
    """

    df = pd.DataFrame(process_steps)

    # Calculate total capacity per period
    df['total_capacity'] = df['capacity_per_hour'] * df['hours_available']

    # Identify bottleneck (minimum capacity)
    bottleneck_idx = df['total_capacity'].idxmin()
    bottleneck = df.loc[bottleneck_idx]

    # System throughput limited by bottleneck
    system_throughput = bottleneck['total_capacity']

    # Calculate utilization based on bottleneck
    df['utilization'] = (system_throughput / df['total_capacity']) * 100

    return {
        'bottleneck_step': bottleneck['name'],
        'system_throughput': system_throughput,
        'bottleneck_capacity': bottleneck['total_capacity'],
        'process_analysis': df
    }

# Example: Manufacturing process
process = [
    {'name': 'Cutting', 'capacity_per_hour': 100, 'hours_available': 160},
    {'name': 'Assembly', 'capacity_per_hour': 80, 'hours_available': 160},
    {'name': 'Testing', 'capacity_per_hour': 120, 'hours_available': 160},
    {'name': 'Packaging', 'capacity_per_hour': 90, 'hours_available': 160}
]

bottleneck_analysis = identify_bottleneck(process)
print(f"Bottleneck: {bottleneck_analysis['bottleneck_step']}")
print(f"System Throughput: {bottleneck_analysis['system_throughput']:,.0f} units/month")
print("\nProcess Analysis:")
print(bottleneck_analysis['process_analysis'])
```

**Drum-Buffer-Rope (DBR) Scheduling:**

```python
class DrumBufferRope:
    """
    Theory of Constraints scheduling method

    - Drum: Bottleneck sets the pace
    - Buffer: Protect bottleneck from disruptions
    - Rope: Pull mechanism to control material release
    """

    def __init__(self, bottleneck_capacity, buffer_time_days=3):
        self.bottleneck_capacity = bottleneck_capacity
        self.buffer_time = buffer_time_days

    def calculate_schedule(self, demand, lead_times):
        """
        Create production schedule based on DBR

        Parameters:
        - demand: array of daily demand
        - lead_times: dict of process step lead times
        """

        schedule = []

        for day, daily_demand in enumerate(demand):
            # Bottleneck sets the pace (DRUM)
            bottleneck_output = min(daily_demand, self.bottleneck_capacity)

            # Buffer: Start production earlier to protect bottleneck
            buffer_start_day = max(0, day - self.buffer_time)

            # Rope: Material release tied to bottleneck schedule
            material_release = bottleneck_output

            schedule.append({
                'day': day,
                'demand': daily_demand,
                'bottleneck_output': bottleneck_output,
                'buffer_start': buffer_start_day,
                'material_release': material_release
            })

        return pd.DataFrame(schedule)

# Example usage
dbr = DrumBufferRope(bottleneck_capacity=800, buffer_time_days=3)

# Daily demand for next 10 days
demand = np.array([750, 850, 800, 900, 700, 800, 950, 800, 850, 800])
lead_times = {'cutting': 1, 'assembly': 2, 'testing': 1}

schedule = dbr.calculate_schedule(demand, lead_times)
print(schedule)
```

---

## Capacity Planning Models

### Aggregate Planning (Linear Programming)

**Objective:** Minimize total costs while meeting demand

**Decision Variables:**
- Production quantity per period
- Workforce levels
- Overtime hours
- Inventory levels
- Subcontracting quantities

**Costs:**
- Regular time production
- Overtime production
- Hiring and firing
- Inventory holding
- Stockout/backorder
- Subcontracting

```python
from pulp import *
import pandas as pd
import numpy as np

def aggregate_planning(demand, costs, constraints, periods=12):
    """
    Aggregate production planning optimization

    Parameters:
    - demand: array of demand by period
    - costs: dict with cost parameters
    - constraints: dict with capacity constraints
    - periods: planning horizon

    Returns optimal plan
    """

    # Create problem
    prob = LpProblem("Aggregate_Planning", LpMinimize)

    # Decision variables
    P = LpVariable.dicts("Production", range(periods), lowBound=0)
    W = LpVariable.dicts("Workforce", range(periods), lowBound=0, cat='Integer')
    O = LpVariable.dicts("Overtime", range(periods), lowBound=0)
    I = LpVariable.dicts("Inventory", range(periods), lowBound=0)
    H = LpVariable.dicts("Hire", range(periods), lowBound=0, cat='Integer')
    F = LpVariable.dicts("Fire", range(periods), lowBound=0, cat='Integer')
    B = LpVariable.dicts("Backorder", range(periods), lowBound=0)
    S = LpVariable.dicts("Subcontract", range(periods), lowBound=0)

    # Objective function
    prob += lpSum([
        # Regular production cost
        costs['regular_cost'] * P[t] +
        # Workforce cost
        costs['labor_cost'] * W[t] +
        # Overtime cost
        costs['overtime_cost'] * O[t] +
        # Inventory holding cost
        costs['holding_cost'] * I[t] +
        # Hiring cost
        costs['hiring_cost'] * H[t] +
        # Firing cost
        costs['firing_cost'] * F[t] +
        # Backorder cost
        costs['backorder_cost'] * B[t] +
        # Subcontracting cost
        costs['subcontract_cost'] * S[t]
        for t in range(periods)
    ])

    # Constraints

    # Initial conditions
    initial_workforce = constraints['initial_workforce']
    initial_inventory = constraints['initial_inventory']

    for t in range(periods):
        # Production capacity constraint
        prob += P[t] <= W[t] * constraints['units_per_worker'], f"Capacity_{t}"

        # Overtime capacity
        prob += O[t] <= W[t] * constraints['overtime_per_worker'], f"Overtime_{t}"

        # Subcontracting capacity
        prob += S[t] <= constraints['max_subcontract'], f"Subcontract_{t}"

        # Workforce balance
        if t == 0:
            prob += W[t] == initial_workforce + H[t] - F[t], f"Workforce_{t}"
        else:
            prob += W[t] == W[t-1] + H[t] - F[t], f"Workforce_{t}"

        # Inventory balance
        if t == 0:
            prob += I[t] == initial_inventory + P[t] + O[t] + S[t] - demand[t] + B[t], f"Inventory_{t}"
        else:
            prob += I[t] == I[t-1] + P[t] + O[t] + S[t] - demand[t] + B[t] - B[t-1], f"Inventory_{t}"

        # Minimum service level (max backorder)
        prob += B[t] <= demand[t] * constraints['max_backorder_pct'], f"Service_{t}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'production': [P[t].varValue for t in range(periods)],
        'workforce': [W[t].varValue for t in range(periods)],
        'overtime': [O[t].varValue for t in range(periods)],
        'inventory': [I[t].varValue for t in range(periods)],
        'hired': [H[t].varValue for t in range(periods)],
        'fired': [F[t].varValue for t in range(periods)],
        'backorders': [B[t].varValue for t in range(periods)],
        'subcontract': [S[t].varValue for t in range(periods)]
    }

    # Create summary DataFrame
    df = pd.DataFrame({
        'Period': range(1, periods + 1),
        'Demand': demand,
        'Production': results['production'],
        'Workforce': results['workforce'],
        'Overtime': results['overtime'],
        'Inventory': results['inventory'],
        'Backorders': results['backorders'],
        'Subcontract': results['subcontract']
    })

    results['summary'] = df

    return results

# Example usage
demand = np.array([1000, 1200, 1500, 1800, 2000, 1800,
                   1600, 1400, 1300, 1200, 1100, 1000])

costs = {
    'regular_cost': 50,
    'labor_cost': 2000,      # per worker per period
    'overtime_cost': 75,
    'holding_cost': 5,
    'hiring_cost': 1000,
    'firing_cost': 1500,
    'backorder_cost': 100,
    'subcontract_cost': 80
}

constraints = {
    'initial_workforce': 40,
    'initial_inventory': 500,
    'units_per_worker': 30,
    'overtime_per_worker': 10,
    'max_subcontract': 500,
    'max_backorder_pct': 0.10
}

plan = aggregate_planning(demand, costs, constraints)
print(f"Optimal Total Cost: ${plan['total_cost']:,.0f}")
print("\nProduction Plan:")
print(plan['summary'])
```

### Capacity Requirements Planning (CRP)

**Process:**
1. Start with Master Production Schedule (MPS)
2. Explode to component requirements (BOM)
3. Calculate work center loads
4. Identify overload/underload periods
5. Adjust capacity or schedule

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CapacityRequirementsPlanning:
    """
    CRP - Calculate and analyze capacity requirements
    based on production schedule and routings
    """

    def __init__(self, work_centers):
        """
        Parameters:
        - work_centers: dict {name: {'capacity': hours, 'efficiency': 0-1}}
        """
        self.work_centers = work_centers

    def calculate_requirements(self, schedule, routings):
        """
        Calculate capacity requirements

        Parameters:
        - schedule: DataFrame with 'product', 'period', 'quantity'
        - routings: dict {product: [(work_center, hours_per_unit)]}

        Returns DataFrame with requirements by work center and period
        """

        requirements = []

        for idx, row in schedule.iterrows():
            product = row['product']
            period = row['period']
            quantity = row['quantity']

            # Get routing for product
            routing = routings.get(product, [])

            for work_center, hours_per_unit in routing:
                total_hours = quantity * hours_per_unit

                # Adjust for efficiency
                efficiency = self.work_centers[work_center]['efficiency']
                required_hours = total_hours / efficiency

                requirements.append({
                    'period': period,
                    'work_center': work_center,
                    'product': product,
                    'quantity': quantity,
                    'hours_required': required_hours
                })

        df = pd.DataFrame(requirements)

        # Aggregate by work center and period
        summary = df.groupby(['period', 'work_center'])['hours_required'].sum().reset_index()

        # Add capacity and utilization
        summary['capacity'] = summary['work_center'].map(
            lambda wc: self.work_centers[wc]['capacity']
        )
        summary['utilization'] = (summary['hours_required'] / summary['capacity']) * 100
        summary['variance'] = summary['capacity'] - summary['hours_required']

        return summary

    def identify_overloads(self, requirements, threshold=100):
        """
        Identify periods/work centers with overload

        Parameters:
        - requirements: output from calculate_requirements
        - threshold: utilization % threshold

        Returns overloaded resources
        """

        overloads = requirements[requirements['utilization'] > threshold].copy()
        overloads = overloads.sort_values(['period', 'work_center'])

        return overloads

    def plot_capacity_profile(self, requirements):
        """Visualize capacity requirements vs. available"""

        work_centers = requirements['work_center'].unique()

        fig, axes = plt.subplots(len(work_centers), 1,
                                figsize=(12, 4 * len(work_centers)),
                                squeeze=False)

        for i, wc in enumerate(work_centers):
            wc_data = requirements[requirements['work_center'] == wc]

            ax = axes[i, 0]

            # Plot capacity line
            ax.axhline(y=wc_data['capacity'].iloc[0],
                      color='green', linestyle='--',
                      linewidth=2, label='Capacity')

            # Plot requirements
            ax.bar(wc_data['period'], wc_data['hours_required'],
                  alpha=0.7, label='Required')

            # Highlight overloads
            overload = wc_data[wc_data['utilization'] > 100]
            if not overload.empty:
                ax.bar(overload['period'], overload['hours_required'],
                      color='red', alpha=0.7, label='Overload')

            ax.set_title(f'{wc} - Capacity Profile')
            ax.set_xlabel('Period')
            ax.set_ylabel('Hours')
            ax.legend()
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage
work_centers = {
    'Cutting': {'capacity': 160, 'efficiency': 0.90},
    'Welding': {'capacity': 160, 'efficiency': 0.85},
    'Assembly': {'capacity': 160, 'efficiency': 0.92},
    'Inspection': {'capacity': 160, 'efficiency': 0.95}
}

crp = CapacityRequirementsPlanning(work_centers)

# Production schedule
schedule = pd.DataFrame({
    'product': ['A', 'A', 'B', 'B', 'C', 'C'] * 3,
    'period': [1, 2, 1, 2, 1, 2] * 3,
    'quantity': [100, 120, 80, 90, 60, 70] * 3
})

# Routings: hours per unit at each work center
routings = {
    'A': [('Cutting', 0.5), ('Welding', 0.8), ('Assembly', 1.0), ('Inspection', 0.3)],
    'B': [('Cutting', 0.6), ('Assembly', 1.2), ('Inspection', 0.4)],
    'C': [('Cutting', 0.4), ('Welding', 1.0), ('Assembly', 0.8), ('Inspection', 0.2)]
}

# Calculate requirements
requirements = crp.calculate_requirements(schedule, routings)
print("Capacity Requirements:")
print(requirements)

# Identify overloads
overloads = crp.identify_overloads(requirements)
if not overloads.empty:
    print("\nOverloaded Resources:")
    print(overloads[['period', 'work_center', 'utilization', 'variance']])
else:
    print("\nNo overloads detected")

# Plot
crp.plot_capacity_profile(requirements)
```

---

## Capacity Expansion Analysis

### Economic Analysis of Capacity Investments

**Net Present Value (NPV) Analysis:**

```python
import numpy as np

def npv_capacity_investment(initial_investment, annual_benefits,
                           annual_costs, discount_rate, years):
    """
    Calculate NPV of capacity investment

    Parameters:
    - initial_investment: upfront cost
    - annual_benefits: revenue increase per year
    - annual_costs: operating costs per year
    - discount_rate: cost of capital (e.g., 0.10 for 10%)
    - years: investment horizon
    """

    cash_flows = [-initial_investment]

    for year in range(1, years + 1):
        net_benefit = annual_benefits - annual_costs
        discounted_benefit = net_benefit / ((1 + discount_rate) ** year)
        cash_flows.append(discounted_benefit)

    npv = sum(cash_flows)

    # Calculate IRR (Internal Rate of Return)
    irr = np.irr([-initial_investment] + [annual_benefits - annual_costs] * years)

    # Payback period
    cumulative = -initial_investment
    payback = None
    for year in range(1, years + 1):
        cumulative += (annual_benefits - annual_costs)
        if cumulative > 0 and payback is None:
            payback = year

    return {
        'npv': npv,
        'irr': irr * 100,
        'payback_years': payback,
        'total_investment': initial_investment,
        'annual_net_benefit': annual_benefits - annual_costs
    }

# Example: Evaluate new production line
investment_analysis = npv_capacity_investment(
    initial_investment=5_000_000,
    annual_benefits=2_000_000,    # Increased revenue
    annual_costs=800_000,          # Operating costs
    discount_rate=0.12,            # 12% cost of capital
    years=10
)

print("Investment Analysis:")
print(f"  NPV: ${investment_analysis['npv']:,.0f}")
print(f"  IRR: {investment_analysis['irr']:.1f}%")
print(f"  Payback: {investment_analysis['payback_years']} years")

if investment_analysis['npv'] > 0:
    print("\n✓ Investment is financially viable")
else:
    print("\n✗ Investment is not viable at this discount rate")
```

### Decision Tree Analysis for Capacity Timing

```python
import matplotlib.pyplot as plt
import numpy as np

class CapacityDecisionTree:
    """
    Decision tree for capacity expansion timing
    under demand uncertainty
    """

    def __init__(self):
        self.scenarios = []

    def add_scenario(self, name, probability, demand_growth,
                    expand_now_cost, expand_later_cost,
                    revenue_per_unit, shortage_cost):
        """Add demand scenario"""

        self.scenarios.append({
            'name': name,
            'probability': probability,
            'demand_growth': demand_growth,
            'expand_now_cost': expand_now_cost,
            'expand_later_cost': expand_later_cost,
            'revenue_per_unit': revenue_per_unit,
            'shortage_cost': shortage_cost
        })

    def evaluate_expand_now(self, current_capacity, periods=5):
        """Calculate expected value of expanding now"""

        ev = 0

        for scenario in self.scenarios:
            # Cost of expanding now
            cost = -scenario['expand_now_cost']

            # Benefits over periods
            for period in range(1, periods + 1):
                demand = current_capacity * (1 + scenario['demand_growth']) ** period
                capacity_after_expansion = current_capacity * 1.5  # Assume 50% expansion

                # Revenue from meeting demand
                served = min(demand, capacity_after_expansion)
                revenue = served * scenario['revenue_per_unit']

                # Discount
                discounted_revenue = revenue / (1.10 ** period)
                cost += discounted_revenue

            # Weight by probability
            ev += cost * scenario['probability']

        return ev

    def evaluate_expand_later(self, current_capacity, expand_period=3, periods=5):
        """Calculate expected value of expanding later"""

        ev = 0

        for scenario in self.scenarios:
            cost = 0

            for period in range(1, periods + 1):
                demand = current_capacity * (1 + scenario['demand_growth']) ** period

                if period < expand_period:
                    # Before expansion: limited by current capacity
                    served = min(demand, current_capacity)
                    shortage = max(0, demand - current_capacity)

                    revenue = served * scenario['revenue_per_unit']
                    shortage_penalty = shortage * scenario['shortage_cost']

                    discounted_value = (revenue - shortage_penalty) / (1.10 ** period)

                elif period == expand_period:
                    # Expansion happens
                    expansion_cost = -scenario['expand_later_cost']
                    served = min(demand, current_capacity * 1.5)
                    revenue = served * scenario['revenue_per_unit']

                    discounted_value = (expansion_cost + revenue) / (1.10 ** period)

                else:
                    # After expansion
                    served = min(demand, current_capacity * 1.5)
                    revenue = served * scenario['revenue_per_unit']

                    discounted_value = revenue / (1.10 ** period)

                cost += discounted_value

            # Weight by probability
            ev += cost * scenario['probability']

        return ev

    def evaluate_no_expansion(self, current_capacity, periods=5):
        """Calculate expected value of not expanding"""

        ev = 0

        for scenario in self.scenarios:
            cost = 0

            for period in range(1, periods + 1):
                demand = current_capacity * (1 + scenario['demand_growth']) ** period

                # Limited by current capacity
                served = min(demand, current_capacity)
                shortage = max(0, demand - current_capacity)

                revenue = served * scenario['revenue_per_unit']
                shortage_penalty = shortage * scenario['shortage_cost']

                discounted_value = (revenue - shortage_penalty) / (1.10 ** period)
                cost += discounted_value

            # Weight by probability
            ev += cost * scenario['probability']

        return ev

    def recommend(self, current_capacity):
        """Determine optimal capacity decision"""

        ev_now = self.evaluate_expand_now(current_capacity)
        ev_later = self.evaluate_expand_later(current_capacity)
        ev_no = self.evaluate_no_expansion(current_capacity)

        results = {
            'expand_now': ev_now,
            'expand_later': ev_later,
            'no_expansion': ev_no
        }

        best_option = max(results, key=results.get)

        return {
            'recommendation': best_option,
            'expected_values': results,
            'best_ev': results[best_option]
        }

# Example usage
dt = CapacityDecisionTree()

# Add demand scenarios
dt.add_scenario(
    name='High Growth',
    probability=0.30,
    demand_growth=0.15,
    expand_now_cost=10_000_000,
    expand_later_cost=12_000_000,
    revenue_per_unit=100,
    shortage_cost=50
)

dt.add_scenario(
    name='Moderate Growth',
    probability=0.50,
    demand_growth=0.08,
    expand_now_cost=10_000_000,
    expand_later_cost=12_000_000,
    revenue_per_unit=100,
    shortage_cost=50
)

dt.add_scenario(
    name='Low Growth',
    probability=0.20,
    demand_growth=0.03,
    expand_now_cost=10_000_000,
    expand_later_cost=12_000_000,
    revenue_per_unit=100,
    shortage_cost=50
)

# Get recommendation
current_capacity = 100000  # units per year
recommendation = dt.recommend(current_capacity)

print("Capacity Expansion Decision Analysis:")
print(f"\nExpected Values:")
for option, ev in recommendation['expected_values'].items():
    print(f"  {option}: ${ev:,.0f}")

print(f"\n✓ Recommendation: {recommendation['recommendation'].upper()}")
print(f"  Expected Value: ${recommendation['best_ev']:,.0f}")
```

---

## Flexible Capacity Strategies

### Options for Capacity Flexibility

**1. Workforce Flexibility**
- Cross-trained workers
- Temporary labor
- Overtime capability
- Variable shifts

**2. Equipment Flexibility**
- Flexible manufacturing systems
- Quick changeover capability
- Mobile equipment
- Shared equipment pools

**3. Facility Flexibility**
- Modular facilities
- Multi-product capable
- Scalable layouts
- Shared warehousing

**4. Partnership Flexibility**
- Contract manufacturing
- Co-packing arrangements
- 3PL relationships
- Supplier flexibility

**Flexibility Valuation:**

```python
def value_of_flexibility(demand_scenarios, fixed_capacity,
                        flexible_capacity, flexibility_cost):
    """
    Calculate value of flexible capacity using real options approach

    Parameters:
    - demand_scenarios: list of (probability, demand) tuples
    - fixed_capacity: base capacity level
    - flexible_capacity: additional flexible capacity available
    - flexibility_cost: cost per unit of flexible capacity

    Returns value of flexibility option
    """

    # Expected value with fixed capacity only
    ev_fixed = 0
    for prob, demand in demand_scenarios:
        served = min(demand, fixed_capacity)
        revenue = served * 100  # Revenue per unit
        shortage_cost = max(0, demand - fixed_capacity) * 50

        ev_fixed += prob * (revenue - shortage_cost)

    # Expected value with flexibility
    ev_flexible = 0
    for prob, demand in demand_scenarios:
        # Use flexible capacity only if needed
        if demand > fixed_capacity:
            flexible_used = min(demand - fixed_capacity, flexible_capacity)
            total_served = fixed_capacity + flexible_used
        else:
            flexible_used = 0
            total_served = demand

        revenue = total_served * 100
        flexibility_usage_cost = flexible_used * flexibility_cost
        shortage_cost = max(0, demand - total_served) * 50

        ev_flexible += prob * (revenue - flexibility_usage_cost - shortage_cost)

    value_of_flexibility = ev_flexible - ev_fixed

    return {
        'ev_without_flexibility': ev_fixed,
        'ev_with_flexibility': ev_flexible,
        'value_of_flexibility': value_of_flexibility,
        'flexibility_cost': flexible_capacity * flexibility_cost
    }

# Example
demand_scenarios = [
    (0.20, 8000),   # Low demand
    (0.50, 10000),  # Expected demand
    (0.30, 13000)   # High demand
]

result = value_of_flexibility(
    demand_scenarios=demand_scenarios,
    fixed_capacity=10000,
    flexible_capacity=3000,
    flexibility_cost=15  # Extra cost per unit for flexible capacity
)

print("Flexibility Analysis:")
print(f"  EV without flexibility: ${result['ev_without_flexibility']:,.0f}")
print(f"  EV with flexibility: ${result['ev_with_flexibility']:,.0f}")
print(f"  Value of flexibility: ${result['value_of_flexibility']:,.0f}")

if result['value_of_flexibility'] > result['flexibility_cost']:
    print(f"\n✓ Flexibility is valuable (worth ${result['value_of_flexibility']:,.0f})")
else:
    print(f"\n✗ Flexibility not cost-effective")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: Linear programming for aggregate planning
- `pyomo`: Advanced optimization modeling
- `scipy.optimize`: Optimization algorithms
- `gekko`: Dynamic optimization

**Simulation:**
- `simpy`: Discrete-event simulation
- `numpy`: Numerical computations
- `pandas`: Data analysis

**Visualization:**
- `matplotlib`, `seaborn`: Charts and graphs
- `plotly`: Interactive dashboards
- `networkx`: Process flow diagrams

### Commercial Software

**Capacity Planning Systems:**
- **SAP APO**: Advanced Planning & Optimization
- **Oracle ASCP**: Advanced Supply Chain Planning
- **Kinaxis RapidResponse**: S&OP with capacity planning
- **Blue Yonder**: Capacity planning modules
- **Anaplan**: Cloud planning platform

**Simulation:**
- **AnyLogic**: Multi-method simulation
- **Arena**: Discrete-event simulation
- **Simio**: 3D simulation with capacity analysis

**ERP Capacity Planning:**
- **SAP**: Work Center Planning, CRP
- **Oracle**: Capacity Requirements Planning
- **Microsoft Dynamics**: Capacity Planning
- **Infor**: Production Capacity Planning

---

## Common Challenges & Solutions

### Challenge: Uncertain Demand

**Problem:**
- Hard to size capacity
- Risk of over/under investment
- Volatility makes planning difficult

**Solutions:**
- Scenario planning and sensitivity analysis
- Build in flexibility (temporary labor, overtime, outsourcing)
- Modular capacity additions (smaller increments)
- Postponement strategies
- Real options analysis for timing

### Challenge: Lumpy Capacity Additions

**Problem:**
- Can't add small increments
- Must add entire production line or facility
- Creates periods of over-capacity

**Solutions:**
- Phased expansion plans
- Start with higher utilization targets
- Alternative uses for excess capacity (contract production)
- Financial analysis with longer payback periods
- Consider leasing vs. buying

### Challenge: Bottleneck Shifting

**Problem:**
- Expand one resource, bottleneck moves elsewhere
- Whack-a-mole problem
- Unbalanced capacity

**Solutions:**
- System-wide capacity analysis (not just one resource)
- Theory of Constraints approach
- Balanced capacity investments
- Buffer inventories at bottlenecks
- Process redesign to eliminate bottlenecks

### Challenge: Long Lead Times

**Problem:**
- Takes 12-24+ months to add capacity
- Demand may change by then
- Hard to react quickly

**Solutions:**
- Leading capacity strategy (anticipate growth)
- Modular/flexible facilities (faster deployment)
- Pre-engineered solutions
- Partnerships for quick capacity (contract manufacturing)
- Continuous planning and forecasting

### Challenge: Seasonal Demand

**Problem:**
- Need capacity for peak, idle rest of year
- High fixed costs
- Utilization swings

**Solutions:**
- Flexible workforce (temporary, seasonal hires)
- Build inventory in low season for high season
- Produce complementary products (counter-seasonal)
- Demand smoothing (promotions in off-season)
- Outsource peak production

---

## Output Format

### Capacity Plan Report

**Executive Summary:**
- Current capacity status and utilization
- Demand forecast and capacity gaps
- Recommended capacity strategy
- Investment requirements and timeline

**Current State Analysis:**

| Resource | Available Capacity | Current Utilization | Effective Capacity | OEE |
|----------|-------------------|---------------------|-------------------|-----|
| Line 1 | 10,000 units/mo | 85% | 8,500 units/mo | 72% |
| Line 2 | 8,000 units/mo | 92% | 7,360 units/mo | 78% |
| Warehouse | 50,000 sq ft | 78% | 39,000 sq ft | N/A |
| Labor | 120 FTE | 88% | 105.6 FTE | N/A |

**Capacity Requirements Forecast:**

| Period | Demand Forecast | Required Capacity | Current Capacity | Gap | Utilization |
|--------|----------------|-------------------|------------------|-----|-------------|
| Q1 2025 | 15,000 | 15,750 | 18,000 | -2,250 | 88% |
| Q2 2025 | 17,500 | 18,375 | 18,000 | +375 | 102% |
| Q3 2025 | 19,000 | 19,950 | 18,000 | +1,950 | 111% |
| Q4 2025 | 20,000 | 21,000 | 18,000 | +3,000 | 117% |

**Bottleneck Analysis:**

- **Current Bottleneck**: Assembly line (8,000 units/month capacity)
- **Impact**: Limits system throughput to 8,000 units/month
- **Constraint Duration**: Expected through Q3 2025
- **Recommended Action**: Add second assembly line

**Capacity Strategy Recommendation:**

**Option 1: Expand Now (Recommended)**
- Add assembly line and warehouse space
- Investment: $3.5M
- Timeline: Ready by Q2 2025
- NPV: $2.1M (10-year horizon)
- Avoids shortage costs and lost revenue

**Option 2: Flexible Capacity**
- Use contract manufacturing for 20% of volume
- Variable cost: +$15/unit
- Lower fixed investment
- Maintains service during growth

**Option 3: Delay Expansion**
- Wait until Q3 2025
- Risk of lost sales: $1.2M
- Lower upfront investment
- Higher long-term costs

**Implementation Plan:**
- Month 1-2: Finalize design and vendors
- Month 3-4: Equipment procurement
- Month 5-6: Installation and testing
- Month 7: Production ramp-up
- Month 8: Full capacity achieved

---

## Questions to Ask

If you need more context:
1. What type of capacity? (production, warehouse, transportation, labor)
2. What's the planning horizon? (short-term, tactical, strategic)
3. Current capacity utilization rates?
4. Demand forecast and growth expectations?
5. Known bottlenecks or constraints?
6. Budget available for capacity investments?
7. Service level requirements?
8. Current operating schedule (shifts, days per week)?

---

## Related Skills

- **master-production-scheduling**: For detailed production scheduling
- **demand-forecasting**: For capacity requirements forecasting
- **sales-operations-planning**: For integrated capacity planning in S&OP
- **network-design**: For facility capacity in network optimization
- **production-scheduling**: For shop floor capacity utilization
- **scenario-planning**: For capacity planning under uncertainty
- **workforce-scheduling**: For labor capacity planning
- **facility-location-problem**: For location-capacity decisions
