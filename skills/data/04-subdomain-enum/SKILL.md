---
name: subdomain-enum
description: Enumerate subdomains using passive and active techniques (subfinder, amass, chaos, assetfinder, crtsh, DNS brute force). Use when the user has a root domain in scope and needs the full subdomain list before probing.
metadata:
  type: skill
  phase: recon
  tools: [subfinder, amass, assetfinder, chaos, findomain, sublist3r, crtsh, anew]
---

# Subdomain Enumeration

> Maximum coverage. Multiple sources. Continuously updated.

## When to invoke

**Trigger phrases:**
- "enumerate subdomains for X"
- "subfinder X"
- "find subdomains of target.com"
- "run full subdomain recon"

## Pre-flight checklist

- [ ] Scope confirmed: `*.target.com` is in-scope (see `[[scope-analysis]]`)
- [ ] OOS list ready (to filter results)
- [ ] API keys configured (see below)
- [ ] Output dir created: `mkdir -p loot/<target>/subs/`

## API keys (set these once)

Most passive sources work without keys but **with keys you 3-5x your coverage**:

```bash
# ~/.config/subfinder/provider-config.yaml
chaos:
  - "YOUR_CHAOS_KEY"
binaryedge:
  - "YOUR_BINARYEDGE_KEY"
censys:
  - "ID:SECRET"
github:
  - "ghp_YOUR_GITHUB_TOKEN"
shodan:
  - "YOUR_SHODAN_KEY"
securitytrails:
  - "YOUR_SECURITYTRAILS_KEY"
virustotal:
  - "YOUR_VT_KEY"
```

Free tiers (sign up):
- **Chaos:** https://chaos.projectdiscovery.io (free for BB hunters)
- **Censys:** 250 queries/month free
- **GitHub:** any PAT works
- **SecurityTrails:** 50/month free
- **VirusTotal:** 4 req/min free

## The full pipeline

### 1. Passive enumeration (no traffic to target)

```bash
TARGET="target.com"
OUT="loot/$TARGET/subs"
mkdir -p "$OUT"

# subfinder — fastest, broadest passive
subfinder -d "$TARGET" -all -recursive -silent > "$OUT/subfinder.txt"

# assetfinder — adds extra sources
assetfinder --subs-only "$TARGET" > "$OUT/assetfinder.txt"

# chaos — ProjectDiscovery's curated dataset
chaos -d "$TARGET" -silent > "$OUT/chaos.txt"

# crtsh — certificate transparency
curl -s "https://crt.sh/?q=%25.${TARGET}&output=json" | \
    jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u > "$OUT/crtsh.txt"

# findomain — Rust-based, fast
findomain -t "$TARGET" -q > "$OUT/findomain.txt" 2>/dev/null

# github-subdomains — mines GitHub for subdomain mentions
# pip install github-subdomains (or use the Go tool)
github-subdomains -d "$TARGET" -t "$GITHUB_TOKEN" -o "$OUT/github.txt"

# Combine & dedupe
cat "$OUT"/*.txt | sort -u > "$OUT/passive.txt"
echo "[+] Passive sources: $(wc -l < "$OUT/passive.txt") unique subdomains"
```

### 2. Active enumeration (DNS brute force)

```bash
# Use a strong wordlist (assetnote wordlists are gold)
WORDLIST="$HOME/tools/assetnote-wordlists/data/manual/best-dns-wordlist.txt"

# puredns is the modern choice (fast, accurate)
# Install: go install github.com/d3mondev/puredns/v2@latest
puredns bruteforce "$WORDLIST" "$TARGET" \
    -r resolvers.txt \
    --rate-limit 1000 \
    --write "$OUT/bruteforce.txt"

# Alternative: shuffledns + dnsx
shuffledns -d "$TARGET" -w "$WORDLIST" -r resolvers.txt -mode bruteforce > "$OUT/shuffle.txt"
```

**Get a fresh resolvers file** (critical for speed):
```bash
# Resolvers — use trusted, fast ones
curl -s https://raw.githubusercontent.com/proabiral/Fresh-Resolvers/master/resolvers.txt > resolvers.txt
# Validate them
dnsvalidator -tL resolvers.txt -threads 200 -o validated-resolvers.txt
```

### 3. Permutation / alteration

```bash
# Combine known subs into permutations
gotator -sub "$OUT/passive.txt" -perm permutations.txt -depth 1 -numbers 5 | \
    puredns resolve --resolvers validated-resolvers.txt > "$OUT/permutations.txt"

# Alternative: dnsgen
cat "$OUT/passive.txt" | dnsgen - | puredns resolve --resolvers validated-resolvers.txt > "$OUT/dnsgen.txt"
```

### 4. Combine, dedupe, filter OOS

```bash
# Everything in one file
cat "$OUT"/*.txt | sort -u > "$OUT/all.txt"

# Remove out-of-scope (from scope-analysis output)
grep -vFf "scope-oos.txt" "$OUT/all.txt" > "$OUT/in-scope.txt"

echo "[+] Total subdomains: $(wc -l < "$OUT/all.txt")"
echo "[+] In-scope:         $(wc -l < "$OUT/in-scope.txt")"
```

### 5. Hand off to next skill

The output `$OUT/in-scope.txt` feeds directly into `[[asset-discovery]]`.

## One-liner full pipeline

```bash
# Save this as scripts/full-sub-recon.sh
TARGET=$1
OUT="loot/$TARGET/subs"
mkdir -p "$OUT"

(subfinder -d "$TARGET" -all -silent;
 assetfinder --subs-only "$TARGET";
 chaos -d "$TARGET" -silent;
 curl -s "https://crt.sh/?q=%25.${TARGET}&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g';
 findomain -t "$TARGET" -q 2>/dev/null) | sort -u | anew "$OUT/passive.txt"

echo "[+] Passive done: $(wc -l < "$OUT/passive.txt") subs"
```

Run:
```bash
chmod +x scripts/full-sub-recon.sh
./scripts/full-sub-recon.sh target.com
```

## Continuous mode

Set up nightly diff alerts → see `[[continuous-monitoring]]`.

```bash
# In cron
0 3 * * * cd /home/user/bb && ./scripts/full-sub-recon.sh target.com && \
          diff -u loot/target.com/subs/yesterday.txt loot/target.com/subs/passive.txt | \
          grep '^+' | grep -v '^+++' | \
          notify -bulk -id discord
```

## Output template

```
target.com
├── subs/
│   ├── passive.txt        ← passive sources
│   ├── bruteforce.txt     ← active DNS brute
│   ├── permutations.txt   ← gotator/dnsgen
│   ├── all.txt            ← combined+sorted
│   └── in-scope.txt       ← filtered against OOS
└── stats.txt
    ├── 247 total
    ├── 14 OOS removed
    └── 233 in-scope
```

## Cross-references

- `[[scope-analysis]]` — gives you the OOS filter
- `[[asset-discovery]]` — next: which of these are alive?
- `[[continuous-monitoring]]` — nightly diff alerts
- `[[subdomain-takeover]]` — check for dangling DNS

## Common pitfalls

1. **No API keys** = passive coverage drops ~70%. Configure Chaos minimum.
2. **Bad resolvers** = false positives. Validate with `dnsvalidator`.
3. **Including OOS** = wasted hunt time, possible report rejection.
4. **One-shot enumeration** = misses new subdomains added daily. Continuous is critical.
5. **Trusting brute force alone** = misses passive-only subs (like internal CDN names).

## Anti-WAF / stealth tips

- Some programs have WAFs on `*.target.com` that rate-limit recon
- Throttle: `--rate-limit 100` on puredns
- Use rotating User-Agents on HTTP-based sources (httpx)
- For private programs, ask the manager if there's a recon allowlist for your IP

## Validation: did we cover everything?

Sanity checks:
- Number of subs > 10 for any non-trivial target?
- Did `*.api.target.com` show up if APIs exist?
- Are subdomain levels covered? (`a.b.c.target.com`)
- Did Wayback / waybackurls also reveal hostnames we missed?
  - ```cat all-urls-from-wayback.txt | unfurl domains | grep target.com | anew "$OUT/wayback-domains.txt"```
