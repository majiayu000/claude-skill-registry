---
name: knapsack-problems
description: When the user wants to solve knapsack optimization problems, select items with constraints, or maximize value with limited capacity. Also use when the user mentions "0/1 knapsack," "bounded knapsack," "unbounded knapsack," "multiple knapsack," "multidimensional knapsack," "value-based packing," "capacity-constrained selection," or "resource allocation with limits." For bin packing, see 2d-bin-packing or 3d-bin-packing. For general optimization, see optimization-modeling.
---

# Knapsack Problems

You are an expert in knapsack optimization problems and resource allocation. Your goal is to help select optimal combinations of items subject to capacity constraints, maximizing value or profit while respecting weight, volume, or other resource limits.

## Initial Assessment

Before solving knapsack problems, understand:

1. **Problem Type**
   - 0/1 Knapsack? (each item taken once or not at all)
   - Bounded Knapsack? (limited quantity of each item)
   - Unbounded Knapsack? (unlimited quantity of each item)
   - Multiple Knapsack? (multiple containers/resources)
   - Multidimensional? (multiple constraints like weight AND volume)

2. **Items and Values**
   - How many item types? (10s, 100s, 1000s)
   - Item values (profit, utility, priority)?
   - Item costs (weight, volume, price)?
   - Any item dependencies or conflicts?

3. **Capacity Constraints**
   - Single constraint (weight only) or multiple (weight + volume)?
   - Capacity limits (weight capacity, volume capacity, budget)?
   - Multiple knapsacks with different capacities?

4. **Optimization Goal**
   - Maximize total value?
   - Minimize total cost while meeting requirements?
   - Multi-objective (value vs. weight)?

5. **Special Requirements**
   - Must-include items?
   - Item categories with quotas?
   - All-or-nothing item groups?

---

## Knapsack Problem Framework

### Problem Classification

**1. 0/1 Knapsack**
- Each item can be selected at most once
- Binary decision: include or exclude
- Most common variant
- Applications: Project selection, cargo loading with value

**2. Bounded Knapsack**
- Each item has limited quantity available
- Decision: how many of each item to take (0 to max_qty)
- Generalization of 0/1
- Applications: Portfolio selection, inventory selection

**3. Unbounded Knapsack**
- Unlimited quantity of each item type
- Can take as many as capacity allows
- Applications: Cutting stock, coin change, resource purchasing

**4. Multiple Knapsack**
- Multiple containers/bins available
- Assign items to knapsacks to maximize total value
- Applications: Multi-vehicle loading, multi-warehouse allocation

**5. Multidimensional Knapsack**
- Multiple capacity constraints (weight, volume, cost, etc.)
- More realistic but harder to solve
- Applications: Cargo loading, project selection with multiple resources

**6. Quadratic Knapsack**
- Item values depend on which other items are selected
- Captures synergies or conflicts
- Applications: Product bundling, portfolio optimization

---

## Mathematical Formulation

### Basic 0/1 Knapsack

**Decision Variables:**
- x_i ∈ {0, 1} for each item i
- x_i = 1 if item i is selected, 0 otherwise

**Objective:**
Maximize Σ (v_i × x_i)

Where v_i = value of item i

**Constraints:**
Σ (w_i × x_i) ≤ W

Where:
- w_i = weight of item i
- W = knapsack capacity

**Complexity:**
- NP-complete
- Pseudo-polynomial algorithms exist using dynamic programming

### Multidimensional Knapsack

**Objective:**
Maximize Σ (v_i × x_i)

**Constraints:**
Σ (w_ij × x_i) ≤ W_j  for all constraints j = 1, 2, ..., m

Where:
- w_ij = resource j consumed by item i
- W_j = capacity of resource j
- m = number of resource types

---

## Algorithms and Solution Methods

### Dynamic Programming for 0/1 Knapsack

```python
def knapsack_01_dynamic(values, weights, capacity):
    """
    Solve 0/1 Knapsack using Dynamic Programming

    Optimal solution with O(n*W) time complexity

    Parameters:
    - values: list of item values
    - weights: list of item weights
    - capacity: knapsack capacity

    Returns: maximum value and selected items
    """

    n = len(values)

    # Create DP table
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build DP table bottom-up
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Option 1: Don't take item i-1
            dp[i][w] = dp[i-1][w]

            # Option 2: Take item i-1 (if it fits)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                              dp[i-1][w - weights[i-1]] + values[i-1])

    # Backtrack to find selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)  # Item i-1 was selected
            w -= weights[i-1]

    selected.reverse()

    return {
        'max_value': dp[n][capacity],
        'selected_items': selected,
        'total_weight': sum(weights[i] for i in selected)
    }

# Example
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

result = knapsack_01_dynamic(values, weights, capacity)
print(f"Maximum value: {result['max_value']}")
print(f"Selected items: {result['selected_items']}")
print(f"Total weight: {result['total_weight']}")
```

**Space-Optimized Version**

```python
def knapsack_01_space_optimized(values, weights, capacity):
    """
    Space-optimized DP solution

    Uses O(W) space instead of O(n*W)
    """

    n = len(values)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # Traverse backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

### Branch and Bound for 0/1 Knapsack

```python
import heapq

def knapsack_branch_and_bound(values, weights, capacity):
    """
    Solve 0/1 Knapsack using Branch and Bound

    More efficient for problems where DP is too slow
    Good for large capacity values

    Parameters:
    - values: list of item values
    - weights: list of item weights
    - capacity: knapsack capacity

    Returns: optimal solution
    """

    n = len(values)

    # Sort items by value/weight ratio (descending)
    items = [(values[i]/weights[i], values[i], weights[i], i) for i in range(n)]
    items.sort(reverse=True)

    class Node:
        def __init__(self, level, value, weight, bound, items_taken):
            self.level = level
            self.value = value
            self.weight = weight
            self.bound = bound
            self.items_taken = items_taken

        def __lt__(self, other):
            return self.bound > other.bound  # Max heap (best bound first)

    def calculate_bound(node):
        """Calculate upper bound of maximum value for this node"""
        if node.weight >= capacity:
            return 0

        bound = node.value
        j = node.level + 1
        remaining_capacity = capacity - node.weight

        # Add items greedily (fractional allowed for bound)
        while j < n and remaining_capacity >= items[j][2]:
            bound += items[j][1]
            remaining_capacity -= items[j][2]
            j += 1

        # Add fraction of next item if any capacity remains
        if j < n and remaining_capacity > 0:
            bound += (remaining_capacity / items[j][2]) * items[j][1]

        return bound

    # Initialize
    best_value = 0
    best_items = []

    # Priority queue (max heap by bound)
    root = Node(-1, 0, 0, 0, [])
    root.bound = calculate_bound(root)
    pq = []
    heapq.heappush(pq, root)

    # Branch and bound search
    while pq:
        node = heapq.heappop(pq)

        if node.bound <= best_value:
            continue  # Prune this branch

        level = node.level + 1
        if level >= n:
            continue

        # Branch 1: Include item at level
        ratio, value, weight, orig_idx = items[level]
        if node.weight + weight <= capacity:
            new_items = node.items_taken + [orig_idx]
            new_value = node.value + value
            new_weight = node.weight + weight

            if new_value > best_value:
                best_value = new_value
                best_items = new_items

            child = Node(level, new_value, new_weight, 0, new_items)
            child.bound = calculate_bound(child)

            if child.bound > best_value:
                heapq.heappush(pq, child)

        # Branch 2: Exclude item at level
        child = Node(level, node.value, node.weight, 0, node.items_taken[:])
        child.bound = calculate_bound(child)

        if child.bound > best_value:
            heapq.heappush(pq, child)

    return {
        'max_value': best_value,
        'selected_items': sorted(best_items),
        'total_weight': sum(weights[i] for i in best_items)
    }
```

### Greedy Approximation

```python
def knapsack_greedy_approximation(values, weights, capacity):
    """
    Greedy approximation for 0/1 Knapsack

    Fast but not optimal
    Good for quick solutions or large problems

    Strategy: Sort by value/weight ratio, take best items first
    """

    n = len(values)

    # Calculate value/weight ratios
    items = [(values[i]/weights[i], values[i], weights[i], i) for i in range(n)]
    items.sort(reverse=True)

    total_value = 0
    total_weight = 0
    selected = []

    for ratio, value, weight, idx in items:
        if total_weight + weight <= capacity:
            selected.append(idx)
            total_value += value
            total_weight += weight

    return {
        'total_value': total_value,
        'selected_items': sorted(selected),
        'total_weight': total_weight
    }
```

### Bounded Knapsack

```python
def bounded_knapsack(values, weights, quantities, capacity):
    """
    Solve Bounded Knapsack Problem

    Each item type has limited quantity available

    Parameters:
    - values: list of item values
    - weights: list of item weights
    - quantities: list of maximum quantities for each item
    - capacity: knapsack capacity

    Returns: optimal solution with quantities
    """

    n = len(values)

    # Expand to 0/1 knapsack by duplicating items
    expanded_values = []
    expanded_weights = []
    item_map = []

    for i in range(n):
        for j in range(quantities[i]):
            expanded_values.append(values[i])
            expanded_weights.append(weights[i])
            item_map.append(i)

    # Solve as 0/1 knapsack
    result = knapsack_01_dynamic(expanded_values, expanded_weights, capacity)

    # Convert back to quantities
    item_quantities = [0] * n
    for selected_idx in result['selected_items']:
        original_item = item_map[selected_idx]
        item_quantities[original_item] += 1

    return {
        'max_value': result['max_value'],
        'item_quantities': item_quantities,
        'total_weight': result['total_weight']
    }

# Example
values = [10, 40, 30, 50]
weights = [5, 4, 6, 3]
quantities = [3, 2, 1, 4]  # Max quantity of each item
capacity = 20

result = bounded_knapsack(values, weights, quantities, capacity)
print(f"Maximum value: {result['max_value']}")
print(f"Item quantities: {result['item_quantities']}")
```

### Unbounded Knapsack

```python
def unbounded_knapsack(values, weights, capacity):
    """
    Solve Unbounded Knapsack Problem

    Unlimited quantity of each item type

    Applications: Cutting stock, coin change, resource purchasing

    Parameters:
    - values: list of item values
    - weights: list of item weights
    - capacity: knapsack capacity

    Returns: maximum value and quantities of each item
    """

    n = len(values)

    # DP array: dp[w] = max value with capacity w
    dp = [0] * (capacity + 1)

    # For backtracking
    used_item = [-1] * (capacity + 1)

    for w in range(1, capacity + 1):
        for i in range(n):
            if weights[i] <= w:
                new_value = dp[w - weights[i]] + values[i]
                if new_value > dp[w]:
                    dp[w] = new_value
                    used_item[w] = i

    # Backtrack to find quantities
    quantities = [0] * n
    w = capacity

    while w > 0 and used_item[w] != -1:
        i = used_item[w]
        quantities[i] += 1
        w -= weights[i]

    return {
        'max_value': dp[capacity],
        'item_quantities': quantities,
        'total_weight': capacity - w
    }

# Example: Cutting steel rods
# Rod lengths and their values
values = [1, 5, 8, 9, 10, 17, 17, 20]  # Value of each length
weights = [1, 2, 3, 4, 5, 6, 7, 8]     # Length of each cut
capacity = 20  # Total rod length

result = unbounded_knapsack(values, weights, capacity)
print(f"Maximum value: {result['max_value']}")
print(f"Cuts to make: {result['item_quantities']}")
```

### Multidimensional Knapsack

```python
def multidimensional_knapsack(values, constraints, capacities):
    """
    Solve Multidimensional Knapsack Problem

    Multiple resource constraints (e.g., weight AND volume)

    Parameters:
    - values: list of item values
    - constraints: 2D list where constraints[i][j] = resource j used by item i
    - capacities: list of capacity limits for each resource

    Returns: approximate solution using greedy + local search

    Note: Exact solution is NP-hard and computationally expensive
    """

    n = len(values)
    m = len(capacities)  # Number of constraints

    # Greedy initialization
    def calculate_efficiency(item_idx):
        """Calculate efficiency ratio for item"""
        # Use minimum slack across all resources
        min_slack = float('inf')
        for j in range(m):
            if constraints[item_idx][j] > 0:
                slack = capacities[j] / constraints[item_idx][j]
                min_slack = min(min_slack, slack)
        return values[item_idx] / min_slack if min_slack > 0 else 0

    # Sort by efficiency
    items = [(calculate_efficiency(i), i) for i in range(n)]
    items.sort(reverse=True)

    # Greedy selection
    selected = [False] * n
    used = [0] * m

    for efficiency, idx in items:
        # Check if item fits all constraints
        fits = True
        for j in range(m):
            if used[j] + constraints[idx][j] > capacities[j]:
                fits = False
                break

        if fits:
            selected[idx] = True
            for j in range(m):
                used[j] += constraints[idx][j]

    # Calculate solution value
    total_value = sum(values[i] for i in range(n) if selected[i])

    return {
        'total_value': total_value,
        'selected_items': [i for i in range(n) if selected[i]],
        'resource_usage': used
    }

# Example: Cargo loading with weight AND volume constraints
values = [10, 40, 30, 50, 35, 25]  # Item values
constraints = [
    # [weight, volume] for each item
    [5, 10],   # Item 0
    [4, 15],   # Item 1
    [6, 12],   # Item 2
    [3, 8],    # Item 3
    [5, 14],   # Item 4
    [4, 10]    # Item 5
]
capacities = [20, 50]  # [max weight, max volume]

result = multidimensional_knapsack(values, constraints, capacities)
print(f"Maximum value: {result['total_value']}")
print(f"Selected items: {result['selected_items']}")
print(f"Resource usage: Weight={result['resource_usage'][0]}, Volume={result['resource_usage'][1]}")
```

### Multiple Knapsack Problem

```python
def multiple_knapsack(values, weights, knapsack_capacities):
    """
    Solve Multiple Knapsack Problem

    Assign items to multiple knapsacks to maximize total value

    Parameters:
    - values: list of item values
    - weights: list of item weights
    - knapsack_capacities: list of capacities for each knapsack

    Returns: assignment of items to knapsacks
    """

    from pulp import *

    n = len(values)
    m = len(knapsack_capacities)

    # Create problem
    prob = LpProblem("Multiple_Knapsack", LpMaximize)

    # Decision variables: x[i,j] = 1 if item i assigned to knapsack j
    x = LpVariable.dicts("assign",
                        [(i, j) for i in range(n) for j in range(m)],
                        cat='Binary')

    # Objective: maximize total value
    prob += lpSum([values[i] * x[i,j]
                   for i in range(n) for j in range(m)]), "Total_Value"

    # Constraint 1: Each item assigned to at most one knapsack
    for i in range(n):
        prob += lpSum([x[i,j] for j in range(m)]) <= 1, f"Item_{i}"

    # Constraint 2: Knapsack capacity constraints
    for j in range(m):
        prob += (lpSum([weights[i] * x[i,j] for i in range(n)]) <=
                knapsack_capacities[j]), f"Capacity_{j}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = [[] for _ in range(m)]
    total_value = 0

    for i in range(n):
        for j in range(m):
            if x[i,j].varValue and x[i,j].varValue > 0.5:
                assignments[j].append(i)
                total_value += values[i]

    return {
        'total_value': total_value,
        'assignments': assignments,
        'status': LpStatus[prob.status]
    }

# Example: Assign items to 3 trucks
values = [15, 10, 8, 20, 12, 18, 9, 14]
weights = [5, 3, 2, 6, 4, 5, 2, 4]
truck_capacities = [10, 12, 8]  # 3 trucks

result = multiple_knapsack(values, weights, truck_capacities)
print(f"Total value: {result['total_value']}")
for i, assignment in enumerate(result['assignments']):
    print(f"Truck {i+1}: Items {assignment}")
```

---

## Complete Knapsack Solver

```python
class KnapsackSolver:
    """
    Comprehensive Knapsack Problem Solver

    Supports multiple knapsack variants
    """

    def __init__(self):
        self.items = []
        self.capacity = None
        self.solution = None

    def add_item(self, value, weight, item_id=None, max_quantity=1, volume=None):
        """
        Add item to knapsack problem

        Parameters:
        - value: item value/profit
        - weight: item weight/cost
        - item_id: item identifier
        - max_quantity: maximum quantity (for bounded knapsack)
        - volume: item volume (for multidimensional)
        """

        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'value': value,
            'weight': weight,
            'max_quantity': max_quantity,
            'volume': volume,
            'ratio': value / weight if weight > 0 else float('inf')
        })

    def solve_01_knapsack(self, capacity, algorithm='dp'):
        """
        Solve 0/1 Knapsack

        Parameters:
        - capacity: knapsack capacity
        - algorithm: 'dp' (dynamic programming) or 'bb' (branch-and-bound)

        Returns: optimal solution
        """

        self.capacity = capacity

        values = [item['value'] for item in self.items]
        weights = [item['weight'] for item in self.items]

        if algorithm == 'dp':
            result = knapsack_01_dynamic(values, weights, capacity)
        elif algorithm == 'bb':
            result = knapsack_branch_and_bound(values, weights, capacity)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        # Enhance result with item details
        self.solution = {
            'type': '0/1 Knapsack',
            'max_value': result['max_value'],
            'total_weight': result['total_weight'],
            'capacity': capacity,
            'utilization': (result['total_weight'] / capacity * 100) if capacity > 0 else 0,
            'items': [self.items[i] for i in result['selected_items']],
            'selected_indices': result['selected_items']
        }

        return self.solution

    def solve_bounded_knapsack(self, capacity):
        """Solve Bounded Knapsack"""

        values = [item['value'] for item in self.items]
        weights = [item['weight'] for item in self.items]
        quantities = [item['max_quantity'] for item in self.items]

        result = bounded_knapsack(values, weights, quantities, capacity)

        self.solution = {
            'type': 'Bounded Knapsack',
            'max_value': result['max_value'],
            'total_weight': result['total_weight'],
            'capacity': capacity,
            'utilization': (result['total_weight'] / capacity * 100) if capacity > 0 else 0,
            'item_quantities': result['item_quantities']
        }

        return self.solution

    def solve_unbounded_knapsack(self, capacity):
        """Solve Unbounded Knapsack"""

        values = [item['value'] for item in self.items]
        weights = [item['weight'] for item in self.items]

        result = unbounded_knapsack(values, weights, capacity)

        self.solution = {
            'type': 'Unbounded Knapsack',
            'max_value': result['max_value'],
            'total_weight': result['total_weight'],
            'capacity': capacity,
            'utilization': (result['total_weight'] / capacity * 100) if capacity > 0 else 0,
            'item_quantities': result['item_quantities']
        }

        return self.solution

    def print_solution(self):
        """Print solution summary"""

        if not self.solution:
            print("No solution available")
            return

        print("=" * 70)
        print(f"KNAPSACK SOLUTION: {self.solution['type']}")
        print("=" * 70)
        print(f"Maximum Value: {self.solution['max_value']}")
        print(f"Total Weight: {self.solution['total_weight']}")
        print(f"Capacity: {self.solution['capacity']}")
        print(f"Utilization: {self.solution['utilization']:.1f}%")
        print()

        if 'items' in self.solution:
            print("Selected Items:")
            for item in self.solution['items']:
                print(f"  {item['id']}: Value={item['value']}, Weight={item['weight']}")

        elif 'item_quantities' in self.solution:
            print("Item Quantities:")
            for i, qty in enumerate(self.solution['item_quantities']):
                if qty > 0:
                    item = self.items[i]
                    print(f"  {item['id']}: Quantity={qty}, "
                          f"Total Value={item['value']*qty}, "
                          f"Total Weight={item['weight']*qty}")


# Example usage
if __name__ == "__main__":
    print("Example 1: 0/1 Knapsack")
    print("-" * 50)

    solver = KnapsackSolver()

    # Add items (value, weight)
    solver.add_item(60, 10, "Item_A")
    solver.add_item(100, 20, "Item_B")
    solver.add_item(120, 30, "Item_C")
    solver.add_item(80, 15, "Item_D")
    solver.add_item(90, 18, "Item_E")

    # Solve 0/1 knapsack
    solution = solver.solve_01_knapsack(capacity=50, algorithm='dp')
    solver.print_solution()

    print("\n" + "=" * 70 + "\n")

    print("Example 2: Bounded Knapsack")
    print("-" * 50)

    solver2 = KnapsackSolver()

    # Add items with quantities
    solver2.add_item(10, 5, "Small_Box", max_quantity=3)
    solver2.add_item(40, 4, "Medium_Box", max_quantity=2)
    solver2.add_item(30, 6, "Large_Box", max_quantity=1)
    solver2.add_item(50, 3, "Premium_Box", max_quantity=4)

    solution2 = solver2.solve_bounded_knapsack(capacity=20)
    solver2.print_solution()
```

---

## Supply Chain Applications

### Project Selection

```python
def project_portfolio_selection(projects, budget, max_projects=None):
    """
    Select optimal project portfolio given budget constraint

    Knapsack where:
    - Items = projects
    - Value = NPV or expected return
    - Weight = project cost
    """

    solver = KnapsackSolver()

    for project in projects:
        solver.add_item(
            value=project['npv'],
            weight=project['cost'],
            item_id=project['name']
        )

    solution = solver.solve_01_knapsack(capacity=budget, algorithm='dp')

    return solution
```

### Cargo Loading Value Optimization

```python
def optimize_cargo_value(cargo_items, weight_limit, volume_limit):
    """
    Maximize cargo value given weight and volume constraints

    Multidimensional knapsack with 2 constraints
    """

    values = [item['value'] for item in cargo_items]
    constraints = [[item['weight'], item['volume']] for item in cargo_items]
    capacities = [weight_limit, volume_limit]

    solution = multidimensional_knapsack(values, constraints, capacities)

    return solution
```

---

## Common Challenges & Solutions

### Challenge: Large Problem Size

**Problem:**
- Thousands of items
- DP table too large
- Computational time excessive

**Solutions:**
- Use branch-and-bound instead of DP
- Apply greedy approximation for fast solution
- Use FPTAS (Fully Polynomial Time Approximation Scheme)
- Solve iteratively with reduced item set
- Parallel computing for independent subproblems

### Challenge: Multiple Constraints

**Problem:**
- Weight AND volume constraints
- Budget AND space limits
- Complex feasibility checks

**Solutions:**
- Use multidimensional knapsack formulation
- Apply greedy heuristics with efficiency ratios
- Integer programming solvers (Gurobi, CPLEX)
- Constraint programming
- Metaheuristics (genetic algorithms, simulated annealing)

---

## Output Format

### Knapsack Solution Report

**Problem:**
- Type: 0/1 Knapsack
- Items: 20
- Capacity: 100 lbs
- Optimization: Maximize value

**Solution:**
- Maximum Value: $2,450
- Total Weight: 98 lbs (98% utilization)
- Items Selected: 12

**Selected Items:**

| Item ID | Value | Weight | Value/Weight Ratio |
|---------|-------|--------|-------------------|
| A001 | $300 | 10 lbs | 30.0 |
| A005 | $500 | 15 lbs | 33.3 |
| B003 | $400 | 18 lbs | 22.2 |
| ... | ... | ... | ... |

**Not Selected:**
- Items C002, C005, D001 (insufficient capacity)
- Opportunity value left: $850

---

## Questions to Ask

1. What type of knapsack problem? (0/1, bounded, unbounded, multiple)
2. What is being optimized? (value, profit, utility)
3. What are the constraints? (weight, volume, budget)
4. How many items? What are their values and costs?
5. Any must-include items or special requirements?
6. Is this a one-time decision or recurring problem?
7. How fast does solution need to be computed?

---

## Related Skills

- **optimization-modeling**: For general optimization problems
- **2d-bin-packing**: For spatial packing without value optimization
- **3d-bin-packing**: For 3D packing problems
- **pallet-loading**: For loading optimization
- **multi-objective-optimization**: For multiple optimization criteria
