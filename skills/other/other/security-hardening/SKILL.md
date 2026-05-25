---
name: security-hardening
description: Reduces attack surface across OS, container, cloud, network, and database layers using CIS Benchmarks and zero-trust principles. Use when hardening production infrastructure, meeting compliance requirements, or implementing defense-in-depth security.
---

# Security Hardening

## Purpose

Proactive reduction of attack surface across infrastructure layers through systematic configuration hardening, least-privilege enforcement, and automated security controls. Applies industry-standard CIS Benchmarks and zero-trust principles to operating systems, containers, cloud configurations, networks, and databases.

## When to Use This Skill

Invoke this skill when:
- Hardening production infrastructure before deployment
- Meeting compliance requirements (SOC 2, PCI-DSS, HIPAA, FedRAMP)
- Implementing zero-trust security architecture
- Reducing container or cloud misconfiguration risks
- Preparing for security audits or penetration tests
- Automating security baseline enforcement
- Responding to vulnerability scan findings

## Hardening Layers

Security hardening applies across five infrastructure layers:

### Layer 1: Operating System (Linux)
- Kernel parameter tuning (sysctl)
- SSH configuration hardening
- User and group management
- File system permissions and mount options
- Service minimization
- SELinux/AppArmor enforcement

### Layer 2: Container
- Minimal base images (Chainguard, Distroless, Alpine)
- Non-root container execution
- Read-only root filesystems
- Seccomp and AppArmor profiles
- Resource limits and capabilities dropping
- Pod Security Standards enforcement

### Layer 3: Cloud Configuration
- IAM least privilege and MFA enforcement
- Network security groups and NACL configuration
- Encryption at rest and in transit
- Public access blocking
- Logging and monitoring enablement
- CSPM (Cloud Security Posture Management) integration

### Layer 4: Network
- Default-deny network policies
- Network segmentation and micro-segmentation
- TLS/mTLS enforcement
- Firewall rule minimization
- DNS security (DNSSEC, DNS filtering)

### Layer 5: Database
- Authentication and authorization hardening
- Connection encryption (SSL/TLS)
- Audit logging enablement
- Network isolation and access control
- Role-based permissions with least privilege

## Core Hardening Principles

### 1. Default Deny, Explicit Allow
Start with all access denied, explicitly permit only required operations. Apply default-deny firewall rules and network policies, then allow specific traffic.

### 2. Least Privilege Access
Grant minimum permissions required for operation. Use RBAC, IAM policies with specific resources, and database roles with limited permissions (no DELETE or DDL unless required).

### 3. Defense in Depth
Implement multiple overlapping security controls: network firewalls, authentication, authorization, audit logging, and encryption working together.

### 4. Minimal Attack Surface
Remove unnecessary components, services, and permissions. Use minimal container base images, disable unused services, and drop all Linux capabilities unless required.

### 5. Fail Securely
On error or misconfiguration, default to secure state. Authentication failures deny access, missing configurations use restrictive defaults, and monitoring failures trigger immediate alerts.

## Hardening Priority Framework

Prioritize hardening efforts based on exposure and data sensitivity:

### Critical Priority: Internet-Facing Systems
**Apply immediately:**
- Container hardening (minimal images, non-root, read-only)
- Network segmentation (DMZ, WAF, DDoS protection)
- TLS termination and certificate management
- Rate limiting and authentication
- Real-time monitoring and alerting

**Tools:** Trivy, Falco, ModSecurity, Cloudflare

### High Priority: Systems with Sensitive Data
**Apply before production:**
- Encryption at rest (AES-256, KMS-managed keys)
- Strict access controls (RBAC, least privilege)
- Comprehensive audit logging
- Database connection encryption
- Regular vulnerability scanning

**Tools:** Checkov, Prowler, Lynis, OpenSCAP

### Standard Priority: Internal Systems
**Apply systematically:**
- OS hardening (CIS Benchmarks)
- Service minimization
- Patch management automation
- Configuration management
- Basic monitoring

**Tools:** Ansible, Puppet, kube-bench, docker-bench-security

## CIS Benchmark Integration

CIS (Center for Internet Security) Benchmarks provide industry-standard hardening guidance.

### Automated CIS Scanning

**Docker CIS Benchmark:**
```bash
docker run --rm -it \
  --net host \
  --pid host \
  --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security
```

**Kubernetes CIS Benchmark:**
```bash
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench
```

**Linux CIS Benchmark:**
```bash
# Using Lynis
lynis audit system --quick

# Using OpenSCAP
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2004-ds.xml
```

### Key CIS Controls Mapping

| CIS Control | Hardening Action | Layer |
|-------------|------------------|-------|
| 4.1 Secure Configuration | Apply hardening baselines | All layers |
| 5.1 Account Management | Enforce least privilege, MFA | OS, Cloud |
| 6.1 Access Control | RBAC, network policies | All layers |
| 8.1 Audit Log Management | Enable comprehensive logging | All layers |
| 13.1 Network Monitoring | Deploy IDS/IPS, flow logs | Network |
| 3.1 Data Protection | Enable encryption at rest/transit | Cloud, Database |

For detailed CIS control mapping, see `references/cis-benchmark-mapping.md`.

## Container Base Image Selection

Choose base images based on security requirements and compatibility needs:

| Use Case | Recommended Base | Size | CVEs | Trade-off |
|----------|------------------|------|------|-----------|
| **Production apps** | Chainguard Images | ~10MB | 0 | Minimal, zero CVEs |
| **Minimal Linux** | Alpine | ~5MB | Few | Small, auditable |
| **Compatibility** | Distroless | ~20MB | Few | No shell, harder debug |
| **Debugging** | Debian slim | ~80MB | More | Has debugging tools |
| **Legacy apps** | Ubuntu | ~100MB | Many | Full compatibility |

**Production recommendation:** Chainguard Images or Distroless for production, Alpine for development.

## Verification and Auditing

Hardening must be verified continuously, not just at implementation.

### Automated Security Scanning

**Container vulnerability scanning:**
```bash
# Trivy: Comprehensive vulnerability and misconfiguration scanner
trivy image --severity HIGH,CRITICAL myapp:latest

# Grype: Fast vulnerability scanner
grype myapp:latest
```

**Infrastructure as Code scanning:**
```bash
# Checkov: Multi-cloud IaC scanner
checkov -d terraform/ --framework terraform

# Terrascan: Policy-as-code scanner
terrascan scan -t terraform -d terraform/
```

**Kubernetes security scanning:**
```bash
# Kubesec: Security risk analysis
kubesec scan k8s/deployment.yaml

# Polaris: Configuration validation
polaris audit --format=pretty

# Trivy K8s scanning
trivy k8s --report summary cluster
```

**Cloud security posture:**
```bash
# Prowler: AWS security assessment
prowler aws --services s3 iam ec2

# ScoutSuite: Multi-cloud security audit
scout aws --services s3 iam ec2
```

### Continuous Verification Pipeline

Integrate security scanning into CI/CD:

```yaml
# GitHub Actions example
name: Security Hardening Verification

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily scan

jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:test .

      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:test'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on findings

  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan IaC with Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false
```

### Compliance Reporting

Generate compliance reports from scan results:

```bash
# Generate CIS compliance report
kube-bench run --json > cis-report.json

# Generate vulnerability report
trivy image --format json --output vuln-report.json myapp:latest

# Aggregate reports for compliance dashboard
python scripts/generate-compliance-report.py \
  --cis cis-report.json \
  --vulns vuln-report.json \
  --output compliance-dashboard.html
```

## Automation Tools

### Hardening Automation
- **Ansible/Puppet/Chef:** Configuration management for OS hardening
- **Terraform/Pulumi:** Infrastructure as Code with security modules
- **Cloud Custodian:** Cloud resource policy enforcement
- **OPA/Gatekeeper:** Kubernetes policy enforcement
- **Kyverno:** Kubernetes-native policy management

### Scanning Tools
- **Trivy:** Universal vulnerability and misconfiguration scanner
- **Checkov:** IaC security and compliance scanner
- **Falco:** Runtime security monitoring
- **Prowler:** AWS security assessment tool
- **ScoutSuite:** Multi-cloud security auditing
- **Lynis:** Linux security auditing
- **docker-bench-security:** Docker CIS benchmark scanner
- **kube-bench:** Kubernetes CIS benchmark scanner

### Monitoring Tools
- **Falco:** Runtime threat detection for containers
- **Sysdig:** Container security and monitoring
- **Wazuh:** Host and endpoint security monitoring
- **OSSEC:** Host-based intrusion detection

## Quick Reference: Common Hardening Tasks

### Harden SSH Access
```bash
# Edit /etc/ssh/sshd_config.d/hardening.conf
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
MaxAuthTries 3
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2

# Restart SSH
systemctl restart sshd
```

### Harden Container Image
```dockerfile
# Use minimal base
FROM cgr.dev/chainguard/python:latest

# Non-root user
USER nonroot

# Read-only filesystem
COPY --chown=nonroot:nonroot app /app
WORKDIR /app

# Drop all capabilities
ENTRYPOINT ["python", "-m", "app"]
```

### Harden Kubernetes Pod
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65534
  seccompProfile:
    type: RuntimeDefault
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

### Harden AWS S3 Bucket
```hcl
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
```

### Harden Network with Default Deny
```yaml
# Kubernetes NetworkPolicy: deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

### Harden Database Access
```sql
-- PostgreSQL hardening
REVOKE ALL ON DATABASE app FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

CREATE ROLE app_user WITH LOGIN;
GRANT CONNECT ON DATABASE app TO app_user;
GRANT SELECT, INSERT, UPDATE ON app.orders TO app_user;

-- Force SSL connections
ALTER SYSTEM SET ssl = on;
-- In pg_hba.conf: hostssl all all 0.0.0.0/0 scram-sha-256
```

## Detailed Hardening Guides

For layer-specific hardening guidance:
- **OS hardening:** See `references/linux-hardening.md`
- **Container hardening:** See `references/container-hardening.md`
- **Cloud hardening:** See `references/cloud-hardening.md`
- **Network hardening:** See `references/network-hardening.md`
- **Database hardening:** See `references/database-hardening.md`

For automation scripts:
- **Python automation:** See `scripts/harden-linux.py`
- **Container host setup:** See `scripts/harden-container-host.sh`
- **Compliance reporting:** See `scripts/generate-compliance-report.py`
- **Infrastructure scanning:** See `scripts/scan-infrastructure.sh`

For working examples:
- **Linux configurations:** See `examples/linux/`
- **Kubernetes manifests:** See `examples/kubernetes/`
- **Terraform modules:** See `examples/terraform/`

## Integration with Related Skills

- **auth-security:** Authentication and authorization patterns complement hardening
- **secret-management:** Secure secrets handling is essential for hardening
- **kubernetes-operations:** Pod security and RBAC hardening
- **infrastructure-as-code:** Security scanning in IaC pipelines
- **building-ci-pipelines:** Automated security scanning integration
- **observability:** Security monitoring and alerting
- **compliance-frameworks:** Mapping hardening to compliance requirements

## Anti-Patterns to Avoid

**❌ Hardening only at deployment**
- Hardening is continuous; scan and verify regularly

**❌ Applying all controls blindly**
- Prioritize based on risk and exposure

**❌ No verification**
- Always verify hardening is applied and effective

**❌ Security through obscurity**
- Obscurity is not security; use proven controls

**❌ Hardening without testing**
- Test hardening changes don't break functionality

**❌ Manual hardening at scale**
- Automate hardening for consistency and repeatability

## Getting Started

1. **Assess current posture:** Run CIS benchmark scans
2. **Prioritize:** Internet-facing → sensitive data → internal
3. **Apply baseline hardening:** OS, container, cloud basics
4. **Automate:** Use scripts and IaC for consistency
5. **Verify continuously:** Integrate scanning into CI/CD
6. **Monitor:** Deploy runtime security monitoring
7. **Iterate:** Review and improve hardening regularly

For step-by-step implementation, start with `references/linux-hardening.md` or `references/container-hardening.md` based on infrastructure type.
