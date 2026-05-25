---
name: managing-vulnerabilities
description: Implementing multi-layer security scanning (container, SAST, DAST, SCA, secrets), SBOM generation, and risk-based vulnerability prioritization in CI/CD pipelines. Use when building DevSecOps workflows, ensuring compliance, or establishing security gates for container deployments.
---

# Vulnerability Management

Implement comprehensive vulnerability detection and remediation workflows across containers, source code, dependencies, and running applications. This skill covers multi-layer scanning strategies, SBOM generation (CycloneDX and SPDX), risk-based prioritization using CVSS/EPSS/KEV, and CI/CD security gate patterns.

## When to Use This Skill

Invoke this skill when:

- Building security scanning into CI/CD pipelines
- Generating Software Bills of Materials (SBOMs) for compliance
- Prioritizing vulnerability remediation using risk-based approaches
- Implementing security gates (fail builds on critical vulnerabilities)
- Scanning container images before deployment
- Detecting secrets, misconfigurations, or code vulnerabilities
- Establishing DevSecOps practices and automation
- Meeting regulatory requirements (SBOM mandates, Executive Order 14028)

## Multi-Layer Scanning Strategy

Vulnerability management requires scanning at multiple layers. Each layer detects different types of security issues.

### Layer Overview

**Container Image Scanning**
- Detects vulnerabilities in OS packages, language dependencies, and binaries
- Tools: Trivy (comprehensive), Grype (accuracy-focused), Snyk Container (commercial)
- When: Every container build, base image selection, registry admission control

**SAST (Static Application Security Testing)**
- Analyzes source code for security flaws before runtime
- Tools: Semgrep (fast, semantic), Snyk Code (developer-first), SonarQube (enterprise)
- When: Every commit, PR checks, main branch protection

**DAST (Dynamic Application Security Testing)**
- Tests running applications for vulnerabilities (black-box testing)
- Tools: OWASP ZAP (open-source), StackHawk (CI/CD native), Burp Suite (manual + automated)
- When: Staging environment testing, API validation, authentication testing

**SCA (Software Composition Analysis)**
- Analyzes third-party dependencies for known vulnerabilities
- Tools: Dependabot (GitHub native), Renovate (advanced), Snyk Open Source (commercial)
- When: Every build, dependency updates, license audits

**Secret Scanning**
- Prevents secrets from being committed to source code
- Tools: Gitleaks (fast, configurable), TruffleHog (entropy detection), GitGuardian (commercial)
- When: Pre-commit hooks, repository scanning, CI/CD artifact checks

### Quick Tool Selection

```
Container Image → Trivy (default choice) OR Grype (accuracy focus)
Source Code → Semgrep (open-source) OR Snyk Code (commercial)
Running Application → OWASP ZAP (open-source) OR StackHawk (CI/CD native)
Dependencies → Dependabot (GitHub) OR Renovate (advanced automation)
Secrets → Gitleaks (open-source) OR GitGuardian (commercial)
```

For detailed tool selection guidance, see `references/tool-selection.md`.

## SBOM Generation

Software Bills of Materials (SBOMs) provide a complete inventory of software components and dependencies. Required for compliance and security transparency.

### CycloneDX vs. SPDX

**CycloneDX** (Recommended for DevSecOps)
- Security-focused, OWASP-maintained
- Native vulnerability references
- Fast, lightweight (JSON/XML/ProtoBuf)
- Best for: DevSecOps pipelines, vulnerability tracking

**SPDX** (Recommended for Legal/Compliance)
- License compliance focus, ISO standard (ISO/IEC 5962:2021)
- Comprehensive legal metadata
- Government/defense preferred format
- Best for: Legal teams, compliance audits, federal requirements

### Generating SBOMs

**With Trivy (CycloneDX or SPDX):**
```bash
# CycloneDX format (recommended for security)
trivy image --format cyclonedx --output sbom.json myapp:latest

# SPDX format (for compliance)
trivy image --format spdx-json --output sbom-spdx.json myapp:latest

# Scan SBOM (faster than re-scanning image)
trivy sbom sbom.json --severity HIGH,CRITICAL
```

**With Syft (high accuracy):**
```bash
# Generate CycloneDX
syft myapp:latest -o cyclonedx-json=sbom.json

# Generate SPDX
syft myapp:latest -o spdx-json=sbom-spdx.json

# Pipe to Grype for scanning
syft myapp:latest -o json | grype
```

For comprehensive SBOM patterns and storage strategies, see `references/sbom-guide.md`.

## Vulnerability Prioritization

Not all vulnerabilities require immediate action. Prioritize based on actual risk using CVSS, EPSS, and KEV.

### Modern Risk-Based Prioritization

**Step 1: Gather Metrics**

| Metric | Source | Purpose |
|--------|--------|---------|
| CVSS Base Score | NVD, vendor advisories | Vulnerability severity (0-10) |
| EPSS Score | FIRST.org API | Exploitation probability (0-1) |
| KEV Status | CISA KEV Catalog | Actively exploited CVEs |
| Asset Criticality | Internal CMDB | Business impact if compromised |
| Exposure | Network topology | Internet-facing vs. internal |

**Step 2: Calculate Priority**

```
Priority Score = (CVSS × 0.3) + (EPSS × 100 × 0.3) + (KEV × 50) + (Asset × 0.2) + (Exposure × 0.2)

KEV: 1 if in KEV catalog, 0 otherwise
Asset: 1 (Critical), 0.7 (High), 0.4 (Medium), 0.1 (Low)
Exposure: 1 (Internet-facing), 0.5 (Internal), 0.1 (Isolated)
```

**Step 3: Apply SLA Tiers**

| Priority | Criteria | SLA | Action |
|----------|----------|-----|--------|
| P0 - Critical | KEV + Internet-facing + Critical asset | 24 hours | Emergency patch immediately |
| P1 - High | CVSS ≥ 9.0 OR (CVSS ≥ 7.0 AND EPSS ≥ 0.1) | 7 days | Prioritize in sprint, patch ASAP |
| P2 - Medium | CVSS 7.0-8.9 OR EPSS ≥ 0.05 | 30 days | Normal sprint planning |
| P3 - Low | CVSS 4.0-6.9, EPSS < 0.05 | 90 days | Backlog, maintenance windows |
| P4 - Info | CVSS < 4.0 | No SLA | Track, address opportunistically |

**Example: Log4Shell (CVE-2021-44228)**
```
CVSS: 10.0
EPSS: 0.975 (97.5% exploitation probability)
KEV: Yes (CISA catalog)
Asset: Critical (payment API)
Exposure: Internet-facing

Priority Score = (10 × 0.3) + (97.5 × 0.3) + 50 + (1 × 0.2) + (1 × 0.2) = 82.65
Result: P0 - Critical (24-hour SLA)
```

For complete prioritization framework and automation scripts, see `references/prioritization-framework.md`.

## CI/CD Integration Patterns

### Multi-Stage Security Pipeline

Implement progressive security gates across pipeline stages:

**Stage 1: Pre-Commit (Developer Workstation)**
```yaml
Tools: Secret scanning (Gitleaks), SAST (Semgrep)
Threshold: Block high-confidence secrets, critical SAST findings
Speed: < 10 seconds
```

**Stage 2: Pull Request (CI Pipeline)**
```yaml
Tools: SAST, SCA, Secret scanning
Threshold: No Critical/High vulnerabilities, no secrets
Speed: < 5 minutes
Action: Block PR merge until fixed
```

**Stage 3: Build (CI Pipeline)**
```yaml
Tools: Container scanning (Trivy), SBOM generation
Threshold: No Critical vulnerabilities in production dependencies
Artifacts: SBOM stored, scan results uploaded
Speed: < 2 minutes
Action: Fail build on Critical findings
```

**Stage 4: Pre-Deployment (Staging)**
```yaml
Tools: DAST, Integration tests
Threshold: No Critical/High DAST findings
Speed: 10-30 minutes
Action: Gate deployment to production
```

**Stage 5: Production (Runtime)**
```yaml
Tools: Continuous scanning, runtime monitoring
Threshold: Alert on new CVEs in deployed images
Action: Alert security team, plan patching
```

### Example: GitHub Actions Multi-Stage Scan

```yaml
name: Security Scan Pipeline

on: [push, pull_request]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          extra_args: --only-verified

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: semgrep/semgrep-action@v1
        with:
          config: p/security-audit

  container:
    runs-on: ubuntu-latest
    needs: [secrets, sast]
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:${{ github.sha }} .

      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: 1

      - name: Generate SBOM
        run: |
          trivy image --format cyclonedx \
            --output sbom.json myapp:${{ github.sha }}

      - uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

For complete CI/CD patterns (GitLab CI, Jenkins, Azure Pipelines), see `references/ci-cd-patterns.md`.

## Container Scanning with Trivy

Trivy is the recommended default for container scanning: comprehensive, fast, and CI/CD native.

### Basic Usage

```bash
# Scan container image
trivy image alpine:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL alpine:latest

# Fail on findings (CI/CD)
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest

# Generate SBOM
trivy image --format cyclonedx --output sbom.json alpine:latest

# Scan filesystem
trivy fs /path/to/project

# Scan Kubernetes manifests
trivy config deployment.yaml
```

### Configuration (.trivy.yaml)

```yaml
severity: HIGH,CRITICAL
exit-code: 1
ignore-unfixed: true  # Only fail on fixable vulnerabilities
vuln-type: os,library
skip-dirs:
  - node_modules
  - vendor
ignorefile: .trivyignore
```

### Ignoring False Positives (.trivyignore)

```
# False positive
CVE-2023-12345

# Accepted risk with justification
CVE-2023-67890  # Risk accepted: Not exploitable in our use case

# Development dependency (not in production)
CVE-2023-11111  # Dev dependency only
```

### GitHub Actions Integration

```yaml
- name: Trivy Scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: HIGH,CRITICAL
    exit-code: 1

- name: Upload to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  if: always()
  with:
    sarif_file: trivy-results.sarif
```

## Alternative: Grype for Accuracy

Grype focuses on minimal false positives and works with Syft for SBOM generation.

**Important:** Use Grype v0.104.1 or later (credential disclosure CVE-2025-65965 patched in earlier versions).

### Basic Usage

```bash
# Scan container image
grype alpine:latest

# Scan with severity threshold
grype alpine:latest --fail-on high

# Scan SBOM (faster)
grype sbom:./sbom.json

# Syft + Grype workflow
syft alpine:latest -o json | grype --fail-on critical
```

### When to Use Grype

- Projects sensitive to false positives
- SBOM-first workflows (generate with Syft, scan with Grype)
- Need second opinion validation
- Anchore ecosystem users

For complete tool comparisons and selection criteria, see `references/tool-selection.md`.

## Security Gates and Thresholds

### Progressive Threshold Strategy

Balance security and development velocity with progressive gates. Configure different thresholds for PR checks (fast, HIGH+CRITICAL), builds (comprehensive), and deployments (strict, CRITICAL only).

### Policy-as-Code

Use OPA (Open Policy Agent) for automated policy enforcement. Create policies to deny Critical vulnerabilities, enforce KEV catalog checks, and implement environment-specific rules.

For complete policy patterns, baseline detection, and OPA examples, see `references/policy-as-code.md`.

## Remediation Workflows

### Automated Remediation

Set up automated workflows to scan daily, extract fixable vulnerabilities, update dependencies, and create remediation pull requests automatically.

### SLA Tracking

Track vulnerability remediation against SLA targets (P0: 24 hours, P1: 7 days, P2: 30 days, P3: 90 days). Monitor overdue vulnerabilities and escalate as needed.

### False Positive Management

Maintain suppression files (.trivyignore) with documented justifications, review dates, and approval tracking. Implement workflows for false positive triage and approval.

For complete remediation workflows, SLA trackers, and automation scripts, see `references/remediation-workflows.md`.

## Integration with Related Skills

**building-ci-pipelines**
- Add security stages to pipeline definitions
- Configure artifacts for SBOM storage
- Implement quality gates with vulnerability thresholds

**secret-management**
- Integrate secret scanning (Gitleaks, TruffleHog)
- Automate secret rotation on detection
- Use pre-commit hooks for prevention

**infrastructure-as-code**
- Scan Terraform and Kubernetes manifests with Trivy config
- Detect misconfigurations before deployment
- Enforce policy-as-code with OPA

**security-hardening**
- Apply remediation guidance from scan results
- Select secure base images
- Implement security best practices

**compliance-frameworks**
- Generate SBOMs for SOC2, ISO 27001 audits
- Track vulnerability metrics for compliance reporting
- Provide evidence for security controls

## Quick Reference

### Essential Commands

```bash
# Trivy: Scan image with severity filter
trivy image --severity HIGH,CRITICAL myapp:latest

# Trivy: Generate SBOM
trivy image --format cyclonedx --output sbom.json myapp:latest

# Trivy: Scan SBOM
trivy sbom sbom.json

# Grype: Scan image
grype myapp:latest --fail-on high

# Syft + Grype: SBOM workflow
syft myapp:latest -o json | grype

# Gitleaks: Scan for secrets
gitleaks detect --source . --verbose
```

### Common Patterns

```bash
# CI/CD: Fail build on Critical
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed --severity HIGH,CRITICAL myapp:latest

# Scan only OS packages
trivy image --vuln-type os myapp:latest

# Skip specific directories
trivy fs --skip-dirs node_modules,vendor .
```

## Progressive Disclosure

This skill provides foundational vulnerability management patterns. For deeper topics:

- **Tool Selection:** `references/tool-selection.md` - Complete decision frameworks
- **SBOM Patterns:** `references/sbom-guide.md` - Generation, storage, consumption
- **Prioritization:** `references/prioritization-framework.md` - CVSS/EPSS/KEV automation
- **CI/CD Integration:** `references/ci-cd-patterns.md` - GitLab CI, Jenkins, Azure Pipelines
- **Remediation:** `references/remediation-workflows.md` - SLA tracking, false positives
- **Policy-as-Code:** `references/policy-as-code.md` - OPA examples, security gates

**Working Examples:**
- `examples/trivy/` - Trivy scanning patterns
- `examples/grype/` - Grype + Syft workflows
- `examples/ci-cd/` - Complete pipeline configurations
- `examples/sbom/` - SBOM generation and management
- `examples/prioritization/` - EPSS and KEV integration scripts

**Automation Scripts:**
- `scripts/vulnerability-report.sh` - Generate executive reports
- `scripts/sla-tracker.sh` - Track remediation SLAs
- `scripts/false-positive-manager.sh` - Manage suppression rules
