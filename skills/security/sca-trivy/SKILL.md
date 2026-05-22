---
name: sca-trivy
description: >
  Software Composition Analysis (SCA) and container vulnerability scanning using Aqua Trivy
  for identifying CVE vulnerabilities in dependencies, container images, IaC misconfigurations,
  and license compliance risks. Use when: (1) Scanning container images and filesystems for
  vulnerabilities and misconfigurations, (2) Analyzing dependencies for known CVEs across
  multiple languages (Go, Python, Node.js, Java, etc.), (3) Detecting IaC security issues
  in Terraform, Kubernetes, Dockerfile, (4) Integrating vulnerability scanning into CI/CD
  pipelines with SARIF output, (5) Generating Software Bill of Materials (SBOM) in CycloneDX
  or SPDX format, (6) Prioritizing remediation by CVSS score and exploitability.
version: 0.1.0
maintainer: SirAppSec
category: devsecops
tags: [sca, trivy, container-security, vulnerability-scanning, sbom, iac-security, dependency-scanning, cvss]
frameworks: [OWASP, CWE, NIST, PCI-DSS, SOC2]
dependencies:
  tools: [trivy, docker]
references:
  - https://aquasecurity.github.io/trivy/
  - https://owasp.org/www-project-dependency-check/
  - https://nvd.nist.gov/
  - https://www.cisa.gov/sbom
---

# Software Composition Analysis with Trivy

## Overview

Trivy is a comprehensive security scanner for containers, filesystems, and git repositories. It detects
vulnerabilities (CVEs) in OS packages and application dependencies, IaC misconfigurations, exposed secrets,
and software licenses. This skill provides workflows for vulnerability scanning, SBOM generation, CI/CD
integration, and remediation prioritization aligned with CVSS and OWASP standards.

## Quick Start

Scan a container image for vulnerabilities:

```bash
# Install Trivy
brew install trivy  # macOS
# or: apt-get install trivy  # Debian/Ubuntu
# or: docker pull aquasec/trivy:latest

# Scan container image
trivy image nginx:latest

# Scan local filesystem for dependencies
trivy fs .

# Scan IaC files for misconfigurations
trivy config .

# Generate SBOM
trivy image --format cyclonedx --output sbom.json nginx:latest
```

## Core Workflows

### Workflow 1: Container Image Security Assessment

Progress:
[ ] 1. Identify target container image (repository:tag)
[ ] 2. Run comprehensive Trivy scan with `trivy image <image-name>`
[ ] 3. Analyze vulnerability findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
[ ] 4. Map CVE findings to CWE categories and OWASP references
[ ] 5. Check for available patches and updated base images
[ ] 6. Generate prioritized remediation report with upgrade recommendations

Work through each step systematically. Check off completed items.

### Workflow 2: Dependency Vulnerability Scanning

Scan project dependencies for known vulnerabilities:

```bash
# Scan filesystem for all dependencies
trivy fs --severity CRITICAL,HIGH .

# Scan specific package manifest
trivy fs --scanners vuln package-lock.json

# Generate JSON report for analysis
trivy fs --format json --output trivy-report.json .

# Generate SARIF for GitHub/GitLab integration
trivy fs --format sarif --output trivy.sarif .
```

For each vulnerability:
1. Review CVE details and CVSS score
2. Check if fixed version is available
3. Consult `references/remediation_guide.md` for language-specific guidance
4. Update dependency to patched version
5. Re-scan to validate fix

### Workflow 3: Infrastructure as Code Security

Detect misconfigurations in IaC files:

```bash
# Scan Terraform configurations
trivy config ./terraform --severity CRITICAL,HIGH

# Scan Kubernetes manifests
trivy config ./k8s --severity CRITICAL,HIGH

# Scan Dockerfile best practices
trivy config --file-patterns dockerfile:Dockerfile .

# Generate report with remediation guidance
trivy config --format json --output iac-findings.json .
```

Review findings by category:
- **Security**: Authentication, authorization, encryption
- **Compliance**: CIS benchmarks, security standards
- **Best Practices**: Resource limits, immutability, least privilege

### Workflow 4: CI/CD Pipeline Integration

#### GitHub Actions

```yaml
name: Trivy Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

#### GitLab CI

```yaml
trivy-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 1 --severity CRITICAL,HIGH --format json --output trivy-report.json .
  artifacts:
    reports:
      dependency_scanning: trivy-report.json
    when: always
  allow_failure: false
```

Use bundled templates from `assets/ci_integration/` for additional platforms.

### Workflow 5: SBOM Generation

Generate Software Bill of Materials for supply chain transparency:

```bash
# Generate CycloneDX SBOM
trivy image --format cyclonedx --output sbom-cyclonedx.json nginx:latest

# Generate SPDX SBOM
trivy image --format spdx-json --output sbom-spdx.json nginx:latest

# SBOM for filesystem/project
trivy fs --format cyclonedx --output project-sbom.json .
```

SBOM use cases:
- **Vulnerability tracking**: Monitor dependencies for new CVEs
- **License compliance**: Identify license obligations and risks
- **Supply chain security**: Verify component provenance
- **Regulatory compliance**: Meet CISA SBOM requirements

## Security Considerations

### Sensitive Data Handling

- **Registry credentials**: Use environment variables or credential helpers, never hardcode
- **Scan reports**: Contain vulnerability details and package versions - treat as sensitive
- **SBOM files**: May reveal internal architecture - control access appropriately
- **Secret scanning**: Enable with `--scanners secret` to detect exposed credentials in images

### Access Control

- **Container registry access**: Requires pull permissions for image scanning
- **Filesystem access**: Read permissions for dependency manifests and IaC files
- **CI/CD integration**: Secure API tokens and registry credentials in secrets management
- **Report storage**: Restrict access to vulnerability reports and SBOM artifacts

### Audit Logging

Log the following for compliance and incident response:
- Scan execution timestamps and scope (image, filesystem, repository)
- Vulnerability counts by severity level
- Policy violations and blocking decisions
- SBOM generation and distribution events
- Remediation actions and version updates

### Compliance Requirements

- **PCI-DSS 6.2**: Ensure system components protected from known vulnerabilities
- **SOC2 CC7.1**: Detect and act upon changes that could affect security
- **NIST 800-53 SI-2**: Flaw remediation and vulnerability scanning
- **CIS Benchmarks**: Container and Kubernetes security hardening
- **OWASP Top 10 A06**: Vulnerable and Outdated Components
- **CWE-1104**: Use of Unmaintained Third-Party Components

## Bundled Resources

### Scripts (`scripts/`)

- `trivy_scan.py` - Comprehensive scanning with JSON/SARIF output and severity filtering
- `sbom_generator.py` - SBOM generation with CycloneDX and SPDX format support
- `vulnerability_report.py` - Parse Trivy output and generate remediation reports with CVSS scores
- `baseline_manager.py` - Baseline creation for tracking new vulnerabilities only

### References (`references/`)

- `scanner_types.md` - Detailed guide for vulnerability, misconfiguration, secret, and license scanning
- `remediation_guide.md` - Language and ecosystem-specific remediation strategies
- `cvss_prioritization.md` - CVSS score interpretation and vulnerability prioritization framework
- `iac_checks.md` - Complete list of IaC security checks with CIS benchmark mappings

### Assets (`assets/`)

- `trivy.yaml` - Custom Trivy configuration with security policies and ignore rules
- `ci_integration/github-actions.yml` - Complete GitHub Actions workflow with security gates
- `ci_integration/gitlab-ci.yml` - Complete GitLab CI pipeline with dependency scanning
- `ci_integration/jenkins.groovy` - Jenkins pipeline with Trivy integration
- `policy_template.rego` - OPA policy template for custom vulnerability policies

## Common Patterns

### Pattern 1: Multi-Stage Security Scanning

Comprehensive security assessment combining multiple scan types:

```bash
# 1. Scan container image for vulnerabilities
trivy image --severity CRITICAL,HIGH myapp:latest

# 2. Scan IaC for misconfigurations
trivy config ./infrastructure --severity CRITICAL,HIGH

# 3. Scan filesystem for dependency vulnerabilities
trivy fs --severity CRITICAL,HIGH ./app

# 4. Scan for exposed secrets
trivy fs --scanners secret ./app

# 5. Generate comprehensive SBOM
trivy image --format cyclonedx --output sbom.json myapp:latest
```

### Pattern 2: Baseline Vulnerability Tracking

Implement baseline scanning to track only new vulnerabilities:

```bash
# Initial scan - create baseline
trivy image --format json --output baseline.json nginx:latest

# Subsequent scans - detect new vulnerabilities
trivy image --format json --output current.json nginx:latest
./scripts/baseline_manager.py --baseline baseline.json --current current.json
```

### Pattern 3: License Compliance Scanning

Detect license compliance risks:

```bash
# Scan for license information
trivy image --scanners license --format json --output licenses.json myapp:latest

# Filter by license type
trivy image --scanners license --severity HIGH,CRITICAL myapp:latest
```

Review findings:
- **High Risk**: GPL, AGPL (strong copyleft)
- **Medium Risk**: LGPL, MPL (weak copyleft)
- **Low Risk**: Apache, MIT, BSD (permissive)

### Pattern 4: Custom Policy Enforcement

Apply custom security policies with OPA:

```bash
# Create Rego policy in assets/policy_template.rego
# Deny images with CRITICAL vulnerabilities or outdated packages

# Run scan with policy enforcement
trivy image --format json --output scan.json myapp:latest
trivy image --ignore-policy assets/policy_template.rego myapp:latest
```

## Integration Points

### CI/CD Integration

- **GitHub Actions**: Native `aquasecurity/trivy-action` with SARIF upload to Security tab
- **GitLab CI**: Dependency scanning report format for Security Dashboard
- **Jenkins**: Docker-based scanning with JUnit XML report generation
- **CircleCI**: Docker executor with artifact storage
- **Azure Pipelines**: Task-based integration with results publishing

### Container Platforms

- **Docker**: Image scanning before push to registry
- **Kubernetes**: Admission controllers with trivy-operator for runtime scanning
- **Harbor**: Built-in Trivy integration for registry scanning
- **AWS ECR**: Scan images on push with enhanced scanning
- **Google Artifact Registry**: Vulnerability scanning integration

### Security Tools Ecosystem

- **SIEM Integration**: Export JSON findings to Splunk, ELK, or Datadog
- **Vulnerability Management**: Import SARIF/JSON into Snyk, Qualys, or Rapid7
- **SBOM Tools**: CycloneDX and SPDX compatibility with dependency-track and GUAC
- **Policy Enforcement**: OPA/Rego integration for custom policy as code

## Troubleshooting

### Issue: High False Positive Rate

**Symptoms**: Many vulnerabilities reported that don't apply to your use case

**Solution**:
1. Use `.trivyignore` file to suppress specific CVEs with justification
2. Filter by exploitability: `trivy image --ignore-unfixed myapp:latest`
3. Apply severity filtering: `--severity CRITICAL,HIGH`
4. Review vendor-specific security advisories for false positive validation
5. See `references/false_positives.md` for common patterns

### Issue: Performance Issues on Large Images

**Symptoms**: Scans taking excessive time or high memory usage

**Solution**:
1. Use cached DB: `trivy image --cache-dir /path/to/cache myapp:latest`
2. Skip unnecessary scanners: `--scanners vuln` (exclude config, secret)
3. Use offline mode after initial DB download: `--offline-scan`
4. Increase timeout: `--timeout 30m`
5. Scan specific layers: `--removed-pkgs` to exclude removed packages

### Issue: Missing Vulnerabilities for Specific Languages

**Symptoms**: Expected CVEs not detected in application dependencies

**Solution**:
1. Verify language support: Check supported languages and file patterns
2. Ensure dependency manifests are present (package.json, go.mod, requirements.txt)
3. Include lock files for accurate version detection
4. For compiled binaries, scan source code separately
5. Consult `references/scanner_types.md` for language-specific requirements

### Issue: Registry Authentication Failures

**Symptoms**: Unable to scan private container images

**Solution**:
```bash
# Use Docker credential helper
docker login registry.example.com
trivy image registry.example.com/private/image:tag

# Or use environment variables
export TRIVY_USERNAME=user
export TRIVY_PASSWORD=pass
trivy image registry.example.com/private/image:tag

# Or use credential file
trivy image --username user --password pass registry.example.com/private/image:tag
```

## Advanced Configuration

### Custom Trivy Configuration

Create `trivy.yaml` configuration file:

```yaml
# trivy.yaml
vulnerability:
  type: os,library
severity: CRITICAL,HIGH,MEDIUM
ignorefile: .trivyignore
ignore-unfixed: false
skip-files:
  - "test/**"
  - "**/node_modules/**"

cache:
  dir: /tmp/trivy-cache

db:
  repository: ghcr.io/aquasecurity/trivy-db:latest

output:
  format: json
  severity-sort: true
```

Use with: `trivy image --config trivy.yaml myapp:latest`

### Trivy Ignore File

Create `.trivyignore` to suppress specific CVEs:

```
# .trivyignore
# False positive - patched in vendor fork
CVE-0000-12345

# Risk accepted by security team - JIRA-1234
CVE-0000-67890

# No fix available, compensating controls in place
CVE-0000-11111
```

### Offline Air-Gapped Scanning

For air-gapped environments:

```bash
# On internet-connected machine:
trivy image --download-db-only --cache-dir /path/to/db

# Transfer cache to air-gapped environment

# On air-gapped machine:
trivy image --skip-db-update --cache-dir /path/to/db --offline-scan myapp:latest
```

## References

- [Trivy Official Documentation](https://aquasecurity.github.io/trivy/)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [NVD - National Vulnerability Database](https://nvd.nist.gov/)
- [CISA SBOM Guidelines](https://www.cisa.gov/sbom)
- [CWE-1104: Use of Unmaintained Third-Party Components](https://cwe.mitre.org/data/definitions/1104.html)
- [OWASP Top 10 - Vulnerable and Outdated Components](https://owasp.org/Top10/)
