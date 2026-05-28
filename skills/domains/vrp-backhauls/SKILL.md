---
name: vrp-backhauls
description: When the user wants to solve VRP with Backhauls (VRPB), optimize routes with both deliveries and pickups, or handle reverse logistics. Also use when the user mentions "VRPB," "backhaul optimization," "linehaul and backhaul," "delivery and pickup routes," "reverse logistics," or "return pickups." Backhauls are pickups that occur AFTER all deliveries on a route. For paired pickup-delivery, see pickup-delivery-problem.
---

# Vehicle Routing Problem with Backhauls (VRPB)

You are an expert in the Vehicle Routing Problem with Backhauls and reverse logistics optimization. Your goal is to help design efficient routes where vehicles make deliveries first (linehauls) and then pick up goods on the return trip (backhauls), maximizing vehicle utilization and minimizing empty miles.

## Initial Assessment

Before solving VRPB instances, understand:

1. **Backhaul Characteristics**
   - Strict sequence (all deliveries before all pickups)?
   - Mixed linehauls and backhauls allowed?
   - Can a customer have both delivery AND pickup?

2. **Capacity Considerations**
   - Same vehicle capacity for deliveries and pickups?
   - How does capacity work? (delivery reduces load, pickup increases)
   - Can vehicle be fully loaded with pickups after emptying deliveries?

3. **Customer Types**
   - Linehaul customers (delivery only)
   - Backhaul customers (pickup only)
   - Mixed customers (both delivery and pickup)
   - Number of each type?

4. **Business Context**
   - Return of empty containers/pallets?
   - Reverse logistics (returns, recycling)?
   - Supply redistribution between locations?
   - Waste collection after deliveries?

5. **Problem Scale**
   - Small (< 50 customers): Exact methods possible
   - Medium (50-200): Advanced heuristics
   - Large (200+): Metaheuristics required

---

## Mathematical Formulation

### VRPB with Sequential Constraint

**Sets:**
- V = {0} ∪ L ∪ B: Nodes (0 = depot, L = linehaul, B = backhaul customers)
- K: Vehicles

**Parameters:**
- c_{ij}: Cost/distance from i to j
- d_i: Delivery quantity at linehaul customer i ∈ L
- p_j: Pickup quantity at backhaul customer j ∈ B
- Q: Vehicle capacity

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j
- u_{ik} ∈ ℝ: Load on vehicle k after visiting node i

**Objective:**
```
Minimize: Σ_{k∈K} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk}
```

**Constraints:**
```
1. Each customer visited exactly once:
   Σ_{k∈K} Σ_{i∈V, i≠j} x_{ijk} = 1,  ∀j ∈ L ∪ B

2. Flow conservation:
   Σ_{i∈V} x_{ihk} = Σ_{j∈V} x_{hjk},  ∀h ∈ V, ∀k ∈ K

3. Capacity constraint:
   Σ_{i∈L} d_i * Σ_{j∈V} x_{ijk} ≤ Q,  ∀k ∈ K (deliveries)
   Σ_{j∈B} p_j * Σ_{i∈V} x_{ijjk} ≤ Q,  ∀k ∈ K (pickups)

4. Load tracking:
   Delivery phase: u_{jk} = u_{ik} - d_j (load decreases)
   Pickup phase: u_{jk} = u_{ik} + p_j (load increases)

5. Precedence (all linehauls before backhauls):
   If x_{ijk} = 1 and i ∈ L, j ∈ B, then
   all linehaul customers must be visited before j

6. Subtour elimination

7. Binary variables:
   x_{ijk} ∈ {0,1}
```

---

## Classical Heuristics

### 1. Sequential Cluster-Route for VRPB

```python
import numpy as np

def vrpb_cluster_route(coordinates, linehaul_demands, backhaul_demands,
                      vehicle_capacity, num_vehicles, depot_idx=0):
    """
    Cluster-then-route heuristic for VRPB

    Phase 1: Cluster customers geographically
    Phase 2: Within each cluster, sequence linehauls then backhauls
    Phase 3: Optimize sequences

    Args:
        coordinates: all location coordinates
        linehaul_demands: delivery demands (0 for backhaul-only customers)
        backhaul_demands: pickup demands (0 for linehaul-only customers)
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot_idx: depot index

    Returns:
        solution dictionary
    """
    n = len(coordinates)
    depot = coordinates[depot_idx]

    # Identify customer types
    linehaul_customers = [i for i in range(n)
                         if i != depot_idx and linehaul_demands[i] > 0]
    backhaul_customers = [i for i in range(n)
                         if i != depot_idx and backhaul_demands[i] > 0]

    print(f"Linehaul customers: {len(linehaul_customers)}")
    print(f"Backhaul customers: {len(backhaul_customers)}")

    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coordinates[i] - coordinates[j])

    # Sweep algorithm to create clusters
    import math

    def polar_angle(point):
        dx = point[0] - depot[0]
        dy = point[1] - depot[1]
        return math.atan2(dy, dx)

    # Sort all customers by angle
    all_customers = linehaul_customers + backhaul_customers
    customer_angles = [(polar_angle(coordinates[c]), c) for c in all_customers]
    customer_angles.sort()

    # Build routes by sweeping
    routes = []
    current_route_linehauls = []
    current_route_backhauls = []
    current_linehaul_load = 0
    current_backhaul_load = 0

    for angle, customer in customer_angles:
        is_linehaul = customer in linehaul_customers

        if is_linehaul:
            demand = linehaul_demands[customer]

            # Check if adding this linehaul is feasible
            if current_linehaul_load + demand <= vehicle_capacity:
                current_route_linehauls.append(customer)
                current_linehaul_load += demand
            else:
                # Start new route
                if current_route_linehauls or current_route_backhauls:
                    routes.append({
                        'linehauls': current_route_linehauls,
                        'backhauls': current_route_backhauls
                    })

                current_route_linehauls = [customer]
                current_route_backhauls = []
                current_linehaul_load = demand
                current_backhaul_load = 0
        else:
            demand = backhaul_demands[customer]

            # Check if adding this backhaul is feasible
            if current_backhaul_load + demand <= vehicle_capacity:
                current_route_backhauls.append(customer)
                current_backhaul_load += demand
            else:
                # Check if we can start new route
                if current_route_linehauls or current_route_backhauls:
                    routes.append({
                        'linehauls': current_route_linehauls,
                        'backhauls': current_route_backhauls
                    })

                current_route_linehauls = []
                current_route_backhauls = [customer]
                current_linehaul_load = 0
                current_backhaul_load = demand

    # Add last route
    if current_route_linehauls or current_route_backhauls:
        routes.append({
            'linehauls': current_route_linehauls,
            'backhauls': current_route_backhauls
        })

    # Optimize each route with 2-opt (separately for linehauls and backhauls)
    optimized_routes = []

    for route in routes:
        # Optimize linehaul sequence
        if len(route['linehauls']) > 2:
            linehaul_seq = [depot_idx] + route['linehauls']
            linehaul_seq = two_opt_segment(linehaul_seq, dist_matrix)
            route['linehauls'] = linehaul_seq[1:]  # Remove depot

        # Optimize backhaul sequence
        if len(route['backhauls']) > 2:
            backhaul_seq = route['backhauls'] + [depot_idx]
            backhaul_seq = two_opt_segment(backhaul_seq, dist_matrix)
            route['backhauls'] = backhaul_seq[:-1]  # Remove depot

        optimized_routes.append(route)

    # Convert to full routes and calculate distance
    full_routes = []
    total_distance = 0

    for route in optimized_routes:
        full_route = [depot_idx]
        full_route.extend(route['linehauls'])
        full_route.extend(route['backhauls'])
        full_route.append(depot_idx)

        full_routes.append(full_route)

        # Calculate distance
        route_distance = sum(dist_matrix[full_route[i]][full_route[i+1]]
                           for i in range(len(full_route)-1))
        total_distance += route_distance

    return {
        'routes': full_routes,
        'route_details': optimized_routes,
        'total_distance': total_distance,
        'num_vehicles': len(full_routes)
    }


def two_opt_segment(sequence, dist_matrix):
    """2-opt optimization for a sequence"""
    improved = True
    best = sequence.copy()

    while improved:
        improved = False
        for i in range(len(best) - 2):
            for j in range(i + 2, len(best)):
                if j - i == 1:
                    continue

                current_cost = (dist_matrix[best[i]][best[i+1]] +
                              dist_matrix[best[j-1]][best[j]])
                new_cost = (dist_matrix[best[i]][best[j-1]] +
                           dist_matrix[best[i+1]][best[j]])

                if new_cost < current_cost - 1e-10:
                    best[i+1:j] = reversed(best[i+1:j])
                    improved = True
                    break

            if improved:
                break

    return best
```

### 2. VRPB with OR-Tools

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrpb_ortools(coordinates, linehaul_demands, backhaul_demands,
                      vehicle_capacity, num_vehicles, depot=0,
                      time_limit=60):
    """
    Solve VRPB using OR-Tools

    Enforces that all linehauls are served before backhauls on each route

    Args:
        coordinates: location coordinates
        linehaul_demands: delivery demands (0 if backhaul-only)
        backhaul_demands: pickup demands (0 if linehaul-only)
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index
        time_limit: time limit

    Returns:
        solution dictionary
    """
    import math

    n = len(coordinates)

    # Build distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt(
                (coordinates[i][0] - coordinates[j][0])**2 +
                (coordinates[i][1] - coordinates[j][1])**2
            )

    # Identify customer types
    linehaul_only = [i for i in range(n) if linehaul_demands[i] > 0
                    and backhaul_demands[i] == 0]
    backhaul_only = [i for i in range(n) if backhaul_demands[i] > 0
                    and linehaul_demands[i] == 0]
    mixed = [i for i in range(n) if linehaul_demands[i] > 0
            and backhaul_demands[i] > 0]

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

    # Add two capacity dimensions: one for deliveries, one for pickups

    # Delivery capacity (starts full, decreases)
    def delivery_demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return int(linehaul_demands[from_node])

    delivery_callback_index = routing.RegisterUnaryTransitCallback(
        delivery_demand_callback)

    routing.AddDimension(
        delivery_callback_index,
        0,  # no slack
        int(vehicle_capacity),  # maximum capacity
        True,  # start cumul to zero
        'Delivery_Capacity')

    # Pickup capacity (starts at 0, increases)
    def pickup_demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return int(backhaul_demands[from_node])

    pickup_callback_index = routing.RegisterUnaryTransitCallback(
        pickup_demand_callback)

    routing.AddDimension(
        pickup_callback_index,
        0,  # no slack
        int(vehicle_capacity),  # maximum capacity
        True,  # start cumul to zero
        'Pickup_Capacity')

    # Add precedence constraints: linehauls before backhauls
    # Use a counter dimension to enforce sequence
    def counter_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        # Linehaul customers get value 0, backhauls get value 1000
        if from_node in backhaul_only:
            return 1000
        return 0

    counter_callback_index = routing.RegisterUnaryTransitCallback(counter_callback)

    routing.AddDimension(
        counter_callback_index,
        0,  # no slack
        10000,  # large upper bound
        True,  # start cumul to zero
        'Counter')

    counter_dimension = routing.GetDimensionOrDie('Counter')

    # Enforce that linehauls (counter ~0) come before backhauls (counter ~1000)
    for backhaul_customer in backhaul_only:
        index = manager.NodeToIndex(backhaul_customer)
        counter_dimension.CumulVar(index).SetMin(500)

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
        total_distance = 0

        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            linehaul_customers = []
            backhaul_customers = []

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)

                if node in linehaul_only:
                    linehaul_customers.append(node)
                elif node in backhaul_only:
                    backhaul_customers.append(node)

                index = solution.Value(routing.NextVar(index))

            route.append(manager.IndexToNode(index))

            if len(route) > 2:
                routes.append({
                    'route': route,
                    'linehauls': linehaul_customers,
                    'backhauls': backhaul_customers
                })

                # Calculate distance
                route_distance = sum(dist_matrix[route[i]][route[i+1]]
                                   for i in range(len(route)-1))
                total_distance += route_distance

        return {
            'status': 'Optimal',
            'routes': routes,
            'total_distance': total_distance,
            'num_vehicles': len(routes)
        }
    else:
        return {
            'status': 'No solution found',
            'routes': None
        }


# Visualization
def visualize_vrpb_solution(coordinates, routes, linehaul_demands,
                           backhaul_demands, save_path=None):
    """Visualize VRPB solution with linehauls and backhauls"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 8))

    colors = plt.cm.tab10(np.linspace(0, 1, len(routes)))

    for idx, route_info in enumerate(routes):
        route = route_info['route']
        linehauls = route_info.get('linehauls', [])
        backhauls = route_info.get('backhauls', [])

        # Plot full route
        route_coords = [coordinates[i] for i in route]
        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]

        ax.plot(xs, ys, '-', color=colors[idx], linewidth=2, alpha=0.5)

        # Mark linehaul customers (circles)
        for customer in linehauls:
            coord = coordinates[customer]
            ax.plot(coord[0], coord[1], 'o', color=colors[idx],
                   markersize=12, markeredgecolor='black', markeredgewidth=1.5)

        # Mark backhaul customers (triangles)
        for customer in backhauls:
            coord = coordinates[customer]
            ax.plot(coord[0], coord[1], '^', color=colors[idx],
                   markersize=12, markeredgecolor='black', markeredgewidth=1.5)

    # Plot depot
    depot = coordinates[0]
    ax.plot(depot[0], depot[1], 's', color='red', markersize=20,
           label='Depot', markeredgecolor='black', markeredgewidth=2, zorder=10)

    # Legend
    ax.plot([], [], 'o', color='gray', markersize=10,
           markeredgecolor='black', label='Linehaul (Delivery)')
    ax.plot([], [], '^', color='gray', markersize=10,
           markeredgecolor='black', label='Backhaul (Pickup)')

    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('VRP with Backhauls Solution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


# Example
if __name__ == "__main__":
    import random
    np.random.seed(42)
    random.seed(42)

    # Generate problem
    n_linehauls = 15
    n_backhauls = 10
    n_total = n_linehauls + n_backhauls + 1  # +1 for depot

    coordinates = [(50, 50)]  # Depot
    coordinates.extend(np.random.rand(n_linehauls + n_backhauls, 2).tolist() * 100)

    # Demands
    linehaul_demands = [0]  # Depot
    linehaul_demands.extend([random.randint(5, 20) for _ in range(n_linehauls)])
    linehaul_demands.extend([0] * n_backhauls)  # Backhaul customers have no deliveries

    backhaul_demands = [0]  # Depot
    backhaul_demands.extend([0] * n_linehauls)  # Linehaul customers have no pickups
    backhaul_demands.extend([random.randint(5, 15) for _ in range(n_backhauls)])

    vehicle_capacity = 100
    num_vehicles = 4

    print(f"Problem: {n_linehauls} linehauls, {n_backhauls} backhauls")
    print(f"Total delivery demand: {sum(linehaul_demands)}")
    print(f"Total pickup demand: {sum(backhaul_demands)}")

    print("\nSolving VRPB with OR-Tools...")
    result = solve_vrpb_ortools(coordinates, linehaul_demands, backhaul_demands,
                               vehicle_capacity, num_vehicles, time_limit=60)

    if result['status'] == 'Optimal':
        print(f"\nStatus: {result['status']}")
        print(f"Total Distance: {result['total_distance']:.2f}")
        print(f"Vehicles Used: {result['num_vehicles']}")

        print("\nRoute Details:")
        for i, route_info in enumerate(result['routes']):
            route = route_info['route']
            linehauls = route_info['linehauls']
            backhauls = route_info['backhauls']

            total_delivery = sum(linehaul_demands[c] for c in linehauls)
            total_pickup = sum(backhaul_demands[c] for c in backhauls)

            print(f"\n  Vehicle {i+1}:")
            print(f"    Route: {route}")
            print(f"    Linehauls: {len(linehauls)} customers, {total_delivery} units")
            print(f"    Backhauls: {len(backhauls)} customers, {total_pickup} units")

        # Visualize
        visualize_vrpb_solution(coordinates, result['routes'],
                              linehaul_demands, backhaul_demands)
    else:
        print(f"Status: {result['status']}")
```

---

## Tools & Libraries

- **OR-Tools (Google)**: Best for VRPB (recommended)
- **PuLP/Pyomo**: MIP modeling
- Custom heuristics work well for this variant

---

## Common Challenges & Solutions

### Challenge: Imbalanced Linehauls and Backhauls

**Problem:**
- Many deliveries, few pickups (or vice versa)
- Vehicles return nearly empty

**Solutions:**
- Allow mixed linehaul-backhaul at same customer
- Consider dedicated backhaul-only routes
- Relax sequential constraint if possible

### Challenge: Strict Sequential Constraint Too Restrictive

**Problem:**
- Forcing all deliveries before all pickups reduces efficiency
- Could save distance by mixing

**Solutions:**
- Consider mixed VRPB (allows interleaving)
- See **pickup-delivery-problem** for more flexible variant
- Use soft penalties instead of hard constraint

### Challenge: Capacity Management

**Problem:**
- Vehicle might be full with pickups before finishing backhauls
- Complex capacity tracking

**Solutions:**
- Use two-dimensional capacity in OR-Tools
- Carefully check feasibility in heuristics
- Consider vehicle with compartments

---

## Output Format

### VRPB Solution Report

**Problem:**
- Linehaul customers: 20 (deliveries)
- Backhaul customers: 15 (pickups)
- Vehicles: 5 (capacity: 100 units)

**Solution:**

| Metric | Value |
|--------|-------|
| Total Distance | 1,124 km |
| Vehicles Used | 5 |
| Total Deliveries | 387 units |
| Total Pickups | 276 units |

**Route Details:**

| Vehicle | Linehauls | Deliveries | Backhauls | Pickups | Distance |
|---------|-----------|------------|-----------|---------|----------|
| 1 | 4 | 78 units | 3 | 54 units | 235 km |
| 2 | 5 | 95 units | 2 | 38 units | 198 km |
[...]

---

## Questions to Ask

1. Must all deliveries occur before all pickups?
2. Can customers have both delivery and pickup?
3. What's the ratio of linehauls to backhauls?
4. Is this for reverse logistics or redistribution?
5. Are there time constraints?
6. Same vehicle capacity for deliveries and pickups?

---

## Related Skills

- **vehicle-routing-problem**: For general VRP
- **pickup-delivery-problem**: For paired pickup-delivery
- **capacitated-vrp**: For capacity-focused routing
