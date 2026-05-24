---
name: ops-compliance
description: >
  Check codebases against compliance frameworks (SOC2, GDPR, HIPAA, PCI-DSS).
  Generates compliance reports with pass/fail status and remediation guidance.
allowed-tools:
  - run_command
  - read_file
triggers:
  - compliance
  - ops-compliance
  - soc2
  - gdpr
  - hipaa
  - pci-dss
  - audit
metadata:
  short-description: Compliance checking (SOC2, GDPR, HIPAA, PCI-DSS)
---

# Compliance-Ops: Compliance Framework Checker

Check codebases against common compliance frameworks and generate audit reports.

## Supported Frameworks

| Framework | Description | Controls |
|-----------|-------------|----------|
| SOC2 | Service Organization Control 2 Type II | CC1-CC9 |
| GDPR | General Data Protection Regulation | Articles 5-49 |
| HIPAA | Health Insurance Portability and Accountability Act | Coming soon |
| PCI-DSS | Payment Card Industry Data Security Standard | Coming soon |

## Features

1. **SOC2 Checks**
   - Access control verification
   - Logging and monitoring
   - Encryption at rest/transit
   - Change management

2. **GDPR Checks**
   - PII detection in code
   - Data inventory validation
   - Consent mechanism verification
   - Data retention policies

3. **Report Generation**
   - Markdown, JSON, HTML formats
   - Executive summary
   - Detailed findings
   - Remediation recommendations

4. **Integrations**
   - Task-monitor: Real-time progress tracking
   - Memory: Historical compliance tracking

## Commands

| Command | Description |
|---------|-------------|
| `./run.sh check --framework soc2` | Run SOC2 compliance checks |
| `./run.sh check --framework gdpr` | Run GDPR compliance checks |
| `./run.sh report --format markdown` | Generate compliance report |
| `./run.sh frameworks` | List available frameworks |

## Usage

```bash
# SOC2 compliance check
./run.sh check --framework soc2 --path /path/to/project

# GDPR compliance check
./run.sh check --framework gdpr --path .

# Generate markdown report
./run.sh report --format markdown --output compliance_report.md

# Store results in memory
./run.sh check --framework soc2 --path . --store-results
```

## Output Format

All commands output structured JSON with:
- `framework`: Framework checked
- `checks`: List of check results
- `status`: pass/fail/warning
- `control_id`: Control category (e.g., CC1.1)
- `description`: What was checked
- `finding`: Issue description if failed
- `remediation`: Suggested fix

## SOC2 Control Categories

| Category | Description |
|----------|-------------|
| CC1 | Control Environment |
| CC2 | Communication and Information |
| CC3 | Risk Assessment |
| CC4 | Monitoring Activities |
| CC5 | Control Activities |
| CC6 | Logical and Physical Access |
| CC7 | System Operations |
| CC8 | Change Management |
| CC9 | Risk Mitigation |

## Integration with Task-Monitor

Compliance scans register with task-monitor:

```bash
# View scan progress
.pi/skills/task-monitor/run.sh tui --filter ops-compliance
```

## Integration with Memory

Track compliance posture over time:

```bash
# Store results
./run.sh check --framework soc2 --path . --store-results

# Recall compliance history
.pi/skills/memory/run.sh recall "SOC2 compliance"
```
