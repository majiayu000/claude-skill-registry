---
name: "sensor-data-aggregator"
description: "Aggregate and analyze IoT sensor data from construction sites. Collect data from multiple sensor types, detect anomalies, and trigger alerts for safety and quality monitoring."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Sensor Data Aggregator

## Overview

Collect, aggregate, and analyze data from IoT sensors deployed across construction sites. Support real-time monitoring of environmental conditions, equipment status, structural integrity, and worker safety through unified data processing.

## IoT Sensor Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  SENSOR DATA AGGREGATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SENSORS                    AGGREGATOR            OUTPUTS       │
│  ───────                    ──────────            ───────       │
│                                                                  │
│  🌡️ Temperature  ─────┐                          📊 Dashboard   │
│  💧 Humidity     ─────┤    ┌──────────────┐      ⚠️ Alerts      │
│  📊 Vibration    ─────┼───→│  AGGREGATE   │───→  📈 Analytics   │
│  🔊 Noise        ─────┤    │  PROCESS     │      📋 Reports     │
│  💨 Air Quality  ─────┤    │  ANALYZE     │      🔄 API         │
│  📍 Location     ─────┘    └──────────────┘                     │
│                                                                  │
│  DATA FLOW:                                                     │
│  Raw → Validate → Transform → Store → Analyze → Alert          │
│                                                                  │
│  ANALYSIS:                                                      │
│  • Real-time monitoring                                         │
│  • Trend detection                                              │
│  • Anomaly identification                                       │
│  • Threshold alerting                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import json

class SensorType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    VIBRATION = "vibration"
    NOISE = "noise"
    AIR_QUALITY = "air_quality"
    DUST = "dust"
    GAS = "gas"
    PRESSURE = "pressure"
    STRAIN = "strain"
    TILT = "tilt"
    GPS = "gps"
    PROXIMITY = "proximity"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class DataQuality(Enum):
    GOOD = "good"
    SUSPECT = "suspect"
    BAD = "bad"
    MISSING = "missing"

@dataclass
class SensorReading:
    sensor_id: str
    sensor_type: SensorType
    timestamp: datetime
    value: float
    unit: str
    quality: DataQuality = DataQuality.GOOD
    location: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class Sensor:
    id: str
    name: str
    sensor_type: SensorType
    unit: str
    location: Dict  # {zone, floor, coordinates}
    thresholds: Dict  # {warning, critical, min, max}
    calibration_date: datetime
    battery_level: float = 100.0
    status: str = "active"

@dataclass
class Alert:
    id: str
    sensor_id: str
    sensor_type: SensorType
    severity: AlertSeverity
    timestamp: datetime
    value: float
    threshold: float
    message: str
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class AggregatedMetric:
    sensor_type: SensorType
    period_start: datetime
    period_end: datetime
    readings_count: int
    min_value: float
    max_value: float
    avg_value: float
    std_dev: float
    alerts_triggered: int

class SensorDataAggregator:
    """Aggregate and analyze IoT sensor data."""

    # Default thresholds by sensor type
    DEFAULT_THRESHOLDS = {
        SensorType.TEMPERATURE: {"warning": 35, "critical": 40, "unit": "°C"},
        SensorType.HUMIDITY: {"warning": 80, "critical": 90, "unit": "%"},
        SensorType.VIBRATION: {"warning": 10, "critical": 25, "unit": "mm/s"},
        SensorType.NOISE: {"warning": 85, "critical": 100, "unit": "dB"},
        SensorType.AIR_QUALITY: {"warning": 100, "critical": 150, "unit": "AQI"},
        SensorType.DUST: {"warning": 3, "critical": 10, "unit": "mg/m³"},
        SensorType.GAS: {"warning": 20, "critical": 50, "unit": "ppm"},
    }

    def __init__(self, site_name: str):
        self.site_name = site_name
        self.sensors: Dict[str, Sensor] = {}
        self.readings: List[SensorReading] = []
        self.alerts: List[Alert] = []
        self.alert_handlers: List[Callable] = []

    def register_sensor(self, id: str, name: str, sensor_type: SensorType,
                       unit: str, location: Dict,
                       thresholds: Dict = None) -> Sensor:
        """Register a new sensor."""
        if thresholds is None:
            thresholds = self.DEFAULT_THRESHOLDS.get(sensor_type, {})

        sensor = Sensor(
            id=id,
            name=name,
            sensor_type=sensor_type,
            unit=unit,
            location=location,
            thresholds=thresholds,
            calibration_date=datetime.now()
        )
        self.sensors[id] = sensor
        return sensor

    def ingest_reading(self, sensor_id: str, value: float,
                      timestamp: datetime = None,
                      metadata: Dict = None) -> SensorReading:
        """Ingest a sensor reading."""
        if sensor_id not in self.sensors:
            raise ValueError(f"Unknown sensor: {sensor_id}")

        sensor = self.sensors[sensor_id]

        # Validate data quality
        quality = self._validate_reading(sensor, value)

        reading = SensorReading(
            sensor_id=sensor_id,
            sensor_type=sensor.sensor_type,
            timestamp=timestamp or datetime.now(),
            value=value,
            unit=sensor.unit,
            quality=quality,
            location=sensor.location,
            metadata=metadata or {}
        )

        self.readings.append(reading)

        # Check thresholds
        if quality == DataQuality.GOOD:
            self._check_thresholds(sensor, reading)

        return reading

    def ingest_batch(self, readings: List[Dict]) -> int:
        """Ingest multiple readings at once."""
        count = 0
        for r in readings:
            try:
                self.ingest_reading(
                    sensor_id=r['sensor_id'],
                    value=r['value'],
                    timestamp=r.get('timestamp', datetime.now()),
                    metadata=r.get('metadata')
                )
                count += 1
            except Exception:
                pass  # Log error but continue
        return count

    def _validate_reading(self, sensor: Sensor, value: float) -> DataQuality:
        """Validate reading quality."""
        thresholds = sensor.thresholds

        # Check if value is within physical limits
        if 'min' in thresholds and value < thresholds['min']:
            return DataQuality.SUSPECT
        if 'max' in thresholds and value > thresholds['max']:
            return DataQuality.SUSPECT

        # Check for sudden spikes (compare with recent readings)
        recent = self.get_recent_readings(sensor.id, minutes=5)
        if len(recent) >= 3:
            avg = statistics.mean([r.value for r in recent])
            if abs(value - avg) > avg * 0.5:  # 50% deviation
                return DataQuality.SUSPECT

        return DataQuality.GOOD

    def _check_thresholds(self, sensor: Sensor, reading: SensorReading):
        """Check if reading exceeds thresholds."""
        thresholds = sensor.thresholds

        if 'critical' in thresholds and reading.value >= thresholds['critical']:
            self._create_alert(sensor, reading, AlertSeverity.CRITICAL)
        elif 'warning' in thresholds and reading.value >= thresholds['warning']:
            self._create_alert(sensor, reading, AlertSeverity.WARNING)

    def _create_alert(self, sensor: Sensor, reading: SensorReading,
                     severity: AlertSeverity):
        """Create and dispatch alert."""
        threshold = sensor.thresholds.get(severity.value, 0)

        alert = Alert(
            id=f"ALERT-{len(self.alerts)+1:06d}",
            sensor_id=sensor.id,
            sensor_type=sensor.sensor_type,
            severity=severity,
            timestamp=reading.timestamp,
            value=reading.value,
            threshold=threshold,
            message=f"{sensor.name}: {reading.value} {reading.unit} exceeds {severity.value} threshold ({threshold})"
        )

        self.alerts.append(alert)

        # Dispatch to handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception:
                pass

    def register_alert_handler(self, handler: Callable):
        """Register alert callback handler."""
        self.alert_handlers.append(handler)

    def get_recent_readings(self, sensor_id: str,
                           minutes: int = 60) -> List[SensorReading]:
        """Get recent readings for sensor."""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [r for r in self.readings
                if r.sensor_id == sensor_id and r.timestamp > cutoff]

    def get_readings_by_type(self, sensor_type: SensorType,
                            start: datetime = None,
                            end: datetime = None) -> List[SensorReading]:
        """Get readings by sensor type."""
        readings = [r for r in self.readings if r.sensor_type == sensor_type]

        if start:
            readings = [r for r in readings if r.timestamp >= start]
        if end:
            readings = [r for r in readings if r.timestamp <= end]

        return readings

    def aggregate_by_period(self, sensor_type: SensorType,
                           period_minutes: int = 60) -> List[AggregatedMetric]:
        """Aggregate readings into time periods."""
        readings = self.get_readings_by_type(sensor_type)

        if not readings:
            return []

        # Group by period
        periods: Dict[datetime, List[SensorReading]] = {}
        for r in readings:
            # Round to period start
            period_start = r.timestamp.replace(
                minute=(r.timestamp.minute // period_minutes) * period_minutes,
                second=0,
                microsecond=0
            )
            if period_start not in periods:
                periods[period_start] = []
            periods[period_start].append(r)

        # Calculate aggregates
        aggregates = []
        for period_start, period_readings in sorted(periods.items()):
            values = [r.value for r in period_readings]

            # Count alerts in period
            period_end = period_start + timedelta(minutes=period_minutes)
            period_alerts = len([a for a in self.alerts
                                if a.sensor_type == sensor_type
                                and period_start <= a.timestamp < period_end])

            aggregates.append(AggregatedMetric(
                sensor_type=sensor_type,
                period_start=period_start,
                period_end=period_end,
                readings_count=len(values),
                min_value=min(values),
                max_value=max(values),
                avg_value=statistics.mean(values),
                std_dev=statistics.stdev(values) if len(values) > 1 else 0,
                alerts_triggered=period_alerts
            ))

        return aggregates

    def detect_anomalies(self, sensor_id: str,
                        lookback_hours: int = 24) -> List[Dict]:
        """Detect anomalies in sensor data."""
        cutoff = datetime.now() - timedelta(hours=lookback_hours)
        readings = [r for r in self.readings
                   if r.sensor_id == sensor_id and r.timestamp > cutoff]

        if len(readings) < 10:
            return []

        values = [r.value for r in readings]
        avg = statistics.mean(values)
        std = statistics.stdev(values)

        anomalies = []
        for r in readings:
            # Z-score based anomaly detection
            if std > 0:
                z_score = abs(r.value - avg) / std
                if z_score > 3:  # 3 standard deviations
                    anomalies.append({
                        "timestamp": r.timestamp,
                        "value": r.value,
                        "expected": avg,
                        "z_score": z_score,
                        "type": "statistical_outlier"
                    })

        return anomalies

    def get_sensor_health(self) -> List[Dict]:
        """Get health status of all sensors."""
        health = []
        now = datetime.now()

        for sensor in self.sensors.values():
            recent = self.get_recent_readings(sensor.id, minutes=30)

            # Determine status
            if not recent:
                status = "offline"
            elif sensor.battery_level < 20:
                status = "low_battery"
            elif any(r.quality != DataQuality.GOOD for r in recent[-5:]):
                status = "degraded"
            else:
                status = "healthy"

            health.append({
                "sensor_id": sensor.id,
                "sensor_name": sensor.name,
                "type": sensor.sensor_type.value,
                "status": status,
                "battery": sensor.battery_level,
                "last_reading": recent[-1].timestamp if recent else None,
                "readings_30min": len(recent)
            })

        return sorted(health, key=lambda x: x['status'] != 'healthy', reverse=True)

    def get_zone_summary(self, zone: str) -> Dict:
        """Get summary for specific zone."""
        zone_sensors = [s for s in self.sensors.values()
                       if s.location.get('zone') == zone]

        if not zone_sensors:
            return {"zone": zone, "error": "No sensors in zone"}

        summary = {
            "zone": zone,
            "sensor_count": len(zone_sensors),
            "by_type": {}
        }

        for sensor in zone_sensors:
            recent = self.get_recent_readings(sensor.id, minutes=15)
            if not recent:
                continue

            values = [r.value for r in recent]
            sensor_type = sensor.sensor_type.value

            if sensor_type not in summary["by_type"]:
                summary["by_type"][sensor_type] = {
                    "current": values[-1] if values else None,
                    "avg": statistics.mean(values) if values else None,
                    "unit": sensor.unit,
                    "status": "normal"
                }

                # Check status
                thresholds = sensor.thresholds
                current = values[-1]
                if 'critical' in thresholds and current >= thresholds['critical']:
                    summary["by_type"][sensor_type]["status"] = "critical"
                elif 'warning' in thresholds and current >= thresholds['warning']:
                    summary["by_type"][sensor_type]["status"] = "warning"

        return summary

    def generate_report(self) -> str:
        """Generate sensor data report."""
        lines = [
            "# Sensor Data Report",
            "",
            f"**Site:** {self.site_name}",
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Sensor Inventory",
            "",
            f"| Sensor | Type | Location | Status |",
            f"|--------|------|----------|--------|"
        ]

        health = self.get_sensor_health()
        for h in health:
            status_icon = "✅" if h['status'] == 'healthy' else "⚠️" if h['status'] == 'degraded' else "🔴"
            lines.append(
                f"| {h['sensor_name']} | {h['type']} | - | {status_icon} {h['status']} |"
            )

        # Recent alerts
        recent_alerts = [a for a in self.alerts
                       if a.timestamp > datetime.now() - timedelta(hours=24)]

        if recent_alerts:
            lines.extend([
                "",
                f"## Alerts (Last 24h) - {len(recent_alerts)} total",
                "",
                "| Time | Sensor | Severity | Value | Threshold |",
                "|------|--------|----------|-------|-----------|"
            ])

            for alert in sorted(recent_alerts, key=lambda x: x.timestamp, reverse=True)[:20]:
                sev_icon = "🔴" if alert.severity == AlertSeverity.CRITICAL else "🟡"
                lines.append(
                    f"| {alert.timestamp.strftime('%H:%M')} | {alert.sensor_id} | "
                    f"{sev_icon} {alert.severity.value} | {alert.value:.1f} | {alert.threshold} |"
                )

        # Current readings by type
        lines.extend([
            "",
            "## Current Readings by Type",
            ""
        ])

        for sensor_type in SensorType:
            readings = self.get_readings_by_type(sensor_type)
            if not readings:
                continue

            recent = [r for r in readings
                     if r.timestamp > datetime.now() - timedelta(minutes=15)]
            if not recent:
                continue

            values = [r.value for r in recent]
            lines.append(
                f"**{sensor_type.value}**: "
                f"Avg={statistics.mean(values):.1f}, "
                f"Min={min(values):.1f}, "
                f"Max={max(values):.1f}"
            )

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize aggregator
aggregator = SensorDataAggregator("Construction Site A")

# Register sensors
aggregator.register_sensor(
    "TEMP-001", "Zone A Temperature",
    SensorType.TEMPERATURE, "°C",
    location={"zone": "A", "floor": 1, "x": 10, "y": 20},
    thresholds={"warning": 32, "critical": 38, "min": -10, "max": 50}
)

aggregator.register_sensor(
    "VIB-001", "Foundation Vibration",
    SensorType.VIBRATION, "mm/s",
    location={"zone": "Foundation", "floor": 0}
)

aggregator.register_sensor(
    "DUST-001", "Dust Monitor",
    SensorType.DUST, "mg/m³",
    location={"zone": "A", "floor": 1}
)

# Register alert handler
def handle_alert(alert):
    print(f"ALERT: {alert.severity.value} - {alert.message}")

aggregator.register_alert_handler(handle_alert)

# Ingest readings
aggregator.ingest_reading("TEMP-001", 28.5)
aggregator.ingest_reading("TEMP-001", 33.0)  # Warning!
aggregator.ingest_reading("VIB-001", 5.2)
aggregator.ingest_reading("DUST-001", 2.1)

# Batch ingest
readings = [
    {"sensor_id": "TEMP-001", "value": 29.0},
    {"sensor_id": "VIB-001", "value": 4.8},
    {"sensor_id": "DUST-001", "value": 2.5}
]
aggregator.ingest_batch(readings)

# Check sensor health
health = aggregator.get_sensor_health()
for h in health:
    print(f"{h['sensor_name']}: {h['status']}")

# Get zone summary
summary = aggregator.get_zone_summary("A")
print(f"Zone A: {summary}")

# Detect anomalies
anomalies = aggregator.detect_anomalies("TEMP-001")
print(f"Anomalies found: {len(anomalies)}")

# Generate report
print(aggregator.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
