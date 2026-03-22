---
name: completion-promise
description: Ralph Wiggum-style completion promise tracking for System 3 sessions. Use when starting a new session with user goals, when verifying feature completion, or when the stop hook needs to evaluate if the session can end. Triggers on session start, completion promise, goal tracking, feature verification, stop gate.
title: "Completion Promise"
status: active
---

# Completion Promise Skill

File-based state tracking that ensures sessions only complete when user goals are verifiably achieved.

## Core Concept

Every session has a **Completion Promise** - the verifiable success criteria extracted from the user's initial request. The session cannot end until these criteria are met or the user explicitly permits early exit.

```
User Prompt → Extract Goals → Track Progress → Verify Completion → Allow Stop
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `cs-init` | Initialize session state (with `--reset` to clear) |
| `cs-promise --create "Title" --ac "Criterion"` | Create promise with structured acceptance criteria |
| `cs-promise --add-ac <id> "Criterion"` | Add criterion to existing promise |
| `cs-promise --meet <id> --ac-id AC-1 --evidence "..." --type test` | Submit evidence for a criterion |
| `cs-promise` | Set epics and features (`--epic`, `--feature`, `--summary`) |
| `cs-status` | Show completion state + extract context (`--goal`, `--prompt`, `--prd`) |
| `cs-verify` | Verify, update status, check readiness (`--check` for stop hook) |

**Scripts location**: `.claude/scripts/completion-state/`

> **DISAMBIGUATION WARNING**: `cs-promise` and `cs-verify` are SEPARATE scripts.
> - `cs-promise` — Create, manage, and submit evidence for promises
> - `cs-verify` — Verify promises and check session readiness
> - **CORRECT**: `cs-verify --promise <id>` (verify a promise)
> - **WRONG**: `cs-promise --verify <id>` (`--verify` flag does NOT exist on cs-promise)

### Consolidated CLI (v2.0)

The CLI has been consolidated from 8 scripts to 4 essential commands:

| Old Command | New Command | Migration |
|-------------|-------------|-----------|
| `cs-add-epic` | `cs-promise --epic` | Use `cs-promise --epic "Title"` |
| `cs-add-feature` | `cs-promise --feature` | Use `cs-promise --feature "Title" --epic E1` |
| `cs-extract` | `cs-status --goal/--prompt/--prd` | Use `cs-status --goal "Description"` |
| `cs-check` | `cs-verify --check` | Use `cs-verify --check [--verbose]` |
| `cs-update` | `cs-verify` | Use `cs-verify --feature F1.1 --status in_progress` |

Archived scripts are in `.claude/scripts/completion-state/archive/`

---

## Session Directory Isolation (NEW)

**Orchestrators use unique session directories to prevent completion state conflicts.**

### Environment Variable

```bash
# Set BEFORE launching Claude Code in orchestrator
export CLAUDE_SESSION_DIR="initiative-${INITIATIVE_NAME}-$(date +%Y%m%d-%H%M%S)"
mkdir -p .claude/completion-state/$CLAUDE_SESSION_DIR
```

### Path Resolution

| CLAUDE_SESSION_DIR | State Path |
|--------------------|------------|
| Not set (default) | `.claude/completion-state/session-state.json` |
| `initiative-auth-20260107-1030` | `.claude/completion-state/initiative-auth-20260107-1030/session-state.json` |

### Why Session Isolation?

- **Prevents conflicts**: Multiple orchestrators don't overwrite each other's state
- **Enables parallel work**: Each initiative tracks its own completion promise
- **Preserves history**: Session states persist after orchestrator terminates

**Note**: The `cs-*` scripts automatically use `$CLAUDE_SESSION_DIR` if set.

---

## Session State Schema

The session state is stored in `.claude/completion-state/${CLAUDE_SESSION_DIR:-default}/session-state.json`:

> **Note**: The `CLAUDE_SESSION_DIR` environment variable enables session isolation. When set (e.g., `export CLAUDE_SESSION_DIR=epic4-20260107`), each orchestrator maintains its own completion state. If not set, defaults to `default/` directory. System 3 sets this automatically when spawning orchestrators.

```json
{
    "version": "2.0",
    "session_id": "session-abc123",
    "started_at": "2026-01-06T10:00:00Z",
    "iteration": 1,
    "max_iterations": 25,

    "completion_promise": {
        "title": "Initiative or session title",
        "raw_prompt": "Original user prompt verbatim...",
        "summary": "One-line summary of what user wants",
        "extracted_at": "2026-01-06T10:00:00Z",
        "acceptance_criteria": [
            {
                "id": "AC-1",
                "description": "First measurable criterion",
                "status": "pending|met|failed",
                "evidence": null,
                "evidence_type": null,
                "met_at": null,
                "met_by": null
            },
            {
                "id": "AC-2",
                "description": "Second measurable criterion",
                "status": "pending|met|failed",
                "evidence": "Test suite passed: 42/42 green",
                "evidence_type": "test|api|e2e|manual|log",
                "met_at": "2026-01-06T11:00:00Z",
                "met_by": "worker-backend"
            }
        ]
    },

    "goals": [
        {
            "id": "G1",
            "description": "Primary goal from user prompt",
            "acceptance_criteria": [
                "Criterion 1 that must be true",
                "Criterion 2 that must be true"
            ],
            "status": "pending|in_progress|passed|failed",
            "verification": null
        }
    ],

    "prd": {
        "source": "path/to/prd.md or null",
        "epics": [
            {
                "id": "E1",
                "title": "Epic title from PRD",
                "status": "pending|in_progress|passed|failed",
                "features": [
                    {
                        "id": "F1.1",
                        "title": "Feature title",
                        "acceptance_criteria": ["Criterion 1", "Criterion 2"],
                        "status": "pending|in_progress|passed|failed",
                        "verification": {
                            "type": "test|api|e2e|manual",
                            "proof": "Description of verification evidence",
                            "command": "Command that was run",
                            "output_summary": "Key output lines",
                            "verified_at": "2026-01-06T11:00:00Z"
                        }
                    }
                ]
            }
        ]
    },

    "progress_log": [
        {
            "iteration": 1,
            "timestamp": "2026-01-06T10:30:00Z",
            "action": "Implemented F1.1",
            "outcome": "success|partial|failed",
            "details": "What happened",
            "learnings": ["Pattern discovered", "Gotcha encountered"]
        }
    ],

    "codebase_patterns": [
        "Pattern 1 discovered during implementation",
        "Pattern 2 for future reference"
    ]
}
```

---

## Initialization

### For System 3: At Session Start

```bash
# 1. Initialize session state
.claude/scripts/completion-state/cs-init

# 2. Extract goals from user's first prompt
.claude/scripts/completion-state/cs-status --prompt "User's original prompt here..."

# 3. If PRD exists, link it
.claude/scripts/completion-state/cs-status --prd ".taskmaster/docs/PRD-{epic-name}.md"

# 4. Create completion promise with structured acceptance criteria
.claude/scripts/completion-state/cs-promise --create "Initiative title" \
    --ac "All unit tests pass" \
    --ac "API endpoints return correct responses" \
    --ac "E2E workflow validated"

# 5. Add additional criteria to existing promise (if needed)
.claude/scripts/completion-state/cs-promise --add-ac <promise-id> "New criterion discovered during work"

# 6. Add epics and features from PRD
.claude/scripts/completion-state/cs-promise --epic "Epic title"
.claude/scripts/completion-state/cs-promise --feature "Feature title" --epic E1 --criteria "Criterion 1"
```

> **Breaking Change (v2.0)**: `cs-promise --create` now **requires** at least one `--ac` flag. Promises without structured acceptance criteria are no longer accepted.

### Extraction Prompt for System 3

When a user provides their first prompt, extract:

1. **Goals**: What the user ultimately wants to achieve
2. **Acceptance Criteria**: How we know each goal is met
3. **PRD Reference**: If user mentions a PRD, extract epics/features from it

Example extraction:
```
User: "I want to implement Epic 4 from the work-history PRD. The voice agent
should be able to handle voicemail detection and retry calls."

Extracted:
- Goal G1: "Voice agent handles voicemail detection"
  - AC: "Agent detects voicemail greeting within 5 seconds"
  - AC: "Agent hangs up on voicemail"
- Goal G2: "Voice agent retries calls"
  - AC: "Failed calls are rescheduled"
  - AC: "Max 3 retry attempts per number"
- PRD: work-history-verification-mvp-prd.md, Epic 4
```

---

## Updating Status

### Mark Feature as In Progress

```bash
.claude/scripts/completion-state/cs-verify --feature F1.1 --status in_progress
```

### Mark Feature as Passed with Verification

```bash
.claude/scripts/completion-state/cs-verify --feature F1.1 \
    --type test \
    --command "pytest tests/test_voicemail.py -v" \
    --proof "All 5 voicemail detection tests passed"
```

### Mark Goal as Passed

```bash
.claude/scripts/completion-state/cs-verify --goal G1 --status passed
# Or with verification proof:
.claude/scripts/completion-state/cs-verify --goal G1 \
    --type e2e \
    --proof "Voice agent correctly detects voicemail in E2E test"
```

### Log Progress

```bash
.claude/scripts/completion-state/cs-verify --log \
    --action "Implemented voicemail detection" \
    --outcome "success" \
    --learning "AMD detection requires 3-second silence threshold"
```

---

## Checking Completion

### Manual Status Check

```bash
.claude/scripts/completion-state/cs-status
```

Output:
```
Session: session-abc123 (iteration 3/25)
Started: 2026-01-06T10:00:00Z

COMPLETION PROMISE:
"Implement Epic 4 voicemail handling"

GOALS:
  [PASSED] G1: Voice agent handles voicemail detection
    - [x] Agent detects voicemail greeting within 5 seconds
    - [x] Agent hangs up on voicemail
  [IN_PROGRESS] G2: Voice agent retries calls
    - [x] Failed calls are rescheduled
    - [ ] Max 3 retry attempts per number

PRD: work-history-verification-mvp-prd.md
EPICS:
  [PASSED] E4: Voicemail Detection
    [PASSED] F4.1: AMD Integration (verified: test)
    [PASSED] F4.2: Voicemail Greeting Detection (verified: test)
    [IN_PROGRESS] F4.3: Retry Scheduling

COMPLETION: 75% (3/4 goals criteria met)
VERDICT: NOT COMPLETE - 1 criterion remaining
```

### Stop Hook Evaluation

```bash
.claude/scripts/completion-state/cs-verify --check [--verbose]
```

Exit codes:
- `0`: All goals and criteria passed - session can end
- `1`: Error reading state
- `2`: Criteria not met - session should continue (returns reason)

---

## Stop Hook Integration

The stop hook uses `cs-verify --check` to gate session completion:

```bash
# In stop-gate.py or stop-hook.sh
result=$(cs-verify --check 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    # All criteria met - allow stop
    exit 0
elif [ $exit_code -eq 2 ]; then
    # Criteria not met - block stop, inject reason
    echo "COMPLETION CRITERIA NOT MET:"
    echo "$result"
    echo ""
    echo "Continue working on: $result"
    exit 2  # Block stop
else
    # Error - allow stop to avoid infinite loop
    exit 0
fi
```

---

## For System 3: Session Flow

### 1. Session Start (First Prompt)

```python
# Initialize state
Bash("cs-init")

# Extract goals from user prompt
Bash(f"cs-status --prompt '{user_prompt}'")

# If PRD referenced, link it
if prd_path:
    Bash(f"cs-status --prd '{prd_path}'")

# Create promise with structured acceptance criteria
Bash('cs-promise --create "Initiative title" '
     '--ac "All unit tests pass" '
     '--ac "API endpoints return correct responses" '
     '--ac "E2E workflow validated"')

# Add epics/features from PRD
Bash(f"cs-promise --epic 'Epic title'")
Bash(f"cs-promise --feature 'Feature' --epic E1 --criteria 'Criterion'")

# Store to Hindsight for meta-awareness
mcp__hindsight__retain(
    content=f"Session started with completion promise: {summary}",
    context="cobuilder-completion-tracking"
)
```

### 2. During Work

```python
# Before starting a feature
Bash(f"cs-verify --feature {feature_id} --status in_progress")

# After completing a feature - meet specific acceptance criteria with evidence
Bash(f'cs-promise --meet <promise-id> --ac-id AC-1 --evidence "42/42 tests passed" --type test')
Bash(f'cs-promise --meet <promise-id> --ac-id AC-2 --evidence "GET /api/v1/users returns 200" --type api')

# Also update feature-level verification
Bash(f"cs-verify --feature {feature_id} --type test --proof '{proof}'")

# Log progress
Bash(f"cs-verify --log --action '{action}' --outcome '{outcome}'")
```

### 3. Before Stopping

The stop hook automatically runs `cs-verify --check`. If blocked:
- Read the returned reason
- Check which acceptance criteria are still unmet
- Meet remaining criteria with evidence via `cs-promise --meet`
- Only when ALL criteria show `status: "met"` will verification pass

```python
# Check which criteria remain unmet
Bash("cs-verify --check --verbose")

# Meet remaining criteria
Bash('cs-promise --meet <id> --ac-id AC-3 --evidence "E2E scenario passed" --type e2e')

# Verify (only succeeds when all criteria are met)
Bash('cs-verify --promise <id>')
```

### 4. Orchestrator Awareness

When spawning orchestrators, inject completion context:

```python
# Include in wisdom injection
completion_context = Bash("cs-status --json")

wisdom = f"""
## Active Completion Promise
{completion_context}

Your work contributes to these goals. Report completion with verification proof.
Use cs-promise --meet to submit per-criterion evidence.
"""
```

---

## Codebase Patterns (Accumulated Learnings)

The session state tracks codebase patterns discovered during implementation:

```bash
# Add a pattern
.claude/scripts/completion-state/cs-verify --pattern "Migrations: Use IF NOT EXISTS for idempotency"

# View patterns
.claude/scripts/completion-state/cs-status --patterns
```

These patterns persist across iterations, building institutional knowledge.

---

## Testing Sub-Agent

System 3 can spawn a verification sub-agent to validate completion:

```python
Task(
    subagent_type="general-purpose",
    model="sonnet",
    description="Verify completion criteria",
    prompt="""
    Read .claude/completion-state/session-state.json

    For each goal and feature marked as 'passed':
    1. Verify the proof is valid
    2. Run the verification command if provided
    3. Confirm the criteria are actually met

    Report:
    - VERIFIED: [list of truly verified items]
    - FAILED: [list of items that don't meet criteria]
    - NEEDS_VERIFICATION: [list without proof]

    Update session-state.json with your findings.
    """
)
```

---

## Files

| File | Purpose |
|------|---------|
| `.claude/completion-state/${CLAUDE_SESSION_DIR:-default}/session-state.json` | Current session state (session-isolated) |
| `.claude/completion-state/${CLAUDE_SESSION_DIR:-default}/history/` | Previous session states |
| `.claude/scripts/completion-state/cs-*` | CLI scripts |
| `.claude/hooks/completion-gate.py` | Stop hook integration |

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDE_SESSION_DIR` | Session isolation directory | `epic4-20260107` |

When `CLAUDE_SESSION_DIR` is set, completion state is isolated per-session. This prevents parallel orchestrators from contaminating each other's completion tracking.

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Marking passed without proof | No verification evidence | Always include proof with `cs-verify --type --proof` |
| Stopping before all goals pass | Incomplete work | Let stop hook block until complete |
| Not extracting goals from prompt | No completion criteria | Always run `cs-status --goal` at session start |
| Manual status claims | No file-based tracking | Use `cs-verify --status` for all status changes |
| Creating promise without `--ac` | No measurable criteria | Always include at least one `--ac` flag with `--create` |
| Using `--proof` without per-AC evidence | Bypasses structured accountability | Use `cs-promise --meet` for each criterion individually |
| Verifying with unmet criteria | Incomplete work, hollow closure | Meet ALL acceptance criteria first, then run `cs-verify` |

---

## Integration with Beads

The completion promise tracks session goals, while Beads tracks work items:

| System | Tracks | Granularity | Who Uses |
|--------|--------|-------------|----------|
| Completion Promise | Session goals | Session | System 3, Stop Hook |
| Beads | Work items | Epic/Task | Orchestrators, Workers |

They complement each other:
- Close a Bead task → Update feature in completion state
- All features pass → Goal criteria may be met
- Stop hook checks completion state → Beads closure is evidence

---

## Validation Response Workflow (Gate 2)

Gate 2 of `cs-verify` checks that **every acceptance criterion** has a corresponding validation file with a passing verdict.

### Storing Validation Results

Use `cs-store-validation` to write a validation response for a specific acceptance criterion:

```bash
cs-store-validation --promise <promise-id> --ac-id AC-1 --response '{
  "verdict": "PASS",
  "reasoning": "All 5 test cases passed with expected output",
  "criteria_results": [
    {
      "criterion_id": "AC-1",
      "status": "PASS",
      "evidence": "pytest tests/test_auth.py: 5/5 passed"
    }
  ]
}'
```

### Validation JSON Schema

Each validation file follows this structure:

```json
{
  "verdict": "PASS",
  "reasoning": "Human-readable explanation of the verdict",
  "criteria_results": [
    {
      "criterion_id": "AC-1",
      "status": "PASS|FAIL",
      "evidence": "Description of evidence or test output"
    }
  ]
}
```

### Valid Verdicts

| Verdict | Meaning | Gate 2 Result |
|---------|---------|---------------|
| `PASS` | Criterion fully met | Accepted |
| `PARTIAL` | Criterion partially met (acceptable) | Accepted |
| `FAIL` | Criterion not met | Blocked |
| `BLOCKED` | Cannot validate (dependency issue) | Blocked |

Verdicts are **case-insensitive** — `pass`, `Pass`, and `PASS` are all accepted.

### Storage Location

Validation files are stored at:

```
.claude/completion-state/validations/{promise-id}/{AC-X}-validation.json
```

### How Gate 2 Connects to cs-verify

When you run `cs-verify --promise <id>`, Gate 2:

1. Reads the promise's acceptance criteria from `session-state.json`
2. For each criterion (`AC-1`, `AC-2`, etc.), looks for a validation file at the storage location above
3. Reads the `verdict` field from each validation JSON
4. **PASS** or **PARTIAL** → criterion accepted
5. **FAIL** or **BLOCKED** → verification blocked with reason
6. **Missing file** → verification blocked with "Missing validation" message
7. All criteria must have accepted verdicts for Gate 2 to pass

---

**Version**: 2.0.0
**Dependencies**: jq, bash
**Integration**: cobuilder-meta-orchestrator, stop-gate.py
**Inspired By**: Ralph Wiggum plugin (completion promise pattern)
**Breaking Changes (v2.0)**: `cs-promise --create` now requires at least one `--ac` flag. Per-criterion evidence via `cs-promise --meet` replaces bulk `--proof` for structured accountability.
