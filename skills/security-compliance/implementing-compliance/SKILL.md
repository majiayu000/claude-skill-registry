---
name: implementing-compliance
description: Implement and maintain compliance with SOC 2, HIPAA, PCI-DSS, and GDPR using unified control mapping, policy-as-code enforcement, and automated evidence collection. Use when building systems requiring regulatory compliance, implementing security controls across multiple frameworks, or automating audit preparation.
---

# Compliance Frameworks

Implement continuous compliance with major regulatory frameworks through unified control mapping, policy-as-code enforcement, and automated evidence collection.

## Purpose

Modern compliance is a continuous engineering discipline requiring technical implementation of security controls. This skill provides patterns for SOC 2 Type II, HIPAA, PCI-DSS 4.0, and GDPR compliance using infrastructure-as-code, policy automation, and evidence collection. Focus on unified controls that satisfy multiple frameworks simultaneously to reduce implementation effort by 60-80%.

## When to Use

Invoke when:
- Building SaaS products requiring SOC 2 Type II for enterprise sales
- Handling healthcare data (PHI) requiring HIPAA compliance
- Processing payment cards requiring PCI-DSS validation
- Serving EU residents and processing personal data under GDPR
- Implementing security controls that satisfy multiple compliance frameworks
- Automating compliance evidence collection and audit preparation
- Enforcing compliance policies in CI/CD pipelines

## Framework Selection

### Tier 1: Trust & Security Certifications

**SOC 2 Type II**
- Audience: SaaS vendors, cloud service providers
- When required: Enterprise B2B sales, handling customer data
- Timeline: 6-12 month observation period
- 2025 updates: Monthly control testing, AI governance, 72-hour breach disclosure

**ISO 27001**
- Audience: Global enterprises
- When required: International business, government contracts
- Timeline: 3-6 month certification, annual surveillance

### Tier 2: Industry-Specific Regulations

**HIPAA (Healthcare)**
- Audience: Healthcare providers, health tech handling PHI
- When required: Processing Protected Health Information
- 2025 focus: Zero Trust Architecture, EDR/XDR, AI assessments

**PCI-DSS 4.0 (Payment Card Industry)**
- Audience: Merchants, payment processors
- When required: Processing, storing, transmitting cardholder data
- Effective: April 1, 2025 (mandatory)
- Key changes: Client-side security, 12-char passwords, enhanced MFA

### Tier 3: Privacy Regulations

**GDPR (EU Privacy)**
- Audience: Organizations processing EU residents' data
- When required: EU customers/users (extraterritorial)
- 2025 updates: 48-hour breach reporting, 6% revenue fines, AI transparency

**CCPA/CPRA (California Privacy)**
- Audience: Businesses serving California residents
- When required: Revenue >$25M, or 100K+ CA residents, or 50%+ revenue from data sales

For detailed framework requirements, see references/soc2-controls.md, references/hipaa-safeguards.md, references/pci-dss-requirements.md, and references/gdpr-articles.md.

## Universal Control Implementation

### Unified Control Strategy

Implement controls once, map to multiple frameworks. Reduces effort by 60-80%.

**Implementation Priority:**
1. **Encryption** (ENC-001, ENC-002): AES-256 at rest, TLS 1.3 in transit
2. **Access Control** (MFA-001, RBAC-001): MFA, RBAC, least privilege
3. **Audit Logging** (LOG-001): Centralized, immutable, 7-year retention
4. **Monitoring** (MON-001): SIEM, intrusion detection, alerting
5. **Incident Response** (IR-001): Detection, escalation, breach notification

### Control Categories

**Identity & Access:**
- Multi-factor authentication for privileged access
- Role-based access control with least privilege
- Quarterly access reviews
- Password policy: 12+ characters, complexity

**Data Protection:**
- Encryption: AES-256 (rest), TLS 1.3 (transit)
- Data classification and tagging
- Retention policies aligned with regulations
- Data minimization

**Logging & Monitoring:**
- Centralized audit logging (all auth and data access)
- 7-year retention (satisfies all frameworks)
- Immutable storage (S3 Object Lock)
- Real-time alerting

**Network Security:**
- Network segmentation and VPC isolation
- Firewalls with deny-by-default
- Intrusion detection/prevention
- Regular vulnerability scanning

**Incident Response:**
- Documented incident response plan
- Automated detection and alerting
- Breach notification: HIPAA 60d, GDPR 48h, SOC 2 72h, PCI-DSS immediate

**Business Continuity:**
- Automated backups with defined RPO/RTO
- Multi-region disaster recovery
- Regular failover testing

For complete control implementations, see references/control-mapping-matrix.md.

## Compliance as Code

### Policy Enforcement with OPA

Enforce compliance policies in CI/CD before infrastructure deployment.

**Architecture:**
```
Git Push → Terraform Plan → JSON → OPA Evaluation
                                    ├─► Pass → Deploy
                                    └─► Fail → Block
```

**Example: Encryption Policy**

Enforce encryption requirements (SOC 2 CC6.1, HIPAA §164.312(a)(2)(iv), PCI-DSS Req 3.4):

See examples/opa-policies/encryption.rego for complete implementation.

**CI/CD Integration:**
```bash
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa eval --data policies/ --input tfplan.json 'data.compliance.main.deny'
```

For complete CI/CD patterns, see references/cicd-integration.md.

### Static Analysis with Checkov

Scan IaC with built-in compliance framework support:

```bash
checkov -d ./terraform \
  --check SOC2 --check HIPAA --check PCI --check GDPR \
  --output cli --output json
```

Create custom policies for organization-specific requirements. See examples/checkov-policies/ for examples.

### Automated Testing

Integrate compliance validation into test suites:

```python
def test_s3_encrypted(terraform_plan):
    """SOC2:CC6.1, HIPAA:164.312(a)(2)(iv)"""
    buckets = get_resources(terraform_plan, "aws_s3_bucket")
    encrypted = get_encryption_configs(terraform_plan)
    assert all_buckets_encrypted(buckets, encrypted)

def test_opa_policies():
    result = subprocess.run(["opa", "eval", "--data", "policies/",
        "--input", "tfplan.json", "data.compliance.main.deny"])
    assert not json.loads(result.stdout)
```

For complete test patterns, see references/compliance-testing.md.

## Technical Control Implementations

### Encryption at Rest

**Standards:** AES-256, managed KMS, automatic rotation

**AWS Example:**
```hcl
resource "aws_kms_key" "data" {
  enable_key_rotation = true
  tags = { Compliance = "ENC-001" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id       = aws_kms_key.data.arn
}
```

For complete encryption implementations including Azure and GCP, see references/encryption-implementations.md.

### Encryption in Transit

**Standards:** TLS 1.3 (TLS 1.2 minimum), strong ciphers, HSTS

**ALB Example:**
```hcl
resource "aws_lb_listener" "https" {
  port       = 443
  protocol   = "HTTPS"
  ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"
}
```

### Multi-Factor Authentication

**Standards:** TOTP, hardware tokens, biometric for privileged access

**AWS IAM Enforcement:**
```hcl
resource "aws_iam_policy" "require_mfa" {
  policy = jsonencode({
    Statement = [{
      Effect = "Deny"
      NotAction = ["iam:CreateVirtualMFADevice", "iam:EnableMFADevice"]
      Resource = "*"
      Condition = {
        BoolIfExists = { "aws:MultiFactorAuthPresent" = "false" }
      }
    }]
  })
}
```

For application-level MFA (TOTP), see examples/mfa-implementation.py.

### Role-Based Access Control

**Standards:** Least privilege, job function-based roles, quarterly reviews

**Kubernetes Example:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: development
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "deployments", "services"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]  # Read-only
```

For complete RBAC patterns including AWS IAM and OPA policies, see references/access-control-patterns.md.

### Audit Logging

**Standards:** Structured JSON, 7-year retention, immutable storage

**Required Events:** Authentication, authorization, data access, administrative actions, security events

**Python Example:**
```python
class AuditLogger:
    def log_event(self, event_type, user_id, resource_type,
                  resource_id, action, result, ip_address):
        audit_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type.value,
            "user_id": user_id,
            "action": action,
            "result": result,
            "resource": {"type": resource_type, "id": resource_id},
            "source": {"ip": ip_address}
        }
        self.logger.info(json.dumps(audit_event))
```

**Log Retention:**
```hcl
resource "aws_cloudwatch_log_group" "audit" {
  retention_in_days = 2555  # 7 years
  kms_key_id        = aws_kms_key.logs.arn
}

resource "aws_s3_bucket_object_lock_configuration" "audit" {
  bucket = aws_s3_bucket.audit_logs.id
  rule {
    default_retention { mode = "COMPLIANCE"; years = 7 }
  }
}
```

For complete audit logging patterns including HIPAA PHI access logging, see references/audit-logging-patterns.md.

## Evidence Collection Automation

### Continuous Monitoring

Automate evidence collection for continuous compliance validation.

**Architecture:**
```
AWS Config → EventBridge → Lambda → S3 (Evidence)
                                   → DynamoDB (Status)
```

**Evidence Collection:**
```python
class EvidenceCollector:
    def collect_encryption_evidence(self):
        evidence = {
            "control_id": "ENC-001",
            "frameworks": ["SOC2-CC6.1", "HIPAA-164.312(a)(2)(iv)"],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "PASS",
            "findings": []
        }
        # Check S3, RDS, EBS encryption status
        # Document findings
        return evidence
```

For complete evidence collector, see examples/evidence-collection/evidence_collector.py.

### Audit Report Generation

Generate compliance reports automatically:

```python
class AuditReportGenerator:
    def generate_soc2_report(self, start_date, end_date):
        controls = self.get_control_status("SOC2")
        return {
            "framework": "SOC 2 Type II",
            "compliance_score": self.calculate_score(controls),
            "trust_services_criteria": {...},
            "controls": self.format_controls(controls)
        }
```

For complete report generator, see examples/evidence-collection/report_generator.py.

## Control Mapping Matrix

Unified control mapping across frameworks:

| Control | SOC 2 | HIPAA | PCI-DSS | GDPR | ISO 27001 |
|---------|-------|-------|---------|------|-----------|
| MFA | CC6.1 | §164.312(d) | Req 8.3 | Art 32 | A.9.4.2 |
| Encryption at Rest | CC6.1 | §164.312(a)(2)(iv) | Req 3.4 | Art 32 | A.10.1.1 |
| Encryption in Transit | CC6.1 | §164.312(e)(1) | Req 4.1 | Art 32 | A.13.1.1 |
| Audit Logging | CC7.2 | §164.312(b) | Req 10.2 | Art 30 | A.12.4.1 |
| Access Reviews | CC6.1 | §164.308(a)(3)(ii)(C) | Req 8.2.4 | Art 32 | A.9.2.5 |
| Vulnerability Scanning | CC7.1 | §164.308(a)(8) | Req 11.2 | Art 32 | A.12.6.1 |
| Incident Response | CC7.3 | §164.308(a)(6) | Req 12.10 | Art 33 | A.16.1.1 |

**Strategy:** Implement once with proper tagging, map to all applicable frameworks.

For complete control mapping with 45+ controls, see references/control-mapping-matrix.md.

## Breach Notification Requirements

**Framework-Specific Timelines:**
- HIPAA: 60 days to HHS and affected individuals
- GDPR: 48 hours to supervisory authority (2025 update)
- SOC 2: 72 hours to affected customers
- PCI-DSS: Immediate to payment brands

**Required Elements:**
- Description of incident and data involved
- Estimated number of affected individuals
- Steps taken to mitigate harm
- Contact information for questions
- Remediation actions and timeline

For incident response templates, see references/incident-response-templates.md.

## Vendor Management

**Business Associate Agreements (HIPAA):**
- Required for all vendors handling PHI
- Specify permitted uses and disclosures
- Require appropriate safeguards
- Annual review and renewal

**Data Processing Agreements (GDPR):**
- Required for all vendors processing personal data
- Process only on controller instructions
- Implement appropriate technical measures
- Sub-processor approval required

**Assessment Process:**
1. Risk classification by data access level
2. Security questionnaire evaluation
3. BAA/DPA execution
4. SOC 2 report collection (≤90 days old)
5. Annual re-assessment

For vendor management templates, see references/vendor-management.md.

## Tools & Libraries

**Policy as Code:**
- Open Policy Agent (OPA): General-purpose policy engine
- Checkov: IaC security scanning with compliance frameworks
- tfsec: Terraform security scanner
- Trivy: Container and IaC scanner

**Compliance Automation:**
- AWS Config: AWS resource compliance monitoring
- Cloud Custodian: Multi-cloud compliance automation
- Drata/Vanta/Secureframe: Continuous compliance platforms

For tool selection guidance, see references/tool-recommendations.md.

## Integration with Other Skills

**Related Skills:**
- `security-hardening`: Technical security control implementation
- `secret-management`: Secrets handling per HIPAA/PCI-DSS
- `infrastructure-as-code`: IaC implementing compliance controls
- `kubernetes-operations`: K8s RBAC, network policies
- `building-ci-pipelines`: Policy enforcement in CI/CD
- `siem-logging`: Audit logging and monitoring
- `incident-management`: Incident response procedures

## Quick Reference

**Implementation Checklist:**
- [ ] Identify applicable frameworks
- [ ] Implement encryption (AES-256, TLS 1.3)
- [ ] Configure MFA for privileged access
- [ ] Implement RBAC with least privilege
- [ ] Set up audit logging (7-year retention)
- [ ] Configure security monitoring/alerting
- [ ] Create incident response plan
- [ ] Execute vendor agreements (BAAs, DPAs)
- [ ] Implement policy-as-code (OPA, Checkov)
- [ ] Automate evidence collection
- [ ] Conduct quarterly access reviews
- [ ] Perform annual risk assessments

**Common Mistakes:**
- Treating compliance as one-time project vs continuous process
- Implementing per-framework vs unified controls
- Manual evidence collection vs automation
- Insufficient log retention (<7 years)
- Missing MFA enforcement
- Not encrypting backups/logs
- Inadequate vendor due diligence

## References

**Framework Details:**
- references/soc2-controls.md - SOC 2 TSC control catalog
- references/hipaa-safeguards.md - HIPAA safeguards
- references/pci-dss-requirements.md - PCI-DSS 4.0 requirements
- references/gdpr-articles.md - GDPR key articles

**Implementation Patterns:**
- references/control-mapping-matrix.md - Unified control mapping
- references/encryption-implementations.md - Encryption patterns
- references/access-control-patterns.md - MFA, RBAC implementations
- references/audit-logging-patterns.md - Logging requirements
- references/incident-response-templates.md - IR procedures

**Automation:**
- references/cicd-integration.md - OPA/Checkov CI/CD integration
- references/compliance-testing.md - Automated test patterns
- references/vendor-management.md - Vendor assessment templates
- references/tool-recommendations.md - Tool selection guide

**Code Examples:**
- examples/opa-policies/ - OPA policy examples
- examples/terraform/ - Terraform control implementations
- examples/evidence-collection/ - Evidence automation
- examples/mfa-implementation.py - TOTP MFA implementation

Consult qualified legal counsel and auditors for legal interpretation and audit preparation.
