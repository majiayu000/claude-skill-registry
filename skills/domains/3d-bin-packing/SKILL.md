---
name: 3d-bin-packing
description: When the user wants to pack 3D boxes into containers, optimize 3D space utilization, or solve container loading problems. Also use when the user mentions "3D packing," "container packing," "box packing," "3D bin packing problem," "cube packing," "three-dimensional packing," "cargo loading," or "space optimization." For pallet-specific loading, see pallet-loading. For container logistics, see container-loading-optimization.
---

# 3D Bin Packing

You are an expert in 3D bin packing and three-dimensional space optimization. Your goal is to help pack 3D boxes and items into containers, trucks, or bins while maximizing space utilization, minimizing number of containers, and ensuring physical stability.

## Initial Assessment

Before solving 3D bin packing problems, understand:

1. **Problem Objectives**
   - Minimize number of containers/bins used?
   - Maximize utilization of fixed containers?
   - Minimize shipping costs?
   - Ensure load stability?

2. **Item Specifications**
   - How many items to pack? (10s, 100s, 1000s)
   - Item dimensions: length x width x height
   - Item weights (important for stability)?
   - Fragility or stackability constraints?
   - Can items be rotated? (all 6 orientations or restricted?)

3. **Container Specifications**
   - Container dimensions: L x W x H
   - Weight capacity limit?
   - Multiple container types available?
   - Unlimited containers or fixed quantity?

4. **Physical Constraints**
   - Weight distribution requirements?
   - Center of gravity constraints?
   - Stacking limits (max items on top)?
   - Fragile items (can't be at bottom)?
   - Load sequence requirements (LIFO/FIFO)?

5. **Special Requirements**
   - Multi-drop deliveries (order matters)?
   - Item grouping by customer?
   - Axle weight limits?
   - Door access considerations?

---

## 3D Bin Packing Framework

### Problem Classification

**1. 3D Bin Packing Problem (3D-BPP)**
- Pack boxes into minimum number of identical bins
- All items must be packed
- No overlapping
- Items axis-aligned or with rotation

**2. Single Container Loading Problem**
- Maximize utilization of one container
- May not fit all items
- Focus on space efficiency

**3. Pallet/Container Loading Problem**
- Pack onto pallets first, then into containers
- Two-level optimization
- Consider pallet arrangements

**4. Multi-Container Heterogeneous Packing**
- Different container sizes available
- Optimize container selection + packing
- Minimize total cost or volume

**5. Weight-Constrained 3D Packing**
- Both volume and weight limits
- Weight distribution matters
- Center of gravity constraints

---

## Mathematical Formulation

### Basic 3D Bin Packing Model

**Decision Variables:**
- x_i, y_i, z_i = coordinates of item i's corner
- b_i = bin/container number for item i
- o_i = orientation of item i (0-5 for 6 possible rotations)
- used_j = 1 if bin j is used, 0 otherwise

**Objective:**
Minimize ∑ used_j (minimize bins)

**Constraints:**
1. **Non-overlap**: No two items in same bin overlap
2. **Containment**: All items fit within bin boundaries
3. **Support**: Items have adequate support from below
4. **Weight**: Total weight ≤ capacity
5. **Stability**: Center of gravity within bounds

**Complexity:**
- NP-hard (even harder than 2D)
- 3D version significantly more complex
- Requires sophisticated heuristics

---

## Algorithms and Solution Methods

### Exact Methods

**Integer Programming Formulation**

```python
from pulp import *
import numpy as np

def solve_3d_bin_packing_ip(items, bin_dims, max_bins=None):
    """
    3D Bin Packing using Integer Programming

    WARNING: Only practical for very small problems (<10 items)

    Parameters:
    - items: list of (length, width, height, weight, id) tuples
    - bin_dims: (length, width, height, weight_capacity)
    - max_bins: maximum bins to consider

    Returns optimal solution (if found within time limit)
    """

    n = len(items)
    if max_bins is None:
        max_bins = n

    L, W, H, max_weight = bin_dims
    bins = range(max_bins)
    item_ids = range(n)

    prob = LpProblem("3D_Bin_Packing", LpMinimize)

    # Decision variables
    # Position of item i in bin b
    x = LpVariable.dicts("x", [(i,b) for i in item_ids for b in bins],
                        lowBound=0, upBound=L, cat='Continuous')
    y = LpVariable.dicts("y", [(i,b) for i in item_ids for b in bins],
                        lowBound=0, upBound=W, cat='Continuous')
    z = LpVariable.dicts("z", [(i,b) for i in item_ids for b in bins],
                        lowBound=0, upBound=H, cat='Continuous')

    # Assignment: item i in bin b
    a = LpVariable.dicts("assign", [(i,b) for i in item_ids for b in bins],
                        cat='Binary')

    # Bin used
    used = LpVariable.dicts("used", bins, cat='Binary')

    # Objective
    prob += lpSum([used[b] for b in bins]), "Total_Bins"

    # Constraints

    # 1. Each item in exactly one bin
    for i in item_ids:
        prob += lpSum([a[i,b] for b in bins]) == 1, f"Assign_{i}"

    # 2. Items fit in bin boundaries
    for i in item_ids:
        for b in bins:
            l, w, h, weight, _ = items[i]
            M = max(L, W, H)  # Big M

            prob += x[i,b] + l <= L + M * (1 - a[i,b]), f"FitL_{i}_{b}"
            prob += y[i,b] + w <= W + M * (1 - a[i,b]), f"FitW_{i}_{b}"
            prob += z[i,b] + h <= H + M * (1 - a[i,b]), f"FitH_{i}_{b}"

    # 3. Weight capacity
    for b in bins:
        prob += lpSum([items[i][3] * a[i,b] for i in item_ids]) <= \
                max_weight, f"Weight_{b}"

    # 4. Bin used if items assigned
    for b in bins:
        for i in item_ids:
            prob += a[i,b] <= used[b], f"BinUsed_{i}_{b}"

    # Note: Non-overlap constraints are complex and omitted in this simplified version

    # Solve with time limit
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))

    if LpStatus[prob.status] != 'Optimal':
        return None

    # Extract solution
    solution = {'num_bins': int(value(prob.objective)), 'bins': []}

    for b in bins:
        if used[b].varValue > 0.5:
            bin_items = []
            for i in item_ids:
                if a[i,b].varValue > 0.5:
                    bin_items.append({
                        'item_id': i,
                        'position': (x[i,b].varValue, y[i,b].varValue, z[i,b].varValue),
                        'dimensions': items[i][:3],
                        'weight': items[i][3]
                    })
            solution['bins'].append(bin_items)

    return solution
```

### Heuristic Methods

**Bottom-Left-Back (BLB) Algorithm**
- Greedy placement strategy
- Place items at lowest, leftmost, back-most position
- Fast but may not be optimal

```python
class Box:
    """3D Box representation"""
    def __init__(self, length, width, height, weight=0, item_id=None):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.item_id = item_id

    def volume(self):
        return self.length * self.width * self.height

    def can_support(self, other_box):
        """Check if this box can support another box on top"""
        # Simple check: base area
        return (self.length >= other_box.length and
                self.width >= other_box.width)

class Space:
    """Available 3D space in container"""
    def __init__(self, x, y, z, length, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height

    def volume(self):
        return self.length * self.width * self.height

    def fits(self, box, orientation):
        """Check if box fits in this space with given orientation"""
        l, w, h = self.get_oriented_dimensions(box, orientation)
        return l <= self.length and w <= self.width and h <= self.height

    @staticmethod
    def get_oriented_dimensions(box, orientation):
        """Get box dimensions for given orientation (0-5)"""
        dims = [box.length, box.width, box.height]

        # 6 possible orientations (assuming rectangular boxes)
        orientations = [
            (0, 1, 2),  # Original: L, W, H
            (0, 2, 1),  # Rotated: L, H, W
            (1, 0, 2),  # Rotated: W, L, H
            (1, 2, 0),  # Rotated: W, H, L
            (2, 0, 1),  # Rotated: H, L, W
            (2, 1, 0),  # Rotated: H, W, L
        ]

        perm = orientations[orientation]
        return dims[perm[0]], dims[perm[1]], dims[perm[2]]

def bottom_left_back_packing(items, container_dims, allow_rotation=True):
    """
    Bottom-Left-Back (BLB) Algorithm for 3D Bin Packing

    Greedy algorithm that places each item at the lowest,
    leftmost, back-most available position

    Parameters:
    - items: list of Box objects
    - container_dims: (length, width, height, max_weight)
    - allow_rotation: whether to try different orientations

    Returns packing solution
    """

    L, W, H, max_weight = container_dims

    # Sort items by volume (largest first)
    sorted_items = sorted(items, key=lambda b: b.volume(), reverse=True)

    containers = []

    for box in sorted_items:
        placed = False

        # Try existing containers
        for container in containers:
            spaces = container['spaces']
            current_weight = container['total_weight']

            # Try each available space
            for space_idx, space in enumerate(spaces):

                # Try different orientations
                orientations = range(6) if allow_rotation else [0]

                for orientation in orientations:
                    l, w, h = Space.get_oriented_dimensions(box, orientation)

                    if (space.fits(box, orientation) and
                        current_weight + box.weight <= max_weight):

                        # Place box
                        container['items'].append({
                            'box': box,
                            'position': (space.x, space.y, space.z),
                            'dimensions': (l, w, h),
                            'orientation': orientation
                        })

                        container['total_weight'] += box.weight

                        # Remove used space and add new spaces
                        spaces.pop(space_idx)
                        new_spaces = create_residual_spaces(space, l, w, h)
                        spaces.extend(new_spaces)

                        # Sort spaces by position (bottom-left-back first)
                        spaces.sort(key=lambda s: (s.z, s.y, s.x))

                        placed = True
                        break

                if placed:
                    break

            if placed:
                break

        # Create new container if not placed
        if not placed:
            l, w, h = box.length, box.width, box.height

            new_container = {
                'items': [{
                    'box': box,
                    'position': (0, 0, 0),
                    'dimensions': (l, w, h),
                    'orientation': 0
                }],
                'spaces': [],
                'total_weight': box.weight,
                'dimensions': (L, W, H)
            }

            # Create initial residual spaces
            initial_space = Space(0, 0, 0, L, W, H)
            new_spaces = create_residual_spaces(initial_space, l, w, h)
            new_container['spaces'] = new_spaces

            containers.append(new_container)

    return {
        'num_containers': len(containers),
        'containers': containers,
        'utilization': calculate_3d_utilization(containers, L, W, H)
    }

def create_residual_spaces(space, used_l, used_w, used_h):
    """
    Create residual spaces after placing a box

    Returns up to 3 new spaces
    """
    spaces = []

    # Space to the right
    if space.length > used_l:
        spaces.append(Space(
            space.x + used_l, space.y, space.z,
            space.length - used_l, space.width, space.height
        ))

    # Space in front
    if space.width > used_w:
        spaces.append(Space(
            space.x, space.y + used_w, space.z,
            used_l, space.width - used_w, space.height
        ))

    # Space above
    if space.height > used_h:
        spaces.append(Space(
            space.x, space.y, space.z + used_h,
            used_l, used_w, space.height - used_h
        ))

    return spaces

def calculate_3d_utilization(containers, L, W, H):
    """Calculate volume utilization percentage"""
    total_item_volume = 0
    for container in containers:
        for item in container['items']:
            l, w, h = item['dimensions']
            total_item_volume += l * w * h

    total_container_volume = len(containers) * L * W * H
    return (total_item_volume / total_container_volume * 100) if total_container_volume > 0 else 0
```

**Layer Building Algorithm**
- Build horizontal layers
- Pack items within each layer (2D problem)
- Stack layers vertically
- Good for real-world packing

```python
def layer_building_algorithm(items, container_dims):
    """
    Layer Building Algorithm for 3D Packing

    Builds horizontal layers and packs items within each layer
    More practical for real-world loading

    Parameters:
    - items: list of Box objects
    - container_dims: (length, width, height, max_weight)

    Returns layered packing solution
    """

    L, W, H, max_weight = container_dims

    # Sort items by height (tallest first for each layer)
    sorted_items = sorted(items, key=lambda b: b.height, reverse=True)

    containers = []

    remaining_items = sorted_items.copy()

    while remaining_items:
        # Start new container
        container = {
            'layers': [],
            'items': [],
            'total_weight': 0,
            'current_height': 0
        }

        while remaining_items and container['current_height'] < H:
            # Select items for new layer
            layer_height = remaining_items[0].height

            # Find items that fit in this layer height
            layer_items = [
                item for item in remaining_items
                if item.height == layer_height
            ]

            if not layer_items:
                # Try next height
                remaining_items.pop(0)
                continue

            # Check if layer fits
            if container['current_height'] + layer_height > H:
                break

            # Pack items in 2D for this layer
            layer_packing = pack_layer_2d(
                layer_items, L, W,
                max_weight - container['total_weight']
            )

            if not layer_packing['items']:
                break

            # Add layer to container
            layer_z = container['current_height']

            for item_data in layer_packing['items']:
                container['items'].append({
                    'box': item_data['box'],
                    'position': (
                        item_data['x'],
                        item_data['y'],
                        layer_z
                    ),
                    'dimensions': (
                        item_data['box'].length,
                        item_data['box'].width,
                        item_data['box'].height
                    ),
                    'layer': len(container['layers'])
                })

                container['total_weight'] += item_data['box'].weight
                remaining_items.remove(item_data['box'])

            container['layers'].append({
                'z': layer_z,
                'height': layer_height,
                'items': layer_packing['items']
            })

            container['current_height'] += layer_height

        if container['items']:
            containers.append(container)

        # If no items packed, need new strategy
        if remaining_items and not container['items']:
            # Force pack at least one item
            item = remaining_items.pop(0)
            new_container = {
                'items': [{
                    'box': item,
                    'position': (0, 0, 0),
                    'dimensions': (item.length, item.width, item.height),
                    'layer': 0
                }],
                'layers': [{'z': 0, 'height': item.height, 'items': [item]}],
                'total_weight': item.weight,
                'current_height': item.height
            }
            containers.append(new_container)

    return {
        'num_containers': len(containers),
        'containers': containers,
        'utilization': calculate_3d_utilization(containers, L, W, H)
    }

def pack_layer_2d(items, layer_length, layer_width, remaining_weight):
    """
    Pack items in 2D for a single layer

    Uses simple FFDH algorithm adapted for 2D
    """

    # Sort by area
    sorted_items = sorted(items, key=lambda b: b.length * b.width, reverse=True)

    packed_items = []
    strips = []  # Horizontal strips in the layer
    total_weight = 0

    for box in sorted_items:
        if total_weight + box.weight > remaining_weight:
            continue

        placed = False

        # Try existing strips
        for strip in strips:
            if (strip['remaining_length'] >= box.length and
                strip['width'] >= box.width):

                # Place in strip
                x = layer_length - strip['remaining_length']
                y = strip['y']

                packed_items.append({
                    'box': box,
                    'x': x,
                    'y': y
                })

                strip['remaining_length'] -= box.length
                total_weight += box.weight
                placed = True
                break

        if not placed:
            # Create new strip
            current_width = sum(s['width'] for s in strips)

            if current_width + box.width <= layer_width:
                new_strip = {
                    'y': current_width,
                    'width': box.width,
                    'remaining_length': layer_length - box.length
                }
                strips.append(new_strip)

                packed_items.append({
                    'box': box,
                    'x': 0,
                    'y': current_width
                })

                total_weight += box.weight

    return {'items': packed_items}
```

**Extreme Point Algorithm**
- Maintains set of extreme points (potential placement positions)
- Places boxes at extreme points
- More sophisticated than BLB

```python
class ExtremePoint:
    """3D Extreme Point for placement"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, other):
        # Sort by z (height), then y (width), then x (length)
        return (self.z, self.y, self.x) < (other.z, other.y, other.x)

def extreme_point_algorithm(items, container_dims, allow_rotation=True):
    """
    Extreme Point Algorithm for 3D Packing

    Uses extreme points as potential placement positions
    Generally better quality than simple BLB

    Parameters:
    - items: list of Box objects
    - container_dims: (L, W, H, max_weight)
    - allow_rotation: allow 6 orientations
    """

    L, W, H, max_weight = container_dims

    # Sort by volume
    sorted_items = sorted(items, key=lambda b: b.volume(), reverse=True)

    containers = []

    for box in sorted_items:
        placed = False

        # Try existing containers
        for container in containers:
            extreme_points = container['extreme_points']
            current_weight = container['total_weight']

            # Sort extreme points (lowest, leftmost, back-most first)
            extreme_points.sort()

            for ep in extreme_points[:]:  # Copy list as we'll modify it
                orientations = range(6) if allow_rotation else [0]

                for orientation in orientations:
                    l, w, h = Space.get_oriented_dimensions(box, orientation)

                    # Check if box fits at this extreme point
                    if (ep.x + l <= L and ep.y + w <= W and ep.z + h <= H and
                        current_weight + box.weight <= max_weight):

                        # Check for overlap with existing items
                        overlaps = False
                        for existing in container['items']:
                            if boxes_overlap_3d(
                                ep.x, ep.y, ep.z, l, w, h,
                                existing['position'][0], existing['position'][1], existing['position'][2],
                                existing['dimensions'][0], existing['dimensions'][1], existing['dimensions'][2]
                            ):
                                overlaps = True
                                break

                        if not overlaps:
                            # Place box
                            container['items'].append({
                                'box': box,
                                'position': (ep.x, ep.y, ep.z),
                                'dimensions': (l, w, h),
                                'orientation': orientation
                            })

                            container['total_weight'] += box.weight

                            # Remove this extreme point
                            extreme_points.remove(ep)

                            # Generate new extreme points
                            new_eps = [
                                ExtremePoint(ep.x + l, ep.y, ep.z),      # Right
                                ExtremePoint(ep.x, ep.y + w, ep.z),      # Front
                                ExtremePoint(ep.x, ep.y, ep.z + h)       # Top
                            ]

                            # Add only feasible extreme points
                            for new_ep in new_eps:
                                if (new_ep.x < L and new_ep.y < W and new_ep.z < H):
                                    # Check if not dominated by existing EP
                                    if not is_dominated(new_ep, extreme_points):
                                        extreme_points.append(new_ep)

                            placed = True
                            break

                if placed:
                    break

            if placed:
                break

        # Create new container
        if not placed:
            l, w, h = box.length, box.width, box.height

            new_container = {
                'items': [{
                    'box': box,
                    'position': (0, 0, 0),
                    'dimensions': (l, w, h),
                    'orientation': 0
                }],
                'extreme_points': [
                    ExtremePoint(l, 0, 0),
                    ExtremePoint(0, w, 0),
                    ExtremePoint(0, 0, h)
                ],
                'total_weight': box.weight
            }

            containers.append(new_container)

    return {
        'num_containers': len(containers),
        'containers': containers,
        'utilization': calculate_3d_utilization(containers, L, W, H)
    }

def boxes_overlap_3d(x1, y1, z1, l1, w1, h1, x2, y2, z2, l2, w2, h2):
    """Check if two 3D boxes overlap"""
    return not (x1 + l1 <= x2 or x2 + l2 <= x1 or
                y1 + w1 <= y2 or y2 + w2 <= y1 or
                z1 + h1 <= z2 or z2 + h2 <= z1)

def is_dominated(point, existing_points):
    """Check if point is dominated by any existing point"""
    for ep in existing_points:
        if ep.x <= point.x and ep.y <= point.y and ep.z <= point.z:
            if ep.x < point.x or ep.y < point.y or ep.z < point.z:
                return True
    return False
```

### Metaheuristic Methods

**Genetic Algorithm for 3D Packing**

```python
import random
import numpy as np

class GeneticAlgorithm3DPacking:
    """
    Genetic Algorithm for 3D Bin Packing

    Chromosome encodes:
    - Item sequence (order to pack)
    - Orientation for each item
    """

    def __init__(self, items, container_dims,
                 population_size=50, generations=100,
                 mutation_rate=0.15, crossover_rate=0.8):
        self.items = items
        self.container_dims = container_dims
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.n_items = len(items)
        self.best_solution = None
        self.best_fitness = float('inf')

    def create_chromosome(self):
        """
        Create random chromosome

        Chromosome = (sequence, orientations)
        """
        sequence = list(np.random.permutation(self.n_items))
        orientations = [random.randint(0, 5) for _ in range(self.n_items)]
        return {'sequence': sequence, 'orientations': orientations}

    def decode_chromosome(self, chromosome):
        """Decode chromosome to packing solution using BLB"""
        ordered_items = [self.items[i] for i in chromosome['sequence']]

        # Apply orientations (simplified - just use orientation 0 for now)
        result = bottom_left_back_packing(
            ordered_items, self.container_dims, allow_rotation=True
        )
        return result

    def fitness(self, chromosome):
        """
        Fitness = number of containers (minimize)
        Secondary: maximize utilization
        """
        solution = self.decode_chromosome(chromosome)
        # Minimize bins, maximize utilization
        return solution['num_containers'] - solution['utilization'] / 1000

    def crossover(self, parent1, parent2):
        """Order crossover for sequence + uniform for orientations"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        # Crossover sequence (OX)
        size = len(parent1['sequence'])
        cx_point1 = random.randint(0, size - 2)
        cx_point2 = random.randint(cx_point1 + 1, size - 1)

        child1_seq = [-1] * size
        child2_seq = [-1] * size

        child1_seq[cx_point1:cx_point2] = parent1['sequence'][cx_point1:cx_point2]
        child2_seq[cx_point1:cx_point2] = parent2['sequence'][cx_point1:cx_point2]

        self._fill_sequence(child1_seq, parent2['sequence'], cx_point2)
        self._fill_sequence(child2_seq, parent1['sequence'], cx_point2)

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
        """
        Mutation: swap two items in sequence
        and randomly change some orientations
        """
        # Swap mutation on sequence
        if random.random() < self.mutation_rate:
            pos1, pos2 = random.sample(range(self.n_items), 2)
            seq = chromosome['sequence']
            seq[pos1], seq[pos2] = seq[pos2], seq[pos1]

        # Random change on orientations
        for i in range(self.n_items):
            if random.random() < self.mutation_rate / 2:
                chromosome['orientations'][i] = random.randint(0, 5)

        return chromosome

    def tournament_selection(self, population, fitnesses, tournament_size=3):
        """Tournament selection"""
        tournament_idx = random.sample(range(len(population)), tournament_size)
        tournament_fit = [fitnesses[i] for i in tournament_idx]
        winner_idx = tournament_idx[tournament_fit.index(min(tournament_fit))]
        return population[winner_idx]

    def solve(self):
        """Run genetic algorithm"""
        # Initialize population
        population = [self.create_chromosome() for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluate fitness
            fitnesses = [self.fitness(chrom) for chrom in population]

            # Track best
            min_fit_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_fit_idx] < self.best_fitness:
                self.best_fitness = fitnesses[min_fit_idx]
                self.best_solution = self.decode_chromosome(population[min_fit_idx])
                print(f"Gen {generation}: Best = {self.best_solution['num_containers']} containers")

            # New population
            new_population = [population[min_fit_idx]]  # Elitism

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

---

## Complete 3D Bin Packing Solver

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

class ThreeDimensionalBinPacker:
    """
    Comprehensive 3D Bin Packing Solver

    Supports multiple algorithms, visualization, and physical constraints
    """

    def __init__(self, container_length, container_width, container_height,
                 weight_capacity=None):
        self.container_dims = (
            container_length, container_width, container_height,
            weight_capacity if weight_capacity else float('inf')
        )
        self.items = []
        self.solution = None

    def add_item(self, length, width, height, weight=0, item_id=None,
                 stackable=True, fragile=False):
        """Add item to pack"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        box = Box(length, width, height, weight, item_id)
        box.stackable = stackable
        box.fragile = fragile
        self.items.append(box)

    def add_items_from_list(self, items_data):
        """
        Add multiple items

        items_data: list of dicts with keys: length, width, height, weight
        """
        for item in items_data:
            self.add_item(
                item.get('length'),
                item.get('width'),
                item.get('height'),
                item.get('weight', 0),
                item.get('id'),
                item.get('stackable', True),
                item.get('fragile', False)
            )

    def solve(self, algorithm='blb', **kwargs):
        """
        Solve 3D packing problem

        Algorithms:
        - 'blb': Bottom-Left-Back
        - 'layer': Layer Building
        - 'extreme_point': Extreme Point
        - 'genetic': Genetic Algorithm
        """

        if algorithm == 'blb':
            self.solution = bottom_left_back_packing(
                self.items, self.container_dims,
                kwargs.get('allow_rotation', True)
            )

        elif algorithm == 'layer':
            self.solution = layer_building_algorithm(
                self.items, self.container_dims
            )

        elif algorithm == 'extreme_point':
            self.solution = extreme_point_algorithm(
                self.items, self.container_dims,
                kwargs.get('allow_rotation', True)
            )

        elif algorithm == 'genetic':
            ga = GeneticAlgorithm3DPacking(
                self.items, self.container_dims,
                population_size=kwargs.get('population_size', 50),
                generations=kwargs.get('generations', 100)
            )
            self.solution = ga.solve()

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return self.solution

    def visualize(self, container_index=0, save_path=None):
        """
        3D visualization of packing solution

        Parameters:
        - container_index: which container to visualize
        - save_path: path to save figure
        """

        if self.solution is None:
            raise ValueError("No solution to visualize")

        if container_index >= len(self.solution['containers']):
            raise ValueError(f"Container index {container_index} out of range")

        container = self.solution['containers'][container_index]
        L, W, H = self.container_dims[:3]

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Draw container boundaries
        self._draw_container_box(ax, L, W, H)

        # Draw items
        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for idx, item in enumerate(container['items']):
            pos = item['position']
            dims = item['dimensions']
            color = colors[idx % 20]

            self._draw_box(ax, pos, dims, color, alpha=0.7)

            # Add label
            center = (
                pos[0] + dims[0]/2,
                pos[1] + dims[1]/2,
                pos[2] + dims[2]/2
            )
            ax.text(center[0], center[1], center[2],
                   str(item['box'].item_id),
                   fontsize=8, ha='center')

        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        ax.set_title(f'Container {container_index + 1}\n'
                    f'{len(container["items"])} items | '
                    f'Weight: {container["total_weight"]:.1f}')

        # Set equal aspect ratio
        max_dim = max(L, W, H)
        ax.set_xlim(0, max_dim)
        ax.set_ylim(0, max_dim)
        ax.set_zlim(0, max_dim)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def _draw_container_box(self, ax, L, W, H):
        """Draw container boundary wireframe"""
        # Define the 8 vertices of the container
        vertices = [
            [0, 0, 0], [L, 0, 0], [L, W, 0], [0, W, 0],  # Bottom
            [0, 0, H], [L, 0, H], [L, W, H], [0, W, H]   # Top
        ]

        # Define the 12 edges
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom
            [4, 5], [5, 6], [6, 7], [7, 4],  # Top
            [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical
        ]

        for edge in edges:
            points = [vertices[edge[0]], vertices[edge[1]]]
            ax.plot3D(*zip(*points), 'k-', linewidth=2)

    def _draw_box(self, ax, position, dimensions, color, alpha=0.7):
        """Draw a 3D box"""
        x, y, z = position
        l, w, h = dimensions

        # Define 8 vertices of the box
        vertices = np.array([
            [x, y, z], [x+l, y, z], [x+l, y+w, z], [x, y+w, z],
            [x, y, z+h], [x+l, y, z+h], [x+l, y+w, z+h], [x, y+w, z+h]
        ])

        # Define 6 faces
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]]   # Top
        ]

        face_collection = Poly3DCollection(faces,
                                          facecolors=color,
                                          linewidths=1,
                                          edgecolors='black',
                                          alpha=alpha)
        ax.add_collection3d(face_collection)

    def get_statistics(self):
        """Get detailed statistics"""
        if self.solution is None:
            return None

        L, W, H, max_weight = self.container_dims

        total_item_volume = sum(b.volume() for b in self.items)
        total_container_volume = self.solution['num_containers'] * L * W * H

        stats = {
            'num_items': len(self.items),
            'num_containers': self.solution['num_containers'],
            'container_dims': (L, W, H),
            'weight_capacity': max_weight,
            'total_item_volume': total_item_volume,
            'total_container_volume': total_container_volume,
            'utilization': self.solution['utilization'],
            'waste': 100 - self.solution['utilization'],
            'containers': []
        }

        for idx, container in enumerate(self.solution['containers']):
            container_vol = sum(
                item['dimensions'][0] * item['dimensions'][1] * item['dimensions'][2]
                for item in container['items']
            )

            stats['containers'].append({
                'container_id': idx,
                'num_items': len(container['items']),
                'total_weight': container['total_weight'],
                'volume_used': container_vol,
                'volume_total': L * W * H,
                'utilization': (container_vol / (L * W * H) * 100)
            })

        return stats

    def print_solution(self):
        """Print solution summary"""
        if self.solution is None:
            print("No solution available")
            return

        stats = self.get_statistics()

        print("=" * 70)
        print("3D BIN PACKING SOLUTION")
        print("=" * 70)
        print(f"Items to pack: {stats['num_items']}")
        print(f"Container dimensions: {stats['container_dims'][0]} x "
              f"{stats['container_dims'][1]} x {stats['container_dims'][2]}")
        print(f"Weight capacity: {stats['weight_capacity']}")
        print(f"Containers used: {stats['num_containers']}")
        print(f"Overall utilization: {stats['utilization']:.2f}%")
        print(f"Waste: {stats['waste']:.2f}%")
        print()

        print("Container Details:")
        print("-" * 70)
        for c_stat in stats['containers']:
            print(f"Container {c_stat['container_id'] + 1}: "
                  f"{c_stat['num_items']} items | "
                  f"Weight: {c_stat['total_weight']:.1f} | "
                  f"Utilization: {c_stat['utilization']:.1f}%")


# Example usage
if __name__ == "__main__":
    # Create packer
    packer = ThreeDimensionalBinPacker(
        container_length=100,
        container_width=100,
        container_height=100,
        weight_capacity=1000
    )

    # Add items
    np.random.seed(42)
    items = [
        {'length': 40, 'width': 30, 'height': 20, 'weight': 50, 'id': 'A1'},
        {'length': 35, 'width': 25, 'height': 30, 'weight': 45, 'id': 'A2'},
        {'length': 50, 'width': 40, 'height': 15, 'weight': 60, 'id': 'A3'},
        {'length': 25, 'width': 25, 'height': 25, 'weight': 30, 'id': 'A4'},
        {'length': 30, 'width': 30, 'height': 40, 'weight': 55, 'id': 'A5'},
        {'length': 20, 'width': 20, 'height': 35, 'weight': 25, 'id': 'A6'},
        {'length': 45, 'width': 35, 'height': 25, 'weight': 65, 'id': 'A7'},
        {'length': 30, 'width': 20, 'height': 30, 'weight': 35, 'id': 'A8'},
    ]

    packer.add_items_from_list(items)

    # Solve
    print("Solving with Bottom-Left-Back algorithm...")
    solution = packer.solve(algorithm='blb', allow_rotation=True)

    # Print results
    packer.print_solution()

    # Visualize
    print("\nGenerating visualization...")
    packer.visualize(container_index=0)
```

---

## Tools & Libraries

### Python Libraries

**py3dbp** - 3D Bin Packing Python library
```python
from py3dbp import Packer, Bin, Item

packer = Packer()

# Add bin
packer.add_bin(Bin('container1', 100, 100, 100, 1000))

# Add items
packer.add_item(Item('item1', 50, 40, 30, 50))
packer.add_item(Item('item2', 40, 30, 20, 40))

# Pack
packer.pack()

# Results
for b in packer.bins:
    print(f"Bin: {b.name}")
    for item in b.items:
        print(f"  {item.name}: position {item.position}")
```

**binpack3d** - Simple 3D packing

**OR-Tools** - Google optimization tools with 3D packing support

### Commercial Software

- **Cargo Planner**: Container loading software
- **EasyCargo**: 3D load planning
- **LoadPlanner**: Truck and container loading
- **Pack Manager**: Pallet and container optimization
- **LoadMaster**: Load optimization software

---

## Common Challenges & Solutions

### Challenge: Poor Space Utilization (<65%)

**Problem:**
- Items don't pack efficiently
- Large gaps between items
- Low container fill rate

**Solutions:**
- Use extreme point algorithm (better than BLB)
- Allow rotation in all 6 orientations
- Apply genetic algorithm for better sequence
- Consider pre-sorting by size ratios
- Group similar-sized items

### Challenge: Weight Distribution

**Problem:**
- Container overweight on one side
- Unstable load
- Axle weight violations

**Solutions:**
- Add center of gravity constraints
- Layer-building approach (distribute weight per layer)
- Place heavy items at bottom center
- Calculate weight distribution during packing
- Post-optimization balancing step

### Challenge: Load Stability

**Problem:**
- Items fall during transport
- Floating items (no support)
- Top-heavy loads

**Solutions:**
- Enforce support constraints (items need support from below)
- Limit stacking height based on item strength
- Place fragile items on top
- Add stability score to fitness function
- Require minimum contact area with supporting surface

### Challenge: Loading/Unloading Sequence

**Problem:**
- Need to unload in specific order
- LIFO/FIFO requirements
- Multi-drop delivery

**Solutions:**
- Incorporate unloading sequence in model
- Zone-based packing (by drop location)
- Last-in-first-out constraint
- Reserve sections per delivery stop
- Sequential packing by route order

### Challenge: Mixed Item Sizes

**Problem:**
- Very large + very small items
- Difficult to pack together efficiently
- Small items fall through gaps

**Solutions:**
- Pre-cluster small items into groups
- Pack large items first, fill with small
- Use layer approach (separate layers for sizes)
- Consider separate bins for small items

---

## Output Format

### 3D Packing Report

**Executive Summary:**
- Items packed: 150 boxes
- Containers used: 3 (40ft containers)
- Average utilization: 82.5%
- Total weight: 18,500 lbs
- Algorithm: Extreme Point + GA

**Container Utilization:**

| Container | Items | Volume Used | Weight | Utilization | COG Offset |
|-----------|-------|-------------|--------|-------------|------------|
| 1 | 55 | 1,985 ft³ | 6,800 lbs | 87.2% | 2.3 in |
| 2 | 52 | 1,850 ft³ | 6,200 lbs | 81.3% | 1.8 in |
| 3 | 43 | 1,750 ft³ | 5,500 lbs | 76.9% | 3.1 in |

**Loading Instructions (Container 1):**

Layer 1 (Bottom):
- Items A001-A015: Heavy boxes (50-80 lbs each)
- Placed centered for weight distribution
- Height: 0-24 inches

Layer 2:
- Items B001-B025: Medium boxes (30-50 lbs each)
- Interlocked pattern for stability
- Height: 24-48 inches

Layer 3 (Top):
- Items C001-C015: Light/fragile boxes (<30 lbs each)
- Protected from crushing
- Height: 48-72 inches

**Item Manifest:**

| Item ID | Dimensions (LxWxH) | Weight | Position | Container | Layer |
|---------|-------------------|--------|----------|-----------|-------|
| A001 | 48x40x24 | 75 lbs | (0,0,0) | 1 | 1 |
| A002 | 40x32x20 | 65 lbs | (48,0,0) | 1 | 1 |

**Warnings/Notes:**
- Container 3 has 23% unused space - consider consolidation
- Item Z005 (fragile) placed on top layer - handle with care
- Center of gravity within acceptable range for all containers

---

## Questions to Ask

If you need more context:
1. What are the container dimensions?
2. How many items need packing? What are their sizes and weights?
3. Can items be rotated freely or are there restrictions?
4. Are there weight limits or weight distribution requirements?
5. Any stacking restrictions? (fragile items, maximum stack height)
6. Is loading/unloading sequence important?
7. Multi-drop deliveries requiring specific zones?
8. Any irregular-shaped items or all rectangular boxes?

---

## Related Skills

- **2d-bin-packing**: For two-dimensional packing problems
- **pallet-loading**: For pallet-specific loading optimization
- **container-loading-optimization**: For container logistics
- **vehicle-loading-optimization**: For truck/vehicle loading
- **knapsack-problems**: For value-based item selection
- **load-building-optimization**: For multi-stage load planning
- **warehouse-slotting-optimization**: For warehouse space optimization
