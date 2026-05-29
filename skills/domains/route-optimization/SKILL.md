---
name: route-optimization
description: When the user wants to optimize delivery routes, solve vehicle routing problems, or minimize transportation costs. Also use when the user mentions "route planning," "delivery optimization," "VRP," "TSP," "multi-stop routing," "route sequencing," or "dispatch optimization." For fleet sizing and management, see fleet-management. For last-mile specific challenges, see last-mile-delivery.
---

# Route Optimization

You are an expert in transportation route optimization and vehicle routing problems. Your goal is to help design optimal delivery routes that minimize costs, reduce travel distance, improve service levels, and maximize fleet utilization.

## Initial Assessment

Before optimizing routes, understand:

1. **Business Context**
   - What type of operation? (delivery, pickup, field service)
   - Fleet size and vehicle types?
   - Current routing method? (manual, basic software, advanced)
   - Primary pain points? (cost, late deliveries, driver overtime)

2. **Operational Constraints**
   - Delivery time windows? (hard/soft constraints)
   - Vehicle capacities (weight, volume, pallets)?
   - Driver shift lengths and break requirements?
   - Service time at each stop?
   - Maximum route duration?

3. **Network Characteristics**
   - Number of stops per day?
   - Depot locations (single/multiple)?
   - Geographic spread? (urban, rural, mixed)
   - Traffic patterns and considerations?
   - Access restrictions (truck routes, height limits)?

4. **Service Requirements**
   - On-time delivery targets?
   - Customer priorities or preferences?
   - Special handling needs?
   - Real-time changes and dynamic requests?

---

## Route Optimization Framework

### Problem Classification

**1. Traveling Salesman Problem (TSP)**
- Single vehicle, visit all locations once
- Return to origin
- Minimize total distance/time
- Use cases: Small deliveries, service routes

**2. Vehicle Routing Problem (VRP)**
- Multiple vehicles from depot
- Each customer visited once
- Capacity constraints
- Minimize total fleet distance/cost

**3. VRP with Time Windows (VRPTW)**
- Customers have delivery time windows
- Hard constraints (must arrive in window)
- Soft constraints (preference, with penalty)
- Most common real-world variant

**4. Capacitated VRP (CVRP)**
- Vehicle capacity limits (weight/volume)
- Cannot exceed capacity on route
- May require return trips

**5. Multi-Depot VRP (MDVRP)**
- Multiple starting locations
- Assign customers to depots
- Optimize depot selection + routes

**6. VRP with Pickup and Delivery (VRPPD)**
- Both pickup and delivery at stops
- Precedence constraints
- Simultaneous or sequential

**7. Dynamic VRP**
- Real-time order insertions
- Route re-optimization during day
- Handle urgent/emergency requests

---

## Optimization Methods

### Exact Methods

**Branch and Bound**
- Guarantees optimal solution
- Only feasible for small problems (<50 stops)
- Exponential time complexity

**Mixed-Integer Programming (MIP)**
- Mathematical optimization model
- Commercial solvers (Gurobi, CPLEX)

```python
from pulp import *
import numpy as np

def vrp_mip_model(distances, demands, vehicle_capacity, num_vehicles):
    """
    Basic VRP using Mixed-Integer Programming

    Parameters:
    - distances: NxN distance matrix
    - demands: list of demands at each location
    - vehicle_capacity: max capacity per vehicle
    - num_vehicles: number of available vehicles
    """

    n = len(distances)  # includes depot at index 0
    customers = range(1, n)
    all_nodes = range(n)
    vehicles = range(num_vehicles)

    # Create problem
    prob = LpProblem("VRP", LpMinimize)

    # Decision variables
    # x[i,j,k] = 1 if vehicle k travels from i to j
    x = LpVariable.dicts("route",
                         [(i,j,k) for i in all_nodes
                          for j in all_nodes
                          for k in vehicles if i != j],
                         cat='Binary')

    # u[i,k] = position of node i in route of vehicle k (for subtour elimination)
    u = LpVariable.dicts("order",
                         [(i,k) for i in customers for k in vehicles],
                         lowBound=1,
                         upBound=n-1,
                         cat='Integer')

    # Objective: minimize total distance
    prob += lpSum([distances[i][j] * x[i,j,k]
                   for i in all_nodes
                   for j in all_nodes
                   for k in vehicles
                   if i != j])

    # Constraints

    # 1. Each customer visited exactly once
    for j in customers:
        prob += lpSum([x[i,j,k]
                      for i in all_nodes
                      for k in vehicles
                      if i != j]) == 1

    # 2. Flow conservation: enter and leave each node
    for k in vehicles:
        for j in all_nodes:
            prob += (lpSum([x[i,j,k] for i in all_nodes if i != j]) ==
                    lpSum([x[j,i,k] for i in all_nodes if i != j]))

    # 3. Each vehicle starts from depot
    for k in vehicles:
        prob += lpSum([x[0,j,k] for j in customers]) <= 1

    # 4. Each vehicle returns to depot
    for k in vehicles:
        prob += lpSum([x[i,0,k] for i in customers]) <= 1

    # 5. Vehicle capacity constraint
    for k in vehicles:
        prob += lpSum([demands[j] * x[i,j,k]
                      for i in all_nodes
                      for j in customers
                      if i != j]) <= vehicle_capacity

    # 6. Subtour elimination (Miller-Tucker-Zemlin)
    for i in customers:
        for j in customers:
            for k in vehicles:
                if i != j:
                    prob += u[i,k] - u[j,k] + n * x[i,j,k] <= n - 1

    # Solve
    prob.solve(PULP_CBC_CMD(msg=1))

    # Extract routes
    routes = extract_routes(x, vehicles, n)

    return {
        'status': LpStatus[prob.status],
        'total_distance': value(prob.objective),
        'routes': routes
    }

def extract_routes(x, vehicles, n):
    """Extract route sequences from solution"""
    routes = []
    for k in vehicles:
        route = [0]  # start at depot
        current = 0
        while True:
            for j in range(n):
                if j != current and (current,j,k) in x:
                    if x[current,j,k].varValue > 0.5:
                        if j == 0:  # back to depot
                            route.append(0)
                            if len(route) > 2:  # non-empty route
                                routes.append(route)
                            current = -1
                            break
                        else:
                            route.append(j)
                            current = j
                            break
            if current == -1 or current == 0:
                break
    return routes
```

### Heuristic Methods

**Nearest Neighbor**
- Start at depot, always visit nearest unvisited customer
- Fast but often suboptimal (10-30% worse than optimal)

```python
import numpy as np

def nearest_neighbor_vrp(distance_matrix, demands, capacity, depot=0):
    """
    Nearest neighbor heuristic for VRP

    Simple construction heuristic - builds routes by always
    selecting the nearest unvisited customer
    """

    n = len(distance_matrix)
    unvisited = set(range(1, n))  # exclude depot
    routes = []

    while unvisited:
        route = [depot]
        current_load = 0
        current_location = depot

        while unvisited:
            # Find nearest feasible customer
            nearest = None
            nearest_dist = float('inf')

            for customer in unvisited:
                if current_load + demands[customer] <= capacity:
                    dist = distance_matrix[current_location][customer]
                    if dist < nearest_dist:
                        nearest = customer
                        nearest_dist = dist

            if nearest is None:
                break  # No feasible customer, return to depot

            route.append(nearest)
            current_load += demands[nearest]
            current_location = nearest
            unvisited.remove(nearest)

        route.append(depot)  # return to depot
        routes.append(route)

    total_distance = sum(calculate_route_distance(route, distance_matrix)
                        for route in routes)

    return {
        'routes': routes,
        'total_distance': total_distance,
        'num_vehicles': len(routes)
    }

def calculate_route_distance(route, distance_matrix):
    """Calculate total distance of a route"""
    distance = 0
    for i in range(len(route) - 1):
        distance += distance_matrix[route[i]][route[i+1]]
    return distance
```

**Savings Algorithm (Clarke-Wright)**
- Merge routes based on savings from combining
- Industry standard heuristic
- Good balance of speed and quality

```python
def clarke_wright_savings(distance_matrix, demands, capacity):
    """
    Clarke-Wright Savings Algorithm for VRP

    Starts with individual routes to each customer,
    then merges routes based on savings
    """

    n = len(distance_matrix)
    depot = 0

    # Calculate savings for all customer pairs
    savings = []
    for i in range(1, n):
        for j in range(i+1, n):
            saving = (distance_matrix[depot][i] +
                     distance_matrix[depot][j] -
                     distance_matrix[i][j])
            savings.append((saving, i, j))

    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])

    # Initialize: each customer has its own route
    routes = {i: [depot, i, depot] for i in range(1, n)}
    route_loads = {i: demands[i] for i in range(1, n)}

    # Try to merge routes based on savings
    for saving_value, i, j in savings:
        # Find routes containing i and j
        route_i = None
        route_j = None

        for route_id, route in routes.items():
            if i in route:
                route_i = route_id
            if j in route:
                route_j = route_id

        # Can only merge if i and j are in different routes
        if route_i != route_j:
            route_i_obj = routes[route_i]
            route_j_obj = routes[route_j]

            # Check if merging is feasible
            combined_load = route_loads[route_i] + route_loads[route_j]

            if combined_load <= capacity:
                # Check if i and j are at ends of their routes
                i_at_end = (route_i_obj[1] == i or route_i_obj[-2] == i)
                j_at_end = (route_j_obj[1] == j or route_j_obj[-2] == j)

                if i_at_end and j_at_end:
                    # Merge routes
                    new_route = merge_routes(route_i_obj, route_j_obj, i, j)

                    # Update routes
                    routes[route_i] = new_route
                    route_loads[route_i] = combined_load

                    del routes[route_j]
                    del route_loads[route_j]

    return {
        'routes': list(routes.values()),
        'total_distance': sum(calculate_route_distance(route, distance_matrix)
                            for route in routes.values()),
        'num_vehicles': len(routes)
    }

def merge_routes(route1, route2, i, j):
    """Merge two routes through nodes i and j"""
    # Remove depot endpoints
    r1 = route1[1:-1]
    r2 = route2[1:-1]

    # Orient routes so i and j connect properly
    if r1[-1] == i and r2[0] == j:
        merged = [0] + r1 + r2 + [0]
    elif r1[-1] == i and r2[-1] == j:
        merged = [0] + r1 + r2[::-1] + [0]
    elif r1[0] == i and r2[0] == j:
        merged = [0] + r1[::-1] + r2 + [0]
    elif r1[0] == i and r2[-1] == j:
        merged = [0] + r2 + r1 + [0]
    else:
        merged = [0] + r1 + r2 + [0]  # fallback

    return merged
```

**Sweep Algorithm**
- Sort customers by angle from depot
- Build routes by sweeping around depot
- Good for clustered customers

```python
import math

def sweep_algorithm(coordinates, demands, capacity, depot_idx=0):
    """
    Sweep Algorithm for VRP

    Sorts customers by polar angle from depot,
    then builds routes by sweeping clockwise
    """

    depot = coordinates[depot_idx]
    n = len(coordinates)

    # Calculate angles from depot
    customers = []
    for i in range(n):
        if i != depot_idx:
            dx = coordinates[i][0] - depot[0]
            dy = coordinates[i][1] - depot[1]
            angle = math.atan2(dy, dx)
            customers.append((i, angle, demands[i]))

    # Sort by angle
    customers.sort(key=lambda x: x[1])

    # Build routes by sweeping
    routes = []
    current_route = [depot_idx]
    current_load = 0

    for customer_id, angle, demand in customers:
        if current_load + demand <= capacity:
            current_route.append(customer_id)
            current_load += demand
        else:
            # Start new route
            current_route.append(depot_idx)
            routes.append(current_route)
            current_route = [depot_idx, customer_id]
            current_load = demand

    # Add final route
    if len(current_route) > 1:
        current_route.append(depot_idx)
        routes.append(current_route)

    return {
        'routes': routes,
        'num_vehicles': len(routes)
    }
```

### Metaheuristic Methods

**Simulated Annealing**
- Probabilistically accept worse solutions
- Escape local optima
- Gradually reduce "temperature"

```python
import random
import math

def simulated_annealing_vrp(initial_solution, distance_matrix,
                           demands, capacity,
                           initial_temp=1000, cooling_rate=0.995,
                           iterations=10000):
    """
    Simulated Annealing for VRP

    Improves initial solution through iterative neighbor search
    with probabilistic acceptance of worse solutions
    """

    current_solution = initial_solution.copy()
    current_cost = calculate_total_distance(current_solution, distance_matrix)

    best_solution = current_solution.copy()
    best_cost = current_cost

    temperature = initial_temp

    for iteration in range(iterations):
        # Generate neighbor solution
        neighbor = generate_neighbor(current_solution, demands, capacity)
        neighbor_cost = calculate_total_distance(neighbor, distance_matrix)

        # Calculate acceptance probability
        delta = neighbor_cost - current_cost

        if delta < 0:
            # Better solution, always accept
            accept = True
        else:
            # Worse solution, accept with probability
            accept_prob = math.exp(-delta / temperature)
            accept = random.random() < accept_prob

        if accept:
            current_solution = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost

        # Cool down
        temperature *= cooling_rate

    return {
        'routes': best_solution,
        'total_distance': best_cost
    }

def generate_neighbor(routes, demands, capacity):
    """Generate neighbor solution using local search operators"""

    neighbor = [route.copy() for route in routes]
    operator = random.choice(['swap', 'relocate', '2-opt'])

    if operator == 'swap' and len(neighbor) >= 2:
        # Swap customers between two routes
        route1_idx = random.randint(0, len(neighbor) - 1)
        route2_idx = random.randint(0, len(neighbor) - 1)
        while route2_idx == route1_idx:
            route2_idx = random.randint(0, len(neighbor) - 1)

        route1 = neighbor[route1_idx]
        route2 = neighbor[route2_idx]

        if len(route1) > 2 and len(route2) > 2:
            pos1 = random.randint(1, len(route1) - 2)
            pos2 = random.randint(1, len(route2) - 2)
            route1[pos1], route2[pos2] = route2[pos2], route1[pos1]

    elif operator == 'relocate':
        # Move customer from one route to another
        if len(neighbor) >= 2:
            route1_idx = random.randint(0, len(neighbor) - 1)
            route2_idx = random.randint(0, len(neighbor) - 1)
            while route2_idx == route1_idx:
                route2_idx = random.randint(0, len(neighbor) - 1)

            route1 = neighbor[route1_idx]
            route2 = neighbor[route2_idx]

            if len(route1) > 2:
                pos1 = random.randint(1, len(route1) - 2)
                customer = route1.pop(pos1)
                pos2 = random.randint(1, len(route2) - 1)
                route2.insert(pos2, customer)

    elif operator == '2-opt':
        # 2-opt within a single route
        route_idx = random.randint(0, len(neighbor) - 1)
        route = neighbor[route_idx]

        if len(route) > 4:
            i = random.randint(1, len(route) - 3)
            j = random.randint(i + 1, len(route) - 2)
            route[i:j+1] = reversed(route[i:j+1])

    return neighbor

def calculate_total_distance(routes, distance_matrix):
    """Calculate total distance across all routes"""
    total = 0
    for route in routes:
        for i in range(len(route) - 1):
            total += distance_matrix[route[i]][route[i+1]]
    return total
```

**Genetic Algorithm**
- Population-based search
- Crossover and mutation operators
- Good for large problems

**Ant Colony Optimization (ACO)**
- Probabilistic construction of solutions
- Pheromone trails guide search
- Good quality solutions

**Large Neighborhood Search (LNS)**
- Destroy and repair parts of solution
- Very effective for large problems

---

## Advanced VRP Variants

### VRP with Time Windows (VRPTW)

```python
def vrptw_earliest_start_heuristic(customers, vehicles, time_windows, service_times, travel_times):
    """
    VRPTW heuristic: insert customers based on earliest feasible start time

    Parameters:
    - customers: list of customer IDs
    - vehicles: list of vehicle objects
    - time_windows: dict {customer_id: (earliest, latest)}
    - service_times: dict {customer_id: service_duration}
    - travel_times: function(from_loc, to_loc) -> travel_time
    """

    routes = []
    unserved = set(customers)

    for vehicle in vehicles:
        if not unserved:
            break

        route = [vehicle.depot]
        current_time = 0
        current_location = vehicle.depot
        route_load = 0

        while unserved:
            # Find best customer to insert
            best_customer = None
            best_start_time = float('inf')

            for customer in unserved:
                # Check capacity
                if route_load + customer.demand > vehicle.capacity:
                    continue

                # Calculate arrival time
                travel_time = travel_times(current_location, customer.location)
                arrival_time = current_time + travel_time

                # Check time window feasibility
                earliest, latest = time_windows[customer.id]

                if arrival_time > latest:
                    continue  # Too late

                start_time = max(arrival_time, earliest)

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_customer = customer

            if best_customer is None:
                break  # No feasible customer

            # Add customer to route
            route.append(best_customer)
            unserved.remove(best_customer)

            travel_time = travel_times(current_location, best_customer.location)
            arrival_time = current_time + travel_time
            earliest, latest = time_windows[best_customer.id]
            current_time = max(arrival_time, earliest) + service_times[best_customer.id]
            current_location = best_customer.location
            route_load += best_customer.demand

        route.append(vehicle.depot)
        routes.append(route)

    return routes
```

### Multi-Depot VRP

```python
def assign_customers_to_depots(customers, depots, distance_matrix):
    """
    Assign customers to nearest depot for MDVRP

    Returns clusters of customers for each depot
    """

    depot_clusters = {depot: [] for depot in depots}

    for customer in customers:
        # Find nearest depot
        nearest_depot = None
        min_distance = float('inf')

        for depot in depots:
            dist = distance_matrix[customer][depot]
            if dist < min_distance:
                min_distance = dist
                nearest_depot = depot

        depot_clusters[nearest_depot].append(customer)

    return depot_clusters

def solve_mdvrp(customers, depots, distance_matrix, demands, capacity):
    """
    Solve Multi-Depot VRP

    1. Assign customers to depots
    2. Solve VRP for each depot independently
    """

    # Assign customers to depots
    clusters = assign_customers_to_depots(customers, depots, distance_matrix)

    all_routes = []
    total_distance = 0

    for depot, depot_customers in clusters.items():
        if not depot_customers:
            continue

        # Solve VRP for this depot
        depot_solution = clarke_wright_savings(
            distance_matrix,
            demands,
            capacity
        )

        all_routes.extend(depot_solution['routes'])
        total_distance += depot_solution['total_distance']

    return {
        'routes': all_routes,
        'total_distance': total_distance,
        'depot_clusters': clusters
    }
```

### Dynamic VRP (Real-Time Routing)

```python
class DynamicVRPSolver:
    """
    Dynamic VRP solver for real-time order insertions

    Handles new orders arriving during route execution
    """

    def __init__(self, initial_routes, distance_matrix):
        self.routes = initial_routes
        self.distance_matrix = distance_matrix
        self.completed_stops = set()

    def insert_urgent_order(self, new_customer, current_vehicle_positions):
        """
        Insert urgent order into existing routes

        Uses cheapest insertion heuristic
        """

        best_route_idx = None
        best_position = None
        min_cost_increase = float('inf')

        for route_idx, route in enumerate(self.routes):
            # Get current position of vehicle on this route
            current_pos = current_vehicle_positions.get(route_idx, 0)

            # Try inserting at each position after current
            for insert_pos in range(current_pos + 1, len(route)):
                # Calculate cost increase
                prev_customer = route[insert_pos - 1]
                next_customer = route[insert_pos]

                current_cost = self.distance_matrix[prev_customer][next_customer]
                new_cost = (self.distance_matrix[prev_customer][new_customer] +
                           self.distance_matrix[new_customer][next_customer])

                cost_increase = new_cost - current_cost

                if cost_increase < min_cost_increase:
                    min_cost_increase = cost_increase
                    best_route_idx = route_idx
                    best_position = insert_pos

        if best_route_idx is not None:
            self.routes[best_route_idx].insert(best_position, new_customer)
            return {
                'success': True,
                'route': best_route_idx,
                'position': best_position,
                'cost_increase': min_cost_increase
            }
        else:
            # Need new route
            self.routes.append([0, new_customer, 0])
            return {
                'success': True,
                'route': len(self.routes) - 1,
                'position': 1,
                'new_route': True
            }

    def mark_completed(self, customer):
        """Mark customer as completed"""
        self.completed_stops.add(customer)

    def reoptimize_remaining(self):
        """Re-optimize remaining stops on all routes"""

        for route in self.routes:
            # Remove completed stops
            route[:] = [stop for stop in route
                       if stop not in self.completed_stops or stop == 0]

        # Remove empty routes
        self.routes = [route for route in self.routes if len(route) > 2]
```

---

## Practical Implementation

### Complete VRP Solver Class

```python
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

class VRPSolver:
    """
    Comprehensive VRP solver with multiple algorithms
    """

    def __init__(self, coordinates, demands, vehicle_capacity,
                 num_vehicles=None, depot_idx=0):
        """
        Initialize VRP solver

        Parameters:
        - coordinates: list of (x, y) tuples for locations
        - demands: list of demand at each location
        - vehicle_capacity: maximum capacity per vehicle
        - num_vehicles: max vehicles (None = unlimited)
        - depot_idx: index of depot location (default 0)
        """

        self.coordinates = np.array(coordinates)
        self.demands = np.array(demands)
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        self.depot_idx = depot_idx

        # Calculate distance matrix
        self.distance_matrix = cdist(self.coordinates, self.coordinates,
                                     metric='euclidean')

        self.best_solution = None
        self.best_cost = float('inf')

    def solve(self, method='clarke_wright', **kwargs):
        """
        Solve VRP using specified method

        Methods:
        - 'nearest_neighbor': Fast, simple heuristic
        - 'clarke_wright': Savings algorithm
        - 'sweep': Angular sweep from depot
        - 'genetic': Genetic algorithm (slower, better quality)
        """

        if method == 'nearest_neighbor':
            solution = nearest_neighbor_vrp(
                self.distance_matrix,
                self.demands,
                self.vehicle_capacity,
                self.depot_idx
            )

        elif method == 'clarke_wright':
            solution = clarke_wright_savings(
                self.distance_matrix,
                self.demands,
                self.vehicle_capacity
            )

        elif method == 'sweep':
            solution = sweep_algorithm(
                self.coordinates,
                self.demands,
                self.vehicle_capacity,
                self.depot_idx
            )

        else:
            raise ValueError(f"Unknown method: {method}")

        # Improve solution with local search
        if kwargs.get('improve', True):
            solution = self.local_search_improvement(solution['routes'])

        self.best_solution = solution
        self.best_cost = solution['total_distance']

        return solution

    def local_search_improvement(self, routes, iterations=1000):
        """
        Improve solution using 2-opt and relocate operators
        """

        current_routes = [route.copy() for route in routes]
        current_cost = calculate_total_distance(current_routes, self.distance_matrix)

        improved = True
        iter_count = 0

        while improved and iter_count < iterations:
            improved = False
            iter_count += 1

            # Try 2-opt within each route
            for route_idx, route in enumerate(current_routes):
                if len(route) < 4:
                    continue

                for i in range(1, len(route) - 2):
                    for j in range(i + 1, len(route) - 1):
                        # Try reversing segment
                        new_route = route.copy()
                        new_route[i:j+1] = reversed(route[i:j+1])

                        # Check if improvement
                        old_dist = calculate_route_distance(route, self.distance_matrix)
                        new_dist = calculate_route_distance(new_route, self.distance_matrix)

                        if new_dist < old_dist:
                            current_routes[route_idx] = new_route
                            current_cost = current_cost - old_dist + new_dist
                            improved = True
                            break

                    if improved:
                        break

        return {
            'routes': current_routes,
            'total_distance': current_cost,
            'num_vehicles': len(current_routes)
        }

    def visualize(self, solution=None, save_path=None):
        """
        Visualize routes on a map
        """

        if solution is None:
            solution = self.best_solution

        if solution is None:
            raise ValueError("No solution to visualize")

        plt.figure(figsize=(12, 8))

        # Plot depot
        depot = self.coordinates[self.depot_idx]
        plt.plot(depot[0], depot[1], 'rs', markersize=15, label='Depot')

        # Plot routes with different colors
        colors = plt.cm.tab20(np.linspace(0, 1, len(solution['routes'])))

        for idx, route in enumerate(solution['routes']):
            route_coords = self.coordinates[route]
            plt.plot(route_coords[:, 0], route_coords[:, 1],
                    'o-', color=colors[idx], linewidth=2, markersize=8,
                    label=f'Route {idx+1}')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'VRP Solution - Total Distance: {solution["total_distance"]:.2f}')
        plt.legend()
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def get_route_statistics(self, solution=None):
        """
        Calculate detailed statistics for solution
        """

        if solution is None:
            solution = self.best_solution

        stats = {
            'num_vehicles': len(solution['routes']),
            'total_distance': solution['total_distance'],
            'routes': []
        }

        for idx, route in enumerate(solution['routes']):
            route_load = sum(self.demands[i] for i in route if i != self.depot_idx)
            route_distance = calculate_route_distance(route, self.distance_matrix)
            num_stops = len([i for i in route if i != self.depot_idx])

            stats['routes'].append({
                'route_id': idx + 1,
                'num_stops': num_stops,
                'total_load': route_load,
                'utilization': route_load / self.vehicle_capacity * 100,
                'distance': route_distance,
                'sequence': route
            })

        return stats

# Example usage
if __name__ == "__main__":
    # Sample problem: 20 customers
    np.random.seed(42)

    num_customers = 20
    coordinates = np.random.rand(num_customers + 1, 2) * 100
    coordinates[0] = [50, 50]  # Depot in center

    demands = np.random.randint(5, 20, num_customers + 1)
    demands[0] = 0  # Depot has no demand

    vehicle_capacity = 50

    # Solve
    solver = VRPSolver(coordinates, demands, vehicle_capacity)
    solution = solver.solve(method='clarke_wright', improve=True)

    # Get statistics
    stats = solver.get_route_statistics()

    print(f"Solution found:")
    print(f"Number of vehicles: {stats['num_vehicles']}")
    print(f"Total distance: {stats['total_distance']:.2f}")
    print("\nRoute details:")

    for route_stat in stats['routes']:
        print(f"  Route {route_stat['route_id']}: "
              f"{route_stat['num_stops']} stops, "
              f"Load: {route_stat['total_load']} "
              f"({route_stat['utilization']:.1f}% utilization), "
              f"Distance: {route_stat['distance']:.2f}")

    # Visualize
    solver.visualize()
```

---

## Commercial Routing Software

### Leading Platforms

**Omnitracs / Roadnet**
- Industry standard for route optimization
- Real-time tracking integration
- Dynamic rerouting

**Descartes Route Planner**
- Multi-depot routing
- Time window optimization
- Territory management

**WorkWave Route Manager**
- SMB-focused
- Mobile driver app
- GPS tracking

**OptimoRoute**
- Cloud-based routing
- Real-time order entry
- Driver mobile app

**Route4Me**
- Multi-stop route optimization
- Territory optimization
- Affordable pricing

**Verizon Connect (Networkfleet)**
- Telematics integration
- Fleet management features

**Teletrac Navman**
- Route optimization + telematics
- Compliance tracking

---

## Python Libraries & Tools

**OR-Tools (Google)**
```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrp_ortools(distance_matrix, num_vehicles, depot=0):
    """Solve VRP using Google OR-Tools"""

    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        num_vehicles,
        depot
    )

    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    # Create distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    # Extract routes
    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)

    return {
        'routes': routes,
        'total_distance': solution.ObjectiveValue()
    }
```

**Python VRP Libraries**
- `python-tsp`: TSP solvers
- `vrpy`: VRP with column generation
- `scipy.optimize`: General optimization
- `networkx`: Graph algorithms
- `geopy`: Distance calculations

---

## Common Challenges & Solutions

### Challenge: Time Windows Too Tight

**Problem:**
- No feasible solution exists
- Many late deliveries

**Solutions:**
- Negotiate wider time windows with customers
- Add more vehicles
- Split large time windows into preferred + acceptable
- Use soft time windows with penalties
- Start routes earlier
- Consider customer priorities (A/B/C)

### Challenge: Unbalanced Routes

**Problem:**
- Some vehicles overloaded, others underutilized
- Some routes very long, others very short

**Solutions:**
- Use post-optimization balancing
- Set min/max stops per route constraints
- Adjust depot territories
- Use max route duration constraints
- Balance by revenue or priority

### Challenge: Real-Time Changes

**Problem:**
- New orders arrive during day
- Customer cancellations
- Traffic delays

**Solutions:**
- Reserve capacity for dynamic orders (10-20%)
- Use dynamic re-optimization every hour
- Implement tiered service (same-day premium)
- Driver communication system
- Geofence-triggered rerouting

### Challenge: Driver Compliance

**Problem:**
- Drivers don't follow optimal routes
- Take unauthorized breaks
- Skip stops

**Solutions:**
- Mobile driver app with turn-by-turn
- Gamification (efficiency scores, bonuses)
- Exception reporting and coaching
- GPS tracking with geofences
- Involve drivers in planning (local knowledge)

### Challenge: Traffic Variability

**Problem:**
- Static routes don't account for traffic
- Consistent late deliveries

**Solutions:**
- Use time-dependent travel times
- Historical traffic data integration
- Real-time traffic APIs (Google, HERE)
- Add buffer time to time windows
- Dynamic rerouting during day

### Challenge: Mixed Fleet

**Problem:**
- Different vehicle types (trucks, vans, bikes)
- Different capacities and costs

**Solutions:**
- Model as heterogeneous fleet VRP
- Assign vehicle type per route
- Cost per mile by vehicle type
- Prioritize smaller/cheaper vehicles
- Consider vehicle-customer compatibility

---

## Output Format

### Route Optimization Report

**Executive Summary:**
- Total routes: 12
- Total distance: 845 miles (15% reduction vs. current)
- Total time: 96 hours
- Vehicle utilization: 87% average
- On-time delivery: 98% (vs. 89% current)

**Route Details:**

| Route | Driver | Stops | Distance | Duration | Load | Utilization | Start Time |
|-------|--------|-------|----------|----------|------|-------------|------------|
| R1 | Smith | 18 | 72 mi | 8.5 hrs | 1,850 lbs | 93% | 7:00 AM |
| R2 | Jones | 15 | 65 mi | 7.8 hrs | 1,720 lbs | 86% | 7:00 AM |
| R3 | Brown | 22 | 83 mi | 9.2 hrs | 1,980 lbs | 99% | 6:30 AM |

**Stop Sequence (Example Route R1):**

1. Depot - 7:00 AM
2. Customer A (123 Main St) - 7:25 AM (ETA: 7:20-7:40)
3. Customer B (456 Oak Ave) - 7:52 AM (ETA: 7:45-8:00)
4. Customer C (789 Elm St) - 8:18 AM (ETA: 8:00-8:30)
...
18. Customer R (321 Pine Rd) - 3:45 PM (ETA: 3:30-4:00)
19. Return to Depot - 4:15 PM

**Performance Metrics:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Total miles | 995 | 845 | -15% |
| Labor hours | 112 | 96 | -14% |
| Vehicles used | 14 | 12 | -14% |
| Avg stops/route | 15 | 18 | +20% |
| Fuel cost | $1,990 | $1,690 | -15% |
| Late deliveries | 11% | 2% | -82% |

**Recommendations:**
1. Implement route optimization software
2. Provide mobile apps to drivers
3. Establish dynamic re-optimization process
4. Monitor and adjust time windows
5. Consider adding 1 vehicle for peak days

---

## Questions to Ask

If you need more context:
1. How many stops per day? How many vehicles?
2. Are there delivery time windows? Hard or soft constraints?
3. What are the vehicle capacity limits?
4. Single depot or multiple depots?
5. Any special constraints (driver shifts, access restrictions)?
6. Do you need pickups, deliveries, or both?
7. Real-time changes needed or static planning?
8. What's the current routing process?

---

## Related Skills

- **vehicle-routing-problem**: Mathematical VRP models and variants
- **fleet-management**: Vehicle sizing, maintenance, and fleet operations
- **last-mile-delivery**: Urban delivery specific optimization
- **network-design**: Depot location and network structure
- **freight-optimization**: Long-haul transportation optimization
- **capacitated-vrp**: Capacity-focused VRP modeling
- **vrp-time-windows**: Time window constraint modeling
- **traveling-salesman-problem**: Single-vehicle routing
- **pickup-delivery-problem**: Pickup and delivery routing
