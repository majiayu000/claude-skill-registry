---
name: standards-expert
version: 1.0.0
description: Expert-level ISO standards, quality management, compliance, and certification
category: professional
tags: [iso, standards, quality-management, compliance, certification]
allowed-tools:
  - Read
  - Write
  - Edit
---

# ISO Standards and Quality Management Expert

Expert guidance for ISO standards, quality management systems, compliance, and certification processes.

## Core Concepts

### ISO Standards
- ISO 9001 (Quality Management)
- ISO 27001 (Information Security)
- ISO 14001 (Environmental Management)
- ISO 45001 (Occupational Health & Safety)
- ISO/IEC 17025 (Testing and Calibration)
- ISO 22000 (Food Safety)

### Quality Management
- Plan-Do-Check-Act (PDCA) cycle
- Process approach
- Risk-based thinking
- Continuous improvement (Kaizen)
- Quality objectives and metrics
- Management review

### Compliance & Certification
- Gap analysis
- Internal audits
- Corrective actions
- Document control
- Management system documentation
- Certification audits

## ISO 9001 Quality Management System

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class ProcessCategory(Enum):
    MANAGEMENT = "management"
    OPERATIONAL = "operational"
    SUPPORT = "support"

@dataclass
class QualityProcess:
    process_id: str
    name: str
    category: ProcessCategory
    owner: str
    inputs: List[str]
    outputs: List[str]
    resources: List[str]
    kpis: List[str]
    risks: List[str]

class ISO9001QMS:
    """ISO 9001 Quality Management System"""

    def __init__(self, organization: str):
        self.organization = organization
        self.processes: Dict[str, QualityProcess] = {}
        self.quality_objectives = []
        self.risks = []
        self.opportunities = []

    def define_process(self, process: QualityProcess):
        """Define a quality process"""
        self.processes[process.process_id] = process

    def define_quality_objective(self, objective: Dict):
        """Define quality objective"""
        self.quality_objectives.append({
            'objective': objective['description'],
            'target': objective['target'],
            'measurement': objective['measurement'],
            'owner': objective['owner'],
            'deadline': objective['deadline'],
            'status': 'active'
        })

    def conduct_pdca_cycle(self, process_id: str) -> Dict:
        """Conduct PDCA cycle for process"""
        return {
            'plan': self._plan_phase(process_id),
            'do': self._do_phase(process_id),
            'check': self._check_phase(process_id),
            'act': self._act_phase(process_id)
        }

    def _plan_phase(self, process_id: str) -> Dict:
        """PDCA Plan phase"""
        process = self.processes.get(process_id)
        return {
            'objectives': 'Define objectives and processes',
            'resources': process.resources if process else [],
            'risks_identified': process.risks if process else []
        }

    def _do_phase(self, process_id: str) -> Dict:
        """PDCA Do phase"""
        return {
            'action': 'Implement the processes',
            'documentation': 'Document execution'
        }

    def _check_phase(self, process_id: str) -> Dict:
        """PDCA Check phase"""
        return {
            'monitoring': 'Monitor and measure processes',
            'analysis': 'Analyze results against objectives'
        }

    def _act_phase(self, process_id: str) -> Dict:
        """PDCA Act phase"""
        return {
            'improvements': 'Implement improvements',
            'corrective_actions': 'Take corrective actions'
        }
```

## ISO 27001 Information Security

```python
class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class InformationAsset:
    asset_id: str
    name: str
    description: str
    owner: str
    classification: str  # public, internal, confidential, restricted
    value: int  # 1-5 scale

@dataclass
class SecurityRisk:
    risk_id: str
    asset_id: str
    threat: str
    vulnerability: str
    likelihood: int  # 1-5 scale
    impact: int  # 1-5 scale
    risk_level: RiskLevel
    controls: List[str]
    residual_risk: RiskLevel

class ISO27001ISMS:
    """ISO 27001 Information Security Management System"""

    def __init__(self, organization: str):
        self.organization = organization
        self.assets: Dict[str, InformationAsset] = {}
        self.risks: Dict[str, SecurityRisk] = {}
        self.controls = {}

    def register_asset(self, asset: InformationAsset):
        """Register information asset"""
        self.assets[asset.asset_id] = asset

    def assess_risk(self, asset_id: str, threat: str,
                   vulnerability: str, likelihood: int, impact: int) -> SecurityRisk:
        """Assess security risk"""
        risk_score = likelihood * impact

        if risk_score >= 20:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 12:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 6:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        risk = SecurityRisk(
            risk_id=f"RISK-{len(self.risks) + 1:03d}",
            asset_id=asset_id,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=likelihood,
            impact=impact,
            risk_level=risk_level,
            controls=[],
            residual_risk=risk_level
        )

        self.risks[risk.risk_id] = risk
        return risk

    def implement_control(self, risk_id: str, control: str,
                         effectiveness: int):
        """Implement security control"""
        if risk_id in self.risks:
            risk = self.risks[risk_id]
            risk.controls.append(control)

            # Recalculate residual risk
            reduced_score = (risk.likelihood * risk.impact) * (1 - effectiveness/10)

            if reduced_score >= 20:
                risk.residual_risk = RiskLevel.CRITICAL
            elif reduced_score >= 12:
                risk.residual_risk = RiskLevel.HIGH
            elif reduced_score >= 6:
                risk.residual_risk = RiskLevel.MEDIUM
            else:
                risk.residual_risk = RiskLevel.LOW

    def generate_soa(self) -> Dict:
        """Generate Statement of Applicability"""
        # Annex A controls from ISO 27001
        controls = {
            'A.5': 'Information security policies',
            'A.6': 'Organization of information security',
            'A.7': 'Human resource security',
            'A.8': 'Asset management',
            'A.9': 'Access control',
            'A.10': 'Cryptography',
            'A.11': 'Physical and environmental security',
            'A.12': 'Operations security',
            'A.13': 'Communications security',
            'A.14': 'System acquisition, development and maintenance',
            'A.15': 'Supplier relationships',
            'A.16': 'Information security incident management',
            'A.17': 'Business continuity management',
            'A.18': 'Compliance'
        }

        return {
            'organization': self.organization,
            'controls': controls,
            'implementation_status': 'To be determined per control'
        }
```

## Audit Management

```python
class AuditType(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    CERTIFICATION = "certification"
    SURVEILLANCE = "surveillance"

@dataclass
class AuditFinding:
    finding_id: str
    audit_id: str
    type: str  # 'non_conformity', 'observation', 'opportunity'
    severity: str  # 'major', 'minor'
    description: str
    clause_reference: str
    evidence: str
    corrective_action: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = 'open'

class AuditManager:
    """Manage quality audits"""

    def __init__(self):
        self.audits = {}
        self.findings: Dict[str, AuditFinding] = {}

    def plan_audit(self, audit_id: str, audit_type: AuditType,
                  scope: List[str], auditors: List[str],
                  date: datetime) -> Dict:
        """Plan an audit"""
        audit = {
            'audit_id': audit_id,
            'type': audit_type.value,
            'scope': scope,
            'auditors': auditors,
            'date': date,
            'status': 'planned'
        }

        self.audits[audit_id] = audit
        return audit

    def record_finding(self, finding: AuditFinding):
        """Record audit finding"""
        self.findings[finding.finding_id] = finding

    def create_corrective_action(self, finding_id: str,
                                 action: str, responsible: str,
                                 due_date: datetime):
        """Create corrective action for finding"""
        if finding_id in self.findings:
            finding = self.findings[finding_id]
            finding.corrective_action = action
            finding.due_date = due_date
            finding.status = 'corrective_action_planned'

            return {
                'finding_id': finding_id,
                'action': action,
                'responsible': responsible,
                'due_date': due_date
            }

    def close_finding(self, finding_id: str, verification: str):
        """Close finding after verification"""
        if finding_id in self.findings:
            finding = self.findings[finding_id]
            finding.status = 'closed'

            return {
                'finding_id': finding_id,
                'closure_date': datetime.now(),
                'verification': verification
            }

    def generate_audit_report(self, audit_id: str) -> Dict:
        """Generate audit report"""
        audit = self.audits.get(audit_id)
        audit_findings = [f for f in self.findings.values()
                         if f.audit_id == audit_id]

        return {
            'audit': audit,
            'findings_count': len(audit_findings),
            'major_nc': sum(1 for f in audit_findings
                          if f.severity == 'major'),
            'minor_nc': sum(1 for f in audit_findings
                          if f.severity == 'minor'),
            'observations': sum(1 for f in audit_findings
                              if f.type == 'observation'),
            'findings': audit_findings
        }
```

## Document Control

```python
@dataclass
class Document:
    document_id: str
    title: str
    version: str
    author: str
    approver: str
    effective_date: datetime
    review_date: datetime
    status: str  # 'draft', 'approved', 'obsolete'

class DocumentControl:
    """Manage controlled documents"""

    def __init__(self):
        self.documents: Dict[str, List[Document]] = {}

    def create_document(self, doc: Document):
        """Create new document"""
        if doc.document_id not in self.documents:
            self.documents[doc.document_id] = []

        self.documents[doc.document_id].append(doc)

    def get_current_version(self, document_id: str) -> Optional[Document]:
        """Get current approved version"""
        if document_id in self.documents:
            versions = [d for d in self.documents[document_id]
                       if d.status == 'approved']
            if versions:
                return max(versions, key=lambda x: x.version)
        return None

    def revise_document(self, document_id: str, changes: str,
                       author: str) -> Document:
        """Create document revision"""
        current = self.get_current_version(document_id)

        if current:
            new_version = self._increment_version(current.version)

            new_doc = Document(
                document_id=document_id,
                title=current.title,
                version=new_version,
                author=author,
                approver=current.approver,
                effective_date=datetime.now(),
                review_date=datetime.now(),
                status='draft'
            )

            self.create_document(new_doc)
            return new_doc

    def _increment_version(self, version: str) -> str:
        """Increment version number"""
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
```

## Best Practices

### Implementation
- Get management commitment
- Conduct gap analysis first
- Define clear scope
- Document processes thoroughly
- Train all personnel
- Implement gradually
- Monitor effectiveness

### Auditing
- Plan audits regularly
- Use competent auditors
- Focus on process effectiveness
- Document findings clearly
- Follow up on corrective actions
- Learn from findings
- Share lessons learned

### Continuous Improvement
- Regular management reviews
- Monitor KPIs consistently
- Respond to changes
- Encourage employee feedback
- Benchmark against best practices
- Document improvements
- Celebrate successes

## Anti-Patterns

❌ Documentation for its own sake
❌ No management involvement
❌ Treating certification as the goal
❌ Ignoring audit findings
❌ No continuous improvement
❌ Poor document control
❌ Insufficient training

## Resources

- ISO: https://www.iso.org/
- ISO 9001:2015: https://www.iso.org/standard/62085.html
- ISO 27001:2022: https://www.iso.org/standard/82875.html
- ASQ (American Society for Quality): https://asq.org/
- ISO Survey: https://www.iso.org/the-iso-survey.html
