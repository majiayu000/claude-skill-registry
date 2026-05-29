---
name: digital-twin-sync
description: "Synchronize construction digital twins with real-time data. Connect BIM models with IoT sensors, progress updates, and field data for live project visualization and monitoring."
---

# Digital Twin Synchronization

## Overview

This skill implements digital twin synchronization for construction projects. Connect BIM models with real-time sensor data, progress updates, and field information to create a living digital representation.

**Capabilities:**
- BIM-IoT data binding
- Real-time status updates
- Historical data tracking
- Anomaly detection
- Predictive analytics
- Multi-source data fusion

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json

class ElementStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ISSUE = "issue"

@dataclass
class TwinElement:
    element_id: str
    ifc_guid: str
    element_type: str
    status: ElementStatus
    properties: Dict[str, Any] = field(default_factory=dict)
    sensor_bindings: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class SensorData:
    sensor_id: str
    value: float
    unit: str
    timestamp: datetime
    quality: float = 1.0

class SimpleTwin:
    """Simple digital twin implementation"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.elements: Dict[str, TwinElement] = {}
        self.sensor_data: Dict[str, List[SensorData]] = {}

    def add_element(self, element: TwinElement):
        self.elements[element.element_id] = element

    def bind_sensor(self, element_id: str, sensor_id: str):
        if element_id in self.elements:
            self.elements[element_id].sensor_bindings.append(sensor_id)

    def update_sensor(self, data: SensorData):
        if data.sensor_id not in self.sensor_data:
            self.sensor_data[data.sensor_id] = []
        self.sensor_data[data.sensor_id].append(data)

        # Update linked elements
        for elem in self.elements.values():
            if data.sensor_id in elem.sensor_bindings:
                elem.properties[f'sensor_{data.sensor_id}'] = data.value
                elem.last_updated = data.timestamp

    def get_element_state(self, element_id: str) -> Dict:
        elem = self.elements.get(element_id)
        if not elem:
            return {}

        state = {
            'element_id': elem.element_id,
            'status': elem.status.value,
            'properties': elem.properties,
            'last_updated': elem.last_updated.isoformat()
        }

        # Add latest sensor values
        for sensor_id in elem.sensor_bindings:
            if sensor_id in self.sensor_data and self.sensor_data[sensor_id]:
                latest = self.sensor_data[sensor_id][-1]
                state[f'sensor_{sensor_id}'] = {
                    'value': latest.value,
                    'unit': latest.unit,
                    'timestamp': latest.timestamp.isoformat()
                }

        return state

# Example
twin = SimpleTwin("PROJECT-001")
twin.add_element(TwinElement(
    element_id="WALL-001",
    ifc_guid="2O2Fr$t4X7Zf8NOew3FLOH",
    element_type="IfcWall",
    status=ElementStatus.IN_PROGRESS
))
twin.bind_sensor("WALL-001", "TEMP-001")
twin.update_sensor(SensorData("TEMP-001", 22.5, "°C", datetime.now()))
print(twin.get_element_state("WALL-001"))
```

## Comprehensive Digital Twin System

### Core Twin Model

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import json
import threading
from queue import Queue
import time

class DataSource(Enum):
    BIM = "bim"
    IOT = "iot"
    SCHEDULE = "schedule"
    FIELD = "field"
    DRONE = "drone"
    MANUAL = "manual"

@dataclass
class PropertyValue:
    value: Any
    unit: Optional[str]
    timestamp: datetime
    source: DataSource
    confidence: float = 1.0
    history: List[Dict] = field(default_factory=list)

@dataclass
class DigitalTwinElement:
    element_id: str
    ifc_guid: str
    element_type: str
    name: str
    status: ElementStatus = ElementStatus.PLANNED
    properties: Dict[str, PropertyValue] = field(default_factory=dict)
    sensor_bindings: Dict[str, str] = field(default_factory=dict)  # property_name -> sensor_id
    geometry_ref: Optional[str] = None
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    schedule_activity_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_property(self, name: str, value: Any, unit: str = None,
                       source: DataSource = DataSource.MANUAL,
                       confidence: float = 1.0):
        """Update property with history tracking"""
        now = datetime.now()

        if name in self.properties:
            # Store previous value in history
            prev = self.properties[name]
            prev.history.append({
                'value': prev.value,
                'timestamp': prev.timestamp.isoformat(),
                'source': prev.source.value
            })
            # Keep only last 100 values
            prev.history = prev.history[-100:]

            prev.value = value
            prev.unit = unit or prev.unit
            prev.timestamp = now
            prev.source = source
            prev.confidence = confidence
        else:
            self.properties[name] = PropertyValue(
                value=value,
                unit=unit,
                timestamp=now,
                source=source,
                confidence=confidence
            )

        self.updated_at = now

@dataclass
class TwinEvent:
    event_id: str
    event_type: str  # property_update, status_change, alert, etc.
    element_id: str
    timestamp: datetime
    data: Dict
    source: DataSource

class DigitalTwinCore:
    """Core digital twin management system"""

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name
        self.elements: Dict[str, DigitalTwinElement] = {}
        self.events: List[TwinEvent] = []
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.update_queue: Queue = Queue()
        self._running = False

    def import_from_ifc(self, ifc_data: List[Dict]):
        """Import elements from IFC data"""
        for elem_data in ifc_data:
            element = DigitalTwinElement(
                element_id=elem_data.get('id', f"ELEM-{len(self.elements)}"),
                ifc_guid=elem_data.get('guid', ''),
                element_type=elem_data.get('type', 'IfcBuildingElement'),
                name=elem_data.get('name', 'Unknown'),
                geometry_ref=elem_data.get('geometry_ref')
            )

            # Import properties
            for prop_name, prop_value in elem_data.get('properties', {}).items():
                element.update_property(
                    prop_name,
                    prop_value.get('value'),
                    prop_value.get('unit'),
                    DataSource.BIM
                )

            self.elements[element.element_id] = element

    def bind_sensor_to_property(self, element_id: str, property_name: str,
                               sensor_id: str, transform: Callable = None):
        """Bind IoT sensor to element property"""
        element = self.elements.get(element_id)
        if element:
            element.sensor_bindings[property_name] = sensor_id
            # Store transform function if needed
            if transform:
                element.sensor_bindings[f'{property_name}_transform'] = transform

    def process_sensor_update(self, sensor_id: str, value: float,
                             unit: str, timestamp: datetime = None):
        """Process incoming sensor data"""
        timestamp = timestamp or datetime.now()

        # Find all elements bound to this sensor
        for element in self.elements.values():
            for prop_name, bound_sensor in element.sensor_bindings.items():
                if bound_sensor == sensor_id and not prop_name.endswith('_transform'):
                    # Apply transform if exists
                    transform_key = f'{prop_name}_transform'
                    if transform_key in element.sensor_bindings:
                        transform = element.sensor_bindings[transform_key]
                        value = transform(value)

                    element.update_property(prop_name, value, unit, DataSource.IOT)

                    # Create event
                    self._emit_event('property_update', element.element_id, {
                        'property': prop_name,
                        'value': value,
                        'sensor_id': sensor_id
                    }, DataSource.IOT)

    def update_status(self, element_id: str, status: ElementStatus,
                     source: DataSource = DataSource.FIELD):
        """Update element construction status"""
        element = self.elements.get(element_id)
        if not element:
            return

        old_status = element.status
        element.status = status
        element.updated_at = datetime.now()

        self._emit_event('status_change', element_id, {
            'old_status': old_status.value,
            'new_status': status.value
        }, source)

    def _emit_event(self, event_type: str, element_id: str,
                   data: Dict, source: DataSource):
        """Emit twin event"""
        event = TwinEvent(
            event_id=f"EVT-{len(self.events):06d}",
            event_type=event_type,
            element_id=element_id,
            timestamp=datetime.now(),
            data=data,
            source=source
        )

        self.events.append(event)

        # Notify handlers
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Event handler error: {e}")

    def on_event(self, event_type: str, handler: Callable):
        """Register event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def get_element_snapshot(self, element_id: str) -> Dict:
        """Get current state snapshot of element"""
        element = self.elements.get(element_id)
        if not element:
            return {}

        return {
            'element_id': element.element_id,
            'ifc_guid': element.ifc_guid,
            'type': element.element_type,
            'name': element.name,
            'status': element.status.value,
            'properties': {
                name: {
                    'value': prop.value,
                    'unit': prop.unit,
                    'timestamp': prop.timestamp.isoformat(),
                    'source': prop.source.value,
                    'confidence': prop.confidence
                }
                for name, prop in element.properties.items()
            },
            'updated_at': element.updated_at.isoformat()
        }

    def get_project_snapshot(self) -> Dict:
        """Get full project state snapshot"""
        status_counts = {}
        for elem in self.elements.values():
            status = elem.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'timestamp': datetime.now().isoformat(),
            'element_count': len(self.elements),
            'status_summary': status_counts,
            'recent_events': [
                {
                    'event_id': e.event_id,
                    'type': e.event_type,
                    'element': e.element_id,
                    'timestamp': e.timestamp.isoformat()
                }
                for e in self.events[-10:]
            ]
        }
```

### Real-Time Synchronization

```python
import asyncio
from typing import Dict, List, Callable
import websockets
import json

class TwinSynchronizer:
    """Real-time twin synchronization service"""

    def __init__(self, twin: DigitalTwinCore):
        self.twin = twin
        self.subscribers: Dict[str, List[websockets.WebSocketServerProtocol]] = {}
        self.sync_interval = 1.0  # seconds

    async def start_server(self, host: str = 'localhost', port: int = 8765):
        """Start WebSocket server for real-time updates"""
        async with websockets.serve(self._handle_connection, host, port):
            print(f"Twin sync server running on ws://{host}:{port}")
            await asyncio.Future()  # Run forever

    async def _handle_connection(self, websocket, path):
        """Handle WebSocket connection"""
        try:
            async for message in websocket:
                data = json.loads(message)
                await self._process_message(websocket, data)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Remove from all subscriptions
            for element_id in list(self.subscribers.keys()):
                if websocket in self.subscribers[element_id]:
                    self.subscribers[element_id].remove(websocket)

    async def _process_message(self, websocket, data: Dict):
        """Process incoming message"""
        msg_type = data.get('type')

        if msg_type == 'subscribe':
            element_id = data.get('element_id', '*')
            if element_id not in self.subscribers:
                self.subscribers[element_id] = []
            self.subscribers[element_id].append(websocket)

            # Send current state
            if element_id == '*':
                state = self.twin.get_project_snapshot()
            else:
                state = self.twin.get_element_snapshot(element_id)

            await websocket.send(json.dumps({
                'type': 'state',
                'data': state
            }))

        elif msg_type == 'update':
            # Handle incoming update from field
            element_id = data.get('element_id')
            updates = data.get('updates', {})

            for prop_name, value in updates.items():
                element = self.twin.elements.get(element_id)
                if element:
                    element.update_property(prop_name, value, source=DataSource.FIELD)

            # Broadcast update
            await self._broadcast_update(element_id)

        elif msg_type == 'status_update':
            element_id = data.get('element_id')
            status = ElementStatus(data.get('status'))
            self.twin.update_status(element_id, status, DataSource.FIELD)
            await self._broadcast_update(element_id)

    async def _broadcast_update(self, element_id: str):
        """Broadcast element update to subscribers"""
        state = self.twin.get_element_snapshot(element_id)
        message = json.dumps({
            'type': 'update',
            'element_id': element_id,
            'data': state
        })

        # Send to specific element subscribers
        for ws in self.subscribers.get(element_id, []):
            try:
                await ws.send(message)
            except:
                pass

        # Send to wildcard subscribers
        for ws in self.subscribers.get('*', []):
            try:
                await ws.send(message)
            except:
                pass

    def setup_sensor_integration(self, mqtt_client):
        """Setup MQTT integration for IoT sensors"""
        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
                self.twin.process_sensor_update(
                    sensor_id=data.get('sensor_id'),
                    value=data.get('value'),
                    unit=data.get('unit'),
                    timestamp=datetime.fromisoformat(data.get('timestamp'))
                )
            except Exception as e:
                print(f"Sensor message error: {e}")

        mqtt_client.on_message = on_message
        mqtt_client.subscribe("sensors/#")
```

### Schedule Integration

```python
from datetime import date, datetime

@dataclass
class ScheduleActivity:
    activity_id: str
    name: str
    planned_start: date
    planned_end: date
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    percent_complete: float = 0
    element_ids: List[str] = field(default_factory=list)

class ScheduleTwinIntegrator:
    """Integrate schedule with digital twin"""

    def __init__(self, twin: DigitalTwinCore):
        self.twin = twin
        self.activities: Dict[str, ScheduleActivity] = {}

    def import_schedule(self, schedule_data: List[Dict]):
        """Import schedule activities"""
        for act_data in schedule_data:
            activity = ScheduleActivity(
                activity_id=act_data['id'],
                name=act_data['name'],
                planned_start=date.fromisoformat(act_data['start']),
                planned_end=date.fromisoformat(act_data['end']),
                element_ids=act_data.get('elements', [])
            )
            self.activities[activity.activity_id] = activity

            # Link elements to activity
            for elem_id in activity.element_ids:
                if elem_id in self.twin.elements:
                    self.twin.elements[elem_id].schedule_activity_id = activity.activity_id

    def update_activity_progress(self, activity_id: str, percent_complete: float,
                                actual_start: date = None, actual_end: date = None):
        """Update activity progress"""
        activity = self.activities.get(activity_id)
        if not activity:
            return

        activity.percent_complete = percent_complete
        if actual_start:
            activity.actual_start = actual_start
        if actual_end:
            activity.actual_end = actual_end

        # Update linked elements
        status = self._determine_status(percent_complete)
        for elem_id in activity.element_ids:
            self.twin.update_status(elem_id, status, DataSource.SCHEDULE)

    def _determine_status(self, percent: float) -> ElementStatus:
        """Determine element status from progress percentage"""
        if percent == 0:
            return ElementStatus.PLANNED
        elif percent < 100:
            return ElementStatus.IN_PROGRESS
        else:
            return ElementStatus.COMPLETED

    def calculate_schedule_variance(self) -> Dict:
        """Calculate schedule performance"""
        today = date.today()
        variances = []

        for activity in self.activities.values():
            planned_duration = (activity.planned_end - activity.planned_start).days
            if planned_duration == 0:
                continue

            if activity.actual_start:
                start_variance = (activity.actual_start - activity.planned_start).days
            else:
                start_variance = None

            if activity.actual_end:
                end_variance = (activity.actual_end - activity.planned_end).days
            else:
                end_variance = None

            # Calculate expected progress
            if today >= activity.planned_end:
                expected_progress = 100
            elif today <= activity.planned_start:
                expected_progress = 0
            else:
                elapsed = (today - activity.planned_start).days
                expected_progress = elapsed / planned_duration * 100

            progress_variance = activity.percent_complete - expected_progress

            variances.append({
                'activity_id': activity.activity_id,
                'name': activity.name,
                'planned_start': activity.planned_start.isoformat(),
                'planned_end': activity.planned_end.isoformat(),
                'actual_progress': activity.percent_complete,
                'expected_progress': expected_progress,
                'progress_variance': progress_variance,
                'start_variance_days': start_variance,
                'status': 'ahead' if progress_variance > 0 else 'behind' if progress_variance < -5 else 'on_track'
            })

        return {
            'date': today.isoformat(),
            'activities': variances,
            'on_track_count': sum(1 for v in variances if v['status'] == 'on_track'),
            'ahead_count': sum(1 for v in variances if v['status'] == 'ahead'),
            'behind_count': sum(1 for v in variances if v['status'] == 'behind')
        }
```

### Anomaly Detection

```python
import numpy as np
from collections import deque

class TwinAnomalyDetector:
    """Detect anomalies in digital twin data"""

    def __init__(self, twin: DigitalTwinCore, window_size: int = 100):
        self.twin = twin
        self.window_size = window_size
        self.value_windows: Dict[str, deque] = {}  # key: element_id:property
        self.thresholds: Dict[str, Dict] = {}

    def set_threshold(self, element_id: str, property_name: str,
                     min_value: float = None, max_value: float = None,
                     std_multiplier: float = 3.0):
        """Set threshold for property monitoring"""
        key = f"{element_id}:{property_name}"
        self.thresholds[key] = {
            'min': min_value,
            'max': max_value,
            'std_multiplier': std_multiplier
        }

    def check_value(self, element_id: str, property_name: str, value: float) -> Dict:
        """Check value for anomalies"""
        key = f"{element_id}:{property_name}"

        # Initialize window if needed
        if key not in self.value_windows:
            self.value_windows[key] = deque(maxlen=self.window_size)

        window = self.value_windows[key]

        anomaly = {
            'is_anomaly': False,
            'type': None,
            'severity': 'normal',
            'details': {}
        }

        # Check against thresholds
        if key in self.thresholds:
            thresh = self.thresholds[key]

            if thresh['min'] is not None and value < thresh['min']:
                anomaly['is_anomaly'] = True
                anomaly['type'] = 'below_minimum'
                anomaly['severity'] = 'warning'
                anomaly['details']['threshold'] = thresh['min']
                anomaly['details']['value'] = value

            if thresh['max'] is not None and value > thresh['max']:
                anomaly['is_anomaly'] = True
                anomaly['type'] = 'above_maximum'
                anomaly['severity'] = 'warning'
                anomaly['details']['threshold'] = thresh['max']
                anomaly['details']['value'] = value

        # Statistical anomaly detection
        if len(window) >= 10:
            mean = np.mean(window)
            std = np.std(window)

            if std > 0:
                z_score = abs(value - mean) / std
                if z_score > 3:
                    anomaly['is_anomaly'] = True
                    anomaly['type'] = 'statistical_outlier'
                    anomaly['severity'] = 'critical' if z_score > 5 else 'warning'
                    anomaly['details']['z_score'] = z_score
                    anomaly['details']['mean'] = mean
                    anomaly['details']['std'] = std

        # Add to window
        window.append(value)

        return anomaly

    def monitor_element(self, element_id: str) -> List[Dict]:
        """Monitor all properties of an element for anomalies"""
        element = self.twin.elements.get(element_id)
        if not element:
            return []

        anomalies = []
        for prop_name, prop in element.properties.items():
            if isinstance(prop.value, (int, float)):
                result = self.check_value(element_id, prop_name, prop.value)
                if result['is_anomaly']:
                    result['element_id'] = element_id
                    result['property'] = prop_name
                    result['timestamp'] = prop.timestamp.isoformat()
                    anomalies.append(result)

        return anomalies
```

## Quick Reference

| Data Source | Update Frequency | Reliability |
|-------------|------------------|-------------|
| BIM Model | On change | High |
| IoT Sensors | Real-time | Variable |
| Schedule | Daily | High |
| Field Updates | Event-driven | Medium |
| Drone Surveys | Periodic | High |

## Resources

- **Digital Twin Consortium**: https://www.digitaltwinconsortium.org
- **IFC/BIM Standards**: https://www.buildingsmart.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `material-tracking-iot` for IoT integration
- See `4d-simulation` for schedule visualization
- See `bim-validation-pipeline` for model validation
