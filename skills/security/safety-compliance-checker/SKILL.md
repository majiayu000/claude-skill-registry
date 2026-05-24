---
name: safety-compliance-checker
description: "Automated safety compliance verification for construction sites. Check PPE usage, zone access, working at heights regulations, and generate compliance reports using rule-based and ML approaches."
---

# Safety Compliance Checker

## Overview

This skill implements automated safety compliance checking for construction projects. Verify regulatory requirements, track safety metrics, and identify potential violations before they become incidents.

**Compliance Areas:**
- Personal Protective Equipment (PPE)
- Working at heights regulations
- Confined space entry
- Hot work permits
- Excavation safety
- Electrical safety
- Fire prevention

## Quick Start

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, date

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    PENDING_REVIEW = "pending_review"

@dataclass
class ComplianceCheck:
    rule_id: str
    rule_name: str
    status: ComplianceStatus
    findings: List[str]
    evidence: Optional[str]
    checked_at: datetime
    checked_by: str

# Quick compliance check
def check_ppe_compliance(workers: List[Dict]) -> List[ComplianceCheck]:
    """Check PPE compliance for workers"""
    checks = []

    for worker in workers:
        findings = []
        required_ppe = worker.get('required_ppe', ['helmet', 'vest', 'boots'])
        actual_ppe = worker.get('actual_ppe', [])

        missing = set(required_ppe) - set(actual_ppe)
        if missing:
            findings.append(f"Missing PPE: {', '.join(missing)}")

        status = ComplianceStatus.COMPLIANT if not missing else ComplianceStatus.NON_COMPLIANT

        checks.append(ComplianceCheck(
            rule_id="PPE-001",
            rule_name="Personal Protective Equipment",
            status=status,
            findings=findings,
            evidence=f"Worker ID: {worker.get('id')}",
            checked_at=datetime.now(),
            checked_by="automated_system"
        ))

    return checks

# Example usage
workers = [
    {'id': 'W001', 'required_ppe': ['helmet', 'vest', 'boots'], 'actual_ppe': ['helmet', 'vest']},
    {'id': 'W002', 'required_ppe': ['helmet', 'vest', 'boots'], 'actual_ppe': ['helmet', 'vest', 'boots']}
]

results = check_ppe_compliance(workers)
for r in results:
    print(f"{r.evidence}: {r.status.value} - {r.findings}")
```

## Comprehensive Safety Compliance System

### Safety Rules Engine

```python
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Any
from enum import Enum
from datetime import datetime, date, timedelta
import json

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RuleCategory(Enum):
    PPE = "Personal Protective Equipment"
    FALL_PROTECTION = "Fall Protection"
    ELECTRICAL = "Electrical Safety"
    EXCAVATION = "Excavation Safety"
    CONFINED_SPACE = "Confined Space"
    HOT_WORK = "Hot Work"
    FIRE = "Fire Prevention"
    HAZMAT = "Hazardous Materials"
    CRANE = "Crane & Lifting"
    SCAFFOLDING = "Scaffolding"

@dataclass
class SafetyRule:
    rule_id: str
    name: str
    description: str
    category: RuleCategory
    risk_level: RiskLevel
    regulation_ref: str  # OSHA, local codes
    check_function: Optional[Callable] = None
    parameters: Dict = field(default_factory=dict)

@dataclass
class Violation:
    rule: SafetyRule
    location: str
    description: str
    detected_at: datetime
    severity: RiskLevel
    corrective_action: str
    deadline: date
    status: str = "open"
    assigned_to: Optional[str] = None

class SafetyComplianceEngine:
    """Rule-based safety compliance checking engine"""

    def __init__(self):
        self.rules: Dict[str, SafetyRule] = {}
        self.violations: List[Violation] = []
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default safety rules"""
        default_rules = [
            SafetyRule(
                rule_id="OSHA-1926.100",
                name="Head Protection",
                description="Employees working in areas where there is a possible danger of head injury shall wear protective helmets",
                category=RuleCategory.PPE,
                risk_level=RiskLevel.HIGH,
                regulation_ref="OSHA 29 CFR 1926.100",
                parameters={"required_ppe": ["helmet"]}
            ),
            SafetyRule(
                rule_id="OSHA-1926.501",
                name="Fall Protection - General",
                description="Each employee on walking/working surfaces with unprotected sides 6 feet or more above lower level shall be protected",
                category=RuleCategory.FALL_PROTECTION,
                risk_level=RiskLevel.CRITICAL,
                regulation_ref="OSHA 29 CFR 1926.501",
                parameters={"height_threshold_ft": 6}
            ),
            SafetyRule(
                rule_id="OSHA-1926.651",
                name="Excavation General Requirements",
                description="Daily inspections of excavations, adjacent areas, and protective systems",
                category=RuleCategory.EXCAVATION,
                risk_level=RiskLevel.HIGH,
                regulation_ref="OSHA 29 CFR 1926.651",
                parameters={"inspection_frequency": "daily"}
            ),
            SafetyRule(
                rule_id="OSHA-1926.1200",
                name="Confined Space Entry",
                description="Permit-required confined space program for construction",
                category=RuleCategory.CONFINED_SPACE,
                risk_level=RiskLevel.CRITICAL,
                regulation_ref="OSHA 29 CFR 1926.1200",
                parameters={"permit_required": True}
            ),
            SafetyRule(
                rule_id="OSHA-1926.352",
                name="Fire Prevention - Welding",
                description="Fire watch and extinguisher required for hot work",
                category=RuleCategory.HOT_WORK,
                risk_level=RiskLevel.HIGH,
                regulation_ref="OSHA 29 CFR 1926.352",
                parameters={"fire_watch_duration_min": 30}
            ),
            SafetyRule(
                rule_id="OSHA-1926.451",
                name="Scaffolding General Requirements",
                description="Scaffold platforms shall be fully planked between front uprights and guardrail supports",
                category=RuleCategory.SCAFFOLDING,
                risk_level=RiskLevel.HIGH,
                regulation_ref="OSHA 29 CFR 1926.451",
                parameters={"max_height_without_tie": 26}
            ),
            SafetyRule(
                rule_id="OSHA-1926.405",
                name="Electrical Wiring Methods",
                description="All electrical equipment and circuits shall be grounded",
                category=RuleCategory.ELECTRICAL,
                risk_level=RiskLevel.CRITICAL,
                regulation_ref="OSHA 29 CFR 1926.405",
                parameters={"gfci_required": True}
            )
        ]

        for rule in default_rules:
            self.rules[rule.rule_id] = rule

    def add_rule(self, rule: SafetyRule):
        """Add custom safety rule"""
        self.rules[rule.rule_id] = rule

    def check_work_activity(self, activity: Dict) -> List[ComplianceCheck]:
        """Check compliance for a work activity"""
        checks = []

        activity_type = activity.get('type', '')
        location = activity.get('location', '')
        height = activity.get('height_ft', 0)
        workers = activity.get('workers', [])
        permits = activity.get('permits', [])
        equipment = activity.get('equipment', [])

        # Fall protection check
        if height >= 6:
            fall_rule = self.rules.get("OSHA-1926.501")
            if fall_rule:
                has_protection = any(
                    'harness' in w.get('ppe', []) or 'guardrail' in equipment
                    for w in workers
                )
                checks.append(ComplianceCheck(
                    rule_id=fall_rule.rule_id,
                    rule_name=fall_rule.name,
                    status=ComplianceStatus.COMPLIANT if has_protection else ComplianceStatus.NON_COMPLIANT,
                    findings=[] if has_protection else [f"Working at {height}ft without fall protection"],
                    evidence=f"Activity: {activity_type} at {location}",
                    checked_at=datetime.now(),
                    checked_by="automated_system"
                ))

        # PPE check for all workers
        for worker in workers:
            ppe_rule = self.rules.get("OSHA-1926.100")
            if ppe_rule:
                has_helmet = 'helmet' in worker.get('ppe', [])
                checks.append(ComplianceCheck(
                    rule_id=ppe_rule.rule_id,
                    rule_name=ppe_rule.name,
                    status=ComplianceStatus.COMPLIANT if has_helmet else ComplianceStatus.NON_COMPLIANT,
                    findings=[] if has_helmet else ["Missing hard hat"],
                    evidence=f"Worker: {worker.get('id')}",
                    checked_at=datetime.now(),
                    checked_by="automated_system"
                ))

        # Hot work permit check
        if activity_type in ['welding', 'cutting', 'brazing']:
            hot_work_rule = self.rules.get("OSHA-1926.352")
            if hot_work_rule:
                has_permit = 'hot_work' in permits
                has_fire_watch = activity.get('fire_watch', False)
                has_extinguisher = 'fire_extinguisher' in equipment

                findings = []
                if not has_permit:
                    findings.append("Missing hot work permit")
                if not has_fire_watch:
                    findings.append("No fire watch assigned")
                if not has_extinguisher:
                    findings.append("No fire extinguisher on site")

                checks.append(ComplianceCheck(
                    rule_id=hot_work_rule.rule_id,
                    rule_name=hot_work_rule.name,
                    status=ComplianceStatus.COMPLIANT if not findings else ComplianceStatus.NON_COMPLIANT,
                    findings=findings,
                    evidence=f"Activity: {activity_type} at {location}",
                    checked_at=datetime.now(),
                    checked_by="automated_system"
                ))

        # Confined space check
        if activity.get('confined_space', False):
            cs_rule = self.rules.get("OSHA-1926.1200")
            if cs_rule:
                has_permit = 'confined_space' in permits
                has_attendant = activity.get('attendant', False)
                atmospheric_tested = activity.get('atmospheric_test', False)

                findings = []
                if not has_permit:
                    findings.append("Missing confined space entry permit")
                if not has_attendant:
                    findings.append("No attendant stationed at entry")
                if not atmospheric_tested:
                    findings.append("Atmospheric testing not performed")

                checks.append(ComplianceCheck(
                    rule_id=cs_rule.rule_id,
                    rule_name=cs_rule.name,
                    status=ComplianceStatus.COMPLIANT if not findings else ComplianceStatus.NON_COMPLIANT,
                    findings=findings,
                    evidence=f"Confined space: {location}",
                    checked_at=datetime.now(),
                    checked_by="automated_system"
                ))

        return checks

    def create_violation(self, check: ComplianceCheck, location: str) -> Violation:
        """Create violation record from failed check"""
        rule = self.rules.get(check.rule_id)

        # Determine deadline based on severity
        if rule.risk_level == RiskLevel.CRITICAL:
            deadline = date.today()  # Immediate
        elif rule.risk_level == RiskLevel.HIGH:
            deadline = date.today() + timedelta(days=1)
        elif rule.risk_level == RiskLevel.MEDIUM:
            deadline = date.today() + timedelta(days=3)
        else:
            deadline = date.today() + timedelta(days=7)

        violation = Violation(
            rule=rule,
            location=location,
            description="; ".join(check.findings),
            detected_at=check.checked_at,
            severity=rule.risk_level,
            corrective_action=self._get_corrective_action(rule, check.findings),
            deadline=deadline
        )

        self.violations.append(violation)
        return violation

    def _get_corrective_action(self, rule: SafetyRule, findings: List[str]) -> str:
        """Generate corrective action based on rule and findings"""
        actions = {
            RuleCategory.PPE: "Provide required PPE to workers and ensure proper usage",
            RuleCategory.FALL_PROTECTION: "Install guardrails, safety nets, or provide personal fall arrest systems",
            RuleCategory.ELECTRICAL: "De-energize equipment, install GFCI protection, verify grounding",
            RuleCategory.EXCAVATION: "Perform required inspections, install shoring/sloping as needed",
            RuleCategory.CONFINED_SPACE: "Stop work, evacuate space, obtain required permits",
            RuleCategory.HOT_WORK: "Obtain hot work permit, assign fire watch, provide extinguishers",
            RuleCategory.SCAFFOLDING: "Inspect scaffold, install missing components, tag out if unsafe",
            RuleCategory.CRANE: "Verify operator certification, check rigging, establish swing radius"
        }

        return actions.get(rule.category, "Review and correct violation immediately")
```

### PPE Detection Integration

```python
class PPEComplianceChecker:
    """PPE compliance checking with CV integration support"""

    def __init__(self):
        self.ppe_requirements = self._load_requirements()

    def _load_requirements(self) -> Dict[str, List[str]]:
        """Load PPE requirements by work type"""
        return {
            'general': ['helmet', 'safety_vest', 'safety_boots'],
            'welding': ['helmet', 'welding_mask', 'gloves', 'apron', 'safety_boots'],
            'excavation': ['helmet', 'safety_vest', 'safety_boots', 'gloves'],
            'electrical': ['helmet', 'safety_glasses', 'insulated_gloves', 'safety_boots'],
            'concrete': ['helmet', 'safety_glasses', 'gloves', 'safety_boots', 'knee_pads'],
            'demolition': ['helmet', 'safety_glasses', 'dust_mask', 'gloves', 'safety_boots'],
            'roofing': ['helmet', 'harness', 'safety_boots', 'gloves'],
            'painting': ['helmet', 'respirator', 'safety_glasses', 'gloves', 'coveralls'],
            'scaffolding': ['helmet', 'harness', 'safety_boots', 'gloves']
        }

    def check_worker_ppe(self, worker_id: str, work_type: str,
                         detected_ppe: List[str]) -> Dict:
        """Check worker PPE against requirements"""
        required = self.ppe_requirements.get(work_type, self.ppe_requirements['general'])

        missing = set(required) - set(detected_ppe)
        extra = set(detected_ppe) - set(required)

        compliance_score = (len(required) - len(missing)) / len(required) * 100

        return {
            'worker_id': worker_id,
            'work_type': work_type,
            'required_ppe': required,
            'detected_ppe': detected_ppe,
            'missing_ppe': list(missing),
            'compliance_score': compliance_score,
            'is_compliant': len(missing) == 0,
            'recommendations': [f"Provide {item}" for item in missing]
        }

    def process_cv_detections(self, detections: List[Dict]) -> List[Dict]:
        """Process detections from computer vision system"""
        results = []

        for detection in detections:
            worker_id = detection.get('worker_id', 'unknown')
            work_type = detection.get('work_type', 'general')
            detected_items = detection.get('ppe_items', [])

            result = self.check_worker_ppe(worker_id, work_type, detected_items)
            result['timestamp'] = detection.get('timestamp')
            result['location'] = detection.get('location')
            result['image_ref'] = detection.get('image_path')

            results.append(result)

        return results
```

### Site Inspection System

```python
from datetime import datetime, date
from typing import List, Dict, Optional
import pandas as pd

@dataclass
class InspectionItem:
    item_id: str
    category: str
    description: str
    is_compliant: bool
    notes: str
    photo_refs: List[str] = field(default_factory=list)
    corrective_action: Optional[str] = None

@dataclass
class SiteInspection:
    inspection_id: str
    site_id: str
    inspector: str
    inspection_date: date
    weather: str
    items: List[InspectionItem]
    overall_score: float
    recommendations: List[str]

class SiteInspectionSystem:
    """Construction site safety inspection management"""

    def __init__(self):
        self.checklists = self._load_checklists()
        self.inspections: List[SiteInspection] = []

    def _load_checklists(self) -> Dict[str, List[Dict]]:
        """Load inspection checklists by category"""
        return {
            'general_safety': [
                {'id': 'GS-001', 'item': 'Site access controlled and secured', 'category': 'Access'},
                {'id': 'GS-002', 'item': 'Safety signage posted at entrance', 'category': 'Signage'},
                {'id': 'GS-003', 'item': 'First aid station accessible and stocked', 'category': 'Emergency'},
                {'id': 'GS-004', 'item': 'Emergency contact numbers posted', 'category': 'Emergency'},
                {'id': 'GS-005', 'item': 'Fire extinguishers accessible and inspected', 'category': 'Fire'},
                {'id': 'GS-006', 'item': 'Evacuation routes clear and marked', 'category': 'Emergency'},
                {'id': 'GS-007', 'item': 'Housekeeping adequate (no tripping hazards)', 'category': 'Housekeeping'},
                {'id': 'GS-008', 'item': 'Material storage organized and stable', 'category': 'Storage'},
                {'id': 'GS-009', 'item': 'Adequate lighting in work areas', 'category': 'Environment'},
                {'id': 'GS-010', 'item': 'Toilets and washing facilities clean', 'category': 'Welfare'}
            ],
            'fall_protection': [
                {'id': 'FP-001', 'item': 'Guardrails installed where required', 'category': 'Guardrails'},
                {'id': 'FP-002', 'item': 'Floor openings covered or protected', 'category': 'Openings'},
                {'id': 'FP-003', 'item': 'Ladders in good condition and secured', 'category': 'Ladders'},
                {'id': 'FP-004', 'item': 'Harnesses inspected and in good condition', 'category': 'PPE'},
                {'id': 'FP-005', 'item': 'Anchor points adequate and tested', 'category': 'Anchors'},
                {'id': 'FP-006', 'item': 'Safety nets installed where required', 'category': 'Nets'},
                {'id': 'FP-007', 'item': 'Stairways have handrails', 'category': 'Stairs'},
                {'id': 'FP-008', 'item': 'Roof edge protection in place', 'category': 'Roof'}
            ],
            'scaffolding': [
                {'id': 'SC-001', 'item': 'Scaffold erected by competent person', 'category': 'Erection'},
                {'id': 'SC-002', 'item': 'Base plates and mudsills in place', 'category': 'Foundation'},
                {'id': 'SC-003', 'item': 'All platforms fully planked', 'category': 'Platforms'},
                {'id': 'SC-004', 'item': 'Guardrails on all open sides', 'category': 'Protection'},
                {'id': 'SC-005', 'item': 'Access ladders provided', 'category': 'Access'},
                {'id': 'SC-006', 'item': 'Tied to structure at required intervals', 'category': 'Stability'},
                {'id': 'SC-007', 'item': 'Inspection tag current', 'category': 'Documentation'},
                {'id': 'SC-008', 'item': 'No damage to components', 'category': 'Condition'}
            ],
            'electrical': [
                {'id': 'EL-001', 'item': 'GFCI protection on all outlets', 'category': 'Protection'},
                {'id': 'EL-002', 'item': 'Extension cords in good condition', 'category': 'Equipment'},
                {'id': 'EL-003', 'item': 'Panel boxes closed and labeled', 'category': 'Panels'},
                {'id': 'EL-004', 'item': 'No exposed live wires', 'category': 'Hazards'},
                {'id': 'EL-005', 'item': 'Lockout/tagout procedures followed', 'category': 'LOTO'},
                {'id': 'EL-006', 'item': 'Temporary wiring properly supported', 'category': 'Installation'}
            ],
            'excavation': [
                {'id': 'EX-001', 'item': 'Competent person inspection completed', 'category': 'Inspection'},
                {'id': 'EX-002', 'item': 'Utilities located and marked', 'category': 'Utilities'},
                {'id': 'EX-003', 'item': 'Protective systems in place (shoring/sloping)', 'category': 'Protection'},
                {'id': 'EX-004', 'item': 'Spoil pile minimum 2ft from edge', 'category': 'Materials'},
                {'id': 'EX-005', 'item': 'Safe access/egress within 25ft', 'category': 'Access'},
                {'id': 'EX-006', 'item': 'Water accumulation managed', 'category': 'Water'},
                {'id': 'EX-007', 'item': 'Barricades around excavation', 'category': 'Barriers'}
            ]
        }

    def conduct_inspection(self, site_id: str, inspector: str,
                           checklist_types: List[str],
                           responses: Dict[str, Dict]) -> SiteInspection:
        """Conduct site inspection"""
        items = []

        for checklist_type in checklist_types:
            checklist = self.checklists.get(checklist_type, [])

            for check in checklist:
                item_id = check['id']
                response = responses.get(item_id, {})

                items.append(InspectionItem(
                    item_id=item_id,
                    category=check['category'],
                    description=check['item'],
                    is_compliant=response.get('compliant', False),
                    notes=response.get('notes', ''),
                    photo_refs=response.get('photos', []),
                    corrective_action=response.get('action') if not response.get('compliant', False) else None
                ))

        # Calculate score
        compliant_count = sum(1 for item in items if item.is_compliant)
        overall_score = (compliant_count / len(items) * 100) if items else 0

        # Generate recommendations
        recommendations = []
        for item in items:
            if not item.is_compliant:
                recommendations.append(f"{item.item_id}: {item.corrective_action or 'Address non-compliance'}")

        inspection = SiteInspection(
            inspection_id=f"INS-{site_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
            site_id=site_id,
            inspector=inspector,
            inspection_date=date.today(),
            weather="Clear",  # Would be input
            items=items,
            overall_score=overall_score,
            recommendations=recommendations[:10]  # Top 10
        )

        self.inspections.append(inspection)
        return inspection

    def generate_inspection_report(self, inspection: SiteInspection) -> pd.DataFrame:
        """Generate inspection report DataFrame"""
        data = []

        for item in inspection.items:
            data.append({
                'Inspection ID': inspection.inspection_id,
                'Date': inspection.inspection_date,
                'Inspector': inspection.inspector,
                'Item ID': item.item_id,
                'Category': item.category,
                'Description': item.description,
                'Compliant': 'Yes' if item.is_compliant else 'No',
                'Notes': item.notes,
                'Corrective Action': item.corrective_action or ''
            })

        return pd.DataFrame(data)

    def get_compliance_trends(self, site_id: str, days: int = 30) -> Dict:
        """Get compliance trends for a site"""
        site_inspections = [
            i for i in self.inspections
            if i.site_id == site_id and
            (date.today() - i.inspection_date).days <= days
        ]

        if not site_inspections:
            return {'message': 'No inspections found'}

        scores = [i.overall_score for i in site_inspections]
        dates = [i.inspection_date for i in site_inspections]

        # Category breakdown
        category_compliance = {}
        for inspection in site_inspections:
            for item in inspection.items:
                if item.category not in category_compliance:
                    category_compliance[item.category] = {'compliant': 0, 'total': 0}
                category_compliance[item.category]['total'] += 1
                if item.is_compliant:
                    category_compliance[item.category]['compliant'] += 1

        return {
            'site_id': site_id,
            'inspection_count': len(site_inspections),
            'average_score': sum(scores) / len(scores),
            'score_trend': list(zip(dates, scores)),
            'category_compliance': {
                k: v['compliant'] / v['total'] * 100
                for k, v in category_compliance.items()
            },
            'latest_inspection': site_inspections[-1].inspection_id
        }
```

### Compliance Dashboard Data

```python
class SafetyDashboard:
    """Generate safety compliance dashboard data"""

    def __init__(self, engine: SafetyComplianceEngine,
                 inspection_system: SiteInspectionSystem):
        self.engine = engine
        self.inspections = inspection_system

    def get_dashboard_data(self, site_id: str) -> Dict:
        """Get comprehensive dashboard data"""
        # Active violations
        open_violations = [v for v in self.engine.violations if v.status == 'open']

        # Violations by severity
        by_severity = {}
        for v in open_violations:
            sev = v.severity.name
            by_severity[sev] = by_severity.get(sev, 0) + 1

        # Violations by category
        by_category = {}
        for v in open_violations:
            cat = v.rule.category.value
            by_category[cat] = by_category.get(cat, 0) + 1

        # Overdue violations
        overdue = [v for v in open_violations if v.deadline < date.today()]

        # Compliance trends
        trends = self.inspections.get_compliance_trends(site_id)

        return {
            'summary': {
                'total_open_violations': len(open_violations),
                'critical_violations': by_severity.get('CRITICAL', 0),
                'overdue_violations': len(overdue),
                'latest_inspection_score': trends.get('average_score', 0)
            },
            'violations_by_severity': by_severity,
            'violations_by_category': by_category,
            'overdue_items': [
                {
                    'rule': v.rule.name,
                    'location': v.location,
                    'deadline': v.deadline.isoformat(),
                    'days_overdue': (date.today() - v.deadline).days
                }
                for v in overdue
            ],
            'compliance_trend': trends.get('score_trend', []),
            'category_compliance': trends.get('category_compliance', {})
        }
```

## Quick Reference

| Check Type | OSHA Reference | Risk Level | Frequency |
|------------|---------------|------------|-----------|
| PPE Compliance | 1926.100-106 | High | Continuous |
| Fall Protection | 1926.501-503 | Critical | Daily |
| Scaffolding | 1926.451-454 | High | Before each use |
| Excavation | 1926.651-652 | High | Daily |
| Electrical | 1926.400-449 | Critical | Daily |
| Confined Space | 1926.1200 | Critical | Before entry |
| Hot Work | 1926.350-354 | High | Per activity |

## Resources

- **OSHA Construction Standards**: https://www.osha.gov/laws-regs/regulations/standardnumber/1926
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `progress-monitoring-cv` for PPE detection with computer vision
- See `risk-assessment-ml` for predictive safety analytics
- See `document-classification-nlp` for safety document processing
