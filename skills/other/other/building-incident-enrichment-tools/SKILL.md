<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: building-incident-enrichment-tools
description: >-
  Build automated incident enrichment tools that correlate IOCs against
  threat intelligence feeds, perform IP/domain reputation lookups, enrich
  alerts with WHOIS/GeoIP data, and produce analyst-ready context packages
  for faster triage and response.
domain: cybersecurity
subdomain: automation-scripting
tags:
  - incident-response
  - ioc-enrichment
  - threat-intelligence
  - whois
  - geoip
  - reputation-lookup
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: []
---

# Building Incident Enrichment Tools

## Overview

SOC analysts waste time on manual lookups during triage. This skill covers
building enrichment tools that automatically correlate IOCs (IPs, domains,
hashes) against multiple intelligence sources, add context (GeoIP, WHOIS,
reputation scores), and package results for analyst consumption.

Mode: `[MODE: INCIDENT]` — Triage enrichment for faster response.

## Prerequisites

| Requirement | Details |
|---|---|
| Python 3.10+ with `requests`, `ipwhois` | Required |
| API keys for VirusTotal, AbuseIPDB, Shodan (optional) | Required |
| MaxMind GeoIP database for geolocation | Required |

## Key Concepts

### IP Enrichment

```python
import requests

def enrich_ip(ip: str, vt_key: str | None = None, abuseipdb_key: str | None = None) -> dict:
    """Enrich an IP with reputation, GeoIP, and WHOIS data."""
    result = {"ip": ip, "sources": {}}

    # AbuseIPDB
    if abuseipdb_key:
        resp = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={"Key": abuseipdb_key, "Accept": "application/json"},
            params={"ipAddress": ip, "maxAgeInDays": 90},
            timeout=10,
        )
        if resp.ok:
            data = resp.json().get("data", {})
            result["sources"]["abuseipdb"] = {
                "abuse_score": data.get("abuseConfidenceScore"),
                "country": data.get("countryCode"),
                "isp": data.get("isp"),
                "total_reports": data.get("totalReports"),
            }

    # VirusTotal
    if vt_key:
        resp = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": vt_key},
            timeout=10,
        )
        if resp.ok:
            attrs = resp.json().get("data", {}).get("attributes", {})
            stats = attrs.get("last_analysis_stats", {})
            result["sources"]["virustotal"] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "country": attrs.get("country"),
                "as_owner": attrs.get("as_owner"),
            }

    return result
```

### Domain Enrichment

```python
def enrich_domain(domain: str, vt_key: str | None = None) -> dict:
    """Enrich a domain with WHOIS and reputation data."""
    result = {"domain": domain, "sources": {}}

    # WHOIS via RDAP
    try:
        resp = requests.get(f"https://rdap.org/domain/{domain}", timeout=10)
        if resp.ok:
            data = resp.json()
            result["sources"]["whois"] = {
                "registrar": next(
                    (e.get("vcardArray", [[],[]])[1][1][3] for e in data.get("entities", [])
                     if "registrar" in e.get("roles", [])),
                    "unknown",
                ),
                "status": data.get("status", []),
                "events": [
                    {"action": e["eventAction"], "date": e["eventDate"]}
                    for e in data.get("events", [])
                ],
            }
    except Exception:
        result["sources"]["whois"] = {"error": "lookup failed"}

    return result
```

### Hash Reputation Check

```python
def check_hash_reputation(file_hash: str, vt_key: str) -> dict:
    """Check file hash against VirusTotal."""
    resp = requests.get(
        f"https://www.virustotal.com/api/v3/files/{file_hash}",
        headers={"x-apikey": vt_key},
        timeout=10,
    )
    if not resp.ok:
        return {"hash": file_hash, "status": "not_found"}
    attrs = resp.json().get("data", {}).get("attributes", {})
    stats = attrs.get("last_analysis_stats", {})
    return {
        "hash": file_hash,
        "detections": f"{stats.get('malicious', 0)}/{sum(stats.values())}",
        "type": attrs.get("type_description"),
        "names": attrs.get("names", [])[:5],
        "tags": attrs.get("tags", [])[:10],
    }
```

## Workflow

### Step 1: Enrich an IP Address

```bash
node scripts/agent.js --action enrich-ip --ioc 1.2.3.4
```

### Step 2: Enrich a Domain

```bash
node scripts/agent.js --action enrich-domain --ioc evil.example.com
```

### Step 3: Check File Hash

```bash
node scripts/agent.js --action check-hash --ioc abc123def456...
```

## Verification

- [ ] IP enrichment returns reputation score, GeoIP, and ASN info
- [ ] Domain enrichment includes WHOIS registrar and registration dates
- [ ] Hash lookup returns detection ratio and file type
- [ ] Handles API rate limits and missing keys gracefully
- [ ] Exit code 0 on success, 1 on malicious IOC, 2 on error

## References

- [VirusTotal API v3](https://docs.virustotal.com/reference/overview)
- [AbuseIPDB API](https://docs.abuseipdb.com/)
- [Shodan API](https://developer.shodan.io/api)
- [MITRE ATT&CK T1071 — Application Layer Protocol](https://attack.mitre.org/techniques/T1071/)
