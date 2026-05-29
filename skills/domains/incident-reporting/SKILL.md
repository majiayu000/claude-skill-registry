---
name: incident-reporting
description: "Construction safety incident reporting and analysis. Capture incidents, conduct investigations, track corrective actions, and analyze trends for prevention."
---

# Incident Reporting System

## Overview

Comprehensive incident reporting system for construction safety. Capture near-misses, injuries, and property damage. Conduct root cause analysis and track corrective actions to prevent recurrence.

> "Near-miss reporting prevents 90% of future serious incidents" — DDC Community

## Incident Pyramid

```
                    △
                   /│\        Fatality (1)
                  / │ \
                 /  │  \      Serious Injury (10)
                /   │   \
               /    │    \    Minor Injury (30)
              /     │     \
             /      │      \  Near Miss (300)
            /       │       \
           /        │        \ Unsafe Acts (3000)
          ──────────┴──────────
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import json

class IncidentType(Enum):
    NEAR_MISS = "near_miss"
    FIRST_AID = "first_aid"
    MEDICAL_TREATMENT = "medical_treatment"
    LOST_TIME = "lost_time"
    FATALITY = "fatality"
    PROPERTY_DAMAGE = "property_damage"
    ENVIRONMENTAL = "environmental"

class IncidentCategory(Enum):
    FALL = "fall"
    STRUCK_BY = "struck_by"
    CAUGHT_IN = "caught_in"
    ELECTROCUTION = "electrocution"
    VEHICLE = "vehicle"
    MATERIAL_HANDLING = "material_handling"
    TOOL_EQUIPMENT = "tool_equipment"
    SLIP_TRIP = "slip_trip"
    FIRE = "fire"
    CHEMICAL = "chemical"
    OTHER = "other"

class InvestigationStatus(Enum):
    REPORTED = "reported"
    UNDER_INVESTIGATION = "under_investigation"
    ROOT_CAUSE_IDENTIFIED = "root_cause_identified"
    CORRECTIVE_ACTIONS_ASSIGNED = "corrective_actions_assigned"
    IN_REMEDIATION = "in_remediation"
    CLOSED = "closed"

@dataclass
class Person:
    name: str
    company: str
    role: str
    contact: str
    years_experience: int = 0

@dataclass
class CorrectiveAction:
    id: str
    description: str
    assigned_to: str
    due_date: datetime
    status: str = "open"
    completed_date: Optional[datetime] = None
    verification_notes: str = ""

@dataclass
class Incident:
    id: str
    incident_type: IncidentType
    category: IncidentCategory
    date_time: datetime
    location: str
    project_id: str
    project_name: str

    # Description
    description: str
    immediate_actions: str

    # People involved
    injured_person: Optional[Person] = None
    witnesses: List[Person] = field(default_factory=list)
    reported_by: str = ""

    # Investigation
    status: InvestigationStatus = InvestigationStatus.REPORTED
    root_causes: List[str] = field(default_factory=list)
    contributing_factors: List[str] = field(default_factory=list)
    corrective_actions: List[CorrectiveAction] = field(default_factory=list)

    # Documentation
    photos: List[str] = field(default_factory=list)
    weather_conditions: str = ""
    equipment_involved: List[str] = field(default_factory=list)

    # Metrics
    days_lost: int = 0
    property_damage_cost: float = 0.0
    osha_recordable: bool = False

class IncidentManager:
    """Manage construction incident reporting and investigation."""

    # 5 Whys root cause categories
    ROOT_CAUSE_CATEGORIES = [
        "Training/Competency",
        "Procedures/Work Instructions",
        "Equipment/Tools",
        "Supervision",
        "Communication",
        "Housekeeping",
        "PPE",
        "Work Environment",
        "Physical/Mental State",
        "Management System"
    ]

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.corrective_actions: Dict[str, CorrectiveAction] = {}

    def report_incident(self, incident_type: IncidentType,
                       category: IncidentCategory,
                       date_time: datetime,
                       location: str,
                       project_id: str,
                       project_name: str,
                       description: str,
                       immediate_actions: str,
                       reported_by: str,
                       injured_person: Dict = None) -> Incident:
        """Report new incident."""
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        injured = None
        if injured_person:
            injured = Person(**injured_person)

        incident = Incident(
            id=incident_id,
            incident_type=incident_type,
            category=category,
            date_time=date_time,
            location=location,
            project_id=project_id,
            project_name=project_name,
            description=description,
            immediate_actions=immediate_actions,
            reported_by=reported_by,
            injured_person=injured
        )

        # Auto-flag OSHA recordable
        if incident_type in [IncidentType.MEDICAL_TREATMENT,
                            IncidentType.LOST_TIME,
                            IncidentType.FATALITY]:
            incident.osha_recordable = True

        self.incidents[incident_id] = incident
        return incident

    def add_witness(self, incident_id: str, witness: Dict) -> Incident:
        """Add witness to incident."""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")

        self.incidents[incident_id].witnesses.append(Person(**witness))
        return self.incidents[incident_id]

    def conduct_investigation(self, incident_id: str,
                             root_causes: List[str],
                             contributing_factors: List[str]) -> Incident:
        """Record investigation findings."""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")

        incident = self.incidents[incident_id]
        incident.root_causes = root_causes
        incident.contributing_factors = contributing_factors
        incident.status = InvestigationStatus.ROOT_CAUSE_IDENTIFIED
        return incident

    def five_whys_analysis(self, incident_id: str, whys: List[str]) -> Dict:
        """Conduct 5 Whys analysis."""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")

        analysis = {
            "incident_id": incident_id,
            "analysis_date": datetime.now().isoformat(),
            "whys": []
        }

        for i, why in enumerate(whys):
            analysis["whys"].append({
                "level": i + 1,
                "question": f"Why #{i+1}?",
                "answer": why
            })

        # The last "why" is typically the root cause
        if whys:
            self.incidents[incident_id].root_causes.append(whys[-1])

        return analysis

    def assign_corrective_action(self, incident_id: str,
                                description: str,
                                assigned_to: str,
                                due_days: int = 7) -> CorrectiveAction:
        """Assign corrective action."""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")

        action_id = f"CA-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        action = CorrectiveAction(
            id=action_id,
            description=description,
            assigned_to=assigned_to,
            due_date=datetime.now() + timedelta(days=due_days)
        )

        self.incidents[incident_id].corrective_actions.append(action)
        self.incidents[incident_id].status = InvestigationStatus.CORRECTIVE_ACTIONS_ASSIGNED
        self.corrective_actions[action_id] = action
        return action

    def complete_corrective_action(self, action_id: str,
                                   verification_notes: str) -> CorrectiveAction:
        """Mark corrective action complete."""
        if action_id not in self.corrective_actions:
            raise ValueError(f"Corrective action {action_id} not found")

        action = self.corrective_actions[action_id]
        action.status = "completed"
        action.completed_date = datetime.now()
        action.verification_notes = verification_notes
        return action

    def get_incident_metrics(self, project_id: str = None,
                            start_date: datetime = None,
                            end_date: datetime = None) -> Dict:
        """Calculate incident metrics."""
        incidents = list(self.incidents.values())

        if project_id:
            incidents = [i for i in incidents if i.project_id == project_id]
        if start_date:
            incidents = [i for i in incidents if i.date_time >= start_date]
        if end_date:
            incidents = [i for i in incidents if i.date_time <= end_date]

        # Calculate metrics
        total = len(incidents)
        near_misses = len([i for i in incidents if i.incident_type == IncidentType.NEAR_MISS])
        first_aid = len([i for i in incidents if i.incident_type == IncidentType.FIRST_AID])
        recordables = len([i for i in incidents if i.osha_recordable])
        lost_time = len([i for i in incidents if i.incident_type == IncidentType.LOST_TIME])
        total_days_lost = sum(i.days_lost for i in incidents)

        # Category breakdown
        by_category = {}
        for cat in IncidentCategory:
            count = len([i for i in incidents if i.category == cat])
            if count > 0:
                by_category[cat.value] = count

        return {
            "total_incidents": total,
            "near_misses": near_misses,
            "first_aid_cases": first_aid,
            "osha_recordables": recordables,
            "lost_time_incidents": lost_time,
            "total_days_lost": total_days_lost,
            "by_category": by_category,
            "near_miss_ratio": near_misses / recordables if recordables else 0
        }

    def calculate_trir(self, hours_worked: int, project_id: str = None) -> float:
        """Calculate Total Recordable Incident Rate."""
        incidents = list(self.incidents.values())
        if project_id:
            incidents = [i for i in incidents if i.project_id == project_id]

        recordables = len([i for i in incidents if i.osha_recordable])

        if hours_worked == 0:
            return 0

        # TRIR = (Recordables × 200,000) / Hours Worked
        return (recordables * 200000) / hours_worked

    def calculate_dart(self, hours_worked: int, project_id: str = None) -> float:
        """Calculate Days Away, Restricted, or Transferred rate."""
        incidents = list(self.incidents.values())
        if project_id:
            incidents = [i for i in incidents if i.project_id == project_id]

        dart_cases = len([i for i in incidents
                         if i.incident_type in [IncidentType.LOST_TIME]])

        if hours_worked == 0:
            return 0

        return (dart_cases * 200000) / hours_worked

    def get_trend_analysis(self, months: int = 6) -> List[Dict]:
        """Analyze incident trends over time."""
        trends = []
        now = datetime.now()

        for i in range(months):
            month_start = datetime(now.year, now.month - i, 1) if now.month > i else datetime(now.year - 1, 12 - (i - now.month), 1)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)

            month_incidents = [inc for inc in self.incidents.values()
                             if month_start <= inc.date_time <= month_end]

            trends.append({
                "month": month_start.strftime("%Y-%m"),
                "total": len(month_incidents),
                "near_misses": len([i for i in month_incidents if i.incident_type == IncidentType.NEAR_MISS]),
                "recordables": len([i for i in month_incidents if i.osha_recordable])
            })

        return list(reversed(trends))

    def generate_incident_report(self, incident_id: str) -> str:
        """Generate detailed incident report."""
        if incident_id not in self.incidents:
            return "Incident not found"

        inc = self.incidents[incident_id]

        lines = [
            f"# Incident Report",
            f"",
            f"**Incident ID:** {inc.id}",
            f"**Type:** {inc.incident_type.value}",
            f"**Category:** {inc.category.value}",
            f"**Date/Time:** {inc.date_time.strftime('%Y-%m-%d %H:%M')}",
            f"**Location:** {inc.location}",
            f"**Project:** {inc.project_name}",
            f"**Status:** {inc.status.value}",
            f"**OSHA Recordable:** {'Yes' if inc.osha_recordable else 'No'}",
            f"",
            f"## Description",
            f"{inc.description}",
            f"",
            f"## Immediate Actions Taken",
            f"{inc.immediate_actions}",
            f"",
        ]

        if inc.injured_person:
            lines.extend([
                f"## Injured Person",
                f"- Name: {inc.injured_person.name}",
                f"- Company: {inc.injured_person.company}",
                f"- Role: {inc.injured_person.role}",
                f"- Experience: {inc.injured_person.years_experience} years",
                f""
            ])

        if inc.root_causes:
            lines.extend([
                f"## Root Causes",
                *[f"- {rc}" for rc in inc.root_causes],
                f""
            ])

        if inc.corrective_actions:
            lines.extend([
                f"## Corrective Actions",
                f"| Action | Assigned To | Due | Status |",
                f"|--------|-------------|-----|--------|"
            ])
            for ca in inc.corrective_actions:
                lines.append(f"| {ca.description} | {ca.assigned_to} | {ca.due_date.strftime('%Y-%m-%d')} | {ca.status} |")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize manager
manager = IncidentManager()

# Report near-miss
incident = manager.report_incident(
    incident_type=IncidentType.NEAR_MISS,
    category=IncidentCategory.STRUCK_BY,
    date_time=datetime.now(),
    location="Level 5, Grid C-4",
    project_id="PRJ-001",
    project_name="Office Tower",
    description="Unsecured tool fell from scaffold, landed 2 feet from worker",
    immediate_actions="Area cordoned off, toolbox talk conducted",
    reported_by="Site Foreman"
)

# 5 Whys analysis
analysis = manager.five_whys_analysis(incident.id, [
    "Tool fell from scaffold",
    "Tool was not secured",
    "No tool lanyard was used",
    "Worker not trained on tool tethering",
    "Tool tethering training not included in orientation"
])

# Assign corrective actions
manager.assign_corrective_action(
    incident.id,
    "Update orientation to include tool tethering training",
    "Safety Manager",
    due_days=14
)

manager.assign_corrective_action(
    incident.id,
    "Provide tool lanyards to all workers at height",
    "Procurement",
    due_days=7
)

# Get metrics
metrics = manager.get_incident_metrics()
print(f"Total Incidents: {metrics['total_incidents']}")
print(f"Near Miss Ratio: {metrics['near_miss_ratio']:.1f}")

# Generate report
print(manager.generate_incident_report(incident.id))
```

## Requirements

```bash
pip install (no external dependencies)
```
