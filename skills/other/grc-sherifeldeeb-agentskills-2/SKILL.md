---
name: grc
description: |
  Governance, Risk, and Compliance documentation and assessment support.
  Generate policies, assess controls, and track compliance status. Use for
  GRC programs, audits, and regulatory compliance.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - No external dependencies (standard library only)
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# GRC Skill

Support Governance, Risk, and Compliance activities with policy generation, control assessment, risk management, and compliance tracking.

## Capabilities

- **Policy Management**: Generate and track security policies
- **Control Assessment**: Document and assess control effectiveness
- **Risk Management**: Maintain risk registers and assessments
- **Compliance Tracking**: Track compliance with multiple frameworks
- **Audit Support**: Generate audit evidence and reports
- **Framework Mapping**: Map controls across frameworks

## Quick Start

```python
from grc_utils import PolicyGenerator, ControlAssessment, RiskRegister, ComplianceTracker

# Generate a policy
policy = PolicyGenerator('Access Control Policy')
policy.add_section('Purpose', 'Define access control requirements...')
policy.add_control('AC-1', 'Users must use unique identifiers')
print(policy.generate())

# Assess a control
assessment = ControlAssessment('AC-1', 'Access Control')
assessment.set_effectiveness('effective')
assessment.add_evidence('access_review_report.pdf', 'Quarterly access review')

# Track compliance
tracker = ComplianceTracker('SOC 2')
tracker.add_control('CC6.1', status='compliant')
print(tracker.get_compliance_status())
```

## Usage

### Policy Management

Generate and manage security policies.

**Example**:
```python
from grc_utils import PolicyGenerator

# Create policy
policy = PolicyGenerator(
    title='Information Security Policy',
    version='1.0',
    owner='CISO',
    classification='Internal'
)

# Add sections
policy.add_section(
    'Purpose',
    '''This policy establishes the information security requirements
    for protecting organizational assets and data.'''
)

policy.add_section(
    'Scope',
    '''This policy applies to all employees, contractors, and third
    parties with access to organizational systems.'''
)

policy.add_section(
    'Policy Statements',
    '''1. All users must complete security awareness training annually.
    2. Multi-factor authentication is required for all remote access.
    3. Data must be classified and handled according to its sensitivity.'''
)

# Add controls
policy.add_control('AC-1', 'Access control policy and procedures')
policy.add_control('AC-2', 'Account management')
policy.add_control('AT-1', 'Security awareness training')

# Set review schedule
policy.set_review_schedule(frequency='annual', next_review='2025-01-01')

# Generate outputs
print(policy.generate())  # Markdown format
print(policy.to_json())   # JSON for storage
```

### Control Assessment

Document and assess control effectiveness.

**Example**:
```python
from grc_utils import ControlAssessment

# Create assessment
assessment = ControlAssessment(
    control_id='AC-2',
    control_name='Account Management',
    framework='NIST 800-53'
)

# Set control details
assessment.set_description('''
The organization manages information system accounts, including:
- Identifying account types
- Establishing conditions for group membership
- Identifying authorized users
- Specifying access privileges
''')

# Document implementation
assessment.set_implementation('''
Account management is implemented through:
- Active Directory for identity management
- Privileged Access Management (PAM) solution
- Quarterly access reviews
- Automated deprovisioning workflows
''')

# Add evidence
assessment.add_evidence(
    filename='access_review_q4_2024.pdf',
    description='Q4 2024 access review report',
    date_collected='2024-01-15'
)

assessment.add_evidence(
    filename='pam_config_screenshot.png',
    description='PAM solution configuration',
    date_collected='2024-01-10'
)

# Set effectiveness
assessment.set_effectiveness(
    rating='effective',
    notes='Control operating as intended with minor documentation gaps'
)

# Identify gaps
assessment.add_gap(
    description='Service account reviews not documented',
    remediation='Implement service account review process',
    priority='Medium',
    due_date='2024-03-01'
)

# Generate report
print(assessment.generate_report())
```

### Risk Management

Maintain risk registers and assessments.

**Example**:
```python
from grc_utils import RiskRegister

register = RiskRegister()

# Add risks
register.add_risk(
    risk_id='RISK-001',
    title='Ransomware Attack',
    description='Risk of ransomware infection causing data loss and operational disruption',
    category='Cybersecurity',
    likelihood='medium',
    impact='high',
    inherent_risk='high'
)

register.add_risk(
    risk_id='RISK-002',
    title='Third-Party Data Breach',
    description='Risk of data breach through third-party vendor',
    category='Third Party',
    likelihood='medium',
    impact='medium',
    inherent_risk='medium'
)

# Add controls/mitigations
register.add_mitigation(
    risk_id='RISK-001',
    control='Endpoint Detection and Response (EDR)',
    effectiveness='high'
)

register.add_mitigation(
    risk_id='RISK-001',
    control='Backup and Recovery Solution',
    effectiveness='high'
)

# Calculate residual risk
register.calculate_residual_risk('RISK-001')

# Set treatment
register.set_treatment(
    risk_id='RISK-001',
    treatment='mitigate',
    owner='Security Operations',
    notes='Continuing to enhance detection and response capabilities'
)

# Generate risk report
print(register.generate_report())
print(register.generate_heatmap_data())
```

### Compliance Tracking

Track compliance across frameworks.

**Example**:
```python
from grc_utils import ComplianceTracker

# Create tracker for SOC 2
tracker = ComplianceTracker('SOC 2 Type II')

# Add controls with status
tracker.add_control(
    control_id='CC6.1',
    description='Logical and physical access controls',
    status='compliant',
    evidence=['access_control_policy.pdf', 'access_review_q4.xlsx']
)

tracker.add_control(
    control_id='CC6.2',
    description='Access credentials management',
    status='compliant',
    evidence=['mfa_implementation.pdf']
)

tracker.add_control(
    control_id='CC6.3',
    description='Access removal',
    status='partially_compliant',
    evidence=['termination_checklist.pdf'],
    gaps=['Delayed offboarding for contractors']
)

tracker.add_control(
    control_id='CC7.1',
    description='Detection of unauthorized changes',
    status='non_compliant',
    gaps=['FIM not fully implemented']
)

# Get compliance status
status = tracker.get_compliance_status()
print(f"Compliant: {status['compliant']}")
print(f"Partially Compliant: {status['partially_compliant']}")
print(f"Non-Compliant: {status['non_compliant']}")

# Generate compliance report
print(tracker.generate_report())
```

### Framework Mapping

Map controls across multiple frameworks.

**Example**:
```python
from grc_utils import FrameworkMapper

mapper = FrameworkMapper()

# Add control mappings
mapper.add_mapping(
    control_name='Access Control Policy',
    mappings={
        'NIST 800-53': 'AC-1',
        'ISO 27001': 'A.9.1.1',
        'SOC 2': 'CC6.1',
        'CIS': 'Control 6.1'
    }
)

mapper.add_mapping(
    control_name='Multi-Factor Authentication',
    mappings={
        'NIST 800-53': 'IA-2(1)',
        'ISO 27001': 'A.9.4.2',
        'SOC 2': 'CC6.1',
        'CIS': 'Control 6.5'
    }
)

# Get control by framework
nist_controls = mapper.get_by_framework('NIST 800-53')

# Find equivalent controls
equivalents = mapper.find_equivalents('NIST 800-53', 'AC-1')

# Generate mapping matrix
print(mapper.generate_matrix())
```

### Audit Support

Generate audit evidence and reports.

**Example**:
```python
from grc_utils import AuditPackage

audit = AuditPackage(
    audit_name='SOC 2 Type II 2024',
    period_start='2024-01-01',
    period_end='2024-12-31'
)

# Add evidence
audit.add_evidence(
    request_id='RQ-001',
    description='Access control policy',
    filename='access_control_policy_v2.1.pdf',
    control_ids=['CC6.1', 'CC6.2'],
    provided_by='security-team',
    date_provided='2024-01-15'
)

audit.add_evidence(
    request_id='RQ-002',
    description='Quarterly access reviews',
    filename='access_reviews_2024.xlsx',
    control_ids=['CC6.1'],
    provided_by='it-team',
    date_provided='2024-01-16'
)

# Track findings
audit.add_finding(
    finding_id='FIND-001',
    description='Delayed access removal for terminated employees',
    severity='Medium',
    control_ids=['CC6.3'],
    management_response='Implementing automated deprovisioning',
    remediation_date='2024-03-01'
)

# Generate audit package
print(audit.generate_evidence_index())
print(audit.generate_finding_summary())
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GRC_OUTPUT_DIR` | Output directory for reports | No | `./output` |
| `GRC_TEMPLATE_DIR` | Directory for policy templates | No | `./templates` |

## Supported Frameworks

- **NIST 800-53** - Security and Privacy Controls
- **NIST CSF** - Cybersecurity Framework
- **ISO 27001** - Information Security Management
- **SOC 2** - Service Organization Controls
- **PCI DSS** - Payment Card Industry
- **HIPAA** - Health Insurance Portability
- **GDPR** - General Data Protection Regulation
- **CIS Controls** - Center for Internet Security

## Limitations

- **No Database**: Data stored in memory only
- **No Workflow**: Manual status updates required
- **Template-Based**: Limited customization

## Troubleshooting

### Invalid Risk Rating

Use valid risk rating values:
```python
# Valid ratings
register.add_risk(..., likelihood='high')    # high, medium, low
register.add_risk(..., impact='critical')    # critical, high, medium, low

# Invalid
register.add_risk(..., likelihood='very high')  # Error!
```

### Compliance Status Values

Use standard compliance statuses:
```python
# Valid
tracker.add_control(..., status='compliant')
tracker.add_control(..., status='partially_compliant')
tracker.add_control(..., status='non_compliant')
tracker.add_control(..., status='not_applicable')
```

## Related Skills

- [vulnerability-management](../vulnerability-management/): Technical compliance
- [docx](../../baseline/docx/): Policy document generation
- [xlsx](../../baseline/xlsx/): Compliance tracking spreadsheets

## References

- [Detailed API Reference](references/REFERENCE.md)
- [NIST 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [ISO 27001:2022](https://www.iso.org/standard/27001)
