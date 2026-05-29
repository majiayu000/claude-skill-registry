---
name: lawyer-expert
version: 1.0.0
description: Expert-level legal systems, contracts, compliance, and legal technology
category: professional
tags: [legal, contracts, compliance, law, legal-tech]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Lawyer Expert

Expert guidance for legal systems, contract law, regulatory compliance, and legal technology implementation.

## Core Concepts

### Legal Systems
- Contract law and drafting
- Intellectual property (IP)
- Corporate law
- Employment law
- Regulatory compliance
- Litigation and dispute resolution

### Legal Technology
- Contract lifecycle management (CLM)
- Legal document automation
- E-discovery systems
- Legal research platforms
- Case management software
- Compliance management systems

### Compliance Frameworks
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- SOX (Sarbanes-Oxley)
- HIPAA (Health Insurance Portability)
- Industry-specific regulations

## Contract Management

```python
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

class ContractStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    NEGOTIATION = "negotiation"
    APPROVED = "approved"
    EXECUTED = "executed"
    EXPIRED = "expired"
    TERMINATED = "terminated"

class Contract:
    def __init__(self, title: str, parties: List[str],
                 effective_date: datetime, expiration_date: datetime):
        self.id = self.generate_contract_id()
        self.title = title
        self.parties = parties
        self.effective_date = effective_date
        self.expiration_date = expiration_date
        self.status = ContractStatus.DRAFT
        self.clauses = []
        self.amendments = []
        self.version = 1

    def add_clause(self, clause_type: str, content: str):
        """Add clause to contract"""
        self.clauses.append({
            "type": clause_type,
            "content": content,
            "added_date": datetime.now()
        })

    def add_amendment(self, amendment: str, reason: str):
        """Add amendment to contract"""
        self.amendments.append({
            "amendment": amendment,
            "reason": reason,
            "date": datetime.now(),
            "version": self.version + 1
        })
        self.version += 1

    def check_expiration(self) -> dict:
        """Check if contract is expiring soon"""
        days_until_expiry = (self.expiration_date - datetime.now()).days

        return {
            "expired": days_until_expiry < 0,
            "days_until_expiry": days_until_expiry,
            "requires_renewal": 0 < days_until_expiry < 90
        }

    def execute(self, signatures: List[dict]) -> dict:
        """Execute contract with signatures"""
        if len(signatures) < len(self.parties):
            raise ValueError("All parties must sign")

        self.status = ContractStatus.EXECUTED

        return {
            "contract_id": self.id,
            "executed_date": datetime.now(),
            "signatures": signatures,
            "status": self.status.value
        }
```

## Legal Document Templates

```python
class LegalDocumentGenerator:
    def generate_nda(self, disclosing_party: str, receiving_party: str,
                     term_months: int = 24) -> str:
        """Generate Non-Disclosure Agreement"""
        template = f"""
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into as of {datetime.now().strftime('%B %d, %Y')}

BETWEEN:
{disclosing_party} ("Disclosing Party")
AND
{receiving_party} ("Receiving Party")

1. DEFINITION OF CONFIDENTIAL INFORMATION
The term "Confidential Information" means any and all information disclosed by the Disclosing Party...

2. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to:
a) Hold Confidential Information in strict confidence
b) Not disclose to any third parties
c) Use solely for the purpose of evaluating potential business relationship

3. TERM
This Agreement shall remain in effect for {term_months} months from the date of execution.

4. RETURN OF MATERIALS
Upon termination, all Confidential Information must be returned or destroyed.

_________________________    _________________________
{disclosing_party}           {receiving_party}
Date: _______________        Date: _______________
"""
        return template

    def generate_service_agreement(self, provider: str, client: str,
                                   services: List[str], fee: float) -> str:
        """Generate Service Agreement"""
        services_list = "\n".join([f"  - {s}" for s in services])

        template = f"""
PROFESSIONAL SERVICES AGREEMENT

Date: {datetime.now().strftime('%B %d, %Y')}

PARTIES:
Service Provider: {provider}
Client: {client}

1. SERVICES
Provider agrees to perform the following services:
{services_list}

2. COMPENSATION
Client agrees to pay ${fee:,.2f} for the services rendered.

3. PAYMENT TERMS
Payment due within 30 days of invoice date.

4. TERM AND TERMINATION
Either party may terminate with 30 days written notice.

5. CONFIDENTIALITY
Both parties agree to maintain confidentiality of proprietary information.

6. LIMITATION OF LIABILITY
Provider's liability limited to the amount of fees paid.

SIGNATURES:
_________________________    _________________________
{provider}                   {client}
"""
        return template
```

## Compliance Management

```python
class ComplianceManager:
    def __init__(self):
        self.regulations = []
        self.compliance_checks = []

    def assess_gdpr_compliance(self, system_data: dict) -> dict:
        """Assess GDPR compliance"""
        checks = {
            "data_inventory": self.check_data_inventory(system_data),
            "consent_management": self.check_consent_mechanisms(system_data),
            "data_subject_rights": self.check_dsr_processes(system_data),
            "data_protection": self.check_encryption(system_data),
            "breach_notification": self.check_breach_procedures(system_data),
            "dpo_appointed": system_data.get("dpo_appointed", False),
            "privacy_policy": self.check_privacy_policy(system_data)
        }

        compliance_score = sum(checks.values()) / len(checks) * 100

        return {
            "compliant": compliance_score >= 90,
            "score": compliance_score,
            "checks": checks,
            "recommendations": self.generate_recommendations(checks)
        }

    def assess_hipaa_compliance(self, healthcare_system: dict) -> dict:
        """Assess HIPAA compliance for healthcare systems"""
        checks = {
            "access_controls": self.check_access_controls(healthcare_system),
            "audit_logs": self.check_audit_logging(healthcare_system),
            "encryption": self.check_phi_encryption(healthcare_system),
            "baa_executed": healthcare_system.get("baa_signed", False),
            "training_completed": self.check_training(healthcare_system),
            "risk_assessment": self.check_risk_assessment(healthcare_system)
        }

        return {
            "compliant": all(checks.values()),
            "checks": checks,
            "violations": [k for k, v in checks.items() if not v]
        }

    def generate_privacy_policy(self, company: str, data_types: List[str]) -> str:
        """Generate privacy policy template"""
        data_collected = "\n".join([f"  - {dt}" for dt in data_types])

        return f"""
PRIVACY POLICY

Last Updated: {datetime.now().strftime('%B %d, %Y')}

{company} ("we", "our", "us") respects your privacy.

1. INFORMATION WE COLLECT
We collect the following types of information:
{data_collected}

2. HOW WE USE YOUR INFORMATION
We use your information to provide and improve our services.

3. DATA SHARING
We do not sell your personal information to third parties.

4. YOUR RIGHTS
You have the right to:
  - Access your personal data
  - Request correction or deletion
  - Object to processing
  - Data portability

5. SECURITY
We implement appropriate technical and organizational measures.

6. CONTACT US
For privacy inquiries: privacy@{company.lower().replace(' ', '')}.com
"""
```

## Best Practices

### Contract Management
- Use version control for all contract documents
- Implement electronic signature workflows
- Set up automated expiration alerts (90/60/30 days)
- Maintain centralized contract repository
- Regular contract audits and reviews
- Clear approval workflows
- Standardized clause libraries

### Compliance
- Regular compliance assessments
- Document all compliance efforts
- Implement privacy by design
- Maintain audit trails
- Regular staff training
- Incident response procedures
- Third-party vendor assessments

### Legal Technology
- Automate routine legal tasks
- Use AI for contract review and analysis
- Implement document management systems
- Maintain secure client portals
- Regular security audits
- Data backup and disaster recovery

## Anti-Patterns

❌ No contract version control
❌ Manual tracking of contract deadlines
❌ Storing sensitive data unencrypted
❌ No compliance documentation
❌ Ignoring data subject rights requests
❌ No legal review of automated documents
❌ Inadequate audit trails

## Resources

- GDPR Official Text: https://gdpr.eu/
- CCPA Information: https://oag.ca.gov/privacy/ccpa
- Legal Tech Resources: https://www.legaltechnology.com/
- Contract Standards: https://www.iaccm.com/
