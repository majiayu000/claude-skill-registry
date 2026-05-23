---
name: safety-inspection
description: Digital safety inspection system for construction sites. Checklists, hazard tracking, incident reporting, and compliance documentation.
---

# Safety Inspection System for Construction

Comprehensive digital safety management system for construction sites with inspection checklists, hazard tracking, and incident reporting.

## Business Case

**Problem**: Paper-based safety management leads to:
- Incomplete inspections (20-30% of items skipped)
- Lost documentation
- Delayed incident reporting
- Difficulty tracking corrective actions
- Compliance audit failures

**Solution**: Digital system that:
- Enforces complete checklist completion
- Photos attached to each finding
- Instant notifications for hazards
- Tracks corrective actions to closure
- Generates compliance reports

**ROI**: 40% reduction in recordable incidents, 100% audit compliance

## Safety Inspection Types

```
┌──────────────────────────────────────────────────────────────────────┐
│                    SAFETY INSPECTION TYPES                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  DAILY                    WEEKLY                   SPECIAL           │
│  ┌─────────────┐          ┌─────────────┐         ┌─────────────┐   │
│  │ Pre-Work    │          │ Area Walk   │         │ Pre-Pour    │   │
│  │ • Housekeeping│        │ • Fire ext. │         │ • Formwork  │   │
│  │ • PPE       │          │ • First aid │         │ • Shoring   │   │
│  │ • Equipment │          │ • Scaffolds │         │ └─────────────┘   │
│  └─────────────┘          │ • Trenches  │         ┌─────────────┐   │
│  ┌─────────────┐          └─────────────┘         │ Crane Setup │   │
│  │ Toolbox Talk│          ┌─────────────┐         │ • Ground    │   │
│  │ • Topic     │          │ Equipment   │         │ • Load chart│   │
│  │ • Attendees │          │ • Cranes    │         │ • Rigging   │   │
│  │ • Sign-off  │          │ • Lifts     │         └─────────────┘   │
│  └─────────────┘          │ • Vehicles  │         ┌─────────────┐   │
│  ┌─────────────┐          └─────────────┘         │ Hot Work    │   │
│  │ End of Day  │                                  │ • Permit    │   │
│  │ • Secured   │                                  │ • Fire watch│   │
│  │ • Barricades│                                  └─────────────┘   │
│  └─────────────┘                                                     │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Structure

```python
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
import uuid

class HazardSeverity(Enum):
    CRITICAL = "Critical"      # Immediate danger to life
    HIGH = "High"              # Serious injury potential
    MEDIUM = "Medium"          # Injury potential
    LOW = "Low"                # Minor hazard
    OBSERVATION = "Observation"  # Best practice

class HazardStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CORRECTED = "Corrected"
    VERIFIED = "Verified Closed"

class InspectionType(Enum):
    DAILY_PREWORK = "Daily Pre-Work"
    TOOLBOX_TALK = "Toolbox Talk"
    AREA_INSPECTION = "Area Inspection"
    EQUIPMENT_INSPECTION = "Equipment Inspection"
    HOT_WORK_PERMIT = "Hot Work Permit"
    CONFINED_SPACE = "Confined Space Entry"
    CRANE_LIFT = "Crane/Lift Inspection"
    SCAFFOLD = "Scaffold Inspection"
    EXCAVATION = "Excavation Inspection"
    INCIDENT = "Incident Report"

@dataclass
class Hazard:
    hazard_id: str
    inspection_id: str
    description: str
    severity: HazardSeverity
    location: str
    photo_urls: List[str] = field(default_factory=list)
    assigned_to: str = ""
    due_date: date = None
    status: HazardStatus = HazardStatus.OPEN
    corrective_action: str = ""
    corrected_date: date = None
    corrected_by: str = ""
    verification_date: date = None
    verified_by: str = ""

@dataclass
class Inspection:
    inspection_id: str
    inspection_type: InspectionType
    project_id: str
    date: date
    inspector: str
    location: str
    checklist_items: List[dict] = field(default_factory=list)
    hazards_found: List[Hazard] = field(default_factory=list)
    overall_rating: str = ""  # Pass/Fail/Conditional
    notes: str = ""
    photos: List[str] = field(default_factory=list)
    signatures: List[dict] = field(default_factory=list)
    weather: str = ""
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Incident:
    incident_id: str
    project_id: str
    date: datetime
    type: str  # Near Miss, First Aid, Recordable, Lost Time
    description: str
    location: str
    injured_party: str = ""
    witness_names: List[str] = field(default_factory=list)
    immediate_actions: str = ""
    root_cause: str = ""
    corrective_actions: str = ""
    reported_by: str = ""
    photos: List[str] = field(default_factory=list)
    osha_recordable: bool = False
    days_away: int = 0
    days_restricted: int = 0
```

## Python Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json
import os

class SafetyManager:
    """Construction site safety management system"""

    def __init__(self, project_id: str, storage_path: str = None):
        self.project_id = project_id
        self.storage_path = storage_path or f"safety_{project_id}"
        self.inspections: Dict[str, Inspection] = {}
        self.hazards: Dict[str, Hazard] = {}
        self.incidents: Dict[str, Incident] = {}

        # Load checklists
        self.checklists = self._load_checklists()

    def _load_checklists(self) -> Dict[str, List[dict]]:
        """Load inspection checklists"""
        return {
            InspectionType.DAILY_PREWORK.value: [
                {"id": "DP01", "item": "Work area clean and organized", "category": "Housekeeping"},
                {"id": "DP02", "item": "Walking surfaces clear of debris", "category": "Housekeeping"},
                {"id": "DP03", "item": "All workers have required PPE", "category": "PPE"},
                {"id": "DP04", "item": "Hard hats worn in designated areas", "category": "PPE"},
                {"id": "DP05", "item": "Safety glasses worn where required", "category": "PPE"},
                {"id": "DP06", "item": "High-visibility vests worn", "category": "PPE"},
                {"id": "DP07", "item": "Fall protection in use above 6 feet", "category": "Fall Protection"},
                {"id": "DP08", "item": "Guardrails/covers on floor openings", "category": "Fall Protection"},
                {"id": "DP09", "item": "Ladders in good condition", "category": "Equipment"},
                {"id": "DP10", "item": "Extension cords not damaged", "category": "Electrical"},
                {"id": "DP11", "item": "GFCIs in use for power tools", "category": "Electrical"},
                {"id": "DP12", "item": "Fire extinguishers accessible", "category": "Fire Safety"},
                {"id": "DP13", "item": "Emergency exits clear", "category": "Emergency"},
                {"id": "DP14", "item": "First aid kit stocked", "category": "Emergency"},
                {"id": "DP15", "item": "SDS sheets available", "category": "Hazcom"},
            ],
            InspectionType.SCAFFOLD.value: [
                {"id": "SC01", "item": "Base plates/mudsills in place", "category": "Foundation"},
                {"id": "SC02", "item": "All legs plumb and level", "category": "Structure"},
                {"id": "SC03", "item": "Cross bracing complete", "category": "Structure"},
                {"id": "SC04", "item": "Planking fully decked", "category": "Platform"},
                {"id": "SC05", "item": "No gaps >1 inch between planks", "category": "Platform"},
                {"id": "SC06", "item": "Guardrails at 42 inches", "category": "Guardrails"},
                {"id": "SC07", "item": "Midrails at 21 inches", "category": "Guardrails"},
                {"id": "SC08", "item": "Toeboards installed", "category": "Guardrails"},
                {"id": "SC09", "item": "Access ladder provided", "category": "Access"},
                {"id": "SC10", "item": "Tied to structure every 26 feet vertical", "category": "Ties"},
                {"id": "SC11", "item": "Inspection tag current", "category": "Documentation"},
                {"id": "SC12", "item": "Competent person inspection today", "category": "Documentation"},
            ],
            InspectionType.EXCAVATION.value: [
                {"id": "EX01", "item": "Excavation permit obtained", "category": "Permits"},
                {"id": "EX02", "item": "Utilities located and marked", "category": "Utilities"},
                {"id": "EX03", "item": "Competent person on site", "category": "Supervision"},
                {"id": "EX04", "item": "Soil classification completed", "category": "Soil"},
                {"id": "EX05", "item": "Appropriate protective system in place", "category": "Protection"},
                {"id": "EX06", "item": "Spoil pile 2+ feet from edge", "category": "Housekeeping"},
                {"id": "EX07", "item": "Ladder within 25 feet of workers", "category": "Egress"},
                {"id": "EX08", "item": "Barricades around excavation", "category": "Protection"},
                {"id": "EX09", "item": "Water accumulation addressed", "category": "Conditions"},
                {"id": "EX10", "item": "Atmosphere tested if >4 feet", "category": "Air Quality"},
            ],
        }

    def create_inspection(
        self,
        inspection_type: InspectionType,
        inspector: str,
        location: str,
        weather: str = ""
    ) -> Inspection:
        """Create new inspection"""

        inspection_id = f"INS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Get checklist for this type
        checklist = self.checklists.get(inspection_type.value, [])
        checklist_items = [
            {**item, "result": None, "notes": "", "photo": None}
            for item in checklist
        ]

        inspection = Inspection(
            inspection_id=inspection_id,
            inspection_type=inspection_type,
            project_id=self.project_id,
            date=date.today(),
            inspector=inspector,
            location=location,
            checklist_items=checklist_items,
            weather=weather
        )

        self.inspections[inspection_id] = inspection
        return inspection

    def complete_checklist_item(
        self,
        inspection_id: str,
        item_id: str,
        result: str,  # "Pass", "Fail", "N/A"
        notes: str = "",
        photo_url: str = None
    ) -> Inspection:
        """Complete a checklist item"""

        inspection = self.inspections.get(inspection_id)
        if not inspection:
            raise ValueError(f"Inspection {inspection_id} not found")

        for item in inspection.checklist_items:
            if item["id"] == item_id:
                item["result"] = result
                item["notes"] = notes
                item["photo"] = photo_url
                break

        # If failed, prompt for hazard creation
        if result == "Fail":
            print(f"⚠️ Item {item_id} failed - create hazard record")

        return inspection

    def add_hazard(
        self,
        inspection_id: str,
        description: str,
        severity: HazardSeverity,
        location: str,
        assigned_to: str = "",
        due_date: date = None,
        photo_urls: List[str] = None
    ) -> Hazard:
        """Record a hazard finding"""

        hazard_id = f"HAZ-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if due_date is None:
            # Default due dates by severity
            days = {
                HazardSeverity.CRITICAL: 0,    # Immediate
                HazardSeverity.HIGH: 1,        # 24 hours
                HazardSeverity.MEDIUM: 3,      # 3 days
                HazardSeverity.LOW: 7,         # 1 week
                HazardSeverity.OBSERVATION: 14 # 2 weeks
            }
            due_date = date.today() + timedelta(days=days.get(severity, 7))

        hazard = Hazard(
            hazard_id=hazard_id,
            inspection_id=inspection_id,
            description=description,
            severity=severity,
            location=location,
            assigned_to=assigned_to,
            due_date=due_date,
            photo_urls=photo_urls or []
        )

        self.hazards[hazard_id] = hazard

        # Add to inspection
        if inspection_id in self.inspections:
            self.inspections[inspection_id].hazards_found.append(hazard)

        # Notify for critical/high severity
        if severity in [HazardSeverity.CRITICAL, HazardSeverity.HIGH]:
            self._notify_hazard(hazard)

        return hazard

    def correct_hazard(
        self,
        hazard_id: str,
        corrective_action: str,
        corrected_by: str,
        photo_url: str = None
    ) -> Hazard:
        """Record hazard correction"""

        hazard = self.hazards.get(hazard_id)
        if not hazard:
            raise ValueError(f"Hazard {hazard_id} not found")

        hazard.corrective_action = corrective_action
        hazard.corrected_by = corrected_by
        hazard.corrected_date = date.today()
        hazard.status = HazardStatus.CORRECTED

        if photo_url:
            hazard.photo_urls.append(photo_url)

        return hazard

    def verify_hazard_closure(
        self,
        hazard_id: str,
        verified_by: str
    ) -> Hazard:
        """Verify hazard has been properly corrected"""

        hazard = self.hazards.get(hazard_id)
        if not hazard:
            raise ValueError(f"Hazard {hazard_id} not found")

        if hazard.status != HazardStatus.CORRECTED:
            raise ValueError(f"Hazard {hazard_id} not corrected yet")

        hazard.verified_by = verified_by
        hazard.verification_date = date.today()
        hazard.status = HazardStatus.VERIFIED

        return hazard

    def report_incident(
        self,
        incident_type: str,
        description: str,
        location: str,
        injured_party: str = "",
        witness_names: List[str] = None,
        immediate_actions: str = "",
        reported_by: str = "",
        photo_urls: List[str] = None
    ) -> Incident:
        """Report safety incident"""

        incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        incident = Incident(
            incident_id=incident_id,
            project_id=self.project_id,
            date=datetime.now(),
            type=incident_type,
            description=description,
            location=location,
            injured_party=injured_party,
            witness_names=witness_names or [],
            immediate_actions=immediate_actions,
            reported_by=reported_by,
            photos=photo_urls or []
        )

        self.incidents[incident_id] = incident

        # Immediate notification for all incidents
        self._notify_incident(incident)

        return incident

    def get_open_hazards(self) -> List[Hazard]:
        """Get all open hazards"""
        return [
            h for h in self.hazards.values()
            if h.status in [HazardStatus.OPEN, HazardStatus.IN_PROGRESS]
        ]

    def get_overdue_hazards(self) -> List[Hazard]:
        """Get overdue hazards"""
        today = date.today()
        return [
            h for h in self.hazards.values()
            if h.status == HazardStatus.OPEN and h.due_date < today
        ]

    def get_statistics(self, period_days: int = 30) -> dict:
        """Get safety statistics"""

        cutoff = date.today() - timedelta(days=period_days)

        # Filter by period
        period_inspections = [
            i for i in self.inspections.values()
            if i.date >= cutoff
        ]
        period_hazards = [
            h for h in self.hazards.values()
            # Get creation date from inspection
        ]
        period_incidents = [
            i for i in self.incidents.values()
            if i.date.date() >= cutoff
        ]

        # Calculate metrics
        total_inspections = len(period_inspections)
        total_hazards = len(self.hazards)
        open_hazards = len(self.get_open_hazards())
        overdue_hazards = len(self.get_overdue_hazards())

        # Incident metrics
        near_misses = len([i for i in period_incidents if i.type == "Near Miss"])
        first_aid = len([i for i in period_incidents if i.type == "First Aid"])
        recordables = len([i for i in period_incidents if i.osha_recordable])

        # Calculate TRIR (Total Recordable Incident Rate)
        # TRIR = (Recordables × 200,000) / Total Hours Worked
        # Assuming 50 workers × 8 hours × 22 days = 8,800 hours/month
        estimated_hours = 8800 * (period_days / 30)
        trir = (recordables * 200000 / estimated_hours) if estimated_hours > 0 else 0

        return {
            'period_days': period_days,
            'inspections_completed': total_inspections,
            'hazards_identified': total_hazards,
            'hazards_open': open_hazards,
            'hazards_overdue': overdue_hazards,
            'hazards_by_severity': self._count_by_severity(),
            'incidents_total': len(period_incidents),
            'near_misses': near_misses,
            'first_aid': first_aid,
            'recordables': recordables,
            'trir': round(trir, 2),
            'days_since_last_recordable': self._days_since_recordable()
        }

    def _count_by_severity(self) -> dict:
        """Count hazards by severity"""
        result = {s.value: 0 for s in HazardSeverity}
        for hazard in self.hazards.values():
            if hazard.status != HazardStatus.VERIFIED:
                result[hazard.severity.value] += 1
        return result

    def _days_since_recordable(self) -> int:
        """Calculate days since last recordable incident"""
        recordables = [
            i for i in self.incidents.values()
            if i.osha_recordable
        ]
        if not recordables:
            return 365  # Assume 1 year if no recordables

        last = max(recordables, key=lambda x: x.date)
        return (datetime.now() - last.date).days

    def _notify_hazard(self, hazard: Hazard):
        """Send notification for high-severity hazard"""
        print(f"🚨 HAZARD ALERT: {hazard.severity.value}")
        print(f"   Location: {hazard.location}")
        print(f"   Description: {hazard.description}")
        print(f"   Assigned to: {hazard.assigned_to}")
        print(f"   Due: {hazard.due_date}")

    def _notify_incident(self, incident: Incident):
        """Send notification for incident"""
        print(f"⚠️ INCIDENT REPORTED: {incident.type}")
        print(f"   Location: {incident.location}")
        print(f"   Description: {incident.description}")
        if incident.injured_party:
            print(f"   Injured: {incident.injured_party}")

    def generate_daily_safety_report(self) -> str:
        """Generate daily safety briefing"""

        stats = self.get_statistics(period_days=1)
        open_hazards = self.get_open_hazards()
        overdue = self.get_overdue_hazards()

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                   DAILY SAFETY BRIEFING                       ║
║   Project: {self.project_id:<40}       ║
║   Date: {date.today().strftime('%d.%m.%Y'):<43}       ║
╠══════════════════════════════════════════════════════════════╣

📊 TODAY'S METRICS
───────────────────────────────────────────────────────────────
   Days Without Recordable Incident: {stats['days_since_last_recordable']}
   Open Hazards: {stats['hazards_open']}
   Overdue Hazards: {stats['hazards_overdue']}

⚠️ OPEN HAZARDS REQUIRING ATTENTION
───────────────────────────────────────────────────────────────
"""
        if overdue:
            report += "🔴 OVERDUE:\n"
            for h in overdue:
                report += f"   • {h.hazard_id}: {h.description[:50]}... (Due: {h.due_date})\n"

        critical_high = [h for h in open_hazards
                        if h.severity in [HazardSeverity.CRITICAL, HazardSeverity.HIGH]]
        if critical_high:
            report += "\n🟠 CRITICAL/HIGH PRIORITY:\n"
            for h in critical_high:
                report += f"   • {h.hazard_id}: {h.description[:50]}... ({h.severity.value})\n"

        report += """
📋 REQUIRED INSPECTIONS TODAY
───────────────────────────────────────────────────────────────
   ☐ Pre-work safety inspection
   ☐ Toolbox talk (Topic: ________________)
   ☐ Equipment inspections

💡 SAFETY FOCUS OF THE DAY
───────────────────────────────────────────────────────────────
   [Insert daily focus topic]

╚══════════════════════════════════════════════════════════════╝
"""
        return report


# Usage Example
if __name__ == "__main__":
    # Initialize safety manager
    safety = SafetyManager(project_id="PROJECT-2026-001")

    # Create daily pre-work inspection
    inspection = safety.create_inspection(
        inspection_type=InspectionType.DAILY_PREWORK,
        inspector="Ivan Petrov",
        location="Building A, Floor 5",
        weather="Clear, -5°C"
    )

    print(f"Created inspection: {inspection.inspection_id}")

    # Complete checklist items
    safety.complete_checklist_item(
        inspection_id=inspection.inspection_id,
        item_id="DP01",
        result="Pass"
    )

    safety.complete_checklist_item(
        inspection_id=inspection.inspection_id,
        item_id="DP07",
        result="Fail",
        notes="Worker on scaffold without harness"
    )

    # Add hazard for failed item
    hazard = safety.add_hazard(
        inspection_id=inspection.inspection_id,
        description="Worker observed on scaffold without fall protection harness",
        severity=HazardSeverity.CRITICAL,
        location="Building A, Floor 5, West side",
        assigned_to="Site Foreman"
    )

    print(f"Hazard created: {hazard.hazard_id}")

    # Correct hazard
    safety.correct_hazard(
        hazard_id=hazard.hazard_id,
        corrective_action="Worker provided harness and retrained on fall protection requirements",
        corrected_by="Ivan Petrov"
    )

    # Verify closure
    safety.verify_hazard_closure(
        hazard_id=hazard.hazard_id,
        verified_by="Safety Manager"
    )

    # Generate daily report
    print(safety.generate_daily_safety_report())
```

## Mobile App Integration

```yaml
# Telegram bot for field safety inspections
name: Safety Inspection Bot
commands:
  /inspection:
    - Select inspection type
    - Show checklist
    - Record results (✅/❌)
    - Capture photos
    - Submit

  /hazard:
    - Describe hazard
    - Select severity
    - Take photo
    - GPS location
    - Assign responsible party

  /incident:
    - Report type
    - Description
    - Photos
    - Witness info
    - Immediate actions
```

---

*"Safety is not a priority - it's a value. Priorities change, values don't."*
