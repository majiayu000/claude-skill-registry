---
name: guillotine-cutting
description: When the user wants to solve cutting problems with guillotine constraints, implement edge-to-edge cutting, or optimize guillotine cutting patterns. Also use when the user mentions "guillotine cuts," "edge-to-edge cutting," "straight cuts only," "two-stage cutting," "three-stage cutting," "n-stage guillotine," or "guillotine cutting stock problem." For general cutting, see 2d-cutting-stock or 1d-cutting-stock. For irregular shapes, see nesting-optimization.
---

# Guillotine Cutting

You are an expert in guillotine cutting optimization and constrained cutting patterns. Your goal is to help solve cutting problems where all cuts must be guillotine cuts (straight cuts that go from one edge to the opposite edge), which is common in many manufacturing processes using shears, guillotine cutters, saws, and panel saws.

## Initial Assessment

Before solving guillotine cutting problems, understand:

1. **Cutting Constraints**
   - Must all cuts be guillotine? (edge-to-edge)
   - What stage structure? (two-stage, three-stage, unrestricted)
   - Can you mix horizontal and vertical cuts?
   - Any preferred cut sequence?
   - Maximum number of stages allowed?

2. **Equipment Characteristics**
   - What cutting equipment? (guillotine shear, panel saw, CNC router)
   - Equipment bed size/capacity?
   - Can equipment rotate pieces?
   - Cut accuracy/tolerance?
   - Setup time per cut?

3. **Material and Items**
   - Sheet/stock dimensions?
   - Item dimensions (all rectangular in guillotine cutting)?
   - Item quantities needed?
   - Can items be rotated 90 degrees?
   - Material grain direction constraints?

4. **Optimization Goals**
   - Minimize number of sheets?
   - Minimize number of cuts?
   - Minimize cutting time?
   - Maximize material utilization?
   - Balance multiple objectives?

5. **Practical Considerations**
   - Minimum cut length?
   - Minimum piece size?
   - Kerf (saw blade width)?
   - Need to track cutting sequence?
   - Real-time vs. batch optimization?

---

## Guillotine Cutting Framework

### Understanding Guillotine Cuts

**Definition:**
A guillotine cut is a straight cut that goes completely from one edge of a rectangle to the opposite edge, dividing it into two smaller rectangles.

**Properties:**
- Cut must be parallel to one of the sides
- Cut extends fully across the material
- Creates two rectangular sub-pieces
- No partial cuts or L-shaped cuts

**Guillotine vs. Non-Guillotine:**

```
Guillotine Cut:                 Non-Guillotine:
┌────────────┐                 ┌────────────┐
│            │                 │ ┌──┐       │
│            │                 │ │  │       │
├────────────┤ ✓               │ └──┘   ┌──┤ ✗
│            │                 │        │  │
│            │                 │        └──┘
└────────────┘                 └────────────┘
```

### Problem Classification

**1. Two-Stage Guillotine Cutting**
- **Stage 1:** Cut sheet into strips (horizontal OR vertical)
- **Stage 2:** Cut strips into items (perpendicular to stage 1)
- Most restrictive but simplest
- Common in industrial panel saws

**2. Three-Stage Guillotine Cutting**
- **Stage 1:** Cut sheet into sections
- **Stage 2:** Cut sections into strips
- **Stage 3:** Cut strips into items
- More flexible than two-stage
- Can achieve better utilization

**3. N-Stage Guillotine Cutting**
- Arbitrary number of stages
- Each cut subdivides a rectangle
- Recursive structure
- Tree representation of cuts

**4. Unrestricted Guillotine Cutting**
- No stage limit
- All cuts must be guillotine
- Most flexible guillotine variant
- Harder to optimize

**5. Exact Guillotine Cutting**
- No trim waste allowed
- Items must exactly fill rectangles
- Very restrictive
- Rare in practice

---

## Mathematical Formulation

### Two-Stage Guillotine Problem

**Given:**
- W × H = sheet dimensions
- Items: {(w₁, h₁, d₁), (w₂, h₂, d₂), ..., (wₙ, hₙ, dₙ)}
  - wᵢ, hᵢ = item dimensions
  - dᵢ = demand quantity

**Decision Variables:**
- Strip patterns for stage 1
- Item patterns within strips for stage 2
- Number of times each pattern is used

**Stage 1 (Strips):**
For horizontal strips:
- Strip height h
- Number of strips with this height
- Constraint: Σ(heights) ≤ H

**Stage 2 (Items in strips):**
For each strip:
- Items that fit in strip height
- 1D cutting stock problem in strip width
- Constraint: Σ(widths) ≤ W

**Objective:**
Minimize number of sheets used

**Complexity:**
- Still NP-hard but more tractable than general 2D cutting
- Stage restriction reduces solution space
- Can use 1D algorithms for strip packing

---

## Algorithms and Solution Methods

### Method 1: Two-Stage Guillotine with Dynamic Programming

```python
import numpy as np
from typing import List, Tuple, Dict

class TwoStageGuillotine:
    """
    Two-Stage Guillotine Cutting Solver

    Stage 1: Cut sheet into horizontal strips
    Stage 2: Cut strips into items using 1D algorithm

    This is practical and widely used in industry
    """

    def __init__(self, sheet_width, sheet_height, kerf=0):
        """
        Initialize solver

        Parameters:
        - sheet_width: sheet width
        - sheet_height: sheet height
        - kerf: saw kerf (material lost per cut)
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.kerf = kerf
        self.items = []

    def add_item(self, width, height, quantity, item_id=None):
        """Add rectangular item"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'width': width,
            'height': height,
            'quantity': quantity,
            'area': width * height
        })

    def generate_strip_types(self):
        """
        Generate all feasible strip types

        A strip type is defined by its height
        """

        # Get unique heights from items
        unique_heights = set()

        for item in self.items:
            # Can use item in normal or rotated orientation
            unique_heights.add(item['height'])
            unique_heights.add(item['width'])

        # Filter heights that fit in sheet
        strip_types = [h for h in unique_heights if h <= self.sheet_height]

        return sorted(strip_types)

    def solve_1d_cutting_for_strip(self, strip_height, strip_width):
        """
        Solve 1D cutting stock for items that fit in a strip

        Returns best patterns for this strip type
        """

        # Get items that can fit in this strip height
        eligible_items = []

        for item in self.items:
            # Try both orientations
            if item['height'] <= strip_height:
                eligible_items.append({
                    'id': item['id'],
                    'length': item['width'],
                    'height': item['height'],
                    'quantity': item['quantity'],
                    'rotated': False
                })

            if item['width'] <= strip_height and item['width'] != item['height']:
                eligible_items.append({
                    'id': item['id'] + '_rot',
                    'length': item['height'],
                    'height': item['width'],
                    'quantity': item['quantity'],
                    'rotated': True
                })

        if not eligible_items:
            return []

        # Generate 1D patterns using dynamic programming
        patterns = self._generate_1d_patterns_dp(eligible_items, strip_width)

        return patterns

    def _generate_1d_patterns_dp(self, items, width):
        """
        Generate 1D cutting patterns using dynamic programming

        For each item type, find maximum number that fits
        """

        patterns = []

        # Simple patterns: one item type per pattern
        for item in items:
            max_fit = int(width / (item['length'] + self.kerf))
            if max_fit > 0:
                pattern = {
                    'items': {item['id']: max_fit},
                    'waste': width - (max_fit * item['length'] + (max_fit - 1) * self.kerf)
                }
                patterns.append(pattern)

        # Combined patterns: two item types
        for i, item1 in enumerate(items):
            for item2 in items[i:]:
                # Try different combinations
                for n1 in range(int(width / (item1['length'] + self.kerf)) + 1):
                    remaining = width - (n1 * item1['length'] + max(0, n1-1) * self.kerf)
                    n2 = int(remaining / (item2['length'] + self.kerf))

                    if n1 + n2 > 0:
                        pattern = {
                            'items': {},
                            'waste': 0
                        }

                        if n1 > 0:
                            pattern['items'][item1['id']] = n1

                        if n2 > 0:
                            pattern['items'][item2['id']] = n2

                        used = (n1 * item1['length'] + n2 * item2['length'] +
                               (n1 + n2 - 1) * self.kerf)
                        pattern['waste'] = width - used

                        if pattern not in patterns:
                            patterns.append(pattern)

        return patterns

    def solve_master_problem(self, strip_types, strip_patterns):
        """
        Solve master problem: select strips to pack into sheets

        This is simplified - full implementation uses integer programming
        """

        from pulp import *

        # Create problem
        prob = LpProblem("Two_Stage_Guillotine", LpMinimize)

        # Variables: number of each strip type pattern to use
        strip_vars = {}
        for strip_height in strip_types:
            for pattern_idx, pattern in enumerate(strip_patterns[strip_height]):
                var_name = f"strip_h{strip_height}_p{pattern_idx}"
                strip_vars[(strip_height, pattern_idx)] = LpVariable(
                    var_name, lowBound=0, cat='Integer'
                )

        # Objective: minimize number of sheets
        # Approximate: sum of strip heights / sheet height
        prob += lpSum(
            strip_vars[(h, p)] * h / self.sheet_height
            for h in strip_types
            for p in range(len(strip_patterns[h]))
        )

        # Demand constraints
        for item in self.items:
            item_id = item['id']

            # Sum across all strips and patterns
            prob += lpSum(
                strip_vars[(h, p)] * pattern['items'].get(item_id, 0) +
                strip_vars[(h, p)] * pattern['items'].get(item_id + '_rot', 0)
                for h in strip_types
                for p, pattern in enumerate(strip_patterns[h])
            ) >= item['quantity'], f"Demand_{item_id}"

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        solution = {
            'status': LpStatus[prob.status],
            'strip_usage': {}
        }

        for (h, p), var in strip_vars.items():
            if var.varValue and var.varValue > 0.5:
                if h not in solution['strip_usage']:
                    solution['strip_usage'][h] = []

                solution['strip_usage'][h].append({
                    'pattern_index': p,
                    'pattern': strip_patterns[h][p],
                    'quantity': int(var.varValue)
                })

        return solution

    def pack_strips_into_sheets(self, strip_usage):
        """
        Pack strips into sheets using FFD height

        Returns list of sheets with their strips
        """

        # Expand strips
        strips_to_pack = []

        for strip_height, patterns in strip_usage.items():
            for pattern_info in patterns:
                for _ in range(pattern_info['quantity']):
                    strips_to_pack.append({
                        'height': strip_height,
                        'pattern': pattern_info['pattern']
                    })

        # Sort by decreasing height
        strips_to_pack.sort(key=lambda s: s['height'], reverse=True)

        # Pack into sheets (FFD)
        sheets = []

        for strip in strips_to_pack:
            placed = False

            # Try existing sheets
            for sheet in sheets:
                if sheet['remaining_height'] >= strip['height']:
                    sheet['strips'].append(strip)
                    sheet['remaining_height'] -= strip['height']
                    placed = True
                    break

            # Need new sheet
            if not placed:
                sheets.append({
                    'strips': [strip],
                    'remaining_height': self.sheet_height - strip['height']
                })

        # Calculate utilization
        for sheet in sheets:
            used_area = 0
            for strip in sheet['strips']:
                # Calculate items in strip
                strip_used = 0
                for item_id, count in strip['pattern']['items'].items():
                    # Get item dimensions (need to look up)
                    # Simplified here
                    strip_used += count * 100  # Placeholder

                used_area += strip_used * strip['height']

            sheet['utilization'] = (used_area / (self.sheet_width * self.sheet_height) * 100)

        return sheets

    def solve(self):
        """
        Solve two-stage guillotine cutting problem

        Returns: cutting plan with sheets and patterns
        """

        print("Solving Two-Stage Guillotine Cutting...")

        # Step 1: Generate strip types
        strip_types = self.generate_strip_types()
        print(f"Strip types: {len(strip_types)}")

        # Step 2: For each strip type, generate 1D patterns
        strip_patterns = {}

        for strip_height in strip_types:
            patterns = self.solve_1d_cutting_for_strip(strip_height, self.sheet_width)
            strip_patterns[strip_height] = patterns
            print(f"Strip height {strip_height}: {len(patterns)} patterns")

        # Step 3: Solve master problem
        master_solution = self.solve_master_problem(strip_types, strip_patterns)

        if master_solution['status'] != 'Optimal':
            print(f"Warning: Status = {master_solution['status']}")

        # Step 4: Pack strips into sheets
        sheets = self.pack_strips_into_sheets(master_solution['strip_usage'])

        print(f"\nSolution: {len(sheets)} sheets needed")

        return {
            'num_sheets': len(sheets),
            'sheets': sheets,
            'strip_patterns': strip_patterns,
            'status': master_solution['status']
        }


# Example usage
def example_two_stage_guillotine():
    """Example: Two-stage guillotine cutting"""

    solver = TwoStageGuillotine(
        sheet_width=2440,
        sheet_height=1220,
        kerf=3
    )

    # Add items
    solver.add_item(800, 600, 12, 'A')
    solver.add_item(1000, 500, 10, 'B')
    solver.add_item(600, 400, 15, 'C')
    solver.add_item(1200, 300, 8, 'D')

    # Solve
    solution = solver.solve()

    print(f"\nSheets: {solution['num_sheets']}")

    return solution
```

### Method 2: Recursive Guillotine Partitioning

```python
class RecursiveGuillotinePartitioning:
    """
    Recursive Guillotine Partitioning

    Recursively subdivides rectangle with guillotine cuts
    Can represent any guillotine cutting pattern

    Uses tree structure to represent cutting plan
    """

    def __init__(self, width, height):
        """
        Initialize with rectangle dimensions

        Parameters:
        - width: rectangle width
        - height: rectangle height
        """
        self.width = width
        self.height = height
        self.root = None

    class CutNode:
        """Node in guillotine cut tree"""

        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

            # Cut information
            self.is_cut = False
            self.cut_position = None
            self.cut_horizontal = None  # True=horizontal, False=vertical

            # Children (if cut)
            self.left_child = None   # or bottom child
            self.right_child = None  # or top child

            # Item assignment (if leaf)
            self.item = None

    def make_cut(self, node, position, horizontal=True):
        """
        Make guillotine cut at node

        Parameters:
        - node: CutNode to cut
        - position: cut position (relative to node origin)
        - horizontal: True for horizontal cut, False for vertical

        Returns: (left/bottom child, right/top child)
        """

        if node.is_cut:
            raise ValueError("Node already cut")

        node.is_cut = True
        node.cut_position = position
        node.cut_horizontal = horizontal

        if horizontal:
            # Horizontal cut: divide into bottom and top
            node.left_child = self.CutNode(
                node.x, node.y,
                node.width, position
            )

            node.right_child = self.CutNode(
                node.x, node.y + position,
                node.width, node.height - position
            )

        else:
            # Vertical cut: divide into left and right
            node.left_child = self.CutNode(
                node.x, node.y,
                position, node.height
            )

            node.right_child = self.CutNode(
                node.x + position, node.y,
                node.width - position, node.height
            )

        return node.left_child, node.right_child

    def assign_item(self, node, item_id, item_width, item_height):
        """
        Assign item to a leaf node

        Parameters:
        - node: leaf node
        - item_id: item identifier
        - item_width, item_height: item dimensions
        """

        if node.is_cut:
            raise ValueError("Cannot assign item to cut node")

        if item_width > node.width or item_height > node.height:
            raise ValueError("Item doesn't fit in node")

        node.item = {
            'id': item_id,
            'width': item_width,
            'height': item_height,
            'waste_width': node.width - item_width,
            'waste_height': node.height - item_height
        }

    def generate_cutting_sequence(self, node=None):
        """
        Generate cutting sequence from tree

        Returns list of cuts in execution order (depth-first)
        """

        if node is None:
            node = self.root

        if not node.is_cut:
            return []

        cuts = []

        # Add this cut
        cuts.append({
            'position': (node.x, node.y),
            'size': (node.width, node.height),
            'cut_position': node.cut_position,
            'horizontal': node.cut_horizontal,
            'cut_line': (
                (node.x, node.y + node.cut_position,
                 node.x + node.width, node.y + node.cut_position)
                if node.cut_horizontal else
                (node.x + node.cut_position, node.y,
                 node.x + node.cut_position, node.y + node.height)
            )
        })

        # Recursively add children cuts
        if node.left_child:
            cuts.extend(self.generate_cutting_sequence(node.left_child))

        if node.right_child:
            cuts.extend(self.generate_cutting_sequence(node.right_child))

        return cuts

    def visualize_cut_tree(self, save_path=None):
        """
        Visualize guillotine cut pattern

        Shows all cuts and items
        """

        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, ax = plt.subplots(figsize=(12, 10))

        # Draw sheet boundary
        ax.add_patch(patches.Rectangle(
            (0, 0), self.width, self.height,
            fill=False, edgecolor='black', linewidth=3
        ))

        # Draw all cuts
        cuts = self.generate_cutting_sequence()

        for idx, cut in enumerate(cuts):
            x1, y1, x2, y2 = cut['cut_line']
            color = 'red' if cut['horizontal'] else 'blue'
            ax.plot([x1, x2], [y1, y2],
                   color=color, linewidth=2, alpha=0.7)

            # Label cut
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y, f"{idx+1}",
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='circle', facecolor='white'))

        # Draw items
        items = self._collect_items(self.root)

        colors = plt.cm.tab10(np.linspace(0, 1, 10))

        for idx, item_info in enumerate(items):
            node = item_info['node']
            item = item_info['item']

            color = colors[idx % 10]

            ax.add_patch(patches.Rectangle(
                (node.x, node.y),
                item['width'], item['height'],
                facecolor=color, edgecolor='black',
                linewidth=1.5, alpha=0.5
            ))

            # Label item
            cx = node.x + item['width'] / 2
            cy = node.y + item['height'] / 2
            ax.text(cx, cy, item['id'],
                   ha='center', va='center',
                   fontsize=11, fontweight='bold')

        ax.set_xlim(-50, self.width + 50)
        ax.set_ylim(-50, self.height + 50)
        ax.set_aspect('equal')
        ax.set_xlabel('Width', fontsize=12)
        ax.set_ylabel('Height', fontsize=12)
        ax.set_title('Guillotine Cutting Pattern\n'
                    'Red=Horizontal cuts, Blue=Vertical cuts',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Legend
        ax.text(0.02, 0.98, f"Total cuts: {len(cuts)}",
               transform=ax.transAxes,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def _collect_items(self, node):
        """Collect all items from tree"""

        if node is None:
            return []

        if node.item:
            return [{'node': node, 'item': node.item}]

        items = []

        if node.left_child:
            items.extend(self._collect_items(node.left_child))

        if node.right_child:
            items.extend(self._collect_items(node.right_child))

        return items


# Example usage
def example_recursive_guillotine():
    """Example: Build guillotine cut tree"""

    # Create partitioner for 2400x1200 sheet
    gp = RecursiveGuillotinePartitioning(2400, 1200)

    # Create root node
    gp.root = gp.CutNode(0, 0, 2400, 1200)

    # Make first horizontal cut at 600
    bottom, top = gp.make_cut(gp.root, 600, horizontal=True)

    # Cut bottom into two vertical sections
    left1, right1 = gp.make_cut(bottom, 1200, horizontal=False)

    # Cut top into two vertical sections
    left2, right2 = gp.make_cut(top, 800, horizontal=False)

    # Assign items to leaves
    gp.assign_item(left1, 'A', 1200, 600)
    gp.assign_item(right1, 'B', 1200, 600)
    gp.assign_item(left2, 'C', 800, 600)
    gp.assign_item(right2, 'D', 1600, 600)

    # Get cutting sequence
    cuts = gp.generate_cutting_sequence()

    print("Cutting Sequence:")
    for idx, cut in enumerate(cuts):
        direction = "Horizontal" if cut['horizontal'] else "Vertical"
        print(f"Cut {idx+1}: {direction} at position {cut['cut_position']}")

    # Visualize
    gp.visualize_cut_tree()

    return gp
```

### Method 3: Three-Stage Guillotine Algorithm

```python
class ThreeStageGuillotine:
    """
    Three-Stage Guillotine Cutting

    More flexible than two-stage

    Stage 1: Cut sheet into large sections
    Stage 2: Cut sections into strips
    Stage 3: Cut strips into items
    """

    def __init__(self, sheet_width, sheet_height):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.items = []

    def add_item(self, width, height, quantity, item_id=None):
        """Add item"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'width': width,
            'height': height,
            'quantity': quantity
        })

    def solve(self):
        """
        Solve three-stage problem

        This is more complex - simplified implementation
        """

        # Stage 1: Decide on section cuts
        # Stage 2: For each section, decide on strip cuts
        # Stage 3: For each strip, pack items

        # This requires sophisticated algorithm
        # Typically uses dynamic programming or column generation

        # Placeholder for full implementation
        pass
```

---

## Guillotine Cutting Algorithms Comparison

### Algorithm Comparison

| Algorithm | Optimality | Speed | Complexity | Best For |
|-----------|------------|-------|------------|----------|
| Two-Stage DP | Good | Fast | Medium | Standard manufacturing |
| Three-Stage | Better | Medium | High | Complex item mixes |
| Recursive Tree | Flexible | Slow | High | Custom requirements |
| Column Generation | Best | Slow | Very High | High-value materials |

---

## Practical Considerations

### Advantages of Guillotine Cuts

1. **Equipment Compatibility**
   - Most cutting equipment naturally makes guillotine cuts
   - Panel saws, guillotine shears work this way
   - Simpler toolpath programming

2. **Operational Simplicity**
   - Easier to execute
   - Fewer setup changes
   - Faster cutting process

3. **Safety**
   - Straight cuts safer than complex paths
   - Easier material handling
   - Better piece stability

### Disadvantages of Guillotine Constraint

1. **Utilization Loss**
   - Typically 5-10% lower utilization vs. non-guillotine
   - More waste due to constraint

2. **Limited Flexibility**
   - Cannot always achieve optimal packing
   - Some item combinations pack poorly

---

## Tools & Libraries

### Software

- **CutList Optimizer**: Guillotine cutting focus
- **OptiCut**: Supports guillotine constraints
- **Cutting Optimization Pro**: Guillotine modes

---

## Questions to Ask

1. Must all cuts be guillotine?
2. What cutting equipment is used?
3. Two-stage or three-stage acceptable?
4. Item dimensions and quantities?
5. Can items rotate?
6. Material cost and waste impact?

---

## Related Skills

- **2d-cutting-stock**: For general 2D cutting
- **1d-cutting-stock**: For 1D cutting in strips
- **trim-loss-minimization**: For waste reduction
- **nesting-optimization**: For non-rectangular shapes
