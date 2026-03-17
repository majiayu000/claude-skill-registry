---
slug: "permit-tracking-automation"
display_name: "Permit Tracking Automation"
description: "Automate construction permit tracking and management. Monitor application status, track renewal deadlines, manage document requirements, and integrate with municipal systems."
---

# Permit Tracking Automation

## Overview

This skill implements automated permit tracking for construction projects. Monitor permit status, manage document requirements, track deadlines, and integrate with local authority systems.

**Capabilities:**
- Permit application tracking
- Document management
- Deadline monitoring
- Status notifications
- Compliance checking
- Renewal automation

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class PermitType(Enum):
    BUILDING = "building"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    MECHANICAL = "mechanical"
    FIRE = "fire"
    DEMOLITION = "demolition"
    EXCAVATION = "excavation"
    OCCUPANCY = "occupancy"
    ENVIRONMENTAL = "environmental"
    SPECIAL_USE = "special_use"

class PermitStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REVISION_REQUIRED = "revision_required"
    APPROVED = "approved"
    ISSUED = "issued"
    ACTIVE = "active"
    EXPIRED = "expired"
    CLOSED = "closed"

@dataclass
class Permit:
    permit_id: str
    permit_type: PermitType
    jurisdiction: str
    status: PermitStatus
    application_date: date
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    description: str = ""
    required_documents: List[str] = field(default_factory=list)
    submitted_documents: List[str] = field(default_factory=list)

def check_permit_status(permit: Permit) -> Dict:
    """Check permit status and upcoming deadlines"""
    today = date.today()
    alerts = []

    # Check expiry
    if permit.expiry_date:
        days_to_expiry = (permit.expiry_date - today).days
        if days_to_expiry < 0:
            alerts.append({'type': 'expired', 'message': 'Permit has expired'})
        elif days_to_expiry <= 30:
            alerts.append({'type': 'expiring_soon', 'days': days_to_expiry})

    # Check missing documents
    missing_docs = set(permit.required_documents) - set(permit.submitted_documents)
    if missing_docs:
        alerts.append({'type': 'missing_documents', 'documents': list(missing_docs)})

    return {
        'permit_id': permit.permit_id,
        'status': permit.status.value,
        'alerts': alerts,
        'is_valid': permit.status in [PermitStatus.ACTIVE, PermitStatus.ISSUED] and
                   (permit.expiry_date is None or permit.expiry_date >= today)
    }

# Example
permit = Permit(
    permit_id="BP-2024-001",
    permit_type=PermitType.BUILDING,
    jurisdiction="City of Moscow",
    status=PermitStatus.ACTIVE,
    application_date=date(2024, 1, 15),
    issued_date=date(2024, 2, 1),
    expiry_date=date.today() + timedelta(days=25),
    required_documents=["drawings", "specs", "survey"],
    submitted_documents=["drawings", "specs"]
)

status = check_permit_status(permit)
print(f"Valid: {status['is_valid']}, Alerts: {status['alerts']}")
```

## Comprehensive Permit Management System

### Permit Data Model

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import uuid

@dataclass
class Jurisdiction:
    jurisdiction_id: str
    name: str
    region: str
    country: str
    permit_portal_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    typical_review_days: Dict[str, int] = field(default_factory=dict)

@dataclass
class RequiredDocument:
    document_id: str
    document_type: str
    description: str
    is_mandatory: bool = True
    format_requirements: str = ""
    template_url: Optional[str] = None

@dataclass
class SubmittedDocument:
    document_id: str
    document_type: str
    filename: str
    file_path: str
    submitted_date: date
    version: int = 1
    status: str = "submitted"  # submitted, accepted, rejected
    reviewer_comments: str = ""

@dataclass
class Inspection:
    inspection_id: str
    inspection_type: str
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    inspector: str = ""
    result: str = ""  # passed, failed, conditional
    notes: str = ""
    required_corrections: List[str] = field(default_factory=list)

@dataclass
class Fee:
    fee_id: str
    fee_type: str
    amount: float
    due_date: date
    paid_date: Optional[date] = None
    receipt_number: str = ""

@dataclass
class PermitApplication:
    # Identification
    application_id: str
    permit_number: Optional[str] = None
    permit_type: PermitType = PermitType.BUILDING
    jurisdiction: Jurisdiction = None

    # Project reference
    project_id: str = ""
    project_name: str = ""
    project_address: str = ""
    parcel_number: str = ""

    # Applicant
    applicant_name: str = ""
    applicant_company: str = ""
    applicant_license: str = ""
    owner_name: str = ""

    # Status
    status: PermitStatus = PermitStatus.DRAFT
    current_phase: str = ""
    submission_date: Optional[date] = None
    approval_date: Optional[date] = None
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None

    # Work scope
    work_description: str = ""
    project_value: float = 0
    building_area_sqm: float = 0
    occupancy_type: str = ""

    # Documents
    required_documents: List[RequiredDocument] = field(default_factory=list)
    submitted_documents: List[SubmittedDocument] = field(default_factory=list)

    # Inspections
    inspections: List[Inspection] = field(default_factory=list)

    # Fees
    fees: List[Fee] = field(default_factory=list)

    # Timeline
    review_comments: List[Dict] = field(default_factory=list)
    status_history: List[Dict] = field(default_factory=list)

    def get_document_status(self) -> Dict:
        """Get document submission status"""
        required_types = {d.document_type for d in self.required_documents if d.is_mandatory}
        submitted_types = {d.document_type for d in self.submitted_documents}

        return {
            'required': len(required_types),
            'submitted': len(submitted_types),
            'missing': list(required_types - submitted_types),
            'complete': required_types.issubset(submitted_types)
        }

    def get_fee_status(self) -> Dict:
        """Get fee payment status"""
        total = sum(f.amount for f in self.fees)
        paid = sum(f.amount for f in self.fees if f.paid_date)
        overdue = [f for f in self.fees if not f.paid_date and f.due_date < date.today()]

        return {
            'total_amount': total,
            'paid_amount': paid,
            'outstanding': total - paid,
            'overdue_fees': len(overdue)
        }
```

### Permit Tracking Engine

```python
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
import json

class PermitTracker:
    """Track and manage construction permits"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.applications: Dict[str, PermitApplication] = {}
        self.jurisdictions: Dict[str, Jurisdiction] = {}

    def add_jurisdiction(self, jurisdiction: Jurisdiction):
        """Register jurisdiction"""
        self.jurisdictions[jurisdiction.jurisdiction_id] = jurisdiction

    def create_application(self, permit_type: PermitType,
                          jurisdiction_id: str,
                          project_name: str,
                          project_address: str) -> PermitApplication:
        """Create new permit application"""
        jurisdiction = self.jurisdictions.get(jurisdiction_id)

        app = PermitApplication(
            application_id=f"APP-{uuid.uuid4().hex[:8].upper()}",
            permit_type=permit_type,
            jurisdiction=jurisdiction,
            project_id=self.project_id,
            project_name=project_name,
            project_address=project_address,
            status=PermitStatus.DRAFT
        )

        # Load required documents for permit type
        app.required_documents = self._get_required_documents(permit_type, jurisdiction_id)

        self.applications[app.application_id] = app
        return app

    def _get_required_documents(self, permit_type: PermitType,
                               jurisdiction_id: str) -> List[RequiredDocument]:
        """Get required documents for permit type"""
        # Standard requirements (would be loaded from database)
        base_requirements = {
            PermitType.BUILDING: [
                RequiredDocument("DOC-001", "site_plan", "Site plan showing property boundaries"),
                RequiredDocument("DOC-002", "floor_plans", "Architectural floor plans"),
                RequiredDocument("DOC-003", "elevations", "Building elevations"),
                RequiredDocument("DOC-004", "structural", "Structural drawings and calculations"),
                RequiredDocument("DOC-005", "title_survey", "Title survey"),
                RequiredDocument("DOC-006", "owner_auth", "Owner authorization letter"),
            ],
            PermitType.ELECTRICAL: [
                RequiredDocument("DOC-101", "electrical_plans", "Electrical plans"),
                RequiredDocument("DOC-102", "load_calculations", "Electrical load calculations"),
                RequiredDocument("DOC-103", "panel_schedule", "Panel schedule"),
            ],
            PermitType.PLUMBING: [
                RequiredDocument("DOC-201", "plumbing_plans", "Plumbing plans"),
                RequiredDocument("DOC-202", "fixture_schedule", "Fixture schedule"),
                RequiredDocument("DOC-203", "riser_diagrams", "Riser diagrams"),
            ]
        }

        return base_requirements.get(permit_type, [])

    def submit_application(self, application_id: str) -> Dict:
        """Submit permit application"""
        app = self.applications.get(application_id)
        if not app:
            return {'success': False, 'error': 'Application not found'}

        # Check documents
        doc_status = app.get_document_status()
        if not doc_status['complete']:
            return {
                'success': False,
                'error': 'Missing required documents',
                'missing': doc_status['missing']
            }

        # Update status
        app.status = PermitStatus.SUBMITTED
        app.submission_date = date.today()
        app.current_phase = "Initial Review"

        # Record history
        app.status_history.append({
            'date': date.today().isoformat(),
            'status': 'submitted',
            'notes': 'Application submitted for review'
        })

        # Calculate expected timeline
        jurisdiction = app.jurisdiction
        if jurisdiction and jurisdiction.typical_review_days:
            review_days = jurisdiction.typical_review_days.get(
                app.permit_type.value, 30
            )
            expected_decision = date.today() + timedelta(days=review_days)
        else:
            expected_decision = date.today() + timedelta(days=30)

        return {
            'success': True,
            'submission_date': app.submission_date.isoformat(),
            'expected_decision': expected_decision.isoformat()
        }

    def update_status(self, application_id: str, new_status: PermitStatus,
                     notes: str = "", reviewer: str = ""):
        """Update application status"""
        app = self.applications.get(application_id)
        if not app:
            return

        old_status = app.status
        app.status = new_status

        if new_status == PermitStatus.APPROVED:
            app.approval_date = date.today()
        elif new_status == PermitStatus.ISSUED:
            app.issued_date = date.today()
            app.permit_number = f"P-{date.today().year}-{len(self.applications):05d}"
            # Set expiry (typically 1-2 years)
            app.expiry_date = date.today() + timedelta(days=365)

        app.status_history.append({
            'date': date.today().isoformat(),
            'from_status': old_status.value,
            'to_status': new_status.value,
            'notes': notes,
            'reviewer': reviewer
        })

    def add_document(self, application_id: str, document_type: str,
                    filename: str, file_path: str) -> SubmittedDocument:
        """Add document to application"""
        app = self.applications.get(application_id)
        if not app:
            return None

        # Check if updating existing document
        existing = [d for d in app.submitted_documents if d.document_type == document_type]
        version = max(d.version for d in existing) + 1 if existing else 1

        doc = SubmittedDocument(
            document_id=f"SUB-{uuid.uuid4().hex[:8].upper()}",
            document_type=document_type,
            filename=filename,
            file_path=file_path,
            submitted_date=date.today(),
            version=version
        )

        app.submitted_documents.append(doc)
        return doc

    def schedule_inspection(self, application_id: str,
                           inspection_type: str,
                           requested_date: date) -> Inspection:
        """Schedule inspection"""
        app = self.applications.get(application_id)
        if not app:
            return None

        inspection = Inspection(
            inspection_id=f"INS-{uuid.uuid4().hex[:8].upper()}",
            inspection_type=inspection_type,
            scheduled_date=requested_date
        )

        app.inspections.append(inspection)
        return inspection

    def record_inspection_result(self, application_id: str,
                                inspection_id: str,
                                result: str,
                                notes: str = "",
                                corrections: List[str] = None):
        """Record inspection result"""
        app = self.applications.get(application_id)
        if not app:
            return

        for inspection in app.inspections:
            if inspection.inspection_id == inspection_id:
                inspection.completed_date = date.today()
                inspection.result = result
                inspection.notes = notes
                if corrections:
                    inspection.required_corrections = corrections
                break
```

### Deadline Monitoring

```python
from datetime import date, timedelta
from typing import List, Dict

class DeadlineMonitor:
    """Monitor permit deadlines and send alerts"""

    def __init__(self, tracker: PermitTracker):
        self.tracker = tracker
        self.alert_thresholds = {
            'expiry': [90, 60, 30, 14, 7],  # Days before expiry
            'fee_due': [30, 14, 7, 1],  # Days before fee due
            'inspection': [7, 3, 1]  # Days before inspection
        }

    def check_all_deadlines(self) -> List[Dict]:
        """Check all permit deadlines"""
        alerts = []
        today = date.today()

        for app_id, app in self.tracker.applications.items():
            # Check expiry
            if app.expiry_date:
                days_to_expiry = (app.expiry_date - today).days
                for threshold in self.alert_thresholds['expiry']:
                    if days_to_expiry == threshold:
                        alerts.append({
                            'type': 'expiry_warning',
                            'application_id': app_id,
                            'permit_number': app.permit_number,
                            'permit_type': app.permit_type.value,
                            'expiry_date': app.expiry_date.isoformat(),
                            'days_remaining': days_to_expiry,
                            'priority': 'high' if days_to_expiry <= 14 else 'medium'
                        })
                        break

                if days_to_expiry < 0:
                    alerts.append({
                        'type': 'expired',
                        'application_id': app_id,
                        'permit_number': app.permit_number,
                        'permit_type': app.permit_type.value,
                        'expiry_date': app.expiry_date.isoformat(),
                        'days_overdue': abs(days_to_expiry),
                        'priority': 'critical'
                    })

            # Check fees
            for fee in app.fees:
                if not fee.paid_date:
                    days_to_due = (fee.due_date - today).days
                    for threshold in self.alert_thresholds['fee_due']:
                        if days_to_due == threshold:
                            alerts.append({
                                'type': 'fee_due',
                                'application_id': app_id,
                                'fee_type': fee.fee_type,
                                'amount': fee.amount,
                                'due_date': fee.due_date.isoformat(),
                                'days_remaining': days_to_due,
                                'priority': 'high' if days_to_due <= 7 else 'medium'
                            })
                            break

                    if days_to_due < 0:
                        alerts.append({
                            'type': 'fee_overdue',
                            'application_id': app_id,
                            'fee_type': fee.fee_type,
                            'amount': fee.amount,
                            'due_date': fee.due_date.isoformat(),
                            'days_overdue': abs(days_to_due),
                            'priority': 'critical'
                        })

            # Check inspections
            for inspection in app.inspections:
                if inspection.scheduled_date and not inspection.completed_date:
                    days_to_inspection = (inspection.scheduled_date - today).days
                    for threshold in self.alert_thresholds['inspection']:
                        if days_to_inspection == threshold:
                            alerts.append({
                                'type': 'upcoming_inspection',
                                'application_id': app_id,
                                'inspection_type': inspection.inspection_type,
                                'scheduled_date': inspection.scheduled_date.isoformat(),
                                'days_remaining': days_to_inspection,
                                'priority': 'medium'
                            })
                            break

        return sorted(alerts, key=lambda x: (
            0 if x['priority'] == 'critical' else 1 if x['priority'] == 'high' else 2
        ))

    def get_permit_calendar(self, months_ahead: int = 3) -> Dict[str, List[Dict]]:
        """Get calendar of permit events"""
        today = date.today()
        end_date = today + timedelta(days=months_ahead * 30)

        calendar = {}

        for app_id, app in self.tracker.applications.items():
            # Expiry dates
            if app.expiry_date and today <= app.expiry_date <= end_date:
                date_str = app.expiry_date.isoformat()
                if date_str not in calendar:
                    calendar[date_str] = []
                calendar[date_str].append({
                    'type': 'expiry',
                    'application_id': app_id,
                    'description': f"{app.permit_type.value} permit expires"
                })

            # Inspections
            for inspection in app.inspections:
                if (inspection.scheduled_date and
                    not inspection.completed_date and
                    today <= inspection.scheduled_date <= end_date):
                    date_str = inspection.scheduled_date.isoformat()
                    if date_str not in calendar:
                        calendar[date_str] = []
                    calendar[date_str].append({
                        'type': 'inspection',
                        'application_id': app_id,
                        'description': f"{inspection.inspection_type} inspection"
                    })

            # Fee due dates
            for fee in app.fees:
                if not fee.paid_date and today <= fee.due_date <= end_date:
                    date_str = fee.due_date.isoformat()
                    if date_str not in calendar:
                        calendar[date_str] = []
                    calendar[date_str].append({
                        'type': 'fee_due',
                        'application_id': app_id,
                        'description': f"{fee.fee_type} fee ${fee.amount}"
                    })

        return dict(sorted(calendar.items()))
```

### Reporting

```python
import pandas as pd

def generate_permit_report(tracker: PermitTracker, output_path: str) -> str:
    """Generate permit status report"""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary
        summary_data = []
        for app in tracker.applications.values():
            doc_status = app.get_document_status()
            fee_status = app.get_fee_status()

            summary_data.append({
                'Application ID': app.application_id,
                'Permit Number': app.permit_number or 'Pending',
                'Type': app.permit_type.value,
                'Status': app.status.value,
                'Submitted': app.submission_date,
                'Issued': app.issued_date,
                'Expires': app.expiry_date,
                'Documents': f"{doc_status['submitted']}/{doc_status['required']}",
                'Fees Outstanding': fee_status['outstanding']
            })

        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

        # Status by type
        by_type = {}
        for app in tracker.applications.values():
            t = app.permit_type.value
            if t not in by_type:
                by_type[t] = {'total': 0, 'active': 0, 'pending': 0}
            by_type[t]['total'] += 1
            if app.status == PermitStatus.ACTIVE:
                by_type[t]['active'] += 1
            elif app.status in [PermitStatus.SUBMITTED, PermitStatus.UNDER_REVIEW]:
                by_type[t]['pending'] += 1

        pd.DataFrame(by_type).T.to_excel(writer, sheet_name='By_Type')

    return output_path
```

## Quick Reference

| Permit Type | Typical Documents | Review Time |
|-------------|-------------------|-------------|
| Building | Site plan, drawings, calculations | 2-8 weeks |
| Electrical | E-plans, load calc, panel schedule | 1-4 weeks |
| Plumbing | P-plans, fixture schedule, risers | 1-4 weeks |
| Mechanical | M-plans, equipment schedule | 1-4 weeks |
| Fire | Fire alarm, sprinkler plans | 2-6 weeks |
| Demolition | Demo plan, survey, abatement | 1-3 weeks |

## Resources

- **International Building Code (IBC)**: Building standards
- **Local AHJ Websites**: Authority Having Jurisdiction portals
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `document-classification-nlp` for document processing
- See `n8n-workflow-automation` for notification workflows
- See `safety-compliance-checker` for inspection integration
