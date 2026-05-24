---
name: compliance-auditor  
description: Automated compliance auditing for SOC2, HIPAA, GDPR, and PCI-DSS. Activates for compliance checks, security audits, regulatory requirements, and compliance automation.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Compliance Auditor

Automated compliance auditing and continuous monitoring for regulatory frameworks.

## When to Use

- Running SOC2, HIPAA, GDPR, or PCI-DSS audits
- Implementing compliance controls
- Generating compliance reports
- Monitoring compliance posture
- Preparing for external audits

## Compliance Frameworks

### SOC2 Type II
**Trust Service Criteria:**
- Security
- Availability  
- Processing Integrity
- Confidentiality
- Privacy

### HIPAA
**Key Requirements:**
- PHI protection
- Access controls
- Audit logging
- Encryption (at rest and in transit)
- Business Associate Agreements

### GDPR
**Key Requirements:**
- PII identification and protection
- Consent management
- Data subject rights
- Data retention policies
- Cross-border transfer controls

### PCI-DSS
**Requirements:**
- Cardholder data protection
- Network segmentation
- Encryption
- Access controls
- Regular security testing

## Automated Compliance Checks

```python
# Compliance scanner
class ComplianceScanner:
    def scan_soc2(self, codebase_path: str) -> ComplianceReport:
        findings = []
        
        # Check for hardcoded secrets
        secrets = self.detect_secrets(codebase_path)
        if secrets:
            findings.append(Finding(
                severity='CRITICAL',
                control='CC6.1 - Logical Access',
                issue='Hardcoded credentials found',
                locations=secrets
            ))
        
        # Check encryption
        if not self.verify_encryption_at_rest():
            findings.append(Finding(
                severity='HIGH',
                control='CC6.7 - Encryption',
                issue='Encryption at rest not enabled'
            ))
        
        # Check audit logging
        if not self.verify_audit_logging():
            findings.append(Finding(
                severity='HIGH',
                control='CC7.2 - Monitoring',
                issue='Insufficient audit logging'
            ))
        
        return ComplianceReport(
            framework='SOC2',
            score=self.calculate_score(findings),
            findings=findings
        )
    
    def scan_hipaa(self, codebase_path: str) -> ComplianceReport:
        findings = []
        
        # Detect PHI in logs
        phi_exposure = self.detect_phi_in_logs(codebase_path)
        if phi_exposure:
            findings.append(Finding(
                severity='CRITICAL',
                requirement='§164.308(a)(1)(ii)(D) - Information Access',
                issue='PHI exposed in application logs',
                locations=phi_exposure
            ))
        
        # Check encryption
        if not self.verify_hipaa_encryption():
            findings.append(Finding(
                severity='CRITICAL',
                requirement='§164.312(a)(2)(iv) - Encryption',
                issue='PHI not encrypted at rest'
            ))
        
        return ComplianceReport(
            framework='HIPAA',
            score=self.calculate_score(findings),
            findings=findings
        )
```

## Compliance Controls Implementation

```yaml
# Infrastructure as Code - Compliance controls
compliance_controls:
  soc2:
    access_control:
      - mfa_required: true
      - password_policy:
          min_length: 12
          require_uppercase: true
          require_numbers: true
          require_symbols: true
      - session_timeout: 900  # 15 minutes
    
    encryption:
      - data_at_rest: AES-256
      - data_in_transit: TLS 1.2+
      - key_rotation: 90  # days
    
    monitoring:
      - centralized_logging: true
      - log_retention: 365  # days
      - alerts:
          - unauthorized_access
          - privilege_escalation
          - data_exfiltration
  
  hipaa:
    phi_protection:
      - encryption_required: true
      - access_logging: true
      - minimum_necessary: true
    
    audit_controls:
      - log_phi_access: true
      - log_modifications: true
      - log_deletions: true
      - retention_period: 2555  # 7 years
```

## Best Practices

- ✅ Run compliance scans weekly minimum
- ✅ Automate compliance checks in CI/CD
- ✅ Maintain compliance evidence automatically
- ✅ Regular security training for team
- ✅ Document all compliance controls
- ✅ Conduct annual risk assessments

## Related Skills

- `security-architect` agent
- `compliance-officer` agent
- `/compliance-scan` command
