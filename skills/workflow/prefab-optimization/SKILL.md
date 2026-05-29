---
slug: "prefab-optimization"
display_name: "Prefab Optimization"
description: "Optimize prefabrication and modular construction workflows. Plan module sequencing, factory scheduling, transportation logistics, and on-site assembly for maximum efficiency."
---

# Prefabrication Optimization

## Overview

This skill implements optimization algorithms for prefabricated and modular construction. Maximize factory utilization, minimize transportation costs, and optimize on-site assembly sequences.

**Optimization Areas:**
- Module design for transport
- Factory production scheduling
- Logistics and transportation
- On-site assembly sequencing
- Crane and equipment planning
- Quality control checkpoints

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple, Optional
from enum import Enum

class ModuleStatus(Enum):
    DESIGN = "design"
    PRODUCTION = "production"
    QC = "quality_control"
    STORAGE = "storage"
    TRANSPORT = "transport"
    ON_SITE = "on_site"
    INSTALLED = "installed"

@dataclass
class PrefabModule:
    module_id: str
    name: str
    module_type: str
    dimensions: Tuple[float, float, float]  # L, W, H in meters
    weight_kg: float
    status: ModuleStatus = ModuleStatus.DESIGN
    production_hours: float = 0
    dependencies: List[str] = field(default_factory=list)

@dataclass
class ProductionSlot:
    slot_id: str
    start_time: datetime
    end_time: datetime
    bay_id: str
    module_id: str

def calculate_transport_constraints(module: PrefabModule) -> Dict:
    """Calculate transport constraints for module"""
    L, W, H = module.dimensions

    # Standard transport limits (varies by region)
    max_width = 4.0  # meters
    max_height = 4.5  # meters
    max_length = 12.0  # meters
    max_weight = 40000  # kg

    constraints = {
        'within_standard': True,
        'requires_escort': False,
        'requires_permit': False,
        'transport_type': 'standard'
    }

    if W > max_width or H > max_height:
        constraints['within_standard'] = False
        constraints['requires_escort'] = True
        constraints['requires_permit'] = True
        constraints['transport_type'] = 'wide_load'

    if L > max_length:
        constraints['requires_permit'] = True
        constraints['transport_type'] = 'long_load'

    if module.weight_kg > max_weight:
        constraints['requires_permit'] = True
        constraints['transport_type'] = 'heavy_load'

    return constraints

# Example
module = PrefabModule(
    module_id="MOD-001",
    name="Bathroom Pod Type A",
    module_type="bathroom",
    dimensions=(4.5, 3.0, 3.2),
    weight_kg=8500,
    production_hours=40
)

constraints = calculate_transport_constraints(module)
print(f"Module {module.name}: {constraints}")
```

## Comprehensive Prefab System

### Module Definition and Analysis

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import numpy as np

class ModuleCategory(Enum):
    BATHROOM_POD = "bathroom_pod"
    KITCHEN_POD = "kitchen_pod"
    STRUCTURAL = "structural"
    FACADE = "facade"
    MEP = "mep"
    STAIR = "stair"
    ELEVATOR = "elevator"
    ROOM_MODULE = "room_module"

@dataclass
class ModuleConnection:
    connection_id: str
    connection_type: str  # structural, mep, electrical
    from_module: str
    to_module: str
    from_point: Tuple[float, float, float]
    to_point: Tuple[float, float, float]
    tolerance_mm: float = 10

@dataclass
class ModuleDesign:
    module_id: str
    name: str
    category: ModuleCategory
    version: str

    # Dimensions and weight
    length_m: float
    width_m: float
    height_m: float
    weight_kg: float

    # Production
    production_hours: float
    required_skills: List[str]
    materials_list: List[Dict]

    # Connections
    connections: List[ModuleConnection] = field(default_factory=list)

    # Dependencies
    required_modules: List[str] = field(default_factory=list)  # Must be installed before
    blocks_modules: List[str] = field(default_factory=list)  # Cannot install until this is done

    # Metadata
    floor_level: int = 0
    grid_position: Tuple[str, str] = ('', '')  # Grid reference
    zone: str = ''

    @property
    def volume_m3(self) -> float:
        return self.length_m * self.width_m * self.height_m

    @property
    def footprint_m2(self) -> float:
        return self.length_m * self.width_m

class ModuleAnalyzer:
    """Analyze prefab modules for optimization"""

    def __init__(self):
        self.transport_limits = {
            'standard': {'width': 2.55, 'height': 4.0, 'length': 12.0, 'weight': 25000},
            'wide_load': {'width': 4.0, 'height': 4.5, 'length': 16.0, 'weight': 40000},
            'special': {'width': 6.0, 'height': 5.0, 'length': 25.0, 'weight': 100000}
        }

    def analyze_transportability(self, module: ModuleDesign) -> Dict:
        """Analyze module transportability"""
        dims = (module.length_m, module.width_m, module.height_m)

        # Check against limits
        for transport_type, limits in self.transport_limits.items():
            if (max(dims[0], dims[1]) <= limits['length'] and
                min(dims[0], dims[1]) <= limits['width'] and
                dims[2] <= limits['height'] and
                module.weight_kg <= limits['weight']):

                analysis = {
                    'feasible': True,
                    'transport_type': transport_type,
                    'orientation': 'length_first' if dims[0] >= dims[1] else 'width_first',
                    'utilization': {
                        'length': max(dims[0], dims[1]) / limits['length'],
                        'width': min(dims[0], dims[1]) / limits['width'],
                        'height': dims[2] / limits['height'],
                        'weight': module.weight_kg / limits['weight']
                    }
                }

                if transport_type == 'standard':
                    analysis['cost_factor'] = 1.0
                elif transport_type == 'wide_load':
                    analysis['cost_factor'] = 1.5
                    analysis['requirements'] = ['escort_vehicle', 'permit', 'route_survey']
                else:
                    analysis['cost_factor'] = 3.0
                    analysis['requirements'] = ['police_escort', 'special_permit', 'night_transport']

                return analysis

        return {
            'feasible': False,
            'reason': 'Exceeds maximum transport dimensions',
            'max_dimension': max(dims),
            'recommendation': 'Consider splitting into smaller modules'
        }

    def analyze_lifting(self, module: ModuleDesign) -> Dict:
        """Analyze lifting requirements"""
        # Estimate crane capacity needed (with safety factor)
        safety_factor = 1.25
        required_capacity = module.weight_kg * safety_factor / 1000  # tonnes

        # Estimate boom length based on typical building heights
        floor_height = 3.5  # meters per floor
        estimated_height = module.floor_level * floor_height + 10  # +10m clearance

        # Rough crane selection
        if required_capacity <= 50 and estimated_height <= 30:
            crane_type = 'mobile_50t'
        elif required_capacity <= 100 and estimated_height <= 50:
            crane_type = 'mobile_100t'
        elif required_capacity <= 200:
            crane_type = 'crawler_200t'
        else:
            crane_type = 'tower_crane'

        return {
            'required_capacity_tonnes': required_capacity,
            'estimated_lift_height_m': estimated_height,
            'recommended_crane': crane_type,
            'lift_points': self._calculate_lift_points(module),
            'center_of_gravity': (module.length_m / 2, module.width_m / 2, module.height_m / 3)
        }

    def _calculate_lift_points(self, module: ModuleDesign) -> List[Tuple[float, float]]:
        """Calculate optimal lift point positions"""
        L, W = module.length_m, module.width_m

        # Standard 4-point lift
        offset = 0.2  # 20% from edges
        return [
            (L * offset, W * offset),
            (L * (1 - offset), W * offset),
            (L * offset, W * (1 - offset)),
            (L * (1 - offset), W * (1 - offset))
        ]
```

### Production Scheduling

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import heapq

@dataclass
class ProductionBay:
    bay_id: str
    bay_type: str  # assembly, finishing, storage
    capacity_m2: float
    available_from: datetime
    skills_available: List[str]

@dataclass
class ProductionOrder:
    module_id: str
    required_date: date
    priority: int  # 1 = highest
    production_hours: float
    required_bay_type: str
    required_skills: List[str]

class ProductionScheduler:
    """Schedule prefab module production"""

    def __init__(self, work_hours_per_day: float = 8):
        self.bays: Dict[str, ProductionBay] = {}
        self.schedule: Dict[str, List[ProductionSlot]] = {}
        self.work_hours = work_hours_per_day

    def add_bay(self, bay: ProductionBay):
        """Add production bay"""
        self.bays[bay.bay_id] = bay
        self.schedule[bay.bay_id] = []

    def schedule_production(self, orders: List[ProductionOrder]) -> Dict:
        """Schedule all production orders"""
        # Sort by priority and required date
        sorted_orders = sorted(orders, key=lambda o: (o.priority, o.required_date))

        scheduled = []
        unscheduled = []

        for order in sorted_orders:
            slot = self._find_best_slot(order)
            if slot:
                self.schedule[slot.bay_id].append(slot)
                scheduled.append({
                    'module_id': order.module_id,
                    'bay_id': slot.bay_id,
                    'start': slot.start_time.isoformat(),
                    'end': slot.end_time.isoformat(),
                    'duration_hours': order.production_hours
                })
            else:
                unscheduled.append(order.module_id)

        return {
            'scheduled': scheduled,
            'unscheduled': unscheduled,
            'utilization': self._calculate_utilization()
        }

    def _find_best_slot(self, order: ProductionOrder) -> Optional[ProductionSlot]:
        """Find best production slot for order"""
        best_slot = None
        best_end_time = datetime.max

        for bay_id, bay in self.bays.items():
            if bay.bay_type != order.required_bay_type:
                continue

            if not set(order.required_skills).issubset(set(bay.skills_available)):
                continue

            # Find earliest available time
            existing_slots = self.schedule.get(bay_id, [])
            if existing_slots:
                last_end = max(s.end_time for s in existing_slots)
                start_time = max(bay.available_from, last_end)
            else:
                start_time = bay.available_from

            # Calculate end time
            production_days = order.production_hours / self.work_hours
            end_time = start_time + timedelta(days=production_days)

            # Check if this meets deadline
            required_datetime = datetime.combine(order.required_date, datetime.min.time())
            if end_time <= required_datetime and end_time < best_end_time:
                best_end_time = end_time
                best_slot = ProductionSlot(
                    slot_id=f"SLOT-{bay_id}-{len(existing_slots)}",
                    start_time=start_time,
                    end_time=end_time,
                    bay_id=bay_id,
                    module_id=order.module_id
                )

        return best_slot

    def _calculate_utilization(self) -> Dict[str, float]:
        """Calculate bay utilization"""
        utilization = {}

        for bay_id, slots in self.schedule.items():
            if not slots:
                utilization[bay_id] = 0.0
                continue

            total_time = (max(s.end_time for s in slots) -
                         min(s.start_time for s in slots)).total_seconds()
            used_time = sum((s.end_time - s.start_time).total_seconds() for s in slots)

            utilization[bay_id] = used_time / total_time if total_time > 0 else 0

        return utilization

    def get_gantt_data(self) -> List[Dict]:
        """Get data for Gantt chart visualization"""
        gantt_data = []

        for bay_id, slots in self.schedule.items():
            for slot in slots:
                gantt_data.append({
                    'bay': bay_id,
                    'module': slot.module_id,
                    'start': slot.start_time.isoformat(),
                    'end': slot.end_time.isoformat()
                })

        return sorted(gantt_data, key=lambda x: x['start'])
```

### Assembly Sequence Optimization

```python
from collections import defaultdict, deque
from typing import List, Dict, Set

class AssemblySequencer:
    """Optimize on-site module assembly sequence"""

    def __init__(self, modules: List[ModuleDesign]):
        self.modules = {m.module_id: m for m in modules}
        self.dependency_graph = self._build_dependency_graph()

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build dependency graph from module dependencies"""
        graph = defaultdict(set)

        for module_id, module in self.modules.items():
            for dep_id in module.required_modules:
                graph[module_id].add(dep_id)

        return graph

    def calculate_sequence(self) -> List[List[str]]:
        """Calculate optimal assembly sequence using topological sort"""
        # Calculate in-degree for each node
        in_degree = defaultdict(int)
        for module_id in self.modules:
            in_degree[module_id] = 0

        for deps in self.dependency_graph.values():
            for dep in deps:
                in_degree[dep] += 1

        # Start with modules that have no dependencies
        queue = deque([
            m_id for m_id in self.modules
            if len(self.dependency_graph[m_id]) == 0
        ])

        sequence = []
        current_level = []

        while queue:
            # Process current level
            current_level = list(queue)
            queue.clear()
            sequence.append(current_level)

            # Find next level
            for module_id in current_level:
                for dependent in self.modules:
                    if module_id in self.dependency_graph[dependent]:
                        self.dependency_graph[dependent].remove(module_id)
                        if len(self.dependency_graph[dependent]) == 0:
                            queue.append(dependent)

        # Check for cycles
        remaining = [m_id for m_id in self.modules if m_id not in
                    [item for sublist in sequence for item in sublist]]
        if remaining:
            print(f"Warning: Circular dependencies detected for: {remaining}")

        return sequence

    def optimize_for_crane(self, crane_positions: List[Tuple[float, float]]) -> List[Dict]:
        """Optimize sequence considering crane movement"""
        base_sequence = self.calculate_sequence()
        optimized = []

        for level in base_sequence:
            # Sort modules in level by proximity to crane positions
            level_with_positions = []
            for module_id in level:
                module = self.modules[module_id]
                # Use grid position to calculate distance
                grid_x = ord(module.grid_position[0]) if module.grid_position[0] else 0
                grid_y = int(module.grid_position[1]) if module.grid_position[1].isdigit() else 0

                # Find nearest crane
                min_dist = float('inf')
                for cx, cy in crane_positions:
                    dist = ((grid_x - cx) ** 2 + (grid_y - cy) ** 2) ** 0.5
                    min_dist = min(min_dist, dist)

                level_with_positions.append({
                    'module_id': module_id,
                    'floor': module.floor_level,
                    'distance_to_crane': min_dist
                })

            # Sort by floor (bottom-up) then by crane distance
            level_with_positions.sort(key=lambda x: (x['floor'], x['distance_to_crane']))
            optimized.append(level_with_positions)

        return optimized

    def generate_installation_plan(self) -> List[Dict]:
        """Generate detailed installation plan"""
        sequence = self.calculate_sequence()
        plan = []
        day = 1
        modules_per_day = 4  # Adjust based on crane capacity

        for level_idx, level in enumerate(sequence):
            for i in range(0, len(level), modules_per_day):
                batch = level[i:i + modules_per_day]

                for module_id in batch:
                    module = self.modules[module_id]
                    plan.append({
                        'day': day,
                        'sequence': len(plan) + 1,
                        'module_id': module_id,
                        'module_name': module.name,
                        'floor': module.floor_level,
                        'grid': module.grid_position,
                        'weight_kg': module.weight_kg,
                        'connections': len(module.connections),
                        'level': level_idx + 1
                    })

                day += 1

        return plan
```

### Transportation Optimization

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

@dataclass
class TransportVehicle:
    vehicle_id: str
    capacity_kg: float
    max_length_m: float
    max_width_m: float
    max_height_m: float
    cost_per_km: float
    available_from: datetime

class TransportOptimizer:
    """Optimize module transportation logistics"""

    def __init__(self, factory_location: Tuple[float, float],
                 site_location: Tuple[float, float]):
        self.factory = factory_location
        self.site = site_location
        self.distance_km = self._calculate_distance()
        self.vehicles: List[TransportVehicle] = []
        self.routes: List[Dict] = []

    def _calculate_distance(self) -> float:
        """Calculate distance between factory and site"""
        # Simplified Haversine for demonstration
        lat1, lon1 = self.factory
        lat2, lon2 = self.site
        R = 6371  # Earth radius in km

        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = (np.sin(dlat/2)**2 +
             np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
             np.sin(dlon/2)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R * c

    def add_vehicle(self, vehicle: TransportVehicle):
        self.vehicles.append(vehicle)

    def optimize_loading(self, modules: List[ModuleDesign],
                        required_dates: Dict[str, date]) -> Dict:
        """Optimize which modules go on which vehicle"""
        # Sort modules by required date
        sorted_modules = sorted(
            modules,
            key=lambda m: required_dates.get(m.module_id, date.max)
        )

        assignments = []
        remaining_modules = list(sorted_modules)

        while remaining_modules:
            # Find best vehicle for next batch
            for vehicle in self.vehicles:
                batch = self._pack_vehicle(vehicle, remaining_modules)
                if batch:
                    assignments.append({
                        'vehicle_id': vehicle.vehicle_id,
                        'modules': [m.module_id for m in batch],
                        'total_weight_kg': sum(m.weight_kg for m in batch),
                        'capacity_used': sum(m.weight_kg for m in batch) / vehicle.capacity_kg,
                        'cost': vehicle.cost_per_km * self.distance_km * 2  # Round trip
                    })

                    for m in batch:
                        remaining_modules.remove(m)
                    break
            else:
                # No vehicle can take remaining modules
                break

        return {
            'assignments': assignments,
            'total_trips': len(assignments),
            'total_cost': sum(a['cost'] for a in assignments),
            'unassigned': [m.module_id for m in remaining_modules]
        }

    def _pack_vehicle(self, vehicle: TransportVehicle,
                     modules: List[ModuleDesign]) -> List[ModuleDesign]:
        """Pack modules onto vehicle (simplified bin packing)"""
        packed = []
        total_weight = 0

        for module in modules:
            # Check if module fits
            dims = sorted([module.length_m, module.width_m])

            if (dims[0] <= vehicle.max_width_m and
                dims[1] <= vehicle.max_length_m and
                module.height_m <= vehicle.max_height_m and
                total_weight + module.weight_kg <= vehicle.capacity_kg):

                packed.append(module)
                total_weight += module.weight_kg

                # Simple: one module per trip for large items
                if max(dims) > 6 or module.weight_kg > vehicle.capacity_kg * 0.7:
                    break

        return packed

    def schedule_deliveries(self, assignments: List[Dict],
                           site_constraints: Dict = None) -> List[Dict]:
        """Schedule deliveries considering site constraints"""
        schedule = []

        # Default constraints
        if site_constraints is None:
            site_constraints = {
                'unload_start_hour': 7,
                'unload_end_hour': 17,
                'max_deliveries_per_day': 4,
                'unload_time_minutes': 60
            }

        current_date = date.today()
        deliveries_today = 0
        current_hour = site_constraints['unload_start_hour']

        for assignment in assignments:
            if deliveries_today >= site_constraints['max_deliveries_per_day']:
                current_date += timedelta(days=1)
                deliveries_today = 0
                current_hour = site_constraints['unload_start_hour']

            if current_hour >= site_constraints['unload_end_hour']:
                current_date += timedelta(days=1)
                deliveries_today = 0
                current_hour = site_constraints['unload_start_hour']

            schedule.append({
                **assignment,
                'delivery_date': current_date.isoformat(),
                'arrival_time': f"{current_hour:02d}:00",
                'departure_time': f"{current_hour + 1:02d}:00"
            })

            current_hour += 2  # 1 hour unload + 1 hour buffer
            deliveries_today += 1

        return schedule
```

## Quick Reference

| Module Type | Typical Dimensions (LxWxH) | Typical Weight | Production Time |
|-------------|---------------------------|----------------|-----------------|
| Bathroom Pod | 3.0 x 2.4 x 2.7m | 4,000-8,000 kg | 30-50 hours |
| Kitchen Pod | 4.0 x 2.4 x 2.7m | 5,000-10,000 kg | 40-60 hours |
| Room Module | 6.0 x 3.0 x 3.0m | 15,000-25,000 kg | 60-100 hours |
| Facade Panel | 6.0 x 3.0 x 0.3m | 2,000-4,000 kg | 15-25 hours |
| Stair Module | 4.0 x 2.5 x 3.5m | 8,000-12,000 kg | 35-50 hours |

## Transport Limits by Region

| Region | Max Width | Max Height | Max Length | Max Weight |
|--------|-----------|------------|------------|------------|
| EU Standard | 2.55m | 4.0m | 12.0m | 40t |
| EU Wide Load | 4.0m | 4.5m | 16.5m | 60t |
| US Standard | 2.6m | 4.1m | 14.6m | 36t |
| US Oversize | 4.3m | 4.6m | 22.0m | 60t |

## Resources

- **Modular Building Institute**: https://www.modular.org
- **Prefabrication Hub**: https://www.prefabhub.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `site-logistics-optimization` for on-site delivery scheduling
- See `4d-simulation` for assembly sequence visualization
- See `bim-validation-pipeline` for module quality checks
