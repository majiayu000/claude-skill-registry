---
name: "equipment-telematics"
description: "Integrate and analyze telematics data from heavy construction equipment. Track location, utilization, fuel consumption, maintenance needs, and operator behavior."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Equipment Telematics

## Overview

Integrate telematics data from heavy construction equipment (excavators, cranes, loaders, trucks) to monitor utilization, track location, analyze fuel efficiency, predict maintenance needs, and ensure safe operation.

## Telematics Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  EQUIPMENT TELEMATICS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EQUIPMENT                  TELEMATICS              ANALYTICS   │
│  ─────────                  ──────────              ─────────   │
│                                                                  │
│  🚜 Excavator  ────┐       📍 Location              📊 Utilization│
│  🏗️ Crane      ────┼──────→ 🔧 Engine Hours ────────→ ⛽ Fuel      │
│  🚛 Truck      ────┤       ⛽ Fuel Level             🔧 Maintenance│
│  🚧 Loader     ────┘       ⚡ Performance            👷 Operator   │
│                                                                  │
│  METRICS TRACKED:                                               │
│  • GPS location and geofencing                                  │
│  • Engine hours and idle time                                   │
│  • Fuel consumption rate                                        │
│  • Load cycles and productivity                                 │
│  • Fault codes and diagnostics                                  │
│  • Operator behavior and safety                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import math

class EquipmentType(Enum):
    EXCAVATOR = "excavator"
    CRANE = "crane"
    LOADER = "loader"
    BULLDOZER = "bulldozer"
    DUMP_TRUCK = "dump_truck"
    CONCRETE_MIXER = "concrete_mixer"
    FORKLIFT = "forklift"
    COMPACTOR = "compactor"
    GRADER = "grader"
    TELEHANDLER = "telehandler"

class OperatingStatus(Enum):
    OPERATING = "operating"
    IDLE = "idle"
    OFF = "off"
    MAINTENANCE = "maintenance"
    FAULT = "fault"

class FaultSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SHUTDOWN = "shutdown"

@dataclass
class GPSLocation:
    latitude: float
    longitude: float
    altitude: float = 0.0
    speed: float = 0.0
    heading: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TelematicsReading:
    equipment_id: str
    timestamp: datetime
    location: GPSLocation
    engine_hours: float
    fuel_level: float  # Percentage
    fuel_rate: float   # L/hr
    engine_rpm: int
    hydraulic_temp: float
    coolant_temp: float
    operating_status: OperatingStatus
    load_percentage: float = 0.0
    operator_id: str = ""

@dataclass
class FaultCode:
    code: str
    description: str
    severity: FaultSeverity
    timestamp: datetime
    equipment_id: str
    resolved: bool = False

@dataclass
class Equipment:
    id: str
    name: str
    equipment_type: EquipmentType
    make: str
    model: str
    year: int
    serial_number: str
    hourly_rate: float = 0.0
    fuel_capacity: float = 0.0  # Liters
    current_hours: float = 0.0
    next_service_hours: float = 0.0
    assigned_site: str = ""
    assigned_operator: str = ""

@dataclass
class Geofence:
    id: str
    name: str
    center_lat: float
    center_lon: float
    radius_meters: float
    allowed_equipment: List[str] = field(default_factory=list)

@dataclass
class UtilizationReport:
    equipment_id: str
    period_start: datetime
    period_end: datetime
    total_hours: float
    operating_hours: float
    idle_hours: float
    off_hours: float
    utilization_pct: float
    idle_pct: float
    fuel_consumed: float
    fuel_efficiency: float  # L/operating hour
    cycles: int

class EquipmentTelematics:
    """Integrate and analyze equipment telematics data."""

    # Maintenance intervals by type (hours)
    SERVICE_INTERVALS = {
        EquipmentType.EXCAVATOR: 250,
        EquipmentType.CRANE: 200,
        EquipmentType.LOADER: 250,
        EquipmentType.BULLDOZER: 250,
        EquipmentType.DUMP_TRUCK: 300,
    }

    # Typical fuel rates (L/hr)
    TYPICAL_FUEL_RATES = {
        EquipmentType.EXCAVATOR: 15,
        EquipmentType.CRANE: 12,
        EquipmentType.LOADER: 18,
        EquipmentType.BULLDOZER: 25,
        EquipmentType.DUMP_TRUCK: 20,
    }

    def __init__(self, fleet_name: str):
        self.fleet_name = fleet_name
        self.equipment: Dict[str, Equipment] = {}
        self.readings: List[TelematicsReading] = []
        self.faults: List[FaultCode] = []
        self.geofences: Dict[str, Geofence] = {}

    def register_equipment(self, id: str, name: str, equipment_type: EquipmentType,
                          make: str, model: str, year: int, serial_number: str,
                          hourly_rate: float = 0, fuel_capacity: float = 0) -> Equipment:
        """Register equipment in fleet."""
        equipment = Equipment(
            id=id,
            name=name,
            equipment_type=equipment_type,
            make=make,
            model=model,
            year=year,
            serial_number=serial_number,
            hourly_rate=hourly_rate,
            fuel_capacity=fuel_capacity
        )
        self.equipment[id] = equipment
        return equipment

    def add_geofence(self, id: str, name: str, center_lat: float,
                    center_lon: float, radius_meters: float,
                    allowed_equipment: List[str] = None) -> Geofence:
        """Add geofence boundary."""
        geofence = Geofence(
            id=id,
            name=name,
            center_lat=center_lat,
            center_lon=center_lon,
            radius_meters=radius_meters,
            allowed_equipment=allowed_equipment or []
        )
        self.geofences[id] = geofence
        return geofence

    def ingest_reading(self, equipment_id: str, location: GPSLocation,
                      engine_hours: float, fuel_level: float, fuel_rate: float,
                      engine_rpm: int, hydraulic_temp: float, coolant_temp: float,
                      load_percentage: float = 0, operator_id: str = "") -> TelematicsReading:
        """Ingest telematics reading from equipment."""
        if equipment_id not in self.equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")

        # Determine operating status
        if engine_rpm == 0:
            status = OperatingStatus.OFF
        elif engine_rpm < 800 or load_percentage < 10:
            status = OperatingStatus.IDLE
        else:
            status = OperatingStatus.OPERATING

        reading = TelematicsReading(
            equipment_id=equipment_id,
            timestamp=location.timestamp,
            location=location,
            engine_hours=engine_hours,
            fuel_level=fuel_level,
            fuel_rate=fuel_rate,
            engine_rpm=engine_rpm,
            hydraulic_temp=hydraulic_temp,
            coolant_temp=coolant_temp,
            operating_status=status,
            load_percentage=load_percentage,
            operator_id=operator_id
        )

        self.readings.append(reading)

        # Update equipment status
        equip = self.equipment[equipment_id]
        equip.current_hours = engine_hours

        # Check for issues
        self._check_diagnostics(equipment_id, reading)
        self._check_geofence(equipment_id, location)

        return reading

    def _check_diagnostics(self, equipment_id: str, reading: TelematicsReading):
        """Check for diagnostic issues."""
        equip = self.equipment[equipment_id]

        # High temperature warning
        if reading.hydraulic_temp > 90:
            self._add_fault(equipment_id, "HYD_TEMP_HIGH",
                          "Hydraulic temperature high", FaultSeverity.WARNING)

        if reading.coolant_temp > 100:
            self._add_fault(equipment_id, "COOLANT_TEMP_HIGH",
                          "Coolant temperature critical", FaultSeverity.CRITICAL)

        # Low fuel warning
        if reading.fuel_level < 15:
            self._add_fault(equipment_id, "FUEL_LOW",
                          "Fuel level below 15%", FaultSeverity.WARNING)

        # Service due
        service_interval = self.SERVICE_INTERVALS.get(equip.equipment_type, 250)
        hours_to_service = equip.next_service_hours - reading.engine_hours

        if hours_to_service < 0:
            self._add_fault(equipment_id, "SERVICE_OVERDUE",
                          "Maintenance service overdue", FaultSeverity.WARNING)
        elif hours_to_service < 50:
            self._add_fault(equipment_id, "SERVICE_DUE",
                          f"Service due in {hours_to_service:.0f} hours", FaultSeverity.INFO)

    def _check_geofence(self, equipment_id: str, location: GPSLocation):
        """Check geofence violations."""
        for geofence in self.geofences.values():
            # Calculate distance from center
            distance = self._haversine_distance(
                location.latitude, location.longitude,
                geofence.center_lat, geofence.center_lon
            )

            if distance > geofence.radius_meters:
                if (not geofence.allowed_equipment or
                    equipment_id in geofence.allowed_equipment):
                    self._add_fault(equipment_id, "GEOFENCE_EXIT",
                                  f"Equipment left {geofence.name} boundary",
                                  FaultSeverity.WARNING)

    def _haversine_distance(self, lat1: float, lon1: float,
                           lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in meters."""
        R = 6371000  # Earth radius in meters

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi/2)**2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def _add_fault(self, equipment_id: str, code: str,
                  description: str, severity: FaultSeverity):
        """Add fault code."""
        # Check if same fault already active
        existing = [f for f in self.faults
                   if f.equipment_id == equipment_id
                   and f.code == code
                   and not f.resolved]
        if existing:
            return

        fault = FaultCode(
            code=code,
            description=description,
            severity=severity,
            timestamp=datetime.now(),
            equipment_id=equipment_id
        )
        self.faults.append(fault)

    def get_current_status(self, equipment_id: str) -> Dict:
        """Get current status of equipment."""
        if equipment_id not in self.equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")

        equip = self.equipment[equipment_id]

        # Get latest reading
        readings = [r for r in self.readings if r.equipment_id == equipment_id]
        if not readings:
            return {"equipment": equip, "status": "no_data"}

        latest = max(readings, key=lambda r: r.timestamp)

        # Active faults
        active_faults = [f for f in self.faults
                        if f.equipment_id == equipment_id and not f.resolved]

        return {
            "equipment_id": equip.id,
            "name": equip.name,
            "type": equip.equipment_type.value,
            "status": latest.operating_status.value,
            "location": {
                "lat": latest.location.latitude,
                "lon": latest.location.longitude,
                "speed": latest.location.speed
            },
            "engine_hours": latest.engine_hours,
            "fuel_level": latest.fuel_level,
            "fuel_rate": latest.fuel_rate,
            "temps": {
                "hydraulic": latest.hydraulic_temp,
                "coolant": latest.coolant_temp
            },
            "operator": latest.operator_id,
            "active_faults": len(active_faults),
            "last_update": latest.timestamp
        }

    def calculate_utilization(self, equipment_id: str,
                             start_date: datetime,
                             end_date: datetime) -> UtilizationReport:
        """Calculate utilization metrics for equipment."""
        readings = [r for r in self.readings
                   if r.equipment_id == equipment_id
                   and start_date <= r.timestamp <= end_date]

        if not readings:
            return None

        readings.sort(key=lambda r: r.timestamp)

        total_hours = (end_date - start_date).total_seconds() / 3600
        operating_hours = 0
        idle_hours = 0
        fuel_consumed = 0

        # Calculate from readings
        for i in range(1, len(readings)):
            prev = readings[i-1]
            curr = readings[i]

            interval_hours = (curr.timestamp - prev.timestamp).total_seconds() / 3600

            if prev.operating_status == OperatingStatus.OPERATING:
                operating_hours += interval_hours
                fuel_consumed += prev.fuel_rate * interval_hours
            elif prev.operating_status == OperatingStatus.IDLE:
                idle_hours += interval_hours
                fuel_consumed += prev.fuel_rate * interval_hours * 0.3  # Idle uses ~30% fuel

        off_hours = total_hours - operating_hours - idle_hours
        utilization_pct = (operating_hours / total_hours * 100) if total_hours > 0 else 0
        idle_pct = (idle_hours / (operating_hours + idle_hours) * 100) if (operating_hours + idle_hours) > 0 else 0
        fuel_efficiency = (fuel_consumed / operating_hours) if operating_hours > 0 else 0

        return UtilizationReport(
            equipment_id=equipment_id,
            period_start=start_date,
            period_end=end_date,
            total_hours=total_hours,
            operating_hours=operating_hours,
            idle_hours=idle_hours,
            off_hours=off_hours,
            utilization_pct=utilization_pct,
            idle_pct=idle_pct,
            fuel_consumed=fuel_consumed,
            fuel_efficiency=fuel_efficiency,
            cycles=0  # Would need load cycle detection
        )

    def get_fleet_summary(self) -> Dict:
        """Get summary of entire fleet."""
        summary = {
            "total_equipment": len(self.equipment),
            "by_status": {},
            "by_type": {},
            "active_faults": 0,
            "service_due": []
        }

        for equip in self.equipment.values():
            # Count by type
            eq_type = equip.equipment_type.value
            summary["by_type"][eq_type] = summary["by_type"].get(eq_type, 0) + 1

            # Get current status
            try:
                status = self.get_current_status(equip.id)
                op_status = status.get("status", "unknown")
                summary["by_status"][op_status] = summary["by_status"].get(op_status, 0) + 1

                # Check service due
                service_interval = self.SERVICE_INTERVALS.get(equip.equipment_type, 250)
                hours_to_service = equip.next_service_hours - equip.current_hours
                if hours_to_service < 50:
                    summary["service_due"].append({
                        "equipment": equip.name,
                        "hours_remaining": hours_to_service
                    })
            except Exception:
                summary["by_status"]["unknown"] = summary["by_status"].get("unknown", 0) + 1

        # Count active faults
        summary["active_faults"] = len([f for f in self.faults if not f.resolved])

        return summary

    def predict_maintenance(self, equipment_id: str) -> Dict:
        """Predict maintenance needs based on usage patterns."""
        if equipment_id not in self.equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")

        equip = self.equipment[equipment_id]

        # Calculate average daily hours
        week_ago = datetime.now() - timedelta(days=7)
        recent_readings = [r for r in self.readings
                         if r.equipment_id == equipment_id
                         and r.timestamp > week_ago]

        if len(recent_readings) < 2:
            return {"prediction": "insufficient_data"}

        hours_start = min(r.engine_hours for r in recent_readings)
        hours_end = max(r.engine_hours for r in recent_readings)
        days = (max(r.timestamp for r in recent_readings) -
                min(r.timestamp for r in recent_readings)).days or 1

        daily_hours = (hours_end - hours_start) / days

        # Predict service date
        service_interval = self.SERVICE_INTERVALS.get(equip.equipment_type, 250)
        hours_to_service = equip.next_service_hours - equip.current_hours

        if daily_hours > 0:
            days_to_service = hours_to_service / daily_hours
            service_date = datetime.now() + timedelta(days=days_to_service)
        else:
            service_date = None

        return {
            "equipment_id": equipment_id,
            "current_hours": equip.current_hours,
            "next_service_hours": equip.next_service_hours,
            "hours_to_service": hours_to_service,
            "avg_daily_hours": daily_hours,
            "predicted_service_date": service_date,
            "service_type": "Routine maintenance",
            "estimated_downtime_hours": 8
        }

    def generate_report(self) -> str:
        """Generate fleet telematics report."""
        summary = self.get_fleet_summary()

        lines = [
            "# Equipment Telematics Report",
            "",
            f"**Fleet:** {self.fleet_name}",
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Fleet Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Equipment | {summary['total_equipment']} |",
            f"| Active Faults | {summary['active_faults']} |",
            f"| Service Due | {len(summary['service_due'])} |",
            "",
            "## Status Distribution",
            ""
        ]

        for status, count in summary["by_status"].items():
            lines.append(f"- {status}: {count}")

        # Equipment details
        lines.extend([
            "",
            "## Equipment Status",
            "",
            "| Equipment | Type | Status | Hours | Fuel | Faults |",
            "|-----------|------|--------|-------|------|--------|"
        ])

        for equip in self.equipment.values():
            try:
                status = self.get_current_status(equip.id)
                status_icon = "✅" if status['status'] == 'operating' else "⏸️" if status['status'] == 'idle' else "⏹️"
                lines.append(
                    f"| {equip.name} | {equip.equipment_type.value} | "
                    f"{status_icon} {status['status']} | {status['engine_hours']:.0f} | "
                    f"{status['fuel_level']:.0f}% | {status['active_faults']} |"
                )
            except Exception:
                lines.append(
                    f"| {equip.name} | {equip.equipment_type.value} | ⚠️ No data | - | - | - |"
                )

        # Service due
        if summary["service_due"]:
            lines.extend([
                "",
                "## Service Due Soon",
                "",
                "| Equipment | Hours Remaining |",
                "|-----------|-----------------|"
            ])
            for svc in summary["service_due"]:
                lines.append(f"| {svc['equipment']} | {svc['hours_remaining']:.0f} |")

        # Active faults
        active_faults = [f for f in self.faults if not f.resolved]
        if active_faults:
            lines.extend([
                "",
                "## Active Faults",
                "",
                "| Equipment | Code | Description | Severity |",
                "|-----------|------|-------------|----------|"
            ])
            for fault in active_faults[:10]:
                sev_icon = "🔴" if fault.severity == FaultSeverity.CRITICAL else "🟡"
                equip = self.equipment.get(fault.equipment_id)
                lines.append(
                    f"| {equip.name if equip else fault.equipment_id} | "
                    f"{fault.code} | {fault.description} | {sev_icon} {fault.severity.value} |"
                )

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize telematics system
telematics = EquipmentTelematics("Site A Fleet")

# Register equipment
telematics.register_equipment(
    "EX-001", "Excavator #1", EquipmentType.EXCAVATOR,
    make="Caterpillar", model="320", year=2022,
    serial_number="CAT320X12345",
    hourly_rate=150, fuel_capacity=400
)

telematics.register_equipment(
    "CR-001", "Tower Crane #1", EquipmentType.CRANE,
    make="Liebherr", model="200EC-H", year=2021,
    serial_number="LH200EC54321",
    hourly_rate=200, fuel_capacity=300
)

# Add geofence for site boundary
telematics.add_geofence(
    "SITE-A", "Site A Boundary",
    center_lat=40.7128, center_lon=-74.0060,
    radius_meters=500
)

# Ingest telematics reading
location = GPSLocation(
    latitude=40.7128, longitude=-74.0059,
    speed=5.0, timestamp=datetime.now()
)

telematics.ingest_reading(
    "EX-001", location,
    engine_hours=1250.5,
    fuel_level=65.0,
    fuel_rate=18.5,
    engine_rpm=1800,
    hydraulic_temp=75.0,
    coolant_temp=85.0,
    load_percentage=75,
    operator_id="OP-101"
)

# Get current status
status = telematics.get_current_status("EX-001")
print(f"Excavator status: {status['status']}")
print(f"Location: {status['location']}")
print(f"Fuel: {status['fuel_level']}%")

# Calculate utilization
util = telematics.calculate_utilization(
    "EX-001",
    datetime.now() - timedelta(days=7),
    datetime.now()
)
if util:
    print(f"Utilization: {util.utilization_pct:.1f}%")
    print(f"Fuel efficiency: {util.fuel_efficiency:.1f} L/hr")

# Predict maintenance
maintenance = telematics.predict_maintenance("EX-001")
print(f"Days to service: {maintenance.get('predicted_service_date')}")

# Fleet summary
summary = telematics.get_fleet_summary()
print(f"Fleet: {summary['total_equipment']} units")

# Generate report
print(telematics.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
