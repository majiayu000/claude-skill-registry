---
name: set-covering-problem
description: When the user wants to solve set covering problems, determine minimum coverage sets, or optimize facility coverage. Also use when the user mentions "set cover," "minimum set cover," "coverage optimization," "facility coverage problem," "service coverage," "location set covering," "maximal covering location problem," or "covering design." For general facility location, see facility-location-problem. For specific applications, see warehouse-location-optimization or hub-location-problem.
---

# Set Covering Problem

You are an expert in set covering problems and coverage-based optimization. Your goal is to help find the minimum cost collection of sets (or facilities) that covers all required elements (or customers), commonly used for facility location, service coverage, and resource allocation problems.

## Initial Assessment

Before solving set covering problems, understand:

1. **Problem Type**
   - Set Covering Problem (SCP)? (cover all elements with minimum cost)
   - Maximal Covering Location Problem (MCLP)? (maximize covered demand with limited resources)
   - Location Set Covering Problem (LSCP)? (minimum facilities for full coverage)
   - Partial Set Covering? (cover a percentage of elements)
   - Redundant Coverage? (elements covered multiple times)

2. **Coverage Requirements**
   - Must cover all elements? (100% coverage)
   - Partial coverage acceptable? (e.g., 95%)
   - Coverage distance/time threshold?
   - Redundancy requirements? (backup coverage)
   - Quality of coverage (single vs. multiple cover)?

3. **Elements to Cover**
   - What needs to be covered? (customers, demand points, areas)
   - How many elements?
   - Weights/priorities for elements?
   - Geographic locations?
   - Time-dependent coverage needs?

4. **Coverage Sets/Facilities**
   - How many potential covering sets/facilities?
   - Cost structure? (fixed costs, variable costs)
   - Coverage radius or service area?
   - Capacity constraints?
   - Can sets/facilities overlap in coverage?

5. **Objectives**
   - Minimize number of facilities?
   - Minimize total cost?
   - Maximize covered demand (with budget)?
   - Balance coverage and cost?
   - Ensure redundancy for reliability?

---

## Set Covering Problem Framework

### Problem Variants

**1. Basic Set Covering Problem (SCP)**
- **Goal**: Cover all elements with minimum cost
- **Constraint**: Every element must be covered at least once
- **Application**: Emergency service location, sensor placement

**2. Location Set Covering Problem (LSCP)**
- **Goal**: Minimize number of facilities for full coverage
- **Constraint**: All demand points within coverage distance
- **Application**: Fire station, ambulance location

**3. Maximal Covering Location Problem (MCLP)**
- **Goal**: Maximize demand covered with limited facilities
- **Constraint**: Can only open p facilities
- **Application**: Retail location with budget constraint

**4. Partial Set Covering**
- **Goal**: Minimize cost while covering at least α% of elements
- **Constraint**: α ≤ coverage ≤ 100%
- **Application**: Cost-effective service coverage

**5. Redundant Coverage (Backup Coverage)**
- **Goal**: Ensure elements covered by multiple facilities
- **Constraint**: Each element covered by at least k facilities
- **Application**: Reliable emergency response, fault-tolerant networks

---

## Mathematical Formulations

### Basic Set Covering Problem (SCP)

**Sets:**
- I = {1, ..., n}: Set of elements to be covered
- J = {1, ..., m}: Set of potential covering sets/facilities

**Parameters:**
- c_j: Cost of selecting set/facility j
- a_{ij}: Coverage coefficient (1 if set j covers element i, 0 otherwise)

**Decision Variables:**
- x_j ∈ {0,1}: 1 if set j is selected, 0 otherwise

**Objective Function:**
```
Minimize: Σ_{j=1}^m c_j × x_j
```

**Constraints:**
```
1. Coverage: Every element must be covered
   Σ_{j:a_{ij}=1} x_j ≥ 1,  ∀i ∈ I

   Or equivalently:
   Σ_{j=1}^m a_{ij} × x_j ≥ 1,  ∀i ∈ I

2. Binary variables:
   x_j ∈ {0,1},  ∀j ∈ J
```

**Complexity:** NP-complete

### Location Set Covering Problem (LSCP)

**Parameters:**
- d_{ij}: Distance from facility site j to demand point i
- S: Maximum service distance (coverage radius)

**Coverage Matrix:**
```
a_{ij} = 1  if  d_{ij} ≤ S
a_{ij} = 0  otherwise
```

**Objective:**
```
Minimize: Σ_{j=1}^m x_j  (minimize number of facilities)
```

**Constraints:**
```
Same coverage constraints as SCP
```

### Maximal Covering Location Problem (MCLP)

**Additional Parameters:**
- w_i: Weight/importance of demand point i (e.g., population, demand)
- p: Number of facilities to locate (budget constraint)

**Decision Variables:**
- x_j ∈ {0,1}: 1 if facility j is opened
- y_i ∈ {0,1}: 1 if demand point i is covered

**Objective Function:**
```
Maximize: Σ_{i=1}^n w_i × y_i  (maximize covered demand)
```

**Constraints:**
```
1. Coverage definition:
   y_i ≤ Σ_{j:a_{ij}=1} x_j,  ∀i ∈ I

2. Facility limit:
   Σ_{j=1}^m x_j ≤ p

3. Binary variables:
   x_j, y_i ∈ {0,1}
```

### Redundant Coverage (k-Coverage)

**Constraint:**
```
Each element must be covered by at least k facilities:
Σ_{j:a_{ij}=1} x_j ≥ k,  ∀i ∈ I
```

---

## Exact Solution Methods

### 1. Set Covering Problem with PuLP

```python
from pulp import *
import numpy as np

def solve_set_covering(costs, coverage_matrix, element_names=None,
                      set_names=None, redundancy=1):
    """
    Solve Set Covering Problem

    Args:
        costs: list of costs for each set/facility
        coverage_matrix: binary matrix [elements x sets]
                        coverage_matrix[i][j] = 1 if set j covers element i
        element_names: optional element names
        set_names: optional set names
        redundancy: coverage redundancy (k-coverage), default 1

    Returns:
        optimal solution
    """
    n_elements = len(coverage_matrix)
    n_sets = len(coverage_matrix[0]) if n_elements > 0 else 0

    if element_names is None:
        element_names = [f"Element_{i}" for i in range(n_elements)]

    if set_names is None:
        set_names = [f"Set_{j}" for j in range(n_sets)]

    # Create problem
    prob = LpProblem("Set_Covering", LpMinimize)

    # Decision variables: x[j] = 1 if set j is selected
    x = LpVariable.dicts("select", range(n_sets), cat='Binary')

    # Objective: Minimize total cost
    prob += lpSum([costs[j] * x[j] for j in range(n_sets)]), "Total_Cost"

    # Constraints: Each element covered at least 'redundancy' times
    for i in range(n_elements):
        prob += (
            lpSum([coverage_matrix[i][j] * x[j] for j in range(n_sets)]) >= redundancy,
            f"Coverage_{i}"
        )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        selected_sets = [j for j in range(n_sets) if x[j].varValue > 0.5]

        # Determine which sets cover each element
        element_coverage = {}
        for i in range(n_elements):
            covering_sets = [j for j in selected_sets
                           if coverage_matrix[i][j] == 1]
            element_coverage[i] = covering_sets

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'num_sets': len(selected_sets),
            'selected_sets': selected_sets,
            'selected_set_names': [set_names[j] for j in selected_sets],
            'element_coverage': element_coverage,
            'solve_time': solve_time,
            'redundancy': redundancy
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    # Example: Emergency service coverage
    # 12 demand points, 8 potential facility locations

    # Costs to establish each facility
    costs = [100, 120, 90, 110, 105, 115, 95, 108]

    # Coverage matrix: coverage[i][j] = 1 if facility j covers demand i
    # Rows = demand points, Columns = facilities
    coverage_matrix = [
        [1, 1, 0, 0, 0, 0, 0, 0],  # Demand 0 covered by facilities 0, 1
        [1, 0, 1, 0, 0, 0, 0, 0],  # Demand 1 covered by facilities 0, 2
        [0, 1, 1, 1, 0, 0, 0, 0],  # Demand 2 covered by facilities 1, 2, 3
        [0, 0, 1, 1, 0, 0, 0, 0],  # Demand 3
        [0, 0, 0, 1, 1, 0, 0, 0],  # Demand 4
        [0, 0, 0, 0, 1, 1, 0, 0],  # Demand 5
        [0, 0, 0, 0, 1, 1, 1, 0],  # Demand 6
        [0, 0, 0, 0, 0, 1, 1, 1],  # Demand 7
        [0, 0, 0, 0, 0, 0, 1, 1],  # Demand 8
        [1, 0, 0, 0, 0, 0, 0, 1],  # Demand 9
        [1, 0, 0, 0, 0, 0, 1, 0],  # Demand 10
        [0, 1, 0, 0, 1, 0, 0, 0],  # Demand 11
    ]

    demand_names = [f"Demand_{i}" for i in range(12)]
    facility_names = [f"Facility_{i}" for i in range(8)]

    print("="*70)
    print("SET COVERING PROBLEM")
    print("="*70)
    print(f"Elements to cover: {len(coverage_matrix)}")
    print(f"Potential facilities: {len(costs)}")

    # Solve with single coverage
    result = solve_set_covering(costs, coverage_matrix,
                               demand_names, facility_names,
                               redundancy=1)

    print(f"\n{'='*70}")
    print(f"OPTIMAL SOLUTION (Single Coverage)")
    print(f"{'='*70}")
    print(f"Status: {result['status']}")
    print(f"Total Cost: ${result['total_cost']:,.2f}")
    print(f"Facilities Selected: {result['num_sets']}")
    print(f"Facility IDs: {result['selected_sets']}")
    print(f"Facility Names: {result['selected_set_names']}")

    print(f"\nCoverage Details:")
    for i, covering_facilities in result['element_coverage'].items():
        print(f"  {demand_names[i]}: covered by facilities {covering_facilities}")

    print(f"\nSolve Time: {result['solve_time']:.2f} seconds")

    # Solve with redundant coverage (backup coverage)
    print(f"\n{'='*70}")
    print(f"REDUNDANT COVERAGE SOLUTION (k=2)")
    print(f"{'='*70}")

    result_redundant = solve_set_covering(costs, coverage_matrix,
                                         demand_names, facility_names,
                                         redundancy=2)

    print(f"Status: {result_redundant['status']}")
    print(f"Total Cost: ${result_redundant['total_cost']:,.2f}")
    print(f"Facilities Selected: {result_redundant['num_sets']}")
    print(f"Selected: {result_redundant['selected_set_names']}")

    print(f"\nCoverage Verification (each point covered ≥ 2 times):")
    for i, covering_facilities in result_redundant['element_coverage'].items():
        coverage_count = len(covering_facilities)
        status = "✓" if coverage_count >= 2 else "✗"
        print(f"  {demand_names[i]}: {status} {coverage_count} facilities "
              f"{covering_facilities}")
```

### 2. Location Set Covering Problem (LSCP)

```python
def solve_location_set_covering(facility_coords, demand_coords,
                               service_radius, facility_costs=None):
    """
    Solve Location Set Covering Problem

    Minimize number of facilities to cover all demand within service radius

    Args:
        facility_coords: array of potential facility coordinates
        demand_coords: array of demand point coordinates
        service_radius: maximum service distance
        facility_costs: optional costs (if None, minimize count)

    Returns:
        optimal facility locations
    """
    n_facilities = len(facility_coords)
    n_demands = len(demand_coords)

    # Calculate coverage matrix based on distances
    coverage_matrix = np.zeros((n_demands, n_facilities))

    for i in range(n_demands):
        for j in range(n_facilities):
            distance = np.linalg.norm(demand_coords[i] - facility_coords[j])
            if distance <= service_radius:
                coverage_matrix[i][j] = 1

    # If no costs provided, minimize number of facilities
    if facility_costs is None:
        facility_costs = [1] * n_facilities

    # Solve as set covering problem
    result = solve_set_covering(facility_costs, coverage_matrix)

    # Add distance information
    if result['status'] in ['Optimal', 'Feasible']:
        # Calculate average and max distance for each demand
        demand_distances = {}
        for i in range(n_demands):
            covering_facilities = result['element_coverage'][i]
            if covering_facilities:
                distances = [
                    np.linalg.norm(demand_coords[i] - facility_coords[j])
                    for j in covering_facilities
                ]
                demand_distances[i] = {
                    'min_distance': min(distances),
                    'covering_facilities': covering_facilities
                }

        result['demand_distances'] = demand_distances
        result['service_radius'] = service_radius

    return result


# Example usage
np.random.seed(42)

# Generate random coordinates
n_facilities = 15
n_demands = 30

facility_coords = np.random.rand(n_facilities, 2) * 100
demand_coords = np.random.rand(n_demands, 2) * 100

service_radius = 25  # Maximum service distance

print("\n" + "="*70)
print("LOCATION SET COVERING PROBLEM")
print("="*70)
print(f"Potential facilities: {n_facilities}")
print(f"Demand points: {n_demands}")
print(f"Service radius: {service_radius}")

result = solve_location_set_covering(facility_coords, demand_coords,
                                    service_radius)

print(f"\n{'='*70}")
print(f"OPTIMAL SOLUTION")
print(f"{'='*70}")
print(f"Status: {result['status']}")
print(f"Facilities Needed: {result['num_sets']}")
print(f"Facility IDs: {result['selected_sets']}")

print(f"\nService Statistics:")
all_min_distances = [d['min_distance'] for d in result['demand_distances'].values()]
print(f"  Average distance to nearest facility: {np.mean(all_min_distances):.2f}")
print(f"  Maximum distance to nearest facility: {np.max(all_min_distances):.2f}")
print(f"  All demands within service radius: {np.max(all_min_distances) <= service_radius}")
```

### 3. Maximal Covering Location Problem (MCLP)

```python
def solve_maximal_covering(facility_coords, demand_coords, demand_weights,
                          service_radius, max_facilities):
    """
    Solve Maximal Covering Location Problem

    Maximize covered demand with limited number of facilities

    Args:
        facility_coords: potential facility coordinates
        demand_coords: demand point coordinates
        demand_weights: demand weights (population, demand volume, etc.)
        service_radius: coverage radius
        max_facilities: maximum number of facilities to open

    Returns:
        optimal solution maximizing covered demand
    """
    n_facilities = len(facility_coords)
    n_demands = len(demand_coords)

    # Calculate coverage matrix
    coverage_matrix = np.zeros((n_demands, n_facilities))
    for i in range(n_demands):
        for j in range(n_facilities):
            distance = np.linalg.norm(demand_coords[i] - facility_coords[j])
            if distance <= service_radius:
                coverage_matrix[i][j] = 1

    # Create problem
    prob = LpProblem("Maximal_Covering", LpMaximize)

    # Decision variables
    x = LpVariable.dicts("facility", range(n_facilities), cat='Binary')
    y = LpVariable.dicts("covered", range(n_demands), cat='Binary')

    # Objective: Maximize total covered demand
    prob += (
        lpSum([demand_weights[i] * y[i] for i in range(n_demands)]),
        "Total_Covered_Demand"
    )

    # Constraints

    # 1. Coverage definition: demand covered only if within radius of open facility
    for i in range(n_demands):
        prob += (
            y[i] <= lpSum([coverage_matrix[i][j] * x[j]
                          for j in range(n_facilities)]),
            f"Coverage_{i}"
        )

    # 2. Facility limit
    prob += (
        lpSum([x[j] for j in range(n_facilities)]) <= max_facilities,
        "Facility_Limit"
    )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        open_facilities = [j for j in range(n_facilities)
                          if x[j].varValue > 0.5]

        covered_demands = [i for i in range(n_demands)
                          if y[i].varValue > 0.5]

        uncovered_demands = [i for i in range(n_demands)
                            if y[i].varValue < 0.5]

        total_demand = sum(demand_weights)
        covered_demand = sum(demand_weights[i] for i in covered_demands)
        coverage_percentage = (covered_demand / total_demand) * 100

        return {
            'status': LpStatus[prob.status],
            'covered_demand': covered_demand,
            'total_demand': total_demand,
            'coverage_percentage': coverage_percentage,
            'num_facilities': len(open_facilities),
            'max_facilities': max_facilities,
            'open_facilities': open_facilities,
            'covered_demands': covered_demands,
            'uncovered_demands': uncovered_demands,
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
demand_weights = np.random.uniform(50, 500, n_demands)  # Population or demand
max_facilities = 5  # Budget allows only 5 facilities

print("\n" + "="*70)
print("MAXIMAL COVERING LOCATION PROBLEM")
print("="*70)
print(f"Potential facilities: {n_facilities}")
print(f"Demand points: {n_demands}")
print(f"Total demand: {demand_weights.sum():,.2f}")
print(f"Maximum facilities: {max_facilities}")
print(f"Service radius: {service_radius}")

result = solve_maximal_covering(facility_coords, demand_coords,
                               demand_weights, service_radius,
                               max_facilities)

print(f"\n{'='*70}")
print(f"OPTIMAL SOLUTION")
print(f"{'='*70}")
print(f"Status: {result['status']}")
print(f"Facilities Opened: {result['num_facilities']} / {result['max_facilities']}")
print(f"Open Facility IDs: {result['open_facilities']}")
print(f"Covered Demand: {result['covered_demand']:,.2f} / {result['total_demand']:,.2f}")
print(f"Coverage: {result['coverage_percentage']:.2f}%")
print(f"Covered Demand Points: {len(result['covered_demands'])} / {n_demands}")
print(f"Uncovered Demand Points: {len(result['uncovered_demands'])}")

if result['uncovered_demands']:
    print(f"\nUncovered Demand Points:")
    for i in result['uncovered_demands'][:10]:  # Show first 10
        print(f"  Demand {i}: weight={demand_weights[i]:.2f}")
```

---

## Greedy Heuristics

### 1. Greedy Set Covering

```python
def greedy_set_covering(costs, coverage_matrix):
    """
    Greedy heuristic for set covering

    Iteratively select set with best cost-effectiveness ratio

    Args:
        costs: set costs
        coverage_matrix: coverage matrix

    Returns:
        heuristic solution
    """
    n_elements = len(coverage_matrix)
    n_sets = len(coverage_matrix[0])

    uncovered_elements = set(range(n_elements))
    selected_sets = []
    total_cost = 0

    while uncovered_elements:
        best_set = None
        best_ratio = float('inf')

        # Find set with best cost per newly covered element
        for j in range(n_sets):
            if j in selected_sets:
                continue

            # Count how many uncovered elements this set covers
            newly_covered = sum(1 for i in uncovered_elements
                              if coverage_matrix[i][j] == 1)

            if newly_covered > 0:
                ratio = costs[j] / newly_covered
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_set = j

        if best_set is None:
            # No set can cover remaining elements
            break

        # Select this set
        selected_sets.append(best_set)
        total_cost += costs[best_set]

        # Remove covered elements
        newly_covered_elements = {i for i in uncovered_elements
                                 if coverage_matrix[i][best_set] == 1}
        uncovered_elements -= newly_covered_elements

    return {
        'selected_sets': selected_sets,
        'num_sets': len(selected_sets),
        'total_cost': total_cost,
        'all_covered': len(uncovered_elements) == 0,
        'method': 'Greedy'
    }
```

### 2. Greedy Location for LSCP

```python
def greedy_location_covering(facility_coords, demand_coords, service_radius):
    """
    Greedy heuristic for location set covering

    Iteratively select facility that covers most uncovered demands

    Args:
        facility_coords: facility coordinates
        demand_coords: demand coordinates
        service_radius: service radius

    Returns:
        heuristic facility selection
    """
    n_facilities = len(facility_coords)
    n_demands = len(demand_coords)

    # Calculate coverage
    coverage = {}
    for j in range(n_facilities):
        coverage[j] = set()
        for i in range(n_demands):
            distance = np.linalg.norm(demand_coords[i] - facility_coords[j])
            if distance <= service_radius:
                coverage[j].add(i)

    uncovered_demands = set(range(n_demands))
    selected_facilities = []

    while uncovered_demands:
        # Select facility covering most uncovered demands
        best_facility = None
        max_new_coverage = 0

        for j in range(n_facilities):
            if j in selected_facilities:
                continue

            new_coverage = len(coverage[j] & uncovered_demands)
            if new_coverage > max_new_coverage:
                max_new_coverage = new_coverage
                best_facility = j

        if best_facility is None:
            # Cannot cover all demands
            break

        selected_facilities.append(best_facility)
        uncovered_demands -= coverage[best_facility]

    return {
        'selected_facilities': selected_facilities,
        'num_facilities': len(selected_facilities),
        'all_covered': len(uncovered_demands) == 0,
        'uncovered_count': len(uncovered_demands),
        'method': 'Greedy Location'
    }
```

---

## Complete Set Covering Solver

```python
class SetCoveringSolver:
    """
    Comprehensive Set Covering Problem Solver
    """

    def __init__(self):
        self.problem_type = None
        self.loaded = False

    def load_set_covering(self, costs, coverage_matrix,
                         element_names=None, set_names=None):
        """Load basic set covering problem"""
        self.costs = np.array(costs)
        self.coverage_matrix = np.array(coverage_matrix)
        self.element_names = element_names
        self.set_names = set_names
        self.problem_type = 'SCP'
        self.loaded = True

        print(f"Loaded Set Covering Problem:")
        print(f"  Elements: {len(coverage_matrix)}")
        print(f"  Sets: {len(costs)}")

    def load_location_covering(self, facility_coords, demand_coords,
                              service_radius, demand_weights=None):
        """Load location-based covering problem"""
        self.facility_coords = np.array(facility_coords)
        self.demand_coords = np.array(demand_coords)
        self.service_radius = service_radius
        self.demand_weights = demand_weights
        self.problem_type = 'LSCP'
        self.loaded = True

        print(f"Loaded Location Set Covering Problem:")
        print(f"  Facilities: {len(facility_coords)}")
        print(f"  Demands: {len(demand_coords)}")
        print(f"  Service radius: {service_radius}")

    def solve_exact(self, redundancy=1, max_facilities=None):
        """Solve with exact MIP"""
        if not self.loaded:
            raise ValueError("Problem not loaded")

        if self.problem_type == 'SCP':
            return solve_set_covering(self.costs, self.coverage_matrix,
                                     self.element_names, self.set_names,
                                     redundancy)

        elif self.problem_type == 'LSCP':
            if max_facilities:
                # Solve as MCLP
                weights = self.demand_weights if self.demand_weights is not None \
                         else np.ones(len(self.demand_coords))
                return solve_maximal_covering(
                    self.facility_coords, self.demand_coords,
                    weights, self.service_radius, max_facilities
                )
            else:
                # Solve as LSCP
                return solve_location_set_covering(
                    self.facility_coords, self.demand_coords,
                    self.service_radius
                )

    def solve_heuristic(self, method='greedy'):
        """Solve with heuristic"""
        if not self.loaded:
            raise ValueError("Problem not loaded")

        if method == 'greedy':
            if self.problem_type == 'SCP':
                return greedy_set_covering(self.costs, self.coverage_matrix)
            elif self.problem_type == 'LSCP':
                return greedy_location_covering(
                    self.facility_coords, self.demand_coords,
                    self.service_radius
                )

    def compare_methods(self, methods=['greedy', 'exact']):
        """Compare solution methods"""
        import pandas as pd

        results = []

        for method in methods:
            import time
            start = time.time()

            try:
                if method == 'exact':
                    sol = self.solve_exact()
                else:
                    sol = self.solve_heuristic(method)

                solve_time = time.time() - start

                results.append({
                    'Method': method,
                    'Sets/Facilities': sol.get('num_sets') or sol.get('num_facilities'),
                    'Cost': sol.get('total_cost', 'N/A'),
                    'Time (s)': f"{solve_time:.3f}"
                })

            except Exception as e:
                print(f"Error with {method}: {e}")

        return pd.DataFrame(results)

    def visualize_coverage(self, solution):
        """Visualize coverage solution"""
        if self.problem_type != 'LSCP':
            print("Visualization only for location problems")
            return

        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 8))

        # Plot demand points
        plt.scatter(self.demand_coords[:, 0], self.demand_coords[:, 1],
                   c='blue', s=50, alpha=0.6, label='Demand Points')

        # Plot all potential facilities (gray)
        plt.scatter(self.facility_coords[:, 0], self.facility_coords[:, 1],
                   c='lightgray', s=200, alpha=0.3, marker='s',
                   label='Potential Facilities')

        # Plot selected facilities (red)
        selected = solution.get('selected_sets') or solution.get('open_facilities') or \
                  solution.get('selected_facilities')

        if selected:
            selected_coords = self.facility_coords[selected]
            plt.scatter(selected_coords[:, 0], selected_coords[:, 1],
                       c='red', s=300, alpha=0.8, marker='s',
                       label='Selected Facilities', edgecolors='black', linewidths=2)

            # Draw coverage circles
            for idx in selected:
                circle = plt.Circle(
                    self.facility_coords[idx],
                    self.service_radius,
                    fill=False, edgecolor='red', alpha=0.3, linewidth=1
                )
                plt.gca().add_patch(circle)

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Set Covering Solution - Facility Coverage')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


# Complete example
if __name__ == "__main__":
    print("="*70)
    print("SET COVERING - COMPREHENSIVE EXAMPLE")
    print("="*70)

    # Example: Emergency service location
    np.random.seed(42)

    n_facilities = 20
    n_demands = 50

    facility_coords = np.random.rand(n_facilities, 2) * 100
    demand_coords = np.random.rand(n_demands, 2) * 100
    service_radius = 20

    # Create solver
    solver = SetCoveringSolver()
    solver.load_location_covering(facility_coords, demand_coords, service_radius)

    # Compare methods
    print("\n" + "="*70)
    print("COMPARING SOLUTION METHODS")
    print("="*70)

    comparison = solver.compare_methods(['greedy', 'exact'])
    print("\n" + comparison.to_string(index=False))

    # Detailed optimal solution
    print("\n" + "="*70)
    print("DETAILED OPTIMAL SOLUTION")
    print("="*70)

    optimal = solver.solve_exact()

    print(f"Facilities Needed: {optimal['num_sets']}")
    print(f"Facility IDs: {optimal['selected_sets']}")
    print(f"Average distance: {np.mean([d['min_distance'] for d in optimal['demand_distances'].values()]):.2f}")

    # Visualize
    solver.visualize_coverage(optimal)
```

---

## Tools & Libraries

**Python:**
- PuLP, Pyomo, OR-Tools
- NetworkX for graph-based coverage
- scikit-learn for clustering

**Applications:**
- Emergency services
- Retail location
- Sensor placement
- Network design

---

## Common Challenges & Solutions

**Large Problems:** Use greedy, column generation, Lagrangian relaxation

**Dynamic Coverage:** Update coverage sets, re-optimize periodically

**Probabilistic Demand:** Stochastic models, robust optimization

---

## Output Format

**Coverage Solution:**
- Sets Selected: X
- Total Cost: $Y
- Coverage: 100% (or Z%)
- Redundancy: k-coverage

---

## Questions to Ask

1. What needs to be covered?
2. Coverage requirements (100%, partial)?
3. Redundancy needed?
4. Budget constraints?
5. Coverage radius/distance?
6. Costs to consider?

---

## Related Skills

- **facility-location-problem**: General facility location
- **warehouse-location-optimization**: Warehouse coverage
- **hub-location-problem**: Hub coverage
- **network-flow-optimization**: Network-based coverage
- **optimization-modeling**: MIP formulation
