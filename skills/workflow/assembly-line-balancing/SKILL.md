---
name: assembly-line-balancing
description: When the user wants to balance assembly lines, assign tasks to workstations, calculate takt time, or optimize line efficiency. Also use when the user mentions "line balancing," "workstation assignment," "takt time," "cycle time balancing," "precedence constraints," "task allocation," "assembly line optimization," "mixed-model balancing," or "U-shaped line." For process optimization, see process-optimization. For production scheduling, see production-scheduling.
---

# Assembly Line Balancing

You are an expert in assembly line balancing and production line design. Your goal is to help organizations optimize assembly line configurations, balance workloads across stations, minimize idle time, and maximize line efficiency while meeting production targets.

## Initial Assessment

Before balancing assembly lines, understand:

1. **Line Configuration**
   - Type of line? (single-model, mixed-model, multi-model)
   - Current line layout? (straight, U-shaped, two-sided)
   - Number of workstations?
   - Current cycle times and bottlenecks?

2. **Product & Tasks**
   - Task list with processing times?
   - Precedence relationships between tasks?
   - Task zoning constraints? (must be together/separate)
   - Equipment or skill requirements?

3. **Production Requirements**
   - Target production volume (units/day)?
   - Available working time per shift?
   - Takt time requirements?
   - Quality requirements?

4. **Constraints**
   - Fixed workstation count or flexible?
   - Space constraints?
   - Ergonomic considerations?
   - Budget for changes?

---

## Assembly Line Balancing Framework

### Problem Formulation

**Assembly Line Balancing Problem (ALBP):**

**Given:**
- Set of tasks T = {t₁, t₂, ..., tₙ}
- Task processing times: p(t)
- Precedence constraints: task i must precede task j
- Cycle time C (takt time)
- Number of workstations m

**Objectives:**
- **Type-1 (ALBP-1)**: Minimize number of workstations for given cycle time
- **Type-2 (ALBP-2)**: Minimize cycle time for given number of workstations
- **Type-E**: Maximize line efficiency

**Constraints:**
- Precedence constraints must be satisfied
- Workstation load ≤ cycle time
- Each task assigned to exactly one workstation

### Line Balancing Metrics

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

class LineBalancingMetrics:
    """
    Calculate assembly line balancing metrics
    """

    def __init__(self, workstation_times, cycle_time):
        """
        Parameters:
        - workstation_times: list of total times at each workstation
        - cycle_time: target cycle time (takt time)
        """
        self.workstation_times = np.array(workstation_times)
        self.cycle_time = cycle_time
        self.num_workstations = len(workstation_times)

    def calculate_metrics(self):
        """
        Calculate comprehensive line balancing metrics
        """

        # Total task time
        total_time = self.workstation_times.sum()

        # Theoretical minimum workstations
        min_workstations = np.ceil(total_time / self.cycle_time)

        # Line efficiency (balance efficiency)
        line_efficiency = (total_time / (self.num_workstations * self.cycle_time)) * 100

        # Balance delay (idle time %)
        balance_delay = 100 - line_efficiency

        # Smoothness index (variability in workstation times)
        # Lower is better
        max_time = self.workstation_times.max()
        smoothness_index = np.sqrt(
            np.sum((max_time - self.workstation_times) ** 2)
        )

        # Idle time at each workstation
        idle_times = self.cycle_time - self.workstation_times

        # Bottleneck identification
        bottleneck_station = np.argmax(self.workstation_times)
        bottleneck_time = self.workstation_times[bottleneck_station]

        return {
            'total_task_time': total_time,
            'cycle_time': self.cycle_time,
            'num_workstations': self.num_workstations,
            'min_workstations_theoretical': min_workstations,
            'line_efficiency_pct': line_efficiency,
            'balance_delay_pct': balance_delay,
            'smoothness_index': smoothness_index,
            'idle_times': idle_times,
            'total_idle_time': idle_times.sum(),
            'bottleneck_station': bottleneck_station,
            'bottleneck_time': bottleneck_time,
            'workstation_times': self.workstation_times
        }

    def calculate_takt_time(self, demand_per_day, available_time_minutes):
        """
        Calculate takt time = available time / customer demand

        Parameters:
        - demand_per_day: required production volume
        - available_time_minutes: working time available per day

        Returns takt time in minutes
        """

        takt_time = available_time_minutes / demand_per_day

        return {
            'demand_per_day': demand_per_day,
            'available_time_minutes': available_time_minutes,
            'takt_time_minutes': takt_time,
            'takt_time_seconds': takt_time * 60,
            'max_units_per_day': available_time_minutes / takt_time
        }

    def plot_balance_chart(self, metrics):
        """
        Visualize line balance with bar chart
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Workstation times vs cycle time
        stations = [f'WS{i+1}' for i in range(self.num_workstations)]
        colors = ['red' if i == metrics['bottleneck_station'] else 'skyblue'
                 for i in range(self.num_workstations)]

        bars = ax1.bar(stations, self.workstation_times, color=colors,
                      edgecolor='black', linewidth=1.5, alpha=0.7)

        # Cycle time line
        ax1.axhline(self.cycle_time, color='green', linestyle='--',
                   linewidth=2, label=f'Cycle Time ({self.cycle_time:.1f} min)')

        # Add value labels
        for i, (bar, time) in enumerate(zip(bars, self.workstation_times)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time:.1f}', ha='center', va='bottom', fontweight='bold')

            # Add idle time annotation
            idle = self.cycle_time - time
            if idle > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'(idle: {idle:.1f})', ha='center', va='bottom',
                        fontsize=9, color='red')

        ax1.set_xlabel('Workstation', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Time (minutes)', fontsize=12, fontweight='bold')
        ax1.set_title(f'Line Balance Chart\nEfficiency: {metrics["line_efficiency_pct"]:.1f}% (Red = Bottleneck)',
                     fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Idle time distribution
        idle_times = metrics['idle_times']
        ax2.bar(stations, idle_times, color='lightcoral', edgecolor='black',
               linewidth=1.5, alpha=0.7)

        ax2.set_xlabel('Workstation', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Idle Time (minutes)', fontsize=12, fontweight='bold')
        ax2.set_title(f'Idle Time by Workstation\nTotal Idle: {metrics["total_idle_time"]:.1f} min',
                     fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        return fig

# Example usage
workstation_times = [5.2, 6.8, 5.5, 6.9, 5.1, 6.5]  # minutes
cycle_time = 7.0  # target cycle time

metrics_calc = LineBalancingMetrics(workstation_times, cycle_time)

# Calculate metrics
metrics = metrics_calc.calculate_metrics()

print("Line Balancing Metrics:")
print(f"  Number of Workstations: {metrics['num_workstations']}")
print(f"  Theoretical Minimum: {metrics['min_workstations_theoretical']:.0f}")
print(f"  Cycle Time: {metrics['cycle_time']:.1f} minutes")
print(f"  Total Task Time: {metrics['total_task_time']:.1f} minutes")
print(f"  Line Efficiency: {metrics['line_efficiency_pct']:.1f}%")
print(f"  Balance Delay: {metrics['balance_delay_pct']:.1f}%")
print(f"  Smoothness Index: {metrics['smoothness_index']:.2f}")
print(f"  Total Idle Time: {metrics['total_idle_time']:.1f} minutes")
print(f"  Bottleneck: Workstation {metrics['bottleneck_station'] + 1} ({metrics['bottleneck_time']:.1f} min)")

# Takt time calculation
takt = metrics_calc.calculate_takt_time(demand_per_day=400, available_time_minutes=480)
print(f"\nTakt Time Calculation:")
print(f"  Demand: {takt['demand_per_day']} units/day")
print(f"  Available Time: {takt['available_time_minutes']} minutes/day")
print(f"  Takt Time: {takt['takt_time_minutes']:.2f} minutes ({takt['takt_time_seconds']:.0f} seconds)")

# Plot
fig = metrics_calc.plot_balance_chart(metrics)
plt.show()
```

---

## Line Balancing Algorithms

### Ranked Positional Weight (RPW) Method

```python
class LineBalancer:
    """
    Assembly line balancing using heuristic algorithms
    """

    def __init__(self, tasks, precedence_graph, cycle_time):
        """
        Parameters:
        - tasks: dict {task_id: processing_time}
        - precedence_graph: dict {task_id: [list of immediate predecessors]}
        - cycle_time: target cycle time (takt time)

        Example:
        tasks = {'A': 3.0, 'B': 2.5, 'C': 4.0, ...}
        precedence_graph = {'A': [], 'B': ['A'], 'C': ['A'], ...}
        """
        self.tasks = tasks
        self.precedence = precedence_graph
        self.cycle_time = cycle_time

    def calculate_positional_weights(self):
        """
        Calculate positional weight for each task
        Positional weight = task time + sum of all following tasks' times
        """

        # Build successor relationships
        successors = defaultdict(list)
        for task, predecessors in self.precedence.items():
            for pred in predecessors:
                successors[pred].append(task)

        # Calculate positional weights (recursive)
        positional_weights = {}

        def calc_weight(task):
            if task in positional_weights:
                return positional_weights[task]

            # Weight = own time + sum of all successors' weights
            weight = self.tasks[task]
            for successor in successors[task]:
                weight += calc_weight(successor)

            positional_weights[task] = weight
            return weight

        # Calculate for all tasks
        for task in self.tasks:
            calc_weight(task)

        return positional_weights

    def rpw_method(self):
        """
        Ranked Positional Weight method for line balancing

        Returns workstation assignments
        """

        # Calculate positional weights
        weights = self.calculate_positional_weights()

        # Sort tasks by positional weight (descending)
        sorted_tasks = sorted(weights.items(), key=lambda x: x[1], reverse=True)

        # Initialize workstations
        workstations = []
        current_station = []
        current_station_time = 0
        assigned_tasks = set()

        # Assign tasks to workstations
        for task, weight in sorted_tasks:
            # Check if task can be assigned (predecessors already assigned)
            predecessors = self.precedence[task]
            if not all(pred in assigned_tasks for pred in predecessors):
                continue  # Skip this task for now

            # Check if task fits in current station
            task_time = self.tasks[task]

            if current_station_time + task_time <= self.cycle_time:
                # Assign to current station
                current_station.append(task)
                current_station_time += task_time
                assigned_tasks.add(task)
            else:
                # Start new station
                if current_station:
                    workstations.append({
                        'tasks': current_station.copy(),
                        'time': current_station_time
                    })

                current_station = [task]
                current_station_time = task_time
                assigned_tasks.add(task)

        # Add last station
        if current_station:
            workstations.append({
                'tasks': current_station.copy(),
                'time': current_station_time
            })

        # If not all tasks assigned, need to iterate again
        # (For simplicity, this basic version may not assign all tasks in one pass)
        unassigned = set(self.tasks.keys()) - assigned_tasks

        # Try to assign remaining tasks
        while unassigned:
            assigned_this_round = []

            for task in list(unassigned):
                predecessors = self.precedence[task]
                if not all(pred in assigned_tasks for pred in predecessors):
                    continue

                task_time = self.tasks[task]

                # Try to fit in existing stations
                fitted = False
                for station in workstations:
                    if station['time'] + task_time <= self.cycle_time:
                        station['tasks'].append(task)
                        station['time'] += task_time
                        assigned_tasks.add(task)
                        assigned_this_round.append(task)
                        fitted = True
                        break

                # If not fitted, create new station
                if not fitted:
                    workstations.append({
                        'tasks': [task],
                        'time': task_time
                    })
                    assigned_tasks.add(task)
                    assigned_this_round.append(task)

            # Remove assigned tasks from unassigned
            for task in assigned_this_round:
                unassigned.remove(task)

            # If nothing assigned this round, break to avoid infinite loop
            if not assigned_this_round:
                break

        return {
            'workstations': workstations,
            'num_workstations': len(workstations),
            'unassigned_tasks': list(unassigned)
        }

    def largest_candidate_rule(self):
        """
        Largest Candidate Rule (LCR) heuristic
        Assign longest task that fits and satisfies precedence
        """

        workstations = []
        current_station = []
        current_station_time = 0
        assigned_tasks = set()
        remaining_tasks = set(self.tasks.keys())

        while remaining_tasks:
            # Find eligible tasks (predecessors assigned)
            eligible = [
                task for task in remaining_tasks
                if all(pred in assigned_tasks for pred in self.precedence[task])
            ]

            if not eligible:
                break  # No eligible tasks (shouldn't happen with valid precedence)

            # Sort eligible by processing time (longest first)
            eligible_sorted = sorted(eligible, key=lambda t: self.tasks[t], reverse=True)

            # Try to assign largest task that fits
            assigned = False
            for task in eligible_sorted:
                task_time = self.tasks[task]

                if current_station_time + task_time <= self.cycle_time:
                    # Assign to current station
                    current_station.append(task)
                    current_station_time += task_time
                    assigned_tasks.add(task)
                    remaining_tasks.remove(task)
                    assigned = True
                    break

            # If no task fits, start new station
            if not assigned:
                if current_station:
                    workstations.append({
                        'tasks': current_station.copy(),
                        'time': current_station_time
                    })

                # Assign smallest eligible task to new station
                task = min(eligible_sorted, key=lambda t: self.tasks[t])
                task_time = self.tasks[task]

                current_station = [task]
                current_station_time = task_time
                assigned_tasks.add(task)
                remaining_tasks.remove(task)

        # Add last station
        if current_station:
            workstations.append({
                'tasks': current_station.copy(),
                'time': current_station_time
            })

        return {
            'workstations': workstations,
            'num_workstations': len(workstations)
        }

    def compare_solutions(self, solution1, solution2):
        """Compare two line balancing solutions"""

        # Calculate metrics for both
        times1 = [ws['time'] for ws in solution1['workstations']]
        times2 = [ws['time'] for ws in solution2['workstations']]

        metrics1 = LineBalancingMetrics(times1, self.cycle_time).calculate_metrics()
        metrics2 = LineBalancingMetrics(times2, self.cycle_time).calculate_metrics()

        comparison = pd.DataFrame({
            'Metric': ['Workstations', 'Efficiency %', 'Balance Delay %', 'Smoothness Index'],
            'Solution 1': [
                metrics1['num_workstations'],
                f"{metrics1['line_efficiency_pct']:.1f}",
                f"{metrics1['balance_delay_pct']:.1f}",
                f"{metrics1['smoothness_index']:.2f}"
            ],
            'Solution 2': [
                metrics2['num_workstations'],
                f"{metrics2['line_efficiency_pct']:.1f}",
                f"{metrics2['balance_delay_pct']:.1f}",
                f"{metrics2['smoothness_index']:.2f}"
            ]
        })

        return comparison

# Example usage
tasks = {
    'A': 3.0,
    'B': 2.5,
    'C': 4.0,
    'D': 1.5,
    'E': 3.5,
    'F': 2.0,
    'G': 3.0,
    'H': 2.5,
    'I': 1.5,
    'J': 2.0
}

precedence = {
    'A': [],
    'B': ['A'],
    'C': ['A'],
    'D': ['B'],
    'E': ['B', 'C'],
    'F': ['D'],
    'G': ['E'],
    'H': ['F', 'G'],
    'I': ['H'],
    'J': ['I']
}

cycle_time = 8.0  # minutes

balancer = LineBalancer(tasks, precedence, cycle_time)

# Calculate positional weights
weights = balancer.calculate_positional_weights()
print("Positional Weights:")
for task, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
    print(f"  Task {task}: {weight:.1f}")

# RPW method
print("\n" + "="*50)
print("Ranked Positional Weight (RPW) Method")
print("="*50)
rpw_solution = balancer.rpw_method()

print(f"\nNumber of Workstations: {rpw_solution['num_workstations']}")
for i, ws in enumerate(rpw_solution['workstations']):
    print(f"  Station {i+1}: {ws['tasks']} - Time: {ws['time']:.1f} min")

if rpw_solution['unassigned_tasks']:
    print(f"  Unassigned: {rpw_solution['unassigned_tasks']}")

# Largest Candidate Rule
print("\n" + "="*50)
print("Largest Candidate Rule (LCR)")
print("="*50)
lcr_solution = balancer.largest_candidate_rule()

print(f"\nNumber of Workstations: {lcr_solution['num_workstations']}")
for i, ws in enumerate(lcr_solution['workstations']):
    print(f"  Station {i+1}: {ws['tasks']} - Time: {ws['time']:.1f} min")

# Compare solutions
print("\n" + "="*50)
print("Solution Comparison")
print("="*50)
comparison = balancer.compare_solutions(rpw_solution, lcr_solution)
print(comparison)
```

---

## Mixed-Model Line Balancing

### Multi-Product Line Balancing

```python
class MixedModelLineBalancer:
    """
    Mixed-model assembly line balancing
    Balance line for multiple product variants
    """

    def __init__(self, products, cycle_time):
        """
        Parameters:
        - products: dict {product_id: {'tasks': {task: time}, 'demand_pct': %}}
        - cycle_time: target cycle time

        Example:
        products = {
            'Model_A': {
                'tasks': {'A': 3.0, 'B': 2.5, 'C': 4.0},
                'demand_pct': 0.50
            },
            'Model_B': {
                'tasks': {'A': 2.5, 'B': 3.0, 'D': 3.5},
                'demand_pct': 0.30
            },
            'Model_C': {
                'tasks': {'A': 3.5, 'C': 3.0, 'D': 4.0},
                'demand_pct': 0.20
            }
        }
        """
        self.products = products
        self.cycle_time = cycle_time

    def calculate_average_task_times(self):
        """
        Calculate weighted average task times across all products
        """

        all_tasks = set()
        for product in self.products.values():
            all_tasks.update(product['tasks'].keys())

        avg_times = {}

        for task in all_tasks:
            weighted_time = 0
            for product in self.products.values():
                task_time = product['tasks'].get(task, 0)  # 0 if task not in product
                weighted_time += task_time * product['demand_pct']

            avg_times[task] = weighted_time

        return avg_times

    def balance_for_average(self):
        """
        Balance line using average task times
        """

        avg_times = self.calculate_average_task_times()

        # Simple greedy assignment
        workstations = []
        current_station = []
        current_time = 0

        # Sort tasks by time (longest first)
        sorted_tasks = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)

        for task, time in sorted_tasks:
            if current_time + time <= self.cycle_time:
                current_station.append(task)
                current_time += time
            else:
                if current_station:
                    workstations.append({
                        'tasks': current_station.copy(),
                        'avg_time': current_time
                    })

                current_station = [task]
                current_time = time

        if current_station:
            workstations.append({
                'tasks': current_station.copy(),
                'avg_time': current_time
            })

        return {
            'workstations': workstations,
            'num_workstations': len(workstations),
            'avg_task_times': avg_times
        }

    def analyze_product_balance(self, solution):
        """
        Analyze balance for each product variant
        """

        product_analysis = {}

        for product_id, product_data in self.products.items():
            workstation_times = []

            for ws in solution['workstations']:
                ws_time = sum(product_data['tasks'].get(task, 0) for task in ws['tasks'])
                workstation_times.append(ws_time)

            metrics = LineBalancingMetrics(workstation_times, self.cycle_time).calculate_metrics()

            product_analysis[product_id] = {
                'demand_pct': product_data['demand_pct'] * 100,
                'efficiency': metrics['line_efficiency_pct'],
                'balance_delay': metrics['balance_delay_pct'],
                'workstation_times': workstation_times
            }

        return pd.DataFrame(product_analysis).T

# Example usage
products = {
    'Model_A': {
        'tasks': {'Task1': 3.0, 'Task2': 2.5, 'Task3': 4.0, 'Task4': 2.0},
        'demand_pct': 0.50
    },
    'Model_B': {
        'tasks': {'Task1': 2.5, 'Task2': 3.0, 'Task3': 3.5, 'Task5': 2.5},
        'demand_pct': 0.30
    },
    'Model_C': {
        'tasks': {'Task1': 3.5, 'Task3': 3.0, 'Task4': 2.5, 'Task5': 3.0},
        'demand_pct': 0.20
    }
}

mixed_balancer = MixedModelLineBalancer(products, cycle_time=10.0)

# Calculate average times
avg_times = mixed_balancer.calculate_average_task_times()
print("Average Task Times (weighted by demand):")
for task, time in sorted(avg_times.items()):
    print(f"  {task}: {time:.2f} minutes")

# Balance line
solution = mixed_balancer.balance_for_average()
print(f"\nMixed-Model Line Balance:")
print(f"  Number of Workstations: {solution['num_workstations']}")

for i, ws in enumerate(solution['workstations']):
    print(f"  Station {i+1}: {ws['tasks']} - Avg Time: {ws['avg_time']:.2f} min")

# Analyze each product
print("\nProduct-Specific Analysis:")
product_analysis = mixed_balancer.analyze_product_balance(solution)
print(product_analysis)
```

---

## Advanced Line Configurations

### U-Shaped Line Analysis

```python
class UShapedLineAnalyzer:
    """
    Analyze U-shaped assembly line configurations
    Benefits: Operator flexibility, reduced material handling
    """

    def __init__(self, tasks, num_operators):
        """
        Parameters:
        - tasks: list of task times in sequence
        - num_operators: number of operators
        """
        self.tasks = tasks
        self.num_operators = num_operators
        self.total_work_content = sum(tasks)

    def calculate_configuration(self):
        """
        Calculate U-shaped line configuration

        In U-shaped line:
        - Operators can work on both sides
        - Entrance and exit are close together
        - Flexible assignment possible
        """

        # Target work per operator
        target_work_per_operator = self.total_work_content / self.num_operators

        # Assign tasks to operators
        assignments = []
        current_operator = []
        current_workload = 0
        operator_num = 1

        for i, task_time in enumerate(self.tasks):
            if current_workload + task_time <= target_work_per_operator * 1.2:  # 20% tolerance
                current_operator.append(i+1)
                current_workload += task_time
            else:
                assignments.append({
                    'operator': operator_num,
                    'tasks': current_operator.copy(),
                    'workload': current_workload
                })

                operator_num += 1
                current_operator = [i+1]
                current_workload = task_time

        # Add last operator
        if current_operator:
            assignments.append({
                'operator': operator_num,
                'tasks': current_operator.copy(),
                'workload': current_workload
            })

        # Calculate metrics
        workloads = [a['workload'] for a in assignments]
        cycle_time = max(workloads)
        efficiency = (self.total_work_content / (len(assignments) * cycle_time)) * 100

        return {
            'assignments': assignments,
            'actual_operators': len(assignments),
            'target_operators': self.num_operators,
            'cycle_time': cycle_time,
            'efficiency_pct': efficiency,
            'target_work_per_operator': target_work_per_operator
        }

    def compare_to_straight_line(self, straight_line_cycle_time):
        """
        Compare U-shaped benefits vs. straight line

        U-shaped advantages:
        - Reduced walking distance
        - Better communication
        - Easier material flow
        - More flexible staffing
        """

        u_config = self.calculate_configuration()

        comparison = {
            'straight_line_cycle_time': straight_line_cycle_time,
            'u_shaped_cycle_time': u_config['cycle_time'],
            'improvement_pct': ((straight_line_cycle_time - u_config['cycle_time']) /
                               straight_line_cycle_time) * 100,
            'space_reduction_pct': 30,  # Typical space reduction
            'material_handling_reduction_pct': 40  # Typical reduction
        }

        return comparison

# Example usage
tasks = [2.5, 3.0, 2.0, 4.0, 3.5, 2.5, 3.0, 2.0, 3.5, 2.5]

u_line = UShapedLineAnalyzer(tasks, num_operators=4)

config = u_line.calculate_configuration()

print("U-Shaped Line Configuration:")
print(f"  Target Operators: {config['target_operators']}")
print(f"  Actual Operators: {config['actual_operators']}")
print(f"  Cycle Time: {config['cycle_time']:.2f} minutes")
print(f"  Line Efficiency: {config['efficiency_pct']:.1f}%")

print("\nOperator Assignments:")
for assignment in config['assignments']:
    print(f"  Operator {assignment['operator']}: Tasks {assignment['tasks']} - Workload: {assignment['workload']:.2f} min")

# Compare to straight line
comparison = u_line.compare_to_straight_line(straight_line_cycle_time=7.5)
print("\nU-Shaped vs. Straight Line Comparison:")
print(f"  Straight Line Cycle Time: {comparison['straight_line_cycle_time']:.2f} min")
print(f"  U-Shaped Cycle Time: {comparison['u_shaped_cycle_time']:.2f} min")
print(f"  Cycle Time Improvement: {comparison['improvement_pct']:.1f}%")
print(f"  Space Reduction: ~{comparison['space_reduction_pct']}%")
print(f"  Material Handling Reduction: ~{comparison['material_handling_reduction_pct']}%")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: Linear programming for line balancing
- `ortools`: Google optimization for assignment problems
- `scipy.optimize`: Optimization algorithms
- `networkx`: Precedence graph analysis

**Analysis:**
- `numpy`, `pandas`: Data analysis
- `matplotlib`, `seaborn`: Visualization

### Commercial Software

**Line Balancing:**
- **Arena**: Simulation with line balancing
- **FlexSim**: 3D simulation and balancing
- **Tecnomatix**: Siemens line balancing tools
- **Delmia**: Dassault line simulation
- **AutoMod**: Line simulation and optimization

**Industrial Engineering:**
- **ProModel**: Line balancing module
- **MOST/MTM**: Methods-Time Measurement

---

## Common Challenges & Solutions

### Challenge: Precedence Constraints

**Problem:**
- Complex task dependencies
- Limited flexibility in assignment
- Hard to achieve good balance

**Solutions:**
- Analyze if precedence can be relaxed
- Consider task splitting (divide complex tasks)
- Use parallel workstations for bottlenecks
- Precedence-aware algorithms (RPW method)

### Challenge: High Task Time Variability

**Problem:**
- Some tasks much longer than others
- Difficult to balance evenly
- Bottlenecks created by long tasks

**Solutions:**
- Task splitting (break long tasks into parts)
- Parallel workstations for long tasks
- Skill-based assignment (faster workers on long tasks)
- Work element standardization
- Automation of long/difficult tasks

### Challenge: Mixed-Model Production

**Problem:**
- Different products have different task times
- Balance good for one product, poor for another
- Frequent model changes

**Solutions:**
- Balance for average (weighted by demand)
- Use flexible/cross-trained operators
- Group similar products together (sequencing)
- Design for commonality (standard tasks)
- Dedicated lines for high-volume models

### Challenge: Operator Skill Differences

**Problem:**
- Not all operators equally skilled
- Task times vary by operator
- Training needs

**Solutions:**
- Multi-skilling and cross-training
- Pair experienced with new operators
- Standard work to reduce variation
- Job rotation for skill development
- Assign easier tasks to less skilled initially

### Challenge: Space Constraints

**Problem:**
- Physical space limits workstation design
- Cannot add workstations
- Equipment placement constraints

**Solutions:**
- U-shaped or two-sided lines (space-efficient)
- Vertical space utilization
- Mobile workstations
- Overlapping work zones
- Task time reduction to fit in fewer stations

---

## Output Format

### Line Balancing Report

**Executive Summary:**
- Current line configuration and performance
- Balancing results and efficiency
- Recommendations for improvement
- Expected benefits

**Current State:**

| Workstation | Tasks | Time (min) | Idle Time | Utilization % |
|-------------|-------|------------|-----------|---------------|
| WS1 | A, B, C | 6.5 | 0.5 | 93% |
| WS2 | D, E | 6.9 | 0.1 | 99% (Bottleneck) |
| WS3 | F, G | 5.5 | 1.5 | 79% |
| WS4 | H, I, J | 6.0 | 1.0 | 86% |

**Current Metrics:**
- Number of Workstations: 4
- Cycle Time: 7.0 minutes
- Line Efficiency: 89.3%
- Balance Delay: 10.7%
- Throughput: 8.6 units/hour

**Proposed Balance:**

| Workstation | Tasks | Time (min) | Idle Time | Utilization % |
|-------------|-------|------------|-----------|---------------|
| WS1 | A, B, D | 6.8 | 0.2 | 97% |
| WS2 | C, E | 6.7 | 0.3 | 96% |
| WS3 | F, G, H | 6.5 | 0.5 | 93% |
| WS4 | I, J | 6.9 | 0.1 | 99% |

**Improved Metrics:**
- Number of Workstations: 4 (no change)
- Cycle Time: 7.0 minutes (same)
- Line Efficiency: 95.7% (+6.4%)
- Balance Delay: 4.3% (-6.4%)
- Throughput: 8.6 units/hour (same)

**Recommendations:**

1. **Rebalance Workstations** (Priority: High)
   - Redistribute tasks per proposed balance
   - Expected: +6.4% efficiency
   - Implementation: 1 week (training, layout changes)
   - Cost: Minimal (training only)

2. **Reduce Bottleneck Task Time** (Priority: Medium)
   - Improve methods at WS2 (Task E)
   - Target: Reduce 0.9 min → 0.6 min
   - Expected: Enable cycle time reduction to 6.7 min (+11% throughput)
   - Methods: Improved tooling, eliminate wasted motion

3. **Implement U-Shaped Line** (Priority: Medium)
   - Convert to U-shaped configuration
   - Expected: -30% space, better flexibility
   - Investment: $50K layout changes
   - ROI: 12 months

**Expected Benefits:**
- Line efficiency: +6-8%
- Throughput: +8-12% (if cycle time reduced)
- Space utilization: +20-30% (U-shaped)
- Operator flexibility: Improved
- WIP reduction: 15-20%

---

## Questions to Ask

If you need more context:
1. What is the current line configuration and number of workstations?
2. What are the task list and processing times?
3. Are there precedence constraints between tasks?
4. What is the target production rate (units/day)?
5. What is the available working time per shift?
6. Are there skill or equipment constraints?
7. Is the line for single model or multiple products?
8. What is current line efficiency and bottleneck?

---

## Related Skills

- **production-scheduling**: For production planning and scheduling
- **process-optimization**: For overall process improvement
- **lean-manufacturing**: For waste elimination and flow
- **quality-management**: For quality at each station
- **capacity-planning**: For long-term capacity analysis
- **workforce-scheduling**: For operator scheduling
- **optimization-modeling**: For mathematical balancing models
- **prescriptive-analytics**: For advanced optimization
