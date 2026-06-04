---
name: asset-discovery
description: Probe subdomain list with httpx/dnsx/naabu to identify live hosts, open ports, status codes, titles, and basic fingerprints. Use after subdomain-enum produces a sub list. Output feeds into fingerprinting and content discovery.
metadata:
  type: skill
  phase: recon
  tools: [httpx, dnsx, naabu, masscan, nmap]
---

# Asset Discovery (Live Host Probing)

> 1000 subdomains in → 80 living web apps + 14 open APIs out.

## When to invoke

**Trigger phrases:**
- "probe with httpx"
- "find live hosts"
- "which subs are alive"
- "port scan in-scope assets"

## Pipeline overview

```
subdomains.txt
     │
     ▼
  ┌─────────┐
  │  dnsx   │  resolve to A/CNAME/MX (drop dead ones)
  └────┬────┘
       │
       ▼
  ┌──────────┐
  │  naabu   │  port scan (top 1000 + custom)
  └─────┬────┘
        │
        ▼
  ┌───────┐
  │ httpx │  HTTP probe — status, title, tech, headers
  └───┬───┘
      │
      ▼
  live.txt (with rich metadata)
```

## Step-by-Step Workflow

### 1. DNS resolution (filter dead subs)

```bash
TARGET="target.com"
OUT="loot/$TARGET"

# dnsx — resolve A, CNAME, drop unresolvable
cat "$OUT/subs/in-scope.txt" | dnsx -silent -a -resp > "$OUT/resolved.txt"

# Just the hostname (no IPs):
cat "$OUT/subs/in-scope.txt" | dnsx -silent > "$OUT/alive-dns.txt"
```

### 2. Port scanning

```bash
# naabu — top 1000 ports, fast SYN scan (requires root for SYN; non-root falls back to connect)
naabu -list "$OUT/alive-dns.txt" -top-ports 1000 -rate 5000 -silent -o "$OUT/ports.txt"

# Or specific ports common for web targets
naabu -list "$OUT/alive-dns.txt" -p 80,443,8080,8443,3000,5000,8000,8888,9000,9443 \
    -rate 5000 -silent -o "$OUT/web-ports.txt"

# For comprehensive (slow): all ports
# naabu -list "$OUT/alive-dns.txt" -p - -rate 2000 -silent -o "$OUT/all-ports.txt"
```

**For deeper service detection on found ports, use nmap follow-up:**
```bash
# Convert naabu output to nmap input
cat "$OUT/ports.txt" | awk -F: '{print $1}' | sort -u > "$OUT/hosts-with-open-ports.txt"

# Service version + scripts (slower, run after naabu narrows)
nmap -sV -sC -p- -Pn --min-rate 1000 -iL "$OUT/hosts-with-open-ports.txt" -oN "$OUT/nmap.txt"
```

### 3. HTTP probing (the goldmine)

```bash
# httpx — comprehensive HTTP probe
cat "$OUT/ports.txt" | httpx \
    -silent \
    -status-code \
    -title \
    -tech-detect \
    -location \
    -content-length \
    -web-server \
    -ip \
    -cname \
    -tls-grab \
    -follow-redirects \
    -timeout 10 \
    -retries 2 \
    -threads 50 \
    -json \
    -o "$OUT/httpx.jsonl"

# Plain text version for quick review
cat "$OUT/ports.txt" | httpx -silent -status-code -title -tech-detect \
    -location -web-server -timeout 10 \
    -o "$OUT/live.txt"
```

### 4. Extract focus targets

```bash
# Only 200/30x responses (avoid 404 noise)
cat "$OUT/httpx.jsonl" | jq -r 'select(.status_code | tostring | startswith("2") or startswith("3")) | .url' > "$OUT/live-2xx-3xx.txt"

# Hosts running interesting tech
cat "$OUT/httpx.jsonl" | jq -r 'select(.tech | tostring | test("Jenkins|GitLab|phpMyAdmin|Spring|GraphQL|Swagger|Kubernetes|Grafana|Elasticsearch|Kibana"; "i")) | .url' > "$OUT/interesting-tech.txt"

# All API-looking endpoints
cat "$OUT/httpx.jsonl" | jq -r '.url' | grep -iE 'api|graphql|v1|v2|v3|swagger|openapi|docs' > "$OUT/api-candidates.txt"

# Admin/dashboard candidates
cat "$OUT/httpx.jsonl" | jq -r '.url' | grep -iE 'admin|dashboard|portal|console|manage|internal' > "$OUT/admin-candidates.txt"
```

### 5. Screenshot (visual triage)

```bash
# httpx can screenshot live URLs
cat "$OUT/live-2xx-3xx.txt" | httpx -screenshot -silent -srd "$OUT/screenshots/"

# Or use eyewitness/gowitness for a gallery
# go install github.com/sensepost/gowitness@latest
gowitness file -f "$OUT/live-2xx-3xx.txt" --screenshot-path "$OUT/screenshots/"
gowitness report serve  # opens browser
```

## Output structure

```
loot/target.com/
├── subs/in-scope.txt          (from subdomain-enum)
├── resolved.txt               (DNS-resolved only)
├── ports.txt                  (host:port format)
├── nmap.txt                   (service versions)
├── httpx.jsonl                (rich metadata, one JSON per line)
├── live.txt                   (plain status+title+tech)
├── live-2xx-3xx.txt          (URLs that respond OK)
├── interesting-tech.txt       (Jenkins, etc.)
├── api-candidates.txt
├── admin-candidates.txt
└── screenshots/
    └── *.png
```

## Quick filters

```bash
# Status code 200 only
cat httpx.jsonl | jq -r 'select(.status_code == 200) | .url'

# Sort by content length (find clusters / outliers)
cat httpx.jsonl | jq -r '"\(.content_length // 0) \(.url)"' | sort -n

# Group by tech
cat httpx.jsonl | jq -r '.tech[]?' | sort | uniq -c | sort -rn

# Find non-target IPs (might indicate misconfig)
cat httpx.jsonl | jq -r '"\(.host) \(.a[]?)"' | grep -v "^target"

# Hosts behind Cloudflare (or other CDNs)
cat httpx.jsonl | jq -r 'select(.cdn) | .url'
```

## High-value patterns to highlight

These almost always lead to bugs:

```bash
# 403s might be reachable with different path
cat httpx.jsonl | jq -r 'select(.status_code == 403) | .url'

# 401 — auth required, may be bypassable
cat httpx.jsonl | jq -r 'select(.status_code == 401) | .url'

# 500 — error pages may leak info
cat httpx.jsonl | jq -r 'select(.status_code == 500) | .url'

# Long redirect chains may have open redirect
cat httpx.jsonl | jq -r 'select(.chain | length > 2) | .url'

# Default credentials candidates (login pages on uncommon hosts)
cat httpx.jsonl | jq -r 'select(.title | test("login|sign in|admin"; "i")) | .url'
```

## Cross-references

- `[[subdomain-enum]]` — feeds this skill
- `[[fingerprinting]]` — deeper tech ID per host
- `[[content-discovery]]` — fuzz paths on live hosts
- `[[subdomain-takeover]]` — check dangling CNAMEs in resolved.txt

## Common pitfalls

1. **Probing only 80/443.** Miss admin panels on 8080/8443/3000/etc.
2. **Following redirects blindly.** Sometimes a redirect chain has the bug.
3. **Ignoring 403/401 hosts.** Often reachable with path manipulation or auth bypass.
4. **Not screenshotting.** Visual triage finds login portals you'd miss in JSON.
5. **Including OOS in probe input.** Always filter before httpx — saves traffic and avoids violations.

## Speed tuning

- `-threads 50` is safe; `-threads 100+` for very large lists
- `-timeout 10` is generous; reduce to 5 for fast scanning
- `-rate-limit-minute` on httpx for stealth
- Naabu `-rate 5000` is fast but loud; reduce to 1000 for stealth

## Don't forget non-HTTP services

Even though we're hunting web, note these from nmap output:
- **22 (SSH)** — version disclosure, weak keys
- **25/465/587 (SMTP)** — open relay, user enum
- **3306 (MySQL)** — public DB (rare but found)
- **6379 (Redis)** — unauth access
- **9200 (Elasticsearch)** — unauth
- **27017 (MongoDB)** — unauth

If found, these may be high-impact in their own right (subject to scope).
