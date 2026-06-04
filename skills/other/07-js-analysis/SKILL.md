---
name: js-analysis
description: Extract endpoints, secrets, and hidden routes from JavaScript files using LinkFinder, SecretFinder, JSluice, and source-map analysis. Use when the user has live hosts and needs to mine the JS for attack surface that's not visible in the UI.
metadata:
  type: skill
  phase: recon
  tools: [LinkFinder, SecretFinder, JSluice, mantra, getJS, sourcemapper, trufflehog]
---

# JS Analysis (Endpoint & Secret Mining)

> 90% of API endpoints aren't in the navbar — they're in `main.bundle.js`.

## When to invoke

**Trigger phrases:**
- "analyze JS"
- "find endpoints in JS"
- "mine secrets from javascript"
- "extract API from bundle"

## Why JS analysis pays

Modern SPAs (React/Vue/Angular) load **all** their API routes in JavaScript. The UI shows you maybe 10% of the routes — the bundle has 100% of them, including:
- Admin / debug endpoints
- Internal API versions (v1 alongside v2)
- Webhook handlers
- File upload endpoints
- Search backends
- Hardcoded API keys (S3, Stripe, Mapbox, Twilio)
- AWS access keys (still happens in 2026)
- Internal hostnames / IPs
- GraphQL queries with field hints

## Step-by-Step Workflow

### 1. Get all JS file URLs

```bash
TARGET="app.target.com"
OUT="loot/$TARGET/js"
mkdir -p "$OUT"

# Method A: katana crawl with JS extraction
katana -u "https://$TARGET" -d 3 -jc -kf all -silent | \
    grep -E '\.js(\?|$)' | sort -u > "$OUT/js-urls.txt"

# Method B: waybackurls / gau for historical JS
echo "$TARGET" | gau --providers wayback,otx | grep -E '\.js(\?|$)' | sort -u >> "$OUT/js-urls.txt"

# Method C: from httpx-grabbed JS
cat live.txt | httpx -silent -extract-regex 'src="([^"]+\.js[^"]*)"' -no-color | sort -u >> "$OUT/js-urls.txt"

# Dedupe
sort -u "$OUT/js-urls.txt" -o "$OUT/js-urls.txt"
echo "[+] $(wc -l < "$OUT/js-urls.txt") JS files found"
```

### 2. Download JS files locally

```bash
# Parallel download
mkdir -p "$OUT/files"
cat "$OUT/js-urls.txt" | xargs -P 10 -I{} sh -c 'curl -s -L -o "$1/files/$(echo "$2" | md5sum | cut -d" " -f1).js" "$2"' _ "$OUT" {}

# Or with getJS tool
go install github.com/003random/getJS@latest
getJS --url "https://$TARGET" --complete --output "$OUT/files/"
```

### 3. Extract endpoints (LinkFinder)

```bash
# LinkFinder — the standard for endpoint extraction
cd ~/tools/LinkFinder
pip install -r requirements.txt  # one-time

# Process each JS file
while read js; do
    python3 linkfinder.py -i "$js" -o cli
done < "$OUT/js-urls.txt" | sort -u > "$OUT/endpoints-raw.txt"

# Or in one shot with a remote URL list
python3 linkfinder.py -i "https://$TARGET" -d -o cli > "$OUT/endpoints-raw.txt"
```

### 4. Filter & normalize endpoints

```bash
# Remove junk (data:, font references, etc.)
cat "$OUT/endpoints-raw.txt" | \
    grep -vE '\.(png|jpg|gif|svg|woff|ttf|css|map)$' | \
    grep -E '^/?[a-zA-Z0-9_/.-]+' | \
    sort -u > "$OUT/endpoints.txt"

# Convert relative → absolute
awk -v target="https://$TARGET" '
    /^\/(api|v[0-9]|graphql|admin|user)/ { print target $0; next }
    /^https?:/ { print; next }
    { print target "/" $0 }
' "$OUT/endpoints.txt" | sort -u > "$OUT/endpoints-absolute.txt"
```

### 5. Mine secrets (SecretFinder + trufflehog)

```bash
# SecretFinder
cd ~/tools/SecretFinder
while read js; do
    python3 SecretFinder.py -i "$js" -o cli
done < "$OUT/js-urls.txt" | tee "$OUT/secrets-raw.txt"

# trufflehog (more comprehensive)
trufflehog filesystem "$OUT/files/" --json | tee "$OUT/trufflehog.jsonl"

# noseyparker (modern, very thorough)
noseyparker scan --datastore /tmp/np-store "$OUT/files/"
noseyparker report --datastore /tmp/np-store > "$OUT/noseyparker.txt"
```

### 6. JSluice — modern, fast, accurate

```bash
# Install
go install github.com/BishopFox/jsluice/cmd/jsluice@latest

# Per-file analysis
while read js; do
    curl -s "$js" | jsluice urls -
    curl -s "$js" | jsluice secrets -
done < "$OUT/js-urls.txt" > "$OUT/jsluice-output.txt"

# Or full crawl
cat "$OUT/js-urls.txt" | jsluice urls --source - --json > "$OUT/jsluice-urls.jsonl"
cat "$OUT/js-urls.txt" | jsluice secrets --source - --json > "$OUT/jsluice-secrets.jsonl"
```

### 7. Hunt source maps (jackpot if exposed)

```bash
# Check for .map files
cat "$OUT/js-urls.txt" | sed 's/$/.map/' | httpx -silent -mc 200 -o "$OUT/sourcemaps-exposed.txt"

# If found — extract original source
# sourcemapper (Go tool)
go install github.com/denandz/sourcemapper@latest
while read map; do
    sourcemapper -url "$map" -output "$OUT/source/$(basename "$map" .map)"
done < "$OUT/sourcemaps-exposed.txt"

# Original source = full file paths, comments, dev hints — gold
```

### 8. Find hardcoded credentials (focused patterns)

Custom regex set for common BB patterns:

```bash
cat "$OUT/files/"*.js | grep -aoE '(AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{24,}|xox[bpoars]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}|ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|AIza[0-9A-Za-z\-_]{35})' | sort -u
# Patterns:
# AKIA…           → AWS Access Key
# sk_live_…       → Stripe Live Secret
# xox[bpoars]-…   → Slack token
# ghp_…           → GitHub PAT
# AIza…           → Google API Key
```

For a richer regex set, use **gitleaks** with extended config on JS files:
```bash
gitleaks dir --source "$OUT/files/" --config ~/tools/gitleaks-config.toml -r "$OUT/gitleaks-report.json"
```

### 9. Mine GraphQL queries embedded in JS

```bash
# GraphQL operations are often hardcoded — full field/argument names!
grep -hE 'query [A-Za-z]+|mutation [A-Za-z]+' "$OUT/files/"*.js | sort -u > "$OUT/graphql-operations.txt"

# Look for field structures
grep -hoE '{ [a-zA-Z_]+ [a-zA-Z_]+' "$OUT/files/"*.js | head -20
```

### 10. Endpoint validation (which are live?)

```bash
# Probe each found endpoint
cat "$OUT/endpoints-absolute.txt" | httpx -silent -status-code -title -mc 200,201,202,204,301,302,401,403 > "$OUT/endpoints-live.txt"

# 401/403 endpoints — auth needed = potential auth bypass targets
grep -E '401|403' "$OUT/endpoints-live.txt" > "$OUT/endpoints-protected.txt"

# 200 endpoints without auth = potential IDOR / info disclosure
grep '200' "$OUT/endpoints-live.txt" > "$OUT/endpoints-public.txt"
```

## Output template

```
loot/target.com/js/
├── js-urls.txt              (list of all JS files)
├── files/                   (downloaded JS)
│   └── *.js
├── endpoints-raw.txt        (LinkFinder output)
├── endpoints-absolute.txt   (normalized URLs)
├── endpoints-live.txt       (httpx-probed)
├── endpoints-protected.txt  (401/403 — auth bypass candidates)
├── endpoints-public.txt     (200 without auth)
├── secrets-raw.txt          (SecretFinder)
├── trufflehog.jsonl
├── noseyparker.txt
├── jsluice-urls.jsonl
├── jsluice-secrets.jsonl
├── sourcemaps-exposed.txt
├── source/                  (decompiled from source maps if exposed)
└── graphql-operations.txt
```

## High-value findings — what to do next

| Finding | Next skill | Potential payout |
|---|---|---|
| Hardcoded AWS key | `[[cloud-misconfig]]` | $$$$ (S3 access, IAM enum) |
| Exposed source map | Manual code review | $$$ (logic bug treasure) |
| Internal hostname leaked | `[[ssrf]]` | $$$$ |
| Admin endpoint visible but 401 | `[[auth-bypass]]` | $$$$ |
| GraphQL operation names + schema | `[[graphql]]` | $$$$ |
| Stripe / Twilio / etc. test key | Account in their system | $ — verify scope first |
| Postman collection URL | Manual review | $$ — endpoint goldmine |

## Cross-references

- `[[asset-discovery]]` — runs before this
- `[[content-discovery]]` — fuzz endpoints found in JS
- `[[idor-hunting]]` — test discovered API routes for IDOR
- `[[graphql]]` — exploit embedded GraphQL ops
- `[[cloud-misconfig]]` — abuse leaked cloud credentials

## Common pitfalls

1. **Trusting LinkFinder blindly.** It produces false positives (`/foo/bar` inside strings). Validate with httpx.
2. **Ignoring `.map` files.** Source maps are often left exposed by accident — high-value.
3. **Only analyzing the main bundle.** Modern apps chunk-load (`chunks/12345.js`); analyze all.
4. **Treating expired AWS keys as worthless.** Even expired keys reveal account ID + naming conventions.
5. **Not re-running on deploys.** New release → new JS → new endpoints. Continuous monitoring is critical.

## Pro tips

- **JS files often `Cache-Control: immutable`** — fingerprints are stable, so MD5-hash them and diff over time.
- **Webpack chunks are named by hash** but the hash → original name mapping is in the entry bundle.
- **Look for `process.env.NEXT_PUBLIC_*` references** in Next.js — leaks env vars.
- **Vue apps may expose Vuex state** via window object — check `window.__INITIAL_STATE__`.
- **Service worker JS (`/sw.js`)** often caches API URLs — easy endpoint mine.

## Anti-anti-bot

Some apps obfuscate / minify aggressively. Beautify before analysis:
```bash
# js-beautify
npm install -g js-beautify
js-beautify -r "$OUT/files/"*.js

# Or use jsnice.org (online, manual)
# Or webcrack — handles webpack + obfuscators
npm install -g webcrack
webcrack "$OUT/files/main.bundle.js" -o "$OUT/files/main.deobfuscated.js"
```
