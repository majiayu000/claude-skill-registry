---
name: security-ownership-map
description: >-
  Analyze git repositories to build a security ownership topology mapping people
  to files, compute bus factor and sensitive-code ownership metrics, detect
  orphaned security code and hidden owners, and export CSV/JSON artifacts for
  graph databases and visualization. Trigger when the user requests
  security-oriented ownership analysis, bus-factor audits, CODEOWNERS reality
  checks, sensitive hotspot identification, or ownership cluster analysis
  grounded in git history. Do not trigger for general contributor lists or
  non-security ownership queries.
allowed-tools:
  - Read
  - Bash
  - Write
  - Glob
  - Grep
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - analyzer
    - security
    - git
    - ownership
    - bus-factor
  provenance:
    upstream_source: "security-ownership-map"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T12:32:23+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.83
---

# Security Ownership Map

Analyze git history to build a bipartite ownership graph (people-to-files), compute security risk metrics (bus factor, sensitivity scores, ownership concentration), detect orphaned sensitive code and hidden owners, and export structured artifacts for Neo4j, Gephi, or downstream analysis.

## Overview

This skill mines git repositories to answer security ownership questions:

- **Who owns security-critical code?** Map people to auth, crypto, secrets, and infrastructure files.
- **What is the bus factor?** Identify files where a single departure creates risk.
- **Is ownership drifting?** Compare CODEOWNERS declarations against actual commit patterns.
- **Where are the orphaned hotspots?** Find stale sensitive code with low bus factor.
- **How do files cluster?** Use co-change analysis (Jaccard similarity) and community detection to reveal logical coupling.

**What it analyzes:**
- Git commit history (author attribution, recency-weighted touches)
- File sensitivity (pattern-matched tags: auth, crypto, secrets, PII, infrastructure)
- Ownership concentration and bus factor per file
- Co-change coupling between files (Jaccard similarity on shared commits)
- Community structure (Louvain greedy modularity on co-change graph)

**What it produces:**
- `people.csv`, `files.csv`, `edges.csv` — graph nodes and relationships
- `cochange_edges.csv` — file-to-file coupling weights
- `summary.json` — orphaned code, hidden owners, bus factor hotspots
- `communities.json` — file clusters with top maintainers
- `cochange.graph.json` / `ownership.graph.json` — NetworkX node-link format
- Optional: `commits.jsonl`, GraphML exports

## Analysis Checklist

### Ownership Risk

- [ ] Identify all files matching sensitivity patterns (auth, crypto, secrets, PII, infrastructure)
- [ ] Compute bus factor per sensitive file (threshold: 1 = danger, <3 = warning)
- [ ] Flag orphaned sensitive code (stale + low bus factor)
- [ ] Detect hidden owners (>50% of a sensitivity tag owned by one person)

### Knowledge Distribution

- [ ] Calculate ownership concentration per file (top contributor share)
- [ ] Identify knowledge islands (single-developer files in security paths)
- [ ] Track timezone distribution of contributors for global coverage gaps
- [ ] Measure recency-weighted ownership to detect recent knowledge loss

### Co-Change Coupling

- [ ] Build co-change graph excluding lockfiles, config, and bot commits
- [ ] Compute Jaccard similarity between file pairs
- [ ] Run community detection (Louvain) on co-change graph
- [ ] Identify cross-team clusters indicating architectural coupling risk

### CODEOWNERS Validation

- [ ] Compare declared CODEOWNERS against actual git history owners
- [ ] Flag ghost owners (no commits in 180+ days)
- [ ] Identify ownership gaps (sensitive files with no CODEOWNERS entry)

## Metrics

### Bus Factor

| Metric | Description | Good | Warning | Critical |
|--------|-------------|------|---------|----------|
| Bus factor | Unique authors per sensitive file | >= 3 | 2 | 1 |
| Ownership concentration | Top contributor's share | < 40% | 40-70% | > 70% |
| Staleness | Days since last security touch | < 90 | 90-365 | > 365 |

### Co-Change Coupling

| Metric | Description | Strong | Moderate | Weak |
|--------|-------------|--------|----------|------|
| Jaccard similarity | Shared-commit overlap between files | > 0.3 | 0.1-0.3 | < 0.1 |
| Community bus factor | Unique authors in a file cluster | >= 5 | 3-4 | 1-2 |

## Workflow

### Step 1: Scope the repository

Choose the target repo and optional time window. Use `--since` / `--until` to narrow large histories.

### Step 2: Configure sensitivity rules

Use built-in defaults (auth, crypto, secrets, SSO, IAM, TLS) or provide a custom CSV:

```
# pattern,tag,weight
**/auth/**,auth,1.0
**/crypto/**,crypto,1.0
**/*.pem,secrets,1.0
**/iam/**,auth,1.0
**/pii/**,pii,1.0
**/terraform/**,infrastructure,1.0
```

### Step 3: Build the ownership map

```bash
python scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

Key flags:
- `--cochange-max-files 50` — ignore supernode commits for co-change graph
- `--no-default-cochange-excludes` — include lockfiles in co-change analysis
- `--cochange-exclude "**/Kbuild"` — add custom exclusions
- `--identity committer` — attribute to committer instead of author
- `--graphml` — emit GraphML for Gephi import
- `--no-communities` — skip community detection
- `--sensitive-config path/to/rules.csv` — custom sensitivity rules

### Step 4: Query results

Use `scripts/query_ownership.py` for bounded JSON slices without loading full datasets:

```bash
# Orphaned sensitive code
python scripts/query_ownership.py --data-dir ownership-map-out \
  summary --section orphaned_sensitive_code

# Auth files with bus factor <= 1
python scripts/query_ownership.py --data-dir ownership-map-out \
  files --tag auth --bus-factor-max 1

# Top sensitive-code contributors
python scripts/query_ownership.py --data-dir ownership-map-out \
  people --sort sensitive_touches --limit 10

# Co-change neighbors for a file
python scripts/query_ownership.py --data-dir ownership-map-out \
  cochange --file crypto/tls --min-jaccard 0.05

# Community maintainers
python scripts/query_ownership.py --data-dir ownership-map-out \
  community --id 3
```

### Step 5: Track maintainers over time

```bash
python scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --top 5 \
  --bucket quarter
```

### Step 6: Persist and visualize

Load artifacts into Neo4j (see `references/neo4j-import.md`) or import CSVs into Gephi for network visualization. Filter by `sensitivity_score > 0` to focus on security-relevant clusters.

## Output Artifacts

| File | Contents |
|------|----------|
| `people.csv` | Person nodes with timezone, touch counts, sensitive touches |
| `files.csv` | File nodes with bus factor, sensitivity score, tags |
| `edges.csv` | Person-to-file edges with touches, recency weight, sensitive weight |
| `cochange_edges.csv` | File-to-file edges with co-change count and Jaccard similarity |
| `summary.json` | Orphaned sensitive code, hidden owners, bus factor hotspots, stats |
| `communities.json` | File clusters with top maintainers per community |
| `cochange.graph.json` | NetworkX node-link JSON with community IDs |
| `commits.jsonl` | Raw commit data (optional, with `--emit-commits`) |
| `*.graphml` | GraphML exports for Gephi (optional, with `--graphml`) |

## Report Format

### Summary

```
Security Ownership Map Report
==============================
Repository: /path/to/repo
Time window: 12 months
Generated: 2026-02-04T12:00:00Z

Stats:
  Commits analyzed: 2,847
  People: 42
  Files: 1,203
  Co-change pairs: 8,412

Key Findings:
- 7 sensitive files with bus factor = 1
- 3 orphaned auth files (stale > 365 days)
- 1 hidden owner controls 63% of crypto code
```

### Security Queries

```bash
# Orphaned sensitive code (stale + low bus factor)
python scripts/query_ownership.py --data-dir ownership-map-out \
  summary --section orphaned_sensitive_code

# Hidden owners by sensitivity tag
python scripts/query_ownership.py --data-dir ownership-map-out \
  summary --section hidden_owners

# Bus factor hotspots
python scripts/query_ownership.py --data-dir ownership-map-out \
  summary --section bus_factor_hotspots
```

## Examples

### Example 1: Quick security audit

```
User: Run a security ownership analysis on this repo for the last year.
Assistant: I'll build a security ownership map from your git history.

1. Running: python scripts/run_ownership_map.py --repo . --out ownership-map-out --since "12 months ago" --emit-commits
2. Querying orphaned sensitive code...
3. Checking bus factor hotspots...

Results:
- 1,203 files analyzed across 42 contributors
- 7 sensitive files with bus factor = 1 (critical)
- 3 orphaned auth files not touched in over a year
- alice@corp controls 63% of all crypto code (hidden owner)

Recommendations:
1. Pair-program on the 7 single-owner sensitive files to spread knowledge
2. Review the 3 orphaned auth files for deprecation or ownership transfer
3. Assign a secondary reviewer for all crypto changes
```

### Example 2: Focused tag analysis

```
User: Which auth files have the lowest bus factor?
Assistant: Querying auth files sorted by bus factor...

python scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 2

Found 4 auth files with bus factor <= 2:
- auth/oauth/handler.rs (bus_factor: 1, last touch: 2025-03-12)
- auth/session/store.rs (bus_factor: 1, last touch: 2025-08-01)
- auth/rbac/policy.rs (bus_factor: 2, last touch: 2025-11-20)
- auth/token/refresh.rs (bus_factor: 2, last touch: 2025-09-15)
```

## Interpretation Guide

### Score Meanings

| Bus Factor | Risk Level | Action |
|------------|------------|--------|
| >= 3 | Low | Maintain current practices |
| 2 | Moderate | Plan knowledge transfer |
| 1 | High | Immediate pair programming needed |
| 0 (stale) | Critical | File may be abandoned; review for deprecation |

### Sensitivity Tags

| Tag | Matches | Risk Context |
|-----|---------|--------------|
| auth | Login, OAuth, RBAC, session, token, IAM, SSO | Authentication and authorization logic |
| crypto | Encryption, TLS, SSL, key derivation | Cryptographic operations |
| secrets | PEM files, key files, P12/PFX certificates | Secret material and credentials |
| pii | Personal data paths (custom config) | Data privacy and compliance |
| infrastructure | Terraform, K8s configs (custom config) | Infrastructure-as-code security |

## Requirements

- Python 3
- `networkx` (required for community detection, enabled by default)

Install: `pip install networkx`

## Notes

- Merge commits are excluded by default; use `--include-merges` to include them.
- Dependabot commits are excluded by default; override with `--no-default-author-excludes`.
- Co-change graph ignores lockfiles, `.github/*`, and editor config by default.
- Compare `summary.json` against CODEOWNERS to highlight ownership drift.
- If `git log` is too large, narrow with `--since` or `--until`.