---
name: job-shop-scheduling
description: When the user wants to solve Job Shop Scheduling Problems (JSP), optimize production sequencing on multiple machines, or minimize makespan with precedence constraints. Also use when the user mentions "job shop," "JSP," "machine scheduling," "production scheduling," "operation sequencing," "makespan minimization," or "flexible job shop." For flow shop, see flow-shop-scheduling. For production planning, see production-scheduling.
---

# Job Shop Scheduling Problem (JSP)

You are an expert in Job Shop Scheduling and production sequencing optimization. Your goal is to help determine the optimal sequence of operations on machines to minimize completion time (makespan), tardiness, or other objectives, while respecting precedence constraints and machine availability.

## Initial Assessment

Before solving JSP instances, understand:

1. **Problem Characteristics**
   - How many jobs need to be scheduled?
   - How many machines are available?
   - Fixed routing (classic JSP) or flexible (FJSP)?
   - Recirculation allowed? (job can visit same machine twice)

2. **Operation Details**
   - Operations per job?
   - Processing times known and deterministic?
   - Precedence constraints within each job?
   - Setup times between operations?

3. **Objectives**
   - Minimize makespan (total completion time)?
   - Minimize total tardiness?
   - Minimize maximum lateness?
   - Weighted combination?

4. **Constraints**
   - No-wait (operations must start immediately after previous)?
   - Limited buffers between machines?
   - Machine breakdown/maintenance windows?
   - Due dates for jobs?

5. **Problem Scale**
   - Small (< 10 jobs, < 10 machines): Exact methods possible
   - Medium (10-20 jobs): Advanced algorithms
   - Large (20+ jobs): Metaheuristics required

---

## Mathematical Formulation

### Job Shop Scheduling (Disjunctive Graph Model)

**Sets:**
- J = {1, ..., n}: Jobs
- M = {1, ..., m}: Machines
- O_j: Set of operations for job j

**Parameters:**
- p_{ij}: Processing time of operation i of job j
- μ(i,j): Machine required for operation i of job j
- Prec_j: Precedence constraints for job j

**Decision Variables:**
- C_{ij}: Completion time of operation i of job j
- S_{ij}: Start time of operation i of job j
- y_{ij,kl} ∈ {0,1}: 1 if operation (i,j) is processed before (k,l) on same machine

**Objective Function:**
```
Minimize makespan: C_max = max_{j∈J, i∈O_j} C_{ij}
```

Or minimize total tardiness:
```
Minimize: Σ_{j∈J} max(0, C_{last(j)} - d_j)
```

**Constraints:**
```
1. Completion time relationship:
   C_{ij} = S_{ij} + p_{ij},  ∀j ∈ J, ∀i ∈ O_j

2. Precedence within jobs:
   C_{i,j} ≤ S_{i+1,j},  ∀j ∈ J, ∀i ∈ O_j\{last}

3. Disjunctive constraints (no machine overlap):
   For operations (i,j) and (k,l) on same machine μ:

   Either: S_{ij} + p_{ij} ≤ S_{kl}  (i,j before k,l)
   Or:     S_{kl} + p_{kl} ≤ S_{ij}  (k,l before i,j)

   Linearized as:
   S_{ij} + p_{ij} ≤ S_{kl} + M*(1 - y_{ij,kl})
   S_{kl} + p_{kl} ≤ S_{ij} + M*y_{ij,kl}

4. Non-negativity:
   S_{ij}, C_{ij} ≥ 0

5. Binary variables:
   y_{ij,kl} ∈ {0,1}
```

---

## Exact Algorithms

### 1. Branch and Bound for JSP

```python
import numpy as np
from collections import defaultdict

class JobShopProblem:
    """Job Shop Scheduling Problem representation"""

    def __init__(self, jobs, machines):
        """
        Args:
            jobs: list of jobs, each job is list of (machine, time) tuples
                  Example: [[(0, 3), (1, 2), (2, 2)],  # Job 0
                           [(0, 2), (2, 1), (1, 4)]]   # Job 1
            machines: number of machines
        """
        self.jobs = jobs
        self.n_jobs = len(jobs)
        self.n_machines = machines
        self.n_operations = sum(len(job) for job in jobs)

    def calculate_lower_bound(self, partial_schedule):
        """
        Calculate lower bound on makespan

        Uses machine-based and job-based bounds
        """
        # Machine lower bound: max completion time for each machine
        machine_times = [0] * self.n_machines

        for job_id, job in enumerate(self.jobs):
            for op_idx, (machine, time) in enumerate(job):
                if (job_id, op_idx) in partial_schedule:
                    continue
                machine_times[machine] += time

        machine_lb = max(machine_times)

        # Job lower bound: max total time for each job
        job_times = []
        for job_id, job in enumerate(self.jobs):
            total_time = sum(time for _, time in job)
            job_times.append(total_time)

        job_lb = max(job_times)

        return max(machine_lb, job_lb)


def jsp_branch_and_bound_simple(jobs, machines, time_limit=60):
    """
    Simple branch-and-bound for small JSP instances

    Args:
        jobs: list of jobs (each job is list of (machine, processing_time))
        machines: number of machines
        time_limit: time limit in seconds

    Returns:
        best schedule found
    """
    import time

    problem = JobShopProblem(jobs, machines)

    best_makespan = float('inf')
    best_schedule = None

    # Current partial schedule
    schedule = []  # List of (job_id, operation_idx, start_time, machine)
    machine_available = [0] * machines  # Next available time for each machine
    job_next_op = [0] * problem.n_jobs  # Next operation index for each job
    job_available = [0] * problem.n_jobs  # Next available time for each job

    start_time = time.time()

    def backtrack(depth):
        nonlocal best_makespan, best_schedule

        if time.time() - start_time > time_limit:
            return

        # All operations scheduled
        if depth == problem.n_operations:
            makespan = max(machine_available)
            if makespan < best_makespan:
                best_makespan = makespan
                best_schedule = schedule.copy()
            return

        # Pruning: check lower bound
        # (simplified - just check current makespan)
        if max(machine_available) >= best_makespan:
            return

        # Try scheduling next operation for each job
        for job_id in range(problem.n_jobs):
            op_idx = job_next_op[job_id]

            # Check if this job has more operations
            if op_idx >= len(jobs[job_id]):
                continue

            machine, proc_time = jobs[job_id][op_idx]

            # Calculate start time
            start = max(job_available[job_id], machine_available[machine])

            # Schedule this operation
            schedule.append((job_id, op_idx, start, machine))
            old_machine_avail = machine_available[machine]
            old_job_avail = job_available[job_id]

            machine_available[machine] = start + proc_time
            job_available[job_id] = start + proc_time
            job_next_op[job_id] += 1

            # Recurse
            backtrack(depth + 1)

            # Undo
            schedule.pop()
            machine_available[machine] = old_machine_avail
            job_available[job_id] = old_job_avail
            job_next_op[job_id] -= 1

    backtrack(0)

    return {
        'makespan': best_makespan,
        'schedule': best_schedule
    }
```

---

## Classical Heuristics

### 1. Priority Dispatch Rules

```python
def jsp_dispatch_rule(jobs, machines, rule='SPT'):
    """
    Dispatch rule heuristic for JSP

    Priority rules:
    - SPT: Shortest Processing Time
    - LPT: Longest Processing Time
    - FCFS: First Come First Served
    - EDD: Earliest Due Date
    - MWR: Most Work Remaining

    Args:
        jobs: list of jobs (each job is list of (machine, time))
        machines: number of machines
        rule: dispatch rule to use

    Returns:
        schedule and makespan
    """
    n_jobs = len(jobs)

    # Track state
    machine_available = [0] * machines
    job_available = [0] * n_jobs
    job_next_op = [0] * n_jobs
    schedule = []

    # Total operations
    n_ops = sum(len(job) for job in jobs)

    for _ in range(n_ops):
        # Find all eligible operations (next operation for each job)
        eligible = []

        for job_id in range(n_jobs):
            op_idx = job_next_op[job_id]

            if op_idx < len(jobs[job_id]):
                machine, proc_time = jobs[job_id][op_idx]

                # Calculate earliest start time
                earliest_start = max(job_available[job_id],
                                   machine_available[machine])

                eligible.append({
                    'job_id': job_id,
                    'op_idx': op_idx,
                    'machine': machine,
                    'time': proc_time,
                    'start': earliest_start
                })

        if not eligible:
            break

        # Select operation based on rule
        if rule == 'SPT':
            selected = min(eligible, key=lambda x: x['time'])
        elif rule == 'LPT':
            selected = max(eligible, key=lambda x: x['time'])
        elif rule == 'FCFS':
            selected = min(eligible, key=lambda x: x['start'])
        elif rule == 'MWR':
            # Most work remaining for this job
            def remaining_work(op):
                job_id = op['job_id']
                op_idx = op['op_idx']
                remaining = sum(t for _, t in jobs[job_id][op_idx:])
                return remaining

            selected = max(eligible, key=remaining_work)
        else:
            selected = eligible[0]

        # Schedule selected operation
        job_id = selected['job_id']
        machine = selected['machine']
        start_time = selected['start']
        proc_time = selected['time']

        schedule.append({
            'job': job_id,
            'operation': selected['op_idx'],
            'machine': machine,
            'start': start_time,
            'end': start_time + proc_time
        })

        machine_available[machine] = start_time + proc_time
        job_available[job_id] = start_time + proc_time
        job_next_op[job_id] += 1

    makespan = max(machine_available)

    return {
        'schedule': schedule,
        'makespan': makespan,
        'rule': rule
    }
```

### 2. Shifting Bottleneck Heuristic

```python
def shifting_bottleneck_jsp(jobs, machines):
    """
    Shifting Bottleneck Heuristic for JSP

    One of the best constructive heuristics for JSP

    Args:
        jobs: list of jobs
        machines: number of machines

    Returns:
        schedule and makespan
    """
    n_jobs = len(jobs)

    # Initialize
    scheduled_machines = set()
    machine_schedules = {m: [] for m in range(machines)}

    while len(scheduled_machines) < machines:
        # Find bottleneck machine
        max_delay = 0
        bottleneck = None

        for machine in range(machines):
            if machine in scheduled_machines:
                continue

            # Calculate delay caused by this machine
            # (simplified: sum of processing times)
            delay = sum(
                proc_time for job in jobs
                for m, proc_time in job
                if m == machine
            )

            if delay > max_delay:
                max_delay = delay
                bottleneck = machine

        if bottleneck is None:
            break

        # Schedule operations on bottleneck machine
        # using one-machine scheduling (EDD or other rule)
        ops_on_machine = []

        for job_id, job in enumerate(jobs):
            for op_idx, (m, proc_time) in enumerate(job):
                if m == bottleneck:
                    ops_on_machine.append((job_id, op_idx, proc_time))

        # Sort by processing time (SPT)
        ops_on_machine.sort(key=lambda x: x[2])

        # Schedule these operations
        current_time = 0
        for job_id, op_idx, proc_time in ops_on_machine:
            machine_schedules[bottleneck].append({
                'job': job_id,
                'operation': op_idx,
                'start': current_time,
                'end': current_time + proc_time
            })
            current_time += proc_time

        scheduled_machines.add(bottleneck)

    # Combine schedules and calculate makespan
    all_schedule = []
    for machine, ops in machine_schedules.items():
        all_schedule.extend(ops)

    makespan = max(op['end'] for ops in machine_schedules.values()
                  for op in ops) if all_schedule else 0

    return {
        'schedule': all_schedule,
        'makespan': makespan
    }
```

---

## Metaheuristics

### 1. Genetic Algorithm for JSP

```python
import random

def jsp_genetic_algorithm(jobs, machines, population_size=50,
                         generations=200, mutation_rate=0.1):
    """
    Genetic Algorithm for JSP

    Chromosome representation: operation-based encoding

    Args:
        jobs: list of jobs
        machines: number of machines
        population_size: GA population size
        generations: number of generations
        mutation_rate: mutation probability

    Returns:
        best schedule found
    """
    n_jobs = len(jobs)

    # Create operation list (job_id repeated by number of operations)
    operations = []
    for job_id, job in enumerate(jobs):
        operations.extend([job_id] * len(job))

    def decode_chromosome(chromosome):
        """
        Decode chromosome to schedule

        Chromosome is a permutation of operations
        """
        job_next_op = [0] * n_jobs
        machine_available = [0] * machines
        job_available = [0] * n_jobs
        schedule = []

        for job_id in chromosome:
            op_idx = job_next_op[job_id]

            if op_idx >= len(jobs[job_id]):
                continue

            machine, proc_time = jobs[job_id][op_idx]

            start = max(job_available[job_id], machine_available[machine])

            schedule.append({
                'job': job_id,
                'operation': op_idx,
                'machine': machine,
                'start': start,
                'end': start + proc_time
            })

            machine_available[machine] = start + proc_time
            job_available[job_id] = start + proc_time
            job_next_op[job_id] += 1

        makespan = max(machine_available)
        return schedule, makespan

    def fitness(chromosome):
        """Fitness = 1 / makespan"""
        _, makespan = decode_chromosome(chromosome)
        return 1.0 / (1.0 + makespan)

    def precedence_crossover(parent1, parent2):
        """Precedence Preserving Crossover (PPX)"""
        child = []
        remaining1 = parent1.copy()
        remaining2 = parent2.copy()

        while remaining1 or remaining2:
            if random.random() < 0.5 and remaining1:
                job = remaining1.pop(0)
                child.append(job)
                if job in remaining2:
                    remaining2.remove(job)
            elif remaining2:
                job = remaining2.pop(0)
                child.append(job)
                if job in remaining1:
                    remaining1.remove(job)

        return child

    def mutate(chromosome):
        """Swap mutation"""
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(chromosome)), 2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

    # Initialize population
    population = []
    for _ in range(population_size):
        individual = operations.copy()
        random.shuffle(individual)
        population.append(individual)

    best_chromosome = None
    best_makespan = float('inf')

    for generation in range(generations):
        # Evaluate fitness
        fitnesses = [fitness(ind) for ind in population]

        # Track best
        for ind, fit in zip(population, fitnesses):
            _, makespan = decode_chromosome(ind)
            if makespan < best_makespan:
                best_makespan = makespan
                best_chromosome = ind.copy()

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

            child = precedence_crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    best_schedule, _ = decode_chromosome(best_chromosome)

    return {
        'schedule': best_schedule,
        'makespan': best_makespan,
        'chromosome': best_chromosome
    }


# Example usage
if __name__ == "__main__":
    # Classic 3x3 JSP instance (FT03)
    jobs = [
        [(0, 1), (1, 3), (2, 6)],  # Job 0
        [(0, 8), (2, 5), (1, 10)], # Job 1
        [(1, 5), (0, 4), (2, 8)]   # Job 2
    ]

    machines = 3

    print("Job Shop Scheduling Problem")
    print(f"Jobs: {len(jobs)}, Machines: {machines}")
    print("\nJob routing and times:")
    for i, job in enumerate(jobs):
        print(f"  Job {i}: {job}")

    # Try different methods
    print("\n" + "="*60)
    print("Dispatch Rules:")
    print("="*60)

    for rule in ['SPT', 'LPT', 'FCFS', 'MWR']:
        result = jsp_dispatch_rule(jobs, machines, rule)
        print(f"\n{rule}: Makespan = {result['makespan']}")

    print("\n" + "="*60)
    print("Genetic Algorithm:")
    print("="*60)

    ga_result = jsp_genetic_algorithm(jobs, machines,
                                     population_size=50,
                                     generations=100)
    print(f"\nGA: Makespan = {ga_result['makespan']}")

    print("\nBest schedule:")
    for op in sorted(ga_result['schedule'], key=lambda x: x['start']):
        print(f"  Job {op['job']} Op {op['operation']} on Machine {op['machine']}: "
              f"[{op['start']}, {op['end']}]")

    # Visualize Gantt chart
    print("\nGantt Chart:")
    print("-" * 60)

    for machine in range(machines):
        print(f"Machine {machine}: ", end="")
        ops_on_machine = [op for op in ga_result['schedule']
                         if op['machine'] == machine]
        ops_on_machine.sort(key=lambda x: x['start'])

        for op in ops_on_machine:
            print(f"J{op['job']}[{op['start']}-{op['end']}] ", end="")
        print()
```

---

## Tools & Libraries

### Python Libraries
- **OR-Tools (Google)**: CP-SAT solver for JSP
- **Pyomo**: MIP/CP modeling
- **simpy**: Discrete event simulation
- **matplotlib**: Gantt chart visualization

### Specialized Software
- **CPLEX CP Optimizer**: Constraint programming
- **Gurobi**: MIP solver
- **OptaPlanner**: Java-based scheduling

---

## Common Challenges & Solutions

### Challenge: Large Search Space

**Problem:**
- n jobs × m machines creates huge solution space
- Exponential complexity (NP-hard)

**Solutions:**
- Use metaheuristics (GA, Tabu Search)
- Good initial solutions from dispatch rules
- Decomposition approaches

### Challenge: Flexible Job Shop (FJSP)

**Problem:**
- Operations can be performed on multiple machines
- Even more complex than classic JSP

**Solutions:**
- Two-level optimization: machine assignment + sequencing
- Hierarchical GA
- OR-Tools handles naturally

### Challenge: Dynamic Arrivals

**Problem:**
- New jobs arrive during execution
- Need to reschedule

**Solutions:**
- Rolling horizon approach
- Right-shift rescheduling
- Robust schedules with buffers

---

## Output Format

### JSP Solution Report

**Problem:**
- Jobs: 10
- Machines: 5
- Total Operations: 47
- Objective: Minimize Makespan

**Solution:**

| Metric | Value |
|--------|-------|
| Makespan | 243 minutes |
| Machine Utilization | 78% average |
| Idle Time | 187 minutes total |

**Gantt Chart:**
```
Machine 0: J2[0-15] J5[15-32] J1[35-48] ...
Machine 1: J1[0-22] J3[22-40] J7[45-67] ...
Machine 2: J4[0-18] J2[20-35] J6[35-52] ...
...
```

---

## Questions to Ask

1. How many jobs and machines?
2. Is routing fixed or flexible (FJSP)?
3. What's the objective? (makespan, tardiness, flowtime)
4. Are there due dates?
5. Setup times between operations?
6. Can operations be interrupted (preemption)?
7. Are machines always available?
8. Is this static or dynamic (new jobs arrive)?

---

## Related Skills

- **flow-shop-scheduling**: For linear routing
- **production-scheduling**: For broader manufacturing
- **master-production-scheduling**: For planning integration
- **constraint-programming**: For CP approaches
- **optimization-modeling**: For MIP formulation
