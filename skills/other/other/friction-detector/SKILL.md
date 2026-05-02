---
name: friction-detector
description: 'Detect friction signals during execution and graduate recurring patterns into rules. Use for session retrospectives and learning pipeline automation.'
version: 1.9.3
alwaysApply: false
trigger: friction, friction detection, session retrospective, learning pipeline, recurring mistakes, pattern graduation, friction report
model_hint: standard
---

# Friction-to-Learning Pipeline

Detect friction signals during agent execution, track
them across sessions, and graduate recurring patterns
into permanent guidance. Bridges the gap between
ephemeral session friction and durable CLAUDE.md rules.

**Research backing**: Claude Coach (hook-based friction
detection with SQLite storage), alirezarezvani's
self-improving-agent (three-tier MEMORY to CLAUDE.md
graduation), and the ACE framework (arXiv: evolving
playbooks from execution feedback, +10.6% on agent
tasks).

**Current gap**: LEARNINGS.md exists but requires manual
aggregation via `/abstract:aggregate-logs`. This skill
adds automatic friction detection and a structured
promotion path.

## Friction Signal Types

| Signal | Detection Method | Weight |
|--------|-----------------|--------|
| Repeated corrections | User overrides same tool call 2+ times in session | High |
| Command failures | Exit code != 0 patterns (same command type fails repeatedly) | Medium |
| Permission denials | User denies tool call, indicating unexpected behavior | High |
| Re-reads | Same file read 3+ times in session (lost context) | Low |
| Retry loops | Same action attempted 3+ times with variations | Medium |
| User frustration | Explicit negative feedback or correction language | High |

Weight scoring: High = 3, Medium = 2, Low = 1 points
per occurrence. Weighted score determines graduation
velocity.

## Three-Tier Storage Graduation

```
Tier 1: Friction Log (ephemeral, per-session)
  Location: ~/.claude/friction/sessions/{date}-{id}.json
  Retention: 30 days, then pruned
  Threshold: 1 occurrence, logged, no action

Tier 2: Pattern Candidate (persistent, LEARNINGS.md)
  Location: ~/.claude/skills/LEARNINGS.md (friction section)
  Threshold: 3+ occurrences across 2+ sessions
  Action: flagged for review in next friction report

Tier 3: Graduated Rule (CLAUDE.md or skill update)
  Threshold: reviewed + user-approved
  Action: permanent guidance added to project/user config
  Constraint: NEVER auto-modify CLAUDE.md
```

### Graduation Formula

```
graduation_score = (weighted_count * recency_factor) / sessions_seen

recency_factor:
  last 7 days  = 1.0
  8-14 days    = 0.7
  15-30 days   = 0.4
  31+ days     = 0.1

Tier 2 threshold: graduation_score >= 6.0
Tier 3 proposal:  graduation_score >= 12.0
```

## Detection Workflow

Run at session end, at 80% context usage (via
`conserve:clear-context`), or after failed improvement
cycles (when `metacognitive-self-mod` detects regression).

### Step 1: Scan Session for Signals

For each friction indicator found, record:

```json
{
  "signal_type": "retry_loop",
  "description": "rg command failed 3x, fell back to grep",
  "context": "searching for pattern in node_modules",
  "weight": "medium",
  "timestamp": "2026-04-14T10:23:00Z",
  "session_id": "abc123"
}
```

### Step 2: Compare Against Existing Log

```bash
FRICTION_DIR=~/.claude/friction/sessions
mkdir -p "$FRICTION_DIR"

# Count prior occurrences of similar signals
if command -v rg &>/dev/null; then
  rg -c "$SIGNAL_TYPE" "$FRICTION_DIR"/*.json 2>/dev/null || echo "0"
else
  grep -rc "$SIGNAL_TYPE" "$FRICTION_DIR"/*.json 2>/dev/null || echo "0"
fi
```

### Step 3: Calculate Graduation Score

Aggregate across session logs: sum weighted occurrences,
apply recency decay, divide by session count, compare
against tier thresholds.

### Step 4: Propose Graduations

Tier 2 crossing: append to LEARNINGS.md friction section.
Tier 3 crossing: present proposal with evidence to user,
wait for explicit approval before any modification.

### Step 5: Store Results

Write session log to
`~/.claude/friction/sessions/{date}-{session_id}.json`
and update `~/.claude/friction/index.json`.

## Anti-Noise Rules

Ignore these signals:

1. **One-off failures**: transient network/CI errors
   (unless they recur 3+ times)
2. **User-initiated exploration**: deliberate
   experimentation is not agent error
3. **Already-graduated patterns**: covered by existing
   CLAUDE.md rules or skill instructions
4. **External tool failures**: MCP server crashes and
   similar tool bugs unrelated to agent behavior

Decay factor: signals older than 30 days contribute
only 10% of their original weight (see graduation
formula recency_factor).

## Friction Report Format

```markdown
## Friction Report -- Session {date}

### New Signals (Tier 1)
- [RETRY] `rg` command failed 3x, fell back to `grep`
- [RE-READ] Read SKILL.md 4 times (lost file structure context)

### Recurring Patterns (Tier 2 candidates)
- [CORRECTION] User corrected file path format 4x across 3 sessions
  Score: 8.4 (threshold: 6.0)
  Candidate: Add path format guidance to CLAUDE.md

### Graduation Proposals (Tier 3)
- [RULE] "Always use absolute paths in Read tool"
  Evidence: 7 corrections across 5 sessions
  Score: 14.2 (threshold: 12.0)
  Action: Approve / Reject / Defer

### Noise Filtered
- 2 transient network timeouts (ignored)
- 1 user-initiated deep exploration (ignored)
```

## Integration

**Feeds into**: LEARNINGS.md (Tier 2 patterns, same
format as `/abstract:aggregate-logs`),
skill-improver (priority scoring), and
metacognitive-self-mod (pipeline effectiveness).

**Consumes from**: session transcripts,
`aggregate_learnings_daily` hook data, and the
performance tracker for trend correlation.

## When NOT to Use

- Single isolated failures (wait for recurrence)
- Skill authoring (use `abstract:skill-authoring`)
- Routine log aggregation (use `/abstract:aggregate-logs`)

## Related

- `abstract:metacognitive-self-mod`: improvement analysis
- `abstract:skills-eval`: evaluation criteria
- `/abstract:aggregate-logs`: manual LEARNINGS.md generation
- `conserve:clear-context`: triggers friction scan at 80%
