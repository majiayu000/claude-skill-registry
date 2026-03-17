---
slug: "rfi-management"
display_name: "Rfi Management"
description: "Complete RFI (Request for Information) management system. Create, track, route, and analyze RFIs with automatic notifications and response deadline tracking."
---

# RFI Management System for Construction

Comprehensive system for managing Requests for Information (RFIs) throughout the construction project lifecycle.

## Business Case

**Problem**: RFI management is chaotic:
- RFIs get lost in email threads
- Response deadlines missed
- No visibility into RFI status
- Difficult to track cost/schedule impacts
- Manual logging wastes hours weekly

**Solution**: Structured RFI management that:
- Auto-assigns RFI numbers
- Routes to correct parties
- Tracks response deadlines
- Sends automatic reminders
- Maintains audit trail
- Analyzes trends and impacts

**ROI**: 60% faster RFI response time, 90% reduction in lost RFIs

## RFI Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│                        RFI LIFECYCLE                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│   │ CREATE  │───►│ SUBMIT  │───►│ REVIEW  │───►│ RESPOND │          │
│   │         │    │         │    │         │    │         │          │
│   │ • Draft │    │ • Route │    │ • Assign│    │ • Answer│          │
│   │ • Attach│    │ • Notify│    │ • Track │    │ • Approve│         │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
│        │              │              │              │                │
│        ▼              ▼              ▼              ▼                │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    RFI DATABASE                              │   │
│   │  • RFI Log        • Attachments      • Response History     │   │
│   │  • Status Track   • Cost Impacts     • Schedule Impacts     │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                         │
│   │ CLOSE   │◄───│ VERIFY  │◄───│IMPLEMENT│                         │
│   │         │    │         │    │         │                         │
│   │ • Archive│   │ • Check │    │ • Action│                         │
│   │ • Report│    │ • Accept│    │ • Update│                         │
│   └─────────┘    └─────────┘    └─────────┘                         │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Structure

### RFI Log Schema

```python
RFI_SCHEMA = {
    # Identification
    'rfi_number': str,          # RFI-001, RFI-002, etc.
    'project_id': str,          # Project identifier
    'revision': int,            # Revision number (0, 1, 2...)

    # Description
    'subject': str,             # Brief title
    'question': str,            # Detailed question
    'spec_section': str,        # CSI spec reference
    'drawing_ref': str,         # Drawing reference (A-101, S-201)
    'location': str,            # Building/floor/area

    # Parties
    'submitted_by': str,        # Originator name
    'submitted_by_company': str,# Originator company
    'assigned_to': str,         # Responsible party
    'cc_list': list,            # Additional recipients

    # Dates
    'date_submitted': date,     # When submitted
    'date_required': date,      # When response needed
    'date_responded': date,     # When answered
    'date_closed': date,        # When closed

    # Status
    'status': str,              # Draft/Open/Pending/Answered/Closed
    'priority': str,            # Critical/High/Medium/Low

    # Response
    'response': str,            # Answer text
    'response_by': str,         # Who answered
    'attachments': list,        # File links

    # Impact
    'cost_impact': bool,        # Has cost impact?
    'cost_amount': float,       # Estimated cost
    'schedule_impact': bool,    # Has schedule impact?
    'schedule_days': int,       # Days of delay
    'change_order_ref': str,    # Related CO number
}
```

## Python Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from enum import Enum
import uuid

class RFIStatus(Enum):
    DRAFT = "Draft"
    OPEN = "Open"
    PENDING = "Pending Review"
    ANSWERED = "Answered"
    CLOSED = "Closed"
    VOID = "Void"

class RFIPriority(Enum):
    CRITICAL = "Critical"  # Stops work
    HIGH = "High"          # Impacts critical path
    MEDIUM = "Medium"      # Standard
    LOW = "Low"            # Informational

@dataclass
class RFI:
    """Request for Information data class"""
    rfi_number: str
    project_id: str
    subject: str
    question: str

    # Optional fields with defaults
    spec_section: str = ""
    drawing_ref: str = ""
    location: str = ""
    submitted_by: str = ""
    submitted_by_company: str = ""
    assigned_to: str = ""
    cc_list: List[str] = field(default_factory=list)

    date_submitted: date = field(default_factory=date.today)
    date_required: date = None
    date_responded: date = None
    date_closed: date = None

    status: RFIStatus = RFIStatus.DRAFT
    priority: RFIPriority = RFIPriority.MEDIUM

    response: str = ""
    response_by: str = ""
    attachments: List[str] = field(default_factory=list)

    cost_impact: bool = False
    cost_amount: float = 0.0
    schedule_impact: bool = False
    schedule_days: int = 0
    change_order_ref: str = ""

    revision: int = 0

    def __post_init__(self):
        if self.date_required is None:
            # Default: 7 days for response
            self.date_required = self.date_submitted + timedelta(days=7)


class RFIManager:
    """Complete RFI management system"""

    def __init__(self, project_id: str, storage_path: str = None):
        self.project_id = project_id
        self.storage_path = storage_path or f"rfi_log_{project_id}.xlsx"
        self.rfis: Dict[str, RFI] = {}
        self._load_rfis()

    def _load_rfis(self):
        """Load RFIs from storage"""
        try:
            df = pd.read_excel(self.storage_path)
            for _, row in df.iterrows():
                rfi = RFI(
                    rfi_number=row['rfi_number'],
                    project_id=row['project_id'],
                    subject=row['subject'],
                    question=row['question'],
                    status=RFIStatus(row['status']),
                    priority=RFIPriority(row.get('priority', 'Medium'))
                )
                self.rfis[rfi.rfi_number] = rfi
        except FileNotFoundError:
            pass

    def _save_rfis(self):
        """Save RFIs to storage"""
        records = []
        for rfi in self.rfis.values():
            records.append({
                'rfi_number': rfi.rfi_number,
                'project_id': rfi.project_id,
                'subject': rfi.subject,
                'question': rfi.question,
                'spec_section': rfi.spec_section,
                'drawing_ref': rfi.drawing_ref,
                'location': rfi.location,
                'submitted_by': rfi.submitted_by,
                'submitted_by_company': rfi.submitted_by_company,
                'assigned_to': rfi.assigned_to,
                'date_submitted': rfi.date_submitted,
                'date_required': rfi.date_required,
                'date_responded': rfi.date_responded,
                'date_closed': rfi.date_closed,
                'status': rfi.status.value,
                'priority': rfi.priority.value,
                'response': rfi.response,
                'response_by': rfi.response_by,
                'cost_impact': rfi.cost_impact,
                'cost_amount': rfi.cost_amount,
                'schedule_impact': rfi.schedule_impact,
                'schedule_days': rfi.schedule_days,
                'change_order_ref': rfi.change_order_ref
            })

        df = pd.DataFrame(records)
        df.to_excel(self.storage_path, index=False)

    def _get_next_number(self) -> str:
        """Generate next RFI number"""
        existing = [int(r.rfi_number.split('-')[1])
                   for r in self.rfis.values()
                   if r.rfi_number.startswith('RFI-')]
        next_num = max(existing, default=0) + 1
        return f"RFI-{next_num:04d}"

    def create_rfi(
        self,
        subject: str,
        question: str,
        submitted_by: str,
        submitted_by_company: str,
        assigned_to: str,
        spec_section: str = "",
        drawing_ref: str = "",
        location: str = "",
        priority: RFIPriority = RFIPriority.MEDIUM,
        days_for_response: int = 7,
        attachments: List[str] = None
    ) -> RFI:
        """Create new RFI"""

        rfi_number = self._get_next_number()

        rfi = RFI(
            rfi_number=rfi_number,
            project_id=self.project_id,
            subject=subject,
            question=question,
            spec_section=spec_section,
            drawing_ref=drawing_ref,
            location=location,
            submitted_by=submitted_by,
            submitted_by_company=submitted_by_company,
            assigned_to=assigned_to,
            priority=priority,
            date_required=date.today() + timedelta(days=days_for_response),
            attachments=attachments or []
        )

        self.rfis[rfi_number] = rfi
        self._save_rfis()

        return rfi

    def submit_rfi(self, rfi_number: str) -> RFI:
        """Submit RFI for response"""
        rfi = self.rfis.get(rfi_number)
        if not rfi:
            raise ValueError(f"RFI {rfi_number} not found")

        if rfi.status != RFIStatus.DRAFT:
            raise ValueError(f"RFI {rfi_number} already submitted")

        rfi.status = RFIStatus.OPEN
        rfi.date_submitted = date.today()
        self._save_rfis()

        # Trigger notification
        self._notify_submission(rfi)

        return rfi

    def respond_to_rfi(
        self,
        rfi_number: str,
        response: str,
        response_by: str,
        attachments: List[str] = None,
        cost_impact: bool = False,
        cost_amount: float = 0.0,
        schedule_impact: bool = False,
        schedule_days: int = 0
    ) -> RFI:
        """Provide response to RFI"""
        rfi = self.rfis.get(rfi_number)
        if not rfi:
            raise ValueError(f"RFI {rfi_number} not found")

        rfi.response = response
        rfi.response_by = response_by
        rfi.date_responded = date.today()
        rfi.status = RFIStatus.ANSWERED

        if attachments:
            rfi.attachments.extend(attachments)

        rfi.cost_impact = cost_impact
        rfi.cost_amount = cost_amount
        rfi.schedule_impact = schedule_impact
        rfi.schedule_days = schedule_days

        self._save_rfis()

        # Trigger notification
        self._notify_response(rfi)

        return rfi

    def close_rfi(self, rfi_number: str, change_order_ref: str = None) -> RFI:
        """Close RFI after implementation"""
        rfi = self.rfis.get(rfi_number)
        if not rfi:
            raise ValueError(f"RFI {rfi_number} not found")

        rfi.status = RFIStatus.CLOSED
        rfi.date_closed = date.today()
        if change_order_ref:
            rfi.change_order_ref = change_order_ref

        self._save_rfis()
        return rfi

    def get_overdue_rfis(self) -> List[RFI]:
        """Get list of overdue RFIs"""
        today = date.today()
        return [
            rfi for rfi in self.rfis.values()
            if rfi.status == RFIStatus.OPEN
            and rfi.date_required < today
        ]

    def get_due_soon_rfis(self, days: int = 3) -> List[RFI]:
        """Get RFIs due within specified days"""
        today = date.today()
        cutoff = today + timedelta(days=days)
        return [
            rfi for rfi in self.rfis.values()
            if rfi.status == RFIStatus.OPEN
            and today <= rfi.date_required <= cutoff
        ]

    def get_rfis_by_status(self, status: RFIStatus) -> List[RFI]:
        """Get RFIs by status"""
        return [r for r in self.rfis.values() if r.status == status]

    def get_rfis_by_assignee(self, assignee: str) -> List[RFI]:
        """Get RFIs assigned to specific party"""
        return [r for r in self.rfis.values() if r.assigned_to == assignee]

    def get_statistics(self) -> dict:
        """Get RFI statistics"""
        all_rfis = list(self.rfis.values())

        if not all_rfis:
            return {'total': 0}

        open_rfis = [r for r in all_rfis if r.status == RFIStatus.OPEN]
        closed_rfis = [r for r in all_rfis if r.status == RFIStatus.CLOSED]

        # Calculate response times for closed RFIs
        response_times = []
        for rfi in closed_rfis:
            if rfi.date_responded and rfi.date_submitted:
                days = (rfi.date_responded - rfi.date_submitted).days
                response_times.append(days)

        # Cost and schedule impacts
        cost_rfis = [r for r in all_rfis if r.cost_impact]
        schedule_rfis = [r for r in all_rfis if r.schedule_impact]

        return {
            'total': len(all_rfis),
            'open': len(open_rfis),
            'closed': len(closed_rfis),
            'overdue': len(self.get_overdue_rfis()),
            'avg_response_days': sum(response_times) / len(response_times) if response_times else 0,
            'with_cost_impact': len(cost_rfis),
            'total_cost_impact': sum(r.cost_amount for r in cost_rfis),
            'with_schedule_impact': len(schedule_rfis),
            'total_schedule_days': sum(r.schedule_days for r in schedule_rfis),
            'by_priority': {
                p.value: len([r for r in all_rfis if r.priority == p])
                for p in RFIPriority
            },
            'by_assignee': self._group_by_assignee(all_rfis)
        }

    def _group_by_assignee(self, rfis: List[RFI]) -> dict:
        """Group RFIs by assignee"""
        result = {}
        for rfi in rfis:
            if rfi.assigned_to not in result:
                result[rfi.assigned_to] = {'total': 0, 'open': 0}
            result[rfi.assigned_to]['total'] += 1
            if rfi.status == RFIStatus.OPEN:
                result[rfi.assigned_to]['open'] += 1
        return result

    def _notify_submission(self, rfi: RFI):
        """Send notification for new RFI"""
        # Implement email/Telegram notification
        print(f"📋 New RFI submitted: {rfi.rfi_number} - {rfi.subject}")
        print(f"   Assigned to: {rfi.assigned_to}")
        print(f"   Due: {rfi.date_required}")

    def _notify_response(self, rfi: RFI):
        """Send notification for RFI response"""
        print(f"✅ RFI responded: {rfi.rfi_number} - {rfi.subject}")
        print(f"   Response by: {rfi.response_by}")

    def generate_report(self, output_path: str = None) -> str:
        """Generate RFI status report"""
        stats = self.get_statistics()

        report = f"""
RFI STATUS REPORT
Project: {self.project_id}
Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}

SUMMARY
═══════════════════════════════════════
Total RFIs:           {stats['total']}
Open:                 {stats['open']}
Closed:               {stats['closed']}
Overdue:              {stats['overdue']}
Avg Response Time:    {stats['avg_response_days']:.1f} days

IMPACT ANALYSIS
═══════════════════════════════════════
RFIs with Cost Impact:     {stats['with_cost_impact']}
Total Cost Impact:         ${stats['total_cost_impact']:,.2f}
RFIs with Schedule Impact: {stats['with_schedule_impact']}
Total Schedule Days:       {stats['total_schedule_days']}

BY PRIORITY
═══════════════════════════════════════
"""
        for priority, count in stats['by_priority'].items():
            report += f"{priority}: {count}\n"

        report += """
BY ASSIGNEE (Open)
═══════════════════════════════════════
"""
        for assignee, data in stats['by_assignee'].items():
            report += f"{assignee}: {data['open']} open / {data['total']} total\n"

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)

        return report


# Usage Example
if __name__ == "__main__":
    # Initialize manager
    manager = RFIManager(project_id="PROJECT-2026-001")

    # Create RFI
    rfi = manager.create_rfi(
        subject="Clarification on electrical panel location",
        question="""
        Drawing E-101 shows main electrical panel in Room 105,
        but specification Section 26 05 00 indicates utility room.
        Please confirm correct location and provide updated drawing
        if Room 105 is correct.
        """,
        submitted_by="Ivan Petrov",
        submitted_by_company="ABC Electrical",
        assigned_to="Architect",
        spec_section="26 05 00",
        drawing_ref="E-101",
        location="Building A, Floor 1",
        priority=RFIPriority.HIGH,
        days_for_response=5
    )

    print(f"Created: {rfi.rfi_number}")

    # Submit RFI
    manager.submit_rfi(rfi.rfi_number)

    # Respond to RFI
    manager.respond_to_rfi(
        rfi_number=rfi.rfi_number,
        response="""
        Room 105 is correct. Updated drawing E-101 Rev 2 attached.
        Specification will be updated in next addendum.
        """,
        response_by="John Architect",
        schedule_impact=True,
        schedule_days=2
    )

    # Close RFI
    manager.close_rfi(rfi.rfi_number)

    # Generate report
    print(manager.generate_report())
```

## n8n Integration

```yaml
name: RFI Notification Workflow
trigger:
  type: webhook
  path: /rfi-notification

steps:
  - parse_rfi:
      node: Code
      code: |
        return {
          rfi_number: $json.rfi_number,
          subject: $json.subject,
          assigned_to: $json.assigned_to,
          due_date: $json.date_required,
          priority: $json.priority
        };

  - get_recipient:
      node: Google Sheets
      operation: readRows
      sheet: Contacts
      filter: role = "={{$json.assigned_to}}"

  - send_email:
      node: Email
      to: "={{$json.email}}"
      subject: "[RFI {{$json.rfi_number}}] {{$json.subject}}"
      body: |
        New RFI requires your response:

        RFI #: {{$json.rfi_number}}
        Subject: {{$json.subject}}
        Priority: {{$json.priority}}
        Due Date: {{$json.due_date}}

        Please respond in the project portal.

  - send_telegram:
      node: Telegram
      operation: sendMessage
      chatId: "={{$json.telegram_id}}"
      text: |
        📋 *New RFI: {{$json.rfi_number}}*

        {{$json.subject}}

        Priority: {{$json.priority}}
        Due: {{$json.due_date}}

        [View in Portal]({{PROJECT_PORTAL_URL}}/rfi/{{$json.rfi_number}})
```

## Templates

### RFI Submission Template

```markdown
## REQUEST FOR INFORMATION

**RFI Number:** [Auto-generated]
**Date:** [Today]
**Project:** [Project Name]

### QUESTION
**Subject:** [Brief title - max 80 characters]

**Specification Section:** [CSI number]
**Drawing Reference:** [Drawing number(s)]
**Location:** [Building/Floor/Area]

**Question:**
[Detailed question - be specific about what clarification is needed]

**Suggested Resolution:**
[If you have a proposed solution, include it here]

### ATTACHMENTS
- [ ] Relevant drawing sections
- [ ] Photos of field conditions
- [ ] Specification excerpts

### IMPACT ASSESSMENT
- Estimated Cost Impact: [ ] Yes [ ] No  Amount: $_______
- Estimated Schedule Impact: [ ] Yes [ ] No  Days: _______
- Work Stoppage: [ ] Yes [ ] No

**Response Required By:** [Date - default +7 days]

---
Submitted by: [Name, Company]
```

---

*"A well-written RFI gets answered faster. Be specific, reference documents, and propose solutions."*
