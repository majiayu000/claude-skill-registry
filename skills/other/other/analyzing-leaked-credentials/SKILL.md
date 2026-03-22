<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: analyzing-leaked-credentials
description: >-
  Analyze leaked credentials from data breaches, paste sites, and dark web
  dumps to assess organizational exposure, identify compromised accounts,
  and support credential stuffing assessments.
domain: cybersecurity
subdomain: osint-recon
tags:
  - credentials
  - breach-data
  - haveibeenpwned
  - credential-stuffing
  - password-analysis
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: >-
  h8mail, haveibeenpwned API, dehashed API, snusbase,
  pwndb, breach-parse.
metadata:
  mitre-attack:
    - "T1589.001"  # Gather Victim Identity Information: Credentials
    - "T1110"      # Brute Force
    - "T1552"      # Unsecured Credentials
---

# Analyzing Leaked Credentials

## Overview

Leaked credential analysis checks whether organizational email addresses and
passwords appear in known data breaches. Sources include HaveIBeenPwned,
Dehashed, breach compilation databases, and paste monitoring services.
Findings reveal password reuse risks, compromised service accounts, and
targets for credential stuffing assessments.

## Prerequisites

- h8mail for multi-source breach queries
- HaveIBeenPwned API key (paid, for domain search)
- Dehashed API credentials (optional)
- Python 3.10+ with `requests`
- Breach compilation databases (legally obtained)

```bash
pip install h8mail requests
```

## Quick Reference

| Task | Command |
|------|---------|
| h8mail single | `h8mail -t user@example.com` |
| h8mail bulk | `h8mail -t emails.txt` |
| HIBP breach | `curl -s -H "hibp-api-key: $KEY" "https://haveibeenpwned.com/api/v3/breachedaccount/user@example.com"` |
| HIBP domain | `curl -s -H "hibp-api-key: $KEY" "https://haveibeenpwned.com/api/v3/breaches"` |
| HIBP pastes | `curl -s -H "hibp-api-key: $KEY" "https://haveibeenpwned.com/api/v3/pasteaccount/user@example.com"` |
| Password check | `echo -n "password" \| sha1sum \| cut -c1-5` then query HIBP range API |

## Workflow

### Step 1: Domain-Wide Breach Check

```bash
# h8mail — check all harvested emails against breach databases
h8mail -t harvested_emails.txt -o breach_results.csv

# h8mail with breach compilation
h8mail -t emails.txt --breach-compilation /path/to/breachcomp -o results.csv
```

### Step 2: HaveIBeenPwned API

```bash
# Check individual email
curl -s -H "hibp-api-key: $HIBP_KEY" -H "user-agent: OSINT-Agent" \
  "https://haveibeenpwned.com/api/v3/breachedaccount/user@example.com?truncateResponse=false"

# List all known breaches
curl -s "https://haveibeenpwned.com/api/v3/breaches" | jq '.[].Name'

# Check pastes
curl -s -H "hibp-api-key: $HIBP_KEY" -H "user-agent: OSINT-Agent" \
  "https://haveibeenpwned.com/api/v3/pasteaccount/user@example.com"
```

### Step 3: Password Exposure Check (k-Anonymity)

```bash
# HIBP Passwords API uses k-anonymity — safe to query
PREFIX=$(echo -n "password123" | sha1sum | cut -c1-5 | tr '[:lower:]' '[:upper:]')
SUFFIX=$(echo -n "password123" | sha1sum | cut -c6-40 | tr '[:lower:]' '[:upper:]')

curl -s "https://api.pwnedpasswords.com/range/$PREFIX" | grep "$SUFFIX"
# Returns count of times the password appeared in breaches
```

### Step 4: Credential Analysis

```python
from collections import Counter

def analyze_breaches(breach_data: list[dict]) -> dict:
    """Analyze breach exposure patterns."""
    breaches = Counter()
    dates = []
    for entry in breach_data:
        for b in entry.get("breaches", []):
            breaches[b["Name"]] += 1
            dates.append(b.get("BreachDate", ""))
    return {
        "total_accounts": len(breach_data),
        "unique_breaches": dict(breaches.most_common(10)),
        "earliest_breach": min(dates) if dates else None,
        "latest_breach": max(dates) if dates else None,
    }
```

### Step 5: Reporting

Produce a credential exposure report:
- **Total accounts checked** vs. accounts found in breaches
- **Breach sources**: which data breaches contain organizational emails
- **High-risk accounts**: accounts in multiple breaches or recent breaches
- **Password reuse indicators**: same email across multiple breach sources
- **Recommendations**: mandatory password resets, MFA enforcement

## Detection Opportunities

- HIBP API queries logged by API key
- Breach database downloads monitored by law enforcement
- Credential stuffing attempts detected by authentication systems

## Verification

- [ ] All harvested emails checked against breach databases
- [ ] HaveIBeenPwned queried for breached accounts and pastes
- [ ] Password exposure assessed via k-anonymity API
- [ ] Breach sources and dates documented
- [ ] High-risk accounts flagged for remediation
- [ ] Report includes exposure statistics and recommendations

## References

- [HaveIBeenPwned](https://haveibeenpwned.com/)
- [HIBP API](https://haveibeenpwned.com/API/v3)
- [h8mail](https://github.com/khast3x/h8mail)
- [Dehashed](https://dehashed.com/)

---
v1.0 | Validated: 2026-03-17
