---
slug: "punch-list-manager"
display_name: "Punch List Manager"
description: "Manage construction punch lists for project closeout. Track deficiencies, assign corrections, and monitor completion status."
---

# Punch List Manager

## Business Case

### Problem Statement
Project closeout challenges:
- Tracking hundreds of items
- Assigning responsibility
- Monitoring completion
- Documentation for handover

### Solution
Systematic punch list management to track deficiencies, assignments, and completion through project closeout.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class PunchItemStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    REJECTED = "rejected"


class PunchItemPriority(Enum):
    CRITICAL = "critical"   # Life safety, code violation
    HIGH = "high"           # Functionality impaired
    MEDIUM = "medium"       # Cosmetic/minor
    LOW = "low"             # Nice to have


class PunchItemCategory(Enum):
    STRUCTURAL = "structural"
    ARCHITECTURAL = "architectural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    EXTERIOR = "exterior"
    SITE = "site"
    GENERAL = "general"


@dataclass
class PunchItem:
    item_id: str
    location: str
    description: str
    category: PunchItemCategory
    priority: PunchItemPriority
    status: PunchItemStatus
    assigned_to: str
    created_date: date
    due_date: date
    completed_date: Optional[date] = None
    verified_date: Optional[date] = None
    verified_by: str = ""
    photos: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PunchListSummary:
    total_items: int
    open_items: int
    in_progress: int
    completed: int
    verified: int
    rejected: int
    completion_rate: float
    by_category: Dict[str, int]
    by_priority: Dict[str, int]
    by_assignee: Dict[str, int]
    overdue_count: int


class PunchListManager:
    """Manage construction punch lists."""

    def __init__(self, project_name: str, target_closeout_date: date):
        self.project_name = project_name
        self.target_date = target_closeout_date
        self.items: Dict[str, PunchItem] = {}
        self._next_id = 1

    def add_item(self,
                 location: str,
                 description: str,
                 category: PunchItemCategory,
                 priority: PunchItemPriority,
                 assigned_to: str,
                 due_date: date = None,
                 notes: str = "") -> PunchItem:
        """Add punch list item."""

        item_id = f"PL-{self._next_id:04d}"
        self._next_id += 1

        if due_date is None:
            # Default based on priority
            if priority == PunchItemPriority.CRITICAL:
                due_date = date.today() + timedelta(days=3)
            elif priority == PunchItemPriority.HIGH:
                due_date = date.today() + timedelta(days=7)
            else:
                due_date = date.today() + timedelta(days=14)

        item = PunchItem(
            item_id=item_id,
            location=location,
            description=description,
            category=category,
            priority=priority,
            status=PunchItemStatus.OPEN,
            assigned_to=assigned_to,
            created_date=date.today(),
            due_date=due_date,
            notes=notes
        )

        self.items[item_id] = item
        return item

    def update_status(self,
                      item_id: str,
                      status: PunchItemStatus,
                      verified_by: str = ""):
        """Update item status."""

        if item_id not in self.items:
            return

        item = self.items[item_id]
        item.status = status

        if status == PunchItemStatus.COMPLETED:
            item.completed_date = date.today()
        elif status == PunchItemStatus.VERIFIED:
            item.verified_date = date.today()
            item.verified_by = verified_by

    def reassign_item(self, item_id: str, new_assignee: str, new_due_date: date = None):
        """Reassign item to different contractor."""

        if item_id not in self.items:
            return

        item = self.items[item_id]
        item.assigned_to = new_assignee

        if new_due_date:
            item.due_date = new_due_date

        item.status = PunchItemStatus.OPEN

    def add_note(self, item_id: str, note: str):
        """Add note to item."""
        if item_id in self.items:
            self.items[item_id].notes += f"\n{date.today()}: {note}"

    def add_photo(self, item_id: str, photo_path: str):
        """Add photo reference to item."""
        if item_id in self.items:
            self.items[item_id].photos.append(photo_path)

    def get_summary(self) -> PunchListSummary:
        """Get punch list summary."""

        items = list(self.items.values())
        today = date.today()

        # Status counts
        open_items = sum(1 for i in items if i.status == PunchItemStatus.OPEN)
        in_progress = sum(1 for i in items if i.status == PunchItemStatus.IN_PROGRESS)
        completed = sum(1 for i in items if i.status == PunchItemStatus.COMPLETED)
        verified = sum(1 for i in items if i.status == PunchItemStatus.VERIFIED)
        rejected = sum(1 for i in items if i.status == PunchItemStatus.REJECTED)

        # Completion rate (verified / total)
        completion_rate = (verified / len(items) * 100) if items else 0

        # By category
        by_category = {}
        for cat in PunchItemCategory:
            count = sum(1 for i in items if i.category == cat and i.status != PunchItemStatus.VERIFIED)
            if count > 0:
                by_category[cat.value] = count

        # By priority
        by_priority = {}
        for pri in PunchItemPriority:
            count = sum(1 for i in items if i.priority == pri and i.status != PunchItemStatus.VERIFIED)
            if count > 0:
                by_priority[pri.value] = count

        # By assignee
        by_assignee = {}
        for item in items:
            if item.status not in [PunchItemStatus.VERIFIED, PunchItemStatus.COMPLETED]:
                if item.assigned_to not in by_assignee:
                    by_assignee[item.assigned_to] = 0
                by_assignee[item.assigned_to] += 1

        # Overdue
        overdue = sum(
            1 for i in items
            if i.due_date < today and i.status not in [PunchItemStatus.VERIFIED, PunchItemStatus.COMPLETED]
        )

        return PunchListSummary(
            total_items=len(items),
            open_items=open_items,
            in_progress=in_progress,
            completed=completed,
            verified=verified,
            rejected=rejected,
            completion_rate=round(completion_rate, 1),
            by_category=by_category,
            by_priority=by_priority,
            by_assignee=by_assignee,
            overdue_count=overdue
        )

    def get_items_by_status(self, status: PunchItemStatus) -> List[PunchItem]:
        """Get items by status."""
        return [i for i in self.items.values() if i.status == status]

    def get_items_by_assignee(self, assignee: str) -> List[PunchItem]:
        """Get items assigned to specific contractor."""
        return [i for i in self.items.values() if i.assigned_to == assignee]

    def get_overdue_items(self) -> List[PunchItem]:
        """Get overdue items."""
        today = date.today()
        return [
            i for i in self.items.values()
            if i.due_date < today and i.status not in [PunchItemStatus.VERIFIED, PunchItemStatus.COMPLETED]
        ]

    def get_critical_items(self) -> List[PunchItem]:
        """Get critical priority items."""
        return [
            i for i in self.items.values()
            if i.priority == PunchItemPriority.CRITICAL
            and i.status not in [PunchItemStatus.VERIFIED]
        ]

    def generate_contractor_report(self, assignee: str) -> pd.DataFrame:
        """Generate report for specific contractor."""

        items = self.get_items_by_assignee(assignee)

        return pd.DataFrame([
            {
                'Item ID': i.item_id,
                'Location': i.location,
                'Description': i.description,
                'Priority': i.priority.value,
                'Status': i.status.value,
                'Due Date': i.due_date,
                'Days Overdue': max(0, (date.today() - i.due_date).days) if i.status != PunchItemStatus.VERIFIED else 0
            }
            for i in items
        ])

    def forecast_completion(self) -> Dict[str, Any]:
        """Forecast closeout completion."""

        summary = self.get_summary()
        remaining = summary.total_items - summary.verified

        if remaining == 0:
            return {
                'status': 'COMPLETE',
                'remaining_items': 0,
                'on_track': True
            }

        # Calculate completion rate (items verified per day)
        verified_items = self.get_items_by_status(PunchItemStatus.VERIFIED)
        if verified_items:
            dates = [i.verified_date for i in verified_items if i.verified_date]
            if dates:
                days_active = (max(dates) - min(dates)).days + 1
                rate = len(dates) / days_active if days_active > 0 else 1
            else:
                rate = 1
        else:
            rate = 1

        days_needed = remaining / rate if rate > 0 else remaining
        projected_completion = date.today() + timedelta(days=int(days_needed))

        return {
            'status': 'IN_PROGRESS',
            'remaining_items': remaining,
            'completion_rate_per_day': round(rate, 1),
            'days_needed': round(days_needed, 0),
            'projected_completion': projected_completion,
            'target_date': self.target_date,
            'on_track': projected_completion <= self.target_date
        }

    def export_to_excel(self, output_path: str) -> str:
        """Export punch list to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = self.get_summary()
            summary_df = pd.DataFrame([{
                'Project': self.project_name,
                'Target Closeout': self.target_date,
                'Total Items': summary.total_items,
                'Open': summary.open_items,
                'In Progress': summary.in_progress,
                'Completed': summary.completed,
                'Verified': summary.verified,
                'Completion %': summary.completion_rate,
                'Overdue': summary.overdue_count
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # All items
            items_df = pd.DataFrame([
                {
                    'Item ID': i.item_id,
                    'Location': i.location,
                    'Description': i.description,
                    'Category': i.category.value,
                    'Priority': i.priority.value,
                    'Status': i.status.value,
                    'Assigned To': i.assigned_to,
                    'Created': i.created_date,
                    'Due': i.due_date,
                    'Completed': i.completed_date,
                    'Verified': i.verified_date,
                    'Notes': i.notes
                }
                for i in self.items.values()
            ])
            items_df.to_excel(writer, sheet_name='All Items', index=False)

            # By Assignee
            assignee_df = pd.DataFrame([
                {'Assignee': k, 'Open Items': v}
                for k, v in summary.by_assignee.items()
            ])
            if not assignee_df.empty:
                assignee_df.to_excel(writer, sheet_name='By Assignee', index=False)

            # Overdue
            overdue = self.get_overdue_items()
            if overdue:
                overdue_df = pd.DataFrame([
                    {
                        'Item ID': i.item_id,
                        'Location': i.location,
                        'Description': i.description,
                        'Assigned To': i.assigned_to,
                        'Due': i.due_date,
                        'Days Overdue': (date.today() - i.due_date).days
                    }
                    for i in overdue
                ])
                overdue_df.to_excel(writer, sheet_name='Overdue', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

# Initialize manager
punch = PunchListManager("Office Building A", target_closeout_date=date(2024, 12, 31))

# Add items
punch.add_item(
    location="Level 3, Room 301",
    description="Ceiling tile damaged",
    category=PunchItemCategory.ARCHITECTURAL,
    priority=PunchItemPriority.MEDIUM,
    assigned_to="ABC Ceilings"
)

punch.add_item(
    location="Lobby",
    description="Fire alarm not functioning",
    category=PunchItemCategory.FIRE_PROTECTION,
    priority=PunchItemPriority.CRITICAL,
    assigned_to="XYZ Fire Protection"
)

# Update status
punch.update_status("PL-0001", PunchItemStatus.COMPLETED)
punch.update_status("PL-0001", PunchItemStatus.VERIFIED, verified_by="John Smith")
```

## Common Use Cases

### 1. Summary Report
```python
summary = punch.get_summary()
print(f"Total: {summary.total_items}")
print(f"Completion: {summary.completion_rate}%")
print(f"Overdue: {summary.overdue_count}")
```

### 2. Contractor Report
```python
report = punch.generate_contractor_report("ABC Ceilings")
print(report)
```

### 3. Forecast Completion
```python
forecast = punch.forecast_completion()
print(f"On Track: {forecast['on_track']}")
print(f"Projected: {forecast['projected_completion']}")
```

## Resources
- **DDC Book**: Chapter 5.1 - Project Closeout
