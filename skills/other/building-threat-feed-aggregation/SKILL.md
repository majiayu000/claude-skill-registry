<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: building-threat-feed-aggregation
description: >-
  Aggregate, normalize, and deduplicate threat intelligence feeds from multiple
  open-source and commercial sources into a unified threat intelligence platform.
domain: cybersecurity
subdomain: threat-intelligence
tags:
  - threat-feeds
  - feed-aggregation
  - misp
  - opencti
  - otx
  - abuse-ch
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: []
---
# Building Threat Feed Aggregation

## Overview

Threat feed aggregation consolidates intelligence from multiple sources (open-source
feeds, commercial providers, ISACs, government advisories) into a unified platform.
This skill covers configuring feed ingestion, normalizing IOC formats, deduplicating
across sources, applying confidence weighting, and maintaining feed health monitoring
to ensure detection systems receive high-quality, actionable intelligence.

## Prerequisites

- Python 3.10+ with `requests`, `stix2`, `feedparser`
- MISP or OpenCTI instance for aggregation platform
- API access: AlienVault OTX, Abuse.ch, ThreatFox, PhishTank
- Understanding of IOC lifecycle and confidence scoring
- Cron or task scheduler for automated polling

```bash
pip install requests stix2 feedparser
```

## Key Concepts

### Feed Quality Assessment

| Metric | Definition | Threshold |
|--------|-----------|-----------|
| False Positive Rate | % of benign indicators in feed | <5% acceptable |
| Staleness | Average age of indicators | <7 days for IPs |
| Context Quality | Tags, malware family, ATT&CK | Must include type+family |
| Update Frequency | How often new indicators arrive | Daily minimum |
| Overlap | % shared with other feeds | >80% = redundant |

### Open-Source Feed Inventory

```
abuse.ch Feeds:
├── MalwareBazaar   — malware samples (hash, signature, tags)
├── ThreatFox       — IOCs (domains, IPs, URLs) with malware family
├── URLhaus         — malicious URLs (distribution sites, C2)
├── Feodo Tracker   — botnet C2 servers (Dridex, Emotet, TrickBot)
└── SSL Blacklist   — malicious SSL certificates

AlienVault OTX:
├── Pulses          — community-contributed IOC collections
└── Subscriptions   — curated feeds by sector/region

MISP Default Feeds:
├── CIRCL OSINT     — curated open-source intelligence
├── Botvrij.eu      — botnet and malware IOCs
└── abuse.ch feeds  — integrated via MISP modules
```

### Normalization Schema

```json
{
  "value": "evil.com",
  "type": "domain",
  "source": "threatfox",
  "confidence": 75,
  "first_seen": "2026-01-15T00:00:00Z",
  "last_seen": "2026-03-01T00:00:00Z",
  "tags": ["cobalt-strike", "c2"],
  "malware_family": "CobaltStrike",
  "tlp": "white",
  "expiry": "2026-04-01T00:00:00Z"
}
```

## Workflow

### Step 1: Fetch Open-Source Feeds

```python
import requests
from datetime import datetime

def fetch_urlhaus() -> list[dict]:
    """Fetch recent malicious URLs from URLhaus."""
    resp = requests.get(
        "https://urlhaus-api.abuse.ch/v1/urls/recent/", timeout=30,
    )
    if resp.status_code == 200:
        return [
            {"value": u["url"], "type": "url", "source": "urlhaus",
             "tags": u.get("tags", []), "threat": u.get("threat", ""),
             "date_added": u.get("date_added", "")}
            for u in resp.json().get("urls", [])[:100]
        ]
    return []

def fetch_feodotracker() -> list[dict]:
    """Fetch botnet C2 IPs from Feodo Tracker."""
    resp = requests.get(
        "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json",
        timeout=30,
    )
    if resp.status_code == 200:
        return [
            {"value": entry["ip_address"], "type": "ip", "source": "feodotracker",
             "port": entry.get("port"), "malware": entry.get("malware", ""),
             "first_seen": entry.get("first_seen", "")}
            for entry in resp.json()[:100]
        ]
    return []

def fetch_otx_pulse(pulse_id: str, api_key: str) -> list[dict]:
    """Fetch indicators from an AlienVault OTX pulse."""
    resp = requests.get(
        f"https://otx.alienvault.com/api/v1/pulses/{pulse_id}/indicators",
        headers={"X-OTX-API-KEY": api_key}, timeout=30,
    )
    if resp.status_code == 200:
        return [
            {"value": i["indicator"], "type": i["type"], "source": "otx",
             "title": i.get("title", ""), "description": i.get("description", "")}
            for i in resp.json().get("results", [])
        ]
    return []
```

### Step 2: Normalize and Deduplicate

```python
from collections import defaultdict

def normalize_indicators(raw_feeds: list[list[dict]]) -> list[dict]:
    """Normalize and deduplicate indicators across feeds."""
    seen: dict[str, dict] = {}
    for feed in raw_feeds:
        for indicator in feed:
            key = f"{indicator['type']}:{indicator['value'].lower()}"
            if key in seen:
                seen[key]["sources"].append(indicator["source"])
                seen[key]["confidence"] = min(seen[key]["confidence"] + 10, 100)
            else:
                seen[key] = {
                    "value": indicator["value"].lower(),
                    "type": indicator["type"],
                    "sources": [indicator["source"]],
                    "confidence": 50,
                    "tags": indicator.get("tags", []),
                    "malware": indicator.get("malware", indicator.get("threat", "")),
                    "first_seen": indicator.get("first_seen", indicator.get("date_added", "")),
                }
    return list(seen.values())
```

### Step 3: Feed Health Monitoring

```python
def check_feed_health(feed_name: str, fetch_fn: callable) -> dict:
    """Monitor feed availability and freshness."""
    try:
        start = datetime.now()
        results = fetch_fn()
        elapsed = (datetime.now() - start).total_seconds()
        return {
            "feed": feed_name,
            "status": "healthy",
            "indicator_count": len(results),
            "response_time_s": elapsed,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "feed": feed_name,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
```

### Step 4: Push to MISP

```python
def push_to_misp(indicators: list[dict], misp_url: str, misp_key: str, event_id: int) -> dict:
    """Push normalized indicators to MISP event."""
    type_map = {"ip": "ip-dst", "domain": "domain", "url": "url", "sha256": "sha256"}
    pushed = 0
    for ind in indicators:
        misp_type = type_map.get(ind["type"], "text")
        payload = {
            "value": ind["value"], "type": misp_type,
            "to_ids": ind["confidence"] >= 70,
            "comment": f"Sources: {', '.join(ind['sources'])}. Confidence: {ind['confidence']}",
        }
        resp = requests.post(
            f"{misp_url}/attributes/add/{event_id}",
            headers={"Authorization": misp_key, "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code == 200:
            pushed += 1
    return {"pushed": pushed, "total": len(indicators), "event_id": event_id}
```

## Verification

- [ ] All configured feeds return data within acceptable response times
- [ ] Indicators normalized to consistent schema across all sources
- [ ] Deduplication correctly merges indicators, boosting multi-source confidence
- [ ] Feed health monitoring alerts on failures or stale data
- [ ] High-confidence indicators pushed to MISP with proper TLP marking
- [ ] Automated polling runs on schedule without manual intervention

## References

- [abuse.ch Threat Intelligence](https://abuse.ch/)
- [AlienVault OTX API](https://otx.alienvault.com/api)
- [MISP Feeds Documentation](https://www.misp-project.org/feeds/)
- [OpenCTI Connectors](https://docs.opencti.io/latest/deployment/connectors/)
- [PhishTank API](https://phishtank.org/api_info.php)
