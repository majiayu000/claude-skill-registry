<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-ssl-tls-audit
description: >-
  Comprehensive SSL/TLS configuration auditing using testssl.sh, sslyze, and
  nmap NSE scripts. Covers cipher suite evaluation, protocol version checks,
  vulnerability scanning (BEAST, POODLE, Heartbleed, ROBOT), HSTS validation,
  and compliance reporting against Mozilla and NIST guidelines.
domain: cybersecurity
subdomain: cryptography
tags:
  - tls
  - ssl
  - audit
  - testssl
  - sslyze
  - cipher-suites
  - hsts
  - vulnerability-scanning
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1557.002"]
---

# Performing SSL/TLS Audit

## Overview

TLS misconfigurations expose services to downgrade attacks, MITM interception,
and data exfiltration. This skill covers systematic auditing of TLS endpoints
using industry-standard tools, evaluating against Mozilla's TLS guidelines
and NIST SP 800-52 Rev. 2.

## Prerequisites

| Requirement | Install |
|---|---|
| testssl.sh | `git clone https://github.com/drwetter/testssl.sh.git` |
| sslyze | `pip install sslyze` |
| nmap | `apt install nmap` |
| OpenSSL 3.x | `apt install openssl` |
| Python 3.10+ | For agent tooling |

## Key Concepts

### Full Audit with testssl.sh

```bash
# Comprehensive scan
testssl.sh --severity HIGH --wide example.com:443

# Check specific vulnerabilities
testssl.sh --vulnerable example.com:443

# Check cipher suites only
testssl.sh --cipher-per-proto example.com:443

# JSON output for automation
testssl.sh --jsonfile results.json example.com:443

# Check STARTTLS services
testssl.sh --starttls smtp mail.example.com:587
```

### sslyze Scanning

```bash
# Regular scan with certificate info
sslyze --regular example.com

# Check for specific vulnerabilities
sslyze --heartbleed --openssl_ccs --robot example.com

# JSON output
sslyze --json_out results.json example.com

# Scan multiple targets
sslyze --targets_in targets.txt --regular
```

### nmap TLS Scripts

```bash
# Enumerate TLS ciphers
nmap --script ssl-enum-ciphers -p 443 example.com

# Check for known vulnerabilities
nmap --script ssl-heartbleed,ssl-poodle,ssl-ccs-injection -p 443 example.com

# Certificate information
nmap --script ssl-cert -p 443 example.com
```

### Known TLS Vulnerabilities

| Vulnerability | CVE | Impact | Test |
|---|---|---|---|
| Heartbleed | CVE-2014-0160 | Memory disclosure | `testssl.sh --heartbleed` |
| POODLE | CVE-2014-3566 | SSLv3 padding oracle | `testssl.sh --poodle` |
| BEAST | CVE-2011-3389 | CBC IV attack (TLS 1.0) | `testssl.sh --beast` |
| ROBOT | CVE-2017-13099 | RSA padding oracle | `testssl.sh --robot` |
| CRIME | CVE-2012-4929 | TLS compression leak | `testssl.sh --crime` |
| DROWN | CVE-2016-0800 | SSLv2 cross-protocol | `testssl.sh --drown` |
| Ticketbleed | CVE-2016-9244 | Session ticket leak | `testssl.sh --ticketbleed` |

### Mozilla TLS Profiles

| Profile | Min TLS | Ciphers | Use Case |
|---|---|---|---|
| Modern | TLS 1.3 only | TLS 1.3 suites only | New services, modern clients |
| Intermediate | TLS 1.2 | ECDHE+AESGCM, ECDHE+CHACHA | General purpose |
| Old | TLS 1.0 | Broad set | Legacy compatibility only |

## Workflow

1. **Scope** — Identify all TLS endpoints (ports 443, 8443, 993, 995, etc.)
2. **Scan** — Run testssl.sh and sslyze against each endpoint
3. **Evaluate** — Compare against Mozilla Intermediate or Modern profile
4. **Classify** — Rate findings by severity (Critical/High/Medium/Low)
5. **Report** — Document with specific remediation per finding
6. **Verify** — Re-scan after remediation to confirm fixes

## Verification

| Check | Method |
|---|---|
| TLS 1.2+ only | testssl.sh shows no SSLv3, TLS 1.0, TLS 1.1 |
| No weak ciphers | No RC4, DES, NULL, EXPORT, anon ciphers |
| No known vulns | testssl.sh `--vulnerable` reports all green |
| HSTS enabled | `curl -sI` shows `Strict-Transport-Security` header |
| Strong key exchange | Only ECDHE or DHE (≥2048-bit) |
| Certificate valid | Not expired, correct SAN, trusted chain |

## References

- [testssl.sh GitHub](https://github.com/drwetter/testssl.sh)
- [sslyze Documentation](https://nabla-c0d3.github.io/sslyze/documentation/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final)
