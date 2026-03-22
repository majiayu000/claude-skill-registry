---
name: web-recon
description: "Website vulnerability scanner and security audit toolkit. Scan any website for security issues: open ports (nmap), exposed secrets, subdomain enumeration, directory bruteforce, security header scoring, CORS misconfigurations, SSL/TLS analysis, WordPress vulnerabilities, and more. One command, full report. Pentesting and OSINT reconnaissance for web applications."
---

# Web Recon

**All-in-one web security scanner for pentesting, bug bounty, and security audits.**

Scan any target with a single command and get a structured report with findings prioritized by severity. Modular — run the full suite or pick individual steps.

## Why Use This

- **One command** → full security assessment with prioritized findings
- **12 scan modules** — DNS, ports, fingerprinting, subdomains, directories, secrets, vulnerabilities, headers, CORS, SSL, WordPress, Nuclei templates
- **Security header scoring** — instant letter-grade for any site's HTTP security posture
- **Secrets detection** — 459 rules covering AWS, GCP, GitHub, Slack, databases, and more
- **Skips missing tools gracefully** — works with whatever you have installed
- **Resume mode** — pick up where a crashed scan left off
- **JSON + Markdown reports** — machine-readable and human-readable output

## Quick Start

```bash
# Quick scan (recon, fingerprint, secrets, header scoring, report)
scripts/webscan.sh example.com --quick

# Full scan (all 12 steps)
scripts/webscan.sh example.com

# Full scan with JSON output and screenshot
scripts/webscan.sh example.com --json --screenshot

# Resume a crashed scan (skips completed steps)
scripts/webscan.sh example.com --resume

# Single step
scripts/webscan.sh example.com recon
scripts/webscan.sh example.com vulns

# Secrets scan only
scripts/titus-web.sh https://example.com
```

Output: `~/.openclaw/workspace/recon/<domain>/`

## Options

| Flag | Description |
|------|------------|
| `--quick` | Light scan: recon, fingerprint, secrets, vulns, report |
| `--full` | All steps (default) |
| `--json` | Generate `results.json` alongside markdown report |
| `--screenshot` | Capture homepage screenshot |
| `--resume` | Skip steps that already have output files |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SHODAN_API_KEY` | Shodan API key for infrastructure intel (falls back to CLI) |
| `OUTDIR` | Override output directory |

## Scan Modules

| Step | What it does | Tools |
|------|-------------|-------|
| `recon` | DNS records, IP geolocation, port scan, Shodan, Wayback URLs | nmap, dig, Shodan |
| `fingerprint` | HTTP headers, tech stack, WAF detection, CMS check | WhatWeb, wafw00f |
| `subdomains` | Subdomain enumeration + live probing | Subfinder, Amass, httpx |
| `dirs` | Directory and file bruteforce | Gobuster, ffuf |
| `secrets` | Secrets scan + sensitive file checks (30+ paths) | Titus (459 rules) |
| `vulns` | Security header scoring, CORS check, SSL analysis, vulnerability scan | Nikto, custom |
| `wpscan` | WordPress-specific vulnerabilities (auto-skips if not WP) | WPScan |
| `nuclei` | Template-based CVE scanning | Nuclei |
| `ssl` | Full SSL/TLS analysis | testssl |
| `screenshot` | Homepage capture | cutycapt/chromium |
| `report` | Markdown + JSON report generation | — |

## Security Header Scoring

Scores 10 security headers by severity:

| Severity | Points | Headers |
|----------|--------|---------|
| Critical | 30 | Strict-Transport-Security, Content-Security-Policy |
| High | 20 | X-Frame-Options |
| Medium | 10 | X-Content-Type-Options, Referrer-Policy, Permissions-Policy |
| Low | 5 | X-XSS-Protection, COOP, CORP, COEP |

Rating: 🟢 ≥80% · 🟡 ≥50% · 🟠 ≥25% · 🔴 <25%

## Output Structure

```
~/.openclaw/workspace/recon/<domain>/
├── results.md              # Markdown report with executive summary
├── results.json            # Machine-readable report (--json)
├── screenshot.png          # Homepage capture (--screenshot)
├── dns.txt / geo.json      # DNS records, IP geolocation
├── ports.txt               # nmap port scan results
├── shodan.json             # Shodan infrastructure data
├── header-score.txt        # Security header score card
├── cors.txt                # CORS misconfiguration check
├── whatweb.txt / waf.txt   # Tech fingerprint, WAF detection
├── subdomains-live.txt     # Discovered live subdomains
├── dirs.txt                # Discovered directories/files
├── sensitive-files.txt     # Exposed config/backup files
├── titus.txt               # Leaked secrets/API keys
├── nikto.txt / nuclei.txt  # Vulnerability findings
├── ssl.txt                 # SSL/TLS analysis
└── wpscan.txt              # WordPress scan (if applicable)
```

## Review Priority

1. **header-score.txt** — overall security posture at a glance
2. **sensitive-files.txt** — any "FOUND" = critical exposure
3. **cors.txt** — misconfigured CORS = data theft risk
4. **titus.txt** — exposed secrets/API keys
5. **ports.txt** — unexpected open ports
6. **nuclei.txt** — known CVEs
7. **subdomains-live.txt** — forgotten/dev subdomains

## Tool Requirements

See [references/tools.md](references/tools.md) for install instructions. Scripts skip missing tools gracefully — you don't need everything installed to get useful results.

## Wordlists

See [references/wordlists.md](references/wordlists.md). Auto-selects medium wordlists, falls back to smaller if unavailable.
