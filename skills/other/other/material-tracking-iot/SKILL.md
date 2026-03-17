---
slug: "material-tracking-iot"
display_name: "Material Tracking IOT"
description: "IoT-based material tracking for construction sites. Monitor material delivery, storage conditions, usage, and inventory with sensors, RFID, GPS, and real-time dashboards."
---

# Material Tracking with IoT

## Overview

This skill implements IoT-based material tracking systems for construction projects. Track materials from procurement to installation using sensors, RFID tags, GPS, and connected devices.

**Tracking Capabilities:**
- Delivery tracking (GPS)
- Inventory management (RFID)
- Storage conditions (temperature, humidity sensors)
- Usage monitoring (weight sensors, counters)
- Waste tracking

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
import json

class MaterialStatus(Enum):
    ORDERED = "ordered"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    IN_STORAGE = "in_storage"
    IN_USE = "in_use"
    INSTALLED = "installed"
    WASTED = "wasted"

@dataclass
class MaterialItem:
    material_id: str
    name: str
    quantity: float
    unit: str
    rfid_tag: Optional[str] = None
    status: MaterialStatus = MaterialStatus.ORDERED
    location: Optional[str] = None
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class SensorReading:
    sensor_id: str
    reading_type: str  # temperature, humidity, weight, gps
    value: float
    unit: str
    timestamp: datetime
    location: Optional[str] = None

# Quick inventory check
def check_inventory(materials: List[MaterialItem]) -> Dict:
    """Quick inventory status check"""
    inventory = {
        'total_items': len(materials),
        'by_status': {},
        'by_location': {}
    }

    for m in materials:
        status = m.status.value
        inventory['by_status'][status] = inventory['by_status'].get(status, 0) + 1

        if m.location:
            inventory['by_location'][m.location] = inventory['by_location'].get(m.location, 0) + 1

    return inventory

# Example
materials = [
    MaterialItem("MAT-001", "Rebar 12mm", 500, "kg", "RFID-001", MaterialStatus.IN_STORAGE, "Yard-A"),
    MaterialItem("MAT-002", "Concrete C30", 50, "m³", None, MaterialStatus.IN_TRANSIT),
    MaterialItem("MAT-003", "Steel Beam HEB200", 20, "pcs", "RFID-002", MaterialStatus.DELIVERED, "Yard-B")
]

print(check_inventory(materials))
```

## Comprehensive IoT Tracking System

### Material Tracking Engine

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import uuid
import json

class SensorType(Enum):
    RFID = "rfid"
    GPS = "gps"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WEIGHT = "weight"
    MOTION = "motion"
    CAMERA = "camera"

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: SensorType
    location: str
    is_active: bool = True
    last_reading: Optional[datetime] = None
    battery_level: float = 100.0

@dataclass
class MaterialMovement:
    movement_id: str
    material_id: str
    from_location: Optional[str]
    to_location: str
    quantity: float
    timestamp: datetime
    recorded_by: str  # sensor_id or user_id
    movement_type: str  # delivery, transfer, usage, waste

@dataclass
class StorageCondition:
    location: str
    timestamp: datetime
    temperature: Optional[float] = None  # Celsius
    humidity: Optional[float] = None  # Percentage
    is_acceptable: bool = True
    alerts: List[str] = field(default_factory=list)

class MaterialTrackingSystem:
    """IoT-based material tracking system"""

    def __init__(self):
        self.materials: Dict[str, MaterialItem] = {}
        self.sensors: Dict[str, Sensor] = {}
        self.movements: List[MaterialMovement] = []
        self.readings: List[SensorReading] = []
        self.storage_conditions: Dict[str, StorageCondition] = {}
        self.alerts: List[Dict] = []

        # Material requirements (for condition monitoring)
        self.material_requirements = {
            'cement': {'max_humidity': 60, 'max_temp': 35, 'min_temp': 5},
            'steel': {'max_humidity': 70, 'max_temp': 50, 'min_temp': -20},
            'wood': {'max_humidity': 65, 'max_temp': 40, 'min_temp': 0},
            'paint': {'max_humidity': 80, 'max_temp': 30, 'min_temp': 5},
            'adhesive': {'max_humidity': 70, 'max_temp': 25, 'min_temp': 10}
        }

    def register_material(self, name: str, quantity: float, unit: str,
                         rfid_tag: Optional[str] = None,
                         material_type: str = 'general') -> MaterialItem:
        """Register new material in the system"""
        material_id = f"MAT-{uuid.uuid4().hex[:8].upper()}"

        material = MaterialItem(
            material_id=material_id,
            name=name,
            quantity=quantity,
            unit=unit,
            rfid_tag=rfid_tag,
            status=MaterialStatus.ORDERED
        )

        self.materials[material_id] = material
        return material

    def register_sensor(self, sensor_type: SensorType, location: str) -> Sensor:
        """Register new sensor"""
        sensor_id = f"SNS-{sensor_type.value.upper()}-{uuid.uuid4().hex[:6].upper()}"

        sensor = Sensor(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            location=location
        )

        self.sensors[sensor_id] = sensor
        return sensor

    def process_sensor_reading(self, sensor_id: str, value: float,
                               unit: str, metadata: Dict = None) -> SensorReading:
        """Process incoming sensor reading"""
        sensor = self.sensors.get(sensor_id)
        if not sensor:
            raise ValueError(f"Unknown sensor: {sensor_id}")

        reading = SensorReading(
            sensor_id=sensor_id,
            reading_type=sensor.sensor_type.value,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            location=sensor.location
        )

        self.readings.append(reading)
        sensor.last_reading = reading.timestamp

        # Process based on sensor type
        if sensor.sensor_type == SensorType.RFID:
            self._process_rfid_reading(reading, metadata)
        elif sensor.sensor_type == SensorType.GPS:
            self._process_gps_reading(reading, metadata)
        elif sensor.sensor_type in [SensorType.TEMPERATURE, SensorType.HUMIDITY]:
            self._process_environment_reading(reading)
        elif sensor.sensor_type == SensorType.WEIGHT:
            self._process_weight_reading(reading, metadata)

        return reading

    def _process_rfid_reading(self, reading: SensorReading, metadata: Dict):
        """Process RFID tag scan"""
        rfid_tag = metadata.get('rfid_tag') if metadata else None
        if not rfid_tag:
            return

        # Find material with this RFID
        material = None
        for m in self.materials.values():
            if m.rfid_tag == rfid_tag:
                material = m
                break

        if material:
            old_location = material.location
            new_location = reading.location

            # Record movement
            if old_location != new_location:
                movement = MaterialMovement(
                    movement_id=f"MOV-{uuid.uuid4().hex[:8]}",
                    material_id=material.material_id,
                    from_location=old_location,
                    to_location=new_location,
                    quantity=material.quantity,
                    timestamp=reading.timestamp,
                    recorded_by=reading.sensor_id,
                    movement_type='transfer'
                )
                self.movements.append(movement)

                material.location = new_location
                material.last_updated = reading.timestamp

                # Update status based on location
                if 'yard' in new_location.lower() or 'storage' in new_location.lower():
                    material.status = MaterialStatus.IN_STORAGE
                elif 'floor' in new_location.lower() or 'zone' in new_location.lower():
                    material.status = MaterialStatus.IN_USE

    def _process_gps_reading(self, reading: SensorReading, metadata: Dict):
        """Process GPS location update"""
        vehicle_id = metadata.get('vehicle_id') if metadata else None
        material_ids = metadata.get('material_ids', []) if metadata else []

        lat, lon = reading.value, metadata.get('longitude', 0) if metadata else 0

        for material_id in material_ids:
            material = self.materials.get(material_id)
            if material:
                material.location = f"GPS: {lat:.6f}, {lon:.6f}"
                material.status = MaterialStatus.IN_TRANSIT
                material.last_updated = reading.timestamp

    def _process_environment_reading(self, reading: SensorReading):
        """Process temperature/humidity reading"""
        location = reading.location

        if location not in self.storage_conditions:
            self.storage_conditions[location] = StorageCondition(
                location=location,
                timestamp=reading.timestamp
            )

        condition = self.storage_conditions[location]
        condition.timestamp = reading.timestamp

        if reading.reading_type == 'temperature':
            condition.temperature = reading.value
        elif reading.reading_type == 'humidity':
            condition.humidity = reading.value

        # Check conditions for materials in this location
        self._check_storage_conditions(location)

    def _check_storage_conditions(self, location: str):
        """Check if storage conditions are acceptable for materials"""
        condition = self.storage_conditions.get(location)
        if not condition:
            return

        condition.alerts = []
        condition.is_acceptable = True

        # Find materials in this location
        materials_here = [m for m in self.materials.values() if m.location == location]

        for material in materials_here:
            # Determine material type from name (simplified)
            material_type = None
            for mtype in self.material_requirements.keys():
                if mtype in material.name.lower():
                    material_type = mtype
                    break

            if not material_type:
                continue

            reqs = self.material_requirements[material_type]

            if condition.temperature is not None:
                if condition.temperature > reqs.get('max_temp', 100):
                    alert = f"Temperature too high for {material.name}: {condition.temperature}°C > {reqs['max_temp']}°C"
                    condition.alerts.append(alert)
                    condition.is_acceptable = False
                    self._create_alert('temperature_high', location, material.material_id, alert)

                if condition.temperature < reqs.get('min_temp', -100):
                    alert = f"Temperature too low for {material.name}: {condition.temperature}°C < {reqs['min_temp']}°C"
                    condition.alerts.append(alert)
                    condition.is_acceptable = False
                    self._create_alert('temperature_low', location, material.material_id, alert)

            if condition.humidity is not None:
                if condition.humidity > reqs.get('max_humidity', 100):
                    alert = f"Humidity too high for {material.name}: {condition.humidity}% > {reqs['max_humidity']}%"
                    condition.alerts.append(alert)
                    condition.is_acceptable = False
                    self._create_alert('humidity_high', location, material.material_id, alert)

    def _process_weight_reading(self, reading: SensorReading, metadata: Dict):
        """Process weight sensor reading for usage tracking"""
        material_id = metadata.get('material_id') if metadata else None
        if not material_id:
            return

        material = self.materials.get(material_id)
        if not material:
            return

        previous_weight = metadata.get('previous_weight', material.quantity)
        current_weight = reading.value

        if current_weight < previous_weight:
            # Material was used
            used_quantity = previous_weight - current_weight

            movement = MaterialMovement(
                movement_id=f"MOV-{uuid.uuid4().hex[:8]}",
                material_id=material_id,
                from_location=reading.location,
                to_location="installed",
                quantity=used_quantity,
                timestamp=reading.timestamp,
                recorded_by=reading.sensor_id,
                movement_type='usage'
            )
            self.movements.append(movement)

            material.quantity = current_weight
            material.last_updated = reading.timestamp

            # Check for low stock
            if material.quantity < metadata.get('reorder_level', 0):
                self._create_alert(
                    'low_stock',
                    reading.location,
                    material_id,
                    f"Low stock: {material.name} at {material.quantity} {material.unit}"
                )

    def _create_alert(self, alert_type: str, location: str,
                      material_id: str, message: str):
        """Create system alert"""
        self.alerts.append({
            'alert_id': f"ALT-{uuid.uuid4().hex[:8]}",
            'type': alert_type,
            'location': location,
            'material_id': material_id,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False
        })

    def record_delivery(self, material_id: str, quantity: float,
                        location: str) -> MaterialMovement:
        """Record material delivery"""
        material = self.materials.get(material_id)
        if not material:
            raise ValueError(f"Unknown material: {material_id}")

        movement = MaterialMovement(
            movement_id=f"MOV-{uuid.uuid4().hex[:8]}",
            material_id=material_id,
            from_location="supplier",
            to_location=location,
            quantity=quantity,
            timestamp=datetime.now(),
            recorded_by="manual_entry",
            movement_type='delivery'
        )

        self.movements.append(movement)

        material.quantity += quantity
        material.location = location
        material.status = MaterialStatus.DELIVERED
        material.last_updated = datetime.now()

        return movement

    def get_material_history(self, material_id: str) -> List[Dict]:
        """Get movement history for a material"""
        history = []

        for movement in self.movements:
            if movement.material_id == material_id:
                history.append({
                    'movement_id': movement.movement_id,
                    'type': movement.movement_type,
                    'from': movement.from_location,
                    'to': movement.to_location,
                    'quantity': movement.quantity,
                    'timestamp': movement.timestamp.isoformat()
                })

        return sorted(history, key=lambda x: x['timestamp'])

    def get_inventory_report(self) -> Dict:
        """Generate inventory report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_materials': len(self.materials),
            'by_status': {},
            'by_location': {},
            'alerts': [a for a in self.alerts if not a['acknowledged']],
            'materials': []
        }

        for material in self.materials.values():
            status = material.status.value
            report['by_status'][status] = report['by_status'].get(status, 0) + 1

            if material.location:
                loc = material.location
                if loc not in report['by_location']:
                    report['by_location'][loc] = []
                report['by_location'][loc].append({
                    'id': material.material_id,
                    'name': material.name,
                    'quantity': material.quantity,
                    'unit': material.unit
                })

            report['materials'].append({
                'id': material.material_id,
                'name': material.name,
                'quantity': material.quantity,
                'unit': material.unit,
                'status': status,
                'location': material.location,
                'rfid': material.rfid_tag,
                'last_updated': material.last_updated.isoformat()
            })

        return report
```

### GPS Fleet Tracking

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

@dataclass
class GPSPosition:
    latitude: float
    longitude: float
    timestamp: datetime
    speed: float = 0  # km/h
    heading: float = 0  # degrees

@dataclass
class DeliveryVehicle:
    vehicle_id: str
    plate_number: str
    driver: str
    current_position: Optional[GPSPosition] = None
    material_ids: List[str] = None
    destination: Optional[Tuple[float, float]] = None
    estimated_arrival: Optional[datetime] = None

class FleetTracker:
    """GPS-based fleet tracking for material deliveries"""

    def __init__(self):
        self.vehicles: Dict[str, DeliveryVehicle] = {}
        self.position_history: Dict[str, List[GPSPosition]] = {}
        self.geofences: Dict[str, Dict] = {}

    def register_vehicle(self, plate_number: str, driver: str) -> DeliveryVehicle:
        """Register delivery vehicle"""
        vehicle_id = f"VEH-{plate_number.replace(' ', '').upper()}"

        vehicle = DeliveryVehicle(
            vehicle_id=vehicle_id,
            plate_number=plate_number,
            driver=driver,
            material_ids=[]
        )

        self.vehicles[vehicle_id] = vehicle
        self.position_history[vehicle_id] = []

        return vehicle

    def update_position(self, vehicle_id: str, lat: float, lon: float,
                       speed: float = 0, heading: float = 0) -> GPSPosition:
        """Update vehicle position"""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            raise ValueError(f"Unknown vehicle: {vehicle_id}")

        position = GPSPosition(
            latitude=lat,
            longitude=lon,
            timestamp=datetime.now(),
            speed=speed,
            heading=heading
        )

        vehicle.current_position = position
        self.position_history[vehicle_id].append(position)

        # Update ETA if destination set
        if vehicle.destination:
            vehicle.estimated_arrival = self._calculate_eta(vehicle)

        # Check geofences
        self._check_geofences(vehicle_id, position)

        return position

    def set_destination(self, vehicle_id: str, lat: float, lon: float):
        """Set delivery destination"""
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle:
            vehicle.destination = (lat, lon)
            if vehicle.current_position:
                vehicle.estimated_arrival = self._calculate_eta(vehicle)

    def assign_materials(self, vehicle_id: str, material_ids: List[str]):
        """Assign materials to vehicle for delivery"""
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle:
            vehicle.material_ids = material_ids

    def add_geofence(self, name: str, center_lat: float, center_lon: float,
                    radius_meters: float, fence_type: str = 'destination'):
        """Add geofence for location monitoring"""
        self.geofences[name] = {
            'center': (center_lat, center_lon),
            'radius': radius_meters,
            'type': fence_type,
            'vehicles_inside': []
        }

    def _calculate_eta(self, vehicle: DeliveryVehicle) -> datetime:
        """Calculate estimated time of arrival"""
        if not vehicle.current_position or not vehicle.destination:
            return None

        distance = self._haversine_distance(
            vehicle.current_position.latitude,
            vehicle.current_position.longitude,
            vehicle.destination[0],
            vehicle.destination[1]
        )

        # Use current speed or assume 40 km/h average
        speed = vehicle.current_position.speed if vehicle.current_position.speed > 0 else 40

        hours = distance / speed
        return datetime.now() + timedelta(hours=hours)

    def _haversine_distance(self, lat1: float, lon1: float,
                           lat2: float, lon2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat/2)**2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def _check_geofences(self, vehicle_id: str, position: GPSPosition):
        """Check if vehicle entered/exited geofences"""
        for fence_name, fence in self.geofences.items():
            distance = self._haversine_distance(
                position.latitude,
                position.longitude,
                fence['center'][0],
                fence['center'][1]
            ) * 1000  # Convert to meters

            is_inside = distance <= fence['radius']
            was_inside = vehicle_id in fence['vehicles_inside']

            if is_inside and not was_inside:
                # Entered geofence
                fence['vehicles_inside'].append(vehicle_id)
                self._on_geofence_enter(vehicle_id, fence_name, fence['type'])

            elif not is_inside and was_inside:
                # Exited geofence
                fence['vehicles_inside'].remove(vehicle_id)
                self._on_geofence_exit(vehicle_id, fence_name, fence['type'])

    def _on_geofence_enter(self, vehicle_id: str, fence_name: str, fence_type: str):
        """Handle geofence entry event"""
        print(f"Vehicle {vehicle_id} entered {fence_name} ({fence_type})")
        # Could trigger webhook, update status, send notification

    def _on_geofence_exit(self, vehicle_id: str, fence_name: str, fence_type: str):
        """Handle geofence exit event"""
        print(f"Vehicle {vehicle_id} exited {fence_name} ({fence_type})")

    def get_fleet_status(self) -> Dict:
        """Get current fleet status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'total_vehicles': len(self.vehicles),
            'vehicles': []
        }

        for vehicle in self.vehicles.values():
            v_status = {
                'id': vehicle.vehicle_id,
                'plate': vehicle.plate_number,
                'driver': vehicle.driver,
                'materials': vehicle.material_ids,
                'position': None,
                'eta': None
            }

            if vehicle.current_position:
                v_status['position'] = {
                    'lat': vehicle.current_position.latitude,
                    'lon': vehicle.current_position.longitude,
                    'speed': vehicle.current_position.speed,
                    'updated': vehicle.current_position.timestamp.isoformat()
                }

            if vehicle.estimated_arrival:
                v_status['eta'] = vehicle.estimated_arrival.isoformat()

            status['vehicles'].append(v_status)

        return status
```

### MQTT Integration for Sensors

```python
import json
from datetime import datetime
from typing import Callable, Dict

class IoTMessageHandler:
    """Handle MQTT messages from IoT sensors"""

    def __init__(self, tracking_system: MaterialTrackingSystem):
        self.tracking = tracking_system
        self.topic_handlers: Dict[str, Callable] = {}
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup topic handlers"""
        self.topic_handlers = {
            'sensors/rfid/+': self._handle_rfid,
            'sensors/gps/+': self._handle_gps,
            'sensors/temperature/+': self._handle_temperature,
            'sensors/humidity/+': self._handle_humidity,
            'sensors/weight/+': self._handle_weight
        }

    def process_message(self, topic: str, payload: bytes):
        """Process incoming MQTT message"""
        try:
            data = json.loads(payload.decode('utf-8'))

            # Find matching handler
            for pattern, handler in self.topic_handlers.items():
                if self._topic_matches(topic, pattern):
                    handler(topic, data)
                    break

        except json.JSONDecodeError:
            print(f"Invalid JSON in message: {topic}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def _topic_matches(self, topic: str, pattern: str) -> bool:
        """Check if topic matches pattern (+ is wildcard)"""
        topic_parts = topic.split('/')
        pattern_parts = pattern.split('/')

        if len(topic_parts) != len(pattern_parts):
            return False

        for t, p in zip(topic_parts, pattern_parts):
            if p != '+' and t != p:
                return False

        return True

    def _handle_rfid(self, topic: str, data: Dict):
        """Handle RFID scan message"""
        sensor_id = topic.split('/')[-1]

        self.tracking.process_sensor_reading(
            sensor_id=sensor_id,
            value=1,  # Scan detected
            unit='scan',
            metadata={
                'rfid_tag': data.get('tag_id'),
                'signal_strength': data.get('rssi')
            }
        )

    def _handle_gps(self, topic: str, data: Dict):
        """Handle GPS position message"""
        sensor_id = topic.split('/')[-1]

        self.tracking.process_sensor_reading(
            sensor_id=sensor_id,
            value=data.get('latitude', 0),
            unit='degrees',
            metadata={
                'longitude': data.get('longitude'),
                'speed': data.get('speed'),
                'vehicle_id': data.get('vehicle_id'),
                'material_ids': data.get('materials', [])
            }
        )

    def _handle_temperature(self, topic: str, data: Dict):
        """Handle temperature sensor message"""
        sensor_id = topic.split('/')[-1]

        self.tracking.process_sensor_reading(
            sensor_id=sensor_id,
            value=data.get('value', 0),
            unit='celsius',
            metadata={}
        )

    def _handle_humidity(self, topic: str, data: Dict):
        """Handle humidity sensor message"""
        sensor_id = topic.split('/')[-1]

        self.tracking.process_sensor_reading(
            sensor_id=sensor_id,
            value=data.get('value', 0),
            unit='percent',
            metadata={}
        )

    def _handle_weight(self, topic: str, data: Dict):
        """Handle weight sensor message"""
        sensor_id = topic.split('/')[-1]

        self.tracking.process_sensor_reading(
            sensor_id=sensor_id,
            value=data.get('value', 0),
            unit='kg',
            metadata={
                'material_id': data.get('material_id'),
                'previous_weight': data.get('previous'),
                'reorder_level': data.get('reorder_level')
            }
        )


# Example MQTT message formats
EXAMPLE_MESSAGES = {
    'rfid_scan': {
        'topic': 'sensors/rfid/SNS-RFID-001',
        'payload': {
            'tag_id': 'RFID-MAT-001',
            'rssi': -45,
            'timestamp': '2024-01-15T10:30:00Z'
        }
    },
    'gps_update': {
        'topic': 'sensors/gps/VEH-ABC123',
        'payload': {
            'latitude': 55.7558,
            'longitude': 37.6173,
            'speed': 45,
            'heading': 90,
            'vehicle_id': 'VEH-ABC123',
            'materials': ['MAT-001', 'MAT-002']
        }
    },
    'temperature': {
        'topic': 'sensors/temperature/SNS-TEMP-001',
        'payload': {
            'value': 28.5,
            'battery': 85
        }
    }
}
```

### Dashboard Data Generator

```python
class MaterialDashboard:
    """Generate data for material tracking dashboard"""

    def __init__(self, tracking: MaterialTrackingSystem,
                 fleet: FleetTracker):
        self.tracking = tracking
        self.fleet = fleet

    def get_dashboard_data(self) -> Dict:
        """Get comprehensive dashboard data"""
        inventory = self.tracking.get_inventory_report()
        fleet_status = self.fleet.get_fleet_status()

        # Calculate usage trends (last 7 days)
        usage_movements = [
            m for m in self.tracking.movements
            if m.movement_type == 'usage' and
            (datetime.now() - m.timestamp).days <= 7
        ]

        daily_usage = {}
        for m in usage_movements:
            day = m.timestamp.strftime('%Y-%m-%d')
            daily_usage[day] = daily_usage.get(day, 0) + m.quantity

        return {
            'summary': {
                'total_materials': inventory['total_materials'],
                'in_transit': inventory['by_status'].get('in_transit', 0),
                'in_storage': inventory['by_status'].get('in_storage', 0),
                'active_alerts': len(inventory['alerts']),
                'active_deliveries': len([v for v in self.fleet.vehicles.values()
                                         if v.material_ids])
            },
            'inventory': inventory,
            'fleet': fleet_status,
            'alerts': inventory['alerts'][:10],  # Top 10
            'usage_trend': daily_usage,
            'storage_conditions': {
                loc: {
                    'temperature': cond.temperature,
                    'humidity': cond.humidity,
                    'ok': cond.is_acceptable
                }
                for loc, cond in self.tracking.storage_conditions.items()
            }
        }
```

## Quick Reference

| Sensor Type | Use Case | Data Format | Update Frequency |
|-------------|----------|-------------|------------------|
| RFID | Material identification | Tag ID, signal strength | On scan |
| GPS | Delivery tracking | Lat/Lon, speed, heading | 10-60 sec |
| Temperature | Storage monitoring | Celsius | 5-15 min |
| Humidity | Storage monitoring | Percentage | 5-15 min |
| Weight | Usage tracking | Kilograms | On change |

## MQTT Topics Structure

```
sensors/
├── rfid/{sensor_id}
├── gps/{vehicle_id}
├── temperature/{sensor_id}
├── humidity/{sensor_id}
├── weight/{sensor_id}
└── motion/{sensor_id}

alerts/
├── low_stock/{material_id}
├── temperature/{location}
├── delivery/{vehicle_id}
└── geofence/{fence_name}
```

## Resources

- **MQTT Protocol**: https://mqtt.org
- **IoT Platforms**: AWS IoT, Azure IoT Hub, ThingsBoard
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `n8n-workflow-automation` for IoT event automation
- See `data-visualization` for tracking dashboards
- See `qto-report` for material quantity integration
