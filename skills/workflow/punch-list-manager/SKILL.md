---
slug: "punch-list-manager"
display_name: "Punch List Manager"
description: "Digital punch list management for construction project closeout. Track deficiencies, assign corrections, photo documentation, and completion verification."
---

# Punch List Manager for Construction Closeout

Complete system for managing construction punch lists from creation through final acceptance.

## Business Case

**Problem**: Punch list management is inefficient:
- Paper lists get lost or outdated
- Difficult to track completion status
- Photos disconnected from items
- Back-charges delayed due to poor documentation
- Multiple walks create duplicate items

**Solution**: Digital punch list system that:
- Creates items with photos and location markup
- Assigns to responsible parties with deadlines
- Tracks completion with before/after photos
- Generates back-charge documentation
- Provides real-time completion dashboards

**ROI**: 50% faster closeout, 80% reduction in disputed back-charges

## Punch List Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│                      PUNCH LIST WORKFLOW                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   CREATION            ASSIGNMENT          COMPLETION                 │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐               │
│   │ Walk    │────────►│ Assign  │────────►│ Correct │               │
│   │ Site    │         │ Items   │         │ Items   │               │
│   └─────────┘         └─────────┘         └─────────┘               │
│       │                   │                   │                      │
│       ▼                   ▼                   ▼                      │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐               │
│   │ Log     │         │ Notify  │         │ Submit  │               │
│   │ Items   │         │ Parties │         │ Photo   │               │
│   └─────────┘         └─────────┘         └─────────┘               │
│       │                   │                   │                      │
│       ▼                   ▼                   ▼                      │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐               │
│   │ Photo   │         │ Set     │         │ Mark    │               │
│   │ + Tag   │         │ Deadline│         │ Complete│               │
│   └─────────┘         └─────────┘         └─────────┘               │
│                                               │                      │
│                                               ▼                      │
│   VERIFICATION        CLOSEOUT           ┌─────────┐               │
│   ┌─────────┐         ┌─────────┐        │ Verify  │               │
│   │ Re-walk │◄────────│ Accept  │◄───────│ Work    │               │
│   │ Site    │         │ Items   │        └─────────┘               │
│   └─────────┘         └─────────┘                                   │
│       │                   │                                          │
│       ▼                   ▼                                          │
│   ┌─────────┐         ┌─────────┐                                   │
│   │ New     │         │ Final   │                                   │
│   │ Items?  │────NO──►│ Accept  │                                   │
│   └────┬────┘         └─────────┘                                   │
│        │YES                                                          │
│        └──────────────► Back to CREATION                            │
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

class PunchItemStatus(Enum):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    READY_FOR_VERIFICATION = "Ready for Verification"
    VERIFIED = "Verified"
    REJECTED = "Rejected"
    ACCEPTED = "Accepted"

class PunchItemPriority(Enum):
    CRITICAL = "Critical"     # Life safety / code compliance
    HIGH = "High"             # Affects occupancy
    MEDIUM = "Medium"         # Standard punch
    LOW = "Low"               # Minor / cosmetic
    OBSERVATION = "Observation"

class TradeCategory(Enum):
    GENERAL = "General Contractor"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    HVAC = "HVAC"
    FIRE_PROTECTION = "Fire Protection"
    DRYWALL = "Drywall/Painting"
    FLOORING = "Flooring"
    MILLWORK = "Millwork/Casework"
    GLAZING = "Glazing"
    ROOFING = "Roofing"
    SITEWORK = "Sitework"
    LANDSCAPING = "Landscaping"
    CONTROLS = "Controls/BMS"
    OTHER = "Other"

@dataclass
class PunchItem:
    item_id: str
    punch_list_id: str
    description: str
    location: str
    trade: TradeCategory
    priority: PunchItemPriority

    # Location details
    building: str = ""
    floor: str = ""
    room: str = ""

    # Assignment
    assigned_to: str = ""
    assigned_date: date = None
    due_date: date = None

    # Documentation
    photo_before: str = ""
    photo_after: str = ""
    drawing_markup: str = ""
    spec_reference: str = ""

    # Status tracking
    status: PunchItemStatus = PunchItemStatus.OPEN
    created_by: str = ""
    created_date: date = field(default_factory=date.today)

    # Completion
    completed_by: str = ""
    completed_date: date = None
    completion_notes: str = ""

    # Verification
    verified_by: str = ""
    verified_date: date = None
    verification_notes: str = ""

    # Back-charge
    back_charge: bool = False
    back_charge_amount: float = 0.0
    back_charge_ref: str = ""

    # History
    history: List[dict] = field(default_factory=list)

@dataclass
class PunchList:
    list_id: str
    project_id: str
    name: str
    walk_date: date
    walk_attendees: List[str]

    items: List[PunchItem] = field(default_factory=list)
    status: str = "Active"  # Active, Complete
    created_by: str = ""
    created_date: date = field(default_factory=date.today)

    area: str = ""  # Building/floor/zone covered
    list_type: str = "Punch"  # Punch, Pre-Punch, Final
```

## Python Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

class PunchListManager:
    """Construction punch list management system"""

    def __init__(self, project_id: str, storage_path: str = None):
        self.project_id = project_id
        self.storage_path = storage_path or f"punch_{project_id}"
        self.punch_lists: Dict[str, PunchList] = {}
        self.items: Dict[str, PunchItem] = {}

    def create_punch_list(
        self,
        name: str,
        walk_date: date,
        attendees: List[str],
        area: str = "",
        list_type: str = "Punch",
        created_by: str = ""
    ) -> PunchList:
        """Create new punch list from walk"""

        list_id = f"PL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        punch_list = PunchList(
            list_id=list_id,
            project_id=self.project_id,
            name=name,
            walk_date=walk_date,
            walk_attendees=attendees,
            area=area,
            list_type=list_type,
            created_by=created_by
        )

        self.punch_lists[list_id] = punch_list
        return punch_list

    def add_item(
        self,
        punch_list_id: str,
        description: str,
        location: str,
        trade: TradeCategory,
        priority: PunchItemPriority = PunchItemPriority.MEDIUM,
        building: str = "",
        floor: str = "",
        room: str = "",
        photo_before: str = "",
        drawing_markup: str = "",
        spec_reference: str = "",
        created_by: str = ""
    ) -> PunchItem:
        """Add item to punch list"""

        if punch_list_id not in self.punch_lists:
            raise ValueError(f"Punch list {punch_list_id} not found")

        # Generate item ID
        punch_list = self.punch_lists[punch_list_id]
        item_num = len(punch_list.items) + 1
        item_id = f"{punch_list_id}-{item_num:04d}"

        item = PunchItem(
            item_id=item_id,
            punch_list_id=punch_list_id,
            description=description,
            location=location,
            trade=trade,
            priority=priority,
            building=building,
            floor=floor,
            room=room,
            photo_before=photo_before,
            drawing_markup=drawing_markup,
            spec_reference=spec_reference,
            created_by=created_by
        )

        # Add history entry
        item.history.append({
            'date': datetime.now(),
            'action': 'Created',
            'by': created_by,
            'notes': ''
        })

        self.items[item_id] = item
        punch_list.items.append(item)

        return item

    def assign_item(
        self,
        item_id: str,
        assigned_to: str,
        due_date: date = None,
        assigned_by: str = ""
    ) -> PunchItem:
        """Assign item to responsible party"""

        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        if due_date is None:
            # Default due dates by priority
            days = {
                PunchItemPriority.CRITICAL: 1,
                PunchItemPriority.HIGH: 3,
                PunchItemPriority.MEDIUM: 7,
                PunchItemPriority.LOW: 14,
                PunchItemPriority.OBSERVATION: 30
            }
            due_date = date.today() + timedelta(days=days.get(item.priority, 7))

        item.assigned_to = assigned_to
        item.assigned_date = date.today()
        item.due_date = due_date
        item.status = PunchItemStatus.ASSIGNED

        item.history.append({
            'date': datetime.now(),
            'action': 'Assigned',
            'by': assigned_by,
            'notes': f'Assigned to {assigned_to}, due {due_date}'
        })

        # Trigger notification
        self._notify_assignment(item)

        return item

    def mark_complete(
        self,
        item_id: str,
        completed_by: str,
        photo_after: str = "",
        completion_notes: str = ""
    ) -> PunchItem:
        """Mark item as completed by trade"""

        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        item.completed_by = completed_by
        item.completed_date = date.today()
        item.photo_after = photo_after
        item.completion_notes = completion_notes
        item.status = PunchItemStatus.READY_FOR_VERIFICATION

        item.history.append({
            'date': datetime.now(),
            'action': 'Completed',
            'by': completed_by,
            'notes': completion_notes
        })

        return item

    def verify_item(
        self,
        item_id: str,
        verified_by: str,
        accepted: bool,
        notes: str = ""
    ) -> PunchItem:
        """Verify completed item"""

        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        item.verified_by = verified_by
        item.verified_date = date.today()
        item.verification_notes = notes

        if accepted:
            item.status = PunchItemStatus.ACCEPTED
            action = 'Accepted'
        else:
            item.status = PunchItemStatus.REJECTED
            action = 'Rejected'
            # Re-assign for rework
            item.assigned_date = date.today()
            item.due_date = date.today() + timedelta(days=3)

        item.history.append({
            'date': datetime.now(),
            'action': action,
            'by': verified_by,
            'notes': notes
        })

        return item

    def add_back_charge(
        self,
        item_id: str,
        amount: float,
        reference: str = ""
    ) -> PunchItem:
        """Add back-charge to item"""

        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        item.back_charge = True
        item.back_charge_amount = amount
        item.back_charge_ref = reference

        item.history.append({
            'date': datetime.now(),
            'action': 'Back Charge',
            'by': '',
            'notes': f'Amount: ${amount:.2f}, Ref: {reference}'
        })

        return item

    def get_items_by_trade(self, trade: TradeCategory) -> List[PunchItem]:
        """Get all items for a specific trade"""
        return [i for i in self.items.values() if i.trade == trade]

    def get_items_by_status(self, status: PunchItemStatus) -> List[PunchItem]:
        """Get items by status"""
        return [i for i in self.items.values() if i.status == status]

    def get_overdue_items(self) -> List[PunchItem]:
        """Get overdue items"""
        today = date.today()
        return [
            i for i in self.items.values()
            if i.status in [PunchItemStatus.OPEN, PunchItemStatus.ASSIGNED, PunchItemStatus.IN_PROGRESS]
            and i.due_date and i.due_date < today
        ]

    def get_statistics(self) -> dict:
        """Get punch list statistics"""

        all_items = list(self.items.values())
        if not all_items:
            return {'total': 0}

        by_status = defaultdict(int)
        by_trade = defaultdict(lambda: {'total': 0, 'open': 0})
        by_priority = defaultdict(int)

        for item in all_items:
            by_status[item.status.value] += 1
            by_trade[item.trade.value]['total'] += 1
            if item.status not in [PunchItemStatus.ACCEPTED, PunchItemStatus.VERIFIED]:
                by_trade[item.trade.value]['open'] += 1
            by_priority[item.priority.value] += 1

        # Calculate completion rate
        accepted = len([i for i in all_items if i.status == PunchItemStatus.ACCEPTED])
        completion_rate = accepted / len(all_items) * 100 if all_items else 0

        # Back charges
        back_charge_items = [i for i in all_items if i.back_charge]
        total_back_charges = sum(i.back_charge_amount for i in back_charge_items)

        return {
            'total': len(all_items),
            'by_status': dict(by_status),
            'by_trade': dict(by_trade),
            'by_priority': dict(by_priority),
            'completion_rate': round(completion_rate, 1),
            'overdue': len(self.get_overdue_items()),
            'back_charge_count': len(back_charge_items),
            'back_charge_total': total_back_charges
        }

    def generate_trade_report(self, trade: TradeCategory) -> str:
        """Generate report for specific trade"""

        items = self.get_items_by_trade(trade)

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           PUNCH LIST - {trade.value.upper():<30}      ║
║   Project: {self.project_id:<40}       ║
║   Date: {date.today().strftime('%d.%m.%Y'):<43}       ║
╠══════════════════════════════════════════════════════════════╣

Total Items: {len(items)}
Open: {len([i for i in items if i.status not in [PunchItemStatus.ACCEPTED]])}
Due Today: {len([i for i in items if i.due_date == date.today()])}
Overdue: {len([i for i in items if i.due_date and i.due_date < date.today() and i.status not in [PunchItemStatus.ACCEPTED]])}

ITEMS REQUIRING ACTION
───────────────────────────────────────────────────────────────
"""
        for item in items:
            if item.status not in [PunchItemStatus.ACCEPTED]:
                overdue_flag = "🔴" if item.due_date and item.due_date < date.today() else ""
                report += f"""
{overdue_flag} [{item.item_id}] {item.priority.value}
   Location: {item.location}
   Description: {item.description}
   Status: {item.status.value}
   Due: {item.due_date}
"""

        report += """
╚══════════════════════════════════════════════════════════════╝
"""
        return report

    def generate_summary_dashboard(self) -> str:
        """Generate overall punch list dashboard"""

        stats = self.get_statistics()

        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    PUNCH LIST DASHBOARD                           ║
║   Project: {self.project_id:<40}          ║
║   Date: {date.today().strftime('%d.%m.%Y'):<43}          ║
╠══════════════════════════════════════════════════════════════════╣

📊 OVERALL STATUS
───────────────────────────────────────────────────────────────────
   Total Items:        {stats['total']}
   Completion Rate:    {stats['completion_rate']}%
   Overdue Items:      {stats['overdue']}

📈 BY STATUS
───────────────────────────────────────────────────────────────────
"""
        for status, count in stats['by_status'].items():
            bar = "█" * int(count / max(stats['by_status'].values()) * 20) if stats['by_status'] else ""
            report += f"   {status:<25} {count:>5}  {bar}\n"

        report += """
🔧 BY TRADE (Open Items)
───────────────────────────────────────────────────────────────────
"""
        for trade, data in sorted(stats['by_trade'].items(), key=lambda x: x[1]['open'], reverse=True):
            if data['open'] > 0:
                report += f"   {trade:<25} {data['open']:>5} open / {data['total']} total\n"

        report += f"""
💰 BACK CHARGES
───────────────────────────────────────────────────────────────────
   Items with Back Charges:  {stats['back_charge_count']}
   Total Back Charges:       ${stats['back_charge_total']:,.2f}

╚══════════════════════════════════════════════════════════════════╝
"""
        return report

    def _notify_assignment(self, item: PunchItem):
        """Send notification for assigned item"""
        print(f"📋 Punch item assigned: {item.item_id}")
        print(f"   To: {item.assigned_to}")
        print(f"   Due: {item.due_date}")
        print(f"   Location: {item.location}")

    def export_to_excel(self, output_path: str) -> str:
        """Export punch list to Excel"""

        records = []
        for item in self.items.values():
            records.append({
                'Item ID': item.item_id,
                'Description': item.description,
                'Location': item.location,
                'Building': item.building,
                'Floor': item.floor,
                'Room': item.room,
                'Trade': item.trade.value,
                'Priority': item.priority.value,
                'Status': item.status.value,
                'Assigned To': item.assigned_to,
                'Due Date': item.due_date,
                'Completed By': item.completed_by,
                'Completed Date': item.completed_date,
                'Back Charge': 'Yes' if item.back_charge else 'No',
                'Back Charge Amount': item.back_charge_amount if item.back_charge else '',
                'Photo Before': item.photo_before,
                'Photo After': item.photo_after
            })

        df = pd.DataFrame(records)
        df.to_excel(output_path, index=False)
        return output_path


# Usage Example
if __name__ == "__main__":
    # Initialize manager
    manager = PunchListManager(project_id="PROJECT-2026-001")

    # Create punch list from walk
    punch_list = manager.create_punch_list(
        name="Floor 5 Pre-Final Walk",
        walk_date=date.today(),
        attendees=["PM", "Architect", "GC Super"],
        area="Building A, Floor 5",
        list_type="Pre-Final",
        created_by="PM"
    )

    # Add items
    item1 = manager.add_item(
        punch_list_id=punch_list.list_id,
        description="Touch up paint at door frame Room 501",
        location="Room 501, door frame",
        trade=TradeCategory.DRYWALL,
        priority=PunchItemPriority.LOW,
        building="A",
        floor="5",
        room="501",
        created_by="PM"
    )

    item2 = manager.add_item(
        punch_list_id=punch_list.list_id,
        description="Missing cover plate on electrical outlet",
        location="Room 502, east wall",
        trade=TradeCategory.ELECTRICAL,
        priority=PunchItemPriority.MEDIUM,
        building="A",
        floor="5",
        room="502",
        created_by="PM"
    )

    # Assign items
    manager.assign_item(
        item_id=item1.item_id,
        assigned_to="ABC Painting",
        assigned_by="GC Super"
    )

    manager.assign_item(
        item_id=item2.item_id,
        assigned_to="XYZ Electric",
        due_date=date.today() + timedelta(days=2),
        assigned_by="GC Super"
    )

    # Mark complete
    manager.mark_complete(
        item_id=item1.item_id,
        completed_by="ABC Painting",
        completion_notes="Paint touched up"
    )

    # Verify
    manager.verify_item(
        item_id=item1.item_id,
        verified_by="PM",
        accepted=True,
        notes="Looks good"
    )

    # Generate reports
    print(manager.generate_summary_dashboard())
    print(manager.generate_trade_report(TradeCategory.ELECTRICAL))
```

## Telegram Bot Integration

```yaml
name: Punch List Bot
commands:
  /newitem:
    steps:
      - Ask: Photo of deficiency
      - Ask: Location (Building/Floor/Room)
      - Ask: Description
      - Ask: Trade (show buttons)
      - Ask: Priority (show buttons)
      - Confirm and create item

  /myitems:
    - Show open items assigned to user
    - Buttons: [Mark Complete] [View Details]

  /complete:
    - Select item from list
    - Ask for completion photo
    - Ask for notes
    - Submit for verification

  /dashboard:
    - Show summary statistics
    - Open items by trade
    - Overdue items
```

---

*"The last 10% of punch takes 50% of the time. Start early, stay organized."*
