---
name: pop-assessment-security
description: "Validates PopKit security posture using concrete vulnerability patterns, automated secret scanning, and OWASP-aligned checklists"
context: fork
triggers:
  - assess security
  - security audit
  - vulnerability scan
version: 1.0.0
---

# Security Assessment Skill

## Purpose

Provides concrete, reproducible security assessment for PopKit plugins using:

- Machine-readable vulnerability patterns
- Automated secret and injection scanning
- OWASP-aligned security checklists
- Deterministic scoring

## How to Use

### Step 1: Run Automated Security Scan

```bash
python skills/pop-assessment-security/scripts/scan_secrets.py packages/plugin/
python skills/pop-assessment-security/scripts/scan_injection.py packages/plugin/
python skills/pop-assessment-security/scripts/calculate_risk.py packages/plugin/
```

### Step 2: Apply Security Checklists

Read and apply checklists in order:

1. `checklists/secret-detection.json` - Hardcoded credentials
2. `checklists/injection-patterns.json` - Command/path injection
3. `checklists/owasp-alignment.json` - OWASP Top 10 mapping

### Step 3: Generate Report

Combine automated findings with checklist results for final security report.

## Standards Reference

| Standard             | File                                | Key Checks            |
| -------------------- | ----------------------------------- | --------------------- |
| Secret Detection     | `standards/secret-patterns.md`      | SD-001 through SD-010 |
| Injection Prevention | `standards/injection-prevention.md` | IP-001 through IP-008 |
| Access Control       | `standards/access-control.md`       | AC-001 through AC-006 |
| Input Validation     | `standards/input-validation.md`     | IV-001 through IV-008 |

## Severity Classification

| Level    | Score | Description               | Action          |
| -------- | ----- | ------------------------- | --------------- |
| Critical | 9-10  | Immediately exploitable   | Block release   |
| High     | 7-8   | Likely exploitable        | Must fix        |
| Medium   | 4-6   | Conditionally exploitable | Should fix      |
| Low      | 1-3   | Minor risk                | Consider fixing |
| Info     | 0     | Best practice             | Optional        |

## Output

Returns JSON with:

- `risk_score`: 0-100 (higher = more risk)
- `vulnerabilities`: List with severity, location, CWE
- `passed_checks`: Security controls that passed
- `recommendations`: Prioritized fix list
