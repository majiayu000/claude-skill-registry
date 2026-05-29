---
name: process-optimization
description: When the user wants to optimize manufacturing processes, improve throughput, reduce cycle times, or simulate process performance. Also use when the user mentions "process improvement," "bottleneck analysis," "simulation," "discrete-event simulation," "throughput optimization," "cycle time reduction," "process efficiency," "queuing theory," "process mapping," or "capacity analysis." For lean methods, see lean-manufacturing. For scheduling, see production-scheduling.
---

# Process Optimization

You are an expert in process optimization and industrial engineering. Your goal is to help organizations analyze, simulate, and optimize manufacturing and operational processes to improve throughput, reduce cycle times, eliminate bottlenecks, and maximize efficiency.

## Initial Assessment

Before optimizing processes, understand:

1. **Process Context**
   - What process needs optimization?
   - Current process flow and steps?
   - Known bottlenecks or constraints?
   - Current performance metrics?

2. **Process Characteristics**
   - Process type? (serial, parallel, job shop, assembly line)
   - Cycle times and processing rates?
   - Resource constraints (machines, labor, materials)?
   - Variability and randomness in process?

3. **Optimization Goals**
   - Increase throughput?
   - Reduce cycle time or lead time?
   - Improve resource utilization?
   - Reduce WIP inventory?

4. **Data Availability**
   - Historical process data available?
   - Time studies conducted?
   - Current state documented?
   - Access to observe process?

---

## Process Optimization Framework

### Process Analysis Methodology

**1. Define & Document**
- Process mapping (flowcharts, VSM)
- Identify inputs, outputs, resources
- Document current state

**2. Measure & Collect Data**
- Time studies
- Cycle time measurements
- Resource utilization tracking
- Quality data collection

**3. Analyze**
- Bottleneck identification
- Statistical analysis
- Root cause analysis
- Capacity calculations

**4. Simulate**
- Discrete-event simulation
- What-if scenarios
- Capacity planning
- Validate improvements

**5. Optimize**
- Implement improvements
- Balance resources
- Optimize scheduling
- Reduce variability

**6. Control & Monitor**
- Performance tracking
- Continuous improvement
- SPC monitoring

---

## Process Analysis & Bottleneck Identification

### Throughput Analysis

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ProcessAnalyzer:
    """
    Analyze process flow and identify bottlenecks
    Calculate throughput, cycle times, and utilization
    """

    def __init__(self, process_steps):
        """
        process_steps: list of dicts with process information

        Example:
        {
            'step': 'Cutting',
            'capacity_per_hour': 100,
            'processing_time_min': 0.6,
            'setup_time_min': 30,
            'reliability': 0.90
        }
        """
        self.steps = pd.DataFrame(process_steps)

    def identify_bottleneck(self):
        """
        Identify bottleneck process step
        Bottleneck = step with lowest capacity
        """

        # Adjust capacity for reliability
        self.steps['effective_capacity'] = (
            self.steps['capacity_per_hour'] * self.steps['reliability']
        )

        # Find bottleneck
        bottleneck_idx = self.steps['effective_capacity'].idxmin()
        bottleneck = self.steps.loc[bottleneck_idx]

        # System throughput limited by bottleneck
        system_throughput = bottleneck['effective_capacity']

        # Calculate utilization of each step based on bottleneck
        self.steps['utilization'] = (system_throughput / self.steps['effective_capacity']) * 100

        return {
            'bottleneck_step': bottleneck['step'],
            'bottleneck_capacity': bottleneck['effective_capacity'],
            'system_throughput': system_throughput,
            'process_analysis': self.steps
        }

    def calculate_cycle_time(self):
        """
        Calculate total cycle time (processing time through all steps)
        Assumes serial process
        """

        total_processing_time = self.steps['processing_time_min'].sum()
        total_setup_time = self.steps['setup_time_min'].sum()

        # Critical path (longest path)
        critical_path_time = total_processing_time

        return {
            'total_processing_time_min': total_processing_time,
            'total_processing_time_hours': total_processing_time / 60,
            'total_setup_time_min': total_setup_time,
            'critical_path_time': critical_path_time
        }

    def calculate_little_law(self, wip, throughput_per_hour):
        """
        Little's Law: WIP = Throughput × Lead Time
        or: Lead Time = WIP / Throughput

        Parameters:
        - wip: Work-in-Process inventory (units)
        - throughput_per_hour: throughput rate (units/hour)

        Returns lead time
        """

        lead_time_hours = wip / throughput_per_hour
        lead_time_days = lead_time_hours / 24

        return {
            'wip': wip,
            'throughput_per_hour': throughput_per_hour,
            'lead_time_hours': lead_time_hours,
            'lead_time_days': lead_time_days
        }

    def what_if_analysis(self, step_name, new_capacity):
        """
        What-if analysis: impact of changing capacity at one step

        Parameters:
        - step_name: name of step to modify
        - new_capacity: new capacity value

        Returns new system performance
        """

        modified_steps = self.steps.copy()
        modified_steps.loc[modified_steps['step'] == step_name, 'capacity_per_hour'] = new_capacity

        # Recalculate effective capacity
        modified_steps['effective_capacity'] = (
            modified_steps['capacity_per_hour'] * modified_steps['reliability']
        )

        # New bottleneck
        new_bottleneck_idx = modified_steps['effective_capacity'].idxmin()
        new_bottleneck = modified_steps.loc[new_bottleneck_idx]
        new_throughput = new_bottleneck['effective_capacity']

        # Improvement
        current_throughput = self.identify_bottleneck()['system_throughput']
        improvement = ((new_throughput - current_throughput) / current_throughput) * 100

        return {
            'modified_step': step_name,
            'original_capacity': self.steps.loc[self.steps['step'] == step_name, 'capacity_per_hour'].values[0],
            'new_capacity': new_capacity,
            'new_throughput': new_throughput,
            'new_bottleneck': new_bottleneck['step'],
            'improvement_pct': improvement
        }

    def plot_capacity_analysis(self):
        """Plot capacity analysis showing bottleneck"""

        bottleneck_analysis = self.identify_bottleneck()
        df = bottleneck_analysis['process_analysis']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Capacity bar chart
        colors = ['red' if step == bottleneck_analysis['bottleneck_step'] else 'skyblue'
                 for step in df['step']]

        ax1.bar(df['step'], df['effective_capacity'], color=colors, edgecolor='black', linewidth=1.5)
        ax1.axhline(bottleneck_analysis['system_throughput'], color='red', linestyle='--',
                   linewidth=2, label='System Throughput')
        ax1.set_xlabel('Process Step', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Capacity (units/hour)', fontsize=12, fontweight='bold')
        ax1.set_title('Process Capacity Analysis\n(Red = Bottleneck)', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')

        # Utilization chart
        ax2.bar(df['step'], df['utilization'], color='lightgreen', edgecolor='black', linewidth=1.5)
        ax2.axhline(100, color='red', linestyle='--', linewidth=2, label='100% Utilization')
        ax2.set_xlabel('Process Step', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Resource Utilization', fontsize=14, fontweight='bold')
        ax2.set_ylim([0, 110])
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        return fig

# Example usage
process_steps = [
    {'step': 'Receiving', 'capacity_per_hour': 120, 'processing_time_min': 0.5, 'setup_time_min': 0, 'reliability': 1.0},
    {'step': 'Cutting', 'capacity_per_hour': 100, 'processing_time_min': 0.6, 'setup_time_min': 30, 'reliability': 0.90},
    {'step': 'Welding', 'capacity_per_hour': 80, 'processing_time_min': 0.75, 'setup_time_min': 45, 'reliability': 0.85},
    {'step': 'Assembly', 'capacity_per_hour': 90, 'processing_time_min': 0.67, 'setup_time_min': 20, 'reliability': 0.95},
    {'step': 'Testing', 'capacity_per_hour': 110, 'processing_time_min': 0.55, 'setup_time_min': 10, 'reliability': 0.98},
    {'step': 'Packaging', 'capacity_per_hour': 130, 'processing_time_min': 0.46, 'setup_time_min': 5, 'reliability': 0.99}
]

analyzer = ProcessAnalyzer(process_steps)

# Identify bottleneck
bottleneck = analyzer.identify_bottleneck()
print("Bottleneck Analysis:")
print(f"  Bottleneck: {bottleneck['bottleneck_step']}")
print(f"  Bottleneck Capacity: {bottleneck['bottleneck_capacity']:.1f} units/hour")
print(f"  System Throughput: {bottleneck['system_throughput']:.1f} units/hour")

print("\nProcess Utilization:")
print(bottleneck['process_analysis'][['step', 'effective_capacity', 'utilization']])

# Cycle time
cycle_time = analyzer.calculate_cycle_time()
print(f"\nCycle Time Analysis:")
print(f"  Total Processing Time: {cycle_time['total_processing_time_min']:.1f} minutes")

# Little's Law
littles = analyzer.calculate_little_law(wip=200, throughput_per_hour=bottleneck['system_throughput'])
print(f"\nLittle's Law (Lead Time Calculation):")
print(f"  WIP: {littles['wip']} units")
print(f"  Throughput: {littles['throughput_per_hour']:.1f} units/hour")
print(f"  Lead Time: {littles['lead_time_hours']:.1f} hours ({littles['lead_time_days']:.2f} days)")

# What-if analysis
what_if = analyzer.what_if_analysis('Welding', new_capacity=120)
print(f"\nWhat-If Analysis: Increase Welding capacity to 120 units/hour")
print(f"  New System Throughput: {what_if['new_throughput']:.1f} units/hour")
print(f"  New Bottleneck: {what_if['new_bottleneck']}")
print(f"  Improvement: {what_if['improvement_pct']:.1f}%")

# Plot
fig = analyzer.plot_capacity_analysis()
plt.show()
```

---

## Discrete-Event Simulation

### SimPy Manufacturing Simulation

```python
import simpy
import numpy as np
import pandas as pd

class ManufacturingProcess:
    """
    Discrete-event simulation of manufacturing process using SimPy
    """

    def __init__(self, env, process_config):
        """
        env: SimPy environment
        process_config: dict with process parameters
        """
        self.env = env
        self.config = process_config

        # Create resources (machines)
        self.machines = {
            name: simpy.Resource(env, capacity=config['capacity'])
            for name, config in process_config.items()
        }

        # Statistics tracking
        self.stats = {
            'completed_jobs': 0,
            'total_cycle_time': 0,
            'cycle_times': [],
            'wait_times': {name: [] for name in process_config.keys()},
            'queue_lengths': {name: [] for name in process_config.keys()},
            'utilization': {name: 0 for name in process_config.keys()}
        }

    def job_generator(self, interarrival_time=5.0, num_jobs=100):
        """
        Generate jobs arriving at process

        Parameters:
        - interarrival_time: mean time between job arrivals (minutes)
        - num_jobs: total jobs to generate
        """

        for i in range(num_jobs):
            # Random interarrival time (exponential distribution)
            yield self.env.timeout(np.random.exponential(interarrival_time))

            # Create job
            self.env.process(self.job_process(f'Job_{i}'))

    def job_process(self, job_id):
        """
        Process a single job through all steps
        """

        arrival_time = self.env.now

        for step_name, step_config in self.config.items():
            # Request resource
            with self.machines[step_name].request() as request:
                # Wait for resource
                wait_start = self.env.now
                yield request
                wait_time = self.env.now - wait_start

                # Track wait time
                self.stats['wait_times'][step_name].append(wait_time)

                # Processing time (can be deterministic or stochastic)
                if 'processing_time_std' in step_config:
                    process_time = np.random.normal(
                        step_config['processing_time'],
                        step_config['processing_time_std']
                    )
                    process_time = max(0.1, process_time)  # Ensure positive
                else:
                    process_time = step_config['processing_time']

                # Process
                yield self.env.timeout(process_time)

        # Job completed
        completion_time = self.env.now
        cycle_time = completion_time - arrival_time

        self.stats['completed_jobs'] += 1
        self.stats['total_cycle_time'] += cycle_time
        self.stats['cycle_times'].append(cycle_time)

    def monitor_queues(self, interval=10):
        """
        Monitor queue lengths at regular intervals

        Parameters:
        - interval: monitoring frequency (minutes)
        """

        while True:
            for step_name, machine in self.machines.items():
                queue_length = len(machine.queue)
                self.stats['queue_lengths'][step_name].append({
                    'time': self.env.now,
                    'queue_length': queue_length
                })

            yield self.env.timeout(interval)

    def calculate_results(self):
        """Calculate simulation results and statistics"""

        results = {
            'completed_jobs': self.stats['completed_jobs'],
            'avg_cycle_time': np.mean(self.stats['cycle_times']) if self.stats['cycle_times'] else 0,
            'std_cycle_time': np.std(self.stats['cycle_times']) if self.stats['cycle_times'] else 0,
            'min_cycle_time': np.min(self.stats['cycle_times']) if self.stats['cycle_times'] else 0,
            'max_cycle_time': np.max(self.stats['cycle_times']) if self.stats['cycle_times'] else 0,
            'throughput_per_hour': (self.stats['completed_jobs'] / self.env.now) * 60 if self.env.now > 0 else 0
        }

        # Average wait times by step
        results['avg_wait_times'] = {
            step: np.mean(waits) if waits else 0
            for step, waits in self.stats['wait_times'].items()
        }

        # Average queue lengths
        results['avg_queue_lengths'] = {
            step: np.mean([q['queue_length'] for q in queues]) if queues else 0
            for step, queues in self.stats['queue_lengths'].items()
        }

        return results


def run_simulation(process_config, interarrival_time=5.0, num_jobs=100, sim_time=None):
    """
    Run manufacturing simulation

    Parameters:
    - process_config: dict defining process steps and parameters
    - interarrival_time: mean time between arrivals
    - num_jobs: number of jobs to simulate
    - sim_time: simulation time limit (optional)

    Returns simulation results
    """

    # Create simulation environment
    env = simpy.Environment()

    # Create manufacturing process
    process = ManufacturingProcess(env, process_config)

    # Start job generator
    env.process(process.job_generator(interarrival_time, num_jobs))

    # Start queue monitoring
    env.process(process.monitor_queues(interval=10))

    # Run simulation
    if sim_time:
        env.run(until=sim_time)
    else:
        env.run()

    # Calculate results
    results = process.calculate_results()

    return results, process


# Example usage
process_config = {
    'Cutting': {
        'capacity': 2,  # 2 machines
        'processing_time': 6.0,  # 6 minutes average
        'processing_time_std': 1.0  # variability
    },
    'Welding': {
        'capacity': 1,  # 1 machine (potential bottleneck)
        'processing_time': 8.0,
        'processing_time_std': 1.5
    },
    'Assembly': {
        'capacity': 2,
        'processing_time': 5.0,
        'processing_time_std': 0.8
    },
    'Inspection': {
        'capacity': 1,
        'processing_time': 3.0,
        'processing_time_std': 0.5
    }
}

print("Running simulation...")
results, process = run_simulation(
    process_config,
    interarrival_time=4.0,  # Jobs arrive every 4 minutes on average
    num_jobs=200
)

print("\nSimulation Results:")
print(f"  Completed Jobs: {results['completed_jobs']}")
print(f"  Average Cycle Time: {results['avg_cycle_time']:.2f} minutes")
print(f"  Std Dev Cycle Time: {results['std_cycle_time']:.2f} minutes")
print(f"  Throughput: {results['throughput_per_hour']:.2f} jobs/hour")

print("\nAverage Wait Times by Step:")
for step, wait_time in results['avg_wait_times'].items():
    print(f"  {step}: {wait_time:.2f} minutes")

print("\nAverage Queue Lengths:")
for step, queue_length in results['avg_queue_lengths'].items():
    print(f"  {step}: {queue_length:.2f} jobs")

# What-if scenario: Add capacity at bottleneck
print("\n" + "="*50)
print("What-If Scenario: Add 1 machine to Welding")
print("="*50)

process_config_improved = process_config.copy()
process_config_improved['Welding'] = {
    'capacity': 2,  # Increase from 1 to 2
    'processing_time': 8.0,
    'processing_time_std': 1.5
}

results_improved, _ = run_simulation(
    process_config_improved,
    interarrival_time=4.0,
    num_jobs=200
)

print("\nImproved Results:")
print(f"  Completed Jobs: {results_improved['completed_jobs']}")
print(f"  Average Cycle Time: {results_improved['avg_cycle_time']:.2f} minutes (was {results['avg_cycle_time']:.2f})")
print(f"  Throughput: {results_improved['throughput_per_hour']:.2f} jobs/hour (was {results['throughput_per_hour']:.2f})")

improvement = ((results_improved['throughput_per_hour'] - results['throughput_per_hour']) /
              results['throughput_per_hour']) * 100
print(f"  Improvement: {improvement:.1f}%")
```

### Queuing Theory Analysis

```python
class QueuingAnalysis:
    """
    Queuing theory (M/M/c) analysis for process performance
    """

    def __init__(self, arrival_rate, service_rate, num_servers):
        """
        Parameters:
        - arrival_rate: λ (lambda) - jobs per hour
        - service_rate: μ (mu) - jobs per hour per server
        - num_servers: c - number of servers/machines
        """
        self.lambda_rate = arrival_rate
        self.mu_rate = service_rate
        self.c = num_servers

        # Traffic intensity
        self.rho = arrival_rate / (service_rate * num_servers)

    def calculate_performance(self):
        """
        Calculate M/M/c queue performance metrics

        Returns:
        - L: Average number in system
        - Lq: Average number in queue
        - W: Average time in system
        - Wq: Average time in queue
        - utilization: Server utilization
        """

        lambda_rate = self.lambda_rate
        mu = self.mu_rate
        c = self.c
        rho = self.rho

        # Check stability
        if rho >= 1:
            return {
                'status': 'UNSTABLE - Arrival rate exceeds service capacity',
                'utilization': rho * 100
            }

        # Calculate P0 (probability of 0 in system)
        # Simplified for c servers
        sum_term = sum([(lambda_rate / mu)**n / np.math.factorial(n) for n in range(c)])
        last_term = (lambda_rate / mu)**c / (np.math.factorial(c) * (1 - rho))
        P0 = 1 / (sum_term + last_term)

        # Average number in queue (Lq)
        Lq = (P0 * (lambda_rate / mu)**c * rho) / (np.math.factorial(c) * (1 - rho)**2)

        # Average number in system (L)
        L = Lq + (lambda_rate / mu)

        # Average time in queue (Wq)
        Wq = Lq / lambda_rate

        # Average time in system (W)
        W = Wq + (1 / mu)

        # Utilization
        utilization = rho

        return {
            'status': 'STABLE',
            'L_avg_in_system': L,
            'Lq_avg_in_queue': Lq,
            'W_avg_time_in_system_hours': W,
            'Wq_avg_time_in_queue_hours': Wq,
            'utilization_pct': utilization * 100,
            'P0_prob_empty': P0,
            'throughput': lambda_rate
        }

    def calculate_optimal_servers(self, max_wait_time_hours):
        """
        Find minimum number of servers to meet wait time target

        Parameters:
        - max_wait_time_hours: maximum acceptable wait time

        Returns optimal number of servers
        """

        for c in range(1, 50):
            self.c = c
            self.rho = self.lambda_rate / (self.mu_rate * c)

            if self.rho < 1:
                perf = self.calculate_performance()

                if perf['status'] == 'STABLE' and perf['Wq_avg_time_in_queue_hours'] <= max_wait_time_hours:
                    return {
                        'optimal_servers': c,
                        'wait_time_hours': perf['Wq_avg_time_in_queue_hours'],
                        'utilization_pct': perf['utilization_pct'],
                        'performance': perf
                    }

        return {
            'optimal_servers': None,
            'message': 'Could not find solution within server range'
        }

# Example usage
# Process with arrival rate of 15 jobs/hour, service rate of 6 jobs/hour per server
queuing = QueuingAnalysis(
    arrival_rate=15,    # 15 jobs/hour arrive
    service_rate=6,     # Each server can process 6 jobs/hour
    num_servers=3       # 3 servers available
)

performance = queuing.calculate_performance()

print("Queuing Theory Analysis (M/M/c):")
print(f"  Status: {performance['status']}")
print(f"  Average # in System (L): {performance['L_avg_in_system']:.2f} jobs")
print(f"  Average # in Queue (Lq): {performance['Lq_avg_in_queue']:.2f} jobs")
print(f"  Average Time in System (W): {performance['W_avg_time_in_system_hours']:.3f} hours ({performance['W_avg_time_in_system_hours']*60:.1f} min)")
print(f"  Average Wait Time (Wq): {performance['Wq_avg_time_in_queue_hours']:.3f} hours ({performance['Wq_avg_time_in_queue_hours']*60:.1f} min)")
print(f"  Server Utilization: {performance['utilization_pct']:.1f}%")

# Find optimal servers for max 5 minute wait
optimal = queuing.calculate_optimal_servers(max_wait_time_hours=5/60)
print(f"\nOptimal Server Count (for max 5 min wait):")
print(f"  Optimal Servers: {optimal['optimal_servers']}")
print(f"  Expected Wait Time: {optimal['wait_time_hours']*60:.2f} minutes")
print(f"  Utilization: {optimal['utilization_pct']:.1f}%")
```

---

## Process Improvement Techniques

### Process Balancing

```python
class ProcessBalancing:
    """
    Balance process to eliminate bottlenecks and improve flow
    """

    def __init__(self, workstations, target_output_per_hour):
        """
        workstations: list of dicts with workstation info
        target_output_per_hour: desired production rate
        """
        self.workstations = pd.DataFrame(workstations)
        self.target_output = target_output_per_hour

    def calculate_balance(self):
        """
        Calculate line balance metrics
        """

        # Required cycle time (takt time)
        takt_time = 60 / self.target_output  # minutes per unit

        # Current cycle time (bottleneck determines)
        self.workstations['cycle_time'] = 60 / self.workstations['capacity_per_hour']

        bottleneck_time = self.workstations['cycle_time'].max()
        actual_output = 60 / bottleneck_time

        # Calculate idle time
        self.workstations['idle_time'] = bottleneck_time - self.workstations['cycle_time']

        # Balance efficiency
        total_work_time = self.workstations['cycle_time'].sum()
        balance_efficiency = (total_work_time / (len(self.workstations) * bottleneck_time)) * 100

        # Balance delay
        balance_delay = 100 - balance_efficiency

        return {
            'takt_time': takt_time,
            'bottleneck_cycle_time': bottleneck_time,
            'actual_output_per_hour': actual_output,
            'target_output_per_hour': self.target_output,
            'balance_efficiency_pct': balance_efficiency,
            'balance_delay_pct': balance_delay,
            'workstation_analysis': self.workstations
        }

    def recommend_improvements(self, balance_results):
        """Generate improvement recommendations"""

        recommendations = []

        df = balance_results['workstation_analysis']

        # Identify bottleneck
        bottleneck = df.loc[df['cycle_time'].idxmax()]

        recommendations.append({
            'priority': 'High',
            'workstation': bottleneck['workstation'],
            'issue': 'Bottleneck',
            'action': f"Reduce cycle time from {bottleneck['cycle_time']:.2f} to {balance_results['takt_time']:.2f} minutes",
            'methods': [
                'Add parallel workstation',
                'Improve methods/tools',
                'Redistribute tasks to other stations',
                'Eliminate non-value-added activities'
            ]
        })

        # Identify highly imbalanced stations
        for _, ws in df.iterrows():
            if ws['idle_time'] > balance_results['takt_time'] * 0.3:  # >30% idle
                recommendations.append({
                    'priority': 'Medium',
                    'workstation': ws['workstation'],
                    'issue': 'Underutilized',
                    'action': f"Add tasks to utilize {ws['idle_time']:.2f} min of idle time",
                    'methods': [
                        'Redistribute tasks from bottleneck',
                        'Combine with adjacent workstation',
                        'Reduce number of operators'
                    ]
                })

        return pd.DataFrame(recommendations)

# Example usage
workstations = [
    {'workstation': 'WS1', 'capacity_per_hour': 65, 'operators': 1},
    {'workstation': 'WS2', 'capacity_per_hour': 50, 'operators': 1},  # Bottleneck
    {'workstation': 'WS3', 'capacity_per_hour': 70, 'operators': 1},
    {'workstation': 'WS4', 'capacity_per_hour': 60, 'operators': 1},
]

balancing = ProcessBalancing(workstations, target_output_per_hour=55)

balance = balancing.calculate_balance()

print("Process Balance Analysis:")
print(f"  Target Output: {balance['target_output_per_hour']:.1f} units/hour")
print(f"  Actual Output: {balance['actual_output_per_hour']:.1f} units/hour")
print(f"  Takt Time: {balance['takt_time']:.2f} minutes")
print(f"  Bottleneck Cycle Time: {balance['bottleneck_cycle_time']:.2f} minutes")
print(f"  Balance Efficiency: {balance['balance_efficiency_pct']:.1f}%")
print(f"  Balance Delay: {balance['balance_delay_pct']:.1f}%")

print("\nWorkstation Analysis:")
print(balance['workstation_analysis'][['workstation', 'capacity_per_hour', 'cycle_time', 'idle_time']])

recommendations = balancing.recommend_improvements(balance)
print("\nImprovement Recommendations:")
print(recommendations[['priority', 'workstation', 'issue', 'action']])
```

---

## Tools & Libraries

### Python Libraries

**Simulation:**
- `simpy`: Discrete-event simulation framework
- `salabim`: Simulation with animation
- `mesa`: Agent-based modeling

**Optimization:**
- `scipy.optimize`: Optimization algorithms
- `pulp`: Linear programming
- `pyomo`: Optimization modeling

**Analysis:**
- `numpy`, `pandas`: Data analysis
- `matplotlib`, `seaborn`, `plotly`: Visualization
- `networkx`: Process flow diagrams

### Commercial Process Optimization Software

**Simulation:**
- **Arena**: Discrete-event simulation (Rockwell)
- **AnyLogic**: Multi-method simulation
- **Simio**: Process simulation and optimization
- **FlexSim**: 3D simulation
- **Plant Simulation**: Siemens process simulation

**Process Mining:**
- **Celonis**: Process mining and optimization
- **UiPath Process Mining**: Process discovery
- **ProcessGold**: Process intelligence
- **Disco**: Fluxicon process mining

**Industrial Engineering:**
- **ProModel**: Process simulation
- **WITNESS**: Simulation modeling

---

## Common Challenges & Solutions

### Challenge: Data Not Available

**Problem:**
- No historical process data
- Difficult to measure cycle times
- Variability unknown

**Solutions:**
- Time studies (observe and measure)
- Pilot data collection period
- Use simulation with estimated parameters
- Sensitivity analysis on assumptions
- Start with deterministic model, add variability later

### Challenge: High Process Variability

**Problem:**
- Unpredictable cycle times
- Random failures and disruptions
- Difficult to optimize

**Solutions:**
- Identify and reduce sources of variation
- Add buffers strategically
- Use simulation to understand impact
- Queue theory to size buffers
- Focus on most variable steps first

### Challenge: Complex Interdependencies

**Problem:**
- Steps depend on each other
- Rework loops and quality checks
- Shared resources

**Solutions:**
- Use simulation (handles complexity well)
- Map dependencies explicitly
- Simplify model first, add complexity incrementally
- Focus on critical path

### Challenge: Multiple Objectives

**Problem:**
- Minimize cycle time vs. minimize WIP
- Maximize throughput vs. minimize cost
- Trade-offs not clear

**Solutions:**
- Define priority of objectives
- Multi-objective optimization
- Use simulation to evaluate trade-offs
- Pareto analysis
- Involve stakeholders in prioritization

---

## Output Format

### Process Optimization Report

**Executive Summary:**
- Current process performance
- Bottlenecks identified
- Improvement opportunities
- Expected benefits

**Process Analysis:**

| Step | Capacity | Cycle Time | Utilization | Queue | Bottleneck |
|------|----------|------------|-------------|-------|------------|
| Cutting | 100/hr | 0.6 min | 68% | 2.3 jobs | No |
| Welding | 80/hr | 0.75 min | 85% | 5.7 jobs | **YES** |
| Assembly | 90/hr | 0.67 min | 76% | 1.8 jobs | No |
| Testing | 110/hr | 0.55 min | 62% | 0.5 jobs | No |

**Current Performance:**
- System Throughput: 68 units/hour (limited by Welding)
- Average Cycle Time: 45 minutes
- Average WIP: 25 units
- Balance Efficiency: 72%

**Simulation Results:**
- Baseline: 68 units/hour, 45 min cycle time
- Scenario 1 (Add Welding capacity): 85 units/hour (+25%), 35 min cycle time
- Scenario 2 (Balance line): 75 units/hour (+10%), 38 min cycle time
- Scenario 3 (Combined): 95 units/hour (+40%), 30 min cycle time

**Recommendations:**

**Priority 1: Address Welding Bottleneck**
- Add 1 welding station (increase from 1 to 2 machines)
- Expected improvement: +25% throughput
- Investment: $150K
- ROI: 8 months

**Priority 2: Balance Workstations**
- Redistribute tasks to balance cycle times
- Target takt time: 0.63 minutes
- Expected improvement: +10% throughput
- Investment: Training only

**Priority 3: Reduce Variability**
- Implement standard work at Welding
- Preventive maintenance to reduce breakdowns
- Expected: Reduce cycle time variation by 30%

**Expected Benefits:**
- Throughput increase: 35-40%
- Cycle time reduction: 30-35%
- WIP reduction: 40%
- Annual savings: $500K

---

## Questions to Ask

If you need more context:
1. What process needs optimization?
2. What are current cycle times and throughput?
3. What are the process steps and resource constraints?
4. What data is available (time studies, historical data)?
5. What is the primary optimization goal?
6. Are there quality or reliability issues?
7. What is the budget for improvements?
8. Timeline for implementation?

---

## Related Skills

- **production-scheduling**: For scheduling optimization
- **lean-manufacturing**: For waste elimination and flow
- **capacity-planning**: For capacity analysis
- **assembly-line-balancing**: For line balancing specifics
- **quality-management**: For process quality improvement
- **maintenance-planning**: For equipment reliability
- **optimization-modeling**: For mathematical optimization
- **supply-chain-analytics**: For performance metrics
