---
name: split-delivery-vrp
description: When the user wants to solve Split Delivery VRP (SDVRP), allow customers to be visited multiple times, or optimize routes where demand exceeds vehicle capacity. Also use when the user mentions "SDVRP," "split deliveries," "multiple visits," "partial deliveries," "demand splitting," or "fractional service." For standard VRP, see vehicle-routing-problem.
---

# Split Delivery Vehicle Routing Problem (SDVRP)

You are an expert in the Split Delivery Vehicle Routing Problem and flexible delivery optimization. Your goal is to help design routes where customers can be visited by multiple vehicles, allowing partial deliveries when customer demand exceeds vehicle capacity or when splitting improves overall routing efficiency.

## Initial Assessment

Before solving SDVRP instances, understand:

1. **Split Delivery Rules**
   - Must customer demand be split if it exceeds capacity?
   - Can demand be split even if it doesn't exceed capacity (for efficiency)?
   - Minimum delivery quantity per visit?
   - Maximum number of visits per customer?

2. **Business Context**
   - Why allow splits? (large orders, routing flexibility, time windows)
   - Cost of multiple visits vs. single visit?
   - Customer preference for single delivery?
   - Administrative/handling costs per delivery?

3. **Capacity and Demand**
   - How many customers have demand > vehicle capacity?
   - Distribution of demand sizes?
   - Vehicle capacity sufficient for most customers?

4. **Additional Costs**
   - Fixed cost per visit?
   - Setup/unloading time at each visit?
   - Customer penalty for multiple visits?

5. **Problem Scale**
   - Small (< 30 customers): Exact methods possible
   - Medium (30-100): Advanced heuristics
   - Large (100+): Metaheuristics

---

## Mathematical Formulation

### SDVRP Formulation

**Sets:**
- V = {0, 1, ..., n}: Nodes (0 = depot, 1..n = customers)
- K = {1, ..., m}: Vehicles

**Parameters:**
- c_{ij}: Cost/distance from i to j
- d_i: Total demand at customer i
- Q: Vehicle capacity
- f: Fixed cost per visit (optional)

**Decision Variables:**
- x_{ijk} ∈ {0,1}: 1 if vehicle k travels from i to j
- q_{ik} ≥ 0: Quantity delivered by vehicle k to customer i

**Objective Function:**
```
Minimize: Σ_{k∈K} Σ_{i∈V} Σ_{j∈V} c_{ij} * x_{ijk} +
          f * Σ_{i=1}^n Σ_{k∈K} [q_{ik} > 0]
```

**Constraints:**
```
1. Total demand satisfied:
   Σ_{k∈K} q_{ik} = d_i,  ∀i ∈ {1,...,n}

2. Flow conservation (if customer i is visited by vehicle k):
   If q_{ik} > 0, then
   Σ_{j∈V, j≠i} x_{ijk} = Σ_{j∈V, j≠i} x_{jik}

3. Vehicle capacity:
   Σ_{i=1}^n q_{ik} ≤ Q,  ∀k ∈ K

4. Delivery only if visited:
   q_{ik} ≤ Q * Σ_{j∈V, j≠i} x_{ijk},  ∀i ∈ {1,...,n}, ∀k ∈ K

5. Subtour elimination

6. Variables:
   x_{ijk} ∈ {0,1}
   q_{ik} ≥ 0
```

---

## Heuristics and Algorithms

### 1. Split Delivery Heuristic

```python
import numpy as np
import random

def sdvrp_greedy_split(dist_matrix, demands, vehicle_capacity,
                      num_vehicles, depot=0, split_penalty=0):
    """
    Greedy split delivery heuristic

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index
        split_penalty: additional cost for splitting a delivery

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    customers = set(range(1, n))
    remaining_demand = {i: demands[i] for i in customers}

    routes = []
    visit_counts = {i: 0 for i in customers}

    for vehicle_id in range(num_vehicles):
        if not any(remaining_demand[i] > 0 for i in customers):
            break

        route = [depot]
        current_location = depot
        current_load = 0

        while True:
            # Find best next customer to visit
            best_customer = None
            best_cost = float('inf')

            for customer in customers:
                if remaining_demand[customer] <= 0:
                    continue

                # Determine delivery quantity
                available_capacity = vehicle_capacity - current_load
                delivery_qty = min(remaining_demand[customer], available_capacity)

                if delivery_qty <= 0:
                    continue

                # Calculate cost (distance + split penalty if this creates a split)
                distance_cost = dist_matrix[current_location][customer]

                # Check if this would be a split delivery
                will_split = (delivery_qty < remaining_demand[customer])
                penalty = split_penalty if will_split else 0

                total_cost = distance_cost + penalty

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_customer = customer

            if best_customer is None:
                break

            # Visit best customer
            route.append(best_customer)

            # Determine delivery quantity
            available_capacity = vehicle_capacity - current_load
            delivery_qty = min(remaining_demand[best_customer], available_capacity)

            remaining_demand[best_customer] -= delivery_qty
            current_load += delivery_qty
            visit_counts[best_customer] += 1
            current_location = best_customer

        # Return to depot
        route.append(depot)

        if len(route) > 2:
            routes.append(route)

    # Calculate statistics
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes
    )

    split_customers = [i for i in customers if visit_counts[i] > 1]
    unserved_customers = [i for i in customers if remaining_demand[i] > 0]

    return {
        'routes': routes,
        'visit_counts': visit_counts,
        'total_distance': total_distance,
        'num_vehicles': len(routes),
        'split_customers': split_customers,
        'unserved_customers': unserved_customers
    }
```

### 2. SDVRP with Clarke-Wright Adaptation

```python
def sdvrp_clarke_wright(dist_matrix, demands, vehicle_capacity, depot=0):
    """
    Clarke-Wright Savings adapted for split deliveries

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        depot: depot index

    Returns:
        solution dictionary
    """
    n = len(dist_matrix)
    customers = list(range(1, n))

    # Track remaining demand for each customer
    remaining_demand = {i: demands[i] for i in customers}

    # Initially, each customer that needs service gets a route
    # If demand > capacity, customer needs multiple initial routes
    routes = []
    route_loads = []

    for customer in customers:
        demand = remaining_demand[customer]

        # Create as many routes as needed for this customer
        while demand > 0:
            delivery = min(demand, vehicle_capacity)
            routes.append([depot, customer, depot])
            route_loads.append(delivery)
            demand -= delivery

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

    # Merge routes based on savings
    for saving_value, i, j in savings:
        # Find routes ending with i and starting with j
        route_i_idx = None
        route_j_idx = None

        for idx, route in enumerate(routes):
            if len(route) > 2:
                if route[-2] == i:  # Route ends at i
                    route_i_idx = idx
                if route[1] == j:  # Route starts at j
                    route_j_idx = idx

        if route_i_idx is None or route_j_idx is None:
            continue

        if route_i_idx == route_j_idx:
            continue

        # Check if merge is feasible (capacity)
        combined_load = route_loads[route_i_idx] + route_loads[route_j_idx]
        if combined_load > vehicle_capacity:
            continue

        # Merge routes
        route_i = routes[route_i_idx]
        route_j = routes[route_j_idx]

        new_route = route_i[:-1] + route_j[1:]  # Remove duplicate depot

        routes[route_i_idx] = new_route
        route_loads[route_i_idx] = combined_load

        del routes[route_j_idx]
        del route_loads[route_j_idx]

    # Calculate total distance and statistics
    total_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes
    )

    # Count visits per customer
    visit_counts = {i: 0 for i in customers}
    for route in routes:
        for customer in route[1:-1]:
            visit_counts[customer] += 1

    split_customers = [i for i in customers if visit_counts[i] > 1]

    return {
        'routes': routes,
        'route_loads': route_loads,
        'visit_counts': visit_counts,
        'total_distance': total_distance,
        'num_vehicles': len(routes),
        'split_customers': split_customers
    }
```

### 3. SDVRP Analysis and Comparison

```python
def compare_sdvrp_vs_cvrp(dist_matrix, demands, vehicle_capacity,
                         num_vehicles, depot=0):
    """
    Compare SDVRP (with splits) vs. CVRP (no splits)

    Shows benefit of allowing split deliveries

    Args:
        dist_matrix: distance matrix
        demands: customer demands
        vehicle_capacity: vehicle capacity
        num_vehicles: number of vehicles
        depot: depot index

    Returns:
        comparison dictionary
    """
    print("=" * 60)
    print("SDVRP vs. CVRP Comparison")
    print("=" * 60)

    # Solve SDVRP
    print("\nSolving with Split Deliveries (SDVRP)...")
    sdvrp_result = sdvrp_greedy_split(
        dist_matrix, demands, vehicle_capacity, num_vehicles, depot)

    # Solve CVRP (no splits) - approximate by rejecting large demands
    print("\nSolving without Split Deliveries (CVRP approximation)...")

    # For CVRP, customers with demand > capacity cannot be served
    feasible_customers = [i for i in range(1, len(demands))
                         if demands[i] <= vehicle_capacity]
    infeasible_customers = [i for i in range(1, len(demands))
                           if demands[i] > vehicle_capacity]

    # Simple nearest neighbor for feasible customers
    from collections import defaultdict

    routes_cvrp = []
    remaining = set(feasible_customers)

    for _ in range(num_vehicles):
        if not remaining:
            break

        route = [depot]
        current_loc = depot
        current_load = 0

        while remaining:
            # Find nearest feasible customer
            best = None
            best_dist = float('inf')

            for customer in remaining:
                if current_load + demands[customer] <= vehicle_capacity:
                    dist = dist_matrix[current_loc][customer]
                    if dist < best_dist:
                        best_dist = dist
                        best = customer

            if best is None:
                break

            route.append(best)
            current_load += demands[best]
            current_loc = best
            remaining.remove(best)

        route.append(depot)

        if len(route) > 2:
            routes_cvrp.append(route)

    cvrp_distance = sum(
        sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        for route in routes_cvrp
    ) if routes_cvrp else float('inf')

    # Print comparison
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)

    print(f"\nSDVRP (with splits):")
    print(f"  Total Distance: {sdvrp_result['total_distance']:.2f}")
    print(f"  Vehicles Used: {sdvrp_result['num_vehicles']}")
    print(f"  Split Customers: {len(sdvrp_result['split_customers'])}")
    print(f"  Unserved Customers: {len(sdvrp_result['unserved_customers'])}")

    print(f"\nCVRP (no splits):")
    print(f"  Total Distance: {cvrp_distance:.2f}")
    print(f"  Vehicles Used: {len(routes_cvrp)}")
    print(f"  Unserved Customers: {len(remaining) + len(infeasible_customers)}")

    if cvrp_distance < float('inf'):
        improvement = (cvrp_distance - sdvrp_result['total_distance']) / cvrp_distance * 100
        print(f"\nImprovement with splits: {improvement:.1f}%")

    return {
        'sdvrp': sdvrp_result,
        'cvrp_distance': cvrp_distance,
        'cvrp_routes': routes_cvrp,
        'infeasible_customers': infeasible_customers
    }


# Example
if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    # Generate problem with some large demands
    n = 21  # 1 depot + 20 customers
    coordinates = np.random.rand(n, 2) * 100

    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(coordinates[i] - coordinates[j])

    # Create demands where some exceed vehicle capacity
    demands = [0]  # Depot
    vehicle_capacity = 50

    for _ in range(n-1):
        # 30% chance of large demand exceeding capacity
        if random.random() < 0.3:
            demand = random.randint(60, 100)  # Exceeds capacity
        else:
            demand = random.randint(10, 40)  # Normal demand

        demands.append(demand)

    num_vehicles = 8

    print(f"Problem: {n-1} customers, capacity: {vehicle_capacity}")
    print(f"Total demand: {sum(demands)}")
    print(f"Customers with demand > capacity: {sum(1 for d in demands if d > vehicle_capacity)}")

    # Run comparison
    comparison = compare_sdvrp_vs_cvrp(
        dist_matrix, demands, vehicle_capacity, num_vehicles)

    # Detailed results for SDVRP
    print("\n" + "=" * 60)
    print("SDVRP Route Details:")
    print("=" * 60)

    for i, route in enumerate(comparison['sdvrp']['routes']):
        print(f"\nVehicle {i+1}: {route}")

    print("\nCustomers requiring multiple visits:")
    for customer in comparison['sdvrp']['split_customers']:
        visits = comparison['sdvrp']['visit_counts'][customer]
        print(f"  Customer {customer}: {visits} visits (demand: {demands[customer]})")
```

---

## Tools & Libraries

- **Custom heuristics**: Often best approach for SDVRP
- **PuLP/Pyomo**: MIP modeling with split variables
- **OR-Tools**: Can be adapted but not native support

---

## Common Challenges & Solutions

### Challenge: When to Split?

**Problem:**
- Splitting everything increases visits/costs
- Not splitting leaves customers unserved

**Solutions:**
- Use split penalty cost
- Only split when necessary (demand > capacity)
- Consider customer preferences

### Challenge: Tracking Partial Deliveries

**Problem:**
- Complex to track which vehicle delivered what
- Route construction becomes more complicated

**Solutions:**
- Use delivery quantity variables (q_{ik})
- Track remaining demand explicitly
- Clear data structure for partial deliveries

### Challenge: Many Small Splits

**Problem:**
- Solution might create many small deliveries
- Inefficient for operations

**Solutions:**
- Add minimum delivery quantity
- Penalize number of splits
- Use maximum visits per customer constraint

---

## Output Format

### SDVRP Solution Report

**Problem:**
- Customers: 25
- Vehicle Capacity: 50 units
- Large orders (>50): 5 customers

**Solution:**

| Metric | Value |
|--------|-------|
| Total Distance | 987 km |
| Vehicles Used | 6 |
| Total Visits | 32 |
| Split Customers | 7 |
| Avg Visits/Customer | 1.28 |

**Split Delivery Details:**

| Customer | Total Demand | Visits | Delivery Pattern |
|----------|--------------|--------|------------------|
| C5 | 85 units | 2 | 50 + 35 units |
| C12 | 120 units | 3 | 50 + 50 + 20 |
| C18 | 65 units | 2 | 50 + 15 |

**Routes:**

**Vehicle 1:**
- Depot → C3 (45u) → C5 (50u) → C9 (5u) → Depot
- Total load: 100 units

**Vehicle 2:**
- Depot → C5 (35u) → C12 (50u) → C8 (15u) → Depot
- Total load: 100 units

[...]

---

## Questions to Ask

1. Can customer demand exceed vehicle capacity?
2. Is there a cost/penalty for splitting deliveries?
3. Should splits be minimized or allowed freely?
4. Are there minimum delivery quantities?
5. Maximum visits per customer?
6. Customer preference for single delivery?
7. Administrative cost per delivery?

---

## Related Skills

- **vehicle-routing-problem**: For standard VRP
- **capacitated-vrp**: For capacity-focused routing
- **pickup-delivery-problem**: For paired deliveries
