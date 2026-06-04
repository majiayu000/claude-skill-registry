---
name: content-discovery
description: Fuzz directories, files, and parameters using ffuf, feroxbuster, arjun, paramspider, and x8. Use when the user has live hosts and needs to find hidden routes, backup files, exposed configs, and untracked URL parameters.
metadata:
  type: skill
  phase: recon
  tools: [ffuf, feroxbuster, dirsearch, arjun, paramspider, x8, gobuster]
---

# Content Discovery & Parameter Mining

> The hidden `/admin/v2/internal/` route is the bug. Find it.

## When to invoke

**Trigger phrases:**
- "fuzz directories"
- "find hidden paths"
- "discover parameters"
- "ffuf this"
- "directory brute force"

## Two-stage approach

```
STAGE 1: Path discovery        STAGE 2: Parameter mining
┌─────────────────┐            ┌─────────────────┐
│ ffuf / ferox    │            │ arjun           │
│ Find hidden     │  ────►     │ paramspider     │
│ paths, files    │            │ x8              │
│                 │            │ Find params on  │
└─────────────────┘            │ found endpoints │
                               └─────────────────┘
```

## Stage 1: Directory & file fuzzing

### A. ffuf — fast, scriptable

```bash
TARGET="https://app.target.com"
OUT="loot/$(echo $TARGET | sed 's|https://||')/fuzz"
mkdir -p "$OUT"

# Standard run
ffuf -u "$TARGET/FUZZ" \
    -w ~/tools/SecLists/Discovery/Web-Content/raft-large-directories.txt \
    -c -mc 200,204,301,302,307,401,403 \
    -fc 404 \
    -t 50 \
    -o "$OUT/ffuf-dirs.json" -of json

# Filter common false positives (size-based)
ffuf -u "$TARGET/FUZZ" -w wordlist.txt -fs 1234,5678 -c

# Extensions for files
ffuf -u "$TARGET/FUZZ" \
    -w ~/tools/SecLists/Discovery/Web-Content/raft-medium-files.txt \
    -e .php,.bak,.old,.zip,.tar.gz,.sql,.env,.json,.yml,.yaml,.config \
    -c -mc 200,204,301,302,307,401,403 \
    -o "$OUT/ffuf-files.json" -of json
```

### B. feroxbuster — recursive, robust

```bash
feroxbuster -u "$TARGET" \
    -w ~/tools/SecLists/Discovery/Web-Content/raft-large-directories.txt \
    -r \
    -s 200,204,301,302,401,403 \
    -t 50 \
    -d 3 \
    -o "$OUT/ferox.txt"

# With extensions
feroxbuster -u "$TARGET" \
    -w wordlist.txt \
    -x .php,.bak,.zip,.env,.json \
    -r -d 2 -t 30 \
    -o "$OUT/ferox-ext.txt"
```

### C. dirsearch — Python alternative

```bash
dirsearch -u "$TARGET" \
    -w ~/tools/SecLists/Discovery/Web-Content/raft-large-directories.txt \
    -e bak,old,zip,env,sql \
    -t 30 \
    -x 404 \
    -o "$OUT/dirsearch.txt"
```

## Wordlist strategy (CRITICAL)

Default wordlists find what everyone finds. **Layer wordlists** for maximum coverage:

```bash
# Layer 1: standard
~/tools/SecLists/Discovery/Web-Content/raft-large-directories.txt

# Layer 2: assetnote (modern, big)
~/tools/assetnote-wordlists/data/manual/httparchive_directories_1m.txt

# Layer 3: tech-specific (after fingerprinting)
# If WordPress:
~/tools/SecLists/Discovery/Web-Content/CMS/wordpress.txt
# If Spring Boot:
~/tools/SecLists/Discovery/Web-Content/spring-boot.txt
# If API discovery:
~/tools/SecLists/Discovery/Web-Content/api/api-endpoints-mazen160.txt

# Layer 4: target-specific (from JS-mined endpoints)
cat loot/target/js/endpoints.txt | unfurl paths | sort -u > target-custom.txt
ffuf -u "$TARGET/FUZZ" -w target-custom.txt -c
```

## High-value paths to always include

Always test these even if not in wordlist:

```bash
HIGH_VALUE=(
    /.env
    /.git/config
    /.git/HEAD
    /.git/logs/HEAD
    /.DS_Store
    /server-status
    /server-info
    /swagger.json
    /swagger-ui/
    /api-docs
    /openapi.json
    /openapi.yaml
    /actuator           # Spring Boot
    /actuator/env       # Spring Boot CRITICAL
    /actuator/heapdump  # Spring Boot CRITICAL
    /actuator/health
    /metrics
    /debug
    /trace
    /phpinfo.php
    /info.php
    /wp-config.php.bak
    /robots.txt
    /sitemap.xml
    /security.txt
    /.well-known/security.txt
    /backup.zip
    /backup.tar.gz
    /db.sql
    /database.sql
    /dump.sql
    /api/v1
    /api/v2
    /api/v3
    /graphql
    /graphiql
    /__graphql
    /api/graphql
    /v1/graphql
    /admin
    /administrator
    /admin.php
    /wp-admin
    /console
    /jolokia            # Spring Boot mgmt
    /env
    /heapdump
    /threaddump
    /loggers
    /h2-console         # H2 DB console
)

for path in "${HIGH_VALUE[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$path")
    if [[ "$code" != "404" ]]; then
        echo "[$code] $TARGET$path"
    fi
done
```

## Stage 2: Parameter discovery

### A. Arjun — fast HTTP parameter discovery

```bash
# Single endpoint
arjun -u "$TARGET/api/v3/search" -m GET -oJ "$OUT/arjun-search.json"

# Multiple endpoints
arjun -i endpoints-live.txt -m GET -oJ "$OUT/arjun-bulk.json"

# POST endpoints (try JSON body)
arjun -u "$TARGET/api/v3/user" -m JSON -oJ "$OUT/arjun-user-post.json"

# Headers — arjun can probe header parameters too
arjun -u "$TARGET/api/v3/order" --headers -oJ "$OUT/arjun-headers.json"
```

### B. paramspider — mine historical params

```bash
paramspider -d target.com --level high -o "$OUT/paramspider.txt"

# Output is URL with FUZZ in each param position — pipe to ffuf or scanners
```

### C. x8 — modern, fast, Rust-based

```bash
# Install: cargo install x8
x8 -u "$TARGET/api/v3/user" -w ~/tools/SecLists/Discovery/Web-Content/burp-parameter-names.txt
```

### D. Manual discovery — from JS bundles

```bash
# From js-analysis output, extract parameter-like strings
grep -hoE '"[a-zA-Z_][a-zA-Z_0-9]{2,30}"\s*:' loot/target/js/files/*.js | \
    sed 's/[":]//g' | sort -u > "$OUT/params-from-js.txt"

# Use as ffuf input
ffuf -u "$TARGET/api/v3/search?FUZZ=test" -w "$OUT/params-from-js.txt" -c -mc 200 -fc 404
```

## Recursion strategy

Found `/admin/`? Recurse. Found `/api/`? Recurse.

```bash
# feroxbuster does this natively with -r and -d
feroxbuster -u "$TARGET" -w wordlist.txt -r -d 4 -t 30

# ffuf needs scripting — but you can chain:
ffuf -u "$TARGET/FUZZ" -w wordlist.txt -mc 200,401,403 -o run1.json
# Extract found dirs from run1, then:
cat run1.json | jq -r '.results[] | select(.status==200 or .status==403) | .url' | \
    while read dir; do
        ffuf -u "${dir}/FUZZ" -w wordlist.txt -mc 200,401,403 -o "$OUT/$(basename $dir).json"
    done
```

## VHost / subdomain discovery via fuzzing

If you suspect more apps behind same IP:

```bash
# Fuzz Host header
ffuf -u "$TARGET" -H "Host: FUZZ.target.com" \
    -w ~/tools/SecLists/Discovery/DNS/subdomains-top1million-110000.txt \
    -fs 1234 \
    -mc 200,301,302
```

## API enumeration with kiterunner

Modern API discovery (uses semantic patterns, not just brute):

```bash
# kiterunner uses massive seed lists of real API routes
kr scan "$TARGET" -A=apiroutes-240528 -o "$OUT/kr.txt"

# Or against the live list
kr scan -A=apiroutes-240528 endpoints-live.txt -o "$OUT/kr.txt"
```

## Output template

```
loot/target.com/fuzz/
├── ffuf-dirs.json
├── ffuf-files.json
├── ferox.txt
├── dirsearch.txt
├── arjun-bulk.json
├── paramspider.txt
├── params-from-js.txt
├── kr.txt
└── interesting/
    ├── 403-endpoints.txt        ← potential auth bypass
    ├── 401-endpoints.txt        ← protected, may have leaks
    ├── 500-endpoints.txt        ← error pages → info disclosure
    └── files-exposed.txt        ← .env, .git, swagger, etc.
```

## Triaging results

After fuzzing, focus on:

1. **5xx responses** — server errors often leak stack traces, hostnames, paths.
2. **403 responses** — try path canonicalization tricks (`//admin`, `/admin/./`, `/admin..;/`).
3. **401 responses** — protected → can you bypass? See `[[auth-bypass]]`.
4. **200 responses on unexpected paths** — may be admin/internal.
5. **Different content-length on common endpoints** — fingerprints variants.

## Cross-references

- `[[asset-discovery]]` — provides live host list
- `[[js-analysis]]` — feeds custom param/path lists
- `[[fingerprinting]]` — choose tech-specific wordlists
- `[[auth-bypass]]` — handle 401/403 findings
- `[[idor-hunting]]` — test parameter discoveries

## Common pitfalls

1. **Default wordlist only.** Misses tech-specific paths.
2. **No size filter.** WAF returns same-size 200 for everything → false positives.
3. **Ignoring 403/401.** Often the most valuable findings.
4. **Not throttling.** 200 threads → blocked or banned.
5. **Skipping extensions.** `.bak`, `.old`, `.zip` are gold mines.

## Speed vs accuracy

| Mode | Threads | Wordlist size | Time | Coverage |
|---|---|---|---|---|
| Stealth | 10 | 10k | 30 min | Medium |
| Standard | 50 | 100k | 1 hr | High |
| Aggressive | 200 | 1M+ | 4+ hr | Maximum |

For most BB programs, **stealth or standard**. Aggressive can trigger WAF / rate limits.

## When fuzzing is forbidden

Some programs say "no automated scanning". You can still:
- Manually test high-value paths (the list above)
- Use JS-mined endpoints (passive discovery)
- Use historical URLs (Wayback / gau)
- Read the program's docs / blog for API hints

Document everything — if scope is unclear, ask the manager.
