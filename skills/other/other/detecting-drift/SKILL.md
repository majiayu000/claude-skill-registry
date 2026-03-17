---
name: detecting-drift
description: Show what changed since last validation for a specific artifact. Computes confidence without writing to frontmatter.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
---

# Detecting Drift

Show what changed since the last validation of a specific artifact. Queries git history and feedback events to produce a drift report with a computed confidence score. Read-only — does NOT modify any files.

---

## Core Principle

**Observe, don't mutate.** This skill computes confidence and reports drift but never writes to frontmatter. Use `/refresh` to update confidence inputs.

---

## Triggers

```
/drift {artifact-path}              # Check specific file
/drift grimoires/observer/canvas/   # Check directory (all files within)
```

**Examples**:
```
/drift grimoires/observer/canvas/xabbu-canvas.md
/drift grimoires/observer/canvas/
/drift grimoires/artisan/taste.md
```

---

## When to Use

- Before deciding whether to refresh an artifact
- After significant code changes to related paths
- When investigating why an artifact feels outdated
- As a follow-up to `/stale` (which lists all; `/drift` gives detail on one)

---

## Workflow

### Phase 1: Read Artifact

```
Parse YAML frontmatter for confidence metadata:
  - last_validated_commit (SHA)
  - last_validated_at (timestamp)
  - validation_count
  - related_paths

IF confidence block is MISSING:
  Classify as "unknown"
  Output: "No confidence metadata — run /refresh {path} to initialize"
  Exit

IF last_validated_commit is missing:
  Warn: "No baseline commit — treating as never validated"
  Use 30-day window for git queries
```

IF a directory path was provided, iterate over all `.md` files within and produce a report for each.

### Phase 2: Query Git (commit-SHA anchored)

```
For each path in related_paths:
  git rev-list --count {last_validated_commit}..HEAD -- {path}
  git log --oneline {last_validated_commit}..HEAD -- {path}

  Collect:
    - commit_count per related path
    - commit summaries (one-line)
    - total commits_since across all related_paths

IF last_validated_commit not found in history (force-push, rebase):
  Fallback: git log --oneline --since="30 days ago" -- {path}
  Warn: "Baseline commit not found — using 30-day window"

IF .git unavailable:
  Use validation_count only
  Mark score as "approx"
  Warn: "Git history unavailable — confidence approximate"
```

### Phase 3: Check Feedback Events

```
Glob: grimoires/shared/feedback/events/*.jsonl

Filter events where:
  target.selector matches this artifact path
  OR target.selector matches "user:{username}" (for canvases)

Filter by timestamp > last_validated_at

Count:
  positive_count (direction = "positive")
  negative_count (direction = "negative")
  neutral_count (direction = "neutral")
  total_events = positive + negative + neutral
```

### Phase 4: Compute Confidence (pure function)

```
Apply decay formula from .loa.config.yaml (same as /stale):

  days_since = days between last_validated_commit date and now
  time_decay = days_since * decay_rate
  code_penalty = commits_since * code_change_penalty
  boost = revalidation_boost * (diminishing_factor ^ validation_count)

  score = clamp(initial_score - time_decay - code_penalty + boost, floor, 0.95)

  Classify: healthy (>=0.70), warning (>=0.50), stale (>=0.30), archive (<0.30)

NOTE: Do NOT write computed score to frontmatter. Output only.
```

### Phase 5: Output Report

```markdown
DRIFT REPORT — {artifact}
═════════════════════════

Since last validation (commit {last_validated_commit[:7]}, {last_validated_at}):

  Code Changes:
    {N} commits touching related files
    {for each related_path with changes:}
      {path}: {count} commits
        - {commit_summary_1}
        - {commit_summary_2}

  Feedback Events:
    {M} events received since last validation
    {P} positive / {Q} negative / {R} neutral

  Confidence: {score} ({status})
    Time decay:     -{time_decay:.2f}
    Code penalty:   -{code_penalty:.2f}
    Revalidation:   +{boost:.2f}

Suggested actions:
  → /refresh {artifact} (re-validate and update baseline)
  → /observe {user} (if user canvas)
  → /ground {component} (if reality file)
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Artifact not found | Error with path suggestion |
| No confidence metadata | Report as "unknown", suggest /refresh |
| Git not available | Use validation_count only, mark "approx" |
| Baseline commit not found | Use 30-day window fallback |
| No feedback events | Report "0 events" (not an error) |
| Config missing | Use defaults |

---

## Integration Points

- **Reads**: Artifact frontmatter, git history, feedback events, `.loa.config.yaml`
- **Does NOT write**: Any files (read-only skill)
- **Related**: `/stale` (broad scan), `/refresh` (re-validate)

---

## Validation

- [ ] Reads confidence frontmatter correctly
- [ ] Git queries use commit-SHA anchoring
- [ ] Fallback for missing baseline commit works
- [ ] Feedback events filtered by target selector
- [ ] Decay formula matches /stale (same computation)
- [ ] Does NOT write to frontmatter
- [ ] Directory mode works (iterates .md files)
- [ ] Handles missing confidence as "unknown"
