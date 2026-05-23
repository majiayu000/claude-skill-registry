---
# VERSION: 2.47.2
name: orchestrator
description: "Full orchestration workflow with Smart Memory-Driven context (v2.47), RLM-inspired routing (v2.46), and quality gates: clarify, smart memory search, classify 3D, plan, delegate, execute with parallel memory, validate quality-first, retrospect. Use when: (1) implementing features, (2) complex refactoring, (3) multi-file changes, (4) tasks requiring coordination. Triggers: /orchestrator, /orch, 'orchestrate', 'full workflow', 'implement feature'."
context: fork
user-invocable: true
agent: orchestrator
allowed-tools:
  - Task
  - AskUserQuestion
  - EnterPlanMode
  - ExitPlanMode
  - TodoWrite
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - mcp__plugin_claude-mem_*
hooks:
  SessionStart:
    - path: ~/.claude/hooks/orchestrator-init.sh
      once: true
  PreToolUse:
    - event: "Task"
      path: ~/.claude/hooks/smart-memory-search.sh
  PostToolUse:
    - event: "Task"
      path: ~/.claude/hooks/parallel-explore.sh
  Stop:
    - path: ~/.claude/hooks/orchestrator-report.sh
---

# Orchestrator - Multi-Agent Ralph v2.52

**Smart Memory-Driven Orchestration** with parallel memory search, RLM-inspired routing, and quality-first validation.

Based on @PerceptualPeak Smart Forking concept:
> "Why not utilize the knowledge gained from your hundreds/thousands of other Claude code sessions? Don't let that valuable context go to waste!!"

## Quick Start

```bash
# Via skill invocation
/orchestrator Implement OAuth2 authentication with Google

# Via CLI
ralph orch "Migrate database from MySQL to PostgreSQL"
```

## Core Workflow (v2.52.0 - 8 Major Steps, 23 Sub-steps)

### Step 0: EVALUATE (3-Dimension Classification)

**0a. Classification (v2.46 RLM)**:
| Dimension | Values | Purpose |
|-----------|--------|---------|
| Complexity | 1-10 | Scope, risk, ambiguity |
| Information Density | CONSTANT / LINEAR / QUADRATIC | How answer scales |
| Context Requirement | FITS / CHUNKED / RECURSIVE | Decomposition needs |

**0b. SMART MEMORY SEARCH (v2.47 NEW)**:

```
┌────────────────────────────────────────────────────────────────┐
│              SMART MEMORY SEARCH (PARALLEL)                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│   │claude-mem│ │ memvid   │ │ handoffs │ │ ledgers  │        │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘        │
│        │ PARALLEL   │ PARALLEL   │ PARALLEL   │ PARALLEL      │
│        └────────────┴────────────┴────────────┘               │
│                         ↓                                      │
│              .claude/memory-context.json                       │
│              ├── past_successes                                │
│              ├── past_errors                                   │
│              ├── recommended_patterns                          │
│              └── fork_suggestions (top 5)                      │
└────────────────────────────────────────────────────────────────┘
```

**AUTOMATIC**: Triggered by PreToolUse hook on Task invocation.

**Workflow Routing**:
| Density | Context | Complexity | Route |
|---------|---------|------------|-------|
| CONSTANT | FITS | 1-3 | **FAST_PATH** (3 steps) |
| CONSTANT | FITS | 4-10 | STANDARD |
| LINEAR | CHUNKED | ANY | PARALLEL_CHUNKS |
| QUADRATIC | ANY | ANY | RECURSIVE_DECOMPOSE |

### Step 0c: FAST_PATH Decision

If FAST_PATH eligible (complexity <= 3, CONSTANT, FITS):
```
DIRECT_EXECUTE -> MICRO_VALIDATE -> DONE (3 steps)
```
Otherwise, continue to Step 1.

### Step 1: CLARIFY (Memory-Enhanced)

**AUTOMATIC TLDR + MEMORY CONTEXT**:
```bash
# 1. Check memory context for similar past implementations
cat .claude/memory-context.json | jq '.fork_suggestions[:3]'

# 2. Semantic search for existing code
tldr semantic "$USER_TASK_KEYWORDS" .
```

**MUST_HAVE Questions** (Blocking):
```yaml
AskUserQuestion:
  questions:
    - question: "What is the primary goal?"
      header: "Goal"
      options:
        - label: "New feature"
        - label: "Bug fix"
        - label: "Refactoring"
        - label: "Performance"
```

### Step 1b: GAP-ANALYST (Memory-Enhanced)

Pre-implementation gap analysis using memory context:
- Check `past_errors` to avoid known pitfalls
- Review `recommended_patterns` for best practices
- Identify requirements not covered by memory

### Step 1c: PARALLEL_EXPLORE (5 Concurrent + Memory)

Launch 5 parallel exploration tasks:
1. **Semantic Search** - Code patterns
2. **Structure Analysis** - Codebase overview
3. **Dependency Scan** - Understanding deps
4. **Pattern Search** - Similar implementations
5. **Memory Correlation** - Match with past sessions

Results aggregated to `.claude/exploration-context.json`

### Step 2: CLASSIFY (3-Dimension)

| Score | Complexity | Model | Adversarial |
|-------|------------|-------|-------------|
| 1-2 | Trivial | MiniMax-lightning | No |
| 3-4 | Simple | MiniMax M2.1 | No |
| 5-6 | Medium | Sonnet | Optional |
| 7-8 | Complex | Opus | Yes |
| 9-10 | Critical | Opus (thinking) | Yes |

### Step 2b: WORKTREE DECISION

```yaml
AskUserQuestion:
  questions:
    - question: "Requires isolated worktree?"
      header: "Isolation"
      options:
        - label: "Yes, create worktree"
        - label: "No, current branch"
```

### Step 3: PLAN (Memory-Informed)

**Use memory context in planning**:
```bash
# Review what worked before
cat .claude/memory-context.json | jq '.insights.past_successes'

# Review what to avoid
cat .claude/memory-context.json | jq '.insights.past_errors'
```

Write plan with:
- Summary (informed by memory)
- Files to modify/create
- Dependencies
- Testing strategy
- Risks (include known issues from memory)

### Step 3b: PERSIST

Write to `.claude/orchestrator-analysis.md`

### Step 3c: PLAN-STATE

Initialize `.claude/plan-state.json` with spec vs actual tracking.

### Step 3d: RECURSIVE_DECOMPOSE (if needed)

For QUADRATIC or RECURSIVE tasks, spawn sub-orchestrators (max depth 3).

### Step 4: PLAN MODE

```yaml
EnterPlanMode: {}  # Claude Code reads orchestrator-analysis.md
```

Exit with `ExitPlanMode` when approved.

### Step 5: DELEGATE (Parallel-First)

**PRIORITY: Parallel execution when possible**

```yaml
# PARALLEL: Independent tasks
Task:
  subagent_type: "security-auditor"
  model: "opus"
  run_in_background: true
  prompt: "Audit: $FILES"

Task:
  subagent_type: "test-architect"
  model: "sonnet"
  run_in_background: true
  prompt: "Generate tests: $FILES"

# SEQUENTIAL: Dependent tasks
# Wait for results before continuing
```

### Step 6: EXECUTE-WITH-SYNC

Nested loop with parallel substeps:

```
EXTERNAL RALPH LOOP (max 25)
└── For EACH step:
    ├── LSA-VERIFY (architecture check)
    ├── IMPLEMENT (parallel if independent)
    ├── PLAN-SYNC (drift detection)
    └── MICRO-GATE (max 3 retries)
```

**CRITICAL: model: "sonnet" for all subagents**

### Step 6b.5: QUALITY-PARALLEL (NEW v2.80)

**Trigger**: `complexity >= 5` OR security-related code

**Launch parallel quality checks**:
```bash
# Launch 4 quality subagents in parallel
QUALITY_RESULT=$(./.claude/scripts/quality-coordinator.sh "$TARGET_FILE" "$COMPLEXITY")

# Parse result and extract run_id
RUN_ID=$(echo "$QUALITY_RESULT" | jq -r '.run_id')

# Store run_id for step 7
echo "$RUN_ID" > .claude/quality-results/current_run_id.txt
```

**Quality Agents Launched** (parallel, non-blocking):
1. **Security** (27 patterns, P0/P1/P2)
2. **Code Review** (4 agents, confidence ≥80)
3. **Deslop** (AI code cleanup)
4. **Stop-Slop** (AI prose cleanup)

**Store RUN_ID** for retrieval in step 7a.

### Step 7: VALIDATE (Quality-First v2.46)

### Step 7a: READ QUALITY RESULTS (NEW v2.80)

**Check if quality checks completed**:
```bash
# Read current run_id
if [[ -f .claude/quality-results/current_run_id.txt ]]; then
    CURRENT_RUN_ID=$(cat .claude/quality-results/current_run_id.txt)

    # Read aggregated results
    QUALITY_RESULTS=$(./.claude/scripts/read-quality-results.sh "$CURRENT_RUN_ID")

    # Parse results
    CRITICAL_COUNT=$(echo "$QUALITY_RESULTS" | jq -r '.summary.critical_findings // 0')
    TOTAL_FINDINGS=$(echo "$QUALITY_RESULTS" | jq -r '.summary.total_findings // 0')

    echo "Quality Results: $TOTAL_FINDINGS findings ($CRITICAL_COUNT critical)"
fi
```

**Decision Logic**:
- `CRITICAL_COUNT > 0`: BLOCK and require fixes
- `TOTAL_FINDINGS == 0`: Proceed to validation
- `TOTAL_FINDINGS > 0` but `CRITICAL_COUNT == 0`: Proceed with warnings

### Step 7: VALIDATE (Quality-First v2.46)

**Stage 1: CORRECTNESS (BLOCKING)**
- Meets requirements?
- Edge cases handled?

**Stage 2: QUALITY (BLOCKING)**
- Security verified?
- Performance OK?
- Tests adequate?

**Stage 3: CONSISTENCY (ADVISORY - not blocking)**
- Follows patterns?
- Style matches?

**Stage 4: ADVERSARIAL (if complexity >= 7)**
```bash
ralph adversarial "Design review"
```

### Step 8: RETROSPECTIVE (Mandatory)

```bash
ralph retrospective
```

**NEW v2.47**: Save learnings to memory for future sessions:
```bash
# Save successful patterns
ralph memvid save "Implemented OAuth2 successfully: [pattern details]"

# Record errors to avoid
ralph memvid save "AVOID: [error pattern] caused [issue]"
```

-> **VERIFIED_DONE**

## Model Routing (v2.47)

| Route | Primary | Secondary | Max Iter |
|-------|---------|-----------|----------|
| FAST_PATH | sonnet | - | 3 |
| STANDARD (1-4) | minimax-m2.1 | sonnet | 25 |
| STANDARD (5-6) | sonnet | opus | 25 |
| STANDARD (7-10) | opus | sonnet | 25 |
| PARALLEL_CHUNKS | sonnet (chunks) | opus (aggregate) | 15/chunk |
| RECURSIVE | opus (root) | sonnet (sub) | 15/sub |

## Integration Points

| Component | Role | When |
|-----------|------|------|
| **smart-memory-search.sh** | **PARALLEL memory search** | **Step 0b (NEW)** |
| /smart-fork | Find relevant sessions | Manual invocation |
| /fast-path-check | Trivial task detection | Step 0c |
| /parallel-explore | 5 concurrent exploration | Step 1c |
| /classify | 3-dimension classification | Step 2 |
| /gates | Quality validation | Step 7 |
| /adversarial | Spec refinement | Step 7 |
| /retrospective | Post-analysis | Step 8 |

## Memory Sources (Searched in Parallel)

| Source | Content | Speed |
|--------|---------|-------|
| **claude-mem MCP** | Semantic observations | Fast |
| **memvid** | Vector-encoded context | Sub-5ms |
| **handoffs** | Session snapshots | Fast |
| **ledgers** | Continuity data | Fast |

## Anti-Patterns

- Never start without smart memory search
- Never skip clarification
- Never use model: "haiku" for subagents
- Never skip retrospective
- Never attempt more than 3 fixes (3-Fix Rule)
- **Never block on consistency issues** (quality over consistency)
- **Never ignore memory context** (learn from history)

## Completion Criteria

`VERIFIED_DONE` requires ALL:
1. Smart Memory Search complete (memory-context.json exists)
2. Task classified (3 dimensions)
3. MUST_HAVE questions answered
4. Plan approved
5. Implementation complete
6. CORRECTNESS passed (blocking)
7. QUALITY passed (blocking)
8. Adversarial passed (if complexity >= 7)
9. Retrospective done + learnings saved to memory

## Examples

### Standard Task with Memory

```
User: "Add JWT authentication"

Step 0a: Classify -> Complexity: 7, LINEAR, FITS
Step 0b: Smart Memory Search
  -> Found: 3 past sessions with auth implementations
  -> past_successes: "Use passport.js for OAuth"
  -> past_errors: "Don't store tokens in localStorage"
  -> fork_suggestion: session-abc123

Step 1: Clarify (informed by memory)
  -> Skip questions about token storage (already known)
  -> Focus on new requirements

... (continue with memory-informed implementation)

Step 8: Retrospective
  -> Save: "JWT with refresh tokens implemented successfully"
  -> Save: "AVOID: Token expiry not handled - fix applied"
```

## CLI Commands (v2.47)

```bash
# Smart memory search
ralph memory-search "OAuth implementation"
ralph fork-suggest "Add authentication"
ralph memory-stats

# Standard orchestration
ralph orch "task description"
ralph gates
ralph adversarial "spec"
```
