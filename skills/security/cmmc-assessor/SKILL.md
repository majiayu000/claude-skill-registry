---
name: cmmc-assessor
description: >
  Assess CMMC Level 2/3 compliance by mapping NIST SP 800-171 controls to
  Embry OS features and detected configurations. Generates gap analysis reports.
allowed-tools:
  - run_command
  - read_file
triggers:
  - cmmc
  - cmmc-assessor
  - nist 800-171
  - compliance assessment
  - cmmc level 2
  - cmmc level 3
  - cybersecurity maturity
  - defense compliance
metadata:
  short-description: CMMC Level 2/3 compliance assessment (NIST SP 800-171)
provides:
  - cmmc-assessor
composes:
  - memory
  - extractor
  - ops-compliance
  - create-figure
  - task-monitor
taxonomy:
  - security
  - compliance
---

# CMMC Assessor

Assess CMMC Level 2 and Level 3 compliance against NIST SP 800-171 Rev 2 (110 controls)
and NIST SP 800-172 enhanced controls. Maps each control to Embry OS features,
workstation configuration, and detected gaps.

## Commands

| Command | Description |
|---------|-------------|
| `./run.sh assess --level 2` | Run full CMMC Level 2 assessment (110 controls) |
| `./run.sh assess --level 3 --profile high` | Level 3 with enhanced SP 800-172 controls |
| `./run.sh assess --family AC` | Assess single family (Access Control) |
| `./run.sh gap-report` | Generate gap analysis with remediation steps |
| `./run.sh controls` | List all 110 NIST SP 800-171 controls |
| `./run.sh families` | List 14 control families |
| `./run.sh map-feature <feature>` | Map Embry OS feature to controls it satisfies |
| `./run.sh status` | Quick pass/fail summary |
| `./run.sh export --format json` | Export assessment as JSON for auditors |
| `./run.sh export --format ssp` | Export as System Security Plan skeleton |

## Control Families (14)

| ID | Family | Controls | Embry OS Coverage |
|----|--------|----------|-------------------|
| AC | Access Control | 22 | KDE session, D-Bus auth, socket perms |
| AT | Awareness & Training | 3 | N/A (organizational) |
| AU | Audit & Accountability | 9 | journald, ArangoDB audit log |
| CM | Configuration Management | 9 | BlueBuild immutable image, embry.yaml |
| IA | Identification & Authentication | 11 | KDE Wallet, PAM, D-Bus auth |
| IR | Incident Response | 3 | monitor-security, SPARTA alerts |
| MA | Maintenance | 6 | BlueBuild updates, OSTree |
| MP | Media Protection | 4 | LUKS, CUI marking |
| PE | Physical & Environmental | 6 | N/A (facility controls) |
| PS | Personnel Security | 2 | N/A (organizational) |
| RA | Risk Assessment | 3 | SPARTA cascade, /hack |
| CA | Security Assessment | 4 | /assess, /security-scan |
| SC | System & Communications Protection | 16 | TLS, socket isolation, air-gap |
| SI | System & Information Integrity | 7 | /security-scan, SAST, deps audit |

## Assessment Logic

Each control is checked against 3 tiers:

1. **Technical** — Can the control be verified programmatically?
   - File permissions, service configuration, crypto settings
   - Socket ACLs, D-Bus policy, firewall rules

2. **Configuration** — Is it configured in embry.yaml / BlueBuild?
   - Image hardening, kernel parameters, service enablement
   - DISA STIG overlay application

3. **Operational** — Does it require human/process verification?
   - Training records, incident response plans, personnel screening
   - Marked as "MANUAL_REVIEW" with guidance for assessors

## Output Format

```json
{
  "assessment": {
    "level": 2,
    "date": "2026-02-18T00:00:00Z",
    "system": "Embry OS v0.2.0",
    "total_controls": 110,
    "satisfied": 72,
    "partial": 18,
    "not_satisfied": 8,
    "not_applicable": 5,
    "manual_review": 7
  },
  "controls": [
    {
      "id": "AC.L2-3.1.1",
      "family": "AC",
      "title": "Authorized Access Control",
      "nist_ref": "3.1.1",
      "status": "SATISFIED",
      "evidence": [
        "KDE session requires PAM authentication",
        "D-Bus services require org.embry.* interface auth",
        "Unix socket permissions restrict to uid 1000"
      ],
      "embry_features": ["kde-session", "dbus-auth", "socket-perms"],
      "remediation": null
    }
  ]
}
```

## Integration

- **Memory**: Stores assessment results for drift detection across runs
- **Extractor**: Reads NIST SP 800-171 PDF to extract control definitions
- **SPARTA**: Maps controls to ATT&CK techniques via cascade analysis
- **ops-compliance**: Extends existing SOC2/GDPR framework with CMMC
