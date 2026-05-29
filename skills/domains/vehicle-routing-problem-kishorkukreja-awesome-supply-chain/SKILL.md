---
name: vehicle-routing-problem
description: When the user wants to solve the Vehicle Routing Problem (VRP), optimize multi-vehicle routes, or plan fleet delivery routes. Also use when the user mentions "VRP," "fleet routing," "multi-vehicle routing," "delivery route planning," "vehicle dispatch," "fleet optimization," or "route assignment." For single vehicle, see traveling-salesman-problem. For time windows, see vrp-time-windows.
---

# Vehicle Routing Problem (VRP)

You are an expert in the Vehicle Routing Problem and fleet optimization. Your goal is to help determine optimal routes for a fleet of vehicles to serve a set of customers, minimizing total distance/cost while respecting vehicle capacities and other constraints.

## Initial Assessment

Before solving VRP instances, understand:

1. **Fleet Characteristics**
   - How many vehicles available?
   - Vehicle capacities (weight, volume, pallets)?
   - Homogeneous fleet (all same) or heterogeneous?
   - Fixed costs per vehicle vs. variable costs?
   - Maximum route duration or distance?

2. **Customer Requirements**
   - How many customers to serve?
   - Customer demands (quantities)?
   - Service time at each location?
   - Any delivery time windows? → see **vrp-time-windows**
   - Pickup and delivery? → see **pickup-delivery-problem**

3. **Problem Scale**
   - Small (< 50 customers, < 5 vehicles): Exact methods possible
   - Medium (50-200 customers): Advanced heuristics
   - Large (200+ customers): Metaheuristics, decomposition

4. **Constraints**
   - Capacity constraints?
   - Maximum route length/duration?
   - Driver breaks required?
   - Depot open hours?
   - Multiple depots? → see **multi-depot-vrp**

5. **Objectives**
   - Minimize total distance?
   - Minimize number of vehicles?
   - Minimize total cost?
   - Balance routes?

---

## Mathematical Formulation

### Capacitated VRP (CVRP) - Two-Index Formulation

**Sets:**
- V = {0, 1, ..., n}: Set of nodes (0 = depot, 1..n = customers)
- K = {1, ..., m}: Set of vehicles

**Parameters:**
- c_{ij}: Cost/distance from node i to node j
- d_i: Demand at customer i
- Q_k: Capacity of vehicle k
- M: Number of available vehicles

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j, 0 otherwise

**Objective Function:**
```
Minimize: Σ_{k∈K} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk}
```

**Constraints:**
```
1. Each customer visited exactly once:
   Σ_{k∈K} Σ_{i∈V} x_{ijk} = 1,  ∀j ∈ V\{0}

2. Flow conservation (what goes in must come out):
   Σ_{i∈V} x_{ihk} - Σ_{j∈V} x_{hjk} = 0,  ∀h ∈ V, ∀k ∈ K

3. Vehicle starts from depot:
   Σ_{j∈V\{0}} x_{0jk} = 1,  ∀k ∈ K

4. Vehicle returns to depot:
   Σ_{i∈V\{0}} x_{i0k} = 1,  ∀k ∈ K

5. Capacity constraint:
   Σ_{i∈V\{0}} Σ_{j∈V} d_i * x_{ijk} ≤ Q_k,  ∀k ∈ K

6. Subtour elimination (various formulations):
   - MTZ constraints
   - Flow-based constraints
   - Cutset constraints

7. Binary variables:
   x_{ijk} ∈ {0,1},  ∀i,j ∈ V, ∀k ∈ K
```

### Vehicle Minimization Formulation

When minimizing number of vehicles is primary objective:

```
Minimize: Σ_{k∈K} Σ_{j∈V\{0}} x_{0jk} + α * Σ_{k∈K} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk}
```

Where α is a small weight on total distance (secondary objective).

---

## Exact Algorithms

### 1. Branch-and-Cut with Set Partitioning

```python
from pulp import *
import numpy as np

def vrp_branch_and_cut_simple(dist_matrix, demands, vehicle_capacity,
                              num_vehicles, depot=0):
    """
    VRP using Branch-and-Cut (simplified version)

    Suitable for small-medium instances (up to 50 customers)

    Args:
        dist_matrix: n x n distance matrix
        demands: list of demands for each customer
        vehicle_capacity: capacity of each vehicle
        num_vehicles: number of available vehicles
        depot: depot node index

    Returns:
        dict with solution details
    """
    n = len(dist_matrix)
    customers = [i for i in range(n) if i != depot]

    # Create problem
    prob = LpProblem("CVRP", LpMinimize)

    # Decision variables: x[i,j,k] = 1 if vehicle k goes from i to j
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(num_vehicles):
                    x[i,j,k] = LpVariable(f"x_{i}_{j}_{k}", cat='Binary')

    # Objective: Minimize total distance
    prob += lpSum([dist_matrix[i][j] * x[i,j,k]
                   for i in range(n) for j in range(n) if i != j
                   for k in range(num_vehicles)]), "Total_Distance"

    # Constraints

    # 1. Each customer visited exactly once
    for j in customers:
        prob += lpSum([x[i,j,k] for i in range(n) if i != j
                      for k in range(num_vehicles)]) == 1, \
                f"Visit_{j}"

    # 2. Flow conservation
    for h in range(n):
        for k in range(num_vehicles):
            prob += (lpSum([x[i,h,k] for i in range(n) if i != h]) ==
                    lpSum([x[h,j,k] for j in range(n) if j != h])), \
                    f"Flow_{h}_{k}"

    # 3. Each vehicle leaves depot at most once
    for k in range(num_vehicles):
        prob += lpSum([x[depot,j,k] for j in customers]) <= 1, \
                f"Leave_Depot_{k}"

    # 4. Each vehicle returns to depot at most once
    for k in range(num_vehicles):
        prob += lpSum([x[i,depot,k] for i in customers]) <= 1, \
                f"Return_Depot_{k}"

    # 5. Capacity constraints (using flow-based formulation)
    for k in range(num_vehicles):
        prob += lpSum([demands[j] * lpSum([x[i,j,k] for i in range(n) if i != j])
                      for j in customers]) <= vehicle_capacity, \
                f"Capacity_{k}"

    # 6. Subtour elimination (MTZ-style)
    u = {}
    for i in customers:
        for k in range(num_vehicles):
            u[i,k] = LpVariable(f"u_{i}_{k}", lowBound=0,
                               upBound=vehicle_capacity, cat='Continuous')

    for k in range(num_vehicles):
        for i in customers:
            for j in customers:
                if i != j:
                    prob += (u[i,k] - u[j,k] + vehicle_capacity * x[i,j,k] <=
                            vehicle_capacity - demands[j]), \
                            f"Subtour_{i}_{j}_{k}"

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] == 'Optimal' or LpStatus[prob.status] == 'Feasible':
        routes = [[] for _ in range(num_vehicles)]

        for k in range(num_vehicles):
            # Build route for vehicle k
            current = depot
            route = [depot]

            while True:
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
                routes[k] = route

        # Remove empty routes
        routes = [r for r in routes if len(r) > 2]

        return {
            'status': LpStatus[prob.status],
            'total_distance': value(prob.objective),
            'routes': routes,
            'num_vehicles_used': len(routes),
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'total_distance': None,
            'routes': None,
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    # Example: 10 customers + 1 depot
    np.random.seed(42)

    # Generate random coordinates
    coords = np.random.rand(11, 2) * 100

    # Calculate distance matrix
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coords[i] - coords[j])

    # Customer demands (depot has 0 demand)
    demands = [0] + [np.random.randint(5, 20) for _ in range(10)]

    vehicle_capacity = 50
    num_vehicles = 3

    result = vrp_branch_and_cut_simple(dist_matrix, demands,
                                      vehicle_capacity, num_vehicles)

    print(f"\nStatus: {result['status']}")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"Number of Vehicles Used: {result['num_vehicles_used']}")
    print("\nRoutes:")
    for i, route in enumerate(result['routes']):
        route_demand = sum(demands[j] for j in route[1:-1])
        print(f"  Vehicle {i+1}: {route}")
        print(f"    Demand: {route_demand}/{vehicle_capacity}")
```

---

## Classical Heuristics

### 1. Clarke-Wright Savings Algorithm

```python
def clarke_wright_savings(dist_matrix, demands, vehicle_capacity, depot=0):
    """
    Clarke-Wright Savings Algorithm for VRP

    One of the most famous VRP heuristics

    Time complexity: O(n^2 log n)
    Quality: Good solutions, fast computation

    Args:
        dist_matrix: n x n distance matrix
        demands: list of demands
        vehicle_capacity: vehicle capacity
        depot: depot index

    Returns:
        dict with routes and total distance
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
    savings.sort(reverse=True)

    # Initialize: each customer in separate route
    routes = [[depot, customer, depot] for customer in customers]
    route_demands = [demands[customer] for customer in customers]

    # Merge routes based on savings
    for saving, i, j in savings:
        # Find routes containing i and j
        route_i = None
        route_j = None

        for idx, route in enumerate(routes):
            if i in route:
                route_i = idx
            if j in route:
                route_j = idx

        if route_i is None or route_j is None:
            continue

        if route_i == route_j:
            continue  # Already in same route

        # Check if i and j are at ends of their routes
        # (can only merge if they're at route ends)
        route_i_data = routes[route_i]
        route_j_data = routes[route_j]

        i_at_end = (route_i_data[1] == i or route_i_data[-2] == i)
        j_at_end = (route_j_data[1] == j or route_j_data[-2] == j)

        if not (i_at_end and j_at_end):
            continue

        # Check capacity constraint
        combined_demand = route_demands[route_i] + route_demands[route_j]
        if combined_demand > vehicle_capacity:
            continue

        # Merge routes
        # Remove depots and merge
        route_i_interior = route_i_data[1:-1]
        route_j_interior = route_j_data[1:-1]

        # Determine merge order
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
        routes[route_i] = new_route
        route_demands[route_i] = combined_demand

        # Remove route_j
        del routes[route_j]
        del route_demands[route_j]

    # Calculate total distance
    total_distance = 0
    for route in routes:
        for i in range(len(route) - 1):
            total_distance += dist_matrix[route[i]][route[i+1]]

    return {
        'routes': routes,
        'total_distance': total_distance,
        'num_vehicles': len(routes),
        'route_demands': route_demands
    }
```

### 2. Sweep Algorithm

```python
def sweep_algorithm(coordinates, demands, vehicle_capacity, depot_idx=0):
    """
    Sweep Algorithm for VRP

    Works with polar coordinates - sweeps around depot

    Best for: Geographically clustered customers

    Args:
        coordinates: list of (x, y) tuples
        demands: list of demands
        vehicle_capacity: vehicle capacity
        depot_idx: depot index

    Returns:
        dict with routes and total distance
    """
    import math

    n = len(coordinates)
    depot = coordinates[depot_idx]

    # Calculate polar angles from depot
    angles = []
    for i, coord in enumerate(coordinates):
        if i == depot_idx:
            continue

        dx = coord[0] - depot[0]
        dy = coord[1] - depot[1]
        angle = math.atan2(dy, dx)
        angles.append((angle, i))

    # Sort customers by angle
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
            # Start new route
            current_route.append(depot_idx)
            routes.append(current_route)

            current_route = [depot_idx, customer]
            current_load = demands[customer]

    # Add last route
    if len(current_route) > 1:
        current_route.append(depot_idx)
        routes.append(current_route)

    # Calculate distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt(
                (coordinates[i][0] - coordinates[j][0])**2 +
                (coordinates[i][1] - coordinates[j][1])**2
            )

    # Calculate total distance
    total_distance = 0
    for route in routes:
        for i in range(len(route) - 1):
            total_distance += dist_matrix[route[i]][route[i+1]]

    return {
        'routes': routes,
        'total_distance': total_distance,
        'num_vehicles': len(routes)
    }
```

### 3. Sequential Insertion Heuristics

```python
def sequential_insertion_vrp(dist_matrix, demands, vehicle_capacity,
                            depot=0, insertion_criterion='cheapest'):
    """
    Sequential insertion heuristic for VRP

    Builds routes one at a time by inserting customers

    Args:
        dist_matrix: n x n distance matrix
        demands: list of demands
        vehicle_capacity: vehicle capacity
        depot: depot index
        insertion_criterion: 'cheapest', 'farthest', 'nearest'

    Returns:
        dict with routes and total distance
    """
    n = len(dist_matrix)
    customers = set(range(n)) - {depot}
    routes = []

    while customers:
        # Start new route
        route = [depot]
        route_load = 0

        # Select seed customer based on criterion
        if insertion_criterion == 'farthest':
            seed = max(customers, key=lambda c: dist_matrix[depot][c])
        elif insertion_criterion == 'nearest':
            seed = min(customers, key=lambda c: dist_matrix[depot][c])
        else:  # cheapest
            seed = min(customers)

        route.append(seed)
        route.append(depot)
        route_load += demands[seed]
        customers.remove(seed)

        # Insert remaining customers into this route
        while customers:
            best_customer = None
            best_position = None
            best_cost_increase = float('inf')

            # Try inserting each customer
            for customer in customers:
                if route_load + demands[customer] > vehicle_capacity:
                    continue

                # Try each position in route
                for pos in range(1, len(route)):
                    # Cost of inserting customer at position pos
                    cost_increase = (
                        dist_matrix[route[pos-1]][customer] +
                        dist_matrix[customer][route[pos]] -
                        dist_matrix[route[pos-1]][route[pos]]
                    )

                    if cost_increase < best_cost_increase:
                        best_cost_increase = cost_increase
                        best_customer = customer
                        best_position = pos

            if best_customer is None:
                break  # No more customers fit in this route

            # Insert best customer
            route.insert(best_position, best_customer)
            route_load += demands[best_customer]
            customers.remove(best_customer)

        routes.append(route)

    # Calculate total distance
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes
    )

    return {
        'routes': routes,
        'total_distance': total_distance,
        'num_vehicles': len(routes)
    }
```

---

## Improvement Heuristics

### 1. Intra-Route Improvement (2-Opt)

```python
def intra_route_2opt(route, dist_matrix):
    """
    2-opt improvement within a single route

    Args:
        route: list of node indices
        dist_matrix: distance matrix

    Returns:
        improved route
    """
    improved = True
    best_route = route.copy()

    while improved:
        improved = False
        n = len(best_route)

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                # Calculate change in distance
                delta = (
                    dist_matrix[best_route[i-1]][best_route[j]] +
                    dist_matrix[best_route[i]][best_route[j+1]] -
                    dist_matrix[best_route[i-1]][best_route[i]] -
                    dist_matrix[best_route[j]][best_route[j+1]]
                )

                if delta < -1e-10:
                    # Improvement found - reverse segment
                    best_route[i:j+1] = reversed(best_route[i:j+1])
                    improved = True
                    break

            if improved:
                break

    return best_route


def improve_all_routes_2opt(routes, dist_matrix):
    """
    Apply 2-opt to all routes

    Args:
        routes: list of routes
        dist_matrix: distance matrix

    Returns:
        improved routes and total distance
    """
    improved_routes = []

    for route in routes:
        improved_route = intra_route_2opt(route, dist_matrix)
        improved_routes.append(improved_route)

    # Calculate total distance
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in improved_routes
    )

    return {
        'routes': improved_routes,
        'total_distance': total_distance
    }
```

### 2. Inter-Route Improvement (Cross-Exchange)

```python
def cross_exchange(routes, dist_matrix, demands, vehicle_capacity):
    """
    Cross-exchange operator between routes

    Tries swapping segments between different routes

    Args:
        routes: list of routes
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity

    Returns:
        improved routes
    """
    num_routes = len(routes)
    improved = True

    while improved:
        improved = False

        for r1 in range(num_routes):
            for r2 in range(r1 + 1, num_routes):
                route1 = routes[r1]
                route2 = routes[r2]

                # Try swapping single customers
                for i in range(1, len(route1) - 1):
                    for j in range(1, len(route2) - 1):
                        # Check capacity feasibility
                        customer1 = route1[i]
                        customer2 = route2[j]

                        load1 = sum(demands[c] for c in route1[1:-1])
                        load2 = sum(demands[c] for c in route2[1:-1])

                        new_load1 = load1 - demands[customer1] + demands[customer2]
                        new_load2 = load2 - demands[customer2] + demands[customer1]

                        if (new_load1 > vehicle_capacity or
                            new_load2 > vehicle_capacity):
                            continue

                        # Calculate change in distance
                        # Current edges
                        current_cost = (
                            dist_matrix[route1[i-1]][route1[i]] +
                            dist_matrix[route1[i]][route1[i+1]] +
                            dist_matrix[route2[j-1]][route2[j]] +
                            dist_matrix[route2[j]][route2[j+1]]
                        )

                        # New edges after swap
                        new_cost = (
                            dist_matrix[route1[i-1]][customer2] +
                            dist_matrix[customer2][route1[i+1]] +
                            dist_matrix[route2[j-1]][customer1] +
                            dist_matrix[customer1][route2[j+1]]
                        )

                        if new_cost < current_cost - 1e-10:
                            # Perform swap
                            route1[i] = customer2
                            route2[j] = customer1
                            improved = True
                            break

                    if improved:
                        break

                if improved:
                    break

            if improved:
                break

    return routes


def relocate_operator(routes, dist_matrix, demands, vehicle_capacity):
    """
    Relocate operator: move customer from one route to another

    Args:
        routes: list of routes
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity

    Returns:
        improved routes
    """
    num_routes = len(routes)
    improved = True

    while improved:
        improved = False

        for r1 in range(num_routes):
            for r2 in range(num_routes):
                if r1 == r2:
                    continue

                route1 = routes[r1]
                route2 = routes[r2]

                # Try moving each customer from route1 to route2
                for i in range(1, len(route1) - 1):
                    customer = route1[i]

                    # Check if route2 can accommodate this customer
                    load2 = sum(demands[c] for c in route2[1:-1])
                    if load2 + demands[customer] > vehicle_capacity:
                        continue

                    # Try inserting at each position in route2
                    for j in range(1, len(route2)):
                        # Calculate change in distance
                        # Removal cost
                        removal_cost = (
                            dist_matrix[route1[i-1]][route1[i]] +
                            dist_matrix[route1[i]][route1[i+1]] -
                            dist_matrix[route1[i-1]][route1[i+1]]
                        )

                        # Insertion cost
                        insertion_cost = (
                            dist_matrix[route2[j-1]][customer] +
                            dist_matrix[customer][route2[j]] -
                            dist_matrix[route2[j-1]][route2[j]]
                        )

                        delta = insertion_cost - removal_cost

                        if delta < -1e-10:
                            # Perform move
                            route2.insert(j, customer)
                            route1.pop(i)
                            improved = True
                            break

                    if improved:
                        break

                if improved:
                    break

            if improved:
                break

    # Remove empty routes
    routes = [r for r in routes if len(r) > 2]

    return routes
```

---

## Metaheuristics

### 1. Genetic Algorithm for VRP

```python
import random

def genetic_algorithm_vrp(dist_matrix, demands, vehicle_capacity,
                         max_vehicles, population_size=50,
                         generations=200, mutation_rate=0.15):
    """
    Genetic Algorithm for VRP

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        max_vehicles: maximum number of vehicles
        population_size: GA population size
        generations: number of generations
        mutation_rate: mutation probability

    Returns:
        best solution found
    """
    n = len(dist_matrix)
    depot = 0
    customers = list(range(1, n))

    def decode_chromosome(chromosome):
        """
        Decode chromosome into routes

        Chromosome is a permutation of customers with
        route delimiters
        """
        routes = []
        current_route = [depot]
        current_load = 0

        for gene in chromosome:
            if gene < 0:  # Route delimiter
                if len(current_route) > 1:
                    current_route.append(depot)
                    routes.append(current_route)
                current_route = [depot]
                current_load = 0
            else:  # Customer
                if current_load + demands[gene] <= vehicle_capacity:
                    current_route.append(gene)
                    current_load += demands[gene]
                else:
                    # Start new route
                    current_route.append(depot)
                    routes.append(current_route)
                    current_route = [depot, gene]
                    current_load = demands[gene]

        if len(current_route) > 1:
            current_route.append(depot)
            routes.append(current_route)

        return routes

    def calculate_fitness(chromosome):
        """Calculate fitness (inverse of total distance)"""
        routes = decode_chromosome(chromosome)

        if len(routes) > max_vehicles:
            return 0  # Infeasible

        total_distance = sum(
            sum(dist_matrix[routes[i][j]][routes[i][j+1]]
                for j in range(len(routes[i])-1))
            for i in range(len(routes))
        )

        return 1.0 / (1.0 + total_distance)

    def create_individual():
        """Create random chromosome"""
        chromosome = customers.copy()
        random.shuffle(chromosome)

        # Insert random route delimiters
        num_delimiters = random.randint(0, max_vehicles - 1)
        positions = random.sample(range(len(chromosome)), num_delimiters)

        for pos in sorted(positions, reverse=True):
            chromosome.insert(pos, -1)  # -1 is route delimiter

        return chromosome

    def crossover(parent1, parent2):
        """Order crossover"""
        # Remove delimiters
        p1_customers = [g for g in parent1 if g >= 0]
        p2_customers = [g for g in parent2 if g >= 0]

        # Perform OX crossover
        size = len(p1_customers)
        start, end = sorted(random.sample(range(size), 2))

        child = [-2] * size
        child[start:end] = p1_customers[start:end]

        pos = end
        for gene in p2_customers[end:] + p2_customers[:end]:
            if gene not in child:
                if pos >= size:
                    pos = 0
                child[pos] = gene
                pos += 1

        # Add random delimiters
        num_delimiters = random.randint(0, max_vehicles - 1)
        positions = random.sample(range(len(child)), num_delimiters)

        for pos in sorted(positions, reverse=True):
            child.insert(pos, -1)

        return child

    def mutate(chromosome):
        """Swap mutation"""
        if random.random() < mutation_rate:
            # Get customer positions (not delimiters)
            customer_positions = [i for i, g in enumerate(chromosome) if g >= 0]

            if len(customer_positions) >= 2:
                i, j = random.sample(customer_positions, 2)
                chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

        return chromosome

    # Initialize population
    population = [create_individual() for _ in range(population_size)]

    best_chromosome = None
    best_fitness = 0

    for generation in range(generations):
        # Evaluate fitness
        fitnesses = [calculate_fitness(ind) for ind in population]

        # Track best
        max_fitness = max(fitnesses)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_chromosome = population[fitnesses.index(max_fitness)].copy()

        # Selection and reproduction
        new_population = []

        # Elitism
        elite_count = int(0.1 * population_size)
        elite_indices = sorted(range(len(fitnesses)),
                             key=lambda i: fitnesses[i],
                             reverse=True)[:elite_count]
        new_population = [population[i].copy() for i in elite_indices]

        # Create offspring
        while len(new_population) < population_size:
            # Tournament selection
            parent1 = max(random.sample(list(zip(population, fitnesses)), 3),
                         key=lambda x: x[1])[0]
            parent2 = max(random.sample(list(zip(population, fitnesses)), 3),
                         key=lambda x: x[1])[0]

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    # Decode best solution
    best_routes = decode_chromosome(best_chromosome)

    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in best_routes
    )

    return {
        'routes': best_routes,
        'total_distance': total_distance,
        'num_vehicles': len(best_routes)
    }
```

### 2. Large Neighborhood Search (LNS)

```python
def large_neighborhood_search_vrp(dist_matrix, demands, vehicle_capacity,
                                 initial_routes, max_iterations=100,
                                 destroy_size=0.3):
    """
    Large Neighborhood Search for VRP

    Destroys and repairs parts of the solution iteratively

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        initial_routes: initial solution
        max_iterations: number of iterations
        destroy_size: fraction of customers to remove (0-1)

    Returns:
        improved solution
    """
    import copy

    def calculate_cost(routes):
        return sum(
            sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
            for route in routes
        )

    def shaw_removal(routes, num_remove):
        """
        Shaw removal: remove similar customers
        """
        all_customers = []
        for route in routes:
            all_customers.extend(route[1:-1])

        if not all_customers:
            return routes, []

        # Select seed customer randomly
        seed = random.choice(all_customers)

        # Calculate relatedness (based on distance)
        relatedness = []
        for customer in all_customers:
            if customer != seed:
                similarity = dist_matrix[seed][customer]
                relatedness.append((similarity, customer))

        relatedness.sort()

        # Remove most related customers
        to_remove = {seed}
        for _, customer in relatedness[:num_remove-1]:
            to_remove.add(customer)

        # Remove from routes
        new_routes = []
        for route in routes:
            new_route = [route[0]]
            for customer in route[1:-1]:
                if customer not in to_remove:
                    new_route.append(customer)
            new_route.append(route[-1])

            if len(new_route) > 2:
                new_routes.append(new_route)

        return new_routes, list(to_remove)

    def greedy_insertion(routes, removed_customers):
        """
        Greedily reinsert removed customers
        """
        depot = routes[0][0]
        uninserted = removed_customers.copy()

        while uninserted:
            best_customer = None
            best_route_idx = None
            best_position = None
            best_cost_increase = float('inf')

            # Try inserting each customer
            for customer in uninserted:
                # Try each route
                for route_idx, route in enumerate(routes):
                    # Check capacity
                    current_load = sum(demands[c] for c in route[1:-1])
                    if current_load + demands[customer] > vehicle_capacity:
                        continue

                    # Try each position
                    for pos in range(1, len(route)):
                        cost_increase = (
                            dist_matrix[route[pos-1]][customer] +
                            dist_matrix[customer][route[pos]] -
                            dist_matrix[route[pos-1]][route[pos]]
                        )

                        if cost_increase < best_cost_increase:
                            best_cost_increase = cost_increase
                            best_customer = customer
                            best_route_idx = route_idx
                            best_position = pos

            if best_customer is None:
                # Create new route
                routes.append([depot, uninserted[0], depot])
                uninserted.pop(0)
            else:
                # Insert customer
                routes[best_route_idx].insert(best_position, best_customer)
                uninserted.remove(best_customer)

        return routes

    # LNS main loop
    current_routes = copy.deepcopy(initial_routes)
    current_cost = calculate_cost(current_routes)

    best_routes = copy.deepcopy(current_routes)
    best_cost = current_cost

    all_customers = []
    for route in current_routes:
        all_customers.extend(route[1:-1])

    num_remove = max(1, int(len(all_customers) * destroy_size))

    for iteration in range(max_iterations):
        # Destroy
        partial_routes, removed = shaw_removal(current_routes, num_remove)

        # Repair
        new_routes = greedy_insertion(partial_routes, removed)

        # Evaluate
        new_cost = calculate_cost(new_routes)

        # Accept or reject (simulated annealing acceptance)
        temp = 100 * (1 - iteration / max_iterations)
        if new_cost < current_cost or random.random() < np.exp(-(new_cost - current_cost) / temp):
            current_routes = new_routes
            current_cost = new_cost

            if new_cost < best_cost:
                best_routes = copy.deepcopy(new_routes)
                best_cost = new_cost

    return {
        'routes': best_routes,
        'total_distance': best_cost,
        'num_vehicles': len(best_routes)
    }
```

---

## Using OR-Tools

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrp_ortools(dist_matrix, demands, vehicle_capacities,
                     num_vehicles, depot=0, time_limit=30):
    """
    Solve VRP using Google OR-Tools

    Most practical and efficient approach for real-world problems

    Args:
        dist_matrix: n x n distance matrix
        demands: list of demands for each location
        vehicle_capacities: list of capacities (or single value)
        num_vehicles: number of vehicles
        depot: depot index
        time_limit: time limit in seconds

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)

    # Handle uniform fleet
    if isinstance(vehicle_capacities, (int, float)):
        vehicle_capacities = [vehicle_capacities] * num_vehicles

    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot)

    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node] * 100)  # Scale for integer

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Demand callback
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    # Add capacity constraints
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        vehicle_capacities,  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = time_limit
    search_parameters.log_search = True

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        routes = []
        total_distance = 0
        total_load = 0

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

            if len(route) > 2:  # Route has customers
                routes.append(route)
                total_load += route_load

                # Calculate route distance
                route_distance = 0
                for i in range(len(route) - 1):
                    route_distance += dist_matrix[route[i]][route[i+1]]
                total_distance += route_distance

        return {
            'status': 'Optimal' if solution.ObjectiveValue() > 0 else 'Feasible',
            'routes': routes,
            'total_distance': total_distance,
            'num_vehicles_used': len(routes),
            'total_load': total_load,
            'objective_value': solution.ObjectiveValue() / 100.0
        }
    else:
        return {
            'status': 'No solution found',
            'routes': None
        }


# Example usage with visualization
def visualize_vrp_solution(coordinates, routes, save_path=None):
    """
    Visualize VRP solution

    Args:
        coordinates: list of (x, y) coordinates
        routes: list of routes
        save_path: path to save figure
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 8))

    colors = plt.cm.tab10(np.linspace(0, 1, len(routes)))

    # Plot routes
    for idx, route in enumerate(routes):
        route_coords = [coordinates[i] for i in route]
        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]

        plt.plot(xs, ys, 'o-', color=colors[idx],
                linewidth=2, markersize=8,
                label=f'Vehicle {idx+1}')

    # Plot depot
    depot = coordinates[0]
    plt.plot(depot[0], depot[1], 's', color='red',
            markersize=15, label='Depot')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('VRP Solution')
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


# Complete example
if __name__ == "__main__":
    # Generate random problem
    np.random.seed(42)

    n = 21  # 1 depot + 20 customers
    coordinates = np.random.rand(n, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coordinates[i] - coordinates[j])

    # Demands (depot has 0 demand)
    demands = [0] + [random.randint(5, 25) for _ in range(n-1)]

    vehicle_capacity = 100
    num_vehicles = 5

    print("Solving VRP with OR-Tools...")
    result = solve_vrp_ortools(dist_matrix, demands, vehicle_capacity,
                              num_vehicles, time_limit=30)

    print(f"\nStatus: {result['status']}")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"Vehicles Used: {result['num_vehicles_used']}/{num_vehicles}")
    print(f"Total Load: {result['total_load']}")

    print("\nRoutes:")
    for i, route in enumerate(result['routes']):
        route_load = sum(demands[j] for j in route[1:-1])
        route_dist = sum(dist_matrix[route[j]][route[j+1]]
                        for j in range(len(route)-1))
        print(f"  Vehicle {i+1}: {route}")
        print(f"    Load: {route_load}/{vehicle_capacity}")
        print(f"    Distance: {route_dist:.2f}")

    # Visualize
    visualize_vrp_solution(coordinates, result['routes'])
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **OR-Tools (Google)**: Best for practical VRP (highly recommended)
- **PuLP**: MIP modeling
- **Pyomo**: Advanced modeling
- **VRPy**: VRP-specific library
- **python-tsp**: TSP and VRP utilities

**Metaheuristics:**
- **pymhlib**: Metaheuristic library
- **deap**: Evolutionary algorithms
- **pyswarms**: Particle swarm optimization

**Visualization:**
- **matplotlib**: Basic plots
- **plotly**: Interactive visualization
- **folium**: Map visualization with real coordinates

### Commercial Software

- **Gurobi**: State-of-art MIP solver
- **CPLEX**: IBM solver
- **Xpress**: FICO optimization
- **ORTEC**: Commercial routing software
- **Descartes**: Route planning software

### Cloud Services

- **Google Maps Platform**: Distance Matrix API
- **HERE Routing API**: Commercial routing
- **Azure Maps**: Microsoft routing service

---

## Common Challenges & Solutions

### Challenge: Problem Too Large

**Problem:**
- 500+ customers makes exact methods impractical
- Need solutions in minutes, not hours

**Solutions:**
- Use OR-Tools with time limits
- Clarke-Wright + 2-opt
- Decompose: cluster customers, solve subproblems
- Rolling horizon for dynamic problems

### Challenge: Heterogeneous Fleet

**Problem:**
- Different vehicle types (capacity, cost, speed)
- Different drivers, shifts

**Solutions:**
- Extend formulation with vehicle-specific parameters
- OR-Tools handles naturally with different capacity arrays
- Sequential approach: assign to vehicle types, then route

### Challenge: Time Windows

**Problem:**
- Customers have delivery time windows
- See **vrp-time-windows** skill

**Solutions:**
- Add temporal constraints to formulation
- Use specialized time window algorithms
- OR-Tools time window dimension

### Challenge: Real-World Distances

**Problem:**
- Euclidean distances unrealistic
- Need real road network

**Solutions:**
- Use Google Maps Distance Matrix API
- Pre-compute distance/time matrix
- Cache frequently used routes
- Consider traffic patterns

### Challenge: Dynamic Requests

**Problem:**
- New orders arrive during execution
- Need to reoptimize on the fly

**Solutions:**
- Keep routes with slack capacity
- Fast re-optimization heuristics
- Insertion methods for new customers
- Trigger re-optimization periodically

---

## Output Format

### VRP Solution Report

**Problem Instance:**
- Customers: 50
- Vehicles: 5 (capacity: 100 units each)
- Depot: Distribution Center
- Total demand: 487 units

**Solution Quality:**

| Metric | Value |
|--------|-------|
| Total Distance | 1,247.3 km |
| Vehicles Used | 5 / 5 |
| Average Route Distance | 249.5 km |
| Total Load | 487 / 500 units |
| Average Load per Vehicle | 97.4% |
| Solution Time | 8.3 seconds |

**Route Details:**

**Vehicle 1:** DC → C12 → C34 → C7 → C23 → DC
- Distance: 235.4 km
- Load: 98 / 100 units (98%)
- Customers: 4

**Vehicle 2:** DC → C5 → C18 → C42 → C31 → C9 → DC
- Distance: 278.9 km
- Load: 95 / 100 units (95%)
- Customers: 5

[Continue for all vehicles...]

**Statistics:**
- Average customers per route: 10.0
- Longest route: Vehicle 2 (278.9 km)
- Shortest route: Vehicle 5 (198.7 km)
- Total driving time: ~15.8 hours

---

## Questions to Ask

If you need more context:
1. How many customers need service? How many vehicles available?
2. What are the vehicle capacities? Homogeneous or heterogeneous fleet?
3. What units are demands measured in? (weight, volume, pallets)
4. Are there time windows for deliveries?
5. Is there a maximum route duration or distance?
6. Do you have coordinates or a distance matrix?
7. Fixed cost per vehicle or just distance-based?
8. Are there multiple depots?
9. Is this a one-time problem or recurring daily?
10. What's the acceptable solution time?

---

## Related Skills

- **traveling-salesman-problem**: For single vehicle routing
- **vrp-time-windows**: For VRP with time window constraints
- **capacitated-vrp**: For detailed CVRP formulations
- **multi-depot-vrp**: For problems with multiple depots
- **pickup-delivery-problem**: For pickup and delivery VRP
- **vrp-backhauls**: For VRP with pickups after deliveries
- **split-delivery-vrp**: For allowing multiple visits
- **route-optimization**: For practical routing applications
- **last-mile-delivery**: For final delivery mile optimization
- **fleet-management**: For overall fleet operations
