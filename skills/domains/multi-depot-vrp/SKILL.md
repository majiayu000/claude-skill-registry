---
name: multi-depot-vrp
description: When the user wants to solve Multi-Depot VRP (MDVRP), optimize routes from multiple warehouses/depots, or handle multi-facility distribution. Also use when the user mentions "MDVRP," "multiple depots," "multi-warehouse routing," "hub routing," "distributed depots," or "regional distribution centers." For single depot, see vehicle-routing-problem.
---

# Multi-Depot Vehicle Routing Problem (MDVRP)

You are an expert in the Multi-Depot Vehicle Routing Problem and multi-facility distribution optimization. Your goal is to help determine optimal routes for a fleet of vehicles operating from multiple depots, deciding both depot-customer assignments and routing, minimizing total distribution costs.

## Initial Assessment

Before solving MDVRP instances, understand:

1. **Depot Configuration**
   - How many depots/warehouses?
   - Are depots identical or different capacities?
   - Can customers be served from any depot?
   - Are there preferred depot-customer assignments?
   - Fixed costs per depot?

2. **Fleet Characteristics**
   - Are vehicles assigned to specific depots?
   - Can vehicles return to different depot?
   - Homogeneous or heterogeneous fleet per depot?
   - Total fleet size or per-depot limits?

3. **Customer Requirements**
   - How many customers to serve?
   - Customer demands and constraints
   - Any customer-depot restrictions?
   - Service time requirements?

4. **Problem Objectives**
   - Minimize total distance?
   - Minimize number of vehicles?
   - Balance workload across depots?
   - Minimize maximum route length?

5. **Problem Scale**
   - Small (< 50 customers, 2-3 depots): Exact methods possible
   - Medium (50-200 customers): Advanced heuristics
   - Large (200+ customers): Metaheuristics required

---

## Mathematical Formulation

### MDVRP Formulation

**Sets:**
- D = {1, ..., m}: Set of depots
- C = {1, ..., n}: Set of customers
- V = D ∪ C: All nodes
- K_d: Set of vehicles at depot d

**Parameters:**
- c_{ij}: Cost/distance from node i to j
- q_i: Demand at customer i
- Q_k: Capacity of vehicle k
- M_d: Maximum vehicles available at depot d

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j
- y_{dk} ∈ {0,1}: 1 if vehicle k is used from depot d

**Objective Function:**
```
Minimize: Σ_{d∈D} Σ_{k∈K_d} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk}
```

**Constraints:**
```
1. Each customer visited exactly once:
   Σ_{d∈D} Σ_{k∈K_d} Σ_{i∈V} x_{ijk} = 1,  ∀j ∈ C

2. Vehicle starts and ends at same depot:
   Σ_{j∈C} x_{djk} = y_{dk},  ∀d ∈ D, k ∈ K_d
   Σ_{i∈C} x_{idk} = y_{dk},  ∀d ∈ D, k ∈ K_d

3. Flow conservation:
   Σ_{i∈V} x_{ihk} = Σ_{j∈V} x_{hjk},  ∀h ∈ C, ∀d ∈ D, k ∈ K_d

4. Capacity constraint:
   Σ_{i∈C} Σ_{j∈V} q_i * x_{ijk} ≤ Q_k,  ∀d ∈ D, k ∈ K_d

5. Maximum vehicles per depot:
   Σ_{k∈K_d} y_{dk} ≤ M_d,  ∀d ∈ D

6. Subtour elimination constraints

7. Binary variables:
   x_{ijk}, y_{dk} ∈ {0,1}
```

---

## Exact and Heuristic Algorithms

### 1. Cluster-First, Route-Second Approach

```python
import numpy as np
from sklearn.cluster import KMeans
import random

def mdvrp_cluster_first(customer_coords, depot_coords, demands,
                       vehicle_capacity, vehicles_per_depot):
    """
    Cluster-first, route-second heuristic for MDVRP

    Phase 1: Assign customers to depots (clustering)
    Phase 2: Solve VRP for each depot

    Args:
        customer_coords: n x 2 array of customer coordinates
        depot_coords: m x 2 array of depot coordinates
        demands: customer demands
        vehicle_capacity: vehicle capacity
        vehicles_per_depot: vehicles available at each depot

    Returns:
        solution dictionary
    """
    n_customers = len(customer_coords)
    n_depots = len(depot_coords)

    # Phase 1: Cluster customers to depots using K-means
    all_coords = np.vstack([depot_coords, customer_coords])

    # Initialize K-means with depot locations
    kmeans = KMeans(n_clusters=n_depots, init=depot_coords, n_init=1)
    customer_clusters = kmeans.fit_predict(customer_coords)

    # Phase 2: Solve VRP for each depot
    depot_routes = []
    total_distance = 0

    for depot_id in range(n_depots):
        # Get customers assigned to this depot
        cluster_customers = [i for i in range(n_customers)
                           if customer_clusters[i] == depot_id]

        if not cluster_customers:
            continue

        # Build distance matrix for this depot and its customers
        depot_coord = depot_coords[depot_id]
        cluster_coords = [depot_coord] + [customer_coords[i]
                                         for i in cluster_customers]

        sub_n = len(cluster_coords)
        sub_dist_matrix = np.zeros((sub_n, sub_n))

        for i in range(sub_n):
            for j in range(sub_n):
                sub_dist_matrix[i][j] = np.linalg.norm(
                    cluster_coords[i] - cluster_coords[j])

        # Demands for this cluster
        cluster_demands = [0] + [demands[i] for i in cluster_customers]

        # Solve VRP for this depot using Clarke-Wright
        routes = clarke_wright_for_depot(
            sub_dist_matrix, cluster_demands,
            vehicle_capacity, vehicles_per_depot)

        # Convert local indices back to global customer indices
        for route in routes:
            global_route = []
            for node in route:
                if node == 0:
                    global_route.append(('depot', depot_id))
                else:
                    global_route.append(('customer', cluster_customers[node-1]))
            depot_routes.append(global_route)

            # Calculate route distance
            route_distance = sum(sub_dist_matrix[route[i]][route[i+1]]
                               for i in range(len(route)-1))
            total_distance += route_distance

    return {
        'routes': depot_routes,
        'customer_to_depot': customer_clusters,
        'total_distance': total_distance,
        'num_vehicles': len(depot_routes)
    }


def clarke_wright_for_depot(dist_matrix, demands, vehicle_capacity, max_vehicles):
    """Clarke-Wright savings for single depot"""
    n = len(dist_matrix)
    customers = list(range(1, n))
    depot = 0

    # Calculate savings
    savings = []
    for i in customers:
        for j in customers:
            if i < j:
                saving = (dist_matrix[depot][i] +
                         dist_matrix[depot][j] -
                         dist_matrix[i][j])
                savings.append((saving, i, j))

    savings.sort(reverse=True)

    # Initialize routes
    routes = [[depot, c, depot] for c in customers]
    route_loads = [demands[c] for c in customers]

    # Merge routes
    for saving_val, i, j in savings:
        if len(routes) <= max_vehicles:
            break

        route_i_idx = next((idx for idx, r in enumerate(routes) if i in r), None)
        route_j_idx = next((idx for idx, r in enumerate(routes) if j in r), None)

        if route_i_idx is None or route_j_idx is None:
            continue
        if route_i_idx == route_j_idx:
            continue

        route_i = routes[route_i_idx]
        route_j = routes[route_j_idx]

        i_at_end = (route_i[1] == i or route_i[-2] == i)
        j_at_end = (route_j[1] == j or route_j[-2] == j)

        if not (i_at_end and j_at_end):
            continue

        combined_load = route_loads[route_i_idx] + route_loads[route_j_idx]
        if combined_load > vehicle_capacity:
            continue

        # Merge
        route_i_interior = route_i[1:-1]
        route_j_interior = route_j[1:-1]

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

        routes[route_i_idx] = new_route
        route_loads[route_i_idx] = combined_load
        del routes[route_j_idx]
        del route_loads[route_j_idx]

    return routes
```

### 2. Multi-Depot OR-Tools Implementation

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_mdvrp_ortools(customer_coords, depot_coords, demands,
                       vehicle_capacity, vehicles_per_depot, time_limit=60):
    """
    Solve MDVRP using Google OR-Tools

    Args:
        customer_coords: customer coordinates
        depot_coords: depot coordinates
        demands: customer demands
        vehicle_capacity: vehicle capacity
        vehicles_per_depot: list of vehicles per depot
        time_limit: time limit in seconds

    Returns:
        solution dictionary
    """
    n_customers = len(customer_coords)
    n_depots = len(depot_coords)
    total_vehicles = sum(vehicles_per_depot)

    # Combine all coordinates (depots first, then customers)
    all_coords = np.vstack([depot_coords, customer_coords])
    n_locations = len(all_coords)

    # Build distance matrix
    dist_matrix = np.zeros((n_locations, n_locations))
    for i in range(n_locations):
        for j in range(n_locations):
            dist_matrix[i][j] = np.linalg.norm(all_coords[i] - all_coords[j])

    # Demands (depots have 0 demand)
    all_demands = [0] * n_depots + list(demands)

    # Create starts and ends for each vehicle
    # Each vehicle starts and ends at its assigned depot
    starts = []
    ends = []
    vehicle_to_depot = []

    for depot_id in range(n_depots):
        for _ in range(vehicles_per_depot[depot_id]):
            starts.append(depot_id)
            ends.append(depot_id)
            vehicle_to_depot.append(depot_id)

    # Create routing manager
    manager = pywrapcp.RoutingIndexManager(n_locations, total_vehicles,
                                          starts, ends)

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
        return int(all_demands[from_node])

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    # Add capacity dimension
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        [int(vehicle_capacity)] * total_vehicles,
        True,  # start cumul to zero
        'Capacity')

    # Prevent visiting depots as intermediate stops
    for depot_id in range(n_depots):
        depot_index = manager.NodeToIndex(depot_id)
        routing.solver().Add(routing.ActiveVar(depot_index) == 0)

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
        depot_assignments = {}
        total_distance = 0

        for vehicle_id in range(total_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id) / 100.0

            route.append(manager.IndexToNode(index))

            if len(route) > 2:  # Route has customers
                depot_id = vehicle_to_depot[vehicle_id]
                routes.append({
                    'vehicle_id': vehicle_id,
                    'depot_id': depot_id,
                    'route': route,
                    'distance': route_distance
                })
                total_distance += route_distance

                # Track customer-depot assignments
                for node in route[1:-1]:  # Skip start/end depot
                    if node >= n_depots:  # Is customer
                        customer_id = node - n_depots
                        depot_assignments[customer_id] = depot_id

        return {
            'status': 'Optimal',
            'routes': routes,
            'depot_assignments': depot_assignments,
            'total_distance': total_distance,
            'num_vehicles_used': len(routes)
        }
    else:
        return {
            'status': 'No solution found',
            'routes': None
        }


# Example usage with visualization
def visualize_mdvrp_solution(customer_coords, depot_coords, routes):
    """Visualize MDVRP solution"""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 8))

    n_depots = len(depot_coords)
    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    # Plot routes by depot
    for route_info in routes:
        depot_id = route_info['depot_id']
        route = route_info['route']
        vehicle_id = route_info['vehicle_id']

        # Get coordinates for this route
        route_coords = []
        for node in route:
            if node < n_depots:
                route_coords.append(depot_coords[node])
            else:
                customer_id = node - n_depots
                route_coords.append(customer_coords[customer_id])

        xs = [c[0] for c in route_coords]
        ys = [c[1] for c in route_coords]

        ax.plot(xs, ys, 'o-', color=colors[depot_id],
               linewidth=2, markersize=6,
               label=f'Depot {depot_id+1}, Vehicle {vehicle_id+1}',
               alpha=0.7)

    # Plot depots
    for i, depot in enumerate(depot_coords):
        ax.plot(depot[0], depot[1], 's', color=colors[i],
               markersize=20, label=f'Depot {i+1}',
               markeredgecolor='black', markeredgewidth=2, zorder=10)

    # Plot customers
    for customer in customer_coords:
        ax.plot(customer[0], customer[1], 'o', color='lightgray',
               markersize=8, markeredgecolor='black', markeredgewidth=1)

    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('Multi-Depot VRP Solution')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# Complete example
if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    # Generate problem
    n_depots = 3
    n_customers = 40

    depot_coords = np.random.rand(n_depots, 2) * 100
    customer_coords = np.random.rand(n_customers, 2) * 100

    demands = [random.randint(5, 20) for _ in range(n_customers)]
    vehicle_capacity = 100
    vehicles_per_depot = [3, 3, 2]  # 8 total vehicles

    print(f"Problem: {n_customers} customers, {n_depots} depots")
    print(f"Total demand: {sum(demands)}")
    print(f"Vehicles per depot: {vehicles_per_depot}")

    print("\nSolving MDVRP with OR-Tools...")
    result = solve_mdvrp_ortools(customer_coords, depot_coords, demands,
                                vehicle_capacity, vehicles_per_depot,
                                time_limit=60)

    print(f"\nStatus: {result['status']}")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"Vehicles Used: {result['num_vehicles_used']}")

    # Count customers per depot
    depot_counts = {}
    for customer_id, depot_id in result['depot_assignments'].items():
        depot_counts[depot_id] = depot_counts.get(depot_id, 0) + 1

    print("\nCustomers assigned to each depot:")
    for depot_id in range(n_depots):
        count = depot_counts.get(depot_id, 0)
        print(f"  Depot {depot_id+1}: {count} customers")

    print("\nRoute Details:")
    for route_info in result['routes']:
        depot_id = route_info['depot_id']
        route = route_info['route']
        distance = route_info['distance']
        n_cust = len(route) - 2

        print(f"  Depot {depot_id+1}, Vehicle {route_info['vehicle_id']+1}:")
        print(f"    Customers: {n_cust}, Distance: {distance:.2f}")

    # Visualize
    visualize_mdvrp_solution(customer_coords, depot_coords, result['routes'])
```

---

## Tools & Libraries

### Python Libraries
- **OR-Tools (Google)**: Best for MDVRP (recommended)
- **PuLP/Pyomo**: MIP modeling
- **scikit-learn**: K-means clustering for depot assignment

### Approaches
- **Cluster-first, route-second**: Fast, good for geographic clustering
- **Route-first, cluster-second**: Better integration but complex
- **Unified approach**: Solve simultaneously (OR-Tools)

---

## Common Challenges & Solutions

### Challenge: Unbalanced Depot Assignments

**Problem:**
- Some depots overloaded, others underutilized
- Geographic imbalance

**Solutions:**
- Add workload balancing constraints
- Use weighted clustering
- Post-optimization rebalancing

### Challenge: Inter-Depot Transfer Not Allowed

**Problem:**
- Vehicles must return to origin depot
- Cannot serve customer from different depot than started

**Solutions:**
- OR-Tools handles naturally with separate start/end indices
- Enforce in clustering phase

### Challenge: Depot Capacity Limits

**Problem:**
- Depots have throughput limits
- Maximum vehicles or customers per depot

**Solutions:**
- Add depot capacity constraints
- Use constrained clustering
- Multi-stage assignment

---

## Output Format

### MDVRP Solution Report

**Problem:**
- Customers: 60
- Depots: 3
- Total Vehicles: 10 (4, 3, 3 per depot)
- Vehicle Capacity: 100 units

**Solution:**

| Metric | Value |
|--------|-------|
| Total Distance | 1,845 km |
| Vehicles Used | 9 / 10 |
| Average Route Length | 205 km |

**Depot Assignments:**

| Depot | Customers | Vehicles | Total Distance | Avg Load |
|-------|-----------|----------|----------------|----------|
| 1 | 24 | 4 | 782 km | 96% |
| 2 | 20 | 3 | 623 km | 94% |
| 3 | 16 | 2 | 440 km | 92% |

---

## Questions to Ask

1. How many depots/warehouses?
2. Can customers be served from any depot?
3. Are vehicles depot-specific or flexible?
4. Should workload be balanced across depots?
5. Are there depot capacity limits?
6. Can vehicles return to different depot than started?

---

## Related Skills

- **vehicle-routing-problem**: For single-depot VRP
- **hub-location-problem**: For depot location optimization
- **facility-location-problem**: For depot placement
- **capacitated-vrp**: For capacity-focused routing
- **network-design**: For distribution network design
