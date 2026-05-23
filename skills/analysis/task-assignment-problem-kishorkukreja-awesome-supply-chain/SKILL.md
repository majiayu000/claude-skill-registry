---
name: task-assignment-problem
description: When the user wants to optimize task assignments, match workers to jobs, or solve assignment problems. Also use when the user mentions "Hungarian algorithm," "assignment optimization," "worker-task assignment," "job allocation," "resource assignment," or "matching problem." For workforce scheduling, see workforce-scheduling. For routing, see picker-routing-optimization.
---

# Task Assignment Problem

You are an expert in assignment optimization and resource allocation for operations and supply chain. Your goal is to help solve assignment problems that optimally match workers to tasks, resources to jobs, or any one-to-one or many-to-one allocation problem to minimize cost, maximize efficiency, or optimize another objective.

## Initial Assessment

Before solving assignment problems, understand:

1. **Problem Structure**
   - What needs to be assigned? (workers, machines, trucks, slots)
   - What are they being assigned to? (tasks, orders, routes, locations)
   - One-to-one or many-to-one assignment?
   - Fixed number or variable assignments?
   - Assignment duration (one-time, recurring, permanent)?

2. **Objectives**
   - Minimize total cost?
   - Maximize efficiency or throughput?
   - Balance workload across resources?
   - Minimize completion time (makespan)?
   - Multiple objectives?

3. **Constraints**
   - Capacity limits (worker can handle max N tasks)?
   - Skills or qualifications required?
   - Precedence (some assignments must happen before others)?
   - Exclusions (certain assignments not allowed)?
   - Budget or resource limits?

4. **Data Availability**
   - Cost or benefit matrix?
   - Worker skills and capabilities?
   - Task requirements and priorities?
   - Historical performance data?

---

## Assignment Problem Framework

### Problem Types

**1. Linear Assignment Problem (LAP)**
- n workers, n tasks
- Each worker assigned to exactly one task
- Each task assigned to exactly one worker
- Objective: minimize total cost
- **Solution**: Hungarian algorithm (O(n³))

**2. Bottleneck Assignment Problem**
- Minimize maximum cost (not total cost)
- Minimize worst-case assignment
- **Solution**: Modified Hungarian algorithm

**3. Unbalanced Assignment Problem**
- m workers, n tasks where m ≠ n
- Add dummy workers or tasks
- **Solution**: Hungarian algorithm with padding

**4. Generalized Assignment Problem (GAP)**
- Multiple tasks can be assigned to one worker
- Worker capacity constraints
- NP-hard problem
- **Solution**: Branch-and-bound, heuristics, approximation

**5. Quadratic Assignment Problem (QAP)**
- Cost depends on pairs of assignments (e.g., facility location)
- NP-hard problem
- **Solution**: Metaheuristics (simulated annealing, genetic algorithms)

**6. Multi-Objective Assignment**
- Minimize cost AND maximize quality
- Trade-offs between objectives
- **Solution**: Weighted sum, Pareto optimization

---

## Mathematical Formulation

### Linear Assignment Problem

**Decision Variables:**
- x[i,j] = 1 if worker i assigned to task j, 0 otherwise

**Parameters:**
- c[i,j] = cost of assigning worker i to task j
- n = number of workers = number of tasks

**Objective:**

```
Minimize: Σ Σ c[i,j] × x[i,j]  for i,j in 1..n
```

**Constraints:**

```python
# 1. Each worker assigned to exactly one task
for i in workers:
    Σ x[i,j] = 1  for all j

# 2. Each task assigned to exactly one worker
for j in tasks:
    Σ x[i,j] = 1  for all i

# 3. Binary assignment
for i in workers:
    for j in tasks:
        x[i,j] ∈ {0, 1}
```

### Generalized Assignment Problem (GAP)

**Decision Variables:**
- x[i,j] = 1 if task j assigned to worker i, 0 otherwise

**Parameters:**
- c[i,j] = cost of assigning task j to worker i
- r[i,j] = resource consumption (e.g., time) when task j assigned to worker i
- R[i] = resource capacity of worker i
- m = number of workers
- n = number of tasks

**Objective:**

```
Minimize: Σ Σ c[i,j] × x[i,j]  for i in 1..m, j in 1..n
```

**Constraints:**

```python
# 1. Each task assigned to exactly one worker
for j in tasks:
    Σ x[i,j] = 1  for all i

# 2. Worker capacity constraint
for i in workers:
    Σ (r[i,j] × x[i,j]) ≤ R[i]  for all j

# 3. Binary assignment
x[i,j] ∈ {0, 1}
```

---

## Assignment Algorithms

### Hungarian Algorithm (Optimal for LAP)

```python
import numpy as np
from scipy.optimize import linear_sum_assignment

def hungarian_assignment(cost_matrix):
    """
    Solve assignment problem using Hungarian algorithm

    Parameters:
    -----------
    cost_matrix : 2D numpy array
        cost[i,j] = cost of assigning worker i to task j

    Returns:
    --------
    Optimal assignment
    """

    # Solve using scipy's implementation
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Calculate total cost
    total_cost = cost_matrix[row_ind, col_ind].sum()

    assignments = list(zip(row_ind, col_ind))

    return {
        'assignments': assignments,
        'total_cost': total_cost,
        'row_indices': row_ind,
        'col_indices': col_ind
    }


# Example: Assign 5 workers to 5 tasks
workers = ['Worker_A', 'Worker_B', 'Worker_C', 'Worker_D', 'Worker_E']
tasks = ['Task_1', 'Task_2', 'Task_3', 'Task_4', 'Task_5']

# Cost matrix (worker × task)
cost_matrix = np.array([
    [9, 2, 7, 8, 5],   # Worker_A costs
    [6, 4, 3, 7, 9],   # Worker_B costs
    [5, 8, 1, 8, 3],   # Worker_C costs
    [7, 6, 9, 4, 2],   # Worker_D costs
    [3, 7, 8, 2, 6]    # Worker_E costs
])

result = hungarian_assignment(cost_matrix)

print("Hungarian Algorithm Solution:")
print(f"Total Cost: {result['total_cost']}")
print("\nAssignments:")
for worker_idx, task_idx in result['assignments']:
    print(f"  {workers[worker_idx]} → {tasks[task_idx]} "
          f"(cost: {cost_matrix[worker_idx, task_idx]})")
```

### Greedy Assignment

```python
import pandas as pd

def greedy_assignment(cost_matrix, workers, tasks):
    """
    Greedy heuristic for assignment problem

    Algorithm:
    1. Find minimum cost assignment
    2. Assign it, remove worker and task from pool
    3. Repeat until all assigned

    Not optimal, but fast O(n²)

    Parameters:
    -----------
    cost_matrix : 2D numpy array
    workers : list
    tasks : list

    Returns:
    --------
    Assignment (not optimal, but fast)
    """

    assignments = []
    total_cost = 0

    available_workers = set(range(len(workers)))
    available_tasks = set(range(len(tasks)))

    while available_workers and available_tasks:
        # Find minimum cost among available assignments
        min_cost = float('inf')
        best_assignment = None

        for i in available_workers:
            for j in available_tasks:
                if cost_matrix[i, j] < min_cost:
                    min_cost = cost_matrix[i, j]
                    best_assignment = (i, j)

        # Make assignment
        worker_idx, task_idx = best_assignment
        assignments.append((worker_idx, task_idx))
        total_cost += min_cost

        # Remove from available
        available_workers.remove(worker_idx)
        available_tasks.remove(task_idx)

    return {
        'assignments': assignments,
        'total_cost': total_cost
    }


result_greedy = greedy_assignment(cost_matrix, workers, tasks)

print("\nGreedy Assignment Solution:")
print(f"Total Cost: {result_greedy['total_cost']}")
print(f"Optimal Cost: {result['total_cost']}")
print(f"Greedy vs Optimal: {(result_greedy['total_cost'] - result['total_cost']) / result['total_cost'] * 100:.1f}% worse")
```

### Generalized Assignment Problem (GAP) - Heuristic

```python
from pulp import *

def solve_gap_heuristic(tasks, workers, costs, resource_usage, capacities):
    """
    Solve Generalized Assignment Problem using MIP

    Parameters:
    -----------
    tasks : list
        Task identifiers
    workers : list
        Worker identifiers
    costs : dict
        {(worker, task): cost}
    resource_usage : dict
        {(worker, task): time_hours}
    capacities : dict
        {worker: max_hours}

    Returns:
    --------
    Assignments (may be suboptimal for large problems)
    """

    prob = LpProblem("Generalized_Assignment", LpMinimize)

    # Decision variables
    x = LpVariable.dicts("assign",
                        [(w, t) for w in workers for t in tasks],
                        cat='Binary')

    # Objective: minimize total cost
    prob += lpSum([
        costs.get((w, t), 1000) * x[w, t]
        for w in workers for t in tasks
    ]), "Total_Cost"

    # Constraints

    # 1. Each task assigned to exactly one worker
    for t in tasks:
        prob += lpSum([x[w, t] for w in workers]) == 1, f"Task_{t}"

    # 2. Worker capacity
    for w in workers:
        prob += lpSum([
            resource_usage.get((w, t), 0) * x[w, t]
            for t in tasks
        ]) <= capacities.get(w, 40), f"Worker_{w}_Capacity"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = []
    total_cost = 0

    for w in workers:
        worker_tasks = []
        for t in tasks:
            if x[w, t].varValue > 0.5:
                worker_tasks.append(t)
                total_cost += costs.get((w, t), 0)

        if worker_tasks:
            assignments.append({
                'worker': w,
                'tasks': worker_tasks,
                'num_tasks': len(worker_tasks),
                'utilization': sum(resource_usage.get((w, t), 0) for t in worker_tasks)
            })

    return {
        'status': LpStatus[prob.status],
        'assignments': pd.DataFrame(assignments),
        'total_cost': total_cost
    }


# Example: Assign 10 tasks to 3 workers
tasks = [f'Task_{i}' for i in range(1, 11)]
workers = ['Worker_A', 'Worker_B', 'Worker_C']

# Different workers have different costs and speeds for tasks
costs = {
    ('Worker_A', t): np.random.randint(10, 50) for t in tasks
}
costs.update({
    ('Worker_B', t): np.random.randint(15, 60) for t in tasks
})
costs.update({
    ('Worker_C', t): np.random.randint(12, 55) for t in tasks
})

# Time required for each worker-task combination
resource_usage = {
    ('Worker_A', t): np.random.uniform(2, 8) for t in tasks
}
resource_usage.update({
    ('Worker_B', t): np.random.uniform(3, 7) for t in tasks
})
resource_usage.update({
    ('Worker_C', t): np.random.uniform(2.5, 6) for t in tasks
})

# Worker capacities (hours available)
capacities = {
    'Worker_A': 40,
    'Worker_B': 30,  # Part-time
    'Worker_C': 40
}

result_gap = solve_gap_heuristic(tasks, workers, costs, resource_usage, capacities)

print(f"\nGAP Solution Status: {result_gap['status']}")
print(f"Total Cost: ${result_gap['total_cost']:.2f}")
print("\nAssignments:")
print(result_gap['assignments'])
```

---

## Advanced Assignment Techniques

### Skills-Based Assignment

```python
def skill_based_assignment(tasks, workers, costs, skill_requirements, worker_skills):
    """
    Assignment with skill constraints

    Workers can only be assigned to tasks matching their skills

    Parameters:
    -----------
    tasks : list
    workers : list
    costs : dict
        {(worker, task): cost}
    skill_requirements : dict
        {task: [required_skills]}
    worker_skills : dict
        {worker: [skills]}

    Returns:
    --------
    Skill-constrained assignments
    """

    prob = LpProblem("Skill_Based_Assignment", LpMinimize)

    # Filter feasible assignments (worker has required skills)
    feasible_assignments = []
    for w in workers:
        for t in tasks:
            required = set(skill_requirements.get(t, []))
            available = set(worker_skills.get(w, []))

            if required.issubset(available):
                feasible_assignments.append((w, t))

    # Decision variables (only for feasible assignments)
    x = LpVariable.dicts("assign",
                        feasible_assignments,
                        cat='Binary')

    # Objective
    prob += lpSum([
        costs.get((w, t), 1000) * x[w, t]
        for (w, t) in feasible_assignments
    ]), "Total_Cost"

    # Constraints

    # 1. Each task assigned to exactly one worker (if possible)
    for t in tasks:
        task_assignments = [(w, t) for (w, t) in feasible_assignments if t == t]
        if task_assignments:
            prob += lpSum([x[w, t] for (w, t) in task_assignments]) == 1, f"Task_{t}"

    # 2. Each worker assigned to at most one task (one-to-one assignment)
    for w in workers:
        worker_assignments = [(w, t) for (w, t) in feasible_assignments if w == w]
        if worker_assignments:
            prob += lpSum([x[w, t] for (w, t) in worker_assignments]) <= 1, f"Worker_{w}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = []
    for (w, t) in feasible_assignments:
        if x[w, t].varValue > 0.5:
            assignments.append({
                'worker': w,
                'task': t,
                'cost': costs.get((w, t), 0),
                'skills_used': skill_requirements.get(t, [])
            })

    return {
        'status': LpStatus[prob.status],
        'assignments': pd.DataFrame(assignments),
        'total_cost': value(prob.objective) if prob.status == 1 else None
    }


# Example
tasks = ['Task_A', 'Task_B', 'Task_C', 'Task_D']
workers = ['Worker_1', 'Worker_2', 'Worker_3', 'Worker_4']

skill_requirements = {
    'Task_A': ['forklift', 'inventory_mgmt'],
    'Task_B': ['packing', 'quality_control'],
    'Task_C': ['forklift'],
    'Task_D': ['receiving', 'inventory_mgmt']
}

worker_skills = {
    'Worker_1': ['forklift', 'inventory_mgmt', 'receiving'],
    'Worker_2': ['packing', 'quality_control'],
    'Worker_3': ['forklift', 'packing'],
    'Worker_4': ['inventory_mgmt', 'receiving', 'quality_control']
}

costs = {
    ('Worker_1', 'Task_A'): 10,
    ('Worker_1', 'Task_C'): 8,
    ('Worker_1', 'Task_D'): 12,
    ('Worker_2', 'Task_B'): 9,
    ('Worker_3', 'Task_C'): 7,
    ('Worker_4', 'Task_D'): 11,
    ('Worker_4', 'Task_B'): 10,
}

result_skills = skill_based_assignment(tasks, workers, costs,
                                       skill_requirements, worker_skills)

print("\nSkill-Based Assignment:")
print(result_skills['assignments'])
```

### Dynamic Task Assignment

```python
class DynamicAssignmentManager:
    """
    Manage dynamic task assignments as new tasks arrive

    Use for real-time environments (warehouse, call center, delivery)
    """

    def __init__(self, workers, initial_workloads=None):
        self.workers = workers
        self.workloads = initial_workloads if initial_workloads else {w: 0 for w in workers}
        self.assignments = []
        self.task_queue = []

    def add_task(self, task_id, priority, estimated_time):
        """Add new task to queue"""
        self.task_queue.append({
            'task_id': task_id,
            'priority': priority,
            'estimated_time': estimated_time,
            'arrival_time': datetime.now()
        })

    def assign_next_task(self, worker_capabilities=None):
        """
        Assign next task to best available worker

        Strategy:
        1. Prioritize high-priority tasks
        2. Assign to worker with lowest current workload
        3. Consider worker capabilities if provided
        """

        if not self.task_queue:
            return None

        # Sort queue by priority (highest first)
        self.task_queue.sort(key=lambda t: t['priority'], reverse=True)

        # Get next task
        next_task = self.task_queue[0]

        # Find best worker (lowest workload)
        if worker_capabilities:
            # Filter workers who can do this task
            capable_workers = [
                w for w in self.workers
                if worker_capabilities.get(w, {}).get(next_task['task_id'], False)
            ]
        else:
            capable_workers = self.workers

        if not capable_workers:
            print(f"No capable workers for task {next_task['task_id']}")
            return None

        # Assign to worker with lowest workload
        best_worker = min(capable_workers, key=lambda w: self.workloads[w])

        # Make assignment
        assignment = {
            'worker': best_worker,
            'task': next_task['task_id'],
            'assigned_time': datetime.now(),
            'estimated_completion': datetime.now() + timedelta(minutes=next_task['estimated_time'])
        }

        self.assignments.append(assignment)
        self.workloads[best_worker] += next_task['estimated_time']
        self.task_queue.pop(0)

        return assignment

    def complete_task(self, worker, actual_time):
        """Update workload when task completed"""
        self.workloads[worker] = max(0, self.workloads[worker] - actual_time)

    def rebalance_workload(self):
        """
        Rebalance tasks if workload becomes very uneven

        Reassign tasks from overloaded to underutilized workers
        """

        avg_workload = sum(self.workloads.values()) / len(self.workers)
        max_workload = max(self.workloads.values())
        min_workload = min(self.workloads.values())

        imbalance = (max_workload - min_workload) / avg_workload

        if imbalance > 0.5:  # 50% imbalance threshold
            print(f"Workload imbalance detected: {imbalance:.1%}")
            # Rebalancing logic would go here
            # Move tasks from overloaded to underutilized

        return imbalance


# Example usage
workers = ['Picker_1', 'Picker_2', 'Picker_3']
manager = DynamicAssignmentManager(workers)

# Simulate arriving tasks
for i in range(10):
    manager.add_task(
        task_id=f'Order_{i}',
        priority=np.random.choice([1, 2, 3]),
        estimated_time=np.random.randint(10, 30)
    )

# Assign tasks
print("Dynamic Task Assignment:")
for _ in range(5):
    assignment = manager.assign_next_task()
    if assignment:
        print(f"  {assignment['worker']} ← {assignment['task']}")

print(f"\nCurrent Workloads: {manager.workloads}")
print(f"Remaining Tasks: {len(manager.task_queue)}")
```

---

## Practical Assignment Applications

### Warehouse: Picker-to-Zone Assignment

```python
def assign_pickers_to_zones(pickers, zones, pick_volumes, picker_productivity):
    """
    Assign pickers to warehouse zones to balance workload

    Parameters:
    -----------
    pickers : list
        Available pickers
    zones : list
        Warehouse zones
    pick_volumes : dict
        {zone: lines_to_pick}
    picker_productivity : dict
        {picker: lines_per_hour}

    Returns:
    --------
    Optimal zone assignments
    """

    # Calculate time required per zone
    zone_hours = {
        zone: pick_volumes[zone] / 100  # Assume 100 lines/hour avg
        for zone in zones
    }

    # For each picker, calculate time if assigned to each zone
    costs = {}
    for picker in pickers:
        productivity = picker_productivity.get(picker, 100)
        for zone in zones:
            # Time = volume / productivity
            # Cost = time (want to minimize total time)
            costs[(picker, zone)] = pick_volumes[zone] / productivity

    # Solve assignment (GAP since multiple zones can go to one picker)
    # Simplified: use one-to-one for this example

    # If more zones than pickers, use GAP
    # If equal or fewer zones, use Hungarian

    if len(zones) <= len(pickers):
        # Pad to make square matrix
        n = max(len(pickers), len(zones))

        cost_matrix = np.full((n, n), 1000)  # High cost for dummy assignments

        for i, picker in enumerate(pickers):
            for j, zone in enumerate(zones):
                cost_matrix[i, j] = costs[(picker, zone)]

        result = hungarian_assignment(cost_matrix)

        assignments = []
        for picker_idx, zone_idx in result['assignments']:
            if picker_idx < len(pickers) and zone_idx < len(zones):
                picker = pickers[picker_idx]
                zone = zones[zone_idx]
                assignments.append({
                    'picker': picker,
                    'zone': zone,
                    'volume': pick_volumes[zone],
                    'estimated_time': costs[(picker, zone)]
                })

        return pd.DataFrame(assignments)

    else:
        # More zones than pickers - use GAP
        print("More zones than pickers - using GAP")
        # Implementation would be similar to solve_gap_heuristic


# Example
pickers = ['Picker_A', 'Picker_B', 'Picker_C', 'Picker_D']
zones = ['Zone_1', 'Zone_2', 'Zone_3', 'Zone_4']

pick_volumes = {
    'Zone_1': 450,
    'Zone_2': 380,
    'Zone_3': 520,
    'Zone_4': 290
}

picker_productivity = {
    'Picker_A': 120,  # Fast
    'Picker_B': 95,   # Average
    'Picker_C': 110,  # Above average
    'Picker_D': 85    # Slower
}

zone_assignments = assign_pickers_to_zones(pickers, zones, pick_volumes, picker_productivity)

print("\nPicker-to-Zone Assignments:")
print(zone_assignments)
print(f"\nMax Time: {zone_assignments['estimated_time'].max():.1f} hours (bottleneck)")
```

### Transportation: Driver-to-Route Assignment

```python
def assign_drivers_to_routes(drivers, routes, costs, constraints=None):
    """
    Assign drivers to delivery routes

    Consider:
    - Driver preferences
    - Route difficulty
    - Driver experience
    - Route constraints (hazmat, special equipment)

    Parameters:
    -----------
    drivers : list
    routes : list
    costs : dict
        {(driver, route): cost/preference_score}
    constraints : dict
        Special requirements

    Returns:
    --------
    Driver-route assignments
    """

    # Filter feasible assignments based on constraints
    feasible = []

    for driver in drivers:
        for route in routes:
            # Check constraints
            is_feasible = True

            if constraints:
                # Example: hazmat certification required
                if constraints.get(route, {}).get('hazmat_required', False):
                    if not constraints.get(driver, {}).get('hazmat_certified', False):
                        is_feasible = False

                # Example: commercial license required for large trucks
                if constraints.get(route, {}).get('cdl_required', False):
                    if not constraints.get(driver, {}).get('has_cdl', False):
                        is_feasible = False

            if is_feasible:
                feasible.append((driver, route))

    # Build cost matrix for feasible assignments
    n_drivers = len(drivers)
    n_routes = len(routes)
    n = max(n_drivers, n_routes)

    cost_matrix = np.full((n, n), 10000)  # High cost for infeasible

    for (driver, route) in feasible:
        i = drivers.index(driver)
        j = routes.index(route)
        cost_matrix[i, j] = costs.get((driver, route), 100)

    # Solve
    result = hungarian_assignment(cost_matrix)

    # Extract valid assignments
    assignments = []
    for driver_idx, route_idx in result['assignments']:
        if driver_idx < n_drivers and route_idx < n_routes:
            driver = drivers[driver_idx]
            route = routes[route_idx]

            if (driver, route) in feasible:
                assignments.append({
                    'driver': driver,
                    'route': route,
                    'cost': costs.get((driver, route), 0)
                })

    return pd.DataFrame(assignments)


# Example
drivers = ['Driver_1', 'Driver_2', 'Driver_3']
routes = ['Route_A', 'Route_B', 'Route_C']

# Cost based on driver preference and route difficulty
costs = {
    ('Driver_1', 'Route_A'): 10,
    ('Driver_1', 'Route_B'): 15,
    ('Driver_1', 'Route_C'): 12,
    ('Driver_2', 'Route_A'): 8,
    ('Driver_2', 'Route_B'): 20,
    ('Driver_2', 'Route_C'): 11,
    ('Driver_3', 'Route_A'): 14,
    ('Driver_3', 'Route_B'): 9,
    ('Driver_3', 'Route_C'): 16,
}

route_assignments = assign_drivers_to_routes(drivers, routes, costs)

print("\nDriver-to-Route Assignments:")
print(route_assignments)
```

---

## Tools & Libraries

### Assignment Software

**Optimization Solvers:**
- **Gurobi**: Commercial MIP solver with assignment models
- **CPLEX (IBM)**: Enterprise optimization solver
- **Google OR-Tools**: Open-source constraint programming and routing
- **COIN-OR CBC**: Open-source MIP solver

**Specialized Assignment:**
- **OptaPlanner (Red Hat)**: AI constraint solver for scheduling/assignment
- **MiniZinc**: Constraint modeling language
- **Satalia**: AI-powered optimization platform

### Python Libraries

```python
# Assignment Algorithms
from scipy.optimize import linear_sum_assignment  # Hungarian algorithm
from pulp import *  # MIP modeling
from ortools.sat.python import cp_model  # Constraint programming
from ortools.linear_solver import pywraplp  # Linear programming

# Optimization
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans  # For grouping before assignment

# Graph Algorithms
import networkx as nx  # For bipartite matching
```

---

## Common Challenges & Solutions

### Challenge: Unbalanced Problems

**Problem:**
- More workers than tasks (or vice versa)
- Can't use standard Hungarian algorithm directly

**Solutions:**
- Add dummy tasks/workers with zero cost
- Solve augmented problem
- Filter out dummy assignments in solution
- Alternative: Use GAP formulation (allows unassigned)

### Challenge: Multiple Objectives

**Problem:**
- Want to minimize cost AND balance workload
- Want to maximize quality AND minimize time
- Trade-offs between objectives

**Solutions:**
- Weighted sum approach (α×cost + β×workload)
- Lexicographic optimization (optimize primary, then secondary)
- Pareto frontier analysis (show trade-off curve)
- Constraints on secondary objective (cost < X, then balance)

### Challenge: Large-Scale Problems

**Problem:**
- 1000+ workers, 1000+ tasks
- Hungarian O(n³) becomes slow
- MIP solver time prohibitive

**Solutions:**
- Decomposition (solve subproblems)
- Heuristics (greedy, local search)
- Auction algorithms (faster for large sparse problems)
- Parallel computing
- Time limits with best-found solution

### Challenge: Dynamic Arrivals

**Problem:**
- Tasks arrive over time (not all known upfront)
- Online assignment problem
- Can't wait to batch and solve optimally

**Solutions:**
- Rolling horizon optimization (re-solve periodically)
- Greedy online assignment (assign immediately)
- Reserve capacity for future arrivals
- Competitive ratio analysis (compare to offline optimal)

### Challenge: Soft Constraints and Preferences

**Problem:**
- Worker preferences (not hard constraints)
- Desired but not required skill matches
- Preferred but not mandatory assignments

**Solutions:**
- Model as penalty costs in objective
- Two-phase: satisfy hard constraints, then preferences
- Multi-objective with preference as secondary
- Fairness constraints (everyone gets some preferred assignments)

---

## Output Format

### Assignment Report

**Task Assignment Results**

**Problem Summary:**
- Workers: 15
- Tasks: 15
- Assignment Type: One-to-one (Linear Assignment Problem)
- Objective: Minimize total cost
- Solution Method: Hungarian Algorithm

**Optimal Assignment:**

| Worker | Task | Cost | Skill Match | Estimated Time |
|--------|------|------|-------------|----------------|
| Worker_A | Task_07 | $25 | 100% | 2.5 hrs |
| Worker_B | Task_03 | $18 | 100% | 1.8 hrs |
| Worker_C | Task_12 | $32 | 80% | 3.2 hrs |
| Worker_D | Task_01 | $15 | 100% | 1.2 hrs |
| ... | ... | ... | ... | ... |

**Performance Metrics:**

| Metric | Value |
|--------|-------|
| Total Cost | $345 |
| Average Cost per Assignment | $23 |
| Workload Balance (Std Dev) | 0.8 hrs |
| Skill Match Rate | 92% |
| Estimated Completion Time | 3.2 hrs (bottleneck) |

**Workload Distribution:**

```
Worker_A: 2.5 hrs
Worker_B: 1.8 hrs
Worker_C: 3.2 hrs (bottleneck)
Worker_D: 1.2 hrs
Worker_E: 2.9 hrs
...

Most Balanced: Worker_B, Worker_D (light load - can help others)
Bottleneck: Worker_C (longest task)
```

**Recommendations:**
1. Consider splitting Task_12 to balance Worker_C's load
2. Worker_B and Worker_D have capacity for additional tasks
3. 92% skill match - consider training to improve flexibility

---

## Questions to Ask

If you need more context:
1. What needs to be assigned (workers, machines, resources)?
2. What are they being assigned to (tasks, jobs, orders)?
3. Is it one-to-one or can multiple tasks go to one worker?
4. What's the objective (minimize cost, maximize efficiency)?
5. Are there capacity constraints or skill requirements?
6. How many assignments (10s, 100s, 1000s)?
7. Is it a one-time assignment or recurring?
8. Do you have cost/preference data?

---

## Related Skills

- **workforce-scheduling**: For shift and labor scheduling
- **vehicle-routing-problem**: For route assignment to vehicles
- **optimization-modeling**: For mathematical formulation
- **constraint-programming**: For complex constraint handling
- **linear-programming**: For LP-based assignment
- **graph-algorithms**: For bipartite matching
- **metaheuristic-optimization**: For large-scale heuristic solutions
