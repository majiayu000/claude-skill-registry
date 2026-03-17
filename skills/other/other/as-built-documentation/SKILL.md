---
slug: "as-built-documentation"
display_name: "As Built Documentation"
description: "Automate as-built documentation and digital handover for construction. Compile project records, generate O&M manuals, create asset databases, and ensure complete project closeout."
---

# As-Built Documentation

## Overview

This skill implements automated as-built documentation and digital handover for construction projects. Compile accurate records, generate operation manuals, and ensure complete documentation for facility management.

**Capabilities:**
- As-built drawing management
- O&M manual generation
- Asset data compilation
- Warranty tracking
- Document organization
- BIM-to-FM handover

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Dict, Optional
from enum import Enum

class DocumentType(Enum):
    DRAWING = "drawing"
    SPECIFICATION = "specification"
    SUBMITTAL = "submittal"
    WARRANTY = "warranty"
    CERTIFICATE = "certificate"
    MANUAL = "manual"
    TEST_REPORT = "test_report"
    COMMISSIONING = "commissioning"
    PHOTO = "photo"

class DocumentStatus(Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    AS_BUILT = "as_built"
    FINAL = "final"

@dataclass
class HandoverDocument:
    doc_id: str
    doc_type: DocumentType
    title: str
    file_path: str
    version: str
    status: DocumentStatus
    system: str  # Building system (HVAC, Electrical, etc.)
    uploaded_date: date
    approved_by: str = ""

@dataclass
class AssetRecord:
    asset_id: str
    asset_name: str
    asset_type: str
    manufacturer: str
    model: str
    serial_number: str
    location: str
    install_date: date
    warranty_end: date
    documents: List[str] = field(default_factory=list)

def check_handover_completeness(documents: List[HandoverDocument],
                                required_types: List[DocumentType]) -> Dict:
    """Check if all required documents are present"""
    present_types = {doc.doc_type for doc in documents if doc.status == DocumentStatus.FINAL}
    missing = set(required_types) - present_types

    return {
        'complete': len(missing) == 0,
        'total_required': len(required_types),
        'total_present': len(present_types),
        'missing_types': [t.value for t in missing]
    }

# Example
documents = [
    HandoverDocument("DOC-001", DocumentType.DRAWING, "Floor Plans As-Built",
                    "/docs/floorplans.pdf", "3.0", DocumentStatus.FINAL, "Architecture", date.today()),
    HandoverDocument("DOC-002", DocumentType.MANUAL, "HVAC O&M Manual",
                    "/docs/hvac_om.pdf", "1.0", DocumentStatus.FINAL, "HVAC", date.today()),
]

required = [DocumentType.DRAWING, DocumentType.MANUAL, DocumentType.WARRANTY]
status = check_handover_completeness(documents, required)
print(f"Complete: {status['complete']}, Missing: {status['missing_types']}")
```

## Comprehensive Handover System

### Document Management

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import uuid
import os

class BuildingSystem(Enum):
    ARCHITECTURAL = "architectural"
    STRUCTURAL = "structural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    CONTROLS = "controls"
    ELEVATOR = "elevator"
    CIVIL = "civil"
    LANDSCAPE = "landscape"

@dataclass
class DocumentRequirement:
    requirement_id: str
    doc_type: DocumentType
    system: BuildingSystem
    description: str
    is_mandatory: bool = True
    quantity: int = 1  # How many documents of this type needed
    format_requirements: str = "PDF"

@dataclass
class ProjectDocument:
    doc_id: str
    requirement_id: Optional[str]
    doc_type: DocumentType
    system: BuildingSystem
    title: str
    description: str
    file_path: str
    file_size_mb: float
    format: str
    version: str
    revision_date: date
    author: str
    reviewer: str
    status: DocumentStatus
    metadata: Dict = field(default_factory=dict)
    related_assets: List[str] = field(default_factory=list)
    supersedes: Optional[str] = None  # Previous version doc_id

class DocumentManager:
    """Manage project handover documents"""

    STANDARD_REQUIREMENTS = {
        BuildingSystem.MECHANICAL: [
            DocumentRequirement("REQ-M01", DocumentType.DRAWING, BuildingSystem.MECHANICAL,
                              "HVAC As-Built Drawings"),
            DocumentRequirement("REQ-M02", DocumentType.MANUAL, BuildingSystem.MECHANICAL,
                              "HVAC Operation & Maintenance Manual"),
            DocumentRequirement("REQ-M03", DocumentType.WARRANTY, BuildingSystem.MECHANICAL,
                              "HVAC Equipment Warranties"),
            DocumentRequirement("REQ-M04", DocumentType.TEST_REPORT, BuildingSystem.MECHANICAL,
                              "TAB Report - Testing, Adjusting, Balancing"),
            DocumentRequirement("REQ-M05", DocumentType.COMMISSIONING, BuildingSystem.MECHANICAL,
                              "Commissioning Report"),
        ],
        BuildingSystem.ELECTRICAL: [
            DocumentRequirement("REQ-E01", DocumentType.DRAWING, BuildingSystem.ELECTRICAL,
                              "Electrical As-Built Drawings"),
            DocumentRequirement("REQ-E02", DocumentType.MANUAL, BuildingSystem.ELECTRICAL,
                              "Electrical O&M Manual"),
            DocumentRequirement("REQ-E03", DocumentType.WARRANTY, BuildingSystem.ELECTRICAL,
                              "Electrical Equipment Warranties"),
            DocumentRequirement("REQ-E04", DocumentType.TEST_REPORT, BuildingSystem.ELECTRICAL,
                              "Electrical Test Reports"),
            DocumentRequirement("REQ-E05", DocumentType.CERTIFICATE, BuildingSystem.ELECTRICAL,
                              "Electrical Inspection Certificate"),
        ],
        BuildingSystem.PLUMBING: [
            DocumentRequirement("REQ-P01", DocumentType.DRAWING, BuildingSystem.PLUMBING,
                              "Plumbing As-Built Drawings"),
            DocumentRequirement("REQ-P02", DocumentType.MANUAL, BuildingSystem.PLUMBING,
                              "Plumbing O&M Manual"),
            DocumentRequirement("REQ-P03", DocumentType.TEST_REPORT, BuildingSystem.PLUMBING,
                              "Pressure Test Reports"),
        ],
        BuildingSystem.FIRE_PROTECTION: [
            DocumentRequirement("REQ-F01", DocumentType.DRAWING, BuildingSystem.FIRE_PROTECTION,
                              "Fire Protection As-Built Drawings"),
            DocumentRequirement("REQ-F02", DocumentType.MANUAL, BuildingSystem.FIRE_PROTECTION,
                              "Fire Systems O&M Manual"),
            DocumentRequirement("REQ-F03", DocumentType.CERTIFICATE, BuildingSystem.FIRE_PROTECTION,
                              "Fire Marshal Approval"),
            DocumentRequirement("REQ-F04", DocumentType.TEST_REPORT, BuildingSystem.FIRE_PROTECTION,
                              "Fire Alarm Acceptance Test"),
        ],
        BuildingSystem.ARCHITECTURAL: [
            DocumentRequirement("REQ-A01", DocumentType.DRAWING, BuildingSystem.ARCHITECTURAL,
                              "Architectural As-Built Drawings"),
            DocumentRequirement("REQ-A02", DocumentType.SPECIFICATION, BuildingSystem.ARCHITECTURAL,
                              "Finish Schedule"),
            DocumentRequirement("REQ-A03", DocumentType.WARRANTY, BuildingSystem.ARCHITECTURAL,
                              "Roofing Warranty"),
        ]
    }

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name
        self.requirements: Dict[str, DocumentRequirement] = {}
        self.documents: Dict[str, ProjectDocument] = {}
        self._load_standard_requirements()

    def _load_standard_requirements(self):
        """Load standard document requirements"""
        for system, reqs in self.STANDARD_REQUIREMENTS.items():
            for req in reqs:
                self.requirements[req.requirement_id] = req

    def add_requirement(self, requirement: DocumentRequirement):
        """Add custom requirement"""
        self.requirements[requirement.requirement_id] = requirement

    def upload_document(self, doc_type: DocumentType, system: BuildingSystem,
                       title: str, file_path: str, author: str,
                       requirement_id: str = None,
                       related_assets: List[str] = None) -> ProjectDocument:
        """Upload new document"""
        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"

        # Get file info
        file_size = os.path.getsize(file_path) / (1024 * 1024) if os.path.exists(file_path) else 0
        file_format = os.path.splitext(file_path)[1].upper().replace('.', '')

        doc = ProjectDocument(
            doc_id=doc_id,
            requirement_id=requirement_id,
            doc_type=doc_type,
            system=system,
            title=title,
            description="",
            file_path=file_path,
            file_size_mb=file_size,
            format=file_format,
            version="1.0",
            revision_date=date.today(),
            author=author,
            reviewer="",
            status=DocumentStatus.DRAFT,
            related_assets=related_assets or []
        )

        self.documents[doc_id] = doc
        return doc

    def approve_document(self, doc_id: str, reviewer: str) -> bool:
        """Approve document"""
        doc = self.documents.get(doc_id)
        if doc:
            doc.status = DocumentStatus.APPROVED
            doc.reviewer = reviewer
            return True
        return False

    def finalize_document(self, doc_id: str) -> bool:
        """Finalize document for handover"""
        doc = self.documents.get(doc_id)
        if doc and doc.status == DocumentStatus.APPROVED:
            doc.status = DocumentStatus.FINAL
            return True
        return False

    def get_status_summary(self) -> Dict:
        """Get document status summary"""
        summary = {
            'total_requirements': len(self.requirements),
            'total_documents': len(self.documents),
            'by_status': {},
            'by_system': {},
            'completion': {}
        }

        # Count by status
        for doc in self.documents.values():
            status = doc.status.value
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1

            system = doc.system.value
            if system not in summary['by_system']:
                summary['by_system'][system] = {'uploaded': 0, 'final': 0}
            summary['by_system'][system]['uploaded'] += 1
            if doc.status == DocumentStatus.FINAL:
                summary['by_system'][system]['final'] += 1

        # Check completion against requirements
        for req_id, req in self.requirements.items():
            matching_docs = [
                d for d in self.documents.values()
                if d.requirement_id == req_id and d.status == DocumentStatus.FINAL
            ]

            summary['completion'][req_id] = {
                'description': req.description,
                'system': req.system.value,
                'required': req.quantity,
                'submitted': len(matching_docs),
                'complete': len(matching_docs) >= req.quantity
            }

        return summary

    def get_missing_documents(self) -> List[DocumentRequirement]:
        """Get list of missing required documents"""
        missing = []

        for req_id, req in self.requirements.items():
            if not req.is_mandatory:
                continue

            matching_docs = [
                d for d in self.documents.values()
                if d.requirement_id == req_id and d.status == DocumentStatus.FINAL
            ]

            if len(matching_docs) < req.quantity:
                missing.append(req)

        return missing
```

### Asset Registry

```python
from datetime import date, timedelta
from typing import List, Dict, Optional

@dataclass
class MaintenanceSchedule:
    schedule_id: str
    task_description: str
    frequency: str  # daily, weekly, monthly, quarterly, annual
    next_due: date
    responsible_party: str
    estimated_duration_hours: float

@dataclass
class AssetDetails:
    asset_id: str
    asset_tag: str
    asset_name: str
    asset_type: str
    category: str  # equipment, fixture, system

    # Identification
    manufacturer: str
    model_number: str
    serial_number: str
    part_number: str = ""

    # Location
    building: str = ""
    floor: str = ""
    room: str = ""
    coordinates: Tuple[float, float, float] = (0, 0, 0)

    # Installation
    install_date: date = None
    installed_by: str = ""
    cost: float = 0

    # Warranty
    warranty_start: date = None
    warranty_end: date = None
    warranty_provider: str = ""
    warranty_terms: str = ""

    # Specifications
    specifications: Dict = field(default_factory=dict)

    # Documents
    manuals: List[str] = field(default_factory=list)
    drawings: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)

    # Maintenance
    maintenance_schedules: List[MaintenanceSchedule] = field(default_factory=list)
    service_contacts: List[Dict] = field(default_factory=list)

    # BIM reference
    ifc_guid: str = ""
    revit_element_id: str = ""

class AssetRegistry:
    """Manage building assets for handover"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.assets: Dict[str, AssetDetails] = {}

    def register_asset(self, asset: AssetDetails):
        """Register new asset"""
        self.assets[asset.asset_id] = asset

    def import_from_bim(self, bim_data: List[Dict]):
        """Import assets from BIM model"""
        for item in bim_data:
            asset = AssetDetails(
                asset_id=f"AST-{uuid.uuid4().hex[:8].upper()}",
                asset_tag=item.get('tag', ''),
                asset_name=item.get('name', ''),
                asset_type=item.get('type', ''),
                category=item.get('category', 'equipment'),
                manufacturer=item.get('manufacturer', ''),
                model_number=item.get('model', ''),
                serial_number=item.get('serial', ''),
                building=item.get('building', ''),
                floor=item.get('floor', ''),
                room=item.get('room', ''),
                ifc_guid=item.get('ifc_guid', ''),
                revit_element_id=item.get('revit_id', '')
            )

            # Add specifications
            for key, value in item.get('parameters', {}).items():
                asset.specifications[key] = value

            self.assets[asset.asset_id] = asset

    def add_warranty(self, asset_id: str, start_date: date,
                    duration_years: int, provider: str, terms: str = ""):
        """Add warranty information"""
        asset = self.assets.get(asset_id)
        if asset:
            asset.warranty_start = start_date
            asset.warranty_end = start_date + timedelta(days=365 * duration_years)
            asset.warranty_provider = provider
            asset.warranty_terms = terms

    def add_maintenance_schedule(self, asset_id: str,
                                 schedule: MaintenanceSchedule):
        """Add maintenance schedule"""
        asset = self.assets.get(asset_id)
        if asset:
            asset.maintenance_schedules.append(schedule)

    def get_warranty_report(self) -> Dict:
        """Get warranty status report"""
        today = date.today()

        report = {
            'total_assets': len(self.assets),
            'with_warranty': 0,
            'active_warranties': 0,
            'expiring_soon': [],  # Within 90 days
            'expired': []
        }

        for asset in self.assets.values():
            if asset.warranty_end:
                report['with_warranty'] += 1

                if asset.warranty_end >= today:
                    report['active_warranties'] += 1

                    days_remaining = (asset.warranty_end - today).days
                    if days_remaining <= 90:
                        report['expiring_soon'].append({
                            'asset_id': asset.asset_id,
                            'asset_name': asset.asset_name,
                            'warranty_end': asset.warranty_end.isoformat(),
                            'days_remaining': days_remaining
                        })
                else:
                    report['expired'].append({
                        'asset_id': asset.asset_id,
                        'asset_name': asset.asset_name,
                        'warranty_end': asset.warranty_end.isoformat()
                    })

        return report

    def export_to_cmms(self) -> List[Dict]:
        """Export assets for CMMS import"""
        export_data = []

        for asset in self.assets.values():
            export_data.append({
                'asset_id': asset.asset_id,
                'asset_tag': asset.asset_tag,
                'name': asset.asset_name,
                'type': asset.asset_type,
                'category': asset.category,
                'manufacturer': asset.manufacturer,
                'model': asset.model_number,
                'serial': asset.serial_number,
                'location': f"{asset.building}/{asset.floor}/{asset.room}",
                'install_date': asset.install_date.isoformat() if asset.install_date else '',
                'warranty_end': asset.warranty_end.isoformat() if asset.warranty_end else '',
                'specifications': asset.specifications
            })

        return export_data
```

### O&M Manual Generator

```python
class OMManualGenerator:
    """Generate O&M manuals from project data"""

    def __init__(self, doc_manager: DocumentManager, asset_registry: AssetRegistry):
        self.docs = doc_manager
        self.assets = asset_registry

    def generate_system_manual(self, system: BuildingSystem,
                              output_path: str) -> Dict:
        """Generate O&M manual for building system"""
        # Collect system documents
        system_docs = [
            d for d in self.docs.documents.values()
            if d.system == system and d.status == DocumentStatus.FINAL
        ]

        # Collect system assets
        system_assets = [
            a for a in self.assets.assets.values()
            if a.asset_type.lower() in system.value.lower() or
               system.value.lower() in a.category.lower()
        ]

        manual_content = {
            'system': system.value,
            'generated_date': date.today().isoformat(),
            'sections': []
        }

        # Section 1: System Overview
        manual_content['sections'].append({
            'title': 'System Overview',
            'content': f"Overview of {system.value} system",
            'subsections': []
        })

        # Section 2: Equipment List
        equipment_list = []
        for asset in system_assets:
            equipment_list.append({
                'tag': asset.asset_tag,
                'name': asset.asset_name,
                'manufacturer': asset.manufacturer,
                'model': asset.model_number,
                'location': f"{asset.building}/{asset.floor}/{asset.room}"
            })

        manual_content['sections'].append({
            'title': 'Equipment Schedule',
            'equipment': equipment_list
        })

        # Section 3: Operation Procedures
        manual_content['sections'].append({
            'title': 'Operation Procedures',
            'content': 'Standard operating procedures',
            'reference_docs': [d.doc_id for d in system_docs if d.doc_type == DocumentType.MANUAL]
        })

        # Section 4: Maintenance Requirements
        maintenance_tasks = []
        for asset in system_assets:
            for schedule in asset.maintenance_schedules:
                maintenance_tasks.append({
                    'asset': asset.asset_name,
                    'task': schedule.task_description,
                    'frequency': schedule.frequency,
                    'duration': schedule.estimated_duration_hours
                })

        manual_content['sections'].append({
            'title': 'Preventive Maintenance',
            'tasks': maintenance_tasks
        })

        # Section 5: Warranty Information
        warranties = []
        for asset in system_assets:
            if asset.warranty_end:
                warranties.append({
                    'asset': asset.asset_name,
                    'provider': asset.warranty_provider,
                    'expires': asset.warranty_end.isoformat(),
                    'terms': asset.warranty_terms
                })

        manual_content['sections'].append({
            'title': 'Warranty Information',
            'warranties': warranties
        })

        # Section 6: Service Contacts
        contacts = []
        for asset in system_assets:
            contacts.extend(asset.service_contacts)

        manual_content['sections'].append({
            'title': 'Service Contacts',
            'contacts': list({c['name']: c for c in contacts}.values())
        })

        # Section 7: Reference Documents
        manual_content['sections'].append({
            'title': 'Reference Documents',
            'documents': [
                {'id': d.doc_id, 'title': d.title, 'type': d.doc_type.value}
                for d in system_docs
            ]
        })

        return manual_content

    def generate_building_manual(self, output_path: str) -> Dict:
        """Generate complete building O&M manual"""
        building_manual = {
            'project': self.docs.project_name,
            'generated': date.today().isoformat(),
            'systems': {}
        }

        for system in BuildingSystem:
            building_manual['systems'][system.value] = self.generate_system_manual(
                system, output_path
            )

        return building_manual
```

### Handover Checklist

```python
def generate_handover_checklist(doc_manager: DocumentManager,
                               asset_registry: AssetRegistry) -> Dict:
    """Generate comprehensive handover checklist"""
    checklist = {
        'generated': date.today().isoformat(),
        'project': doc_manager.project_name,
        'overall_status': 'incomplete',
        'categories': []
    }

    # Documents category
    doc_status = doc_manager.get_status_summary()
    missing_docs = doc_manager.get_missing_documents()

    checklist['categories'].append({
        'name': 'Documents',
        'complete': len(missing_docs) == 0,
        'items': [
            {
                'item': req.description,
                'system': req.system.value,
                'status': 'complete' if req.requirement_id not in [m.requirement_id for m in missing_docs] else 'missing'
            }
            for req in doc_manager.requirements.values()
        ]
    })

    # Assets category
    warranty_report = asset_registry.get_warranty_report()

    checklist['categories'].append({
        'name': 'Asset Registration',
        'complete': warranty_report['total_assets'] > 0,
        'items': [
            {'item': 'All major equipment registered', 'status': 'complete' if warranty_report['total_assets'] > 0 else 'incomplete'},
            {'item': 'Warranty information entered', 'status': 'complete' if warranty_report['with_warranty'] > 0 else 'incomplete'},
            {'item': 'Maintenance schedules defined', 'status': 'complete' if any(a.maintenance_schedules for a in asset_registry.assets.values()) else 'incomplete'}
        ]
    })

    # Training category
    checklist['categories'].append({
        'name': 'Training',
        'complete': False,
        'items': [
            {'item': 'Operations staff training completed', 'status': 'pending'},
            {'item': 'Maintenance staff training completed', 'status': 'pending'},
            {'item': 'Safety systems training completed', 'status': 'pending'}
        ]
    })

    # Determine overall status
    all_complete = all(cat['complete'] for cat in checklist['categories'])
    checklist['overall_status'] = 'complete' if all_complete else 'incomplete'

    return checklist
```

## Quick Reference

| Document Type | Typical Source | When Required |
|---------------|---------------|---------------|
| As-Built Drawings | Contractor | Substantial completion |
| O&M Manuals | Manufacturer/Contractor | Before training |
| Warranties | Manufacturers | At installation |
| Test Reports | Testing agency | After testing |
| Certificates | Authorities | Final inspection |
| Training Records | Contractor | Before handover |

## Resources

- **COBie Standard**: Construction Operations Building Information Exchange
- **ASHRAE Guideline 0**: Commissioning process
- **IFMA**: Facility Management resources
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `bim-validation-pipeline` for BIM handover
- See `document-classification-nlp` for document processing
- See `digital-twin-sync` for FM integration
