---
name: theharvester
description: >-
  Passive email, subdomain, and IP harvesting from public sources using theHarvester. Use when:
  gathering corporate email lists, enumerating subdomains passively, pre-engagement recon, finding
  exposed employee contacts without triggering alerts.
license: Apache-2.0
compatibility: "Python 3.9+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: research
  tags: [theharvester, email, subdomain, passive, harvesting]
  use-cases:
    - "Harvest all email addresses for a target domain from public sources"
    - "Enumerate subdomains passively before an authorized penetration test"
    - "Find employee contacts via LinkedIn, Hunter, and search engines"
    - "Gather IP ranges and hostnames associated with an organization"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# theHarvester

## Overview

theHarvester is a passive OSINT tool that aggregates information about a target domain from multiple public sources. It finds email addresses, subdomains, hostnames, and IP ranges without making any direct requests to the target — making it ideal for stealth recon during the pre-engagement phase of penetration tests or OSINT investigations.

**Sources include:** Google, Bing, DuckDuckGo, LinkedIn, Shodan, Hunter.io, CertSpotter, DNSDumpster, VirusTotal, and more.

## Instructions

### Step 1: Install theHarvester

```bash
# Option 1: pip (in a virtual environment recommended)
pip install theHarvester

# Option 2: Clone from GitHub (most up-to-date)
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip install -r requirements/base.txt

# Option 3: Docker
docker pull ghcr.io/laramies/theharvester
docker run ghcr.io/laramies/theharvester -d example.com -b google
```

### Step 2: Basic usage

```bash
# Syntax: theHarvester -d <domain> -b <source> [options]
# -d  target domain
# -b  data source(s)
# -l  limit results (default: 500)
# -f  output filename (supports XML and JSON)
# -n  DNS lookup on discovered hosts
# -v  verify host via DNS resolution

# Search a single source
theHarvester -d example.com -b google

# Search all available sources
theHarvester -d example.com -b all

# Limit results, enable DNS lookup, save output
theHarvester -d example.com -b google,bing,linkedin -l 200 -n -f results_example

# Run from cloned repo
python3 theHarvester.py -d example.com -b all -l 500 -f output
```

### Step 3: Choose sources strategically

```bash
# Email harvesting — best sources
theHarvester -d example.com -b google,bing,hunter,linkedin

# Subdomain enumeration — best sources
theHarvester -d example.com -b certspotter,dnsdumpster,virustotal,shodan

# Comprehensive (slower, uses all sources)
theHarvester -d example.com -b all -l 1000 -f full_recon_example

# LinkedIn employee discovery (requires LinkedIn API key in api-keys.yaml)
theHarvester -d example.com -b linkedin -l 200
```

### Step 4: Configure API keys

```yaml
# api-keys.yaml (place in theHarvester directory or specify with -c flag)
apikeys:
  hunter:
    key: YOUR_HUNTER_IO_KEY
  shodan:
    key: YOUR_SHODAN_KEY
  virustotal:
    key: YOUR_VIRUSTOTAL_KEY
  binaryedge:
    key: YOUR_BINARYEDGE_KEY
  fullhunt:
    key: YOUR_FULLHUNT_KEY
  securityTrails:
    key: YOUR_SECURITYTRAILS_KEY
  github:
    key: YOUR_GITHUB_TOKEN
```

### Step 5: Parse and process output with Python

```python
import json
import subprocess
import re

def run_harvester(domain, sources="google,bing,certspotter,dnsdumpster", limit=500):
    """Run theHarvester and return parsed results."""
    output_file = f"harvester_{domain.replace('.', '_')}"
    cmd = [
        "theHarvester",
        "-d", domain,
        "-b", sources,
        "-l", str(limit),
        "-f", output_file,
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    print(result.stdout)

    # Parse JSON output
    json_file = f"{output_file}.json"
    try:
        with open(json_file) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Fall back to parsing stdout
        return parse_stdout(result.stdout)

def parse_stdout(output):
    """Extract emails, hosts, and IPs from raw stdout."""
    emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', output))
    # Filter out false positives
    emails = {e for e in emails if not e.endswith(('.png', '.jpg', '.css', '.js'))}

    hosts = set(re.findall(r'[\w\.-]+\.\w{2,}', output))
    ips = set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', output))

    return {"emails": list(emails), "hosts": list(hosts), "ips": list(ips)}

def deduplicate_and_report(data, domain):
    """Clean and summarize harvested data."""
    emails = sorted(set(data.get("emails", [])))
    hosts = sorted(set(data.get("hosts", [])))
    ips = sorted(set(data.get("ips", [])))

    # Filter to target domain
    domain_emails = [e for e in emails if domain in e]
    domain_hosts = [h for h in hosts if domain in h]

    print(f"\n=== Harvest Report: {domain} ===")
    print(f"Emails found:    {len(domain_emails)}")
    print(f"Subdomains:      {len(domain_hosts)}")
    print(f"IP addresses:    {len(ips)}")

    if domain_emails:
        print("\nEmails:")
        for e in domain_emails[:20]:
            print(f"  {e}")

    if domain_hosts:
        print("\nSubdomains:")
        for h in domain_hosts[:20]:
            print(f"  {h}")

    return {
        "emails": domain_emails,
        "subdomains": domain_hosts,
        "ips": ips,
    }

# Usage
results = run_harvester("target-company.com", sources="google,bing,certspotter,hunter")
clean = deduplicate_and_report(results, "target-company.com")

# Save cleaned results
with open("clean_results.json", "w") as f:
    json.dump(clean, f, indent=2)
```

### Step 6: Combine with other tools

```bash
# Pass discovered subdomains to nmap (only with explicit authorization)
theHarvester -d example.com -b all -f hosts
cat hosts.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for host in data.get('hosts', []):
    print(host)
" > subdomains.txt

# Feed subdomains into amass for deeper DNS enumeration
cat subdomains.txt | amass enum -df - -passive

# Check emails against breach databases
cat emails.txt | while read email; do
    curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/$email" \
         -H "hibp-api-key: YOUR_HIBP_KEY"
done
```

## Available Sources Reference

| Source | Data Type | API Key Required |
|--------|-----------|-----------------|
| `google` | Emails, subdomains | No |
| `bing` | Emails, subdomains | No |
| `duckduckgo` | Emails, subdomains | No |
| `linkedin` | Employees, emails | Optional |
| `hunter` | Emails | Yes |
| `certspotter` | Subdomains (SSL certs) | No |
| `dnsdumpster` | Subdomains, IPs | No |
| `virustotal` | Subdomains | Yes |
| `shodan` | IPs, open ports | Yes |
| `securitytrails` | Subdomains, DNS | Yes |
| `github` | Emails, code | Yes |
| `binaryedge` | IPs, services | Yes |

## Guidelines

- **Always get authorization** before running theHarvester against a target — passive does not mean invisible. Data queries may be logged by third-party services.
- **Rate limits**: Without API keys, theHarvester relies on scraping search engines which may throttle or block requests. Add API keys for reliable results.
- **Combine sources**: No single source is complete. Use multiple sources and deduplicate.
- **Email format detection**: Once you have a few emails (e.g., `jsmith@corp.com`, `john.smith@corp.com`), infer the naming convention and use it to generate a target list.
- **DNS verification**: Always use `-n` or `-v` to verify discovered hosts are live before reporting.
