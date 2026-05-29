---
name: "change-order-manager"
description: "Manage construction change orders from request to approval. Track costs, schedule impacts, and maintain audit trail for dispute prevention."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📝", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Change Order Manager

## Overview

Manage the complete change order lifecycle from potential change identification through approval and payment. Track cost and schedule impacts, maintain documentation, and provide analytics for project control.

## Change Order Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  CHANGE ORDER WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Identify  →  Document  →  Price  →  Negotiate  →  Execute     │
│  ────────     ────────     ─────     ─────────     ───────     │
│  📋 PCO       📝 RFP       💰 Quote  🤝 Review     ✅ Approve   │
│  🔍 Review    📸 Photos    ⏰ Time   📧 Submit     📄 Sign      │
│  📧 Notify    📄 Backup    📊 Impact 💬 Discuss    💵 Pay       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class ChangeOrderStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    PRICING = "pricing"
    NEGOTIATING = "negotiating"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    VOID = "void"

class ChangeType(Enum):
    OWNER_DIRECTED = "owner_directed"
    DESIGN_ERROR = "design_error"
    FIELD_CONDITION = "field_condition"
    CODE_CHANGE = "code_change"
    VALUE_ENGINEERING = "value_engineering"
    SCHEDULE_ACCELERATION = "schedule_acceleration"
    SCOPE_REDUCTION = "scope_reduction"

class PricingMethod(Enum):
    LUMP_SUM = "lump_sum"
    UNIT_PRICE = "unit_price"
    TIME_AND_MATERIALS = "time_and_materials"
    COST_PLUS = "cost_plus"

@dataclass
class CostBreakdown:
    labor: float = 0.0
    materials: float = 0.0
    equipment: float = 0.0
    subcontractor: float = 0.0
    overhead: float = 0.0
    profit: float = 0.0
    bond: float = 0.0

    @property
    def direct_cost(self) -> float:
        return self.labor + self.materials + self.equipment + self.subcontractor

    @property
    def total(self) -> float:
        return self.direct_cost + self.overhead + self.profit + self.bond

@dataclass
class ChangeOrderItem:
    id: str
    description: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float
    spec_section: str = ""
    csi_code: str = ""

@dataclass
class ChangeOrder:
    id: str
    number: int
    title: str
    description: str
    change_type: ChangeType
    status: ChangeOrderStatus

    # Dates
    identified_date: datetime
    submitted_date: Optional[datetime] = None
    approved_date: Optional[datetime] = None
    executed_date: Optional[datetime] = None

    # Pricing
    pricing_method: PricingMethod = PricingMethod.LUMP_SUM
    proposed_amount: float = 0.0
    approved_amount: float = 0.0
    cost_breakdown: CostBreakdown = field(default_factory=CostBreakdown)
    line_items: List[ChangeOrderItem] = field(default_factory=list)

    # Schedule
    proposed_time_days: int = 0
    approved_time_days: int = 0
    impacts_critical_path: bool = False

    # Documentation
    rfi_references: List[str] = field(default_factory=list)
    drawing_references: List[str] = field(default_factory=list)
    photo_attachments: List[str] = field(default_factory=list)
    backup_documents: List[str] = field(default_factory=list)

    # Tracking
    created_by: str = ""
    assigned_to: str = ""
    notes: List[Dict] = field(default_factory=list)

@dataclass
class ChangeOrderLog:
    project_id: str
    project_name: str
    original_contract: float
    change_orders: List[ChangeOrder]
    total_approved: float
    total_pending: float
    revised_contract: float

class ChangeOrderManager:
    """Manage construction change orders."""

    # Default markup rates
    DEFAULT_MARKUPS = {
        "overhead": 0.10,  # 10%
        "profit": 0.10,    # 10%
        "bond": 0.01,      # 1%
    }

    def __init__(self, project_id: str, project_name: str,
                 original_contract: float):
        self.project_id = project_id
        self.project_name = project_name
        self.original_contract = original_contract
        self.change_orders: Dict[str, ChangeOrder] = {}
        self.next_number = 1
        self.markup_rates = dict(self.DEFAULT_MARKUPS)

    def set_markup_rates(self, overhead: float = None, profit: float = None,
                        bond: float = None):
        """Set markup rates for cost calculations."""
        if overhead is not None:
            self.markup_rates["overhead"] = overhead
        if profit is not None:
            self.markup_rates["profit"] = profit
        if bond is not None:
            self.markup_rates["bond"] = bond

    def create_change_order(self, title: str, description: str,
                           change_type: ChangeType,
                           created_by: str = "") -> ChangeOrder:
        """Create new change order."""
        co_id = f"CO-{self.project_id}-{self.next_number:04d}"

        co = ChangeOrder(
            id=co_id,
            number=self.next_number,
            title=title,
            description=description,
            change_type=change_type,
            status=ChangeOrderStatus.DRAFT,
            identified_date=datetime.now(),
            created_by=created_by
        )

        self.change_orders[co_id] = co
        self.next_number += 1

        return co

    def add_line_item(self, co_id: str, description: str,
                     quantity: float, unit: str, unit_price: float,
                     spec_section: str = "", csi_code: str = "") -> ChangeOrderItem:
        """Add line item to change order."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]

        item_id = f"{co_id}-{len(co.line_items)+1:03d}"
        item = ChangeOrderItem(
            id=item_id,
            description=description,
            quantity=quantity,
            unit=unit,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            spec_section=spec_section,
            csi_code=csi_code
        )

        co.line_items.append(item)

        # Update totals
        self._recalculate_totals(co)

        return item

    def set_cost_breakdown(self, co_id: str, labor: float = 0,
                          materials: float = 0, equipment: float = 0,
                          subcontractor: float = 0) -> CostBreakdown:
        """Set cost breakdown and calculate markups."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]

        direct = labor + materials + equipment + subcontractor

        co.cost_breakdown = CostBreakdown(
            labor=labor,
            materials=materials,
            equipment=equipment,
            subcontractor=subcontractor,
            overhead=direct * self.markup_rates["overhead"],
            profit=direct * self.markup_rates["profit"],
            bond=direct * self.markup_rates["bond"]
        )

        co.proposed_amount = co.cost_breakdown.total

        return co.cost_breakdown

    def _recalculate_totals(self, co: ChangeOrder):
        """Recalculate change order totals from line items."""
        if co.line_items:
            direct_cost = sum(item.total_price for item in co.line_items)

            co.cost_breakdown.labor = direct_cost * 0.4  # Estimate
            co.cost_breakdown.materials = direct_cost * 0.4
            co.cost_breakdown.equipment = direct_cost * 0.1
            co.cost_breakdown.subcontractor = direct_cost * 0.1

            co.cost_breakdown.overhead = direct_cost * self.markup_rates["overhead"]
            co.cost_breakdown.profit = direct_cost * self.markup_rates["profit"]
            co.cost_breakdown.bond = direct_cost * self.markup_rates["bond"]

            co.proposed_amount = co.cost_breakdown.total

    def submit_change_order(self, co_id: str) -> ChangeOrder:
        """Submit change order for review."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]
        co.status = ChangeOrderStatus.SUBMITTED
        co.submitted_date = datetime.now()

        self._add_note(co, "Submitted for review")

        return co

    def approve_change_order(self, co_id: str, approved_amount: float,
                            approved_time: int = 0) -> ChangeOrder:
        """Approve change order."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]
        co.status = ChangeOrderStatus.APPROVED
        co.approved_date = datetime.now()
        co.approved_amount = approved_amount
        co.approved_time_days = approved_time

        self._add_note(co, f"Approved: ${approved_amount:,.2f}, {approved_time} days")

        return co

    def reject_change_order(self, co_id: str, reason: str) -> ChangeOrder:
        """Reject change order."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]
        co.status = ChangeOrderStatus.REJECTED

        self._add_note(co, f"Rejected: {reason}")

        return co

    def execute_change_order(self, co_id: str) -> ChangeOrder:
        """Mark change order as executed."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]
        if co.status != ChangeOrderStatus.APPROVED:
            raise ValueError("Change order must be approved before execution")

        co.status = ChangeOrderStatus.EXECUTED
        co.executed_date = datetime.now()

        self._add_note(co, "Executed")

        return co

    def _add_note(self, co: ChangeOrder, text: str):
        """Add note to change order."""
        co.notes.append({
            "timestamp": datetime.now().isoformat(),
            "text": text
        })

    def add_reference(self, co_id: str, ref_type: str, reference: str):
        """Add reference document to change order."""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order {co_id} not found")

        co = self.change_orders[co_id]

        if ref_type == "rfi":
            co.rfi_references.append(reference)
        elif ref_type == "drawing":
            co.drawing_references.append(reference)
        elif ref_type == "photo":
            co.photo_attachments.append(reference)
        elif ref_type == "backup":
            co.backup_documents.append(reference)

    def get_summary(self) -> Dict:
        """Get change order summary statistics."""
        total_approved = sum(
            co.approved_amount for co in self.change_orders.values()
            if co.status in [ChangeOrderStatus.APPROVED, ChangeOrderStatus.EXECUTED]
        )

        total_pending = sum(
            co.proposed_amount for co in self.change_orders.values()
            if co.status in [ChangeOrderStatus.SUBMITTED, ChangeOrderStatus.UNDER_REVIEW,
                            ChangeOrderStatus.PRICING, ChangeOrderStatus.NEGOTIATING]
        )

        by_type = {}
        for co in self.change_orders.values():
            t = co.change_type.value
            by_type[t] = by_type.get(t, 0) + (co.approved_amount or co.proposed_amount)

        by_status = {}
        for co in self.change_orders.values():
            s = co.status.value
            by_status[s] = by_status.get(s, 0) + 1

        return {
            "original_contract": self.original_contract,
            "total_approved": total_approved,
            "total_pending": total_pending,
            "revised_contract": self.original_contract + total_approved,
            "change_order_count": len(self.change_orders),
            "change_percentage": (total_approved / self.original_contract * 100) if self.original_contract else 0,
            "by_type": by_type,
            "by_status": by_status
        }

    def generate_log(self) -> str:
        """Generate change order log."""
        summary = self.get_summary()

        lines = [
            "# Change Order Log",
            "",
            f"**Project:** {self.project_name}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## Summary",
            "",
            f"| Metric | Amount |",
            f"|--------|--------|",
            f"| Original Contract | ${summary['original_contract']:,.2f} |",
            f"| Approved Changes | ${summary['total_approved']:,.2f} |",
            f"| Pending Changes | ${summary['total_pending']:,.2f} |",
            f"| **Revised Contract** | **${summary['revised_contract']:,.2f}** |",
            f"| Change % | {summary['change_percentage']:.1f}% |",
            "",
            "## Change Orders",
            "",
            "| # | Title | Type | Status | Proposed | Approved | Time |",
            "|---|-------|------|--------|----------|----------|------|"
        ]

        for co in sorted(self.change_orders.values(), key=lambda x: x.number):
            lines.append(
                f"| {co.number} | {co.title[:30]} | {co.change_type.value} | "
                f"{co.status.value} | ${co.proposed_amount:,.0f} | "
                f"${co.approved_amount:,.0f} | {co.approved_time_days}d |"
            )

        return "\n".join(lines)

    def generate_co_document(self, co_id: str) -> str:
        """Generate formal change order document."""
        if co_id not in self.change_orders:
            return "Change order not found"

        co = self.change_orders[co_id]

        lines = [
            f"# CHANGE ORDER NO. {co.number}",
            "",
            f"**Project:** {self.project_name}",
            f"**Change Order ID:** {co.id}",
            f"**Date:** {co.submitted_date.strftime('%Y-%m-%d') if co.submitted_date else 'Draft'}",
            "",
            "---",
            "",
            f"## Description of Change",
            "",
            co.description,
            "",
            f"**Type:** {co.change_type.value.replace('_', ' ').title()}",
            "",
        ]

        if co.line_items:
            lines.extend([
                "## Schedule of Values",
                "",
                "| Item | Description | Qty | Unit | Unit Price | Total |",
                "|------|-------------|-----|------|------------|-------|"
            ])
            for item in co.line_items:
                lines.append(
                    f"| {item.id} | {item.description} | {item.quantity} | "
                    f"{item.unit} | ${item.unit_price:,.2f} | ${item.total_price:,.2f} |"
                )
            lines.append("")

        lines.extend([
            "## Cost Summary",
            "",
            f"| Category | Amount |",
            f"|----------|--------|",
            f"| Labor | ${co.cost_breakdown.labor:,.2f} |",
            f"| Materials | ${co.cost_breakdown.materials:,.2f} |",
            f"| Equipment | ${co.cost_breakdown.equipment:,.2f} |",
            f"| Subcontractor | ${co.cost_breakdown.subcontractor:,.2f} |",
            f"| Overhead | ${co.cost_breakdown.overhead:,.2f} |",
            f"| Profit | ${co.cost_breakdown.profit:,.2f} |",
            f"| Bond | ${co.cost_breakdown.bond:,.2f} |",
            f"| **Total** | **${co.cost_breakdown.total:,.2f}** |",
            "",
            f"## Time Impact",
            "",
            f"Proposed Extension: **{co.proposed_time_days} days**",
            f"Critical Path Impact: {'Yes' if co.impacts_critical_path else 'No'}",
            "",
        ])

        if co.rfi_references:
            lines.extend([
                "## References",
                "",
                f"- RFIs: {', '.join(co.rfi_references)}",
                f"- Drawings: {', '.join(co.drawing_references)}" if co.drawing_references else "",
            ])

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize manager
manager = ChangeOrderManager(
    project_id="PRJ-001",
    project_name="Office Tower",
    original_contract=5000000.0
)

# Create change order
co = manager.create_change_order(
    title="Additional Structural Steel",
    description="Add steel reinforcement at Level 5 per RFI-042",
    change_type=ChangeType.DESIGN_ERROR,
    created_by="Project Manager"
)

# Add line items
manager.add_line_item(
    co.id,
    "W12x26 Steel Beam",
    quantity=450,
    unit="LF",
    unit_price=85.00,
    csi_code="05 12 00"
)

# Or set cost breakdown directly
manager.set_cost_breakdown(
    co.id,
    labor=15000,
    materials=25000,
    equipment=2000,
    subcontractor=5000
)

# Add references
manager.add_reference(co.id, "rfi", "RFI-042")
manager.add_reference(co.id, "drawing", "S-501 Rev 2")

# Submit for approval
manager.submit_change_order(co.id)

# Approve (with negotiated amount)
manager.approve_change_order(co.id, approved_amount=50000, approved_time=5)

# Generate documents
print(manager.generate_co_document(co.id))
print(manager.generate_log())
```

## Requirements

```bash
pip install (no external dependencies)
```
