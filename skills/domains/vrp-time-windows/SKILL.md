---
name: vrp-time-windows
description: When the user wants to solve VRP with time windows (VRPTW), optimize routes with delivery time constraints, or handle appointment scheduling. Also use when the user mentions "VRPTW," "time window routing," "scheduled deliveries," "appointment routing," "delivery windows," "earliest/latest delivery," or "hard/soft time windows." For basic VRP, see vehicle-routing-problem.
---

# Vehicle Routing Problem with Time Windows (VRPTW)

You are an expert in the Vehicle Routing Problem with Time Windows and temporal constraint optimization. Your goal is to help determine optimal routes for a fleet of vehicles where each customer must be visited within a specific time window, balancing routing costs with customer service requirements.

## Initial Assessment

Before solving VRPTW instances, understand:

1. **Time Window Characteristics**
   - Hard time windows (must be satisfied) or soft (can violate with penalty)?
   - How many customers have time windows? All or subset?
   - Width of time windows? (narrow = harder problem)
   - Distribution of windows throughout the day?

2. **Temporal Parameters**
   - Service time at each customer?
   - Travel times between locations?
   - Vehicle shift duration/maximum route time?
   - Depot operating hours?
   - Driver break requirements?

3. **Fleet Information**
   - Number of vehicles available?
   - Vehicle capacities?
   - Earliest start time from depot?
   - Latest return time to depot?

4. **Problem Scale**
   - Small (< 25 customers): Exact methods possible
   - Medium (25-100 customers): Advanced heuristics
   - Large (100+ customers): Metaheuristics required

5. **Objectives**
   - Minimize total distance/time?
   - Minimize number of vehicles (primary)?
   - Minimize time window violations?
   - Minimize waiting time?

---

## Mathematical Formulation

### VRPTW with Hard Time Windows

**Sets:**
- V = {0, 1, ..., n}: Nodes (0 = depot, 1..n = customers)
- K = {1, ..., m}: Vehicles

**Parameters:**
- c_{ij}: Cost/distance from node i to j
- t_{ij}: Travel time from node i to j
- d_i: Demand at customer i
- s_i: Service time at customer i
- [e_i, l_i]: Time window at customer i (earliest, latest)
- Q_k: Capacity of vehicle k
- T_max: Maximum route duration

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j
- w_i ≥ 0: Arrival time at customer i

**Objective Function:**
```
Minimize: Σ_{k∈K} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk}
```

Or minimize vehicles first:
```
Minimize: Σ_{k∈K} Σ_{j∈V\{0}} x_{0jk} + α * Σ_{k∈K} Σ_{i,j∈V} c_{ij} * x_{ijk}
```

**Constraints:**
```
1. Each customer visited exactly once:
   Σ_{k∈K} Σ_{i∈V} x_{ijk} = 1,  ∀j ∈ V\{0}

2. Flow conservation:
   Σ_{i∈V} x_{ihk} - Σ_{j∈V} x_{hjk} = 0,  ∀h ∈ V, ∀k ∈ K

3. Vehicle starts from depot:
   Σ_{j∈V\{0}} x_{0jk} ≤ 1,  ∀k ∈ K

4. Vehicle returns to depot:
   Σ_{i∈V\{0}} x_{i0k} ≤ 1,  ∀k ∈ K

5. Capacity constraint:
   Σ_{i∈V\{0}} Σ_{j∈V} d_i * x_{ijk} ≤ Q_k,  ∀k ∈ K

6. Time window constraints:
   e_i ≤ w_i ≤ l_i,  ∀i ∈ V

7. Time consistency (if vehicle k goes from i to j):
   w_i + s_i + t_{ij} ≤ w_j + M*(1 - Σ_k x_{ijk}),  ∀i,j ∈ V, i≠j

8. Maximum route duration:
   w_i + s_i + t_{i0} ≤ T_max,  ∀i ∈ V\{0}

9. Binary variables:
   x_{ijk} ∈ {0,1},  ∀i,j ∈ V, ∀k ∈ K
```

### Soft Time Windows Formulation

Add penalty variables and costs:

**Additional Variables:**
- α_i ≥ 0: Early arrival at i (before e_i)
- β_i ≥ 0: Late arrival at i (after l_i)

**Modified Objective:**
```
Minimize: Σ_{k,i,j} c_{ij} * x_{ijk} +
          Σ_i (penalty_early * α_i + penalty_late * β_i)
```

**Modified Time Window Constraints:**
```
w_i + α_i ≥ e_i,  ∀i
w_i - β_i ≤ l_i,  ∀i
```

---

## Exact Algorithms

### 1. Branch-and-Price for VRPTW

```python
from pulp import *
import numpy as np

def vrptw_mip(dist_matrix, time_matrix, demands, time_windows,
              service_times, vehicle_capacity, num_vehicles,
              depot=0, max_route_time=480):
    """
    VRPTW using MIP formulation

    Args:
        dist_matrix: n x n distance matrix
        time_matrix: n x n travel time matrix (minutes)
        demands: list of demands
        time_windows: list of (earliest, latest) tuples (minutes)
        service_times: list of service times (minutes)
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index
        max_route_time: maximum route duration (minutes)

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    customers = [i for i in range(n) if i != depot]

    # Create problem
    prob = LpProblem("VRPTW", LpMinimize)

    # Decision variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(num_vehicles):
                    x[i,j,k] = LpVariable(f"x_{i}_{j}_{k}", cat='Binary')

    # Arrival time variables
    w = {}
    for i in range(n):
        for k in range(num_vehicles):
            w[i,k] = LpVariable(f"w_{i}_{k}",
                               lowBound=time_windows[i][0],
                               upBound=time_windows[i][1],
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

    # 3. Capacity constraints
    for k in range(num_vehicles):
        prob += lpSum([demands[j] * x[i,j,k]
                      for i in range(n) for j in customers if i != j]) \
                <= vehicle_capacity, f"Capacity_{k}"

    # 4. Time consistency constraints
    M = 10000  # Big-M
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(num_vehicles):
                    prob += (w[i,k] + service_times[i] + time_matrix[i][j] <=
                            w[j,k] + M * (1 - x[i,j,k])), \
                            f"Time_{i}_{j}_{k}"

    # 5. Time windows already enforced by variable bounds

    # 6. Maximum route duration
    for k in range(num_vehicles):
        for i in customers:
            prob += (w[i,k] + service_times[i] + time_matrix[i][depot] <=
                    time_windows[depot][1]), f"MaxTime_{i}_{k}"

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=600))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        routes = []
        arrival_times = []

        for k in range(num_vehicles):
            route = [depot]
            times = [w[depot,k].varValue]
            current = depot

            while True:
                next_node = None
                for j in range(n):
                    if j != current and (current,j,k) in x:
                        if x[current,j,k].varValue > 0.5:
                            next_node = j
                            break

                if next_node is None or next_node == depot:
                    route.append(depot)
                    times.append(w[depot,k].varValue +
                               sum(service_times[route[i]] + time_matrix[route[i]][route[i+1]]
                                   for i in range(len(route)-1)))
                    break

                route.append(next_node)
                times.append(w[next_node,k].varValue)
                current = next_node

            if len(route) > 2:
                routes.append(route)
                arrival_times.append(times)

        return {
            'status': LpStatus[prob.status],
            'total_distance': value(prob.objective),
            'routes': routes,
            'arrival_times': arrival_times,
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
```

---

## Constructive Heuristics

### 1. Solomon's I1 Insertion Heuristic

```python
def solomon_i1_insertion(dist_matrix, time_matrix, demands, time_windows,
                        service_times, vehicle_capacity, depot=0,
                        alpha=1.0, mu=1.0, lambda_param=1.0):
    """
    Solomon's I1 insertion heuristic for VRPTW

    One of the best constructive heuristics for VRPTW

    Args:
        dist_matrix: distance matrix
        time_matrix: travel time matrix
        demands: customer demands
        time_windows: list of (earliest, latest) tuples
        service_times: service times
        vehicle_capacity: vehicle capacity
        depot: depot index
        alpha, mu, lambda_param: criterion weights

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    customers = set(range(n)) - {depot}
    routes = []
    route_loads = []
    route_times = []

    while customers:
        # Initialize new route with seed customer
        # Select farthest customer from depot
        seed = max(customers, key=lambda c: dist_matrix[depot][c])

        route = [depot, seed, depot]
        current_time = [time_windows[depot][0],
                       max(time_windows[depot][0] + time_matrix[depot][seed],
                           time_windows[seed][0]),
                       0]

        # Update current_time[2] (return to depot)
        current_time[2] = (current_time[1] + service_times[seed] +
                          time_matrix[seed][depot])

        current_load = demands[seed]
        customers.remove(seed)

        # Insert remaining customers into this route
        while customers:
            best_customer = None
            best_position = None
            best_criterion = float('inf')

            # Try inserting each unrouted customer
            for customer in list(customers):
                if current_load + demands[customer] > vehicle_capacity:
                    continue

                # Try each insertion position
                for pos in range(1, len(route)):
                    i = route[pos - 1]
                    j = route[pos]

                    # Calculate feasibility
                    # Arrival time at customer
                    arrival_at_customer = (current_time[pos-1] +
                                         service_times[i] +
                                         time_matrix[i][customer])

                    # Check time window feasibility
                    if arrival_at_customer > time_windows[customer][1]:
                        continue  # Too late

                    # Start service time (wait if early)
                    start_service = max(arrival_at_customer,
                                      time_windows[customer][0])

                    # Check if rest of route is still feasible
                    push_forward = max(0, start_service + service_times[customer] +
                                     time_matrix[customer][j] - current_time[pos])

                    # Check if pushing forward violates time windows
                    feasible = True
                    temp_time = current_time[pos] + push_forward

                    for k in range(pos, len(route) - 1):
                        if temp_time > time_windows[route[k]][1]:
                            feasible = False
                            break
                        temp_time = (max(temp_time, time_windows[route[k]][0]) +
                                   service_times[route[k]] +
                                   time_matrix[route[k]][route[k+1]])

                    if not feasible:
                        continue

                    # Calculate insertion criterion (c1)
                    # c11: distance increase
                    c11 = (dist_matrix[i][customer] + dist_matrix[customer][j] -
                          mu * dist_matrix[i][j])

                    # c12: time increase
                    c12 = (start_service - current_time[pos-1])

                    c1 = alpha * c11 + (1 - alpha) * c12

                    # c2: distance from depot (encourages early insertion)
                    c2 = dist_matrix[depot][customer]

                    # Combined criterion
                    criterion = lambda_param * c1 - c2

                    if criterion < best_criterion:
                        best_criterion = criterion
                        best_customer = customer
                        best_position = pos

            if best_customer is None:
                break  # No more customers fit

            # Insert best customer
            route.insert(best_position, best_customer)
            current_load += demands[best_customer]

            # Update arrival times
            new_times = [current_time[0]]
            for k in range(1, len(route)):
                arrival = (new_times[k-1] +
                          service_times[route[k-1]] +
                          time_matrix[route[k-1]][route[k]])
                start = max(arrival, time_windows[route[k]][0])
                new_times.append(start)

            current_time = new_times
            customers.remove(best_customer)

        routes.append(route)
        route_loads.append(current_load)

    # Calculate total distance
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes
    )

    return {
        'routes': routes,
        'route_loads': route_loads,
        'total_distance': total_distance,
        'num_vehicles': len(routes)
    }
```

### 2. Nearest Neighbor with Time Windows

```python
def nearest_neighbor_tw(dist_matrix, time_matrix, demands, time_windows,
                       service_times, vehicle_capacity, depot=0):
    """
    Nearest neighbor heuristic adapted for time windows

    Args:
        dist_matrix, time_matrix: distance and time matrices
        demands: customer demands
        time_windows: list of (earliest, latest) tuples
        service_times: service times
        vehicle_capacity: vehicle capacity
        depot: depot index

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    unrouted = set(range(n)) - {depot}
    routes = []

    while unrouted:
        route = [depot]
        current_time = time_windows[depot][0]
        current_load = 0
        current_location = depot

        while True:
            # Find nearest feasible customer
            best_customer = None
            best_distance = float('inf')

            for customer in unrouted:
                # Check capacity
                if current_load + demands[customer] > vehicle_capacity:
                    continue

                # Check time window feasibility
                arrival_time = current_time + time_matrix[current_location][customer]

                if arrival_time > time_windows[customer][1]:
                    continue  # Too late

                # This customer is feasible
                distance = dist_matrix[current_location][customer]

                if distance < best_distance:
                    best_distance = distance
                    best_customer = customer

            if best_customer is None:
                break  # No feasible customers

            # Add customer to route
            route.append(best_customer)
            arrival_time = current_time + time_matrix[current_location][best_customer]
            current_time = max(arrival_time, time_windows[best_customer][0])
            current_time += service_times[best_customer]
            current_load += demands[best_customer]
            current_location = best_customer
            unrouted.remove(best_customer)

        # Return to depot
        route.append(depot)
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

### 1. 2-Opt with Time Window Feasibility

```python
def two_opt_tw(route, dist_matrix, time_matrix, time_windows, service_times):
    """
    2-opt improvement with time window checks

    Args:
        route: route to improve
        dist_matrix: distance matrix
        time_matrix: travel time matrix
        time_windows: time windows
        service_times: service times

    Returns:
        improved route
    """
    def check_tw_feasibility(route):
        """Check if route satisfies all time windows"""
        current_time = time_windows[route[0]][0]

        for i in range(len(route) - 1):
            current_time += time_matrix[route[i]][route[i+1]]

            # Check if arrival is within time window
            if current_time > time_windows[route[i+1]][1]:
                return False

            # Wait if early
            current_time = max(current_time, time_windows[route[i+1]][0])
            current_time += service_times[route[i+1]]

        return True

    improved = True
    best_route = route.copy()

    while improved:
        improved = False
        n = len(best_route)

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                # Try reversing segment [i, j]
                new_route = best_route.copy()
                new_route[i:j+1] = reversed(new_route[i:j+1])

                # Check time window feasibility
                if not check_tw_feasibility(new_route):
                    continue

                # Calculate distance change
                old_dist = (dist_matrix[best_route[i-1]][best_route[i]] +
                           dist_matrix[best_route[j]][best_route[j+1]])
                new_dist = (dist_matrix[new_route[i-1]][new_route[i]] +
                           dist_matrix[new_route[j]][new_route[j+1]])

                if new_dist < old_dist - 1e-10:
                    best_route = new_route
                    improved = True
                    break

            if improved:
                break

    return best_route
```

### 2. Cross-Exchange with Time Windows

```python
def cross_exchange_tw(routes, dist_matrix, time_matrix, demands,
                     time_windows, service_times, vehicle_capacity):
    """
    Cross-exchange operator with time window feasibility

    Args:
        routes: list of routes
        dist_matrix, time_matrix: distance and time matrices
        demands: customer demands
        time_windows: time windows
        service_times: service times
        vehicle_capacity: vehicle capacity

    Returns:
        improved routes
    """
    def calculate_route_cost(route):
        return sum(dist_matrix[route[i]][route[i+1]]
                  for i in range(len(route)-1))

    def check_route_feasibility(route):
        """Check capacity and time window feasibility"""
        # Check capacity
        load = sum(demands[c] for c in route[1:-1])
        if load > vehicle_capacity:
            return False

        # Check time windows
        current_time = time_windows[route[0]][0]
        for i in range(len(route) - 1):
            current_time += time_matrix[route[i]][route[i+1]]
            if current_time > time_windows[route[i+1]][1]:
                return False
            current_time = max(current_time, time_windows[route[i+1]][0])
            current_time += service_times[route[i+1]]

        return True

    num_routes = len(routes)
    improved = True

    while improved:
        improved = False

        for r1 in range(num_routes):
            for r2 in range(r1 + 1, num_routes):
                route1 = routes[r1].copy()
                route2 = routes[r2].copy()

                # Try swapping customers
                for i in range(1, len(route1) - 1):
                    for j in range(1, len(route2) - 1):
                        # Create new routes with swap
                        new_route1 = route1.copy()
                        new_route2 = route2.copy()

                        new_route1[i] = route2[j]
                        new_route2[j] = route1[i]

                        # Check feasibility
                        if (not check_route_feasibility(new_route1) or
                            not check_route_feasibility(new_route2)):
                            continue

                        # Calculate improvement
                        old_cost = (calculate_route_cost(route1) +
                                  calculate_route_cost(route2))
                        new_cost = (calculate_route_cost(new_route1) +
                                  calculate_route_cost(new_route2))

                        if new_cost < old_cost - 1e-10:
                            routes[r1] = new_route1
                            routes[r2] = new_route2
                            improved = True
                            break

                    if improved:
                        break

                if improved:
                    break

            if improved:
                break

    return routes
```

---

## Metaheuristics

### 1. Adaptive Large Neighborhood Search (ALNS)

```python
import random

def alns_vrptw(dist_matrix, time_matrix, demands, time_windows,
              service_times, vehicle_capacity, initial_solution,
              iterations=1000, destroy_size=0.3):
    """
    Adaptive Large Neighborhood Search for VRPTW

    Args:
        dist_matrix, time_matrix: distance and time matrices
        demands: customer demands
        time_windows: time windows
        service_times: service times
        vehicle_capacity: vehicle capacity
        initial_solution: initial routes
        iterations: number of iterations
        destroy_size: fraction of customers to remove

    Returns:
        best solution found
    """
    import copy

    def calculate_cost(routes):
        return sum(sum(dist_matrix[route[i]][route[i+1]]
                      for i in range(len(route)-1))
                  for route in routes)

    def shaw_removal_tw(routes, num_remove):
        """Remove related customers (considering location and time)"""
        all_customers = []
        for route in routes:
            all_customers.extend(route[1:-1])

        if not all_customers or num_remove == 0:
            return routes, []

        seed = random.choice(all_customers)
        to_remove = {seed}

        # Calculate relatedness (distance + time window similarity)
        relatedness = []
        for customer in all_customers:
            if customer != seed:
                dist_similarity = dist_matrix[seed][customer]
                time_similarity = abs(time_windows[seed][0] - time_windows[customer][0])
                combined = dist_similarity + 0.1 * time_similarity
                relatedness.append((combined, customer))

        relatedness.sort()

        for _, customer in relatedness[:min(num_remove-1, len(relatedness))]:
            to_remove.add(customer)

        # Remove from routes
        new_routes = []
        depot = routes[0][0]
        for route in routes:
            new_route = [depot]
            for customer in route[1:-1]:
                if customer not in to_remove:
                    new_route.append(customer)
            new_route.append(depot)
            if len(new_route) > 2:
                new_routes.append(new_route)

        return new_routes, list(to_remove)

    def greedy_insertion_tw(routes, removed_customers, depot):
        """Reinsert customers with time window checking"""
        uninserted = removed_customers.copy()

        def check_insertion_feasibility(route, customer, position):
            """Check if inserting customer at position is feasible"""
            new_route = route[:position] + [customer] + route[position:]

            # Check capacity
            load = sum(demands[c] for c in new_route[1:-1])
            if load > vehicle_capacity:
                return False

            # Check time windows
            current_time = time_windows[new_route[0]][0]
            for i in range(len(new_route) - 1):
                current_time += time_matrix[new_route[i]][new_route[i+1]]
                if current_time > time_windows[new_route[i+1]][1]:
                    return False
                current_time = max(current_time, time_windows[new_route[i+1]][0])
                current_time += service_times[new_route[i+1]]

            return True

        while uninserted:
            best_customer = None
            best_route_idx = None
            best_position = None
            best_cost = float('inf')

            for customer in uninserted:
                # Try existing routes
                for r_idx, route in enumerate(routes):
                    for pos in range(1, len(route)):
                        if check_insertion_feasibility(route, customer, pos):
                            cost = (dist_matrix[route[pos-1]][customer] +
                                  dist_matrix[customer][route[pos]] -
                                  dist_matrix[route[pos-1]][route[pos]])

                            if cost < best_cost:
                                best_cost = cost
                                best_customer = customer
                                best_route_idx = r_idx
                                best_position = pos

            if best_customer is None:
                # Create new route
                routes.append([depot, uninserted.pop(0), depot])
            else:
                routes[best_route_idx].insert(best_position, best_customer)
                uninserted.remove(best_customer)

        return routes

    # ALNS main loop
    current_routes = copy.deepcopy(initial_solution)
    current_cost = calculate_cost(current_routes)

    best_routes = copy.deepcopy(current_routes)
    best_cost = current_cost

    depot = current_routes[0][0]

    # Count customers
    all_customers = []
    for route in current_routes:
        all_customers.extend(route[1:-1])
    num_remove = max(1, int(len(all_customers) * destroy_size))

    for iteration in range(iterations):
        # Destroy
        partial_routes, removed = shaw_removal_tw(current_routes, num_remove)

        # Repair
        new_routes = greedy_insertion_tw(partial_routes, removed, depot)

        # Evaluate
        new_cost = calculate_cost(new_routes)

        # Simulated annealing acceptance
        temperature = 100 * (1 - iteration / iterations)
        accept = (new_cost < current_cost or
                 random.random() < np.exp(-(new_cost - current_cost) / max(temperature, 1)))

        if accept:
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

def solve_vrptw_ortools(dist_matrix, time_matrix, demands, time_windows,
                       service_times, vehicle_capacities, num_vehicles,
                       depot=0, time_limit=60):
    """
    Solve VRPTW using Google OR-Tools

    Most practical approach for real-world VRPTW

    Args:
        dist_matrix: distance matrix
        time_matrix: travel time matrix
        demands: customer demands
        time_windows: list of (earliest, latest) tuples
        service_times: service times at each location
        vehicle_capacities: vehicle capacities
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
        return int(dist_matrix[from_node][to_node] * 100)

    distance_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback_index)

    # Time callback
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(time_matrix[from_node][to_node] + service_times[from_node])

    time_callback_index = routing.RegisterTransitCallback(time_callback)

    # Add time window constraints
    routing.AddDimension(
        time_callback_index,
        30,  # allow waiting time
        3000,  # maximum time per vehicle
        False,  # don't force start cumul to zero
        'Time')

    time_dimension = routing.GetDimensionOrDie('Time')

    # Add time window constraints for each location
    for location_idx in range(n):
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(
            int(time_windows[location_idx][0]),
            int(time_windows[location_idx][1])
        )

    # Add time window constraints for depot (all vehicles)
    for vehicle_id in range(num_vehicles):
        start_index = routing.Start(vehicle_id)
        end_index = routing.End(vehicle_id)
        time_dimension.CumulVar(start_index).SetRange(
            int(time_windows[depot][0]),
            int(time_windows[depot][1])
        )
        time_dimension.CumulVar(end_index).SetRange(
            int(time_windows[depot][0]),
            int(time_windows[depot][1])
        )

    # Instantiate route start and end times to produce feasible times
    for i in range(num_vehicles):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Add capacity constraints
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        vehicle_capacities,
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
        arrival_times = []
        total_distance = 0

        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            times = []

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                time_var = time_dimension.CumulVar(index)
                route.append(node)
                times.append(solution.Value(time_var))
                index = solution.Value(routing.NextVar(index))

            # Add depot at end
            node = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            route.append(node)
            times.append(solution.Value(time_var))

            if len(route) > 2:
                routes.append(route)
                arrival_times.append(times)

                # Calculate route distance
                route_distance = sum(dist_matrix[route[i]][route[i+1]]
                                   for i in range(len(route)-1))
                total_distance += route_distance

        return {
            'status': 'Optimal' if solution.ObjectiveValue() > 0 else 'Feasible',
            'routes': routes,
            'arrival_times': arrival_times,
            'total_distance': total_distance,
            'num_vehicles_used': len(routes),
            'objective_value': solution.ObjectiveValue() / 100.0
        }
    else:
        return {
            'status': 'No solution found',
            'routes': None
        }


# Example with visualization
def visualize_vrptw_solution(coordinates, routes, arrival_times, time_windows,
                            save_path=None):
    """
    Visualize VRPTW solution with Gantt chart

    Args:
        coordinates: list of (x, y) coordinates
        routes: list of routes
        arrival_times: arrival times at each location
        time_windows: time windows
        save_path: path to save figure
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot routes
    colors = plt.cm.tab10(np.linspace(0, 1, len(routes)))

    for idx, route in enumerate(routes):
        route_coords = [coordinates[i] for i in route]
        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]

        ax1.plot(xs, ys, 'o-', color=colors[idx],
                linewidth=2, markersize=8,
                label=f'Vehicle {idx+1}')

    depot = coordinates[0]
    ax1.plot(depot[0], depot[1], 's', color='red',
            markersize=15, label='Depot', zorder=10)

    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.set_title('VRPTW Routes')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot Gantt chart
    for idx, (route, times) in enumerate(zip(routes, arrival_times)):
        for i in range(1, len(route) - 1):
            customer = route[i]
            arrival = times[i]
            tw_early, tw_late = time_windows[customer]

            # Draw time window
            ax2.add_patch(Rectangle((tw_early, idx - 0.3),
                                   tw_late - tw_early, 0.6,
                                   facecolor='lightgray', edgecolor='black',
                                   alpha=0.5))

            # Draw arrival/service
            ax2.plot(arrival, idx, 'o', color=colors[idx], markersize=10)
            ax2.text(arrival, idx + 0.4, f'C{customer}',
                    ha='center', va='bottom', fontsize=8)

    ax2.set_xlabel('Time')
    ax2.set_ylabel('Vehicle')
    ax2.set_title('Schedule (Gantt Chart)')
    ax2.set_yticks(range(len(routes)))
    ax2.set_yticklabels([f'Vehicle {i+1}' for i in range(len(routes))])
    ax2.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


# Complete example
if __name__ == "__main__":
    # Generate Solomon-like problem instance
    np.random.seed(42)

    n = 26  # 1 depot + 25 customers
    coordinates = np.random.rand(n, 2) * 100

    # Distance and time matrices
    dist_matrix = np.zeros((n, n))
    time_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist = np.linalg.norm(coordinates[i] - coordinates[j])
            dist_matrix[i][j] = dist
            time_matrix[i][j] = dist / 40 * 60  # 40 km/h in minutes

    # Generate time windows (clustered)
    time_windows = [(0, 480)]  # Depot: 8-hour day

    for i in range(1, n):
        # Random center time
        center = random.randint(60, 420)
        width = random.randint(30, 90)
        time_windows.append((center - width, center + width))

    # Service times
    service_times = [0] + [random.randint(10, 20) for _ in range(n-1)]

    # Demands
    demands = [0] + [random.randint(5, 20) for _ in range(n-1)]

    vehicle_capacity = 100
    num_vehicles = 5

    print("Solving VRPTW with OR-Tools...")
    result = solve_vrptw_ortools(
        dist_matrix, time_matrix, demands, time_windows,
        service_times, vehicle_capacity, num_vehicles,
        time_limit=60
    )

    print(f"\nStatus: {result['status']}")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"Vehicles Used: {result['num_vehicles_used']}/{num_vehicles}")

    print("\nRoute Details:")
    for i, (route, times) in enumerate(zip(result['routes'],
                                           result['arrival_times'])):
        print(f"\nVehicle {i+1}: {route}")
        print("  Arrival times:")
        for j, (customer, time) in enumerate(zip(route, times)):
            tw = time_windows[customer]
            print(f"    Stop {j}: Customer {customer} at time {time:.1f} "
                  f"(window: [{tw[0]:.1f}, {tw[1]:.1f}])")

    # Visualize
    visualize_vrptw_solution(coordinates, result['routes'],
                            result['arrival_times'], time_windows)
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **OR-Tools (Google)**: Best for practical VRPTW (highly recommended)
- **PuLP**: MIP modeling
- **VRPy**: Specialized VRP library with time windows support
- **python-mip**: Alternative MIP library

**Route Planning:**
- **OSRM**: Open Source Routing Machine (real-world distances)
- **Google Maps API**: Distance and time matrices
- **Valhalla**: Open-source routing engine

**Visualization:**
- **matplotlib**: Basic visualization
- **plotly**: Interactive Gantt charts
- **folium**: Map-based visualization

### Benchmark Instances

- **Solomon Instances**: Standard VRPTW benchmarks (R1, C1, RC1, R2, C2, RC2)
- **Gehring & Homberger**: Large-scale VRPTW instances
- **Sintef**: Comprehensive VRP test sets

---

## Common Challenges & Solutions

### Challenge: Tight Time Windows

**Problem:**
- Narrow time windows make problem highly constrained
- Many infeasible combinations

**Solutions:**
- Use time-oriented insertion criteria (Solomon's I1)
- Consider soft time windows with penalties
- Sequence-first, route-second approach
- Allow longer routes if necessary

### Challenge: Wide Time Horizon

**Problem:**
- Time windows span long periods (e.g., all-day delivery)
- Less constraint, but many possible solutions

**Solutions:**
- Use distance/cost as primary criterion
- Consider clustering customers by time preference
- Balance route duration

### Challenge: Mixed Hard/Soft Windows

**Problem:**
- Some customers have strict appointments
- Others are flexible

**Solutions:**
- Two-stage approach: satisfy hard windows first
- Use penalty costs for soft window violations
- Prioritize hard window customers in insertion

### Challenge: Real-World Timing

**Problem:**
- Traffic varies by time of day
- Stochastic travel times

**Solutions:**
- Time-dependent travel time matrices
- Add time buffers/slack
- Stochastic VRPTW models
- Real-time re-optimization

---

## Output Format

### VRPTW Solution Report

**Problem Instance:**
- Customers: 50
- Time Horizon: 8:00 AM - 6:00 PM (600 minutes)
- Vehicles: 5 (capacity: 100 units each)
- Average time window width: 60 minutes

**Solution Quality:**

| Metric | Value |
|--------|-------|
| Total Distance | 892.4 km |
| Total Time | 18.2 hours |
| Vehicles Used | 5 / 5 |
| Average Route Duration | 3.64 hours |
| Time Window Violations | 0 (feasible) |
| Average Waiting Time | 12.3 minutes |

**Route Schedule:**

**Vehicle 1:** Start 8:00 AM

| Stop | Customer | Arrival | Time Window | Wait | Service | Depart |
|------|----------|---------|-------------|------|---------|--------|
| 0 | Depot | 8:00 | [8:00-18:00] | 0 | 0 | 8:00 |
| 1 | C12 | 8:23 | [8:15-9:15] | 0 | 15 | 8:38 |
| 2 | C7 | 9:05 | [9:00-10:00] | 0 | 12 | 9:17 |
| 3 | C34 | 9:42 | [9:30-10:30] | 0 | 10 | 9:52 |
| 4 | Depot | 10:35 | [8:00-18:00] | - | - | - |

**Route Distance:** 187.2 km
**Route Duration:** 2:35
**Total Load:** 97 / 100 units

[Continue for all vehicles...]

**Statistics:**
- On-time arrivals: 100%
- Early arrivals requiring wait: 8%
- Average slack in time windows: 23 minutes

---

## Questions to Ask

If you need more context:
1. Do all customers have time windows or only a subset?
2. Are time windows hard (must satisfy) or soft (can penalize violations)?
3. How wide are the time windows typically?
4. What's the planning horizon? (8 hours, 12 hours, 24 hours)
5. Do you have actual travel times or should we estimate from distances?
6. Are service times significant?
7. Is minimizing vehicles or total distance the primary goal?
8. Do routes have maximum duration limits?
9. Are there driver break requirements?
10. Is this recurring daily or a one-time problem?

---

## Related Skills

- **vehicle-routing-problem**: For basic VRP without time windows
- **traveling-salesman-problem**: For single vehicle routing
- **pickup-delivery-problem**: For paired pickup-delivery with time windows
- **capacitated-vrp**: For pure capacity-focused VRP
- **multi-depot-vrp**: For multiple depot routing
- **route-optimization**: For practical routing applications
- **last-mile-delivery**: For final delivery optimization
- **fleet-management**: For fleet operations
