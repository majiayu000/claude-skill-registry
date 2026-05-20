---
slug: "as-built-tracker"
display_name: "As Built Tracker"
description: "Track as-built documentation and record drawings. Monitor submission status, manage revisions, and ensure completeness for handover."
---

# As-Built Documentation Tracker

## Business Case

### Problem Statement
As-built documentation challenges:
- Tracking hundreds of drawings
- Managing revisions
- Ensuring completeness
- Meeting handover deadlines

### Solution
Systematic tracking of as-built documentation submissions, revisions, and approval status.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class DocumentStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    RESUBMIT = "resubmit"


class DocumentType(Enum):
    ARCHITECTURAL = "architectural"
    STRUCTURAL = "structural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    CIVIL = "civil"
    LANDSCAPE = "landscape"
    SPECIFICATIONS = "specifications"
    O_AND_M = "o_and_m"


@dataclass
class AsBuiltDocument:
    document_id: str
    document_number: str
    title: str
    doc_type: DocumentType
    discipline: str
    contractor: str
    status: DocumentStatus
    current_revision: str
    required_date: date
    submitted_date: Optional[date] = None
    approved_date: Optional[date] = None
    reviewer: str = ""
    comments: str = ""
    file_path: str = ""


@dataclass
class DocumentSubmission:
    submission_id: str
    document_id: str
    revision: str
    submission_date: date
    submitted_by: str
    file_path: str
    status: DocumentStatus
    review_comments: str = ""


class AsBuiltTracker:
    """Track as-built documentation."""

    def __init__(self, project_name: str, handover_date: date):
        self.project_name = project_name
        self.handover_date = handover_date
        self.documents: Dict[str, AsBuiltDocument] = {}
        self.submissions: List[DocumentSubmission] = []
        self._next_id = 1

    def add_document(self,
                     document_number: str,
                     title: str,
                     doc_type: DocumentType,
                     discipline: str,
                     contractor: str,
                     required_date: date = None) -> AsBuiltDocument:
        """Add document to tracking."""

        doc_id = f"DOC-{self._next_id:04d}"
        self._next_id += 1

        if required_date is None:
            required_date = self.handover_date - timedelta(days=14)

        doc = AsBuiltDocument(
            document_id=doc_id,
            document_number=document_number,
            title=title,
            doc_type=doc_type,
            discipline=discipline,
            contractor=contractor,
            status=DocumentStatus.NOT_STARTED,
            current_revision="0",
            required_date=required_date
        )

        self.documents[doc_id] = doc
        return doc

    def import_document_list(self, df: pd.DataFrame):
        """Import document list from DataFrame."""

        for _, row in df.iterrows():
            doc_type = DocumentType(row.get('type', 'architectural').lower())
            req_date = pd.to_datetime(row.get('required_date', self.handover_date)).date() if 'required_date' in row else None

            self.add_document(
                document_number=str(row['document_number']),
                title=row['title'],
                doc_type=doc_type,
                discipline=row.get('discipline', ''),
                contractor=row.get('contractor', ''),
                required_date=req_date
            )

    def record_submission(self,
                          document_id: str,
                          revision: str,
                          submitted_by: str,
                          file_path: str = "") -> Optional[DocumentSubmission]:
        """Record document submission."""

        if document_id not in self.documents:
            return None

        doc = self.documents[document_id]

        submission = DocumentSubmission(
            submission_id=f"SUB-{len(self.submissions)+1:04d}",
            document_id=document_id,
            revision=revision,
            submission_date=date.today(),
            submitted_by=submitted_by,
            file_path=file_path,
            status=DocumentStatus.SUBMITTED
        )

        self.submissions.append(submission)

        # Update document
        doc.status = DocumentStatus.SUBMITTED
        doc.current_revision = revision
        doc.submitted_date = date.today()

        return submission

    def review_submission(self,
                          document_id: str,
                          approved: bool,
                          reviewer: str,
                          comments: str = ""):
        """Review submitted document."""

        if document_id not in self.documents:
            return

        doc = self.documents[document_id]

        if approved:
            doc.status = DocumentStatus.APPROVED
            doc.approved_date = date.today()
        else:
            doc.status = DocumentStatus.REJECTED

        doc.reviewer = reviewer
        doc.comments = comments

        # Update latest submission
        for sub in reversed(self.submissions):
            if sub.document_id == document_id:
                sub.status = DocumentStatus.APPROVED if approved else DocumentStatus.REJECTED
                sub.review_comments = comments
                break

    def get_summary(self) -> Dict[str, Any]:
        """Get documentation status summary."""

        docs = list(self.documents.values())
        today = date.today()

        # Status counts
        status_counts = {}
        for status in DocumentStatus:
            status_counts[status.value] = sum(1 for d in docs if d.status == status)

        # By type
        by_type = {}
        for doc_type in DocumentType:
            pending = sum(1 for d in docs if d.doc_type == doc_type and d.status != DocumentStatus.APPROVED)
            if pending > 0:
                by_type[doc_type.value] = pending

        # Overdue
        overdue = sum(
            1 for d in docs
            if d.required_date < today and d.status != DocumentStatus.APPROVED
        )

        # Completion rate
        approved = sum(1 for d in docs if d.status == DocumentStatus.APPROVED)
        completion = (approved / len(docs) * 100) if docs else 0

        return {
            'total_documents': len(docs),
            'approved': approved,
            'completion_rate': round(completion, 1),
            'by_status': status_counts,
            'by_type': by_type,
            'overdue': overdue,
            'days_to_handover': (self.handover_date - today).days
        }

    def get_contractor_status(self, contractor: str) -> Dict[str, Any]:
        """Get status for specific contractor."""

        docs = [d for d in self.documents.values() if d.contractor == contractor]

        approved = sum(1 for d in docs if d.status == DocumentStatus.APPROVED)
        pending = len(docs) - approved

        return {
            'contractor': contractor,
            'total': len(docs),
            'approved': approved,
            'pending': pending,
            'completion_rate': round(approved / len(docs) * 100, 1) if docs else 0
        }

    def get_overdue_documents(self) -> List[Dict[str, Any]]:
        """Get overdue documents."""

        today = date.today()
        overdue = []

        for doc in self.documents.values():
            if doc.required_date < today and doc.status != DocumentStatus.APPROVED:
                overdue.append({
                    'document_id': doc.document_id,
                    'document_number': doc.document_number,
                    'title': doc.title,
                    'contractor': doc.contractor,
                    'required_date': doc.required_date,
                    'days_overdue': (today - doc.required_date).days,
                    'status': doc.status.value
                })

        return sorted(overdue, key=lambda x: x['days_overdue'], reverse=True)

    def forecast_completion(self) -> Dict[str, Any]:
        """Forecast documentation completion."""

        summary = self.get_summary()
        pending = summary['total_documents'] - summary['approved']

        # Calculate submission rate
        recent_approvals = sum(
            1 for d in self.documents.values()
            if d.approved_date and d.approved_date >= date.today() - timedelta(days=14)
        )
        weekly_rate = recent_approvals / 2 if recent_approvals > 0 else 1

        weeks_needed = pending / weekly_rate if weekly_rate > 0 else pending
        projected_completion = date.today() + timedelta(weeks=weeks_needed)

        return {
            'pending_documents': pending,
            'approval_rate_per_week': round(weekly_rate, 1),
            'weeks_needed': round(weeks_needed, 1),
            'projected_completion': projected_completion,
            'handover_date': self.handover_date,
            'on_track': projected_completion <= self.handover_date
        }

    def generate_transmittal(self,
                              document_ids: List[str],
                              to: str,
                              subject: str) -> Dict[str, Any]:
        """Generate transmittal for documents."""

        docs = [self.documents[d] for d in document_ids if d in self.documents]

        return {
            'transmittal_number': f"TR-{date.today().strftime('%Y%m%d')}-001",
            'date': date.today(),
            'from': self.project_name,
            'to': to,
            'subject': subject,
            'documents': [
                {
                    'number': d.document_number,
                    'title': d.title,
                    'revision': d.current_revision
                }
                for d in docs
            ],
            'document_count': len(docs)
        }

    def export_to_excel(self, output_path: str) -> str:
        """Export tracking to Excel."""

        summary = self.get_summary()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': self.project_name,
                'Handover Date': self.handover_date,
                'Total Documents': summary['total_documents'],
                'Approved': summary['approved'],
                'Completion %': summary['completion_rate'],
                'Overdue': summary['overdue'],
                'Days to Handover': summary['days_to_handover']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # All Documents
            docs_df = pd.DataFrame([
                {
                    'ID': d.document_id,
                    'Number': d.document_number,
                    'Title': d.title,
                    'Type': d.doc_type.value,
                    'Discipline': d.discipline,
                    'Contractor': d.contractor,
                    'Status': d.status.value,
                    'Revision': d.current_revision,
                    'Required': d.required_date,
                    'Submitted': d.submitted_date,
                    'Approved': d.approved_date
                }
                for d in self.documents.values()
            ])
            docs_df.to_excel(writer, sheet_name='Documents', index=False)

            # Overdue
            overdue = self.get_overdue_documents()
            if overdue:
                overdue_df = pd.DataFrame(overdue)
                overdue_df.to_excel(writer, sheet_name='Overdue', index=False)

            # By Contractor
            contractors = set(d.contractor for d in self.documents.values())
            contractor_data = [self.get_contractor_status(c) for c in contractors]
            if contractor_data:
                contractor_df = pd.DataFrame(contractor_data)
                contractor_df.to_excel(writer, sheet_name='By Contractor', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

# Initialize tracker
tracker = AsBuiltTracker("Office Building A", handover_date=date(2024, 12, 31))

# Add documents
tracker.add_document(
    document_number="A-001",
    title="Floor Plans Level 1-5",
    doc_type=DocumentType.ARCHITECTURAL,
    discipline="Architecture",
    contractor="ABC Architects"
)

tracker.add_document(
    document_number="M-001",
    title="HVAC Layout",
    doc_type=DocumentType.MECHANICAL,
    discipline="HVAC",
    contractor="XYZ MEP"
)

# Record submission
tracker.record_submission("DOC-0001", revision="A", submitted_by="John Smith")

# Review
tracker.review_submission("DOC-0001", approved=True, reviewer="PM", comments="Approved")
```

## Common Use Cases

### 1. Status Summary
```python
summary = tracker.get_summary()
print(f"Completion: {summary['completion_rate']}%")
print(f"Overdue: {summary['overdue']}")
```

### 2. Contractor Report
```python
status = tracker.get_contractor_status("ABC Architects")
print(f"Pending: {status['pending']}")
```

### 3. Forecast
```python
forecast = tracker.forecast_completion()
print(f"On Track: {forecast['on_track']}")
```

## Resources
- **DDC Book**: Chapter 5.1 - Documentation Management
