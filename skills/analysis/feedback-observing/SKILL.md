---
name: feedback-observing
description: Read agent interaction logs across packs and detect operational patterns. Emits state-transition FeedbackEvents for degradation/recovery.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Feedback Observing

Read agent interaction logs across all packs, detect operational patterns (error rates, duration outliers, zero-invocation skills), and emit state-transition FeedbackEvents when patterns change.

This skill closes the agent feedback loop — agents report back what worked and what failed.

---

## Core Principle

**State-transition only emission.** Only emit FeedbackEvents when a skill's operational state *changes* (healthy → concerning, concerning → healthy). This prevents recursive signal inflation from repeated analysis of the same stable state.

---

## Triggers

```
/feedback-observe                    # Analyze all packs' agent logs
/feedback-observe --pack observer    # Specific pack only
/feedback-observe --since 7d         # Time range (default: 30d)
```

---

## When to Use

- Periodically to check agent health across packs
- After deploying new skills or modifying existing ones
- When suspecting a skill is silently failing
- As part of a daily/weekly maintenance routine

---

## Workflow

### Phase 1: Collect Logs

```
Glob: grimoires/*/agent-logs/*.jsonl

For each JSONL file:
  Parse each line (skip malformed lines, log warning)
  Filter by --pack if specified
  Filter by --since if specified (compare ts field)

Collect all log entries into a unified dataset.
```

**If no log files found**: Report "No agent logs found. Skills need to emit logs — see agent-log-format.md" and exit.

### Phase 2: Detect Patterns

Group entries by `pack` and `skill`, then compute:

```
For each (pack, skill) pair:

  1. ERROR RATE
     error_count = entries where status="error"
     total_count = all entries
     error_rate = error_count / total_count

     IF error_rate > 0.20 → state = "concerning"
     IF error_rate <= 0.10 → state = "healthy"
     IF 0.10 < error_rate <= 0.20 → state = "warning"

  2. DURATION OUTLIERS
     Compute median duration_ms across all entries for this skill
     IF any entry has duration_ms > 2x median → flag as outlier

     IF outlier_count / total_count > 0.20 → state = "slow"

  3. ZERO-INVOCATION SKILLS
     Compare skills found in logs against manifest.json skills arrays
     Skills in manifest but NOT in logs → "dormant" (potential discoverability problem)

  4. RETRY PATTERNS
     Detect same skill invoked 3+ times within 5 minutes → "friction"

  5. MISSING ARTIFACT PATTERNS
     Entries where error contains "not found" or "missing" → "missing dependency"
```

### Phase 3: Compare with Previous Report

```
Read previous report: grimoires/observer/agent-feedback/report-latest.md

IF previous report exists:
  Parse previous state per skill
  Compare current state with previous state

  ONLY emit FeedbackEvents for STATE TRANSITIONS:
    - healthy → concerning (degradation)
    - concerning → healthy (recovery)
    - new skill appeared as "dormant"
    - skill crossed duration outlier threshold for first time

  DO NOT re-emit for unchanged states.

IF no previous report:
  Treat all current states as new (emit for any non-healthy state)
```

### Phase 4: Emit State-Transition FeedbackEvents

For each state transition detected, emit via the Loa event bus:

```bash
source .claude/scripts/lib/event-bus.sh

emit_event "observer.state_transition" \
  '{
    "domain": "code",
    "target": {
      "type": "artifact",
      "selector": "{pack}/{skill}"
    },
    "signal": {
      "direction": "{negative for degradation, positive for recovery}",
      "weight": 0.5,
      "specificity": 0.7,
      "content": "{state_transition}: {description}",
      "kind": "behavioral"
    },
    "fingerprint": "{sha256 of '{pattern_type}:{pack}:{skill}:{window_start}:{window_end}'}"
  }' \
  "observer/feedback-observing" \
  "" "" \
  "{pack}/{skill}"
```

The bus auto-generates `id`, `time`, `specversion` in the CloudEvents envelope.

**Fingerprint deduplication**: The `fingerprint` field maps to the bus idempotency key. Same fingerprint = same finding for the same time window. The bus `.idempotency/` store prevents duplicate processing.

### Phase 5: Generate Report

Write to `grimoires/observer/agent-feedback/report-{YYYY-MM-DD}.md`:

```markdown
---
type: agent-feedback-report
generated: "{RFC 3339 UTC}"
period: "{start} to {end}"
packs_analyzed: {N}
skills_analyzed: {N}
transitions_detected: {N}
---

# Agent Feedback Report: {date}

## Skill Health Matrix

| Pack | Skill | Invocations | Error Rate | Median Duration | State |
|------|-------|-------------|-----------|-----------------|-------|
| observer | observing-users | 12 | 8% | 340ms | healthy |
| artisan | inscribing-taste | 5 | 40% | 120ms | concerning |
| ... | ... | ... | ... | ... | ... |

## State Transitions (since last report)

| Skill | Previous | Current | Evidence |
|-------|----------|---------|----------|
| artisan/inscribing-taste | healthy | concerning | Error rate 8% → 40% |

## Duration Analysis

| Skill | Median | P95 | Outliers |
|-------|--------|-----|----------|
| ... | ... | ... | ... |

## Dormant Skills

| Pack | Skill | In Manifest | Invocations |
|------|-------|-------------|-------------|
| ... | ... | yes | 0 |

## Suggested Actions

- {actionable recommendation per concerning skill}
```

Also copy to `grimoires/observer/agent-feedback/report-latest.md` (overwrite).

Create `grimoires/observer/agent-feedback/` directory if it doesn't exist.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No log files found | Report empty state, exit 0 |
| Malformed JSONL line | Skip line, log warning, continue |
| No previous report | Treat all states as new |
| Manifest not found | Skip dormant skill detection |
| `--pack` not found in logs | Report "No logs for pack {name}" |

---

## Integration Points

- **Reads**: `grimoires/*/agent-logs/*.jsonl`, `grimoires/observer/agent-feedback/report-latest.md`
- **Writes**: `grimoires/observer/agent-feedback/report-{date}.md`, `grimoires/shared/feedback/events/{date}.jsonl`
- **Depends on**: Skills emitting agent logs (Task 1.7)
- **Consumed by**: `/artisan-patterns` cross-domain analysis, `/stale` confidence system

---

## Validation

- [ ] Reads all packs' agent logs via glob
- [ ] Correctly computes error rate, duration outliers
- [ ] Only emits FeedbackEvents on state transitions
- [ ] Fingerprint prevents duplicate emissions for same window
- [ ] Report includes all analyzed skills
- [ ] `report-latest.md` is updated
- [ ] `--pack` filter works correctly
- [ ] `--since` filter works correctly
- [ ] Handles empty/missing log directories gracefully
