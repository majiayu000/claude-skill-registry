---
slug: "compliance-tracker"
display_name: "Compliance Tracker"
description: "Track regulatory compliance for construction projects. Monitor permits, certifications, inspections, and regulatory requirements with automated alerts and reporting."
---

# Compliance Tracker

## Overview

Track and manage regulatory compliance across construction projects. Monitor permits, licenses, certifications, inspections, and regulatory requirements. Automated alerts for expirations and deadlines.

> "Proactive compliance tracking prevents costly project delays and penalties" — DDC Community

## Compliance Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE TRACKING                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Permits          Certifications    Inspections    Training     │
│  ───────          ──────────────    ───────────    ────────     │
│  🏗️ Building      👷 Workers         📋 Fire        🎓 OSHA      │
│  🔥 Fire          🏢 Company         ⚡ Electrical   🦺 Safety    │
│  ⚡ Electrical    🔧 Equipment       🔧 Mechanical   🏗️ Trade     │
│  🚰 Plumbing      📜 Insurance       🏗️ Structural  🚗 Equipment │
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

class ComplianceType(Enum):
    PERMIT = "permit"
    LICENSE = "license"
    CERTIFICATION = "certification"
    INSURANCE = "insurance"
    INSPECTION = "inspection"
    TRAINING = "training"
    SUBMITTAL = "submittal"

class ComplianceStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    EXPIRING_SOON = "expiring_soon"
    NOT_APPLICABLE = "not_applicable"
    REJECTED = "rejected"

class Priority(Enum):
    CRITICAL = "critical"  # Work stoppage if missing
    HIGH = "high"          # Significant impact
    MEDIUM = "medium"      # Moderate impact
    LOW = "low"            # Administrative

@dataclass
class ComplianceItem:
    id: str
    name: str
    compliance_type: ComplianceType
    category: str
    description: str

    # Dates
    issue_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None

    # Status
    status: ComplianceStatus = ComplianceStatus.PENDING
    priority: Priority = Priority.MEDIUM

    # Ownership
    responsible_party: str = ""
    issuing_authority: str = ""

    # Documentation
    document_url: str = ""
    reference_number: str = ""
    notes: str = ""

    # Tracking
    alert_days_before: int = 30
    last_checked: Optional[datetime] = None

@dataclass
class ComplianceAlert:
    id: str
    compliance_item_id: str
    alert_type: str  # expiring, expired, action_required
    message: str
    due_date: datetime
    acknowledged: bool = False
    acknowledged_by: str = ""

class ComplianceTracker:
    """Track construction regulatory compliance."""

    # Standard compliance requirements by project type
    STANDARD_REQUIREMENTS = {
        "commercial": [
            {"name": "Building Permit", "type": ComplianceType.PERMIT, "category": "Building", "priority": Priority.CRITICAL},
            {"name": "Fire Permit", "type": ComplianceType.PERMIT, "category": "Fire", "priority": Priority.CRITICAL},
            {"name": "Electrical Permit", "type": ComplianceType.PERMIT, "category": "Electrical", "priority": Priority.HIGH},
            {"name": "Plumbing Permit", "type": ComplianceType.PERMIT, "category": "Plumbing", "priority": Priority.HIGH},
            {"name": "Mechanical Permit", "type": ComplianceType.PERMIT, "category": "Mechanical", "priority": Priority.HIGH},
            {"name": "General Liability Insurance", "type": ComplianceType.INSURANCE, "category": "Insurance", "priority": Priority.CRITICAL},
            {"name": "Workers Comp Insurance", "type": ComplianceType.INSURANCE, "category": "Insurance", "priority": Priority.CRITICAL},
            {"name": "OSHA 10/30 Training", "type": ComplianceType.TRAINING, "category": "Safety", "priority": Priority.HIGH},
        ],
        "residential": [
            {"name": "Building Permit", "type": ComplianceType.PERMIT, "category": "Building", "priority": Priority.CRITICAL},
            {"name": "Electrical Permit", "type": ComplianceType.PERMIT, "category": "Electrical", "priority": Priority.HIGH},
            {"name": "Plumbing Permit", "type": ComplianceType.PERMIT, "category": "Plumbing", "priority": Priority.HIGH},
            {"name": "General Liability Insurance", "type": ComplianceType.INSURANCE, "category": "Insurance", "priority": Priority.CRITICAL},
        ]
    }

    # Required inspections by permit type
    REQUIRED_INSPECTIONS = {
        "Building": ["Foundation", "Framing", "Insulation", "Final"],
        "Electrical": ["Rough-in", "Service", "Final"],
        "Plumbing": ["Underground", "Rough-in", "Final"],
        "Mechanical": ["Rough-in", "Final"],
        "Fire": ["Underground", "Rough-in", "Final", "Alarm"]
    }

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name
        self.compliance_items: Dict[str, ComplianceItem] = {}
        self.alerts: List[ComplianceAlert] = []

    def initialize_requirements(self, project_type: str = "commercial") -> List[ComplianceItem]:
        """Initialize standard compliance requirements."""
        requirements = self.STANDARD_REQUIREMENTS.get(project_type, [])
        created = []

        for req in requirements:
            item = self.add_compliance_item(
                name=req["name"],
                compliance_type=req["type"],
                category=req["category"],
                description=f"Standard {req['name']} requirement",
                priority=req["priority"]
            )
            created.append(item)

        return created

    def add_compliance_item(self, name: str, compliance_type: ComplianceType,
                           category: str, description: str = "",
                           priority: Priority = Priority.MEDIUM,
                           expiration_date: datetime = None,
                           responsible_party: str = "",
                           issuing_authority: str = "") -> ComplianceItem:
        """Add compliance item to track."""
        item_id = f"COMP-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.compliance_items)}"

        item = ComplianceItem(
            id=item_id,
            name=name,
            compliance_type=compliance_type,
            category=category,
            description=description,
            priority=priority,
            expiration_date=expiration_date,
            responsible_party=responsible_party,
            issuing_authority=issuing_authority
        )

        self.compliance_items[item_id] = item
        return item

    def update_status(self, item_id: str, status: ComplianceStatus,
                     issue_date: datetime = None,
                     expiration_date: datetime = None,
                     reference_number: str = "",
                     document_url: str = "") -> ComplianceItem:
        """Update compliance item status."""
        if item_id not in self.compliance_items:
            raise ValueError(f"Compliance item {item_id} not found")

        item = self.compliance_items[item_id]
        item.status = status
        item.last_checked = datetime.now()

        if issue_date:
            item.issue_date = issue_date
        if expiration_date:
            item.expiration_date = expiration_date
        if reference_number:
            item.reference_number = reference_number
        if document_url:
            item.document_url = document_url

        return item

    def check_all_status(self) -> List[ComplianceAlert]:
        """Check status of all items and generate alerts."""
        new_alerts = []
        today = datetime.now()

        for item in self.compliance_items.values():
            # Skip non-applicable items
            if item.status == ComplianceStatus.NOT_APPLICABLE:
                continue

            # Check for expired
            if item.expiration_date and item.expiration_date < today:
                if item.status != ComplianceStatus.EXPIRED:
                    item.status = ComplianceStatus.EXPIRED
                    alert = self._create_alert(item, "expired",
                        f"EXPIRED: {item.name} expired on {item.expiration_date.strftime('%Y-%m-%d')}")
                    new_alerts.append(alert)

            # Check for expiring soon
            elif item.expiration_date:
                days_until = (item.expiration_date - today).days
                if days_until <= item.alert_days_before:
                    if item.status != ComplianceStatus.EXPIRING_SOON:
                        item.status = ComplianceStatus.EXPIRING_SOON
                        alert = self._create_alert(item, "expiring",
                            f"EXPIRING: {item.name} expires in {days_until} days")
                        new_alerts.append(alert)

            # Check pending items
            elif item.status == ComplianceStatus.PENDING:
                if item.priority == Priority.CRITICAL:
                    alert = self._create_alert(item, "action_required",
                        f"ACTION REQUIRED: {item.name} is pending - Critical priority")
                    new_alerts.append(alert)

        self.alerts.extend(new_alerts)
        return new_alerts

    def _create_alert(self, item: ComplianceItem, alert_type: str, message: str) -> ComplianceAlert:
        """Create compliance alert."""
        return ComplianceAlert(
            id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            compliance_item_id=item.id,
            alert_type=alert_type,
            message=message,
            due_date=item.expiration_date or datetime.now()
        )

    def get_compliance_summary(self) -> Dict:
        """Get compliance status summary."""
        total = len(self.compliance_items)
        by_status = {}
        by_type = {}
        by_priority = {}

        for item in self.compliance_items.values():
            # By status
            status = item.status.value
            by_status[status] = by_status.get(status, 0) + 1

            # By type
            comp_type = item.compliance_type.value
            by_type[comp_type] = by_type.get(comp_type, 0) + 1

            # By priority
            priority = item.priority.value
            by_priority[priority] = by_priority.get(priority, 0) + 1

        # Calculate compliance rate
        active = by_status.get("active", 0)
        compliance_rate = (active / total * 100) if total else 0

        critical_missing = len([i for i in self.compliance_items.values()
                               if i.priority == Priority.CRITICAL
                               and i.status in [ComplianceStatus.PENDING, ComplianceStatus.EXPIRED]])

        return {
            "total_items": total,
            "compliance_rate": compliance_rate,
            "by_status": by_status,
            "by_type": by_type,
            "by_priority": by_priority,
            "critical_missing": critical_missing,
            "active_alerts": len([a for a in self.alerts if not a.acknowledged])
        }

    def get_expiring_items(self, days: int = 30) -> List[ComplianceItem]:
        """Get items expiring within specified days."""
        cutoff = datetime.now() + timedelta(days=days)
        return [item for item in self.compliance_items.values()
                if item.expiration_date and item.expiration_date <= cutoff
                and item.status != ComplianceStatus.EXPIRED]

    def get_required_inspections(self, permit_category: str) -> List[str]:
        """Get required inspections for permit type."""
        return self.REQUIRED_INSPECTIONS.get(permit_category, [])

    def schedule_inspection(self, permit_id: str, inspection_name: str,
                           scheduled_date: datetime) -> ComplianceItem:
        """Schedule required inspection."""
        if permit_id not in self.compliance_items:
            raise ValueError(f"Permit {permit_id} not found")

        permit = self.compliance_items[permit_id]

        inspection = self.add_compliance_item(
            name=f"{permit.category} - {inspection_name} Inspection",
            compliance_type=ComplianceType.INSPECTION,
            category=permit.category,
            description=f"Required inspection for {permit.name}",
            priority=Priority.HIGH,
            expiration_date=scheduled_date
        )

        return inspection

    def generate_compliance_report(self) -> str:
        """Generate compliance status report."""
        summary = self.get_compliance_summary()

        lines = [
            f"# Compliance Status Report",
            f"",
            f"**Project:** {self.project_name}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"**Compliance Rate:** {summary['compliance_rate']:.1f}%",
            f"",
            f"## Summary",
            f"",
            f"| Status | Count |",
            f"|--------|-------|",
        ]

        for status, count in summary['by_status'].items():
            lines.append(f"| {status.title()} | {count} |")

        # Critical items
        critical_pending = [i for i in self.compliance_items.values()
                          if i.priority == Priority.CRITICAL
                          and i.status == ComplianceStatus.PENDING]
        if critical_pending:
            lines.extend([
                f"",
                f"## Critical Items Pending",
                f""
            ])
            for item in critical_pending:
                lines.append(f"- **{item.name}** - {item.responsible_party or 'Unassigned'}")

        # Expiring items
        expiring = self.get_expiring_items(30)
        if expiring:
            lines.extend([
                f"",
                f"## Items Expiring in 30 Days",
                f""
            ])
            for item in expiring:
                days = (item.expiration_date - datetime.now()).days
                lines.append(f"- **{item.name}** - Expires in {days} days ({item.expiration_date.strftime('%Y-%m-%d')})")

        # Active alerts
        active_alerts = [a for a in self.alerts if not a.acknowledged]
        if active_alerts:
            lines.extend([
                f"",
                f"## Active Alerts ({len(active_alerts)})",
                f""
            ])
            for alert in active_alerts[:10]:
                lines.append(f"- {alert.message}")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize tracker
tracker = ComplianceTracker("PRJ-001", "Office Tower")

# Initialize standard requirements
items = tracker.initialize_requirements("commercial")
print(f"Initialized {len(items)} compliance items")

# Update permit status
building_permit = [i for i in tracker.compliance_items.values()
                   if i.name == "Building Permit"][0]

tracker.update_status(
    building_permit.id,
    status=ComplianceStatus.ACTIVE,
    issue_date=datetime.now(),
    expiration_date=datetime.now() + timedelta(days=365),
    reference_number="BP-2024-12345"
)

# Check all status and generate alerts
alerts = tracker.check_all_status()
print(f"Generated {len(alerts)} alerts")

# Get summary
summary = tracker.get_compliance_summary()
print(f"Compliance Rate: {summary['compliance_rate']:.1f}%")
print(f"Critical Missing: {summary['critical_missing']}")

# Generate report
print(tracker.generate_compliance_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
