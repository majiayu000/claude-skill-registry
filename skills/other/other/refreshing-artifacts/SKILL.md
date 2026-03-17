---
name: refreshing-artifacts
description: Re-validate an artifact and update its confidence inputs. Routes to appropriate re-validation skill based on artifact type.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Refreshing Artifacts

Re-validate an artifact by routing to the appropriate re-validation skill, then update confidence inputs (NOT the computed score) in frontmatter.

---

## Core Principle

**Update inputs, not outputs.** This skill updates `last_validated_at`, `last_validated_commit`, and `validation_count` in frontmatter. It never stores a computed confidence score — that is always derived by `/stale` and `/drift`.

---

## Triggers

```
/refresh {artifact-path}
```

**Examples**:
```
/refresh grimoires/observer/canvas/xabbu-canvas.md
/refresh grimoires/artisan/taste.md
/refresh grimoires/observer/reality/profile.md
```

---

## When to Use

- After `/stale` or `/drift` shows an artifact needs refreshing
- After significant code changes to validate artifact is still accurate
- Periodically to keep high-value artifacts fresh
- To initialize confidence tracking on artifacts without metadata

---

## Workflow

### Phase 1: Read Artifact

```
Parse YAML frontmatter:
  - type (user-canvas, journey, reality, taste, etc.)
  - confidence block (may be missing)

IF confidence block is MISSING:
  Initialize confidence metadata:
    confidence:
      created_at: {now, RFC 3339 UTC}
      last_validated_at: {now}
      last_validated_commit: {git rev-parse HEAD}
      validation_count: 0
      related_paths: {infer from artifact type — see defaults below}

  Write frontmatter and report "Confidence tracking initialized for {path}"
  Skip Phase 2 (no re-validation needed for initialization)
  Proceed to Phase 3
```

### Phase 2: Route to Re-Validation

Based on artifact type, suggest and perform the appropriate re-validation:

```
IF type == "user-canvas":
  → Suggest: /observe --enrich @{user} --wallet {wallet}
  → Run Score API enrichment to refresh snapshot
  → Update frontmatter score_snapshot if wallet available

IF type == "journey":
  → Suggest: /shape {journey-id}
  → Re-validate journey against current canvases

IF type == "reality":
  → Suggest: /ground {component}
  → Re-extract from current codebase

IF type == "taste" or artifact is grimoires/artisan/taste.md:
  → Suggest: Review taste tokens against current design
  → Validate taste.md still reflects current brand direction

IF type is unknown or unrecognized:
  → Inform user: "Cannot auto-route — please validate manually"
  → Still update confidence inputs in Phase 3
```

### Phase 3: Update Confidence Inputs

Update ONLY these frontmatter fields:

```yaml
confidence:
  last_validated_at: "{now, RFC 3339 UTC}"
  last_validated_commit: "{git rev-parse HEAD}"
  validation_count: {previous + 1}
  # created_at: UNCHANGED (immutable)
  # related_paths: UNCHANGED (unless user specifies)
```

**Do NOT store a computed `current` score.** Score is always derived.

### Phase 4: Emit FeedbackEvent

Emit to `grimoires/shared/feedback/events/{YYYY-MM-DD}.jsonl`:

```json
{
  "schema_version": 1,
  "id": "fe-{unix_timestamp}-{random4hex}",
  "timestamp": "{RFC 3339 UTC}",
  "domain": "{inferred from artifact type: research for canvas, design for taste, code for reality}",
  "source_pack": "observer",
  "source_skill": "refreshing-artifacts",
  "target": {
    "type": "artifact",
    "selector": "{artifact path relative to repo root}"
  },
  "signal": {
    "direction": "positive",
    "weight": 0.7,
    "specificity": 0.8,
    "content": "Artifact re-validated, confidence inputs updated (validation #{N})",
    "kind": "behavioral"
  },
  "context": {
    "artifact_path": "{artifact path}",
    "confidence_at_time": "{computed score at time of refresh (for reference only)}"
  }
}
```

### Phase 5: Report Output

```
✓ Artifact refreshed: {artifact-path}

  Validation: #{validation_count}
  Baseline commit: {last_validated_commit[:7]}
  Previous confidence: {computed score before refresh}
  Current confidence:  {computed score after refresh}
  Boost applied:       +{boost value}

  Re-validation: {what was done or suggested}

Next steps:
  → /stale (check overall artifact health)
  → /drift {path} (see detailed drift report)
```

---

## Default Related Paths

When initializing confidence for the first time, infer `related_paths` from artifact type:

| Artifact Type | Default related_paths |
|---------------|----------------------|
| user-canvas | `["lib/score-api/**", "grimoires/observer/canvas/"]` |
| journey | `["grimoires/observer/canvas/", "grimoires/observer/journeys/"]` |
| reality | `["src/", "lib/"]` |
| taste | `["grimoires/artisan/", "src/components/"]` |
| unknown | `[]` (empty — user should configure) |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Artifact not found | Error with path suggestion |
| Git not available | Use current timestamp, skip commit SHA, warn |
| Frontmatter parse error | Attempt repair, or error with backup suggestion |
| Re-validation skill not available | Update inputs anyway, note in report |
| No wallet for canvas enrichment | Skip enrichment, update inputs only |

---

## Integration Points

- **Reads**: Artifact frontmatter, git state
- **Writes**: Artifact frontmatter (confidence inputs only), FeedbackEvent
- **Routes to**: `/observe --enrich`, `/shape`, `/ground` (depending on type)
- **Consumed by**: `/stale` and `/drift` (after refresh, scores improve)

---

## Validation

- [ ] Reads confidence frontmatter correctly
- [ ] Initializes confidence when missing
- [ ] Routes to correct re-validation per type
- [ ] Updates ONLY inputs (last_validated_at, last_validated_commit, validation_count)
- [ ] Does NOT store computed score
- [ ] Emits FeedbackEvent
- [ ] Report shows before/after confidence
- [ ] Default related_paths are reasonable per type
