---
name: pickup-delivery-problem
description: When the user wants to solve Pickup and Delivery Problems (PDP), Vehicle Routing with Pickup and Delivery (VRPPD), or handle paired pickup-delivery requests. Also use when the user mentions "PDP," "VRPPD," "pickup and delivery routing," "paired requests," "dial-a-ride," "courier routing," "moving services," or "taxi/rideshare routing." For general VRP, see vehicle-routing-problem.
---

# Pickup and Delivery Problem (PDP)

You are an expert in Pickup and Delivery Problems and paired request routing optimization. Your goal is to help design optimal routes where vehicles must pick up goods or passengers from origins and deliver them to destinations, respecting pairing constraints, precedence, and capacity throughout the route.

## Initial Assessment

Before solving PDP instances, understand:

1. **Problem Variant**
   - One-to-one (each pickup paired with delivery)?
   - Many-to-many (multiple pickups/deliveries)?
   - Dial-a-ride (passenger transportation)?
   - Same-day courier service?
   - Moving/relocation services?

2. **Pairing Constraints**
   - Hard pairing (pickup i MUST precede delivery i)?
   - Time window between pickup and delivery?
   - Maximum ride time (dial-a-ride)?
   - Can pickup/delivery be split across vehicles? (usually NO)

3. **Capacity Considerations**
   - Is capacity consumed from pickup to delivery?
   - LIFO (last-in-first-out) constraint?
   - Vehicle capacity during entire route?

4. **Temporal Constraints**
   - Time windows at pickup locations?
   - Time windows at delivery locations?
   - Maximum delivery lag after pickup?
   - Service times at each location?

5. **Problem Scale**
   - Small (< 20 requests): Exact methods possible
   - Medium (20-100 requests): Advanced heuristics
   - Large (100+ requests): Metaheuristics required

---

## Mathematical Formulation

### Pickup and Delivery VRP (PDVRP)

**Sets:**
- N = {0, 1, ..., 2n}: Nodes (0 = depot, 1..n = pickups, n+1..2n = deliveries)
- P = {1, ..., n}: Pickup nodes
- D = {n+1, ..., 2n}: Delivery nodes
- K = {1, ..., m}: Vehicles

**Parameters:**
- c_{ij}: Cost/distance from node i to j
- t_{ij}: Travel time from i to j
- s_i: Service time at node i
- q_i: Load change at node i (positive for pickup, negative for delivery)
- [e_i, l_i]: Time window at node i
- Q: Vehicle capacity

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j
- w_{ik} ≥ 0: Arrival time of vehicle k at node i
- u_{ik} ≥ 0: Load of vehicle k when leaving node i

**Objective Function:**
```
Minimize: Σ_{k∈K} Σ_{i∈N} Σ_{j∈N} c_{ij} * x_{ijk}
```

**Constraints:**
```
1. Each pickup visited exactly once:
   Σ_{k∈K} Σ_{j∈N, j≠i} x_{ijk} = 1,  ∀i ∈ P

2. Each delivery visited exactly once:
   Σ_{k∈K} Σ_{j∈N, j≠i} x_{ijk} = 1,  ∀i ∈ D

3. Pickup and delivery on same vehicle:
   Σ_{j∈N, j≠i} x_{ijk} = Σ_{j∈N, j≠(n+i)} x_{(n+i)jk},  ∀i ∈ P, ∀k ∈ K

4. Pickup before delivery (precedence):
   w_{ik} + s_i + t_{i,n+i} ≤ w_{n+i,k},  ∀i ∈ P, ∀k ∈ K

5. Flow conservation:
   Σ_{i∈N, i≠h} x_{ihk} = Σ_{j∈N, j≠h} x_{hjk},  ∀h ∈ N\{0}, ∀k ∈ K

6. Time consistency:
   w_{ik} + s_i + t_{ij} ≤ w_{jk} + M*(1 - x_{ijk}),  ∀i,j ∈ N, ∀k ∈ K

7. Time windows:
   e_i ≤ w_{ik} ≤ l_i,  ∀i ∈ N, ∀k ∈ K

8. Capacity tracking:
   u_{jk} ≥ u_{ik} + q_j - Q*(1 - x_{ijk}),  ∀i,j ∈ N, ∀k ∈ K
   0 ≤ u_{ik} ≤ Q,  ∀i ∈ N, ∀k ∈ K

9. Binary variables:
   x_{ijk} ∈ {0,1}
```

---

## Exact and Heuristic Algorithms

### 1. Insertion Heuristic for PDP

```python
import numpy as np
import random

def pdp_insertion_heuristic(dist_matrix, time_matrix, requests,
                           vehicle_capacity, num_vehicles,
                           depot=0, max_route_time=480):
    """
    Sequential insertion heuristic for PDP

    Args:
        dist_matrix: distance matrix
        time_matrix: travel time matrix
        requests: list of dicts with 'pickup_node', 'delivery_node',
                 'quantity', 'pickup_tw', 'delivery_tw'
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index
        max_route_time: maximum route duration

    Returns:
        solution dictionary
    """

    def check_feasibility(route, pickup_idx, delivery_idx,
                         pickup_pos, delivery_pos):
        """
        Check if inserting pickup and delivery is feasible

        Must check:
        - Capacity along entire route
        - Time windows
        - Precedence (pickup before delivery)
        """

        # Build temporary route
        temp_route = route.copy()
        # Insert in correct order (pickup first)
        if pickup_pos < delivery_pos:
            temp_route.insert(pickup_pos, pickup_idx)
            temp_route.insert(delivery_pos, delivery_idx)
        else:
            temp_route.insert(delivery_pos, delivery_idx)
            temp_route.insert(pickup_pos, pickup_idx)

        # Check capacity
        current_load = 0
        node_to_request = {}
        for req_idx, req in enumerate(requests):
            node_to_request[req['pickup_node']] = (req_idx, 'pickup')
            node_to_request[req['delivery_node']] = (req_idx, 'delivery')

        for node in temp_route[1:-1]:  # Skip depot
            if node in node_to_request:
                req_idx, action = node_to_request[node]
                if action == 'pickup':
                    current_load += requests[req_idx]['quantity']
                else:
                    current_load -= requests[req_idx]['quantity']

                if current_load > vehicle_capacity or current_load < 0:
                    return False

        # Check time windows and precedence
        current_time = 0
        service_times = {}  # Default service time

        for i in range(len(temp_route) - 1):
            current_node = temp_route[i]
            next_node = temp_route[i+1]

            # Travel to next node
            current_time += time_matrix[current_node][next_node]

            # Check time window
            if next_node in node_to_request:
                req_idx, action = node_to_request[next_node]
                req = requests[req_idx]

                if action == 'pickup':
                    tw = req['pickup_tw']
                else:
                    tw = req['delivery_tw']

                if current_time > tw[1]:
                    return False  # Too late

                # Wait if early
                current_time = max(current_time, tw[0])

                # Add service time
                current_time += service_times.get(next_node, 10)

        # Check total route time
        if current_time > max_route_time:
            return False

        return True

    def calculate_insertion_cost(route, pickup_idx, delivery_idx,
                                pickup_pos, delivery_pos):
        """Calculate cost increase of insertion"""

        pickup_node = requests[pickup_idx]['pickup_node']
        delivery_node = requests[delivery_idx]['delivery_node']

        # Cost of inserting pickup
        i = route[pickup_pos - 1]
        j = route[pickup_pos]
        pickup_cost = (dist_matrix[i][pickup_node] +
                      dist_matrix[pickup_node][j] -
                      dist_matrix[i][j])

        # Cost of inserting delivery (accounting for pickup already inserted)
        temp_route = route.copy()
        temp_route.insert(pickup_pos, pickup_node)

        i = temp_route[delivery_pos - 1]
        j = temp_route[delivery_pos]
        delivery_cost = (dist_matrix[i][delivery_node] +
                        dist_matrix[delivery_node][j] -
                        dist_matrix[i][j])

        return pickup_cost + delivery_cost

    # Initialize routes
    routes = [[depot, depot] for _ in range(num_vehicles)]
    unassigned_requests = list(range(len(requests)))

    # Sort requests by some criterion (e.g., earliest pickup time)
    unassigned_requests.sort(
        key=lambda r: requests[r]['pickup_tw'][0])

    # Insert requests one by one
    for req_idx in unassigned_requests[:]:
        best_route = None
        best_pickup_pos = None
        best_delivery_pos = None
        best_cost = float('inf')

        # Try inserting in each route
        for route_idx, route in enumerate(routes):
            # Try all valid insertion positions
            for pickup_pos in range(1, len(route)):
                for delivery_pos in range(pickup_pos + 1, len(route) + 1):
                    if check_feasibility(route, req_idx, req_idx,
                                       pickup_pos, delivery_pos):
                        cost = calculate_insertion_cost(
                            route, req_idx, req_idx,
                            pickup_pos, delivery_pos)

                        if cost < best_cost:
                            best_cost = cost
                            best_route = route_idx
                            best_pickup_pos = pickup_pos
                            best_delivery_pos = delivery_pos

        # Insert request in best position
        if best_route is not None:
            pickup_node = requests[req_idx]['pickup_node']
            delivery_node = requests[req_idx]['delivery_node']

            routes[best_route].insert(best_pickup_pos, pickup_node)
            routes[best_route].insert(best_delivery_pos, delivery_node)

            unassigned_requests.remove(req_idx)

    # Calculate total distance
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes if len(route) > 2
    )

    # Remove empty routes
    routes = [r for r in routes if len(r) > 2]

    return {
        'routes': routes,
        'total_distance': total_distance,
        'num_vehicles': len(routes),
        'unassigned': unassigned_requests
    }
```

### 2. PDP with OR-Tools

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_pdp_ortools(locations, requests, vehicle_capacity,
                     num_vehicles, depot=0, time_limit=60):
    """
    Solve PDP using Google OR-Tools

    Args:
        locations: list of (x, y) coordinates for all locations
        requests: list of dicts:
          - pickup: pickup location index
          - delivery: delivery location index
          - quantity: load quantity
          - pickup_tw: (early, late) time window
          - delivery_tw: (early, late) time window
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index
        time_limit: time limit in seconds

    Returns:
        solution dictionary
    """
    import math

    n_locations = len(locations)

    # Build distance and time matrices
    dist_matrix = np.zeros((n_locations, n_locations))
    time_matrix = np.zeros((n_locations, n_locations))

    for i in range(n_locations):
        for j in range(n_locations):
            dist = math.sqrt((locations[i][0] - locations[j][0])**2 +
                           (locations[i][1] - locations[j][1])**2)
            dist_matrix[i][j] = dist
            time_matrix[i][j] = dist / 40 * 60  # 40 km/h in minutes

    # Create routing manager
    manager = pywrapcp.RoutingIndexManager(n_locations, num_vehicles, depot)

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
        return int(time_matrix[from_node][to_node] + 10)  # +10 min service

    time_callback_index = routing.RegisterTransitCallback(time_callback)

    # Add time dimension
    routing.AddDimension(
        time_callback_index,
        30,  # allow waiting time
        3000,  # maximum time per vehicle
        False,
        'Time')

    time_dimension = routing.GetDimensionOrDie('Time')

    # Add capacity dimension with pickups and deliveries
    def demand_callback(from_index):
        """Returns the demand at the node"""
        from_node = manager.IndexToNode(from_index)
        # Check if this is a pickup or delivery
        for req in requests:
            if from_node == req['pickup']:
                return req['quantity']
            elif from_node == req['delivery']:
                return -req['quantity']
        return 0

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        [vehicle_capacity] * num_vehicles,
        True,  # start cumul to zero
        'Capacity')

    # Add pickup and delivery constraints
    for request in requests:
        pickup_index = manager.NodeToIndex(request['pickup'])
        delivery_index = manager.NodeToIndex(request['delivery'])

        # Pickup and delivery must be on same route
        routing.solver().Add(
            routing.VehicleVar(pickup_index) ==
            routing.VehicleVar(delivery_index))

        # Pickup must occur before delivery
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index) <=
            time_dimension.CumulVar(delivery_index))

        # Add time windows
        time_dimension.CumulVar(pickup_index).SetRange(
            int(request['pickup_tw'][0]),
            int(request['pickup_tw'][1]))

        time_dimension.CumulVar(delivery_index).SetRange(
            int(request['delivery_tw'][0]),
            int(request['delivery_tw'][1]))

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
            route_times = []

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                time_var = time_dimension.CumulVar(index)
                route.append(node)
                route_times.append(solution.Value(time_var))
                index = solution.Value(routing.NextVar(index))

            route.append(manager.IndexToNode(index))
            time_var = time_dimension.CumulVar(index)
            route_times.append(solution.Value(time_var))

            if len(route) > 2:
                routes.append({
                    'vehicle_id': vehicle_id,
                    'route': route,
                    'times': route_times
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


# Complete example
if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    # Generate PDP problem
    n_requests = 10
    depot_location = (50, 50)

    # Generate pickup and delivery locations
    pickup_locations = np.random.rand(n_requests, 2) * 100
    delivery_locations = np.random.rand(n_requests, 2) * 100

    # All locations (depot + pickups + deliveries)
    locations = [depot_location]
    locations.extend(pickup_locations.tolist())
    locations.extend(delivery_locations.tolist())

    # Create requests
    requests = []
    for i in range(n_requests):
        pickup_idx = i + 1
        delivery_idx = i + 1 + n_requests

        # Generate time windows
        pickup_early = random.randint(0, 200)
        pickup_late = pickup_early + random.randint(60, 120)
        delivery_early = pickup_late + 20
        delivery_late = delivery_early + random.randint(60, 120)

        requests.append({
            'pickup': pickup_idx,
            'delivery': delivery_idx,
            'quantity': random.randint(10, 30),
            'pickup_tw': (pickup_early, pickup_late),
            'delivery_tw': (delivery_early, delivery_late)
        })

    vehicle_capacity = 100
    num_vehicles = 4

    print(f"Problem: {n_requests} requests, {num_vehicles} vehicles")
    print(f"Capacity: {vehicle_capacity}")

    print("\nSolving PDP with OR-Tools...")
    result = solve_pdp_ortools(locations, requests, vehicle_capacity,
                              num_vehicles, time_limit=60)

    if result['status'] == 'Optimal':
        print(f"\nStatus: {result['status']}")
        print(f"Total Distance: {result['total_distance']:.2f}")
        print(f"Vehicles Used: {result['num_vehicles']}")

        print("\nRoutes:")
        for route_info in result['routes']:
            route = route_info['route']
            times = route_info['times']
            vehicle_id = route_info['vehicle_id']

            print(f"\n  Vehicle {vehicle_id + 1}:")
            print(f"    Route: {route}")

            # Identify pickups and deliveries
            for i, (node, time) in enumerate(zip(route, times)):
                if node == 0:
                    print(f"      Stop {i}: Depot at time {time:.0f}")
                elif node <= n_requests:
                    req_idx = node - 1
                    print(f"      Stop {i}: Pickup {req_idx} at time {time:.0f}")
                else:
                    req_idx = node - n_requests - 1
                    print(f"      Stop {i}: Delivery {req_idx} at time {time:.0f}")
    else:
        print(f"Status: {result['status']}")
```

---

## Tools & Libraries

- **OR-Tools (Google)**: Best for practical PDP (recommended)
- **PuLP/Pyomo**: MIP modeling
- **jsprit**: Java-based VRP solver with PDP support

---

## Common Challenges & Solutions

### Challenge: Tight Time Windows

**Problem:**
- Pickup and delivery time windows hard to satisfy
- Precedence + time windows creates difficulty

**Solutions:**
- Use time-oriented insertion criteria
- Allow some time window violations with penalties
- Increase fleet size

### Challenge: Long Ride Times (Dial-a-Ride)

**Problem:**
- Passengers have maximum ride time limits
- Hard to serve many requests efficiently

**Solutions:**
- Add ride time constraints in formulation
- Use insertion heuristics with ride time checks
- Consider direct vs. shared rides

### Challenge: LIFO Constraints

**Problem:**
- Last item picked up must be first delivered (truck loading)
- Restricts routing flexibility

**Solutions:**
- Track loading sequence explicitly
- Use specialized LIFO checking in feasibility
- May need to reject some request combinations

---

## Output Format

### PDP Solution Report

**Problem:**
- Requests: 25 pickup-delivery pairs
- Vehicles: 5 (capacity: 100 units)

**Solution:**

| Metric | Value |
|--------|-------|
| Total Distance | 892 km |
| Vehicles Used | 4 / 5 |
| Requests Served | 25 / 25 |
| On-time Pickups | 100% |
| On-time Deliveries | 100% |

**Route Details:**

**Vehicle 1:**
- Pickup 3 (8:15) → Pickup 7 (8:45) → Delivery 3 (9:20) → Delivery 7 (10:05) → Depot

---

## Questions to Ask

1. Is each pickup paired with exactly one delivery?
2. Must pickup occur before delivery on same vehicle?
3. Are there time windows at pickups/deliveries?
4. Is there max time between pickup and delivery?
5. Are there LIFO (stacking) constraints?
6. Is this dial-a-ride (passenger) or freight?

---

## Related Skills

- **vehicle-routing-problem**: For general VRP
- **vrp-time-windows**: For time window handling
- **traveling-salesman-problem**: For route sequencing
