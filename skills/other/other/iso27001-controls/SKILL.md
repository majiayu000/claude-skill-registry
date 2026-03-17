---
name: iso27001-controls
description: Эксперт ISO 27001. Используй для ISMS, security controls и compliance implementation.
---

# ISO 27001 Controls Expert

Expert in implementing and auditing ISO 27001 Information Security Management System controls.

## Control Categories Overview

### ISO 27001:2022 Annex A Structure

| Category | Controls | Focus Area |
|----------|----------|------------|
| A.5 Organizational | 37 controls | Policies, roles, responsibilities |
| A.6 People | 8 controls | HR security, awareness |
| A.7 Physical | 14 controls | Physical and environmental |
| A.8 Technological | 34 controls | Technical security measures |

### Risk-Based Approach

- Controls selection based on risk assessment outcomes
- Statement of Applicability (SoA) documents rationale
- Controls can be implemented, not applicable, or excluded with justification
- Continuous improvement through PDCA cycle

## Control Implementation Framework

### Control Assessment Template

```yaml
control_assessment:
  control_id: "A.8.24"
  control_name: "Use of Cryptography"
  category: "Technological Controls"
  objective: "Ensure proper and effective use of cryptography to protect confidentiality, authenticity and integrity of information"

  current_state:
    implementation_status: "Partial"
    existing_controls:
      - "TLS 1.2 for web traffic"
      - "AES-256 for database encryption"
    gaps:
      - "No key management policy"
      - "Legacy systems using TLS 1.0"
      - "Inconsistent encryption at rest"

  risk_assessment:
    likelihood: "Medium"
    impact: "High"
    risk_level: "High"
    risk_treatment: "Mitigate"

  implementation_plan:
    actions:
      - description: "Develop cryptography policy"
        owner: "Security Manager"
        deadline: "2024-03-01"
        status: "In Progress"

      - description: "Upgrade all systems to TLS 1.3"
        owner: "IT Infrastructure"
        deadline: "2024-04-15"
        status: "Planned"

      - description: "Implement key management solution"
        owner: "Security Operations"
        deadline: "2024-05-01"
        status: "Planned"

  evidence_required:
    - "Cryptography policy document"
    - "TLS configuration audit report"
    - "Key management procedures"
    - "Encryption inventory"

  success_metrics:
    - "100% systems using TLS 1.2+"
    - "All sensitive data encrypted at rest"
    - "Key rotation performed quarterly"
```

## Key Control Areas

### A.5 Organizational Controls

```yaml
A.5.1_Policies_for_Information_Security:
  requirement: "Information security policy and topic-specific policies shall be defined, approved by management, published, communicated and acknowledged"

  implementation:
    policies_required:
      - "Information Security Policy (overarching)"
      - "Acceptable Use Policy"
      - "Access Control Policy"
      - "Data Classification Policy"
      - "Incident Response Policy"
      - "Business Continuity Policy"
      - "Cryptography Policy"

    policy_structure:
      - "Purpose and scope"
      - "Roles and responsibilities"
      - "Policy statements"
      - "Compliance requirements"
      - "Review and update procedures"

    review_cycle: "Annual minimum, or upon significant changes"

  evidence:
    - "Approved policy documents"
    - "Communication records"
    - "Acknowledgment signatures/records"
    - "Review meeting minutes"

A.5.15_Access_Control:
  requirement: "Rules to control physical and logical access to information and other associated assets shall be established and implemented"

  implementation:
    principles:
      - "Need-to-know basis"
      - "Least privilege"
      - "Segregation of duties"
      - "Role-based access control"

    processes:
      access_request:
        - "Formal request submission"
        - "Manager approval"
        - "Security review for sensitive access"
        - "Provisioning within SLA"

      access_review:
        frequency: "Quarterly for privileged, annual for standard"
        scope: "All access rights"
        output: "Remediation of inappropriate access"

      access_revocation:
        triggers:
          - "Employment termination"
          - "Role change"
          - "Extended leave"
        sla: "Same day for terminations"

  evidence:
    - "Access control policy"
    - "Access request forms/tickets"
    - "Approval records"
    - "Access review reports"
    - "Revocation procedures"
```

### A.8 Technological Controls

```yaml
A.8.9_Configuration_Management:
  requirement: "Configurations, including security configurations, of hardware, software, services and networks shall be established, documented, implemented, monitored and reviewed"

  implementation:
    baseline_configurations:
      servers:
        - "Hardened OS images"
        - "Disabled unnecessary services"
        - "Security patches current"
        - "Logging enabled"

      network_devices:
        - "Encrypted management protocols"
        - "Access lists configured"
        - "Logging to SIEM"
        - "Firmware current"

      endpoints:
        - "Endpoint protection installed"
        - "Disk encryption enabled"
        - "Auto-updates enabled"
        - "Local firewall active"

    change_management:
      - "Configuration change requests"
      - "Security impact assessment"
      - "Testing before deployment"
      - "Rollback procedures"

    monitoring:
      - "Configuration drift detection"
      - "Automated compliance scanning"
      - "Alert on unauthorized changes"

  tools:
    - "Ansible/Terraform for IaC"
    - "CIS Benchmarks"
    - "Qualys/Nessus for scanning"
    - "SIEM for change detection"

A.8.24_Use_of_Cryptography:
  requirement: "Rules for the effective use of cryptography, including cryptographic key management, shall be defined and implemented"

  implementation:
    encryption_standards:
      data_at_rest:
        algorithm: "AES-256"
        scope: "All sensitive data"
        key_storage: "HSM or secure vault"

      data_in_transit:
        protocol: "TLS 1.3 (minimum 1.2)"
        cipher_suites: "ECDHE with AES-GCM"
        certificate_management: "Automated renewal"

      hashing:
        passwords: "bcrypt/Argon2"
        integrity: "SHA-256 or higher"
        prohibited: "MD5, SHA-1"

    key_management:
      generation: "Cryptographically secure RNG"
      storage: "HSM for production keys"
      rotation:
        symmetric: "Annual or per policy"
        asymmetric: "Per certificate validity"
      destruction: "Secure deletion with audit trail"

  prohibited_algorithms:
    - "DES, 3DES"
    - "RC4"
    - "MD5 for security purposes"
    - "SHA-1 for signatures"
    - "TLS 1.0, 1.1"

A.8.16_Monitoring_Activities:
  requirement: "Networks, systems and applications shall be monitored for anomalous behaviour and appropriate actions taken"

  implementation:
    log_sources:
      - "Authentication systems"
      - "Firewalls and network devices"
      - "Servers and endpoints"
      - "Applications and databases"
      - "Cloud services"

    monitoring_capabilities:
      real_time:
        - "Failed authentication attempts"
        - "Privileged account usage"
        - "Malware detection"
        - "Network anomalies"

      periodic:
        - "Access reviews"
        - "Vulnerability scans"
        - "Configuration compliance"
        - "Log analysis"

    alerting:
      critical:
        response_time: "15 minutes"
        examples:
          - "Multiple failed authentications"
          - "Privileged escalation"
          - "Malware detection"
          - "Data exfiltration indicators"

      high:
        response_time: "1 hour"
        examples:
          - "Unusual access patterns"
          - "Policy violations"
          - "Configuration changes"

    retention:
      security_logs: "12 months minimum"
      audit_logs: "7 years for compliance"
```

## Statement of Applicability (SoA)

```yaml
soa_template:
  document_control:
    version: "1.0"
    date: "2024-01-15"
    owner: "Information Security Manager"
    approved_by: "CISO"
    next_review: "2025-01-15"

  controls:
    A.5.1:
      control_name: "Policies for information security"
      applicable: true
      justification: "Required for ISMS governance"
      implementation_status: "Implemented"
      implementation_description: "Suite of 12 security policies approved and communicated"
      evidence_reference: "POL-001 to POL-012"

    A.5.2:
      control_name: "Information security roles and responsibilities"
      applicable: true
      justification: "Required for clear accountability"
      implementation_status: "Implemented"
      implementation_description: "RACI matrix and job descriptions updated"
      evidence_reference: "ORG-RACI-001"

    A.7.4:
      control_name: "Physical security monitoring"
      applicable: false
      justification: "Fully cloud-based organization, no physical premises to protect"
      residual_risk_acceptance: "Accepted by CISO on 2024-01-10"

  summary:
    total_controls: 93
    applicable: 87
    not_applicable: 6
    implemented: 72
    partially_implemented: 12
    planned: 3
```

## Audit Preparation

### Internal Audit Checklist

```yaml
audit_checklist:
  documentation_review:
    - "ISMS scope and boundaries defined"
    - "Information security policy approved"
    - "Risk assessment methodology documented"
    - "Risk treatment plan current"
    - "Statement of Applicability complete"
    - "Policies and procedures accessible"

  control_testing:
    access_control:
      - "Review user access provisioning process"
      - "Sample access requests for approval evidence"
      - "Verify access review completion"
      - "Test termination access revocation"

    change_management:
      - "Review change management procedure"
      - "Sample changes for approval evidence"
      - "Verify testing before production"
      - "Check rollback capability"

    incident_management:
      - "Review incident response procedure"
      - "Sample incidents for handling evidence"
      - "Verify root cause analysis"
      - "Check lessons learned implementation"

  interviews:
    - "Management commitment to ISMS"
    - "Staff awareness of security policies"
    - "IT understanding of technical controls"
    - "HR knowledge of people controls"

audit_evidence_requirements:
  for_each_control:
    - "Policy/procedure documentation"
    - "Implementation evidence"
    - "Operating effectiveness evidence"
    - "Exception handling records"
```

### Common Non-Conformities

```yaml
common_findings:
  major_non_conformities:
    - finding: "No risk assessment performed"
      clause: "6.1.2"
      typical_cause: "Lack of methodology or resources"
      remediation: "Conduct formal risk assessment"

    - finding: "Missing Statement of Applicability"
      clause: "6.1.3 d)"
      typical_cause: "Incomplete documentation"
      remediation: "Create comprehensive SoA"

    - finding: "No management review conducted"
      clause: "9.3"
      typical_cause: "Lack of ISMS awareness"
      remediation: "Schedule and conduct management review"

  minor_non_conformities:
    - finding: "Access reviews not performed quarterly"
      control: "A.5.18"
      typical_cause: "Process not established"
      remediation: "Implement automated review process"

    - finding: "Incident response plan not tested"
      control: "A.5.24"
      typical_cause: "Resource constraints"
      remediation: "Schedule tabletop exercise"

  observations:
    - finding: "Security awareness training could be more frequent"
      control: "A.6.3"
      recommendation: "Increase from annual to quarterly"

    - finding: "Vulnerability scan results not trending"
      control: "A.8.8"
      recommendation: "Implement dashboard for metrics"
```

## Continuous Improvement

```yaml
pdca_cycle:
  plan:
    activities:
      - "Conduct risk assessment"
      - "Define security objectives"
      - "Create implementation plan"
      - "Allocate resources"
    outputs:
      - "Risk treatment plan"
      - "Security objectives"
      - "Implementation roadmap"

  do:
    activities:
      - "Implement controls"
      - "Conduct training"
      - "Deploy security tools"
      - "Document procedures"
    outputs:
      - "Implemented controls"
      - "Training records"
      - "Operational procedures"

  check:
    activities:
      - "Internal audits"
      - "Management reviews"
      - "Monitor KPIs"
      - "Incident analysis"
    outputs:
      - "Audit reports"
      - "Performance metrics"
      - "Improvement opportunities"

  act:
    activities:
      - "Corrective actions"
      - "Preventive actions"
      - "Process improvements"
      - "Control updates"
    outputs:
      - "Updated controls"
      - "Improved processes"
      - "Enhanced ISMS"

kpis:
  effectiveness:
    - "Number of security incidents"
    - "Mean time to detect/respond"
    - "Vulnerability remediation time"
    - "Audit findings closure rate"

  compliance:
    - "Policy acknowledgment rate"
    - "Training completion rate"
    - "Access review completion"
    - "Patch compliance percentage"

  maturity:
    - "Control implementation percentage"
    - "Process automation level"
    - "Risk treatment progress"
```

## Лучшие практики

1. **Risk-based approach** — приоритизируйте контроли по уровню риска
2. **Document everything** — evidence критичен для аудита
3. **Continuous monitoring** — не только для сертификации
4. **Management commitment** — без поддержки руководства ISMS не работает
5. **Regular reviews** — ежегодный минимум для всех политик
6. **Lessons learned** — учитесь на инцидентах и аудитах
