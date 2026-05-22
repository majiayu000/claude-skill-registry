---
name: "quality-control-workflow"
description: "Construction quality control workflow automation. Manage QC inspections, track defects, generate NCRs, and ensure specification compliance throughout the project."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🦺", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Quality Control Workflow

## Overview

Automate construction quality control workflows from inspection planning through defect resolution. Track quality metrics, manage non-conformance reports (NCRs), and ensure specification compliance.

> "Structured QC workflows reduce rework by 40% and improve first-time quality" — DDC Community

## QC Workflow Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                    QC WORKFLOW PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Plan        →    Inspect    →    Document    →    Resolve      │
│  ────             ───────         ────────         ───────      │
│  📋 ITP           🔍 Check        📝 NCR           🔧 Fix        │
│  📅 Schedule      📸 Photo        📊 Log           ✅ Verify     │
│  👥 Assign        📏 Measure      📧 Notify        📈 Close      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import json

class QCStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    ON_HOLD = "on_hold"

class DefectSeverity(Enum):
    CRITICAL = "critical"  # Stop work, structural/safety issue
    MAJOR = "major"        # Must fix before cover-up
    MINOR = "minor"        # Fix before completion
    COSMETIC = "cosmetic"  # Punch list item

class NCRStatus(Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    ACCEPTED = "accepted"
    DISPUTED = "disputed"
    IN_REMEDIATION = "in_remediation"
    VERIFIED = "verified"
    CLOSED = "closed"

@dataclass
class InspectionPoint:
    id: str
    name: str
    spec_reference: str
    acceptance_criteria: str
    inspection_method: str
    hold_point: bool = False  # Requires sign-off before proceeding
    witness_point: bool = False  # Client/engineer may witness

@dataclass
class QCInspection:
    id: str
    inspection_point: InspectionPoint
    location: str
    scheduled_date: datetime
    inspector: str
    status: QCStatus = QCStatus.PENDING
    actual_date: Optional[datetime] = None
    result: str = ""
    measurements: Dict[str, float] = field(default_factory=dict)
    photos: List[str] = field(default_factory=list)
    notes: str = ""
    sign_off_by: str = ""

@dataclass
class Defect:
    id: str
    inspection_id: str
    description: str
    location: str
    severity: DefectSeverity
    spec_reference: str
    photos: List[str] = field(default_factory=list)
    assigned_to: str = ""
    due_date: Optional[datetime] = None
    status: str = "open"
    root_cause: str = ""
    corrective_action: str = ""
    verified_by: str = ""
    closed_date: Optional[datetime] = None

@dataclass
class NonConformanceReport:
    id: str
    defect_ids: List[str]
    title: str
    description: str
    contractor: str
    spec_sections: List[str]
    status: NCRStatus = NCRStatus.DRAFT
    issued_date: Optional[datetime] = None
    response_due: Optional[datetime] = None
    contractor_response: str = ""
    remediation_plan: str = ""
    cost_impact: float = 0.0
    schedule_impact_days: int = 0

class QualityControlManager:
    """Manage construction quality control workflow."""

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name
        self.inspection_points: Dict[str, InspectionPoint] = {}
        self.inspections: Dict[str, QCInspection] = {}
        self.defects: Dict[str, Defect] = {}
        self.ncrs: Dict[str, NonConformanceReport] = {}

    def create_itp(self, work_package: str, inspection_points: List[Dict]) -> List[InspectionPoint]:
        """Create Inspection and Test Plan (ITP)."""
        created = []
        for idx, point in enumerate(inspection_points):
            ip = InspectionPoint(
                id=f"{work_package}-{idx+1:03d}",
                name=point['name'],
                spec_reference=point.get('spec_ref', ''),
                acceptance_criteria=point.get('criteria', ''),
                inspection_method=point.get('method', 'Visual'),
                hold_point=point.get('hold_point', False),
                witness_point=point.get('witness_point', False)
            )
            self.inspection_points[ip.id] = ip
            created.append(ip)
        return created

    def schedule_inspection(self, inspection_point_id: str, location: str,
                           scheduled_date: datetime, inspector: str) -> QCInspection:
        """Schedule a QC inspection."""
        if inspection_point_id not in self.inspection_points:
            raise ValueError(f"Inspection point {inspection_point_id} not found")

        inspection_id = f"QCI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        inspection = QCInspection(
            id=inspection_id,
            inspection_point=self.inspection_points[inspection_point_id],
            location=location,
            scheduled_date=scheduled_date,
            inspector=inspector
        )
        self.inspections[inspection_id] = inspection
        return inspection

    def conduct_inspection(self, inspection_id: str, result: str,
                          measurements: Dict[str, float] = None,
                          photos: List[str] = None,
                          notes: str = "") -> QCInspection:
        """Record inspection results."""
        if inspection_id not in self.inspections:
            raise ValueError(f"Inspection {inspection_id} not found")

        inspection = self.inspections[inspection_id]
        inspection.actual_date = datetime.now()
        inspection.result = result
        inspection.measurements = measurements or {}
        inspection.photos = photos or []
        inspection.notes = notes
        inspection.status = QCStatus.PASSED if result == "pass" else QCStatus.FAILED

        return inspection

    def record_defect(self, inspection_id: str, description: str,
                     location: str, severity: DefectSeverity,
                     spec_reference: str, photos: List[str] = None,
                     assigned_to: str = "") -> Defect:
        """Record a defect from inspection."""
        defect_id = f"DEF-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Set due date based on severity
        due_days = {
            DefectSeverity.CRITICAL: 1,
            DefectSeverity.MAJOR: 3,
            DefectSeverity.MINOR: 7,
            DefectSeverity.COSMETIC: 14
        }

        defect = Defect(
            id=defect_id,
            inspection_id=inspection_id,
            description=description,
            location=location,
            severity=severity,
            spec_reference=spec_reference,
            photos=photos or [],
            assigned_to=assigned_to,
            due_date=datetime.now() + timedelta(days=due_days[severity])
        )

        self.defects[defect_id] = defect
        return defect

    def create_ncr(self, defect_ids: List[str], title: str,
                  contractor: str, description: str = "") -> NonConformanceReport:
        """Create Non-Conformance Report from defects."""
        ncr_id = f"NCR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Collect spec references from defects
        spec_sections = []
        for def_id in defect_ids:
            if def_id in self.defects:
                spec_sections.append(self.defects[def_id].spec_reference)

        ncr = NonConformanceReport(
            id=ncr_id,
            defect_ids=defect_ids,
            title=title,
            description=description or self._generate_ncr_description(defect_ids),
            contractor=contractor,
            spec_sections=list(set(spec_sections)),
            response_due=datetime.now() + timedelta(days=5)
        )

        self.ncrs[ncr_id] = ncr
        return ncr

    def _generate_ncr_description(self, defect_ids: List[str]) -> str:
        """Generate NCR description from defects."""
        lines = ["The following non-conformances have been identified:", ""]
        for def_id in defect_ids:
            if def_id in self.defects:
                d = self.defects[def_id]
                lines.append(f"- {d.description} at {d.location}")
                lines.append(f"  Reference: {d.spec_reference}")
        return "\n".join(lines)

    def issue_ncr(self, ncr_id: str) -> NonConformanceReport:
        """Issue NCR to contractor."""
        if ncr_id not in self.ncrs:
            raise ValueError(f"NCR {ncr_id} not found")

        ncr = self.ncrs[ncr_id]
        ncr.status = NCRStatus.ISSUED
        ncr.issued_date = datetime.now()
        return ncr

    def record_ncr_response(self, ncr_id: str, response: str,
                           remediation_plan: str, cost_impact: float = 0,
                           schedule_impact: int = 0) -> NonConformanceReport:
        """Record contractor response to NCR."""
        if ncr_id not in self.ncrs:
            raise ValueError(f"NCR {ncr_id} not found")

        ncr = self.ncrs[ncr_id]
        ncr.contractor_response = response
        ncr.remediation_plan = remediation_plan
        ncr.cost_impact = cost_impact
        ncr.schedule_impact_days = schedule_impact
        ncr.status = NCRStatus.ACCEPTED
        return ncr

    def verify_remediation(self, ncr_id: str, verified_by: str) -> NonConformanceReport:
        """Verify NCR remediation is complete."""
        if ncr_id not in self.ncrs:
            raise ValueError(f"NCR {ncr_id} not found")

        ncr = self.ncrs[ncr_id]
        ncr.status = NCRStatus.VERIFIED

        # Close associated defects
        for def_id in ncr.defect_ids:
            if def_id in self.defects:
                self.defects[def_id].status = "closed"
                self.defects[def_id].verified_by = verified_by
                self.defects[def_id].closed_date = datetime.now()

        return ncr

    def get_quality_metrics(self) -> Dict:
        """Calculate quality metrics."""
        total_inspections = len(self.inspections)
        passed = len([i for i in self.inspections.values() if i.status == QCStatus.PASSED])
        failed = len([i for i in self.inspections.values() if i.status == QCStatus.FAILED])

        open_defects = len([d for d in self.defects.values() if d.status == "open"])
        overdue_defects = len([d for d in self.defects.values()
                              if d.status == "open" and d.due_date and d.due_date < datetime.now()])

        open_ncrs = len([n for n in self.ncrs.values()
                        if n.status not in [NCRStatus.VERIFIED, NCRStatus.CLOSED]])

        return {
            "total_inspections": total_inspections,
            "passed_inspections": passed,
            "failed_inspections": failed,
            "first_time_pass_rate": (passed / total_inspections * 100) if total_inspections else 0,
            "open_defects": open_defects,
            "overdue_defects": overdue_defects,
            "open_ncrs": open_ncrs,
            "total_cost_impact": sum(n.cost_impact for n in self.ncrs.values()),
            "total_schedule_impact": sum(n.schedule_impact_days for n in self.ncrs.values())
        }

    def generate_qc_report(self) -> str:
        """Generate QC status report."""
        metrics = self.get_quality_metrics()

        lines = [
            f"# Quality Control Report",
            f"",
            f"**Project:** {self.project_name}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"",
            f"## Summary Metrics",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| First-Time Pass Rate | {metrics['first_time_pass_rate']:.1f}% |",
            f"| Open Defects | {metrics['open_defects']} |",
            f"| Overdue Defects | {metrics['overdue_defects']} |",
            f"| Open NCRs | {metrics['open_ncrs']} |",
            f"| Cost Impact | ${metrics['total_cost_impact']:,.0f} |",
            f"| Schedule Impact | {metrics['total_schedule_impact']} days |",
            f"",
        ]

        # Critical defects
        critical = [d for d in self.defects.values()
                   if d.severity == DefectSeverity.CRITICAL and d.status == "open"]
        if critical:
            lines.append("## Critical Open Defects")
            for d in critical:
                lines.append(f"- **{d.id}**: {d.description}")
                lines.append(f"  - Location: {d.location}")
                lines.append(f"  - Due: {d.due_date.strftime('%Y-%m-%d') if d.due_date else 'N/A'}")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize QC Manager
qc = QualityControlManager("PRJ-001", "Office Tower")

# Create Inspection Test Plan
concrete_itp = qc.create_itp("CONC", [
    {"name": "Rebar placement", "spec_ref": "03200", "criteria": "Per drawings", "hold_point": True},
    {"name": "Concrete placement", "spec_ref": "03300", "criteria": "Slump 4-6 inches"},
    {"name": "Concrete finish", "spec_ref": "03350", "criteria": "Level within 1/8 inch"},
])

# Schedule inspection
inspection = qc.schedule_inspection(
    "CONC-001",
    location="Level 3, Grid A-C",
    scheduled_date=datetime.now(),
    inspector="QC Engineer"
)

# Conduct inspection (found defect)
qc.conduct_inspection(inspection.id, result="fail", notes="Rebar spacing incorrect")

# Record defect
defect = qc.record_defect(
    inspection.id,
    description="Rebar spacing 8 inches instead of 6 inches per spec",
    location="Level 3, Grid B-2",
    severity=DefectSeverity.MAJOR,
    spec_reference="03200-3.2",
    assigned_to="ABC Concrete"
)

# Create NCR
ncr = qc.create_ncr([defect.id], "Rebar Spacing Non-Conformance", "ABC Concrete")
qc.issue_ncr(ncr.id)

# Get metrics
print(qc.generate_qc_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
