---
name: workforce-scheduling
description: When the user wants to optimize workforce scheduling, create shift plans, or balance labor demand. Also use when the user mentions "staff scheduling," "labor planning," "shift optimization," "crew scheduling," "roster optimization," or "employee scheduling." For task assignment, see task-assignment-problem. For wave planning labor, see wave-planning-optimization.
---

# Workforce Scheduling

You are an expert in workforce scheduling and labor optimization for warehouses and supply chain operations. Your goal is to help create optimal shift schedules that match labor supply with demand, minimize costs, ensure compliance, and improve employee satisfaction.

## Initial Assessment

Before optimizing workforce scheduling, understand:

1. **Labor Demand**
   - Daily/weekly order volume patterns?
   - Peak periods and seasonality?
   - Tasks to be performed (picking, packing, receiving)?
   - Required skills and certifications?
   - Service level targets (on-time shipping)?

2. **Labor Supply**
   - Total workforce size (full-time, part-time, temp)?
   - Employee availability and preferences?
   - Skill levels and cross-training?
   - Shift length preferences (8hr, 10hr, 12hr)?
   - Union rules and labor agreements?

3. **Business Constraints**
   - Operating hours (24/5, 24/7, day shift only)?
   - Minimum staffing levels?
   - Maximum consecutive days worked?
   - Overtime rules and costs?
   - Break and meal period requirements?
   - Weekend and holiday staffing needs?

4. **Current State**
   - Current scheduling method (manual, software)?
   - Current labor costs (regular + OT)?
   - Labor utilization rates?
   - Employee satisfaction with schedules?
   - Schedule change frequency?

---

## Workforce Scheduling Framework

### Scheduling Objectives

**Primary Goals:**
1. **Match Demand**: Ensure sufficient labor for forecasted workload
2. **Minimize Cost**: Optimize mix of regular hours, overtime, and temps
3. **Maximize Utilization**: Reduce idle time and overstaffing
4. **Employee Satisfaction**: Consider preferences, fairness, work-life balance
5. **Compliance**: Meet labor laws, union rules, company policies

**Key Metrics:**
- Labor cost per unit ($/order, $/line picked)
- Labor utilization % (productive time / scheduled time)
- Schedule efficiency (actual vs. planned labor hours)
- Employee turnover and absenteeism
- Overtime % (OT hours / total hours)

### Shift Design Strategies

**1. Fixed Shifts**
- Same schedule every week
- **Pros**: Predictable, easy to plan life around
- **Cons**: Inflexible, may not match demand
- **Use**: Stable demand, union environments

**2. Rotating Shifts**
- Employees rotate through different shifts
- **Pros**: Fair distribution of undesirable shifts
- **Cons**: Disrupts circadian rhythms, harder on employees
- **Use**: 24/7 operations, fairness priority

**3. Flexible/Variable Shifts**
- Shift start times and lengths vary
- **Pros**: Matches demand, reduces costs
- **Cons**: Unpredictable for employees, harder to schedule
- **Use**: Variable demand, high labor cost sensitivity

**4. Compressed Workweeks**
- 4×10hr or 3×12hr instead of 5×8hr
- **Pros**: Fewer workdays, employee preference, coverage
- **Cons**: Fatigue, may require premium pay
- **Use**: Continuous operations, employee retention

**5. On-Call/Flex Pool**
- Variable hours based on need
- **Pros**: Maximum flexibility, cost-effective
- **Cons**: Unpredictable for workers, may increase turnover
- **Use**: Peak periods, backup capacity

---

## Mathematical Formulation

### Workforce Scheduling as Optimization Problem

**Decision Variables:**
- x[i,s,d] = 1 if employee i works shift s on day d, 0 otherwise
- y[s,d] = number of employees on shift s on day d
- o[i,d] = overtime hours for employee i on day d

**Parameters:**
- D[s,d] = labor demand (hours) for shift s on day d
- C_reg = regular hourly wage
- C_ot = overtime hourly wage (typically 1.5× regular)
- C_temp = temporary worker hourly wage
- A[i,s,d] = availability of employee i for shift s on day d (0 or 1)
- H[s] = length of shift s (hours)
- Max_hours[i] = maximum hours per week for employee i
- Min_rest = minimum hours between shifts

**Objective Function:**

```
Minimize:
  Total Labor Cost = Regular + Overtime + Temp + Penalties

Formally:
  Σ Σ Σ (C_reg × H[s] × x[i,s,d])  # Regular time
  + Σ Σ (C_ot × o[i,d])  # Overtime
  + Σ Σ (C_temp × temp_hours[s,d])  # Temporary workers
  + α × (Σ schedule_disruption_penalty)  # Preference violations
  + β × (Σ understaffing_penalty)  # Demand shortfall
```

**Constraints:**

```python
# 1. Meet demand (with possible understaffing penalty)
for s in shifts:
    for d in days:
        Σ (H[s] × x[i,s,d]) + temp_hours[s,d] >= D[s,d]

# 2. Each employee works at most one shift per day
for i in employees:
    for d in days:
        Σ x[i,s,d] <= 1  for all s

# 3. Respect employee availability
for i in employees:
    for s in shifts:
        for d in days:
            x[i,s,d] <= A[i,s,d]

# 4. Maximum hours per week
for i in employees:
    for week in weeks:
        Σ Σ (H[s] × x[i,s,d]) <= Max_hours[i]  for d in week, s in shifts

# 5. Minimum rest between shifts
for i in employees:
    for d in days[:-1]:
        if x[i, evening_shift, d] = 1:
            x[i, morning_shift, d+1] = 0  # Example: no evening then morning

# 6. Maximum consecutive working days
for i in employees:
    for d in days:
        Σ x[i,s,d'] <= 6  for d' in [d...d+6], s in shifts

# 7. Minimum employees per shift (coverage)
for s in shifts:
    for d in days:
        Σ x[i,s,d] >= Min_coverage[s,d]  for all i

# 8. Skill requirements
for s in shifts:
    for d in days:
        Σ x[i,s,d] × skill[i,k] >= required_skill[k,s,d]
          for all i, k in skills
```

---

## Scheduling Algorithms

### Greedy Demand-Driven Scheduling

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def greedy_workforce_scheduling(demand, employees, shifts, days):
    """
    Greedy heuristic for workforce scheduling

    Algorithm:
    1. Sort days by demand (highest first)
    2. For each day, assign employees to meet demand
    3. Prioritize employees with availability and low weekly hours

    Parameters:
    -----------
    demand : dict
        {(shift, day): required_hours}
    employees : DataFrame
        Columns: employee_id, max_hours_per_week, availability
    shifts : list
        Shift identifiers
    days : list
        Day identifiers (e.g., dates)

    Returns:
    --------
    Schedule assignments
    """

    # Initialize schedule
    schedule = []
    employee_hours = {emp['employee_id']: 0 for _, emp in employees.iterrows()}

    # Sort (shift, day) pairs by demand
    demand_sorted = sorted(demand.items(), key=lambda x: x[1], reverse=True)

    for (shift, day), required_hours in demand_sorted:
        assigned_hours = 0

        # Get available employees for this shift/day
        available_employees = employees[
            employees['availability'].apply(lambda x: (shift, day) in x)
        ].copy()

        # Sort by current hours worked (assign to those with fewer hours first)
        available_employees['current_hours'] = available_employees['employee_id'].map(employee_hours)
        available_employees = available_employees.sort_values('current_hours')

        # Assign employees until demand met
        for idx, emp in available_employees.iterrows():
            emp_id = emp['employee_id']
            shift_length = 8  # Assume 8-hour shifts

            # Check if employee can work (not exceeding max hours)
            if employee_hours[emp_id] + shift_length <= emp['max_hours_per_week']:
                # Assign employee
                schedule.append({
                    'employee_id': emp_id,
                    'shift': shift,
                    'day': day,
                    'hours': shift_length
                })

                employee_hours[emp_id] += shift_length
                assigned_hours += shift_length

                if assigned_hours >= required_hours:
                    break

        # Check if demand met
        if assigned_hours < required_hours:
            print(f"Warning: Understaffed on {day}, shift {shift} "
                  f"({assigned_hours}/{required_hours} hours)")

    return pd.DataFrame(schedule)


# Example usage
employees = pd.DataFrame({
    'employee_id': [f'EMP{i:03d}' for i in range(1, 21)],
    'max_hours_per_week': [40] * 15 + [20] * 5,  # 15 full-time, 5 part-time
    'availability': [
        [(s, d) for s in ['morning', 'afternoon', 'evening']
         for d in range(7)]  # Available all shifts/days
        for _ in range(20)
    ]
})

shifts = ['morning', 'afternoon', 'evening']
days = list(range(7))  # Monday=0, Sunday=6

# Demand varies by day and shift
demand = {
    (shift, day): np.random.randint(40, 120)
    for shift in shifts for day in days
}

# Higher demand on weekdays, mornings and afternoons
for day in range(5):  # Mon-Fri
    demand[('morning', day)] *= 1.5
    demand[('afternoon', day)] *= 1.3

schedule = greedy_workforce_scheduling(demand, employees, shifts, days)

print("Workforce Schedule:")
print(f"Total Scheduled Hours: {schedule['hours'].sum()}")
print(f"Employees Scheduled: {schedule['employee_id'].nunique()}")
print(f"\nSchedule by Shift:")
print(schedule.groupby('shift')['hours'].sum())
```

### Integer Programming Model

```python
from pulp import *

def optimize_workforce_schedule(demand, employees, shifts, days,
                                cost_regular=20, cost_overtime=30):
    """
    Optimal workforce scheduling using MIP

    Parameters:
    -----------
    demand : dict
        {(shift, day): hours_needed}
    employees : DataFrame
        Employee data with availability and constraints
    shifts : list
        Available shifts
    days : list
        Days to schedule
    cost_regular : float
        Regular hourly cost
    cost_overtime : float
        Overtime hourly cost

    Returns:
    --------
    Optimal schedule
    """

    prob = LpProblem("Workforce_Scheduling", LpMinimize)

    # Decision variables
    # x[emp, shift, day] = 1 if employee works this shift on this day
    x = LpVariable.dicts("assign",
                        [(emp['employee_id'], shift, day)
                         for _, emp in employees.iterrows()
                         for shift in shifts
                         for day in days],
                        cat='Binary')

    # Overtime hours variables
    overtime = LpVariable.dicts("overtime",
                               [(emp['employee_id'], day)
                                for _, emp in employees.iterrows()
                                for day in days],
                               lowBound=0,
                               cat='Continuous')

    # Understaffing variables (soft constraint)
    understaffed = LpVariable.dicts("understaffed",
                                   [(shift, day) for shift in shifts for day in days],
                                   lowBound=0,
                                   cat='Continuous')

    # Objective: minimize cost
    shift_hours = 8  # Assume 8-hour shifts

    prob += (
        # Regular time cost
        cost_regular * shift_hours * lpSum([
            x[emp['employee_id'], shift, day]
            for _, emp in employees.iterrows()
            for shift in shifts
            for day in days
        ]) +

        # Overtime cost
        cost_overtime * lpSum([
            overtime[emp['employee_id'], day]
            for _, emp in employees.iterrows()
            for day in days
        ]) +

        # Understaffing penalty (high cost)
        1000 * lpSum([
            understaffed[shift, day]
            for shift in shifts
            for day in days
        ])
    ), "Total_Cost"

    # Constraints

    # 1. Meet demand (with possible understaffing)
    for shift in shifts:
        for day in days:
            prob += (
                lpSum([
                    shift_hours * x[emp['employee_id'], shift, day]
                    for _, emp in employees.iterrows()
                ]) + understaffed[shift, day] >= demand.get((shift, day), 0)
            ), f"Demand_{shift}_{day}"

    # 2. Each employee works at most one shift per day
    for _, emp in employees.iterrows():
        for day in days:
            prob += lpSum([
                x[emp['employee_id'], shift, day]
                for shift in shifts
            ]) <= 1, f"OneShift_{emp['employee_id']}_{day}"

    # 3. Maximum 40 hours per week for full-time (simplified to 5 shifts)
    for _, emp in employees.iterrows():
        max_shifts = emp['max_hours_per_week'] // shift_hours

        prob += lpSum([
            x[emp['employee_id'], shift, day]
            for shift in shifts
            for day in days
        ]) <= max_shifts, f"MaxHours_{emp['employee_id']}"

    # 4. Calculate overtime (hours beyond 40)
    for _, emp in employees.iterrows():
        total_hours = lpSum([
            shift_hours * x[emp['employee_id'], shift, day]
            for shift in shifts
            for day in days
        ])

        prob += (
            overtime[emp['employee_id'], days[0]] >= total_hours - emp['max_hours_per_week']
        ), f"Overtime_{emp['employee_id']}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    schedule = []
    for _, emp in employees.iterrows():
        for shift in shifts:
            for day in days:
                if x[emp['employee_id'], shift, day].varValue > 0.5:
                    schedule.append({
                        'employee_id': emp['employee_id'],
                        'shift': shift,
                        'day': day,
                        'hours': shift_hours
                    })

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'schedule': pd.DataFrame(schedule)
    }


result = optimize_workforce_schedule(demand, employees, shifts, days)

print(f"\nOptimization Status: {result['status']}")
print(f"Total Cost: ${result['total_cost']:,.2f}")
print(f"\nSchedule Summary:")
print(result['schedule'].groupby('shift').size())
```

---

## Advanced Scheduling Techniques

### Shift Bidding and Preference-Based Scheduling

```python
class PreferenceBasedScheduler:
    """
    Schedule based on employee preferences and seniority
    """

    def __init__(self, employees, shifts, days):
        self.employees = employees
        self.shifts = shifts
        self.days = days
        self.schedule = []

    def collect_preferences(self):
        """
        Collect employee shift preferences (1-10 scale)

        In practice, would come from employee input system
        """

        preferences = {}

        for _, emp in self.employees.iterrows():
            emp_id = emp['employee_id']
            preferences[emp_id] = {}

            for shift in self.shifts:
                for day in self.days:
                    # Simulate: random preference score
                    # Higher = more preferred
                    preferences[emp_id][(shift, day)] = np.random.randint(1, 11)

        return preferences

    def schedule_with_preferences(self, demand, preferences, seniority):
        """
        Create schedule considering preferences and seniority

        Algorithm:
        1. Sort employees by seniority
        2. Senior employees pick preferred shifts first
        3. Fill remaining shifts with junior employees
        4. Balance to meet demand

        Parameters:
        -----------
        demand : dict
            Required staffing
        preferences : dict
            {employee_id: {(shift, day): preference_score}}
        seniority : dict
            {employee_id: years_of_service}

        Returns:
        --------
        Schedule with preference satisfaction
        """

        # Sort employees by seniority
        employees_sorted = sorted(
            self.employees['employee_id'],
            key=lambda emp_id: seniority.get(emp_id, 0),
            reverse=True
        )

        remaining_demand = demand.copy()
        employee_assignments = {emp: 0 for emp in employees_sorted}

        schedule = []

        # Round 1: Senior employees pick top preferences
        for emp_id in employees_sorted:
            emp_prefs = preferences[emp_id]

            # Get top 5 preferred shifts
            top_prefs = sorted(emp_prefs.items(),
                             key=lambda x: x[1],
                             reverse=True)[:5]

            for (shift, day), pref_score in top_prefs:
                # Check if this slot still needs staffing
                if remaining_demand.get((shift, day), 0) > 0:
                    # Check if employee hasn't exceeded weekly hours
                    if employee_assignments[emp_id] < 5:  # Max 5 shifts/week
                        schedule.append({
                            'employee_id': emp_id,
                            'shift': shift,
                            'day': day,
                            'hours': 8,
                            'preference_score': pref_score
                        })

                        employee_assignments[emp_id] += 1
                        remaining_demand[(shift, day)] -= 8

                        break  # Move to next employee

        # Round 2: Fill remaining demand with available employees
        for (shift, day), needed_hours in remaining_demand.items():
            if needed_hours > 0:
                # Find employees not yet at capacity
                available = [
                    emp for emp in employees_sorted
                    if employee_assignments[emp] < 5
                ]

                for emp_id in available:
                    if needed_hours <= 0:
                        break

                    schedule.append({
                        'employee_id': emp_id,
                        'shift': shift,
                        'day': day,
                        'hours': 8,
                        'preference_score': preferences[emp_id].get((shift, day), 0)
                    })

                    employee_assignments[emp_id] += 1
                    needed_hours -= 8

        schedule_df = pd.DataFrame(schedule)

        # Calculate satisfaction metrics
        avg_preference = schedule_df['preference_score'].mean()
        pref_above_7 = (schedule_df['preference_score'] >= 7).sum() / len(schedule_df) * 100

        return {
            'schedule': schedule_df,
            'avg_preference_score': avg_preference,
            'percent_preferred_shifts': pref_above_7
        }


# Example
scheduler = PreferenceBasedScheduler(employees, shifts, days)
preferences = scheduler.collect_preferences()
seniority = {f'EMP{i:03d}': np.random.randint(1, 15) for i in range(1, 21)}

result_pref = scheduler.schedule_with_preferences(demand, preferences, seniority)

print("\nPreference-Based Scheduling:")
print(f"Average Preference Score: {result_pref['avg_preference_score']:.2f}/10")
print(f"Preferred Shifts (7+): {result_pref['percent_preferred_shifts']:.1f}%")
```

### Dynamic Scheduling with Real-Time Adjustments

```python
class DynamicScheduleManager:
    """
    Manage real-time schedule adjustments

    Handle call-outs, demand surges, schedule swaps
    """

    def __init__(self, base_schedule, employee_pool):
        self.base_schedule = base_schedule
        self.employee_pool = employee_pool
        self.adjustments = []

    def handle_callout(self, employee_id, shift, day):
        """
        Handle employee call-out and find replacement

        Priority:
        1. Overtime for already-scheduled employees
        2. On-call employees
        3. Temporary workers
        """

        print(f"Call-out: {employee_id} for {shift} on day {day}")

        # Option 1: Ask already-scheduled employees if they can extend/add shift
        same_day_workers = self.base_schedule[
            (self.base_schedule['day'] == day) &
            (self.base_schedule['employee_id'] != employee_id)
        ]

        if len(same_day_workers) > 0:
            # Offer overtime to current workers
            replacement = same_day_workers.iloc[0]['employee_id']
            print(f"  Replacement: {replacement} (overtime)")

            self.adjustments.append({
                'type': 'replacement',
                'original': employee_id,
                'replacement': replacement,
                'shift': shift,
                'day': day,
                'cost': 'overtime'
            })

            return replacement

        # Option 2: Call on-call employee
        on_call = self.employee_pool[self.employee_pool['type'] == 'on_call']

        if len(on_call) > 0:
            replacement = on_call.iloc[0]['employee_id']
            print(f"  Replacement: {replacement} (on-call)")

            self.adjustments.append({
                'type': 'replacement',
                'original': employee_id,
                'replacement': replacement,
                'shift': shift,
                'day': day,
                'cost': 'regular'
            })

            return replacement

        # Option 3: Hire temp worker
        print(f"  Replacement: TEMP (temporary agency)")

        self.adjustments.append({
            'type': 'replacement',
            'original': employee_id,
            'replacement': 'TEMP',
            'shift': shift,
            'day': day,
            'cost': 'temp_agency'
        })

        return 'TEMP'

    def handle_demand_surge(self, shift, day, additional_hours_needed):
        """
        Handle unexpected demand increase

        Options:
        1. Extend shifts (overtime)
        2. Call in off-duty employees
        3. Hire temps
        """

        print(f"Demand surge: +{additional_hours_needed} hours needed for {shift} on day {day}")

        # Option 1: Extend current shift
        current_workers = self.base_schedule[
            (self.base_schedule['shift'] == shift) &
            (self.base_schedule['day'] == day)
        ]

        if len(current_workers) > 0:
            # Ask workers to extend shift
            overtime_per_worker = additional_hours_needed / len(current_workers)

            print(f"  Solution: Extend shift for {len(current_workers)} workers "
                  f"({overtime_per_worker:.1f} OT hours each)")

            self.adjustments.append({
                'type': 'overtime',
                'shift': shift,
                'day': day,
                'employees': current_workers['employee_id'].tolist(),
                'ot_hours': overtime_per_worker
            })

            return 'overtime'

        # Option 2: Call in off-duty
        # (implementation similar to call-out)

        return 'temp'


# Example usage
manager = DynamicScheduleManager(schedule, employees)

# Simulate call-out
manager.handle_callout('EMP005', 'morning', 2)

# Simulate demand surge
manager.handle_demand_surge('afternoon', 3, 24)

print(f"\nTotal Adjustments: {len(manager.adjustments)}")
```

---

## Tools & Libraries

### Workforce Scheduling Software

**Specialized Scheduling:**
- **Workforce Software (Kronos)**: Enterprise scheduling and time tracking
- **ADP Workforce Now**: Integrated HR and scheduling
- **Shiftboard**: Shift scheduling and labor management
- **When I Work**: Employee scheduling app
- **Deputy**: Workforce management platform
- **7shifts**: Restaurant/retail scheduling
- **Humanity (TCP)**: Employee scheduling and tracking

**WMS with Labor Management:**
- **Manhattan WMS**: Labor management system (LMS)
- **Blue Yonder (JDA) WMS**: Labor planning and scheduling
- **SAP EWM**: Integrated labor management
- **HighJump WMS**: LMS module with engineered standards

### Python Libraries

```python
# Optimization
from pulp import *
from ortools.sat.python import cp_model

# Scheduling
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Constraint Programming
from constraint import Problem, AllDifferentConstraint
```

---

## Common Challenges & Solutions

### Challenge: Unpredictable Demand

**Problem:**
- Daily order volume varies ±30%
- Can't predict staffing needs accurately
- Either overstaffed (wasted cost) or understaffed (missed shipments)

**Solutions:**
- Flexible workforce (core + flex pool)
- On-call employees (4-hour notice)
- Cross-train for multiple tasks
- Dynamic scheduling (adjust intraday)
- Overtime as buffer (expensive but effective)
- Partner with temp agencies (fast ramp-up)

### Challenge: Employee Availability Constraints

**Problem:**
- Students only available evenings/weekends
- Parents need specific hours (drop-off/pick-up)
- Second jobs limit availability
- Many unavailability requests

**Solutions:**
- Self-service shift bidding system
- Build larger workforce with part-time
- Premium pay for less desirable shifts
- Advance notice for schedule (2+ weeks)
- Allow shift swaps (peer-to-peer)
- Honor availability constraints in optimization

### Challenge: Fairness and Morale

**Problem:**
- Some employees always get weekends off
- Senior employees get best shifts
- Perceived favoritism
- Low morale affects productivity

**Solutions:**
- Transparent scheduling rules
- Rotate undesirable shifts fairly
- Seniority-based shift bidding (fair process)
- Equal distribution of weekend shifts
- Track and publish fairness metrics
- Anonymous feedback on scheduling

### Challenge: Skill Mix Requirements

**Problem:**
- Not all employees can do all tasks
- Need certified forklift operators
- Quality control requires experienced workers
- Can't schedule purely on availability

**Solutions:**
- Track skills in employee database
- Include skill constraints in optimization
- Minimum skilled workers per shift
- Cross-training programs (expand skill base)
- Pay premiums for critical skills
- Certification tracking and renewal

### Challenge: Last-Minute Changes

**Problem:**
- Call-outs (sick, emergency)
- Demand spikes (unexpected large order)
- Equipment breakdown (need more labor)
- Schedule becomes obsolete

**Solutions:**
- On-call staff pool (10-15% of workforce)
- Automated call-out notification
- Temp agency on retainer
- Overtime authorization rules
- Real-time schedule adjustment app
- Plan for 5-10% call-out rate

---

## Output Format

### Workforce Schedule Report

**Weekly Schedule - Week of January 15-21, 2024**

**Schedule Summary:**

| Day | Shift | Employees | Total Hours | Demand (hrs) | Utilization |
|-----|-------|-----------|-------------|--------------|-------------|
| Mon | Morning | 12 | 96 | 92 | 96% |
| Mon | Afternoon | 10 | 80 | 78 | 98% |
| Mon | Evening | 6 | 48 | 45 | 94% |
| Tue | Morning | 11 | 88 | 85 | 97% |
| ... | ... | ... | ... | ... | ... |

**Employee Assignments:**

```
Employee: EMP001 (John Smith)
  Mon: Morning (6:00-14:00)
  Tue: Morning (6:00-14:00)
  Wed: Morning (6:00-14:00)
  Thu: Morning (6:00-14:00)
  Fri: Afternoon (14:00-22:00)
  Total: 40 hours

Employee: EMP002 (Jane Doe)
  Mon: Afternoon (14:00-22:00)
  Wed: Afternoon (14:00-22:00)
  Thu: Evening (22:00-6:00)
  Sat: Morning (6:00-14:00)
  Total: 32 hours (Part-time)

...
```

**Cost Analysis:**

| Category | Hours | Rate | Cost |
|----------|-------|------|------|
| Regular Time | 1,520 | $20/hr | $30,400 |
| Overtime | 85 | $30/hr | $2,550 |
| Temporary | 40 | $25/hr | $1,000 |
| **Total** | **1,645** | - | **$33,950** |

**Performance Metrics:**

- Average Utilization: 95%
- Overtime %: 5.2%
- Employee Satisfaction (Preferences): 8.2/10
- Coverage: 100% (no understaffed shifts)
- Cost per Hour: $20.64

**Schedule Compliance:**

- ✓ All shifts meet minimum staffing
- ✓ No employees exceed 40 regular hours
- ✓ Minimum 11-hour rest between shifts
- ✓ No more than 6 consecutive days worked
- ✓ Skill requirements met (forklift, QC)

---

## Questions to Ask

If you need more context:
1. What are your operating hours and shift structure?
2. What's your workforce size (full-time, part-time)?
3. How does demand vary (daily, weekly, seasonally)?
4. What scheduling constraints exist (union, overtime rules)?
5. What's your current scheduling method?
6. What's your labor cost structure (regular, OT, temp)?
7. Do employees have availability constraints or preferences?
8. Are there skill or certification requirements?

---

## Related Skills

- **task-assignment-problem**: For assigning workers to specific tasks
- **capacity-planning**: For long-term workforce planning
- **wave-planning-optimization**: For planning pick waves with labor
- **demand-forecasting**: For predicting labor demand
- **constraint-programming**: For complex scheduling constraints
- **optimization-modeling**: For mathematical scheduling models
- **production-scheduling**: For manufacturing workforce scheduling
