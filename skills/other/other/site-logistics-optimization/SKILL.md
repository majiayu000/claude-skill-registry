---
name: "site-logistics-optimization"
description: "Optimize construction site logistics including material delivery scheduling, crane positioning, storage area allocation, and traffic flow using operations research and simulation."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Site Logistics Optimization

## Overview

This skill implements optimization algorithms for construction site logistics. Minimize delays, reduce costs, and improve safety through data-driven planning of deliveries, equipment placement, and material storage.

**Optimization Areas:**
- Material delivery scheduling
- Crane and equipment positioning
- Storage area allocation
- Site traffic flow
- Workforce routing
- Just-in-time delivery

## Quick Start

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import heapq

@dataclass
class Delivery:
    delivery_id: str
    material_type: str
    quantity: float
    required_date: datetime
    unload_duration_min: int
    storage_area: str
    priority: int = 1  # 1=highest

@dataclass
class TimeSlot:
    start: datetime
    end: datetime
    is_available: bool = True
    delivery_id: str = None

def schedule_deliveries(deliveries: List[Delivery],
                       slots_per_day: int = 8,
                       unload_bays: int = 2) -> Dict[str, TimeSlot]:
    """Simple delivery scheduling"""
    # Sort by priority and required date
    sorted_deliveries = sorted(deliveries, key=lambda d: (d.priority, d.required_date))

    schedule = {}
    bay_schedules = {i: [] for i in range(unload_bays)}

    for delivery in sorted_deliveries:
        # Find available slot
        target_date = delivery.required_date.replace(hour=8, minute=0)

        for bay in range(unload_bays):
            # Check if bay has capacity
            bay_end = max([s.end for s in bay_schedules[bay]], default=target_date)

            if bay_end <= target_date:
                slot_start = target_date
            else:
                slot_start = bay_end

            slot_end = slot_start + timedelta(minutes=delivery.unload_duration_min)

            # Check if within working hours (8:00-18:00)
            if slot_end.hour <= 18:
                slot = TimeSlot(
                    start=slot_start,
                    end=slot_end,
                    is_available=False,
                    delivery_id=delivery.delivery_id
                )
                bay_schedules[bay].append(slot)
                schedule[delivery.delivery_id] = {
                    'bay': bay,
                    'slot': slot
                }
                break

    return schedule

# Example
deliveries = [
    Delivery("D001", "concrete", 50, datetime(2024, 1, 15, 9, 0), 45, "Zone-A", 1),
    Delivery("D002", "rebar", 10, datetime(2024, 1, 15, 10, 0), 30, "Zone-B", 2),
    Delivery("D003", "formwork", 20, datetime(2024, 1, 15, 9, 0), 60, "Zone-A", 1),
]

schedule = schedule_deliveries(deliveries)
for d_id, info in schedule.items():
    print(f"{d_id}: Bay {info['bay']}, {info['slot'].start.strftime('%H:%M')}-{info['slot'].end.strftime('%H:%M')}")
```

## Comprehensive Logistics Optimization

### Site Layout Model

```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime, date, timedelta
from enum import Enum
import numpy as np
from scipy.optimize import linear_sum_assignment
import heapq

class ZoneType(Enum):
    CONSTRUCTION = "construction"
    STORAGE = "storage"
    UNLOADING = "unloading"
    STAGING = "staging"
    ACCESS = "access"
    EQUIPMENT = "equipment"
    OFFICE = "office"

@dataclass
class SiteZone:
    zone_id: str
    zone_type: ZoneType
    area_sqm: float
    capacity: float  # Depends on type (tons, units, etc.)
    current_usage: float = 0
    position: Tuple[float, float] = (0, 0)  # x, y coordinates
    access_points: List[Tuple[float, float]] = field(default_factory=list)
    restrictions: List[str] = field(default_factory=list)

@dataclass
class Equipment:
    equipment_id: str
    equipment_type: str  # crane, forklift, etc.
    max_reach: float  # meters
    capacity: float  # tons
    position: Tuple[float, float] = (0, 0)
    operating_radius: float = 0

@dataclass
class DeliveryRequest:
    request_id: str
    material_type: str
    quantity: float
    unit: str
    required_date: date
    required_time_window: Tuple[int, int]  # (start_hour, end_hour)
    unload_duration_min: int
    vehicle_type: str
    destination_zone: str
    priority: int = 1
    requires_crane: bool = False

class SiteLogisticsModel:
    """Construction site logistics model"""

    def __init__(self, site_name: str):
        self.site_name = site_name
        self.zones: Dict[str, SiteZone] = {}
        self.equipment: Dict[str, Equipment] = {}
        self.deliveries: List[DeliveryRequest] = []
        self.routes: Dict[str, List[Tuple[float, float]]] = {}

    def add_zone(self, zone: SiteZone):
        """Add zone to site"""
        self.zones[zone.zone_id] = zone

    def add_equipment(self, equipment: Equipment):
        """Add equipment to site"""
        self.equipment[equipment.equipment_id] = equipment

    def add_delivery(self, delivery: DeliveryRequest):
        """Add delivery request"""
        self.deliveries.append(delivery)

    def calculate_distance(self, point1: Tuple[float, float],
                          point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def get_zone_distances(self) -> Dict[Tuple[str, str], float]:
        """Calculate distances between all zones"""
        distances = {}
        zone_ids = list(self.zones.keys())

        for i, z1 in enumerate(zone_ids):
            for z2 in zone_ids[i+1:]:
                dist = self.calculate_distance(
                    self.zones[z1].position,
                    self.zones[z2].position
                )
                distances[(z1, z2)] = dist
                distances[(z2, z1)] = dist

        return distances

    def check_crane_coverage(self, crane_id: str, zone_id: str) -> bool:
        """Check if crane can reach zone"""
        crane = self.equipment.get(crane_id)
        zone = self.zones.get(zone_id)

        if not crane or not zone:
            return False

        distance = self.calculate_distance(crane.position, zone.position)
        return distance <= crane.max_reach
```

### Delivery Scheduling Optimizer

```python
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import numpy as np

@dataclass
class ScheduledDelivery:
    delivery: DeliveryRequest
    scheduled_date: date
    scheduled_time: datetime
    assigned_bay: str
    assigned_crane: Optional[str]
    estimated_completion: datetime

class DeliveryScheduler:
    """Optimize delivery scheduling"""

    def __init__(self, site: SiteLogisticsModel):
        self.site = site
        self.schedule: Dict[date, List[ScheduledDelivery]] = {}
        self.bay_capacity = 2  # Simultaneous unloading bays
        self.working_hours = (7, 18)  # 7 AM to 6 PM

    def schedule_deliveries(self, deliveries: List[DeliveryRequest],
                           planning_horizon_days: int = 14) -> List[ScheduledDelivery]:
        """Schedule all deliveries optimally"""
        # Sort by priority and required date
        sorted_deliveries = sorted(
            deliveries,
            key=lambda d: (d.priority, d.required_date, -d.quantity)
        )

        scheduled = []
        bay_schedules = {f"bay_{i}": [] for i in range(self.bay_capacity)}

        for delivery in sorted_deliveries:
            best_slot = self._find_best_slot(delivery, bay_schedules)

            if best_slot:
                sched = ScheduledDelivery(
                    delivery=delivery,
                    scheduled_date=best_slot['date'],
                    scheduled_time=best_slot['start_time'],
                    assigned_bay=best_slot['bay'],
                    assigned_crane=best_slot.get('crane'),
                    estimated_completion=best_slot['end_time']
                )
                scheduled.append(sched)

                # Update bay schedule
                bay_schedules[best_slot['bay']].append({
                    'delivery_id': delivery.request_id,
                    'start': best_slot['start_time'],
                    'end': best_slot['end_time']
                })

        return scheduled

    def _find_best_slot(self, delivery: DeliveryRequest,
                       bay_schedules: Dict) -> Optional[Dict]:
        """Find optimal delivery slot"""
        target_date = delivery.required_date
        time_window = delivery.required_time_window

        # Try target date first, then surrounding days
        for day_offset in range(0, 7):  # Look up to 7 days ahead
            check_date = target_date + timedelta(days=day_offset)

            for bay_id, bay_schedule in bay_schedules.items():
                slot = self._find_slot_in_bay(
                    delivery, check_date, time_window, bay_id, bay_schedule
                )
                if slot:
                    # Check crane availability if needed
                    if delivery.requires_crane:
                        crane = self._find_available_crane(
                            delivery.destination_zone,
                            slot['start_time'],
                            slot['end_time']
                        )
                        if crane:
                            slot['crane'] = crane
                        else:
                            continue  # No crane available

                    return slot

        return None

    def _find_slot_in_bay(self, delivery: DeliveryRequest,
                          check_date: date,
                          time_window: Tuple[int, int],
                          bay_id: str,
                          bay_schedule: List[Dict]) -> Optional[Dict]:
        """Find available slot in specific bay"""
        start_hour = max(self.working_hours[0], time_window[0])
        end_hour = min(self.working_hours[1], time_window[1])

        # Get existing bookings for this date
        date_bookings = [
            b for b in bay_schedule
            if b['start'].date() == check_date
        ]

        # Sort by start time
        date_bookings.sort(key=lambda x: x['start'])

        # Find gaps
        current_time = datetime.combine(check_date, datetime.min.time().replace(hour=start_hour))
        end_time = datetime.combine(check_date, datetime.min.time().replace(hour=end_hour))

        for booking in date_bookings:
            if booking['start'] > current_time:
                gap_duration = (booking['start'] - current_time).seconds // 60
                if gap_duration >= delivery.unload_duration_min:
                    return {
                        'bay': bay_id,
                        'date': check_date,
                        'start_time': current_time,
                        'end_time': current_time + timedelta(minutes=delivery.unload_duration_min)
                    }
            current_time = max(current_time, booking['end'])

        # Check remaining time at end of day
        if current_time < end_time:
            remaining = (end_time - current_time).seconds // 60
            if remaining >= delivery.unload_duration_min:
                return {
                    'bay': bay_id,
                    'date': check_date,
                    'start_time': current_time,
                    'end_time': current_time + timedelta(minutes=delivery.unload_duration_min)
                }

        return None

    def _find_available_crane(self, zone_id: str,
                             start_time: datetime,
                             end_time: datetime) -> Optional[str]:
        """Find available crane that can reach zone"""
        for crane_id, crane in self.site.equipment.items():
            if crane.equipment_type != 'crane':
                continue

            if self.site.check_crane_coverage(crane_id, zone_id):
                # Simplified availability check
                # In practice, would check crane schedule
                return crane_id

        return None

    def get_daily_schedule(self, target_date: date) -> List[Dict]:
        """Get schedule for specific date"""
        schedule = []

        for sched in self.schedule.get(target_date, []):
            schedule.append({
                'time': sched.scheduled_time.strftime('%H:%M'),
                'material': sched.delivery.material_type,
                'quantity': f"{sched.delivery.quantity} {sched.delivery.unit}",
                'bay': sched.assigned_bay,
                'destination': sched.delivery.destination_zone,
                'crane': sched.assigned_crane,
                'duration': f"{sched.delivery.unload_duration_min} min"
            })

        return sorted(schedule, key=lambda x: x['time'])
```

### Storage Area Optimization

```python
class StorageOptimizer:
    """Optimize storage area allocation"""

    def __init__(self, site: SiteLogisticsModel):
        self.site = site
        self.storage_assignments: Dict[str, List[Dict]] = {}

    def allocate_storage(self, materials: List[Dict]) -> Dict[str, str]:
        """Allocate materials to storage zones

        materials: List of {material_id, material_type, quantity, destination_zone, arrival_date}
        """
        # Get storage zones
        storage_zones = {
            zid: zone for zid, zone in self.site.zones.items()
            if zone.zone_type == ZoneType.STORAGE
        }

        # Calculate zone scores for each material
        allocations = {}
        zone_usage = {zid: zone.current_usage for zid, zone in storage_zones.items()}

        for material in materials:
            best_zone = None
            best_score = -float('inf')

            for zone_id, zone in storage_zones.items():
                score = self._calculate_allocation_score(
                    material, zone, zone_usage[zone_id]
                )
                if score > best_score:
                    best_score = score
                    best_zone = zone_id

            if best_zone:
                allocations[material['material_id']] = best_zone
                zone_usage[best_zone] += material['quantity']

        return allocations

    def _calculate_allocation_score(self, material: Dict,
                                   zone: SiteZone,
                                   current_usage: float) -> float:
        """Calculate score for allocating material to zone"""
        # Check capacity
        remaining_capacity = zone.capacity - current_usage
        if remaining_capacity < material['quantity']:
            return -float('inf')

        score = 0

        # Distance to destination (closer is better)
        dest_zone = self.site.zones.get(material['destination_zone'])
        if dest_zone:
            distance = self.site.calculate_distance(zone.position, dest_zone.position)
            score += 100 / (1 + distance)  # Closer = higher score

        # Available capacity (more space is slightly better)
        capacity_ratio = remaining_capacity / zone.capacity
        score += capacity_ratio * 20

        # Material type restrictions
        if zone.restrictions:
            if material['material_type'] in zone.restrictions:
                score -= 100  # Penalize restricted materials

        return score

    def get_storage_utilization(self) -> Dict[str, Dict]:
        """Get storage utilization report"""
        report = {}

        for zone_id, zone in self.site.zones.items():
            if zone.zone_type != ZoneType.STORAGE:
                continue

            utilization = zone.current_usage / zone.capacity * 100 if zone.capacity > 0 else 0

            report[zone_id] = {
                'capacity': zone.capacity,
                'used': zone.current_usage,
                'available': zone.capacity - zone.current_usage,
                'utilization_pct': utilization,
                'status': 'critical' if utilization > 90 else 'normal' if utilization < 70 else 'high'
            }

        return report
```

### Crane Positioning Optimizer

```python
from scipy.optimize import minimize
import numpy as np

class CranePositionOptimizer:
    """Optimize crane placement on site"""

    def __init__(self, site: SiteLogisticsModel):
        self.site = site

    def optimize_single_crane(self, crane: Equipment,
                             priority_zones: List[str],
                             constraints: Dict = None) -> Tuple[float, float]:
        """Find optimal position for a single crane"""
        # Get zone positions
        zone_positions = [
            self.site.zones[zid].position
            for zid in priority_zones
            if zid in self.site.zones
        ]

        if not zone_positions:
            return crane.position

        # Objective: minimize weighted distance to priority zones
        def objective(pos):
            total_dist = 0
            for i, zone_pos in enumerate(zone_positions):
                dist = np.sqrt((pos[0] - zone_pos[0])**2 + (pos[1] - zone_pos[1])**2)
                weight = len(zone_positions) - i  # Higher weight for earlier zones
                total_dist += dist * weight
            return total_dist

        # Initial position
        x0 = np.array([crane.position[0], crane.position[1]])

        # Bounds (site boundaries)
        bounds = constraints.get('bounds', [(0, 100), (0, 100)]) if constraints else [(0, 100), (0, 100)]

        result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

        return tuple(result.x)

    def optimize_multiple_cranes(self, cranes: List[Equipment],
                                zones: List[str]) -> Dict[str, Tuple[float, float]]:
        """Optimize positions for multiple cranes to maximize coverage"""
        positions = {}

        # Assignment problem: which crane covers which zones
        zone_list = list(zones)
        crane_list = list(cranes)

        # Create cost matrix
        n_cranes = len(crane_list)
        n_zones = len(zone_list)

        cost_matrix = np.zeros((n_cranes, n_zones))

        for i, crane in enumerate(crane_list):
            for j, zone_id in enumerate(zone_list):
                zone = self.site.zones.get(zone_id)
                if zone:
                    dist = self.site.calculate_distance(crane.position, zone.position)
                    # Penalize if out of reach
                    if dist > crane.max_reach:
                        cost_matrix[i, j] = dist * 10
                    else:
                        cost_matrix[i, j] = dist

        # Solve assignment
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # Assign zones to cranes
        crane_zones = {c.equipment_id: [] for c in crane_list}
        for i, j in zip(row_ind, col_ind):
            crane_zones[crane_list[i].equipment_id].append(zone_list[j])

        # Optimize each crane position based on assigned zones
        for crane in crane_list:
            assigned_zones = crane_zones[crane.equipment_id]
            if assigned_zones:
                optimal_pos = self.optimize_single_crane(crane, assigned_zones)
                positions[crane.equipment_id] = optimal_pos
            else:
                positions[crane.equipment_id] = crane.position

        return positions

    def visualize_coverage(self, output_path: str = None):
        """Generate crane coverage visualization data"""
        coverage_data = []

        for crane_id, crane in self.site.equipment.items():
            if crane.equipment_type != 'crane':
                continue

            # Check coverage for each zone
            for zone_id, zone in self.site.zones.items():
                dist = self.site.calculate_distance(crane.position, zone.position)
                is_covered = dist <= crane.max_reach

                coverage_data.append({
                    'crane_id': crane_id,
                    'crane_x': crane.position[0],
                    'crane_y': crane.position[1],
                    'crane_reach': crane.max_reach,
                    'zone_id': zone_id,
                    'zone_x': zone.position[0],
                    'zone_y': zone.position[1],
                    'distance': dist,
                    'is_covered': is_covered
                })

        return coverage_data
```

### Traffic Flow Simulation

```python
from collections import defaultdict
import random

class TrafficSimulator:
    """Simulate and optimize site traffic flow"""

    def __init__(self, site: SiteLogisticsModel):
        self.site = site
        self.routes: Dict[str, List[str]] = {}  # route_id -> [zone_ids]
        self.traffic_data: List[Dict] = []

    def define_route(self, route_id: str, zones: List[str]):
        """Define a traffic route through zones"""
        self.routes[route_id] = zones

    def simulate_day(self, deliveries: List[ScheduledDelivery],
                    n_iterations: int = 100) -> Dict:
        """Simulate a day's traffic and identify bottlenecks"""
        # Track zone congestion over time
        congestion = defaultdict(list)

        for _ in range(n_iterations):
            time_slots = defaultdict(set)

            for delivery in deliveries:
                # Simulate vehicle movement
                arrival = delivery.scheduled_time
                departure = delivery.estimated_completion

                # Entry route
                entry_zones = ['gate', 'main_road', delivery.assigned_bay]
                for zone in entry_zones:
                    slot = arrival.hour
                    time_slots[(zone, slot)].add(delivery.delivery.request_id)

                # Unloading
                slot = arrival.hour
                time_slots[(delivery.assigned_bay, slot)].add(delivery.delivery.request_id)

                # Exit route
                exit_zones = [delivery.assigned_bay, 'main_road', 'gate']
                for zone in exit_zones:
                    slot = departure.hour
                    time_slots[(zone, slot)].add(delivery.delivery.request_id)

            # Record congestion
            for (zone, slot), vehicles in time_slots.items():
                congestion[(zone, slot)].append(len(vehicles))

        # Analyze results
        bottlenecks = []
        for (zone, slot), counts in congestion.items():
            avg_count = sum(counts) / len(counts)
            max_count = max(counts)

            if avg_count > 2 or max_count > 4:  # Threshold for bottleneck
                bottlenecks.append({
                    'zone': zone,
                    'time_slot': f"{slot}:00-{slot+1}:00",
                    'avg_vehicles': avg_count,
                    'max_vehicles': max_count,
                    'severity': 'high' if avg_count > 3 else 'medium'
                })

        return {
            'bottlenecks': sorted(bottlenecks, key=lambda x: x['avg_vehicles'], reverse=True),
            'total_deliveries': len(deliveries),
            'simulation_runs': n_iterations
        }

    def suggest_improvements(self, simulation_results: Dict) -> List[str]:
        """Suggest traffic flow improvements"""
        suggestions = []

        for bottleneck in simulation_results['bottlenecks']:
            zone = bottleneck['zone']
            time_slot = bottleneck['time_slot']

            if bottleneck['severity'] == 'high':
                suggestions.append(
                    f"Critical congestion at {zone} during {time_slot}. "
                    f"Consider adding alternative access route or spreading deliveries."
                )
            else:
                suggestions.append(
                    f"Moderate congestion at {zone} during {time_slot}. "
                    f"Consider adjusting delivery schedule."
                )

        return suggestions
```

## Quick Reference

| Optimization | Method | Complexity |
|--------------|--------|------------|
| Delivery Scheduling | Priority-based heuristic | O(n log n) |
| Storage Allocation | Scoring + greedy | O(n × m) |
| Crane Positioning | BFGS optimization | Iterative |
| Traffic Simulation | Monte Carlo | O(iterations × n) |

## Resources

- **SciPy Optimization**: https://docs.scipy.org/doc/scipy/reference/optimize.html
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `4d-simulation` for schedule integration
- See `material-tracking-iot` for real-time tracking
- See `data-visualization` for logistics dashboards
