---
name: maritime-expert
version: 1.0.0
description: Expert-level maritime systems, vessel tracking, port operations, cargo management, and maritime logistics
category: domains
tags: [maritime, shipping, logistics, vessel, port, cargo]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Maritime Expert

Expert guidance for maritime systems, vessel tracking, port operations, cargo management, maritime logistics, and shipping industry software.

## Core Concepts

### Maritime Systems
- Vessel Traffic Services (VTS)
- Port Management Systems
- Cargo Management Systems
- Fleet Management
- Maritime Communication Systems
- Container Terminal Operating Systems (TOS)
- Ship Performance Monitoring

### Maritime Technologies
- AIS (Automatic Identification System)
- ECDIS (Electronic Chart Display and Information System)
- Satellite communication (VSAT)
- Weather routing systems
- Ballast water management
- Engine monitoring systems
- Container tracking (IoT)

### Standards and Protocols
- IMO regulations (International Maritime Organization)
- SOLAS (Safety of Life at Sea)
- MARPOL (Marine Pollution)
- ISM Code (International Safety Management)
- ISPS Code (International Ship and Port Facility Security)
- UN/EDIFACT for EDI
- NMEA protocols

## Vessel Tracking System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from decimal import Decimal
from enum import Enum
import numpy as np

class VesselType(Enum):
    CONTAINER = "container"
    BULK_CARRIER = "bulk_carrier"
    TANKER = "tanker"
    RO_RO = "ro_ro"
    CRUISE = "cruise"
    CARGO = "general_cargo"

class VesselStatus(Enum):
    UNDERWAY = "underway"
    AT_ANCHOR = "at_anchor"
    MOORED = "moored"
    NOT_UNDER_COMMAND = "not_under_command"
    RESTRICTED_MANEUVERABILITY = "restricted_maneuverability"

@dataclass
class Vessel:
    """Vessel information"""
    imo_number: str  # International Maritime Organization number
    mmsi: str  # Maritime Mobile Service Identity
    vessel_name: str
    vessel_type: VesselType
    flag: str
    call_sign: str
    length_m: float
    beam_m: float
    draft_m: float
    gross_tonnage: int
    deadweight_tonnage: int
    max_speed_kts: float
    current_position: Tuple[float, float]
    heading: float
    speed_kts: float
    status: VesselStatus

@dataclass
class Voyage:
    """Voyage information"""
    voyage_id: str
    vessel_imo: str
    departure_port: str
    destination_port: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    cargo_manifest: List[dict]
    route_waypoints: List[Tuple[float, float]]
    estimated_fuel_consumption: float

class VesselTrackingSystem:
    """Maritime vessel tracking and monitoring"""

    def __init__(self):
        self.vessels = {}
        self.voyages = {}
        self.ais_messages = []

    def process_ais_message(self, ais_data: dict) -> dict:
        """Process AIS position report"""
        mmsi = ais_data['mmsi']
        vessel = self._get_vessel_by_mmsi(mmsi)

        if not vessel:
            return {'error': 'Vessel not found', 'mmsi': mmsi}

        # Update vessel position
        vessel.current_position = (ais_data['latitude'], ais_data['longitude'])
        vessel.heading = ais_data.get('heading', 0)
        vessel.speed_kts = ais_data.get('speed', 0)
        vessel.status = VesselStatus(ais_data.get('status', 'underway'))

        # Store AIS message
        self.ais_messages.append({
            'timestamp': datetime.now(),
            'mmsi': mmsi,
            'position': vessel.current_position,
            'speed': vessel.speed_kts,
            'heading': vessel.heading
        })

        # Check for anomalies
        anomalies = self._detect_anomalies(vessel, ais_data)

        return {
            'mmsi': mmsi,
            'vessel_name': vessel.vessel_name,
            'position': vessel.current_position,
            'speed_kts': vessel.speed_kts,
            'heading': vessel.heading,
            'status': vessel.status.value,
            'anomalies': anomalies,
            'timestamp': datetime.now().isoformat()
        }

    def _detect_anomalies(self, vessel: Vessel, ais_data: dict) -> List[dict]:
        """Detect unusual vessel behavior"""
        anomalies = []

        # Speed anomaly
        if vessel.speed_kts > vessel.max_speed_kts * 1.1:
            anomalies.append({
                'type': 'excessive_speed',
                'severity': 'medium',
                'message': f'Speed {vessel.speed_kts} kts exceeds maximum'
            })

        # Draft anomaly
        if 'draft' in ais_data and ais_data['draft'] > vessel.draft_m * 1.2:
            anomalies.append({
                'type': 'excessive_draft',
                'severity': 'high',
                'message': 'Draft exceeds vessel specifications'
            })

        # Unexpected stop
        if vessel.status == VesselStatus.AT_ANCHOR and vessel.speed_kts > 0.5:
            anomalies.append({
                'type': 'anchor_drag',
                'severity': 'critical',
                'message': 'Vessel moving while at anchor'
            })

        return anomalies

    def calculate_eta(self, voyage_id: str) -> dict:
        """Calculate estimated time of arrival"""
        voyage = self.voyages.get(voyage_id)
        if not voyage:
            return {'error': 'Voyage not found'}

        vessel = self.vessels.get(voyage.vessel_imo)
        if not vessel:
            return {'error': 'Vessel not found'}

        # Calculate remaining distance
        dest_coords = self._get_port_coordinates(voyage.destination_port)
        remaining_distance_nm = self._calculate_distance(
            vessel.current_position,
            dest_coords
        )

        # Calculate ETA based on current speed
        if vessel.speed_kts > 0:
            hours_remaining = remaining_distance_nm / vessel.speed_kts
            eta = datetime.now() + timedelta(hours=hours_remaining)
        else:
            # Use average speed if vessel is stopped
            avg_speed = vessel.max_speed_kts * 0.7  # Assume 70% of max
            hours_remaining = remaining_distance_nm / avg_speed
            eta = datetime.now() + timedelta(hours=hours_remaining)

        # Calculate delay
        delay_hours = (eta - voyage.scheduled_arrival).total_seconds() / 3600

        return {
            'voyage_id': voyage_id,
            'vessel_name': vessel.vessel_name,
            'destination': voyage.destination_port,
            'current_position': vessel.current_position,
            'remaining_distance_nm': remaining_distance_nm,
            'current_speed_kts': vessel.speed_kts,
            'estimated_arrival': eta.isoformat(),
            'scheduled_arrival': voyage.scheduled_arrival.isoformat(),
            'delay_hours': delay_hours,
            'on_schedule': delay_hours <= 0
        }

    def optimize_route(self,
                      start_position: Tuple[float, float],
                      destination: str,
                      vessel_type: VesselType,
                      departure_time: datetime) -> dict:
        """Optimize vessel route considering weather and fuel"""
        dest_coords = self._get_port_coordinates(destination)

        # Calculate great circle route
        gc_distance = self._calculate_distance(start_position, dest_coords)

        # Get weather forecast
        weather = self._get_weather_forecast(start_position, dest_coords, departure_time)

        # Calculate fuel consumption for different routes
        routes = [
            {
                'name': 'Great Circle',
                'distance_nm': gc_distance,
                'waypoints': self._generate_waypoints(start_position, dest_coords, 10)
            },
            {
                'name': 'Weather Optimized',
                'distance_nm': gc_distance * 1.05,  # 5% longer to avoid weather
                'waypoints': self._generate_weather_route(start_position, dest_coords, weather)
            }
        ]

        # Calculate fuel and time for each route
        for route in routes:
            avg_speed = 18.0  # knots
            transit_time = route['distance_nm'] / avg_speed
            fuel_consumption = self._estimate_fuel_consumption(
                route['distance_nm'],
                vessel_type,
                avg_speed
            )

            route['transit_time_hours'] = transit_time
            route['fuel_consumption_mt'] = fuel_consumption
            route['estimated_fuel_cost'] = fuel_consumption * 500  # $500/MT

        # Recommend optimal route
        recommended = min(routes, key=lambda r: r['estimated_fuel_cost'])

        return {
            'routes': routes,
            'recommended_route': recommended['name'],
            'savings': {
                'fuel_mt': routes[0]['fuel_consumption_mt'] - recommended['fuel_consumption_mt'],
                'cost_usd': routes[0]['estimated_fuel_cost'] - recommended['estimated_fuel_cost']
            }
        }

    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate great circle distance in nautical miles"""
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(point1[0]), radians(point1[1])
        lat2, lon2 = radians(point2[0]), radians(point2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distance_km = 6371 * c
        distance_nm = distance_km * 0.539957

        return distance_nm

    def _get_vessel_by_mmsi(self, mmsi: str) -> Optional[Vessel]:
        """Get vessel by MMSI"""
        for vessel in self.vessels.values():
            if vessel.mmsi == mmsi:
                return vessel
        return None

    def _get_port_coordinates(self, port_code: str) -> Tuple[float, float]:
        """Get port coordinates"""
        ports = {
            'USNYC': (40.6694, -74.0450),  # New York
            'NLRTM': (51.9244, 4.4777),    # Rotterdam
            'SGSIN': (1.2644, 103.8227),   # Singapore
            'CNSHA': (31.2304, 121.4737)   # Shanghai
        }
        return ports.get(port_code, (0.0, 0.0))

    def _generate_waypoints(self, start: Tuple[float, float], end: Tuple[float, float], count: int) -> List[Tuple[float, float]]:
        """Generate waypoints along great circle route"""
        waypoints = []
        for i in range(count + 1):
            fraction = i / count
            lat = start[0] + (end[0] - start[0]) * fraction
            lon = start[1] + (end[1] - start[1]) * fraction
            waypoints.append((lat, lon))
        return waypoints

    def _get_weather_forecast(self, start: Tuple[float, float], end: Tuple[float, float], time: datetime) -> dict:
        """Get weather forecast for route"""
        # Would integrate with weather API
        return {'wind_speed': 15, 'wave_height': 2.5}

    def _generate_weather_route(self, start: Tuple[float, float], end: Tuple[float, float], weather: dict) -> List[Tuple[float, float]]:
        """Generate weather-optimized route"""
        # Simplified - would use sophisticated weather routing
        return self._generate_waypoints(start, end, 12)

    def _estimate_fuel_consumption(self, distance_nm: float, vessel_type: VesselType, speed_kts: float) -> float:
        """Estimate fuel consumption in metric tons"""
        # Fuel consumption rates (MT per day at cruising speed)
        daily_consumption = {
            VesselType.CONTAINER: 80,
            VesselType.BULK_CARRIER: 30,
            VesselType.TANKER: 50
        }

        base_consumption = daily_consumption.get(vessel_type, 40)

        # Speed factor (fuel increases with cube of speed)
        speed_factor = (speed_kts / 18.0) ** 3

        days_at_sea = (distance_nm / speed_kts) / 24
        total_fuel = base_consumption * days_at_sea * speed_factor

        return total_fuel
```

## Port Operations System

```python
@dataclass
class BerthAllocation:
    """Berth allocation for vessel"""
    allocation_id: str
    vessel_imo: str
    berth_id: str
    scheduled_arrival: datetime
    scheduled_departure: datetime
    actual_arrival: Optional[datetime]
    actual_departure: Optional[datetime]
    cargo_operations: List[dict]

class PortOperationsSystem:
    """Port and terminal operations management"""

    def __init__(self):
        self.berths = {}
        self.allocations = []
        self.cargo_operations = []

    def allocate_berth(self, vessel_imo: str, eta: datetime, cargo_type: str) -> dict:
        """Allocate berth for arriving vessel"""
        # Find suitable berth
        suitable_berth = self._find_suitable_berth(cargo_type, eta)

        if not suitable_berth:
            return {'error': 'No suitable berth available'}

        # Estimate time at berth
        time_at_berth = self._estimate_port_time(cargo_type)

        allocation = BerthAllocation(
            allocation_id=self._generate_allocation_id(),
            vessel_imo=vessel_imo,
            berth_id=suitable_berth['berth_id'],
            scheduled_arrival=eta,
            scheduled_departure=eta + timedelta(hours=time_at_berth),
            actual_arrival=None,
            actual_departure=None,
            cargo_operations=[]
        )

        self.allocations.append(allocation)

        return {
            'allocation_id': allocation.allocation_id,
            'berth_id': suitable_berth['berth_id'],
            'scheduled_arrival': eta.isoformat(),
            'scheduled_departure': allocation.scheduled_departure.isoformat(),
            'estimated_hours_at_berth': time_at_berth
        }

    def track_container(self, container_number: str) -> dict:
        """Track container through port"""
        # Container tracking using IoT sensors
        container_data = {
            'container_number': container_number,
            'status': 'in_yard',
            'location': 'Block A, Row 12, Tier 3',
            'last_move': datetime.now() - timedelta(hours=2),
            'vessel_loaded': None,
            'customs_cleared': True,
            'temperature': 5.0  # For reefer containers
        }

        return container_data

    def optimize_yard_operations(self, expected_moves: int) -> dict:
        """Optimize container yard operations"""
        # Simplified yard optimization
        # In production, would use complex algorithms

        return {
            'expected_moves': expected_moves,
            'optimal_sequence': 'calculated',
            'estimated_time_hours': expected_moves * 0.1,  # 6 minutes per move
            'crane_allocation': {
                'crane_1': expected_moves // 2,
                'crane_2': expected_moves // 2
            }
        }

    def _find_suitable_berth(self, cargo_type: str, eta: datetime) -> Optional[dict]:
        """Find suitable berth for vessel"""
        # Check berth availability and suitability
        for berth_id, berth in self.berths.items():
            if cargo_type in berth['cargo_types']:
                # Check if berth is available
                if self._is_berth_available(berth_id, eta):
                    return berth
        return None

    def _is_berth_available(self, berth_id: str, time: datetime) -> bool:
        """Check if berth is available at given time"""
        for allocation in self.allocations:
            if allocation.berth_id == berth_id:
                if allocation.scheduled_arrival <= time <= allocation.scheduled_departure:
                    return False
        return True

    def _estimate_port_time(self, cargo_type: str) -> float:
        """Estimate time vessel will spend in port (hours)"""
        port_times = {
            'container': 24,
            'bulk': 48,
            'tanker': 18,
            'general_cargo': 36
        }
        return port_times.get(cargo_type, 24)

    def _generate_allocation_id(self) -> str:
        import uuid
        return f"BERTH-{uuid.uuid4().hex[:8].upper()}"
```

## Cargo Management

```python
class CargoManagementSystem:
    """Cargo and freight management"""

    def calculate_stowage_plan(self, containers: List[dict], vessel_capacity: dict) -> dict:
        """Calculate optimal container stowage plan"""
        # Simplified stowage planning
        # In production, would use sophisticated algorithms

        # Sort containers by weight (heaviest on bottom)
        sorted_containers = sorted(containers, key=lambda c: c['weight'], reverse=True)

        stowage_plan = {
            'bay_plans': [],
            'total_containers': len(containers),
            'total_weight': sum(c['weight'] for c in containers),
            'utilization': (len(containers) / vessel_capacity['max_containers']) * 100
        }

        return stowage_plan

    def track_bill_of_lading(self, bl_number: str) -> dict:
        """Track shipment by Bill of Lading"""
        # Track cargo shipment
        return {
            'bl_number': bl_number,
            'status': 'in_transit',
            'current_location': 'At Sea',
            'vessel': 'MV EXAMPLE',
            'departure_port': 'CNSHA',
            'destination_port': 'USNYC',
            'eta': (datetime.now() + timedelta(days=18)).isoformat()
        }
```

## Best Practices

### Vessel Operations
- Maintain accurate AIS transmission
- Follow IMO regulations strictly
- Implement fuel optimization
- Conduct regular safety drills
- Maintain proper manning levels
- Use weather routing services
- Implement environmental compliance

### Port Operations
- Optimize berth allocation
- Minimize vessel waiting time
- Implement automated gate systems
- Use container tracking technology
- Optimize yard operations
- Maintain equipment reliability
- Ensure security compliance (ISPS)

### Cargo Management
- Maintain accurate documentation
- Implement proper stowage planning
- Use standardized EDI messages
- Track cargo in real-time
- Ensure proper handling of dangerous goods
- Maintain cold chain for reefers
- Implement quality control

### Safety and Environment
- Follow SOLAS requirements
- Implement ISM Code
- Comply with MARPOL regulations
- Conduct risk assessments
- Maintain pollution prevention
- Implement ballast water management
- Train crew regularly

## Anti-Patterns

❌ Inaccurate AIS data transmission
❌ Poor cargo documentation
❌ Inefficient port operations
❌ No weather routing
❌ Inadequate maintenance
❌ Poor crew training
❌ Ignoring environmental regulations
❌ No cargo tracking
❌ Inefficient fuel management

## Resources

- IMO (International Maritime Organization): https://www.imo.org/
- ICS (International Chamber of Shipping): https://www.ics-shipping.org/
- BIMCO: https://www.bimco.org/
- Marine Traffic: https://www.marinetraffic.com/
- Port Technology: https://www.porttechnology.org/
- Maritime and Port Authority: https://www.mpa.gov.sg/
- SOLAS Convention: https://www.imo.org/en/About/Conventions/Pages/SOLAS.aspx
