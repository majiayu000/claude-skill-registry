---
name: optimization-modeling
description: When the user wants to build optimization models, solve mathematical programming problems, or find optimal solutions. Also use when the user mentions "linear programming," "integer programming," "mixed-integer programming," "constraint optimization," "mathematical optimization," "operations research," "optimal solution," or "decision optimization." For network design specifically, see network-design. For routing, see route-optimization.
---

# Optimization Modeling

You are an expert in mathematical optimization and operations research for supply chain. Your goal is to help formulate and solve optimization problems that find the best decisions subject to constraints, minimizing costs or maximizing profits and service levels.

## Initial Assessment

Before building optimization models, understand:

1. **Business Problem**
   - What decision needs to be made? (production, inventory, routing, scheduling)
   - What's being optimized? (minimize cost, maximize profit, maximize service)
   - Time horizon? (operational, tactical, strategic)
   - Expected impact and value?

2. **Decision Variables**
   - What can be controlled? (quantities, assignments, schedules)
   - Continuous or discrete decisions?
   - Scale? (10 variables vs. 100,000 variables)

3. **Constraints**
   - What limits exist? (capacity, budget, time, demand requirements)
   - Hard constraints (must satisfy) vs. soft constraints (preferences)?
   - How many constraints? (dozens vs. millions)

4. **Data Availability**
   - All parameters known with certainty?
   - Uncertainty or variability?
   - Data quality and completeness?

5. **Technical Environment**
   - Optimization expertise in team?
   - Solver access? (commercial vs. open-source)
   - Computational resources?
   - Integration requirements?

---

## Optimization Problem Types

### Linear Programming (LP)

**Characteristics:**
- Continuous decision variables
- Linear objective function
- Linear constraints
- Fast to solve (polynomial time)

**Supply Chain Applications:**
- Production planning
- Transportation optimization
- Blending problems
- Network flow optimization

**Example: Production Planning**

```python
from pulp import *
import pandas as pd

def production_planning_lp(products, resources, demand, capacity, costs):
    """
    Determine optimal production quantities

    Decision: How much to produce of each product?
    Objective: Minimize total production cost
    Constraints: Resource capacity, meet demand

    products: list of product names
    resources: list of resource names
    demand: dict {product: demand_quantity}
    capacity: dict {resource: available_capacity}
    costs: dict {(product, resource): cost_per_unit}
    """

    # Create problem
    prob = LpProblem("Production_Planning", LpMinimize)

    # Decision variables: production quantity for each product
    production = LpVariable.dicts("Produce",
                                  products,
                                  lowBound=0,
                                  cat='Continuous')

    # Objective: Minimize total cost
    prob += lpSum([costs[product] * production[product]
                   for product in products]), "Total_Cost"

    # Constraints
    # 1. Meet demand
    for product in products:
        prob += production[product] >= demand[product], \
                f"Meet_Demand_{product}"

    # 2. Resource capacity
    # Assume resource_usage[product][resource] is known
    for resource in resources:
        prob += lpSum([resource_usage[product][resource] * production[product]
                      for product in products]) <= capacity[resource], \
                f"Capacity_{resource}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=1))

    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'production_plan': {
            product: production[product].varValue
            for product in products
        }
    }

    return results

# Example data
products = ['Product_A', 'Product_B', 'Product_C']
resources = ['Labor', 'Machine', 'Material']

demand = {
    'Product_A': 100,
    'Product_B': 150,
    'Product_C': 80
}

capacity = {
    'Labor': 1000,  # hours
    'Machine': 800,  # hours
    'Material': 5000  # units
}

costs = {
    'Product_A': 50,
    'Product_B': 75,
    'Product_C': 60
}

resource_usage = {
    'Product_A': {'Labor': 2, 'Machine': 3, 'Material': 10},
    'Product_B': {'Labor': 3, 'Machine': 2, 'Material': 15},
    'Product_C': {'Labor': 1.5, 'Machine': 4, 'Material': 12}
}

result = production_planning_lp(products, resources, demand, capacity, costs)
print(f"Optimal Cost: ${result['total_cost']:,.2f}")
print("Production Plan:")
for product, qty in result['production_plan'].items():
    print(f"  {product}: {qty:.2f} units")
```

### Integer Programming (IP) / Mixed-Integer Programming (MIP)

**Characteristics:**
- Some/all variables must be integers
- Binary (0/1) decisions common
- NP-hard (exponential complexity)
- Requires branch-and-bound or cutting planes

**Supply Chain Applications:**
- Facility location
- Assignment problems
- Lot sizing with setup costs
- Vehicle routing
- Capacity planning

**Example: Facility Location Problem**

```python
def facility_location_mip(customers, facilities, demand, costs_dict):
    """
    Facility location problem with fixed costs

    Decision:
    - Which facilities to open (binary)
    - How much to ship from each facility to each customer (continuous)

    Objective: Minimize total cost (fixed + transportation)

    customers: list of customer IDs
    facilities: list of potential facility IDs
    demand: dict {customer: demand}
    costs_dict: {
        'fixed': {facility: fixed_cost},
        'capacity': {facility: capacity},
        'transport': {(customer, facility): cost_per_unit}
    }
    """

    prob = LpProblem("Facility_Location", LpMinimize)

    # Decision variables
    # y[j] = 1 if facility j is opened, 0 otherwise
    y = LpVariable.dicts("Open_Facility",
                        facilities,
                        cat='Binary')

    # x[i,j] = quantity shipped from facility j to customer i
    x = LpVariable.dicts("Ship",
                        [(i, j) for i in customers for j in facilities],
                        lowBound=0,
                        cat='Continuous')

    # Objective: Minimize total cost
    prob += (
        # Fixed costs
        lpSum([costs_dict['fixed'][j] * y[j] for j in facilities]) +

        # Transportation costs
        lpSum([costs_dict['transport'][i,j] * x[i,j]
              for i in customers for j in facilities])
    ), "Total_Cost"

    # Constraints

    # 1. Demand satisfaction
    for i in customers:
        prob += lpSum([x[i,j] for j in facilities]) >= demand[i], \
                f"Demand_{i}"

    # 2. Capacity constraints
    for j in facilities:
        prob += lpSum([x[i,j] for i in customers]) <= \
                costs_dict['capacity'][j] * y[j], \
                f"Capacity_{j}"

    # 3. Can only ship from open facilities
    for i in customers:
        for j in facilities:
            prob += x[i,j] <= demand[i] * y[j], \
                    f"Open_Required_{i}_{j}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=1))

    # Extract results
    open_facilities = [j for j in facilities if y[j].varValue > 0.5]

    flows = {}
    for i in customers:
        for j in facilities:
            if x[i,j].varValue > 0.01:
                flows[(i,j)] = x[i,j].varValue

    results = {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'open_facilities': open_facilities,
        'num_facilities': len(open_facilities),
        'flows': flows
    }

    return results

# Example usage
customers = ['Customer_A', 'Customer_B', 'Customer_C', 'Customer_D']
facilities = ['DC_1', 'DC_2', 'DC_3']

demand = {
    'Customer_A': 1000,
    'Customer_B': 1500,
    'Customer_C': 800,
    'Customer_D': 1200
}

costs_dict = {
    'fixed': {
        'DC_1': 500000,
        'DC_2': 600000,
        'DC_3': 450000
    },
    'capacity': {
        'DC_1': 3000,
        'DC_2': 2500,
        'DC_3': 2000
    },
    'transport': {
        ('Customer_A', 'DC_1'): 5.0,
        ('Customer_A', 'DC_2'): 8.0,
        ('Customer_A', 'DC_3'): 12.0,
        ('Customer_B', 'DC_1'): 7.0,
        ('Customer_B', 'DC_2'): 4.0,
        ('Customer_B', 'DC_3'): 9.0,
        ('Customer_C', 'DC_1'): 10.0,
        ('Customer_C', 'DC_2'): 6.0,
        ('Customer_C', 'DC_3'): 5.0,
        ('Customer_D', 'DC_1'): 8.0,
        ('Customer_D', 'DC_2'): 9.0,
        ('Customer_D', 'DC_3'): 7.0
    }
}

result = facility_location_mip(customers, facilities, demand, costs_dict)
print(f"\nOptimal Solution:")
print(f"Total Cost: ${result['total_cost']:,.2f}")
print(f"Open Facilities: {result['open_facilities']}")
```

### Nonlinear Programming (NLP)

**Characteristics:**
- Nonlinear objective or constraints
- Continuous variables
- Local vs. global optima
- Requires specialized solvers

**Supply Chain Applications:**
- Inventory optimization with nonlinear holding costs
- Pricing optimization
- Production with economies of scale
- Supply chain network with nonlinear costs

```python
from scipy.optimize import minimize
import numpy as np

def inventory_optimization_nlp(products_data, budget):
    """
    Multi-product inventory optimization with nonlinear costs

    Decision: Safety stock levels for each product
    Objective: Minimize total cost (holding + stockout)
    Constraint: Budget limit

    products_data: list of dicts with {
        'sku': product ID,
        'demand_mean': average demand,
        'demand_std': demand std dev,
        'lead_time': lead time in days,
        'unit_cost': cost per unit,
        'stockout_cost': cost per stockout event
    }
    """

    n_products = len(products_data)

    def objective(safety_stocks):
        """
        Total cost: holding cost + expected stockout cost

        holding cost = safety_stock * unit_cost * holding_rate
        stockout cost = stockout_probability * stockout_cost
        """

        total_cost = 0
        holding_rate = 0.25  # 25% annual holding cost

        for i, ss in enumerate(safety_stocks):
            product = products_data[i]

            # Holding cost (linear)
            holding_cost = ss * product['unit_cost'] * holding_rate

            # Stockout cost (nonlinear)
            # Calculate service level from safety stock
            from scipy import stats
            std_during_lt = product['demand_std'] * np.sqrt(product['lead_time'])

            if std_during_lt > 0:
                z = ss / std_during_lt
                service_level = stats.norm.cdf(z)
                stockout_prob = 1 - service_level
            else:
                stockout_prob = 0

            expected_stockout_cost = stockout_prob * product['stockout_cost']

            total_cost += holding_cost + expected_stockout_cost

        return total_cost

    def budget_constraint(safety_stocks):
        """Budget constraint: total inventory value <= budget"""
        total_value = sum(
            ss * products_data[i]['unit_cost']
            for i, ss in enumerate(safety_stocks)
        )
        return budget - total_value

    # Initial guess: allocate budget equally
    avg_unit_cost = np.mean([p['unit_cost'] for p in products_data])
    x0 = np.full(n_products, budget / (n_products * avg_unit_cost))

    # Constraints
    constraints = [
        {'type': 'ineq', 'fun': budget_constraint}
    ]

    # Bounds: non-negative safety stock
    bounds = [(0, None) for _ in range(n_products)]

    # Solve
    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'disp': True}
    )

    # Extract results
    optimal_ss = result.x

    results_df = pd.DataFrame(products_data)
    results_df['optimal_safety_stock'] = optimal_ss
    results_df['inventory_value'] = optimal_ss * results_df['unit_cost']

    return {
        'status': 'Optimal' if result.success else 'Failed',
        'total_cost': result.fun,
        'products': results_df,
        'total_inventory_value': results_df['inventory_value'].sum()
    }

# Example
products_data = [
    {'sku': 'A', 'demand_mean': 100, 'demand_std': 20,
     'lead_time': 14, 'unit_cost': 50, 'stockout_cost': 500},
    {'sku': 'B', 'demand_mean': 200, 'demand_std': 40,
     'lead_time': 7, 'unit_cost': 30, 'stockout_cost': 300},
    {'sku': 'C', 'demand_mean': 50, 'demand_std': 25,
     'lead_time': 21, 'unit_cost': 100, 'stockout_cost': 1000},
]

result = inventory_optimization_nlp(products_data, budget=50000)
print(f"Total Cost: ${result['total_cost']:,.2f}")
print(f"Total Inventory Value: ${result['total_inventory_value']:,.2f}")
print("\nOptimal Safety Stocks:")
print(result['products'][['sku', 'optimal_safety_stock', 'inventory_value']])
```

---

## Advanced Optimization Techniques

### Multi-Objective Optimization

**Weighted Sum Approach:**

```python
def multi_objective_network_design(customers, facilities, demand, costs,
                                   alpha=0.6, beta=0.4):
    """
    Network design with multiple objectives

    Objectives:
    1. Minimize cost (weight: alpha)
    2. Minimize average distance / maximize service (weight: beta)

    alpha + beta = 1.0
    """

    prob = LpProblem("Multi_Objective_Network", LpMinimize)

    # Decision variables
    y = LpVariable.dicts("Open", facilities, cat='Binary')
    x = LpVariable.dicts("Flow",
                        [(i,j) for i in customers for j in facilities],
                        lowBound=0)

    # Normalize cost and distance objectives
    max_cost = sum(costs['fixed'].values()) + \
               sum(costs['transport'].values()) * sum(demand.values())

    max_distance = max(costs['distance'].values()) * sum(demand.values())

    # Weighted objective
    prob += (
        alpha * (
            lpSum([costs['fixed'][j] * y[j] for j in facilities]) +
            lpSum([costs['transport'][i,j] * x[i,j]
                  for i in customers for j in facilities])
        ) / max_cost +

        beta * (
            lpSum([costs['distance'][i,j] * x[i,j]
                  for i in customers for j in facilities])
        ) / max_distance
    ), "Weighted_Objective"

    # Add constraints (similar to previous examples)
    # ... demand, capacity, facility opening constraints ...

    prob.solve()

    return extract_results(prob, y, x)

# Run with different weights to get Pareto frontier
pareto_solutions = []

for alpha in [0.9, 0.7, 0.5, 0.3, 0.1]:
    beta = 1.0 - alpha
    result = multi_objective_network_design(
        customers, facilities, demand, costs,
        alpha=alpha, beta=beta
    )
    pareto_solutions.append({
        'alpha': alpha,
        'cost': result['total_cost'],
        'avg_distance': result['avg_distance'],
        'open_facilities': result['open_facilities']
    })

# Plot Pareto frontier
pareto_df = pd.DataFrame(pareto_solutions)

plt.figure(figsize=(10, 6))
plt.plot(pareto_df['cost'], pareto_df['avg_distance'], 'o-', markersize=10)
plt.xlabel('Total Cost ($)')
plt.ylabel('Average Distance (miles)')
plt.title('Pareto Frontier: Cost vs. Service Trade-off')
plt.grid(True, alpha=0.3)

for i, row in pareto_df.iterrows():
    plt.annotate(f"α={row['alpha']:.1f}",
                (row['cost'], row['avg_distance']),
                textcoords="offset points",
                xytext=(0,10),
                ha='center')

plt.show()
```

### Stochastic Optimization

**Two-Stage Stochastic Programming:**

```python
def two_stage_stochastic_production(scenarios):
    """
    Production planning under demand uncertainty

    Stage 1 (before uncertainty): Decide production quantities
    Stage 2 (after demand realized): Decide inventory/backorder

    scenarios: list of dicts with {
        'demand': demand realization,
        'probability': scenario probability
    }
    """

    prob = LpProblem("Stochastic_Production", LpMinimize)

    products = ['A', 'B', 'C']
    production_cost = {'A': 10, 'B': 15, 'C': 12}
    inventory_cost = {'A': 2, 'B': 3, 'C': 2}
    backorder_cost = {'A': 50, 'B': 60, 'C': 55}
    capacity = 1000

    # Stage 1: Production decisions (before uncertainty)
    produce = LpVariable.dicts("Produce", products, lowBound=0)

    # Stage 2: Recourse decisions for each scenario
    inventory = LpVariable.dicts("Inventory",
                                [(s, p) for s in range(len(scenarios))
                                        for p in products],
                                lowBound=0)

    backorder = LpVariable.dicts("Backorder",
                                [(s, p) for s in range(len(scenarios))
                                        for p in products],
                                lowBound=0)

    # Objective: Stage 1 cost + Expected Stage 2 cost
    prob += (
        # Stage 1: Production cost
        lpSum([production_cost[p] * produce[p] for p in products]) +

        # Stage 2: Expected recourse cost
        lpSum([scenarios[s]['probability'] * (
            inventory_cost[p] * inventory[s,p] +
            backorder_cost[p] * backorder[s,p]
        ) for s in range(len(scenarios)) for p in products])
    ), "Expected_Total_Cost"

    # Stage 1 constraints
    prob += lpSum([produce[p] for p in products]) <= capacity, "Capacity"

    # Stage 2 constraints (for each scenario)
    for s, scenario in enumerate(scenarios):
        for p in products:
            # Inventory balance
            prob += (produce[p] + backorder[s,p] ==
                    scenario['demand'][p] + inventory[s,p]), \
                    f"Balance_S{s}_{p}"

    # Solve
    prob.solve()

    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'expected_cost': value(prob.objective),
        'production_plan': {p: produce[p].varValue for p in products},
        'scenarios': []
    }

    for s, scenario in enumerate(scenarios):
        results['scenarios'].append({
            'demand': scenario['demand'],
            'probability': scenario['probability'],
            'inventory': {p: inventory[s,p].varValue for p in products},
            'backorder': {p: backorder[s,p].varValue for p in products}
        })

    return results

# Example with 3 demand scenarios
scenarios = [
    {
        'demand': {'A': 100, 'B': 150, 'C': 80},
        'probability': 0.3  # Low demand
    },
    {
        'demand': {'A': 150, 'B': 200, 'C': 120},
        'probability': 0.5  # Medium demand
    },
    {
        'demand': {'A': 200, 'B': 250, 'C': 150},
        'probability': 0.2  # High demand
    }
]

result = two_stage_stochastic_production(scenarios)
print(f"Expected Total Cost: ${result['expected_cost']:,.2f}")
print("\nFirst-Stage Production Plan:")
for product, qty in result['production_plan'].items():
    print(f"  {product}: {qty:.2f} units")
```

### Robust Optimization

```python
def robust_production_planning(products, nominal_demand, uncertainty_budget):
    """
    Robust optimization: protect against demand uncertainty

    Uses budgeted uncertainty set (Bertsimas & Sim)

    nominal_demand: dict {product: nominal_value}
    uncertainty_budget: Gamma parameter (0 to len(products))
    """

    prob = LpProblem("Robust_Production", LpMinimize)

    # Decision variables
    produce = LpVariable.dicts("Produce", products, lowBound=0)

    # Auxiliary variables for robust constraints
    z = LpVariable.dicts("Z", products, lowBound=0)
    p = LpVariable("P", lowBound=0)

    production_cost = {p: 10 for p in products}
    capacity = 1000

    # Objective
    prob += lpSum([production_cost[p] * produce[p] for p in products]), \
            "Production_Cost"

    # Capacity constraint
    prob += lpSum([produce[p] for p in products]) <= capacity, "Capacity"

    # Robust demand satisfaction
    # Must satisfy demand even if up to Gamma products have worst-case demand
    deviation = {p: nominal_demand[p] * 0.2 for p in products}  # 20% deviation

    for p in products:
        # Nominal constraint
        prob += produce[p] >= nominal_demand[p], f"Nominal_Demand_{p}"

        # Robust constraint
        prob += z[p] >= deviation[p], f"Deviation_{p}"

    prob += (
        lpSum([produce[p] for p in products]) >=
        lpSum([nominal_demand[p] for p in products]) +
        lpSum([z[p] for p in products]) * uncertainty_budget / len(products)
    ), "Robust_Demand"

    prob.solve()

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'production': {p: produce[p].varValue for p in products}
    }

# Compare robust vs. nominal solution
products = ['A', 'B', 'C']
nominal_demand = {'A': 100, 'B': 150, 'C': 80}

# Nominal solution (Gamma = 0)
nominal_result = robust_production_planning(products, nominal_demand, 0)

# Robust solution (Gamma = 2)
robust_result = robust_production_planning(products, nominal_demand, 2)

print("Nominal Solution:")
print(f"  Cost: ${nominal_result['total_cost']:,.2f}")
print(f"  Production: {nominal_result['production']}")

print("\nRobust Solution (Gamma=2):")
print(f"  Cost: ${robust_result['total_cost']:,.2f}")
print(f"  Production: {robust_result['production']}")

print(f"\nPrice of Robustness: ${robust_result['total_cost'] - nominal_result['total_cost']:,.2f}")
```

---

## Decomposition Methods

### Benders Decomposition

```python
def benders_decomposition_network(customers, facilities, demand, costs, max_iter=20):
    """
    Benders decomposition for large-scale network design

    Master problem: Facility location decisions
    Subproblem: Transportation flows given facility decisions
    """

    # Master problem
    master = LpProblem("Master", LpMinimize)

    y = LpVariable.dicts("Open", facilities, cat='Binary')
    theta = LpVariable("Theta", lowBound=0)  # Transportation cost approximation

    # Master objective: Fixed costs + transportation cost approximation
    master += (
        lpSum([costs['fixed'][j] * y[j] for j in facilities]) + theta
    ), "Master_Obj"

    # Initial constraint: at least one facility must open
    master += lpSum([y[j] for j in facilities]) >= 1, "At_Least_One"

    iteration = 0
    best_solution = None
    best_obj = float('inf')

    while iteration < max_iter:
        iteration += 1

        # Solve master problem
        master.solve(PULP_CBC_CMD(msg=0))

        if LpStatus[master.status] != 'Optimal':
            break

        # Get facility decisions
        y_vals = {j: y[j].varValue for j in facilities}
        open_facilities = [j for j in facilities if y_vals[j] > 0.5]

        # Solve subproblem (transportation given open facilities)
        sub_result = solve_transportation_subproblem(
            customers, open_facilities, demand, costs
        )

        # Check termination
        master_obj = value(master.objective)
        total_obj = sum([costs['fixed'][j] * y_vals[j] for j in facilities]) + \
                   sub_result['transport_cost']

        print(f"Iteration {iteration}: Master={master_obj:.2f}, Total={total_obj:.2f}")

        if total_obj < best_obj:
            best_obj = total_obj
            best_solution = {
                'open_facilities': open_facilities,
                'flows': sub_result['flows']
            }

        # Check convergence
        if abs(master_obj - total_obj) < 0.01:
            break

        # Add Benders cut to master
        cut = create_benders_cut(y, sub_result['dual_values'], facilities)
        master += cut, f"Benders_Cut_{iteration}"

    return {
        'iterations': iteration,
        'total_cost': best_obj,
        'solution': best_solution
    }

def solve_transportation_subproblem(customers, open_facilities, demand, costs):
    """Solve transportation subproblem with fixed facilities"""

    sub = LpProblem("Subproblem", LpMinimize)

    x = LpVariable.dicts("Ship",
                        [(i,j) for i in customers for j in open_facilities],
                        lowBound=0)

    # Objective
    sub += lpSum([costs['transport'][i,j] * x[i,j]
                 for i in customers for j in open_facilities]), "Transport_Cost"

    # Demand constraints
    dual_values = {}
    for i in customers:
        constraint = lpSum([x[i,j] for j in open_facilities]) >= demand[i]
        sub += constraint, f"Demand_{i}"

    # Solve
    sub.solve(PULP_CBC_CMD(msg=0))

    # Extract dual values (for Benders cut)
    # Note: PuLP doesn't easily provide duals, simplified here

    return {
        'transport_cost': value(sub.objective),
        'flows': {(i,j): x[i,j].varValue
                 for i in customers for j in open_facilities
                 if x[i,j].varValue > 0.01},
        'dual_values': dual_values
    }
```

---

## Column Generation

```python
def cutting_stock_column_generation(rolls, demands, roll_width):
    """
    Cutting stock problem using column generation

    Problem: Cut large rolls into smaller pieces to meet demand,
             minimizing number of rolls used

    rolls: list of available roll IDs
    demands: dict {piece_width: quantity_needed}
    roll_width: width of standard roll
    """

    # Master problem: Select cutting patterns
    master = LpProblem("Master_CSP", LpMinimize)

    # Initial patterns: one piece type per pattern
    patterns = []
    for width, qty in demands.items():
        pattern = {width: roll_width // width}  # Maximum pieces of this width
        patterns.append(pattern)

    # Decision variables: number of times to use each pattern
    pattern_vars = LpVariable.dicts("Pattern",
                                    range(len(patterns)),
                                    lowBound=0,
                                    cat='Integer')

    # Objective: Minimize number of rolls used
    master += lpSum([pattern_vars[i] for i in range(len(patterns))]), \
              "Num_Rolls"

    # Constraints: Meet demand for each piece width
    for width, qty in demands.items():
        master += (
            lpSum([patterns[i].get(width, 0) * pattern_vars[i]
                  for i in range(len(patterns))]) >= qty
        ), f"Demand_{width}"

    iteration = 0
    max_iterations = 100

    while iteration < max_iterations:
        iteration += 1

        # Solve master problem
        master.solve(PULP_CBC_CMD(msg=0))

        # Get dual values (shadow prices) from demand constraints
        # This tells us the value of one more unit of each width
        dual_values = {}
        for width in demands.keys():
            # Simplified: would extract from constraint
            dual_values[width] = 1.0  # Placeholder

        # Solve pricing subproblem: find new profitable pattern
        new_pattern = solve_cutting_pricing(dual_values, roll_width, demands.keys())

        # Check if new pattern improves solution
        reduced_cost = 1 - sum([new_pattern.get(w, 0) * dual_values[w]
                               for w in demands.keys()])

        if reduced_cost >= -0.001:  # No improvement
            break

        # Add new pattern to master
        patterns.append(new_pattern)
        new_var = LpVariable(f"Pattern_{len(patterns)-1}",
                           lowBound=0, cat='Integer')
        pattern_vars[len(patterns)-1] = new_var

        # Update master problem
        master.objective = lpSum([pattern_vars[i] for i in range(len(patterns))])

        for width, qty in demands.items():
            constraint_name = f"Demand_{width}"
            # Update constraint with new pattern

    # Extract final solution
    solution = {
        'num_rolls': value(master.objective),
        'patterns_used': {
            i: pattern_vars[i].varValue
            for i in range(len(patterns))
            if pattern_vars[i].varValue > 0.01
        },
        'patterns': patterns,
        'iterations': iteration
    }

    return solution

def solve_cutting_pricing(dual_values, roll_width, piece_widths):
    """
    Pricing subproblem: Find best cutting pattern

    This is a knapsack problem
    """

    sub = LpProblem("Pricing", LpMaximize)

    # Variables: number of pieces of each width in pattern
    pieces = LpVariable.dicts("Pieces",
                             piece_widths,
                             lowBound=0,
                             cat='Integer')

    # Objective: Maximize dual value (profit from this pattern)
    sub += lpSum([dual_values[w] * pieces[w] for w in piece_widths]), \
           "Pattern_Value"

    # Constraint: Don't exceed roll width
    sub += lpSum([w * pieces[w] for w in piece_widths]) <= roll_width, \
           "Roll_Width"

    sub.solve(PULP_CBC_CMD(msg=0))

    new_pattern = {w: int(pieces[w].varValue) for w in piece_widths
                  if pieces[w].varValue > 0.01}

    return new_pattern
```

---

## Tools & Solvers

### Open-Source Solvers

**Linear/Mixed-Integer Programming:**
- **CBC (COIN-OR)**: Open-source MIP solver (default in PuLP)
- **GLPK**: GNU Linear Programming Kit
- **HiGHS**: High-performance LP/MIP solver
- **SCIP**: Solving Constraint Integer Programs

**Nonlinear Programming:**
- **Ipopt**: Interior point optimizer
- **BONMIN**: Basic Open-source Nonlinear MIP
- **CasADi**: Symbolic framework for optimization

### Commercial Solvers

**High-Performance:**
- **Gurobi**: State-of-art MIP solver (free academic license)
- **CPLEX (IBM)**: Industry-standard solver
- **FICO Xpress**: Optimization suite
- **MOSEK**: Conic optimization

**Supply Chain Specific:**
- **AIMMS**: Modeling & optimization platform
- **AMPL**: Algebraic modeling language
- **GAMS**: General Algebraic Modeling System

### Python Modeling Libraries

**Algebraic Modeling:**
- **PuLP**: Simple LP/MIP modeling
- **Pyomo**: Advanced optimization modeling
- **CVXPY**: Convex optimization
- **OR-Tools (Google)**: Constraint programming & optimization
- **scipy.optimize**: Scientific optimization

**Example: Using Pyomo**

```python
from pyomo.environ import *

def production_planning_pyomo():
    """
    Production planning using Pyomo (more advanced than PuLP)
    """

    model = ConcreteModel()

    # Sets
    model.products = Set(initialize=['A', 'B', 'C'])
    model.periods = RangeSet(1, 12)  # 12 months

    # Parameters
    demand = {
        ('A', 1): 100, ('A', 2): 120, ('A', 3): 110,
        ('B', 1): 150, ('B', 2): 160, ('B', 3): 155,
        ('C', 1): 80, ('C', 2): 85, ('C', 3): 90
    }

    model.demand = Param(model.products, model.periods,
                        initialize=demand, default=0)

    model.prod_cost = Param(model.products,
                           initialize={'A': 10, 'B': 15, 'C': 12})

    model.inv_cost = Param(model.products,
                          initialize={'A': 2, 'B': 3, 'C': 2})

    model.capacity = Param(initialize=1000)

    # Variables
    model.produce = Var(model.products, model.periods,
                       domain=NonNegativeReals)

    model.inventory = Var(model.products, model.periods,
                         domain=NonNegativeReals)

    # Objective
    def obj_rule(m):
        return sum(m.prod_cost[p] * m.produce[p,t] +
                  m.inv_cost[p] * m.inventory[p,t]
                  for p in m.products for t in m.periods)

    model.total_cost = Objective(rule=obj_rule, sense=minimize)

    # Constraints
    def capacity_rule(m, t):
        return sum(m.produce[p,t] for p in m.products) <= m.capacity

    model.capacity_constraint = Constraint(model.periods, rule=capacity_rule)

    def inventory_balance_rule(m, p, t):
        if t == 1:
            return m.inventory[p,t] == m.produce[p,t] - m.demand[p,t]
        else:
            return m.inventory[p,t] == (m.inventory[p,t-1] +
                                       m.produce[p,t] -
                                       m.demand[p,t])

    model.inventory_balance = Constraint(model.products, model.periods,
                                        rule=inventory_balance_rule)

    # Solve
    solver = SolverFactory('glpk')  # or 'gurobi', 'cplex'
    results = solver.solve(model, tee=True)

    # Extract results
    production_plan = {}
    for p in model.products:
        for t in model.periods:
            production_plan[(p,t)] = value(model.produce[p,t])

    return {
        'status': results.solver.status,
        'objective': value(model.total_cost),
        'production_plan': production_plan
    }
```

---

## Optimization Modeling Best Practices

### Model Formulation Tips

**1. Problem Decomposition:**
- Break large problems into smaller subproblems
- Use hierarchical decomposition (strategic → tactical → operational)
- Exploit problem structure (network flow, assignment, etc.)

**2. Variable Tightening:**
- Add valid inequalities to strengthen formulation
- Use tighter bounds on variables
- Eliminate symmetry

**3. Big-M Constraints:**
- Avoid large Big-M values (causes numerical issues)
- Calculate tightest possible Big-M
- Consider alternative formulations

**4. Scaling:**
- Normalize objective coefficients (similar magnitude)
- Scale constraints appropriately
- Check constraint matrix condition number

### Computational Performance

**For Large-Scale Problems:**

```python
# Performance tips
def optimize_large_problem():
    """Tips for solving large optimization problems"""

    # 1. Use warm starts
    model.solve(warmstart=True)  # If you have a good initial solution

    # 2. Set time limits
    model.solve(options={'timelimit': 300})  # 5 minutes max

    # 3. Set MIP gap tolerance
    model.solve(options={'mipgap': 0.01})  # Accept 1% optimality gap

    # 4. Use multiple threads
    model.solve(options={'threads': 8})

    # 5. Adjust solver parameters
    model.solve(options={
        'presolve': 2,  # Aggressive presolve
        'cuts': 2,  # Aggressive cuts
        'heuristics': 2  # Aggressive heuristics
    })

    # 6. Use callback functions for custom branching/cutting
    # (advanced, solver-specific)
```

---

## Common Challenges & Solutions

### Challenge: Model Too Large to Solve

**Problem:**
- Millions of variables/constraints
- Exceeds memory or time limits

**Solutions:**
- Decomposition methods (Benders, Dantzig-Wolfe)
- Column generation
- Aggregation (reduce granularity)
- Rolling horizon (solve periods sequentially)
- Heuristic methods (metaheuristics)
- Parallel/distributed optimization

### Challenge: Integer Variables Make Problem Intractable

**Problem:**
- Integer variables create combinatorial explosion
- Branch-and-bound tree too large

**Solutions:**
- LP relaxation for bounds
- Lagrangian relaxation
- Fix-and-optimize heuristics
- Progressive tightening of integrality
- Approximate with continuous variables where possible

### Challenge: Infeasible Model

**Problem:**
- No feasible solution exists
- Constraints are conflicting

**Solutions:**
- Add slack variables to identify infeasibility
- Relax constraints iteratively
- Use Elastic Filter method
- Check data for errors
- Visualize constraints (for small problems)

```python
def find_infeasibility(model):
    """
    Add slack variables to find infeasible constraints
    """

    # Add slack to each constraint
    slacks = {}
    for constraint_name in model.constraints:
        slack_pos = LpVariable(f"Slack_Pos_{constraint_name}", lowBound=0)
        slack_neg = LpVariable(f"Slack_Neg_{constraint_name}", lowBound=0)

        # Modify constraint: original - slack_pos + slack_neg
        # original constraint: expr <= rhs
        # becomes: expr - slack_pos + slack_neg <= rhs

        slacks[constraint_name] = (slack_pos, slack_neg)

    # New objective: Minimize sum of slacks
    model += lpSum([slack_pos + slack_neg
                   for slack_pos, slack_neg in slacks.values()])

    model.solve()

    # Identify constraints with non-zero slack
    infeasible_constraints = []
    for name, (slack_pos, slack_neg) in slacks.items():
        if slack_pos.varValue > 0.01 or slack_neg.varValue > 0.01:
            infeasible_constraints.append({
                'constraint': name,
                'slack': slack_pos.varValue + slack_neg.varValue
            })

    return infeasible_constraints
```

---

## Output Format

### Optimization Report Template

**Executive Summary:**
- Problem description
- Optimal solution found
- Key results and recommendations
- Implementation impact

**Problem Formulation:**
- Decision variables defined
- Objective function
- Constraints listed
- Data sources

**Solution Quality:**

| Metric | Value |
|--------|-------|
| Objective Value | $1,245,678 |
| Optimality Gap | 0.5% |
| Solve Time | 45 seconds |
| Variables | 10,542 |
| Constraints | 8,234 |
| Solver | Gurobi 10.0 |

**Optimal Solution:**
- Decision variable values
- Resource utilization
- Constraint binding analysis

**Sensitivity Analysis:**
- Key parameter ranges
- Shadow prices (dual values)
- Reduced costs
- What-if scenarios

**Implementation Plan:**
- Recommended actions
- Expected savings/improvements
- Risks and mitigation
- Timeline

---

## Questions to Ask

If you need more context:
1. What decision needs to be made?
2. What's being optimized? (minimize cost, maximize profit, maximize service)
3. What can be controlled? (production quantities, facility locations, routes)
4. What constraints exist? (capacity, budget, time, demand)
5. How large is the problem? (number of variables, constraints)
6. Is uncertainty involved? (stochastic or deterministic)
7. What solver access do you have? (open-source or commercial)
8. What's the acceptable solve time?

---

## Related Skills

- **network-design**: For supply chain network optimization
- **facility-location-problem**: For facility location models
- **route-optimization**: For vehicle routing
- **production-scheduling**: For manufacturing optimization
- **inventory-optimization**: For inventory policy optimization
- **prescriptive-analytics**: For optimization-based recommendations
- **supply-chain-analytics**: For KPI tracking post-optimization
- **digital-twin-modeling**: For simulation-optimization integration
