---
name: nesting-optimization
description: When the user wants to nest irregular shapes on sheets, pack non-rectangular parts optimally, or solve nesting problems for manufacturing. Also use when the user mentions "nesting," "irregular shape packing," "polygon nesting," "shape nesting," "marker making," "leather nesting," "sheet metal nesting," "garment cutting optimization," or "CNC nesting." For rectangular items, see 2d-cutting-stock. For 1D problems, see 1d-cutting-stock.
---

# Nesting Optimization

You are an expert in nesting optimization for irregular shapes and polygon packing. Your goal is to help minimize material waste when cutting irregular, non-rectangular parts from sheet materials such as sheet metal, leather, fabric, wood, or composite materials.

## Initial Assessment

Before solving nesting problems, understand:

1. **Shape Characteristics**
   - What types of shapes? (simple polygons, complex curves, holes)
   - How are shapes defined? (coordinates, CAD files, DXF, SVG)
   - Number of different part types?
   - Total number of parts to nest?
   - Part complexity (number of vertices/curves)?

2. **Material Specifications**
   - What material? (sheet metal, leather, fabric, wood, composite)
   - Sheet dimensions (width × height)?
   - Single sheet size or multiple available?
   - Material cost per sheet or per area?
   - Grain direction important?
   - Material defects or zones to avoid?

3. **Nesting Constraints**
   - Can parts rotate? (any angle or discrete angles like 90°, 180°?)
   - Minimum spacing between parts?
   - Minimum distance from sheet edge?
   - Parts must align with grain direction?
   - Any parts that must be grouped together?
   - Maximum parts per sheet?

4. **Cutting Technology**
   - Manual cutting, CNC router, laser, waterjet, plasma?
   - Cutting path optimization needed?
   - Bridge/tab requirements for part holding?
   - Entry/exit point constraints?

5. **Optimization Objective**
   - Minimize number of sheets?
   - Minimize total material area/cost?
   - Maximize sheet utilization?
   - Minimize cutting time/path length?
   - Balance multiple objectives?

---

## Nesting Problem Framework

### Problem Classification

**1. Irregular Shape Nesting (2D Packing)**
- Pack arbitrary polygons/shapes onto sheets
- Minimize sheets used or waste
- Most general and complex variant
- NP-hard problem

**2. Strip Packing with Irregular Shapes**
- Fixed width, minimize height
- Single long strip of material
- Common in fabric/textile cutting
- Height minimization

**3. Constrained Nesting**
- Additional constraints:
  - Fixed orientations
  - Grain direction alignment
  - Part grouping requirements
  - Quality zones on material

**4. Online Nesting**
- Parts arrive dynamically over time
- Cannot reorganize already placed parts
- Real-time decision making
- Production scheduling integration

**5. Multi-Material Nesting**
- Different materials with different costs
- Assign parts to appropriate materials
- Minimize total material cost

---

## Mathematical Formulation

### Basic Nesting Problem

**Given:**
- S = sheet with dimensions W × H
- P = {p₁, p₂, ..., pₙ} = set of parts (polygons)
- d_i = demand (quantity) for part p_i

**Decision Variables:**
- x_i, y_i = position of part i (reference point)
- θ_i = rotation angle of part i
- s_j = 1 if sheet j is used, 0 otherwise

**Objective:**
Minimize Σ s_j (minimize number of sheets)

Or: Minimize total material area used

**Constraints:**
1. **Non-overlap:** Parts must not overlap
   - For all pairs (i, k): φ(p_i, p_k, x_i, y_i, θ_i, x_k, y_k, θ_k) = 0
   - Where φ is the overlap function

2. **Containment:** Parts must be within sheet boundaries
   - p_i(x_i, y_i, θ_i) ⊆ S for all i

3. **Spacing:** Minimum distance between parts
   - d(p_i, p_k) ≥ d_min for all pairs (i, k)

4. **Demand:** Meet quantity requirements
   - Each part placed correct number of times

**Complexity:**
- Strongly NP-hard
- No efficient exact algorithm for general case
- Requires metaheuristic approaches

---

## Algorithms and Solution Methods

### Method 1: Bottom-Left (BL) Heuristic

```python
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, rotate
import matplotlib.pyplot as plt

class BottomLeftNesting:
    """
    Bottom-Left (BL) Heuristic for Polygon Nesting

    Classic nesting heuristic:
    1. Place each part at bottom-left-most feasible position
    2. Check overlaps and containment
    3. Move until valid position found

    Fast but not optimal - good starting solution
    """

    def __init__(self, sheet_width, sheet_height, spacing=0):
        """
        Initialize nesting solver

        Parameters:
        - sheet_width: width of sheet
        - sheet_height: height of sheet
        - spacing: minimum spacing between parts
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.spacing = spacing
        self.parts = []
        self.placed_parts = []

    def add_part(self, polygon_coords, quantity=1, part_id=None, rotation_allowed=True):
        """
        Add part to nest

        Parameters:
        - polygon_coords: list of (x,y) coordinates defining polygon
        - quantity: number of this part needed
        - part_id: identifier
        - rotation_allowed: can part be rotated?
        """
        if part_id is None:
            part_id = f"Part_{len(self.parts)}"

        polygon = Polygon(polygon_coords)

        for i in range(quantity):
            self.parts.append({
                'id': f"{part_id}_{i}" if quantity > 1 else part_id,
                'polygon': polygon,
                'original_polygon': polygon,
                'rotation_allowed': rotation_allowed,
                'area': polygon.area
            })

    def find_bottom_left_position(self, part_polygon, placed_polygons):
        """
        Find bottom-left position for a part

        Strategy:
        1. Start at (0, 0)
        2. Move right until no overlap
        3. Move down if possible
        4. Repeat until valid position found
        """

        # Try different positions in a grid search
        step = 10  # mm grid resolution

        for y in range(0, int(self.sheet_height), step):
            for x in range(0, int(self.sheet_width), step):
                # Try this position
                test_polygon = translate(part_polygon, xoff=x, yoff=y)

                # Check if fits in sheet
                if not self._fits_in_sheet(test_polygon):
                    continue

                # Check overlaps with placed parts
                if self._has_overlap(test_polygon, placed_polygons):
                    continue

                # Valid position found
                return x, y, test_polygon

        return None, None, None

    def _fits_in_sheet(self, polygon):
        """Check if polygon fits within sheet boundaries"""
        bounds = polygon.bounds  # (minx, miny, maxx, maxy)
        return (bounds[0] >= 0 and
                bounds[1] >= 0 and
                bounds[2] <= self.sheet_width and
                bounds[3] <= self.sheet_height)

    def _has_overlap(self, polygon, placed_polygons):
        """Check if polygon overlaps with any placed polygons"""
        for placed in placed_polygons:
            # Buffer for spacing
            if self.spacing > 0:
                buffered_placed = placed.buffer(self.spacing / 2)
                buffered_polygon = polygon.buffer(self.spacing / 2)
                if buffered_polygon.intersects(buffered_placed):
                    return True
            else:
                if polygon.intersects(placed):
                    return True
        return False

    def nest(self, rotation_angles=[0, 90, 180, 270]):
        """
        Perform bottom-left nesting

        Parameters:
        - rotation_angles: list of angles to try (degrees)

        Returns: nesting solution
        """

        # Sort parts by area (largest first)
        sorted_parts = sorted(self.parts, key=lambda p: p['area'], reverse=True)

        sheets = []
        current_sheet_parts = []

        for part in sorted_parts:
            placed = False

            # Try rotations if allowed
            angles_to_try = rotation_angles if part['rotation_allowed'] else [0]

            best_position = None
            best_polygon = None
            best_angle = 0

            for angle in angles_to_try:
                # Rotate part
                rotated_polygon = rotate(part['polygon'], angle, origin='centroid')

                # Find position
                x, y, positioned_polygon = self.find_bottom_left_position(
                    rotated_polygon, current_sheet_parts
                )

                if x is not None:
                    # Check if this is better (more bottom-left)
                    if best_position is None or (y < best_position[1] or
                                                 (y == best_position[1] and x < best_position[0])):
                        best_position = (x, y)
                        best_polygon = positioned_polygon
                        best_angle = angle

            if best_position is not None:
                # Place part
                current_sheet_parts.append(best_polygon)
                self.placed_parts.append({
                    'id': part['id'],
                    'polygon': best_polygon,
                    'position': best_position,
                    'angle': best_angle,
                    'sheet': len(sheets)
                })
                placed = True

            if not placed:
                # Start new sheet
                if current_sheet_parts:
                    sheets.append(current_sheet_parts)

                current_sheet_parts = []

                # Place on new sheet
                for angle in angles_to_try:
                    rotated_polygon = rotate(part['polygon'], angle, origin='centroid')
                    x, y, positioned_polygon = self.find_bottom_left_position(
                        rotated_polygon, []
                    )

                    if x is not None:
                        current_sheet_parts.append(positioned_polygon)
                        self.placed_parts.append({
                            'id': part['id'],
                            'polygon': positioned_polygon,
                            'position': (x, y),
                            'angle': angle,
                            'sheet': len(sheets)
                        })
                        break

        # Add last sheet
        if current_sheet_parts:
            sheets.append(current_sheet_parts)

        # Calculate statistics
        total_part_area = sum(p['polygon'].area for p in self.placed_parts)
        total_sheet_area = len(sheets) * self.sheet_width * self.sheet_height
        utilization = (total_part_area / total_sheet_area * 100) if total_sheet_area > 0 else 0

        return {
            'num_sheets': len(sheets),
            'sheets': sheets,
            'placed_parts': self.placed_parts,
            'utilization': utilization,
            'waste': total_sheet_area - total_part_area
        }

    def visualize(self, sheet_index=0, save_path=None):
        """
        Visualize nesting for a specific sheet

        Parameters:
        - sheet_index: which sheet to visualize
        - save_path: path to save figure
        """

        if not self.placed_parts:
            raise ValueError("No nesting solution. Run nest() first.")

        # Get parts for this sheet
        sheet_parts = [p for p in self.placed_parts if p['sheet'] == sheet_index]

        if not sheet_parts:
            raise ValueError(f"Sheet {sheet_index} has no parts")

        fig, ax = plt.subplots(figsize=(12, 10))

        # Draw sheet boundary
        ax.add_patch(plt.Rectangle(
            (0, 0), self.sheet_width, self.sheet_height,
            fill=False, edgecolor='black', linewidth=2
        ))

        # Draw parts
        colors = plt.cm.tab20(np.linspace(0, 1, 20))

        for idx, part in enumerate(sheet_parts):
            polygon = part['polygon']
            color = colors[idx % 20]

            # Draw polygon
            x, y = polygon.exterior.xy
            ax.fill(x, y, facecolor=color, edgecolor='black',
                   linewidth=1.5, alpha=0.6)

            # Add label
            centroid = polygon.centroid
            ax.text(centroid.x, centroid.y, part['id'],
                   ha='center', va='center',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            # Add rotation indicator if rotated
            if part['angle'] != 0:
                ax.text(centroid.x, centroid.y - 20, f"∠{part['angle']}°",
                       ha='center', va='top',
                       fontsize=7, style='italic')

        ax.set_xlim(-50, self.sheet_width + 50)
        ax.set_ylim(-50, self.sheet_height + 50)
        ax.set_aspect('equal')
        ax.set_xlabel('Width (mm)', fontsize=12)
        ax.set_ylabel('Height (mm)', fontsize=12)
        ax.set_title(
            f'Nesting Solution - Sheet {sheet_index + 1}\n'
            f'Parts: {len(sheet_parts)} | Sheet: {self.sheet_width}×{self.sheet_height}mm',
            fontsize=14, fontweight='bold'
        )
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()


# Example usage
def example_bottom_left_nesting():
    """Example: Nesting irregular shapes"""

    nester = BottomLeftNesting(sheet_width=3000, sheet_height=1500, spacing=5)

    # Add some irregular parts (simplified polygons)
    # L-shaped part
    l_shape = [(0, 0), (100, 0), (100, 200), (50, 200), (50, 50), (0, 50)]
    nester.add_part(l_shape, quantity=5, part_id='L_Bracket')

    # T-shaped part
    t_shape = [(0, 0), (150, 0), (150, 30), (90, 30), (90, 100), (60, 100), (60, 30), (0, 30)]
    nester.add_part(t_shape, quantity=8, part_id='T_Bracket')

    # Rectangular part
    rect = [(0, 0), (80, 0), (80, 120), (0, 120)]
    nester.add_part(rect, quantity=10, part_id='Rectangle')

    # Nest
    print("Nesting parts...")
    solution = nester.nest(rotation_angles=[0, 90, 180, 270])

    print(f"\nSolution:")
    print(f"Sheets needed: {solution['num_sheets']}")
    print(f"Utilization: {solution['utilization']:.2f}%")
    print(f"Waste: {solution['waste']:.0f} mm²")

    # Visualize
    nester.visualize(sheet_index=0)

    return solution
```

### Method 2: Genetic Algorithm for Nesting

```python
import random
import numpy as np
from shapely.geometry import Polygon
from shapely.affinity import translate, rotate

class GeneticAlgorithmNesting:
    """
    Genetic Algorithm for Polygon Nesting

    Chromosome encoding:
    - Sequence of parts (permutation)
    - Rotation angles for each part

    Fitness: Minimizes sheets used and waste
    """

    def __init__(self, sheet_width, sheet_height, spacing=0,
                 population_size=50, generations=100,
                 mutation_rate=0.1, crossover_rate=0.8):
        """
        Initialize GA nesting solver

        Parameters:
        - sheet_width, sheet_height: sheet dimensions
        - spacing: minimum spacing between parts
        - population_size: GA population size
        - generations: number of generations
        - mutation_rate: probability of mutation
        - crossover_rate: probability of crossover
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.spacing = spacing
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.parts = []
        self.n_parts = 0

        self.best_solution = None
        self.best_fitness = float('inf')

    def add_part(self, polygon_coords, quantity=1, part_id=None,
                rotation_angles=[0, 90, 180, 270]):
        """
        Add part to nest

        Parameters:
        - polygon_coords: list of (x,y) coordinates
        - quantity: number of parts
        - part_id: identifier
        - rotation_angles: allowed rotation angles
        """
        if part_id is None:
            part_id = f"Part_{len(self.parts)}"

        polygon = Polygon(polygon_coords)

        for i in range(quantity):
            self.parts.append({
                'id': f"{part_id}_{i}" if quantity > 1 else part_id,
                'polygon': polygon,
                'rotation_angles': rotation_angles,
                'area': polygon.area
            })

        self.n_parts = len(self.parts)

    def create_chromosome(self):
        """
        Create random chromosome

        Chromosome = (permutation, rotation_angles)
        - permutation: order to place parts
        - rotation_angles: angle choice for each part
        """
        permutation = list(np.random.permutation(self.n_parts))
        rotation_indices = [random.randint(0, len(self.parts[i]['rotation_angles']) - 1)
                           for i in range(self.n_parts)]

        return {
            'permutation': permutation,
            'rotation_indices': rotation_indices
        }

    def decode_chromosome(self, chromosome):
        """
        Decode chromosome to nesting solution

        Use Bottom-Left placement with specified order and rotations
        """
        permutation = chromosome['permutation']
        rotation_indices = chromosome['rotation_indices']

        sheets = [[]]  # List of lists of polygons
        placed_parts = []

        for idx in permutation:
            part = self.parts[idx]
            angle_idx = rotation_indices[idx]
            angle = part['rotation_angles'][angle_idx]

            # Rotate part
            rotated_polygon = rotate(part['polygon'], angle, origin='centroid')

            # Try to place on current sheet
            placed = False

            for sheet_idx, sheet in enumerate(sheets):
                # Try bottom-left placement
                position = self._find_position_in_sheet(rotated_polygon, sheet)

                if position is not None:
                    x, y = position
                    placed_polygon = translate(rotated_polygon, xoff=x, yoff=y)
                    sheet.append(placed_polygon)
                    placed_parts.append({
                        'id': part['id'],
                        'polygon': placed_polygon,
                        'sheet': sheet_idx,
                        'angle': angle
                    })
                    placed = True
                    break

            if not placed:
                # Create new sheet
                position = self._find_position_in_sheet(rotated_polygon, [])
                if position:
                    x, y = position
                    placed_polygon = translate(rotated_polygon, xoff=x, yoff=y)
                    sheets.append([placed_polygon])
                    placed_parts.append({
                        'id': part['id'],
                        'polygon': placed_polygon,
                        'sheet': len(sheets) - 1,
                        'angle': angle
                    })

        return {
            'sheets': sheets,
            'placed_parts': placed_parts,
            'num_sheets': len(sheets)
        }

    def _find_position_in_sheet(self, polygon, placed_polygons):
        """Find valid position for polygon in sheet"""
        # Simplified: try grid positions
        step = 20

        for y in range(0, int(self.sheet_height), step):
            for x in range(0, int(self.sheet_width), step):
                test_polygon = translate(polygon, xoff=x, yoff=y)

                # Check bounds
                bounds = test_polygon.bounds
                if (bounds[0] < 0 or bounds[1] < 0 or
                    bounds[2] > self.sheet_width or bounds[3] > self.sheet_height):
                    continue

                # Check overlaps
                valid = True
                for placed in placed_polygons:
                    if self.spacing > 0:
                        if test_polygon.buffer(self.spacing/2).intersects(
                           placed.buffer(self.spacing/2)):
                            valid = False
                            break
                    else:
                        if test_polygon.intersects(placed):
                            valid = False
                            break

                if valid:
                    return (x, y)

        return None

    def fitness(self, chromosome):
        """
        Calculate fitness of chromosome

        Fitness = num_sheets + waste_penalty

        Lower is better
        """
        solution = self.decode_chromosome(chromosome)

        num_sheets = solution['num_sheets']

        # Calculate total waste
        total_part_area = sum(p['polygon'].area for p in solution['placed_parts'])
        total_sheet_area = num_sheets * self.sheet_width * self.sheet_height
        waste = total_sheet_area - total_part_area

        # Fitness function
        fitness = num_sheets * 10000 + waste

        return fitness

    def crossover(self, parent1, parent2):
        """
        Order Crossover for permutation
        Uniform crossover for rotation angles
        """
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        # Order crossover for permutation
        size = self.n_parts
        cx_point1 = random.randint(0, size - 2)
        cx_point2 = random.randint(cx_point1 + 1, size - 1)

        # Create children
        child1_perm = [-1] * size
        child2_perm = [-1] * size

        # Copy segments
        child1_perm[cx_point1:cx_point2] = parent1['permutation'][cx_point1:cx_point2]
        child2_perm[cx_point1:cx_point2] = parent2['permutation'][cx_point1:cx_point2]

        # Fill remaining
        self._fill_permutation(child1_perm, parent2['permutation'], cx_point2)
        self._fill_permutation(child2_perm, parent1['permutation'], cx_point2)

        # Uniform crossover for rotation indices
        child1_rot = []
        child2_rot = []
        for i in range(size):
            if random.random() < 0.5:
                child1_rot.append(parent1['rotation_indices'][i])
                child2_rot.append(parent2['rotation_indices'][i])
            else:
                child1_rot.append(parent2['rotation_indices'][i])
                child2_rot.append(parent1['rotation_indices'][i])

        child1 = {'permutation': child1_perm, 'rotation_indices': child1_rot}
        child2 = {'permutation': child2_perm, 'rotation_indices': child2_rot}

        return child1, child2

    def _fill_permutation(self, child, parent, start_pos):
        """Fill remaining positions in child permutation"""
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
        Mutation: swap two positions in permutation
        Random change in rotation angles
        """
        # Mutate permutation
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.n_parts), 2)
            chromosome['permutation'][i], chromosome['permutation'][j] = \
                chromosome['permutation'][j], chromosome['permutation'][i]

        # Mutate rotation angles
        if random.random() < self.mutation_rate:
            idx = random.randint(0, self.n_parts - 1)
            part = self.parts[chromosome['permutation'][idx]]
            chromosome['rotation_indices'][idx] = random.randint(
                0, len(part['rotation_angles']) - 1
            )

        return chromosome

    def tournament_selection(self, population, fitnesses, tournament_size=3):
        """Tournament selection"""
        tournament_idx = random.sample(range(len(population)), tournament_size)
        tournament_fit = [fitnesses[i] for i in tournament_idx]
        winner_idx = tournament_idx[tournament_fit.index(min(tournament_fit))]
        return population[winner_idx]

    def solve(self):
        """
        Run genetic algorithm

        Returns: best nesting solution found
        """

        print("Starting Genetic Algorithm Nesting...")
        print(f"Parts: {self.n_parts}")
        print(f"Population: {self.population_size}")
        print(f"Generations: {self.generations}")
        print()

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
                print(f"Generation {generation}: Best fitness = {self.best_fitness:.0f}, "
                      f"Sheets = {self.best_solution['num_sheets']}")

            # Create new population
            new_population = []

            # Elitism
            new_population.append(population[min_fit_idx])

            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)

                child1, child2 = self.crossover(parent1, parent2)

                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        print(f"\nFinal solution:")
        print(f"Sheets: {self.best_solution['num_sheets']}")

        return self.best_solution


# Example usage
def example_genetic_nesting():
    """Example: GA-based nesting"""

    ga = GeneticAlgorithmNesting(
        sheet_width=3000,
        sheet_height=1500,
        spacing=5,
        population_size=30,
        generations=50
    )

    # Add parts
    l_shape = [(0, 0), (100, 0), (100, 200), (50, 200), (50, 50), (0, 50)]
    ga.add_part(l_shape, quantity=8, part_id='L_Bracket')

    t_shape = [(0, 0), (150, 0), (150, 30), (90, 30), (90, 100), (60, 100), (60, 30), (0, 30)]
    ga.add_part(t_shape, quantity=6, part_id='T_Bracket')

    solution = ga.solve()

    return solution
```

### Method 3: No-Fit Polygon (NFP) Based Nesting

```python
class NoFitPolygonNesting:
    """
    No-Fit Polygon (NFP) Based Nesting

    NFP is a geometric construct that represents all positions
    where polygon A can be placed relative to polygon B such that
    A just touches but doesn't overlap with B.

    This is the state-of-the-art for industrial nesting but
    computationally complex.

    Simplified implementation for demonstration.
    """

    def __init__(self, sheet_width, sheet_height):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height

    def compute_nfp(self, polygon_a, polygon_b):
        """
        Compute No-Fit Polygon for polygon_a relative to polygon_b

        The NFP represents all positions where polygon_a touches
        but doesn't overlap with polygon_b

        This is a simplified placeholder - full NFP computation
        is complex and typically uses Minkowski sum algorithms
        """

        # In practice, use libraries like:
        # - pyclipper for Minkowski operations
        # - shapely for polygon operations
        # - SVGNest algorithms

        # Simplified: just return boundary approximation
        from shapely.ops import unary_union

        # Buffer approach (approximation)
        nfp = polygon_b.buffer(0.01).boundary

        return nfp

    def nest_with_nfp(self, parts):
        """
        Nest parts using NFP-based placement

        This is a conceptual outline - full implementation
        requires sophisticated NFP algorithms
        """

        # This would implement:
        # 1. Compute NFPs for all part pairs
        # 2. Use NFPs to find valid placement positions
        # 3. Optimize placement order and positions
        # 4. Handle rotations using rotated NFPs

        pass  # Placeholder for full implementation
```

---

## Complete Nesting Solver

```python
class ComprehensiveNestingSolver:
    """
    Comprehensive Nesting Solver

    Supports:
    - Multiple algorithms (BL, GA)
    - Visualization
    - Export to DXF/SVG
    """

    def __init__(self, sheet_width, sheet_height, spacing=0):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.spacing = spacing
        self.parts = []
        self.solution = None

    def add_part_from_coordinates(self, coords, quantity=1, part_id=None, rotatable=True):
        """Add part from coordinate list"""
        self.parts.append({
            'coords': coords,
            'quantity': quantity,
            'id': part_id or f"Part_{len(self.parts)}",
            'rotatable': rotatable
        })

    def solve(self, method='bottom_left', **kwargs):
        """
        Solve nesting problem

        Methods:
        - 'bottom_left': Bottom-left heuristic (fast)
        - 'genetic': Genetic algorithm (better quality)
        """

        if method == 'bottom_left':
            solver = BottomLeftNesting(self.sheet_width, self.sheet_height, self.spacing)
            for part in self.parts:
                solver.add_part(part['coords'], part['quantity'], part['id'], part['rotatable'])
            self.solution = solver.nest()

        elif method == 'genetic':
            solver = GeneticAlgorithmNesting(self.sheet_width, self.sheet_height, self.spacing)
            for part in self.parts:
                solver.add_part(part['coords'], part['quantity'], part['id'])
            self.solution = solver.solve()

        return self.solution

    def print_summary(self):
        """Print solution summary"""
        if not self.solution:
            print("No solution available")
            return

        print("="*70)
        print("NESTING SOLUTION")
        print("="*70)
        print(f"Sheets used: {self.solution['num_sheets']}")
        print(f"Utilization: {self.solution.get('utilization', 0):.2f}%")
        print(f"Sheet size: {self.sheet_width} × {self.sheet_height}")
```

---

## Tools & Libraries

### Python Libraries

- **shapely**: Polygon operations and geometry
- **pyclipper**: Polygon clipping and offsetting
- **SVGNest**: JavaScript nesting (can call from Python)
- **nestable**: Python nesting library

### Commercial Software

- **SigmaNEST**: Professional nesting for manufacturing
- **TruTops**: Sheet metal nesting (Trumpf)
- **Lantek**: CNC nesting and cutting
- **Alma CAM**: Nesting for various industries
- **DeepNest**: Open-source web-based nesting

---

## Common Challenges & Solutions

### Challenge: Complex Irregular Shapes

**Solution:** Use NFP-based algorithms or advanced metaheuristics

### Challenge: Computation Time

**Solution:** Hierarchical nesting, parallel processing, time-limited search

### Challenge: Material Grain Direction

**Solution:** Add orientation constraints to placement algorithm

---

## Output Format

**Nesting Report:**
- Sheets: 12
- Utilization: 84.5%
- Parts: 145
- Waste: 15.5%

---

## Questions to Ask

1. What shapes need to be nested?
2. Sheet dimensions?
3. Can parts rotate?
4. Minimum spacing?
5. Material constraints?

---

## Related Skills

- **2d-cutting-stock**: For rectangular cutting
- **guillotine-cutting**: For guillotine constraints
- **trim-loss-minimization**: For waste minimization
- **optimization-modeling**: For general optimization
