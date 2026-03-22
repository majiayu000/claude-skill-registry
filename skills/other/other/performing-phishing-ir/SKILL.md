<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-phishing-ir
description: >-
  Investigates and responds to phishing incidents including email header analysis,
  payload examination, recipient scope assessment, and credential compromise remediation.
domain: cybersecurity
subdomain: incident-response
tags:
  - phishing
  - email-forensics
  - credential-compromise
  - BEC
  - social-engineering
  - email-headers
version: '1.0'
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1566"]
---

# Performing Phishing Incident Response

## Overview

Phishing is the #1 initial access vector. Effective phishing IR requires rapid
analysis of the phishing email (headers, links, attachments), assessment of how
many users received and interacted with it, containment of compromised credentials,
and blocking of the attacker infrastructure. Speed matters — every minute a
phishing link stays active means more potential victims.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Email gateway logs | Delivery tracking | M365 / Google Workspace / Proofpoint |
| PhishTool | Email header analysis | https://www.phishtool.com |
| URLScan.io | Safe URL analysis | https://urlscan.io |
| VirusTotal | Attachment/URL analysis | API key required |
| ANY.RUN | Interactive sandbox | https://any.run |
| MsgParser | .msg file parsing | `pip install msg-parser` |
| oletools | Office macro analysis | `pip install oletools` |

## Key Concepts

### Phishing Types

| Type | Description | Key Indicator |
|------|-------------|---------------|
| Credential harvest | Fake login page | URL with misspelled domain |
| Malware delivery | Malicious attachment | Macro-enabled Office doc, ZIP with exe |
| BEC | Business email compromise | Spoofed executive, wire transfer request |
| Spear phishing | Targeted individual | Personal details, specific context |
| Vishing/Smishing | Voice/SMS phishing | Callback number, shortened URLs |

### Email Header Analysis

Key headers to examine:
- **From** vs **Return-Path** vs **Reply-To** — mismatches indicate spoofing
- **Received** — trace email path (read bottom to top)
- **Authentication-Results** — SPF, DKIM, DMARC pass/fail
- **X-Originating-IP** — sender's actual IP
- **Message-ID** — unique identifier for correlation

### DMARC/SPF/DKIM Verification

```
SPF:   Does sending IP match domain's SPF record?
DKIM:  Does cryptographic signature verify?
DMARC: Combined SPF+DKIM policy evaluation
```

## Workflow

### Step 1 — Analyze the Phishing Email

```bash
# Extract email headers (from .eml file)
cat phishing.eml | grep -E "^(From|To|Subject|Date|Received|Return-Path|Reply-To|Message-ID|X-Originating|Authentication-Results):"

# Check authentication results
cat phishing.eml | grep "Authentication-Results" | tr ';' '\n'

# Extract URLs from email body
cat phishing.eml | grep -oE "https?://[a-zA-Z0-9./?=&_%-]+" | sort -u

# Extract attachment hashes
# If attachment is base64 encoded in .eml:
cat phishing.eml | sed -n '/Content-Disposition: attachment/,/^--/p' | \
  grep -v "^--\|Content-" | base64 -d | sha256sum

# Analyze Office document for macros
olevba suspicious_document.docx
mraptor suspicious_document.docx
```

### Step 2 — Analyze Malicious URLs and Attachments

```bash
# Check URL with URLScan.io
curl -s -X POST "https://urlscan.io/api/v1/scan/" \
  -H "API-Key: $URLSCAN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://suspicious-domain.com/login","visibility":"unlisted"}'

# Check URL/domain with VirusTotal
curl -s "https://www.virustotal.com/api/v3/urls/$(echo -n 'https://suspicious.com' | base64 -w0)" \
  -H "x-apikey: $VT_KEY" | jq '.data.attributes.last_analysis_stats'

# Analyze attachment hash
curl -s "https://www.virustotal.com/api/v3/files/$SHA256" \
  -H "x-apikey: $VT_KEY" | jq '.data.attributes.last_analysis_stats'

# Submit to ANY.RUN sandbox (via API or manual)
# Check domain registration date (newly registered = suspicious)
whois suspicious-domain.com | grep -i "creation\|registrar\|registrant"
```

### Step 3 — Assess Recipient Scope

```powershell
# M365 — Find all recipients of phishing email (Message Trace)
Get-MessageTrace -SenderAddress "attacker@phishing.com" -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) |
  Select-Object Received, RecipientAddress, Status, Subject

# M365 — Search by subject line
Get-MessageTrace -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) |
  Where-Object {$_.Subject -like "*Urgent Invoice*"} |
  Select-Object RecipientAddress, Status

# Google Workspace — Admin audit log
# Use Admin Console > Reports > Email Log Search

# Count: received, delivered, clicked, submitted credentials
```

### Step 4 — Contain

```bash
# Block sender domain at email gateway
# Block phishing URL at web proxy / DNS sinkhole
echo "address=/phishing-domain.com/127.0.0.1" >> /etc/dnsmasq.d/sinkhole.conf

# M365 — Purge phishing email from all mailboxes
New-ComplianceSearch -Name "PhishPurge" -ExchangeLocation All \
  -ContentMatchQuery 'from:attacker@phishing.com AND subject:"Urgent Invoice"'
Start-ComplianceSearch -Identity "PhishPurge"
# After search completes:
New-ComplianceSearchAction -SearchName "PhishPurge" -Purge -PurgeType SoftDelete

# Reset credentials for users who submitted credentials
# Revoke active sessions
```

```powershell
# Disable affected users and force password reset
$AffectedUsers = @("user1@corp.com", "user2@corp.com")
foreach ($user in $AffectedUsers) {
    Set-ADUser -Identity $user -ChangePasswordAtLogon $true
    Revoke-AzureADUserAllRefreshToken -ObjectId (Get-AzureADUser -ObjectId $user).ObjectId
}
```

### Step 5 — Post-Incident Actions

```bash
# Block IOCs in security tools
# Update email filtering rules
# Notify affected users
# Report to anti-phishing working group (reportphishing@apwg.org)
# Update phishing awareness training
# Add detection rule for this campaign pattern
```

## Detection

```yaml
title: Phishing Ir Detection
id: 1ba1a85f-5f5c-46be-aa2e-e62ed8c144b6
status: experimental
description: Detects suspicious activity related to performing phishing ir techniques in incident response context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*performing*phishing*"
  condition: selection
level: high
tags:
  - attack.t1566
  - attack.impact
falsepositives:
  - Incident response team running authorized forensic collection tools
```

## Verification

- [ ] Email headers analyzed (SPF, DKIM, DMARC results)
- [ ] Malicious URLs and attachments analyzed in sandbox
- [ ] Full recipient list identified and categorized (received/clicked/compromised)
- [ ] Phishing email purged from all mailboxes
- [ ] Sender domain/IP blocked at email gateway
- [ ] Malicious URL blocked at proxy/DNS
- [ ] Compromised credentials reset and sessions revoked
- [ ] IOCs shared with security team and threat intelligence

## References

- NIST SP 800-177: Trustworthy Email
- SANS FOR578: Cyber Threat Intelligence
- Anti-Phishing Working Group: https://apwg.org
- URLScan.io API: https://urlscan.io/docs/api
- Microsoft Message Trace: https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message
