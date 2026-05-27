---
name: capacitated-vrp
description: When the user wants to solve the Capacitated Vehicle Routing Problem (CVRP), optimize routes with vehicle capacity limits, or handle weight/volume constraints. Also use when the user mentions "CVRP," "capacity-constrained routing," "load limits," "vehicle weight limits," "volume constraints," or "payload optimization." For time windows, see vrp-time-windows. For general VRP, see vehicle-routing-problem.
---

# Capacitated Vehicle Routing Problem (CVRP)

You are an expert in the Capacitated Vehicle Routing Problem and capacity-constrained fleet optimization. Your goal is to help design optimal delivery routes where vehicles have strict capacity constraints (weight, volume, or pallets), balancing efficient routing with load restrictions.

## Initial Assessment

Before solving CVRP instances, understand:

1. **Capacity Constraints**
   - What capacity units? (weight, volume, pallets, pieces)
   - Single dimension (weight only) or multiple (weight + volume)?
   - Are vehicles homogeneous (all same capacity)?
   - Any minimum load requirements?

2. **Customer Demands**
   - How many customers to serve?
   - Distribution of demands? (uniform, varied, heavy/light mix)
   - Any indivisible items? (can't split orders)
   - Demand certainty or variability?

3. **Fleet Characteristics**
   - Number of vehicles available?
   - Vehicle capacities (if heterogeneous)
   - Fixed cost per vehicle vs. variable (distance)?
   - Minimize vehicles or minimize distance?

4. **Problem Scale**
   - Small (< 50 customers): Exact methods possible
   - Medium (50-200 customers): Heuristics recommended
   - Large (200+ customers): Metaheuristics, decomposition

5. **Additional Constraints**
   - Any time windows? → see **vrp-time-windows**
   - Multiple depots? → see **multi-depot-vrp**
   - Pickups and deliveries? → see **pickup-delivery-problem**
   - Backhauls? → see **vrp-backhauls**

---

## Mathematical Formulation

### CVRP - Standard Two-Index Formulation

**Sets:**
- V = {0, 1, ..., n}: Nodes (0 = depot, 1..n = customers)
- K = {1, ..., m}: Vehicles

**Parameters:**
- c_{ij}: Cost/distance from node i to j
- q_i: Demand at customer i (q_0 = 0 for depot)
- Q: Vehicle capacity (homogeneous fleet)
- m: Number of vehicles

**Decision Variables:**
- x_{ij}^k ∈ {0,1}: 1 if vehicle k travels from i to j, 0 otherwise
- u_i^k ∈ ℝ: Cumulative load when vehicle k arrives at node i

**Objective Function:**
```
Minimize: Σ_{k∈K} Σ_{i∈V} Σ_{j∈V, i≠j} c_{ij} * x_{ij}^k
```

**Constraints:**
```
1. Each customer visited exactly once:
   Σ_{k∈K} Σ_{i∈V, i≠j} x_{ij}^k = 1,  ∀j ∈ V\{0}

2. Flow conservation:
   Σ_{i∈V, i≠h} x_{ih}^k = Σ_{j∈V, j≠h} x_{hj}^k,  ∀h ∈ V, ∀k ∈ K

3. Each vehicle leaves depot at most once:
   Σ_{j∈V\{0}} x_{0j}^k ≤ 1,  ∀k ∈ K

4. Each vehicle returns to depot at most once:
   Σ_{i∈V\{0}} x_{i0}^k ≤ 1,  ∀k ∈ K

5. Capacity constraint (load-based):
   u_j^k ≥ u_i^k + q_j - Q*(1 - x_{ij}^k),  ∀i,j ∈ V\{0}, ∀k ∈ K
   q_i ≤ u_i^k ≤ Q,  ∀i ∈ V\{0}, ∀k ∈ K

6. Binary variables:
   x_{ij}^k ∈ {0,1},  ∀i,j ∈ V, ∀k ∈ K
```

### Alternative: Single-Index Formulation (Compact)

**Decision Variables:**
- x_{ij} ∈ {0,1}: 1 if arc (i,j) is used by any vehicle
- u_i ≥ 0: Cumulative load upon arrival at customer i

**Objective:**
```
Minimize: Σ_{i∈V} Σ_{j∈V, i≠j} c_{ij} * x_{ij}
```

**Key Constraints:**
```
1. Degree constraints:
   Σ_{j∈V, j≠i} x_{ij} = 1,  ∀i ∈ V\{0}
   Σ_{i∈V, i≠j} x_{ij} = 1,  ∀j ∈ V\{0}

2. Capacity constraints:
   u_j ≥ u_i + q_j - Q*(1 - x_{ij}),  ∀i,j ∈ V\{0}, i≠j
   q_i ≤ u_i ≤ Q,  ∀i ∈ V\{0}

3. Valid cuts can be added for strengthening
```

---

## Exact Algorithms

### 1. Branch-and-Cut with Capacity Cuts

```python
from pulp import *
import numpy as np

def cvrp_branch_and_cut(dist_matrix, demands, vehicle_capacity,
                        num_vehicles=None, depot=0):
    """
    CVRP using branch-and-cut with capacity inequalities

    Args:
        dist_matrix: n x n distance matrix
        demands: list of customer demands (depot = 0)
        vehicle_capacity: vehicle capacity
        num_vehicles: max number of vehicles (None = unlimited)
        depot: depot index

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    customers = [i for i in range(n) if i != depot]

    # Calculate minimum vehicles needed
    total_demand = sum(demands[i] for i in customers)
    min_vehicles = int(np.ceil(total_demand / vehicle_capacity))

    if num_vehicles is None:
        num_vehicles = min_vehicles
    elif num_vehicles < min_vehicles:
        return {
            'status': 'Infeasible',
            'message': f'Need at least {min_vehicles} vehicles for total demand {total_demand}'
        }

    # Create problem
    prob = LpProblem("CVRP", LpMinimize)

    # Decision variables: x[i,j,k] for each vehicle
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(num_vehicles):
                    x[i,j,k] = LpVariable(f"x_{i}_{j}_{k}", cat='Binary')

    # Load variables for capacity tracking
    u = {}
    for i in customers:
        for k in range(num_vehicles):
            u[i,k] = LpVariable(f"u_{i}_{k}",
                               lowBound=demands[i],
                               upBound=vehicle_capacity,
                               cat='Continuous')

    # Objective: Minimize total distance
    prob += lpSum([dist_matrix[i][j] * x[i,j,k]
                   for i in range(n) for j in range(n) if i != j
                   for k in range(num_vehicles)]), "Total_Distance"

    # Constraints

    # 1. Each customer visited exactly once
    for j in customers:
        prob += lpSum([x[i,j,k] for i in range(n) if i != j
                      for k in range(num_vehicles)]) == 1, f"Visit_{j}"

    # 2. Flow conservation
    for h in range(n):
        for k in range(num_vehicles):
            prob += (lpSum([x[i,h,k] for i in range(n) if i != h]) ==
                    lpSum([x[h,j,k] for j in range(n) if j != h])), \
                    f"Flow_{h}_{k}"

    # 3. Vehicle capacity (load-based subtour elimination)
    for k in range(num_vehicles):
        for i in customers:
            for j in customers:
                if i != j:
                    prob += (u[i,k] + demands[j] <=
                            u[j,k] + vehicle_capacity * (1 - x[i,j,k])), \
                            f"Load_{i}_{j}_{k}"

    # 4. Each vehicle used at most once
    for k in range(num_vehicles):
        prob += lpSum([x[depot,j,k] for j in customers]) <= 1, \
                f"Leave_Depot_{k}"

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        routes = []
        route_loads = []

        for k in range(num_vehicles):
            route = [depot]
            current = depot

            for _ in range(n):
                next_node = None
                for j in range(n):
                    if j != current and (current,j,k) in x:
                        if x[current,j,k].varValue > 0.5:
                            next_node = j
                            break

                if next_node is None or next_node == depot:
                    route.append(depot)
                    break

                route.append(next_node)
                current = next_node

            if len(route) > 2:  # Route has customers
                routes.append(route)
                load = sum(demands[i] for i in route[1:-1])
                route_loads.append(load)

        return {
            'status': LpStatus[prob.status],
            'total_distance': value(prob.objective),
            'routes': routes,
            'route_loads': route_loads,
            'num_vehicles_used': len(routes),
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    np.random.seed(42)

    # Generate random problem
    n = 16  # 1 depot + 15 customers
    coords = np.random.rand(n, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coords[i] - coords[j])

    # Demands (depot has 0)
    demands = [0] + [np.random.randint(5, 25) for _ in range(n-1)]

    vehicle_capacity = 50

    print(f"Total demand: {sum(demands)}")
    print(f"Min vehicles needed: {int(np.ceil(sum(demands) / vehicle_capacity))}")

    result = cvrp_branch_and_cut(dist_matrix, demands, vehicle_capacity)

    if result['status'] in ['Optimal', 'Feasible']:
        print(f"\nStatus: {result['status']}")
        print(f"Total Distance: {result['total_distance']:.2f}")
        print(f"Vehicles Used: {result['num_vehicles_used']}")

        for i, (route, load) in enumerate(zip(result['routes'],
                                              result['route_loads'])):
            print(f"\nVehicle {i+1}: {route}")
            print(f"  Load: {load}/{vehicle_capacity} ({load/vehicle_capacity*100:.1f}%)")
    else:
        print(f"Status: {result['status']}")
```

---

## Classical Heuristics

### 1. Clarke-Wright Savings Algorithm (Parallel Version)

```python
def clarke_wright_parallel_cvrp(dist_matrix, demands, vehicle_capacity, depot=0):
    """
    Clarke-Wright Savings Algorithm (Parallel version) for CVRP

    Most famous CVRP heuristic - merges routes based on savings

    Time complexity: O(n^2 log n)
    Solution quality: Typically within 5-10% of optimal

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        depot: depot index

    Returns:
        solution dictionary with routes and costs
    """
    n = len(dist_matrix)
    customers = [i for i in range(n) if i != depot]

    # Calculate savings s_{ij} = d_{0i} + d_{0j} - d_{ij}
    savings = []

    for i in customers:
        for j in customers:
            if i < j:
                saving = (dist_matrix[depot][i] +
                         dist_matrix[depot][j] -
                         dist_matrix[i][j])
                savings.append((saving, i, j))

    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])

    # Initialize: each customer in separate route
    routes = [[depot, c, depot] for c in customers]
    route_loads = [demands[c] for c in customers]

    # Merge routes based on savings
    for saving_value, i, j in savings:
        # Find routes containing i and j
        route_i_idx = None
        route_j_idx = None

        for idx, route in enumerate(routes):
            if i in route:
                route_i_idx = idx
            if j in route:
                route_j_idx = idx

        if route_i_idx is None or route_j_idx is None:
            continue

        if route_i_idx == route_j_idx:
            continue  # Already in same route

        # Check if i and j are at route ends (interior = 1 and -2 positions)
        route_i = routes[route_i_idx]
        route_j = routes[route_j_idx]

        i_at_end = (route_i[1] == i or route_i[-2] == i)
        j_at_end = (route_j[1] == j or route_j[-2] == j)

        if not (i_at_end and j_at_end):
            continue

        # Check capacity constraint
        combined_load = route_loads[route_i_idx] + route_loads[route_j_idx]
        if combined_load > vehicle_capacity:
            continue

        # Merge routes
        route_i_interior = route_i[1:-1]
        route_j_interior = route_j[1:-1]

        # Determine correct merge order
        if route_i_interior[-1] == i and route_j_interior[0] == j:
            new_route = [depot] + route_i_interior + route_j_interior + [depot]
        elif route_i_interior[-1] == i and route_j_interior[-1] == j:
            new_route = [depot] + route_i_interior + route_j_interior[::-1] + [depot]
        elif route_i_interior[0] == i and route_j_interior[0] == j:
            new_route = [depot] + route_i_interior[::-1] + route_j_interior + [depot]
        elif route_i_interior[0] == i and route_j_interior[-1] == j:
            new_route = [depot] + route_j_interior + route_i_interior + [depot]
        else:
            continue

        # Update routes
        routes[route_i_idx] = new_route
        route_loads[route_i_idx] = combined_load

        # Remove merged route
        del routes[route_j_idx]
        del route_loads[route_j_idx]

    # Calculate total distance
    total_distance = 0
    for route in routes:
        for i in range(len(route) - 1):
            total_distance += dist_matrix[route[i]][route[i+1]]

    return {
        'routes': routes,
        'route_loads': route_loads,
        'total_distance': total_distance,
        'num_vehicles': len(routes)
    }
```

### 2. Sweep Algorithm for CVRP

```python
def sweep_cvrp(coordinates, demands, vehicle_capacity, depot_idx=0):
    """
    Sweep Algorithm for CVRP

    Sweeps around depot in polar coordinates, creating routes

    Best for: Geographically clustered problems

    Args:
        coordinates: list of (x, y) coordinates
        demands: customer demands
        vehicle_capacity: vehicle capacity
        depot_idx: depot index

    Returns:
        solution dictionary
    """
    import math

    n = len(coordinates)
    depot = coordinates[depot_idx]
    customers = [i for i in range(n) if i != depot_idx]

    # Calculate polar angles from depot
    angles = []
    for i in customers:
        dx = coordinates[i][0] - depot[0]
        dy = coordinates[i][1] - depot[1]
        angle = math.atan2(dy, dx)
        angles.append((angle, i))

    # Sort by angle
    angles.sort()

    # Build routes by sweeping
    routes = []
    current_route = [depot_idx]
    current_load = 0

    for angle, customer in angles:
        if current_load + demands[customer] <= vehicle_capacity:
            current_route.append(customer)
            current_load += demands[customer]
        else:
            # Finish current route and start new one
            current_route.append(depot_idx)
            routes.append(current_route)

            current_route = [depot_idx, customer]
            current_load = demands[customer]

    # Add last route
    if len(current_route) > 1:
        current_route.append(depot_idx)
        routes.append(current_route)

    # Optimize each route with 2-opt
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt(
                (coordinates[i][0] - coordinates[j][0])**2 +
                (coordinates[i][1] - coordinates[j][1])**2
            )

    optimized_routes = []
    for route in routes:
        # Simple 2-opt on each route
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    if (dist_matrix[route[i-1]][route[j]] +
                        dist_matrix[route[i]][route[j+1]] <
                        dist_matrix[route[i-1]][route[i]] +
                        dist_matrix[route[j]][route[j+1]]):

                        route[i:j+1] = reversed(route[i:j+1])
                        improved = True
                        break
                if improved:
                    break

        optimized_routes.append(route)

    # Calculate total distance
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in optimized_routes
    )

    return {
        'routes': optimized_routes,
        'total_distance': total_distance,
        'num_vehicles': len(optimized_routes)
    }
```

---

## Using OR-Tools for CVRP

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_cvrp_ortools(dist_matrix, demands, vehicle_capacities,
                      num_vehicles=None, depot=0, time_limit=30):
    """
    Solve CVRP using Google OR-Tools

    Most practical and efficient for real-world CVRP

    Args:
        dist_matrix: n x n distance matrix
        demands: list of demands
        vehicle_capacities: capacity (single value or list)
        num_vehicles: number of vehicles (None = auto)
        depot: depot index
        time_limit: time limit in seconds

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)

    # Calculate minimum vehicles if not specified
    if num_vehicles is None:
        total_demand = sum(demands)
        if isinstance(vehicle_capacities, list):
            capacity = vehicle_capacities[0]
        else:
            capacity = vehicle_capacities
        num_vehicles = int(np.ceil(total_demand / capacity))

    # Handle uniform fleet
    if isinstance(vehicle_capacities, (int, float)):
        vehicle_capacities = [int(vehicle_capacities)] * num_vehicles

    # Create routing manager
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot)

    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node] * 100)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Demand callback
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return int(demands[from_node])

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    # Add capacity dimension
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        vehicle_capacities,  # vehicle capacities
        True,  # start cumul to zero
        'Capacity')

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = time_limit

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        routes = []
        route_loads = []
        total_distance = 0

        capacity_dimension = routing.GetDimensionOrDie('Capacity')

        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            route_load = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                route_load += demands[node]
                index = solution.Value(routing.NextVar(index))

            route.append(manager.IndexToNode(index))

            if len(route) > 2:
                routes.append(route)
                route_loads.append(route_load)

                # Calculate route distance
                route_distance = sum(dist_matrix[route[i]][route[i+1]]
                                   for i in range(len(route)-1))
                total_distance += route_distance

        return {
            'status': 'Optimal' if solution.ObjectiveValue() > 0 else 'Feasible',
            'routes': routes,
            'route_loads': route_loads,
            'total_distance': total_distance,
            'num_vehicles_used': len(routes),
            'average_load_percent': np.mean([load/cap*100
                                            for load, cap in zip(route_loads, vehicle_capacities[:len(routes)])])
        }
    else:
        return {
            'status': 'No solution found',
            'routes': None
        }


# Complete example with visualization
def visualize_cvrp_solution(coordinates, routes, route_loads, capacity,
                           save_path=None):
    """Visualize CVRP solution with load percentages"""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    colors = plt.cm.tab10(np.linspace(0, 1, len(routes)))

    # Plot routes
    for idx, (route, load) in enumerate(zip(routes, route_loads)):
        route_coords = [coordinates[i] for i in route]
        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]

        ax1.plot(xs, ys, 'o-', color=colors[idx],
                linewidth=2, markersize=8,
                label=f'Vehicle {idx+1} ({load}/{capacity})')

    depot = coordinates[0]
    ax1.plot(depot[0], depot[1], 's', color='red',
            markersize=15, label='Depot', zorder=10)

    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.set_title('CVRP Routes')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot load distribution
    vehicle_ids = [f'V{i+1}' for i in range(len(routes))]
    load_percents = [load/capacity*100 for load in route_loads]

    bars = ax2.bar(vehicle_ids, load_percents, color=colors)
    ax2.axhline(y=100, color='r', linestyle='--', label='Capacity')
    ax2.set_xlabel('Vehicle')
    ax2.set_ylabel('Load (%)')
    ax2.set_title('Vehicle Load Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, load, percent in zip(bars, route_loads, load_percents):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{load}\n({percent:.0f}%)',
                ha='center', va='bottom')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


# Example
if __name__ == "__main__":
    np.random.seed(42)
    import random

    n = 31  # 1 depot + 30 customers
    coordinates = np.random.rand(n, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coordinates[i] - coordinates[j])

    # Demands
    demands = [0] + [random.randint(5, 25) for _ in range(n-1)]

    vehicle_capacity = 100
    num_vehicles = 5

    print(f"Total demand: {sum(demands)}")
    print(f"Theoretical min vehicles: {np.ceil(sum(demands)/vehicle_capacity)}")

    print("\nSolving CVRP with OR-Tools...")
    result = solve_cvrp_ortools(dist_matrix, demands, vehicle_capacity,
                               num_vehicles, time_limit=30)

    print(f"\nStatus: {result['status']}")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"Vehicles Used: {result['num_vehicles_used']}/{num_vehicles}")
    print(f"Average Load: {result['average_load_percent']:.1f}%")

    print("\nRoute Details:")
    for i, (route, load) in enumerate(zip(result['routes'], result['route_loads'])):
        print(f"  Vehicle {i+1}: {len(route)-2} customers")
        print(f"    Load: {load}/{vehicle_capacity} ({load/vehicle_capacity*100:.1f}%)")
        print(f"    Route: {route}")

    # Visualize
    visualize_cvrp_solution(coordinates, result['routes'],
                          result['route_loads'], vehicle_capacity)
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **OR-Tools (Google)**: Best for practical CVRP (recommended)
- **PuLP**: MIP modeling
- **Pyomo**: Advanced modeling
- **VRPy**: Specialized VRP library

### Benchmark Instances

- **Augerat et al. (A, B, P sets)**: Classic CVRP benchmarks
- **Christofides & Eilon**: Standard test instances
- **Golden et al.**: Large-scale instances
- **CVRPLIB**: Comprehensive benchmark library

---

## Common Challenges & Solutions

### Challenge: Tight Capacity Constraints

**Problem:**
- High utilization required
- Small vehicle capacity relative to demands

**Solutions:**
- Use exact methods if small enough
- Clarke-Wright savings works well
- Consider route balancing objectives

### Challenge: Heterogeneous Fleet

**Problem:**
- Different vehicle capacities
- Different costs per vehicle type

**Solutions:**
- Sequential assignment: sort by capacity, assign largest first
- OR-Tools handles naturally with capacity array
- Multi-stage approach

### Challenge: Multiple Capacity Dimensions

**Problem:**
- Weight AND volume constraints
- Pallets AND weight limits

**Solutions:**
- Check both dimensions in feasibility
- Use most restrictive constraint
- OR-Tools supports multiple dimensions

---

## Output Format

### CVRP Solution Report

**Problem Instance:**
- Customers: 50
- Vehicle Capacity: 100 units
- Total Demand: 487 units
- Theoretical Min Vehicles: 5

**Solution:**

| Metric | Value |
|--------|-------|
| Total Distance | 1,247 km |
| Vehicles Used | 5 |
| Average Load | 97.4 units (97.4%) |
| Load Std Dev | 3.2 units |
| Min Load | 92 units (92%) |
| Max Load | 100 units (100%) |

**Routes:**

| Vehicle | Customers | Load | % Capacity | Distance |
|---------|-----------|------|------------|----------|
| 1 | 12 | 98 | 98% | 245 km |
| 2 | 11 | 100 | 100% | 267 km |
| 3 | 9 | 95 | 95% | 198 km |
| 4 | 10 | 92 | 92% | 289 km |
| 5 | 8 | 102 | 102% | 248 km |

---

## Questions to Ask

1. What units are capacities measured in? (weight, volume, pallets)
2. Are vehicles homogeneous or different capacities?
3. Is there a fixed cost per vehicle or just distance cost?
4. Should we minimize vehicles or minimize distance?
5. Are there multiple dimensions to consider (weight AND volume)?
6. Can deliveries be split across multiple visits?
7. What's the acceptable solution time?

---

## Related Skills

- **vehicle-routing-problem**: For general VRP overview
- **vrp-time-windows**: For adding time constraints
- **split-delivery-vrp**: For allowing split deliveries
- **multi-depot-vrp**: For multiple depot problems
- **traveling-salesman-problem**: For single vehicle case
