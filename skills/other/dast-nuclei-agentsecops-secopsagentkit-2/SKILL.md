---
name: dast-nuclei
description: >
  Fast, template-based vulnerability scanning using ProjectDiscovery's Nuclei with extensive community
  templates covering CVEs, OWASP Top 10, misconfigurations, and security issues across web applications,
  APIs, and infrastructure. Use when: (1) Performing rapid vulnerability scanning with automated CVE
  detection, (2) Testing for known vulnerabilities and security misconfigurations in web apps and APIs,
  (3) Running template-based security checks in CI/CD pipelines with customizable severity thresholds,
  (4) Creating custom security templates for organization-specific vulnerability patterns, (5) Scanning
  multiple targets efficiently with concurrent execution and rate limiting controls.
version: 0.1.0
maintainer: SirAppSec
category: appsec
tags: [dast, nuclei, vulnerability-scanning, cve, owasp, api-testing, automation, templates]
frameworks: [OWASP, CWE, CVE]
dependencies:
  tools: [nuclei]
  optional: [docker, git]
references:
  - https://docs.projectdiscovery.io/tools/nuclei/overview
  - https://github.com/projectdiscovery/nuclei
  - https://github.com/projectdiscovery/nuclei-templates
---

# DAST with Nuclei

## Overview

Nuclei is a fast, template-based vulnerability scanner from ProjectDiscovery that uses YAML templates to detect
security vulnerabilities, misconfigurations, and exposures across web applications, APIs, networks, and cloud
infrastructure. With 7,000+ community templates covering CVEs, OWASP vulnerabilities, and custom checks, Nuclei
provides efficient automated security testing with minimal false positives.

## Quick Start

### Installation

```bash
# Install via Go
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Or using Docker
docker pull projectdiscovery/nuclei:latest

# Update templates (automatically downloads 7000+ community templates)
nuclei -update-templates
```

### Basic Vulnerability Scan

```bash
# Scan single target with all templates
nuclei -u https://target-app.com

# Scan with specific severity levels
nuclei -u https://target-app.com -severity critical,high

# Scan multiple targets from file
nuclei -list targets.txt -severity critical,high,medium -o results.txt
```

### Quick CVE Scan

```bash
# Scan for specific CVEs
nuclei -u https://target-app.com -tags cve -severity critical,high

# Scan for recent CVEs
nuclei -u https://target-app.com -tags cve -severity critical -template-condition "contains(id, 'CVE-')"
```

## Core Workflow

### Workflow Checklist

Progress:
[ ] 1. Install Nuclei and update templates to latest version
[ ] 2. Define target scope (URLs, domains, IP ranges)
[ ] 3. Select appropriate templates based on target type and risk tolerance
[ ] 4. Configure scan parameters (rate limiting, severity, concurrency)
[ ] 5. Execute scan with proper authentication if needed
[ ] 6. Review findings, filter false positives, and verify vulnerabilities
[ ] 7. Map findings to OWASP/CWE frameworks
[ ] 8. Generate security report with remediation guidance

Work through each step systematically. Check off completed items.

### Step 1: Template Selection and Target Scoping

Identify target applications and select relevant template categories:

```bash
# List available template categories
nuclei -tl

# List templates by tag
nuclei -tl -tags owasp
nuclei -tl -tags cve,misconfig

# Show template statistics
nuclei -tl -tags cve -severity critical | wc -l
```

**Template Categories:**
- **cve**: Known CVE vulnerabilities (7000+ CVE templates)
- **owasp**: OWASP Top 10 vulnerabilities
- **misconfig**: Common security misconfigurations
- **exposed-panels**: Admin panels and login pages
- **takeovers**: Subdomain takeover vulnerabilities
- **default-logins**: Default credentials
- **exposures**: Sensitive file and data exposures
- **tech**: Technology detection and fingerprinting

**Target Scoping Best Practices:**
- Create target list excluding third-party services
- Group targets by application type for focused scanning
- Define exclusions for sensitive endpoints (payment, logout, delete actions)

### Step 2: Configure Scan Parameters

Set appropriate rate limiting and concurrency for target environment:

```bash
# Conservative scan (avoid overwhelming target)
nuclei -u https://target-app.com \
  -severity critical,high \
  -rate-limit 50 \
  -concurrency 10 \
  -timeout 10

# Aggressive scan (faster, higher load)
nuclei -u https://target-app.com \
  -severity critical,high,medium \
  -rate-limit 150 \
  -concurrency 25 \
  -bulk-size 25
```

**Parameter Guidelines:**
- **rate-limit**: Requests per second (50-150 typical, lower for production)
- **concurrency**: Parallel template execution (10-25 typical)
- **bulk-size**: Parallel host scanning (10-25 for multiple targets)
- **timeout**: Per-request timeout in seconds (10-30 typical)

For CI/CD integration patterns, see `scripts/nuclei_ci.sh`.

### Step 3: Execute Targeted Scans

Run scans based on security objectives:

**Critical Vulnerability Scan:**
```bash
# Focus on critical and high severity issues
nuclei -u https://target-app.com \
  -severity critical,high \
  -tags cve,owasp \
  -o critical-findings.txt \
  -json -jsonl-export critical-findings.jsonl
```

**Technology-Specific Scan:**
```bash
# Scan specific technology stack
nuclei -u https://target-app.com -tags apache,nginx,wordpress,drupal

# Scan for exposed sensitive files
nuclei -u https://target-app.com -tags exposure,config

# Scan for authentication issues
nuclei -u https://target-app.com -tags auth,login,default-logins
```

**API Security Scan:**
```bash
# API-focused security testing
nuclei -u https://api.target.com \
  -tags api,graphql,swagger \
  -severity critical,high,medium \
  -header "Authorization: Bearer $API_TOKEN"
```

**Custom Template Scan:**
```bash
# Scan with organization-specific templates
nuclei -u https://target-app.com \
  -t custom-templates/ \
  -t nuclei-templates/http/cves/ \
  -severity critical,high
```

### Step 4: Authenticated Scanning

Perform authenticated scans for complete coverage:

```bash
# Scan with authentication headers
nuclei -u https://target-app.com \
  -header "Authorization: Bearer $AUTH_TOKEN" \
  -header "Cookie: session=$SESSION_COOKIE" \
  -tags cve,owasp

# Scan with custom authentication using bundled script
python3 scripts/nuclei_auth_scan.py \
  --target https://target-app.com \
  --auth-type bearer \
  --token-env AUTH_TOKEN \
  --severity critical,high \
  --output auth-scan-results.jsonl
```

For OAuth, SAML, and MFA scenarios, see `references/authentication_patterns.md`.

### Step 5: Results Analysis and Validation

Review findings and eliminate false positives:

```bash
# Parse JSON output for high-level summary
python3 scripts/parse_nuclei_results.py \
  --input critical-findings.jsonl \
  --output report.html \
  --group-by severity

# Filter and verify findings
nuclei -u https://target-app.com \
  -tags cve \
  -severity critical \
  -verify \
  -verbose
```

**Validation Workflow:**
1. Review critical findings first (immediate action required)
2. Verify each finding manually (curl, browser inspection, PoC testing)
3. Check for false positives using `references/false_positive_guide.md`
4. Map confirmed vulnerabilities to OWASP Top 10 using `references/owasp_mapping.md`
5. Cross-reference with CWE classifications for remediation patterns

**Feedback Loop Pattern:**
```bash
# 1. Initial scan
nuclei -u https://target-app.com -severity critical,high -o scan1.txt

# 2. Apply fixes to identified vulnerabilities

# 3. Re-scan to verify remediation
nuclei -u https://target-app.com -severity critical,high -o scan2.txt

# 4. Compare results to ensure vulnerabilities are resolved
diff scan1.txt scan2.txt
```

### Step 6: Reporting and Remediation Tracking

Generate comprehensive security reports:

```bash
# Generate detailed report with OWASP/CWE mappings
python3 scripts/nuclei_report_generator.py \
  --input scan-results.jsonl \
  --output security-report.html \
  --format html \
  --include-remediation \
  --map-frameworks owasp,cwe

# Export to SARIF for GitHub Security tab
nuclei -u https://target-app.com \
  -severity critical,high \
  -sarif-export github-sarif.json
```

See `assets/report_templates/` for customizable report formats.

## Automation & CI/CD Integration

### GitHub Actions Integration

```yaml
# .github/workflows/nuclei-scan.yml
name: Nuclei Security Scan
on: [push, pull_request]

jobs:
  nuclei:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Nuclei Scan
        uses: projectdiscovery/nuclei-action@main
        with:
          target: https://staging.target-app.com
          severity: critical,high
          templates: cves,owasp,misconfig

      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: nuclei.sarif
```

### Docker-Based CI/CD Scanning

```bash
# Run in CI/CD pipeline with Docker
docker run --rm \
  -v $(pwd):/reports \
  projectdiscovery/nuclei:latest \
  -u $TARGET_URL \
  -severity critical,high \
  -json -jsonl-export /reports/nuclei-results.jsonl

# Check exit code and fail build on critical findings
if grep -q '"severity":"critical"' nuclei-results.jsonl; then
  echo "Critical vulnerabilities detected!"
  exit 1
fi
```

### Advanced Automation with Custom Scripts

```bash
# Automated multi-target scanning with parallel execution
./scripts/nuclei_bulk_scanner.sh \
  --targets-file production-apps.txt \
  --severity critical,high \
  --slack-webhook $SLACK_WEBHOOK \
  --output-dir scan-reports/

# Scheduled vulnerability monitoring
./scripts/nuclei_scheduler.sh \
  --schedule daily \
  --targets targets.txt \
  --diff-mode \
  --alert-on new-findings
```

For complete CI/CD integration examples, see `scripts/ci_integration_examples/`.

## Custom Template Development

Create organization-specific security templates:

```yaml
# custom-templates/api-key-exposure.yaml
id: custom-api-key-exposure
info:
  name: Custom API Key Exposure Check
  author: security-team
  severity: high
  description: Detects exposed API keys in custom application endpoints
  tags: api,exposure,custom

http:
  - method: GET
    path:
      - "{{BaseURL}}/api/v1/config"
      - "{{BaseURL}}/.env"

    matchers-condition: and
    matchers:
      - type: word
        words:
          - "api_key"
          - "secret_key"

      - type: status
        status:
          - 200

    extractors:
      - type: regex
        name: api_key
        regex:
          - 'api_key["\s:=]+([a-zA-Z0-9_-]{32,})'
```

**Template Development Resources:**
- `references/template_development.md` - Complete template authoring guide
- `assets/template_examples/` - Sample templates for common patterns
- [Nuclei Template Guide](https://docs.projectdiscovery.io/templates/introduction)

## Security Considerations

- **Authorization**: Obtain explicit written permission before scanning any systems not owned by your organization
- **Rate Limiting**: Configure appropriate rate limits to avoid overwhelming target applications or triggering DDoS protections
- **Production Safety**: Use conservative scan parameters (rate-limit 50, concurrency 10) for production environments
- **Sensitive Data**: Scan results may contain sensitive URLs, parameters, and application details - sanitize before sharing
- **False Positives**: Manually verify all critical and high severity findings before raising security incidents
- **Access Control**: Restrict access to scan results and templates containing organization-specific vulnerability patterns
- **Audit Logging**: Log all scan executions, targets, findings severity, and remediation actions for compliance
- **Legal Compliance**: Adhere to computer fraud and abuse laws; unauthorized scanning may violate laws
- **Credentials Management**: Never hardcode credentials in templates; use environment variables or secrets management
- **Scope Validation**: Double-check target lists to avoid scanning third-party or out-of-scope systems

## Bundled Resources

### Scripts (`scripts/`)

- `nuclei_ci.sh` - CI/CD integration wrapper with exit code handling and artifact generation
- `nuclei_auth_scan.py` - Authenticated scanning with multiple authentication methods (Bearer, API key, Cookie)
- `nuclei_bulk_scanner.sh` - Parallel scanning of multiple targets with aggregated reporting
- `nuclei_scheduler.sh` - Scheduled scanning with diff detection and alerting
- `parse_nuclei_results.py` - JSON/JSONL parser for generating HTML/CSV reports with severity grouping
- `nuclei_report_generator.py` - Comprehensive report generator with OWASP/CWE mappings and remediation guidance
- `template_validator.py` - Custom template validation and testing framework

### References (`references/`)

- `owasp_mapping.md` - OWASP Top 10 mapping for Nuclei findings
- `template_development.md` - Custom template authoring guide
- `authentication_patterns.md` - Advanced authentication patterns (OAuth, SAML, MFA)
- `false_positive_guide.md` - False positive identification and handling

### Assets (`assets/`)

- `github_actions.yml` - GitHub Actions workflow with SARIF export
- `nuclei_config.yaml` - Comprehensive configuration template

## Common Patterns

### Pattern 1: Progressive Severity Scanning

Start with critical vulnerabilities and progressively expand scope:

```bash
# Stage 1: Critical vulnerabilities only (fast)
nuclei -u https://target-app.com -severity critical -o critical.txt

# Stage 2: High severity if critical issues found
if [ -s critical.txt ]; then
  nuclei -u https://target-app.com -severity high -o high.txt
fi

# Stage 3: Medium/Low for comprehensive assessment
nuclei -u https://target-app.com -severity medium,low -o all-findings.txt
```

### Pattern 2: Technology-Specific Scanning

Focus on known technology stack vulnerabilities:

```bash
# 1. Identify technologies
nuclei -u https://target-app.com -tags tech -o tech-detected.txt

# 2. Parse detected technologies
TECHS=$(grep -oP 'matched at \K\w+' tech-detected.txt | sort -u)

# 3. Scan for technology-specific vulnerabilities
for tech in $TECHS; do
  nuclei -u https://target-app.com -tags $tech -severity critical,high -o vulns-$tech.txt
done
```

### Pattern 3: Multi-Stage API Security Testing

Comprehensive API security assessment:

```bash
# Stage 1: API discovery and fingerprinting
nuclei -u https://api.target.com -tags api,swagger,graphql -o api-discovery.txt

# Stage 2: Authentication testing
nuclei -u https://api.target.com -tags auth,jwt,oauth -o api-auth.txt

# Stage 3: Known API CVEs
nuclei -u https://api.target.com -tags api,cve -severity critical,high -o api-cves.txt

# Stage 4: Business logic testing with custom templates
nuclei -u https://api.target.com -t custom-templates/api/ -o api-custom.txt
```

### Pattern 4: Continuous Security Monitoring

```bash
# Daily scan with diff detection
nuclei -u https://production-app.com \
  -severity critical,high -tags cve \
  -json -jsonl-export scan-$(date +%Y%m%d).jsonl

# Use bundled scripts for diff analysis and alerting
```

## Integration Points

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps, Travis CI
- **Issue Tracking**: Jira, GitHub Issues, ServiceNow, Linear (via SARIF or custom scripts)
- **Security Platforms**: Defect Dojo, Splunk, ELK Stack, SIEM platforms (via JSON export)
- **Notification**: Slack, Microsoft Teams, Discord, PagerDuty, email (via webhook scripts)
- **SDLC**: Pre-deployment scanning, security regression testing, vulnerability monitoring
- **Cloud Platforms**: AWS Lambda, Google Cloud Functions, Azure Functions (serverless scanning)
- **Reporting**: HTML, JSON, JSONL, SARIF, Markdown, CSV formats

## Troubleshooting

Common issues and solutions:

- **Too Many False Positives**: Filter by severity (`-severity critical,high`), exclude tags (`-etags tech,info`). See `references/false_positive_guide.md`
- **Incomplete Coverage**: Verify templates loaded (`nuclei -tl | wc -l`), update templates (`nuclei -update-templates`)
- **Rate Limiting/WAF**: Reduce aggressiveness (`-rate-limit 20 -concurrency 5 -timeout 15`)
- **High Resource Usage**: Reduce parallelism (`-concurrency 5 -bulk-size 5`)
- **Auth Headers Not Working**: Debug with `-debug`, verify token format, see `references/authentication_patterns.md`

## References

- [Nuclei Documentation](https://docs.projectdiscovery.io/tools/nuclei/overview)
- [Nuclei Templates Repository](https://github.com/projectdiscovery/nuclei-templates)
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Database](https://cwe.mitre.org/)
