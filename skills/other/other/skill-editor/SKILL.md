---
name: skill-editor
description: Use when creating, modifying, or refactoring Claude Code skills that require structured multi-agent review and quality validation

# Handoff metadata (custom extension -- see workflow-coordinator/references/frontmatter-metadata-standard.md)
handoff:
  accepts_from:
    - "*"
  provides_to:
    - programming-pm
    - technical-pm
  schema_version: "3.0"
  schema_type: universal

categories:
  - skill-development
  - workflow-creation

input_requirements:
  - specification
  - skill-request

output_types:
  - skill
  - agent-configuration
  - documentation
---

# Skill Editor

Comprehensive multi-agent workflow system for editing Claude Code skills with structured phases, quality gates, and expert review.

## When to Use This Skill

Use this skill when:

1. **Creating new skills**: User wants to add a new skill to the repository
2. **Modifying existing skills**: User wants to update, enhance, or refactor a skill
3. **Complex skill changes**: Change involves multiple files, agents, or architectural decisions
4. **Quality assurance needed**: Change requires thorough review and validation

This skill provides:
- Structured 4-phase workflow
- Interactive requirements refinement
- Parallel expert analysis (4 simultaneous agents)
- Adversarial review before implementation
- Automated validation and testing
- Integration with sync-config.py and planning journal

## When NOT to Use This Skill

Do NOT use this skill when:

- **Simple documentation fixes**: Typo fixes, minor documentation updates (edit directly)
- **Non-skill changes**: Modifying agents, settings, or other configuration
- **Urgent hotfixes**: Emergency fixes that can't wait for full workflow
- **Exploratory work**: Just browsing or understanding skills (use Read or Explore agent)

## Delegation Mandate

You are an **orchestrator**. You coordinate specialist agents -- you do not perform specialist analysis, research, or implementation yourself.

**You ARE the coordinator who ensures** analysis, research, review, and implementation happen through delegation to specialist agents via Task tool.

**You are NOT** an analyst, researcher, reviewer, or implementor. You do not perform best-practices analysis, external research, edge-case simulation, knowledge-engineering analysis, adversarial review, or code implementation yourself.

**Orchestrator-owned tasks** (you DO perform these yourself):
- Session setup, directory creation, state file management
- Mode detection and user interaction for mode selection
- Quality gate evaluation (checking that agent outputs meet criteria)
- User communication (presenting options, gathering decisions)
- Workflow routing (determining which phase to execute next)
- Pre-flight validation (git checks, file existence)
- Orchestrator detection (determining if target skill is an orchestrator)

### When You Might Be Resisting Delegation

| Rationalization | Reality |
|----------------|---------|
| "This analysis is too simple to delegate" | Simple tasks still consume context window. Delegate. |
| "I can do it faster myself" | Speed is not the goal; context isolation and specialist quality are. |
| "The agent will just repeat what I already know" | The agent provides independent verification. Your knowledge may be incomplete. |
| "It's just a quick read of the file" | Reading specialist content to make specialist decisions IS specialist work. |

**Self-check before every action**: "Am I about to load specialist instructions into my context so I can do their work? If yes, use Task tool instead."

## State Anchoring

Start every response with a phase indicator:

```
[Phase N/4 - {phase_name}] {brief status}
```

Examples:
- `[Phase 1/4 - Refinement] Gathering requirements from user`
- `[Phase 2/4 - Analysis] 3/4 agents completed, waiting for external-researcher`
- `[Phase 3/4 - Decision] Synthesizing 4 analysis reports`
- `[Phase 4/4 - Execution] Implementing change 3/12`

**Protocol**:
1. Before starting any phase: Read `${SESSION_DIR}/session-state.json`. Confirm current_phase matches expectations.
2. After any user interaction: Answer the user, then re-anchor with phase indicator.
3. If phase indicator and state file disagree: Trust state file, not memory.

## Tool Selection

| Situation | Tool | Reason |
|-----------|------|--------|
| Phase 2 parallel analysis (4 agents) | Task tool | Context isolation, parallel execution |
| Phase 2.5 strategic review | Task tool | Separate specialist context |
| Phase 3 synthesis | Task tool | Independent decision-making context |
| Phase 3 adversarial review | Task tool | Independent, skeptical review |
| Phase 4 implementation | Task tool | Isolated execution environment |
| Loading reference docs for YOUR routing decisions | Read tool | Orchestrator decision support |
| Loading skill instructions to decide WHICH specialist to invoke | Read tool (brief scan) | Routing information, not specialist work |
| User interaction (questions, approvals, options) | AskUserQuestion | Structured user communication |
| File operations (create, modify files) | Write tool (via executor agent) | Delegated to executor specialist |
| Validation scripts, git operations | Bash tool | Infrastructure commands |

**Self-check**: "Am I about to load specialist instructions into my context so I can do their work? If yes, use Task tool instead."

## Workflow Overview

```
SIMPLE MODE (15-45 min)
├── Phase 1: Refinement (5-15 min)
├── Mode Selection: User confirms SIMPLE
├── [SKIP Phase 2: No parallel analysis]
├── [SKIP Phase 2.5: No strategic review]
├── Phase 3: Lightweight Decision (10-20 min)
│   └── Minimal synthesis from specification only
└── Phase 4: Execution (10-20 min)
    └── Gates 4 & 5 always run

STANDARD MODE (1.5-3 hours) [Current default]
├── Phase 1: Refinement (10-30 min)
├── Mode Selection: User confirms STANDARD
├── Phase 2: Parallel Analysis (30-60 min, 4 agents)
├── [Phase 2.5: Strategic Review - conditional, stricter triggers]
├── Phase 3: Decision & Review (45-90 min)
│   └── Full synthesis + adversarial review
└── Phase 4: Execution (60-120 min)
    └── Gates 4 & 5 always run

EXPERIMENTAL MODE (10-30 min) [User-requested]
├── Phase 1: Quick Refinement (5-10 min)
├── Mode Selection: User explicitly requests EXPERIMENTAL
├── [SKIP Phase 2]
├── [SKIP Phase 2.5]
├── Phase 3: Minimal Decision (5-10 min)
│   └── Direct implementation plan with experimental tags
└── Phase 4: Execution with rollback plan (5-15 min)
    └── Gates 4 & 5 always run + experimental tagging
```

## Workflow

### Pre-Workflow: Safety Checks

Before starting workflow:

```bash
# Strict git pre-flight checks
echo "=== Git Safety Checks ==="

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "✗ Git working directory is not clean"
  git status --short
  echo ""
  echo "Please commit or stash changes before running skill-editor"
  exit 1
fi

# Check for merge/rebase in progress
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "✗ Rebase in progress"
  exit 1
fi

if [ -f .git/MERGE_HEAD ]; then
  echo "✗ Merge in progress"
  exit 1
fi

# Check for detached HEAD
if ! git symbolic-ref HEAD &>/dev/null; then
  echo "⚠ WARNING: Detached HEAD state"
  read -p "Continue anyway? (y/n): " CONTINUE
  [ "$CONTINUE" != "y" ] && exit 1
fi

echo "✓ Git working directory is clean"

# Check sync status
./sync-config.py status
# Should show "No changes detected" or expected divergence

# Verify in correct directory
pwd
# Should be repo root: /Users/davidangelesalbores/repos/claude

# Archival Awareness Check
# After git safety checks, detect archival guidelines for awareness (not enforcement).
# skill-editor writes to claude-config/skills/, which is typically not covered by
# archival guidelines. This check provides awareness so the request-refiner agent
# can factor archival conventions into the specification if relevant.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
ARCHIVE_METADATA="${REPO_ROOT}/.archive-metadata.yaml"
if [ -f "$ARCHIVE_METADATA" ]; then
  echo "Archival guidelines detected (.archive-metadata.yaml present)"
  echo "These will be available to the request-refiner for specification context"
  # Reference: ~/.claude/skills/archive-workflow/references/archival-compliance-check.md
  # Step 1 (detection) applied; Steps 2-5 not enforced for skill-editor output
  ARCHIVAL_GUIDELINES_PRESENT=true
else
  ARCHIVAL_GUIDELINES_PRESENT=false
fi

# Add trap for graceful interrupt handling
trap 'echo ""; echo "Session paused. Resume with: /skill-editor"; jq ".status = \"paused\"" "${SESSION_DIR}/session-state.json" > "${SESSION_DIR}/session-state.tmp.json" && mv "${SESSION_DIR}/session-state.tmp.json" "${SESSION_DIR}/session-state.json"; exit 130' INT TERM

# Session management commands
if [ "$1" = "--list-sessions" ]; then
  echo "=== All Sessions ==="
  ls -d /tmp/skill-editor-session/session-* 2>/dev/null | while read SESSION_PATH; do
    SESSION_ID=$(basename "$SESSION_PATH")
    if [ -f "${SESSION_PATH}/session-state.json" ]; then
      PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      echo "  ${SESSION_ID}"
      echo "    Status: ${STATUS} | Phase: ${PHASE} | ${TIMESTAMP}"
    fi
  done
  exit 0
fi

if [ "$1" = "--cleanup" ]; then
  echo "Scanning for completed sessions..."
  COMPLETED_SESSIONS=($(ls -d /tmp/skill-editor-session/session-* 2>/dev/null | while read SESSION_PATH; do
    STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json" 2>/dev/null)
    if [ "$STATUS" = "completed" ]; then
      echo "$SESSION_PATH"
    fi
  done))

  if [ ${#COMPLETED_SESSIONS[@]} -eq 0 ]; then
    echo "No completed sessions found"
    exit 0
  fi

  echo "Found ${#COMPLETED_SESSIONS[@]} completed session(s):"
  for SESSION_PATH in "${COMPLETED_SESSIONS[@]}"; do
    SESSION_ID=$(basename "$SESSION_PATH")
    TIMESTAMP=$(jq -r .completed_at "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
    echo "  ${SESSION_ID} - Completed: ${TIMESTAMP}"
  done

  read -p "Remove these completed sessions? (yes/no): " CONFIRM
  if [ "$CONFIRM" = "yes" ]; then
    for SESSION_PATH in "${COMPLETED_SESSIONS[@]}"; do
      rm -rf "$SESSION_PATH"
    done
    echo "✅ ${#COMPLETED_SESSIONS[@]} completed session(s) removed"
  fi
  exit 0
fi

# Resume protocol with multi-session support
SESSIONS=($(ls -d /tmp/skill-editor-session/session-* 2>/dev/null | sort -r))

if [ ${#SESSIONS[@]} -gt 0 ]; then
  echo "Found ${#SESSIONS[@]} existing session(s):"
  echo ""
  echo "Active/Paused Sessions:"
  for SESSION_PATH in "${SESSIONS[@]}"; do
    SESSION_ID=$(basename "$SESSION_PATH")
    if [ -f "${SESSION_PATH}/session-state.json" ]; then
      TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json")
      PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json")
      STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json")

      # Only show non-completed sessions by default
      if [ "$STATUS" != "completed" ]; then
        echo "  ${SESSION_ID}"
        echo "    Status: ${STATUS} | Phase: ${PHASE} | ${TIMESTAMP}"
      fi
    fi
  done
  echo ""
  echo "Options:"
  echo "  - Enter session ID to resume"
  echo "  - Enter 'list-all' to see completed sessions"
  echo "  - Enter 'n' to start new session"
  read -p "Choice: " RESUME_CHOICE

  if [ "$RESUME_CHOICE" = "list-all" ]; then
    echo ""
    echo "All Sessions (including completed):"
    for SESSION_PATH in "${SESSIONS[@]}"; do
      SESSION_ID=$(basename "$SESSION_PATH")
      if [ -f "${SESSION_PATH}/session-state.json" ]; then
        TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json")
        PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json")
        STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json")
        echo "  ${SESSION_ID} - ${STATUS} - Phase ${PHASE} - ${TIMESTAMP}"
      fi
    done
    echo ""
    read -p "Resume a session? Enter session ID or 'n' for new: " RESUME_CHOICE
  fi

  if [ "$RESUME_CHOICE" != "n" ]; then
    SESSION_ID="$RESUME_CHOICE"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
    echo "Resuming ${SESSION_ID}"
  else
    # Create new session
    SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
  fi
else
  # Check for legacy session format
  LEGACY_STATE="/tmp/skill-editor-session/session-state.json"
  if [ -f "$LEGACY_STATE" ]; then
    echo "Detected legacy session format"
    LEGACY_TIMESTAMP=$(jq -r .timestamp "$LEGACY_STATE")
    LEGACY_SESSION_ID="session-legacy-$(echo $LEGACY_TIMESTAMP | tr -d ':TZ-')"

    read -p "Migrate to new format as ${LEGACY_SESSION_ID}? (y/n): " MIGRATE
    if [ "$MIGRATE" = "y" ]; then
      mkdir -p "/tmp/skill-editor-session/${LEGACY_SESSION_ID}"
      mv /tmp/skill-editor-session/*.{json,md} "/tmp/skill-editor-session/${LEGACY_SESSION_ID}/" 2>/dev/null
      SESSION_ID="$LEGACY_SESSION_ID"
      SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
      echo "Migration complete. Resuming as ${SESSION_ID}"
    else
      # Create new session
      SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
      SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
    fi
  else
    # Create new session
    SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
  fi
fi

# Create session directory and initialize state if new session
mkdir -p "${SESSION_DIR}"
echo "Session directory: ${SESSION_DIR}"
echo "Session ID: ${SESSION_ID}"

if [ ! -f "${SESSION_DIR}/session-state.json" ]; then
  # Initialize session state with lifecycle status
  jq -n \
    --arg phase "0" \
    --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg session_id "$SESSION_ID" \
    --arg status "in_progress" \
    '{
      phase: $phase,
      timestamp: $timestamp,
      session_id: $session_id,
      status: $status,
      agents_completed: []
    }' > "${SESSION_DIR}/session-state.json"
  echo "Starting new session"
else
  echo "Resuming from Phase $(jq -r .phase ${SESSION_DIR}/session-state.json)"
fi
```

If checks fail: Ask user to resolve before proceeding.

### If User Cancels (Ctrl+C)

Session state is preserved in `${SESSION_DIR}/session-state.json`.

On next invocation:
1. Offer to resume from last phase
2. If declined, session remains in /tmp/skill-editor-session/{session-id}
3. Re-sync if needed: `./sync-config.py push`

### Phase 1: Refinement (Interactive)

**Objective**: Transform user's request into detailed, unambiguous specification.

**Agent**: `skill-editor-request-refiner`

**Model**: Opus 4.5

**Process**:

1. Launch request-refiner agent via Task tool
2. Agent asks clarifying questions to understand:
   - What user wants to change
   - Why they want this change
   - What success looks like
   - What's in scope vs. out of scope
3. Agent reads existing skill (if modifying)
4. Agent establishes clear boundaries and success criteria
5. Agent presents refined specification to user

**Output File**: `${SESSION_DIR}/refined-specification.md` containing:
- Objective (one sentence)
- Scope (IN/OUT lists)
- Success criteria (measurable)
- Files affected
- User approval

**Quality Gate 1: Specification Approval**

User must approve:
- [ ] Specification matches intent
- [ ] Scope is appropriate
- [ ] Success criteria are clear
- [ ] Ready to proceed to analysis

**If Gate 1 fails**: Return to request-refiner for more refinement.

**If Gate 1 passes**: Update session state and proceed to Mode Selection.

**Post-Gate 1: Orchestrator Detection**

After specification approval, determine if the target skill is an orchestrator:

1. Read target SKILL.md (if editing an existing skill)
2. Score against detection criteria:

| Signal | Score | Check |
|--------|-------|-------|
| Name contains orchestrator keyword (pm, coordinator, orchestrator, pipeline, architect) | +1 | Check skill name |
| Description mentions coordination terms (coordinate, orchestrate, multi-agent, pipeline) | +1 | Check description field |
| Delegates to other skills via Task tool | +2 | Search for Task tool usage |
| Has named phases/stages with sequential progression | +1 | Search for Phase/Stage headers |
| Has quality gates between phases | +1 | Search for Gate references |
| Manages session state across phases | +1 | Search for state file management |

3. Apply thresholds:
   - Score >= 4: `"Detected as orchestrator (confidence: high). Apply orchestrator analysis? [Y/n]"`
   - Score 2-3: `"May be an orchestrator (confidence: medium). Apply orchestrator analysis? [y/N]"`
   - Score 0-1: Not an orchestrator. Skip orchestrator analysis.
   - Always append: `"If this IS an orchestrator, reply 'orchestrator' to enable pattern analysis."`

4. If creating a new skill: Ask directly: "Will this skill orchestrate other skills? [y/N]"

5. Record detection result in session state (add to the session-state.json update):
   ```json
   "orchestrator_detected": true/false,
   "orchestrator_confidence": "high"/"medium"/"none",
   "orchestrator_user_confirmed": true/false
   ```

```bash
# Update session state
jq -n \
  --arg phase "1.5" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson agents_completed '["request-refiner"]' \
  '{phase: $phase, timestamp: $timestamp, agents_completed: $agents_completed}' \
  > ${SESSION_DIR}/session-state.json
```

---

### Mode Selection (After Phase 1)

**Objective**: Select workflow execution mode based on complexity detection and user preference.

**Trigger**: After Quality Gate 1 passes (specification approved)

#### Step 1: Run Three-Tier Detection

```bash
echo "=== Mode Selection ==="
echo ""

SPEC_FILE="${SESSION_DIR}/refined-specification.md"

# Source detection function (see references/complexity-detection-criteria.md)
# Inline detection for robustness

# Extract metrics (POSIX-compatible - no grep -oP)
FILES_CHANGED=$(grep -c "File:" "$SPEC_FILE" 2>/dev/null || echo 0)
# [FIX: Adversarial Issue #4] Use POSIX-compatible grep instead of grep -oP
LINES_CHANGED=$(grep -o 'Lines: [0-9]*' "$SPEC_FILE" 2>/dev/null | grep -o '[0-9]*' | awk '{sum+=$1} END {print sum+0}')
[ -z "$LINES_CHANGED" ] && LINES_CHANGED=0
SCOPE=$(grep -A10 "^## Scope" "$SPEC_FILE")

# Initialize
DETECTED_TIER="STANDARD"
CONFIDENCE="low"
REASON=""

# === FAIL-SAFE DEFAULT ===
if [ ! -f "$SPEC_FILE" ] || [ ! -s "$SPEC_FILE" ]; then
  echo "WARNING: Mode detection encountered an error (spec file issue)."
  echo "Defaulting to STANDARD mode for safety."
  DETECTED_TIER="STANDARD"
  CONFIDENCE="error"
  REASON="Spec file unreadable, defaulting to STANDARD (safest option)"
fi

# === COMPLEX DETECTION (Phase 2.5 triggers) ===
if grep -qi "Create new skill" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="New skill creation"
elif [ "$FILES_CHANGED" -gt 4 ]; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="Multiple files affected (>4)"
elif [ "$LINES_CHANGED" -gt 300 ]; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="Large change (>300 lines)"
elif grep -qi "strategic review\|architectural assessment" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="User explicitly requested strategic review"
elif grep -qi "refactor\|reorganize\|restructure\|migrate" "$SPEC_FILE" 2>/dev/null; then
  if [ "$FILES_CHANGED" -gt 2 ] || [ "$LINES_CHANGED" -gt 150 ]; then
    DETECTED_TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="Refactoring with moderate+ scope"
  fi
fi

# === SIMPLE DETECTION ===
if [ "$CONFIDENCE" != "high" ]; then
  if echo "$SCOPE" | grep -qi "documentation\|typo\|comment\|example"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      DETECTED_TIER="SIMPLE"
      CONFIDENCE="high"
      REASON="Documentation-only change"
    fi
  fi
  if echo "$SCOPE" | grep -qi "fix bug\|fix typo\|fix error"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      DETECTED_TIER="SIMPLE"
      CONFIDENCE="high"
      REASON="Minor bug fix"
    fi
  fi
fi

# === STANDARD DETECTION (default) ===
if [ "$CONFIDENCE" != "high" ]; then
  if grep -qi "agent\|workflow\|phase\|quality gate" "$SPEC_FILE" 2>/dev/null; then
    if [ "$FILES_CHANGED" -le 2 ] && [ "$LINES_CHANGED" -le 100 ]; then
      DETECTED_TIER="STANDARD"
      CONFIDENCE="medium"
      REASON="Keywords detected but change is small"
    else
      DETECTED_TIER="STANDARD"
      CONFIDENCE="medium"
      REASON="Workflow keywords with moderate change size"
    fi
  fi
fi

# === WARNING ZONE (soft thresholds) ===
if [ "$FILES_CHANGED" -ge 3 ] && [ "$FILES_CHANGED" -le 4 ]; then
  if [ "$DETECTED_TIER" = "STANDARD" ]; then
    CONFIDENCE="medium"
    REASON="$REASON (near Phase 2.5 file threshold: $FILES_CHANGED files)"
  fi
fi
if [ "$LINES_CHANGED" -ge 200 ] && [ "$LINES_CHANGED" -le 300 ]; then
  if [ "$DETECTED_TIER" = "STANDARD" ]; then
    CONFIDENCE="medium"
    REASON="$REASON (near Phase 2.5 line threshold: $LINES_CHANGED lines)"
  fi
fi

# === EXPERIMENTAL OVERRIDE (user keywords) ===
if grep -qi "experimental\|quick\|try\|test this\|prototype" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="EXPERIMENTAL"
  CONFIDENCE="high"
  REASON="User requested experimental/quick mode"
fi

# === DEFAULT for unclear ===
if [ "$CONFIDENCE" = "low" ]; then
  if [ "$FILES_CHANGED" -ge 2 ] || [ "$LINES_CHANGED" -ge 100 ]; then
    DETECTED_TIER="STANDARD"
    CONFIDENCE="low"
    REASON="Moderate size with unclear scope"
  else
    DETECTED_TIER="SIMPLE"
    CONFIDENCE="medium"
    REASON="Small change with unclear scope"
  fi
fi

echo "Detected tier: $DETECTED_TIER (confidence: $CONFIDENCE)"
echo "Reason: $REASON"
echo ""
```

#### Step 2: Display Mode Selection Prompt

```bash
cat << EOF
================================================================================
SPECIFICATION APPROVED - SELECT WORKFLOW MODE
================================================================================

Detected complexity: $DETECTED_TIER (confidence: $CONFIDENCE)
Reason: $REASON

Select workflow mode:

  [A] SIMPLE MODE          ~30 min    Skip analysis, direct implementation
      Best for: typos, documentation, single-file fixes
      Quality: Basic validation only (Gates 4, 5 always run)
      Skips: Phase 2 (4 agents), Phase 2.5 (strategic review)

  [B] STANDARD MODE        ~2-3 hrs   Full analysis and expert review
      Best for: workflow changes, features, refactoring
      Quality: 4-agent analysis + adversarial review
      Runs: All phases (current default behavior)

  [C] EXPERIMENTAL MODE    ~15 min    Minimal process, quick iteration
      Best for: prototypes, testing ideas, will iterate
      Quality: REDUCED - plan to iterate
      WARNING: Creates experimental-tagged output
      Skips: Phase 2, Phase 2.5, full adversarial review

Recommended: [$DETECTED_TIER]

Enter choice [A/B/C] (default based on detection, 60s timeout):
EOF

read -t 60 USER_CHOICE

# Handle timeout
if [ $? -ne 0 ]; then
  echo ""
  echo "No selection made. Using recommended mode: $DETECTED_TIER"
  case "$DETECTED_TIER" in
    SIMPLE) USER_CHOICE="A" ;;
    STANDARD) USER_CHOICE="B" ;;
    COMPLEX) USER_CHOICE="B" ;;  # COMPLEX uses STANDARD mode
    EXPERIMENTAL) USER_CHOICE="C" ;;
    *) USER_CHOICE="B" ;;
  esac
fi

# Normalize input
USER_CHOICE=$(echo "$USER_CHOICE" | tr '[:lower:]' '[:upper:]')

# Map selection to mode
case "$USER_CHOICE" in
  A) SELECTED_MODE="SIMPLE" ;;
  B) SELECTED_MODE="STANDARD" ;;
  C) SELECTED_MODE="EXPERIMENTAL" ;;
  *) SELECTED_MODE="STANDARD" ;;  # Default
esac
```

#### Step 3: User Override Confirmation

```bash
# Check for risky overrides
USER_OVERRIDE=false
if [ "$SELECTED_MODE" != "$DETECTED_TIER" ]; then
  USER_OVERRIDE=true

  # Additional confirmation for risky overrides
  if [ "$DETECTED_TIER" = "STANDARD" ] || [ "$DETECTED_TIER" = "COMPLEX" ]; then
    if [ "$SELECTED_MODE" = "SIMPLE" ] || [ "$SELECTED_MODE" = "EXPERIMENTAL" ]; then
      echo ""
      echo "WARNING: You selected $SELECTED_MODE but detection recommended $DETECTED_TIER."
      echo "This change may be more complex than $SELECTED_MODE mode handles."
      read -p "Confirm override? (yes/no): " CONFIRM
      if [ "$CONFIRM" != "yes" ]; then
        SELECTED_MODE="STANDARD"
        USER_OVERRIDE=false
        echo "Using recommended mode: $SELECTED_MODE"
      fi
    fi
  fi
fi

# Experimental mode warning
if [ "$SELECTED_MODE" = "EXPERIMENTAL" ]; then
  echo ""
  echo "=========================================="
  echo "  EXPERIMENTAL MODE SELECTED"
  echo "=========================================="
  echo ""
  echo "  WARNING: Reduced quality assurance"
  echo "  - No Phase 2 analysis agents"
  echo "  - Minimal decision synthesis"
  echo "  - Output will be tagged as experimental"
  echo "  - NOT production-ready without further review"
  echo ""
  read -p "Acknowledge and proceed? (yes/no): " ACK
  if [ "$ACK" != "yes" ]; then
    echo "Returning to mode selection..."
    # Re-run mode selection
  fi
fi
```

#### Step 4: Record Mode Selection

```bash
# Record mode selection in session state
jq -n \
  --arg workflow_mode "$SELECTED_MODE" \
  --arg detected_tier "$DETECTED_TIER" \
  --arg confidence "$CONFIDENCE" \
  --arg reason "$REASON" \
  --argjson user_override "$USER_OVERRIDE" \
  '{
    workflow_mode: $workflow_mode,
    detected_tier: $detected_tier,
    confidence: $confidence,
    reason: $reason,
    user_override: $user_override,
    timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }' \
  > ${SESSION_DIR}/mode-selection.json

# Update main session state
jq --arg mode "$SELECTED_MODE" \
   '. + {workflow_mode: $mode}' \
   ${SESSION_DIR}/session-state.json > ${SESSION_DIR}/session-state.tmp.json && \
   mv ${SESSION_DIR}/session-state.tmp.json ${SESSION_DIR}/session-state.json

echo ""
echo "[$SELECTED_MODE MODE] Mode selected. Proceeding..."
echo ""
```

#### Step 5: Mode-Based Branching

```bash
case "$SELECTED_MODE" in
  SIMPLE)
    echo "[$SIMPLE MODE] Skipping Phase 2 (no analysis agents)"
    echo "[$SIMPLE MODE] Skipping Phase 2.5 (no strategic review)"
    echo "[$SIMPLE MODE] Proceeding to Phase 3 (lightweight synthesis)"
    # Skip to Phase 3 Lightweight section
    ;;
  STANDARD)
    echo "[STANDARD MODE] Running full workflow"
    echo "[STANDARD MODE] Proceeding to Phase 2 (4 parallel agents)"
    # Continue to Phase 2 (existing behavior)
    ;;
  EXPERIMENTAL)
    echo "[EXPERIMENTAL MODE] Minimal workflow with experimental tagging"
    echo "[EXPERIMENTAL MODE] Skipping Phase 2 (no analysis agents)"
    echo "[EXPERIMENTAL MODE] Skipping Phase 2.5 (no strategic review)"
    echo "[EXPERIMENTAL MODE] Proceeding to Phase 3 (minimal synthesis)"
    # Skip to Phase 3 Minimal section
    ;;
esac
```

---

### Phase 2: Parallel Analysis (4 Simultaneous Agents)

**Objective**: Analyze proposed change from multiple expert perspectives.

**Agents** (all run in parallel):
1. `skill-editor-best-practices-reviewer` (Opus 4.5) - Critical
2. `skill-editor-external-researcher` (Opus 4.5) - Supplementary
3. `skill-editor-edge-case-simulator` (Opus 4.5) - Critical
4. `skill-editor-knowledge-engineer` (Opus 4.5) - Critical [NEW]

**Process**:

Launch all 4 agents with wave-based execution to reduce resource contention:

**Wave 1 (T=0s)**: Launch critical analysis agents
```markdown
Task 1: best-practices-reviewer
- Reviews against Anthropic guidelines
- Checks skill structure specification
- Identifies architectural concerns

Task 2: edge-case-simulator
- Simulates failure scenarios
- Identifies edge cases
- Proposes handling strategies
```

**Wave 2 (T=30s)**: Launch structural analysis agent
```markdown
Task 3: knowledge-engineer [NEW]
- Analyzes structural completeness via domain frameworks
- Identifies missing elements using professional standards
- Provides cross-domain pattern recommendations
```

**Wave 3 (T=60s)**: Launch supplementary research agent
```markdown
Task 4: external-researcher
- Searches community patterns and forums
- Finds relevant documentation and examples
- Identifies recommended approaches
```

**Rationale for wave-based execution**: Staggering launches by 30-60 seconds reduces system resource contention and improves reliability for parallel agent execution.

**Important**: All 4 agents run in parallel (waves overlap). Wait for all to complete before proceeding to Phase 3.

**Orchestrator Analysis (conditional -- only when orchestrator_detected is true in session state)**:

When the target skill is an orchestrator, Phase 2 agents perform additional analysis:

**best-practices-reviewer** (evaluates REQUIRED patterns):
- Use Read tool to read `/Users/davidangelesalbores/repos/claude/claude-config/skills/skill-editor/references/orchestrator-checklist.md` (REQUIRED section only)
- Evaluate the 6 REQUIRED patterns against the target skill
- For each pattern: report PRESENT / PARTIAL / ABSENT with one-sentence evidence citation
- Do NOT sacrifice general best-practices review depth for orchestrator checklist completeness

**knowledge-engineer** (evaluates RECOMMENDED patterns):
- Use Read tool to read `/Users/davidangelesalbores/repos/claude/claude-config/skills/skill-editor/references/orchestrator-checklist.md` (RECOMMENDED section only)
- Evaluate the 4 RECOMMENDED patterns as part of structural completeness analysis
- For each pattern: report PRESENT / PARTIAL / ABSENT / N/A with evidence
- N/A is valid when architectural mismatch exists (e.g., event-driven orchestrator lacks phases)

**Neither agent evaluates all 11 patterns. Division of labor prevents cognitive overload.**

**external-researcher and edge-case-simulator**: No additional orchestrator-specific tasks.

**Agent Timeouts and Retry Logic**: Each agent has a 10-minute timeout. If any agent exceeds this:

**For Critical Agents** (best-practices-reviewer, edge-case-simulator, knowledge-engineer):
1. Automatic retry (wait 30 seconds, retry once)
2. If second failure: Ask user
   - Proceed with placeholder report
   - Abort workflow

**For Supplementary Agent** (external-researcher):
1. No automatic retry
2. Proceed without this analysis (note in synthesis)

**Retry Protocol**:
- First failure → Wait 30s → Retry automatically
- Second failure → User decision required
- Maximum 2 attempts per critical agent

**Note**: Task tool calls do not currently support explicit timeout parameters. Monitor agent progress and manually intervene if agents run longer than 10 minutes.

**Output Files** (must be created before proceeding to Phase 3):
- `${SESSION_DIR}/best-practices-review.md`
- `${SESSION_DIR}/external-research.md`
- `${SESSION_DIR}/edge-cases.md`
- `${SESSION_DIR}/knowledge-engineering-analysis.md` [NEW]

**Verification**: Before Phase 3, verify all output files exist:
```bash
ls -lh ${SESSION_DIR}/*.md
# Should show all 4 files with content
```

**Quality Gate 2: Analysis Completion**

Check agent completion status:
- [ ] best-practices-review.md exists and is >100 words
- [ ] edge-cases.md exists and is >100 words
- [ ] knowledge-engineering-analysis.md exists and is >100 words [NEW]
- [ ] external-research.md exists and is >100 words

**Gate 2 Decision Logic**:

| Completed Agents | Critical Agents Status | Action |
|------------------|----------------------|--------|
| 4/4 | All critical complete | ✅ PASS - Proceed to Phase 3 |
| 3/4 | All critical complete (only external-researcher failed) | ✅ PASS - Proceed with note |
| 3/4 | 1 critical failed (first attempt) | 🔄 RETRY - Retry failed critical agent once |
| 3/4 | 1 critical failed (after retry) | ⚠️ ASK USER - Proceed with placeholder or abort? |
| 2/4 or fewer | Multiple critical failed | ❌ FAIL - Retry all failed critical agents or abort |

**Critical Agents**: best-practices-reviewer, edge-case-simulator, knowledge-engineer
**Supplementary**: external-researcher

**Retry Protocol** (for critical agent failure):
1. First failure → Automatic retry (wait 30s, retry once)
2. Second failure → Ask user: "Proceed with placeholder report or abort?"
3. User chooses proceed → Create placeholder noting timeout/failure
4. User chooses abort → Stop workflow, rollback changes

**Graceful Degradation** (if user approves proceeding after retry):
- Create placeholder report noting timeout/failure
- Proceed to Phase 3 with 3 complete analyses
- decision-synthesizer acknowledges missing perspective in synthesis

Additional checks:
- [ ] No critical blocking issues flagged
- [ ] No conflicting recommendations (or conflicts documented for synthesis)
- [ ] Sufficient information for decision-making

**If Gate 2 passes**: Update session state and proceed to Phase 3.

```bash
# Update session state
jq -n \
  --arg phase "3" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson agents_completed '["request-refiner", "best-practices-reviewer", "external-researcher", "edge-case-simulator", "knowledge-engineer"]' \
  '{phase: $phase, timestamp: $timestamp, agents_completed: $agents_completed}' \
  > ${SESSION_DIR}/session-state.json
```

---

### Phase 2.5: STRATEGIC REVIEW [CONDITIONAL]

**Purpose**: Strategic architectural assessment for complex changes using cross-domain pattern matching to detect fundamental mismatches and major refactoring opportunities before synthesis.

**When**: Conditionally executed based on complexity detection. Skipped for simple changes (<100 lines, single file, documentation).

**Duration**: 10-30 minutes (for complex changes), ~0 seconds (for simple changes)

**Agent**: strategy-consultant (Opus 4.5)

---

#### Step 1: Complexity Detection

**Determine whether strategic review is needed**:

```bash
# Run complexity detection function
# See /Users/davidangelesalbores/repos/claude/claude-config/skills/skill-editor/references/complexity-detection-criteria.md

SPEC_FILE="${SESSION_DIR}/refined-specification.md"
COMPLEX=false
CONFIDENCE="low"
REASON=""

# Extract metrics from spec
FILES_CHANGED=$(grep -c "File:" "$SPEC_FILE" 2>/dev/null || echo 0)
LINES_CHANGED=$(grep -oP "Lines: \K[0-9]+" "$SPEC_FILE" 2>/dev/null | awk '{sum+=$1} END {print sum}')
[ -z "$LINES_CHANGED" ] && LINES_CHANGED=0

SCOPE=$(grep -A10 "^## Scope" "$SPEC_FILE")

# High-confidence complex triggers
if grep -qi "Create new skill" "$SPEC_FILE"; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="New skill creation"
elif [ "$FILES_CHANGED" -gt 3 ]; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="Multiple files affected (>3)"
elif [ "$LINES_CHANGED" -gt 200 ]; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="Large change (>200 lines)"
elif grep -qi "strategic review\|architectural assessment" "$SPEC_FILE"; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="User explicitly requested strategic review"
fi

# High-confidence simple (override complex if both match)
if [ "$CONFIDENCE" != "high" ]; then
  if echo "$SCOPE" | grep -qi "documentation\|typo\|comment\|example"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      COMPLEX=false
      CONFIDENCE="high"
      REASON="Documentation-only change"
    fi
  fi

  if echo "$SCOPE" | grep -qi "fix bug\|fix typo\|fix error"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      COMPLEX=false
      CONFIDENCE="high"
      REASON="Minor bug fix"
    fi
  fi
fi

# Medium-confidence detection
if [ "$CONFIDENCE" != "high" ]; then
  if grep -qi "agent\|workflow\|phase\|quality gate\|multi-agent" "$SPEC_FILE"; then
    if [ "$FILES_CHANGED" -le 2 ] && [ "$LINES_CHANGED" -le 100 ]; then
      COMPLEX=false
      CONFIDENCE="medium"
      REASON="Keywords detected but change is small (user confirmation recommended)"
    else
      COMPLEX=true
      CONFIDENCE="medium"
      REASON="Workflow/agent keywords with moderate change size"
    fi
  fi
fi

# Default for unclear cases
if [ "$CONFIDENCE" = "low" ]; then
  if [ "$FILES_CHANGED" -ge 2 ] || [ "$LINES_CHANGED" -ge 100 ]; then
    COMPLEX=true
    CONFIDENCE="low"
    REASON="Moderate size with unclear scope (user confirmation recommended)"
  else
    COMPLEX=false
    CONFIDENCE="medium"
    REASON="Small change with unclear scope"
  fi
fi

echo "=== Phase 2.5: Complexity Detection ==="
echo "Result: $COMPLEX (confidence: $CONFIDENCE)"
echo "Reason: $REASON"
echo ""

# High-confidence decisions
PROCEED_TO_STRATEGY_CONSULTANT=false
if [ "$CONFIDENCE" = "high" ]; then
  if [ "$COMPLEX" = "true" ]; then
    echo "→ Complex change detected: Launching strategy consultant"
    PROCEED_TO_STRATEGY_CONSULTANT=true
  else
    echo "→ Simple change detected: Skipping Phase 2.5"
    echo "   Proceeding directly to Phase 3 (decision synthesis)"
    PROCEED_TO_STRATEGY_CONSULTANT=false
  fi
else
  # Medium/low confidence: User confirmation
  echo "Confidence is $CONFIDENCE. User confirmation recommended."
  echo ""
  read -p "Do you want strategic architectural review (Phase 2.5)?
  (Y) Yes - run strategic assessment (adds 10-30 min)
  (N) No - skip Phase 2.5 (proceed to synthesis)
Choice [Y/n]: " USER_CHOICE

  if [ "$USER_CHOICE" = "n" ] || [ "$USER_CHOICE" = "N" ]; then
    PROCEED_TO_STRATEGY_CONSULTANT=false
    echo "→ Skipping Phase 2.5 (user override)"
  else
    PROCEED_TO_STRATEGY_CONSULTANT=true
    echo "→ Running Phase 2.5 (user confirmed)"
  fi
fi

# Record decision
jq -n \
  --argjson complex "$COMPLEX" \
  --arg confidence "$CONFIDENCE" \
  --arg reason "$REASON" \
  --argjson proceed "$PROCEED_TO_STRATEGY_CONSULTANT" \
  '{
    complexity_detected: $complex,
    confidence: $confidence,
    reason: $reason,
    proceed_to_phase_2_5: $proceed,
    timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }' \
  > ${SESSION_DIR}/complexity-detection.json

# Branch logic
if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "false" ]; then
  echo ""
  echo "✓ Phase 2.5 skipped (simple change)"
  echo "→ Proceeding to Phase 3: Decision Synthesis"
  # Continue to Phase 3
fi

# If PROCEED_TO_STRATEGY_CONSULTANT is true, continue to Step 2
```

---

#### Step 2: Launch Strategy Consultant

**If complexity detection triggered Phase 2.5**:

```bash
if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "true" ]; then
  echo "=== Phase 2.5: Strategic Architectural Assessment ==="
  echo ""
  echo "Launching strategy-consultant agent (Opus 4.5)..."
  echo "Expected duration: 10-30 minutes"
  echo ""
  echo "This agent will:"
  echo "  - Read all Phase 2 analysis reports"
  echo "  - Perform cross-domain pattern matching"
  echo "  - Assess architectural fit"
  echo "  - Classify recommendations (minor/major)"
  echo "  - Detect major refactoring opportunities"
  echo ""

  # Launch agent with 30-minute timeout
  TIMEOUT_SECONDS=1800
  START_TIME=$(date +%s)

  timeout ${TIMEOUT_SECONDS} claude-agent skill-editor-strategy-consultant

  EXIT_CODE=$?
  END_TIME=$(date +%s)
  ELAPSED=$((END_TIME - START_TIME))

  echo ""
  echo "Strategy consultant completed in ${ELAPSED} seconds"

  # Handle timeout
  if [ $EXIT_CODE -eq 124 ]; then
    echo "⚠ WARNING: Strategy consultant timed out after 30 minutes"

    # Check for partial report
    if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
      WORD_COUNT=$(wc -w < ${SESSION_DIR}/strategic-review.md)
      if [ $WORD_COUNT -gt 50 ]; then
        echo "Partial report found (${WORD_COUNT} words)"
        echo "" >> ${SESSION_DIR}/strategic-review.md
        echo "## INCOMPLETE REPORT" >> ${SESSION_DIR}/strategic-review.md
        echo "Note: Strategic review timed out. This is a partial analysis." >> ${SESSION_DIR}/strategic-review.md
      else
        rm ${SESSION_DIR}/strategic-review.md
      fi
    fi

    # User decision on timeout
    read -p "Strategy consultant timed out. Options:
  (A) Proceed without strategic review
  (B) Retry with extended timeout (60 minutes)
  (C) Abort workflow
Choice: " TIMEOUT_CHOICE

    case $TIMEOUT_CHOICE in
      A)
        echo "Proceeding without strategic review"
        rm -f ${SESSION_DIR}/strategic-review.md
        ;;
      B)
        echo "Retrying with 60-minute timeout..."
        timeout 3600 claude-agent skill-editor-strategy-consultant
        ;;
      C)
        echo "Aborting workflow"
        exit 1
        ;;
    esac
  elif [ $EXIT_CODE -ne 0 ]; then
    echo "✗ ERROR: Strategy consultant failed with exit code $EXIT_CODE"
    read -p "Proceed without strategic review? (yes/no): " PROCEED
    if [ "$PROCEED" != "yes" ]; then
      exit 1
    fi
  fi
fi
```

---

#### Step 3: Validate Strategic Review Quality

**After strategy consultant completes**:

```bash
if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "true" ]; then
  echo "=== Validating Strategic Review Quality ==="

  REVIEW_FILE="${SESSION_DIR}/strategic-review.md"

  if [ ! -f "$REVIEW_FILE" ]; then
    echo "⚠ No strategic review produced (agent may have failed)"
    read -p "Proceed without strategic review? (yes/no): " PROCEED
    if [ "$PROCEED" != "yes" ]; then
      exit 1
    fi
    echo "→ Skipping to Phase 3"
  else
    # Quality checks
    WORD_COUNT=$(wc -w < "$REVIEW_FILE")
    PATTERN_COUNT=$(grep -c "Pattern:" "$REVIEW_FILE" || echo 0)
    RECOMMENDATION_COUNT=$(grep -c "Recommendation:" "$REVIEW_FILE" || grep -c "^- " "$REVIEW_FILE" || echo 0)

    echo "Quality metrics:"
    echo "  - Word count: $WORD_COUNT"
    echo "  - Patterns identified: $PATTERN_COUNT"
    echo "  - Recommendations: $RECOMMENDATION_COUNT"

    # Minimum thresholds
    MIN_WORDS=200
    MIN_PATTERNS=1
    MIN_RECOMMENDATIONS=1

    QUALITY_SUFFICIENT=true

    if [ "$WORD_COUNT" -lt "$MIN_WORDS" ]; then
      echo "⚠ WARNING: Strategic review is brief ($WORD_COUNT words < $MIN_WORDS minimum)"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$PATTERN_COUNT" -lt "$MIN_PATTERNS" ]; then
      echo "⚠ WARNING: No patterns identified"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$RECOMMENDATION_COUNT" -lt "$MIN_RECOMMENDATIONS" ]; then
      echo "⚠ WARNING: No recommendations provided"
      QUALITY_SUFFICIENT=false
    fi

    # Check for generic content
    if grep -qi "looks reasonable\|looks good\|no concerns\|follow best practices\|seems fine" "$REVIEW_FILE" | head -2 | wc -l | grep -q "2"; then
      echo "⚠ WARNING: Strategic review contains generic/superficial content"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$QUALITY_SUFFICIENT" = "false" ]; then
      echo ""
      echo "Strategic review quality is below threshold."
      echo "Preview (first 500 words):"
      head -c 3000 "$REVIEW_FILE"
      echo ""
      echo "..."
      echo ""
      read -p "Options:
  (A) Accept strategic review as-is
  (B) Retry strategy consultant (extended time budget)
  (C) Skip strategic review and proceed without it
Choice: " QUALITY_CHOICE

      case $QUALITY_CHOICE in
        A)
          echo "Accepting strategic review"
          ;;
        B)
          echo "Retrying strategy consultant..."
          mv "$REVIEW_FILE" "${REVIEW_FILE}.first-attempt"
          timeout 3600 claude-agent skill-editor-strategy-consultant --mode=detailed
          ;;
        C)
          echo "Skipping strategic review"
          rm "$REVIEW_FILE"
          ;;
      esac
    fi

    echo "✓ Strategic review validated"
  fi
fi
```

---

#### Step 4: Check for Major Refactoring

**Determine if go/no-go decision needed**:

```bash
echo "=== Checking for Major Refactoring Opportunity ==="

REVIEW_FILE="${SESSION_DIR}/strategic-review.md"

if [ ! -f "$REVIEW_FILE" ]; then
  echo "No strategic review file (Phase 2.5 was skipped or failed)"
  echo "→ Proceeding to Phase 3"
else
  # Check classification
  if grep -qi "Classification:.*MAJOR REFACTORING DETECTED" "$REVIEW_FILE"; then
    echo "🔴 MAJOR REFACTORING OPPORTUNITY DETECTED"
    echo ""
    echo "The strategy consultant has identified a fundamental architectural issue."
    echo ""

    # Extract details from report
    ISSUE=$(grep -A5 "Major Refactoring Opportunity" "$REVIEW_FILE" | head -6)
    echo "$ISSUE"
    echo ""

    # Note: Major refactoring decision is handled by strategy-consultant agent
    # via AskUserQuestion. User decision is recorded in strategic-review.md.

    # Check user decision from report
    if grep -qi "User decision:.*Explore refactoring in parallel" "$REVIEW_FILE"; then
      echo "User selected: Explore refactoring in parallel (Option B)"
      echo ""
      echo "⚠ Parallel exploration will be triggered after Phase 3 completes"
      echo "  - Track 1 (current plan) continues through Phase 3"
      echo "  - Track 2 (alternative exploration) launches in parallel"
      echo "  - You'll see both approaches before Phase 4 execution"
      echo ""

      # Set flag for parallel exploration
      jq -n '{
        parallel_exploration: true,
        trigger_after_phase: 3
      }' > ${SESSION_DIR}/parallel-exploration-flag.json

    elif grep -qi "User decision:.*Proceed with current plan" "$REVIEW_FILE"; then
      echo "User selected: Proceed with current plan (Option A)"
      echo "→ Continuing with original specification approach"

    elif grep -qi "User decision:.*Abort" "$REVIEW_FILE"; then
      echo "User selected: Abort workflow (Option C)"
      echo "Stopping workflow. Session data preserved in ${SESSION_DIR}"
      exit 1
    fi
  else
    echo "✓ No major refactoring detected (minor recommendations only)"
  fi

  echo ""
  echo "→ Proceeding to Quality Gate 2.5"
fi
```

---

#### Quality Gate 2.5: Strategic Review Complete

**Check criteria before proceeding to Phase 3**:

```bash
echo "=== Quality Gate 2.5: Strategic Review Complete ==="
echo ""

GATE_PASS=true

# Check 1: Complexity detection completed
if [ ! -f "${SESSION_DIR}/complexity-detection.json" ]; then
  echo "✗ Complexity detection not completed"
  GATE_PASS=false
else
  echo "✓ Complexity detection completed"
fi

# Check 2: If complex, strategic review exists
PROCEED=$(jq -r '.proceed_to_phase_2_5' ${SESSION_DIR}/complexity-detection.json 2>/dev/null || echo "false")

if [ "$PROCEED" = "true" ]; then
  if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
    WORD_COUNT=$(wc -w < ${SESSION_DIR}/strategic-review.md)
    if [ $WORD_COUNT -gt 100 ]; then
      echo "✓ Strategic review exists and is substantive ($WORD_COUNT words)"
    else
      echo "⚠ Strategic review exists but is too brief ($WORD_COUNT words)"
      read -p "Accept brief review and proceed? (yes/no): " ACCEPT
      if [ "$ACCEPT" != "yes" ]; then
        GATE_PASS=false
      fi
    fi
  else
    echo "⚠ Strategic review missing (expected for complex change)"
    read -p "Proceed without strategic review? (yes/no): " PROCEED_ANYWAY
    if [ "$PROCEED_ANYWAY" != "yes" ]; then
      GATE_PASS=false
    fi
  fi
else
  echo "✓ Phase 2.5 skipped (simple change)"
fi

# Check 3: If major refactoring, user decision recorded
if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
  if grep -qi "MAJOR REFACTORING DETECTED" ${SESSION_DIR}/strategic-review.md; then
    if grep -qi "User decision:" ${SESSION_DIR}/strategic-review.md; then
      DECISION=$(grep -i "User decision:" ${SESSION_DIR}/strategic-review.md | head -1 | cut -d: -f2 | xargs)
      echo "✓ Major refactoring decision recorded: $DECISION"
    else
      echo "✗ Major refactoring detected but no user decision recorded"
      GATE_PASS=false
    fi
  fi
fi

# Check 4: Git repository still clean (re-check)
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠ WARNING: Git working directory is no longer clean"
  git status --short
  echo ""
  read -p "Files were modified during Phase 2.5. Options:
  (A) Stash changes and continue
  (B) Abort workflow
  (C) Ignore and continue (DANGEROUS)
Choice: " GIT_CHOICE

  case $GIT_CHOICE in
    A)
      git stash push -m "skill-editor-auto-stash-$(date +%Y%m%d-%H%M%S)"
      echo "✓ Changes stashed"
      ;;
    B)
      echo "Aborting workflow"
      exit 1
      ;;
    C)
      echo "⚠ Continuing with dirty git state"
      ;;
  esac
else
  echo "✓ Git working directory clean"
fi

# Gate decision
echo ""
if [ "$GATE_PASS" = "true" ]; then
  echo "✅ Quality Gate 2.5: PASS"
  echo "→ Proceeding to Phase 3: Decision Synthesis"
else
  echo "❌ Quality Gate 2.5: FAIL"
  echo "Resolve issues above before proceeding"
  exit 1
fi

# Update session state
jq -n \
  --arg phase "3" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson agents_completed '["request-refiner", "best-practices-reviewer", "external-researcher", "edge-case-simulator", "knowledge-engineer", "strategy-consultant"]' \
  '{
    phase: $phase,
    timestamp: $timestamp,
    agents_completed: $agents_completed
  }' \
  > ${SESSION_DIR}/session-state.json

echo ""
echo "✓ Session state updated: Phase 2.5 complete"
```

**Note**: Phase 2.5 is optional and conditional. If skipped, strategic-review.md will not exist, and Phase 3 agents (decision-synthesizer, adversarial-reviewer) will handle this gracefully.

---

### Phase 3 Variants by Mode

#### Phase 3: SIMPLE MODE (Lightweight Decision)

**Duration**: 10-20 minutes
**Trigger**: SELECTED_MODE = "SIMPLE"

```bash
echo "=== Phase 3: SIMPLE MODE - Lightweight Decision ==="
echo ""

SPEC_FILE="${SESSION_DIR}/refined-specification.md"
PLAN_FILE="${SESSION_DIR}/implementation-plan.md"

# Create minimal implementation plan from specification
cat << 'PLAN_HEADER' > "$PLAN_FILE"
# Implementation Plan (Simple Mode)

**Mode**: SIMPLE
**Quality Level**: Basic validation only (no expert analysis)

## Note

This plan was created in Simple Mode without Phase 2 expert analysis.
For changes requiring deeper review, re-run with Standard Mode.

PLAN_HEADER

echo "## Objective" >> "$PLAN_FILE"
grep -A5 "^## Objective" "$SPEC_FILE" >> "$PLAN_FILE"

echo "" >> "$PLAN_FILE"
echo "## Files to Modify" >> "$PLAN_FILE"
grep -A20 "^## Scope" "$SPEC_FILE" | grep -E "^\s*-|File:|Edit:|Modify:" >> "$PLAN_FILE"

echo "" >> "$PLAN_FILE"
echo "## Validation Steps" >> "$PLAN_FILE"
cat << 'VALIDATION' >> "$PLAN_FILE"

1. Validate YAML frontmatter (Gate 4)
2. Run sync-config.py --dry-run
3. Test skill invocation (Gate 5)

## Rollback Plan

If anything fails:
1. `git reset --hard HEAD`
2. `./sync-config.py push`
VALIDATION

echo "[SIMPLE MODE] Lightweight implementation plan created."

# [FIX: Adversarial Issue #3] File-based adversarial trigger instead of keyword matching
# Check if target files include core workflow/agent files
NEEDS_ADVERSARIAL=false

# Extract target files from plan
TARGET_FILES=$(grep -E "File:|Edit:|Modify:" "$PLAN_FILE" | grep -o 'claude-config/[^ ]*' || echo "")

# Check for core workflow files
if echo "$TARGET_FILES" | grep -qE "SKILL\.md|agents/.*\.md"; then
  NEEDS_ADVERSARIAL=true
  echo ""
  echo "[SIMPLE MODE] Core workflow/agent files detected - running lightweight validation..."
fi

if [ "$NEEDS_ADVERSARIAL" = "true" ]; then
  # Check file paths exist
  while IFS= read -r FILE_PATH; do
    if [ -n "$FILE_PATH" ]; then
      FULL_PATH="/Users/davidangelesalbores/repos/claude/$FILE_PATH"
      if [ ! -f "$FULL_PATH" ]; then
        echo "WARNING: File does not exist: $FILE_PATH"
      fi
    fi
  done < <(echo "$TARGET_FILES")

  # Warn if touching SKILL.md workflow sections
  if echo "$TARGET_FILES" | grep -q "SKILL\.md"; then
    echo ""
    echo "WARNING: Plan modifies SKILL.md (core workflow file)."
    read -p "Continue with Simple Mode or upgrade? [simple/standard]: " UPGRADE
    if [ "$UPGRADE" = "standard" ]; then
      SELECTED_MODE="STANDARD"
      echo "Upgrading to Standard Mode..."
      # Jump to Phase 2
    fi
  fi
else
  echo "[SIMPLE MODE] No core workflow/agent files affected - skipping adversarial check"
fi

echo ""
echo "[SIMPLE MODE] Phase 3 complete. Proceeding to Phase 4."
```

---

#### Phase 3: EXPERIMENTAL MODE (Minimal Decision)

**Duration**: 5-10 minutes
**Trigger**: SELECTED_MODE = "EXPERIMENTAL"

```bash
echo "=== Phase 3: EXPERIMENTAL MODE - Minimal Decision ==="
echo ""

SPEC_FILE="${SESSION_DIR}/refined-specification.md"
PLAN_FILE="${SESSION_DIR}/implementation-plan.md"

# Create plan with experimental flags
cat << 'PLAN_HEADER' > "$PLAN_FILE"
# Implementation Plan (Experimental Mode)

**Mode**: EXPERIMENTAL
**Quality Level**: Minimal - prototype quality
**experimental**: true

## WARNING

This is an EXPERIMENTAL implementation plan.
- No Phase 2 expert analysis was performed
- No strategic architectural review
- Reduced quality assurance

**RECOMMENDED**: Run Standard Mode before production use.

PLAN_HEADER

echo "## Objective" >> "$PLAN_FILE"
grep -A5 "^## Objective" "$SPEC_FILE" >> "$PLAN_FILE"

echo "" >> "$PLAN_FILE"
echo "## Files to Modify" >> "$PLAN_FILE"
grep -A20 "^## Scope" "$SPEC_FILE" | grep -E "^\s*-|File:|Edit:|Modify:" >> "$PLAN_FILE"

echo "" >> "$PLAN_FILE"
echo "## Validation Steps" >> "$PLAN_FILE"
cat << 'VALIDATION' >> "$PLAN_FILE"

1. Validate YAML frontmatter (Gate 4)
2. Run sync-config.py --dry-run
3. Basic smoke test

## Rollback Plan (REQUIRED for experimental)

1. `git reset --hard HEAD`
2. `./sync-config.py push`

Consider creating a branch for experimental work:
```bash
git checkout -b experimental/[feature-name]
```

---

**EXPERIMENTAL OUTPUT**: This skill is NOT production-ready.
Run `/skill-editor` with Standard Mode for full review before production use.
VALIDATION

echo "[EXPERIMENTAL] Minimal implementation plan created."

# Optional adversarial review
read -p "[EXPERIMENTAL] Run optional adversarial review? (adds ~15 min) [y/N]: " DO_REVIEW
if [ "$DO_REVIEW" = "y" ]; then
  echo "Launching adversarial-reviewer..."
  # Launch full adversarial reviewer agent
fi

echo ""
echo "[EXPERIMENTAL] Phase 3 complete. Proceeding to Phase 4."
```

---

#### Phase 3 Mode Checkpoint

Before launching synthesis, offer mode change option:

```bash
CURRENT_MODE=$(jq -r '.workflow_mode' ${SESSION_DIR}/session-state.json 2>/dev/null || echo "STANDARD")

echo "=== Phase 3 Mode Checkpoint ==="
echo ""
echo "Current workflow mode: $CURRENT_MODE"

if [ "$CURRENT_MODE" = "SIMPLE" ] || [ "$CURRENT_MODE" = "EXPERIMENTAL" ]; then
  echo "Phase 2 status: SKIPPED (no expert analysis performed)"
  echo ""
  echo "Options:"
  echo "  (1) Continue with $CURRENT_MODE Mode"
  echo "  (2) Switch to Standard Mode (will run Phase 2 now, adds ~1.5 hours)"
  echo ""
  read -p "Choice [1]: " CHECKPOINT_CHOICE

  if [ "$CHECKPOINT_CHOICE" = "2" ]; then
    echo "Switching to Standard Mode..."
    jq '.workflow_mode = "STANDARD"' ${SESSION_DIR}/session-state.json > ${SESSION_DIR}/session-state.tmp.json
    mv ${SESSION_DIR}/session-state.tmp.json ${SESSION_DIR}/session-state.json
    CURRENT_MODE="STANDARD"
    echo "[STANDARD MODE] Running Phase 2 (4 parallel agents)..."
    # Jump to Phase 2 execution
  fi
fi

echo ""
echo "[$CURRENT_MODE MODE] Proceeding with Phase 3..."
```

---

### Phase 3: Decision & Review (Synthesis + Adversarial)

**Objective**: Synthesize analyses, make decisions, create plan, get expert approval.

#### Part A: Decision Synthesis

**Agent**: `skill-editor-decision-synthesizer`

**Model**: Opus 4.5 (critical decision-making)

**Process**:

1. Read all 4 analysis reports + refined specification
2. Identify consensus and conflicts
3. Resolve conflicts or present options to user:
   - **Major decisions**: MUST ask user (new agents, structure changes)
   - **Medium decisions**: SHOULD ask user (workflow changes)
   - **Minor decisions**: Agent decides (examples, docs)
4. Create detailed implementation plan with:
   - Exact file paths
   - Specific changes (line numbers if possible)
   - Edge case handling
   - Git workflow
   - Validation steps
   - Rollback plan

**Orchestrator-Specific Synthesis** (when orchestrator_detected is true in session state):

5. Read orchestrator checklist results from both best-practices-review.md and knowledge-engineering-analysis.md
6. If REQUIRED patterns are ABSENT: Implementation plan MUST include adding those patterns
7. If RECOMMENDED patterns are ABSENT: Implementation plan SHOULD note them as suggested additions
8. Reference pattern templates from `orchestrator-best-practices.md` for copy-paste inclusion in the plan
9. Check Pattern Interactions section in orchestrator-best-practices.md to avoid contradictions between added patterns
10. For existing orchestrators: PARTIAL with a working variant is acceptable -- do NOT recommend replacing working implementations with standard templates

**Output File**: `${SESSION_DIR}/implementation-plan.md`

#### Part B: Adversarial Review

**Agent**: `skill-editor-adversarial-reviewer`

**Model**: Opus 4.5 (expert review)

**Process**:

1. Read implementation plan with expert skepticism
2. Challenge assumptions and approach
3. Identify failure modes not caught by analysis
4. Verify exact file paths (run bash checks)
5. Verify git workflow safety
6. Check alignment with original specification
7. Provide go/no-go decision

**Output File**: `${SESSION_DIR}/adversarial-review.md` containing:
- Architecture assessment
- Failure mode analysis
- Integration risk assessment
- Exact file path verification
- Git workflow verification
- Final decision: ✅ GO / ⚠️ CONDITIONAL / ❌ NO-GO

**Quality Gate 3: Plan Approval**

Check:
- [ ] Implementation plan has exact file paths
- [ ] Git workflow is safe and correct
- [ ] Integration points identified
- [ ] No architectural concerns
- [ ] Adversarial reviewer approved (GO or CONDITIONAL with fixes applied)
- [ ] User approves plan

**If Gate 3 fails**:
- If CONDITIONAL: Fix issues, re-review
- If NO-GO: Return to decision-synthesizer, revise plan
- If user doesn't approve: Refine plan or return to Phase 1

**If Gate 3 passes**: Update session state and proceed to Phase 4.

```bash
# Update session state
jq -n \
  --arg phase "4" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson agents_completed '["request-refiner", "best-practices-reviewer", "external-researcher", "edge-case-simulator", "decision-synthesizer", "adversarial-reviewer"]' \
  '{phase: $phase, timestamp: $timestamp, agents_completed: $agents_completed}' \
  > ${SESSION_DIR}/session-state.json
```

---

### Phase 4: Execution (Implement + Validate + Commit)

**Objective**: Execute approved plan with validation at each step.

**Agent**: `skill-editor-executor`

**Model**: Opus 4.5

**Process**:

#### Step 1: Pre-Implementation Safety

```bash
git status  # Must be clean
./sync-config.py status  # Must be synced
pwd  # Must be repo root
```

Stop if any check fails.

#### Step 2: Implement Changes

For each file in implementation plan:
- **Edit**: Read first, then Edit with exact string replacement
- **Create**: Write new file
- **Delete**: Remove file

#### Experimental Mode Output Tagging

If workflow_mode = "EXPERIMENTAL", add tags to output files:

```bash
CURRENT_MODE=$(jq -r '.workflow_mode' ${SESSION_DIR}/session-state.json 2>/dev/null || echo "STANDARD")

if [ "$CURRENT_MODE" = "EXPERIMENTAL" ]; then
  echo "[EXPERIMENTAL] Adding experimental tags to output files..."

  # For each skill file being created/modified
  # [FIX: Adversarial Issue #4] Use POSIX-compatible grep instead of grep -oP
  for SKILL_FILE in $(grep -o 'skills/[^/]*/SKILL\.md' ${SESSION_DIR}/implementation-plan.md | sort -u); do
    FULL_PATH="/Users/davidangelesalbores/repos/claude/claude-config/$SKILL_FILE"

    if [ -f "$FULL_PATH" ]; then
      # Check if experimental tag already exists in frontmatter
      if ! head -20 "$FULL_PATH" | grep -q "experimental: true"; then
        # [FIX: Adversarial Issue #1] BSD-compatible: Use temp file approach instead of sed -i with append
        # Insert experimental: true after first line (which is ---)
        { head -1 "$FULL_PATH"; echo "experimental: true"; tail -n +2 "$FULL_PATH"; } > "$FULL_PATH.tmp" && mv "$FULL_PATH.tmp" "$FULL_PATH"
        echo "  Added experimental tag to: $SKILL_FILE"
      fi

      # Add warning comment after frontmatter if not present
      if ! grep -q "EXPERIMENTAL SKILL" "$FULL_PATH"; then
        # First check if file has valid frontmatter (starts with ---)
        if head -1 "$FULL_PATH" | grep -q "^---"; then
          # Find end of frontmatter (second ---) and add comment using awk
          awk '/^---$/{c++} c==2{print; print ""; print "<!-- EXPERIMENTAL SKILL: Created via skill-editor experimental mode -->"; print "<!-- This skill has NOT been fully analyzed. Run Standard Mode before production use. -->"; c++; next}1' "$FULL_PATH" > "$FULL_PATH.tmp" && mv "$FULL_PATH.tmp" "$FULL_PATH"
          echo "  Added experimental warning to: $SKILL_FILE"
        else
          echo "  WARNING: No frontmatter found in $SKILL_FILE, skipping warning insertion"
        fi
      fi
    fi
  done
fi
```

#### Step 3: Quality Gate 4 - Pre-Sync Validation

Validate before syncing to `~/.claude/`:

```bash
# Validate YAML (for skills)
for skill in claude-config/skills/*/SKILL.md; do
  python3 -c "import yaml; yaml.safe_load(open('$skill').read().split('---')[1])"
done

# Validate JSON (for agents)
for agent in claude-config/agents/*.json; do
  python3 -m json.tool "$agent" > /dev/null
done

# Dry-run sync
./sync-config.py push --dry-run
```

**Quality Gate 4 Checklist**:
- [ ] YAML frontmatter validates
- [ ] JSON validates (if agents modified)
- [ ] Skill structure follows specification
- [ ] File naming conventions followed
- [ ] No conflicting settings
- [ ] Dry-run sync succeeds

**If Gate 4 fails**: Fix issues, re-validate, do NOT proceed until pass.

#### Step 4: Sync to ~/.claude/

```bash
# Sync (prompts user for confirmation)
./sync-config.py push

# Verify
./sync-config.py status  # Should show no divergence
```

#### Step 5: Test Skill Invocation

```bash
# Create test script
cat > /tmp/test-skill.sh << 'EOF'
#!/bin/bash
SKILL_NAME="$1"
# Check skill exists
[ -f "$HOME/.claude/skills/$SKILL_NAME/SKILL.md" ] || exit 1
# Check YAML parses
python3 -c "import yaml; yaml.safe_load(open('$HOME/.claude/skills/$SKILL_NAME/SKILL.md').read().split('---')[1])"
EOF
chmod +x /tmp/test-skill.sh

# Test skill
/tmp/test-skill.sh {skill-name}

# Smoke test existing skills (no regressions)
/tmp/test-skill.sh skill-editor
/tmp/test-skill.sh completion-verifier
```

#### Step 6: Quality Gate 5 - Post-Execution Verification

**Quality Gate 5 Checklist**:
- [ ] Original requirement met (from refined spec)
- [ ] Edge cases handled (from edge-case report)
- [ ] sync-config.py push successful
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal entry ready

**If Gate 5 fails**: Rollback via `git reset --hard HEAD`, re-sync, fix, retry.

#### Step 7: Update Planning Journal

```bash
./sync-config.py plan --title "[Brief description from refined spec]"

# Document in entry:
# - Objective
# - Changes made (files, lines)
# - Testing results
# - Outcome: Success
```

#### Optional: Git Strategy Advisory

Before committing changes, you MAY invoke `git-strategy-advisor` via Task tool in
post-work mode to get scope-adaptive git recommendations:

**Invocation** (via Task tool):
```
Use git-strategy-advisor to determine git strategy for completed work.

mode: post-work
```

The advisor analyzes actual changes and may recommend creating a feature branch
(for larger skill changes) vs direct commit (for typo fixes), branch naming
convention, push timing, and PR creation.

**Conflict resolution**: If the advisor's recommendation differs from Step 8's
existing logic (which commits directly), Step 8 logic takes precedence
unconditionally. Present the advisor's recommendation as an informational note
in the completion summary (e.g., "Note: git-strategy-advisor suggests creating a
feature branch for this scope of changes").

**Response handling**: Read the advisor's `summary` field for the human-readable
recommendation. Include in the planning journal entry if noteworthy.

**Confidence handling**: If the advisor returns confidence "none", silently skip.
If confidence is "low", present with a caveat.

This is **advisory only**. If `git-strategy-advisor` is not available or returns
an error, proceed with existing Step 8 logic unchanged.

#### Step 8: Commit Changes

```bash
# Determine commit prefix based on mode
CURRENT_MODE=$(jq -r '.workflow_mode' ${SESSION_DIR}/session-state.json 2>/dev/null || echo "STANDARD")

if [ "$CURRENT_MODE" = "EXPERIMENTAL" ]; then
  COMMIT_PREFIX="experimental"
  COMMIT_SUFFIX="

[EXPERIMENTAL - requires full review before production use]"
else
  COMMIT_PREFIX="feat"
  COMMIT_SUFFIX=""
fi

# Stage specific files (NEVER -A or .)
git add claude-config/skills/{skill-name}/SKILL.md
git add claude-config/skills/{skill-name}/examples/example.md  # if created
git add claude-config/agents/{agent-name}.json  # if modified
git add planning/$(hostname)/*.md

# Commit with HEREDOC (multi-line message)
git commit -m "$(cat <<EOF
${COMMIT_PREFIX}(skill-name): [Brief description]

[Detailed description from implementation plan]

Changes:
- Modified SKILL.md: [what changed]
- Added example: [why]

Testing:
- Validated YAML
- Tested invocation
- No regressions

See planning/$(hostname)/[date]-[title].md${COMMIT_SUFFIX}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Verify commit
git log -1 --stat

# Mark session as completed
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Skill-editor workflow completed successfully"

  # Mark session as completed
  jq '.status = "completed" | .phase = "4" | .completed_at = (now | strftime("%Y-%m-%dT%H:%M:%SZ"))' \
    "${SESSION_DIR}/session-state.json" > "${SESSION_DIR}/session-state.tmp.json" && \
    mv "${SESSION_DIR}/session-state.tmp.json" "${SESSION_DIR}/session-state.json"

  echo "Session ${SESSION_ID} marked as completed"
  echo "Session artifacts preserved in: ${SESSION_DIR}"
else
  # Mark as failed if git commit fails
  jq '.status = "failed" | .error = "Git commit failed"' \
    "${SESSION_DIR}/session-state.json" > "${SESSION_DIR}/session-state.tmp.json" && \
    mv "${SESSION_DIR}/session-state.tmp.json" "${SESSION_DIR}/session-state.json"

  echo "❌ Session ${SESSION_ID} marked as failed"
fi
```

**Git Safety Checklist**:
- [ ] Specific files staged (not -A or .)
- [ ] Conventional commit format (feat/fix/docs)
- [ ] Descriptive message
- [ ] Co-authored-by line
- [ ] No destructive operations
- [ ] No hook bypasses

#### Step 9: Report Completion

Generate completion report with:
- Summary of changes
- Validation results (Gates 4 & 5)
- Testing results
- Commit SHA
- Planning journal entry path
- Success criteria verification
- Session completion status

---

## Escalation Framework

Decision thresholds (from CONFIG_MANAGEMENT.md):

### Major Decisions → User Approval Required

- Add new agent to workflow
- Change skill structure specification
- Modify core workflow phases

**Action**: Use AskUserQuestion before proceeding

### Medium Decisions → User Approval Required

- Modify existing skill's core workflow
- Add new supporting skill
- Change skill naming convention

**Action**: Use AskUserQuestion with options

### Minor Decisions → Agent Decides

- Add example to existing skill
- Fix documentation typo
- Update reference material

**Action**: Proceed, notify user

## Error Handling

### Retry Protocol (Phase 2 Agent Failures)
- First failure: Wait 30s, retry automatically
- Second failure: User decision required (proceed with placeholder or abort)
- Maximum 2 attempts per critical agent
- Retried operations should be idempotent (re-running should not create duplicate analysis files)

### Graceful Degradation (Supplementary Agent Failures)
- external-researcher timeout: Proceed without research analysis
- knowledge-engineer timeout (after retry): Proceed with 3 analyses
- Decision-synthesizer notes missing perspectives in synthesis

### Circuit Breaker (Cascading Failures)
- If 2+ critical agents fail in Phase 2: Stop retrying, escalate to user
- User choices: retry all, proceed with available, or abort
- Reference: programming-pm circuit breaker pattern (open after consecutive failures)

### Rollback Protocol (Phase 4 Failures)
1. Stop immediately
2. `git reset --hard HEAD` (revert uncommitted changes)
3. `./sync-config.py push` (re-sync from repo)
4. Document failure in planning journal
5. Report to user with options: retry, skip, or abort

### Interrupt Handling (User Cancels)
1. Check git status
2. Rollback uncommitted changes: `git reset --hard HEAD`
3. Re-sync: `./sync-config.py push`
4. Session state preserved in `${SESSION_DIR}/` for potential resume
5. Document in planning journal: "Cancelled by user"

## Integration with Existing Tools

### CONFIG_MANAGEMENT.md

This workflow extends the 7-step CONFIG_MANAGEMENT.md process:

- **Step 1 (Safety Check)**: Pre-workflow checks
- **Step 2 (Planning Entry)**: Phase 4, Step 7
- **Step 3 (Implement)**: Phase 4, Step 2
- **Step 4 (Quality Analysis)**: Phases 2-3, Quality Gates
- **Step 5 (Preview/Sync)**: Phase 4, Steps 3-4
- **Step 6 (Test)**: Phase 4, Step 5
- **Step 7 (Commit)**: Phase 4, Step 8

### sync-config.py

Executor agent uses sync-config.py:
- `./sync-config.py status` (pre-flight check)
- `./sync-config.py push --dry-run` (validation)
- `./sync-config.py push` (apply changes)
- `./sync-config.py plan` (create planning entry)

### Planning Journal

Planning entry created in Phase 4, Step 7:
- Title: Brief description from refined spec
- Objective: From refined specification
- Changes: Files modified
- Testing: Validation and test results
- Outcome: Success/Partial/Failed

## Quality Gates Summary

| Gate | Phase | Owner | Criteria | Failure Action |
|------|-------|-------|----------|----------------|
| 1 | Phase 1 | request-refiner | Spec approved | Return to refinement |
| 2 | Phase 2 | decision-synthesizer | All analyses complete | Re-run agents |
| 3 | Phase 3 | adversarial-reviewer | Plan approved | Revise plan |
| 4 | Phase 4 | executor | Syntax validated | Fix issues |
| 5 | Phase 4 | executor | Implementation verified | Rollback |

## Examples

### Example 1: Add Parallel Execution to Researcher

**User Request**:
```
/skill-editor "Add parallel web search to researcher skill"
```

**Phase 1 Output**:
```markdown
Objective: Modify researcher skill to execute 3 WebSearch calls in parallel

Scope:
- IN: researcher/SKILL.md Phase 2 workflow
- OUT: No changes to agents or other phases

Success Criteria:
- 3 WebSearch calls execute simultaneously
- Results synthesized correctly
- No regressions
```

**Phase 2 Findings**:
- Best practices: Use Task tool for parallel calls ✅
- Research: Community uses this pattern ✅
- Edge cases: Handle timeout, network failure

**Phase 3 Plan**:
```markdown
Edit: claude-config/skills/researcher/SKILL.md
Lines 45-60: Replace sequential WebSearch with parallel

Implementation:
[3 Task tool calls in single message]
```

**Phase 4 Result**:
```bash
✅ YAML validates
✅ Sync succeeds
✅ Skill invokes correctly
✅ Commit: feat(researcher): Add parallel web search
```

### Example 2: Create New Skill

**User Request**:
```
/skill-editor "Create a new skill for API documentation"
```

**Process**:
- Phase 1: Refine requirements (which APIs? format? tools?)
- Phase 2: Analyze (best practices for doc skills, community patterns, edge cases)
- Phase 3: Plan (file structure, workflow steps, examples)
- Phase 4: Create files, validate, sync, test, commit

## Timeout Configuration

| Phase | Component | Timeout | Exceeded Action |
|-------|-----------|---------|-----------------|
| 1 | request-refiner | 30 min | Escalate to user |
| 2 | critical agents (Wave 1-2) | 10 min each | Auto-retry once, then user decision |
| 2 | supplementary agent (Wave 3) | 10 min | Proceed without |
| 2.5 | strategy-consultant | 30 min | User decision (proceed/retry/abort) |
| 3 | decision-synthesizer | 30 min | Escalate to user |
| 3 | adversarial-reviewer | 30 min | Escalate to user |
| 4 | executor | 60 min | Escalate to user |
| Global | entire workflow | 4 hours | Safety ceiling, force escalate |

## Notes

- **Parallel execution in Phase 2**: All 4 agents run simultaneously with wave-based launches (30-60s stagger reduces resource contention)
- **All agents use Opus 4.5**: Maximum quality for all workflow phases (requirements analysis, research, edge cases, structural completeness, decision-making, review, execution)
- **Quality gates enforce standards**: No bypassing validation
- **Rollback on failure**: Safe to abort at any point
- **Planning journal provides traceability**: Full documentation of changes
- **Integration tested**: Works with sync-config.py and existing workflows

## References

See `skill-editor/references/` for:
- `anthropic-guidelines-summary.md`: Anthropic best practices
- `skill-structure-specification.md`: Skill format and validation
- `quality-gates.md`: Detailed quality gate checklists
- `config-management-integration.md`: Integration with CONFIG_MANAGEMENT.md

## Success Criteria

Skill-editor workflow succeeds when:

- [ ] User's original request is fulfilled
- [ ] All quality gates pass
- [ ] Changes are synced to `~/.claude/`
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal documents changes
- [ ] Changes committed to git
- [ ] User confirms satisfaction
