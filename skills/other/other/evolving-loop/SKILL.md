---
name: evolving-loop
description: Self-Evolving Development Loop - Dynamic skill generation with learning and evolution
user-invocable: true
---

# Self-Evolving Development Loop

Execute an autonomous development cycle that dynamically generates, validates, and evolves its own execution strategy. Integrates with Meta-Engineering memory system for pattern learning and tool evolution.

> **Architecture Details**: See [docs/EVOLVING-LOOP-ARCHITECTURE.md](../../../docs/EVOLVING-LOOP-ARCHITECTURE.md)

---

## Usage

```bash
# Start new task
/evolving-loop "Your task description

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
"

# Flags
/evolving-loop --resume    # Resume interrupted session
/evolving-loop --status    # Check status
/evolving-loop --force     # Clear and restart
/evolving-loop --evolve    # Trigger manual evolution
/evolving-loop --memory    # Show memory system status
```

---

## How It Works

```
┌──────────────────────────────────────────────────────┐
│  8-Phase Self-Evolving Loop                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Phase -2: CONTEXT_CHECK  → Check token pressure     │
│  Phase -1A: PATTERN_LOOKUP → Match task patterns     │
│                                                      │
│  ┌─────────────── Main Loop ───────────────┐        │
│  │ Phase 1: ANALYZE   → Extract AC         │        │
│  │ Phase 2: GENERATE  → Create skills      │        │
│  │ Phase 3: EXECUTE   → TDD implementation │        │
│  │ Phase 4: VALIDATE  → Score 0-100        │        │
│  │ Phase 5: DECIDE    → SHIP/FIX/EVOLVE    │        │
│  │ Phase 6: LEARN     → Extract patterns   │        │
│  │ Phase 7: EVOLVE    → Improve skills     │        │
│  └──────────────────────────────────────────┘        │
│                                                      │
│  Phase -1C: EVOLUTION → Update memory (on SHIP)     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Execution

When user runs `/evolving-loop "$ARGUMENTS"`:

### 1. Handle Flags

```bash
STATE_DIR=".self-evolving-loop"
MEMORY_DIR=".claude/memory/meta-engineering"
CHECKPOINT="$STATE_DIR/state/checkpoint.json"

# --status: Show current state
if [[ "$ARGUMENTS" == *"--status"* ]]; then
    /evolving-status
    exit 0
fi

# --memory: Show memory system status
if [[ "$ARGUMENTS" == *"--memory"* ]]; then
    echo "Memory System Status:"
    if [ -d "$MEMORY_DIR" ]; then
        echo "Tool Usage: $(jq '.tools | length' "$MEMORY_DIR/tool-usage.json" 2>/dev/null || echo "0") tools"
        echo "Patterns: $(jq '.task_patterns | keys | length' "$MEMORY_DIR/patterns.json" 2>/dev/null || echo "0") patterns"
        echo "Evolution: v$(jq -r '.version' "$MEMORY_DIR/evolution.json" 2>/dev/null || echo "0")"
    else
        echo "(Not initialized - will create on first run)"
    fi
    exit 0
fi

# --resume: Continue from checkpoint
if [[ "$ARGUMENTS" == *"--resume"* ]]; then
    if [ ! -f "$CHECKPOINT" ] || [ "$(jq -r '.status' "$CHECKPOINT")" == "idle" ]; then
        echo "No active session to resume."
        exit 1
    fi
fi

# --force: Clear old state
if [[ "$ARGUMENTS" == *"--force"* ]]; then
    rm -rf "$STATE_DIR/state/*" "$STATE_DIR/reports/*" "$STATE_DIR/generated-skills/*"
fi
```

### 2. Initialize (First-Run Safe)

```bash
# Create directories (first-run safe)
mkdir -p "$MEMORY_DIR"
mkdir -p "$STATE_DIR"/{state,reports,generated-skills,history,backups}

# Helper: Read JSON with fallback
read_json_safe() {
    local file="$1"
    local default="$2"
    if [ -f "$file" ]; then
        cat "$file" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

# Detect first run
IS_FIRST_RUN=false
if [ ! -f "$MEMORY_DIR/patterns.json" ]; then
    IS_FIRST_RUN=true
    echo "📝 First run detected - initializing memory system..."
fi

# Initialize memory files if missing (see docs for full schema)
```

### 3. Delegate to Orchestrator

**CRITICAL**: Use context isolation - orchestrator runs in fork context.

```markdown
Task(subagent_type="evolving-orchestrator", prompt="""
Request: $ARGUMENTS
Task Type: $TASK_TYPE (from pattern matching)

Execute phases in sequence, each in fork context.
Return only brief status updates (1 line per phase).
Store ALL detailed output in files.

Return format:
📊 CONTEXT: [OK/Warning] - [N]% usage
🔍 PATTERNS: Matched [type], [N] recommendations
✅ ANALYZE: [N] AC identified
✅ GENERATE: Created v[N] skills
🔄 EXECUTE: Iter [N] - [status]
✅ VALIDATE: Score [N]/100
➡️ DECIDE: [SHIP/FIX/EVOLVE]
""")
```

---

## Output Example

```
🚀 Starting Self-Evolving Loop (Meta-Engineering v2.0)...

📊 CONTEXT: OK - 15% usage
🔍 PATTERNS: Matched 'auth', 3 recommendations
✅ ANALYZE: 5 acceptance criteria identified
✅ GENERATE: Created executor-v1, validator-v1, fixer-v1
🔄 EXECUTE: Iteration 1 - 4 files modified, 3/5 tests passing
✅ VALIDATE: Score 72/100
➡️ DECIDE: FIX (minor test failures)
🔄 EXECUTE: Iteration 2 - 2 files modified, 5/5 tests passing
✅ VALIDATE: Score 94/100
➡️ DECIDE: SHIP
📚 LEARN: 2 patterns identified
🧬 EVOLUTION: Updated memory
✅ SHIP: All criteria met!

📊 Summary: 2 iterations, 6 files changed, 5/5 AC complete
```

---

## Phase Agents

| Phase | Agent | Output File |
|-------|-------|-------------|
| ANALYZE | `requirement-analyzer` | `reports/analysis.json` |
| GENERATE | `skill-synthesizer` | `generated-skills/*.md` |
| EXECUTE | (generated executor) | codebase changes |
| VALIDATE | (generated validator) | `reports/validation.json` |
| DECIDE | `completion-judge` | `reports/decision.json` |
| LEARN | `experience-extractor` | `reports/learning.json` |
| EVOLVE | `skill-evolver` | evolved skills |

---

## State Files

```
.self-evolving-loop/          ← Session state (temporary)
├── state/checkpoint.json     ← Current state
├── reports/*.json            ← Phase outputs
├── generated-skills/*.md     ← Dynamic skills
└── history/*.jsonl           ← Event logs

.claude/memory/meta-engineering/  ← Persistent memory
├── tool-usage.json           ← Usage statistics
├── patterns.json             ← Learned patterns
└── evolution.json            ← Evolution history
```

---

## Stop / Resume

```bash
# Stop after current phase
touch .self-evolving-loop/state/stop

# Resume later
/evolving-loop --resume
```

---

## Related

- [/evolving-status](../evolving-status/SKILL.md) - View status and memory
- [evolving-orchestrator](../../agents/evolving-orchestrator.md) - Phase coordinator
- [Architecture Details](../../../docs/EVOLVING-LOOP-ARCHITECTURE.md) - Full technical docs
