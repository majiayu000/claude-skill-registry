---
name: claims-documentation
description: "Document construction claims for disputes and recovery. Compile evidence, calculate damages, track notice requirements, and prepare claim packages."
---

# Claims Documentation

## Overview

Document and manage construction claims for schedule delays, cost impacts, and scope disputes. Track contractual notice requirements, compile supporting evidence, calculate damages, and prepare comprehensive claim packages.

## Claims Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAIMS PROCESS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Notice  →  Document  →  Quantify  →  Submit  →  Negotiate     │
│  ──────     ────────     ────────     ──────     ─────────     │
│  📋 Identify  📂 Collect   💰 Calculate  📤 Package  🤝 Resolve │
│  📧 Timely    📸 Evidence  ⏱️ Time       📋 Format   ⚖️ Settle  │
│  📝 Written   📄 Chain     📊 Cost       ✓ Review   💵 Payment  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class ClaimType(Enum):
    DELAY = "delay"
    DISRUPTION = "disruption"
    ACCELERATION = "acceleration"
    DIFFERING_CONDITIONS = "differing_conditions"
    OWNER_CHANGE = "owner_change"
    SUSPENSION = "suspension"
    TERMINATION = "termination"
    DEFECTIVE_SPECS = "defective_specs"

class ClaimStatus(Enum):
    DRAFT = "draft"
    NOTICE_SENT = "notice_sent"
    DOCUMENTING = "documenting"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    NEGOTIATING = "negotiating"
    SETTLED = "settled"
    DISPUTED = "disputed"
    LITIGATION = "litigation"
    WITHDRAWN = "withdrawn"

class EvidenceType(Enum):
    DAILY_REPORT = "daily_report"
    PHOTO = "photo"
    VIDEO = "video"
    EMAIL = "email"
    LETTER = "letter"
    MEETING_MINUTES = "meeting_minutes"
    SCHEDULE = "schedule"
    COST_RECORD = "cost_record"
    INVOICE = "invoice"
    TIMESHEET = "timesheet"
    WEATHER_DATA = "weather_data"
    DELIVERY_TICKET = "delivery_ticket"
    INSPECTION_REPORT = "inspection_report"
    RFI = "rfi"
    SUBMITTAL = "submittal"

@dataclass
class Evidence:
    id: str
    evidence_type: EvidenceType
    description: str
    date: datetime
    file_path: str
    source: str
    relevance: str
    authenticated: bool = False

@dataclass
class NoticeRequirement:
    notice_type: str
    deadline_days: int
    recipient: str
    method: str  # Written, certified mail, etc.
    contract_reference: str
    sent: bool = False
    sent_date: Optional[datetime] = None
    confirmation: str = ""

@dataclass
class DamageCalculation:
    category: str
    description: str
    amount: float
    basis: str  # How calculated
    supporting_docs: List[str] = field(default_factory=list)

@dataclass
class Claim:
    id: str
    claim_type: ClaimType
    title: str
    description: str
    status: ClaimStatus

    # Event details
    event_date: datetime
    discovery_date: datetime
    responsible_party: str
    contract_references: List[str] = field(default_factory=list)

    # Notice
    notice_requirements: List[NoticeRequirement] = field(default_factory=list)
    notice_compliant: bool = False

    # Documentation
    evidence: List[Evidence] = field(default_factory=list)
    narrative: str = ""

    # Damages
    time_claimed_days: int = 0
    cost_claimed: float = 0.0
    damage_calculations: List[DamageCalculation] = field(default_factory=list)

    # Resolution
    time_awarded_days: int = 0
    amount_awarded: float = 0.0
    settlement_date: Optional[datetime] = None
    settlement_notes: str = ""

class ClaimsDocumentor:
    """Document and manage construction claims."""

    # Common notice requirements
    DEFAULT_NOTICE_REQUIREMENTS = {
        ClaimType.DELAY: [
            {"notice_type": "Intent to Claim", "deadline_days": 21, "method": "Written"},
            {"notice_type": "Detailed Claim", "deadline_days": 45, "method": "Written"},
        ],
        ClaimType.DIFFERING_CONDITIONS: [
            {"notice_type": "Immediate Notice", "deadline_days": 2, "method": "Written/Verbal"},
            {"notice_type": "Written Notice", "deadline_days": 7, "method": "Written"},
        ],
        ClaimType.OWNER_CHANGE: [
            {"notice_type": "Notice of Impact", "deadline_days": 14, "method": "Written"},
        ],
    }

    def __init__(self, project_name: str, contract_date: datetime):
        self.project_name = project_name
        self.contract_date = contract_date
        self.claims: Dict[str, Claim] = {}

    def create_claim(self, claim_type: ClaimType, title: str,
                    description: str, event_date: datetime,
                    responsible_party: str) -> Claim:
        """Create new claim."""
        claim_id = f"CLM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        claim = Claim(
            id=claim_id,
            claim_type=claim_type,
            title=title,
            description=description,
            status=ClaimStatus.DRAFT,
            event_date=event_date,
            discovery_date=datetime.now(),
            responsible_party=responsible_party
        )

        # Add default notice requirements
        for req in self.DEFAULT_NOTICE_REQUIREMENTS.get(claim_type, []):
            notice = NoticeRequirement(
                notice_type=req["notice_type"],
                deadline_days=req["deadline_days"],
                recipient=responsible_party,
                method=req["method"],
                contract_reference=""
            )
            claim.notice_requirements.append(notice)

        self.claims[claim_id] = claim
        return claim

    def record_notice_sent(self, claim_id: str, notice_type: str,
                          confirmation: str = "") -> NoticeRequirement:
        """Record that notice was sent."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]

        for notice in claim.notice_requirements:
            if notice.notice_type == notice_type:
                notice.sent = True
                notice.sent_date = datetime.now()
                notice.confirmation = confirmation

                # Check overall notice compliance
                claim.notice_compliant = all(n.sent for n in claim.notice_requirements)

                if claim.status == ClaimStatus.DRAFT:
                    claim.status = ClaimStatus.NOTICE_SENT

                return notice

        raise ValueError(f"Notice type {notice_type} not found")

    def check_notice_deadlines(self, claim_id: str) -> List[Dict]:
        """Check status of notice deadlines."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]
        status = []

        for notice in claim.notice_requirements:
            deadline = claim.event_date + timedelta(days=notice.deadline_days)
            days_remaining = (deadline - datetime.now()).days

            status.append({
                "notice_type": notice.notice_type,
                "deadline": deadline,
                "days_remaining": days_remaining,
                "sent": notice.sent,
                "overdue": days_remaining < 0 and not notice.sent,
                "status": "Sent" if notice.sent else ("OVERDUE" if days_remaining < 0 else f"{days_remaining} days left")
            })

        return status

    def add_evidence(self, claim_id: str, evidence_type: EvidenceType,
                    description: str, date: datetime, file_path: str,
                    source: str, relevance: str) -> Evidence:
        """Add evidence to claim."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        evidence_id = f"EVD-{len(self.claims[claim_id].evidence)+1:04d}"

        evidence = Evidence(
            id=evidence_id,
            evidence_type=evidence_type,
            description=description,
            date=date,
            file_path=file_path,
            source=source,
            relevance=relevance
        )

        self.claims[claim_id].evidence.append(evidence)

        if self.claims[claim_id].status == ClaimStatus.NOTICE_SENT:
            self.claims[claim_id].status = ClaimStatus.DOCUMENTING

        return evidence

    def add_damage_calculation(self, claim_id: str, category: str,
                              description: str, amount: float,
                              basis: str, supporting_docs: List[str] = None) -> DamageCalculation:
        """Add damage calculation to claim."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        calc = DamageCalculation(
            category=category,
            description=description,
            amount=amount,
            basis=basis,
            supporting_docs=supporting_docs or []
        )

        claim = self.claims[claim_id]
        claim.damage_calculations.append(calc)

        # Update total claimed
        claim.cost_claimed = sum(c.amount for c in claim.damage_calculations)

        return calc

    def calculate_delay_damages(self, claim_id: str, delay_days: int,
                               daily_rate: float,
                               include_escalation: bool = True) -> Dict:
        """Calculate delay damages using Eichleay formula or daily rate."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]

        # Direct costs
        extended_general_conditions = delay_days * daily_rate

        # Add standard categories
        self.add_damage_calculation(
            claim_id, "Extended General Conditions",
            f"{delay_days} days × ${daily_rate:,.2f}/day",
            extended_general_conditions,
            "Daily rate method"
        )

        # Escalation (if applicable)
        escalation = 0
        if include_escalation:
            escalation = extended_general_conditions * 0.03  # 3% escalation
            self.add_damage_calculation(
                claim_id, "Material/Labor Escalation",
                "Cost increase due to extended duration",
                escalation,
                "3% escalation factor"
            )

        claim.time_claimed_days = delay_days

        return {
            "delay_days": delay_days,
            "daily_rate": daily_rate,
            "extended_gc": extended_general_conditions,
            "escalation": escalation,
            "total": claim.cost_claimed
        }

    def write_narrative(self, claim_id: str, narrative: str):
        """Write claim narrative."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        self.claims[claim_id].narrative = narrative

    def submit_claim(self, claim_id: str) -> Claim:
        """Submit claim."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]
        claim.status = ClaimStatus.SUBMITTED
        return claim

    def record_settlement(self, claim_id: str, time_awarded: int,
                         amount_awarded: float, notes: str = "") -> Claim:
        """Record claim settlement."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]
        claim.status = ClaimStatus.SETTLED
        claim.time_awarded_days = time_awarded
        claim.amount_awarded = amount_awarded
        claim.settlement_date = datetime.now()
        claim.settlement_notes = notes

        return claim

    def generate_evidence_index(self, claim_id: str) -> str:
        """Generate evidence index."""
        if claim_id not in self.claims:
            return "Claim not found"

        claim = self.claims[claim_id]

        lines = [
            "# Evidence Index",
            "",
            f"**Claim:** {claim.title}",
            f"**Claim ID:** {claim.id}",
            "",
            "| # | Type | Date | Description | Source | Relevance |",
            "|---|------|------|-------------|--------|-----------|"
        ]

        for i, ev in enumerate(sorted(claim.evidence, key=lambda e: e.date), 1):
            lines.append(
                f"| {i} | {ev.evidence_type.value} | {ev.date.strftime('%Y-%m-%d')} | "
                f"{ev.description[:30]} | {ev.source} | {ev.relevance[:30]} |"
            )

        return "\n".join(lines)

    def generate_claim_package(self, claim_id: str) -> str:
        """Generate complete claim package."""
        if claim_id not in self.claims:
            return "Claim not found"

        claim = self.claims[claim_id]

        lines = [
            "# CLAIM PACKAGE",
            "",
            f"## Claim: {claim.title}",
            "",
            f"**Claim ID:** {claim.id}",
            f"**Type:** {claim.claim_type.value.replace('_', ' ').title()}",
            f"**Status:** {claim.status.value}",
            f"**Event Date:** {claim.event_date.strftime('%Y-%m-%d')}",
            f"**Responsible Party:** {claim.responsible_party}",
            "",
            "---",
            "",
            "## 1. Executive Summary",
            "",
            claim.description,
            "",
            f"**Time Claimed:** {claim.time_claimed_days} days",
            f"**Amount Claimed:** ${claim.cost_claimed:,.2f}",
            "",
            "## 2. Factual Narrative",
            "",
            claim.narrative if claim.narrative else "*Narrative pending*",
            "",
            "## 3. Contract References",
            "",
        ]

        for ref in claim.contract_references:
            lines.append(f"- {ref}")

        lines.extend([
            "",
            "## 4. Notice Compliance",
            "",
            "| Notice Type | Deadline | Status | Sent Date |",
            "|-------------|----------|--------|-----------|"
        ])

        for notice in claim.notice_requirements:
            deadline = claim.event_date + timedelta(days=notice.deadline_days)
            status = "✓ Sent" if notice.sent else "Pending"
            sent = notice.sent_date.strftime('%Y-%m-%d') if notice.sent_date else "-"
            lines.append(f"| {notice.notice_type} | {deadline.strftime('%Y-%m-%d')} | {status} | {sent} |")

        lines.extend([
            "",
            "## 5. Damage Calculations",
            "",
            "| Category | Description | Amount | Basis |",
            "|----------|-------------|--------|-------|"
        ])

        for calc in claim.damage_calculations:
            lines.append(f"| {calc.category} | {calc.description} | ${calc.amount:,.2f} | {calc.basis} |")

        lines.extend([
            "",
            f"**Total Claimed: ${claim.cost_claimed:,.2f}**",
            "",
            "## 6. Evidence Summary",
            "",
            f"Total Documents: {len(claim.evidence)}",
            ""
        ])

        # Group evidence by type
        by_type = {}
        for ev in claim.evidence:
            t = ev.evidence_type.value
            by_type[t] = by_type.get(t, 0) + 1

        for t, count in sorted(by_type.items()):
            lines.append(f"- {t.replace('_', ' ').title()}: {count}")

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize documentor
documentor = ClaimsDocumentor("Office Tower", datetime(2024, 1, 1))

# Create claim
claim = documentor.create_claim(
    claim_type=ClaimType.DELAY,
    title="Owner-Caused Delay - Design Changes",
    description="Multiple design changes to structural system caused 45-day delay",
    event_date=datetime(2024, 6, 15),
    responsible_party="Owner"
)

# Check notice deadlines
deadlines = documentor.check_notice_deadlines(claim.id)
for d in deadlines:
    print(f"{d['notice_type']}: {d['status']}")

# Record notice sent
documentor.record_notice_sent(claim.id, "Intent to Claim", "Certified Mail #12345")

# Add evidence
documentor.add_evidence(
    claim.id,
    EvidenceType.RFI,
    "RFI-042 requesting structural clarification",
    datetime(2024, 6, 10),
    "/docs/RFI-042.pdf",
    "Project Files",
    "Shows owner's delayed response"
)

# Calculate damages
damages = documentor.calculate_delay_damages(
    claim.id,
    delay_days=45,
    daily_rate=5000.0
)
print(f"Total damages: ${damages['total']:,.2f}")

# Write narrative
documentor.write_narrative(claim.id, """
On June 15, 2024, the Owner issued a design change directive requiring
modifications to the structural steel at Levels 5-8. This change...
""")

# Generate claim package
print(documentor.generate_claim_package(claim.id))
```

## Requirements

```bash
pip install (no external dependencies)
```
