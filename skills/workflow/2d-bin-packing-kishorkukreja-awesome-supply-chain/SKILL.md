---
name: 2d-bin-packing
description: When the user wants to pack 2D rectangular items into bins, optimize 2D cutting patterns, or minimize material waste in 2D packing. Also use when the user mentions "2D packing," "rectangular packing," "sheet packing," "2D bin packing problem," "guillotine cutting," "two-dimensional packing," or "rectangle packing optimization." For 1D problems, see 1d-cutting-stock. For 3D problems, see 3d-bin-packing.
---

# 2D Bin Packing

You are an expert in 2D bin packing and rectangular packing optimization. Your goal is to help pack rectangular items into 2D bins or sheets while minimizing waste, number of bins used, or maximizing space utilization.

## Initial Assessment

Before solving 2D bin packing problems, understand:

1. **Problem Type**
   - Pack into fixed-size bins (minimize bins used)?
   - Pack into variable-size bins (minimize total area)?
   - Single large bin (maximize utilization)?
   - Cutting from sheets (minimize waste)?

2. **Item Characteristics**
   - How many items to pack? (10s, 100s, 1000s)
   - Item dimensions: width x height
   - Can items be rotated? (90-degree rotation allowed?)
   - Are items all different or some identical?
   - Any item priorities or grouping requirements?

3. **Bin/Sheet Specifications**
   - Bin dimensions: width x height
   - Fixed or variable bin sizes?
   - Unlimited bins or limited quantity?
   - Any margin/spacing requirements between items?

4. **Cutting Constraints**
   - Guillotine cuts only? (straight cuts across entire sheet)
   - Free-form packing allowed?
   - Maximum number of cutting stages?
   - Trim loss acceptable?

5. **Optimization Objective**
   - Minimize number of bins used?
   - Minimize total area/material cost?
   - Maximize utilization percentage?
   - Minimize cutting complexity?

---

## 2D Bin Packing Framework

### Problem Classification

**1. 2D Bin Packing Problem (2D-BPP)**
- Pack rectangles into minimum number of identical bins
- All items must be packed
- Items cannot overlap
- Items typically axis-aligned

**2. 2D Strip Packing Problem**
- Fixed width, minimize height
- Single strip (bin with infinite height)
- Minimize total height used

**3. 2D Cutting Stock Problem**
- Cut items from larger sheets
- Minimize material waste
- Often with guillotine constraints

**4. Rectangle Packing Problem**
- Pack into single large rectangle
- Maximize number of items packed
- Or maximize space utilization

**5. Two-Dimensional Knapsack**
- Items have values
- Maximize total value in fixed bin
- Items may not all fit

---

## Mathematical Formulation

### Basic 2D Bin Packing Model

**Decision Variables:**
- x_i, y_i = coordinates of item i's bottom-left corner
- b_i = bin number assigned to item i
- w_j = 1 if bin j is used, 0 otherwise
- r_i = 1 if item i is rotated, 0 otherwise

**Objective:**
Minimize ∑ w_j (minimize bins used)

**Constraints:**
1. Non-overlap: items in same bin don't overlap
2. Containment: items fit within bin boundaries
3. Assignment: each item assigned to exactly one bin
4. Rotation (optional): items can be rotated 90°

**Complexity:**
- NP-hard problem
- No polynomial-time optimal algorithm (unless P=NP)
- Requires heuristic or metaheuristic approaches

---

## Algorithms and Solution Methods

### Exact Methods

**Branch and Bound**
- Guarantees optimal solution
- Only practical for small problems (<20-30 items)
- Exponential time complexity

**Integer Programming Formulation**

```python
from pulp import *

def solve_2d_bin_packing_ip(items, bin_width, bin_height, max_bins=None):
    """
    2D Bin Packing using Integer Programming

    Parameters:
    - items: list of (width, height) tuples
    - bin_width: width of each bin
    - bin_height: height of each bin
    - max_bins: maximum number of bins to consider

    Returns optimal packing solution

    Note: Only practical for small problems (<20 items)
    """

    n = len(items)
    if max_bins is None:
        max_bins = n  # Worst case: one item per bin

    bins = range(max_bins)
    item_ids = range(n)

    # Create problem
    prob = LpProblem("2D_Bin_Packing", LpMinimize)

    # Decision variables
    # x[i,b] = x coordinate of item i in bin b
    x = LpVariable.dicts("x",
                        [(i, b) for i in item_ids for b in bins],
                        lowBound=0, upBound=bin_width, cat='Continuous')

    # y[i,b] = y coordinate of item i in bin b
    y = LpVariable.dicts("y",
                        [(i, b) for i in item_ids for b in bins],
                        lowBound=0, upBound=bin_height, cat='Continuous')

    # a[i,b] = 1 if item i assigned to bin b
    a = LpVariable.dicts("assign",
                        [(i, b) for i in item_ids for b in bins],
                        cat='Binary')

    # w[b] = 1 if bin b is used
    w = LpVariable.dicts("use_bin", bins, cat='Binary')

    # Objective: minimize number of bins
    prob += lpSum([w[b] for b in bins]), "Total_Bins"

    # Constraints

    # 1. Each item assigned to exactly one bin
    for i in item_ids:
        prob += lpSum([a[i,b] for b in bins]) == 1, f"Assign_{i}"

    # 2. Item fits within bin boundaries
    for i in item_ids:
        for b in bins:
            prob += x[i,b] + items[i][0] <= bin_width + (1 - a[i,b]) * bin_width, \
                    f"Fit_Width_{i}_{b}"
            prob += y[i,b] + items[i][1] <= bin_height + (1 - a[i,b]) * bin_height, \
                    f"Fit_Height_{i}_{b}"

    # 3. Bin is used if any item assigned to it
    for b in bins:
        for i in item_ids:
            prob += a[i,b] <= w[b], f"Bin_Used_{i}_{b}"

    # 4. Non-overlapping constraints (simplified - full version more complex)
    # This is a simplified model; full non-overlap requires additional binary variables

    # Solve
    status = prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))

    if LpStatus[status] != 'Optimal':
        return None

    # Extract solution
    solution = {
        'num_bins': int(value(prob.objective)),
        'bins': []
    }

    for b in bins:
        if w[b].varValue > 0.5:
            bin_items = []
            for i in item_ids:
                if a[i,b].varValue > 0.5:
                    bin_items.append({
                        'item_id': i,
                        'x': x[i,b].varValue,
                        'y': y[i,b].varValue,
                        'width': items[i][0],
                        'height': items[i][1]
                    })
            solution['bins'].append(bin_items)

    return solution
```

### Heuristic Methods

**First Fit Decreasing Height (FFDH)**
- Sort items by decreasing height
- Pack items left-to-right on shelves
- Start new shelf when item doesn't fit

```python
def first_fit_decreasing_height(items, bin_width, bin_height):
    """
    First Fit Decreasing Height (FFDH) Algorithm

    Classic shelf-based packing heuristic
    - Sorts items by decreasing height
    - Packs items left-to-right on shelves
    - Opens new shelf/bin when needed

    Parameters:
    - items: list of (width, height, item_id) tuples
    - bin_width: bin width
    - bin_height: bin height

    Returns packing solution
    """

    # Sort by decreasing height, then decreasing width
    sorted_items = sorted(items, key=lambda x: (x[1], x[0]), reverse=True)

    bins = []

    for item_width, item_height, item_id in sorted_items:
        placed = False

        # Try to place in existing bins
        for bin_idx, bin_data in enumerate(bins):
            shelves = bin_data['shelves']

            # Try each shelf
            for shelf in shelves:
                if (shelf['remaining_width'] >= item_width and
                    shelf['height'] >= item_height):
                    # Place on this shelf
                    x = bin_width - shelf['remaining_width']
                    y = shelf['y']

                    bin_data['items'].append({
                        'id': item_id,
                        'x': x,
                        'y': y,
                        'width': item_width,
                        'height': item_height
                    })

                    shelf['remaining_width'] -= item_width
                    placed = True
                    break

            if placed:
                break

            # Try to create new shelf in this bin
            if not placed:
                current_height = sum(s['height'] for s in shelves)
                if current_height + item_height <= bin_height:
                    # Create new shelf
                    new_shelf = {
                        'y': current_height,
                        'height': item_height,
                        'remaining_width': bin_width - item_width
                    }
                    shelves.append(new_shelf)

                    bin_data['items'].append({
                        'id': item_id,
                        'x': 0,
                        'y': current_height,
                        'width': item_width,
                        'height': item_height
                    })
                    placed = True
                    break

        # Need new bin
        if not placed:
            new_bin = {
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': 0,
                    'width': item_width,
                    'height': item_height
                }],
                'shelves': [{
                    'y': 0,
                    'height': item_height,
                    'remaining_width': bin_width - item_width
                }]
            }
            bins.append(new_bin)

    return {
        'num_bins': len(bins),
        'bins': bins,
        'utilization': calculate_utilization(bins, bin_width, bin_height)
    }

def calculate_utilization(bins, bin_width, bin_height):
    """Calculate space utilization percentage"""
    total_item_area = 0
    for bin_data in bins:
        for item in bin_data['items']:
            total_item_area += item['width'] * item['height']

    total_bin_area = len(bins) * bin_width * bin_height
    return (total_item_area / total_bin_area * 100) if total_bin_area > 0 else 0
```

**Next Fit Decreasing Height (NFDH)**
- Similar to FFDH but only considers current bin
- Simpler but less efficient

**Best Fit Decreasing Height (BFDH)**
- Tries to find best shelf for each item
- Better utilization than FFDH

```python
def best_fit_decreasing_height(items, bin_width, bin_height):
    """
    Best Fit Decreasing Height Algorithm

    Finds the shelf with minimum remaining space that fits the item
    """

    sorted_items = sorted(items, key=lambda x: (x[1], x[0]), reverse=True)
    bins = []

    for item_width, item_height, item_id in sorted_items:
        best_bin = None
        best_shelf = None
        min_waste = float('inf')

        # Find best fitting shelf
        for bin_idx, bin_data in enumerate(bins):
            for shelf_idx, shelf in enumerate(bin_data['shelves']):
                if (shelf['remaining_width'] >= item_width and
                    shelf['height'] >= item_height):
                    waste = shelf['remaining_width'] - item_width
                    if waste < min_waste:
                        min_waste = waste
                        best_bin = bin_idx
                        best_shelf = shelf_idx

        if best_bin is not None:
            # Place on best shelf
            shelf = bins[best_bin]['shelves'][best_shelf]
            x = bin_width - shelf['remaining_width']
            y = shelf['y']

            bins[best_bin]['items'].append({
                'id': item_id,
                'x': x,
                'y': y,
                'width': item_width,
                'height': item_height
            })

            shelf['remaining_width'] -= item_width
        else:
            # Try to create new shelf or new bin
            placed = False
            for bin_idx, bin_data in enumerate(bins):
                shelves = bin_data['shelves']
                current_height = sum(s['height'] for s in shelves)

                if current_height + item_height <= bin_height:
                    new_shelf = {
                        'y': current_height,
                        'height': item_height,
                        'remaining_width': bin_width - item_width
                    }
                    shelves.append(new_shelf)

                    bin_data['items'].append({
                        'id': item_id,
                        'x': 0,
                        'y': current_height,
                        'width': item_width,
                        'height': item_height
                    })
                    placed = True
                    break

            if not placed:
                # Create new bin
                new_bin = {
                    'items': [{
                        'id': item_id,
                        'x': 0,
                        'y': 0,
                        'width': item_width,
                        'height': item_height
                    }],
                    'shelves': [{
                        'y': 0,
                        'height': item_height,
                        'remaining_width': bin_width - item_width
                    }]
                }
                bins.append(new_bin)

    return {
        'num_bins': len(bins),
        'bins': bins,
        'utilization': calculate_utilization(bins, bin_width, bin_height)
    }
```

**Guillotine Algorithm**
- Recursive subdivision using guillotine cuts
- Each cut goes completely across rectangle
- Common in manufacturing/cutting applications

```python
class Rectangle:
    """Rectangle representation for guillotine algorithm"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_id = None

    def area(self):
        return self.width * self.height

    def fits(self, item_width, item_height):
        return self.width >= item_width and self.height >= item_height

def guillotine_algorithm(items, bin_width, bin_height, split_rule='shorter_leftover'):
    """
    Guillotine Algorithm with Free Rectangles

    Maintains list of free rectangles
    Places items and splits rectangles with guillotine cuts

    Parameters:
    - items: list of (width, height, id) tuples
    - bin_width, bin_height: bin dimensions
    - split_rule: 'shorter_leftover' or 'longer_leftover'

    Returns packing solution
    """

    # Sort items by area (largest first)
    sorted_items = sorted(items, key=lambda x: x[0] * x[1], reverse=True)

    bins = []

    for item_width, item_height, item_id in sorted_items:
        placed = False

        # Try rotation
        rotations = [(item_width, item_height, False)]
        rotations.append((item_height, item_width, True))  # 90-degree rotation

        for try_width, try_height, rotated in rotations:
            if placed:
                break

            # Try existing bins
            for bin_data in bins:
                free_rects = bin_data['free_rectangles']

                # Find best free rectangle
                best_rect_idx = None
                best_rect_score = float('inf')

                for idx, rect in enumerate(free_rects):
                    if rect.fits(try_width, try_height):
                        # Score: prefer smaller remaining area
                        score = rect.area() - (try_width * try_height)
                        if score < best_rect_score:
                            best_rect_score = score
                            best_rect_idx = idx

                if best_rect_idx is not None:
                    rect = free_rects.pop(best_rect_idx)

                    # Place item
                    bin_data['items'].append({
                        'id': item_id,
                        'x': rect.x,
                        'y': rect.y,
                        'width': try_width,
                        'height': try_height,
                        'rotated': rotated
                    })

                    # Split rectangle with guillotine cut
                    new_rects = split_rectangle(rect, try_width, try_height, split_rule)
                    free_rects.extend(new_rects)

                    placed = True
                    break

            if placed:
                break

        # Create new bin if not placed
        if not placed:
            new_bin = {
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': 0,
                    'width': item_width,
                    'height': item_height,
                    'rotated': False
                }],
                'free_rectangles': []
            }

            # Add remaining free rectangles from split
            initial_rect = Rectangle(0, 0, bin_width, bin_height)
            new_rects = split_rectangle(initial_rect, item_width, item_height, split_rule)
            new_bin['free_rectangles'] = new_rects

            bins.append(new_bin)

    return {
        'num_bins': len(bins),
        'bins': bins,
        'utilization': calculate_utilization(bins, bin_width, bin_height)
    }

def split_rectangle(rect, used_width, used_height, split_rule):
    """
    Split rectangle after placing item

    Creates two new free rectangles using guillotine cut
    """

    new_rects = []

    remaining_width = rect.width - used_width
    remaining_height = rect.height - used_height

    if split_rule == 'shorter_leftover':
        # Horizontal cut if remaining width is shorter
        if remaining_width <= remaining_height:
            # Horizontal cut
            if remaining_width > 0:
                new_rects.append(Rectangle(
                    rect.x + used_width, rect.y,
                    remaining_width, rect.height
                ))
            if remaining_height > 0:
                new_rects.append(Rectangle(
                    rect.x, rect.y + used_height,
                    used_width, remaining_height
                ))
        else:
            # Vertical cut
            if remaining_height > 0:
                new_rects.append(Rectangle(
                    rect.x, rect.y + used_height,
                    rect.width, remaining_height
                ))
            if remaining_width > 0:
                new_rects.append(Rectangle(
                    rect.x + used_width, rect.y,
                    remaining_width, used_height
                ))

    return new_rects
```

**Maximal Rectangles Algorithm**
- Maintains list of all maximal free rectangles
- More complex but better utilization
- No guillotine constraint

```python
def maximal_rectangles_algorithm(items, bin_width, bin_height):
    """
    Maximal Rectangles Algorithm

    More sophisticated than guillotine - maintains all maximal free rectangles
    No guillotine constraint, allowing better packing

    This allows more flexible packing patterns
    """

    sorted_items = sorted(items, key=lambda x: x[0] * x[1], reverse=True)
    bins = []

    for item_width, item_height, item_id in sorted_items:
        placed = False

        # Try both orientations
        for try_width, try_height, rotated in [(item_width, item_height, False),
                                                 (item_height, item_width, True)]:
            if placed:
                break

            # Try existing bins
            for bin_data in bins:
                free_rects = bin_data['free_rectangles']

                # Find best free rectangle using Best Area Fit
                best_idx = None
                best_score = float('inf')
                best_x, best_y = 0, 0

                for idx, rect in enumerate(free_rects):
                    if rect.width >= try_width and rect.height >= try_height:
                        # Score: prefer tightest fit
                        leftover_x = rect.width - try_width
                        leftover_y = rect.height - try_height
                        score = min(leftover_x, leftover_y)

                        if score < best_score:
                            best_score = score
                            best_idx = idx
                            best_x = rect.x
                            best_y = rect.y

                if best_idx is not None:
                    # Place item
                    bin_data['items'].append({
                        'id': item_id,
                        'x': best_x,
                        'y': best_y,
                        'width': try_width,
                        'height': try_height,
                        'rotated': rotated
                    })

                    # Update free rectangles
                    placed_rect = Rectangle(best_x, best_y, try_width, try_height)
                    update_maximal_rectangles(free_rects, placed_rect)

                    placed = True
                    break

            if placed:
                break

        if not placed:
            # Create new bin
            initial_rect = Rectangle(0, 0, bin_width, bin_height)

            new_bin = {
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': 0,
                    'width': item_width,
                    'height': item_height,
                    'rotated': False
                }],
                'free_rectangles': [initial_rect]
            }

            placed_rect = Rectangle(0, 0, item_width, item_height)
            update_maximal_rectangles(new_bin['free_rectangles'], placed_rect)

            bins.append(new_bin)

    return {
        'num_bins': len(bins),
        'bins': bins,
        'utilization': calculate_utilization(bins, bin_width, bin_height)
    }

def update_maximal_rectangles(free_rects, placed_rect):
    """
    Update list of maximal free rectangles after placing an item

    Split intersecting rectangles and remove non-maximal ones
    """

    new_rects = []

    for rect in free_rects[:]:
        if rectangles_intersect(rect, placed_rect):
            # Split this rectangle
            splits = split_intersecting_rectangle(rect, placed_rect)
            new_rects.extend(splits)
        else:
            new_rects.append(rect)

    # Remove non-maximal rectangles
    free_rects.clear()
    for rect in new_rects:
        is_maximal = True
        for other in new_rects:
            if rect != other and contains(other, rect):
                is_maximal = False
                break
        if is_maximal:
            free_rects.append(rect)

def rectangles_intersect(rect1, rect2):
    """Check if two rectangles intersect"""
    return not (rect1.x + rect1.width <= rect2.x or
                rect2.x + rect2.width <= rect1.x or
                rect1.y + rect1.height <= rect2.y or
                rect2.y + rect2.height <= rect1.y)

def contains(outer, inner):
    """Check if outer rectangle contains inner rectangle"""
    return (outer.x <= inner.x and
            outer.y <= inner.y and
            outer.x + outer.width >= inner.x + inner.width and
            outer.y + outer.height >= inner.y + inner.height)

def split_intersecting_rectangle(rect, placed):
    """Split rectangle by removing placed rectangle area"""
    splits = []

    # Create up to 4 new rectangles around the placed item

    # Left piece
    if placed.x > rect.x:
        splits.append(Rectangle(
            rect.x, rect.y,
            placed.x - rect.x, rect.height
        ))

    # Right piece
    if placed.x + placed.width < rect.x + rect.width:
        splits.append(Rectangle(
            placed.x + placed.width, rect.y,
            rect.x + rect.width - (placed.x + placed.width), rect.height
        ))

    # Bottom piece
    if placed.y > rect.y:
        splits.append(Rectangle(
            rect.x, rect.y,
            rect.width, placed.y - rect.y
        ))

    # Top piece
    if placed.y + placed.height < rect.y + rect.height:
        splits.append(Rectangle(
            rect.x, placed.y + placed.height,
            rect.width, rect.y + rect.height - (placed.y + placed.height)
        ))

    return splits
```

### Metaheuristic Methods

**Genetic Algorithm for 2D Packing**

```python
import random
import numpy as np

class GeneticAlgorithm2DBinPacking:
    """
    Genetic Algorithm for 2D Bin Packing

    Chromosome: permutation of items (packing order)
    Fitness: number of bins used (lower is better)
    """

    def __init__(self, items, bin_width, bin_height,
                 population_size=100, generations=200,
                 mutation_rate=0.1, crossover_rate=0.8):
        self.items = items
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.n_items = len(items)
        self.best_solution = None
        self.best_fitness = float('inf')

    def create_chromosome(self):
        """Create random chromosome (item permutation)"""
        return list(np.random.permutation(self.n_items))

    def decode_chromosome(self, chromosome):
        """
        Decode chromosome to packing solution
        Uses FFDH to pack items in the order specified by chromosome
        """
        ordered_items = [self.items[i] for i in chromosome]
        result = first_fit_decreasing_height(
            ordered_items, self.bin_width, self.bin_height
        )
        return result

    def fitness(self, chromosome):
        """
        Fitness function: number of bins used
        Lower is better
        """
        solution = self.decode_chromosome(chromosome)
        return solution['num_bins']

    def crossover(self, parent1, parent2):
        """
        Order Crossover (OX) for permutations
        """
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        size = len(parent1)

        # Select crossover points
        cx_point1 = random.randint(0, size - 2)
        cx_point2 = random.randint(cx_point1 + 1, size - 1)

        # Create offspring
        child1 = [-1] * size
        child2 = [-1] * size

        # Copy segments
        child1[cx_point1:cx_point2] = parent1[cx_point1:cx_point2]
        child2[cx_point1:cx_point2] = parent2[cx_point1:cx_point2]

        # Fill remaining positions
        self._fill_offspring(child1, parent2, cx_point2)
        self._fill_offspring(child2, parent1, cx_point2)

        return child1, child2

    def _fill_offspring(self, child, parent, start_pos):
        """Fill remaining positions in offspring"""
        child_set = set([x for x in child if x != -1])
        pos = start_pos

        for item in parent[start_pos:] + parent[:start_pos]:
            if item not in child_set:
                while child[pos % len(child)] != -1:
                    pos += 1
                child[pos % len(child)] = item
                child_set.add(item)

    def mutate(self, chromosome):
        """
        Swap mutation: swap two random positions
        """
        if random.random() < self.mutation_rate:
            pos1, pos2 = random.sample(range(len(chromosome)), 2)
            chromosome[pos1], chromosome[pos2] = chromosome[pos2], chromosome[pos1]
        return chromosome

    def tournament_selection(self, population, fitnesses, tournament_size=3):
        """Tournament selection"""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitnesses.index(min(tournament_fitnesses))]
        return population[winner_idx]

    def solve(self):
        """
        Run genetic algorithm
        """
        # Initialize population
        population = [self.create_chromosome() for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluate fitness
            fitnesses = [self.fitness(chrom) for chrom in population]

            # Track best solution
            min_fitness_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_fitness_idx] < self.best_fitness:
                self.best_fitness = fitnesses[min_fitness_idx]
                self.best_solution = self.decode_chromosome(population[min_fitness_idx])
                print(f"Generation {generation}: Best = {self.best_fitness} bins")

            # Create new population
            new_population = []

            # Elitism: keep best solution
            new_population.append(population[min_fitness_idx])

            # Generate offspring
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)

                # Crossover
                child1, child2 = self.crossover(parent1, parent2)

                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        return self.best_solution

# Usage example
def example_genetic_algorithm():
    """Example usage of genetic algorithm"""

    # Generate random items
    np.random.seed(42)
    n_items = 30
    items = [(random.randint(10, 50), random.randint(10, 50), i)
             for i in range(n_items)]

    bin_width = 100
    bin_height = 100

    # Run genetic algorithm
    ga = GeneticAlgorithm2DBinPacking(
        items, bin_width, bin_height,
        population_size=50,
        generations=100
    )

    solution = ga.solve()

    print(f"\nFinal Solution:")
    print(f"Number of bins: {solution['num_bins']}")
    print(f"Utilization: {solution['utilization']:.2f}%")

    return solution
```

**Simulated Annealing**

```python
import math
import random

def simulated_annealing_2d_packing(items, bin_width, bin_height,
                                    initial_temp=1000, cooling_rate=0.995,
                                    iterations=10000):
    """
    Simulated Annealing for 2D Bin Packing

    Neighborhood: swap two items in packing order
    """

    # Initial solution: random order + FFDH
    current_order = list(range(len(items)))
    random.shuffle(current_order)

    current_items = [items[i] for i in current_order]
    current_solution = first_fit_decreasing_height(
        current_items, bin_width, bin_height
    )
    current_cost = current_solution['num_bins']

    best_order = current_order.copy()
    best_solution = current_solution
    best_cost = current_cost

    temperature = initial_temp

    for iteration in range(iterations):
        # Generate neighbor: swap two items
        neighbor_order = current_order.copy()
        i, j = random.sample(range(len(items)), 2)
        neighbor_order[i], neighbor_order[j] = neighbor_order[j], neighbor_order[i]

        # Evaluate neighbor
        neighbor_items = [items[idx] for idx in neighbor_order]
        neighbor_solution = first_fit_decreasing_height(
            neighbor_items, bin_width, bin_height
        )
        neighbor_cost = neighbor_solution['num_bins']

        # Acceptance criterion
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_order = neighbor_order
            current_solution = neighbor_solution
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_order = current_order.copy()
                best_solution = current_solution
                best_cost = current_cost
                print(f"Iteration {iteration}: New best = {best_cost} bins")

        # Cool down
        temperature *= cooling_rate

    return best_solution
```

---

## Complete 2D Bin Packing Solver

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class TwoDimensionalBinPacker:
    """
    Comprehensive 2D Bin Packing Solver

    Supports multiple algorithms and visualization
    """

    def __init__(self, bin_width, bin_height):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.items = []
        self.solution = None

    def add_item(self, width, height, item_id=None):
        """Add item to pack"""
        if item_id is None:
            item_id = len(self.items)
        self.items.append((width, height, item_id))

    def add_items(self, items_list):
        """Add multiple items: list of (width, height) tuples"""
        for width, height in items_list:
            self.add_item(width, height)

    def solve(self, algorithm='ffdh', **kwargs):
        """
        Solve using specified algorithm

        Algorithms:
        - 'ffdh': First Fit Decreasing Height
        - 'bfdh': Best Fit Decreasing Height
        - 'guillotine': Guillotine algorithm
        - 'maxrects': Maximal Rectangles
        - 'genetic': Genetic Algorithm
        - 'simulated_annealing': Simulated Annealing
        """

        if algorithm == 'ffdh':
            self.solution = first_fit_decreasing_height(
                self.items, self.bin_width, self.bin_height
            )

        elif algorithm == 'bfdh':
            self.solution = best_fit_decreasing_height(
                self.items, self.bin_width, self.bin_height
            )

        elif algorithm == 'guillotine':
            self.solution = guillotine_algorithm(
                self.items, self.bin_width, self.bin_height
            )

        elif algorithm == 'maxrects':
            self.solution = maximal_rectangles_algorithm(
                self.items, self.bin_width, self.bin_height
            )

        elif algorithm == 'genetic':
            ga = GeneticAlgorithm2DBinPacking(
                self.items, self.bin_width, self.bin_height,
                **kwargs
            )
            self.solution = ga.solve()

        elif algorithm == 'simulated_annealing':
            self.solution = simulated_annealing_2d_packing(
                self.items, self.bin_width, self.bin_height,
                **kwargs
            )

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return self.solution

    def visualize(self, bin_indices=None, save_path=None):
        """
        Visualize packing solution

        Parameters:
        - bin_indices: list of bin indices to visualize (None = all)
        - save_path: path to save figure
        """

        if self.solution is None:
            raise ValueError("No solution to visualize. Run solve() first.")

        bins = self.solution['bins']

        if bin_indices is None:
            bin_indices = range(len(bins))

        n_bins = len(bin_indices)
        cols = min(3, n_bins)
        rows = (n_bins + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        if n_bins == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if n_bins > 1 else [axes]

        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for idx, bin_idx in enumerate(bin_indices):
            ax = axes[idx]
            bin_data = bins[bin_idx]

            # Draw bin boundary
            ax.add_patch(patches.Rectangle(
                (0, 0), self.bin_width, self.bin_height,
                fill=False, edgecolor='black', linewidth=2
            ))

            # Draw items
            for item_idx, item in enumerate(bin_data['items']):
                color = colors[item['id'] % 20]

                rect = patches.Rectangle(
                    (item['x'], item['y']),
                    item['width'], item['height'],
                    facecolor=color, edgecolor='black',
                    linewidth=1, alpha=0.7
                )
                ax.add_patch(rect)

                # Add item ID label
                cx = item['x'] + item['width'] / 2
                cy = item['y'] + item['height'] / 2
                ax.text(cx, cy, str(item['id']),
                       ha='center', va='center',
                       fontsize=8, fontweight='bold')

            ax.set_xlim(0, self.bin_width)
            ax.set_ylim(0, self.bin_height)
            ax.set_aspect('equal')
            ax.set_title(f'Bin {bin_idx + 1}')
            ax.set_xlabel('Width')
            ax.set_ylabel('Height')
            ax.grid(True, alpha=0.3)

        # Hide empty subplots
        for idx in range(len(bin_indices), len(axes)):
            axes[idx].axis('off')

        plt.suptitle(
            f'2D Bin Packing Solution\n'
            f'Bins Used: {self.solution["num_bins"]} | '
            f'Utilization: {self.solution["utilization"]:.1f}%',
            fontsize=14, fontweight='bold'
        )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def get_statistics(self):
        """Get detailed statistics about the solution"""

        if self.solution is None:
            return None

        total_item_area = sum(w * h for w, h, _ in self.items)
        total_bin_area = self.solution['num_bins'] * self.bin_width * self.bin_height

        stats = {
            'num_items': len(self.items),
            'num_bins': self.solution['num_bins'],
            'bin_size': (self.bin_width, self.bin_height),
            'total_item_area': total_item_area,
            'total_bin_area': total_bin_area,
            'utilization': self.solution['utilization'],
            'waste_percentage': 100 - self.solution['utilization'],
            'bins': []
        }

        for bin_idx, bin_data in enumerate(self.solution['bins']):
            bin_item_area = sum(
                item['width'] * item['height']
                for item in bin_data['items']
            )
            bin_area = self.bin_width * self.bin_height

            stats['bins'].append({
                'bin_id': bin_idx,
                'num_items': len(bin_data['items']),
                'used_area': bin_item_area,
                'total_area': bin_area,
                'utilization': (bin_item_area / bin_area * 100)
            })

        return stats

    def print_solution(self):
        """Print solution summary"""

        if self.solution is None:
            print("No solution available.")
            return

        stats = self.get_statistics()

        print("=" * 60)
        print("2D BIN PACKING SOLUTION")
        print("=" * 60)
        print(f"Items to pack: {stats['num_items']}")
        print(f"Bin dimensions: {stats['bin_size'][0]} x {stats['bin_size'][1]}")
        print(f"Bins used: {stats['num_bins']}")
        print(f"Overall utilization: {stats['utilization']:.2f}%")
        print(f"Waste percentage: {stats['waste_percentage']:.2f}%")
        print()

        print("Bin Details:")
        print("-" * 60)
        for bin_stat in stats['bins']:
            print(f"Bin {bin_stat['bin_id'] + 1}: "
                  f"{bin_stat['num_items']} items, "
                  f"{bin_stat['utilization']:.1f}% utilization")


# Example usage
if __name__ == "__main__":
    # Create packer
    packer = TwoDimensionalBinPacker(bin_width=100, bin_height=100)

    # Add items
    np.random.seed(42)
    items = [
        (30, 40), (25, 35), (50, 20), (40, 30),
        (20, 25), (35, 45), (15, 30), (25, 20),
        (40, 40), (30, 30), (20, 40), (35, 25),
        (45, 35), (25, 25), (30, 35), (20, 30)
    ]
    packer.add_items(items)

    # Solve using different algorithms
    print("Testing FFDH algorithm:")
    solution_ffdh = packer.solve(algorithm='ffdh')
    packer.print_solution()

    print("\nTesting Guillotine algorithm:")
    solution_guillotine = packer.solve(algorithm='guillotine')
    packer.print_solution()

    # Visualize
    packer.visualize()
```

---

## Tools & Libraries

### Python Libraries

**rectpack**
```python
from rectpack import newPacker

def pack_with_rectpack(items, bin_width, bin_height):
    """Use rectpack library for 2D packing"""
    packer = newPacker()

    # Add bins
    for i in range(len(items)):  # Add enough bins
        packer.add_bin(bin_width, bin_height)

    # Add items
    for i, (w, h, item_id) in enumerate(items):
        packer.add_rect(w, h, rid=item_id)

    # Pack
    packer.pack()

    # Extract results
    bins_used = len([b for b in packer if b])

    return {
        'num_bins': bins_used,
        'packer': packer
    }
```

**binpack** - Simple 1D/2D bin packing

**py2dbp** - 2D bin packing algorithms

**OR-Tools** - Google's optimization library

### Commercial Software

- **CutLogic 2D**: Professional cutting optimization
- **Cutting Optimization Pro**: Cutting and nesting
- **OptiCut**: Sheet optimization software
- **MaxCut**: Cutting stock optimization

---

## Common Challenges & Solutions

### Challenge: Items Don't Fit Efficiently

**Problem:**
- Low utilization (<70%)
- Too many bins used
- Odd-shaped gaps

**Solutions:**
- Allow 90-degree rotation
- Try different sorting strategies
- Use metaheuristic algorithms (GA, SA)
- Combine small items strategically
- Consider pre-grouping similar sizes

### Challenge: Guillotine Constraint Too Restrictive

**Problem:**
- Guillotine cuts waste space
- Need more flexible packing

**Solutions:**
- Use maximal rectangles algorithm
- Allow limited non-guillotine patterns
- Multi-stage cutting approach
- Optimize stage sequence

### Challenge: Real-Time Packing Needed

**Problem:**
- Items arrive dynamically
- Need fast solution
- Can't repack already placed items

**Solutions:**
- Use fast online algorithms (FFDH, NFDH)
- Reserve space for expected items
- Periodic re-optimization windows
- Hybrid online/offline approach

### Challenge: Many Small Items

**Problem:**
- Thousands of tiny items
- Combinatorial explosion
- Slow computation

**Solutions:**
- Pre-cluster similar items
- Use hierarchical approach
- Limit search time with time-based stopping
- Parallel processing

---

## Output Format

### 2D Bin Packing Report

**Executive Summary:**
- Items packed: 150
- Bins used: 12 sheets (100cm x 100cm each)
- Utilization: 87.3%
- Waste: 12.7%
- Algorithm: Guillotine with GA optimization

**Packing Details:**

| Bin | Items | Used Area | Utilization | Waste |
|-----|-------|-----------|-------------|-------|
| 1 | 15 | 8,750 cm² | 87.5% | 12.5% |
| 2 | 13 | 9,100 cm² | 91.0% | 9.0% |
| 3 | 14 | 8,450 cm² | 84.5% | 15.5% |

**Cutting Pattern Example (Bin 1):**
```
+------------------+
|  A   |  B  | C  |
|------+-----+----|
|  D   | E  F|  G |
|------+-----+----|
|  H   |  I  |  J |
+------------------+
```

**Item List:**

| Item ID | Width | Height | Bin | Position (x,y) | Rotated |
|---------|-------|--------|-----|----------------|---------|
| A001 | 40 | 30 | 1 | (0, 0) | No |
| A002 | 25 | 30 | 1 | (40, 0) | No |
| A003 | 20 | 30 | 1 | (65, 0) | Yes |

**Cost Analysis:**
- Material cost per sheet: $50
- Total material cost: $600
- Waste cost: $76 (12.7%)
- Potential savings with perfect packing: $76

---

## Questions to Ask

If you need more context:
1. What are the bin/sheet dimensions?
2. How many items need to be packed? What are their sizes?
3. Can items be rotated 90 degrees?
4. Are there guillotine cutting constraints?
5. What's the optimization goal? (minimize bins, minimize waste, maximize value)
6. Are there any spacing requirements between items?
7. Do items have priorities or must-pack requirements?
8. Is this a one-time problem or recurring production?

---

## Related Skills

- **1d-cutting-stock**: For one-dimensional cutting problems
- **3d-bin-packing**: For three-dimensional packing
- **pallet-loading**: For pallet loading optimization
- **container-loading-optimization**: For container packing
- **strip-packing**: For strip packing problems
- **guillotine-cutting**: For guillotine cutting constraints
- **nesting-optimization**: For irregular shape nesting
- **knapsack-problems**: For value-based packing
