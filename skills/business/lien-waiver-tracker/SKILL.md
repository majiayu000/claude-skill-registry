---
name: lien-waiver-tracker
description: "Track and manage construction lien waivers. Monitor conditional and unconditional waivers, ensure compliance before payments, and prevent lien exposure."
---

# Lien Waiver Tracker

## Overview

Track and manage lien waivers throughout the construction payment process. Ensure proper waivers are received before releasing payments, monitor waiver status by subcontractor, and minimize lien exposure.

## Lien Waiver Types

```
┌─────────────────────────────────────────────────────────────────┐
│                    LIEN WAIVER TYPES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONDITIONAL                        UNCONDITIONAL                │
│  ───────────                        ─────────────                │
│  📋 Progress - Conditional          ✅ Progress - Unconditional  │
│     Effective when paid                Immediately effective     │
│     Use with payment                   Use after check clears    │
│                                                                  │
│  📋 Final - Conditional             ✅ Final - Unconditional     │
│     For final payment                  For final payment         │
│     Upon receipt of funds              After funds received      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class WaiverType(Enum):
    CONDITIONAL_PROGRESS = "conditional_progress"
    UNCONDITIONAL_PROGRESS = "unconditional_progress"
    CONDITIONAL_FINAL = "conditional_final"
    UNCONDITIONAL_FINAL = "unconditional_final"

class WaiverStatus(Enum):
    REQUESTED = "requested"
    RECEIVED = "received"
    VERIFIED = "verified"
    REJECTED = "rejected"
    MISSING = "missing"

class PaymentStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    HELD = "held"
    RELEASED = "released"

@dataclass
class Subcontractor:
    id: str
    name: str
    trade: str
    contract_amount: float
    contact_name: str
    contact_email: str
    tier: int = 1  # 1 = direct, 2 = sub-sub

@dataclass
class LienWaiver:
    id: str
    subcontractor_id: str
    waiver_type: WaiverType
    payment_application: int  # Pay app number
    through_date: datetime
    amount: float
    status: WaiverStatus = WaiverStatus.REQUESTED
    requested_date: datetime = field(default_factory=datetime.now)
    received_date: Optional[datetime] = None
    verified_by: str = ""
    file_path: str = ""
    notes: str = ""

@dataclass
class PaymentApplication:
    number: int
    period_end: datetime
    subcontractor_id: str
    amount_requested: float
    amount_approved: float
    retainage: float
    status: PaymentStatus = PaymentStatus.PENDING
    waivers_complete: bool = False
    payment_date: Optional[datetime] = None

@dataclass
class LienExposure:
    subcontractor_id: str
    subcontractor_name: str
    total_paid: float
    unconditional_waivers: float
    conditional_pending: float
    exposure: float

class LienWaiverTracker:
    """Track and manage construction lien waivers."""

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name
        self.subcontractors: Dict[str, Subcontractor] = {}
        self.waivers: Dict[str, LienWaiver] = {}
        self.pay_apps: Dict[str, PaymentApplication] = {}

    def add_subcontractor(self, id: str, name: str, trade: str,
                         contract_amount: float, contact_name: str,
                         contact_email: str, tier: int = 1) -> Subcontractor:
        """Add subcontractor to tracking."""
        sub = Subcontractor(
            id=id,
            name=name,
            trade=trade,
            contract_amount=contract_amount,
            contact_name=contact_name,
            contact_email=contact_email,
            tier=tier
        )
        self.subcontractors[id] = sub
        return sub

    def create_payment_application(self, number: int, period_end: datetime,
                                  subcontractor_id: str, amount_requested: float,
                                  retainage_rate: float = 0.10) -> PaymentApplication:
        """Create payment application record."""
        if subcontractor_id not in self.subcontractors:
            raise ValueError(f"Subcontractor {subcontractor_id} not found")

        retainage = amount_requested * retainage_rate
        amount_approved = amount_requested - retainage

        pay_app = PaymentApplication(
            number=number,
            period_end=period_end,
            subcontractor_id=subcontractor_id,
            amount_requested=amount_requested,
            amount_approved=amount_approved,
            retainage=retainage
        )

        key = f"{subcontractor_id}-{number}"
        self.pay_apps[key] = pay_app

        # Create waiver request
        self.request_waiver(subcontractor_id, number, period_end, amount_approved)

        return pay_app

    def request_waiver(self, subcontractor_id: str, pay_app_number: int,
                      through_date: datetime, amount: float,
                      waiver_type: WaiverType = WaiverType.CONDITIONAL_PROGRESS) -> LienWaiver:
        """Request lien waiver from subcontractor."""
        waiver_id = f"LW-{subcontractor_id}-{pay_app_number}"

        waiver = LienWaiver(
            id=waiver_id,
            subcontractor_id=subcontractor_id,
            waiver_type=waiver_type,
            payment_application=pay_app_number,
            through_date=through_date,
            amount=amount
        )

        self.waivers[waiver_id] = waiver
        return waiver

    def receive_waiver(self, waiver_id: str, file_path: str,
                      verified_by: str = "") -> LienWaiver:
        """Record receipt of lien waiver."""
        if waiver_id not in self.waivers:
            raise ValueError(f"Waiver {waiver_id} not found")

        waiver = self.waivers[waiver_id]
        waiver.status = WaiverStatus.RECEIVED
        waiver.received_date = datetime.now()
        waiver.file_path = file_path
        waiver.verified_by = verified_by

        # Check if all waivers for pay app complete
        self._check_pay_app_waivers(waiver.subcontractor_id, waiver.payment_application)

        return waiver

    def verify_waiver(self, waiver_id: str, verified_by: str) -> LienWaiver:
        """Verify waiver details are correct."""
        if waiver_id not in self.waivers:
            raise ValueError(f"Waiver {waiver_id} not found")

        waiver = self.waivers[waiver_id]
        waiver.status = WaiverStatus.VERIFIED
        waiver.verified_by = verified_by

        return waiver

    def reject_waiver(self, waiver_id: str, reason: str) -> LienWaiver:
        """Reject waiver (incorrect amount, wrong form, etc.)."""
        if waiver_id not in self.waivers:
            raise ValueError(f"Waiver {waiver_id} not found")

        waiver = self.waivers[waiver_id]
        waiver.status = WaiverStatus.REJECTED
        waiver.notes = f"Rejected: {reason}"

        return waiver

    def convert_to_unconditional(self, waiver_id: str, payment_date: datetime) -> LienWaiver:
        """Convert conditional waiver to unconditional after payment clears."""
        if waiver_id not in self.waivers:
            raise ValueError(f"Waiver {waiver_id} not found")

        waiver = self.waivers[waiver_id]

        # Create new unconditional waiver
        new_type = (WaiverType.UNCONDITIONAL_PROGRESS
                   if waiver.waiver_type == WaiverType.CONDITIONAL_PROGRESS
                   else WaiverType.UNCONDITIONAL_FINAL)

        return self.request_waiver(
            waiver.subcontractor_id,
            waiver.payment_application,
            waiver.through_date,
            waiver.amount,
            new_type
        )

    def _check_pay_app_waivers(self, subcontractor_id: str, pay_app_number: int):
        """Check if all waivers for pay app are received."""
        key = f"{subcontractor_id}-{pay_app_number}"

        if key not in self.pay_apps:
            return

        pay_app = self.pay_apps[key]

        # Check all related waivers
        related_waivers = [
            w for w in self.waivers.values()
            if w.subcontractor_id == subcontractor_id
            and w.payment_application == pay_app_number
        ]

        pay_app.waivers_complete = all(
            w.status in [WaiverStatus.RECEIVED, WaiverStatus.VERIFIED]
            for w in related_waivers
        )

    def calculate_exposure(self, subcontractor_id: str) -> LienExposure:
        """Calculate lien exposure for subcontractor."""
        if subcontractor_id not in self.subcontractors:
            raise ValueError(f"Subcontractor {subcontractor_id} not found")

        sub = self.subcontractors[subcontractor_id]

        # Sum payments
        total_paid = sum(
            pa.amount_approved for pa in self.pay_apps.values()
            if pa.subcontractor_id == subcontractor_id
            and pa.status == PaymentStatus.RELEASED
        )

        # Sum unconditional waivers
        unconditional = sum(
            w.amount for w in self.waivers.values()
            if w.subcontractor_id == subcontractor_id
            and w.waiver_type in [WaiverType.UNCONDITIONAL_PROGRESS, WaiverType.UNCONDITIONAL_FINAL]
            and w.status in [WaiverStatus.RECEIVED, WaiverStatus.VERIFIED]
        )

        # Sum conditional pending
        conditional = sum(
            w.amount for w in self.waivers.values()
            if w.subcontractor_id == subcontractor_id
            and w.waiver_type in [WaiverType.CONDITIONAL_PROGRESS, WaiverType.CONDITIONAL_FINAL]
            and w.status in [WaiverStatus.RECEIVED, WaiverStatus.VERIFIED]
        )

        # Exposure = Paid - Unconditional waivers
        exposure = total_paid - unconditional

        return LienExposure(
            subcontractor_id=subcontractor_id,
            subcontractor_name=sub.name,
            total_paid=total_paid,
            unconditional_waivers=unconditional,
            conditional_pending=conditional,
            exposure=exposure
        )

    def get_missing_waivers(self) -> List[Dict]:
        """Get list of missing or pending waivers."""
        missing = []

        for waiver in self.waivers.values():
            if waiver.status in [WaiverStatus.REQUESTED, WaiverStatus.MISSING]:
                sub = self.subcontractors.get(waiver.subcontractor_id)
                missing.append({
                    "waiver_id": waiver.id,
                    "subcontractor": sub.name if sub else waiver.subcontractor_id,
                    "pay_app": waiver.payment_application,
                    "amount": waiver.amount,
                    "type": waiver.waiver_type.value,
                    "requested_date": waiver.requested_date,
                    "days_outstanding": (datetime.now() - waiver.requested_date).days
                })

        return sorted(missing, key=lambda x: -x["days_outstanding"])

    def get_waiver_status_by_sub(self, subcontractor_id: str) -> Dict:
        """Get waiver status summary for subcontractor."""
        if subcontractor_id not in self.subcontractors:
            raise ValueError(f"Subcontractor {subcontractor_id} not found")

        sub = self.subcontractors[subcontractor_id]

        waivers = [w for w in self.waivers.values() if w.subcontractor_id == subcontractor_id]

        by_status = {}
        for w in waivers:
            s = w.status.value
            by_status[s] = by_status.get(s, 0) + 1

        return {
            "subcontractor": sub.name,
            "total_waivers": len(waivers),
            "by_status": by_status,
            "total_amount": sum(w.amount for w in waivers),
            "verified_amount": sum(w.amount for w in waivers if w.status == WaiverStatus.VERIFIED)
        }

    def can_release_payment(self, subcontractor_id: str, pay_app_number: int) -> Dict:
        """Check if payment can be released."""
        key = f"{subcontractor_id}-{pay_app_number}"

        if key not in self.pay_apps:
            return {"can_release": False, "reason": "Payment application not found"}

        pay_app = self.pay_apps[key]

        # Check for conditional waiver
        waivers = [
            w for w in self.waivers.values()
            if w.subcontractor_id == subcontractor_id
            and w.payment_application == pay_app_number
            and w.waiver_type == WaiverType.CONDITIONAL_PROGRESS
        ]

        if not waivers:
            return {"can_release": False, "reason": "No conditional waiver received"}

        for w in waivers:
            if w.status not in [WaiverStatus.RECEIVED, WaiverStatus.VERIFIED]:
                return {"can_release": False, "reason": f"Waiver {w.id} not verified"}

        return {"can_release": True, "reason": "All waivers verified", "amount": pay_app.amount_approved}

    def generate_report(self) -> str:
        """Generate lien waiver status report."""
        lines = [
            "# Lien Waiver Status Report",
            "",
            f"**Project:** {self.project_name}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## Summary",
            "",
            f"- Total Subcontractors: {len(self.subcontractors)}",
            f"- Total Waivers Tracked: {len(self.waivers)}",
            f"- Missing Waivers: {len(self.get_missing_waivers())}",
            "",
            "## Exposure by Subcontractor",
            "",
            "| Subcontractor | Paid | Unconditional | Exposure |",
            "|---------------|------|---------------|----------|"
        ]

        total_exposure = 0
        for sub_id in self.subcontractors:
            exposure = self.calculate_exposure(sub_id)
            total_exposure += exposure.exposure
            lines.append(
                f"| {exposure.subcontractor_name} | ${exposure.total_paid:,.0f} | "
                f"${exposure.unconditional_waivers:,.0f} | ${exposure.exposure:,.0f} |"
            )

        lines.extend([
            f"| **TOTAL** | | | **${total_exposure:,.0f}** |",
            "",
            "## Missing Waivers",
            ""
        ])

        missing = self.get_missing_waivers()
        if missing:
            lines.append("| Subcontractor | Pay App | Amount | Days Outstanding |")
            lines.append("|---------------|---------|--------|------------------|")
            for m in missing[:10]:
                lines.append(
                    f"| {m['subcontractor']} | #{m['pay_app']} | "
                    f"${m['amount']:,.0f} | {m['days_outstanding']} |"
                )
        else:
            lines.append("*No missing waivers*")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize tracker
tracker = LienWaiverTracker("PRJ-001", "Office Tower")

# Add subcontractors
tracker.add_subcontractor(
    "SUB-001", "ABC Mechanical", "HVAC",
    contract_amount=500000,
    contact_name="John Smith",
    contact_email="john@abcmech.com"
)

tracker.add_subcontractor(
    "SUB-002", "XYZ Electric", "Electrical",
    contract_amount=350000,
    contact_name="Jane Doe",
    contact_email="jane@xyzelectric.com"
)

# Create payment applications
pa1 = tracker.create_payment_application(
    number=1,
    period_end=datetime.now(),
    subcontractor_id="SUB-001",
    amount_requested=50000
)

# Receive waiver
waiver_id = f"LW-SUB-001-1"
tracker.receive_waiver(waiver_id, "/waivers/sub001_pa1.pdf", "PM")

# Check if can release payment
result = tracker.can_release_payment("SUB-001", 1)
print(f"Can release: {result['can_release']} - {result['reason']}")

# Calculate exposure
exposure = tracker.calculate_exposure("SUB-001")
print(f"Lien exposure: ${exposure.exposure:,.2f}")

# Generate report
print(tracker.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
