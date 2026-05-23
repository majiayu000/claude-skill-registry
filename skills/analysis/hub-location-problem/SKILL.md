---
name: hub-location-problem
description: When the user wants to solve hub location problems, design hub-and-spoke networks, optimize hub placement for logistics networks. Also use when the user mentions "hub location," "hub-and-spoke," "p-hub median," "hub covering," "single allocation hub," "multiple allocation hub," "airline hub network," "postal hub network," or "consolidation center location." For general facility location, see facility-location-problem. For distribution centers, see distribution-center-network.
---

# Hub Location Problem

You are an expert in hub location problems and hub-and-spoke network design. Your goal is to help design efficient hub-and-spoke networks where flows between origin-destination pairs are consolidated through hub facilities, minimizing total transportation and routing costs.

## Initial Assessment

Before solving hub location problems, understand:

1. **Network Type**
   - Hub-and-spoke network? (consolidation through hubs)
   - How many hubs to locate? (p-hub problem)
   - Hub covering problem? (coverage requirements)
   - Hub hierarchy? (multi-level hubs)

2. **Allocation Type**
   - Single allocation? (each node assigned to exactly one hub)
   - Multiple allocation? (nodes can connect to multiple hubs)
   - r-allocation? (each node connects to at most r hubs)

3. **Flow Characteristics**
   - Origin-destination (O-D) flow matrix?
   - Demand between all pairs?
   - Flow volumes/patterns?
   - Directionality (symmetric or asymmetric)?

4. **Hub Characteristics**
   - Hub capacity constraints?
   - Fixed costs to establish hubs?
   - Hub processing/handling costs?
   - Economies of scale at hubs?
   - Discount factor (α) for inter-hub connections?

5. **Network Objectives**
   - Minimize total transportation cost?
   - Minimize maximum travel time? (p-hub center)
   - Minimize number of hubs?
   - Balance hub loads?

---

## Hub Location Problem Framework

### Hub-and-Spoke Network Concept

**Structure:**
```
Origin → Access Hub → Hub-to-Hub → Egress Hub → Destination

Collection   |  Consolidation  |   Distribution
   Leg       |      Leg        |      Leg
```

**Key Features:**
- **Consolidation**: Flows between O-D pairs routed through hubs
- **Economies of Scale**: Inter-hub transport cheaper (discount factor α)
- **Hub Facilities**: Special facilities with sorting/consolidation capability
- **Reduced Connections**: Not all nodes directly connected

**Applications:**
- Airline passenger networks
- Cargo/freight networks
- Postal/package delivery
- Telecommunications networks
- Supply chain distribution
- Public transportation

---

## Problem Classification

### 1. p-Hub Median Problem (pHMP)

**Description:**
- Locate exactly p hubs
- Minimize total transportation cost
- Most common hub location variant

**Variants:**
- **Single Allocation (SA-pHMP)**: Each non-hub node connected to exactly one hub
- **Multiple Allocation (MA-pHMP)**: Non-hub nodes can connect to multiple hubs

**Characteristics:**
- Fixed number of hubs (p)
- Cost minimization
- Network efficiency focus

### 2. Hub Covering Problem

**Description:**
- Cover all O-D pairs within distance/time threshold
- Minimize number of hubs needed

**Applications:**
- Emergency service networks
- Time-sensitive delivery
- Service quality guarantees

### 3. p-Hub Center Problem

**Description:**
- Minimize maximum O-D distance/cost
- Equity-focused objective
- Ensure no O-D pair has excessive cost

**Applications:**
- Emergency response
- Equal service quality
- Fair network design

### 4. Hub Arc Location Problem

**Description:**
- Decide which inter-hub connections to establish
- Not all hubs necessarily connected
- Trade-off connectivity vs. cost

### 5. Hierarchical Hub Location

**Description:**
- Multiple levels of hubs (regional, national, international)
- Flows cascade through hierarchy
- Complex multi-tier networks

---

## Mathematical Formulations

### Single Allocation p-Hub Median Problem (SA-pHMP)

**Sets:**
- N = {1, ..., n}: Set of nodes (potential hubs and non-hubs)

**Parameters:**
- w_{ij}: Flow from node i to node j
- c_{ij}: Unit cost from node i to node j
- α: Inter-hub discount factor (typically 0.2 - 0.8)
- p: Number of hubs to locate

**Decision Variables:**
- y_k ∈ {0,1}: 1 if node k is a hub, 0 otherwise
- x_{ik} ∈ {0,1}: 1 if node i is allocated to hub k, 0 otherwise

**Cost Structure:**
```
For flow from i to j allocated to hubs k and m:
- Collection: c_{ik} (origin to hub)
- Transfer: α × c_{km} (hub to hub, discounted)
- Distribution: c_{mj} (hub to destination)

Total: c_{ik} + α × c_{km} + c_{mj}
```

**Objective Function:**
```
Minimize: Σ_i Σ_j Σ_k Σ_m w_{ij} × (c_{ik} + α×c_{km} + c_{mj}) × x_{ik} × x_{jm}
```

**Constraints:**
```
1. Each node allocated to exactly one hub:
   Σ_k x_{ik} = 1,  ∀i ∈ N

2. Exactly p hubs located:
   Σ_k y_k = p

3. Allocation only to hubs:
   x_{ik} ≤ y_k,  ∀i ∈ N, ∀k ∈ N

4. Hubs allocated to themselves:
   x_{kk} = y_k,  ∀k ∈ N

5. Binary variables:
   y_k ∈ {0,1},  ∀k ∈ N
   x_{ik} ∈ {0,1},  ∀i,k ∈ N
```

**Complexity:** NP-hard

### Multiple Allocation p-Hub Median Problem (MA-pHMP)

**Modified Variables:**
- x_{ikm} ∈ [0,1]: Fraction of flow from i to j through hubs k and m

**Objective:**
```
Minimize: Σ_i Σ_j Σ_k Σ_m w_{ij} × (c_{ik} + α×c_{km} + c_{mj}) × x_{ikm}
```

**Key Constraints:**
```
1. Flow conservation:
   Σ_k Σ_m x_{ikm} = 1,  ∀i,j ∈ N

2. Exactly p hubs:
   Σ_k y_k = p

3. Flow only through hubs:
   x_{ikm} ≤ y_k,  ∀i,j,k,m
   x_{ikm} ≤ y_m,  ∀i,j,k,m
```

---

## Exact Solution Methods

### 1. Single Allocation p-Hub Median (PuLP)

```python
from pulp import *
import numpy as np

def solve_single_allocation_phub(flows, costs, p, alpha=0.75):
    """
    Solve Single Allocation p-Hub Median Problem

    Args:
        flows: n x n matrix of flows between O-D pairs
        costs: n x n matrix of unit transportation costs
        p: number of hubs to locate
        alpha: inter-hub discount factor (0 < α < 1)

    Returns:
        optimal hub location and allocation solution
    """
    n = len(flows)

    # Create problem
    prob = LpProblem("Single_Allocation_pHub_Median", LpMinimize)

    # Decision variables
    # y[k] = 1 if node k is a hub
    y = LpVariable.dicts("hub", range(n), cat='Binary')

    # x[i,k] = 1 if node i is allocated to hub k
    x = LpVariable.dicts("allocation",
                         [(i, k) for i in range(n) for k in range(n)],
                         cat='Binary')

    # Objective: Minimize total weighted transportation cost
    # Cost for flow from i to j through hubs k and m:
    # c_ik + alpha*c_km + c_mj
    objective = []

    for i in range(n):
        for j in range(n):
            if i == j or flows[i][j] == 0:
                continue

            for k in range(n):
                for m in range(n):
                    cost_ij_via_km = (costs[i][k] +
                                     alpha * costs[k][m] +
                                     costs[m][j])

                    objective.append(
                        flows[i][j] * cost_ij_via_km * x[i,k] * x[j,m]
                    )

    prob += lpSum(objective), "Total_Transportation_Cost"

    # Constraints

    # 1. Each node allocated to exactly one hub
    for i in range(n):
        prob += (
            lpSum([x[i,k] for k in range(n)]) == 1,
            f"Allocation_{i}"
        )

    # 2. Exactly p hubs located
    prob += (
        lpSum([y[k] for k in range(n)]) == p,
        "p_Hubs"
    )

    # 3. Can only allocate to hubs
    for i in range(n):
        for k in range(n):
            prob += (
                x[i,k] <= y[k],
                f"Allocation_to_Hub_{i}_{k}"
            )

    # 4. Hubs must be allocated to themselves
    for k in range(n):
        prob += (
            x[k,k] == y[k],
            f"Hub_Self_Allocation_{k}"
        )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=600))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        hubs = [k for k in range(n) if y[k].varValue > 0.5]

        allocations = {}
        for i in range(n):
            for k in range(n):
                if x[i,k].varValue > 0.5:
                    allocations[i] = k
                    break

        # Calculate flows through each hub
        hub_inflow = {k: 0 for k in hubs}
        hub_outflow = {k: 0 for k in hubs}

        for i in range(n):
            for j in range(n):
                if i != j and flows[i][j] > 0:
                    hub_i = allocations[i]
                    hub_j = allocations[j]

                    hub_outflow[hub_i] += flows[i][j]
                    hub_inflow[hub_j] += flows[i][j]

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'hubs': hubs,
            'num_hubs': len(hubs),
            'allocations': allocations,
            'hub_inflow': hub_inflow,
            'hub_outflow': hub_outflow,
            'solve_time': solve_time,
            'alpha': alpha
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    np.random.seed(42)

    # 10-node network
    n = 10

    # Generate random coordinates
    coords = np.random.rand(n, 2) * 100

    # Calculate Euclidean distance matrix
    costs = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            costs[i][j] = np.linalg.norm(coords[i] - coords[j])

    # Generate flow matrix (random demands)
    flows = np.random.uniform(10, 100, (n, n))
    np.fill_diagonal(flows, 0)  # No self-flow

    # Parameters
    p = 3  # Number of hubs
    alpha = 0.75  # Inter-hub discount factor

    print(f"{'='*70}")
    print(f"SINGLE ALLOCATION p-HUB MEDIAN PROBLEM")
    print(f"{'='*70}")
    print(f"Nodes: {n}")
    print(f"Hubs to locate: {p}")
    print(f"Inter-hub discount factor: {alpha}")
    print(f"Total O-D flow: {flows.sum():.2f}")

    result = solve_single_allocation_phub(flows, costs, p, alpha)

    print(f"\n{'='*70}")
    print(f"SOLUTION")
    print(f"{'='*70}")
    print(f"Status: {result['status']}")
    print(f"Total Cost: {result['total_cost']:,.2f}")
    print(f"Hubs Located: {result['hubs']}")
    print(f"Solve Time: {result['solve_time']:.2f} seconds")

    print(f"\nNode Allocations:")
    for node, hub in result['allocations'].items():
        hub_indicator = " (HUB)" if node in result['hubs'] else ""
        print(f"  Node {node} → Hub {hub}{hub_indicator}")

    print(f"\nHub Traffic:")
    for hub in result['hubs']:
        print(f"  Hub {hub}:")
        print(f"    Inflow: {result['hub_inflow'][hub]:.2f}")
        print(f"    Outflow: {result['hub_outflow'][hub]:.2f}")
        print(f"    Total: {result['hub_inflow'][hub] + result['hub_outflow'][hub]:.2f}")
```

### 2. Multiple Allocation p-Hub Median

```python
def solve_multiple_allocation_phub(flows, costs, p, alpha=0.75):
    """
    Solve Multiple Allocation p-Hub Median Problem

    Allows each node to send/receive flows through multiple hubs

    Args:
        flows: n x n flow matrix
        costs: n x n cost matrix
        p: number of hubs
        alpha: inter-hub discount factor

    Returns:
        optimal solution
    """
    n = len(flows)

    prob = LpProblem("Multiple_Allocation_pHub_Median", LpMinimize)

    # Decision variables
    y = LpVariable.dicts("hub", range(n), cat='Binary')

    # x[i,j,k,m] = fraction of flow from i to j through hubs k and m
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0:
                for k in range(n):
                    for m in range(n):
                        x[i,j,k,m] = LpVariable(f"flow_{i}_{j}_{k}_{m}",
                                               lowBound=0, upBound=1,
                                               cat='Continuous')

    # Objective: Minimize total cost
    objective = []
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0:
                for k in range(n):
                    for m in range(n):
                        cost_via_km = (costs[i][k] +
                                      alpha * costs[k][m] +
                                      costs[m][j])

                        objective.append(
                            flows[i][j] * cost_via_km * x[i,j,k,m]
                        )

    prob += lpSum(objective), "Total_Cost"

    # Constraints

    # 1. Flow conservation: all flow from i to j routed through some hub pair
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0:
                prob += (
                    lpSum([x[i,j,k,m] for k in range(n) for m in range(n)]) == 1,
                    f"Flow_{i}_{j}"
                )

    # 2. Exactly p hubs
    prob += (
        lpSum([y[k] for k in range(n)]) == p,
        "p_Hubs"
    )

    # 3. Flow only through open hubs
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0:
                for k in range(n):
                    for m in range(n):
                        prob += (
                            x[i,j,k,m] <= y[k],
                            f"Hub_k_{i}_{j}_{k}_{m}"
                        )
                        prob += (
                            x[i,j,k,m] <= y[m],
                            f"Hub_m_{i}_{j}_{k}_{m}"
                        )

    # Solve
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=600))
    solve_time = time.time() - start_time

    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        hubs = [k for k in range(n) if y[k].varValue > 0.5]

        # Extract flow routing
        flow_routing = {}
        for i in range(n):
            for j in range(n):
                if i != j and flows[i][j] > 0:
                    flow_routing[i,j] = []
                    for k in range(n):
                        for m in range(n):
                            if x[i,j,k,m].varValue > 0.01:
                                flow_routing[i,j].append({
                                    'via_hubs': (k, m),
                                    'fraction': x[i,j,k,m].varValue,
                                    'flow': flows[i][j] * x[i,j,k,m].varValue
                                })

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'hubs': hubs,
            'flow_routing': flow_routing,
            'solve_time': solve_time,
            'alpha': alpha
        }
    else:
        return {'status': LpStatus[prob.status]}


# Example usage
result_ma = solve_multiple_allocation_phub(flows, costs, p=3, alpha=0.75)

print(f"\n{'='*70}")
print(f"MULTIPLE ALLOCATION p-HUB MEDIAN SOLUTION")
print(f"{'='*70}")
print(f"Status: {result_ma['status']}")
print(f"Total Cost: {result_ma['total_cost']:,.2f}")
print(f"Hubs: {result_ma['hubs']}")

print(f"\nSample Flow Routing (first 5 O-D pairs):")
count = 0
for (i, j), routing in result_ma['flow_routing'].items():
    if count >= 5:
        break
    print(f"  Flow {i}→{j} (total={flows[i][j]:.2f}):")
    for route in routing:
        via_k, via_m = route['via_hubs']
        print(f"    via hubs ({via_k}, {via_m}): "
              f"{route['fraction']*100:.1f}% ({route['flow']:.2f} units)")
    count += 1
```

---

## Greedy Heuristics

### 1. Greedy Hub Selection

```python
def greedy_hub_selection(flows, costs, p, alpha=0.75):
    """
    Greedy heuristic for p-Hub Median

    Iteratively select hub that gives maximum cost reduction

    Args:
        flows: flow matrix
        costs: cost matrix
        p: number of hubs
        alpha: inter-hub discount

    Returns:
        heuristic solution
    """
    n = len(flows)

    hubs = []
    allocations = {}

    def calculate_cost(current_hubs):
        """Calculate total cost for given hub set"""
        if not current_hubs:
            return float('inf')

        # Allocate each node to nearest hub
        node_allocations = {}
        for i in range(n):
            nearest_hub = min(current_hubs, key=lambda k: costs[i][k])
            node_allocations[i] = nearest_hub

        # Calculate total cost
        total_cost = 0
        for i in range(n):
            for j in range(n):
                if i != j and flows[i][j] > 0:
                    hub_i = node_allocations[i]
                    hub_j = node_allocations[j]

                    cost = (costs[i][hub_i] +
                           alpha * costs[hub_i][hub_j] +
                           costs[hub_j][j])

                    total_cost += flows[i][j] * cost

        return total_cost, node_allocations

    # Greedily select p hubs
    for iteration in range(p):
        best_hub = None
        best_cost = float('inf')
        best_allocations = None

        # Try adding each remaining node as a hub
        for k in range(n):
            if k in hubs:
                continue

            test_hubs = hubs + [k]
            cost, allocations_test = calculate_cost(test_hubs)

            if cost < best_cost:
                best_cost = cost
                best_hub = k
                best_allocations = allocations_test

        if best_hub is not None:
            hubs.append(best_hub)
            allocations = best_allocations

    return {
        'hubs': hubs,
        'allocations': allocations,
        'total_cost': best_cost,
        'method': 'Greedy Hub Selection'
    }
```

### 2. Concentration-Based Heuristic

```python
def concentration_heuristic(flows, costs, p, alpha=0.75):
    """
    Concentration-based heuristic for hub location

    Select nodes with highest total flow (originating + terminating)

    Args:
        flows: flow matrix
        costs: cost matrix
        p: number of hubs
        alpha: inter-hub discount

    Returns:
        heuristic solution
    """
    n = len(flows)

    # Calculate total flow for each node
    node_flows = []
    for i in range(n):
        total_flow = flows[i, :].sum() + flows[:, i].sum()
        node_flows.append((total_flow, i))

    # Sort by flow (descending)
    node_flows.sort(reverse=True)

    # Select top p nodes as hubs
    hubs = [node for _, node in node_flows[:p]]

    # Allocate each node to nearest hub
    allocations = {}
    for i in range(n):
        nearest_hub = min(hubs, key=lambda k: costs[i][k])
        allocations[i] = nearest_hub

    # Calculate total cost
    total_cost = 0
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0:
                hub_i = allocations[i]
                hub_j = allocations[j]

                cost = (costs[i][hub_i] +
                       alpha * costs[hub_i][hub_j] +
                       costs[hub_j][j])

                total_cost += flows[i][j] * cost

    return {
        'hubs': hubs,
        'allocations': allocations,
        'total_cost': total_cost,
        'method': 'Concentration Heuristic'
    }
```

---

## Local Search Improvements

### 1. Hub Swap Local Search

```python
def hub_swap_local_search(flows, costs, initial_hubs, alpha=0.75,
                         max_iterations=100):
    """
    Local search with hub swap moves

    Swap a hub with a non-hub if it improves objective

    Args:
        flows: flow matrix
        costs: cost matrix
        initial_hubs: initial hub locations
        alpha: inter-hub discount
        max_iterations: maximum iterations

    Returns:
        improved solution
    """
    n = len(flows)

    current_hubs = set(initial_hubs)
    non_hubs = set(range(n)) - current_hubs

    def evaluate_solution(hub_set):
        """Evaluate cost for given hub configuration"""
        # Allocate nodes
        allocations = {}
        for i in range(n):
            allocations[i] = min(hub_set, key=lambda k: costs[i][k])

        # Calculate cost
        total_cost = 0
        for i in range(n):
            for j in range(n):
                if i != j and flows[i][j] > 0:
                    hub_i = allocations[i]
                    hub_j = allocations[j]

                    cost = (costs[i][hub_i] +
                           alpha * costs[hub_i][hub_j] +
                           costs[hub_j][j])

                    total_cost += flows[i][j] * cost

        return total_cost, allocations

    current_cost, current_allocations = evaluate_solution(current_hubs)
    best_hubs = current_hubs.copy()
    best_cost = current_cost
    best_allocations = current_allocations

    for iteration in range(max_iterations):
        improved = False

        # Try all possible swaps
        for hub_out in list(current_hubs):
            for hub_in in non_hubs:
                # Test swap
                test_hubs = (current_hubs - {hub_out}) | {hub_in}
                test_cost, test_allocations = evaluate_solution(test_hubs)

                if test_cost < best_cost - 1e-6:
                    best_cost = test_cost
                    best_hubs = test_hubs
                    best_allocations = test_allocations
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

        # Update current solution
        current_hubs = best_hubs.copy()
        non_hubs = set(range(n)) - current_hubs

    return {
        'hubs': list(best_hubs),
        'allocations': best_allocations,
        'total_cost': best_cost,
        'method': 'Hub Swap Local Search'
    }
```

---

## Metaheuristics

### 1. Simulated Annealing for Hub Location

```python
import random
import math

def simulated_annealing_hub(flows, costs, p, alpha=0.75,
                           initial_temp=1000, cooling_rate=0.95,
                           max_iterations=5000):
    """
    Simulated Annealing for p-Hub Median

    Args:
        flows: flow matrix
        costs: cost matrix
        p: number of hubs
        alpha: inter-hub discount
        initial_temp: starting temperature
        cooling_rate: cooling factor
        max_iterations: max iterations

    Returns:
        best solution found
    """
    n = len(flows)

    def evaluate(hub_set):
        """Calculate cost for hub configuration"""
        allocations = {}
        for i in range(n):
            allocations[i] = min(hub_set, key=lambda k: costs[i][k])

        total_cost = 0
        for i in range(n):
            for j in range(n):
                if i != j and flows[i][j] > 0:
                    hub_i = allocations[i]
                    hub_j = allocations[j]

                    cost = (costs[i][hub_i] +
                           alpha * costs[hub_i][hub_j] +
                           costs[hub_j][j])

                    total_cost += flows[i][j] * cost

        return total_cost, allocations

    # Initial solution: random hubs
    current_hubs = set(random.sample(range(n), p))
    current_cost, current_allocations = evaluate(current_hubs)

    best_hubs = current_hubs.copy()
    best_cost = current_cost
    best_allocations = current_allocations

    temperature = initial_temp

    for iteration in range(max_iterations):
        # Generate neighbor: swap one hub
        non_hubs = list(set(range(n)) - current_hubs)

        hub_out = random.choice(list(current_hubs))
        hub_in = random.choice(non_hubs)

        neighbor_hubs = (current_hubs - {hub_out}) | {hub_in}
        neighbor_cost, neighbor_allocations = evaluate(neighbor_hubs)

        delta = neighbor_cost - current_cost

        # Accept or reject
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_hubs = neighbor_hubs
            current_cost = neighbor_cost
            current_allocations = neighbor_allocations

            if current_cost < best_cost:
                best_hubs = current_hubs.copy()
                best_cost = current_cost
                best_allocations = current_allocations

        # Cool down
        temperature *= cooling_rate

        if temperature < 0.1:
            break

    return {
        'hubs': list(best_hubs),
        'allocations': best_allocations,
        'total_cost': best_cost,
        'method': 'Simulated Annealing'
    }
```

---

## Complete Hub Location Solver

```python
class HubLocationSolver:
    """
    Comprehensive Hub Location Problem Solver

    Supports single/multiple allocation, various solution methods
    """

    def __init__(self):
        self.flows = None
        self.costs = None
        self.coords = None
        self.n = None

    def load_problem(self, flows, costs, coords=None):
        """
        Load problem data

        Args:
            flows: n x n flow matrix
            costs: n x n cost matrix
            coords: optional node coordinates for visualization
        """
        self.flows = np.array(flows)
        self.costs = np.array(costs)
        self.coords = np.array(coords) if coords is not None else None
        self.n = len(flows)

        print(f"Loaded hub location problem:")
        print(f"  Nodes: {self.n}")
        print(f"  Total O-D flow: {self.flows.sum():.2f}")
        print(f"  Average cost: {self.costs.mean():.2f}")

    def solve_exact_sa(self, p, alpha=0.75, time_limit=600):
        """Solve single allocation with exact MIP"""
        print(f"\nSolving Single Allocation p-Hub Median (exact)...")
        return solve_single_allocation_phub(self.flows, self.costs, p, alpha)

    def solve_exact_ma(self, p, alpha=0.75, time_limit=600):
        """Solve multiple allocation with exact MIP"""
        print(f"\nSolving Multiple Allocation p-Hub Median (exact)...")
        return solve_multiple_allocation_phub(self.flows, self.costs, p, alpha)

    def solve_heuristic(self, method, p, alpha=0.75):
        """
        Solve with heuristic method

        Args:
            method: 'greedy', 'concentration', 'sa' (simulated annealing)
            p: number of hubs
            alpha: inter-hub discount

        Returns:
            heuristic solution
        """
        print(f"\nSolving with {method} heuristic...")

        if method == 'greedy':
            return greedy_hub_selection(self.flows, self.costs, p, alpha)
        elif method == 'concentration':
            return concentration_heuristic(self.flows, self.costs, p, alpha)
        elif method == 'sa':
            return simulated_annealing_hub(self.flows, self.costs, p, alpha)
        else:
            raise ValueError(f"Unknown method: {method}")

    def compare_methods(self, p, alpha=0.75,
                       methods=['greedy', 'concentration', 'sa', 'exact_sa']):
        """
        Compare multiple solution methods

        Args:
            p: number of hubs
            alpha: inter-hub discount
            methods: list of methods to compare

        Returns:
            comparison dataframe
        """
        import pandas as pd
        import time

        results = []

        for method in methods:
            start_time = time.time()

            try:
                if method == 'exact_sa':
                    solution = self.solve_exact_sa(p, alpha)
                elif method == 'exact_ma':
                    solution = self.solve_exact_ma(p, alpha)
                else:
                    solution = self.solve_heuristic(method, p, alpha)

                solve_time = time.time() - start_time

                results.append({
                    'Method': method,
                    'Total Cost': solution['total_cost'],
                    'Hubs': str(solution['hubs']),
                    'Time (s)': f"{solve_time:.3f}"
                })

            except Exception as e:
                print(f"  Error with {method}: {e}")

        df = pd.DataFrame(results)

        # Calculate gap from best
        if len(df) > 0:
            best_cost = df['Total Cost'].min()
            df['Gap %'] = ((df['Total Cost'] - best_cost) / best_cost * 100).round(2)

        return df

    def visualize_hub_network(self, solution, title="Hub Network"):
        """
        Visualize hub-and-spoke network

        Args:
            solution: solution dictionary with hubs and allocations
            title: plot title
        """
        import matplotlib.pyplot as plt

        if self.coords is None:
            print("No coordinates available for visualization")
            return

        plt.figure(figsize=(12, 8))

        hubs = solution['hubs']
        allocations = solution['allocations']

        # Plot non-hub nodes (small blue circles)
        for i in range(self.n):
            if i not in hubs:
                plt.plot(self.coords[i, 0], self.coords[i, 1],
                        'o', color='lightblue', markersize=8)

        # Plot connections (spoke lines)
        for node, hub in allocations.items():
            if node not in hubs:
                plt.plot([self.coords[node, 0], self.coords[hub, 0]],
                        [self.coords[node, 1], self.coords[hub, 1]],
                        'k-', alpha=0.2, linewidth=0.5)

        # Plot inter-hub connections (thick red lines)
        for i, hub_i in enumerate(hubs):
            for hub_j in hubs[i+1:]:
                plt.plot([self.coords[hub_i, 0], self.coords[hub_j, 0]],
                        [self.coords[hub_i, 1], self.coords[hub_j, 1]],
                        'r-', alpha=0.6, linewidth=2)

        # Plot hub nodes (large red squares)
        for hub in hubs:
            plt.plot(self.coords[hub, 0], self.coords[hub, 1],
                    's', color='red', markersize=15, label='Hub' if hub == hubs[0] else '')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


# Complete example
if __name__ == "__main__":
    print("="*70)
    print("HUB LOCATION PROBLEM - COMPREHENSIVE EXAMPLE")
    print("="*70)

    # Generate problem data
    np.random.seed(42)
    n = 15

    # Node coordinates
    coords = np.random.rand(n, 2) * 100

    # Cost matrix (Euclidean distances)
    costs = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            costs[i][j] = np.linalg.norm(coords[i] - coords[j])

    # Flow matrix (random demands)
    flows = np.random.uniform(10, 100, (n, n))
    np.fill_diagonal(flows, 0)

    # Parameters
    p = 3  # Number of hubs
    alpha = 0.75  # Inter-hub discount (25% discount on hub-to-hub travel)

    # Create solver
    solver = HubLocationSolver()
    solver.load_problem(flows, costs, coords)

    # Compare methods
    print(f"\n{'='*70}")
    print(f"COMPARING SOLUTION METHODS (p={p}, α={alpha})")
    print(f"{'='*70}")

    comparison = solver.compare_methods(p, alpha,
                                       methods=['greedy', 'concentration', 'sa'])
    print("\n" + comparison.to_string(index=False))

    # Solve with best method and visualize
    print(f"\n{'='*70}")
    print(f"DETAILED SOLUTION")
    print(f"{'='*70}")

    solution = solver.solve_heuristic('greedy', p, alpha)

    print(f"\nHubs Located: {solution['hubs']}")
    print(f"Total Cost: {solution['total_cost']:,.2f}")

    print(f"\nNode Allocations:")
    for node, hub in solution['allocations'].items():
        hub_indicator = " (HUB)" if node in solution['hubs'] else ""
        distance = costs[node][hub]
        print(f"  Node {node} → Hub {hub}{hub_indicator} (distance={distance:.2f})")

    # Visualize
    solver.visualize_hub_network(solution,
                                title=f"Hub Network: {solution['method']} (p={p}, α={alpha})")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **PuLP**: MIP modeling for hub location
- **Pyomo**: Advanced optimization
- **OR-Tools**: Google optimization tools
- **Gurobi/CPLEX**: Commercial solvers

**Network Analysis:**
- **NetworkX**: Graph algorithms and visualization
- **igraph**: Fast network analysis

**Visualization:**
- **matplotlib**: Basic plotting
- **plotly**: Interactive network visualization
- **folium**: Geographic maps

### Specialized Tools

- **HubLocator**: Academic hub location software
- **SITATION**: Network design software

---

## Common Challenges & Solutions

### Challenge: Problem Size

**Problem:**
- Large networks (100+ nodes)
- Exact methods too slow
- Many O-D pairs

**Solutions:**
- Use heuristics (greedy, concentration)
- Metaheuristics (SA, GA, Tabu Search)
- Decomposition approaches
- Lagrangian relaxation
- Column generation

### Challenge: Multiple Allocation Complexity

**Problem:**
- MA-pHMP has more variables than SA-pHMP
- Harder to solve optimally
- Better solutions but higher computational cost

**Solutions:**
- Use SA-pHMP as approximation
- Restricted multiple allocation (limit connections per node)
- Start with SA solution, refine to MA
- Time limits with commercial solvers

### Challenge: Determining Number of Hubs (p)

**Problem:**
- Don't know optimal p
- Trade-off between hub costs and routing efficiency

**Solutions:**
- Solve for multiple values of p
- Plot cost vs. p curve
- Consider fixed costs explicitly
- Sensitivity analysis
- Use uncapacitated hub location (no fixed p)

### Challenge: Uncertain Demand

**Problem:**
- Flow patterns uncertain or time-varying
- Hub locations long-term strategic decisions

**Solutions:**
- Robust optimization
- Stochastic programming
- Scenario-based analysis
- Flexible/modular hub design
- Multi-period models

---

## Output Format

### Hub Location Solution Report

**Problem Instance:**
- Network: 25 nodes
- Hubs to locate: 4
- Inter-hub discount: α = 0.75 (25% discount)
- Allocation: Single Allocation
- Total O-D flow: 12,450 units

**Optimal Solution:**

| Metric | Value |
|--------|-------|
| Total Cost | $1,247,385 |
| Solution Method | MIP Optimal |
| Hubs Located | {5, 12, 18, 23} |
| Solution Time | 45.3 seconds |
| Status | Optimal |

**Hub Details:**

| Hub ID | Location | Nodes Allocated | Total Inflow | Total Outflow |
|--------|----------|-----------------|--------------|---------------|
| 5 | (34.5, 67.2) | 7 | 3,240 | 3,180 |
| 12 | (78.3, 23.8) | 6 | 2,890 | 2,950 |
| 18 | (12.7, 89.1) | 5 | 2,450 | 2,520 |
| 23 | (56.4, 45.3) | 7 | 3,870 | 3,800 |

**Cost Breakdown:**
- Collection costs (nodes → hubs): $412,450 (33.1%)
- Inter-hub transfer: $298,120 (23.9%)
- Distribution costs (hubs → nodes): $536,815 (43.0%)

**Network Statistics:**
- Average distance to nearest hub: 15.3 km
- Maximum distance to hub: 28.7 km
- Average inter-hub distance: 52.4 km

---

## Questions to Ask

1. What type of network? (freight, passenger, postal, telecom)
2. How many nodes in the network?
3. Do you have O-D flow data?
4. How many hubs should be located? (or should this be optimized?)
5. Single allocation or multiple allocation?
6. What is the inter-hub discount factor (α)?
7. Are there capacity constraints at hubs?
8. Fixed costs to establish hubs?
9. Do you have coordinates or distance/cost matrix?
10. Are flows symmetric or directional?
11. Time-sensitive constraints?
12. Is this strategic (long-term) or tactical planning?

---

## Related Skills

- **facility-location-problem**: General facility location
- **distribution-center-network**: DC network design
- **warehouse-location-optimization**: Warehouse siting
- **network-design**: General supply chain network
- **network-flow-optimization**: Flow optimization
- **set-covering-problem**: Coverage-based location
- **vehicle-routing-problem**: Last-mile routing from hubs
- **optimization-modeling**: MIP formulation techniques
- **multi-objective-optimization**: Multi-criteria hub location
