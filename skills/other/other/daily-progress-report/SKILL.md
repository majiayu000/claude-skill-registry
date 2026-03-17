---
slug: "daily-progress-report"
display_name: "Daily Progress Report"
description: "Generate automated daily progress reports from site data. Track work completed, labor hours, equipment usage, and weather conditions."
---

# Daily Progress Report Generator

## Business Case

### Problem Statement
Site managers spend hours creating daily reports:
- Manual data collection
- Inconsistent formats
- Delayed submissions
- Missing information

### Solution
Automated daily progress report generation from structured site data inputs.

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class WeatherCondition(Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    SNOW = "snow"
    WIND = "wind"
    EXTREME = "extreme"


class WorkStatus(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    DELAYED = "delayed"
    NOT_STARTED = "not_started"


@dataclass
class WorkActivity:
    activity_id: str
    description: str
    location: str
    planned_qty: float
    actual_qty: float
    unit: str
    status: WorkStatus
    crew_size: int
    hours_worked: float
    notes: str = ""


@dataclass
class LaborEntry:
    trade: str
    company: str
    workers: int
    hours: float
    overtime_hours: float = 0


@dataclass
class EquipmentEntry:
    equipment_type: str
    equipment_id: str
    hours_used: float
    status: str  # active, idle, maintenance
    operator: str = ""


@dataclass
class DailyReport:
    report_date: date
    project_name: str
    project_number: str
    weather: WeatherCondition
    temperature_high: float
    temperature_low: float
    work_activities: List[WorkActivity]
    labor: List[LaborEntry]
    equipment: List[EquipmentEntry]
    delays: List[str]
    safety_incidents: int
    visitors: List[str]
    deliveries: List[str]
    prepared_by: str


class DailyProgressReporter:
    """Generate daily progress reports."""

    def __init__(self, project_name: str, project_number: str):
        self.project_name = project_name
        self.project_number = project_number

    def create_report(self,
                      report_date: date,
                      weather: WeatherCondition,
                      temp_high: float,
                      temp_low: float,
                      prepared_by: str) -> DailyReport:
        """Create new daily report."""

        return DailyReport(
            report_date=report_date,
            project_name=self.project_name,
            project_number=self.project_number,
            weather=weather,
            temperature_high=temp_high,
            temperature_low=temp_low,
            work_activities=[],
            labor=[],
            equipment=[],
            delays=[],
            safety_incidents=0,
            visitors=[],
            deliveries=[],
            prepared_by=prepared_by
        )

    def add_work_activity(self,
                          report: DailyReport,
                          activity_id: str,
                          description: str,
                          location: str,
                          planned_qty: float,
                          actual_qty: float,
                          unit: str,
                          crew_size: int,
                          hours_worked: float,
                          notes: str = ""):
        """Add work activity to report."""

        # Determine status
        if actual_qty >= planned_qty:
            status = WorkStatus.COMPLETED
        elif actual_qty > 0:
            status = WorkStatus.IN_PROGRESS
        elif actual_qty == 0 and planned_qty > 0:
            status = WorkStatus.DELAYED
        else:
            status = WorkStatus.NOT_STARTED

        activity = WorkActivity(
            activity_id=activity_id,
            description=description,
            location=location,
            planned_qty=planned_qty,
            actual_qty=actual_qty,
            unit=unit,
            status=status,
            crew_size=crew_size,
            hours_worked=hours_worked,
            notes=notes
        )

        report.work_activities.append(activity)

    def add_labor(self,
                  report: DailyReport,
                  trade: str,
                  company: str,
                  workers: int,
                  hours: float,
                  overtime_hours: float = 0):
        """Add labor entry."""

        report.labor.append(LaborEntry(
            trade=trade,
            company=company,
            workers=workers,
            hours=hours,
            overtime_hours=overtime_hours
        ))

    def add_equipment(self,
                      report: DailyReport,
                      equipment_type: str,
                      equipment_id: str,
                      hours_used: float,
                      status: str,
                      operator: str = ""):
        """Add equipment entry."""

        report.equipment.append(EquipmentEntry(
            equipment_type=equipment_type,
            equipment_id=equipment_id,
            hours_used=hours_used,
            status=status,
            operator=operator
        ))

    def calculate_summary(self, report: DailyReport) -> Dict[str, Any]:
        """Calculate report summary metrics."""

        total_workers = sum(l.workers for l in report.labor)
        total_manhours = sum(l.workers * l.hours for l in report.labor)
        total_overtime = sum(l.workers * l.overtime_hours for l in report.labor)
        equipment_hours = sum(e.hours_used for e in report.equipment)

        completed = sum(1 for a in report.work_activities if a.status == WorkStatus.COMPLETED)
        in_progress = sum(1 for a in report.work_activities if a.status == WorkStatus.IN_PROGRESS)
        delayed = sum(1 for a in report.work_activities if a.status == WorkStatus.DELAYED)

        return {
            'total_workers': total_workers,
            'total_manhours': round(total_manhours, 1),
            'total_overtime': round(total_overtime, 1),
            'equipment_hours': round(equipment_hours, 1),
            'activities_completed': completed,
            'activities_in_progress': in_progress,
            'activities_delayed': delayed,
            'safety_incidents': report.safety_incidents,
            'deliveries_count': len(report.deliveries)
        }

    def export_to_excel(self, report: DailyReport, output_path: str) -> str:
        """Export report to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Header
            header_df = pd.DataFrame([{
                'Project': report.project_name,
                'Project #': report.project_number,
                'Date': report.report_date,
                'Weather': report.weather.value,
                'High Temp': report.temperature_high,
                'Low Temp': report.temperature_low,
                'Prepared By': report.prepared_by
            }])
            header_df.to_excel(writer, sheet_name='Summary', index=False)

            # Work Activities
            if report.work_activities:
                activities_df = pd.DataFrame([
                    {
                        'Activity ID': a.activity_id,
                        'Description': a.description,
                        'Location': a.location,
                        'Planned': a.planned_qty,
                        'Actual': a.actual_qty,
                        'Unit': a.unit,
                        'Status': a.status.value,
                        'Crew': a.crew_size,
                        'Hours': a.hours_worked,
                        'Notes': a.notes
                    }
                    for a in report.work_activities
                ])
                activities_df.to_excel(writer, sheet_name='Work Activities', index=False)

            # Labor
            if report.labor:
                labor_df = pd.DataFrame([
                    {
                        'Trade': l.trade,
                        'Company': l.company,
                        'Workers': l.workers,
                        'Hours': l.hours,
                        'Overtime': l.overtime_hours,
                        'Total Hours': l.workers * (l.hours + l.overtime_hours)
                    }
                    for l in report.labor
                ])
                labor_df.to_excel(writer, sheet_name='Labor', index=False)

            # Equipment
            if report.equipment:
                equip_df = pd.DataFrame([
                    {
                        'Type': e.equipment_type,
                        'ID': e.equipment_id,
                        'Hours': e.hours_used,
                        'Status': e.status,
                        'Operator': e.operator
                    }
                    for e in report.equipment
                ])
                equip_df.to_excel(writer, sheet_name='Equipment', index=False)

        return output_path

    def generate_text_report(self, report: DailyReport) -> str:
        """Generate text version of report."""

        summary = self.calculate_summary(report)

        lines = [
            f"DAILY PROGRESS REPORT",
            f"=" * 50,
            f"Project: {report.project_name}",
            f"Project #: {report.project_number}",
            f"Date: {report.report_date}",
            f"Prepared by: {report.prepared_by}",
            f"",
            f"WEATHER CONDITIONS",
            f"-" * 30,
            f"Conditions: {report.weather.value}",
            f"Temperature: {report.temperature_low}°C - {report.temperature_high}°C",
            f"",
            f"SUMMARY",
            f"-" * 30,
            f"Total Workers: {summary['total_workers']}",
            f"Total Man-hours: {summary['total_manhours']}",
            f"Equipment Hours: {summary['equipment_hours']}",
            f"Activities Completed: {summary['activities_completed']}",
            f"Activities In Progress: {summary['activities_in_progress']}",
            f"Activities Delayed: {summary['activities_delayed']}",
            f"Safety Incidents: {summary['safety_incidents']}",
        ]

        if report.delays:
            lines.extend([f"", f"DELAYS", f"-" * 30])
            for delay in report.delays:
                lines.append(f"• {delay}")

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import date

# Initialize reporter
reporter = DailyProgressReporter("Office Tower A", "PRJ-2024-001")

# Create report
report = reporter.create_report(
    report_date=date.today(),
    weather=WeatherCondition.CLEAR,
    temp_high=28,
    temp_low=18,
    prepared_by="John Smith"
)

# Add activities
reporter.add_work_activity(
    report,
    activity_id="A-101",
    description="Pour concrete slab Level 3",
    location="Level 3, Zone A",
    planned_qty=150,
    actual_qty=150,
    unit="m3",
    crew_size=8,
    hours_worked=10
)

# Add labor
reporter.add_labor(report, "Concrete", "ABC Concrete Co", 8, 10, 2)

# Export
reporter.export_to_excel(report, "daily_report.xlsx")
```

## Common Use Cases

### 1. Generate Text Summary
```python
text = reporter.generate_text_report(report)
print(text)
```

### 2. Track Delays
```python
report.delays.append("Weather delay - rain from 14:00-16:00")
report.delays.append("Material delivery late by 2 hours")
```

### 3. Calculate Metrics
```python
summary = reporter.calculate_summary(report)
print(f"Productivity: {summary['total_manhours']} man-hours")
```

## Resources
- **DDC Book**: Chapter 4.1 - Site Data Collection
