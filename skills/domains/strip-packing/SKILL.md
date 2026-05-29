---
name: strip-packing
description: When the user wants to solve strip packing problems, pack items into fixed-width strips, or minimize packing height. Also use when the user mentions "strip packing," "cutting stock with fixed width," "ribbon packing," "shelf packing," "minimize height packing," or "2D strip packing problem." For general 2D packing, see 2d-bin-packing. For 3D packing, see 3d-bin-packing.
---

# Strip Packing

You are an expert in strip packing optimization. Your goal is to help pack rectangular items into a strip of fixed width while minimizing the total height used, which is common in manufacturing, printing, fabric cutting, and material utilization problems.

## Initial Assessment

Before solving strip packing problems, understand:

1. **Strip Specifications**
   - Strip width? (fixed dimension)
   - Maximum height allowed? (or unlimited)
   - Strip material and cost structure?
   - Single strip or multiple strips?

2. **Items to Pack**
   - How many rectangles to pack?
   - Item dimensions (width x height)?
   - Can items be rotated 90 degrees?
   - All items must be packed?
   - Item priorities or packing sequence?

3. **Packing Constraints**
   - Guillotine cuts only? (straight cuts across strip)
   - Free-form packing allowed?
   - Minimum spacing between items?
   - Items must be axis-aligned?

4. **Optimization Goal**
   - Minimize total height (most common)?
   - Minimize waste percentage?
   - Minimize number of strips used?
   - Balance between height and cutting complexity?

---

## Strip Packing Framework

### Problem Definition

**Strip Packing Problem (SPP)**
- Given: Rectangle items and strip of fixed width W
- Find: Arrangement minimizing total height H
- Constraints: No overlapping, items within strip bounds
- Orientation: Items can typically be rotated 90°

**Key Difference from Bin Packing:**
- Bin packing: minimize number of bins (both dimensions fixed)
- Strip packing: minimize height (width fixed, height variable)

### Problem Variants

**1. Guillotine Strip Packing**
- All cuts must be guillotine cuts
- Simplifies cutting process
- May sacrifice some efficiency
- Common in manufacturing

**2. Non-Guillotine Strip Packing**
- Free-form packing allowed
- Better space utilization
- More complex cutting patterns
- May require CNC equipment

**3. Multiple Strip Packing**
- Use minimum number of strips
- Each strip has fixed width and max height
- Hybrid between strip packing and bin packing

**4. Online Strip Packing**
- Items arrive sequentially
- Pack without knowing future items
- Cannot rearrange previously placed items
- Real-time manufacturing scenarios

---

## Mathematical Formulation

### Basic Strip Packing Model

**Decision Variables:**
- x_i = x-coordinate of item i's bottom-left corner
- y_i = y-coordinate of item i's bottom-left corner
- r_i ∈ {0, 1} = rotation of item i (0=original, 1=rotated 90°)
- H = total height of packing

**Objective:**
Minimize H

**Constraints:**
1. **Within strip bounds:**
   - 0 ≤ x_i ≤ W - width_i for all i
   - 0 ≤ y_i for all i

2. **No overlap:**
   - For all pairs (i, j): items don't overlap

3. **Height constraint:**
   - y_i + height_i ≤ H for all i

**Complexity:**
- NP-hard problem
- Harder than 2D bin packing
- No polynomial-time optimal algorithm

---

## Algorithms and Solution Methods

### Shelf-Based Algorithms

**Next Fit Decreasing Height (NFDH)**

```python
def next_fit_decreasing_height(items, strip_width):
    """
    Next Fit Decreasing Height Algorithm

    Simple shelf-based approach:
    1. Sort items by decreasing height
    2. Pack items left-to-right on shelves
    3. Start new shelf when item doesn't fit width

    Parameters:
    - items: list of (width, height, item_id) tuples
    - strip_width: fixed width of strip

    Returns: packing with minimized height
    """

    # Sort by decreasing height
    sorted_items = sorted(items, key=lambda x: x[1], reverse=True)

    shelves = []
    current_shelf = None

    for width, height, item_id in sorted_items:
        # Check if item fits on current shelf
        if current_shelf is None or current_shelf['remaining_width'] < width:
            # Start new shelf
            if current_shelf is not None:
                shelves.append(current_shelf)

            current_shelf = {
                'y': sum(s['height'] for s in shelves),
                'height': height,
                'remaining_width': strip_width - width,
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': sum(s['height'] for s in shelves),
                    'width': width,
                    'height': height
                }]
            }
        else:
            # Add to current shelf
            x = strip_width - current_shelf['remaining_width']
            current_shelf['items'].append({
                'id': item_id,
                'x': x,
                'y': current_shelf['y'],
                'width': width,
                'height': height
            })
            current_shelf['remaining_width'] -= width

    # Add last shelf
    if current_shelf is not None:
        shelves.append(current_shelf)

    # Calculate total height
    total_height = sum(s['height'] for s in shelves)

    # Collect all items
    packed_items = []
    for shelf in shelves:
        packed_items.extend(shelf['items'])

    return {
        'height': total_height,
        'width': strip_width,
        'shelves': shelves,
        'items': packed_items,
        'utilization': calculate_utilization(packed_items, strip_width, total_height)
    }

def calculate_utilization(items, width, height):
    """Calculate space utilization percentage"""
    item_area = sum(item['width'] * item['height'] for item in items)
    strip_area = width * height
    return (item_area / strip_area * 100) if strip_area > 0 else 0

# Example
items = [
    (20, 30, 'A'), (15, 25, 'B'), (25, 35, 'C'),
    (18, 28, 'D'), (22, 30, 'E'), (12, 20, 'F')
]
strip_width = 50

result = next_fit_decreasing_height(items, strip_width)
print(f"Strip height: {result['height']}")
print(f"Utilization: {result['utilization']:.1f}%")
```

**First Fit Decreasing Height (FFDH)**

```python
def first_fit_decreasing_height(items, strip_width):
    """
    First Fit Decreasing Height Algorithm

    More efficient than NFDH:
    - Tries to place each item on the first shelf that fits
    - Creates new shelf only if no existing shelf works
    - Better utilization than NFDH

    Parameters:
    - items: list of (width, height, item_id) tuples
    - strip_width: fixed width of strip

    Returns: optimized packing solution
    """

    sorted_items = sorted(items, key=lambda x: (x[1], x[0]), reverse=True)
    shelves = []

    for width, height, item_id in sorted_items:
        placed = False

        # Try to place on existing shelves
        for shelf in shelves:
            if (shelf['remaining_width'] >= width and
                shelf['height'] >= height):
                # Place on this shelf
                x = strip_width - shelf['remaining_width']
                shelf['items'].append({
                    'id': item_id,
                    'x': x,
                    'y': shelf['y'],
                    'width': width,
                    'height': height
                })
                shelf['remaining_width'] -= width
                placed = True
                break

        # Create new shelf if not placed
        if not placed:
            y_position = sum(s['height'] for s in shelves)
            new_shelf = {
                'y': y_position,
                'height': height,
                'remaining_width': strip_width - width,
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': y_position,
                    'width': width,
                    'height': height
                }]
            }
            shelves.append(new_shelf)

    total_height = sum(s['height'] for s in shelves)
    packed_items = []
    for shelf in shelves:
        packed_items.extend(shelf['items'])

    return {
        'height': total_height,
        'width': strip_width,
        'shelves': shelves,
        'items': packed_items,
        'utilization': calculate_utilization(packed_items, strip_width, total_height)
    }
```

**Best Fit Decreasing Height (BFDH)**

```python
def best_fit_decreasing_height(items, strip_width):
    """
    Best Fit Decreasing Height Algorithm

    Finds the shelf with minimum wasted space
    - Tries to minimize gaps
    - Better utilization than FFDH
    - More computation time

    Parameters:
    - items: list of (width, height, item_id) tuples
    - strip_width: fixed width of strip

    Returns: optimized packing
    """

    sorted_items = sorted(items, key=lambda x: (x[1], x[0]), reverse=True)
    shelves = []

    for width, height, item_id in sorted_items:
        best_shelf = None
        min_waste = float('inf')

        # Find shelf with minimum waste
        for idx, shelf in enumerate(shelves):
            if (shelf['remaining_width'] >= width and
                shelf['height'] >= height):
                waste = shelf['remaining_width'] - width
                if waste < min_waste:
                    min_waste = waste
                    best_shelf = idx

        if best_shelf is not None:
            # Place on best shelf
            shelf = shelves[best_shelf]
            x = strip_width - shelf['remaining_width']
            shelf['items'].append({
                'id': item_id,
                'x': x,
                'y': shelf['y'],
                'width': width,
                'height': height
            })
            shelf['remaining_width'] -= width
        else:
            # Create new shelf
            y_position = sum(s['height'] for s in shelves)
            new_shelf = {
                'y': y_position,
                'height': height,
                'remaining_width': strip_width - width,
                'items': [{
                    'id': item_id,
                    'x': 0,
                    'y': y_position,
                    'width': width,
                    'height': height
                }]
            }
            shelves.append(new_shelf)

    total_height = sum(s['height'] for s in shelves)
    packed_items = []
    for shelf in shelves:
        packed_items.extend(shelf['items'])

    return {
        'height': total_height,
        'width': strip_width,
        'shelves': shelves,
        'items': packed_items,
        'utilization': calculate_utilization(packed_items, strip_width, total_height)
    }
```

### Bottom-Left Algorithm

```python
def bottom_left_strip_packing(items, strip_width, allow_rotation=True):
    """
    Bottom-Left Algorithm for Strip Packing

    Places each item at the lowest, leftmost position available
    - No shelf constraint
    - More flexible packing
    - Better utilization than shelf algorithms

    Parameters:
    - items: list of (width, height, item_id) tuples
    - strip_width: fixed width
    - allow_rotation: allow 90-degree rotation

    Returns: free-form packing
    """

    # Sort by area (largest first)
    sorted_items = sorted(items,
                         key=lambda x: x[0] * x[1],
                         reverse=True)

    packed_items = []
    max_height = 0

    for width, height, item_id in sorted_items:
        orientations = [(width, height, False)]
        if allow_rotation:
            orientations.append((height, width, True))

        best_position = None
        best_y = float('inf')

        for w, h, rotated in orientations:
            # Try all possible x positions
            for x in range(0, strip_width - w + 1):
                # Find lowest feasible y
                y = find_lowest_position(x, w, h, packed_items, strip_width)

                if y is not None and y < best_y:
                    best_y = y
                    best_position = (x, y, w, h, rotated)

        if best_position:
            x, y, w, h, rotated = best_position
            packed_items.append({
                'id': item_id,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'rotated': rotated
            })
            max_height = max(max_height, y + h)

    return {
        'height': max_height,
        'width': strip_width,
        'items': packed_items,
        'utilization': calculate_utilization(packed_items, strip_width, max_height)
    }

def find_lowest_position(x, width, height, placed_items, strip_width):
    """
    Find lowest y-coordinate where item can be placed

    Checks for overlaps with existing items
    """

    if x + width > strip_width:
        return None

    y = 0

    while True:
        # Check for overlap
        overlap = False
        for item in placed_items:
            if rectangles_intersect(
                x, y, width, height,
                item['x'], item['y'], item['width'], item['height']
            ):
                overlap = True
                # Move above this item
                y = item['y'] + item['height']
                break

        if not overlap:
            return y

        # Safety check (prevent infinite loop)
        if y > 10000:
            return None

def rectangles_intersect(x1, y1, w1, h1, x2, y2, w2, h2):
    """Check if two rectangles intersect"""
    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or
                y1 + h1 <= y2 or y2 + h2 <= y1)
```

### Genetic Algorithm for Strip Packing

```python
import random
import numpy as np

class GeneticAlgorithmStripPacking:
    """
    Genetic Algorithm for Strip Packing

    Optimizes packing sequence and orientations
    """

    def __init__(self, items, strip_width,
                 population_size=50, generations=100,
                 mutation_rate=0.15, crossover_rate=0.8):
        self.items = items
        self.strip_width = strip_width
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.n_items = len(items)
        self.best_solution = None
        self.best_height = float('inf')

    def create_chromosome(self):
        """Create random chromosome: (sequence, orientations)"""
        sequence = list(np.random.permutation(self.n_items))
        orientations = [random.choice([True, False]) for _ in range(self.n_items)]
        return {'sequence': sequence, 'orientations': orientations}

    def decode_chromosome(self, chromosome):
        """Decode chromosome to packing using FFDH"""
        ordered_items = []
        for idx in chromosome['sequence']:
            w, h, item_id = self.items[idx]
            if chromosome['orientations'][idx]:
                w, h = h, w  # Rotate
            ordered_items.append((w, h, item_id))

        result = first_fit_decreasing_height(ordered_items, self.strip_width)
        return result

    def fitness(self, chromosome):
        """Fitness = total height (minimize)"""
        result = self.decode_chromosome(chromosome)
        return result['height']

    def crossover(self, parent1, parent2):
        """Order crossover for sequence + uniform for orientations"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        # Crossover sequence (OX)
        size = len(parent1['sequence'])
        cx1 = random.randint(0, size - 2)
        cx2 = random.randint(cx1 + 1, size - 1)

        child1_seq = [-1] * size
        child2_seq = [-1] * size

        child1_seq[cx1:cx2] = parent1['sequence'][cx1:cx2]
        child2_seq[cx1:cx2] = parent2['sequence'][cx1:cx2]

        self._fill_sequence(child1_seq, parent2['sequence'], cx2)
        self._fill_sequence(child2_seq, parent1['sequence'], cx2)

        # Crossover orientations (uniform)
        child1_orient = []
        child2_orient = []
        for i in range(size):
            if random.random() < 0.5:
                child1_orient.append(parent1['orientations'][i])
                child2_orient.append(parent2['orientations'][i])
            else:
                child1_orient.append(parent2['orientations'][i])
                child2_orient.append(parent1['orientations'][i])

        return (
            {'sequence': child1_seq, 'orientations': child1_orient},
            {'sequence': child2_seq, 'orientations': child2_orient}
        )

    def _fill_sequence(self, child, parent, start_pos):
        """Fill offspring sequence"""
        child_set = set([x for x in child if x != -1])
        pos = start_pos

        for item in parent[start_pos:] + parent[:start_pos]:
            if item not in child_set:
                while child[pos % len(child)] != -1:
                    pos += 1
                child[pos % len(child)] = item
                child_set.add(item)

    def mutate(self, chromosome):
        """Swap mutation + bit flip"""
        # Swap in sequence
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.n_items), 2)
            chromosome['sequence'][i], chromosome['sequence'][j] = \
                chromosome['sequence'][j], chromosome['sequence'][i]

        # Flip orientations
        for i in range(self.n_items):
            if random.random() < self.mutation_rate / 2:
                chromosome['orientations'][i] = not chromosome['orientations'][i]

        return chromosome

    def tournament_selection(self, population, fitnesses, tournament_size=3):
        """Tournament selection"""
        indices = random.sample(range(len(population)), tournament_size)
        fits = [fitnesses[i] for i in indices]
        winner_idx = indices[fits.index(min(fits))]
        return population[winner_idx]

    def solve(self):
        """Run genetic algorithm"""
        population = [self.create_chromosome() for _ in range(self.population_size)]

        for generation in range(self.generations):
            fitnesses = [self.fitness(chrom) for chrom in population]

            # Track best
            min_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_idx] < self.best_height:
                self.best_height = fitnesses[min_idx]
                self.best_solution = self.decode_chromosome(population[min_idx])
                print(f"Gen {generation}: Best height = {self.best_height:.1f}")

            # New population
            new_population = [population[min_idx]]  # Elitism

            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)

                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        return self.best_solution
```

### Complete Strip Packing Solver

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class StripPackingSolver:
    """
    Comprehensive Strip Packing Solver

    Supports multiple algorithms and visualization
    """

    def __init__(self, strip_width, max_height=None):
        self.strip_width = strip_width
        self.max_height = max_height
        self.items = []
        self.solution = None

    def add_item(self, width, height, item_id=None):
        """Add rectangular item to pack"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"
        self.items.append((width, height, item_id))

    def solve(self, algorithm='ffdh', allow_rotation=False, **kwargs):
        """
        Solve strip packing problem

        Algorithms:
        - 'nfdh': Next Fit Decreasing Height
        - 'ffdh': First Fit Decreasing Height (default)
        - 'bfdh': Best Fit Decreasing Height
        - 'bottom_left': Bottom-Left algorithm
        - 'genetic': Genetic Algorithm
        """

        if algorithm == 'nfdh':
            self.solution = next_fit_decreasing_height(self.items, self.strip_width)

        elif algorithm == 'ffdh':
            self.solution = first_fit_decreasing_height(self.items, self.strip_width)

        elif algorithm == 'bfdh':
            self.solution = best_fit_decreasing_height(self.items, self.strip_width)

        elif algorithm == 'bottom_left':
            self.solution = bottom_left_strip_packing(
                self.items, self.strip_width, allow_rotation
            )

        elif algorithm == 'genetic':
            ga = GeneticAlgorithmStripPacking(
                self.items, self.strip_width,
                population_size=kwargs.get('population_size', 50),
                generations=kwargs.get('generations', 100)
            )
            self.solution = ga.solve()

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return self.solution

    def visualize(self, save_path=None):
        """Visualize strip packing solution"""

        if self.solution is None:
            raise ValueError("No solution to visualize")

        fig, ax = plt.subplots(figsize=(10, 12))

        # Draw strip boundary
        strip_rect = patches.Rectangle(
            (0, 0), self.strip_width, self.solution['height'],
            linewidth=2, edgecolor='black', facecolor='none'
        )
        ax.add_patch(strip_rect)

        # Draw items
        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for idx, item in enumerate(self.solution['items']):
            color = colors[idx % 20]

            rect = patches.Rectangle(
                (item['x'], item['y']),
                item['width'], item['height'],
                linewidth=1, edgecolor='black',
                facecolor=color, alpha=0.7
            )
            ax.add_patch(rect)

            # Add label
            cx = item['x'] + item['width'] / 2
            cy = item['y'] + item['height'] / 2
            ax.text(cx, cy, str(item['id']),
                   ha='center', va='center',
                   fontsize=8, fontweight='bold')

        ax.set_xlim(-2, self.strip_width + 2)
        ax.set_ylim(-2, self.solution['height'] + 2)
        ax.set_aspect('equal')
        ax.set_xlabel('Width')
        ax.set_ylabel('Height')
        ax.set_title(f'Strip Packing Solution\n'
                    f'Width: {self.strip_width} | Height: {self.solution["height"]:.1f} | '
                    f'Utilization: {self.solution["utilization"]:.1f}%')
        ax.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def print_solution(self):
        """Print solution summary"""

        if self.solution is None:
            print("No solution available")
            return

        print("=" * 70)
        print("STRIP PACKING SOLUTION")
        print("=" * 70)
        print(f"Strip Width: {self.solution['width']}")
        print(f"Total Height: {self.solution['height']:.1f}")
        print(f"Items Packed: {len(self.solution['items'])}")
        print(f"Utilization: {self.solution['utilization']:.1f}%")
        print(f"Waste: {100 - self.solution['utilization']:.1f}%")


# Example usage
if __name__ == "__main__":
    # Create solver
    solver = StripPackingSolver(strip_width=100)

    # Add items
    items = [
        (40, 30), (35, 25), (50, 20), (30, 40),
        (25, 35), (45, 30), (20, 25), (35, 35),
        (30, 20), (40, 25)
    ]

    for w, h in items:
        solver.add_item(w, h)

    # Solve using FFDH
    print("Solving with FFDH algorithm...")
    solution = solver.solve(algorithm='ffdh')

    # Print results
    solver.print_solution()

    # Visualize
    solver.visualize()
```

---

## Common Challenges & Solutions

### Challenge: Poor Height Utilization

**Problem:**
- Large wasted space
- Height much more than necessary
- Gaps between items

**Solutions:**
- Use BFDH instead of NFDH
- Allow item rotation
- Try bottom-left algorithm for non-shelf packing
- Use genetic algorithm for optimization
- Sort items differently (by area, perimeter)

### Challenge: Guillotine Cut Requirement

**Problem:**
- Manufacturing requires guillotine cuts
- Shelf algorithms don't guarantee guillotine
- Need to modify patterns

**Solutions:**
- Use explicit guillotine algorithm
- Constrain placement to guillotine-compatible positions
- Generate cutting pattern separately
- Trade some efficiency for guillotine compliance

---

## Output Format

### Strip Packing Report

**Problem:**
- Items: 50 rectangles
- Strip Width: 100 cm
- Optimization: Minimize height

**Solution:**
- Algorithm: FFDH
- Total Height: 185 cm
- Utilization: 87.3%
- Waste: 12.7%

**Items Packed:**
- Layer 1 (0-30cm): 12 items
- Layer 2 (30-55cm): 10 items
- Layer 3 (55-85cm): 13 items
- Layer 4 (85-120cm): 9 items
- Layer 5 (120-185cm): 6 items

---

## Questions to Ask

1. What is the strip width?
2. How many items need to be packed?
3. Can items be rotated?
4. Is there a maximum height limit?
5. Are guillotine cuts required?
6. Is this a one-time problem or recurring?

---

## Related Skills

- **2d-bin-packing**: For general 2D packing with fixed dimensions
- **1d-cutting-stock**: For one-dimensional cutting
- **guillotine-cutting**: For guillotine-constrained cutting
- **trim-loss-minimization**: For waste minimization
