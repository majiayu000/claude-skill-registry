---
name: production-scheduling
description: When the user wants to schedule production operations, optimize manufacturing schedules, balance workloads, or sequence jobs. Also use when the user mentions "job shop scheduling," "flow shop scheduling," "dispatching rules," "sequence optimization," "machine scheduling," "MRP," "finite capacity scheduling," "production planning," or "shop floor scheduling." For capacity planning, see capacity-planning. For master scheduling, see master-production-scheduling.
---

# Production Scheduling

You are an expert in production scheduling and manufacturing operations. Your goal is to help organizations create efficient production schedules that minimize makespan, reduce WIP, meet due dates, and maximize resource utilization.

## Initial Assessment

Before developing production schedules, understand:

1. **Manufacturing Environment**
   - Shop type? (job shop, flow shop, batch production, continuous)
   - Number of machines/work centers?
   - Product variety and volumes?
   - Make-to-order, make-to-stock, or assemble-to-order?

2. **Scheduling Constraints**
   - Precedence constraints (routing/sequence requirements)?
   - Machine capabilities and restrictions?
   - Setup times and changeover requirements?
   - Resource constraints (labor, tooling, materials)?
   - Shift patterns and availability?

3. **Scheduling Objectives**
   - Primary goal? (minimize makespan, meet due dates, reduce WIP)
   - Due date commitments and penalties?
   - Priority rules for competing jobs?
   - Trade-offs between objectives?

4. **Current State**
   - Current scheduling method? (manual, ERP, spreadsheet)
   - Schedule performance metrics?
   - Known bottlenecks or issues?
   - Planning horizon and replan frequency?

---

## Production Scheduling Framework

### Shop Floor Configurations

**1. Job Shop**
- Multiple products with unique routings
- High variety, low volume
- Complex scheduling problem (NP-hard)
- Flexible machines, varied sequences
- Example: Custom machinery, tool & die shops

**2. Flow Shop**
- Linear production flow
- All products follow same machine sequence
- Easier to schedule than job shop
- Focus on sequence optimization
- Example: Electronics assembly, food processing

**3. Batch Production**
- Produce in batches
- Setup-dependent scheduling
- Minimize changeovers
- Balance batch sizes with demand
- Example: Chemicals, pharmaceuticals

**4. Continuous Production**
- 24/7 operations
- Minimize changeovers and downtime
- Focus on throughput maximization
- Production leveling important
- Example: Oil refining, paper mills

### Scheduling Objectives

**Common Objectives:**

1. **Minimize Makespan** - Total completion time for all jobs
2. **Minimize Tardiness** - Late deliveries relative to due dates
3. **Minimize WIP** - Work-in-process inventory
4. **Maximize Throughput** - Units produced per period
5. **Maximize Utilization** - Equipment and labor efficiency
6. **Minimize Setup Time** - Reduce changeovers between jobs

**Multi-Objective Optimization:**
- Often need to balance multiple objectives
- Use weighted objective functions or Pareto optimization
- Trade-off analysis between competing goals

---

## Job Shop Scheduling

### Problem Formulation

**Job Shop Scheduling Problem (JSP):**

Given:
- n jobs J₁, J₂, ..., Jₙ
- m machines M₁, M₂, ..., Mₘ
- Each job has sequence of operations with processing times
- Each operation requires specific machine
- No preemption (operations can't be interrupted)

Objective: Minimize makespan (Cmax = max completion time)

### Classic JSP Algorithms

**Dispatching Rules:**

Simple priority rules for job sequencing:

```python
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

class DispatchingRules:
    """
    Common dispatching rules for production scheduling
    """

    @staticmethod
    def FCFS(jobs):
        """First Come First Served - arrival order"""
        return sorted(jobs, key=lambda j: j['arrival_time'])

    @staticmethod
    def SPT(jobs):
        """Shortest Processing Time first"""
        return sorted(jobs, key=lambda j: j['processing_time'])

    @staticmethod
    def LPT(jobs):
        """Longest Processing Time first"""
        return sorted(jobs, key=lambda j: j['processing_time'], reverse=True)

    @staticmethod
    def EDD(jobs):
        """Earliest Due Date first"""
        return sorted(jobs, key=lambda j: j['due_date'])

    @staticmethod
    def CR(jobs, current_time):
        """Critical Ratio = (due_date - current_time) / remaining_processing_time"""
        for job in jobs:
            slack = job['due_date'] - current_time
            job['cr'] = slack / job['remaining_time'] if job['remaining_time'] > 0 else float('inf')
        return sorted(jobs, key=lambda j: j['cr'])

    @staticmethod
    def SLACK(jobs, current_time):
        """Minimum Slack = due_date - current_time - remaining_processing_time"""
        for job in jobs:
            job['slack'] = job['due_date'] - current_time - job['remaining_time']
        return sorted(jobs, key=lambda j: j['slack'])

    @staticmethod
    def WSPT(jobs):
        """Weighted Shortest Processing Time"""
        for job in jobs:
            job['wspt'] = job['priority'] / job['processing_time']
        return sorted(jobs, key=lambda j: j['wspt'], reverse=True)

# Example usage
jobs = [
    {'id': 'J1', 'arrival_time': 0, 'processing_time': 5, 'due_date': 15,
     'remaining_time': 5, 'priority': 3},
    {'id': 'J2', 'arrival_time': 1, 'processing_time': 3, 'due_date': 10,
     'remaining_time': 3, 'priority': 2},
    {'id': 'J3', 'arrival_time': 2, 'processing_time': 8, 'due_date': 20,
     'remaining_time': 8, 'priority': 1},
    {'id': 'J4', 'arrival_time': 3, 'processing_time': 4, 'due_date': 12,
     'remaining_time': 4, 'priority': 2},
]

# Apply different rules
spt_sequence = DispatchingRules.SPT(jobs.copy())
edd_sequence = DispatchingRules.EDD(jobs.copy())
cr_sequence = DispatchingRules.CR(jobs.copy(), current_time=5)

print("SPT Sequence:", [j['id'] for j in spt_sequence])
print("EDD Sequence:", [j['id'] for j in edd_sequence])
print("CR Sequence:", [j['id'] for j in cr_sequence])
```

### Job Shop Scheduling with Constraint Programming

```python
from ortools.sat.python import cp_model
import pandas as pd

class JobShopScheduler:
    """
    Solve Job Shop Scheduling Problem using CP-SAT
    Minimize makespan
    """

    def __init__(self, jobs_data):
        """
        jobs_data: list of jobs, each job is list of (machine, duration) tuples

        Example:
        jobs_data = [
            [(0, 3), (1, 2), (2, 2)],  # Job 0: M0(3h) -> M1(2h) -> M2(2h)
            [(0, 2), (2, 1), (1, 4)],  # Job 1: M0(2h) -> M2(1h) -> M1(4h)
            [(1, 4), (2, 3)]           # Job 2: M1(4h) -> M2(3h)
        ]
        """
        self.jobs_data = jobs_data
        self.num_jobs = len(jobs_data)
        self.num_machines = max(task[0] for job in jobs_data for task in job) + 1
        self.all_machines = range(self.num_machines)

        # Compute horizon (upper bound on makespan)
        self.horizon = sum(task[1] for job in jobs_data for task in job)

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def create_model(self):
        """Build the constraint programming model"""

        # Create variables
        self.task_type = {}
        self.starts = {}
        self.ends = {}
        self.intervals = {}

        for job_id, job in enumerate(self.jobs_data):
            for task_id, task in enumerate(job):
                machine, duration = task
                suffix = f'_{job_id}_{task_id}'

                # Start time variable
                start_var = self.model.NewIntVar(0, self.horizon, f'start{suffix}')
                # End time variable
                end_var = self.model.NewIntVar(0, self.horizon, f'end{suffix}')
                # Interval variable
                interval_var = self.model.NewIntervalVar(
                    start_var, duration, end_var, f'interval{suffix}'
                )

                self.task_type[(job_id, task_id)] = (machine, duration)
                self.starts[(job_id, task_id)] = start_var
                self.ends[(job_id, task_id)] = end_var
                self.intervals[(job_id, task_id)] = interval_var

        # Precedence constraints (within each job)
        for job_id, job in enumerate(self.jobs_data):
            for task_id in range(len(job) - 1):
                self.model.Add(
                    self.ends[(job_id, task_id)] <=
                    self.starts[(job_id, task_id + 1)]
                )

        # No overlap constraints (for each machine)
        for machine in self.all_machines:
            intervals_on_machine = [
                self.intervals[(job_id, task_id)]
                for job_id, job in enumerate(self.jobs_data)
                for task_id, task in enumerate(job)
                if task[0] == machine
            ]
            if intervals_on_machine:
                self.model.AddNoOverlap(intervals_on_machine)

        # Objective: minimize makespan
        self.makespan = self.model.NewIntVar(0, self.horizon, 'makespan')
        self.model.AddMaxEquality(
            self.makespan,
            [self.ends[(job_id, len(job) - 1)]
             for job_id, job in enumerate(self.jobs_data)]
        )
        self.model.Minimize(self.makespan)

    def solve(self, time_limit_seconds=10):
        """Solve the scheduling problem"""

        self.solver.parameters.max_time_in_seconds = time_limit_seconds
        status = self.solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._extract_solution()
        else:
            return None

    def _extract_solution(self):
        """Extract schedule from solved model"""

        schedule = []

        for job_id, job in enumerate(self.jobs_data):
            for task_id, task in enumerate(job):
                machine, duration = task
                start = self.solver.Value(self.starts[(job_id, task_id)])
                end = self.solver.Value(self.ends[(job_id, task_id)])

                schedule.append({
                    'job': job_id,
                    'task': task_id,
                    'machine': machine,
                    'start': start,
                    'end': end,
                    'duration': duration
                })

        makespan = self.solver.Value(self.makespan)

        return {
            'makespan': makespan,
            'schedule': pd.DataFrame(schedule),
            'objective': self.solver.ObjectiveValue(),
            'solve_time': self.solver.WallTime()
        }

    def print_schedule(self, solution):
        """Print the schedule in readable format"""

        if solution is None:
            print("No solution found")
            return

        print(f"\nOptimal Makespan: {solution['makespan']}")
        print(f"Solve Time: {solution['solve_time']:.2f} seconds\n")

        df = solution['schedule'].sort_values(['machine', 'start'])

        for machine in sorted(df['machine'].unique()):
            print(f"Machine {machine}:")
            machine_tasks = df[df['machine'] == machine]
            for _, row in machine_tasks.iterrows():
                print(f"  Job {row['job']}, Task {row['task']}: "
                      f"[{row['start']}, {row['end']}] (duration={row['duration']})")
            print()

# Example: Classic 3x3 Job Shop Problem (Fisher & Thompson)
jobs_data = [
    [(0, 3), (1, 2), (2, 2)],  # Job 0
    [(0, 2), (2, 1), (1, 4)],  # Job 1
    [(1, 4), (2, 3)]           # Job 2
]

jsp = JobShopScheduler(jobs_data)
jsp.create_model()
solution = jsp.solve(time_limit_seconds=10)
jsp.print_schedule(solution)
```

### Gantt Chart Visualization

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_gantt_chart(schedule_df, title="Production Schedule"):
    """
    Create Gantt chart visualization of production schedule

    Parameters:
    - schedule_df: DataFrame with columns [job, machine, start, end]
    """

    fig, ax = plt.subplots(figsize=(14, 8))

    # Assign colors to jobs
    jobs = schedule_df['job'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(jobs)))
    job_colors = {job: colors[i] for i, job in enumerate(jobs)}

    # Create bars for each task
    for idx, row in schedule_df.iterrows():
        ax.barh(
            y=row['machine'],
            width=row['end'] - row['start'],
            left=row['start'],
            height=0.8,
            color=job_colors[row['job']],
            edgecolor='black',
            linewidth=1.5,
            label=f"Job {row['job']}" if idx == 0 or
                  row['job'] not in schedule_df.iloc[:idx]['job'].values else ""
        )

        # Add job label on bar
        ax.text(
            (row['start'] + row['end']) / 2,
            row['machine'],
            f"J{row['job']}",
            ha='center',
            va='center',
            fontweight='bold',
            fontsize=10
        )

    # Configure axes
    machines = sorted(schedule_df['machine'].unique())
    ax.set_yticks(machines)
    ax.set_yticklabels([f'Machine {m}' for m in machines])
    ax.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax.set_ylabel('Machine', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add grid
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')

    # Add legend (unique jobs only)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(),
              loc='upper right', fontsize=10)

    plt.tight_layout()
    return fig

# Use with previous solution
if solution:
    fig = plot_gantt_chart(solution['schedule'],
                          title=f"Job Shop Schedule (Makespan={solution['makespan']})")
    plt.show()
```

---

## Flow Shop Scheduling

### NEH Algorithm (Nawaz-Enscore-Ham)

Best heuristic for permutation flow shop scheduling:

```python
import numpy as np
import itertools

class FlowShopNEH:
    """
    NEH Algorithm for Permutation Flow Shop Scheduling
    Minimize makespan
    """

    def __init__(self, processing_times):
        """
        processing_times: 2D array [n_jobs x m_machines]
        processing_times[j][m] = time for job j on machine m
        """
        self.processing_times = np.array(processing_times)
        self.n_jobs, self.n_machines = self.processing_times.shape

    def calculate_makespan(self, sequence):
        """
        Calculate makespan for given job sequence

        Parameters:
        - sequence: list of job indices

        Returns completion time (makespan)
        """
        n = len(sequence)
        m = self.n_machines

        # Completion times: C[j][m] = completion time of job j on machine m
        C = np.zeros((n, m))

        for j_idx, job in enumerate(sequence):
            for machine in range(m):
                if j_idx == 0 and machine == 0:
                    # First job, first machine
                    C[j_idx][machine] = self.processing_times[job][machine]
                elif j_idx == 0:
                    # First job, subsequent machines
                    C[j_idx][machine] = (C[j_idx][machine-1] +
                                        self.processing_times[job][machine])
                elif machine == 0:
                    # Subsequent jobs, first machine
                    C[j_idx][machine] = (C[j_idx-1][machine] +
                                        self.processing_times[job][machine])
                else:
                    # Subsequent jobs, subsequent machines
                    C[j_idx][machine] = (max(C[j_idx-1][machine],
                                            C[j_idx][machine-1]) +
                                        self.processing_times[job][machine])

        return C[n-1][m-1]  # Makespan = completion time of last job on last machine

    def neh_algorithm(self):
        """
        NEH heuristic algorithm

        Returns:
        - best_sequence: optimal job sequence
        - makespan: corresponding makespan
        """

        # Step 1: Calculate total processing time for each job
        total_times = self.processing_times.sum(axis=1)

        # Step 2: Sort jobs by descending total processing time
        sorted_jobs = np.argsort(-total_times)  # Descending order

        # Step 3: Build sequence iteratively
        sequence = [sorted_jobs[0]]  # Start with job with highest total time

        for job in sorted_jobs[1:]:
            best_makespan = float('inf')
            best_position = 0

            # Try inserting job at each position
            for pos in range(len(sequence) + 1):
                trial_sequence = sequence[:pos] + [job] + sequence[pos:]
                makespan = self.calculate_makespan(trial_sequence)

                if makespan < best_makespan:
                    best_makespan = makespan
                    best_position = pos

            # Insert job at best position
            sequence.insert(best_position, job)

        final_makespan = self.calculate_makespan(sequence)

        return {
            'sequence': sequence,
            'makespan': final_makespan,
            'job_labels': [f'Job_{j}' for j in sequence]
        }

# Example: 4 jobs x 3 machines
processing_times = [
    [5, 3, 4],  # Job 0
    [3, 4, 2],  # Job 1
    [6, 2, 3],  # Job 2
    [4, 5, 1]   # Job 3
]

fs = FlowShopNEH(processing_times)
result = fs.neh_algorithm()

print(f"Optimal Sequence: {result['job_labels']}")
print(f"Makespan: {result['makespan']}")
```

### Flow Shop with Setup Times

```python
class FlowShopWithSetups:
    """
    Flow shop scheduling with sequence-dependent setup times
    """

    def __init__(self, processing_times, setup_times):
        """
        processing_times: 2D array [n_jobs x m_machines]
        setup_times: 3D array [n_jobs x n_jobs x m_machines]
                     setup_times[i][j][m] = setup time from job i to job j on machine m
        """
        self.processing_times = np.array(processing_times)
        self.setup_times = np.array(setup_times)
        self.n_jobs, self.n_machines = self.processing_times.shape

    def calculate_makespan_with_setups(self, sequence):
        """Calculate makespan including setup times"""

        n = len(sequence)
        m = self.n_machines
        C = np.zeros((n, m))

        for j_idx, job in enumerate(sequence):
            for machine in range(m):
                # Get setup time
                if j_idx == 0:
                    setup_time = 0  # No setup for first job
                else:
                    prev_job = sequence[j_idx - 1]
                    setup_time = self.setup_times[prev_job][job][machine]

                processing_time = self.processing_times[job][machine]

                if j_idx == 0 and machine == 0:
                    C[j_idx][machine] = processing_time
                elif j_idx == 0:
                    C[j_idx][machine] = C[j_idx][machine-1] + setup_time + processing_time
                elif machine == 0:
                    C[j_idx][machine] = C[j_idx-1][machine] + setup_time + processing_time
                else:
                    C[j_idx][machine] = (max(C[j_idx-1][machine], C[j_idx][machine-1]) +
                                        setup_time + processing_time)

        return C[n-1][m-1]

    def genetic_algorithm(self, population_size=50, generations=100,
                         mutation_rate=0.1, crossover_rate=0.8):
        """
        Genetic algorithm for flow shop with setups

        Returns best sequence found
        """

        # Initialize population with random sequences
        population = [np.random.permutation(self.n_jobs).tolist()
                     for _ in range(population_size)]

        best_solution = None
        best_makespan = float('inf')

        for gen in range(generations):
            # Evaluate fitness (lower makespan = better)
            fitness = []
            for seq in population:
                makespan = self.calculate_makespan_with_setups(seq)
                fitness.append(1.0 / makespan)  # Inverse for maximization

                if makespan < best_makespan:
                    best_makespan = makespan
                    best_solution = seq.copy()

            # Selection: tournament selection
            new_population = []
            fitness = np.array(fitness)

            for _ in range(population_size):
                # Tournament of size 3
                tournament = np.random.choice(population_size, 3, replace=False)
                winner = tournament[np.argmax(fitness[tournament])]
                new_population.append(population[winner].copy())

            # Crossover: order crossover (OX)
            for i in range(0, population_size-1, 2):
                if np.random.random() < crossover_rate:
                    parent1 = new_population[i]
                    parent2 = new_population[i+1]
                    child1, child2 = self._order_crossover(parent1, parent2)
                    new_population[i] = child1
                    new_population[i+1] = child2

            # Mutation: swap mutation
            for i in range(population_size):
                if np.random.random() < mutation_rate:
                    new_population[i] = self._swap_mutation(new_population[i])

            population = new_population

        return {
            'sequence': best_solution,
            'makespan': best_makespan
        }

    def _order_crossover(self, parent1, parent2):
        """Order crossover (OX) for permutation"""
        size = len(parent1)
        start, end = sorted(np.random.choice(size, 2, replace=False))

        child1 = [-1] * size
        child2 = [-1] * size

        # Copy segment
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        # Fill remaining from other parent
        self._fill_remaining(child1, parent2, start, end)
        self._fill_remaining(child2, parent1, start, end)

        return child1, child2

    def _fill_remaining(self, child, parent, start, end):
        """Helper for order crossover"""
        size = len(child)
        parent_idx = end
        child_idx = end

        while -1 in child:
            if parent[parent_idx % size] not in child:
                child[child_idx % size] = parent[parent_idx % size]
                child_idx += 1
            parent_idx += 1

    def _swap_mutation(self, sequence):
        """Swap two random positions"""
        seq = sequence.copy()
        i, j = np.random.choice(len(seq), 2, replace=False)
        seq[i], seq[j] = seq[j], seq[i]
        return seq

# Example with setup times
processing_times = [
    [5, 3, 4],
    [3, 4, 2],
    [6, 2, 3],
    [4, 5, 1]
]

# Setup times: [from_job][to_job][machine]
n_jobs, n_machines = 4, 3
setup_times = np.random.randint(1, 3, size=(n_jobs, n_jobs, n_machines))
# No setup from job to itself
for i in range(n_jobs):
    setup_times[i][i][:] = 0

fs_setup = FlowShopWithSetups(processing_times, setup_times)
result = fs_setup.genetic_algorithm(population_size=50, generations=100)

print(f"Best Sequence: {result['sequence']}")
print(f"Makespan: {result['makespan']}")
```

---

## Advanced Scheduling Techniques

### Finite Capacity Scheduling (FCS)

```python
from datetime import datetime, timedelta
import pandas as pd

class FiniteCapacityScheduler:
    """
    Finite capacity scheduler with resource constraints
    Forward and backward scheduling
    """

    def __init__(self, work_centers):
        """
        work_centers: dict {wc_id: {'capacity_hours': X, 'efficiency': Y}}
        """
        self.work_centers = work_centers
        self.schedule = []

    def forward_schedule(self, orders, start_date):
        """
        Forward scheduling from start date
        Schedule as early as possible

        Parameters:
        - orders: list of dicts with 'order_id', 'routing', 'quantity'
        - routing is list of (work_center, hours_per_unit)
        """

        # Track work center availability
        wc_availability = {wc: start_date for wc in self.work_centers}

        # Sort orders by priority (if available) or order
        orders = sorted(orders, key=lambda x: x.get('priority', 0), reverse=True)

        results = []

        for order in orders:
            order_start = start_date

            for operation_idx, (wc, hours_per_unit) in enumerate(order['routing']):
                # Calculate required hours
                required_hours = order['quantity'] * hours_per_unit
                efficiency = self.work_centers[wc]['efficiency']
                actual_hours = required_hours / efficiency

                # Earliest start is max of order flow and resource availability
                operation_start = max(order_start, wc_availability[wc])
                operation_end = operation_start + timedelta(hours=actual_hours)

                # Update work center availability
                wc_availability[wc] = operation_end

                # Record operation
                results.append({
                    'order_id': order['order_id'],
                    'operation': operation_idx,
                    'work_center': wc,
                    'start': operation_start,
                    'end': operation_end,
                    'hours': actual_hours
                })

                # Next operation starts after this one
                order_start = operation_end

        return pd.DataFrame(results)

    def backward_schedule(self, orders, due_dates):
        """
        Backward scheduling from due dates
        Schedule as late as possible (just-in-time)

        Parameters:
        - orders: list of dicts with 'order_id', 'routing', 'quantity'
        - due_dates: dict {order_id: due_date}
        """

        results = []

        for order in orders:
            order_due = due_dates[order['order_id']]

            # Process routing in reverse
            routing = list(reversed(order['routing']))

            for operation_idx, (wc, hours_per_unit) in enumerate(routing):
                required_hours = order['quantity'] * hours_per_unit
                efficiency = self.work_centers[wc]['efficiency']
                actual_hours = required_hours / efficiency

                operation_end = order_due
                operation_start = operation_end - timedelta(hours=actual_hours)

                results.append({
                    'order_id': order['order_id'],
                    'operation': len(routing) - operation_idx - 1,
                    'work_center': wc,
                    'start': operation_start,
                    'end': operation_end,
                    'hours': actual_hours
                })

                order_due = operation_start

        return pd.DataFrame(results).sort_values(['order_id', 'operation'])

    def check_capacity_feasibility(self, schedule, planning_horizon):
        """
        Check if schedule is feasible given capacity constraints

        Returns overload periods
        """

        overloads = []

        for wc in self.work_centers:
            wc_schedule = schedule[schedule['work_center'] == wc]
            capacity = self.work_centers[wc]['capacity_hours']

            # Check each day/period
            current_date = schedule['start'].min().date()
            end_date = schedule['end'].max().date()

            while current_date <= end_date:
                day_start = datetime.combine(current_date, datetime.min.time())
                day_end = day_start + timedelta(days=1)

                # Calculate load for this day
                daily_ops = wc_schedule[
                    (wc_schedule['start'] < day_end) &
                    (wc_schedule['end'] > day_start)
                ]

                load = 0
                for _, op in daily_ops.iterrows():
                    # Calculate overlap with this day
                    overlap_start = max(op['start'], day_start)
                    overlap_end = min(op['end'], day_end)
                    overlap_hours = (overlap_end - overlap_start).total_seconds() / 3600
                    load += overlap_hours

                if load > capacity:
                    overloads.append({
                        'work_center': wc,
                        'date': current_date,
                        'load': load,
                        'capacity': capacity,
                        'overload': load - capacity
                    })

                current_date += timedelta(days=1)

        return pd.DataFrame(overloads) if overloads else None

# Example usage
work_centers = {
    'Cutting': {'capacity_hours': 16, 'efficiency': 0.90},
    'Welding': {'capacity_hours': 16, 'efficiency': 0.85},
    'Assembly': {'capacity_hours': 16, 'efficiency': 0.92}
}

orders = [
    {
        'order_id': 'ORD001',
        'quantity': 100,
        'priority': 1,
        'routing': [('Cutting', 0.5), ('Welding', 0.8), ('Assembly', 1.0)]
    },
    {
        'order_id': 'ORD002',
        'quantity': 75,
        'priority': 2,
        'routing': [('Cutting', 0.6), ('Assembly', 1.2)]
    }
]

fcs = FiniteCapacityScheduler(work_centers)

# Forward schedule
start_date = datetime(2025, 2, 1, 8, 0)
forward_schedule = fcs.forward_schedule(orders, start_date)
print("Forward Schedule:")
print(forward_schedule)

# Check capacity
overloads = fcs.check_capacity_feasibility(forward_schedule, planning_horizon=30)
if overloads is not None:
    print("\nCapacity Overloads:")
    print(overloads)
else:
    print("\nSchedule is feasible - no capacity violations")
```

### Schedule Optimization with Genetic Algorithm

```python
import random

class ScheduleOptimizer:
    """
    Genetic algorithm for multi-objective scheduling
    Minimize: makespan, tardiness, setup costs
    """

    def __init__(self, jobs, machines, setup_matrix):
        self.jobs = jobs  # List of job objects
        self.machines = machines
        self.setup_matrix = setup_matrix  # Setup time between jobs

    def create_individual(self):
        """Create random job sequence (chromosome)"""
        return random.sample(self.jobs, len(self.jobs))

    def calculate_fitness(self, sequence):
        """
        Multi-objective fitness function
        Lower is better
        """
        makespan = self._calculate_makespan(sequence)
        tardiness = self._calculate_tardiness(sequence)
        setup_cost = self._calculate_setup_cost(sequence)

        # Weighted sum (normalize and weight)
        fitness = (
            0.4 * (makespan / 100) +     # Normalize to reasonable scale
            0.4 * (tardiness / 100) +
            0.2 * (setup_cost / 50)
        )

        return {
            'fitness': fitness,
            'makespan': makespan,
            'tardiness': tardiness,
            'setup_cost': setup_cost
        }

    def _calculate_makespan(self, sequence):
        """Calculate total completion time"""
        time = 0
        for job in sequence:
            time += job['processing_time']
        return time

    def _calculate_tardiness(self, sequence):
        """Calculate total tardiness (late deliveries)"""
        time = 0
        total_tardiness = 0

        for job in sequence:
            time += job['processing_time']
            tardiness = max(0, time - job['due_date'])
            total_tardiness += tardiness

        return total_tardiness

    def _calculate_setup_cost(self, sequence):
        """Calculate total setup time/cost"""
        total_setup = 0

        for i in range(len(sequence) - 1):
            current_job = sequence[i]['id']
            next_job = sequence[i + 1]['id']
            total_setup += self.setup_matrix.get((current_job, next_job), 0)

        return total_setup

    def optimize(self, population_size=100, generations=200):
        """Run genetic algorithm"""

        # Initialize population
        population = [self.create_individual() for _ in range(population_size)]

        best_solution = None
        best_fitness = float('inf')
        history = []

        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = []
            for individual in population:
                metrics = self.calculate_fitness(individual)
                fitness_scores.append(metrics['fitness'])

                if metrics['fitness'] < best_fitness:
                    best_fitness = metrics['fitness']
                    best_solution = individual.copy()
                    best_metrics = metrics

            history.append({
                'generation': generation,
                'best_fitness': best_fitness,
                'avg_fitness': sum(fitness_scores) / len(fitness_scores)
            })

            # Selection: tournament
            selected = []
            for _ in range(population_size):
                tournament = random.sample(list(zip(population, fitness_scores)), 5)
                winner = min(tournament, key=lambda x: x[1])[0]
                selected.append(winner)

            # Crossover and mutation
            next_generation = []
            for i in range(0, population_size, 2):
                parent1 = selected[i]
                parent2 = selected[i + 1] if i + 1 < population_size else selected[0]

                if random.random() < 0.8:  # Crossover rate
                    child1, child2 = self._pmx_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()

                if random.random() < 0.2:  # Mutation rate
                    child1 = self._swap_mutation(child1)
                if random.random() < 0.2:
                    child2 = self._swap_mutation(child2)

                next_generation.extend([child1, child2])

            population = next_generation[:population_size]

        return {
            'best_sequence': [j['id'] for j in best_solution],
            'metrics': best_metrics,
            'history': pd.DataFrame(history)
        }

    def _pmx_crossover(self, parent1, parent2):
        """Partially Mapped Crossover for permutation"""
        size = len(parent1)
        child1 = [None] * size
        child2 = [None] * size

        # Select crossover points
        cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

        # Copy segments
        child1[cx_point1:cx_point2] = parent1[cx_point1:cx_point2]
        child2[cx_point1:cx_point2] = parent2[cx_point1:cx_point2]

        # Fill remaining positions
        for i in range(size):
            if i < cx_point1 or i >= cx_point2:
                # Fill from parent2 for child1
                gene = parent2[i]
                while gene in child1:
                    idx = parent2.index(gene)
                    if cx_point1 <= idx < cx_point2:
                        gene = parent1[idx]
                    else:
                        break
                child1[i] = gene

                # Fill from parent1 for child2
                gene = parent1[i]
                while gene in child2:
                    idx = parent1.index(gene)
                    if cx_point1 <= idx < cx_point2:
                        gene = parent2[idx]
                    else:
                        break
                child2[i] = gene

        return child1, child2

    def _swap_mutation(self, sequence):
        """Swap two random jobs"""
        seq = sequence.copy()
        i, j = random.sample(range(len(seq)), 2)
        seq[i], seq[j] = seq[j], seq[i]
        return seq
```

---

## MRP and Production Scheduling Integration

### Material Requirements Planning (MRP)

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MRPScheduler:
    """
    MRP logic with production scheduling
    Calculate material requirements and schedule production
    """

    def __init__(self, bom, inventory, lead_times):
        """
        Parameters:
        - bom: bill of materials dict {parent: [(child, quantity)]}
        - inventory: current on-hand inventory {item: quantity}
        - lead_times: production/procurement lead times {item: days}
        """
        self.bom = bom
        self.inventory = inventory
        self.lead_times = lead_times

    def explode_bom(self, item, quantity, level=0):
        """
        Recursively explode BOM
        Returns list of (item, quantity, level) tuples
        """
        requirements = [(item, quantity, level)]

        if item in self.bom:
            for component, qty_per in self.bom[item]:
                requirements.extend(
                    self.explode_bom(component, quantity * qty_per, level + 1)
                )

        return requirements

    def calculate_net_requirements(self, gross_requirements):
        """
        Calculate net requirements considering on-hand inventory

        Parameters:
        - gross_requirements: dict {item: quantity}

        Returns net requirements and planned orders
        """
        net_requirements = {}
        planned_orders = {}

        for item, gross_qty in gross_requirements.items():
            on_hand = self.inventory.get(item, 0)
            net_qty = max(0, gross_qty - on_hand)

            if net_qty > 0:
                net_requirements[item] = net_qty
                planned_orders[item] = net_qty

                # Update inventory (consumption)
                self.inventory[item] = max(0, on_hand - gross_qty)
            else:
                # Sufficient inventory
                self.inventory[item] = on_hand - gross_qty

        return net_requirements, planned_orders

    def time_phase_mrp(self, master_schedule, planning_horizon_days=90):
        """
        Time-phased MRP calculation

        Parameters:
        - master_schedule: list of dicts {'item', 'quantity', 'due_date'}
        - planning_horizon_days: planning horizon

        Returns time-phased requirements and production schedule
        """

        start_date = min(order['due_date'] for order in master_schedule)
        end_date = start_date + timedelta(days=planning_horizon_days)

        # Create time buckets (weekly)
        time_buckets = pd.date_range(start=start_date, end=end_date, freq='W')

        # Initialize requirements by time bucket
        all_items = set()
        for order in master_schedule:
            all_items.add(order['item'])
            requirements = self.explode_bom(order['item'], order['quantity'])
            for item, qty, level in requirements:
                all_items.add(item)

        mrp_records = []

        for item in all_items:
            # Gross requirements by time bucket
            gross_req = pd.Series(0, index=time_buckets)

            for order in master_schedule:
                if order['item'] == item:
                    # Find appropriate time bucket
                    bucket = time_buckets[time_buckets >= order['due_date']][0]
                    gross_req[bucket] += order['quantity']
                else:
                    # Check if item is a component
                    requirements = self.explode_bom(order['item'], order['quantity'])
                    for req_item, qty, level in requirements:
                        if req_item == item:
                            # Offset by parent lead time
                            parent_lead = self.lead_times.get(order['item'], 0)
                            offset_date = order['due_date'] - timedelta(days=parent_lead)
                            if offset_date >= time_buckets[0]:
                                bucket = time_buckets[time_buckets >= offset_date][0]
                                gross_req[bucket] += qty

            # Calculate net requirements and planned orders
            on_hand = self.inventory.get(item, 0)

            for bucket in time_buckets:
                gross = gross_req[bucket]

                if gross > 0:
                    net = max(0, gross - on_hand)

                    if net > 0:
                        # Planned order release (offset by lead time)
                        lead_time = self.lead_times.get(item, 0)
                        release_date = bucket - timedelta(days=lead_time)

                        mrp_records.append({
                            'item': item,
                            'bucket': bucket,
                            'gross_requirement': gross,
                            'on_hand_start': on_hand,
                            'net_requirement': net,
                            'planned_order': net,
                            'release_date': release_date
                        })

                        on_hand = 0  # Inventory consumed
                    else:
                        # Sufficient inventory
                        mrp_records.append({
                            'item': item,
                            'bucket': bucket,
                            'gross_requirement': gross,
                            'on_hand_start': on_hand,
                            'net_requirement': 0,
                            'planned_order': 0,
                            'release_date': None
                        })

                        on_hand -= gross

        return pd.DataFrame(mrp_records)

# Example usage
bom = {
    'Product_A': [('Subassembly_X', 2), ('Component_Y', 4)],
    'Subassembly_X': [('Part_1', 3), ('Part_2', 1)],
}

inventory = {
    'Product_A': 10,
    'Subassembly_X': 5,
    'Component_Y': 20,
    'Part_1': 50,
    'Part_2': 30
}

lead_times = {
    'Product_A': 5,
    'Subassembly_X': 7,
    'Component_Y': 3,
    'Part_1': 10,
    'Part_2': 14
}

mrp = MRPScheduler(bom, inventory, lead_times)

# Master production schedule
master_schedule = [
    {'item': 'Product_A', 'quantity': 100, 'due_date': datetime(2025, 3, 1)},
    {'item': 'Product_A', 'quantity': 150, 'due_date': datetime(2025, 3, 15)},
]

mrp_plan = mrp.time_phase_mrp(master_schedule)
print(mrp_plan[mrp_plan['planned_order'] > 0])
```

---

## Performance Metrics

### Key Scheduling Metrics

```python
def calculate_scheduling_metrics(schedule_df, jobs_df):
    """
    Calculate comprehensive scheduling performance metrics

    Parameters:
    - schedule_df: DataFrame with actual schedule [job, start, end, machine]
    - jobs_df: DataFrame with job details [job, processing_time, due_date, priority]

    Returns dict of metrics
    """

    # Merge schedule with job details
    df = schedule_df.merge(jobs_df, on='job')

    # 1. Makespan
    makespan = df['end'].max() - df['start'].min()

    # 2. Mean flow time
    flow_times = df.groupby('job')['end'].max() - df.groupby('job')['start'].min()
    mean_flow_time = flow_times.mean()

    # 3. Tardiness
    completion_times = df.groupby('job')['end'].max()
    due_dates = df.groupby('job')['due_date'].first()
    tardiness = (completion_times - due_dates).clip(lower=0)
    total_tardiness = tardiness.sum()
    mean_tardiness = tardiness.mean()
    num_tardy = (tardiness > 0).sum()

    # 4. Utilization
    total_processing_time = df['processing_time'].sum()
    num_machines = df['machine'].nunique()
    utilization = (total_processing_time / (makespan * num_machines)) * 100

    # 5. WIP (Work in Process)
    # Average number of jobs in system
    all_times = sorted(set(df['start'].tolist() + df['end'].tolist()))
    wip_samples = []

    for t in all_times[:-1]:
        jobs_in_process = ((df['start'] <= t) & (df['end'] > t)).sum()
        wip_samples.append(jobs_in_process)

    avg_wip = np.mean(wip_samples) if wip_samples else 0

    # 6. On-time delivery rate
    otd_rate = ((tardiness == 0).sum() / len(tardiness)) * 100

    return {
        'makespan': makespan,
        'mean_flow_time': mean_flow_time,
        'total_tardiness': total_tardiness,
        'mean_tardiness': mean_tardiness,
        'num_tardy_jobs': num_tardy,
        'utilization_pct': utilization,
        'avg_wip': avg_wip,
        'on_time_delivery_pct': otd_rate
    }
```

---

## Tools & Libraries

### Python Libraries

**Optimization & Scheduling:**
- `ortools`: Google's constraint programming and optimization (CP-SAT solver)
- `pulp`: Linear programming for scheduling problems
- `pyomo`: Advanced optimization modeling
- `gekko`: Dynamic optimization and scheduling
- `docplex`: IBM CPLEX Python API
- `simanneal`: Simulated annealing metaheuristic

**Simulation:**
- `simpy`: Discrete-event simulation for manufacturing
- `salabim`: Animation and simulation
- `numpy`: Numerical computations

**Visualization:**
- `matplotlib`, `plotly`: Gantt charts and schedules
- `seaborn`: Statistical visualizations
- `gantt`: Gantt chart library

### Commercial Scheduling Software

**Advanced Planning Systems (APS):**
- **SAP APO (PP/DS)**: Production Planning & Detailed Scheduling
- **Oracle Advanced Supply Chain Planning (ASCP)**: Constraint-based planning
- **Blue Yonder (JDA)**: Manufacturing planning and scheduling
- **Kinaxis RapidResponse**: Concurrent planning and scheduling
- **Dassault Systèmes DELMIA**: Production scheduling and simulation

**Specialized Schedulers:**
- **Asprova**: APS for job shops and mixed-mode manufacturing
- **Preactor**: Finite capacity scheduling (Siemens)
- **Opcenter APS**: Advanced planning and scheduling (Siemens)
- **Ortems**: APS for complex manufacturing
- **FELIOS**: Manufacturing execution and scheduling

**MES (Manufacturing Execution Systems):**
- **SAP ME/MII**: Manufacturing execution
- **Rockwell FactoryTalk**: Production scheduling module
- **Wonderware MES**: Real-time scheduling
- **Parsec TrakSYS**: MES with scheduling

---

## Common Challenges & Solutions

### Challenge: Schedule Nervousness

**Problem:**
- Frequent schedule changes
- Disrupts shop floor
- Reduces credibility of schedule

**Solutions:**
- Freeze zones (don't reschedule near-term)
- Schedule stability metrics
- Rolling horizon approach
- Buffer times for uncertainty
- Communication protocols for changes

### Challenge: Unexpected Disruptions

**Problem:**
- Machine breakdowns
- Material shortages
- Quality issues
- Rush orders

**Solutions:**
- Dynamic rescheduling capability
- Buffer capacity at bottlenecks
- Alternative routings
- Expediting procedures
- Real-time monitoring (MES integration)
- Reactive scheduling algorithms

### Challenge: Setup Time Optimization

**Problem:**
- Significant setup/changeover times
- Trade-off between sequence optimization and due dates
- Complex setup dependencies

**Solutions:**
- Campaign scheduling (batch similar jobs)
- Setup time matrix optimization
- Sequence-dependent scheduling algorithms
- Setup time reduction (SMED - Single Minute Exchange of Die)
- Parallel setups when possible

### Challenge: Multi-Objective Conflicts

**Problem:**
- Minimize makespan vs. meet due dates
- Reduce WIP vs. keep machines busy
- Conflicting priorities

**Solutions:**
- Clearly defined priority hierarchy
- Weighted multi-objective functions
- Pareto optimization (trade-off curves)
- Simulation to test scenarios
- Collaborative planning (S&OP)

### Challenge: Limited Capacity at Bottlenecks

**Problem:**
- Bottleneck machines constrain throughput
- Non-bottleneck machines starved or blocked
- System-wide impact

**Solutions:**
- Theory of Constraints (TOC) / Drum-Buffer-Rope
- Protective buffers at bottleneck
- Subordinate non-bottleneck schedules to bottleneck
- Offload work from bottleneck (outsourcing, alternate routing)
- Increase bottleneck capacity (overtime, equipment)

### Challenge: Data Quality and Accuracy

**Problem:**
- Inaccurate processing times
- Wrong routings in system
- Outdated lead times
- Poor schedule performance

**Solutions:**
- Regular data audits and updates
- Feedback from shop floor (MES)
- Statistical analysis of actual vs. standard times
- Data governance processes
- Learning algorithms to adjust parameters

---

## Output Format

### Production Schedule Report

**Executive Summary:**
- Schedule period and horizon
- Key performance metrics (makespan, utilization, OTD)
- Critical bottlenecks or constraints
- Schedule changes from prior version

**Detailed Schedule by Work Center:**

| Work Center | Job | Operation | Start Time | End Time | Duration | Setup Time | Status |
|-------------|-----|-----------|------------|----------|----------|------------|--------|
| Cutting | J001 | OP10 | 2025-02-01 08:00 | 2025-02-01 11:30 | 3.5h | 0.5h | Scheduled |
| Cutting | J003 | OP10 | 2025-02-01 12:00 | 2025-02-01 16:00 | 4.0h | 0.5h | Scheduled |
| Welding | J001 | OP20 | 2025-02-01 12:00 | 2025-02-01 18:00 | 6.0h | 1.0h | Scheduled |

**Capacity Analysis:**

| Work Center | Available Hours | Scheduled Hours | Utilization % | Overload Hours |
|-------------|----------------|-----------------|---------------|----------------|
| Cutting | 160 | 152 | 95% | 0 |
| Welding | 160 | 168 | 105% | 8 |
| Assembly | 160 | 128 | 80% | 0 |

**Schedule Performance Metrics:**
- **Makespan**: 12 days
- **Mean Flow Time**: 6.5 days
- **Total Tardiness**: 45 hours
- **On-Time Delivery**: 87%
- **Average WIP**: 23 jobs
- **Machine Utilization**: 88%

**Gantt Chart:**
[Visual representation of schedule]

**Action Items:**
- Welding work center overloaded in Week 2 - recommend overtime or outsourcing
- Jobs J005, J012, J018 at risk of missing due dates
- Setup time on Cutting can be reduced by sequencing similar jobs together
- Material for J023 not available until Feb 5 - schedule hold

---

## Questions to Ask

If you need more context:
1. What type of manufacturing environment? (job shop, flow shop, batch, continuous)
2. How many machines/work centers? What are the routings?
3. What are the key scheduling objectives? (makespan, due dates, WIP, utilization)
4. Are there setup times or changeover constraints?
5. What is the current scheduling method and known issues?
6. What is the planning horizon and replan frequency?
7. Are there resource constraints beyond machines (labor, tooling, materials)?
8. Integration requirements with ERP/MES systems?

---

## Related Skills

- **master-production-scheduling**: For MPS and demand-driven scheduling
- **capacity-planning**: For capacity analysis and requirements planning
- **job-shop-scheduling**: For detailed JSP algorithms
- **flow-shop-scheduling**: For flow shop specific methods
- **assembly-line-balancing**: For line balancing and takt time
- **lean-manufacturing**: For pull scheduling and JIT
- **inventory-optimization**: For WIP and buffer stock optimization
- **optimization-modeling**: For mathematical scheduling models
- **constraint-programming**: For advanced constraint-based scheduling
