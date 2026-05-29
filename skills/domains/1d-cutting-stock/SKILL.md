---
name: 1d-cutting-stock
description: When the user wants to cut 1D materials optimally, minimize waste in linear cutting, or solve one-dimensional cutting stock problems. Also use when the user mentions "1D cutting," "linear cutting optimization," "rod cutting," "pipe cutting," "beam cutting," "trim loss," "cutting stock problem," "pattern generation," or "column generation for cutting." For 2D problems, see 2d-cutting-stock. For general trim loss, see trim-loss-minimization.
---

# 1D Cutting Stock Problem

You are an expert in one-dimensional cutting stock problems and linear cutting optimization. Your goal is to help minimize material waste and costs when cutting standard-length stock materials (pipes, rods, beams, paper rolls, etc.) into smaller pieces to meet customer demand.

## Initial Assessment

Before solving 1D cutting stock problems, understand:

1. **Problem Characteristics**
   - What material is being cut? (steel rods, pipes, lumber, paper, fabric)
   - Standard stock lengths available? (e.g., 6m, 12m, custom lengths)
   - Are multiple stock lengths available or single length?
   - Cost per stock piece or per unit length?

2. **Demand Requirements**
   - How many different item lengths needed?
   - Quantity of each length? (10s, 100s, 1000s)
   - Complete list of (length, quantity) pairs?
   - Any tolerance on lengths (+/- allowance)?

3. **Cutting Constraints**
   - Minimum usable piece length?
   - Maximum number of cuts per stock?
   - Kerf width (saw blade thickness/material lost per cut)?
   - Any setup costs for different cutting patterns?

4. **Optimization Objective**
   - Minimize number of stock pieces used?
   - Minimize total material cost?
   - Minimize trim waste percentage?
   - Maximize utilization?

5. **Solution Requirements**
   - Need exact optimal solution or fast approximation?
   - Real-time cutting (online) or batch planning (offline)?
   - Can patterns be complex or need simplicity?

---

## 1D Cutting Stock Framework

### Problem Classification

**1. Classical Cutting Stock Problem (CSP)**
- Single stock length
- Multiple item lengths with demands
- Minimize number of stocks used
- Minimize waste

**2. Multiple Stock Lengths Problem**
- Different stock lengths available
- Each has different cost
- Minimize total cost (not just quantity)

**3. Residual Length Problem**
- Previously cut stocks with residual lengths available
- Use residuals before cutting new stocks
- Minimize total material consumption

**4. Cutting Stock with Setup Costs**
- Each distinct cutting pattern has setup cost
- Minimize stocks used + pattern complexity
- Trade-off between waste and setups

**5. Two-Stage Cutting**
- First cut stocks into intermediate pieces
- Then cut intermediates into final items
- Common in integrated production

---

## Mathematical Formulation

### Classical Cutting Stock Problem

**Given:**
- L = standard stock length
- n = number of item types
- l_i = length of item type i (i = 1, ..., n)
- d_i = demand for item type i

**Pattern Definition:**
A cutting pattern j is a vector a_j = (a_1j, a_2j, ..., a_nj) where:
- a_ij = number of items of type i cut from pattern j
- Σ(l_i × a_ij) ≤ L (pattern feasibility)

**Decision Variables:**
- x_j = number of times pattern j is used

**Objective:**
Minimize Σ x_j (minimize total stocks used)

**Constraints:**
Σ(a_ij × x_j) ≥ d_i  for all i = 1, ..., n (meet demand)
x_j ≥ 0, integer

**Key Challenge:**
- Number of possible patterns is exponential
- Cannot enumerate all patterns explicitly
- Requires column generation technique

---

## Algorithms and Solution Methods

### Method 1: First Fit Decreasing (FFD) - Simple Heuristic

```python
def first_fit_decreasing(items, stock_length):
    """
    First Fit Decreasing Heuristic for 1D Cutting Stock

    Fast greedy algorithm - good for quick solutions

    Parameters:
    - items: list of (length, quantity, item_id) tuples
    - stock_length: length of standard stock

    Returns: cutting plan with patterns

    Performance: Typically 10-30% above optimal
    Complexity: O(n log n + nk) where k = number of stocks used
    """

    # Expand items by quantity and sort by decreasing length
    pieces = []
    for length, quantity, item_id in items:
        for _ in range(quantity):
            pieces.append((length, item_id))

    pieces.sort(reverse=True, key=lambda x: x[0])

    # Initialize bins (stocks)
    stocks = []

    for piece_length, item_id in pieces:
        # Try to fit in existing stock
        placed = False

        for stock in stocks:
            if stock['remaining'] >= piece_length:
                stock['items'].append({
                    'length': piece_length,
                    'id': item_id
                })
                stock['remaining'] -= piece_length
                placed = True
                break

        # Need new stock
        if not placed:
            new_stock = {
                'items': [{
                    'length': piece_length,
                    'id': item_id
                }],
                'remaining': stock_length - piece_length
            }
            stocks.append(new_stock)

    # Calculate statistics
    total_used = sum(stock_length - s['remaining'] for s in stocks)
    total_available = len(stocks) * stock_length
    utilization = (total_used / total_available * 100) if total_available > 0 else 0

    return {
        'num_stocks': len(stocks),
        'stocks': stocks,
        'utilization': utilization,
        'waste': total_available - total_used
    }


# Example usage
items = [
    (2300, 5, 'A'),  # 5 pieces of 2300mm
    (1500, 8, 'B'),  # 8 pieces of 1500mm
    (1200, 12, 'C'), # 12 pieces of 1200mm
    (800, 6, 'D')    # 6 pieces of 800mm
]
stock_length = 6000

result = first_fit_decreasing(items, stock_length)
print(f"Stocks needed: {result['num_stocks']}")
print(f"Utilization: {result['utilization']:.2f}%")
print(f"Waste: {result['waste']}mm")
```

### Method 2: Best Fit Decreasing (BFD) - Improved Heuristic

```python
def best_fit_decreasing(items, stock_length):
    """
    Best Fit Decreasing Heuristic

    Better than FFD - finds tightest fit to minimize waste

    Parameters:
    - items: list of (length, quantity, item_id) tuples
    - stock_length: length of standard stock

    Returns: cutting plan

    Performance: Typically 5-20% above optimal
    """

    # Expand and sort pieces
    pieces = []
    for length, quantity, item_id in items:
        for _ in range(quantity):
            pieces.append((length, item_id))

    pieces.sort(reverse=True, key=lambda x: x[0])

    stocks = []

    for piece_length, item_id in pieces:
        # Find best fitting stock (minimum remaining space after placement)
        best_stock_idx = None
        min_remaining = float('inf')

        for idx, stock in enumerate(stocks):
            if stock['remaining'] >= piece_length:
                remaining_after = stock['remaining'] - piece_length
                if remaining_after < min_remaining:
                    min_remaining = remaining_after
                    best_stock_idx = idx

        if best_stock_idx is not None:
            # Place in best fitting stock
            stocks[best_stock_idx]['items'].append({
                'length': piece_length,
                'id': item_id
            })
            stocks[best_stock_idx]['remaining'] -= piece_length
        else:
            # Create new stock
            new_stock = {
                'items': [{
                    'length': piece_length,
                    'id': item_id
                }],
                'remaining': stock_length - piece_length
            }
            stocks.append(new_stock)

    # Calculate statistics
    total_used = sum(stock_length - s['remaining'] for s in stocks)
    total_available = len(stocks) * stock_length

    return {
        'num_stocks': len(stocks),
        'stocks': stocks,
        'utilization': (total_used / total_available * 100) if total_available > 0 else 0,
        'waste': total_available - total_used
    }
```

### Method 3: Column Generation - Optimal Solution

```python
from pulp import *
import numpy as np

class ColumnGenerationCuttingStock:
    """
    Column Generation for 1D Cutting Stock Problem

    Finds optimal or near-optimal solution using:
    1. Master Problem (LP): Select best patterns
    2. Pricing Problem (Knapsack): Generate new profitable patterns

    This is the state-of-the-art exact method for cutting stock
    """

    def __init__(self, stock_length, items, kerf=0):
        """
        Initialize cutting stock problem

        Parameters:
        - stock_length: length of standard stock
        - items: list of (length, demand, item_id) tuples
        - kerf: material lost per cut (saw blade width)
        """
        self.stock_length = stock_length
        self.items = items
        self.kerf = kerf
        self.n_items = len(items)

        # Extract lengths and demands
        self.lengths = [item[0] for item in items]
        self.demands = [item[1] for item in items]
        self.item_ids = [item[2] for item in items]

        # Storage for patterns
        self.patterns = []
        self.pattern_count = 0

    def generate_initial_patterns(self):
        """
        Generate initial patterns (one item type per pattern)
        Each pattern cuts maximum number of one item type
        """
        initial_patterns = []

        for i in range(self.n_items):
            pattern = [0] * self.n_items
            # Maximum number of item i that fits in one stock
            max_fit = int(self.stock_length / (self.lengths[i] + self.kerf))
            pattern[i] = max_fit
            initial_patterns.append(pattern)

        self.patterns = initial_patterns
        return initial_patterns

    def solve_master_problem(self):
        """
        Solve Master Problem (Restricted)

        Linear Programming Relaxation:
        Minimize Σ x_j
        Subject to: Σ(a_ij × x_j) ≥ d_i for all i
                    x_j ≥ 0

        Returns: solution and dual values
        """

        prob = LpProblem("Cutting_Stock_Master", LpMinimize)

        # Decision variables: x_j = number of times pattern j is used
        num_patterns = len(self.patterns)
        x = [LpVariable(f"x_{j}", lowBound=0, cat='Continuous')
             for j in range(num_patterns)]

        # Objective: minimize total stocks used
        prob += lpSum(x), "Total_Stocks"

        # Constraints: meet demand for each item type
        constraints = []
        for i in range(self.n_items):
            constraint = lpSum(self.patterns[j][i] * x[j]
                             for j in range(num_patterns)) >= self.demands[i]
            prob += constraint, f"Demand_{i}"
            constraints.append(constraint)

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        solution = {
            'objective': value(prob.objective),
            'pattern_usage': [x[j].varValue for j in range(num_patterns)],
            'status': LpStatus[prob.status]
        }

        # Extract dual values (shadow prices)
        dual_values = []
        for i in range(self.n_items):
            constraint_name = f"Demand_{i}"
            for name, constraint in prob.constraints.items():
                if constraint_name in name:
                    dual_values.append(constraint.pi)
                    break

        solution['dual_values'] = dual_values

        return solution

    def solve_pricing_problem(self, dual_values):
        """
        Solve Pricing Problem (Knapsack)

        Find new pattern with negative reduced cost:
        max Σ(π_i × a_i)
        subject to: Σ(l_i × a_i) ≤ L
                    a_i ≥ 0, integer

        This is a 0/1 knapsack variant (unbounded knapsack)

        Parameters:
        - dual_values: dual values from master problem (π_i)

        Returns: new pattern if found, None otherwise
        """

        # Solve unbounded knapsack
        # dp[w] = maximum value achievable with weight w
        capacity = self.stock_length
        dp = [0] * (capacity + 1)
        item_used = [[-1, 0] for _ in range(capacity + 1)]  # [item_idx, count]

        for w in range(1, capacity + 1):
            for i in range(self.n_items):
                item_length = self.lengths[i] + self.kerf
                if item_length <= w:
                    value = dp[w - item_length] + dual_values[i]
                    if value > dp[w]:
                        dp[w] = value
                        item_used[w] = [i, 1]

        # Check if new pattern is profitable (reduced cost < 0)
        # Reduced cost = 1 - max_value
        max_value = dp[capacity]
        reduced_cost = 1 - max_value

        if reduced_cost >= -1e-6:  # No profitable pattern found
            return None

        # Backtrack to find pattern
        new_pattern = [0] * self.n_items
        w = capacity

        while w > 0 and item_used[w][0] != -1:
            item_idx = item_used[w][0]
            # Count how many of this item in the pattern
            temp_w = w
            count = 0
            while temp_w > 0 and item_used[temp_w][0] == item_idx:
                count += 1
                item_length = self.lengths[item_idx] + self.kerf
                temp_w -= item_length

            new_pattern[item_idx] += count
            w = temp_w

        # Alternative: use proper unbounded knapsack backtracking
        new_pattern = self._knapsack_backtrack(dual_values)

        return new_pattern

    def _knapsack_backtrack(self, values):
        """
        Solve unbounded knapsack properly and backtrack
        """
        capacity = self.stock_length
        dp = [0] * (capacity + 1)
        used_item = [-1] * (capacity + 1)

        for w in range(1, capacity + 1):
            for i in range(self.n_items):
                item_length = self.lengths[i] + self.kerf
                if item_length <= w:
                    new_value = dp[w - item_length] + values[i]
                    if new_value > dp[w]:
                        dp[w] = new_value
                        used_item[w] = i

        # Backtrack
        pattern = [0] * self.n_items
        w = capacity

        while w > 0 and used_item[w] != -1:
            i = used_item[w]
            pattern[i] += 1
            w -= (self.lengths[i] + self.kerf)

        return pattern

    def solve(self, max_iterations=100, tolerance=1e-6):
        """
        Solve cutting stock problem using column generation

        Algorithm:
        1. Start with initial patterns
        2. Solve master problem (LP)
        3. Get dual values
        4. Solve pricing problem to generate new pattern
        5. If profitable pattern found, add to master and repeat
        6. Otherwise, solve master as IP for integer solution

        Returns: optimal cutting plan
        """

        # Generate initial patterns
        self.generate_initial_patterns()

        print("Starting Column Generation...")
        print(f"Items: {self.n_items}")
        print(f"Total demand: {sum(self.demands)}")
        print(f"Stock length: {self.stock_length}")
        print()

        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Solve master problem
            master_solution = self.solve_master_problem()

            if master_solution['status'] != 'Optimal':
                print(f"Warning: Master problem not optimal: {master_solution['status']}")
                break

            dual_values = master_solution['dual_values']

            print(f"Iteration {iteration}: LP Objective = {master_solution['objective']:.2f}")

            # Solve pricing problem
            new_pattern = self.solve_pricing_problem(dual_values)

            if new_pattern is None:
                print("No more profitable patterns. LP optimal.")
                break

            # Add new pattern
            self.patterns.append(new_pattern)
            print(f"  Added pattern: {new_pattern}")

        # Solve master problem as Integer Program for final solution
        print("\nSolving integer program for final solution...")
        integer_solution = self.solve_master_ip()

        return integer_solution

    def solve_master_ip(self):
        """
        Solve Master Problem as Integer Program

        Get integer solution from LP relaxation
        """

        prob = LpProblem("Cutting_Stock_IP", LpMinimize)

        num_patterns = len(self.patterns)
        x = [LpVariable(f"x_{j}", lowBound=0, cat='Integer')
             for j in range(num_patterns)]

        # Objective
        prob += lpSum(x), "Total_Stocks"

        # Constraints
        for i in range(self.n_items):
            prob += (lpSum(self.patterns[j][i] * x[j] for j in range(num_patterns))
                    >= self.demands[i]), f"Demand_{i}"

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        pattern_usage = [x[j].varValue for j in range(num_patterns)]

        # Build cutting plan
        stocks = []
        for j, usage in enumerate(pattern_usage):
            if usage and usage > 0.5:
                for _ in range(int(usage)):
                    stock = {
                        'pattern_id': j,
                        'pattern': self.patterns[j],
                        'items': []
                    }

                    # Add items according to pattern
                    for i in range(self.n_items):
                        if self.patterns[j][i] > 0:
                            for _ in range(self.patterns[j][i]):
                                stock['items'].append({
                                    'length': self.lengths[i],
                                    'id': self.item_ids[i]
                                })

                    # Calculate utilization
                    total_length = sum(item['length'] for item in stock['items'])
                    stock['used_length'] = total_length
                    stock['waste'] = self.stock_length - total_length

                    stocks.append(stock)

        total_used = sum(s['used_length'] for s in stocks)
        total_available = len(stocks) * self.stock_length

        solution = {
            'num_stocks': int(value(prob.objective)),
            'stocks': stocks,
            'patterns': self.patterns,
            'pattern_usage': pattern_usage,
            'utilization': (total_used / total_available * 100) if total_available > 0 else 0,
            'total_waste': total_available - total_used,
            'status': LpStatus[prob.status]
        }

        print(f"\nOptimal solution found!")
        print(f"Stocks needed: {solution['num_stocks']}")
        print(f"Utilization: {solution['utilization']:.2f}%")
        print(f"Total waste: {solution['total_waste']}")

        return solution


# Example usage
def example_column_generation():
    """Example: Cutting steel rods"""

    # Items: (length, quantity, id)
    items = [
        (2300, 5, 'A'),   # 5 pieces of 2300mm
        (1500, 8, 'B'),   # 8 pieces of 1500mm
        (1200, 12, 'C'),  # 12 pieces of 1200mm
        (800, 6, 'D'),    # 6 pieces of 800mm
        (600, 10, 'E')    # 10 pieces of 600mm
    ]

    stock_length = 6000  # 6 meter standard stock
    kerf = 5  # 5mm saw blade width

    solver = ColumnGenerationCuttingStock(stock_length, items, kerf)
    solution = solver.solve()

    # Print detailed results
    print("\n" + "="*70)
    print("CUTTING PLAN")
    print("="*70)

    for idx, stock in enumerate(solution['stocks']):
        print(f"\nStock {idx+1}:")
        print(f"  Pattern: {stock['pattern']}")
        print(f"  Items: {[f\"{item['id']}({item['length']})\" for item in stock['items']]}")
        print(f"  Used: {stock['used_length']}mm")
        print(f"  Waste: {stock['waste']}mm ({stock['waste']/stock_length*100:.1f}%)")

    return solution
```

### Method 4: Dynamic Programming - Small Problems

```python
def cutting_stock_dp_small(items, stock_length, max_stocks=None):
    """
    Dynamic Programming approach for small cutting stock problems

    Only practical for small problems due to exponential state space

    Parameters:
    - items: list of (length, quantity, item_id)
    - stock_length: standard stock length
    - max_stocks: maximum number of stocks to consider

    Returns: optimal solution

    Limitation: Only works for small problems (total items < 30)
    """

    # Expand items
    pieces = []
    for length, quantity, item_id in items:
        for _ in range(quantity):
            pieces.append((length, item_id))

    n = len(pieces)

    if n > 30:
        raise ValueError("Problem too large for DP approach. Use column generation.")

    if max_stocks is None:
        max_stocks = n  # Worst case

    # State: (items_packed_bitmask, number_of_stocks)
    # Value: True if achievable, False otherwise

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def can_pack(remaining_mask, num_stocks):
        """Check if remaining items can be packed in num_stocks"""

        if remaining_mask == 0:
            return True

        if num_stocks == 0:
            return False

        # Try all possible patterns for next stock
        # Enumerate all subsets of remaining items that fit in one stock
        for pattern_mask in range(1, remaining_mask + 1):
            if (pattern_mask & remaining_mask) != pattern_mask:
                continue

            # Check if pattern fits in one stock
            total_length = 0
            for i in range(n):
                if pattern_mask & (1 << i):
                    total_length += pieces[i][0]

            if total_length <= stock_length:
                # Try this pattern
                new_remaining = remaining_mask & ~pattern_mask
                if can_pack(new_remaining, num_stocks - 1):
                    return True

        return False

    # Find minimum number of stocks needed
    initial_mask = (1 << n) - 1  # All items need to be packed

    for num_stocks in range(1, max_stocks + 1):
        if can_pack(initial_mask, num_stocks):
            return {
                'min_stocks': num_stocks,
                'method': 'DP (exact)',
                'note': 'Optimal solution'
            }

    return None
```

---

## Complete 1D Cutting Stock Solver

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class OneDCuttingStockSolver:
    """
    Comprehensive 1D Cutting Stock Solver

    Supports multiple solution methods:
    - Fast heuristics (FFD, BFD)
    - Optimal column generation
    - Visualization
    """

    def __init__(self, stock_length, kerf=0):
        """
        Initialize solver

        Parameters:
        - stock_length: length of standard stock material
        - kerf: material lost per cut (saw blade width)
        """
        self.stock_length = stock_length
        self.kerf = kerf
        self.items = []
        self.solution = None

    def add_item(self, length, quantity, item_id=None):
        """Add item to cutting list"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append((length, quantity, item_id))

    def add_items(self, items_list):
        """
        Add multiple items

        items_list: list of (length, quantity) or (length, quantity, id)
        """
        for item in items_list:
            if len(item) == 2:
                self.add_item(item[0], item[1])
            else:
                self.add_item(item[0], item[1], item[2])

    def solve(self, method='column_generation', **kwargs):
        """
        Solve cutting stock problem

        Methods:
        - 'ffd': First Fit Decreasing (fast)
        - 'bfd': Best Fit Decreasing (better)
        - 'column_generation': Optimal or near-optimal

        Returns: solution dictionary
        """

        if method == 'ffd':
            self.solution = first_fit_decreasing(self.items, self.stock_length)
            self.solution['method'] = 'First Fit Decreasing'

        elif method == 'bfd':
            self.solution = best_fit_decreasing(self.items, self.stock_length)
            self.solution['method'] = 'Best Fit Decreasing'

        elif method == 'column_generation':
            cg_solver = ColumnGenerationCuttingStock(
                self.stock_length, self.items, self.kerf
            )
            self.solution = cg_solver.solve(**kwargs)
            self.solution['method'] = 'Column Generation (Optimal)'

        else:
            raise ValueError(f"Unknown method: {method}")

        return self.solution

    def visualize(self, max_stocks=10, save_path=None):
        """
        Visualize cutting patterns

        Parameters:
        - max_stocks: maximum number of stocks to display
        - save_path: path to save figure
        """

        if self.solution is None:
            raise ValueError("No solution to visualize. Run solve() first.")

        stocks_to_show = min(max_stocks, len(self.solution['stocks']))

        fig, axes = plt.subplots(stocks_to_show, 1,
                                figsize=(12, stocks_to_show * 0.8))

        if stocks_to_show == 1:
            axes = [axes]

        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for idx in range(stocks_to_show):
            ax = axes[idx]
            stock = self.solution['stocks'][idx]

            # Draw stock boundary
            ax.add_patch(patches.Rectangle(
                (0, 0), self.stock_length, 1,
                fill=False, edgecolor='black', linewidth=2
            ))

            # Draw pieces
            current_pos = 0
            for item_idx, item in enumerate(stock['items']):
                color = colors[hash(item['id']) % 20]

                # Draw piece
                ax.add_patch(patches.Rectangle(
                    (current_pos, 0), item['length'], 1,
                    facecolor=color, edgecolor='black',
                    linewidth=1, alpha=0.7
                ))

                # Add label
                center_x = current_pos + item['length'] / 2
                ax.text(center_x, 0.5, f"{item['id']}\n{item['length']}",
                       ha='center', va='center',
                       fontsize=8, fontweight='bold')

                current_pos += item['length']

            # Draw waste area
            if current_pos < self.stock_length:
                waste = self.stock_length - current_pos
                ax.add_patch(patches.Rectangle(
                    (current_pos, 0), waste, 1,
                    facecolor='gray', edgecolor='black',
                    linewidth=1, alpha=0.3, hatch='//'
                ))
                ax.text(current_pos + waste/2, 0.5, f"Waste\n{waste}",
                       ha='center', va='center',
                       fontsize=7, style='italic')

            ax.set_xlim(0, self.stock_length)
            ax.set_ylim(0, 1)
            ax.set_aspect('auto')
            ax.set_title(f'Stock {idx+1} (Used: {current_pos}, Waste: {self.stock_length-current_pos})',
                        fontsize=10)
            ax.set_xlabel('Length')
            ax.set_yticks([])
            ax.grid(True, alpha=0.3, axis='x')

        plt.suptitle(
            f'1D Cutting Stock Solution - {self.solution["method"]}\n'
            f'Stocks Used: {self.solution["num_stocks"]} | '
            f'Utilization: {self.solution["utilization"]:.1f}%',
            fontsize=14, fontweight='bold'
        )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def print_solution(self):
        """Print detailed solution summary"""

        if self.solution is None:
            print("No solution available.")
            return

        print("=" * 80)
        print("1D CUTTING STOCK SOLUTION")
        print("=" * 80)
        print(f"Method: {self.solution['method']}")
        print(f"Stock length: {self.stock_length}")
        print(f"Stocks used: {self.solution['num_stocks']}")
        print(f"Utilization: {self.solution['utilization']:.2f}%")
        print(f"Total waste: {self.solution.get('total_waste', self.solution.get('waste', 0))}")
        print()

        print("CUTTING PATTERNS:")
        print("-" * 80)

        for idx, stock in enumerate(self.solution['stocks'][:20]):  # Show first 20
            items_str = ", ".join([f"{item['id']}({item['length']})"
                                  for item in stock['items']])
            waste = self.stock_length - sum(item['length'] for item in stock['items'])
            print(f"Stock {idx+1:3d}: {items_str:50s} | Waste: {waste}")

        if len(self.solution['stocks']) > 20:
            print(f"... and {len(self.solution['stocks']) - 20} more stocks")

        print()

        # Item summary
        print("ITEM SUMMARY:")
        print("-" * 80)
        for length, quantity, item_id in self.items:
            print(f"{item_id}: {quantity} pieces × {length} = {quantity * length} total length")

    def export_cutting_list(self, filename):
        """Export cutting list to CSV"""

        if self.solution is None:
            raise ValueError("No solution to export. Run solve() first.")

        import csv

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Stock #', 'Item ID', 'Length', 'Position', 'Stock Waste'])

            for stock_idx, stock in enumerate(self.solution['stocks']):
                position = 0
                waste = self.stock_length - sum(item['length'] for item in stock['items'])

                for item in stock['items']:
                    writer.writerow([
                        stock_idx + 1,
                        item['id'],
                        item['length'],
                        position,
                        waste if position == 0 else ''
                    ])
                    position += item['length']

        print(f"Cutting list exported to {filename}")


# Example usage
if __name__ == "__main__":

    print("Example 1: Steel Rod Cutting")
    print("=" * 80)

    # Create solver
    solver = OneDCuttingStockSolver(stock_length=6000, kerf=5)

    # Add items to cut
    solver.add_items([
        (2300, 5, 'A'),   # 5 pieces of 2300mm
        (1500, 8, 'B'),   # 8 pieces of 1500mm
        (1200, 12, 'C'),  # 12 pieces of 1200mm
        (800, 6, 'D'),    # 6 pieces of 800mm
        (600, 10, 'E')    # 10 pieces of 600mm
    ])

    # Solve using column generation (optimal)
    print("\nSolving with Column Generation (optimal)...")
    solution = solver.solve(method='column_generation')
    solver.print_solution()

    # Visualize
    solver.visualize(max_stocks=5)

    # Export cutting list
    solver.export_cutting_list('cutting_list.csv')

    print("\n" + "=" * 80)
    print("Example 2: Compare Methods")
    print("=" * 80)

    # Compare different methods
    methods = ['ffd', 'bfd', 'column_generation']
    results = {}

    for method in methods:
        solver2 = OneDCuttingStockSolver(stock_length=6000)
        solver2.add_items([
            (2300, 5, 'A'),
            (1500, 8, 'B'),
            (1200, 12, 'C'),
            (800, 6, 'D')
        ])

        solution = solver2.solve(method=method)
        results[method] = {
            'stocks': solution['num_stocks'],
            'utilization': solution['utilization']
        }

    print("\nMethod Comparison:")
    print("-" * 60)
    print(f"{'Method':<25} {'Stocks':<10} {'Utilization':<15}")
    print("-" * 60)
    for method, result in results.items():
        print(f"{method:<25} {result['stocks']:<10} {result['utilization']:<15.2f}%")
```

---

## Tools & Libraries

### Python Libraries

**PuLP** - Linear Programming
```bash
pip install pulp
```

**Google OR-Tools** - Comprehensive optimization
```python
from ortools.linear_solver import pywraplp

# OR-Tools has built-in cutting stock examples
```

**SciPy** - Optimization toolkit
```python
from scipy.optimize import linprog
```

**pycutstock** - Cutting stock specialized library
```bash
pip install pycutstock
```

### Commercial Software

- **CutList Plus** - Professional cutting optimizer
- **OptiCut** - 1D/2D cutting optimization
- **Cutting Optimization Pro** - Multi-material cutting
- **MaxCut** - Industrial cutting stock software

### Online Tools

- **Cut List Optimizer** - Free web-based
- **Cut List Calculator** - Simple cutting planner

---

## Common Challenges & Solutions

### Challenge: Large Number of Items

**Problem:**
- Hundreds or thousands of items
- Column generation too slow
- Many patterns to consider

**Solutions:**
- Use FFD/BFD for initial quick solution
- Apply column generation with time limit
- Group similar lengths together
- Use parallel pattern generation
- Implement pattern pool management

### Challenge: Multiple Stock Lengths

**Problem:**
- Different stock lengths available
- Each has different cost
- Must choose which stock to use

**Solutions:**
```python
def multi_length_cutting_stock(items, stock_specs):
    """
    Solve cutting stock with multiple stock lengths

    Parameters:
    - items: list of (length, quantity, id)
    - stock_specs: list of (length, cost, availability)

    Returns: solution minimizing total cost
    """

    from pulp import *

    # For each stock type, generate patterns
    all_patterns = []
    pattern_costs = []
    pattern_stock_type = []

    for stock_idx, (stock_length, stock_cost, availability) in enumerate(stock_specs):
        # Generate patterns for this stock length
        # (simplified - use proper pattern generation)
        patterns = generate_patterns_for_stock(items, stock_length)

        for pattern in patterns:
            all_patterns.append(pattern)
            pattern_costs.append(stock_cost)
            pattern_stock_type.append(stock_idx)

    # Solve with cost objective
    prob = LpProblem("Multi_Stock_Cutting", LpMinimize)

    n_patterns = len(all_patterns)
    x = [LpVariable(f"x_{j}", lowBound=0, cat='Integer')
         for j in range(n_patterns)]

    # Objective: minimize total cost
    prob += lpSum(pattern_costs[j] * x[j] for j in range(n_patterns))

    # Demand constraints
    n_items = len(items)
    for i in range(n_items):
        prob += lpSum(all_patterns[j][i] * x[j]
                     for j in range(n_patterns)) >= items[i][1]

    # Availability constraints
    for stock_idx in range(len(stock_specs)):
        if stock_specs[stock_idx][2] is not None:  # If availability limited
            prob += lpSum(x[j] for j in range(n_patterns)
                         if pattern_stock_type[j] == stock_idx) <= stock_specs[stock_idx][2]

    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'total_cost': value(prob.objective),
        'pattern_usage': [x[j].varValue for j in range(n_patterns)]
    }

def generate_patterns_for_stock(items, stock_length):
    """Generate feasible patterns for a given stock length"""
    # Simplified pattern generation
    patterns = []
    # Implementation similar to column generation pricing problem
    return patterns
```

### Challenge: Residual/Leftover Management

**Problem:**
- Previously cut stocks with leftovers
- Want to use residuals before cutting new stock
- Inventory of various length leftovers

**Solutions:**
```python
def cutting_with_residuals(items, stock_length, residuals):
    """
    Cutting stock considering existing residual pieces

    Parameters:
    - items: list of (length, quantity, id)
    - stock_length: new stock length
    - residuals: list of (length, quantity) of leftover pieces

    Strategy:
    1. First try to satisfy demand from residuals
    2. Then cut new stock for remaining demand
    """

    # Step 1: Allocate residuals using FFD
    remaining_items = []

    for item_length, item_qty, item_id in items:
        qty_needed = item_qty

        # Try to use residuals
        for res_idx, (res_length, res_qty) in enumerate(residuals):
            if res_length >= item_length and res_qty > 0:
                use_qty = min(qty_needed, res_qty)
                residuals[res_idx] = (res_length, res_qty - use_qty)
                qty_needed -= use_qty

                if qty_needed == 0:
                    break

        if qty_needed > 0:
            remaining_items.append((item_length, qty_needed, item_id))

    # Step 2: Cut new stock for remaining items
    if remaining_items:
        solution = first_fit_decreasing(remaining_items, stock_length)
    else:
        solution = {'num_stocks': 0, 'stocks': []}

    return {
        'new_stocks_needed': solution['num_stocks'],
        'residuals_used': sum(r[1] for r in residuals if r[1] > 0),
        'solution': solution
    }
```

### Challenge: Setup Costs and Pattern Complexity

**Problem:**
- Different cutting patterns require different setup
- Trade-off between waste and number of patterns
- Prefer simpler patterns

**Solutions:**
- Modify objective: minimize (stocks + α × num_patterns)
- Add pattern complexity penalty
- Limit number of distinct patterns
- Use pattern repetition bonus

---

## Output Format

### Cutting Stock Solution Report

**Problem Summary:**
- Material: Steel rods
- Stock length: 6000mm
- Saw kerf: 5mm
- Total items: 41 pieces (5 different lengths)
- Total length needed: 51,400mm

**Solution:**
- Method: Column Generation (Optimal)
- Stocks used: 12
- Total material: 72,000mm
- Material utilized: 51,400mm (71.4%)
- Total waste: 20,600mm (28.6%)
- Average waste per stock: 1,717mm

**Cutting Patterns:**

| Pattern | Usage | Items | Waste | Efficiency |
|---------|-------|-------|-------|-----------|
| 1 | 3 | 2×2300, 1×1200 | 195mm | 96.8% |
| 2 | 4 | 3×1500, 1×800 | 200mm | 96.7% |
| 3 | 2 | 4×1200, 1×600 | 595mm | 90.1% |
| 4 | 3 | 6×800 | 1,200mm | 80.0% |

**Detailed Cutting List:**

```
Stock 1: A(2300) A(2300) C(1200) | Waste: 195mm
Stock 2: A(2300) A(2300) C(1200) | Waste: 195mm
Stock 3: A(2300) A(2300) C(1200) | Waste: 195mm
Stock 4: B(1500) B(1500) B(1500) D(800) | Waste: 200mm
...
```

**Material Cost Analysis:**
- Cost per stock: $45.00
- Total material cost: $540.00
- Waste cost: $154.50 (28.6%)
- Cost per item: $13.17

---

## Questions to Ask

If you need more context:

1. What material are you cutting? (steel, wood, pipe, paper, fabric)
2. What is the standard stock length(s)?
3. What items do you need? (list of lengths and quantities)
4. Is there a saw blade kerf/cutting width to account for?
5. Do you have any leftover pieces to use first?
6. Is there a minimum usable piece length?
7. What's more important: minimizing stocks or minimizing waste percentage?
8. Do you need the optimal solution or is a fast good solution okay?
9. Are there multiple stock lengths available with different costs?
10. Will this be a one-time cut or recurring production?

---

## Related Skills

- **2d-cutting-stock**: For two-dimensional sheet cutting
- **guillotine-cutting**: For guillotine cutting constraints
- **nesting-optimization**: For irregular shape nesting
- **trim-loss-minimization**: For general trim loss optimization
- **knapsack-problems**: For value-based cutting optimization
- **column-generation**: For advanced pattern generation techniques
- **optimization-modeling**: For general optimization problem formulation
