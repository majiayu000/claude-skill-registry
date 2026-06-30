---
name: engagement-memory
description: Use when recalling prior techniques at recon/weaponize, or recording a confirmed finding at report — cross-engagement pattern memory ranked by impact
metadata:
  type: support
  phase: all
  tools: pattern_db.py, schemas.py, rotation.py
kill_chain:
  phase: [recon, weaponize, report]
  step: [1, 2, 8]
  attck_tactics: []
  attck_techniques: []
depends_on: [vulnerability-analysis]
feeds_into: [recon-osint, exploit-development, web-pentest]
inputs: [confirmed_findings, target, tech_stack]
outputs: [prior_intel, ranked_patterns]
references: []
scripts:
  - scripts/pattern_db.py
  - scripts/schemas.py
  - scripts/rotation.py
---

# Engagement Memory (cross-engagement learning)

## When to Activate

- At **recon/weaponize**: recall what already worked against this target class / tech stack.
- At **report**: persist each `[CONFIRMED]` finding as a reusable pattern (ranked by impact).
- Periodic housekeeping: compact the pattern DB / rotate the audit log.

## Model

Append-only JSONL store (`~/.claude/engagement-memory/patterns.jsonl`, override `$ENGAGEMENT_DB`).
Three record types in their own files so they never mix: **patterns** (`patterns.jsonl`),
**target profiles** (`profiles.jsonl`), **audit log** (`audit.jsonl`, disposable). A pattern is keyed
by `(target, vuln_class, technique)`, ranked by **severity / CVSS / confidence** (real impact, never
payout), and carries a **lifecycle status** (`proposed/active/stale/deprecated/...`). Recall is an
**explicit top-N query** (anti-context-bloat). Duplicates **merge** (count bumped, most-recent status
wins), never blind-discarded; `compact` runs automatically over a size threshold and stays lossless.
TTL `stale` patterns and `deprecated/rejected` ones drop out of default recall but are kept.

## Commands

```bash
# RECALL — relevance-ranked (stdlib BM25 + aliases), active-only by default
python skills/engagement-memory/scripts/pattern_db.py match --vuln-class ssrf --query "imds metadata" --tech-stack aws
# INJECT — budgeted prior-intel card for a phase (top-N, byte-capped; $ENGAGEMENT_MEMORY_MODE=auto|debug|off)
python skills/engagement-memory/scripts/pattern_db.py inject --vuln-class ssrf --query imds --max-bytes 1500

# RECORD a confirmed finding (flags or finding JSON). A key collision needs --resolve update|merge|reject|force.
python skills/engagement-memory/scripts/pattern_db.py record --target acme.com --vuln-class ssrf \
    --cwe CWE-918 --attack-id T1190 --severity high --cvss 9.1 --tech-stack nginx,aws --technique "metadata theft"
python skills/engagement-memory/scripts/pattern_db.py record --json '<finding json from validate_findings>'

# LIFECYCLE + cross-client
python skills/engagement-memory/scripts/pattern_db.py promote   --target acme.com --vuln-class ssrf --technique "metadata theft" [--global]
python skills/engagement-memory/scripts/pattern_db.py deprecate --target acme.com --vuln-class ssrf --technique "metadata theft"
python skills/engagement-memory/scripts/pattern_db.py match --vuln-class ssrf --include-global   # add sanitized cross-client TTPs

# PROFILES + housekeeping + observability
python skills/engagement-memory/scripts/pattern_db.py profile --target acme.com --tech-stack nginx,aws --endpoints /api,/admin
python skills/engagement-memory/scripts/pattern_db.py recall-profile --target acme.com
python skills/engagement-memory/scripts/pattern_db.py compact         # manual lossless dedup-merge
python skills/engagement-memory/scripts/pattern_db.py stats           # patterns by class + profile count
python skills/engagement-memory/scripts/pattern_db.py audit-stats     # action log: by tool/action/outcome
```

Or use the `/engage.memory` command (recall | inject | record | promote | deprecate | gc | stats).

## OPSEC & Detection

| Concern | Note |
|---------|------|
| Secrets at rest | Stores technique + CWE/CVSS + an evidence *reference*, never loot. A **secret-input guard** rejects `evidence_ref`/`source` that look like inline secrets (private keys, `password=`, AKIA, JWTs, tokens) — store a path; **rotate** the exposed credential, don't just delete. |
| Cross-client bleed | Per-client isolation is the default (`$ENGAGEMENT_DB`). The shared global store is opt-in (`promote --global` / `record --global`) and **sanitized** (target + evidence blanked); recall it only with `--include-global`. |
| Trust | New auto-captures can be `proposed`; only confirmed/reviewed findings are `active`. A key collision is **review-gated** (`--resolve`), not silently merged. |
| Auditability | Every record/match/compact/promote — and every refused line (`denial`) — is written to `audit.jsonl` (rotated by discard, with a retention-gap marker). The append-only patterns journal + audit log ARE the history. |
| Integrity | Records carry `schema_version`; malformed/type-poisoned/foreign lines are skipped on read, never trusted. |

## Deep Dives

- `scripts/schemas.py` — record types (pattern/audit/target_profile/retention_gap), validation + secret guard, `pattern_key`/`pattern_id`, impact+confidence `rank_score`, recency-resolving `merge`.
- `scripts/pattern_db.py` — typed routing, merge-on-read with TTL staleness, BM25 relevance recall, `inject`, lifecycle verbs, global scope, CLI.
- `scripts/rotation.py` — `compact`/`maybe_gc` (lossless dedup-merge, auto-triggered) vs `rotate_audit` (discard the disposable log + write a retention-gap marker).
