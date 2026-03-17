---
name: aerospace-expert
version: 1.0.0
description: Expert-level aerospace systems, flight management, maintenance tracking, aviation safety, and aerospace software
category: domains
tags: [aerospace, aviation, flight, maintenance, safety, atc]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Aerospace Expert

Expert guidance for aerospace systems, flight management, maintenance tracking, aviation safety, air traffic control systems, and aerospace software development.

## Core Concepts

### Aerospace Systems
- Flight Management Systems (FMS)
- Maintenance, Repair, and Overhaul (MRO)
- Air Traffic Control (ATC) systems
- Aircraft Health Monitoring
- Flight Operations Quality Assurance (FOQA)
- Crew resource management
- Ground handling systems

### Aviation Technologies
- Avionics systems
- ACARS (Aircraft Communications Addressing and Reporting System)
- ADS-B (Automatic Dependent Surveillance-Broadcast)
- Flight data recorders (black boxes)
- Weather radar systems
- Autopilot and fly-by-wire
- Satellite communications

### Standards and Regulations
- FAA regulations (Federal Aviation Administration)
- EASA standards (European Union Aviation Safety Agency)
- ICAO standards (International Civil Aviation Organization)
- DO-178C (software airworthiness)
- DO-254 (hardware airworthiness)
- SPEC-42 (maintenance tracking)
- ATA chapters (maintenance organization)

## Flight Management System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from decimal import Decimal
from enum import Enum
import numpy as np

class FlightPhase(Enum):
    PRE_FLIGHT = "pre_flight"
    TAXI = "taxi"
    TAKEOFF = "takeoff"
    CLIMB = "climb"
    CRUISE = "cruise"
    DESCENT = "descent"
    APPROACH = "approach"
    LANDING = "landing"
    COMPLETED = "completed"

class FlightStatus(Enum):
    SCHEDULED = "scheduled"
    BOARDING = "boarding"
    DEPARTED = "departed"
    EN_ROUTE = "en_route"
    DELAYED = "delayed"
    ARRIVED = "arrived"
    CANCELLED = "cancelled"

@dataclass
class Waypoint:
    """Navigation waypoint"""
    name: str
    latitude: float
    longitude: float
    altitude_ft: int
    estimated_time: datetime

@dataclass
class Flight:
    """Flight information"""
    flight_number: str
    aircraft_id: str
    aircraft_type: str
    departure_airport: str
    arrival_airport: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    status: FlightStatus
    route: List[Waypoint]
    crew_members: List[str]
    passenger_count: int
    cargo_weight_kg: float

@dataclass
class FlightPlan:
    """Filed flight plan"""
    flight_plan_id: str
    flight_number: str
    aircraft_id: str
    departure: str
    destination: str
    alternate_airports: List[str]
    route_string: str
    cruise_altitude_ft: int
    cruise_speed_kts: int
    estimated_flight_time: timedelta
    fuel_required_kg: float
    filed_at: datetime

class FlightManagementSystem:
    """Flight planning and management"""

    def __init__(self):
        self.flights = {}
        self.flight_plans = {}
        self.aircraft_positions = {}

    def create_flight_plan(self, flight_data: dict) -> FlightPlan:
        """Create and file flight plan"""
        flight_plan_id = self._generate_flight_plan_id()

        # Calculate route
        route = self._calculate_optimal_route(
            flight_data['departure'],
            flight_data['destination'],
            flight_data['aircraft_type']
        )

        # Calculate fuel requirements
        fuel_required = self._calculate_fuel_requirements(
            route['distance_nm'],
            flight_data['aircraft_type'],
            flight_data.get('passenger_count', 0),
            flight_data.get('cargo_weight_kg', 0)
        )

        flight_plan = FlightPlan(
            flight_plan_id=flight_plan_id,
            flight_number=flight_data['flight_number'],
            aircraft_id=flight_data['aircraft_id'],
            departure=flight_data['departure'],
            destination=flight_data['destination'],
            alternate_airports=flight_data.get('alternates', []),
            route_string=route['route_string'],
            cruise_altitude_ft=route['cruise_altitude'],
            cruise_speed_kts=route['cruise_speed'],
            estimated_flight_time=route['estimated_time'],
            fuel_required_kg=fuel_required,
            filed_at=datetime.now()
        )

        self.flight_plans[flight_plan_id] = flight_plan

        # File with ATC
        self._file_with_atc(flight_plan)

        return flight_plan

    def _calculate_optimal_route(self,
                                 departure: str,
                                 destination: str,
                                 aircraft_type: str) -> dict:
        """Calculate optimal flight route"""
        # Get airport coordinates
        dep_coords = self._get_airport_coordinates(departure)
        dest_coords = self._get_airport_coordinates(destination)

        # Calculate great circle distance
        distance_nm = self._calculate_distance(dep_coords, dest_coords)

        # Determine cruise altitude based on distance and aircraft
        if distance_nm < 500:
            cruise_altitude = 25000  # FL250
        elif distance_nm < 1500:
            cruise_altitude = 35000  # FL350
        else:
            cruise_altitude = 39000  # FL390

        # Determine cruise speed based on aircraft type
        cruise_speeds = {
            'B737': 450,   # knots
            'B777': 490,
            'A320': 450,
            'A350': 490
        }
        cruise_speed = cruise_speeds.get(aircraft_type, 450)

        # Calculate flight time
        flight_time_hours = distance_nm / cruise_speed
        estimated_time = timedelta(hours=flight_time_hours)

        # Generate route string (simplified)
        route_string = f"{departure} DCT {destination}"

        return {
            'distance_nm': distance_nm,
            'cruise_altitude': cruise_altitude,
            'cruise_speed': cruise_speed,
            'estimated_time': estimated_time,
            'route_string': route_string
        }

    def _calculate_fuel_requirements(self,
                                    distance_nm: float,
                                    aircraft_type: str,
                                    passengers: int,
                                    cargo_kg: float) -> float:
        """Calculate required fuel for flight"""
        # Fuel consumption rates (kg per nm)
        fuel_rates = {
            'B737': 3.5,
            'B777': 8.0,
            'A320': 3.2,
            'A350': 7.5
        }

        base_rate = fuel_rates.get(aircraft_type, 4.0)

        # Calculate trip fuel
        trip_fuel = distance_nm * base_rate

        # Add weight penalty (simplified)
        weight_penalty = (passengers * 100 + cargo_kg) / 10000 * trip_fuel * 0.1

        # Reserve fuel (45 minutes at cruise)
        reserve_fuel = base_rate * 45 * 7.5  # 7.5 nm per minute

        # Contingency fuel (5% of trip fuel)
        contingency_fuel = trip_fuel * 0.05

        # Alternate fuel (for diversion)
        alternate_fuel = 100 * base_rate  # 100 nm

        total_fuel = trip_fuel + weight_penalty + reserve_fuel + contingency_fuel + alternate_fuel

        return total_fuel

    def track_flight_progress(self, flight_number: str) -> dict:
        """Track real-time flight progress"""
        flight = self.flights.get(flight_number)
        if not flight:
            return {'error': 'Flight not found'}

        # Get current position
        current_position = self.aircraft_positions.get(flight.aircraft_id)

        if not current_position:
            return {
                'flight_number': flight_number,
                'status': flight.status.value,
                'message': 'No position data available'
            }

        # Calculate progress
        total_distance = self._calculate_distance(
            self._get_airport_coordinates(flight.departure_airport),
            self._get_airport_coordinates(flight.arrival_airport)
        )

        distance_from_origin = self._calculate_distance(
            self._get_airport_coordinates(flight.departure_airport),
            (current_position['latitude'], current_position['longitude'])
        )

        progress_percent = (distance_from_origin / total_distance) * 100

        # Calculate ETA
        if current_position.get('ground_speed', 0) > 0:
            distance_remaining = total_distance - distance_from_origin
            time_remaining_hours = distance_remaining / current_position['ground_speed']
            eta = datetime.now() + timedelta(hours=time_remaining_hours)
        else:
            eta = flight.scheduled_arrival

        return {
            'flight_number': flight_number,
            'status': flight.status.value,
            'current_position': {
                'latitude': current_position['latitude'],
                'longitude': current_position['longitude'],
                'altitude_ft': current_position['altitude_ft'],
                'ground_speed_kts': current_position['ground_speed']
            },
            'progress_percent': progress_percent,
            'distance_remaining_nm': total_distance - distance_from_origin,
            'estimated_arrival': eta.isoformat(),
            'on_time': eta <= flight.scheduled_arrival
        }

    def calculate_landing_performance(self,
                                     aircraft_type: str,
                                     runway_length_ft: int,
                                     wind_speed_kts: int,
                                     wind_direction: int,
                                     runway_heading: int,
                                     temperature_c: float,
                                     altitude_ft: int) -> dict:
        """Calculate landing performance requirements"""
        # Base landing distance for aircraft type
        base_distances = {
            'B737': 5000,  # feet
            'B777': 7000,
            'A320': 4800,
            'A350': 6500
        }

        base_distance = base_distances.get(aircraft_type, 5500)

        # Wind component calculation
        wind_angle = abs(wind_direction - runway_heading)
        headwind = wind_speed_kts * np.cos(np.radians(wind_angle))
        crosswind = wind_speed_kts * np.sin(np.radians(wind_angle))

        # Adjust for headwind/tailwind
        # Headwind: reduce distance by 10% per 10 knots
        # Tailwind: increase distance by 20% per 10 knots
        if headwind > 0:  # Headwind
            distance_adjustment = -0.1 * (headwind / 10)
        else:  # Tailwind
            distance_adjustment = 0.2 * (abs(headwind) / 10)

        # Adjust for temperature (density altitude)
        isa_temp = 15 - (altitude_ft / 1000 * 2)  # ISA standard
        temp_deviation = temperature_c - isa_temp
        temp_adjustment = temp_deviation * 0.01  # 1% per degree

        # Calculate required landing distance
        adjustments = 1 + distance_adjustment + temp_adjustment
        required_distance = base_distance * adjustments

        # Safety margin (typical 1.67 for dry runway)
        safety_factor = 1.67
        required_distance_with_margin = required_distance * safety_factor

        # Check if runway is adequate
        runway_adequate = runway_length_ft >= required_distance_with_margin

        return {
            'aircraft_type': aircraft_type,
            'required_landing_distance_ft': int(required_distance_with_margin),
            'available_runway_ft': runway_length_ft,
            'runway_adequate': runway_adequate,
            'margin_ft': runway_length_ft - required_distance_with_margin,
            'conditions': {
                'headwind_kts': headwind,
                'crosswind_kts': crosswind,
                'temperature_c': temperature_c,
                'altitude_ft': altitude_ft
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

        distance_km = 6371 * c  # Earth radius in km
        distance_nm = distance_km * 0.539957  # Convert to nautical miles

        return distance_nm

    def _get_airport_coordinates(self, icao_code: str) -> Tuple[float, float]:
        """Get airport coordinates"""
        # Would query airport database
        airports = {
            'KJFK': (40.6413, -73.7781),  # JFK
            'KLAX': (33.9416, -118.4085),  # LAX
            'EGLL': (51.4700, -0.4543),    # Heathrow
            'LFPG': (49.0097, 2.5479)      # Charles de Gaulle
        }
        return airports.get(icao_code, (0.0, 0.0))

    def _file_with_atc(self, flight_plan: FlightPlan):
        """File flight plan with ATC"""
        # Implementation would submit to ATC systems
        pass

    def _generate_flight_plan_id(self) -> str:
        import uuid
        return f"FPL-{uuid.uuid4().hex[:10].upper()}"
```

## Aircraft Maintenance System

```python
from enum import Enum

class MaintenanceType(Enum):
    A_CHECK = "a_check"  # Every 400-600 flight hours
    B_CHECK = "b_check"  # Every 6-8 months
    C_CHECK = "c_check"  # Every 18-24 months
    D_CHECK = "d_check"  # Every 6-10 years
    LINE_MAINTENANCE = "line_maintenance"
    UNSCHEDULED = "unscheduled"

@dataclass
class Aircraft:
    """Aircraft information"""
    aircraft_id: str
    registration: str
    aircraft_type: str
    manufacturer: str
    model: str
    serial_number: str
    manufacture_date: datetime
    total_flight_hours: float
    total_cycles: int  # Takeoff/landing cycles
    last_a_check: datetime
    last_c_check: datetime
    airworthiness_certificate: str
    next_major_inspection: datetime

@dataclass
class MaintenanceRecord:
    """Maintenance work record"""
    record_id: str
    aircraft_id: str
    maintenance_type: MaintenanceType
    work_performed: str
    components_replaced: List[str]
    performed_by: str
    performed_at: datetime
    flight_hours_at_maintenance: float
    cycles_at_maintenance: int
    next_due_hours: Optional[float]
    next_due_date: Optional[datetime]

class AircraftMaintenanceSystem:
    """MRO (Maintenance, Repair, Overhaul) system"""

    def __init__(self):
        self.aircraft = {}
        self.maintenance_records = []
        self.component_tracking = {}

    def check_maintenance_due(self, aircraft_id: str) -> dict:
        """Check if maintenance is due for aircraft"""
        aircraft = self.aircraft.get(aircraft_id)
        if not aircraft:
            return {'error': 'Aircraft not found'}

        due_items = []

        # Check A-check (every 500 hours)
        hours_since_a_check = aircraft.total_flight_hours - self._get_last_check_hours(
            aircraft_id, MaintenanceType.A_CHECK
        )

        if hours_since_a_check >= 500:
            due_items.append({
                'type': 'A-check',
                'urgency': 'high' if hours_since_a_check >= 550 else 'medium',
                'hours_overdue': max(0, hours_since_a_check - 500)
            })

        # Check calendar-based C-check
        days_since_c_check = (datetime.now() - aircraft.last_c_check).days

        if days_since_c_check >= 540:  # 18 months
            due_items.append({
                'type': 'C-check',
                'urgency': 'critical' if days_since_c_check >= 600 else 'high',
                'days_overdue': max(0, days_since_c_check - 540)
            })

        # Check component life limits
        component_items = self._check_component_life_limits(aircraft_id)
        due_items.extend(component_items)

        return {
            'aircraft_id': aircraft_id,
            'registration': aircraft.registration,
            'maintenance_required': len(due_items) > 0,
            'due_items': due_items,
            'airworthy': len([item for item in due_items if item['urgency'] == 'critical']) == 0
        }

    def _get_last_check_hours(self, aircraft_id: str, check_type: MaintenanceType) -> float:
        """Get flight hours at last check"""
        records = [
            r for r in self.maintenance_records
            if r.aircraft_id == aircraft_id and r.maintenance_type == check_type
        ]

        if records:
            latest = max(records, key=lambda r: r.performed_at)
            return latest.flight_hours_at_maintenance

        return 0.0

    def _check_component_life_limits(self, aircraft_id: str) -> List[dict]:
        """Check component life limits"""
        due_items = []

        components = self.component_tracking.get(aircraft_id, {})

        for component_name, component_data in components.items():
            if component_data['life_limit_hours']:
                hours_used = component_data['hours_since_new']
                life_limit = component_data['life_limit_hours']

                if hours_used >= life_limit * 0.9:  # Within 90% of life limit
                    due_items.append({
                        'type': 'component_replacement',
                        'component': component_name,
                        'urgency': 'critical' if hours_used >= life_limit else 'high',
                        'hours_remaining': max(0, life_limit - hours_used)
                    })

        return due_items

    def record_maintenance(self,
                          aircraft_id: str,
                          maintenance_data: dict) -> MaintenanceRecord:
        """Record completed maintenance"""
        aircraft = self.aircraft.get(aircraft_id)
        if not aircraft:
            raise ValueError("Aircraft not found")

        record = MaintenanceRecord(
            record_id=self._generate_record_id(),
            aircraft_id=aircraft_id,
            maintenance_type=MaintenanceType(maintenance_data['type']),
            work_performed=maintenance_data['work_performed'],
            components_replaced=maintenance_data.get('components_replaced', []),
            performed_by=maintenance_data['technician_id'],
            performed_at=datetime.now(),
            flight_hours_at_maintenance=aircraft.total_flight_hours,
            cycles_at_maintenance=aircraft.total_cycles,
            next_due_hours=maintenance_data.get('next_due_hours'),
            next_due_date=maintenance_data.get('next_due_date')
        )

        self.maintenance_records.append(record)

        # Update aircraft maintenance dates
        if record.maintenance_type == MaintenanceType.A_CHECK:
            aircraft.last_a_check = datetime.now()
        elif record.maintenance_type == MaintenanceType.C_CHECK:
            aircraft.last_c_check = datetime.now()

        return record

    def predict_maintenance_cost(self,
                                aircraft_type: str,
                                flight_hours_per_year: float) -> dict:
        """Predict annual maintenance costs"""
        # Base maintenance costs per aircraft type
        base_costs = {
            'B737': {
                'hourly_rate': 800,  # $ per flight hour
                'a_check': 25000,
                'c_check': 500000,
                'd_check': 5000000
            },
            'B777': {
                'hourly_rate': 1500,
                'a_check': 50000,
                'c_check': 1000000,
                'd_check': 10000000
            }
        }

        costs = base_costs.get(aircraft_type, base_costs['B737'])

        # Calculate annual costs
        hourly_maintenance = flight_hours_per_year * costs['hourly_rate']

        # A-checks (assume 2 per year for 1000 hours/year)
        a_checks_per_year = flight_hours_per_year / 500
        a_check_costs = a_checks_per_year * costs['a_check']

        # C-check (amortized over 18 months)
        c_check_annual = costs['c_check'] / 1.5

        # D-check (amortized over 8 years)
        d_check_annual = costs['d_check'] / 8

        total_annual = hourly_maintenance + a_check_costs + c_check_annual + d_check_annual

        return {
            'aircraft_type': aircraft_type,
            'flight_hours_per_year': flight_hours_per_year,
            'maintenance_costs': {
                'hourly_maintenance': hourly_maintenance,
                'a_checks': a_check_costs,
                'c_check_amortized': c_check_annual,
                'd_check_amortized': d_check_annual,
                'total_annual': total_annual
            },
            'cost_per_flight_hour': total_annual / flight_hours_per_year
        }

    def _generate_record_id(self) -> str:
        import uuid
        return f"MX-{uuid.uuid4().hex[:10].upper()}"
```

## Aviation Safety Analysis

```python
class AviationSafetySystem:
    """Flight safety and FOQA analysis"""

    def __init__(self):
        self.safety_reports = []
        self.foqa_events = []

    def analyze_flight_data(self, flight_data: dict) -> dict:
        """Analyze flight data for safety events (FOQA)"""
        events_detected = []

        # Check for hard landings
        if flight_data.get('landing_vertical_speed_fpm', 0) < -600:
            events_detected.append({
                'event_type': 'hard_landing',
                'severity': 'medium',
                'value': flight_data['landing_vertical_speed_fpm'],
                'threshold': -600
            })

        # Check for unstabilized approaches
        if flight_data.get('approach_speed_deviation_kts', 0) > 10:
            events_detected.append({
                'event_type': 'unstabilized_approach',
                'severity': 'high',
                'value': flight_data['approach_speed_deviation_kts'],
                'threshold': 10
            })

        # Check for altitude deviations
        if flight_data.get('altitude_deviation_ft', 0) > 300:
            events_detected.append({
                'event_type': 'altitude_deviation',
                'severity': 'high',
                'value': flight_data['altitude_deviation_ft'],
                'threshold': 300
            })

        # Check for excessive bank angles
        if flight_data.get('max_bank_angle_deg', 0) > 30:
            events_detected.append({
                'event_type': 'excessive_bank',
                'severity': 'medium',
                'value': flight_data['max_bank_angle_deg'],
                'threshold': 30
            })

        # Calculate overall safety score
        safety_score = 100.0 - (len(events_detected) * 10)

        return {
            'flight_number': flight_data['flight_number'],
            'events_detected': events_detected,
            'safety_score': max(0.0, safety_score),
            'requires_review': len(events_detected) > 0
        }

    def calculate_safety_metrics(self, flights_data: List[dict]) -> dict:
        """Calculate safety KPIs"""
        total_flights = len(flights_data)
        total_hours = sum(f.get('flight_hours', 0) for f in flights_data)

        # Count safety events
        safety_events = sum(
            len(self.analyze_flight_data(f)['events_detected'])
            for f in flights_data
        )

        # Event rate per 1000 flights
        event_rate = (safety_events / total_flights * 1000) if total_flights > 0 else 0

        return {
            'total_flights': total_flights,
            'total_flight_hours': total_hours,
            'safety_events': safety_events,
            'event_rate_per_1000_flights': event_rate,
            'safety_rating': 'Excellent' if event_rate < 5 else
                           'Good' if event_rate < 10 else
                           'Needs Improvement'
        }
```

## Best Practices

### Flight Operations
- File complete and accurate flight plans
- Conduct thorough pre-flight checks
- Monitor fuel continuously
- Maintain communication with ATC
- Follow standard operating procedures (SOPs)
- Implement crew resource management
- Use automation appropriately

### Maintenance Management
- Follow manufacturer maintenance schedules
- Track all component life limits
- Maintain detailed maintenance logs
- Use certified parts and technicians
- Implement predictive maintenance
- Conduct regular inspections
- Ensure airworthiness compliance

### Safety Management
- Implement Safety Management System (SMS)
- Encourage safety reporting culture
- Analyze FOQA data regularly
- Conduct regular safety audits
- Maintain emergency procedures
- Train crew on CRM principles
- Track safety KPIs

### Regulatory Compliance
- Maintain current certifications
- Follow DO-178C for software
- Implement quality management systems
- Conduct regular audits
- Maintain proper documentation
- Follow ATA chapter organization
- Ensure ETOPS compliance (if applicable)

## Anti-Patterns

❌ Delaying required maintenance
❌ Poor flight planning
❌ Inadequate fuel reserves
❌ Ignoring weather conditions
❌ Poor crew communication
❌ No safety management system
❌ Inadequate record keeping
❌ Using uncertified parts
❌ Skipping pre-flight checks

## Resources

- FAA: https://www.faa.gov/
- ICAO: https://www.icao.int/
- EASA: https://www.easa.europa.eu/
- IATA: https://www.iata.org/
- Flight Safety Foundation: https://flightsafety.org/
- FAA Airworthiness Directives: https://www.faa.gov/regulations_policies/airworthiness_directives/
- DO-178C Standard: https://www.rtca.org/
