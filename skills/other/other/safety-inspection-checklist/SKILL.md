---
name: "safety-inspection-checklist"
description: "Digital safety inspection checklists for construction sites. Generate, conduct, and track safety inspections with automated reporting and compliance monitoring."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🦺", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Safety Inspection Checklist

## Overview

Digital safety inspection checklists streamline site safety management. Generate inspection forms, conduct mobile inspections, track findings, and automate compliance reporting.

> "Digital checklists reduce inspection time by 60% and improve compliance tracking" — DDC Community

## Why Digital Checklists?

| Feature | Benefit |
|---------|---------|
| Mobile-first | Inspect anywhere on site |
| Photo documentation | Visual evidence attached |
| Real-time sync | Immediate notification of issues |
| Automated reports | Weekly/monthly summaries |
| Trend analysis | Identify recurring hazards |
| Compliance tracking | OSHA/local regulation alignment |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                SAFETY INSPECTION SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Templates         Mobile App           Backend                  │
│  ─────────         ──────────           ───────                  │
│                                                                  │
│  📋 OSHA forms  →  📱 Conduct    →   💾 Store                   │
│  🏗️ Site-specific   📸 Photos        📊 Analyze                 │
│  ⚡ Quick checks    📍 Location       📧 Alert                   │
│                     ✅ Sign-off       📈 Report                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import json

class InspectionType(Enum):
    DAILY_SITE = "daily_site"
    WEEKLY_SAFETY = "weekly_safety"
    SCAFFOLD = "scaffold"
    EXCAVATION = "excavation"
    ELECTRICAL = "electrical"
    CRANE_LIFT = "crane_lift"
    HOT_WORK = "hot_work"
    CONFINED_SPACE = "confined_space"
    FALL_PROTECTION = "fall_protection"

class FindingSeverity(Enum):
    CRITICAL = "critical"      # Stop work immediately
    MAJOR = "major"            # Correct within 24 hours
    MINOR = "minor"            # Correct within 1 week
    OBSERVATION = "observation" # Best practice recommendation

class FindingStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CORRECTED = "corrected"
    VERIFIED = "verified"

@dataclass
class ChecklistItem:
    id: str
    category: str
    question: str
    regulation_ref: str = ""
    guidance: str = ""
    requires_photo: bool = False
    critical: bool = False

@dataclass
class InspectionFinding:
    item_id: str
    status: str  # pass, fail, na
    severity: Optional[FindingSeverity] = None
    description: str = ""
    photo_urls: List[str] = field(default_factory=list)
    location: str = ""
    assigned_to: str = ""
    due_date: Optional[datetime] = None
    corrective_action: str = ""
    finding_status: FindingStatus = FindingStatus.OPEN

@dataclass
class SafetyInspection:
    id: str
    inspection_type: InspectionType
    project_id: str
    project_name: str
    location: str
    inspector: str
    date: datetime
    weather: str
    workers_on_site: int
    findings: List[InspectionFinding] = field(default_factory=list)
    overall_score: float = 0.0
    signed_off: bool = False
    sign_off_by: str = ""

class SafetyInspectionManager:
    """Manage construction safety inspections."""

    # OSHA-aligned checklist templates
    CHECKLIST_TEMPLATES = {
        InspectionType.DAILY_SITE: [
            ChecklistItem("DS001", "General", "Site access controlled and secure?", "1926.20"),
            ChecklistItem("DS002", "General", "Emergency exits clear and marked?", "1926.34"),
            ChecklistItem("DS003", "Housekeeping", "Work areas clean and organized?", "1926.25"),
            ChecklistItem("DS004", "Housekeeping", "Waste properly disposed?", "1926.25"),
            ChecklistItem("DS005", "PPE", "All workers wearing required PPE?", "1926.28", critical=True),
            ChecklistItem("DS006", "PPE", "Hard hats worn in designated areas?", "1926.100"),
            ChecklistItem("DS007", "Fall Protection", "Guardrails in place at open edges?", "1926.502", critical=True),
            ChecklistItem("DS008", "Fall Protection", "Floor openings covered/protected?", "1926.502"),
            ChecklistItem("DS009", "Electrical", "No exposed wiring or damaged cords?", "1926.405"),
            ChecklistItem("DS010", "Electrical", "GFCIs in use for power tools?", "1926.404"),
            ChecklistItem("DS011", "Fire", "Fire extinguishers accessible?", "1926.150"),
            ChecklistItem("DS012", "Fire", "Hot work permits in place?", "1926.352"),
            ChecklistItem("DS013", "Equipment", "Equipment inspected before use?", "1926.20"),
            ChecklistItem("DS014", "Scaffolding", "Scaffolds properly erected?", "1926.451"),
            ChecklistItem("DS015", "Excavation", "Excavations properly sloped/shored?", "1926.652", critical=True),
        ],
        InspectionType.SCAFFOLD: [
            ChecklistItem("SC001", "Foundation", "Base plates on solid foundation?", "1926.451(c)"),
            ChecklistItem("SC002", "Foundation", "Mudsills adequate for load?", "1926.451(c)"),
            ChecklistItem("SC003", "Erection", "Plumb and level?", "1926.451(c)"),
            ChecklistItem("SC004", "Erection", "Cross bracing installed?", "1926.451(c)"),
            ChecklistItem("SC005", "Platforms", "Fully planked (no gaps >1 inch)?", "1926.451(b)"),
            ChecklistItem("SC006", "Platforms", "Planks secured against movement?", "1926.451(b)"),
            ChecklistItem("SC007", "Guardrails", "Top rail at 42 inches?", "1926.451(g)"),
            ChecklistItem("SC008", "Guardrails", "Mid-rail installed?", "1926.451(g)"),
            ChecklistItem("SC009", "Guardrails", "Toeboards at open edges?", "1926.451(h)"),
            ChecklistItem("SC010", "Access", "Safe access provided (ladder, stairs)?", "1926.451(e)"),
            ChecklistItem("SC011", "Capacity", "Load rating posted?", "1926.451(f)"),
            ChecklistItem("SC012", "Inspection", "Competent person inspection tag?", "1926.451(f)"),
        ],
        InspectionType.EXCAVATION: [
            ChecklistItem("EX001", "Planning", "Dig permit obtained?", "1926.651"),
            ChecklistItem("EX002", "Planning", "Utilities located and marked?", "1926.651(b)", critical=True),
            ChecklistItem("EX003", "Soil", "Soil classification completed?", "1926.652(a)"),
            ChecklistItem("EX004", "Protection", "Proper sloping/benching?", "1926.652(b)"),
            ChecklistItem("EX005", "Protection", "Shoring/shielding in place?", "1926.652(c)"),
            ChecklistItem("EX006", "Access", "Safe access within 25 feet?", "1926.651(c)"),
            ChecklistItem("EX007", "Spoils", "Spoils 2+ feet from edge?", "1926.651(j)"),
            ChecklistItem("EX008", "Water", "Water accumulation controlled?", "1926.651(h)"),
            ChecklistItem("EX009", "Atmosphere", "Hazardous atmosphere tested?", "1926.651(g)"),
            ChecklistItem("EX010", "Inspection", "Daily inspection by competent person?", "1926.651(k)"),
        ],
    }

    def __init__(self):
        self.inspections: Dict[str, SafetyInspection] = {}
        self.findings_db: List[InspectionFinding] = []

    def create_inspection(self, inspection_type: InspectionType,
                         project_id: str, project_name: str,
                         location: str, inspector: str,
                         weather: str = "", workers: int = 0) -> SafetyInspection:
        """Create new inspection from template."""
        inspection_id = f"INS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        inspection = SafetyInspection(
            id=inspection_id,
            inspection_type=inspection_type,
            project_id=project_id,
            project_name=project_name,
            location=location,
            inspector=inspector,
            date=datetime.now(),
            weather=weather,
            workers_on_site=workers
        )

        self.inspections[inspection_id] = inspection
        return inspection

    def get_checklist(self, inspection_type: InspectionType) -> List[ChecklistItem]:
        """Get checklist template for inspection type."""
        return self.CHECKLIST_TEMPLATES.get(inspection_type, [])

    def record_finding(self, inspection_id: str, item_id: str,
                      status: str, severity: FindingSeverity = None,
                      description: str = "", photos: List[str] = None,
                      location: str = "", assigned_to: str = "") -> InspectionFinding:
        """Record inspection finding."""
        finding = InspectionFinding(
            item_id=item_id,
            status=status,
            severity=severity,
            description=description,
            photo_urls=photos or [],
            location=location,
            assigned_to=assigned_to
        )

        if inspection_id in self.inspections:
            self.inspections[inspection_id].findings.append(finding)

        if status == "fail":
            self.findings_db.append(finding)

        return finding

    def calculate_score(self, inspection_id: str) -> float:
        """Calculate inspection score (pass rate)."""
        if inspection_id not in self.inspections:
            return 0.0

        inspection = self.inspections[inspection_id]
        if not inspection.findings:
            return 0.0

        applicable = [f for f in inspection.findings if f.status != "na"]
        if not applicable:
            return 100.0

        passed = len([f for f in applicable if f.status == "pass"])
        score = (passed / len(applicable)) * 100

        inspection.overall_score = score
        return score

    def get_open_findings(self, project_id: str = None) -> List[InspectionFinding]:
        """Get all open findings, optionally filtered by project."""
        open_findings = []

        for inspection in self.inspections.values():
            if project_id and inspection.project_id != project_id:
                continue

            for finding in inspection.findings:
                if finding.status == "fail" and finding.finding_status in [FindingStatus.OPEN, FindingStatus.IN_PROGRESS]:
                    open_findings.append(finding)

        return sorted(open_findings, key=lambda f: (
            0 if f.severity == FindingSeverity.CRITICAL else
            1 if f.severity == FindingSeverity.MAJOR else 2
        ))

    def generate_report(self, inspection_id: str) -> str:
        """Generate inspection report."""
        if inspection_id not in self.inspections:
            return "Inspection not found"

        insp = self.inspections[inspection_id]
        score = self.calculate_score(inspection_id)

        lines = [
            f"# Safety Inspection Report",
            f"",
            f"**Inspection ID:** {insp.id}",
            f"**Type:** {insp.inspection_type.value}",
            f"**Project:** {insp.project_name}",
            f"**Location:** {insp.location}",
            f"**Date:** {insp.date.strftime('%Y-%m-%d %H:%M')}",
            f"**Inspector:** {insp.inspector}",
            f"**Weather:** {insp.weather}",
            f"**Workers on Site:** {insp.workers_on_site}",
            f"",
            f"## Overall Score: {score:.1f}%",
            f"",
        ]

        # Summary by severity
        critical = [f for f in insp.findings if f.severity == FindingSeverity.CRITICAL]
        major = [f for f in insp.findings if f.severity == FindingSeverity.MAJOR]
        minor = [f for f in insp.findings if f.severity == FindingSeverity.MINOR]

        if critical:
            lines.append(f"### CRITICAL FINDINGS ({len(critical)})")
            for f in critical:
                lines.append(f"- **{f.item_id}**: {f.description}")
                lines.append(f"  - Location: {f.location}")
                lines.append(f"  - Assigned: {f.assigned_to}")
            lines.append("")

        if major:
            lines.append(f"### Major Findings ({len(major)})")
            for f in major:
                lines.append(f"- **{f.item_id}**: {f.description}")
            lines.append("")

        if minor:
            lines.append(f"### Minor Findings ({len(minor)})")
            for f in minor:
                lines.append(f"- {f.item_id}: {f.description}")
            lines.append("")

        return "\n".join(lines)

    def generate_weekly_summary(self, project_id: str, week_start: datetime) -> Dict:
        """Generate weekly safety summary."""
        week_inspections = [
            insp for insp in self.inspections.values()
            if insp.project_id == project_id
            and insp.date >= week_start
        ]

        total_findings = sum(len([f for f in insp.findings if f.status == "fail"])
                            for insp in week_inspections)

        critical_count = sum(
            len([f for f in insp.findings if f.severity == FindingSeverity.CRITICAL])
            for insp in week_inspections
        )

        avg_score = sum(insp.overall_score for insp in week_inspections) / len(week_inspections) if week_inspections else 0

        return {
            "week_start": week_start.isoformat(),
            "inspections_conducted": len(week_inspections),
            "total_findings": total_findings,
            "critical_findings": critical_count,
            "average_score": avg_score,
            "trend": "improving" if avg_score > 85 else "needs_attention"
        }
```

## Quick Start

```python
# Initialize manager
manager = SafetyInspectionManager()

# Create daily inspection
inspection = manager.create_inspection(
    inspection_type=InspectionType.DAILY_SITE,
    project_id="PRJ-001",
    project_name="Office Tower",
    location="Building A - Level 5",
    inspector="John Smith",
    weather="Clear, 72F",
    workers=45
)

# Get checklist items
checklist = manager.get_checklist(InspectionType.DAILY_SITE)
for item in checklist[:5]:
    print(f"{item.id}: {item.question}")

# Record findings
manager.record_finding(
    inspection.id,
    item_id="DS005",
    status="fail",
    severity=FindingSeverity.MAJOR,
    description="3 workers without safety glasses in welding area",
    location="Level 5, Grid C-4",
    assigned_to="Site Foreman"
)

# Calculate score and generate report
score = manager.calculate_score(inspection.id)
print(f"Inspection Score: {score:.1f}%")

report = manager.generate_report(inspection.id)
print(report)
```

## Integration with n8n

```json
{
  "workflow": "Safety Inspection Alert",
  "trigger": "New critical finding recorded",
  "nodes": [
    {"type": "Webhook", "event": "finding.critical"},
    {"type": "Email", "to": "safety@company.com", "subject": "CRITICAL Safety Finding"},
    {"type": "Slack", "channel": "#safety-alerts"},
    {"type": "Database", "action": "log_incident"}
  ]
}
```

## Requirements

```bash
pip install (no external dependencies - uses standard library)
```

## Resources

- OSHA Construction Standards: https://www.osha.gov/construction
- Safety inspection best practices
- Mobile inspection apps integration
