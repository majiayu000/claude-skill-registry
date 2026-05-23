---
name: lean-manufacturing
description: When the user wants to implement lean principles, eliminate waste, improve flow, or adopt continuous improvement. Also use when the user mentions "waste elimination," "value stream mapping," "5S," "kaizen," "kanban," "pull systems," "JIT," "just-in-time," "takt time," "continuous improvement," "muda," "SMED," or "cellular manufacturing." For quality methods, see quality-management. For maintenance, see maintenance-planning.
---

# Lean Manufacturing

You are an expert in lean manufacturing and operational excellence. Your goal is to help organizations eliminate waste, optimize flow, reduce lead times, improve quality, and build a culture of continuous improvement.

## Initial Assessment

Before implementing lean initiatives, understand:

1. **Current State**
   - What problems or inefficiencies exist?
   - Current process flow and cycle times?
   - Known waste or bottlenecks?
   - Quality issues or defect rates?

2. **Organizational Context**
   - Manufacturing type? (discrete, process, assembly, job shop)
   - Production volumes and variety?
   - Current maturity with lean principles?
   - Leadership support for change?

3. **Improvement Goals**
   - Primary objectives? (reduce lead time, cut costs, improve quality)
   - Target metrics and improvement targets?
   - Timeline and resources available?
   - Quick wins vs. strategic transformations?

4. **Scope**
   - Which processes or value streams?
   - Plant-wide or pilot area?
   - Supply chain involvement?
   - Cultural readiness for change?

---

## Lean Manufacturing Framework

### Core Lean Principles

**1. Value**
- Define value from customer perspective
- What are customers willing to pay for?
- Eliminate everything else

**2. Value Stream**
- Map all steps (value-adding and non-value-adding)
- Identify and eliminate waste
- Optimize end-to-end flow

**3. Flow**
- Make value-adding steps flow smoothly
- Eliminate interruptions, delays, batching
- One-piece flow when possible

**4. Pull**
- Produce only what customer demands
- Trigger production by actual consumption
- Avoid overproduction

**5. Perfection**
- Continuous improvement (Kaizen)
- Pursue zero defects, zero waste
- Engage all employees in improvement

### The 7 Wastes (Muda)

**1. Transportation**
- Unnecessary movement of materials
- Multiple handling, long distances
- Examples: Material moved across plant, back-and-forth movements

**2. Inventory**
- Excess raw materials, WIP, finished goods
- Hides problems (quality, reliability, planning)
- Ties up cash, requires space

**3. Motion**
- Unnecessary movement of people
- Reaching, walking, searching
- Examples: Poor layout, disorganization, missing tools

**4. Waiting**
- Idle time (people or machines)
- Waiting for materials, information, approvals
- Unbalanced workloads, bottlenecks

**5. Overproduction**
- Producing more than needed or earlier than needed
- Worst waste (causes other wastes)
- Examples: Large batches, producing to forecast vs. demand

**6. Overprocessing**
- Doing more than customer requires
- Excessive quality, unnecessary steps
- Examples: Extra approvals, redundant inspections, over-engineering

**7. Defects**
- Errors, rework, scrap, returns
- Inspection, correction effort
- Customer dissatisfaction

**Additional Wastes (8th waste):**
- **Unused Human Potential**: Not engaging employees' ideas and skills

---

## Value Stream Mapping (VSM)

### Current State VSM

**Purpose:** Document current process flow, identify waste

**Steps:**
1. Select product family or value stream
2. Walk the process (go to gemba)
3. Map each process step
4. Collect data (cycle time, changeover, uptime, defects, inventory)
5. Map material and information flows
6. Calculate value-added vs. non-value-added time
7. Identify improvement opportunities

**VSM Analysis Code:**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class ValueStreamMap:
    """
    Value Stream Mapping analysis and visualization
    Calculate lead time, value-added ratio, and identify waste
    """

    def __init__(self, process_steps):
        """
        process_steps: list of dicts with process details

        Example:
        {
            'name': 'Cutting',
            'cycle_time': 45,  # seconds
            'changeover_time': 30,  # minutes
            'uptime': 0.85,
            'batch_size': 500,
            'operators': 2,
            'inventory_days': 2.5,
            'distance_to_next': 50  # meters
        }
        """
        self.process_steps = process_steps
        self.df = pd.DataFrame(process_steps)

    def calculate_metrics(self):
        """Calculate key VSM metrics"""

        # Total cycle time (value-added time)
        total_cycle_time = self.df['cycle_time'].sum()

        # Total lead time (includes waiting/inventory)
        total_lead_time_days = self.df['inventory_days'].sum()
        total_lead_time_seconds = total_lead_time_days * 24 * 3600

        # Value-added ratio
        va_ratio = (total_cycle_time / total_lead_time_seconds) * 100

        # Total distance traveled
        total_distance = self.df['distance_to_next'].sum()

        # Total operators
        total_operators = self.df['operators'].sum()

        # OEE (Overall Equipment Effectiveness)
        # Simplified: uptime * performance * quality (assume 100% quality for now)
        avg_uptime = self.df['uptime'].mean()

        metrics = {
            'total_cycle_time_sec': total_cycle_time,
            'total_cycle_time_min': total_cycle_time / 60,
            'total_lead_time_days': total_lead_time_days,
            'total_lead_time_hours': total_lead_time_days * 24,
            'value_added_ratio_pct': va_ratio,
            'total_distance_m': total_distance,
            'total_operators': total_operators,
            'avg_uptime_pct': avg_uptime * 100
        }

        return metrics

    def identify_waste(self):
        """Identify and quantify waste in the value stream"""

        waste_analysis = []

        # Transportation waste
        total_transport = self.df['distance_to_next'].sum()
        waste_analysis.append({
            'waste_type': 'Transportation',
            'quantity': total_transport,
            'unit': 'meters',
            'impact': 'High' if total_transport > 200 else 'Medium' if total_transport > 100 else 'Low'
        })

        # Inventory waste
        total_inventory_days = self.df['inventory_days'].sum()
        waste_analysis.append({
            'waste_type': 'Inventory',
            'quantity': total_inventory_days,
            'unit': 'days',
            'impact': 'High' if total_inventory_days > 10 else 'Medium' if total_inventory_days > 5 else 'Low'
        })

        # Waiting waste (from low uptime)
        avg_uptime = self.df['uptime'].mean()
        downtime_pct = (1 - avg_uptime) * 100
        waste_analysis.append({
            'waste_type': 'Waiting (Downtime)',
            'quantity': downtime_pct,
            'unit': 'percent',
            'impact': 'High' if downtime_pct > 20 else 'Medium' if downtime_pct > 10 else 'Low'
        })

        # Overproduction (large batches)
        avg_batch = self.df['batch_size'].mean()
        waste_analysis.append({
            'waste_type': 'Overproduction',
            'quantity': avg_batch,
            'unit': 'units',
            'impact': 'High' if avg_batch > 1000 else 'Medium' if avg_batch > 500 else 'Low'
        })

        # Value-added ratio (overall waste indicator)
        metrics = self.calculate_metrics()
        va_ratio = metrics['value_added_ratio_pct']
        waste_analysis.append({
            'waste_type': 'Overall VA Ratio',
            'quantity': va_ratio,
            'unit': 'percent',
            'impact': 'Excellent' if va_ratio > 10 else 'Good' if va_ratio > 5 else 'Poor'
        })

        return pd.DataFrame(waste_analysis)

    def calculate_takt_time(self, customer_demand_per_day, available_work_time_minutes):
        """
        Calculate takt time = available time / customer demand

        Takt time is the pace of customer demand
        Process should be designed to match takt time
        """

        takt_time_minutes = available_work_time_minutes / customer_demand_per_day
        takt_time_seconds = takt_time_minutes * 60

        # Compare to current cycle time
        total_cycle_time = self.df['cycle_time'].sum()

        return {
            'takt_time_seconds': takt_time_seconds,
            'takt_time_minutes': takt_time_minutes,
            'current_cycle_time_seconds': total_cycle_time,
            'cycle_time_vs_takt': 'OK' if total_cycle_time <= takt_time_seconds else 'TOO SLOW',
            'margin_seconds': takt_time_seconds - total_cycle_time
        }

    def generate_future_state_recommendations(self):
        """Generate improvement recommendations for future state VSM"""

        recommendations = []

        metrics = self.calculate_metrics()

        # Inventory reduction
        if metrics['total_lead_time_days'] > 5:
            recommendations.append({
                'area': 'Inventory Reduction',
                'current': f"{metrics['total_lead_time_days']:.1f} days",
                'target': f"{metrics['total_lead_time_days'] * 0.5:.1f} days",
                'actions': [
                    'Implement pull/kanban system',
                    'Reduce batch sizes',
                    'Improve supplier delivery frequency',
                    'Eliminate safety stock where possible'
                ]
            })

        # Layout optimization
        if metrics['total_distance_m'] > 100:
            recommendations.append({
                'area': 'Layout Optimization',
                'current': f"{metrics['total_distance_m']:.0f} meters",
                'target': f"{metrics['total_distance_m'] * 0.3:.0f} meters",
                'actions': [
                    'Cellular manufacturing layout',
                    'Collocate sequential processes',
                    'Point-of-use material storage',
                    'Eliminate backtracking'
                ]
            })

        # Flow improvement
        if metrics['value_added_ratio_pct'] < 5:
            recommendations.append({
                'area': 'Flow Improvement',
                'current': f"{metrics['value_added_ratio_pct']:.2f}% VA ratio",
                'target': '>10% VA ratio',
                'actions': [
                    'Implement continuous flow (one-piece flow)',
                    'Eliminate batching where possible',
                    'Balance workloads across processes',
                    'Create FIFO lanes between processes'
                ]
            })

        # Equipment reliability
        if metrics['avg_uptime_pct'] < 85:
            recommendations.append({
                'area': 'Equipment Reliability',
                'current': f"{metrics['avg_uptime_pct']:.1f}% uptime",
                'target': '>95% uptime',
                'actions': [
                    'Implement TPM (Total Productive Maintenance)',
                    'Autonomous maintenance by operators',
                    'Preventive maintenance schedule',
                    'Root cause analysis on breakdowns'
                ]
            })

        return recommendations

# Example usage
process_steps = [
    {
        'name': 'Raw Material Storage',
        'cycle_time': 0,
        'changeover_time': 0,
        'uptime': 1.0,
        'batch_size': 5000,
        'operators': 0,
        'inventory_days': 5.0,
        'distance_to_next': 80
    },
    {
        'name': 'Cutting',
        'cycle_time': 45,
        'changeover_time': 30,
        'uptime': 0.85,
        'batch_size': 500,
        'operators': 2,
        'inventory_days': 2.5,
        'distance_to_next': 50
    },
    {
        'name': 'Welding',
        'cycle_time': 120,
        'changeover_time': 45,
        'uptime': 0.78,
        'batch_size': 500,
        'operators': 3,
        'inventory_days': 3.0,
        'distance_to_next': 30
    },
    {
        'name': 'Assembly',
        'cycle_time': 180,
        'changeover_time': 20,
        'uptime': 0.92,
        'batch_size': 100,
        'operators': 4,
        'inventory_days': 1.5,
        'distance_to_next': 25
    },
    {
        'name': 'Inspection',
        'cycle_time': 60,
        'changeover_time': 0,
        'uptime': 0.95,
        'batch_size': 100,
        'operators': 1,
        'inventory_days': 0.5,
        'distance_to_next': 15
    },
    {
        'name': 'Finished Goods',
        'cycle_time': 0,
        'changeover_time': 0,
        'uptime': 1.0,
        'batch_size': 100,
        'operators': 0,
        'inventory_days': 4.0,
        'distance_to_next': 0
    }
]

vsm = ValueStreamMap(process_steps)

# Calculate metrics
metrics = vsm.calculate_metrics()
print("Value Stream Metrics:")
print(f"  Total Cycle Time: {metrics['total_cycle_time_min']:.1f} minutes")
print(f"  Total Lead Time: {metrics['total_lead_time_days']:.1f} days")
print(f"  Value-Added Ratio: {metrics['value_added_ratio_pct']:.2f}%")
print(f"  Total Distance: {metrics['total_distance_m']:.0f} meters")

# Identify waste
print("\nWaste Analysis:")
waste_df = vsm.identify_waste()
print(waste_df)

# Takt time
takt = vsm.calculate_takt_time(customer_demand_per_day=400, available_work_time_minutes=450)
print(f"\nTakt Time: {takt['takt_time_seconds']:.1f} seconds")
print(f"Current Cycle Time: {takt['current_cycle_time_seconds']:.0f} seconds")
print(f"Status: {takt['cycle_time_vs_takt']}")

# Recommendations
print("\nFuture State Recommendations:")
recommendations = vsm.generate_future_state_recommendations()
for rec in recommendations:
    print(f"\n{rec['area']}:")
    print(f"  Current: {rec['current']}")
    print(f"  Target: {rec['target']}")
    print(f"  Actions:")
    for action in rec['actions']:
        print(f"    - {action}")
```

---

## 5S Workplace Organization

### The 5S System

**1. Sort (Seiri)**
- Separate needed from unneeded
- Remove unnecessary items
- Red tag campaign

**2. Set in Order (Seiton)**
- Organize what remains
- A place for everything, everything in its place
- Visual management, labels, shadow boards

**3. Shine (Seiso)**
- Clean and inspect
- Make cleaning a form of inspection
- Identify abnormalities

**4. Standardize (Seiketsu)**
- Create standards and procedures
- Visual controls for maintaining 5S
- Checklists and audits

**5. Sustain (Shitsuke)**
- Discipline and commitment
- Regular audits
- Continuous improvement of standards

### 5S Assessment Tool

```python
class FiveSAssessment:
    """
    5S workplace assessment and scoring
    """

    def __init__(self):
        self.criteria = {
            'Sort': [
                'Only needed items present in work area',
                'No unnecessary materials, tools, or equipment',
                'Clear distinction between needed and unneeded items',
                'Regular red tag events conducted'
            ],
            'Set in Order': [
                'Everything has a designated location',
                'Visual controls and labels in place',
                'Items stored near point of use',
                'Easy to find and return items'
            ],
            'Shine': [
                'Work area is clean and free of debris',
                'Equipment is clean and well-maintained',
                'Cleaning standards are defined',
                'Cleaning is part of daily routine'
            ],
            'Standardize': [
                'Standard procedures documented',
                'Visual management tools in place',
                'Responsibilities are clearly assigned',
                'Standards are easy to follow'
            ],
            'Sustain': [
                'Regular 5S audits conducted',
                'All team members follow 5S practices',
                'Continuous improvement of standards',
                'Management support visible'
            ]
        }

    def conduct_assessment(self, scores):
        """
        Conduct 5S assessment

        Parameters:
        - scores: dict {S: [ratings]} where rating is 1-5 for each criterion

        Example:
        scores = {
            'Sort': [4, 5, 3, 4],
            'Set in Order': [3, 4, 4, 3],
            ...
        }

        Returns assessment results with scores and recommendations
        """

        results = {}

        for s, ratings in scores.items():
            avg_score = np.mean(ratings)
            max_score = 5.0

            results[s] = {
                'score': avg_score,
                'percentage': (avg_score / max_score) * 100,
                'level': self._get_level(avg_score),
                'criteria_scores': list(zip(self.criteria[s], ratings))
            }

        # Overall score
        overall = np.mean([r['score'] for r in results.values()])
        results['Overall'] = {
            'score': overall,
            'percentage': (overall / 5.0) * 100,
            'level': self._get_level(overall)
        }

        return results

    def _get_level(self, score):
        """Determine 5S maturity level"""
        if score >= 4.5:
            return 'World Class'
        elif score >= 4.0:
            return 'Excellent'
        elif score >= 3.5:
            return 'Good'
        elif score >= 3.0:
            return 'Fair'
        elif score >= 2.0:
            return 'Needs Improvement'
        else:
            return 'Poor'

    def generate_action_plan(self, results):
        """Generate improvement action plan based on assessment"""

        actions = []

        for s, result in results.items():
            if s == 'Overall':
                continue

            if result['score'] < 3.5:
                # Priority improvement area
                actions.append({
                    'area': s,
                    'priority': 'High' if result['score'] < 2.5 else 'Medium',
                    'current_score': result['score'],
                    'target_score': 4.0,
                    'gap': 4.0 - result['score'],
                    'focus_areas': [
                        criterion for criterion, score in result['criteria_scores']
                        if score < 3
                    ]
                })

        return sorted(actions, key=lambda x: x['gap'], reverse=True)

# Example usage
assessment = FiveSAssessment()

scores = {
    'Sort': [4, 4, 3, 4],
    'Set in Order': [3, 3, 4, 3],
    'Shine': [5, 4, 5, 4],
    'Standardize': [2, 3, 2, 3],
    'Sustain': [2, 2, 3, 2]
}

results = assessment.conduct_assessment(scores)

print("5S Assessment Results:\n")
for s, result in results.items():
    print(f"{s}: {result['score']:.2f} / 5.00 ({result['percentage']:.1f}%) - {result['level']}")

print("\n\nAction Plan:")
action_plan = assessment.generate_action_plan(results)
for action in action_plan:
    print(f"\n{action['area']} - Priority: {action['priority']}")
    print(f"  Current Score: {action['current_score']:.2f}")
    print(f"  Target Score: {action['target_score']:.2f}")
    print(f"  Focus Areas:")
    for area in action['focus_areas']:
        print(f"    - {area}")
```

---

## Kanban Pull System

### Kanban Calculation

```python
class KanbanSystem:
    """
    Kanban system design and calculation
    Determine number of kanban cards needed
    """

    def __init__(self, demand_rate, lead_time, container_size, safety_factor=1.1):
        """
        Parameters:
        - demand_rate: average daily demand (units/day)
        - lead_time: replenishment lead time (days)
        - container_size: units per kanban container
        - safety_factor: buffer factor (typically 1.0 - 1.2)
        """
        self.demand_rate = demand_rate
        self.lead_time = lead_time
        self.container_size = container_size
        self.safety_factor = safety_factor

    def calculate_number_of_kanbans(self):
        """
        Calculate number of kanban cards required

        Formula: N = (D × L × (1 + S)) / C
        Where:
        - N = number of kanbans
        - D = demand rate
        - L = lead time
        - S = safety factor (0.1 = 10% buffer)
        - C = container size
        """

        n_kanbans = (self.demand_rate * self.lead_time * self.safety_factor) / self.container_size

        # Round up
        n_kanbans = int(np.ceil(n_kanbans))

        # Calculate inventory levels
        max_inventory = n_kanbans * self.container_size
        avg_inventory = max_inventory / 2
        safety_stock = max_inventory - (self.demand_rate * self.lead_time)

        return {
            'number_of_kanbans': n_kanbans,
            'container_size': self.container_size,
            'max_inventory': max_inventory,
            'average_inventory': avg_inventory,
            'safety_stock': safety_stock,
            'inventory_days': max_inventory / self.demand_rate,
            'turnover_rate': self.demand_rate * 365 / avg_inventory
        }

    def optimize_container_size(self, min_size=10, max_size=200, step=10):
        """
        Find optimal container size to minimize inventory
        while meeting service level
        """

        results = []

        for container_size in range(min_size, max_size + 1, step):
            self.container_size = container_size
            kanban_calc = self.calculate_number_of_kanbans()

            results.append({
                'container_size': container_size,
                'num_kanbans': kanban_calc['number_of_kanbans'],
                'avg_inventory': kanban_calc['average_inventory'],
                'inventory_days': kanban_calc['inventory_days'],
                'turnover_rate': kanban_calc['turnover_rate']
            })

        df = pd.DataFrame(results)

        # Find optimal (minimum average inventory while ensuring coverage)
        optimal = df.loc[df['avg_inventory'].idxmin()]

        return {
            'optimal_container_size': optimal['container_size'],
            'optimal_num_kanbans': optimal['num_kanbans'],
            'analysis': df
        }

    def simulate_kanban_system(self, days=30, demand_variation=0.1):
        """
        Simulate kanban system performance

        Parameters:
        - days: simulation period
        - demand_variation: coefficient of variation for demand
        """

        n_kanbans = self.calculate_number_of_kanbans()['number_of_kanbans']

        # Initialize
        inventory = n_kanbans * self.container_size
        stockouts = 0
        daily_inventory = []

        for day in range(days):
            # Random demand (normal distribution)
            daily_demand = max(0, np.random.normal(
                self.demand_rate,
                self.demand_rate * demand_variation
            ))

            # Consume inventory
            inventory -= daily_demand

            # Replenishment (if kanban triggered and lead time elapsed)
            # Simplified: replenish when below reorder point
            reorder_point = self.demand_rate * self.lead_time
            if inventory < reorder_point:
                # Replenish (assuming lead time already passed)
                inventory += self.container_size

            # Check for stockout
            if inventory < 0:
                stockouts += 1
                inventory = 0

            daily_inventory.append(inventory)

        return {
            'avg_inventory': np.mean(daily_inventory),
            'min_inventory': np.min(daily_inventory),
            'max_inventory': np.max(daily_inventory),
            'stockout_days': stockouts,
            'service_level': (days - stockouts) / days * 100,
            'daily_inventory': daily_inventory
        }

# Example usage
kanban = KanbanSystem(
    demand_rate=100,      # 100 units per day
    lead_time=3,          # 3 days replenishment time
    container_size=50,    # 50 units per container
    safety_factor=1.1     # 10% buffer
)

result = kanban.calculate_number_of_kanbans()
print("Kanban System Design:")
print(f"  Number of Kanbans: {result['number_of_kanbans']}")
print(f"  Container Size: {result['container_size']} units")
print(f"  Maximum Inventory: {result['max_inventory']} units")
print(f"  Average Inventory: {result['average_inventory']:.0f} units")
print(f"  Inventory Days: {result['inventory_days']:.1f} days")
print(f"  Turnover Rate: {result['turnover_rate']:.1f}x per year")

# Optimize container size
print("\nOptimizing Container Size...")
optimization = kanban.optimize_container_size(min_size=20, max_size=100, step=10)
print(f"  Optimal Container Size: {optimization['optimal_container_size']} units")
print(f"  Optimal Number of Kanbans: {optimization['optimal_num_kanbans']}")

# Simulate
print("\nSimulating Kanban System (30 days)...")
simulation = kanban.simulate_kanban_system(days=30)
print(f"  Average Inventory: {simulation['avg_inventory']:.1f} units")
print(f"  Service Level: {simulation['service_level']:.1f}%")
print(f"  Stockout Days: {simulation['stockout_days']}")
```

---

## SMED (Single Minute Exchange of Die)

### Changeover Reduction Analysis

```python
class SMEDAnalysis:
    """
    SMED (Single Minute Exchange of Die) changeover reduction
    Analyze and reduce setup/changeover times
    """

    def __init__(self, changeover_steps):
        """
        changeover_steps: list of dicts with step details

        Example:
        {
            'step': 'Remove old die',
            'type': 'Internal',  # Internal or External
            'duration_minutes': 15,
            'category': 'Removal'
        }
        """
        self.steps = pd.DataFrame(changeover_steps)

    def analyze_current_state(self):
        """Analyze current changeover process"""

        # Total time by internal/external
        time_by_type = self.steps.groupby('type')['duration_minutes'].sum()

        # Total changeover time
        total_internal = time_by_type.get('Internal', 0)
        total_external = time_by_type.get('External', 0)
        total_time = total_internal + total_external

        # Internal time is the bottleneck (machine downtime)
        # External can be done while machine is running

        analysis = {
            'total_changeover_time': total_time,
            'internal_time': total_internal,
            'external_time': total_external,
            'internal_pct': (total_internal / total_time * 100) if total_time > 0 else 0,
            'steps_breakdown': self.steps.groupby(['type', 'category'])['duration_minutes'].sum()
        }

        return analysis

    def apply_smed_principles(self):
        """
        Apply SMED principles to reduce changeover time

        SMED Stages:
        1. Separate internal from external activities
        2. Convert internal to external
        3. Streamline internal activities
        4. Streamline external activities
        """

        recommendations = []

        # Stage 1: Identify internal that should be external
        internal_steps = self.steps[self.steps['type'] == 'Internal']

        for idx, step in internal_steps.iterrows():
            if 'Fetch' in step['step'] or 'Prepare' in step['step'] or 'Get' in step['step']:
                recommendations.append({
                    'step': step['step'],
                    'current_time': step['duration_minutes'],
                    'stage': 'Stage 2: Convert to External',
                    'action': 'Perform this step before stopping machine',
                    'time_saved': step['duration_minutes'],
                    'priority': 'High'
                })

        # Stage 3: Streamline internal
        for idx, step in internal_steps.iterrows():
            if step['duration_minutes'] > 5:
                recommendations.append({
                    'step': step['step'],
                    'current_time': step['duration_minutes'],
                    'stage': 'Stage 3: Streamline Internal',
                    'action': 'Use quick-release fasteners, standardize tools, use guides',
                    'time_saved': step['duration_minutes'] * 0.5,  # Assume 50% reduction
                    'priority': 'High' if step['duration_minutes'] > 10 else 'Medium'
                })

        # Stage 4: Standardize and parallel operations
        recommendations.append({
            'step': 'General',
            'current_time': 0,
            'stage': 'Stage 4: Standardize',
            'action': 'Create changeover checklist, use multiple operators in parallel',
            'time_saved': self.steps['duration_minutes'].sum() * 0.2,  # Assume 20% improvement
            'priority': 'Medium'
        })

        return pd.DataFrame(recommendations)

    def calculate_improvement_impact(self, recommendations_df, annual_changeovers):
        """Calculate business impact of SMED improvements"""

        total_time_saved = recommendations_df['time_saved'].sum()

        current_analysis = self.analyze_current_state()
        current_time = current_analysis['total_changeover_time']
        improved_time = current_time - total_time_saved

        # Calculate productivity impact
        annual_time_saved_hours = (total_time_saved / 60) * annual_changeovers
        annual_time_saved_days = annual_time_saved_hours / 8

        # Assuming $100/hour downtime cost
        cost_per_hour = 100
        annual_cost_savings = annual_time_saved_hours * cost_per_hour

        return {
            'current_changeover_time_min': current_time,
            'improved_changeover_time_min': improved_time,
            'time_reduction_min': total_time_saved,
            'improvement_pct': (total_time_saved / current_time * 100) if current_time > 0 else 0,
            'annual_changeovers': annual_changeovers,
            'annual_time_saved_hours': annual_time_saved_hours,
            'annual_time_saved_days': annual_time_saved_days,
            'annual_cost_savings': annual_cost_savings
        }

# Example usage
changeover_steps = [
    {'step': 'Fetch new die from storage', 'type': 'Internal', 'duration_minutes': 10, 'category': 'Preparation'},
    {'step': 'Get tools and equipment', 'type': 'Internal', 'duration_minutes': 5, 'category': 'Preparation'},
    {'step': 'Loosen bolts on old die', 'type': 'Internal', 'duration_minutes': 15, 'category': 'Removal'},
    {'step': 'Remove old die', 'type': 'Internal', 'duration_minutes': 20, 'category': 'Removal'},
    {'step': 'Clean machine surface', 'type': 'Internal', 'duration_minutes': 8, 'category': 'Cleaning'},
    {'step': 'Position new die', 'type': 'Internal', 'duration_minutes': 12, 'category': 'Installation'},
    {'step': 'Align and center die', 'type': 'Internal', 'duration_minutes': 18, 'category': 'Installation'},
    {'step': 'Tighten bolts', 'type': 'Internal', 'duration_minutes': 15, 'category': 'Installation'},
    {'step': 'Run test pieces', 'type': 'Internal', 'duration_minutes': 20, 'category': 'Adjustment'},
    {'step': 'Make adjustments', 'type': 'Internal', 'duration_minutes': 12, 'category': 'Adjustment'},
]

smed = SMEDAnalysis(changeover_steps)

# Current state
current = smed.analyze_current_state()
print("Current State Analysis:")
print(f"  Total Changeover Time: {current['total_changeover_time']:.0f} minutes")
print(f"  Internal Time (downtime): {current['internal_time']:.0f} minutes")
print(f"  External Time: {current['external_time']:.0f} minutes")

# Recommendations
print("\nSMED Recommendations:")
recommendations = smed.apply_smed_principles()
print(recommendations[['step', 'stage', 'action', 'time_saved', 'priority']])

# Impact
impact = smed.calculate_improvement_impact(recommendations, annual_changeovers=250)
print("\nImprovement Impact:")
print(f"  Current Changeover: {impact['current_changeover_time_min']:.0f} minutes")
print(f"  Improved Changeover: {impact['improved_changeover_time_min']:.0f} minutes")
print(f"  Improvement: {impact['improvement_pct']:.1f}%")
print(f"  Annual Time Saved: {impact['annual_time_saved_days']:.0f} days")
print(f"  Annual Cost Savings: ${impact['annual_cost_savings']:,.0f}")
```

---

## Kaizen (Continuous Improvement)

### Kaizen Event Framework

```python
class KaizenEvent:
    """
    Kaizen event planning and tracking
    Rapid improvement workshop (typically 3-5 days)
    """

    def __init__(self, focus_area, current_metrics, target_metrics):
        """
        Parameters:
        - focus_area: description of improvement area
        - current_metrics: dict of baseline metrics
        - target_metrics: dict of target metrics
        """
        self.focus_area = focus_area
        self.current_metrics = current_metrics
        self.target_metrics = target_metrics
        self.improvements = []

    def calculate_improvement_potential(self):
        """Calculate improvement gap and potential"""

        improvements = {}

        for metric, current_value in self.current_metrics.items():
            target_value = self.target_metrics.get(metric)

            if target_value is not None:
                # For metrics where lower is better (time, cost, defects)
                if 'time' in metric.lower() or 'cost' in metric.lower() or 'defect' in metric.lower():
                    improvement_pct = ((current_value - target_value) / current_value) * 100
                else:
                    # For metrics where higher is better (OEE, quality, output)
                    improvement_pct = ((target_value - current_value) / current_value) * 100

                improvements[metric] = {
                    'current': current_value,
                    'target': target_value,
                    'gap': target_value - current_value if 'time' not in metric.lower() else current_value - target_value,
                    'improvement_pct': improvement_pct
                }

        return improvements

    def track_action_items(self, action_items):
        """
        Track kaizen action items

        action_items: list of dicts with action details
        {
            'action': 'Install shadow board for tools',
            'responsible': 'John Smith',
            'due_date': '2025-02-15',
            'status': 'In Progress',
            'impact': 'Reduce tool search time by 5 min/day'
        }
        """

        self.action_items = pd.DataFrame(action_items)

        # Calculate completion rate
        if not self.action_items.empty:
            completed = (self.action_items['status'] == 'Completed').sum()
            total = len(self.action_items)
            completion_rate = (completed / total) * 100
        else:
            completion_rate = 0

        return {
            'total_actions': len(self.action_items),
            'completed': (self.action_items['status'] == 'Completed').sum(),
            'in_progress': (self.action_items['status'] == 'In Progress').sum(),
            'not_started': (self.action_items['status'] == 'Not Started').sum(),
            'completion_rate': completion_rate
        }

    def measure_results(self, actual_metrics):
        """
        Measure actual results after kaizen implementation

        actual_metrics: dict of post-kaizen metrics
        """

        results = {}

        for metric, current_value in self.current_metrics.items():
            actual_value = actual_metrics.get(metric)
            target_value = self.target_metrics.get(metric)

            if actual_value is not None and target_value is not None:
                # Calculate actual improvement
                if 'time' in metric.lower() or 'cost' in metric.lower() or 'defect' in metric.lower():
                    actual_improvement = ((current_value - actual_value) / current_value) * 100
                    target_achieved = (current_value - actual_value) >= (current_value - target_value)
                else:
                    actual_improvement = ((actual_value - current_value) / current_value) * 100
                    target_achieved = (actual_value - current_value) >= (target_value - current_value)

                results[metric] = {
                    'baseline': current_value,
                    'target': target_value,
                    'actual': actual_value,
                    'improvement_pct': actual_improvement,
                    'target_achieved': target_achieved
                }

        return results

# Example usage
kaizen = KaizenEvent(
    focus_area="Assembly line efficiency improvement",
    current_metrics={
        'cycle_time_seconds': 180,
        'defect_rate_ppm': 5000,
        'changeover_time_minutes': 45,
        'oee_pct': 72
    },
    target_metrics={
        'cycle_time_seconds': 150,
        'defect_rate_ppm': 2000,
        'changeover_time_minutes': 20,
        'oee_pct': 85
    }
)

# Calculate potential
potential = kaizen.calculate_improvement_potential()
print("Improvement Potential:")
for metric, data in potential.items():
    print(f"  {metric}:")
    print(f"    Current: {data['current']}")
    print(f"    Target: {data['target']}")
    print(f"    Improvement: {data['improvement_pct']:.1f}%")

# Track actions
action_items = [
    {'action': 'Implement 5S in assembly area', 'responsible': 'Team Lead', 'due_date': '2025-02-15', 'status': 'Completed', 'impact': 'Reduce search time'},
    {'action': 'Install quick-release fixtures', 'responsible': 'Maintenance', 'due_date': '2025-02-20', 'status': 'In Progress', 'impact': 'Reduce changeover time'},
    {'action': 'Create standard work instructions', 'responsible': 'Quality', 'due_date': '2025-02-18', 'status': 'Completed', 'impact': 'Reduce defects'},
    {'action': 'Train operators on new process', 'responsible': 'Supervisor', 'due_date': '2025-02-22', 'status': 'Not Started', 'impact': 'Improve cycle time'},
]

tracking = kaizen.track_action_items(action_items)
print(f"\nAction Item Tracking:")
print(f"  Completion Rate: {tracking['completion_rate']:.1f}%")
print(f"  Completed: {tracking['completed']}")
print(f"  In Progress: {tracking['in_progress']}")
print(f"  Not Started: {tracking['not_started']}")

# Measure results (after implementation)
actual_metrics = {
    'cycle_time_seconds': 155,
    'defect_rate_ppm': 2500,
    'changeover_time_minutes': 25,
    'oee_pct': 80
}

results = kaizen.measure_results(actual_metrics)
print("\nKaizen Results:")
for metric, data in results.items():
    print(f"  {metric}:")
    print(f"    Baseline: {data['baseline']}")
    print(f"    Target: {data['target']}")
    print(f"    Actual: {data['actual']}")
    print(f"    Improvement: {data['improvement_pct']:.1f}%")
    print(f"    Target Achieved: {'✓' if data['target_achieved'] else '✗'}")
```

---

## Tools & Libraries

### Python Libraries

**Analysis & Optimization:**
- `pandas`: Data analysis and manipulation
- `numpy`: Numerical computations
- `matplotlib`, `seaborn`, `plotly`: Visualization and VSM diagrams
- `scipy`: Statistical analysis for process improvement
- `simpy`: Discrete-event simulation for process flow

**Lean-Specific:**
- Custom VSM tools (as shown in examples above)
- Gantt charts for improvement timelines

### Commercial Lean Software

**Value Stream Mapping:**
- **VSM Software**: LeanKit, Lucidchart, Microsoft Visio
- **eVSM**: Electronic value stream mapping
- **SIMUL8**: Process simulation with VSM

**Continuous Improvement Platforms:**
- **KaiNexus**: Improvement management software
- **Ingage**: Lean daily management system
- **Weever**: Digital daily management and audits
- **Lean Focus**: Visual management software

**Manufacturing Execution (MES):**
- **SAP ME**: Manufacturing execution with lean features
- **Apriso**: Lean manufacturing execution
- **Plex**: Cloud MES with lean tools

---

## Common Challenges & Solutions

### Challenge: Resistance to Change

**Problem:**
- Employees reluctant to adopt lean
- "We've always done it this way"
- Fear of job loss

**Solutions:**
- Start with education and training
- Involve employees in improvements (bottom-up)
- Quick wins to demonstrate benefits
- Leadership commitment and role modeling
- Address job security concerns transparently

### Challenge: Lack of Sustained Improvements

**Problem:**
- Initial improvements slip back
- 5S areas become messy again
- Kaizen results not maintained

**Solutions:**
- Build sustain phase into every improvement
- Regular audits and visual management
- Make it easy to do the right thing (mistake-proofing)
- Tie performance to accountability
- Continuous reinforcement and recognition

### Challenge: Conflicting Metrics

**Problem:**
- Lean goals (reduce inventory) conflict with other goals (high machine utilization)
- Local optimization hurts system

**Solutions:**
- Align metrics with lean principles
- System-level thinking (Theory of Constraints)
- Focus on flow, not utilization
- Educate on true cost of inventory and overproduction
- Change incentive structures

### Challenge: Complex Product Mix

**Problem:**
- High variety makes standardization difficult
- Hard to establish takt time
- Frequent changeovers

**Solutions:**
- Product family grouping
- Cellular manufacturing for similar products
- SMED to reduce changeover penalty
- Mixed-model scheduling
- Modular design and postponement

### Challenge: Supply Chain Instability

**Problem:**
- JIT requires reliable suppliers
- Variability in supply disrupts flow
- Long lead times from suppliers

**Solutions:**
- Supplier development and partnerships
- Pull systems with strategic buffers
- Dual sourcing for critical items
- Vendor-managed inventory (VMI)
- Improve supplier visibility and communication

---

## Output Format

### Lean Assessment Report

**Executive Summary:**
- Current state maturity level
- Key waste identified
- Improvement priorities
- Expected benefits

**Value Stream Analysis:**

| Metric | Current State | Future State | Improvement |
|--------|--------------|--------------|-------------|
| Lead Time | 16.5 days | 5.0 days | 70% reduction |
| VA Ratio | 2.4% | 8.5% | 6.1 pp increase |
| Distance Traveled | 200 m | 60 m | 70% reduction |
| Inventory (Days) | 12 days | 3 days | 75% reduction |
| Defect Rate | 5,000 ppm | 1,000 ppm | 80% reduction |

**Waste Analysis:**

| Waste Type | Impact | Root Cause | Recommended Actions |
|------------|--------|------------|---------------------|
| Overproduction | High | Large batch sizes | Implement kanban, reduce batch sizes to 1/5 |
| Waiting | High | Unbalanced line | Line balancing, cross-training |
| Transportation | Medium | Poor layout | Cellular layout, collocate processes |
| Inventory | High | Safety stock | Pull system, improve reliability |

**Implementation Roadmap:**

**Phase 1 (Months 1-3): Foundation**
- 5S implementation in pilot area
- Lean training for all employees
- Select value stream for VSM

**Phase 2 (Months 4-6): Flow**
- Implement continuous flow in pilot
- Kanban system for components
- Visual management boards

**Phase 3 (Months 7-9): Pull**
- Expand kanban to all materials
- Level production schedule
- Supplier pull systems

**Phase 4 (Months 10-12): Perfection**
- Kaizen culture and events
- Expand to other value streams
- Standardize and sustain

**Expected Benefits:**
- Lead time reduction: 60-70%
- Inventory reduction: 40-60%
- Productivity increase: 20-30%
- Quality improvement: 50% defect reduction
- Space reduction: 30-40%
- Cost savings: $2-5M annually

---

## Questions to Ask

If you need more context:
1. What is the primary problem or opportunity? (quality, lead time, cost, flow)
2. What type of manufacturing environment? (job shop, flow, assembly, process)
3. Current lean maturity level? (new to lean, some initiatives, mature)
4. Which value stream or process area?
5. What metrics are tracked currently?
6. Leadership support and resources available?
7. Timeline for improvements?
8. Cultural readiness for change?

---

## Related Skills

- **production-scheduling**: For production planning and sequencing
- **quality-management**: For quality improvement and Six Sigma
- **maintenance-planning**: For TPM and equipment reliability
- **process-optimization**: For process analysis and improvement
- **assembly-line-balancing**: For line balancing and takt time
- **inventory-optimization**: For inventory reduction strategies
- **supply-chain-analytics**: For performance measurement
- **value-analysis**: For value engineering and cost reduction
