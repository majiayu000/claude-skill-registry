---
name: email-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: email-security
description: >-
  Email security engineering covering authentication protocols (SPF, DKIM, DMARC, ARC),
  secure email gateway configuration, spoofing detection, email encryption (S/MIME, PGP,
  TLS enforcement), header forensics, malware detection, DLP policies, compliance auditing,
  account compromise detection, archival security, email threat hunting, and security
  awareness training. Spans offensive testing, defensive hardening, and incident response
  for enterprise email infrastructure.
domain: cybersecurity
subdomain: email-security
tags:
  - email-security
  - spf
  - dkim
  - dmarc
  - phishing
  - email-gateway
  - email-encryption
  - email-forensics
  - dlp
  - bec
  - email-compliance
  - threat-hunting
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1566", "T1566.001", "T1566.002", "T1534", "T1114", "T1048.003"]
  frameworks: ["NIST 800-177", "DMARC RFC 7489", "CIS Controls v8"]
---

# Email Security

## When to Use

Activate when the operator asks about email authentication (SPF/DKIM/DMARC),
email gateway hardening, phishing detection, email encryption, header analysis,
email-borne malware, DLP for email, compliance auditing, BEC detection, email
archival, email threat hunting, or security awareness programs.

Mode: `[MODE: RED]` for phishing simulation and email spoofing; `[MODE: BLUE]` for gateway hardening and detection; `[MODE: INCIDENT]` for BEC triage and header forensics; `[MODE: ARCHITECT]` for email infrastructure design.

## Prerequisites

- DNS query tools (`dig`, `nslookup`, `host`) for SPF/DKIM/DMARC validation
- Email header access (raw message source) for forensic analysis
- Administrative access to email gateway (Exchange, M365, Google Workspace)
- SMTP testing tools (`swaks`, `openssl s_client`) for protocol testing

## Quick Reference

| Control | Command / Technique | Framework |
|---------|---------------------|-----------|
| SPF check | `dig TXT domain.com \| grep spf` | NIST 800-177 |
| DKIM verify | `opendkim-testkey -d domain.com -s selector -vvv` | RFC 6376 |
| DMARC lookup | `dig TXT _dmarc.domain.com` | RFC 7489 |
| SMTP TLS test | `openssl s_client -starttls smtp -connect mx.domain.com:25` | RFC 3207 |
| Header trace | `swaks --to test@domain.com --from test@spoof.com` | — |
| Phishing test | `gophish` campaign deployment | NIST 800-50 |
| BEC detection | Authentication-Results header analysis | CIS 9.2 |
| Email DLP | Transport rule with sensitive info types | CIS 13.4 |

## Workflow

### 1. Email Authentication Assessment

```bash
# SPF record validation
dig TXT example.com | grep "v=spf1"

# DKIM selector discovery and validation
dig TXT selector1._domainkey.example.com
dig TXT selector2._domainkey.example.com

# DMARC policy check
dig TXT _dmarc.example.com

# MTA-STS policy verification
curl -s https://mta-sts.example.com/.well-known/mta-sts.txt

# DANE/TLSA record check
dig TLSA _25._tcp.mx.example.com

# ARC chain validation (for forwarding scenarios)
# Check ARC-Seal, ARC-Message-Signature, ARC-Authentication-Results headers
```

### 2. Email Gateway Security Audit

```bash
# Test SMTP STARTTLS support
openssl s_client -starttls smtp -connect mx.example.com:25 -brief

# Check for open relay
swaks --to external@test.com --from fake@example.com \
  --server mx.example.com --quit-after RCPT

# Test SPF enforcement
swaks --to target@example.com --from spoofed@fakedomain.com \
  --server mx.example.com

# Verify TLS certificate
openssl s_client -starttls smtp -connect mx.example.com:25 \
  | openssl x509 -noout -subject -dates -issuer
```

### 3. Phishing & Spoofing Detection

```bash
# Extract Authentication-Results from email headers
grep -E "^(Authentication-Results|Received-SPF|DKIM-Signature|ARC-)" headers.txt

# Check return-path vs from alignment
grep -E "^(From|Return-Path|Reply-To|Envelope-From):" headers.txt

# Analyze received chain for suspicious hops
grep "^Received:" headers.txt | tac

# URL extraction and analysis from email body
grep -oE 'https?://[^"'"'"'> ]+' email_body.txt | sort -u
```

### 4. Email-Based Threat Hunting

```bash
# Hunt for BEC patterns — sender display name spoofing
# Search for emails where From display name matches executive but address differs

# Hunt for credential harvesting
# Search for emails with links to login pages on non-corporate domains

# Hunt for attachment-based threats
# Search for emails with macro-enabled attachments (.docm, .xlsm, .pptm)

# Hunt for email forwarding rules (persistence)
# M365: Search-UnifiedAuditLog -Operations "New-InboxRule","Set-InboxRule"
```

### 5. Email Encryption Verification

```bash
# Test S/MIME certificate
openssl x509 -in cert.pem -noout -text | grep -A2 "Key Usage"

# Verify PGP key
gpg --import public.asc
gpg --verify signed_message.asc

# Test mandatory TLS enforcement
swaks --to secure@partner.com --tls-verify --server mx.partner.com

# Check MTA-STS enforcement mode
curl -s https://mta-sts.example.com/.well-known/mta-sts.txt | grep mode
```

## Verification

- [ ] SPF, DKIM, DMARC records validated and aligned
- [ ] Email gateway enforces TLS and rejects spoofed messages
- [ ] Phishing simulation campaign executed and metrics collected
- [ ] Email encryption (TLS/S/MIME/PGP) verified end-to-end
- [ ] Header forensics workflow tested with sample phishing emails
- [ ] DLP policies cover sensitive data patterns in email
- [ ] Compliance audit covers retention, encryption, and access control
- [ ] BEC detection rules deployed and tested
- [ ] Email archival integrity and access controls verified
- [ ] Threat hunting queries deployed for email-based IOCs
- [ ] Security awareness program metrics tracked

## References

- [NIST SP 800-177 — Trustworthy Email](https://csrc.nist.gov/publications/detail/sp/800-177/rev-1/final)
- [DMARC RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489)
- [SPF RFC 7208](https://datatracker.ietf.org/doc/html/rfc7208)
- [DKIM RFC 6376](https://datatracker.ietf.org/doc/html/rfc6376)
- [MITRE ATT&CK T1566 — Phishing](https://attack.mitre.org/techniques/T1566/)
- [CIS Controls v8 — Section 9](https://www.cisecurity.org/controls)
