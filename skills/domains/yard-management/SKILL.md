---
name: yard-management
description: When the user wants to optimize yard operations, manage trailer parking, or improve dock door utilization. Also use when the user mentions "yard management," "trailer tracking," "yard jockey," "drop trailer program," "trailer pool," "dock scheduling," or "gate management." For cross-dock operations, see cross-docking. For warehouse design, see warehouse-design.
---

# Yard Management

You are an expert in yard management and trailer logistics. Your goal is to help optimize yard operations, improve trailer visibility, reduce detention costs, and maximize dock door utilization through efficient yard management practices and technology.

## Initial Assessment

Before optimizing yard operations, understand:

1. **Facility Characteristics**
   - Yard size and capacity? (trailer spots)
   - Number of dock doors?
   - Layout constraints? (space, access, turning radius)
   - Gate security and check-in process?

2. **Operational Volume**
   - Daily inbound/outbound trailers?
   - Average dwell time per trailer?
   - Peak times and patterns?
   - Types of trailers? (dry van, reefer, flatbed)

3. **Current Challenges**
   - Trailer visibility issues?
   - Long wait times at gate or dock?
   - High detention/demurrage costs?
   - Difficulty finding trailers in yard?
   - Congestion at doors?

4. **Resources**
   - Number of yard jockeys?
   - Yard tractors available?
   - Technology in place? (YMS, GPS, RFID)
   - Staffing and shifts?

---

## Yard Management Framework

### Core Functions of Yard Management

**1. Gate Management**
- Check-in/check-out process
- Carrier credential verification
- BOL and documentation
- Safety inspections
- Appointment verification

**2. Yard Planning & Layout**
- Trailer parking locations
- Staging zones by priority
- Dock door assignments
- Traffic flow optimization

**3. Trailer Movement**
- Yard jockey dispatch
- Spotting trailers at doors
- Repositioning for loading/unloading
- Trailer pool management

**4. Tracking & Visibility**
- Real-time trailer location
- Load status (empty, loaded, in-process)
- Dwell time monitoring
- Exception management

**5. Dock Scheduling**
- Appointment booking
- Door assignment
- Load/unload coordination
- Carrier communication

---

## Yard Layout Optimization

### Yard Design Principles

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

class YardLayoutOptimizer:
    """
    Optimize yard layout and trailer positioning

    Minimize jockey moves and door spotting time
    """

    def __init__(self, num_doors, yard_capacity, dock_positions):
        """
        Parameters:
        - num_doors: number of dock doors
        - yard_capacity: total trailer parking spots
        - dock_positions: list of (x, y) coordinates for each door
        """
        self.num_doors = num_doors
        self.yard_capacity = yard_capacity
        self.dock_positions = np.array(dock_positions)

    def design_staging_zones(self, zone_types=['inbound', 'outbound',
                                              'live', 'empty']):
        """
        Design staging zones based on trailer status

        Returns optimal zone assignments
        """

        # Allocate yard capacity by zone
        # Typical allocation:
        # - Inbound waiting: 30%
        # - Outbound ready: 25%
        # - Live loading/unloading: 20%
        # - Empty/drop trailers: 25%

        allocations = {
            'inbound': int(self.yard_capacity * 0.30),
            'outbound': int(self.yard_capacity * 0.25),
            'live': int(self.yard_capacity * 0.20),
            'empty': int(self.yard_capacity * 0.25)
        }

        # Position zones near relevant doors
        zones = {}

        # Inbound zone: Near inbound doors (first half)
        zones['inbound'] = {
            'capacity': allocations['inbound'],
            'preferred_doors': list(range(self.num_doors // 2)),
            'avg_distance_to_door': 50  # feet
        }

        # Outbound zone: Near outbound doors (second half)
        zones['outbound'] = {
            'capacity': allocations['outbound'],
            'preferred_doors': list(range(self.num_doors // 2, self.num_doors)),
            'avg_distance_to_door': 50
        }

        # Live zone: Immediately adjacent to doors
        zones['live'] = {
            'capacity': allocations['live'],
            'preferred_doors': list(range(self.num_doors)),
            'avg_distance_to_door': 20  # Closest
        }

        # Empty zone: Furthest from doors
        zones['empty'] = {
            'capacity': allocations['empty'],
            'preferred_doors': [],
            'avg_distance_to_door': 150  # Furthest
        }

        return zones

    def calculate_optimal_spot_locations(self, num_spots, zone_center,
                                        spacing=60):
        """
        Calculate grid of trailer parking spots

        Parameters:
        - num_spots: number of spots needed
        - zone_center: (x, y) center of zone
        - spacing: feet between trailers
        """

        # Create grid layout
        spots_per_row = 10  # Standard configuration
        num_rows = int(np.ceil(num_spots / spots_per_row))

        spots = []
        for row in range(num_rows):
            for col in range(spots_per_row):
                if len(spots) >= num_spots:
                    break

                x = zone_center[0] + (col * spacing)
                y = zone_center[1] + (row * spacing)

                spots.append({
                    'spot_id': f'S{len(spots)+1:03d}',
                    'position': (x, y),
                    'row': row,
                    'col': col
                })

        return spots

    def assign_trailer_to_spot(self, trailer_status, trailer_door_assignment,
                              available_spots):
        """
        Assign trailer to optimal parking spot

        Minimize distance to assigned door

        Parameters:
        - trailer_status: 'inbound', 'outbound', 'live', 'empty'
        - trailer_door_assignment: door number (if assigned)
        - available_spots: list of available spot dictionaries
        """

        # Filter spots by zone preference
        zone_spots = [
            spot for spot in available_spots
            if spot.get('zone') == trailer_status
        ]

        if not zone_spots:
            zone_spots = available_spots  # Use any available

        if not zone_spots:
            return None  # Yard full

        # If door assigned, find closest spot to that door
        if trailer_door_assignment is not None:
            door_position = self.dock_positions[trailer_door_assignment]

            # Calculate distances
            distances = [
                distance.euclidean(spot['position'], door_position)
                for spot in zone_spots
            ]

            # Select closest spot
            best_spot_idx = np.argmin(distances)
            assigned_spot = zone_spots[best_spot_idx]

        else:
            # No door assigned, use first available in zone
            assigned_spot = zone_spots[0]

        return assigned_spot

    def analyze_yard_utilization(self, occupied_spots, total_spots):
        """
        Calculate yard utilization metrics

        Returns utilization by zone and overall
        """

        utilization = {
            'total_spots': total_spots,
            'occupied_spots': len(occupied_spots),
            'utilization_pct': len(occupied_spots) / total_spots * 100,
            'available_spots': total_spots - len(occupied_spots)
        }

        # By zone
        zones = {}
        for spot in occupied_spots:
            zone = spot.get('zone', 'unknown')
            if zone not in zones:
                zones[zone] = 0
            zones[zone] += 1

        utilization['by_zone'] = zones

        return utilization

# Example usage
optimizer = YardLayoutOptimizer(
    num_doors=40,
    yard_capacity=200,
    dock_positions=[(i*20, 0) for i in range(40)]  # Doors in a line
)

zones = optimizer.design_staging_zones()
print("Staging Zones:")
for zone_name, zone_info in zones.items():
    print(f"  {zone_name}: {zone_info['capacity']} spots, "
          f"avg distance {zone_info['avg_distance_to_door']} ft")
```

---

## Dock Door Scheduling

### Appointment Scheduling System

```python
import pandas as pd
from datetime import datetime, timedelta

class DockSchedulingSystem:
    """
    Manage dock door appointments and scheduling

    Optimize door utilization and minimize wait times
    """

    def __init__(self, num_doors, hours_of_operation=(6, 22)):
        """
        Parameters:
        - num_doors: number of dock doors
        - hours_of_operation: (start_hour, end_hour) tuple
        """
        self.num_doors = num_doors
        self.start_hour = hours_of_operation[0]
        self.end_hour = hours_of_operation[1]
        self.schedule = {}

    def create_time_slots(self, date, slot_duration_hours=2):
        """
        Create available time slots for a date

        Returns list of time slots
        """

        slots = []
        current_time = datetime.combine(date, datetime.min.time()).replace(
            hour=self.start_hour
        )
        end_time = datetime.combine(date, datetime.min.time()).replace(
            hour=self.end_hour
        )

        while current_time < end_time:
            slot_end = current_time + timedelta(hours=slot_duration_hours)

            slots.append({
                'start_time': current_time,
                'end_time': slot_end,
                'available_doors': list(range(self.num_doors))
            })

            current_time = slot_end

        return slots

    def book_appointment(self, carrier, appointment_type, requested_time,
                        duration_hours=2, door_preference=None):
        """
        Book dock appointment

        Parameters:
        - carrier: carrier name
        - appointment_type: 'inbound' or 'outbound'
        - requested_time: datetime
        - duration_hours: expected duration
        - door_preference: specific door number (optional)
        """

        date = requested_time.date()

        # Get or create slots for date
        if date not in self.schedule:
            self.schedule[date] = self.create_time_slots(date)

        # Find matching time slot
        for slot in self.schedule[date]:
            if (slot['start_time'] <= requested_time <
                slot['end_time'] and
                len(slot['available_doors']) > 0):

                # Assign door
                if door_preference and door_preference in slot['available_doors']:
                    assigned_door = door_preference
                else:
                    assigned_door = slot['available_doors'][0]

                # Remove door from available
                slot['available_doors'].remove(assigned_door)

                appointment = {
                    'appointment_id': f"APT{len(self.schedule)*100 + 1}",
                    'carrier': carrier,
                    'type': appointment_type,
                    'scheduled_time': slot['start_time'],
                    'door': assigned_door,
                    'duration': duration_hours,
                    'status': 'scheduled'
                }

                return appointment

        # No available slot found
        return {
            'error': 'No available slot',
            'requested_time': requested_time,
            'suggestion': 'Try different time or date'
        }

    def check_availability(self, date, appointment_type=None):
        """
        Check door availability for a date

        Returns available slots
        """

        if date not in self.schedule:
            self.schedule[date] = self.create_time_slots(date)

        availability = []

        for slot in self.schedule[date]:
            if len(slot['available_doors']) > 0:
                availability.append({
                    'time_slot': f"{slot['start_time'].strftime('%H:%M')} - "
                                f"{slot['end_time'].strftime('%H:%M')}",
                    'available_doors': len(slot['available_doors']),
                    'door_numbers': slot['available_doors'][:5]  # Show first 5
                })

        return availability

    def calculate_utilization(self, date):
        """
        Calculate door utilization for a date

        Returns utilization percentage
        """

        if date not in self.schedule:
            return {'utilization': 0, 'message': 'No appointments scheduled'}

        total_door_slots = 0
        used_door_slots = 0

        for slot in self.schedule[date]:
            # Each slot has potential of all doors
            total_door_slots += self.num_doors

            # Count used doors (initially available - currently available)
            used_doors = self.num_doors - len(slot['available_doors'])
            used_door_slots += used_doors

        utilization = used_door_slots / total_door_slots * 100 if total_door_slots > 0 else 0

        return {
            'date': date,
            'utilization_pct': utilization,
            'total_door_slots': total_door_slots,
            'used_door_slots': used_door_slots,
            'target_utilization': 75  # Best practice target
        }

    def optimize_door_assignments(self, appointments):
        """
        Re-optimize door assignments to minimize moves

        Group similar appointment types on adjacent doors
        """

        # Separate by type
        inbound = [a for a in appointments if a['type'] == 'inbound']
        outbound = [a for a in appointments if a['type'] == 'outbound']

        # Assign inbound to first half of doors
        inbound_doors = list(range(self.num_doors // 2))
        outbound_doors = list(range(self.num_doors // 2, self.num_doors))

        # Reassign
        for idx, appt in enumerate(inbound):
            if idx < len(inbound_doors):
                appt['door'] = inbound_doors[idx]

        for idx, appt in enumerate(outbound):
            if idx < len(outbound_doors):
                appt['door'] = outbound_doors[idx]

        return appointments

# Example usage
scheduler = DockSchedulingSystem(num_doors=40)

# Book appointments
appt1 = scheduler.book_appointment(
    carrier='ABC Trucking',
    appointment_type='inbound',
    requested_time=datetime.now().replace(hour=8, minute=0)
)

print(f"Appointment booked: Door {appt1.get('door')} at "
      f"{appt1.get('scheduled_time')}")

# Check availability
tomorrow = datetime.now().date() + timedelta(days=1)
availability = scheduler.check_availability(tomorrow)
print(f"\nAvailability for {tomorrow}:")
for slot in availability[:3]:
    print(f"  {slot['time_slot']}: {slot['available_doors']} doors available")
```

---

## Trailer Tracking & Visibility

### Yard Management System (YMS) Core Functions

```python
class YardManagementSystem:
    """
    Core yard management system functionality

    Track trailers, manage moves, monitor dwell time
    """

    def __init__(self):
        self.trailers = {}  # trailer_id -> trailer info
        self.yard_spots = {}  # spot_id -> trailer_id
        self.move_history = []
        self.alerts = []

    def check_in_trailer(self, trailer_id, carrier, seal_number,
                        trailer_type='dry_van', is_loaded=True):
        """
        Check in trailer at gate

        Creates trailer record in system
        """

        check_in_time = datetime.now()

        trailer_info = {
            'trailer_id': trailer_id,
            'carrier': carrier,
            'seal_number': seal_number,
            'trailer_type': trailer_type,
            'is_loaded': is_loaded,
            'status': 'in_yard',
            'check_in_time': check_in_time,
            'current_location': 'gate',
            'dock_door': None,
            'moves': 0
        }

        self.trailers[trailer_id] = trailer_info

        # Log move
        self.move_history.append({
            'trailer_id': trailer_id,
            'timestamp': check_in_time,
            'action': 'check_in',
            'location': 'gate'
        })

        return trailer_info

    def assign_yard_spot(self, trailer_id, spot_id):
        """
        Assign trailer to yard parking spot

        Parameters:
        - trailer_id: unique trailer identifier
        - spot_id: yard spot identifier
        """

        if trailer_id not in self.trailers:
            return {'error': f'Trailer {trailer_id} not found'}

        if spot_id in self.yard_spots and self.yard_spots[spot_id] is not None:
            return {'error': f'Spot {spot_id} already occupied'}

        # Update trailer location
        trailer = self.trailers[trailer_id]
        old_location = trailer['current_location']
        trailer['current_location'] = spot_id
        trailer['moves'] += 1

        # Update spot
        if old_location in self.yard_spots:
            self.yard_spots[old_location] = None  # Free old spot

        self.yard_spots[spot_id] = trailer_id

        # Log move
        self.move_history.append({
            'trailer_id': trailer_id,
            'timestamp': datetime.now(),
            'action': 'move_to_spot',
            'from': old_location,
            'to': spot_id
        })

        return {
            'trailer_id': trailer_id,
            'assigned_spot': spot_id,
            'moves': trailer['moves']
        }

    def spot_trailer_at_door(self, trailer_id, door_number):
        """
        Spot trailer at dock door for loading/unloading

        Parameters:
        - trailer_id: trailer to spot
        - door_number: dock door number
        """

        if trailer_id not in self.trailers:
            return {'error': f'Trailer {trailer_id} not found'}

        trailer = self.trailers[trailer_id]
        old_location = trailer['current_location']

        # Update trailer
        trailer['current_location'] = f'door_{door_number}'
        trailer['dock_door'] = door_number
        trailer['status'] = 'at_door'
        trailer['door_arrival_time'] = datetime.now()
        trailer['moves'] += 1

        # Free old spot if in yard
        if old_location in self.yard_spots:
            self.yard_spots[old_location] = None

        # Log move
        self.move_history.append({
            'trailer_id': trailer_id,
            'timestamp': datetime.now(),
            'action': 'spot_at_door',
            'door': door_number,
            'from': old_location
        })

        return {
            'trailer_id': trailer_id,
            'door': door_number,
            'spotted_time': trailer['door_arrival_time']
        }

    def complete_door_activity(self, trailer_id):
        """
        Complete loading/unloading at door

        Move trailer back to yard or check out
        """

        if trailer_id not in self.trailers:
            return {'error': f'Trailer {trailer_id} not found'}

        trailer = self.trailers[trailer_id]

        if trailer['status'] != 'at_door':
            return {'error': 'Trailer not at door'}

        # Calculate door dwell time
        door_dwell = (datetime.now() - trailer['door_arrival_time']).total_seconds() / 3600

        trailer['status'] = 'completed'
        trailer['door_departure_time'] = datetime.now()
        trailer['door_dwell_hours'] = door_dwell

        # Log
        self.move_history.append({
            'trailer_id': trailer_id,
            'timestamp': datetime.now(),
            'action': 'complete_door_activity',
            'door_dwell_hours': door_dwell
        })

        # Check for excessive door time (>2 hours)
        if door_dwell > 2:
            self.alerts.append({
                'alert_type': 'excessive_door_dwell',
                'trailer_id': trailer_id,
                'door_dwell_hours': door_dwell,
                'timestamp': datetime.now()
            })

        return {
            'trailer_id': trailer_id,
            'door_dwell_hours': door_dwell,
            'status': 'completed'
        }

    def check_out_trailer(self, trailer_id):
        """
        Check out trailer from facility

        Final step before trailer leaves
        """

        if trailer_id not in self.trailers:
            return {'error': f'Trailer {trailer_id} not found'}

        trailer = self.trailers[trailer_id]

        # Calculate total yard dwell
        total_dwell = (datetime.now() - trailer['check_in_time']).total_seconds() / 3600

        trailer['status'] = 'checked_out'
        trailer['check_out_time'] = datetime.now()
        trailer['total_yard_dwell_hours'] = total_dwell

        # Log
        self.move_history.append({
            'trailer_id': trailer_id,
            'timestamp': datetime.now(),
            'action': 'check_out',
            'total_dwell_hours': total_dwell
        })

        # Alert if excessive yard dwell (>24 hours)
        if total_dwell > 24:
            self.alerts.append({
                'alert_type': 'excessive_yard_dwell',
                'trailer_id': trailer_id,
                'total_dwell_hours': total_dwell,
                'timestamp': datetime.now()
            })

        return {
            'trailer_id': trailer_id,
            'total_yard_dwell_hours': total_dwell,
            'total_moves': trailer['moves']
        }

    def get_yard_status(self):
        """
        Get current yard status summary

        Returns counts by status
        """

        status_counts = {}
        for trailer in self.trailers.values():
            status = trailer['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        total_trailers = len(self.trailers)
        occupied_spots = sum(1 for spot in self.yard_spots.values()
                           if spot is not None)

        return {
            'total_trailers_in_yard': total_trailers,
            'occupied_spots': occupied_spots,
            'by_status': status_counts,
            'active_alerts': len(self.alerts)
        }

    def find_trailer(self, trailer_id):
        """
        Locate trailer in yard

        Returns current location
        """

        if trailer_id not in self.trailers:
            return {'error': 'Trailer not found'}

        trailer = self.trailers[trailer_id]

        return {
            'trailer_id': trailer_id,
            'current_location': trailer['current_location'],
            'status': trailer['status'],
            'carrier': trailer['carrier'],
            'dwell_time_hours': (datetime.now() - trailer['check_in_time']).total_seconds() / 3600
        }

    def calculate_performance_metrics(self):
        """
        Calculate yard performance metrics

        Returns KPIs
        """

        if not self.trailers:
            return {'message': 'No data available'}

        # Average dwell time
        dwell_times = []
        for trailer in self.trailers.values():
            if 'total_yard_dwell_hours' in trailer:
                dwell_times.append(trailer['total_yard_dwell_hours'])

        avg_dwell = np.mean(dwell_times) if dwell_times else 0

        # Average moves per trailer
        moves = [t['moves'] for t in self.trailers.values()]
        avg_moves = np.mean(moves) if moves else 0

        # Door dwell times
        door_dwells = []
        for trailer in self.trailers.values():
            if 'door_dwell_hours' in trailer:
                door_dwells.append(trailer['door_dwell_hours'])

        avg_door_dwell = np.mean(door_dwells) if door_dwells else 0

        return {
            'avg_yard_dwell_hours': avg_dwell,
            'avg_moves_per_trailer': avg_moves,
            'avg_door_dwell_hours': avg_door_dwell,
            'total_trailers': len(self.trailers),
            'total_alerts': len(self.alerts),
            'target_yard_dwell_hours': 24,
            'target_door_dwell_hours': 2
        }

# Example usage
yms = YardManagementSystem()

# Check in trailer
trailer = yms.check_in_trailer(
    trailer_id='TRL12345',
    carrier='ABC Trucking',
    seal_number='SEAL987',
    is_loaded=True
)
print(f"Trailer {trailer['trailer_id']} checked in at {trailer['check_in_time']}")

# Assign to yard spot
yms.assign_yard_spot('TRL12345', 'S045')
print("Trailer assigned to spot S045")

# Spot at door
yms.spot_trailer_at_door('TRL12345', door_number=12)
print("Trailer spotted at door 12")

# Get yard status
status = yms.get_yard_status()
print(f"\nYard Status: {status['total_trailers_in_yard']} trailers in yard")
```

---

## Yard Jockey Optimization

### Jockey Dispatch & Task Management

```python
class YardJockeyDispatcher:
    """
    Optimize yard jockey task assignment

    Minimize moves and maximize productivity
    """

    def __init__(self, num_jockeys, yard_layout):
        self.num_jockeys = num_jockeys
        self.yard_layout = yard_layout
        self.jockeys = {
            f'Jockey_{i+1}': {
                'current_location': 'office',
                'status': 'available',
                'tasks_completed': 0,
                'total_distance': 0
            }
            for i in range(num_jockeys)
        }
        self.task_queue = []

    def add_move_task(self, trailer_id, from_location, to_location, priority='normal'):
        """
        Add trailer move task to queue

        Parameters:
        - priority: 'urgent', 'normal', 'low'
        """

        task = {
            'task_id': f'TASK{len(self.task_queue)+1:04d}',
            'trailer_id': trailer_id,
            'from': from_location,
            'to': to_location,
            'priority': priority,
            'status': 'queued',
            'created_time': datetime.now()
        }

        self.task_queue.append(task)

        # Sort by priority
        priority_order = {'urgent': 0, 'normal': 1, 'low': 2}
        self.task_queue.sort(
            key=lambda x: priority_order.get(x['priority'], 1)
        )

        return task

    def assign_next_task(self):
        """
        Assign next task to available jockey

        Uses nearest jockey to minimize deadhead
        """

        # Find available jockey
        available_jockeys = [
            (jid, jinfo) for jid, jinfo in self.jockeys.items()
            if jinfo['status'] == 'available'
        ]

        if not available_jockeys or not self.task_queue:
            return None

        # Get next task
        task = self.task_queue[0]

        # Find nearest jockey
        nearest_jockey = None
        min_distance = float('inf')

        for jockey_id, jockey_info in available_jockeys:
            # Calculate distance from jockey to task start location
            distance = self._calculate_distance(
                jockey_info['current_location'],
                task['from']
            )

            if distance < min_distance:
                min_distance = distance
                nearest_jockey = jockey_id

        if nearest_jockey:
            # Assign task
            self.jockeys[nearest_jockey]['status'] = 'busy'
            self.jockeys[nearest_jockey]['current_task'] = task['task_id']

            task['status'] = 'in_progress'
            task['assigned_jockey'] = nearest_jockey
            task['start_time'] = datetime.now()

            self.task_queue.pop(0)

            return {
                'task_id': task['task_id'],
                'jockey': nearest_jockey,
                'trailer': task['trailer_id'],
                'move': f"{task['from']} -> {task['to']}"
            }

        return None

    def complete_task(self, task_id):
        """
        Mark task as completed

        Update jockey status and location
        """

        # Find task
        for task in self.task_queue:
            if task['task_id'] == task_id:
                task['status'] = 'completed'
                task['completion_time'] = datetime.now()

                # Update jockey
                jockey_id = task.get('assigned_jockey')
                if jockey_id:
                    self.jockeys[jockey_id]['status'] = 'available'
                    self.jockeys[jockey_id]['current_location'] = task['to']
                    self.jockeys[jockey_id]['tasks_completed'] += 1

                    # Calculate distance
                    distance = self._calculate_distance(task['from'], task['to'])
                    self.jockeys[jockey_id]['total_distance'] += distance

                return {
                    'task_id': task_id,
                    'jockey': jockey_id,
                    'status': 'completed'
                }

        return {'error': 'Task not found'}

    def _calculate_distance(self, location1, location2):
        """Calculate distance between two locations (simplified)"""

        # In practice, use actual yard coordinates
        # Simplified: random distance 50-500 feet
        return np.random.randint(50, 500)

    def get_jockey_productivity(self):
        """
        Calculate jockey productivity metrics

        Returns moves per hour, utilization
        """

        productivity = []

        for jockey_id, jockey_info in self.jockeys.items():
            productivity.append({
                'jockey_id': jockey_id,
                'tasks_completed': jockey_info['tasks_completed'],
                'total_distance': jockey_info['total_distance'],
                'current_status': jockey_info['status']
            })

        return pd.DataFrame(productivity)

    def optimize_task_sequence(self, tasks):
        """
        Optimize sequence of tasks to minimize total distance

        Uses greedy nearest-neighbor approach
        """

        if not tasks:
            return []

        optimized_sequence = []
        remaining_tasks = tasks.copy()
        current_location = 'office'

        while remaining_tasks:
            # Find nearest task
            nearest_task = None
            min_distance = float('inf')

            for task in remaining_tasks:
                distance = self._calculate_distance(
                    current_location,
                    task['from']
                )

                if distance < min_distance:
                    min_distance = distance
                    nearest_task = task

            if nearest_task:
                optimized_sequence.append(nearest_task)
                remaining_tasks.remove(nearest_task)
                current_location = nearest_task['to']

        return optimized_sequence
```

---

## Common Challenges & Solutions

### Challenge: Trailer Visibility

**Problem:**
- Can't find trailers in yard
- Drivers search for 15-30 minutes
- Wasted time and frustration

**Solutions:**
- Implement YMS with GPS/RFID tracking
- Zone-based yard layout with clear signage
- Mobile app for drivers (trailer locator)
- Digital yard map with real-time updates
- Dedicated staging zones by status
- Color-coded yard spots
- Regular yard audits to verify locations

### Challenge: High Detention Costs

**Problem:**
- Paying detention fees ($50-100/hour)
- Trailers sitting at doors too long
- Slow loading/unloading

**Solutions:**
- Set hard time limits for door dwell (<2 hours)
- Monitor and alert on approaching detention
- Pre-stage loads (ready before truck arrives)
- Live loading/unloading where possible
- Negotiate detention grace periods
- Optimize dock scheduling (avoid overbooking)
- Cross-training to flex labor to doors
- Automated alerts at 75% of free time

### Challenge: Yard Congestion

**Problem:**
- Too many trailers, not enough space
- Difficulty maneuvering jockeys
- Blocked access to trailers

**Solutions:**
- Implement drop trailer program (pre-loaded outbound)
- Dedicated empty trailer pool off-site
- Just-in-time arrival scheduling
- Turn away non-appointment arrivals
- Expand yard capacity or use overflow lot
- Improve trailer turn time (reduce dwell)
- Better appointment scheduling (smooth arrivals)

### Challenge: Long Wait Times at Gate

**Problem:**
- Trucks waiting 30-60 minutes at gate
- Manual check-in process slow
- Paperwork errors and delays

**Solutions:**
- Implement online pre-check-in portal
- Use kiosks for self-check-in
- Dedicated lanes for pre-registered drivers
- Automate BOL scanning and validation
- Pre-approve appointments (pre-verify credentials)
- Add gate capacity (more lanes)
- Mobile check-in before arrival

### Challenge: Inefficient Jockey Utilization

**Problem:**
- Jockeys idle or making unnecessary moves
- Long deadhead distances
- Poor task prioritization

**Solutions:**
- Implement jockey dispatch system
- Zone-based jockey assignments
- Real-time task queue with priorities
- Optimize task sequencing (minimize distance)
- Right-size jockey staffing
- Cross-train warehouse staff as backup
- Performance metrics and incentives

### Challenge: Lack of Appointment Compliance

**Problem:**
- Carriers show up without appointments
- Early or late arrivals disrupt schedule
- Overbooking of doors

**Solutions:**
- Require appointments (enforce policy)
- Charge premium for non-appointment arrivals
- Communicate appointment importance
- Partner with carriers on compliance
- Send appointment reminders (day before, morning of)
- Track and report carrier compliance
- Refuse service to repeat offenders

---

## Yard Management Technology

### Yard Management System (YMS) Selection

**Enterprise YMS Platforms:**
- **C3 Solutions**: Industry leader
- **Zebra (formerly Yard Management Solutions)**: RFID-based
- **Manhattan Associates YMS**: WMS-integrated
- **Oracle Yard Management**: Cloud-based
- **Blue Yonder YMS**: AI-powered
- **4Sight Yard Management**: Mid-market

**Key YMS Features:**
- Real-time trailer tracking (GPS, RFID, manual)
- Gate check-in/check-out automation
- Dock appointment scheduling
- Jockey task management and dispatch
- Dwell time monitoring and alerts
- Reporting and analytics
- Integration with WMS and TMS

### Tracking Technologies

**RFID Tags:**
- Passive tags on trailers
- Readers at gates and key points
- Automatic location updates
- Cost: $5-10 per tag, $1K-5K per reader

**GPS Tracking:**
- Active GPS devices on trailers
- Real-time location accuracy
- Higher cost, requires power
- Cost: $50-150 per device + monthly fees

**Geofencing:**
- Virtual boundaries in yard
- Trigger alerts when crossed
- Works with GPS or RFID

**Barcode/QR Scanning:**
- Low-tech, manual scanning
- Mobile app for jockeys
- Lower accuracy, requires compliance

---

## Output Format

### Yard Management Analysis Report

**Executive Summary:**
- Average yard dwell time: 18.5 hours (target: <12 hours)
- Detention costs: $18,500/month (target: <$10,000)
- Door utilization: 62% (target: 75%)
- Yard capacity utilization: 85% (near capacity)
- Recommendation: Implement YMS, improve dock scheduling

**Current State Metrics:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg yard dwell time | 18.5 hrs | <12 hrs | ⚠️ 54% over |
| Avg door dwell time | 2.8 hrs | <2 hrs | ⚠️ 40% over |
| Detention costs/month | $18.5K | <$10K | ⚠️ 85% over |
| Gate wait time | 22 min | <10 min | ⚠️ 120% over |
| Door utilization | 62% | 75% | ⚠️ Below target |
| Yard occupancy | 85% | 80% | ⚠️ Near capacity |

**Detention Cost Analysis:**

| Carrier | Monthly Charges | Incidents | Avg Duration | Root Cause |
|---------|----------------|-----------|--------------|------------|
| Carrier A | $6,200 | 42 | 3.2 hrs | Slow unloading |
| Carrier B | $4,800 | 35 | 2.9 hrs | Dock congestion |
| Carrier C | $3,500 | 28 | 2.6 hrs | Missing appointments |
| Others | $4,000 | 32 | 2.5 hrs | Various |

**Yard Dwell Time by Status:**

| Trailer Status | Count | Avg Dwell | Max Dwell | % Over 24 hrs |
|---------------|-------|-----------|-----------|---------------|
| Inbound staged | 45 | 12.5 hrs | 38 hrs | 15% |
| At door (loading) | 18 | 2.8 hrs | 4.5 hrs | 0% |
| Outbound ready | 32 | 28.0 hrs | 72 hrs | 45% ⚠️ |
| Empty/Drop | 25 | 36.0 hrs | 120 hrs | 60% ⚠️ |

**Root Cause: Outbound Delays**
- Waiting for consolidation (3+ days)
- No carrier pickup scheduled
- Recommendation: Daily pickup schedule or use 3PL

**Door Utilization by Day/Time:**

| Time Slot | Mon | Tue | Wed | Thu | Fri | Avg |
|-----------|-----|-----|-----|-----|-----|-----|
| 6-9 AM | 85% | 82% | 88% | 90% | 85% | 86% |
| 9-12 PM | 75% | 70% 72% | 78% | 75% | 74% |
| 12-3 PM | 55% | 52% | 58% | 60% | 55% | 56% ⚠️ |
| 3-6 PM | 48% | 45% | 50% | 52% | 48% | 49% ⚠️ |

**Recommendation: Evening shift to utilize afternoons**

**Improvement Initiatives:**

1. **Implement YMS** - Impact: -30% dwell time, -40% detention
   - Real-time trailer tracking
   - Automated door scheduling
   - Jockey dispatch optimization
   - Investment: $180K, ROI: 14 months

2. **Optimize Dock Scheduling** - Impact: +13% door utilization
   - Implement appointment system
   - Enforce appointment compliance
   - Balance arrivals throughout day
   - Investment: $25K (software)

3. **Reduce Outbound Dwell** - Impact: -50% yard congestion
   - Daily carrier pickup schedule
   - Pre-loaded outbound staging
   - Drop trailer program
   - Savings: $120K annually

4. **Expand Gate Capacity** - Impact: -60% wait time
   - Add second gate lane
   - Self-service kiosk check-in
   - Pre-registration portal
   - Investment: $75K

**Expected Results (12 months):**

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Avg yard dwell | 18.5 hrs | 12 hrs | -35% |
| Detention costs | $18.5K/mo | $9K/mo | -51% |
| Door utilization | 62% | 75% | +13 pts |
| Gate wait time | 22 min | 8 min | -64% |
| Yard occupancy | 85% | 70% | -15 pts |

---

## Questions to Ask

If you need more context:
1. How many dock doors and yard spots?
2. What's your daily trailer volume (in/out)?
3. Do you have a YMS or tracking system?
4. What's your average yard dwell time?
5. Are you paying detention costs? How much?
6. Any appointment scheduling system?
7. How many yard jockeys/tractors?
8. Main pain points? (visibility, congestion, detention, wait times)

---

## Related Skills

- **dock-door-assignment**: Optimize dock door scheduling and assignment
- **cross-docking**: Cross-dock operations and flow-through
- **warehouse-design**: Facility layout and design
- **route-optimization**: Outbound routing and delivery
- **freight-optimization**: Carrier management and transportation
- **supply-chain-automation**: Automation and technology selection
- **process-optimization**: Operational process improvement
- **maintenance-planning**: Equipment and yard tractor maintenance
