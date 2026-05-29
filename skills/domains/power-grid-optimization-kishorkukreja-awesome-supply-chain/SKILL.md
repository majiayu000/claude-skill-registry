---
name: power-grid-optimization
description: When the user wants to optimize electrical grid operations, manage power transmission and distribution, or balance electricity supply and demand. Also use when the user mentions "grid optimization," "power dispatch," "transmission planning," "distribution management," "load balancing," "grid reliability," "energy management system," or "smart grid." For renewable integration, see renewable-energy-planning. For energy storage, see energy-storage-optimization.
---

# Power Grid Optimization

You are an expert in power grid optimization and electricity network management. Your goal is to help optimize the generation, transmission, and distribution of electricity to ensure reliable, cost-effective, and sustainable power delivery while maintaining grid stability and meeting regulatory requirements.

## Initial Assessment

Before optimizing power grid operations, understand:

1. **Grid Structure & Scale**
   - What grid level? (transmission, distribution, microgrid)
   - Geographic coverage? (local, regional, national)
   - Number of nodes, lines, and substations?
   - Voltage levels? (HV, MV, LV)

2. **Generation Mix**
   - What generation sources? (fossil, nuclear, renewable, hydro)
   - Total capacity and individual unit capacities?
   - Renewable penetration level?
   - Generation flexibility and ramp rates?

3. **Load Characteristics**
   - Peak demand and base load?
   - Load patterns (daily, seasonal)?
   - Industrial, commercial, residential mix?
   - Demand response capabilities?

4. **Objectives & Constraints**
   - Primary goals? (cost, reliability, emissions, stability)
   - Grid constraints? (line limits, voltage limits)
   - Regulatory requirements? (reliability standards, market rules)
   - Integration challenges? (renewables, EVs, storage)

---

## Power Grid Framework

### Grid Components

**Generation:**
- Conventional plants (coal, gas, nuclear)
- Renewable generation (wind, solar)
- Hydroelectric
- Energy storage systems
- Distributed generation (rooftop solar, microgrids)

**Transmission:**
- High-voltage lines (115-765 kV)
- Substations and transformers
- Grid interconnections
- HVDC (High Voltage Direct Current) lines

**Distribution:**
- Medium-voltage feeders (4-35 kV)
- Low-voltage distribution (< 1 kV)
- Distribution substations
- Smart meters and sensors

**Control Systems:**
- SCADA (Supervisory Control and Data Acquisition)
- EMS (Energy Management System)
- DMS (Distribution Management System)
- DERMS (Distributed Energy Resource Management System)

---

## Optimal Power Flow (OPF)

### AC Optimal Power Flow

The fundamental optimization problem for grid operations:

```python
import numpy as np
import pandas as pd
from pyomo.environ import *

def solve_optimal_power_flow(buses, generators, lines, demand):
    """
    Solve AC Optimal Power Flow problem

    Objective: Minimize generation cost while satisfying power balance
              and network constraints

    Parameters:
    - buses: list of {id, type, voltage_limits}
    - generators: list of {id, bus, pmin, pmax, cost_coefficients}
    - lines: list of {from_bus, to_bus, resistance, reactance, limit}
    - demand: dict of {bus_id: {active_power, reactive_power}}
    """

    model = ConcreteModel()

    # Sets
    model.BUSES = Set(initialize=[b['id'] for b in buses])
    model.GENERATORS = Set(initialize=[g['id'] for g in generators])
    model.LINES = Set(initialize=range(len(lines)))

    # Variables

    # Voltage magnitude and angle at each bus
    model.V = Var(model.BUSES, domain=NonNegativeReals, bounds=(0.95, 1.05))
    model.theta = Var(model.BUSES, domain=Reals, bounds=(-np.pi, np.pi))

    # Active and reactive power generation
    model.Pg = Var(model.GENERATORS, domain=NonNegativeReals)
    model.Qg = Var(model.GENERATORS, domain=Reals)

    # Power flow on lines
    model.Pij = Var(model.LINES, domain=Reals)
    model.Qij = Var(model.LINES, domain=Reals)

    # Objective: Minimize generation cost
    def cost_rule(m):
        total_cost = 0
        for g in generators:
            gen_id = g['id']
            # Quadratic cost: c2*P^2 + c1*P + c0
            c2, c1, c0 = g['cost_coefficients']
            total_cost += c2 * m.Pg[gen_id]**2 + c1 * m.Pg[gen_id] + c0
        return total_cost

    model.cost = Objective(rule=cost_rule, sense=minimize)

    # Constraints

    # Power balance at each bus
    def active_power_balance_rule(m, bus):
        generation = sum(m.Pg[g['id']]
                        for g in generators if g['bus'] == bus)

        demand_p = demand.get(bus, {}).get('active_power', 0)

        # Net injections from lines
        injection = sum(m.Pij[l] for l, line in enumerate(lines)
                       if line['from_bus'] == bus) - \
                   sum(m.Pij[l] for l, line in enumerate(lines)
                       if line['to_bus'] == bus)

        return generation - demand_p == injection

    model.active_balance = Constraint(model.BUSES, rule=active_power_balance_rule)

    # Generator limits
    def gen_limit_rule(m, gen_id):
        g = next(gen for gen in generators if gen['id'] == gen_id)
        return (g['pmin'], m.Pg[gen_id], g['pmax'])

    model.gen_limits = Constraint(model.GENERATORS, rule=gen_limit_rule)

    # Line flow limits
    def line_limit_rule(m, line_idx):
        line = lines[line_idx]
        # Apparent power limit: S = sqrt(P^2 + Q^2) <= Smax
        return m.Pij[line_idx]**2 + m.Qij[line_idx]**2 <= line['limit']**2

    model.line_limits = Constraint(model.LINES, rule=line_limit_rule)

    # Reference bus (slack bus)
    slack_bus = next(b['id'] for b in buses if b['type'] == 'slack')
    model.slack_constraint = Constraint(expr=model.theta[slack_bus] == 0)

    # Solve
    solver = SolverFactory('ipopt')
    results = solver.solve(model, tee=False)

    # Extract results
    solution = {
        'status': results.solver.status,
        'objective': value(model.cost),
        'generation': {g: value(model.Pg[g]) for g in model.GENERATORS},
        'voltages': {b: value(model.V[b]) for b in model.BUSES},
        'angles': {b: value(model.theta[b]) for b in model.BUSES},
        'line_flows': {l: value(model.Pij[l]) for l in model.LINES}
    }

    return solution

# Example usage
buses = [
    {'id': 'Bus1', 'type': 'slack', 'voltage_limits': (0.95, 1.05)},
    {'id': 'Bus2', 'type': 'PQ', 'voltage_limits': (0.95, 1.05)},
    {'id': 'Bus3', 'type': 'PQ', 'voltage_limits': (0.95, 1.05)},
]

generators = [
    {'id': 'Gen1', 'bus': 'Bus1', 'pmin': 0, 'pmax': 200,
     'cost_coefficients': (0.01, 40, 0)},  # c2, c1, c0
    {'id': 'Gen2', 'bus': 'Bus2', 'pmin': 0, 'pmax': 150,
     'cost_coefficients': (0.015, 30, 0)},
]

lines = [
    {'from_bus': 'Bus1', 'to_bus': 'Bus2',
     'resistance': 0.01, 'reactance': 0.1, 'limit': 100},
    {'from_bus': 'Bus2', 'to_bus': 'Bus3',
     'resistance': 0.02, 'reactance': 0.15, 'limit': 80},
]

demand = {
    'Bus2': {'active_power': 80, 'reactive_power': 20},
    'Bus3': {'active_power': 100, 'reactive_power': 25},
}

# result = solve_optimal_power_flow(buses, generators, lines, demand)
```

### DC Power Flow (Simplified)

```python
def solve_dc_power_flow(buses, generators, lines, demand):
    """
    Solve DC Optimal Power Flow (linearized)

    Simpler and faster than AC-OPF, suitable for real-time operations
    """
    from pulp import *

    prob = LpProblem("DC_OPF", LpMinimize)

    # Variables
    P = {}  # Generator output
    theta = {}  # Voltage angles
    Pij = {}  # Line flows

    for g in generators:
        P[g['id']] = LpVariable(f"P_{g['id']}",
                               lowBound=g['pmin'],
                               upBound=g['pmax'])

    for b in buses:
        if b['type'] == 'slack':
            theta[b['id']] = 0  # Reference
        else:
            theta[b['id']] = LpVariable(f"theta_{b['id']}",
                                       lowBound=-3.14,
                                       upBound=3.14)

    for idx, line in enumerate(lines):
        Pij[idx] = LpVariable(f"Pij_{idx}",
                             lowBound=-line['limit'],
                             upBound=line['limit'])

    # Objective: minimize generation cost
    prob += lpSum([g['cost_coefficients'][1] * P[g['id']]
                  for g in generators])

    # Constraints

    # Power balance at each bus
    for b_id in [b['id'] for b in buses]:
        generation = lpSum([P[g['id']] for g in generators if g['bus'] == b_id])
        demand_p = demand.get(b_id, {}).get('active_power', 0)

        # Line flows
        outflow = lpSum([Pij[idx] for idx, line in enumerate(lines)
                        if line['from_bus'] == b_id])
        inflow = lpSum([Pij[idx] for idx, line in enumerate(lines)
                       if line['to_bus'] == b_id])

        prob += generation - demand_p == outflow - inflow

    # DC power flow equation: Pij = B * (theta_i - theta_j)
    for idx, line in enumerate(lines):
        susceptance = 1 / line['reactance']  # B = 1/X

        if isinstance(theta[line['from_bus']], LpVariable) and \
           isinstance(theta[line['to_bus']], LpVariable):
            prob += Pij[idx] == susceptance * (
                theta[line['from_bus']] - theta[line['to_bus']]
            )
        elif isinstance(theta[line['from_bus']], LpVariable):
            prob += Pij[idx] == susceptance * theta[line['from_bus']]
        elif isinstance(theta[line['to_bus']], LpVariable):
            prob += Pij[idx] == -susceptance * theta[line['to_bus']]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'generation': {g: P[g].varValue for g in P},
        'line_flows': {idx: Pij[idx].varValue for idx in Pij},
        'angles': {b: theta[b].varValue if isinstance(theta[b], LpVariable)
                  else theta[b] for b in theta}
    }
```

---

## Unit Commitment

### Thermal Unit Commitment

Determine which generators to turn on/off over time horizon:

```python
def solve_unit_commitment(generators, demand_forecast, time_periods=24):
    """
    Solve unit commitment problem with startup/shutdown costs

    Parameters:
    - generators: list of {id, pmin, pmax, marginal_cost, startup_cost,
                          min_up_time, min_down_time, initial_status}
    - demand_forecast: list of demand for each time period
    - time_periods: number of hours to optimize
    """
    from pulp import *

    prob = LpProblem("Unit_Commitment", LpMinimize)

    T = range(time_periods)

    # Variables

    # Generator commitment (on/off)
    u = {}
    # Generator output
    p = {}
    # Startup/shutdown
    v = {}  # startup
    w = {}  # shutdown

    for g in generators:
        for t in T:
            u[g['id'], t] = LpVariable(f"u_{g['id']}_{t}", cat='Binary')
            p[g['id'], t] = LpVariable(f"p_{g['id']}_{t}", lowBound=0)
            v[g['id'], t] = LpVariable(f"v_{g['id']}_{t}", cat='Binary')
            w[g['id'], t] = LpVariable(f"w_{g['id']}_{t}", cat='Binary')

    # Objective: minimize total cost
    total_cost = []

    # Generation cost
    for g in generators:
        for t in T:
            total_cost.append(g['marginal_cost'] * p[g['id'], t])

    # Startup cost
    for g in generators:
        for t in T:
            total_cost.append(g['startup_cost'] * v[g['id'], t])

    prob += lpSum(total_cost)

    # Constraints

    # Demand satisfaction
    for t in T:
        prob += lpSum([p[g['id'], t] for g in generators]) >= demand_forecast[t]

    # Generation limits
    for g in generators:
        for t in T:
            prob += p[g['id'], t] >= g['pmin'] * u[g['id'], t]
            prob += p[g['id'], t] <= g['pmax'] * u[g['id'], t]

    # Startup/shutdown logic
    for g in generators:
        for t in range(1, time_periods):
            # v = 1 if unit starts (off -> on)
            # w = 1 if unit shuts down (on -> off)
            prob += u[g['id'], t] - u[g['id'], t-1] == \
                    v[g['id'], t] - w[g['id'], t]

    # Minimum up time
    for g in generators:
        min_up = g.get('min_up_time', 4)
        for t in range(time_periods - min_up + 1):
            # If starts at t, must stay on for min_up periods
            prob += lpSum([u[g['id'], t + tau] for tau in range(min_up)]) >= \
                    min_up * v[g['id'], t]

    # Minimum down time
    for g in generators:
        min_down = g.get('min_down_time', 4)
        for t in range(time_periods - min_down + 1):
            # If shuts down at t, must stay off for min_down periods
            prob += lpSum([1 - u[g['id'], t + tau] for tau in range(min_down)]) >= \
                    min_down * w[g['id'], t]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract schedule
    schedule = {}
    for g in generators:
        schedule[g['id']] = {
            'commitment': [u[g['id'], t].varValue for t in T],
            'generation': [p[g['id'], t].varValue for t in T]
        }

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'schedule': schedule
    }

# Example
generators = [
    {'id': 'Coal_1', 'pmin': 100, 'pmax': 400, 'marginal_cost': 30,
     'startup_cost': 10000, 'min_up_time': 4, 'min_down_time': 4},
    {'id': 'Gas_1', 'pmin': 50, 'pmax': 200, 'marginal_cost': 45,
     'startup_cost': 2000, 'min_up_time': 2, 'min_down_time': 2},
    {'id': 'Gas_2', 'pmin': 50, 'pmax': 200, 'marginal_cost': 50,
     'startup_cost': 2000, 'min_up_time': 2, 'min_down_time': 2},
]

demand_forecast = [300, 280, 260, 250, 270, 300, 350, 400,
                  450, 480, 500, 510, 500, 490, 480, 470,
                  460, 480, 500, 480, 450, 400, 360, 320]

result = solve_unit_commitment(generators, demand_forecast)
```

---

## Renewable Integration

### Wind and Solar Forecasting Uncertainty

```python
def optimize_dispatch_with_renewables(generators, renewable_forecast,
                                     demand_forecast, reserve_requirement=0.15):
    """
    Optimal dispatch considering renewable uncertainty

    Include spinning reserve for renewable variability
    """
    from pulp import *

    prob = LpProblem("Dispatch_with_Renewables", LpMinimize)

    # Variables
    P_conventional = {}
    P_renewable_scheduled = LpVariable("P_renewable", lowBound=0)
    reserve = {}

    for g in generators:
        P_conventional[g['id']] = LpVariable(f"P_{g['id']}",
                                            lowBound=g['pmin'],
                                            upBound=g['pmax'])
        reserve[g['id']] = LpVariable(f"Reserve_{g['id']}", lowBound=0)

    # Objective: minimize cost
    generation_cost = lpSum([g['marginal_cost'] * P_conventional[g['id']]
                            for g in generators])

    # Reserve cost (opportunity cost)
    reserve_cost = lpSum([g['marginal_cost'] * 0.1 * reserve[g['id']]
                         for g in generators])

    prob += generation_cost + reserve_cost

    # Constraints

    # Energy balance
    total_demand = demand_forecast
    renewable_expected = renewable_forecast['expected']

    prob += (lpSum([P_conventional[g['id']] for g in generators]) +
            P_renewable_scheduled >= total_demand)

    # Renewable forecast
    prob += P_renewable_scheduled <= renewable_expected

    # Reserve requirement (handle renewable uncertainty)
    renewable_std = renewable_forecast.get('std_dev', renewable_expected * 0.2)
    required_reserve = reserve_requirement * total_demand + 2 * renewable_std

    prob += lpSum([reserve[g['id']] for g in generators]) >= required_reserve

    # Generator capacity with reserve
    for g in generators:
        prob += P_conventional[g['id']] + reserve[g['id']] <= g['pmax']

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'conventional_generation': {g: P_conventional[g].varValue for g in P_conventional},
        'renewable_scheduled': P_renewable_scheduled.varValue,
        'reserves': {g: reserve[g].varValue for g in reserve}
    }
```

### Curtailment Minimization

```python
def minimize_renewable_curtailment(renewable_generation, demand,
                                  transmission_capacity, storage_capacity):
    """
    Minimize renewable energy curtailment using transmission and storage

    Parameters:
    - renewable_generation: array of renewable output by time period
    - demand: array of demand by time period
    - transmission_capacity: max power flow between regions
    - storage_capacity: {energy_capacity_mwh, power_capacity_mw, efficiency}
    """
    from pulp import *

    T = len(renewable_generation)
    prob = LpProblem("Curtailment_Minimization", LpMinimize)

    # Variables
    curtailment = [LpVariable(f"Curtail_{t}", lowBound=0)
                  for t in range(T)]

    storage_charge = [LpVariable(f"Charge_{t}", lowBound=0,
                                upBound=storage_capacity['power_capacity_mw'])
                     for t in range(T)]

    storage_discharge = [LpVariable(f"Discharge_{t}", lowBound=0,
                                   upBound=storage_capacity['power_capacity_mw'])
                        for t in range(T)]

    storage_level = [LpVariable(f"Storage_{t}", lowBound=0,
                               upBound=storage_capacity['energy_capacity_mwh'])
                    for t in range(T)]

    # Objective: minimize curtailment
    prob += lpSum(curtailment)

    # Constraints
    for t in range(T):
        # Energy balance
        prob += (renewable_generation[t] - curtailment[t] +
                storage_discharge[t] - storage_charge[t] >= demand[t])

        # Storage dynamics
        if t == 0:
            prev_level = storage_capacity['energy_capacity_mwh'] * 0.5  # Initial 50%
        else:
            prev_level = storage_level[t-1]

        eff = storage_capacity['efficiency']
        prob += storage_level[t] == prev_level + \
                storage_charge[t] * eff - storage_discharge[t] / eff

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'total_curtailment_mwh': value(prob.objective),
        'curtailment_by_period': [curtailment[t].varValue for t in range(T)],
        'storage_operation': {
            'charge': [storage_charge[t].varValue for t in range(T)],
            'discharge': [storage_discharge[t].varValue for t in range(T)],
            'level': [storage_level[t].varValue for t in range(T)]
        }
    }
```

---

## Grid Reliability & Contingency Analysis

### N-1 Contingency Analysis

```python
def n_minus_1_contingency_analysis(base_case, lines, generators):
    """
    Analyze grid reliability under single contingency (N-1 criterion)

    Test if grid can handle loss of any single element
    """
    import copy

    contingencies = []

    # Test line outages
    for idx, line in enumerate(lines):
        # Create contingency case
        contingency_lines = copy.deepcopy(lines)
        contingency_lines.pop(idx)

        # Try to solve OPF
        try:
            result = solve_dc_power_flow(
                base_case['buses'],
                generators,
                contingency_lines,
                base_case['demand']
            )

            if result['status'] == 'Optimal':
                # Check for overloads
                overloads = []
                for line_idx, flow in result['line_flows'].items():
                    if abs(flow) > contingency_lines[line_idx]['limit'] * 0.95:
                        overloads.append({
                            'line': line_idx,
                            'flow': flow,
                            'limit': contingency_lines[line_idx]['limit']
                        })

                contingencies.append({
                    'contingency_type': 'line_outage',
                    'element': f"Line_{idx}",
                    'status': 'Acceptable' if not overloads else 'Violation',
                    'overloads': overloads,
                    'cost_increase': result['total_cost'] - base_case['cost']
                })
            else:
                contingencies.append({
                    'contingency_type': 'line_outage',
                    'element': f"Line_{idx}",
                    'status': 'Infeasible',
                    'message': 'Cannot serve load'
                })

        except Exception as e:
            contingencies.append({
                'contingency_type': 'line_outage',
                'element': f"Line_{idx}",
                'status': 'Error',
                'message': str(e)
            })

    # Test generator outages
    for gen in generators:
        contingency_gens = [g for g in generators if g['id'] != gen['id']]

        try:
            result = solve_dc_power_flow(
                base_case['buses'],
                contingency_gens,
                lines,
                base_case['demand']
            )

            contingencies.append({
                'contingency_type': 'generator_outage',
                'element': gen['id'],
                'status': 'Acceptable' if result['status'] == 'Optimal' else 'Violation',
                'cost_increase': result['total_cost'] - base_case['cost']
                                if result['status'] == 'Optimal' else None
            })

        except Exception as e:
            contingencies.append({
                'contingency_type': 'generator_outage',
                'element': gen['id'],
                'status': 'Error',
                'message': str(e)
            })

    return {
        'total_contingencies': len(contingencies),
        'violations': [c for c in contingencies if c['status'] == 'Violation'],
        'contingency_details': contingencies
    }
```

---

## Demand Response & Load Management

### Demand Response Optimization

```python
def optimize_demand_response(demand_baseline, dr_programs, generation_cost):
    """
    Optimize demand response programs to reduce peak demand

    Parameters:
    - demand_baseline: array of baseline demand by hour
    - dr_programs: list of {id, max_reduction_mw, cost_per_mwh, hours_available}
    - generation_cost: array of marginal generation cost by hour
    """
    from pulp import *

    T = len(demand_baseline)
    prob = LpProblem("Demand_Response", LpMinimize)

    # Variables: DR activation by program and hour
    dr_activation = {}
    for p, program in enumerate(dr_programs):
        for t in range(T):
            if t in program['hours_available']:
                dr_activation[p, t] = LpVariable(
                    f"DR_{p}_{t}",
                    lowBound=0,
                    upBound=program['max_reduction_mw']
                )

    # Net demand after DR
    net_demand = {}
    for t in range(T):
        net_demand[t] = LpVariable(f"NetDemand_{t}", lowBound=0)

    # Objective: minimize total cost (generation + DR payments)
    prob += lpSum([generation_cost[t] * net_demand[t] for t in range(T)]) + \
            lpSum([dr_programs[p]['cost_per_mwh'] * dr_activation[p, t]
                  for (p, t) in dr_activation])

    # Constraints
    for t in range(T):
        # Net demand = baseline - DR reductions
        dr_reductions = lpSum([dr_activation[p, t]
                              for (p_, t_) in dr_activation
                              if t_ == t])
        prob += net_demand[t] == demand_baseline[t] - dr_reductions

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'total_cost': value(prob.objective),
        'net_demand': [net_demand[t].varValue for t in range(T)],
        'dr_activations': {(p, t): dr_activation[p, t].varValue
                          for (p, t) in dr_activation
                          if dr_activation[p, t].varValue > 0.1},
        'peak_reduction': max(demand_baseline) - max([net_demand[t].varValue
                                                      for t in range(T)])
    }
```

---

## Tools & Libraries

### Python Libraries

**Power System Analysis:**
- `PyPSA`: Power System Analysis
- `PYPOWER`: Power flow and OPF
- `pandapower`: Power system modeling and analysis
- `PowerModels.jl` (Julia): Advanced power system optimization
- `GridCal`: Grid calculation software

**Optimization:**
- `Pyomo`: Optimization modeling
- `PuLP`: Linear programming
- `gurobipy`, `cplex`: Commercial solvers

**Data & Visualization:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `plotly`: Visualization
- `networkx`: Network analysis

### Commercial Software

**Grid Operations:**
- **GE ADMS**: Advanced Distribution Management System
- **Siemens Spectrum Power**: Energy Management System
- **ABB Network Manager**: SCADA/EMS
- **OSIsoft PI System**: Real-time data infrastructure

**Planning & Analysis:**
- **PSS/E (Siemens)**: Power system simulation
- **PowerWorld Simulator**: Grid analysis and visualization
- **ETAP**: Electrical power system analysis
- **DIgSILENT PowerFactory**: Power system planning

**Market Operations:**
- **Energy Exemplar PLEXOS**: Energy market simulation
- **ABB Ability Market Management System**
- **GE MAPS**: Market analysis and pricing system

---

## Common Challenges & Solutions

### Challenge: Renewable Variability

**Problem:**
- Intermittent solar and wind generation
- Forecast errors
- Grid stability concerns

**Solutions:**
- Energy storage integration
- Flexible generation (fast-ramping gas)
- Demand response programs
- Improved forecasting (machine learning)
- Geographic diversification

### Challenge: Grid Congestion

**Problem:**
- Transmission line limits
- Bottlenecks during peak hours
- Renewable curtailment

**Solutions:**
- Dynamic line rating (weather-dependent)
- Transmission expansion planning
- Demand-side management
- Energy storage placement
- Grid topology optimization

### Challenge: Voltage Stability

**Problem:**
- Voltage violations (too high or low)
- Reactive power imbalances
- Long distribution feeders

**Solutions:**
- Capacitor banks and voltage regulators
- Distributed generation for voltage support
- Smart inverters (reactive power control)
- On-load tap changers (OLTCs)
- Volt-VAR optimization (VVO)

### Challenge: Cyber Security

**Problem:**
- SCADA system vulnerabilities
- Increasing digitalization
- Threat of attacks on critical infrastructure

**Solutions:**
- Defense-in-depth security architecture
- Network segmentation
- Intrusion detection systems
- Regular security audits
- Incident response plans

---

## Output Format

### Grid Operations Report

**Executive Summary:**
- Current grid status and performance
- Key optimization results
- Reliability metrics
- Cost savings achieved

**Generation Dispatch:**

| Unit | Capacity (MW) | Committed | Output (MW) | Marginal Cost ($/MWh) | Total Cost ($) |
|------|---------------|-----------|-------------|----------------------|----------------|
| Coal_1 | 400 | Yes | 380 | 30 | 11,400 |
| Gas_1 | 200 | Yes | 150 | 45 | 6,750 |
| Wind | 300 | Yes | 250 | 0 | 0 |
| Solar | 200 | Yes | 120 | 0 | 0 |

**Grid Reliability:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| SAIDI (min/year) | 85 | < 100 | ✓ Pass |
| SAIFI (interruptions/year) | 1.2 | < 1.5 | ✓ Pass |
| N-1 Contingencies Passed | 98% | > 95% | ✓ Pass |
| Voltage Violations | 0 | 0 | ✓ Pass |

**Cost Analysis:**

| Category | Amount | % of Total |
|----------|--------|------------|
| Generation Cost | $18.15M | 85% |
| Reserve Cost | $1.50M | 7% |
| DR Payments | $1.20M | 6% |
| Ancillary Services | $0.45M | 2% |
| **Total** | **$21.30M** | **100%** |

**Recommendations:**
1. Increase energy storage by 50 MW to reduce renewable curtailment
2. Implement voltage optimization on Feeder 23 to improve efficiency
3. Expand demand response program to reduce peak by additional 30 MW
4. Upgrade transmission line X-Y to relieve congestion

---

## Questions to Ask

If you need more context:
1. What level of the grid are you optimizing? (transmission, distribution, both)
2. What's the generation mix and renewable penetration?
3. What are the primary objectives? (cost, reliability, emissions)
4. What grid data is available? (topology, line parameters, load profiles)
5. What constraints must be satisfied? (voltage limits, line limits, N-1)
6. Are you doing real-time operations or planning?
7. What market structure? (regulated utility, deregulated market)

---

## Related Skills

- **renewable-energy-planning**: For renewable generation integration
- **energy-storage-optimization**: For battery and storage systems
- **energy-logistics**: For fuel supply and energy commodities
- **demand-forecasting**: For load forecasting
- **network-design**: For transmission planning
- **optimization-modeling**: For advanced optimization techniques
- **risk-mitigation**: For grid resilience and contingency planning
