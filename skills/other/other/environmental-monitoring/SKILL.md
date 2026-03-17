---
name: "environmental-monitoring"
description: "Monitor environmental conditions on construction sites. Track air quality, noise levels, vibration, dust, and weather to ensure compliance and worker safety."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Environmental Monitoring

## Overview

Monitor and analyze environmental conditions on construction sites including air quality, noise, vibration, dust, and weather. Support regulatory compliance, worker safety, and community relations through real-time environmental tracking.

## Environmental Monitoring System

```
┌─────────────────────────────────────────────────────────────────┐
│                ENVIRONMENTAL MONITORING                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SENSORS                   MONITORING            COMPLIANCE     │
│  ───────                   ──────────            ──────────     │
│                                                                  │
│  💨 Air Quality  ───┐                            ✅ OSHA limits  │
│  🔊 Noise Level  ───┼─────→ Real-time   ────────→ ✅ EPA limits  │
│  📊 Vibration    ───┤       Dashboard            ✅ Local codes │
│  🌫️ Dust/PM     ───┤       Alerts               ✅ Permits     │
│  🌡️ Weather     ───┘       Reports              ✅ Neighbors   │
│                                                                  │
│  THRESHOLDS:                                                    │
│  • Noise: 85 dB (OSHA 8hr TWA)                                 │
│  • PM2.5: 35 µg/m³ (EPA 24hr)                                  │
│  • Vibration: 25 mm/s (structural)                             │
│  • CO: 50 ppm (OSHA ceiling)                                   │
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

class ParameterType(Enum):
    NOISE = "noise"
    PM25 = "pm25"
    PM10 = "pm10"
    CO = "co"
    CO2 = "co2"
    VOC = "voc"
    VIBRATION = "vibration"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    WIND_DIRECTION = "wind_direction"
    RAINFALL = "rainfall"

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    EXCEEDANCE = "exceedance"
    CRITICAL = "critical"

class AlertType(Enum):
    THRESHOLD_WARNING = "threshold_warning"
    THRESHOLD_EXCEEDANCE = "threshold_exceedance"
    EQUIPMENT_MALFUNCTION = "equipment_malfunction"
    WEATHER_ALERT = "weather_alert"
    COMMUNITY_COMPLAINT = "community_complaint"

@dataclass
class RegulatoryLimit:
    parameter: ParameterType
    limit_value: float
    unit: str
    averaging_period_hours: float  # e.g., 8 for 8-hour TWA
    regulation: str  # e.g., "OSHA", "EPA"
    description: str

@dataclass
class EnvironmentalReading:
    station_id: str
    parameter: ParameterType
    timestamp: datetime
    value: float
    unit: str
    quality_flag: str = "valid"

@dataclass
class MonitoringStation:
    id: str
    name: str
    location: Dict  # {lat, lon, description}
    parameters: List[ParameterType]
    installation_date: datetime
    last_calibration: datetime
    status: str = "active"

@dataclass
class ComplianceRecord:
    parameter: ParameterType
    regulation: str
    limit_value: float
    measured_value: float
    averaging_period: str
    status: ComplianceStatus
    timestamp: datetime
    location: str

@dataclass
class EnvironmentalAlert:
    id: str
    alert_type: AlertType
    parameter: ParameterType
    station_id: str
    timestamp: datetime
    value: float
    threshold: float
    message: str
    acknowledged: bool = False
    resolved: bool = False
    resolution_notes: str = ""

@dataclass
class DailyReport:
    date: datetime
    site_name: str
    parameters_monitored: int
    readings_collected: int
    exceedances: int
    alerts_triggered: int
    compliance_status: ComplianceStatus
    summary: Dict[str, Dict]

class EnvironmentalMonitor:
    """Monitor environmental conditions on construction sites."""

    # Default regulatory limits
    REGULATORY_LIMITS = {
        ParameterType.NOISE: [
            RegulatoryLimit(ParameterType.NOISE, 85, "dBA", 8.0, "OSHA", "8-hour TWA"),
            RegulatoryLimit(ParameterType.NOISE, 90, "dBA", 8.0, "OSHA", "Action level"),
            RegulatoryLimit(ParameterType.NOISE, 115, "dBA", 0.25, "OSHA", "15-min max"),
        ],
        ParameterType.PM25: [
            RegulatoryLimit(ParameterType.PM25, 35, "µg/m³", 24.0, "EPA", "24-hour standard"),
            RegulatoryLimit(ParameterType.PM25, 12, "µg/m³", 8760.0, "EPA", "Annual standard"),
        ],
        ParameterType.PM10: [
            RegulatoryLimit(ParameterType.PM10, 150, "µg/m³", 24.0, "EPA", "24-hour standard"),
        ],
        ParameterType.CO: [
            RegulatoryLimit(ParameterType.CO, 50, "ppm", 0.0, "OSHA", "Ceiling limit"),
            RegulatoryLimit(ParameterType.CO, 35, "ppm", 8.0, "OSHA", "8-hour TWA"),
        ],
        ParameterType.VIBRATION: [
            RegulatoryLimit(ParameterType.VIBRATION, 25, "mm/s", 0.0, "ISO 4866", "Structural damage threshold"),
            RegulatoryLimit(ParameterType.VIBRATION, 5, "mm/s", 0.0, "DIN 4150", "Sensitive structures"),
        ],
    }

    def __init__(self, site_name: str):
        self.site_name = site_name
        self.stations: Dict[str, MonitoringStation] = {}
        self.readings: List[EnvironmentalReading] = []
        self.alerts: List[EnvironmentalAlert] = []
        self.custom_limits: Dict[ParameterType, List[RegulatoryLimit]] = {}

    def add_station(self, id: str, name: str, location: Dict,
                   parameters: List[ParameterType]) -> MonitoringStation:
        """Add monitoring station."""
        station = MonitoringStation(
            id=id,
            name=name,
            location=location,
            parameters=parameters,
            installation_date=datetime.now(),
            last_calibration=datetime.now()
        )
        self.stations[id] = station
        return station

    def add_custom_limit(self, parameter: ParameterType, limit_value: float,
                        unit: str, averaging_hours: float, regulation: str,
                        description: str):
        """Add custom regulatory limit."""
        limit = RegulatoryLimit(
            parameter=parameter,
            limit_value=limit_value,
            unit=unit,
            averaging_period_hours=averaging_hours,
            regulation=regulation,
            description=description
        )
        if parameter not in self.custom_limits:
            self.custom_limits[parameter] = []
        self.custom_limits[parameter].append(limit)

    def record_reading(self, station_id: str, parameter: ParameterType,
                      value: float, unit: str,
                      timestamp: datetime = None) -> EnvironmentalReading:
        """Record environmental reading."""
        if station_id not in self.stations:
            raise ValueError(f"Unknown station: {station_id}")

        reading = EnvironmentalReading(
            station_id=station_id,
            parameter=parameter,
            timestamp=timestamp or datetime.now(),
            value=value,
            unit=unit
        )

        self.readings.append(reading)

        # Check against limits
        self._check_limits(station_id, parameter, value)

        return reading

    def record_batch(self, readings: List[Dict]) -> int:
        """Record multiple readings."""
        count = 0
        for r in readings:
            try:
                self.record_reading(
                    station_id=r['station_id'],
                    parameter=ParameterType(r['parameter']),
                    value=r['value'],
                    unit=r['unit'],
                    timestamp=r.get('timestamp')
                )
                count += 1
            except Exception:
                pass
        return count

    def _check_limits(self, station_id: str, parameter: ParameterType, value: float):
        """Check value against regulatory limits."""
        # Get applicable limits
        limits = self.REGULATORY_LIMITS.get(parameter, [])
        limits.extend(self.custom_limits.get(parameter, []))

        for limit in limits:
            if limit.averaging_period_hours == 0:
                # Instantaneous limit
                check_value = value
            else:
                # Time-weighted average
                check_value = self._calculate_twa(
                    station_id, parameter, limit.averaging_period_hours
                )
                if check_value is None:
                    continue

            # Check against limit
            if check_value >= limit.limit_value:
                self._create_alert(
                    station_id, parameter, check_value, limit
                )
            elif check_value >= limit.limit_value * 0.8:
                # Warning at 80% of limit
                self._create_alert(
                    station_id, parameter, check_value, limit,
                    is_warning=True
                )

    def _calculate_twa(self, station_id: str, parameter: ParameterType,
                      hours: float) -> Optional[float]:
        """Calculate time-weighted average."""
        cutoff = datetime.now() - timedelta(hours=hours)
        readings = [r for r in self.readings
                   if r.station_id == station_id
                   and r.parameter == parameter
                   and r.timestamp > cutoff]

        if not readings:
            return None

        return statistics.mean([r.value for r in readings])

    def _create_alert(self, station_id: str, parameter: ParameterType,
                     value: float, limit: RegulatoryLimit,
                     is_warning: bool = False):
        """Create environmental alert."""
        # Avoid duplicate alerts
        recent_alerts = [a for a in self.alerts
                        if a.station_id == station_id
                        and a.parameter == parameter
                        and not a.resolved
                        and (datetime.now() - a.timestamp).total_seconds() < 3600]

        if recent_alerts:
            return

        alert_type = (AlertType.THRESHOLD_WARNING if is_warning
                     else AlertType.THRESHOLD_EXCEEDANCE)

        station = self.stations.get(station_id)

        alert = EnvironmentalAlert(
            id=f"ENV-{len(self.alerts)+1:05d}",
            alert_type=alert_type,
            parameter=parameter,
            station_id=station_id,
            timestamp=datetime.now(),
            value=value,
            threshold=limit.limit_value,
            message=f"{parameter.value} {'approaching' if is_warning else 'exceeds'} "
                    f"{limit.regulation} limit ({limit.limit_value} {limit.unit}) "
                    f"at {station.name if station else station_id}"
        )

        self.alerts.append(alert)

    def get_current_conditions(self, station_id: str = None) -> Dict:
        """Get current environmental conditions."""
        conditions = {}

        stations = ([self.stations[station_id]] if station_id
                   else self.stations.values())

        for station in stations:
            station_conditions = {}

            for param in station.parameters:
                # Get latest reading
                readings = [r for r in self.readings
                           if r.station_id == station.id
                           and r.parameter == param]

                if readings:
                    latest = max(readings, key=lambda r: r.timestamp)
                    station_conditions[param.value] = {
                        "value": latest.value,
                        "unit": latest.unit,
                        "timestamp": latest.timestamp,
                        "status": self._get_compliance_status(param, latest.value)
                    }

            conditions[station.id] = {
                "name": station.name,
                "location": station.location,
                "parameters": station_conditions
            }

        return conditions

    def _get_compliance_status(self, parameter: ParameterType,
                              value: float) -> ComplianceStatus:
        """Determine compliance status for value."""
        limits = self.REGULATORY_LIMITS.get(parameter, [])
        limits.extend(self.custom_limits.get(parameter, []))

        # Check instantaneous limits
        instant_limits = [l for l in limits if l.averaging_period_hours == 0]
        for limit in instant_limits:
            if value >= limit.limit_value:
                return ComplianceStatus.EXCEEDANCE
            elif value >= limit.limit_value * 0.9:
                return ComplianceStatus.WARNING

        return ComplianceStatus.COMPLIANT

    def check_compliance(self, start_date: datetime,
                        end_date: datetime) -> List[ComplianceRecord]:
        """Check compliance for period."""
        records = []

        for station in self.stations.values():
            for param in station.parameters:
                limits = self.REGULATORY_LIMITS.get(param, [])
                limits.extend(self.custom_limits.get(param, []))

                for limit in limits:
                    # Calculate average for period
                    readings = [r for r in self.readings
                               if r.station_id == station.id
                               and r.parameter == param
                               and start_date <= r.timestamp <= end_date]

                    if not readings:
                        continue

                    avg_value = statistics.mean([r.value for r in readings])
                    max_value = max(r.value for r in readings)

                    # Check appropriate value
                    if limit.averaging_period_hours == 0:
                        check_value = max_value
                        period_str = "Instantaneous"
                    else:
                        check_value = avg_value
                        period_str = f"{limit.averaging_period_hours:.0f}-hour avg"

                    # Determine status
                    if check_value >= limit.limit_value:
                        status = ComplianceStatus.EXCEEDANCE
                    elif check_value >= limit.limit_value * 0.9:
                        status = ComplianceStatus.WARNING
                    else:
                        status = ComplianceStatus.COMPLIANT

                    records.append(ComplianceRecord(
                        parameter=param,
                        regulation=limit.regulation,
                        limit_value=limit.limit_value,
                        measured_value=check_value,
                        averaging_period=period_str,
                        status=status,
                        timestamp=end_date,
                        location=station.name
                    ))

        return records

    def get_exceedance_summary(self, days: int = 30) -> Dict:
        """Get summary of exceedances."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_alerts = [a for a in self.alerts
                       if a.timestamp > cutoff
                       and a.alert_type == AlertType.THRESHOLD_EXCEEDANCE]

        summary = {
            "period_days": days,
            "total_exceedances": len(recent_alerts),
            "by_parameter": {},
            "by_station": {},
            "recent_events": []
        }

        for alert in recent_alerts:
            # By parameter
            param = alert.parameter.value
            summary["by_parameter"][param] = summary["by_parameter"].get(param, 0) + 1

            # By station
            station = alert.station_id
            summary["by_station"][station] = summary["by_station"].get(station, 0) + 1

        # Recent events
        summary["recent_events"] = sorted(
            recent_alerts, key=lambda a: a.timestamp, reverse=True
        )[:10]

        return summary

    def generate_daily_report(self, date: datetime = None) -> DailyReport:
        """Generate daily environmental report."""
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        next_day = date + timedelta(days=1)

        # Filter readings
        day_readings = [r for r in self.readings
                       if date <= r.timestamp < next_day]

        # Filter alerts
        day_alerts = [a for a in self.alerts
                     if date <= a.timestamp < next_day]

        # Check compliance
        compliance_records = self.check_compliance(date, next_day)
        exceedances = [r for r in compliance_records
                      if r.status == ComplianceStatus.EXCEEDANCE]

        # Overall status
        if exceedances:
            overall_status = ComplianceStatus.EXCEEDANCE
        elif any(r.status == ComplianceStatus.WARNING for r in compliance_records):
            overall_status = ComplianceStatus.WARNING
        else:
            overall_status = ComplianceStatus.COMPLIANT

        # Summary by parameter
        param_summary = {}
        for param in ParameterType:
            param_readings = [r for r in day_readings if r.parameter == param]
            if param_readings:
                values = [r.value for r in param_readings]
                param_summary[param.value] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": statistics.mean(values),
                    "exceedances": len([r for r in compliance_records
                                       if r.parameter == param
                                       and r.status == ComplianceStatus.EXCEEDANCE])
                }

        return DailyReport(
            date=date,
            site_name=self.site_name,
            parameters_monitored=len(set(r.parameter for r in day_readings)),
            readings_collected=len(day_readings),
            exceedances=len(exceedances),
            alerts_triggered=len(day_alerts),
            compliance_status=overall_status,
            summary=param_summary
        )

    def generate_report(self) -> str:
        """Generate environmental monitoring report."""
        lines = [
            "# Environmental Monitoring Report",
            "",
            f"**Site:** {self.site_name}",
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Monitoring Stations",
            "",
            "| Station | Location | Parameters | Status |",
            "|---------|----------|------------|--------|"
        ]

        for station in self.stations.values():
            params = ", ".join([p.value for p in station.parameters])
            lines.append(
                f"| {station.name} | {station.location.get('description', '-')} | "
                f"{params} | {station.status} |"
            )

        # Current conditions
        conditions = self.get_current_conditions()
        lines.extend([
            "",
            "## Current Conditions",
            ""
        ])

        for station_id, data in conditions.items():
            lines.append(f"### {data['name']}")
            lines.append("")
            lines.append("| Parameter | Value | Status |")
            lines.append("|-----------|-------|--------|")

            for param, values in data['parameters'].items():
                status_icon = ("✅" if values['status'] == ComplianceStatus.COMPLIANT
                              else "⚠️" if values['status'] == ComplianceStatus.WARNING
                              else "🔴")
                lines.append(
                    f"| {param} | {values['value']:.1f} {values['unit']} | "
                    f"{status_icon} {values['status'].value} |"
                )

            lines.append("")

        # Exceedance summary
        exceedance_summary = self.get_exceedance_summary(30)
        lines.extend([
            "## 30-Day Exceedance Summary",
            "",
            f"**Total Exceedances:** {exceedance_summary['total_exceedances']}",
            ""
        ])

        if exceedance_summary['by_parameter']:
            lines.append("By Parameter:")
            for param, count in exceedance_summary['by_parameter'].items():
                lines.append(f"- {param}: {count}")

        # Active alerts
        active_alerts = [a for a in self.alerts if not a.resolved]
        if active_alerts:
            lines.extend([
                "",
                f"## Active Alerts ({len(active_alerts)})",
                "",
                "| Time | Parameter | Station | Value | Threshold |",
                "|------|-----------|---------|-------|-----------|"
            ])

            for alert in sorted(active_alerts, key=lambda a: a.timestamp, reverse=True)[:10]:
                lines.append(
                    f"| {alert.timestamp.strftime('%Y-%m-%d %H:%M')} | "
                    f"{alert.parameter.value} | {alert.station_id} | "
                    f"{alert.value:.1f} | {alert.threshold} |"
                )

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize monitor
monitor = EnvironmentalMonitor("Downtown Construction Site")

# Add monitoring stations
monitor.add_station(
    "STA-001", "North Perimeter",
    location={"lat": 40.7128, "lon": -74.0060, "description": "North fence line"},
    parameters=[ParameterType.NOISE, ParameterType.PM25, ParameterType.PM10]
)

monitor.add_station(
    "STA-002", "Equipment Area",
    location={"lat": 40.7125, "lon": -74.0055, "description": "Near excavation"},
    parameters=[ParameterType.NOISE, ParameterType.VIBRATION, ParameterType.CO]
)

# Add custom limit for local ordinance
monitor.add_custom_limit(
    ParameterType.NOISE, 65, "dBA", 0,
    "Local Ordinance", "Residential boundary limit"
)

# Record readings
monitor.record_reading("STA-001", ParameterType.NOISE, 78.5, "dBA")
monitor.record_reading("STA-001", ParameterType.PM25, 28.3, "µg/m³")
monitor.record_reading("STA-002", ParameterType.VIBRATION, 8.2, "mm/s")

# Batch record
readings = [
    {"station_id": "STA-001", "parameter": "noise", "value": 82.0, "unit": "dBA"},
    {"station_id": "STA-001", "parameter": "pm25", "value": 31.5, "unit": "µg/m³"},
    {"station_id": "STA-002", "parameter": "noise", "value": 88.0, "unit": "dBA"}
]
monitor.record_batch(readings)

# Get current conditions
conditions = monitor.get_current_conditions()
for station, data in conditions.items():
    print(f"\n{data['name']}:")
    for param, values in data['parameters'].items():
        print(f"  {param}: {values['value']} {values['unit']} - {values['status'].value}")

# Check compliance
compliance = monitor.check_compliance(
    datetime.now() - timedelta(days=1),
    datetime.now()
)
for record in compliance:
    if record.status != ComplianceStatus.COMPLIANT:
        print(f"⚠️ {record.parameter.value}: {record.measured_value} vs limit {record.limit_value}")

# Generate daily report
report = monitor.generate_daily_report()
print(f"\nDaily Status: {report.compliance_status.value}")
print(f"Exceedances: {report.exceedances}")

# Full report
print(monitor.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
