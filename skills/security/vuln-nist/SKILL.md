---
name: vuln-nist
description: NIST vulnerability database lookup and CVE analysis
allowed-tools: [Bash, Read, WebFetch]
---

# NIST Vulnerability Skill

## Overview

NIST National Vulnerability Database lookup. 90%+ context savings.

## Tools (Progressive Disclosure)

### CVE Lookup

| Tool        | Description            |
| ----------- | ---------------------- |
| search-cve  | Search CVEs by keyword |
| get-cve     | Get CVE details by ID  |
| recent-cves | List recent CVEs       |

### Analysis

| Tool              | Description            |
| ----------------- | ---------------------- |
| cvss-score        | Get CVSS score         |
| cpe-match         | Match CPE identifiers  |
| affected-products | List affected products |

### Reporting

| Tool             | Description             |
| ---------------- | ----------------------- |
| export-json      | Export CVE data as JSON |
| severity-summary | Summarize by severity   |

## Agent Integration

- **security-architect** (primary): Vulnerability assessment
- **compliance-auditor** (primary): Compliance reporting
- **developer** (secondary): Dependency security
