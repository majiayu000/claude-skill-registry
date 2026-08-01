---
name: extracting-iocs-from-samples
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: extracting-iocs-from-samples
description: >-
  Systematically extract Indicators of Compromise (IOCs) from malware samples
  including hashes, domains, IPs, URLs, mutexes, file paths, and registry keys.
domain: cybersecurity
subdomain: malware-analysis
tags:
  - ioc-extraction
  - threat-intelligence
  - stix
  - openioc
  - malware-triage
  - hash-analysis
  - network-indicators
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1587.001"]
---

# Extracting IOCs from Samples

## Overview

Indicators of Compromise (IOCs) are forensic artifacts — file hashes, IP addresses, domain names, URLs, mutexes, registry keys, and behavioral patterns — that identify malicious activity. Systematic IOC extraction from malware samples enables threat detection, hunting, blocking, and intelligence sharing. IOCs feed into SIEMs, EDR platforms, firewalls, and threat intelligence platforms (TIPs). Output formats include STIX 2.1, OpenIOC, CSV, and JSON for automated ingestion.

## Prerequisites

- Python 3.10+ with `iocextract`, `pefile`, `yara-python`, `stix2`
- `strings`, `floss` for string extraction
- VirusTotal API key for enrichment
- MISP or OpenCTI for IOC sharing
- Isolated analysis environment

## Key Concepts

### IOC Types and Confidence

| IOC Type | Example | Confidence | Shelf Life |
|----------|---------|-----------|------------|
| File hash (SHA256) | `a1b2c3...` | Very High | Permanent (for that sample) |
| File hash (MD5) | `d4e5f6...` | High | Permanent (collision risk) |
| Domain | `evil.example.com` | Medium-High | Weeks-months |
| IP address | `192.168.1.100` | Medium | Days-weeks (dynamic IPs) |
| URL | `http://evil.com/payload` | High | Days-weeks |
| Mutex | `Global\\MyMutex` | High | Months (sample-specific) |
| Registry key | `HKLM\...\Run\malware` | Medium | Varies |
| User-Agent | `Mozilla/5.0 Custom/1.0` | Medium | Months |
| YARA rule | Behavioral pattern | Very High | Months-years |
| JARM hash | TLS fingerprint | High | Months |

### IOC Pyramid of Pain

From easiest (bottom) to hardest (top) for attackers to change:
1. **Hash values** — trivial to change (recompile)
2. **IP addresses** — easy to change (new infrastructure)
3. **Domain names** — moderate effort (new registration)
4. **Network artifacts** — significant effort (new C2 profile)
5. **Host artifacts** — significant effort (new TTPs)
6. **Tools** — hard (develop new tooling)
7. **TTPs** — very hard (change methodology)

## Workflow

### Step 1: Hash Generation

```bash
# Multiple hash types
md5sum sample.exe
sha1sum sample.exe
sha256sum sample.exe
ssdeep sample.exe        # Fuzzy hash for similarity
tlsh sample.exe          # Trend Micro Locality Sensitive Hash
imphash sample.exe       # Import hash (pefile)

# Python hash generation
python3 -c "
import hashlib, pefile
data = open('sample.exe', 'rb').read()
print(f'MD5:    {hashlib.md5(data).hexdigest()}')
print(f'SHA1:   {hashlib.sha1(data).hexdigest()}')
print(f'SHA256: {hashlib.sha256(data).hexdigest()}')
pe = pefile.PE('sample.exe')
print(f'Imphash: {pe.get_imphash()}')
"
```

### Step 2: String-Based IOC Extraction

```bash
# Raw strings
strings -a -n 6 sample.exe > strings.txt

# FLOSS for obfuscated strings
floss sample.exe -j > floss_output.json

# Extract with regex patterns
grep -oP 'https?://[^\s"'"'"']+' strings.txt              # URLs
grep -oP '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b' strings.txt  # IPs
grep -oP '[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}' strings.txt      # Domains
grep -oP 'HKLM\\[^\s"]+|HKCU\\[^\s"]+' strings.txt        # Registry
```

### Step 3: Automated IOC Extraction

```python
#!/usr/bin/env python3
"""Comprehensive IOC extraction from malware samples."""
import hashlib
import re
import json
from pathlib import Path
from ipaddress import ip_address

# IOC regex patterns
IOC_PATTERNS = {
    "ipv4": r'\b(?:(?:25[0-5]|2[0-4]\d|1?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|1?\d\d?)\b',
    "ipv6": r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
    "url": r'https?://[^\s<>"\'{}|\\^`\[\]]+',
    "domain": r'\b[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,6}\b',
    "email": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
    "md5": r'\b[a-fA-F0-9]{32}\b',
    "sha1": r'\b[a-fA-F0-9]{40}\b',
    "sha256": r'\b[a-fA-F0-9]{64}\b',
    "registry": r'(?:HKLM|HKCU|HKCR|HKU|HKCC)\\[^\s"\']+',
    "filepath_win": r'[A-Z]:\\(?:[^\s<>"\'|]+\\)*[^\s<>"\'|]+',
    "filepath_unix": r'(?:/(?:tmp|var|etc|usr|opt|home|root)/[^\s"\']+)',
    "mutex": r'(?:Global\\|Local\\)[^\s"\']+',
    "useragent": r'Mozilla/5\.0[^\r\n"\']{10,}',
    "bitcoin": r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
}

# False positive filters
FP_DOMAINS = {'example.com', 'microsoft.com', 'google.com', 'localhost',
              'schema.org', 'w3.org', 'xmlsoap.org'}
FP_IPS = {'0.0.0.0', '127.0.0.1', '255.255.255.255'}

def extract_iocs(text: str) -> dict:
    """Extract all IOC types from text."""
    iocs = {}
    for ioc_type, pattern in IOC_PATTERNS.items():
        matches = set(re.findall(pattern, text))
        # Filter false positives
        if ioc_type == "domain":
            matches -= FP_DOMAINS
            matches = {d for d in matches if '.' in d and not d.endswith('.exe')}
        elif ioc_type == "ipv4":
            matches -= FP_IPS
            matches = {ip for ip in matches if is_routable(ip)}
        iocs[ioc_type] = sorted(matches)
    return {k: v for k, v in iocs.items() if v}

def is_routable(ip_str: str) -> bool:
    """Check if IP is routable (not private/reserved)."""
    try:
        ip = ip_address(ip_str)
        return not (ip.is_private or ip.is_reserved or ip.is_loopback)
    except ValueError:
        return False

def extract_from_file(filepath: str) -> dict:
    """Full IOC extraction pipeline for a file."""
    path = Path(filepath)
    data = path.read_bytes()
    text = data.decode('utf-8', errors='replace')

    # File hashes
    file_iocs = {
        "file_hashes": {
            "md5": hashlib.md5(data).hexdigest(),
            "sha1": hashlib.sha1(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "file_size": len(data),
        "file_name": path.name,
    }

    # String-based IOCs
    string_iocs = extract_iocs(text)
    file_iocs["network_iocs"] = {
        "urls": string_iocs.get("url", []),
        "domains": string_iocs.get("domain", []),
        "ips": string_iocs.get("ipv4", []),
        "emails": string_iocs.get("email", []),
    }
    file_iocs["host_iocs"] = {
        "registry_keys": string_iocs.get("registry", []),
        "file_paths": string_iocs.get("filepath_win", []) + string_iocs.get("filepath_unix", []),
        "mutexes": string_iocs.get("mutex", []),
    }
    file_iocs["crypto"] = {
        "bitcoin_addresses": string_iocs.get("bitcoin", []),
    }

    return file_iocs
```

### Step 4: VirusTotal Enrichment

```python
import requests

def enrich_hash_vt(sha256: str, api_key: str) -> dict:
    """Enrich file hash via VirusTotal API."""
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    headers = {"x-apikey": api_key}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()["data"]["attributes"]
        return {
            "detection_ratio": f"{data['last_analysis_stats']['malicious']}/{sum(data['last_analysis_stats'].values())}",
            "first_seen": data.get("first_submission_date"),
            "names": data.get("names", [])[:5],
            "tags": data.get("tags", []),
            "type": data.get("type_description", ""),
        }
    return {"error": f"VT API returned {resp.status_code}"}
```

### Step 5: Export as STIX 2.1

```python
from stix2 import Indicator, Bundle, Malware, Relationship
from datetime import datetime

def export_stix(iocs: dict) -> str:
    """Export IOCs as STIX 2.1 bundle."""
    objects = []

    # File hash indicator
    sha256 = iocs["file_hashes"]["sha256"]
    file_indicator = Indicator(
        name=f"Malware hash: {iocs['file_name']}",
        pattern=f"[file:hashes.'SHA-256' = '{sha256}']",
        pattern_type="stix",
        valid_from=datetime.utcnow(),
    )
    objects.append(file_indicator)

    # Network indicators
    for domain in iocs.get("network_iocs", {}).get("domains", []):
        ind = Indicator(
            name=f"Malicious domain: {domain}",
            pattern=f"[domain-name:value = '{domain}']",
            pattern_type="stix",
            valid_from=datetime.utcnow(),
        )
        objects.append(ind)

    for ip in iocs.get("network_iocs", {}).get("ips", []):
        ind = Indicator(
            name=f"Malicious IP: {ip}",
            pattern=f"[ipv4-addr:value = '{ip}']",
            pattern_type="stix",
            valid_from=datetime.utcnow(),
        )
        objects.append(ind)

    bundle = Bundle(objects=objects)
    return bundle.serialize(pretty=True)
```

## Detection

```yaml
title: Extracting Iocs From Samples Detection
id: ea5ef027-7667-4f5c-9eb4-e2bd476e0913
status: experimental
description: Detects suspicious activity related to extracting iocs from samples techniques in malware analysis context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*extracting*iocs*"
  condition: selection
level: high
tags:
  - attack.t1587.001
  - attack.execution
falsepositives:
  - Sandbox detonation environments analyzing submitted samples
```

## Verification

- [ ] All hash types generated (MD5, SHA1, SHA256, imphash, ssdeep)
- [ ] Network IOCs extracted (domains, IPs, URLs)
- [ ] Host IOCs extracted (registry, files, mutexes)
- [ ] False positives filtered (private IPs, common domains)
- [ ] IOCs enriched via VT/threat intel
- [ ] Output exported in standard format (STIX/CSV/JSON)
- [ ] IOCs shared with detection team and TIP

## References

- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [MISP - Threat Intelligence Platform](https://www.misp-project.org/)
- [VirusTotal API v3](https://developers.virustotal.com/reference)
- [iocextract Python Library](https://github.com/InQuest/iocextract)
- [David Bianco's Pyramid of Pain](http://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
