---
name: spiderfoot
description: >-
  SpiderFoot automated OSINT framework with 200+ modules for comprehensive target profiling. Use
  when: running automated OSINT investigations on a target, correlating data across dozens of
  sources, building threat intelligence profiles, or mapping connections between entities.
license: Apache-2.0
compatibility: "Python 3.9+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: research
  tags: [spiderfoot, threat-intel, recon, profiling, osint]
  use-cases:
    - "Run automated OSINT scan on a company domain to build a full profile"
    - "Investigate an IP address across dark web, breach data, and social sources"
    - "Gather threat intelligence on a suspicious email or domain"
    - "Correlate data from 200+ sources to map relationships between entities"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# SpiderFoot

## Overview

SpiderFoot is an open-source intelligence automation platform with 200+ modules that query hundreds of public data sources simultaneously. It correlates data across passive DNS, Whois, social media, dark web, certificate transparency, breach databases, geolocation services, and more. SpiderFoot is unique in its ability to automatically chain discoveries — finding an email leads to social profiles, which leads to more domains, which leads to more IPs, building a comprehensive intelligence picture automatically.

**Supports two modes:** Web UI (browser-based, visual) and CLI (scriptable, automated).

## Instructions

### Step 1: Install SpiderFoot

```bash
# Clone and install
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot
pip install -r requirements.txt

# Verify
python3 sf.py --help
```

### Step 2: Launch the Web UI

```bash
# Start the web server (default: http://127.0.0.1:5001)
python3 sf.py -l 127.0.0.1:5001

# Bind to all interfaces (use with caution — no auth by default)
python3 sf.py -l 0.0.0.0:5001

# Access the UI at http://127.0.0.1:5001
# Create a new scan: Scans → New Scan → Enter target + select modules
```

### Step 3: CLI usage — run scans without the UI

```bash
# Basic syntax
python3 sf.py -s TARGET -t TARGET_TYPE -m MODULE1,MODULE2

# Target types:
# INTERNET_NAME  — domain or hostname (example.com)
# IP_ADDRESS     — IPv4 address (1.2.3.4)
# EMAILADDR      — email address (user@example.com)
# USERNAME       — username
# NETBLOCK       — IP range (1.2.3.0/24)
# PHONE_NUMBER   — phone number
# HUMAN_NAME     — person name

# Scan a domain with all modules
python3 sf.py -s example.com -t INTERNET_NAME -m ALL -o json -f results.json

# Scan with specific modules only (faster, focused)
python3 sf.py -s example.com -t INTERNET_NAME \
  -m sfp_dnsresolve,sfp_dnsdumpster,sfp_shodan,sfp_certspotter,sfp_whois \
  -o json -f dns_results.json

# Scan an IP address
python3 sf.py -s 1.2.3.4 -t IP_ADDRESS \
  -m sfp_shodan,sfp_virustotal,sfp_ipinfo,sfp_abuseipdb \
  -o json -f ip_results.json

# Scan an email address
python3 sf.py -s user@example.com -t EMAILADDR \
  -m sfp_haveibeenpwned,sfp_hunter,sfp_emailrep \
  -o json -f email_results.json

# List all available modules
python3 sf.py -M
```

### Step 4: Key module categories and selections

```bash
# Passive DNS and infrastructure
PASSIVE_DNS_MODULES="sfp_dnsresolve,sfp_dnsdumpster,sfp_certspotter,sfp_crt,sfp_passivetotal"

# Subdomain discovery
SUBDOMAIN_MODULES="sfp_dnsbrute,sfp_dnsdumpster,sfp_certspotter,sfp_virustotal,sfp_shodan"

# Social media and people
SOCIAL_MODULES="sfp_twitter,sfp_linkedin,sfp_instagram,sfp_github,sfp_keybase"

# Breach and leaked data
BREACH_MODULES="sfp_haveibeenpwned,sfp_dehashed,sfp_leakix,sfp_intelx"

# Dark web
DARKWEB_MODULES="sfp_torch,sfp_ahmia,sfp_onionsearchengine"

# Geolocation
GEO_MODULES="sfp_ipinfo,sfp_maxmind,sfp_abstractapi"

# Malware / threat intel
THREAT_MODULES="sfp_virustotal,sfp_threatcrowd,sfp_abuseipdb,sfp_maltiverse"

# Run a focused infrastructure scan
python3 sf.py -s example.com -t INTERNET_NAME \
  -m "$PASSIVE_DNS_MODULES,$SUBDOMAIN_MODULES" \
  -o json -f infra_scan.json
```

### Step 5: Parse JSON output programmatically

```python
import json
import subprocess
from collections import defaultdict

def run_spiderfoot_scan(target, target_type="INTERNET_NAME", modules=None, output_file=None):
    """Run a SpiderFoot CLI scan and return parsed results."""
    if output_file is None:
        output_file = f"sf_{target.replace('.', '_').replace('@', '_at_')}.json"

    if modules is None:
        modules = "sfp_dnsresolve,sfp_dnsdumpster,sfp_certspotter,sfp_whois,sfp_shodan"

    cmd = [
        "python3", "sf.py",
        "-s", target,
        "-t", target_type,
        "-m", modules,
        "-o", "json",
        "-f", output_file,
    ]

    print(f"Starting SpiderFoot scan: {target} ({target_type})")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd="./spiderfoot")
    if result.returncode != 0:
        print(f"Warning: {result.stderr[:500]}")

    return parse_sf_output(output_file)

def parse_sf_output(json_file):
    """Parse SpiderFoot JSON output and categorize findings."""
    try:
        with open(json_file) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not parse output: {e}")
        return {}

    # SpiderFoot output is a list of [type, source, data, confidence, ...]
    findings = defaultdict(list)
    for row in data:
        if len(row) >= 3:
            event_type = row[0]
            source = row[1]
            value = row[2]
            findings[event_type].append({"value": value, "source": source})

    return dict(findings)

def summarize_findings(findings):
    """Print a summary of SpiderFoot scan results."""
    priority_types = [
        "EMAILADDR", "INTERNET_NAME", "IP_ADDRESS", "PHONE_NUMBER",
        "USERNAME", "LINKEDIN_URL", "TWITTER_URL", "GITHUB_URL",
        "LEAKEDDATA", "HACKED_EMAIL", "VULNERABILITY_CVE_CRITICAL",
        "VULNERABILITY_CVE_HIGH", "SSL_CERTIFICATE_MISMATCH",
    ]

    print("\n=== SpiderFoot Scan Summary ===")
    for event_type in priority_types:
        items = findings.get(event_type, [])
        if items:
            print(f"\n{event_type} ({len(items)}):")
            for item in items[:10]:
                print(f"  {item['value']}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more")

    print(f"\nAll event types found: {sorted(findings.keys())}")
    print(f"Total events: {sum(len(v) for v in findings.values())}")

# Example usage
findings = run_spiderfoot_scan(
    "example.com",
    target_type="INTERNET_NAME",
    modules="sfp_dnsresolve,sfp_certspotter,sfp_haveibeenpwned,sfp_shodan,sfp_whois"
)
summarize_findings(findings)
```

### Step 6: Configure API keys in SpiderFoot

```bash
# Via Web UI: Settings → API Keys → enter keys for each module

# Via config file (~/.spiderfoot/spiderfoot.cfg or sf.cfg)
# Key settings to configure:
# sfp_shodan → shodan_api_key
# sfp_virustotal → virustotal_api_key
# sfp_haveibeenpwned → hibp_api_key
# sfp_hunter → hunter_api_key
# sfp_securitytrails → securitytrails_api_key
# sfp_censys → censys_api_id + censys_api_secret
# sfp_ipinfo → ipinfo_api_key
```

### Step 7: Use the REST API for automation

```python
import requests
import time

SPIDERFOOT_URL = "http://127.0.0.1:5001"

def create_scan_via_api(target, scan_name, modules="sfp_dnsresolve,sfp_certspotter"):
    """Create and start a SpiderFoot scan via the REST API."""
    resp = requests.post(f"{SPIDERFOOT_URL}/startscan", data={
        "scanname": scan_name,
        "scantarget": target,
        "scantype": "INTERNET_NAME",
        "modulelist": modules,
        "typelist": "",
    })
    if resp.status_code == 200:
        scan_id = resp.json().get("id")
        print(f"Scan started: {scan_id}")
        return scan_id
    raise Exception(f"Failed to create scan: {resp.text}")

def wait_for_scan(scan_id, poll_interval=30):
    """Poll until scan completes."""
    while True:
        resp = requests.get(f"{SPIDERFOOT_URL}/scanopts?id={scan_id}")
        status = resp.json().get("status", "")
        print(f"Status: {status}")
        if status in ("FINISHED", "FAILED", "ABORTED"):
            return status
        time.sleep(poll_interval)

def get_scan_results(scan_id):
    """Fetch all results for a completed scan."""
    resp = requests.get(f"{SPIDERFOOT_URL}/scaneventresults?id={scan_id}&eventType=ALL")
    return resp.json()

scan_id = create_scan_via_api("example.com", "Example Corp Scan")
status = wait_for_scan(scan_id)
if status == "FINISHED":
    results = get_scan_results(scan_id)
    print(f"Got {len(results)} findings")
```

## Common SpiderFoot Modules Reference

| Module | Purpose |
|--------|---------|
| `sfp_dnsresolve` | DNS resolution for discovered hosts |
| `sfp_dnsdumpster` | Passive DNS history lookup |
| `sfp_certspotter` | Certificate transparency log search |
| `sfp_shodan` | Query Shodan for host information |
| `sfp_virustotal` | VirusTotal domain/IP/file reputation |
| `sfp_haveibeenpwned` | Check emails in breach database |
| `sfp_whois` | WHOIS lookup for domains |
| `sfp_hunter` | Hunter.io email discovery |
| `sfp_linkedin` | LinkedIn profile search |
| `sfp_twitter` | Twitter/X profile lookup |
| `sfp_github` | GitHub user and code search |
| `sfp_abuseipdb` | IP abuse score lookup |
| `sfp_threatcrowd` | Threat intelligence correlation |
| `sfp_leakix` | LeakIX exposed service data |

## Guidelines

- **Module selection matters**: Running all 200+ modules against a target takes hours and consumes significant API credits. Select focused module sets for specific investigative goals.
- **API keys**: Many modules are no-ops without API keys. Configure at least Shodan, VirusTotal, and HIBP for meaningful results.
- **Correlation is the superpower**: SpiderFoot's unique value is automatically chaining discoveries. Let it run fully on a focused set of modules rather than stopping it early.
- **Legal notice**: SpiderFoot should only be used on targets you have authorization to investigate. Even passive OSINT may violate terms of service of some data providers.
- **Dark web modules**: Modules like `sfp_torch` require Tor to be running locally (`tor` service on port 9050).
