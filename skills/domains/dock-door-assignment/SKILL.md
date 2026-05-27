---
name: dock-door-assignment
description: When the user wants to optimize dock door assignments, schedule truck arrivals, or minimize yard congestion. Also use when the user mentions "dock scheduling," "door assignment," "yard management," "truck scheduling," "cross-dock optimization," or "appointment scheduling." For cross-docking operations, see cross-docking. For yard management, see yard-management.
---

# Dock Door Assignment

You are an expert in dock door assignment optimization and yard management. Your goal is to help optimize the assignment of inbound/outbound shipments to dock doors to minimize congestion, reduce dwell time, maximize throughput, and improve overall warehouse efficiency.

## Initial Assessment

Before optimizing dock door assignments, understand:

1. **Facility Layout**
   - Number of dock doors (inbound, outbound, shared)?
   - Door capabilities (height, width, equipment)?
   - Distance from doors to storage zones?
   - Staging area capacity near each door?
   - Cross-dock lanes vs. put-away lanes?

2. **Operations Profile**
   - Daily truck arrivals (inbound/outbound)?
   - Peak vs. off-peak times?
   - Average unload/load time per truck?
   - Mix of loads (full truckload, LTL, parcel)?
   - Appointment system in place?

3. **Product Characteristics**
   - Product types and storage zones?
   - Temperature requirements?
   - Hazmat or special handling?
   - High-velocity vs. slow-moving items?
   - Cross-dock percentage?

4. **Current Challenges**
   - Door utilization rates?
   - Truck waiting times?
   - Congestion hot spots?
   - Detention costs?
   - Labor allocation issues?

---

## Dock Door Assignment Framework

### Assignment Objectives

**Primary Goals:**
1. **Minimize Travel Distance**: Assign doors closest to destination storage zone
2. **Maximize Throughput**: Optimize door utilization and avoid congestion
3. **Balance Workload**: Even distribution across dock workers
4. **Minimize Detention**: Reduce truck waiting and dwell time
5. **Support Cross-Docking**: Align inbound/outbound for direct transfer

**Key Metrics:**
- Door utilization rate (target: 70-85%)
- Average truck dwell time (target: <90 minutes)
- Distance traveled (forklift feet/day)
- Detention costs ($ per day)
- Dock-to-stock time

### Assignment Strategies

**1. Zone-Based Assignment**
- Group doors by destination zone
- Inbound Door 1-5 → Zone A
- Inbound Door 6-10 → Zone B
- Minimizes average travel distance

**2. Product-Based Assignment**
- Hazmat doors (isolated, special equipment)
- Refrigerated doors (near cold storage)
- High-velocity doors (near forward pick)
- Bulk doors (larger staging area)

**3. Time-Slotted Assignment**
- Appointments in 30-60 minute windows
- Prevent arrival conflicts
- Smooth labor demand

**4. Cross-Dock Pairing**
- Pair inbound/outbound doors
- Direct transfer lanes
- Minimize re-handling

---

## Mathematical Formulation

### Assignment Problem Formulation

**Decision Variables:**
- x[i,j,t] = 1 if truck i assigned to door j at time t, 0 otherwise

**Parameters:**
- d[j,z] = distance from door j to storage zone z
- z[i] = destination zone for truck i
- p[i] = processing time for truck i
- a[i] = arrival time of truck i
- c[j] = capacity (trucks/day) of door j
- cap[j] = staging area capacity at door j

**Objective Function:**

```
Minimize:
  α × Σ Σ Σ (d[j,z[i]] × x[i,j,t])  # Travel distance
  + β × Σ Σ Σ (max(0, t - a[i]) × x[i,j,t])  # Waiting time
  + γ × Σ max_truck_overlap[j]  # Congestion penalty

where:
  α, β, γ = weights for different objectives
```

**Constraints:**

```python
# 1. Each truck assigned to exactly one door at one time
for i in trucks:
    Σ Σ x[i,j,t] = 1  for all j, t

# 2. Door capacity (trucks per time slot)
for j in doors:
    for t in time_slots:
        Σ x[i,j,t] ≤ door_capacity[j]  for all i

# 3. No overlap (truck occupies door for processing time)
for j in doors:
    for t in time_slots:
        Σ x[i,j,t'] ≤ 1  for all i, where t' in [t, t+p[i]]

# 4. Truck can't be assigned before arrival
for i in trucks:
    for t < a[i]:
        Σ x[i,j,t] = 0  for all j

# 5. Staging area capacity
for j in doors:
    Σ (volume[i] × x[i,j,t]) ≤ staging_capacity[j]  for all i, t
```

---

## Assignment Algorithms

### Greedy Assignment (Simple)

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def greedy_dock_assignment(trucks, doors, distances, processing_times):
    """
    Greedy heuristic for dock door assignment

    Assign each truck to the nearest available door

    Parameters:
    -----------
    trucks : list of dict
        [{truck_id, arrival_time, destination_zone, volume}, ...]
    doors : list of dict
        [{door_id, capacity, zone_affinity}, ...]
    distances : dict
        {(door_id, zone): distance}
    processing_times : dict
        {truck_id: duration_minutes}

    Returns:
    --------
    Assignment schedule
    """

    # Sort trucks by arrival time
    trucks_sorted = sorted(trucks, key=lambda x: x['arrival_time'])

    # Track door availability (door_id -> next_available_time)
    door_availability = {door['door_id']: datetime.min for door in doors}

    assignments = []

    for truck in trucks_sorted:
        truck_id = truck['truck_id']
        arrival = truck['arrival_time']
        dest_zone = truck['destination_zone']
        process_time = processing_times.get(truck_id, 60)  # default 60 min

        # Find best door
        best_door = None
        best_score = float('inf')

        for door in doors:
            door_id = door['door_id']
            available_time = door_availability[door_id]

            # Can't assign before door is available and truck arrives
            start_time = max(arrival, available_time)

            # Calculate score: distance + waiting time
            distance = distances.get((door_id, dest_zone), 1000)
            waiting_time = (start_time - arrival).total_seconds() / 60

            score = distance * 1.0 + waiting_time * 0.5

            if score < best_score:
                best_score = score
                best_door = door_id
                best_start = start_time

        # Assign truck to best door
        end_time = best_start + timedelta(minutes=process_time)
        door_availability[best_door] = end_time

        assignments.append({
            'truck_id': truck_id,
            'door_id': best_door,
            'scheduled_start': best_start,
            'scheduled_end': end_time,
            'arrival_time': arrival,
            'wait_time_min': (best_start - arrival).total_seconds() / 60,
            'destination_zone': dest_zone
        })

    return pd.DataFrame(assignments)


# Example usage
trucks = [
    {'truck_id': 'T001', 'arrival_time': datetime(2024, 1, 1, 8, 0),
     'destination_zone': 'A', 'volume': 1000},
    {'truck_id': 'T002', 'arrival_time': datetime(2024, 1, 1, 8, 15),
     'destination_zone': 'B', 'volume': 800},
    {'truck_id': 'T003', 'arrival_time': datetime(2024, 1, 1, 8, 30),
     'destination_zone': 'A', 'volume': 1200},
    {'truck_id': 'T004', 'arrival_time': datetime(2024, 1, 1, 9, 0),
     'destination_zone': 'C', 'volume': 900},
]

doors = [
    {'door_id': 'D1', 'capacity': 3, 'zone_affinity': 'A'},
    {'door_id': 'D2', 'capacity': 3, 'zone_affinity': 'B'},
    {'door_id': 'D3', 'capacity': 3, 'zone_affinity': 'C'},
]

distances = {
    ('D1', 'A'): 50, ('D1', 'B'): 150, ('D1', 'C'): 200,
    ('D2', 'A'): 150, ('D2', 'B'): 50, ('D2', 'C'): 180,
    ('D3', 'A'): 200, ('D3', 'B'): 180, ('D3', 'C'): 50,
}

processing_times = {
    'T001': 45, 'T002': 60, 'T003': 50, 'T004': 55
}

schedule = greedy_dock_assignment(trucks, doors, distances, processing_times)
print("Dock Assignment Schedule:")
print(schedule[['truck_id', 'door_id', 'scheduled_start', 'wait_time_min']])
```

### Hungarian Algorithm for Optimal Assignment

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

def hungarian_dock_assignment(trucks, doors, cost_matrix):
    """
    Optimal one-to-one assignment using Hungarian algorithm

    Use when number of trucks = number of available door slots

    Parameters:
    -----------
    trucks : list
        Truck identifiers
    doors : list
        Door identifiers
    cost_matrix : 2D numpy array
        cost[i,j] = cost of assigning truck i to door j

    Returns:
    --------
    Optimal assignments
    """

    # Solve assignment problem
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assignments = []
    total_cost = 0

    for i, j in zip(row_ind, col_ind):
        assignments.append({
            'truck_id': trucks[i],
            'door_id': doors[j],
            'cost': cost_matrix[i, j]
        })
        total_cost += cost_matrix[i, j]

    return {
        'assignments': assignments,
        'total_cost': total_cost
    }


# Example
trucks = ['T1', 'T2', 'T3', 'T4']
doors = ['D1', 'D2', 'D3', 'D4']

# Cost matrix: distance + penalty
cost_matrix = np.array([
    [50, 150, 200, 180],  # T1 costs to each door
    [150, 50, 180, 160],  # T2
    [50, 140, 210, 190],  # T3
    [200, 180, 50, 70],   # T4
])

result = hungarian_dock_assignment(trucks, doors, cost_matrix)
print("Optimal Assignment (Hungarian):")
for assignment in result['assignments']:
    print(f"  {assignment['truck_id']} → {assignment['door_id']} "
          f"(cost: {assignment['cost']})")
print(f"Total Cost: {result['total_cost']}")
```

### Mixed-Integer Programming Model

```python
from pulp import *
import pandas as pd

def optimize_dock_assignment(trucks, doors, time_slots, distances,
                             processing_times, arrivals):
    """
    Comprehensive dock assignment using MIP

    Parameters:
    -----------
    trucks : list
        Truck identifiers
    doors : list
        Door identifiers
    time_slots : list
        Time slot identifiers (e.g., [0, 1, 2, ...])
    distances : dict
        {(truck, door): distance_to_zone}
    processing_times : dict
        {truck: slots_required}
    arrivals : dict
        {truck: earliest_slot}

    Returns:
    --------
    Optimal assignment with timing
    """

    prob = LpProblem("Dock_Assignment", LpMinimize)

    # Decision variables
    # x[i,j,t] = 1 if truck i assigned to door j starting at time t
    x = LpVariable.dicts("assign",
                        [(i, j, t) for i in trucks
                                   for j in doors
                                   for t in time_slots],
                        cat='Binary')

    # Waiting time variables
    wait = LpVariable.dict("wait",
                          trucks,
                          lowBound=0,
                          cat='Continuous')

    # Objective: minimize weighted sum of distance and waiting
    alpha = 1.0  # distance weight
    beta = 0.5   # waiting time weight

    prob += (
        alpha * lpSum([
            distances.get((i, j), 1000) * x[i, j, t]
            for i in trucks for j in doors for t in time_slots
        ]) +
        beta * lpSum([wait[i] for i in trucks])
    ), "Total_Cost"

    # Constraints

    # 1. Each truck assigned to exactly one door-time combination
    for i in trucks:
        prob += lpSum([
            x[i, j, t] for j in doors for t in time_slots
        ]) == 1, f"Truck_{i}_Assignment"

    # 2. Door capacity: no overlapping assignments
    for j in doors:
        for t in time_slots:
            # Count trucks using this door at this time
            prob += lpSum([
                x[i, j, t_start]
                for i in trucks
                for t_start in range(max(0, t - processing_times.get(i, 1) + 1), t + 1)
                if t_start in time_slots
            ]) <= 1, f"Door_{j}_Time_{t}_Capacity"

    # 3. Truck can't be assigned before arrival
    for i in trucks:
        arrival_slot = arrivals.get(i, 0)
        for t in time_slots:
            if t < arrival_slot:
                for j in doors:
                    prob += x[i, j, t] == 0, f"Truck_{i}_Arrival_Time_{t}"

    # 4. Calculate waiting time
    for i in trucks:
        arrival_slot = arrivals.get(i, 0)
        prob += wait[i] >= lpSum([
            (t - arrival_slot) * x[i, j, t]
            for j in doors for t in time_slots
        ]), f"Wait_{i}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = []
    for i in trucks:
        for j in doors:
            for t in time_slots:
                if x[i, j, t].varValue > 0.5:
                    assignments.append({
                        'truck_id': i,
                        'door_id': j,
                        'time_slot': t,
                        'wait_slots': wait[i].varValue if wait[i].varValue else 0
                    })

    return {
        'status': LpStatus[prob.status],
        'objective_value': value(prob.objective),
        'assignments': pd.DataFrame(assignments)
    }


# Example
trucks = ['T1', 'T2', 'T3', 'T4', 'T5']
doors = ['D1', 'D2', 'D3']
time_slots = list(range(0, 20))  # 20 time slots (e.g., 30-min each)

# Distance from each truck's destination zone to each door
distances = {
    ('T1', 'D1'): 50, ('T1', 'D2'): 150, ('T1', 'D3'): 200,
    ('T2', 'D1'): 150, ('T2', 'D2'): 50, ('T2', 'D3'): 180,
    ('T3', 'D1'): 50, ('T3', 'D2'): 140, ('T3', 'D3'): 210,
    ('T4', 'D1'): 200, ('T4', 'D2'): 180, ('T4', 'D3'): 50,
    ('T5', 'D1'): 100, ('T5', 'D2'): 100, ('T5', 'D3'): 100,
}

# Processing time in time slots (e.g., 2 slots = 1 hour)
processing_times = {'T1': 2, 'T2': 3, 'T3': 2, 'T4': 3, 'T5': 2}

# Arrival times (time slot)
arrivals = {'T1': 0, 'T2': 2, 'T3': 3, 'T4': 5, 'T5': 6}

result = optimize_dock_assignment(
    trucks, doors, time_slots, distances, processing_times, arrivals
)

print(f"Optimization Status: {result['status']}")
print(f"Objective Value: {result['objective_value']:.2f}")
print("\nAssignments:")
print(result['assignments'])
```

---

## Advanced Techniques

### Cross-Dock Door Pairing

```python
def optimize_crossdock_pairing(inbound_trucks, outbound_trucks,
                               crossdock_items, doors, distances):
    """
    Optimize door assignment for cross-docking operations

    Match inbound and outbound doors to minimize transfer distance

    Parameters:
    -----------
    inbound_trucks : list of dict
        [{truck_id, arrival_time, items: [sku_list]}, ...]
    outbound_trucks : list of dict
        [{truck_id, departure_time, items: [sku_list]}, ...]
    crossdock_items : dict
        {inbound_truck: {outbound_truck: [items_to_transfer]}}
    doors : dict
        {'inbound': [door_list], 'outbound': [door_list]}
    distances : dict
        {(inbound_door, outbound_door): transfer_distance}

    Returns:
    --------
    Paired door assignments
    """

    prob = LpProblem("CrossDock_Pairing", LpMinimize)

    inbound_ids = [t['truck_id'] for t in inbound_trucks]
    outbound_ids = [t['truck_id'] for t in outbound_trucks]
    inbound_doors = doors['inbound']
    outbound_doors = doors['outbound']

    # Decision variables
    # y_in[i,d] = 1 if inbound truck i assigned to door d
    y_in = LpVariable.dicts("inbound",
                           [(i, d) for i in inbound_ids for d in inbound_doors],
                           cat='Binary')

    # y_out[i,d] = 1 if outbound truck i assigned to door d
    y_out = LpVariable.dicts("outbound",
                            [(i, d) for i in outbound_ids for d in outbound_doors],
                            cat='Binary')

    # Flow variables: f[in_door, out_door] = volume transferred
    f = LpVariable.dicts("flow",
                        [(d1, d2) for d1 in inbound_doors for d2 in outbound_doors],
                        lowBound=0,
                        cat='Continuous')

    # Objective: minimize transfer distance
    prob += lpSum([
        distances.get((d1, d2), 100) * f[d1, d2]
        for d1 in inbound_doors for d2 in outbound_doors
    ]), "Transfer_Distance"

    # Constraints

    # Each truck assigned to one door
    for i in inbound_ids:
        prob += lpSum([y_in[i, d] for d in inbound_doors]) == 1

    for i in outbound_ids:
        prob += lpSum([y_out[i, d] for d in outbound_doors]) == 1

    # Link flow to door assignments
    # (Simplified: would need actual crossdock volumes)
    for d1 in inbound_doors:
        for d2 in outbound_doors:
            # Flow limited by door assignments
            prob += f[d1, d2] <= 1000, f"Flow_{d1}_{d2}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    inbound_assignments = {}
    outbound_assignments = {}

    for i in inbound_ids:
        for d in inbound_doors:
            if y_in[i, d].varValue > 0.5:
                inbound_assignments[i] = d

    for i in outbound_ids:
        for d in outbound_doors:
            if y_out[i, d].varValue > 0.5:
                outbound_assignments[i] = d

    flows = {}
    for d1 in inbound_doors:
        for d2 in outbound_doors:
            if f[d1, d2].varValue > 0.01:
                flows[(d1, d2)] = f[d1, d2].varValue

    return {
        'status': LpStatus[prob.status],
        'inbound_assignments': inbound_assignments,
        'outbound_assignments': outbound_assignments,
        'flows': flows,
        'total_distance': value(prob.objective)
    }
```

### Appointment Scheduling System

```python
from datetime import datetime, timedelta

class DockAppointmentScheduler:
    """
    Manage dock appointment scheduling with time windows
    """

    def __init__(self, doors, operating_hours, slot_duration=30):
        """
        Initialize scheduler

        Parameters:
        -----------
        doors : list
            Available door IDs
        operating_hours : dict
            {'start': time, 'end': time}
        slot_duration : int
            Minutes per appointment slot
        """
        self.doors = doors
        self.operating_hours = operating_hours
        self.slot_duration = slot_duration
        self.appointments = {}  # {(door, datetime): truck_id}
        self.truck_schedules = {}  # {truck_id: (door, start_time, end_time)}

    def generate_time_slots(self, date):
        """Generate available time slots for a date"""
        slots = []
        current = datetime.combine(date, self.operating_hours['start'])
        end = datetime.combine(date, self.operating_hours['end'])

        while current < end:
            slots.append(current)
            current += timedelta(minutes=self.slot_duration)

        return slots

    def find_available_slots(self, date, duration_minutes, preferred_doors=None):
        """
        Find available appointment slots

        Parameters:
        -----------
        date : datetime.date
            Target date
        duration_minutes : int
            Required duration
        preferred_doors : list, optional
            Preferred door IDs

        Returns:
        --------
        List of available (door, start_time) tuples
        """
        time_slots = self.generate_time_slots(date)
        slots_needed = int(np.ceil(duration_minutes / self.slot_duration))

        available = []
        doors_to_check = preferred_doors if preferred_doors else self.doors

        for door in doors_to_check:
            for i, start_time in enumerate(time_slots[:-slots_needed + 1]):
                # Check if all required slots are free
                all_free = True
                for offset in range(slots_needed):
                    slot_time = time_slots[i + offset]
                    if (door, slot_time) in self.appointments:
                        all_free = False
                        break

                if all_free:
                    end_time = time_slots[i + slots_needed - 1] + \
                              timedelta(minutes=self.slot_duration)
                    available.append({
                        'door': door,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': duration_minutes
                    })

        return available

    def book_appointment(self, truck_id, door, start_time, duration_minutes):
        """
        Book an appointment

        Returns:
        --------
        Success (bool) and confirmation details
        """
        slots_needed = int(np.ceil(duration_minutes / self.slot_duration))

        # Check availability
        current_slot = start_time
        for _ in range(slots_needed):
            if (door, current_slot) in self.appointments:
                return {
                    'success': False,
                    'message': f'Slot {current_slot} on {door} already booked'
                }
            current_slot += timedelta(minutes=self.slot_duration)

        # Book slots
        current_slot = start_time
        for _ in range(slots_needed):
            self.appointments[(door, current_slot)] = truck_id
            current_slot += timedelta(minutes=self.slot_duration)

        end_time = start_time + timedelta(minutes=duration_minutes)
        self.truck_schedules[truck_id] = (door, start_time, end_time)

        return {
            'success': True,
            'truck_id': truck_id,
            'door': door,
            'start_time': start_time,
            'end_time': end_time,
            'confirmation': f'{truck_id} booked on {door} from {start_time} to {end_time}'
        }

    def cancel_appointment(self, truck_id):
        """Cancel an existing appointment"""
        if truck_id not in self.truck_schedules:
            return {'success': False, 'message': 'Appointment not found'}

        door, start_time, end_time = self.truck_schedules[truck_id]

        # Remove appointment slots
        current_slot = start_time
        while current_slot < end_time:
            if (door, current_slot) in self.appointments:
                del self.appointments[(door, current_slot)]
            current_slot += timedelta(minutes=self.slot_duration)

        del self.truck_schedules[truck_id]

        return {'success': True, 'message': f'Appointment {truck_id} cancelled'}

    def get_door_utilization(self, date):
        """Calculate door utilization for a date"""
        time_slots = self.generate_time_slots(date)
        total_slots = len(time_slots) * len(self.doors)

        booked_slots = sum(
            1 for (door, slot_time) in self.appointments
            if slot_time.date() == date
        )

        return {
            'date': date,
            'utilization': (booked_slots / total_slots * 100) if total_slots > 0 else 0,
            'booked_slots': booked_slots,
            'total_slots': total_slots
        }


# Example usage
from datetime import time

scheduler = DockAppointmentScheduler(
    doors=['D1', 'D2', 'D3', 'D4'],
    operating_hours={'start': time(6, 0), 'end': time(18, 0)},
    slot_duration=30
)

# Find available slots for 90-minute appointment
target_date = datetime(2024, 1, 15).date()
available = scheduler.find_available_slots(target_date, 90, preferred_doors=['D1', 'D2'])

print(f"Available slots on {target_date}:")
for slot in available[:5]:  # Show first 5
    print(f"  {slot['door']}: {slot['start_time'].strftime('%H:%M')} - "
          f"{slot['end_time'].strftime('%H:%M')}")

# Book appointments
booking1 = scheduler.book_appointment('TRUCK001', 'D1',
                                     datetime(2024, 1, 15, 8, 0), 90)
print(f"\n{booking1['confirmation']}")

booking2 = scheduler.book_appointment('TRUCK002', 'D1',
                                     datetime(2024, 1, 15, 10, 0), 60)
print(booking2['confirmation'])

# Check utilization
util = scheduler.get_door_utilization(target_date)
print(f"\nDoor Utilization: {util['utilization']:.1f}%")
```

---

## Tools & Libraries

### Dock Management Software

**Warehouse Management Systems with Dock Scheduling:**
- **Manhattan WMS**: Advanced dock appointment scheduling
- **Blue Yonder (JDA) WMS**: Yard and dock management
- **SAP EWM**: Extended warehouse with dock door optimization
- **HighJump WMS**: Dock scheduling and labor management
- **Oracle WMS**: Dock door assignment and appointment booking

**Specialized Yard Management Systems (YMS):**
- **C3 Yard Management**: Dock scheduling and trailer tracking
- **Descartes Yard Management**: Appointment scheduling and optimization
- **FourKites Yard Management**: Real-time visibility and scheduling
- **PINC Yard Management**: RFID-based yard and dock tracking
- **Kaleris (formerly Navis)**: Yard orchestration platform

**Transportation Management Systems (TMS) with Dock Integration:**
- **MercuryGate TMS**: Dock appointment scheduling
- **BluJay Solutions**: Dock scheduling and carrier collaboration
- **E2open TMS**: Integrated dock and yard management

### Python Libraries

```python
# Optimization
from pulp import *  # Linear programming
from scipy.optimize import linear_sum_assignment  # Hungarian algorithm
from ortools.sat.python import cp_model  # Constraint programming

# Scheduling
import schedule  # Job scheduling
from datetime import datetime, timedelta
import pandas as pd

# Simulation
import simpy  # Discrete event simulation for dock operations
```

---

## Common Challenges & Solutions

### Challenge: Uneven Arrival Patterns

**Problem:**
- Morning peak with long queues
- Afternoon lull with idle doors
- Unpredictable carrier arrivals

**Solutions:**
- Implement mandatory appointment system
- Offer incentives for off-peak appointments (priority unloading, reduced fees)
- Communicate detention charges for late/early arrivals
- Use dynamic pricing for peak slots
- Reserve capacity for urgent/unscheduled trucks (10-15%)
- Pre-schedule recurring routes (milk runs)

### Challenge: Cross-Dock Inefficiency

**Problem:**
- Long transfer distances between inbound/outbound doors
- Multiple touches and re-handling
- Staging area congestion

**Solutions:**
- Dedicate adjacent door pairs for cross-dock
- Use flow-through dock configuration (I-shaped or L-shaped)
- Pre-assign based on SKU overlap between inbound/outbound
- Implement direct loading (inbound pallet → outbound trailer)
- Use conveyor or AGV for cross-dock transfers
- Real-time visibility of inbound/outbound synchronization

### Challenge: Variable Processing Times

**Problem:**
- Some trucks take 30 min, others 3 hours
- Schedule becomes unreliable
- Cascading delays

**Solutions:**
- Historical data analysis by carrier, load type
- Buffer time between appointments (15-20%)
- Adjust slot duration based on load type (LTL=30min, FTL=90min)
- Allow early departure if done ahead
- Dynamic re-scheduling for delays >30 min
- Split large loads across multiple doors

### Challenge: Equipment Conflicts

**Problem:**
- Limited forklifts and dock equipment
- Multiple doors compete for resources
- Bottlenecks at busy times

**Solutions:**
- Schedule labor and equipment concurrently with doors
- Reserve equipment for high-priority doors
- Cross-train operators for flexibility
- Use zone-based equipment assignment
- Real-time equipment tracking and dispatch
- Shared equipment pool with dynamic allocation

### Challenge: Seasonal and Peak Surges

**Problem:**
- Holiday season doubles truck volume
- Existing doors insufficient
- Overtime costs skyrocket

**Solutions:**
- Add temporary yard storage (drop trailers)
- Extended operating hours (overnight shifts)
- Pre-receive inventory before peak
- Rent overflow capacity (3PL, public warehouse)
- Use mobile yard ramps (additional doors)
- Negotiate staggered delivery windows with suppliers

### Challenge: Live Unload vs. Drop Trailer

**Problem:**
- Carriers charge detention for live unload
- Trailer pool required for drop trailer
- Mixed mode creates scheduling complexity

**Solutions:**
- Prefer drop trailer for all non-urgent inbound
- Negotiate carrier contracts (detention fees vs. trailer pools)
- Dedicated doors for live unload (fast lanes)
- Pre-assign live unload to high-throughput doors
- Track and minimize dwell time (target <2 hours)
- Use yard management system to optimize trailer moves

---

## Output Format

### Dock Assignment Schedule

**Daily Door Schedule - January 15, 2024:**

| Time | D1 (Zone A) | D2 (Zone B) | D3 (Zone C) | D4 (Cross-Dock) |
|------|-------------|-------------|-------------|-----------------|
| 06:00-07:30 | T101 (Inbound) | T102 (Inbound) | - | T201 (Outbound) |
| 07:30-09:00 | T103 (Inbound) | - | T104 (Inbound) | - |
| 09:00-10:30 | - | T105 (Inbound) | T106 (Inbound) | T202 (Outbound) |
| 10:30-12:00 | T107 (Inbound) | T108 (Inbound) | - | T203 (Outbound) |
| 12:00-13:30 | T109 (Inbound) | - | T110 (Inbound) | - |
| 13:30-15:00 | - | T111 (Inbound) | - | T204 (Outbound) |
| 15:00-16:30 | T112 (Inbound) | T113 (Inbound) | T114 (Inbound) | T205 (Outbound) |

**Performance Metrics:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Door Utilization | 78% | 70-85% | ✓ On Target |
| Avg Wait Time | 12 min | <15 min | ✓ On Target |
| Detention Events | 2 | <5 | ✓ On Target |
| Avg Travel Distance | 285 ft | <300 ft | ✓ On Target |
| Trucks Processed | 28 | 25-30 | ✓ On Target |

**Assignment Details:**

```
Truck T101:
  - Carrier: ABC Freight
  - Arrival: 05:45 (15 min early)
  - Assigned Door: D1
  - Scheduled: 06:00 - 07:30
  - Destination Zone: A
  - Distance to Zone: 45 ft
  - Status: Completed on time

Truck T102:
  - Carrier: XYZ Logistics
  - Arrival: 06:05 (5 min late)
  - Assigned Door: D2
  - Scheduled: 06:00 - 07:30
  - Destination Zone: B
  - Distance to Zone: 52 ft
  - Status: Completed with 10 min delay
```

**Optimization Summary:**

- Total Travel Distance: 7,980 ft (15% reduction vs. unoptimized)
- Total Wait Time: 336 min (avg 12 min/truck)
- Detention Costs: $150 (2 events × $75)
- Door Utilization: D1=85%, D2=78%, D3=68%, D4=82%

**Recommendations:**
1. Door D3 underutilized - consider consolidating with D1
2. Zone A has highest inbound volume - add one door affinity
3. Peak time 09:00-11:00 - shift 2 appointments to afternoon
4. Cross-dock efficiency good - maintain current pairing

---

## Questions to Ask

If you need more context:
1. How many dock doors (inbound/outbound/shared)?
2. What's the daily/weekly truck volume?
3. Do you have an appointment scheduling system?
4. What are average unload/load times?
5. What's the warehouse zone layout relative to doors?
6. Are there cross-dock operations?
7. What are current detention costs?
8. What equipment is used (forklifts, conveyors)?

---

## Related Skills

- **cross-docking**: For cross-dock operations optimization
- **yard-management**: For broader yard and trailer management
- **warehouse-design**: For dock configuration and layout
- **task-assignment-problem**: For assigning dock workers to doors
- **workforce-scheduling**: For dock labor scheduling
- **vehicle-routing-problem**: For coordinating inbound/outbound routes
- **appointment-scheduling**: For carrier appointment systems
- **constraint-programming**: For complex scheduling constraints
