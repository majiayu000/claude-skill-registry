---
name: detecting-staleness
description: Scan all artifacts for confidence metadata and report staleness using pure derived scoring.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Detecting Staleness

Scan all artifacts with confidence metadata, compute freshness scores using a pure derived formula, and output a staleness report with suggested actions.

---

## Core Principle

**Confidence is always derived, never stored.** The score is computed from immutable inputs (frontmatter + git history + config). Same inputs always produce the same score.

---

## Triggers

```
/stale                              # All artifacts, default threshold
/stale --threshold 0.50             # Custom threshold
/stale --pack observer              # Specific pack's artifacts
```

---

## When to Use

- Periodic health check of artifact freshness
- Before starting a new sprint (are our artifacts still valid?)
- After a burst of code changes (did anything go stale?)
- When planning what to refresh next

---

## Workflow

### Phase 1: Scan Artifacts

```
Glob the following paths for artifacts with confidence frontmatter:

  grimoires/*/canvas/*.md
  grimoires/*/journeys/*.md
  grimoires/*/reality/*.md
  grimoires/artisan/taste.md

IF --pack specified:
  Filter to grimoires/{pack}/ only

For each file:
  Parse YAML frontmatter
  Look for confidence: block
```

**When frontmatter is MISSING**: Classify artifact as `unknown` with suggested action:
```
Run `/refresh {path}` to initialize confidence tracking
```

### Phase 2: Compute Scores

For each artifact WITH confidence metadata:

```
READ INPUTS (from frontmatter):
  last_validated_commit   # Git SHA anchor
  validation_count        # Times re-validated

READ INPUTS (from git):
  commits_since = git rev-list --count {last_validated_commit}..HEAD -- {related_paths}

  IF last_validated_commit not found in history:
    Fallback: git log --oneline --since="30 days ago" -- {related_paths} | wc -l
    Warn: "Baseline commit not found — using 30-day window"

  IF .git unavailable (shallow clone, no git):
    Use validation_count only
    Mark score as "approx"
    Warn: "Git history unavailable — confidence approximate"

READ INPUTS (from .loa.config.yaml):
  decay_rate              = confidence.decay.rate (default: 0.02)
  code_change_penalty     = confidence.penalties.code_change (default: 0.05)
  revalidation_boost      = confidence.boosts.revalidation (default: 0.20)
  diminishing_factor      = confidence.boosts.diminishing_factor (default: 0.7)
  floor                   = confidence.decay.floor (default: 0.20)
  initial_score           = confidence.initial_score (default: 0.90)

COMPUTE:
  days_since = days between last_validated_commit date and now (UTC)
  time_decay = days_since * decay_rate
  code_penalty = commits_since * code_change_penalty
  boost = revalidation_boost * (diminishing_factor ^ validation_count)

  score = clamp(initial_score - time_decay - code_penalty + boost, floor, 0.95)

CLASSIFY:
  score >= healthy_threshold (0.70)  → "healthy"
  score >= warning_threshold (0.50)  → "warning"
  score >= stale_threshold (0.30)    → "stale"
  score < stale_threshold            → "archive"
```

### Phase 3: Output Table

```markdown
STALENESS REPORT
════════════════

| Artifact | Confidence | Status | Last Validated | Suggested Action |
|----------|-----------|--------|----------------|------------------|
| canvas/xabbu.md | 0.72 | healthy | 2026-02-01 | — |
| canvas/elcapitan.md | 0.48 | warning | 2026-01-20 | /drift, /refresh |
| reality/profile.md | 0.31 | stale | 2026-01-10 | /ground profile |
| taste.md | unknown | unknown | — | /refresh grimoires/artisan/taste.md |

Summary: {N} healthy, {M} warning, {P} stale, {Q} archive, {R} unknown
```

IF `--threshold` specified: Only show artifacts below the threshold.

---

## Configuration

Thresholds and decay parameters are read from `.loa.config.yaml`:

```yaml
confidence:
  initial_score: 0.90
  decay:
    rate: 0.02
    floor: 0.20
  thresholds:
    healthy: 0.70
    warning: 0.50
    stale: 0.30
  penalties:
    code_change: 0.05
  boosts:
    revalidation: 0.20
    diminishing_factor: 0.7
```

If config is missing, use the defaults shown above.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No artifacts found | Report "No artifacts with confidence metadata found" |
| Git not available | Use validation_count only, mark as "approx" |
| Config missing | Use defaults |
| Frontmatter parse error | Skip artifact, log warning |
| Baseline commit not in history | Use 30-day window fallback |

---

## Integration Points

- **Reads**: Artifact frontmatter, git history, `.loa.config.yaml`
- **Consumed by**: Operators deciding what to refresh
- **Related**: `/drift` (detailed per-artifact), `/refresh` (re-validate)

---

## Validation

- [ ] Scans all artifact paths (canvas, journeys, reality, taste.md)
- [ ] Correctly computes decay formula
- [ ] Handles missing confidence frontmatter as "unknown"
- [ ] Handles missing git as "approx"
- [ ] Respects --threshold filter
- [ ] Respects --pack filter
- [ ] Config defaults work when .loa.config.yaml missing
