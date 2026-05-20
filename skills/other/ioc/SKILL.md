---
name: ioc
description: IOC extraction, enrichment, and threat intelligence correlation
---

# IOC Intelligence

Extract and enrich indicators:
- Extract IOCs from any source (reports, logs, samples)
- Normalize and validate indicators
- Enrich with threat intel (VT, AbuseIPDB, WHOIS)
- Correlate infrastructure
- Export in multiple formats

## IOC Types
IPv4/IPv6, domains, URLs, hashes (MD5/SHA1/SHA256), emails, registry keys, file paths, mutexes

## Required Context
1. **Source**: File path, text, or paste content
2. **IOC Types**: All or specific types
3. **Enrichment**: Basic (WHOIS) or full (VT, Shodan)
4. **Output**: JSON, CSV, STIX, MISP

## Example
```
/ioc
Source: threat_report.pdf
Enrichment: Full
Output: JSON
```
