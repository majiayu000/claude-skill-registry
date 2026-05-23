---
name: constraint-programming
description: When the user wants to solve complex scheduling, allocation, or combinatorial problems using constraint programming (CP). Also use when the user mentions "constraint programming," "CP-SAT," "constraint satisfaction," "all-different constraint," "global constraints," "propagation," "search strategies," or when the problem has complex logical constraints, scheduling with disjunctive resources, or allocation problems. For MIP, see optimization-modeling. For metaheuristics, see metaheuristic-optimization.
---

# Constraint Programming

You are an expert in constraint programming for supply chain optimization. Your goal is to help solve complex combinatorial problems using constraint propagation, global constraints, and intelligent search strategies that excel where traditional MIP struggles.

## Initial Assessment

Before applying constraint programming, understand:

1. **Problem Characteristics**
   - Type? (scheduling, allocation, sequencing, assignment)
   - Constraints complex or logical? (if-then, all-different, etc.)
   - Variables: discrete domains?
   - Many feasibility constraints vs. optimization?

2. **Why Constraint Programming**
   - MIP formulation too weak?
   - Scheduling with disjunctive resources?
   - Complex logical constraints?
   - Need to find feasible solution quickly?

3. **Problem Size**
   - Number of variables?
   - Domain sizes?
   - Number of constraints?
   - Time limit for solving?

4. **Technical Environment**
   - CP solver available? (OR-Tools, Gecode, MiniZinc)
   - Need integrated with other systems?
   - Optimization or just feasibility?

---

## Constraint Programming Fundamentals

### Core Concepts

**Variables**: Decision variables with discrete domains
```python
# Example: Variable x can take values 1, 2, or 3
x ∈ {1, 2, 3}
```

**Constraints**: Relations that must hold between variables
```python
# Example: x + y ≤ 10
# Example: AllDifferent([x, y, z])
```

**Propagation**: Reduce variable domains based on constraints
```python
# If x + y ≤ 10 and x = 8, then propagate y ≤ 2
```

**Search**: Systematic exploration with backtracking
```python
# Try x = 1, check consistency, recurse
# If inconsistent, backtrack and try x = 2
```

---

## Job Shop Scheduling with CP

### Implementation with OR-Tools CP-SAT

```python
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict

class CPJobShopScheduler:
    """
    Job Shop Scheduling using Constraint Programming

    Problem: Schedule jobs on machines minimizing makespan
    Each job has sequence of operations on specific machines
    """

    def __init__(self,
                 jobs: List[List[Tuple[int, int]]],
                 time_limit_seconds: int = 60):
        """
        Initialize CP Job Shop Scheduler

        jobs: list of jobs, each job is list of (machine, duration)
              Example: [[(0, 3), (1, 2), (2, 2)],  # Job 0
                       [(0, 2), (2, 1), (1, 4)]]   # Job 1
        """

        self.jobs = jobs
        self.n_jobs = len(jobs)
        self.n_machines = max(max(op[0] for op in job) for job in jobs) + 1
        self.time_limit = time_limit_seconds

        # CP model
        self.model = cp_model.CpModel()

        # Decision variables
        self.job_starts = []  # [job][operation] -> start time variable
        self.job_ends = []    # [job][operation] -> end time variable
        self.job_intervals = []  # [job][operation] -> interval variable

        self.makespan = None
        self.solution = None

    def build_model(self):
        """Build CP model for job shop scheduling"""

        # Upper bound on time horizon
        horizon = sum(duration for job in self.jobs
                     for machine, duration in job)

        print(f"Building CP model...")
        print(f"Jobs: {self.n_jobs}, Machines: {self.n_machines}")
        print(f"Time Horizon: {horizon}")

        # Create variables for each operation
        for job_id, job in enumerate(self.jobs):
            job_start_vars = []
            job_end_vars = []
            job_interval_vars = []

            for op_id, (machine, duration) in enumerate(job):
                # Suffix for variable names
                suffix = f'_j{job_id}_o{op_id}_m{machine}'

                # Start time variable
                start_var = self.model.NewIntVar(0, horizon, f'start{suffix}')

                # End time variable
                end_var = self.model.NewIntVar(0, horizon, f'end{suffix}')

                # Interval variable (start, duration, end)
                interval_var = self.model.NewIntervalVar(
                    start_var, duration, end_var, f'interval{suffix}'
                )

                job_start_vars.append(start_var)
                job_end_vars.append(end_var)
                job_interval_vars.append(interval_var)

            self.job_starts.append(job_start_vars)
            self.job_ends.append(job_end_vars)
            self.job_intervals.append(job_interval_vars)

        # Precedence constraints: operations within job must be sequential
        for job_id in range(self.n_jobs):
            for op_id in range(len(self.jobs[job_id]) - 1):
                self.model.Add(
                    self.job_ends[job_id][op_id] <=
                    self.job_starts[job_id][op_id + 1]
                )

        # Disjunctive constraints: operations on same machine cannot overlap
        machine_to_intervals = [[] for _ in range(self.n_machines)]

        for job_id, job in enumerate(self.jobs):
            for op_id, (machine, duration) in enumerate(job):
                machine_to_intervals[machine].append(
                    self.job_intervals[job_id][op_id]
                )

        # NoOverlap constraint for each machine
        for machine in range(self.n_machines):
            if machine_to_intervals[machine]:
                self.model.AddNoOverlap(machine_to_intervals[machine])

        # Objective: minimize makespan
        self.makespan = self.model.NewIntVar(0, horizon, 'makespan')

        # Makespan is max end time of all jobs
        for job_id in range(self.n_jobs):
            last_op_idx = len(self.jobs[job_id]) - 1
            self.model.Add(
                self.makespan >= self.job_ends[job_id][last_op_idx]
            )

        self.model.Minimize(self.makespan)

        print("CP model built successfully!")

    def solve(self) -> Dict:
        """
        Solve the CP model

        Returns: solution dictionary
        """

        print(f"\nSolving with time limit: {self.time_limit}s...")

        # Create solver
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit

        # Optional: set number of workers for parallel solving
        solver.parameters.num_search_workers = 8

        # Solve
        status = solver.Solve(self.model)

        # Extract solution
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"\nSolution found!")
            print(f"Status: {'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'}")
            print(f"Makespan: {solver.Value(self.makespan)}")
            print(f"Solve time: {solver.WallTime():.2f}s")

            # Extract schedule
            schedule = []
            for job_id in range(self.n_jobs):
                for op_id, (machine, duration) in enumerate(self.jobs[job_id]):
                    start = solver.Value(self.job_starts[job_id][op_id])
                    end = solver.Value(self.job_ends[job_id][op_id])

                    schedule.append({
                        'job': job_id,
                        'operation': op_id,
                        'machine': machine,
                        'start': start,
                        'end': end,
                        'duration': duration
                    })

            self.solution = {
                'status': 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE',
                'makespan': solver.Value(self.makespan),
                'schedule': schedule,
                'solve_time': solver.WallTime(),
                'lower_bound': solver.BestObjectiveBound(),
                'gap': (solver.Value(self.makespan) - solver.BestObjectiveBound()) /
                       solver.Value(self.makespan) * 100
            }

            return self.solution

        else:
            print("No solution found!")
            return {
                'status': 'INFEASIBLE' if status == cp_model.INFEASIBLE else 'UNKNOWN',
                'makespan': None,
                'schedule': [],
                'solve_time': solver.WallTime()
            }

    def plot_gantt(self):
        """Visualize schedule as Gantt chart"""

        if not self.solution or not self.solution['schedule']:
            print("No solution to visualize!")
            return

        schedule = self.solution['schedule']

        fig, ax = plt.subplots(figsize=(14, 8))

        colors = plt.cm.Set3(np.linspace(0, 1, self.n_jobs))

        for task in schedule:
            ax.barh(
                task['machine'],
                task['duration'],
                left=task['start'],
                height=0.6,
                color=colors[task['job']],
                edgecolor='black',
                linewidth=1.5
            )

            # Add job label
            ax.text(
                task['start'] + task['duration'] / 2,
                task['machine'],
                f"J{task['job']}\nO{task['operation']}",
                ha='center',
                va='center',
                fontsize=9,
                fontweight='bold'
            )

        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Machine', fontsize=12)
        ax.set_title(
            f"Job Shop Schedule - Makespan: {self.solution['makespan']}",
            fontsize=14
        )
        ax.set_yticks(range(self.n_machines))
        ax.set_yticklabels([f'M{i}' for i in range(self.n_machines)])
        ax.grid(True, axis='x', alpha=0.3)

        # Legend
        legend_elements = [
            plt.Rectangle((0,0),1,1, fc=colors[i],
                         edgecolor='black', label=f'Job {i}')
            for i in range(self.n_jobs)
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    # Classic 6x6 job shop problem (Fisher and Thompson, 1963)
    jobs = [
        [(0, 1), (1, 3), (2, 6), (3, 7), (4, 3), (5, 6)],
        [(1, 8), (0, 5), (2, 10), (4, 10), (5, 10), (3, 4)],
        [(0, 5), (1, 4), (2, 8), (4, 9), (3, 1), (5, 7)],
        [(1, 5), (0, 5), (2, 5), (3, 3), (4, 8), (5, 9)],
        [(2, 9), (1, 3), (3, 5), (4, 4), (5, 3), (0, 1)],
        [(1, 3), (2, 3), (4, 9), (3, 10), (5, 4), (0, 1)]
    ]

    # Create scheduler
    scheduler = CPJobShopScheduler(jobs, time_limit_seconds=30)

    # Build and solve
    scheduler.build_model()
    result = scheduler.solve()

    # Print results
    if result['status'] in ['OPTIMAL', 'FEASIBLE']:
        print(f"\nMakespan: {result['makespan']}")
        print(f"Lower Bound: {result['lower_bound']}")
        print(f"Gap: {result['gap']:.2f}%")

        # Visualize
        scheduler.plot_gantt()
```

---

## Nurse Scheduling with Global Constraints

```python
from ortools.sat.python import cp_model
from typing import List, Dict
import pandas as pd

class NurseSchedulingCP:
    """
    Nurse Scheduling using Constraint Programming

    Constraints:
    - Shift coverage requirements
    - No overlapping shifts for same nurse
    - Rest periods between shifts
    - Fair distribution of shifts
    - Skill requirements
    """

    def __init__(self,
                 num_nurses: int,
                 num_days: int,
                 shifts: List[str],
                 requirements: Dict,
                 time_limit: int = 60):
        """
        Initialize nurse scheduling model

        num_nurses: number of nurses
        num_days: scheduling horizon
        shifts: list of shift names (e.g., ['Morning', 'Evening', 'Night'])
        requirements: dict with {shift: required_nurses_per_day}
        """

        self.num_nurses = num_nurses
        self.num_days = num_days
        self.shifts = shifts
        self.num_shifts = len(shifts)
        self.requirements = requirements
        self.time_limit = time_limit

        self.model = cp_model.CpModel()
        self.schedule_vars = {}
        self.solution = None

    def build_model(self):
        """Build CP model for nurse scheduling"""

        print(f"Building Nurse Scheduling model...")
        print(f"Nurses: {self.num_nurses}, Days: {self.num_days}")
        print(f"Shifts: {self.shifts}")

        # Decision variables: schedule[n][d][s] = 1 if nurse n works shift s on day d
        for n in range(self.num_nurses):
            for d in range(self.num_days):
                for s in range(self.num_shifts):
                    self.schedule_vars[(n, d, s)] = self.model.NewBoolVar(
                        f'schedule_n{n}_d{d}_s{s}'
                    )

        # Constraint 1: Shift coverage requirements
        for d in range(self.num_days):
            for s in range(self.num_shifts):
                shift_name = self.shifts[s]
                required = self.requirements[shift_name]

                self.model.Add(
                    sum(self.schedule_vars[(n, d, s)]
                        for n in range(self.num_nurses)) >= required
                )

        # Constraint 2: Each nurse works at most one shift per day
        for n in range(self.num_nurses):
            for d in range(self.num_days):
                self.model.Add(
                    sum(self.schedule_vars[(n, d, s)]
                        for s in range(self.num_shifts)) <= 1
                )

        # Constraint 3: Rest period between shifts
        # If nurse works night shift, cannot work next day
        night_shift_idx = self.shifts.index('Night') if 'Night' in self.shifts else -1

        if night_shift_idx >= 0:
            for n in range(self.num_nurses):
                for d in range(self.num_days - 1):
                    # If works night shift on day d, cannot work on day d+1
                    night_works = self.schedule_vars[(n, d, night_shift_idx)]

                    for s in range(self.num_shifts):
                        self.model.Add(
                            self.schedule_vars[(n, d + 1, s)] == 0
                        ).OnlyEnforceIf(night_works)

        # Constraint 4: Fair distribution of shifts
        # Each nurse works similar number of shifts
        min_shifts_per_nurse = (self.num_days * sum(self.requirements.values())) // self.num_nurses - 2
        max_shifts_per_nurse = min_shifts_per_nurse + 4

        for n in range(self.num_nurses):
            total_shifts = sum(
                self.schedule_vars[(n, d, s)]
                for d in range(self.num_days)
                for s in range(self.num_shifts)
            )
            self.model.Add(total_shifts >= min_shifts_per_nurse)
            self.model.Add(total_shifts <= max_shifts_per_nurse)

        # Constraint 5: Weekend constraints (optional)
        # Try to give nurses complete weekends off
        for n in range(self.num_nurses):
            for week in range(self.num_days // 7):
                saturday = week * 7 + 5
                sunday = week * 7 + 6

                if saturday < self.num_days and sunday < self.num_days:
                    saturday_works = sum(
                        self.schedule_vars[(n, saturday, s)]
                        for s in range(self.num_shifts)
                    )
                    sunday_works = sum(
                        self.schedule_vars[(n, sunday, s)]
                        for s in range(self.num_shifts)
                    )

                    # If works Saturday, more likely to work Sunday
                    # This is soft constraint - implement with objectives

        print("Model built successfully!")

    def solve(self) -> Dict:
        """Solve the model"""

        print(f"\nSolving with time limit: {self.time_limit}s...")

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit
        solver.parameters.num_search_workers = 4

        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"Solution found!")
            print(f"Status: {'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'}")

            # Extract schedule
            schedule = []
            for n in range(self.num_nurses):
                for d in range(self.num_days):
                    for s in range(self.num_shifts):
                        if solver.Value(self.schedule_vars[(n, d, s)]) == 1:
                            schedule.append({
                                'nurse': n,
                                'day': d,
                                'shift': self.shifts[s]
                            })

            self.solution = {
                'status': 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE',
                'schedule': schedule,
                'solve_time': solver.WallTime()
            }

            return self.solution
        else:
            return {
                'status': 'INFEASIBLE',
                'schedule': [],
                'solve_time': solver.WallTime()
            }

    def print_schedule(self):
        """Print schedule in readable format"""

        if not self.solution or not self.solution['schedule']:
            print("No solution to print!")
            return

        df_data = []
        for item in self.solution['schedule']:
            df_data.append({
                'Nurse': f"N{item['nurse']}",
                'Day': item['day'],
                'Shift': item['shift']
            })

        df = pd.DataFrame(df_data)

        # Pivot table
        pivot = df.pivot_table(
            index='Nurse',
            columns='Day',
            values='Shift',
            aggfunc='first',
            fill_value='-'
        )

        print("\nNurse Schedule:")
        print(pivot)


# Example usage
if __name__ == "__main__":
    # 7 nurses, 14 days, 3 shifts
    scheduler = NurseSchedulingCP(
        num_nurses=7,
        num_days=14,
        shifts=['Morning', 'Evening', 'Night'],
        requirements={
            'Morning': 2,
            'Evening': 2,
            'Night': 1
        },
        time_limit=30
    )

    scheduler.build_model()
    result = scheduler.solve()

    if result['status'] in ['OPTIMAL', 'FEASIBLE']:
        scheduler.print_schedule()
```

---

## Global Constraints

### AllDifferent Constraint

```python
# Ensure all variables take different values
# Example: Assign workers to tasks, each worker gets different task
model.AddAllDifferent([task[worker] for worker in workers])
```

### Cumulative Constraint

```python
# Resource capacity constraint
# Sum of resource usage at any time ≤ capacity
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Tasks with resource requirements
tasks = [...]
resource_usage = [...]
capacity = 10

# Create interval variables
intervals = []
demands = []

for i, (start, duration, demand) in enumerate(tasks):
    start_var = model.NewIntVar(0, 100, f'start_{i}')
    end_var = model.NewIntVar(0, 100, f'end_{i}')
    interval = model.NewIntervalVar(start_var, duration, end_var, f'interval_{i}')

    intervals.append(interval)
    demands.append(demand)

# Cumulative constraint
model.AddCumulative(intervals, demands, capacity)
```

### Circuit Constraint

```python
# Create Hamiltonian circuit (TSP, VRP)
# Variables represent next node in tour
model.AddCircuit([(i, next[i]) for i in nodes])
```

### Table Constraint

```python
# Variable tuple must match one of allowed tuples
# Example: (x, y, z) must be in {(1,2,3), (2,3,4), (3,4,5)}
allowed_tuples = [(1,2,3), (2,3,4), (3,4,5)]
model.AddAllowedAssignments([x, y, z], allowed_tuples)
```

### Reservoir Constraint

```python
# Track resource level over time (inventory, battery level)
# Starts at initial level, changes with events, stays within bounds
model.AddReservoirConstraint(
    times=[t1, t2, t3],
    demands=[d1, d2, d3],
    min_level=0,
    max_level=100
)
```

---

## Search Strategies

### Variable Selection

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# Define search strategy
model.AddDecisionStrategy(
    variables=[x, y, z],
    var_selection_strategy=cp_model.CHOOSE_FIRST,
    value_selection_strategy=cp_model.SELECT_MIN_VALUE
)

# Variable selection strategies:
# - CHOOSE_FIRST: static order
# - CHOOSE_LOWEST_MIN: smallest lower bound
# - CHOOSE_HIGHEST_MAX: largest upper bound
# - CHOOSE_MIN_DOMAIN_SIZE: smallest domain
```

### Large Neighborhood Search (LNS)

```python
# OR-Tools uses LNS automatically, but can customize
solver.parameters.num_search_workers = 8  # Parallel search
solver.parameters.log_search_progress = True

# Focus on improving incumbent
solver.parameters.optimize_with_core = True
```

---

## CP vs MIP: When to Use CP

**Use CP When:**
- Complex logical constraints (if-then, reified constraints)
- Scheduling with disjunctive resources
- Finding feasible solution is primary goal
- Symmetry breaking difficult in MIP
- Need for global constraints (AllDifferent, Circuit)

**Use MIP When:**
- Linear objective and constraints
- Need dual bounds and gaps
- Warm starting important
- Well-studied problem class (network flow, etc.)

**Use Hybrid When:**
- Large problem with both CP and MIP characteristics
- CP for subproblem, MIP for master
- Decomposition possible

---

## Tools & Libraries

### Python CP Libraries

**OR-Tools CP-SAT:**
- Google's constraint solver
- Excellent performance
- Free and open-source
- Strong MIP-style search

**MiniZinc:**
- Modeling language for CP
- Multiple solver backends
- Good for prototyping

**python-constraint:**
- Simple CP library
- Good for learning
- Limited scalability

### Commercial CP Solvers

**IBM CPLEX CP Optimizer:**
- Industrial-strength CP
- Integrated with CPLEX
- Scheduling-focused

**Gecode:**
- Open-source C++ CP toolkit
- Highly customizable
- Python bindings available

---

## Common Challenges & Solutions

### Challenge: Solution Quality Varies

**Problem**: CP finds feasible solution but quality varies run-to-run

**Solutions:**
- Run multiple times with different seeds
- Use LNS (large neighborhood search)
- Provide good initial solution
- Tune search strategies
- Use optimization objective (not just feasibility)

### Challenge: No Solution Found

**Problem**: Solver returns infeasible or times out

**Solutions:**
- Relax constraints progressively
- Start with smaller problem
- Add solution hints
- Check for conflicting constraints
- Use relaxation variables with penalties

### Challenge: Slow Performance

**Problem**: Solver takes too long

**Solutions:**
- Add implied constraints (redundant but helpful)
- Better search strategy
- Break symmetries
- Use cumulative/global constraints
- Parallelize search
- Time-limited solving

---

## Best Practices

1. **Model Incrementally**: Start simple, add constraints gradually
2. **Use Global Constraints**: More efficient than decomposition
3. **Break Symmetries**: Add symmetry-breaking constraints
4. **Provide Hints**: Give solver good starting solution
5. **Tune Search**: Experiment with variable/value selection
6. **Monitor Progress**: Log search progress
7. **Set Time Limits**: Don't wait forever for optimality
8. **Test on Small Instances**: Verify model correctness

---

## Output Format

### CP Solution Report

**Executive Summary:**
- Problem solved
- Solution status (optimal/feasible/infeasible)
- Key results

**Problem Details:**
- Variables: count and types
- Constraints: count by type
- Global constraints used

**Solution Quality:**

| Metric | Value |
|--------|-------|
| Status | OPTIMAL |
| Objective | 145 |
| Lower Bound | 145 |
| Gap | 0% |
| Solve Time | 12.3s |
| Failures | 1,234 |
| Branches | 5,678 |

**Solution:**
- Detailed schedule/assignment
- Constraint satisfaction verification
- Resource utilization

---

## Questions to Ask

1. What type of problem? (scheduling, allocation, routing)
2. What makes this hard? (logical constraints, disjunctive resources)
3. Is finding any feasible solution the goal, or optimization?
4. What are the key constraints?
5. How large is the problem?
6. Time limit for solving?
7. Need optimality guarantee or good-enough solution?

---

## Related Skills

- **optimization-modeling**: For MIP approaches
- **metaheuristic-optimization**: For large-scale heuristics
- **production-scheduling**: For manufacturing scheduling
- **route-optimization**: For routing problems
- **workforce-scheduling**: For labor scheduling
- **assembly-line-balancing**: For line balancing
- **job-shop-scheduling**: For job shop problems
