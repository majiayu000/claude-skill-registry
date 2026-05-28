---
name: flow-shop-scheduling
description: When the user wants to solve Flow Shop Scheduling Problems (FSP), optimize production on assembly lines, or minimize makespan with linear routing. Also use when the user mentions "flow shop," "FSP," "permutation flow shop," "assembly line scheduling," "sequential processing," or "linear production." For job shop (flexible routing), see job-shop-scheduling.
---

# Flow Shop Scheduling Problem (FSP)

You are an expert in Flow Shop Scheduling and assembly line optimization. Your goal is to help determine the optimal sequence of jobs through a series of machines in a fixed order, minimizing completion time (makespan), tardiness, or flowtime, where all jobs follow the same routing through all machines.

## Initial Assessment

Before solving FSP instances, understand:

1. **Problem Characteristics**
   - How many jobs to schedule?
   - How many machines in sequence?
   - Permutation flow shop (same order on all machines)?
   - No-wait flow shop (no waiting between machines)?
   - Blocking flow shop (limited buffers)?

2. **Processing Times**
   - Processing times known and deterministic?
   - Setup times independent or sequence-dependent?
   - Machine-specific processing times?

3. **Objectives**
   - Minimize makespan (total completion time)?
   - Minimize total flowtime (sum of completion times)?
   - Minimize total tardiness?
   - Minimize maximum lateness?

4. **Constraints**
   - Permutation constraint (same sequence all machines)?
   - No-wait (immediate processing after previous machine)?
   - Limited buffer space?
   - Due dates?

5. **Problem Scale**
   - Small (< 10 jobs, 2-3 machines): Exact methods possible
   - Medium (10-50 jobs): Heuristics
   - Large (50+ jobs): Metaheuristics

---

## Mathematical Formulation

### Permutation Flow Shop Scheduling

**Parameters:**
- n: Number of jobs
- m: Number of machines
- p_{ij}: Processing time of job i on machine j
- J = {1, ..., n}: Set of jobs
- M = {1, ..., m}: Set of machines

**Decision Variables:**
- π: Permutation (sequence) of jobs
- C_{i,j}: Completion time of job π(i) on machine j

**Objective Function:**
```
Minimize makespan: C_max = C_{n,m}
```

Or minimize total flowtime:
```
Minimize: Σ_{i=1}^n C_{i,m}
```

**Constraints:**
```
1. First machine:
   C_{1,1} = p_{π(1),1}
   C_{i,1} = C_{i-1,1} + p_{π(i),1},  i = 2,...,n

2. First job:
   C_{1,j} = C_{1,j-1} + p_{π(1),j},  j = 2,...,m

3. Other jobs and machines:
   C_{i,j} = max(C_{i-1,j}, C_{i,j-1}) + p_{π(i),j},
             i = 2,...,n; j = 2,...,m
```

---

## Exact Algorithms

### 1. Johnson's Algorithm (2-Machine FSP)

```python
import numpy as np

def johnsons_algorithm(processing_times):
    """
    Johnson's Algorithm for 2-machine flow shop

    Optimal algorithm for m=2

    Args:
        processing_times: n x 2 array where
                         processing_times[i][0] = time on machine 1
                         processing_times[i][1] = time on machine 2

    Returns:
        optimal sequence and makespan
    """
    n = len(processing_times)
    jobs = list(range(n))

    # Separate into two sets
    set_1 = []  # Jobs where machine 1 time < machine 2 time
    set_2 = []  # Jobs where machine 1 time >= machine 2 time

    for job_id in jobs:
        m1_time = processing_times[job_id][0]
        m2_time = processing_times[job_id][1]

        if m1_time < m2_time:
            set_1.append((job_id, m1_time))
        else:
            set_2.append((job_id, m2_time))

    # Sort set_1 by machine 1 time (ascending)
    set_1.sort(key=lambda x: x[1])

    # Sort set_2 by machine 2 time (descending)
    set_2.sort(key=lambda x: x[1], reverse=True)

    # Combine: set_1 first, then set_2
    sequence = [job_id for job_id, _ in set_1] + [job_id for job_id, _ in set_2]

    # Calculate makespan
    makespan = calculate_makespan_2machine(sequence, processing_times)

    return {
        'sequence': sequence,
        'makespan': makespan,
        'algorithm': 'Johnson'
    }


def calculate_makespan_2machine(sequence, processing_times):
    """Calculate makespan for 2-machine flow shop"""
    n = len(sequence)

    m1_completion = 0
    m2_completion = 0

    for job_id in sequence:
        m1_time = processing_times[job_id][0]
        m2_time = processing_times[job_id][1]

        # Machine 1
        m1_completion += m1_time

        # Machine 2 (must wait for both machine 1 and previous job on machine 2)
        m2_completion = max(m2_completion, m1_completion) + m2_time

    return m2_completion
```

### 2. Dynamic Programming (Small Instances)

```python
def flowshop_dp_small(processing_times):
    """
    Dynamic programming for small flow shop instances

    Args:
        processing_times: n x m array (n jobs, m machines)

    Returns:
        optimal sequence and makespan
    """
    n, m = processing_times.shape

    # For very small instances only (n <= 12)
    if n > 12:
        raise ValueError("DP only for n <= 12 due to exponential complexity")

    import itertools

    best_sequence = None
    best_makespan = float('inf')

    # Try all permutations
    for sequence in itertools.permutations(range(n)):
        makespan = calculate_makespan(sequence, processing_times)

        if makespan < best_makespan:
            best_makespan = makespan
            best_sequence = sequence

    return {
        'sequence': list(best_sequence),
        'makespan': best_makespan,
        'algorithm': 'Dynamic Programming (enumerate)'
    }


def calculate_makespan(sequence, processing_times):
    """
    Calculate makespan for a given sequence

    Args:
        sequence: job sequence
        processing_times: n x m processing time matrix

    Returns:
        makespan (completion time of last job on last machine)
    """
    n = len(sequence)
    m = processing_times.shape[1]

    # Completion time matrix
    C = np.zeros((n, m))

    # First job
    C[0][0] = processing_times[sequence[0]][0]
    for j in range(1, m):
        C[0][j] = C[0][j-1] + processing_times[sequence[0]][j]

    # First machine
    for i in range(1, n):
        C[i][0] = C[i-1][0] + processing_times[sequence[i]][0]

    # Other positions
    for i in range(1, n):
        for j in range(1, m):
            job = sequence[i]
            C[i][j] = max(C[i-1][j], C[i][j-1]) + processing_times[job][j]

    return C[n-1][m-1]
```

---

## Classical Heuristics

### 1. NEH (Nawaz-Enscore-Ham) Heuristic

```python
def neh_heuristic(processing_times):
    """
    NEH Heuristic for permutation flow shop

    One of the best constructive heuristics for FSP

    Args:
        processing_times: n x m array

    Returns:
        sequence and makespan
    """
    n, m = processing_times.shape

    # Step 1: Sort jobs by total processing time (descending)
    total_times = processing_times.sum(axis=1)
    sorted_jobs = np.argsort(-total_times)

    # Step 2: Build sequence iteratively
    sequence = [sorted_jobs[0]]

    for k in range(1, n):
        job = sorted_jobs[k]

        # Try inserting job at each position
        best_position = 0
        best_makespan = float('inf')

        for pos in range(len(sequence) + 1):
            # Create temporary sequence
            temp_sequence = sequence[:pos] + [job] + sequence[pos:]

            # Calculate makespan
            makespan = calculate_makespan(temp_sequence, processing_times)

            if makespan < best_makespan:
                best_makespan = makespan
                best_position = pos

        # Insert job at best position
        sequence.insert(best_position, job)

    final_makespan = calculate_makespan(sequence, processing_times)

    return {
        'sequence': sequence,
        'makespan': final_makespan,
        'algorithm': 'NEH'
    }
```

### 2. Palmer's Heuristic

```python
def palmer_heuristic(processing_times):
    """
    Palmer's Heuristic for flow shop

    Simple slope-based heuristic

    Args:
        processing_times: n x m array

    Returns:
        sequence and makespan
    """
    n, m = processing_times.shape

    # Calculate slope index for each job
    slopes = []

    for job_id in range(n):
        slope = 0
        for machine in range(m):
            weight = m - 2*machine - 1
            slope += weight * processing_times[job_id][machine]
        slopes.append((slope, job_id))

    # Sort by slope (descending)
    slopes.sort(reverse=True)
    sequence = [job_id for _, job_id in slopes]

    makespan = calculate_makespan(sequence, processing_times)

    return {
        'sequence': sequence,
        'makespan': makespan,
        'algorithm': 'Palmer'
    }
```

### 3. CDS (Campbell-Dudek-Smith) Heuristic

```python
def cds_heuristic(processing_times):
    """
    CDS Heuristic for flow shop

    Applies Johnson's algorithm m-1 times on aggregated machines

    Args:
        processing_times: n x m array

    Returns:
        best sequence and makespan
    """
    n, m = processing_times.shape

    best_sequence = None
    best_makespan = float('inf')

    # Apply Johnson's algorithm for each aggregation level
    for k in range(1, m):
        # Aggregate first k machines and last k machines
        aggregated = np.zeros((n, 2))

        for job in range(n):
            # First k machines (sum)
            aggregated[job][0] = processing_times[job][:k].sum()

            # Last k machines (sum)
            aggregated[job][1] = processing_times[job][-k:].sum()

        # Apply Johnson's algorithm
        result = johnsons_algorithm(aggregated)
        sequence = result['sequence']

        # Calculate actual makespan with full schedule
        makespan = calculate_makespan(sequence, processing_times)

        if makespan < best_makespan:
            best_makespan = makespan
            best_sequence = sequence

    return {
        'sequence': best_sequence,
        'makespan': best_makespan,
        'algorithm': 'CDS'
    }
```

---

## Improvement Heuristics

### 1. Local Search (2-Opt for FSP)

```python
def flowshop_local_search(initial_sequence, processing_times, max_iterations=100):
    """
    Local search (2-opt) for flow shop

    Args:
        initial_sequence: initial job sequence
        processing_times: n x m processing time matrix
        max_iterations: maximum iterations

    Returns:
        improved sequence and makespan
    """
    current_sequence = initial_sequence.copy()
    current_makespan = calculate_makespan(current_sequence, processing_times)

    for iteration in range(max_iterations):
        improved = False

        # Try all pairwise swaps
        for i in range(len(current_sequence)):
            for j in range(i + 1, len(current_sequence)):
                # Swap
                new_sequence = current_sequence.copy()
                new_sequence[i], new_sequence[j] = new_sequence[j], new_sequence[i]

                # Evaluate
                new_makespan = calculate_makespan(new_sequence, processing_times)

                if new_makespan < current_makespan:
                    current_sequence = new_sequence
                    current_makespan = new_makespan
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return {
        'sequence': current_sequence,
        'makespan': current_makespan
    }
```

---

## Metaheuristics

### 1. Genetic Algorithm for FSP

```python
import random

def flowshop_genetic_algorithm(processing_times, population_size=50,
                               generations=200, mutation_rate=0.1):
    """
    Genetic Algorithm for Flow Shop Scheduling

    Args:
        processing_times: n x m processing time matrix
        population_size: population size
        generations: number of generations
        mutation_rate: mutation probability

    Returns:
        best sequence and makespan
    """
    n = processing_times.shape[0]

    def fitness(sequence):
        makespan = calculate_makespan(sequence, processing_times)
        return 1.0 / (1.0 + makespan)

    def order_crossover(parent1, parent2):
        """Order Crossover (OX)"""
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))

        child = [-1] * size
        child[start:end] = parent1[start:end]

        pos = end
        for gene in parent2[end:] + parent2[:end]:
            if gene not in child:
                if pos >= size:
                    pos = 0
                child[pos] = gene
                pos += 1

        return child

    def mutate(sequence):
        """Swap mutation"""
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(sequence)), 2)
            sequence[i], sequence[j] = sequence[j], sequence[i]
        return sequence

    # Initialize population
    population = []
    for _ in range(population_size):
        individual = list(range(n))
        random.shuffle(individual)
        population.append(individual)

    best_sequence = None
    best_makespan = float('inf')

    for generation in range(generations):
        # Evaluate fitness
        fitnesses = [fitness(ind) for ind in population]

        # Track best
        for ind in population:
            makespan = calculate_makespan(ind, processing_times)
            if makespan < best_makespan:
                best_makespan = makespan
                best_sequence = ind.copy()

        # Selection and reproduction
        new_population = []

        # Elitism
        elite_count = int(0.1 * population_size)
        elite_indices = sorted(range(len(fitnesses)),
                              key=lambda i: fitnesses[i],
                              reverse=True)[:elite_count]
        new_population = [population[i].copy() for i in elite_indices]

        # Create offspring
        while len(new_population) < population_size:
            # Tournament selection
            parent1 = max(random.sample(list(zip(population, fitnesses)), 3),
                         key=lambda x: x[1])[0]
            parent2 = max(random.sample(list(zip(population, fitnesses)), 3),
                         key=lambda x: x[1])[0]

            child = order_crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    return {
        'sequence': best_sequence,
        'makespan': best_makespan,
        'algorithm': 'Genetic Algorithm'
    }
```

---

## Visualization

```python
def visualize_flowshop_schedule(sequence, processing_times, save_path=None):
    """
    Visualize flow shop schedule as Gantt chart

    Args:
        sequence: job sequence
        processing_times: processing time matrix
        save_path: path to save figure
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    n = len(sequence)
    m = processing_times.shape[1]

    # Calculate completion times
    C = np.zeros((n, m))

    # First job
    C[0][0] = processing_times[sequence[0]][0]
    for j in range(1, m):
        C[0][j] = C[0][j-1] + processing_times[sequence[0]][j]

    # First machine
    for i in range(1, n):
        C[i][0] = C[i-1][0] + processing_times[sequence[i]][0]

    # Other positions
    for i in range(1, n):
        for j in range(1, m):
            job = sequence[i]
            start_time = max(C[i-1][j], C[i][j-1])
            C[i][j] = start_time + processing_times[job][j]

    # Create Gantt chart
    fig, ax = plt.subplots(figsize=(14, 6))

    colors = plt.cm.Set3(np.linspace(0, 1, n))

    for j in range(m):
        for i in range(n):
            job = sequence[i]
            proc_time = processing_times[job][j]

            if i == 0 and j == 0:
                start = 0
            elif j == 0:
                start = C[i-1][j]
            elif i == 0:
                start = C[i][j-1]
            else:
                start = max(C[i-1][j], C[i][j-1])

            # Draw rectangle
            rect = mpatches.Rectangle((start, j - 0.4), proc_time, 0.8,
                                     facecolor=colors[job],
                                     edgecolor='black', linewidth=1)
            ax.add_patch(rect)

            # Add job label
            ax.text(start + proc_time/2, j, f'J{job}',
                   ha='center', va='center', fontweight='bold')

    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_yticks(range(m))
    ax.set_yticklabels([f'M{i}' for i in range(m)])
    ax.set_xlim(0, C[n-1][m-1] * 1.05)
    ax.set_ylim(-0.5, m - 0.5)
    ax.set_title(f'Flow Shop Schedule (Makespan: {C[n-1][m-1]:.1f})')
    ax.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


# Complete example
if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    # Generate random flow shop problem
    n_jobs = 10
    n_machines = 5

    processing_times = np.random.randint(5, 50, size=(n_jobs, n_machines))

    print("Flow Shop Scheduling Problem")
    print(f"Jobs: {n_jobs}, Machines: {n_machines}")
    print("\nProcessing Times:")
    print(processing_times)

    # Compare different algorithms
    print("\n" + "="*60)
    print("Algorithm Comparison:")
    print("="*60)

    algorithms = [
        ('NEH', neh_heuristic),
        ('Palmer', palmer_heuristic),
        ('CDS', cds_heuristic)
    ]

    results = []

    for name, algorithm in algorithms:
        result = algorithm(processing_times)
        results.append((name, result))
        print(f"\n{name}:")
        print(f"  Makespan: {result['makespan']:.1f}")
        print(f"  Sequence: {result['sequence']}")

    # Genetic Algorithm
    print("\n" + "="*60)
    print("Genetic Algorithm:")
    print("="*60)

    ga_result = flowshop_genetic_algorithm(processing_times,
                                          population_size=50,
                                          generations=100)
    print(f"\nGA Makespan: {ga_result['makespan']:.1f}")
    print(f"GA Sequence: {ga_result['sequence']}")

    # Find best result
    all_results = results + [('GA', ga_result)]
    best_name, best_result = min(all_results, key=lambda x: x[1]['makespan'])

    print("\n" + "="*60)
    print(f"Best Algorithm: {best_name}")
    print(f"Best Makespan: {best_result['makespan']:.1f}")
    print("="*60)

    # Visualize best schedule
    visualize_flowshop_schedule(best_result['sequence'], processing_times)

    # Calculate machine utilization
    makespan = best_result['makespan']
    total_processing = processing_times.sum()
    utilization = total_processing / (makespan * n_machines) * 100

    print(f"\nMachine Utilization: {utilization:.1f}%")
    print(f"Idle Time: {makespan * n_machines - total_processing:.1f}")
```

---

## Tools & Libraries

### Python Libraries
- **NumPy**: Array operations and calculations
- **OR-Tools**: CP-SAT for scheduling
- **matplotlib**: Gantt chart visualization
- **pandas**: Data handling

### Specialized Software
- **Lekin**: Educational scheduling system
- **CPLEX**: MIP solver
- **Gurobi**: MIP solver

---

## Common Challenges & Solutions

### Challenge: Large Problem Size

**Problem:**
- Hundreds of jobs makes exact methods impractical
- Even heuristics can be slow

**Solutions:**
- Use NEH heuristic (very good quality)
- Metaheuristics for larger instances
- Parallel evaluation of sequences

### Challenge: No-Wait Flow Shop

**Problem:**
- No buffers between machines
- Job must immediately proceed to next machine

**Solutions:**
- Modified completion time calculation
- Specialized NEH variant
- Add no-wait constraint to metaheuristics

### Challenge: Sequence-Dependent Setup Times

**Problem:**
- Setup time depends on previous job
- Increases complexity significantly

**Solutions:**
- Modify makespan calculation to include setups
- Use Traveling Salesman formulation
- Advanced metaheuristics

---

## Output Format

### Flow Shop Solution Report

**Problem:**
- Jobs: 20
- Machines: 6 (linear sequence)
- Objective: Minimize Makespan

**Solution:**

| Metric | Value |
|--------|-------|
| Makespan | 487 minutes |
| Machine Utilization | 82% |
| Total Flowtime | 8,945 minutes |
| Average Flowtime | 447 minutes |

**Sequence:**
```
J5 → J12 → J3 → J18 → J7 → J15 → J2 → J10 → ...
```

**Gantt Chart:**
```
M0: J5[0-23] J12[23-48] J3[48-71] ...
M1: [idle] J5[23-45] J12[48-72] ...
M2: [idle] J5[45-63] J12[72-94] ...
...
```

**Machine Statistics:**

| Machine | Processing Time | Idle Time | Utilization |
|---------|----------------|-----------|-------------|
| M0 | 423 | 64 | 87% |
| M1 | 401 | 86 | 82% |
| M2 | 389 | 98 | 80% |
[...]

---

## Questions to Ask

1. How many jobs and machines?
2. Is this permutation flow shop (same order all machines)?
3. What's the objective? (makespan, flowtime, tardiness)
4. Are there buffers between machines?
5. No-wait constraint?
6. Setup times (sequence-dependent or independent)?
7. Are there due dates?
8. Can we use metaheuristics or need guaranteed optimal?

---

## Related Skills

- **job-shop-scheduling**: For flexible routing
- **production-scheduling**: For broader manufacturing
- **assembly-line-balancing**: For line design
- **master-production-scheduling**: For planning
- **optimization-modeling**: For mathematical formulation
