---
name: automotive-expert
version: 1.0.0
description: Expert-level automotive systems, connected vehicles, fleet management, telematics, ADAS, and automotive software
category: domains
tags: [automotive, connected-car, fleet, telematics, adas, vehicle]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Automotive Expert

Expert guidance for automotive systems, connected vehicles, fleet management, telematics, advanced driver assistance systems (ADAS), and automotive software development.

## Core Concepts

### Automotive Systems
- Telematics and fleet management
- Connected car platforms
- Advanced Driver Assistance Systems (ADAS)
- Electric Vehicle (EV) management
- Vehicle-to-Everything (V2X) communication
- Infotainment systems
- Diagnostic systems (OBD-II)

### Technologies
- CAN bus and automotive networks
- AUTOSAR architecture
- Over-the-air (OTA) updates
- Autonomous driving systems
- Battery management systems
- Computer vision for ADAS
- Edge computing in vehicles

### Standards and Protocols
- ISO 26262 (functional safety)
- AUTOSAR (automotive software architecture)
- J1939 (heavy-duty vehicle communication)
- UDS (Unified Diagnostic Services)
- SOME/IP (service-oriented middleware)
- MQTT for telematics
- CAN, LIN, FlexRay protocols

## Fleet Management System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from enum import Enum
import numpy as np

class VehicleStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"

class FuelType(Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    CNG = "cng"

@dataclass
class Vehicle:
    """Fleet vehicle information"""
    vehicle_id: str
    vin: str  # Vehicle Identification Number
    make: str
    model: str
    year: int
    license_plate: str
    fuel_type: FuelType
    status: VehicleStatus
    odometer_km: int
    last_service_km: int
    next_service_km: int
    assigned_driver_id: Optional[str]
    location: tuple  # (latitude, longitude)
    fuel_level_percent: float

@dataclass
class Trip:
    """Vehicle trip record"""
    trip_id: str
    vehicle_id: str
    driver_id: str
    start_time: datetime
    end_time: Optional[datetime]
    start_location: tuple
    end_location: Optional[tuple]
    distance_km: float
    fuel_consumed_liters: float
    average_speed_kmh: float
    max_speed_kmh: float
    harsh_braking_count: int
    harsh_acceleration_count: int

class FleetManagementSystem:
    """Fleet management and telematics system"""

    def __init__(self):
        self.vehicles = {}
        self.trips = []
        self.maintenance_schedules = []

    def track_vehicle_location(self, vehicle_id: str) -> dict:
        """Track real-time vehicle location"""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return {'error': 'Vehicle not found'}

        # Get GPS data from telematics device
        location = self._get_gps_location(vehicle_id)
        speed = self._get_current_speed(vehicle_id)
        heading = self._get_heading(vehicle_id)

        vehicle.location = location

        return {
            'vehicle_id': vehicle_id,
            'location': {
                'latitude': location[0],
                'longitude': location[1]
            },
            'speed_kmh': speed,
            'heading': heading,
            'timestamp': datetime.now().isoformat(),
            'status': vehicle.status.value
        }

    def start_trip(self, vehicle_id: str, driver_id: str) -> Trip:
        """Start a new trip"""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        trip = Trip(
            trip_id=self._generate_trip_id(),
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            start_time=datetime.now(),
            end_time=None,
            start_location=vehicle.location,
            end_location=None,
            distance_km=0.0,
            fuel_consumed_liters=0.0,
            average_speed_kmh=0.0,
            max_speed_kmh=0.0,
            harsh_braking_count=0,
            harsh_acceleration_count=0
        )

        vehicle.status = VehicleStatus.ACTIVE
        self.trips.append(trip)

        return trip

    def end_trip(self, trip_id: str) -> dict:
        """End trip and calculate metrics"""
        trip = next((t for t in self.trips if t.trip_id == trip_id), None)
        if not trip:
            return {'error': 'Trip not found'}

        vehicle = self.vehicles.get(trip.vehicle_id)

        trip.end_time = datetime.now()
        trip.end_location = vehicle.location

        # Calculate trip metrics
        duration_hours = (trip.end_time - trip.start_time).total_seconds() / 3600
        trip.average_speed_kmh = trip.distance_km / duration_hours if duration_hours > 0 else 0

        # Calculate fuel efficiency
        fuel_efficiency = trip.distance_km / trip.fuel_consumed_liters if trip.fuel_consumed_liters > 0 else 0

        # Calculate driver score
        driver_score = self._calculate_driver_score(trip)

        vehicle.status = VehicleStatus.IDLE

        return {
            'trip_id': trip_id,
            'duration_hours': duration_hours,
            'distance_km': trip.distance_km,
            'fuel_consumed': trip.fuel_consumed_liters,
            'fuel_efficiency_km_per_liter': fuel_efficiency,
            'average_speed': trip.average_speed_kmh,
            'max_speed': trip.max_speed_kmh,
            'harsh_events': trip.harsh_braking_count + trip.harsh_acceleration_count,
            'driver_score': driver_score
        }

    def _calculate_driver_score(self, trip: Trip) -> float:
        """Calculate driver safety score"""
        score = 100.0

        # Penalize harsh events
        score -= trip.harsh_braking_count * 5
        score -= trip.harsh_acceleration_count * 5

        # Penalize speeding
        if trip.max_speed_kmh > 120:
            score -= (trip.max_speed_kmh - 120) * 0.5

        # Penalize low fuel efficiency
        # Implementation would compare to vehicle baseline

        return max(0.0, min(100.0, score))

    def schedule_maintenance(self, vehicle_id: str) -> dict:
        """Schedule vehicle maintenance"""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return {'error': 'Vehicle not found'}

        # Check if maintenance is due
        km_since_service = vehicle.odometer_km - vehicle.last_service_km
        km_until_service = vehicle.next_service_km - vehicle.odometer_km

        if km_until_service <= 1000:  # Within 1000km of service
            maintenance_type = self._determine_maintenance_type(km_since_service)

            schedule = {
                'vehicle_id': vehicle_id,
                'maintenance_type': maintenance_type,
                'current_odometer': vehicle.odometer_km,
                'recommended_by_odometer': vehicle.next_service_km,
                'urgency': 'high' if km_until_service <= 500 else 'medium',
                'estimated_cost': self._estimate_maintenance_cost(maintenance_type)
            }

            self.maintenance_schedules.append(schedule)

            return schedule

        return {
            'vehicle_id': vehicle_id,
            'maintenance_required': False,
            'km_until_service': km_until_service
        }

    def optimize_routes(self, deliveries: List[dict]) -> dict:
        """Optimize delivery routes for fleet"""
        # Simplified route optimization
        # In production, would use sophisticated algorithms (TSP, VRP)

        available_vehicles = [
            v for v in self.vehicles.values()
            if v.status == VehicleStatus.IDLE
        ]

        if not available_vehicles:
            return {'error': 'No available vehicles'}

        # Assign deliveries to vehicles
        assignments = []
        for i, delivery in enumerate(deliveries):
            vehicle = available_vehicles[i % len(available_vehicles)]

            route = self._calculate_route(
                vehicle.location,
                delivery['destination']
            )

            assignments.append({
                'vehicle_id': vehicle.vehicle_id,
                'delivery_id': delivery['delivery_id'],
                'route': route,
                'estimated_distance_km': route['distance'],
                'estimated_time_minutes': route['duration'],
                'estimated_fuel_cost': self._estimate_fuel_cost(
                    route['distance'],
                    vehicle.fuel_type
                )
            })

        return {
            'total_deliveries': len(deliveries),
            'vehicles_assigned': len(set(a['vehicle_id'] for a in assignments)),
            'assignments': assignments,
            'total_distance_km': sum(a['estimated_distance_km'] for a in assignments),
            'total_estimated_cost': sum(a['estimated_fuel_cost'] for a in assignments)
        }

    def analyze_fleet_utilization(self) -> dict:
        """Analyze fleet utilization and efficiency"""
        total_vehicles = len(self.vehicles)

        active = sum(1 for v in self.vehicles.values() if v.status == VehicleStatus.ACTIVE)
        idle = sum(1 for v in self.vehicles.values() if v.status == VehicleStatus.IDLE)
        maintenance = sum(1 for v in self.vehicles.values() if v.status == VehicleStatus.MAINTENANCE)

        utilization_rate = (active / total_vehicles * 100) if total_vehicles > 0 else 0

        # Calculate average fuel efficiency
        recent_trips = self.trips[-100:]  # Last 100 trips
        if recent_trips:
            avg_fuel_efficiency = np.mean([
                t.distance_km / t.fuel_consumed_liters
                for t in recent_trips
                if t.fuel_consumed_liters > 0
            ])
        else:
            avg_fuel_efficiency = 0

        return {
            'total_vehicles': total_vehicles,
            'status_breakdown': {
                'active': active,
                'idle': idle,
                'maintenance': maintenance,
                'out_of_service': total_vehicles - active - idle - maintenance
            },
            'utilization_rate': utilization_rate,
            'average_fuel_efficiency': avg_fuel_efficiency,
            'recommendation': 'Reduce fleet size' if utilization_rate < 60 else
                           'Expand fleet' if utilization_rate > 90 else
                           'Optimal'
        }

    def _determine_maintenance_type(self, km_since_service: int) -> str:
        """Determine type of maintenance required"""
        if km_since_service >= 100000:
            return "major_service"
        elif km_since_service >= 50000:
            return "intermediate_service"
        else:
            return "routine_service"

    def _estimate_maintenance_cost(self, maintenance_type: str) -> Decimal:
        """Estimate maintenance cost"""
        costs = {
            'routine_service': Decimal('150'),
            'intermediate_service': Decimal('500'),
            'major_service': Decimal('1500')
        }
        return costs.get(maintenance_type, Decimal('200'))

    def _calculate_route(self, start: tuple, end: tuple) -> dict:
        """Calculate route between two points"""
        # Would use routing API (Google Maps, Mapbox, etc.)
        # Simplified calculation
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(start[0]), radians(start[1])
        lat2, lon2 = radians(end[0]), radians(end[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distance_km = 6371 * c  # Earth radius in km

        return {
            'distance': distance_km,
            'duration': distance_km / 60 * 60  # Assume 60 km/h average, return minutes
        }

    def _estimate_fuel_cost(self, distance_km: float, fuel_type: FuelType) -> Decimal:
        """Estimate fuel cost for trip"""
        fuel_prices = {
            FuelType.GASOLINE: Decimal('1.50'),  # per liter
            FuelType.DIESEL: Decimal('1.40'),
            FuelType.ELECTRIC: Decimal('0.30'),  # per kWh equivalent
            FuelType.HYBRID: Decimal('1.20'),
            FuelType.CNG: Decimal('1.00')
        }

        fuel_efficiency = 8.0  # km per liter (average)
        fuel_needed = distance_km / fuel_efficiency
        fuel_price = fuel_prices.get(fuel_type, Decimal('1.50'))

        return Decimal(str(fuel_needed)) * fuel_price

    def _get_gps_location(self, vehicle_id: str) -> tuple:
        """Get GPS location from telematics device"""
        # Implementation would connect to telematics API
        return (40.7128, -74.0060)  # Placeholder

    def _get_current_speed(self, vehicle_id: str) -> float:
        """Get current vehicle speed"""
        return np.random.uniform(0, 100)  # Placeholder

    def _get_heading(self, vehicle_id: str) -> float:
        """Get vehicle heading in degrees"""
        return np.random.uniform(0, 360)  # Placeholder

    def _generate_trip_id(self) -> str:
        import uuid
        return f"TRIP-{uuid.uuid4().hex[:10].upper()}"
```

## Connected Vehicle Platform

```python
@dataclass
class VehicleTelemetry:
    """Real-time vehicle telemetry data"""
    vehicle_id: str
    timestamp: datetime
    location: tuple
    speed_kmh: float
    rpm: int
    engine_temp_c: float
    battery_voltage: float
    fuel_level_percent: float
    odometer_km: int
    dtc_codes: List[str]  # Diagnostic Trouble Codes

class ConnectedVehiclePlatform:
    """Connected car platform with OTA updates"""

    def __init__(self):
        self.vehicles = {}
        self.telemetry_buffer = []
        self.ota_updates = {}

    def process_telemetry(self, telemetry: VehicleTelemetry) -> dict:
        """Process incoming telemetry data"""
        self.telemetry_buffer.append(telemetry)

        # Analyze telemetry for anomalies
        alerts = []

        # Check engine temperature
        if telemetry.engine_temp_c > 110:
            alerts.append({
                'type': 'high_engine_temp',
                'severity': 'warning',
                'value': telemetry.engine_temp_c,
                'message': 'Engine temperature above normal'
            })

        # Check battery voltage
        if telemetry.battery_voltage < 12.0:
            alerts.append({
                'type': 'low_battery',
                'severity': 'warning',
                'value': telemetry.battery_voltage,
                'message': 'Battery voltage low'
            })

        # Check for diagnostic trouble codes
        if telemetry.dtc_codes:
            alerts.append({
                'type': 'dtc_codes',
                'severity': 'critical',
                'codes': telemetry.dtc_codes,
                'message': f'{len(telemetry.dtc_codes)} diagnostic code(s) detected'
            })

        # Check for harsh driving
        if len(self.telemetry_buffer) >= 2:
            prev = self.telemetry_buffer[-2]
            if telemetry.vehicle_id == prev.vehicle_id:
                time_diff = (telemetry.timestamp - prev.timestamp).total_seconds()
                if time_diff > 0:
                    acceleration = (telemetry.speed_kmh - prev.speed_kmh) / time_diff

                    if abs(acceleration) > 5:  # > 5 km/h per second
                        alerts.append({
                            'type': 'harsh_driving',
                            'severity': 'info',
                            'acceleration': acceleration,
                            'message': 'Harsh acceleration/braking detected'
                        })

        return {
            'vehicle_id': telemetry.vehicle_id,
            'timestamp': telemetry.timestamp.isoformat(),
            'alerts': alerts,
            'health_score': self._calculate_vehicle_health(telemetry)
        }

    def deploy_ota_update(self,
                         vehicle_ids: List[str],
                         update_package: dict) -> dict:
        """Deploy over-the-air software update"""
        update_id = self._generate_update_id()

        ota_update = {
            'update_id': update_id,
            'version': update_package['version'],
            'description': update_package['description'],
            'package_size_mb': update_package['size_mb'],
            'target_vehicles': vehicle_ids,
            'deployed_at': datetime.now(),
            'status_by_vehicle': {}
        }

        for vehicle_id in vehicle_ids:
            # Schedule update for vehicle
            ota_update['status_by_vehicle'][vehicle_id] = {
                'status': 'scheduled',
                'download_progress': 0,
                'install_progress': 0
            }

        self.ota_updates[update_id] = ota_update

        return {
            'update_id': update_id,
            'vehicles_targeted': len(vehicle_ids),
            'estimated_completion': 'Within 48 hours'
        }

    def diagnose_vehicle(self, vehicle_id: str, dtc_codes: List[str]) -> dict:
        """Diagnose vehicle issues from DTC codes"""
        diagnoses = []

        for code in dtc_codes:
            diagnosis = self._lookup_dtc_code(code)
            diagnoses.append(diagnosis)

        # Calculate severity
        max_severity = max(d['severity'] for d in diagnoses)

        return {
            'vehicle_id': vehicle_id,
            'dtc_codes': dtc_codes,
            'diagnoses': diagnoses,
            'overall_severity': max_severity,
            'service_recommended': max_severity in ['high', 'critical']
        }

    def _calculate_vehicle_health(self, telemetry: VehicleTelemetry) -> float:
        """Calculate overall vehicle health score"""
        score = 100.0

        # Engine temperature
        if telemetry.engine_temp_c > 110:
            score -= 15
        elif telemetry.engine_temp_c > 100:
            score -= 5

        # Battery voltage
        if telemetry.battery_voltage < 11.5:
            score -= 20
        elif telemetry.battery_voltage < 12.0:
            score -= 10

        # DTC codes
        score -= len(telemetry.dtc_codes) * 15

        return max(0.0, score)

    def _lookup_dtc_code(self, code: str) -> dict:
        """Lookup diagnostic trouble code"""
        # Simplified DTC lookup
        # In production, would use comprehensive OBD-II code database

        dtc_database = {
            'P0171': {
                'description': 'System Too Lean (Bank 1)',
                'severity': 'medium',
                'possible_causes': ['Vacuum leak', 'Faulty MAF sensor', 'Fuel filter clogged']
            },
            'P0300': {
                'description': 'Random/Multiple Cylinder Misfire Detected',
                'severity': 'high',
                'possible_causes': ['Faulty spark plugs', 'Ignition coil failure', 'Fuel injector issue']
            }
        }

        return dtc_database.get(code, {
            'description': f'Unknown code: {code}',
            'severity': 'medium',
            'possible_causes': ['Requires diagnostic scan']
        })

    def _generate_update_id(self) -> str:
        import uuid
        return f"OTA-{uuid.uuid4().hex[:8].upper()}"
```

## Electric Vehicle Management

```python
class ElectricVehicleManagement:
    """EV-specific management functions"""

    def __init__(self):
        self.charging_stations = {}
        self.charging_sessions = []

    def calculate_range(self,
                       battery_capacity_kwh: float,
                       battery_soc_percent: float,
                       consumption_kwh_per_km: float) -> dict:
        """Calculate remaining range for EV"""
        available_energy = battery_capacity_kwh * (battery_soc_percent / 100)
        range_km = available_energy / consumption_kwh_per_km

        # Adjust for temperature (simplified)
        # Cold weather reduces range by up to 40%
        temperature_factor = 0.8  # Assume moderate conditions

        adjusted_range = range_km * temperature_factor

        return {
            'nominal_range_km': range_km,
            'adjusted_range_km': adjusted_range,
            'battery_soc_percent': battery_soc_percent,
            'available_energy_kwh': available_energy
        }

    def find_charging_stations(self,
                              current_location: tuple,
                              max_distance_km: float) -> List[dict]:
        """Find nearby charging stations"""
        nearby_stations = []

        for station_id, station in self.charging_stations.items():
            distance = self._calculate_distance(current_location, station['location'])

            if distance <= max_distance_km:
                nearby_stations.append({
                    'station_id': station_id,
                    'name': station['name'],
                    'location': station['location'],
                    'distance_km': distance,
                    'available_chargers': station['available_chargers'],
                    'charging_speed_kw': station['max_power_kw'],
                    'cost_per_kwh': station['cost_per_kwh']
                })

        # Sort by distance
        nearby_stations.sort(key=lambda x: x['distance_km'])

        return nearby_stations

    def optimize_charging_schedule(self,
                                  battery_capacity_kwh: float,
                                  current_soc_percent: float,
                                  target_soc_percent: float,
                                  departure_time: datetime) -> dict:
        """Optimize EV charging schedule based on electricity rates"""
        energy_needed = battery_capacity_kwh * ((target_soc_percent - current_soc_percent) / 100)

        # Get electricity rate schedule
        rate_schedule = self._get_electricity_rates(departure_time)

        # Find lowest rate period
        optimal_period = min(rate_schedule, key=lambda x: x['rate'])

        charging_duration_hours = energy_needed / 7.0  # Assume 7kW home charger

        return {
            'energy_needed_kwh': energy_needed,
            'optimal_start_time': optimal_period['start_time'].isoformat(),
            'charging_duration_hours': charging_duration_hours,
            'estimated_cost': energy_needed * float(optimal_period['rate']),
            'will_complete_by': (optimal_period['start_time'] +
                               timedelta(hours=charging_duration_hours)).isoformat()
        }

    def _calculate_distance(self, point1: tuple, point2: tuple) -> float:
        """Calculate distance between two points"""
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(point1[0]), radians(point1[1])
        lat2, lon2 = radians(point2[0]), radians(point2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return 6371 * c  # Earth radius in km

    def _get_electricity_rates(self, date: datetime) -> List[dict]:
        """Get time-of-use electricity rates"""
        # Simplified rate schedule
        # Off-peak: 11 PM - 7 AM
        # Peak: 2 PM - 8 PM
        # Mid-peak: all other times

        return [
            {
                'start_time': date.replace(hour=23, minute=0),
                'end_time': date.replace(hour=7, minute=0) + timedelta(days=1),
                'rate': Decimal('0.08')  # $0.08/kWh
            },
            {
                'start_time': date.replace(hour=14, minute=0),
                'end_time': date.replace(hour=20, minute=0),
                'rate': Decimal('0.25')  # $0.25/kWh
            }
        ]
```

## Best Practices

### Fleet Management
- Track all vehicle metrics in real-time
- Implement predictive maintenance
- Optimize routes for fuel efficiency
- Monitor driver behavior
- Use telematics for theft prevention
- Maintain detailed service records
- Implement fuel management systems

### Connected Vehicles
- Ensure secure V2X communication
- Implement robust cybersecurity
- Use encrypted data transmission
- Support OTA updates
- Monitor vehicle health continuously
- Provide driver assistance features
- Enable remote diagnostics

### EV Management
- Optimize charging schedules
- Monitor battery health
- Provide range prediction
- Support multiple charging networks
- Implement thermal management
- Track total cost of ownership
- Enable smart grid integration

### Safety and Compliance
- Follow ISO 26262 for safety-critical systems
- Implement fail-safe mechanisms
- Conduct regular safety audits
- Maintain compliance with emissions standards
- Support vehicle recall management
- Implement driver identification
- Provide emergency response features

## Anti-Patterns

❌ No telematics or GPS tracking
❌ Reactive maintenance only
❌ Manual route planning
❌ Ignoring driver behavior data
❌ No vehicle diagnostics
❌ Poor fuel management
❌ Inadequate cybersecurity
❌ No OTA update capability
❌ Inefficient EV charging

## Resources

- AUTOSAR: https://www.autosar.org/
- ISO 26262: https://www.iso.org/standard/68383.html
- SAE International: https://www.sae.org/
- OBD-II Standards: https://www.obdii.com/
- CAN Bus Specification: https://www.can-cia.org/
- Automotive Edge Computing Consortium: https://aecc.org/
- CharIN (EV Charging): https://www.charin.global/
