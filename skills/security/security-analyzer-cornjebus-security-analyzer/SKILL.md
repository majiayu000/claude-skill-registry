---
name: security-analyzer
description: Comprehensive security vulnerability analysis for codebases and infrastructure. Scans dependencies (npm, pip, gem, go, cargo), containers (Docker, Kubernetes), cloud IaC (Terraform, CloudFormation), and detects secrets exposure. Fetches live CVE data from OSV.dev, calculates risk scores, and generates phased remediation plans with TDD validation tests. Use when users mention security scan, vulnerability, CVE, exploit, security audit, penetration test, OWASP, hardening, dependency audit, container security, or want to improve security posture.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Security Analyzer

Analyze environments for vulnerabilities, fetch current CVE/exploit data, and generate phased remediation plans with TDD validation.

## Quick Start

When the user requests a security scan:

1. Run environment discovery: `python .claude/skills/security-analyzer/scripts/discover_env.py .`
2. Save output to `inventory.json`
3. Run vulnerability scan: `python .claude/skills/security-analyzer/scripts/fetch_vulns.py inventory.json`
4. Save output to `scan_results.json`
5. Generate reports: `python .claude/skills/security-analyzer/scripts/generate_report.py scan_results.json inventory.json`

## Workflow

### Phase 1: Environment Discovery

Scan working directory for:
- **Dependencies**: `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, `pom.xml`
- **Containers**: `Dockerfile`, `docker-compose.yml`, `kubernetes/*.yaml`
- **Cloud IaC**: `terraform/*.tf`, `cloudformation/*.yaml`, `*.bicep`
- **Secrets**: `.env*` files (flag exposure risk, never log values)

Run the discovery script:
```bash
python .claude/skills/security-analyzer/scripts/discover_env.py /path/to/project > inventory.json
```

### Phase 2: Vulnerability Intelligence

Fetch current threat data using the vulnerability scanner:

```bash
python .claude/skills/security-analyzer/scripts/fetch_vulns.py inventory.json > scan_results.json
```

| Source | Priority | Use For |
|--------|----------|---------|
| CISA KEV | 1 | Actively exploited vulns (use WebSearch) |
| NVD | 2 | CVE details + CVSS scores (use WebSearch) |
| GitHub Advisories | 3 | Package-specific vulns (use WebSearch) |
| OSV.dev | 4 | Open source vulns (API in script) |

For CISA KEV and additional context, supplement with:
```
WebSearch: "CVE-XXXX-YYYY CISA KEV exploit"
```

### Phase 3: Risk Scoring

The scanner calculates risk scores using:

```
Risk = (CVSS * 0.3) + (Exploitability * 0.3) + (Criticality * 0.2) + (Exposure * 0.2)

Exploitability: 10=CISA KEV, 7=public exploit, 3=theoretical
Criticality: 10=auth/payment, 5=core business, 2=logging
Exposure: 10=internet-facing, 5=internal, 2=air-gapped
```

### Phase 4: Phased Remediation

Generate reports with fix commands and validation tests:

```bash
python .claude/skills/security-analyzer/scripts/generate_report.py scan_results.json inventory.json
```

Each finding includes:
1. Vulnerability details + risk score
2. Actual fix code/patch (not just recommendations)
3. Pre-fix test (proves vuln exists)
4. Remediation unit tests (tests the fix code)
5. Post-fix validation (proves vuln resolved)

### Phase 5: Reports

Output two reports:
- `security-report-technical.md` — Full details for engineers
- `security-report-executive.md` — Summary for leadership

See `references/report-templates.md` for output structure.

## TDD Pattern

For each vulnerability, generate three test types:

```python
def test_vuln_exists():
    """PASS before fix, FAIL after"""
    assert is_vulnerable("component") == True

def test_fix_works():
    """Unit test for remediation code"""
    result = apply_fix(vulnerable_config)
    assert result.is_secure()

def test_vuln_resolved():
    """FAIL before fix, PASS after"""
    assert is_vulnerable("component") == False
```

## Fix Types by Finding

| Finding | Output |
|---------|--------|
| Dependency CVE | Version bump command + lockfile update |
| Container issue | Dockerfile patch |
| IaC misconfiguration | Terraform/K8s fix |
| Code vulnerability | Source patch + test |
| Secret exposure | Rotation commands + `.gitignore` update |

## Example Interaction

**User:** "Run a security scan on this project"

**Claude:**
1. Discovers 47 npm dependencies, 3 Dockerfiles, 2 Terraform configs
2. Fetches current CVE data from OSV.dev
3. Identifies 12 vulnerabilities (2 critical, 4 high, 6 medium)
4. Generates phased remediation plan with:
   - Actual fix commands (`npm install lodash@4.17.21`)
   - Code patches for IaC misconfigurations
   - TDD tests proving each fix works
5. Outputs technical and executive reports
