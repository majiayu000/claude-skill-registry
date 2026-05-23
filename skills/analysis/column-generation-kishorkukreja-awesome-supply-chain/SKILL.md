---
name: column-generation
description: When the user wants to solve large-scale optimization problems using column generation, decomposition methods, or Dantzig-Wolfe decomposition. Also use when the user mentions "column generation," "master problem," "pricing problem," "cutting stock," "crew scheduling," "vehicle routing with column gen," "branch-and-price," or when the problem has exponentially many variables. For general optimization, see optimization-modeling. For metaheuristics, see metaheuristic-optimization.
---

# Column Generation

You are an expert in column generation and decomposition methods for large-scale supply chain optimization. Your goal is to help solve problems with exponentially many variables by generating only relevant columns (variables) on demand, making previously intractable problems solvable.

## Initial Assessment

Before applying column generation, understand:

1. **Problem Structure**
   - Does problem have exponentially many variables?
   - Can it be decomposed into master and subproblems?
   - Is there a natural decomposition structure?
   - Are constraints decomposable?

2. **Problem Characteristics**
   - Problem type? (cutting stock, routing, crew scheduling, packing)
   - Size? (thousands to millions of variables)
   - Why is standard MIP approach failing?
   - Required solution quality?

3. **Computational Environment**
   - Solver access? (need LP/MIP solver)
   - Subproblem complexity? (easy or hard to solve)
   - Time constraints?
   - Parallel computing available?

4. **Technical Expertise**
   - Team familiarity with column generation?
   - Ability to formulate subproblem?
   - Need for exact vs. heuristic solutions?

---

## Column Generation Framework

### Core Concept

**Problem Decomposition:**
- **Master Problem**: Restricted problem with subset of variables
- **Pricing Problem**: Find new variables (columns) to improve solution
- **Iteration**: Solve master → solve pricing → add columns → repeat
- **Termination**: When no improving columns found

### Mathematical Foundation

**Original Problem (Set Partitioning):**
```
min  Σ c_j x_j
s.t. Σ a_ij x_j = 1  ∀i  (cover each element exactly once)
     x_j ∈ {0,1}
```

**Relaxed Master Problem:**
```
min  Σ c_j x_j      (j ∈ J_current)
s.t. Σ a_ij x_j = 1  ∀i
     x_j ≥ 0

Dual variables: π_i
```

**Pricing Problem:**
```
Find column j with reduced cost: c_j - Σ a_ij π_i < 0

This becomes an optimization problem specific to the application
```

---

## Cutting Stock Problem with Column Generation

### Problem Description

**1D Cutting Stock:**
- Cut large rolls of width W into smaller pieces
- Meet demand for different piece widths
- Minimize number of rolls used (minimize waste)

### Implementation

```python
import numpy as np
from pulp import *
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

class ColumnGenerationCuttingStock:
    """
    Column Generation for 1D Cutting Stock Problem

    Problem: Cut standard-width rolls into smaller pieces to meet demand
    Objective: Minimize number of rolls used
    """

    def __init__(self,
                 roll_width: float,
                 piece_widths: List[float],
                 piece_demands: List[int],
                 max_iterations: int = 100):
        """
        Initialize Column Generation for Cutting Stock

        roll_width: width of standard roll
        piece_widths: list of required piece widths
        piece_demands: demand for each piece width
        """

        self.roll_width = roll_width
        self.piece_widths = piece_widths
        self.piece_demands = piece_demands
        self.n_pieces = len(piece_widths)

        self.max_iterations = max_iterations

        # Pattern storage: each pattern is dict {piece_idx: quantity}
        self.patterns = []

        # Results
        self.optimal_patterns = None
        self.num_rolls = None
        self.iteration_history = []

    def _generate_initial_patterns(self) -> List[Dict[int, int]]:
        """
        Generate initial patterns (one piece type per pattern)

        Each pattern: maximum pieces of one width that fit in roll
        """

        patterns = []

        for i, width in enumerate(self.piece_widths):
            max_pieces = int(self.roll_width / width)
            pattern = {i: max_pieces}
            patterns.append(pattern)

        return patterns

    def _solve_master_problem(self, patterns: List[Dict[int, int]]) -> Tuple[float, List[float]]:
        """
        Solve Restricted Master Problem (RMP)

        Minimize number of rolls used
        Subject to: meet demand for each piece type

        Returns: objective value, dual values (shadow prices)
        """

        n_patterns = len(patterns)

        # Create LP model
        master = LpProblem("Master_Cutting_Stock", LpMinimize)

        # Decision variables: number of times to use each pattern
        pattern_vars = [LpVariable(f"Pattern_{j}", lowBound=0, cat='Continuous')
                       for j in range(n_patterns)]

        # Objective: minimize total number of rolls
        master += lpSum(pattern_vars), "Total_Rolls"

        # Constraints: meet demand for each piece type
        constraints = []
        for i in range(self.n_pieces):
            constraint = lpSum([
                patterns[j].get(i, 0) * pattern_vars[j]
                for j in range(n_patterns)
            ]) >= self.piece_demands[i]

            master += constraint, f"Demand_Piece_{i}"
            constraints.append(constraint)

        # Solve
        master.solve(PULP_CBC_CMD(msg=0))

        # Extract results
        obj_value = value(master.objective)

        # Extract dual values (shadow prices)
        dual_values = []
        for constraint in constraints:
            # Get dual value from constraint
            dual = constraint.pi if hasattr(constraint, 'pi') else 0
            dual_values.append(dual)

        # Fallback if dual extraction fails (use simplified approach)
        if all(d == 0 for d in dual_values):
            # Estimate duals from solution
            for i in range(self.n_pieces):
                total_produced = sum(patterns[j].get(i, 0) * pattern_vars[j].varValue
                                   for j in range(n_patterns))
                if total_produced > 0:
                    dual_values[i] = 1.0 / self.piece_widths[i]
                else:
                    dual_values[i] = 1.0

        return obj_value, dual_values

    def _solve_pricing_problem(self, dual_values: List[float]) -> Tuple[Dict[int, int], float]:
        """
        Solve Pricing Subproblem (knapsack problem)

        Find cutting pattern with negative reduced cost

        Reduced cost = 1 - Σ (pieces_i * dual_i)

        This is a knapsack problem:
        max  Σ dual_i * pieces_i
        s.t. Σ width_i * pieces_i ≤ roll_width
             pieces_i ≥ 0, integer

        Returns: new pattern, reduced cost
        """

        # Create knapsack model
        pricing = LpProblem("Pricing_Knapsack", LpMaximize)

        # Decision variables: number of pieces of each type in pattern
        pieces = [LpVariable(f"Piece_{i}", lowBound=0, cat='Integer')
                 for i in range(self.n_pieces)]

        # Objective: maximize value (dual values)
        pricing += lpSum([dual_values[i] * pieces[i]
                         for i in range(self.n_pieces)]), "Pattern_Value"

        # Constraint: don't exceed roll width
        pricing += lpSum([self.piece_widths[i] * pieces[i]
                         for i in range(self.n_pieces)]) <= self.roll_width, \
                   "Roll_Width"

        # Solve
        pricing.solve(PULP_CBC_CMD(msg=0))

        # Extract pattern
        new_pattern = {}
        for i in range(self.n_pieces):
            quantity = int(pieces[i].varValue)
            if quantity > 0:
                new_pattern[i] = quantity

        # Calculate reduced cost
        pattern_value = value(pricing.objective)
        reduced_cost = 1.0 - pattern_value

        return new_pattern, reduced_cost

    def optimize(self) -> Dict:
        """
        Run Column Generation algorithm

        Returns: optimization results
        """

        print(f"Starting Column Generation for Cutting Stock...")
        print(f"Roll Width: {self.roll_width}")
        print(f"Piece Types: {self.n_pieces}")
        print(f"Total Demand: {sum(self.piece_demands)}")

        # Initialize with simple patterns
        self.patterns = self._generate_initial_patterns()

        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1

            # Solve master problem
            obj_value, dual_values = self._solve_master_problem(self.patterns)

            self.iteration_history.append({
                'iteration': iteration,
                'objective': obj_value,
                'num_patterns': len(self.patterns)
            })

            print(f"\nIteration {iteration}:")
            print(f"  Current Objective: {obj_value:.2f} rolls")
            print(f"  Number of Patterns: {len(self.patterns)}")
            print(f"  Dual Values: {[f'{d:.3f}' for d in dual_values]}")

            # Solve pricing problem
            new_pattern, reduced_cost = self._solve_pricing_problem(dual_values)

            print(f"  Reduced Cost: {reduced_cost:.6f}")

            # Check termination
            if reduced_cost >= -1e-6:  # No improving pattern found
                print(f"\nOptimality reached! No more improving patterns.")
                break

            # Add new pattern
            print(f"  Adding new pattern: {new_pattern}")
            self.patterns.append(new_pattern)

        # Final solve with integer variables
        print(f"\nSolving final MIP with {len(self.patterns)} patterns...")
        self.num_rolls, self.optimal_patterns = self._solve_final_mip(self.patterns)

        return {
            'num_rolls': self.num_rolls,
            'optimal_patterns': self.optimal_patterns,
            'all_patterns': self.patterns,
            'iterations': iteration,
            'iteration_history': self.iteration_history
        }

    def _solve_final_mip(self, patterns: List[Dict[int, int]]) -> Tuple[float, Dict]:
        """
        Solve final MIP with integer pattern variables

        Returns: optimal number of rolls, pattern usage
        """

        n_patterns = len(patterns)

        # Create MIP model
        final = LpProblem("Final_Cutting_Stock_MIP", LpMinimize)

        # Decision variables: integer number of times to use each pattern
        pattern_vars = [LpVariable(f"Pattern_{j}", lowBound=0, cat='Integer')
                       for j in range(n_patterns)]

        # Objective: minimize total number of rolls
        final += lpSum(pattern_vars), "Total_Rolls"

        # Constraints: meet demand for each piece type
        for i in range(self.n_pieces):
            final += lpSum([
                patterns[j].get(i, 0) * pattern_vars[j]
                for j in range(n_patterns)
            ]) >= self.piece_demands[i], f"Demand_Piece_{i}"

        # Solve
        final.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        num_rolls = value(final.objective)

        pattern_usage = {}
        for j in range(n_patterns):
            usage = pattern_vars[j].varValue
            if usage > 0.5:  # Used
                pattern_usage[j] = int(usage)

        return num_rolls, pattern_usage

    def print_solution(self):
        """Print detailed solution"""

        print("\n" + "="*70)
        print("OPTIMAL CUTTING STOCK SOLUTION")
        print("="*70)

        print(f"\nTotal Rolls Used: {self.num_rolls}")
        print(f"\nPatterns Used:")

        total_pieces_produced = {i: 0 for i in range(self.n_pieces)}

        for pattern_idx, usage in sorted(self.optimal_patterns.items()):
            pattern = self.patterns[pattern_idx]

            print(f"\n  Pattern {pattern_idx} (use {usage} times):")

            for piece_idx, quantity in sorted(pattern.items()):
                width = self.piece_widths[piece_idx]
                print(f"    - {quantity} pieces of width {width}")
                total_pieces_produced[piece_idx] += quantity * usage

            # Calculate waste
            used_width = sum(self.piece_widths[i] * quantity
                           for i, quantity in pattern.items())
            waste = self.roll_width - used_width
            waste_pct = (waste / self.roll_width) * 100
            print(f"    Waste: {waste:.2f} ({waste_pct:.1f}%)")

        # Verify demand met
        print(f"\nDemand Satisfaction:")
        for i in range(self.n_pieces):
            demand = self.piece_demands[i]
            produced = total_pieces_produced[i]
            status = "✓" if produced >= demand else "✗"
            print(f"  Width {self.piece_widths[i]}: "
                  f"Demand = {demand}, Produced = {produced} {status}")

        # Calculate total waste
        total_waste = 0
        for pattern_idx, usage in self.optimal_patterns.items():
            pattern = self.patterns[pattern_idx]
            used_width = sum(self.piece_widths[i] * quantity
                           for i, quantity in pattern.items())
            total_waste += (self.roll_width - used_width) * usage

        total_material = self.num_rolls * self.roll_width
        waste_pct = (total_waste / total_material) * 100

        print(f"\nTotal Waste: {total_waste:.2f} ({waste_pct:.1f}%)")
        print("="*70)

    def plot_convergence(self):
        """Plot convergence of objective value"""

        iterations = [h['iteration'] for h in self.iteration_history]
        objectives = [h['objective'] for h in self.iteration_history]

        plt.figure(figsize=(10, 6))
        plt.plot(iterations, objectives, 'b-o', linewidth=2, markersize=6)
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Number of Rolls (LP Relaxation)', fontsize=12)
        plt.title('Column Generation Convergence', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_patterns(self):
        """Visualize cutting patterns"""

        if not self.optimal_patterns:
            print("No solution to plot!")
            return

        fig, axes = plt.subplots(len(self.optimal_patterns), 1,
                                figsize=(14, 2*len(self.optimal_patterns)))

        if len(self.optimal_patterns) == 1:
            axes = [axes]

        colors = plt.cm.Set3(np.linspace(0, 1, self.n_pieces))

        for ax_idx, (pattern_idx, usage) in enumerate(sorted(self.optimal_patterns.items())):
            pattern = self.patterns[pattern_idx]

            ax = axes[ax_idx]

            # Draw roll
            ax.add_patch(plt.Rectangle((0, 0), self.roll_width, 1,
                                      fill=False, edgecolor='black', linewidth=2))

            # Draw pieces
            current_pos = 0
            for piece_idx in sorted(pattern.keys()):
                quantity = pattern[piece_idx]
                width = self.piece_widths[piece_idx]

                for _ in range(quantity):
                    ax.add_patch(plt.Rectangle((current_pos, 0), width, 1,
                                              facecolor=colors[piece_idx],
                                              edgecolor='black', linewidth=1))
                    # Add label
                    ax.text(current_pos + width/2, 0.5, f'{width}',
                           ha='center', va='center', fontsize=10, fontweight='bold')

                    current_pos += width

            # Waste
            waste = self.roll_width - current_pos
            if waste > 0:
                ax.add_patch(plt.Rectangle((current_pos, 0), waste, 1,
                                          facecolor='lightgray',
                                          edgecolor='black', linewidth=1,
                                          hatch='//'))
                ax.text(current_pos + waste/2, 0.5, 'Waste',
                       ha='center', va='center', fontsize=9, style='italic')

            ax.set_xlim(0, self.roll_width)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Pattern {pattern_idx} (use {usage} times)',
                        fontsize=11, fontweight='bold')

        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    # Example problem
    roll_width = 100  # Standard roll width

    # Required piece widths and demands
    piece_widths = [45, 36, 31, 14]
    piece_demands = [97, 610, 395, 211]

    print("Cutting Stock Problem:")
    print(f"  Standard Roll Width: {roll_width}")
    for i, (width, demand) in enumerate(zip(piece_widths, piece_demands)):
        print(f"  Piece {i}: Width = {width}, Demand = {demand}")

    # Create and solve
    cg_solver = ColumnGenerationCuttingStock(
        roll_width=roll_width,
        piece_widths=piece_widths,
        piece_demands=piece_demands,
        max_iterations=50
    )

    result = cg_solver.optimize()

    # Print solution
    cg_solver.print_solution()

    # Visualize
    cg_solver.plot_convergence()
    cg_solver.plot_patterns()
```

---

## Vehicle Routing with Column Generation

### Route-Based Formulation

**Instead of**: arc variables x_{ij} (exponentially many)
**Use**: route variables r_k (generate on demand)

### Implementation Outline

```python
class ColumnGenerationVRP:
    """
    Column Generation for Vehicle Routing Problem

    Master Problem: Select routes to cover all customers
    Pricing Problem: Find new profitable route (ESPP - shortest path with resources)
    """

    def __init__(self, customers, demands, capacity, distances):
        self.customers = customers
        self.demands = demands
        self.capacity = capacity
        self.distances = distances

        # Route storage
        self.routes = []  # List of routes (each route is list of customer IDs)

    def _generate_initial_routes(self):
        """Generate initial routes (one customer per route)"""

        routes = []
        for customer in self.customers:
            if self.demands[customer] <= self.capacity:
                routes.append([customer])

        return routes

    def _solve_master_problem(self, routes):
        """
        Set Partitioning Master Problem

        min  Σ cost(route_k) * x_k
        s.t. Σ a_ik * x_k = 1  ∀i  (each customer covered exactly once)
             x_k ∈ {0,1}  (route used or not)

        LP Relaxation for column generation
        """

        master = LpProblem("VRP_Master", LpMinimize)

        # Decision variables
        route_vars = [LpVariable(f"Route_{k}", lowBound=0, cat='Continuous')
                     for k in range(len(routes))]

        # Objective: minimize total route cost
        master += lpSum([self._route_cost(routes[k]) * route_vars[k]
                        for k in range(len(routes))]), "Total_Cost"

        # Constraints: each customer covered exactly once
        for customer in self.customers:
            master += lpSum([
                (1 if customer in routes[k] else 0) * route_vars[k]
                for k in range(len(routes))
            ]) == 1, f"Cover_Customer_{customer}"

        master.solve(PULP_CBC_CMD(msg=0))

        # Extract dual values
        dual_values = self._extract_duals(master)

        return value(master.objective), dual_values

    def _solve_pricing_problem(self, dual_values):
        """
        Elementary Shortest Path Problem with Resource Constraints (ESPPRC)

        Find route with negative reduced cost:
        cost(route) - Σ dual_i (for customers in route) < 0

        This is NP-hard, often solved with:
        - Dynamic programming (labeling algorithm)
        - Heuristics for large instances
        """

        # Simplified: use heuristic (nearest neighbor with dual values)
        new_route, reduced_cost = self._heuristic_pricing(dual_values)

        return new_route, reduced_cost

    def _heuristic_pricing(self, dual_values):
        """
        Heuristic pricing using nearest neighbor with dual values

        Build route greedily to maximize: Σ dual_i - distance_cost
        """

        best_route = None
        best_reduced_cost = 0

        # Try starting from each customer
        for start_customer in self.customers:
            route = [start_customer]
            remaining_capacity = self.capacity - self.demands[start_customer]
            unvisited = set(self.customers) - {start_customer}
            current = start_customer

            # Greedy construction
            while unvisited:
                # Find best next customer
                best_next = None
                best_value = -float('inf')

                for next_customer in unvisited:
                    if self.demands[next_customer] <= remaining_capacity:
                        # Value = dual - distance cost
                        value = (dual_values.get(next_customer, 0) -
                               self.distances[current][next_customer])

                        if value > best_value:
                            best_value = value
                            best_next = next_customer

                if best_next is None:
                    break

                route.append(best_next)
                current = best_next
                remaining_capacity -= self.demands[best_next]
                unvisited.remove(best_next)

            # Calculate reduced cost for this route
            route_cost = self._route_cost(route)
            dual_sum = sum(dual_values.get(c, 0) for c in route)
            reduced_cost = route_cost - dual_sum

            if reduced_cost < best_reduced_cost:
                best_reduced_cost = reduced_cost
                best_route = route

        return best_route, best_reduced_cost

    def optimize(self):
        """Run column generation for VRP"""

        # Initialize routes
        self.routes = self._generate_initial_routes()

        iteration = 0
        max_iterations = 100

        while iteration < max_iterations:
            iteration += 1

            # Solve master
            obj_value, dual_values = self._solve_master_problem(self.routes)

            print(f"Iteration {iteration}: Objective = {obj_value:.2f}")

            # Solve pricing
            new_route, reduced_cost = self._solve_pricing_problem(dual_values)

            if reduced_cost >= -1e-6:  # No improving route
                print("Optimal solution found!")
                break

            # Add new route
            self.routes.append(new_route)
            print(f"  Added route: {new_route}")

        return self.routes
```

---

## Branch-and-Price

### Combining Column Generation with Branch-and-Bound

**Branch-and-Price:**
- Column generation at each node of branch-and-bound tree
- Needed when integer solution required
- Branching on original variables difficult (many not in RMP)

**Branching Strategies:**
1. **Branch on original variables**: Force variable to 0 or 1
2. **Branch on aggregate information**: e.g., "customer i served by vehicle k"
3. **Ryan-Foster branching**: For set partitioning

### Implementation Sketch

```python
class BranchAndPrice:
    """
    Branch-and-Price framework

    Combines column generation (pricing) with branch-and-bound (branching)
    """

    def __init__(self, problem):
        self.problem = problem
        self.incumbent = None
        self.incumbent_value = float('inf')

    def solve(self):
        """Branch-and-price algorithm"""

        # Initialize with root node
        root_node = BPNode(
            problem=self.problem,
            bounds=[],  # No branching constraints yet
            depth=0
        )

        node_queue = [root_node]

        while node_queue:
            # Select node (depth-first or best-first)
            node = node_queue.pop(0)

            # Solve node with column generation
            node_solution = self._solve_node_column_generation(node)

            # Pruning
            if node_solution['bound'] >= self.incumbent_value:
                continue  # Prune by bound

            # Check integrality
            if self._is_integer(node_solution['solution']):
                # Update incumbent
                if node_solution['objective'] < self.incumbent_value:
                    self.incumbent = node_solution['solution']
                    self.incumbent_value = node_solution['objective']
                continue

            # Branch
            child_nodes = self._branch(node, node_solution)
            node_queue.extend(child_nodes)

        return self.incumbent

    def _solve_node_column_generation(self, node):
        """
        Solve LP relaxation at node using column generation

        Modified pricing problem with branching constraints
        """

        # Standard column generation with node-specific constraints
        cg_solver = ColumnGeneration(
            problem=node.problem,
            branching_constraints=node.bounds
        )

        return cg_solver.optimize()

    def _branch(self, node, solution):
        """
        Create child nodes by branching

        Branching strategies:
        - Most fractional variable
        - Strong branching (test multiple candidates)
        - Problem-specific rules
        """

        # Select branching variable/constraint
        branch_var = self._select_branching_variable(solution)

        # Create two child nodes
        child1 = BPNode(
            problem=node.problem,
            bounds=node.bounds + [(branch_var, '==', 0)],
            depth=node.depth + 1
        )

        child2 = BPNode(
            problem=node.problem,
            bounds=node.bounds + [(branch_var, '==', 1)],
            depth=node.depth + 1
        )

        return [child1, child2]
```

---

## Advanced Column Generation Techniques

### Stabilization

**Problem**: Master problem dual values oscillate
**Solution**: Stabilized column generation

```python
def stabilized_column_generation(problem, alpha=0.5):
    """
    Stabilized column generation using dual price smoothing

    alpha: smoothing parameter (0 = no stabilization, 1 = full smoothing)
    """

    dual_values = initialize_duals()
    dual_history = []

    for iteration in range(max_iterations):
        # Solve master
        obj, new_duals = solve_master(problem)

        # Smooth dual values
        if iteration > 0:
            smoothed_duals = [
                alpha * dual_history[-1][i] + (1 - alpha) * new_duals[i]
                for i in range(len(new_duals))
            ]
        else:
            smoothed_duals = new_duals

        dual_history.append(new_duals)

        # Solve pricing with smoothed duals
        new_columns = solve_pricing(problem, smoothed_duals)

        if not new_columns:
            break

        # Add columns to master
        add_columns_to_master(new_columns)

    return solve_master_final()
```

### Column Pool Management

**Strategy**: Limit active columns to reduce master problem size

```python
def column_pool_management(all_columns, max_active=1000):
    """
    Keep only most promising columns active

    Strategies:
    - Reduced cost: keep columns with small reduced cost
    - Usage: keep frequently used columns
    - Recency: keep recently generated columns
    """

    # Score columns
    scores = []
    for col in all_columns:
        score = (
            -col.reduced_cost * 0.5 +      # Negative reduced cost is good
            col.usage_count * 0.3 +         # Frequently used
            col.recency * 0.2               # Recently generated
        )
        scores.append(score)

    # Select top columns
    sorted_idx = np.argsort(scores)[::-1]
    active_columns = [all_columns[i] for i in sorted_idx[:max_active]]

    return active_columns
```

### Heuristic Pricing

**When**: Pricing problem is hard to solve optimally
**Approach**: Use heuristics to find improving columns quickly

```python
def heuristic_pricing(dual_values, problem):
    """
    Fast heuristic to find improving columns

    Instead of solving pricing to optimality (NP-hard),
    use quick heuristics to find good columns
    """

    improving_columns = []

    # Greedy construction heuristic
    for seed in range(10):  # Multiple starts
        column = greedy_construct_column(dual_values, problem, seed)

        if column.reduced_cost < -1e-6:
            improving_columns.append(column)

    # Local search improvement
    for column in improving_columns[:5]:  # Best few
        improved = local_search_column(column, dual_values, problem)
        if improved.reduced_cost < column.reduced_cost:
            improving_columns.append(improved)

    # Sort by reduced cost
    improving_columns.sort(key=lambda c: c.reduced_cost)

    return improving_columns[:20]  # Return top 20
```

---

## Applications in Supply Chain

### 1. Crew Scheduling (Airlines, Transportation)

**Master**: Select schedules covering all flights/trips
**Pricing**: Find new profitable schedule (sequence of trips)

### 2. Cutting Stock (Manufacturing)

**Master**: Select cutting patterns minimizing waste
**Pricing**: Find new pattern (knapsack problem)

### 3. Vehicle Routing

**Master**: Select routes covering all customers
**Pricing**: Find new profitable route (shortest path with constraints)

### 4. Production Planning

**Master**: Select production plans meeting demand
**Pricing**: Find new profitable production combination

### 5. Bin Packing

**Master**: Select packing patterns for bins
**Pricing**: Find new efficient packing pattern

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: LP modeling (used in examples)
- `pyomo`: Advanced modeling
- `gurobipy`: Gurobi interface (commercial)
- `cplex`: CPLEX interface (commercial)

**Column Generation Frameworks:**
- `gcg`: Generic column generation (C++)
- `vroom`: VRP optimization (routing)
- Custom implementations (most common)

### Commercial Software

**Built-in Column Generation:**
- **FICO Xpress**: Mosel with column generation
- **CPLEX**: Callback framework for custom branching
- **Gurobi**: Callback framework

**Specialized Solvers:**
- **BaPCod**: Branch-and-Price framework
- **VRPSolver**: VRP with column generation

---

## Common Challenges & Solutions

### Challenge: Pricing Problem Too Hard

**Problem**: Subproblem is NP-hard, solving optimally too slow

**Solutions:**
- Heuristic pricing (find some improving columns, not necessarily best)
- Limited exact pricing (optimize few most promising)
- Restrict subproblem (simplify constraints)
- Lagrangian relaxation of pricing problem

### Challenge: Tailing Off Effect

**Problem**: Many iterations with small improvements

**Solutions:**
- Stabilization techniques
- Early termination criteria
- Switch to MIP earlier
- Better initialization

### Challenge: Slow Convergence

**Problem**: Too many iterations to reach optimality

**Solutions:**
- Better initial columns (use heuristics)
- Dual stabilization
- Column management (drop inactive columns)
- Parallel pricing (solve multiple subproblems simultaneously)

### Challenge: Memory Issues

**Problem**: Too many columns generated

**Solutions:**
- Column pool management
- Remove columns with bad reduced cost
- Compact master problem periodically
- Use column indices instead of storing full columns

---

## Best Practices

### Implementation Guidelines

1. **Start Simple**: Implement basic CG before branch-and-price
2. **Validate Subproblem**: Ensure pricing problem correctly formulated
3. **Test on Small Instances**: Verify optimality on solvable problems
4. **Monitor Convergence**: Track objective values and reduced costs
5. **Handle Edge Cases**: Empty master, infeasible pricing, etc.

### Performance Optimization

**Master Problem:**
- Use warm starts (reuse basis)
- Limit active constraints
- Choose efficient solver

**Pricing Problem:**
- Solve exactly when cheap
- Use heuristics when expensive
- Cache partial solutions
- Parallelize if multiple subproblems

**Column Management:**
- Generate multiple columns per iteration
- Remove dominated columns
- Pool frequently used columns

---

## Output Format

### Column Generation Report Template

**Executive Summary:**
- Problem description
- Solution approach
- Results and benefits

**Problem Formulation:**
- Master problem formulation
- Pricing problem description
- Decomposition structure

**Algorithm Configuration:**

| Component | Method | Details |
|-----------|--------|---------|
| Master Solver | CPLEX | LP relaxation |
| Pricing Method | Dynamic Programming | Labeling algorithm |
| Branching | Ryan-Foster | On customer pairs |
| Stabilization | Dual smoothing | α = 0.5 |

**Convergence:**

| Iteration | Objective (LP) | Columns Added | Reduced Cost | Time (s) |
|-----------|---------------|---------------|--------------|----------|
| 1 | 1523.4 | 15 | -45.2 | 0.3 |
| 5 | 1425.6 | 8 | -12.3 | 1.2 |
| 10 | 1398.2 | 3 | -2.1 | 2.5 |
| 15 | 1395.7 | 0 | 0.1 | 3.8 |

**Final Solution:**
- Objective value: 1396 (MIP)
- LP relaxation: 1395.7
- Gap: 0.02%
- Total columns generated: 156
- Columns in final solution: 23
- Total time: 45 seconds

---

## Questions to Ask

If you need more context:
1. What type of problem are you solving?
2. Why is standard MIP approach failing? (too many variables?)
3. Can problem be decomposed into master and subproblems?
4. What is the pricing subproblem? (knapsack, shortest path, etc.)
5. Is exact or heuristic solution acceptable?
6. What are computational time constraints?
7. Need integer solution or LP relaxation sufficient?
8. Available solver licenses? (commercial vs open-source)

---

## Related Skills

- **optimization-modeling**: For general MIP formulations
- **metaheuristic-optimization**: For heuristic approaches
- **route-optimization**: For VRP applications
- **production-scheduling**: For scheduling with CG
- **network-design**: For network optimization
- **inventory-optimization**: For multi-echelon systems
- **1d-cutting-stock**: For cutting stock applications
- **vehicle-routing-problem**: For VRP with column generation
