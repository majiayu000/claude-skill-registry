---
name: "material-procurement-tracker"
description: "Track material procurement from requisition to delivery. Monitor lead times, vendors, and costs."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🛒", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Material Procurement Tracker

## Business Case

Long lead items and material procurement require careful tracking to avoid schedule delays.

## Technical Implementation

```python
import pandas as pd
from datetime import date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ProcurementStatus(Enum):
    REQUISITIONED = "requisitioned"
    RFQ_SENT = "rfq_sent"
    QUOTED = "quoted"
    PO_ISSUED = "po_issued"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class ProcurementItem:
    item_id: str
    description: str
    spec_section: str
    quantity: float
    unit: str
    required_date: date
    lead_time_days: int
    status: ProcurementStatus
    priority: Priority
    vendor: str = ""
    po_number: str = ""
    po_amount: float = 0.0
    order_date: Optional[date] = None
    expected_delivery: Optional[date] = None
    actual_delivery: Optional[date] = None

    @property
    def must_order_by(self) -> date:
        return self.required_date - timedelta(days=self.lead_time_days)

    @property
    def is_late_to_order(self) -> bool:
        if self.status in [ProcurementStatus.PO_ISSUED, ProcurementStatus.IN_PRODUCTION,
                          ProcurementStatus.SHIPPED, ProcurementStatus.DELIVERED]:
            return False
        return date.today() > self.must_order_by


class MaterialProcurementTracker:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.items: Dict[str, ProcurementItem] = {}
        self._counter = 0

    def add_item(self, description: str, spec_section: str, quantity: float,
                unit: str, required_date: date, lead_time_days: int,
                priority: Priority = Priority.NORMAL) -> ProcurementItem:
        self._counter += 1
        item_id = f"PROC-{self._counter:04d}"

        item = ProcurementItem(
            item_id=item_id,
            description=description,
            spec_section=spec_section,
            quantity=quantity,
            unit=unit,
            required_date=required_date,
            lead_time_days=lead_time_days,
            status=ProcurementStatus.REQUISITIONED,
            priority=priority
        )
        self.items[item_id] = item
        return item

    def issue_po(self, item_id: str, vendor: str, po_number: str,
                amount: float, expected_delivery: date):
        if item_id in self.items:
            item = self.items[item_id]
            item.status = ProcurementStatus.PO_ISSUED
            item.vendor = vendor
            item.po_number = po_number
            item.po_amount = amount
            item.order_date = date.today()
            item.expected_delivery = expected_delivery

    def update_status(self, item_id: str, status: ProcurementStatus):
        if item_id in self.items:
            self.items[item_id].status = status
            if status == ProcurementStatus.DELIVERED:
                self.items[item_id].actual_delivery = date.today()

    def get_items_to_order(self) -> List[ProcurementItem]:
        """Get items that need to be ordered soon."""
        cutoff = date.today() + timedelta(days=14)
        return [i for i in self.items.values()
                if i.status in [ProcurementStatus.REQUISITIONED, ProcurementStatus.RFQ_SENT,
                               ProcurementStatus.QUOTED]
                and i.must_order_by <= cutoff]

    def get_late_items(self) -> List[ProcurementItem]:
        return [i for i in self.items.values() if i.is_late_to_order]

    def get_summary(self) -> Dict[str, Any]:
        by_status = {}
        total_value = 0
        for item in self.items.values():
            status = item.status.value
            by_status[status] = by_status.get(status, 0) + 1
            total_value += item.po_amount

        return {
            'total_items': len(self.items),
            'by_status': by_status,
            'total_po_value': total_value,
            'items_to_order': len(self.get_items_to_order()),
            'late_items': len(self.get_late_items())
        }

    def export_log(self, output_path: str):
        data = [{
            'ID': i.item_id,
            'Description': i.description,
            'Spec': i.spec_section,
            'Qty': i.quantity,
            'Unit': i.unit,
            'Required': i.required_date,
            'Lead Time': i.lead_time_days,
            'Must Order By': i.must_order_by,
            'Status': i.status.value,
            'Vendor': i.vendor,
            'PO': i.po_number,
            'Amount': i.po_amount
        } for i in self.items.values()]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
tracker = MaterialProcurementTracker("Office Tower")

item = tracker.add_item(
    description="Structural Steel W14x90",
    spec_section="05 12 00",
    quantity=500,
    unit="TON",
    required_date=date(2024, 6, 1),
    lead_time_days=90,
    priority=Priority.CRITICAL
)

tracker.issue_po(item.item_id, "ABC Steel", "PO-2024-001", 450000,
                date(2024, 5, 15))

urgent = tracker.get_items_to_order()
print(f"Items needing order: {len(urgent)}")
```

## Resources
- **DDC Book**: Chapter 3.4 - Procurement
