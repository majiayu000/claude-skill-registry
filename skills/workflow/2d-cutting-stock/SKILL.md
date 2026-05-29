---
name: 2d-cutting-stock
description: When the user wants to cut 2D sheets optimally, minimize waste in rectangular sheet cutting, or solve two-dimensional cutting stock problems. Also use when the user mentions "2D cutting," "sheet cutting optimization," "panel cutting," "glass cutting," "steel plate cutting," "guillotine cutting patterns," "two-stage cutting," or "2D trim loss." For 1D problems, see 1d-cutting-stock. For bin packing, see 2d-bin-packing. For irregular shapes, see nesting-optimization.
---

# 2D Cutting Stock Problem

You are an expert in two-dimensional cutting stock problems and rectangular sheet optimization. Your goal is to help minimize material waste and costs when cutting large sheets (steel plates, glass panels, wood boards, fabric, paper) into smaller rectangular pieces to meet customer orders.

## Initial Assessment

Before solving 2D cutting stock problems, understand:

1. **Material Characteristics**
   - What material? (steel plate, glass, wood, fabric, paper)
   - Standard sheet dimensions? (e.g., 2440×1220mm, 3000×1500mm)
   - Single sheet size or multiple available?
   - Sheet cost per piece or per square meter?
   - Material grain direction matters?

2. **Item Requirements**
   - How many different rectangular items needed?
   - Dimensions of each item (width × height)?
   - Quantity of each item?
   - Total list of (width, height, quantity) tuples?
   - Can items be rotated 90 degrees?

3. **Cutting Constraints**
   - Guillotine cuts only? (straight cuts across entire sheet)
   - Free-form cutting allowed?
   - Maximum number of cutting stages? (2-stage, 3-stage)
   - Saw blade kerf (material lost per cut)?
   - Minimum trim size?

4. **Optimization Objective**
   - Minimize number of sheets used?
   - Minimize total material cost?
   - Minimize trim waste percentage?
   - Minimize cutting complexity?
   - Balance waste vs. setup time?

5. **Production Constraints**
   - Any item grouping requirements?
   - Maximum items per sheet?
   - Cutting machine limitations?
   - Time constraints for solution?

---

## 2D Cutting Stock Framework

### Problem Classification

**1. Unconstrained 2D Cutting Stock**
- Free-form cutting allowed
- Any cutting pattern acceptable
- Minimize sheets used or waste
- Most flexible but complex

**2. Guillotine 2D Cutting Stock**
- All cuts must be guillotine (edge-to-edge)
- Simpler cutting process
- May increase waste vs. free-form
- Common in manufacturing

**3. Two-Stage Guillotine Cutting**
- Stage 1: Cut sheet into strips
- Stage 2: Cut strips into items
- Practical for many cutting machines
- Restricted pattern space

**4. Three-Stage Guillotine Cutting**
- Stage 1: Cut sheet into sections
- Stage 2: Cut sections into strips
- Stage 3: Cut strips into items
- More flexible than two-stage

**5. Non-Guillotine with Limited Cuts**
- Allow some non-guillotine cuts
- Minimize number of non-guillotine cuts
- Balance flexibility vs. complexity

---

## Mathematical Formulation

### Classical 2D Cutting Stock Problem

**Given:**
- W, H = sheet width and height
- n = number of item types
- w_i, h_i = width and height of item type i
- d_i = demand for item type i

**Pattern Definition:**
A cutting pattern p is a layout of items on one sheet where:
- Items don't overlap
- Items fit within sheet boundaries
- a_ip = number of items of type i in pattern p
- Can be represented by coordinates: (x, y, w, h, rotation) for each item

**Decision Variables:**
- x_p = number of times pattern p is used

**Objective:**
Minimize Σ x_p (minimize sheets used)

Or: Minimize Σ (cost_p × x_p) (minimize material cost)

**Constraints:**
Σ (a_ip × x_p) ≥ d_i  for all i = 1, ..., n (meet demand)
x_p ≥ 0, integer

**Complexity:**
- Strongly NP-hard
- Pattern generation is itself NP-hard (2D knapsack)
- Requires sophisticated algorithms

---

## Algorithms and Solution Methods

### Method 1: Two-Stage Guillotine Cutting - Practical Heuristic

```python
import numpy as np
from typing import List, Tuple, Dict

class TwoStageGuillotineCutting:
    """
    Two-Stage Guillotine Cutting for 2D Cutting Stock

    Stage 1: Cut sheet horizontally into strips
    Stage 2: Cut strips vertically into items

    This is a practical approximation that works well for many applications
    """

    def __init__(self, sheet_width, sheet_height, kerf=0):
        """
        Initialize solver

        Parameters:
        - sheet_width: width of standard sheet
        - sheet_height: height of standard sheet
        - kerf: material lost per cut
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.kerf = kerf
        self.items = []

    def add_item(self, width, height, quantity, item_id=None):
        """Add item to cut list"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'width': width,
            'height': height,
            'quantity': quantity,
            'area': width * height
        })

    def generate_strip_patterns(self):
        """
        Generate feasible strip patterns

        A strip pattern: one height, multiple items of possibly different widths

        Returns: list of strip patterns
        """
        strip_patterns = []

        # For each unique height, generate strip patterns
        unique_heights = list(set(item['height'] for item in self.items))

        for strip_height in unique_heights:
            if strip_height > self.sheet_height:
                continue

            # Items that fit this height
            eligible_items = [item for item in self.items
                            if item['height'] <= strip_height]

            # Use 1D cutting stock to pack items into strip width
            patterns = self._generate_1d_patterns_for_strip(
                eligible_items, strip_height, self.sheet_width
            )

            for pattern in patterns:
                strip_patterns.append({
                    'height': strip_height,
                    'items': pattern,
                    'waste_width': self._calculate_strip_waste(pattern)
                })

        return strip_patterns

    def _generate_1d_patterns_for_strip(self, eligible_items, strip_height, strip_width):
        """
        Generate 1D patterns for items that fit in a strip

        This is essentially 1D cutting stock in the width dimension
        """
        patterns = []

        # Simple greedy pattern generation
        # In practice, use proper 1D column generation here

        # Pattern 1: Single item type per strip (simple patterns)
        for item in eligible_items:
            if item['height'] == strip_height:
                num_fit = int(strip_width / (item['width'] + self.kerf))
                if num_fit > 0:
                    pattern = {item['id']: num_fit}
                    patterns.append(pattern)

        # Pattern 2: Multiple item types (mixed patterns)
        # Simplified: try pairs of items
        for i, item1 in enumerate(eligible_items):
            if item1['height'] > strip_height:
                continue

            for item2 in eligible_items[i:]:
                if item2['height'] > strip_height:
                    continue

                # Try different combinations
                for n1 in range(int(strip_width / (item1['width'] + self.kerf)) + 1):
                    remaining = strip_width - n1 * (item1['width'] + self.kerf)
                    n2 = int(remaining / (item2['width'] + self.kerf))

                    if n1 + n2 > 0:
                        pattern = {}
                        if n1 > 0:
                            pattern[item1['id']] = n1
                        if n2 > 0:
                            pattern[item2['id']] = n2
                        patterns.append(pattern)

        return patterns

    def _calculate_strip_waste(self, pattern):
        """Calculate waste width in a strip pattern"""
        total_width = 0
        for item in self.items:
            if item['id'] in pattern:
                total_width += item['width'] * pattern[item['id']]
        return self.sheet_width - total_width

    def solve_column_generation(self):
        """
        Solve 2-stage guillotine cutting using column generation

        This is simplified - full implementation would use proper pricing problem
        """

        from pulp import *

        # Generate initial strip patterns
        strip_patterns = self.generate_strip_patterns()

        # Master problem: select strips to pack into sheets
        prob = LpProblem("Two_Stage_Cutting", LpMinimize)

        # Variables: how many of each strip pattern to use
        n_patterns = len(strip_patterns)
        x = [LpVariable(f"strip_{i}", lowBound=0, cat='Integer')
             for i in range(n_patterns)]

        # Approximate number of sheets as sum of strip heights / sheet height
        # This is a simplification; exact formulation requires bin packing constraint
        prob += lpSum(x[i] * strip_patterns[i]['height'] / self.sheet_height
                     for i in range(n_patterns)), "Sheets"

        # Demand constraints
        for item in self.items:
            item_id = item['id']
            prob += lpSum(x[i] * strip_patterns[i]['items'].get(item_id, 0)
                         for i in range(n_patterns)) >= item['quantity'], f"Demand_{item_id}"

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        strip_usage = [x[i].varValue for i in range(n_patterns)]

        # Pack strips into sheets
        sheets = self._pack_strips_into_sheets(strip_patterns, strip_usage)

        return {
            'num_sheets': len(sheets),
            'sheets': sheets,
            'strip_patterns': strip_patterns,
            'strip_usage': strip_usage
        }

    def _pack_strips_into_sheets(self, strip_patterns, strip_usage):
        """
        Pack strips into sheets using First Fit Decreasing Height
        """

        # Create list of strips to pack
        strips_to_pack = []
        for i, usage in enumerate(strip_usage):
            if usage and usage > 0.5:
                for _ in range(int(usage)):
                    strips_to_pack.append(strip_patterns[i])

        # Sort by decreasing height
        strips_to_pack.sort(key=lambda s: s['height'], reverse=True)

        # Pack into sheets
        sheets = []

        for strip in strips_to_pack:
            # Try to fit in existing sheet
            placed = False

            for sheet in sheets:
                if sheet['remaining_height'] >= strip['height']:
                    sheet['strips'].append(strip)
                    sheet['remaining_height'] -= strip['height']
                    placed = True
                    break

            if not placed:
                # Create new sheet
                sheets.append({
                    'strips': [strip],
                    'remaining_height': self.sheet_height - strip['height']
                })

        # Calculate utilization
        for sheet in sheets:
            used_area = sum(
                (self.sheet_width - s['waste_width']) * s['height']
                for s in sheet['strips']
            )
            sheet['utilization'] = used_area / (self.sheet_width * self.sheet_height) * 100

        return sheets

    def solve_simple(self):
        """
        Simple two-stage solution without column generation

        Faster but less optimal
        """

        # Sort items by area (largest first)
        sorted_items = sorted(self.items, key=lambda x: x['area'], reverse=True)

        sheets = []
        remaining_items = {item['id']: item['quantity'] for item in self.items}

        while any(qty > 0 for qty in remaining_items.values()):
            # Create new sheet
            sheet = self._fill_sheet_greedy(remaining_items)
            sheets.append(sheet)

        total_used_area = sum(
            sum(item['width'] * item['height'] * item.get('count', 1)
                for item in sheet['items'])
            for sheet in sheets
        )
        total_sheet_area = len(sheets) * self.sheet_width * self.sheet_height

        return {
            'num_sheets': len(sheets),
            'sheets': sheets,
            'utilization': (total_used_area / total_sheet_area * 100) if total_sheet_area > 0 else 0
        }

    def _fill_sheet_greedy(self, remaining_items):
        """Fill one sheet greedily using two-stage approach"""

        sheet = {
            'strips': [],
            'items': [],
            'remaining_height': self.sheet_height
        }

        # Sort items by height (tallest first)
        items_by_height = sorted(
            [(item, remaining_items[item['id']]) for item in self.items
             if remaining_items[item['id']] > 0],
            key=lambda x: x[0]['height'],
            reverse=True
        )

        for item, qty_needed in items_by_height:
            if sheet['remaining_height'] < item['height']:
                continue

            # Create strip for this item
            strip_height = item['height']
            strip_width = self.sheet_width
            num_items_in_strip = int(strip_width / (item['width'] + self.kerf))

            if num_items_in_strip > 0:
                num_items_to_cut = min(num_items_in_strip, qty_needed)

                sheet['strips'].append({
                    'height': strip_height,
                    'items': [{
                        'id': item['id'],
                        'width': item['width'],
                        'height': item['height'],
                        'count': num_items_to_cut
                    }]
                })

                sheet['items'].extend([item] * num_items_to_cut)
                remaining_items[item['id']] -= num_items_to_cut
                sheet['remaining_height'] -= strip_height

        return sheet


# Example usage
def example_two_stage_cutting():
    """Example: Cutting steel plates"""

    solver = TwoStageGuillotineCutting(
        sheet_width=2440,  # mm
        sheet_height=1220,  # mm
        kerf=3  # mm saw kerf
    )

    # Add items to cut
    solver.add_item(800, 600, 10, 'A')
    solver.add_item(1000, 500, 8, 'B')
    solver.add_item(600, 400, 15, 'C')
    solver.add_item(1200, 800, 5, 'D')

    # Solve
    print("Solving two-stage guillotine cutting...")
    solution = solver.solve_simple()

    print(f"\nSheets needed: {solution['num_sheets']}")
    print(f"Utilization: {solution['utilization']:.2f}%")

    for i, sheet in enumerate(solution['sheets']):
        print(f"\nSheet {i+1}:")
        for strip in sheet['strips']:
            print(f"  Strip (h={strip['height']}): {strip['items']}")

    return solution
```

### Method 2: Column Generation for 2D Cutting Stock

```python
from pulp import *
import itertools

class ColumnGeneration2DCuttingStock:
    """
    Column Generation for 2D Cutting Stock Problem

    Uses:
    - Master Problem: Select best cutting patterns
    - Pricing Problem: Generate new patterns (2D knapsack)

    Note: Pricing problem for 2D is NP-hard itself
    We use heuristics for pattern generation
    """

    def __init__(self, sheet_width, sheet_height, items, kerf=0):
        """
        Initialize solver

        Parameters:
        - sheet_width: sheet width
        - sheet_height: sheet height
        - items: list of {'id', 'width', 'height', 'quantity'}
        - kerf: cutting kerf
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.items = items
        self.kerf = kerf
        self.n_items = len(items)

        self.patterns = []

    def generate_initial_patterns(self):
        """
        Generate initial patterns

        Simple approach: one item type per pattern, maximum quantity that fits
        """
        initial_patterns = []

        for item in self.items:
            # Calculate max items that fit
            max_cols = int(self.sheet_width / (item['width'] + self.kerf))
            max_rows = int(self.sheet_height / (item['height'] + self.kerf))
            max_items = max_cols * max_rows

            if max_items > 0:
                pattern = {
                    'items': {item['id']: max_items},
                    'layout': self._create_simple_layout(item, max_cols, max_rows)
                }
                initial_patterns.append(pattern)

            # Also try rotated
            if item['width'] != item['height']:
                max_cols_rot = int(self.sheet_width / (item['height'] + self.kerf))
                max_rows_rot = int(self.sheet_height / (item['width'] + self.kerf))
                max_items_rot = max_cols_rot * max_rows_rot

                if max_items_rot > max_items:
                    pattern = {
                        'items': {item['id']: max_items_rot},
                        'layout': self._create_simple_layout_rotated(item, max_cols_rot, max_rows_rot)
                    }
                    initial_patterns.append(pattern)

        self.patterns = initial_patterns
        return initial_patterns

    def _create_simple_layout(self, item, cols, rows):
        """Create simple grid layout"""
        layout = []
        for row in range(rows):
            for col in range(cols):
                layout.append({
                    'id': item['id'],
                    'x': col * (item['width'] + self.kerf),
                    'y': row * (item['height'] + self.kerf),
                    'width': item['width'],
                    'height': item['height'],
                    'rotated': False
                })
        return layout

    def _create_simple_layout_rotated(self, item, cols, rows):
        """Create simple grid layout with rotation"""
        layout = []
        for row in range(rows):
            for col in range(cols):
                layout.append({
                    'id': item['id'],
                    'x': col * (item['height'] + self.kerf),
                    'y': row * (item['width'] + self.kerf),
                    'width': item['height'],  # Swapped
                    'height': item['width'],  # Swapped
                    'rotated': True
                })
        return layout

    def solve_master_problem(self):
        """
        Solve Master Problem (LP Relaxation)

        min Σ x_p
        s.t. Σ a_ip * x_p >= d_i  ∀i
             x_p >= 0
        """

        prob = LpProblem("2D_Cutting_Master", LpMinimize)

        n_patterns = len(self.patterns)
        x = [LpVariable(f"x_{p}", lowBound=0, cat='Continuous')
             for p in range(n_patterns)]

        # Objective: minimize sheets
        prob += lpSum(x), "Total_Sheets"

        # Demand constraints
        for item in self.items:
            item_id = item['id']
            prob += lpSum(
                self.patterns[p]['items'].get(item_id, 0) * x[p]
                for p in range(n_patterns)
            ) >= item['quantity'], f"Demand_{item_id}"

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract dual values
        dual_values = {}
        for item in self.items:
            constraint_name = f"Demand_{item['id']}"
            for name, constraint in prob.constraints.items():
                if constraint_name in name:
                    dual_values[item['id']] = constraint.pi
                    break

        return {
            'objective': value(prob.objective),
            'pattern_usage': [x[p].varValue for p in range(n_patterns)],
            'dual_values': dual_values,
            'status': LpStatus[prob.status]
        }

    def solve_pricing_problem(self, dual_values):
        """
        Solve Pricing Problem: Find pattern with negative reduced cost

        This is a 2D knapsack problem - NP-hard
        We use heuristic pattern generation

        max Σ π_i * a_i
        s.t. items fit in sheet without overlap
        """

        # Use greedy heuristic to generate pattern
        # Try several heuristics and pick best

        best_pattern = None
        best_value = 0

        # Heuristic 1: Greedy by value density
        pattern1 = self._generate_pattern_greedy_value(dual_values)
        value1 = self._calculate_pattern_value(pattern1, dual_values)

        if value1 > best_value:
            best_value = value1
            best_pattern = pattern1

        # Heuristic 2: First Fit Decreasing
        pattern2 = self._generate_pattern_ffd(dual_values)
        value2 = self._calculate_pattern_value(pattern2, dual_values)

        if value2 > best_value:
            best_value = value2
            best_pattern = pattern2

        # Check reduced cost
        reduced_cost = 1 - best_value

        if reduced_cost >= -1e-6:
            return None  # No profitable pattern

        return best_pattern

    def _generate_pattern_greedy_value(self, dual_values):
        """Generate pattern greedily by value density"""

        # Calculate value per area for each item
        items_with_value = []
        for item in self.items:
            value_density = dual_values.get(item['id'], 0) / (item['width'] * item['height'])
            items_with_value.append((value_density, item))

        items_with_value.sort(reverse=True)

        # Greedy placement
        placed_items = []
        occupied = np.zeros((self.sheet_height, self.sheet_width), dtype=bool)

        for _, item in items_with_value:
            # Try to place as many as possible
            for rotation in [False, True]:
                w = item['width'] if not rotation else item['height']
                h = item['height'] if not rotation else item['width']

                # Find positions where item fits
                for y in range(0, self.sheet_height - h + 1, max(1, h // 10)):
                    for x in range(0, self.sheet_width - w + 1, max(1, w // 10)):
                        if not occupied[y:y+h, x:x+w].any():
                            # Place item
                            placed_items.append({
                                'id': item['id'],
                                'x': x,
                                'y': y,
                                'width': w,
                                'height': h,
                                'rotated': rotation
                            })
                            occupied[y:y+h, x:x+w] = True

        # Convert to pattern format
        pattern = {'items': {}, 'layout': placed_items}
        for placed in placed_items:
            item_id = placed['id']
            pattern['items'][item_id] = pattern['items'].get(item_id, 0) + 1

        return pattern

    def _generate_pattern_ffd(self, dual_values):
        """Generate pattern using First Fit Decreasing"""

        # Sort items by value (dual value)
        items_sorted = sorted(
            self.items,
            key=lambda x: dual_values.get(x['id'], 0),
            reverse=True
        )

        # Use shelf-based packing
        shelves = []
        placed_items = []

        for item in items_sorted:
            # Try both orientations
            for rotation in [False, True]:
                w = item['width'] if not rotation else item['height']
                h = item['height'] if not rotation else item['width']

                # Try to fit on existing shelf
                placed = False
                for shelf in shelves:
                    if shelf['remaining_width'] >= w and shelf['height'] >= h:
                        # Place on shelf
                        x = self.sheet_width - shelf['remaining_width']
                        y = shelf['y']

                        placed_items.append({
                            'id': item['id'],
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'rotated': rotation
                        })

                        shelf['remaining_width'] -= w
                        placed = True
                        break

                if placed:
                    break

                # Try new shelf
                current_height = sum(s['height'] for s in shelves)
                if not placed and current_height + h <= self.sheet_height:
                    shelves.append({
                        'y': current_height,
                        'height': h,
                        'remaining_width': self.sheet_width - w
                    })

                    placed_items.append({
                        'id': item['id'],
                        'x': 0,
                        'y': current_height,
                        'width': w,
                        'height': h,
                        'rotated': rotation
                    })
                    break

        # Convert to pattern
        pattern = {'items': {}, 'layout': placed_items}
        for placed in placed_items:
            item_id = placed['id']
            pattern['items'][item_id] = pattern['items'].get(item_id, 0) + 1

        return pattern

    def _calculate_pattern_value(self, pattern, dual_values):
        """Calculate total value of pattern"""
        total_value = 0
        for item_id, count in pattern['items'].items():
            total_value += dual_values.get(item_id, 0) * count
        return total_value

    def solve(self, max_iterations=50):
        """
        Solve 2D cutting stock using column generation

        Returns: solution with patterns and usage
        """

        print("Starting 2D Column Generation...")

        # Generate initial patterns
        self.generate_initial_patterns()
        print(f"Initial patterns: {len(self.patterns)}")

        for iteration in range(max_iterations):
            # Solve master problem
            master_sol = self.solve_master_problem()

            print(f"Iteration {iteration+1}: LP Obj = {master_sol['objective']:.2f}")

            # Solve pricing problem
            new_pattern = self.solve_pricing_problem(master_sol['dual_values'])

            if new_pattern is None:
                print("No profitable pattern found. Optimal.")
                break

            # Add pattern
            self.patterns.append(new_pattern)
            print(f"  Added pattern with {sum(new_pattern['items'].values())} items")

        # Solve as IP
        print("\nSolving integer program...")
        final_solution = self.solve_master_ip()

        return final_solution

    def solve_master_ip(self):
        """Solve master problem as integer program"""

        prob = LpProblem("2D_Cutting_IP", LpMinimize)

        n_patterns = len(self.patterns)
        x = [LpVariable(f"x_{p}", lowBound=0, cat='Integer')
             for p in range(n_patterns)]

        prob += lpSum(x), "Total_Sheets"

        for item in self.items:
            item_id = item['id']
            prob += lpSum(
                self.patterns[p]['items'].get(item_id, 0) * x[p]
                for p in range(n_patterns)
            ) >= item['quantity'], f"Demand_{item_id}"

        prob.solve(PULP_CBC_CMD(msg=0))

        # Build solution
        pattern_usage = [x[p].varValue for p in range(n_patterns)]

        sheets = []
        for p, usage in enumerate(pattern_usage):
            if usage and usage > 0.5:
                for _ in range(int(usage)):
                    sheets.append({
                        'pattern_id': p,
                        'pattern': self.patterns[p],
                        'layout': self.patterns[p]['layout']
                    })

        # Calculate utilization
        sheet_area = self.sheet_width * self.sheet_height
        total_used = 0
        for sheet in sheets:
            for placed in sheet['layout']:
                total_used += placed['width'] * placed['height']

        utilization = (total_used / (len(sheets) * sheet_area) * 100) if sheets else 0

        return {
            'num_sheets': len(sheets),
            'sheets': sheets,
            'utilization': utilization,
            'total_waste': len(sheets) * sheet_area - total_used
        }


# Example usage
def example_2d_column_generation():
    """Example: 2D cutting stock with column generation"""

    items = [
        {'id': 'A', 'width': 800, 'height': 600, 'quantity': 10},
        {'id': 'B', 'width': 1000, 'height': 500, 'quantity': 8},
        {'id': 'C', 'width': 600, 'height': 400, 'quantity': 15},
        {'id': 'D', 'width': 1200, 'height': 800, 'quantity': 5}
    ]

    solver = ColumnGeneration2DCuttingStock(
        sheet_width=2440,
        sheet_height=1220,
        items=items,
        kerf=3
    )

    solution = solver.solve()

    print(f"\n{'='*70}")
    print(f"SOLUTION")
    print(f"{'='*70}")
    print(f"Sheets needed: {solution['num_sheets']}")
    print(f"Utilization: {solution['utilization']:.2f}%")
    print(f"Total waste: {solution['total_waste']}")

    return solution
```

### Method 3: Guillotine Cutting with Pattern Generation

```python
class GuillotineCuttingPattern:
    """
    Generate guillotine cutting patterns

    All cuts must be straight edge-to-edge
    """

    def __init__(self, sheet_width, sheet_height):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height

    def generate_guillotine_patterns(self, items, max_patterns=100):
        """
        Generate feasible guillotine cutting patterns

        Uses recursive subdivision
        """

        patterns = []

        # Try different first-cut positions and orientations
        for first_cut_horizontal in [True, False]:
            if first_cut_horizontal:
                # Horizontal first cut
                for cut_pos in range(100, self.sheet_height, 100):
                    pattern = self._recursive_guillotine(
                        0, 0, self.sheet_width, self.sheet_height,
                        items, cut_pos, True
                    )
                    if pattern:
                        patterns.append(pattern)

            else:
                # Vertical first cut
                for cut_pos in range(100, self.sheet_width, 100):
                    pattern = self._recursive_guillotine(
                        0, 0, self.sheet_width, self.sheet_height,
                        items, cut_pos, False
                    )
                    if pattern:
                        patterns.append(pattern)

            if len(patterns) >= max_patterns:
                break

        return patterns

    def _recursive_guillotine(self, x, y, width, height, items, cut_pos, horizontal):
        """
        Recursively generate guillotine pattern

        Parameters:
        - x, y: position of current rectangle
        - width, height: size of current rectangle
        - items: items to pack
        - cut_pos: position of guillotine cut
        - horizontal: True if horizontal cut, False if vertical
        """

        # Base case: try to fit single item type
        pattern = {'items': {}, 'layout': []}

        for item in items:
            # Try both orientations
            for rotated in [False, True]:
                w = item['width'] if not rotated else item['height']
                h = item['height'] if not rotated else item['width']

                # How many fit?
                cols = int(width / w)
                rows = int(height / h)
                count = cols * rows

                if count > 0:
                    # Create pattern with this item
                    for row in range(rows):
                        for col in range(cols):
                            pattern['layout'].append({
                                'id': item['id'],
                                'x': x + col * w,
                                'y': y + row * h,
                                'width': w,
                                'height': h,
                                'rotated': rotated
                            })
                    pattern['items'][item['id']] = count
                    return pattern

        return None
```

---

## Complete 2D Cutting Stock Solver

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class TwoDCuttingStockSolver:
    """
    Comprehensive 2D Cutting Stock Solver

    Supports:
    - Two-stage guillotine cutting
    - Column generation
    - Visualization
    - Export to cutting lists
    """

    def __init__(self, sheet_width, sheet_height, kerf=0):
        """
        Initialize solver

        Parameters:
        - sheet_width: standard sheet width
        - sheet_height: standard sheet height
        - kerf: saw blade kerf (material lost per cut)
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.kerf = kerf
        self.items = []
        self.solution = None

    def add_item(self, width, height, quantity, item_id=None):
        """Add rectangular item to cut list"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'width': width,
            'height': height,
            'quantity': quantity
        })

    def solve(self, method='two_stage'):
        """
        Solve 2D cutting stock problem

        Methods:
        - 'two_stage': Two-stage guillotine (fast, practical)
        - 'column_generation': Column generation (better, slower)

        Returns: solution
        """

        if method == 'two_stage':
            solver = TwoStageGuillotineCutting(
                self.sheet_width, self.sheet_height, self.kerf
            )
            for item in self.items:
                solver.add_item(item['width'], item['height'],
                              item['quantity'], item['id'])
            self.solution = solver.solve_simple()
            self.solution['method'] = 'Two-Stage Guillotine'

        elif method == 'column_generation':
            solver = ColumnGeneration2DCuttingStock(
                self.sheet_width, self.sheet_height, self.items, self.kerf
            )
            self.solution = solver.solve()
            self.solution['method'] = 'Column Generation'

        return self.solution

    def visualize(self, sheet_index=0, save_path=None):
        """
        Visualize cutting pattern for a specific sheet

        Parameters:
        - sheet_index: index of sheet to visualize
        - save_path: path to save figure
        """

        if self.solution is None:
            raise ValueError("No solution. Run solve() first.")

        if sheet_index >= len(self.solution['sheets']):
            raise ValueError(f"Sheet index {sheet_index} out of range")

        sheet = self.solution['sheets'][sheet_index]

        fig, ax = plt.subplots(figsize=(12, 8))

        # Draw sheet boundary
        ax.add_patch(patches.Rectangle(
            (0, 0), self.sheet_width, self.sheet_height,
            fill=False, edgecolor='black', linewidth=3
        ))

        # Get layout
        if 'layout' in sheet:
            layout = sheet['layout']
        else:
            # Reconstruct from strips
            layout = []
            y_pos = 0
            for strip in sheet.get('strips', []):
                for item in strip.get('items', []):
                    for i in range(item.get('count', 1)):
                        layout.append({
                            'id': item['id'],
                            'x': i * item['width'],
                            'y': y_pos,
                            'width': item['width'],
                            'height': item['height']
                        })
                y_pos += strip['height']

        # Draw items
        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for item in layout:
            color = colors[hash(item['id']) % 20]

            rect = patches.Rectangle(
                (item['x'], item['y']),
                item['width'], item['height'],
                facecolor=color, edgecolor='black',
                linewidth=1, alpha=0.7
            )
            ax.add_patch(rect)

            # Label
            cx = item['x'] + item['width'] / 2
            cy = item['y'] + item['height'] / 2
            ax.text(cx, cy, f"{item['id']}\n{item['width']}×{item['height']}",
                   ha='center', va='center',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xlim(0, self.sheet_width)
        ax.set_ylim(0, self.sheet_height)
        ax.set_aspect('equal')
        ax.set_xlabel('Width (mm)', fontsize=12)
        ax.set_ylabel('Height (mm)', fontsize=12)
        ax.set_title(
            f'2D Cutting Pattern - Sheet {sheet_index + 1}\n'
            f'Sheet: {self.sheet_width}×{self.sheet_height}mm',
            fontsize=14, fontweight='bold'
        )
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def print_solution(self):
        """Print solution summary"""

        if not self.solution:
            print("No solution available.")
            return

        print("=" * 80)
        print("2D CUTTING STOCK SOLUTION")
        print("=" * 80)
        print(f"Method: {self.solution.get('method', 'Unknown')}")
        print(f"Sheet size: {self.sheet_width} × {self.sheet_height}")
        print(f"Sheets used: {self.solution['num_sheets']}")
        print(f"Utilization: {self.solution.get('utilization', 0):.2f}%")
        print()

        print("Items to cut:")
        for item in self.items:
            print(f"  {item['id']}: {item['quantity']} pcs @ {item['width']}×{item['height']}")


# Example usage
if __name__ == "__main__":

    print("Example: Steel Plate Cutting")
    print("=" * 80)

    solver = TwoDCuttingStockSolver(
        sheet_width=2440,
        sheet_height=1220,
        kerf=3
    )

    solver.add_item(800, 600, 10, 'A')
    solver.add_item(1000, 500, 8, 'B')
    solver.add_item(600, 400, 15, 'C')
    solver.add_item(1200, 800, 5, 'D')

    # Solve
    solution = solver.solve(method='two_stage')
    solver.print_solution()

    # Visualize first sheet
    solver.visualize(sheet_index=0)
```

---

## Tools & Libraries

### Python Libraries

- **PuLP**: Linear programming for column generation
- **OR-Tools**: Google's optimization toolkit
- **py2d-pack**: 2D packing algorithms
- **rectpack**: Rectangle packing library

### Commercial Software

- **CutLogic 2D**: Professional 2D cutting optimizer
- **Cutting Optimization Pro**: Glass and metal cutting
- **OptiCut**: Sheet cutting optimization
- **MaxCut**: Industrial cutting stock

---

## Common Challenges & Solutions

### Challenge: Guillotine Constraint Too Restrictive

**Solution:** Use three-stage cutting or limited non-guillotine cuts

### Challenge: Many Small Items

**Solution:** Pre-clustering and hierarchical optimization

### Challenge: Mixed Materials

**Solution:** Multi-objective optimization balancing cost and waste

---

## Output Format

**Solution Summary:**
- Sheets used: 8
- Utilization: 87.3%
- Method: Two-Stage Guillotine

**Pattern Details:** See cutting diagrams

---

## Questions to Ask

1. What material? (steel, glass, wood, fabric)
2. Standard sheet size?
3. Items list with dimensions and quantities?
4. Guillotine cuts only?
5. Can items rotate?
6. Saw kerf width?
7. Optimization goal?

---

## Related Skills

- **1d-cutting-stock**: For 1D cutting problems
- **guillotine-cutting**: For guillotine-specific algorithms
- **nesting-optimization**: For irregular shapes
- **trim-loss-minimization**: For general trim loss
- **2d-bin-packing**: For bin packing variants
