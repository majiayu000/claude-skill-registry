---
name: ralph-bridge
description: Fresh-instance orchestration for multi-story features. Use when N>5 stories risk context exhaustion. Spawns fresh Claude per story via bash script. Triggers on "ralph", "fresh instances", "multi-story loop", "context exhaustion".
---

# Ralph Bridge

Fresh-instance loop orchestration for multi-story feature development.

## When to Use

| Situation | Recommendation |
|-----------|----------------|
| Single story, clear scope | `/loop:start` |
| 2-5 related stories | `/loop:prd` with dependencies |
| **N>5 stories, independent** | **Ralph Bridge** |
| Long-running feature (days) | Ralph Bridge |
| Context exhaustion risk | Ralph Bridge |

**Key insight:** Fresh instances solve context window exhaustion. Each story gets full context.

---

## How It Works

```
┌─────────────────────────────────────────┐
│           Ralph Orchestrator            │
│         (moo-ralph.sh script)           │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌────────┐
│ Story 1│  │ Story 2│  │ Story 3│
│ Fresh  │  │ Fresh  │  │ Fresh  │
│ Claude │  │ Claude │  │ Claude │
└────────┘  └────────┘  └────────┘
    │            │            │
    ▼            ▼            ▼
┌─────────────────────────────────────────┐
│           prd.json + progress.txt       │
│            (Shared State)               │
└─────────────────────────────────────────┘
```

---

## Prerequisites

1. **prd.json** — Structured PRD with stories
2. **Git branch** — Feature branch for all work
3. **Claude Code** — Installed and configured

### prd.json Format

```json
{
  "feature": "User Settings",
  "branch": "feature/user-settings",
  "stories": [
    {
      "id": "S-001",
      "title": "Settings route",
      "description": "Add /settings route with basic layout",
      "acceptance": [
        "Route renders without error",
        "Navigation link added to header"
      ],
      "blockedBy": [],
      "passes": false
    },
    {
      "id": "S-002",
      "title": "Settings form",
      "description": "Create form with email and name fields",
      "acceptance": [
        "Form validates required fields",
        "Submit calls API endpoint"
      ],
      "blockedBy": ["S-001"],
      "passes": false
    }
  ]
}
```

---

## Usage

### Basic

```bash
./moo-ralph.sh
```

Runs until all stories pass or max iterations reached.

### With Options

```bash
./moo-ralph.sh [max_iterations] [--colleague-pause]
```

| Option | Description |
|--------|-------------|
| `max_iterations` | Default 50. Total Claude invocations allowed. |
| `--colleague-pause` | Pause after each story for human review. |

---

## Execution Flow

### Per-Story Protocol

1. **Pre-Flight Check**
   - Verify prd.json exists
   - Verify git branch matches
   - Check no uncommitted changes

2. **Story Selection**
   - Find first story with `passes: false`
   - Verify `blockedBy` stories all pass
   - Skip blocked stories

3. **Silent Audit (per story)**
   - Score spec (should be ≥8 for well-written PRD)
   - Calculate fit score
   - Determine workflow shape

4. **Must-NOT Extraction**
   - Parse story context for constraints
   - Add to circuit breaker triggers

5. **Execute**
   - Fresh Claude instance
   - Full context window available
   - Work on single story

6. **Completion Signal**
   - Claude outputs `<story-complete>` when done
   - Script verifies acceptance criteria
   - Updates prd.json with `passes: true`

---

## Completion Signals

### Story Complete

```xml
<story-complete>
Story: S-001
Acceptance verified:
- [x] Route renders without error
- [x] Navigation link added
</story-complete>
```

### Feature Complete

```xml
<feature-complete>
All stories complete:
- S-001: Settings route ✓
- S-002: Settings form ✓
- S-003: Settings API ✓
</feature-complete>
```

---

## Progress Tracking

### progress.txt

Human-readable log of all story completions:

```
[2026-02-01 10:15] S-001: Settings route - COMPLETE
[2026-02-01 10:32] S-002: Settings form - COMPLETE
[2026-02-01 10:45] S-003: Settings API - IN PROGRESS
```

### prd.json Updates

After each story completes:

```json
{
  "id": "S-001",
  "passes": true,
  "completedAt": "2026-02-01T10:15:00Z"
}
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Story fails 3x consecutively | Pause, request human intervention |
| Dependency not met | Skip to next available story |
| Git conflict | Pause, require manual resolution |
| Budget exceeded | Pause with progress summary |

---

## Colleague Mode

With `--colleague-pause`, after each story:

```
[RALPH] Story S-001 complete
Acceptance criteria verified:
- Route renders: ✓
- Nav link added: ✓

Continue to S-002? [Y/n/skip/quit]
```

| Response | Action |
|----------|--------|
| Y (default) | Continue to next story |
| n | Re-run current story |
| skip | Mark as skipped, move to next |
| quit | Stop orchestration |

---

## Limitations

- **No cross-story context:** Each instance is fresh
- **Sequential by default:** Parallel requires multiple scripts
- **JSON output parsing:** Stories must signal completion clearly
- **Git-based:** Requires clean working directory

---

## When NOT to Use

| Situation | Why Not | Alternative |
|-----------|---------|-------------|
| Stories are interdependent | Context loss hurts | `/loop:prd` |
| Rapid iteration needed | Script overhead | `/loop:start` |
| Debug/investigation | Fresh context loses findings | Standard loop |
| < 5 stories | Overhead not worth it | `/loop:prd` |

---

## Script Location

```
loop/scripts/moo-ralph.sh
```

Ensure executable: `chmod +x loop/scripts/moo-ralph.sh`
