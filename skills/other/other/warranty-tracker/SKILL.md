---
name: "warranty-tracker"
description: "Track and manage construction warranties. Monitor expiration dates, claims, and manufacturer documentation."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "✅", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Warranty Tracker

## Business Case

### Problem Statement
Warranty management is often neglected:
- Missing warranty documentation
- Expired warranties untracked
- Difficult to file claims
- Scattered across multiple files

### Solution
Centralized warranty tracking system that monitors expiration dates, stores documentation, and manages claims.

### Business Value
- **Cost savings** - File claims before expiration
- **Organization** - Central warranty repository
- **Compliance** - Meet handover requirements
- **Proactive** - Automatic expiration alerts

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class WarrantyType(Enum):
    """Types of warranties."""
    MANUFACTURER = "manufacturer"
    CONTRACTOR = "contractor"
    INSTALLER = "installer"
    EXTENDED = "extended"
    PERFORMANCE = "performance"


class WarrantyStatus(Enum):
    """Warranty status."""
    ACTIVE = "active"
    EXPIRING_SOON = "expiring_soon"  # Within 90 days
    EXPIRED = "expired"
    CLAIMED = "claimed"
    VOID = "void"


class ClaimStatus(Enum):
    """Warranty claim status."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DENIED = "denied"
    RESOLVED = "resolved"


class BuildingSystem(Enum):
    """Building systems."""
    STRUCTURAL = "structural"
    ROOFING = "roofing"
    HVAC = "hvac"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    ELEVATORS = "elevators"
    FIRE_PROTECTION = "fire_protection"
    GLAZING = "glazing"
    FLOORING = "flooring"
    PAINTING = "painting"
    APPLIANCES = "appliances"
    EXTERIOR = "exterior"
    OTHER = "other"


@dataclass
class WarrantyDocument:
    """Warranty document reference."""
    document_id: str
    filename: str
    document_type: str  # certificate, manual, conditions
    upload_date: date
    file_path: str


@dataclass
class Warranty:
    """Warranty record."""
    warranty_id: str
    item_description: str
    system: BuildingSystem
    warranty_type: WarrantyType
    manufacturer: str
    contractor: str
    start_date: date
    end_date: date
    duration_years: int
    coverage_details: str
    exclusions: str
    contact_name: str
    contact_phone: str
    contact_email: str
    location: str
    documents: List[WarrantyDocument] = field(default_factory=list)
    notes: str = ""

    @property
    def status(self) -> WarrantyStatus:
        """Calculate current warranty status."""
        today = date.today()
        if today > self.end_date:
            return WarrantyStatus.EXPIRED
        elif (self.end_date - today).days <= 90:
            return WarrantyStatus.EXPIRING_SOON
        else:
            return WarrantyStatus.ACTIVE

    @property
    def days_remaining(self) -> int:
        """Days until warranty expires."""
        return (self.end_date - date.today()).days

    def to_dict(self) -> Dict[str, Any]:
        return {
            'warranty_id': self.warranty_id,
            'item': self.item_description,
            'system': self.system.value,
            'type': self.warranty_type.value,
            'manufacturer': self.manufacturer,
            'contractor': self.contractor,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'duration_years': self.duration_years,
            'status': self.status.value,
            'days_remaining': self.days_remaining,
            'contact': self.contact_email
        }


@dataclass
class WarrantyClaim:
    """Warranty claim record."""
    claim_id: str
    warranty_id: str
    issue_description: str
    issue_date: date
    reported_date: date
    status: ClaimStatus
    reported_by: str
    resolution: str = ""
    resolution_date: Optional[date] = None
    cost_covered: float = 0.0
    documents: List[str] = field(default_factory=list)
    notes: str = ""


class WarrantyTracker:
    """Track and manage construction warranties."""

    EXPIRING_THRESHOLD_DAYS = 90

    def __init__(self, project_name: str, substantial_completion_date: date):
        self.project_name = project_name
        self.completion_date = substantial_completion_date
        self.warranties: Dict[str, Warranty] = {}
        self.claims: Dict[str, WarrantyClaim] = {}
        self._warranty_counter = 0
        self._claim_counter = 0

    def add_warranty(self,
                    item_description: str,
                    system: BuildingSystem,
                    warranty_type: WarrantyType,
                    manufacturer: str,
                    contractor: str,
                    duration_years: int,
                    coverage_details: str,
                    contact_email: str,
                    start_date: date = None,
                    contact_name: str = "",
                    contact_phone: str = "",
                    exclusions: str = "",
                    location: str = "") -> Warranty:
        """Add new warranty record."""
        self._warranty_counter += 1
        warranty_id = f"WRT-{self._warranty_counter:04d}"

        start = start_date or self.completion_date
        end = start + timedelta(days=duration_years * 365)

        warranty = Warranty(
            warranty_id=warranty_id,
            item_description=item_description,
            system=system,
            warranty_type=warranty_type,
            manufacturer=manufacturer,
            contractor=contractor,
            start_date=start,
            end_date=end,
            duration_years=duration_years,
            coverage_details=coverage_details,
            exclusions=exclusions,
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email,
            location=location
        )

        self.warranties[warranty_id] = warranty
        return warranty

    def add_document(self, warranty_id: str,
                    filename: str,
                    document_type: str,
                    file_path: str) -> WarrantyDocument:
        """Add document to warranty."""
        if warranty_id not in self.warranties:
            raise ValueError(f"Warranty {warranty_id} not found")

        doc_id = f"{warranty_id}-DOC-{len(self.warranties[warranty_id].documents) + 1:02d}"
        document = WarrantyDocument(
            document_id=doc_id,
            filename=filename,
            document_type=document_type,
            upload_date=date.today(),
            file_path=file_path
        )

        self.warranties[warranty_id].documents.append(document)
        return document

    def file_claim(self,
                  warranty_id: str,
                  issue_description: str,
                  issue_date: date,
                  reported_by: str) -> WarrantyClaim:
        """File warranty claim."""
        if warranty_id not in self.warranties:
            raise ValueError(f"Warranty {warranty_id} not found")

        warranty = self.warranties[warranty_id]

        # Check if warranty is active
        if warranty.status == WarrantyStatus.EXPIRED:
            raise ValueError(f"Warranty {warranty_id} has expired")

        self._claim_counter += 1
        claim_id = f"CLM-{self._claim_counter:04d}"

        claim = WarrantyClaim(
            claim_id=claim_id,
            warranty_id=warranty_id,
            issue_description=issue_description,
            issue_date=issue_date,
            reported_date=date.today(),
            status=ClaimStatus.DRAFT,
            reported_by=reported_by
        )

        self.claims[claim_id] = claim
        return claim

    def update_claim_status(self, claim_id: str,
                           status: ClaimStatus,
                           resolution: str = "",
                           cost_covered: float = 0.0):
        """Update claim status."""
        if claim_id not in self.claims:
            raise ValueError(f"Claim {claim_id} not found")

        claim = self.claims[claim_id]
        claim.status = status

        if resolution:
            claim.resolution = resolution

        if cost_covered > 0:
            claim.cost_covered = cost_covered

        if status in [ClaimStatus.APPROVED, ClaimStatus.DENIED, ClaimStatus.RESOLVED]:
            claim.resolution_date = date.today()

    def get_expiring_warranties(self, days: int = None) -> List[Warranty]:
        """Get warranties expiring within specified days."""
        threshold = days or self.EXPIRING_THRESHOLD_DAYS
        cutoff = date.today() + timedelta(days=threshold)

        return [w for w in self.warranties.values()
                if w.status == WarrantyStatus.ACTIVE and w.end_date <= cutoff]

    def get_active_warranties(self) -> List[Warranty]:
        """Get all active warranties."""
        return [w for w in self.warranties.values()
                if w.status in [WarrantyStatus.ACTIVE, WarrantyStatus.EXPIRING_SOON]]

    def get_warranties_by_system(self, system: BuildingSystem) -> List[Warranty]:
        """Get warranties for specific building system."""
        return [w for w in self.warranties.values() if w.system == system]

    def get_summary(self) -> Dict[str, Any]:
        """Generate warranty summary."""
        by_status = {}
        by_system = {}

        for warranty in self.warranties.values():
            # By status
            status = warranty.status.value
            by_status[status] = by_status.get(status, 0) + 1

            # By system
            system = warranty.system.value
            by_system[system] = by_system.get(system, 0) + 1

        # Claims summary
        open_claims = sum(1 for c in self.claims.values()
                        if c.status not in [ClaimStatus.RESOLVED, ClaimStatus.DENIED])
        total_covered = sum(c.cost_covered for c in self.claims.values()
                          if c.status == ClaimStatus.RESOLVED)

        return {
            'total_warranties': len(self.warranties),
            'by_status': by_status,
            'by_system': by_system,
            'expiring_soon': len(self.get_expiring_warranties()),
            'total_claims': len(self.claims),
            'open_claims': open_claims,
            'total_cost_recovered': total_covered,
            'project': self.project_name,
            'completion_date': self.completion_date.isoformat()
        }

    def generate_expiration_report(self, months_ahead: int = 12) -> pd.DataFrame:
        """Generate warranty expiration report."""
        cutoff = date.today() + timedelta(days=months_ahead * 30)
        upcoming = [w for w in self.warranties.values() if w.end_date <= cutoff]

        data = []
        for w in sorted(upcoming, key=lambda x: x.end_date):
            data.append({
                'Warranty ID': w.warranty_id,
                'Item': w.item_description,
                'System': w.system.value,
                'Manufacturer': w.manufacturer,
                'End Date': w.end_date,
                'Days Remaining': w.days_remaining,
                'Status': w.status.value,
                'Contact': w.contact_email
            })

        return pd.DataFrame(data)

    def export_to_excel(self, output_path: str):
        """Export all warranty data to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Warranties
            warranties_df = pd.DataFrame([w.to_dict() for w in self.warranties.values()])
            if not warranties_df.empty:
                warranties_df.to_excel(writer, sheet_name='Warranties', index=False)

            # Claims
            claims_data = []
            for claim in self.claims.values():
                warranty = self.warranties.get(claim.warranty_id)
                claims_data.append({
                    'Claim ID': claim.claim_id,
                    'Warranty ID': claim.warranty_id,
                    'Item': warranty.item_description if warranty else '',
                    'Issue': claim.issue_description,
                    'Issue Date': claim.issue_date,
                    'Status': claim.status.value,
                    'Resolution': claim.resolution,
                    'Cost Covered': claim.cost_covered
                })

            if claims_data:
                pd.DataFrame(claims_data).to_excel(writer, sheet_name='Claims', index=False)

            # Expiring soon
            expiring = self.generate_expiration_report(6)
            if not expiring.empty:
                expiring.to_excel(writer, sheet_name='Expiring Soon', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date

# Initialize tracker
tracker = WarrantyTracker(
    project_name="Office Tower",
    substantial_completion_date=date(2024, 6, 1)
)

# Add warranties
tracker.add_warranty(
    item_description="HVAC System - Rooftop Units",
    system=BuildingSystem.HVAC,
    warranty_type=WarrantyType.MANUFACTURER,
    manufacturer="Carrier",
    contractor="ABC Mechanical",
    duration_years=5,
    coverage_details="Parts and labor for manufacturing defects",
    contact_email="warranty@carrier.com"
)

# Check expiring warranties
expiring = tracker.get_expiring_warranties(90)
print(f"Warranties expiring in 90 days: {len(expiring)}")
```

## Common Use Cases

### 1. Monthly Review
```python
# Get expiration report
report = tracker.generate_expiration_report(months_ahead=3)
print(report[['Item', 'End Date', 'Days Remaining']])
```

### 2. File Claim
```python
claim = tracker.file_claim(
    warranty_id="WRT-0001",
    issue_description="RTU-1 compressor failure",
    issue_date=date.today(),
    reported_by="Building Manager"
)
```

### 3. Export for Handover
```python
tracker.export_to_excel("warranty_register.xlsx")
```

## Resources
- **DDC Book**: Chapter 5 - Project Closeout
- **Reference**: AIA Document G714
