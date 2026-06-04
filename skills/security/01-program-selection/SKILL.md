---
name: program-selection
description: Evaluate HackerOne / Bugcrowd / Intigriti programs before committing time. Decide signal-to-noise, payout history, response time, scope size, and competition level. Use when the user is considering a new bug bounty target or asking "should I hunt this".
metadata:
  type: skill
  phase: pre-hunt
  platforms: [hackerone, bugcrowd, intigriti, immunefi]
---

# Program Selection

> Your time is the most expensive thing you have. Pick wrong, lose a month.

## When to invoke

**Trigger phrases:**
- "should I hunt this program"
- "is this H1 worth it"
- "pick me a Bugcrowd target"
- "evaluate this program"
- "what target next"

**Do not invoke when:** the user has already committed to a target and is asking about recon or hunting.

## The 7 Selection Criteria

Score each from 1-5. Hunt programs scoring **≥ 25/35**.

### 1. Payout History (weight: ×2)
- Look at the **last 50 disclosed reports** on the program page
- Median bounty for the severity you're confident in
- Programs paying **only minimums** are red flag — they downgrade aggressively
- **5/5**: median Critical > $5k, median High > $2k
- **3/5**: median Critical $1-5k, High $500-2k
- **1/5**: minimums only, or "swag/rep only"

### 2. Response Time
- HackerOne shows **avg time to first response** and **avg time to triage**
- Bugcrowd shows similar in program stats
- **5/5**: first response < 24h, triage < 3 days
- **3/5**: first response < 72h, triage < 7 days
- **1/5**: response > 1 week — your dupe risk skyrockets

### 3. Scope Size
- Count **in-scope assets** (domains, mobile apps, APIs, smart contracts)
- Bigger scope = more attack surface, but more competition
- **5/5**: wide scope `*.target.com` with subsidiary domains
- **3/5**: 5-20 specific assets
- **1/5**: one URL, no subdomains

### 4. Scope Quality (out-of-scope analysis)
Read the OOS list carefully. Red flags:
- "Self-XSS won't be paid" (fine, standard)
- "No subdomain takeover" → kills entire vuln class
- "No reports about CSP / cookie flags / missing headers" (good — saves time)
- "Findings must demonstrate impact" → high bar, plan PoC accordingly
- **5/5**: OOS is sensible; high-impact classes welcome
- **1/5**: too many vuln classes excluded

### 5. Competition Level
- Public programs: high competition, dupes likely
- Private invitation: lower competition, higher payout typical
- **Signal of saturation:** if disclosed reports show heavy clustering on the same paths, the program is "hunted dry" for the easy stuff
- **5/5**: private invite, < 6 months old
- **3/5**: public, < 12 months old
- **1/5**: public, > 3 years old (low-hanging gone)

### 6. Tech Stack Match
- Are you strong in the tech they use?
- E.g., if you're a GraphQL/JS specialist and the target is a Java/Spring monolith, that's a mismatch
- **5/5**: stack matches your top 2 skills
- **3/5**: partial overlap
- **1/5**: tech you've never touched

### 7. Program Hygiene
- Has the program **closed reports as N/A or Informative > 30%**?
- Have they downgraded severities controversially? (check disclosed activity)
- Does the manager respond to triagers?
- **5/5**: clean record, fair severity assessment
- **1/5**: known for harsh downgrades or ghosting

## Step-by-Step Workflow

### 1. Pull program metadata

For HackerOne:
```bash
# View program page (manually copy URL into Claude / browser)
# Key fields to extract:
#   - Avg time to first response
#   - Avg time to triage
#   - Avg bounty (last 90 days)
#   - Disclosed report count
#   - In-scope assets

# If using HackerOne API (requires auth):
# https://api.hackerone.com/v1/hackers/programs
```

For Bugcrowd:
```bash
# Navigate to program → Activity tab → "Recent Validations"
# Key fields:
#   - VRT (Vulnerability Rating Taxonomy) used
#   - Average payout per VRT bucket
#   - Last activity
```

### 2. Score against the 7 criteria

Open `templates/program-score-card.md` and fill in.

### 3. Read 10 disclosed reports

- Pick the **most recent 10**
- Note: vuln classes that paid, severity disputes, triager tone
- This is the single best signal of "what works here"

### 4. Tech stack fingerprint

Quick passive recon (no scanning yet):
```bash
# DNS lookup
dig +short target.com

# Cert transparency for breadth
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u | head -30

# Wappalyzer-style fingerprint via httpx
echo "target.com" | httpx -tech-detect -title -status-code -json
```

### 5. Decision

| Total Score (out of 35) | Decision |
|---|---|
| 30-35 | **Hunt immediately** — high ROI expected |
| 25-29 | **Hunt with focus** — pick 1-2 strong vuln classes |
| 20-24 | **Time-box 1 week** — pull out if nothing found |
| < 20 | **Skip** — better targets exist |

## Output template

```markdown
# Program Selection Report: <program_name>

**Platform:** HackerOne / Bugcrowd / Intigriti
**Date evaluated:** YYYY-MM-DD
**Scope:** *.example.com + mobile (iOS, Android)

## Scoring (35 max)

| Criterion | Score | Note |
|---|---|---|
| Payout history (×2) | 4/5 (8/10) | Median High = $1,500 |
| Response time | 5/5 | First response avg 6h |
| Scope size | 5/5 | ~80 subdomains found |
| Scope quality | 3/5 | Subdomain takeover excluded |
| Competition | 2/5 | Public for 4 years |
| Tech stack match | 4/5 | React + GraphQL = my strong stack |
| Program hygiene | 4/5 | Fair triage, no controversies |
| **TOTAL** | **26/35** | **HUNT WITH FOCUS** |

## Recommended attack vectors
1. GraphQL endpoint at api.example.com — introspection, batching, deep-query attacks
2. New mobile app v3.x — re-scan after recent release
3. Auth flow — OIDC implementation, possibly custom

## Pass on:
- Subdomain takeover (excluded)
- Anything CSRF — they auto-mark N/A

## Time budget: 5 days
```

## Cross-references

- `[[scope-analysis]]` — once you decide to hunt, fully parse the scope
- `[[threat-modeling-mindmap]]` — turn scope into hunt plan
- `[[continuous-monitoring]]` — set up watcher on private programs

## Common pitfalls

1. **Chasing big logos.** Big company ≠ big payout. Many enterprise H1 programs pay min.
2. **Ignoring competition.** A 4-year public program on Yahoo's scope is picked clean.
3. **Going after CVSS-only programs without considering business impact.** Bugcrowd's VRT often pays more than CVSS would suggest.
4. **Overweighting your familiarity bias.** "I know X tech" ≠ "X tech still has bugs here".
5. **Not reading the OOS list before scanning.** You burn hours on a class they exclude.

## Always-rejected check

Before committing, verify the program does NOT auto-reject:
- Missing security headers (X-Frame-Options, CSP without exploit)
- Theoretical CSRF on state-changing forms without PoC
- Self-XSS
- Email enumeration without bypass
- Outdated software without exploit
- TLS/SSL config issues without working PoC
- Subdomain takeover (if excluded)
- Open redirects (if excluded, OR if no impact chain)
- Logout CSRF
- Brute force without rate-limit evidence

→ See `docs/always-rejected-list.md` for the full list.
