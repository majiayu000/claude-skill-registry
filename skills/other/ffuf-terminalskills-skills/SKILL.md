---
name: ffuf
description: >-
  Discover hidden content, directories, subdomains, and API endpoints with ffuf —
  the fastest web fuzzer. Use when someone asks to "find hidden directories",
  "fuzz URLs", "discover API endpoints", "subdomain enumeration", "content
  discovery", "ffuf", "brute force paths", or "find hidden files on a website".
  Covers directory fuzzing, parameter fuzzing, subdomain discovery, virtual host
  enumeration, and recursive scanning.
license: Apache-2.0
compatibility: "Any OS. Go binary."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["security", "fuzzing", "recon", "ffuf", "content-discovery"]
---

# ffuf (Fuzz Faster U Fool)

## Overview

ffuf is the fastest web fuzzer available — written in Go, it discovers hidden files, directories, subdomains, and API endpoints by sending thousands of requests with wordlist-based payloads. Unlike dirbuster or gobuster, ffuf supports multiple fuzzing positions (URL, headers, POST body, cookies), response filtering, and recursive scanning.

## When to Use

- Discovering hidden directories and files on web servers
- Finding undocumented API endpoints
- Subdomain and virtual host enumeration
- Parameter discovery (GET/POST)
- Bug bounty reconnaissance
- Pre-pentest content discovery

## Instructions

### Setup

```bash
# Install
go install github.com/ffuf/ffuf/v2@latest

# Or download binary
wget https://github.com/ffuf/ffuf/releases/latest/download/ffuf_linux_amd64.tar.gz
tar xzf ffuf_linux_amd64.tar.gz

# Get wordlists (SecLists is the standard)
git clone --depth 1 https://github.com/danielmiessler/SecLists.git
```

### Directory Discovery

```bash
# Basic directory fuzzing — FUZZ keyword marks the injection point
ffuf -u https://target.com/FUZZ -w SecLists/Discovery/Web-Content/common.txt

# Filter by response code (ignore 404s)
ffuf -u https://target.com/FUZZ -w common.txt -fc 404

# Filter by response size (remove default pages)
ffuf -u https://target.com/FUZZ -w common.txt -fs 4242

# Match only specific codes
ffuf -u https://target.com/FUZZ -w common.txt -mc 200,301,302,403

# Recursive scanning — follow discovered directories
ffuf -u https://target.com/FUZZ -w common.txt -recursion -recursion-depth 2

# With extensions
ffuf -u https://target.com/FUZZ -w common.txt -e .php,.bak,.old,.txt,.json,.env
```

### Subdomain Discovery

```bash
# Subdomain fuzzing via DNS
ffuf -u https://FUZZ.target.com -w SecLists/Discovery/DNS/subdomains-top1million-5000.txt -fc 404

# Virtual host discovery (different from DNS — checks Host header)
ffuf -u https://target.com -w subdomains.txt -H "Host: FUZZ.target.com" -fs 1234
```

### API Endpoint Discovery

```bash
# REST API path fuzzing
ffuf -u https://api.target.com/v1/FUZZ -w SecLists/Discovery/Web-Content/api/api-endpoints.txt -mc 200,401,403

# API with authentication
ffuf -u https://api.target.com/v1/FUZZ -w api-endpoints.txt \
  -H "Authorization: Bearer eyJhbG..." -mc 200

# Parameter fuzzing (GET)
ffuf -u "https://target.com/api/users?FUZZ=value" -w SecLists/Discovery/Web-Content/burp-parameter-names.txt -fs 0

# POST body parameter fuzzing
ffuf -u https://target.com/api/login -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","FUZZ":"test"}' \
  -w params.txt -fc 400
```

### Advanced Usage

```bash
# Multiple wordlists (two FUZZ positions: W1 and W2)
ffuf -u https://target.com/W1/W2 -w endpoints.txt:W1 -w ids.txt:W2

# Output to JSON for automation
ffuf -u https://target.com/FUZZ -w common.txt -o results.json -of json

# Throttled scanning (polite)
ffuf -u https://target.com/FUZZ -w common.txt -rate 50 -t 10

# Custom match on response body
ffuf -u https://target.com/FUZZ -w common.txt -mr "admin|dashboard|config"
```

## Examples

### Example 1: Full recon on a new target

**User prompt:** "I have permission to pentest example.com. Start with content discovery."

The agent will run ffuf for directory discovery with common.txt, then check for backup files (.bak, .old, .sql), hidden API endpoints, and admin panels.

### Example 2: Find hidden API endpoints

**User prompt:** "Our API has undocumented endpoints left by previous developers. Find them."

The agent will fuzz API paths with REST-specific wordlists, try common API versioning patterns (/v1/, /v2/), and check HTTP methods (GET, POST, PUT, DELETE) on discovered endpoints.

## Guidelines

- **ALWAYS have authorization** — fuzzing without permission is illegal
- **Start with common.txt** — then escalate to bigger wordlists if needed
- **Filter noise first** — use `-fc 404` or `-fs <size>` to remove false positives
- **Rate limit** — `-rate 50` for production targets, unlimited for local/staging
- **FUZZ is the keyword** — place it wherever you want to inject wordlist entries
- **Extensions matter** — `-e .php,.bak,.env` catches backup and config files
- **JSON output for automation** — `-o results.json -of json` for pipeline integration
- **Recursive with caution** — `-recursion-depth 2` max to avoid infinite loops
- **SecLists is essential** — the standard wordlist collection for web fuzzing
