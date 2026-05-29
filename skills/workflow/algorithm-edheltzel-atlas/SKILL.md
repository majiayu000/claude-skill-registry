---
name: Algorithm
description: Atlas skill, universal execution engine using scientific method to achieve ideal state. USE WHEN complex tasks, multi-step work, "run the algorithm", "use the algorithm", OR any non-trivial request that benefits from structured execution with ISC (Ideal State Criteria) tracking.
---

# THE ALGORITHM - Universal Execution Engine

**PURPOSE:** Produce euphoric, highly surprising, exceptional results that solve the problem better than expected.

**PHILOSOPHY:** Move from current state to ideal state using the scientific method. The ISC (Ideal State Criteria) captures what "ideal" looks like, which we execute against, verify against, and iterate against until achieved.

**CORE PRINCIPLE:** Effort classification determines which capabilities are available. Higher effort unlocks more powerful tools.

## Visual Display & Voice Notifications

**Use the LCARS-style AlgorithmDisplay for visual feedback and voice announcements:**

```bash
# Start algorithm with effort level (shows banner + announces via voice)
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts start THOROUGH -r "your request"

# Transition phases (updates display + voice announcement)
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts phase THINK
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts phase EXECUTE

# Show current status anytime
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts show

# Show just the effort banner
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts effort DETERMINED
```

**Phase Icons:** OBSERVE -> THINK -> PLAN -> BUILD -> EXECUTE -> VERIFY -> LEARN

## Quick Start

```bash
# 1. START WITH VISUAL DISPLAY (shows banner + voice announcement)
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts start STANDARD -r "your request"

# 2. CLASSIFY EFFORT (if not using display start)
bun run ~/.claude/skills/Algorithm/Tools/EffortClassifier.ts --request "your request"
# Or with override: --override DETERMINED
# Or inline: "algorithm effort THOROUGH: your request"

# 3. LOAD CAPABILITIES for effort level
bun run ~/.claude/skills/Algorithm/Tools/CapabilityLoader.ts --effort STANDARD

# 4. CREATE ISC
bun run ~/.claude/skills/Algorithm/Tools/ISCManager.ts create --request "your request"

# 5. TRANSITION PHASES (voice + visual update)
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts phase THINK
bun run ~/.claude/skills/Algorithm/Tools/AlgorithmDisplay.ts phase PLAN
# ... continues through EXECUTE, VERIFY, LEARN

# 6. MANAGE ISC during EXECUTE
bun run ~/.claude/skills/Algorithm/Tools/ISCManager.ts capability --row 1 -c research.perplexity
bun run ~/.claude/skills/Algorithm/Tools/ISCManager.ts update --row 1 --status DONE
bun run ~/.claude/skills/Algorithm/Tools/ISCManager.ts show
```

## Effort to Capability Matrix

| Effort | Models | Thinking | Debate | Research | Agents | Parallel |
|--------|--------|----------|--------|----------|--------|----------|
| **TRIVIAL** | - | - | - | - | - | 0 |
| **QUICK** | haiku | - | - | - | Intern | 1 |
| **STANDARD** | haiku, sonnet | UltraThink, FirstPrinciples | - | 1 agent | Engineer, QA, Designer | 1-3 |
| **THOROUGH** | haiku, sonnet | All | Council | parallel | All + Architect, Pentester | 3-5 |
| **DETERMINED** | all + opus | All | Council + RedTeam | all | unlimited | 10 |

## ISC Scale (CRITICAL)

**The ISC is NOT limited to a small number of rows.** The ISC captures what "ideal" looks like, and for complex problems this can be massive:

| Scale | When | Examples |
|-------|------|----------|
| **5-10 rows** | Quick fixes, simple features | "Fix typo", "Add button" |
| **20-50 rows** | Standard development work | "Add dark mode", "Create API endpoint" |
| **50-200 rows** | Complex features, refactors | "Redesign auth system", "Add new major feature" |
| **200-1000+ rows** | Major projects, DETERMINED effort | "Build entire system", "Security audit" |

**ISC rows come from:**
- **EXPLICIT requirements** - What user literally asked for
- **INFERRED requirements** - From context (tech stack preferences, past work, etc.)
- **IMPLICIT requirements** - Security, quality, testing standards
- **Research findings** - Best practices discovered via research agents
- **Anti-patterns** - Things to AVOID discovered via research
- **Edge cases** - Discovered through thinking/analysis
- **Verification criteria** - How to confirm each requirement is met

## The 7 Phases

Execute IN ORDER. Each phase mutates the ISC:

| Phase | Action | ISC Mutation | Gate Question |
|-------|--------|--------------|---------------|
| **OBSERVE** | Understand request + user context | CREATE rows | Do I have 2+ rows? Used context to infer? |
| **THINK** | Ensure nothing missing | COMPLETE rows | All rows clear, testable? |
| **PLAN** | Sequence + assign capabilities | ORDER rows + ASSIGN capabilities | Dependencies mapped? Capabilities assigned? |
| **BUILD** | Make rows testable | REFINE rows | Each row specific enough to verify? |
| **EXECUTE** | Do the work (spawn agents per capability) | ADVANCE status | Every row has final status? |
| **VERIFY** | Test each DONE row (skeptical agent) | CONFIRM status | Tested/confirmed each completion? |
| **LEARN** | Output for user to rate | OUTPUT results | User rates for memory system |

## The ISC Table

```markdown
## ISC: Request Summary

**Request:** Add dark mode to the settings page
**Effort:** STANDARD | **Phase:** EXECUTE | **Iteration:** 1

| # | What Ideal Looks Like | Source | Capability | Status |
|---|----------------------|--------|------------|--------|
| 1 | Research good patterns | INFERRED | research.perplexity | PENDING |
| 2 | Toggle component works | EXPLICIT | execution.engineer | ACTIVE |
| 3 | Theme state persists | EXPLICIT | execution.engineer | PENDING |
| 4 | Uses TypeScript | INFERRED | - | DONE |
| 5 | Tests pass | IMPLICIT | verification.qa | PENDING |
```

**Source types:**
- `EXPLICIT` - User literally said this
- `INFERRED` - Derived from user context (tech stack preferences, etc.)
- `IMPLICIT` - Universal standards (security, quality)

**Status progression:**
- `PENDING` -> `ACTIVE` -> `DONE`
- `ADJUSTED` - Modified with reason
- `BLOCKED` - Cannot achieve, triggers loop-back

## Iteration Loop

When VERIFY finds issues:

```
BLOCKED row
    |
    +- Unclear what ideal looks like? -> Loop to THINK
    +- Wrong approach? -> Loop to PLAN
    +- Execution error? -> Loop to EXECUTE

Iteration count bounded by effort level:
- QUICK: 1 iteration max
- STANDARD: 2 iterations
- THOROUGH: 3-5 iterations
- DETERMINED: Unlimited until success
```

## Integration

### Uses
- **Agents Skill** - AgentFactory for dynamic agent composition
- **CORE Skill** - User context for ISC inference
- **Browser Skill** - Web verification in VERIFY phase
- **DeepPlan Skill** - Persistent planning integration

### Memory
- ISC artifacts: `~/.claude/MEMORY/Work/{session}/ISC.md`
- Learnings: `~/.claude/MEMORY/Learning/ALGORITHM/`
- State: `~/.claude/MEMORY/State/algorithm-state.json`

## Workflow Routing

| Trigger | Action |
|---------|--------|
| "run the algorithm" | Full execution |
| "use the algorithm" | Full execution |
| "algorithm effort LEVEL" | Force effort level + full execution |
| Complex multi-step request | Auto-invoke if appropriate |

## Files

| File | Purpose |
|------|---------|
| `Tools/AlgorithmDisplay.ts` | LCARS visual display + voice announcements + loopback detection |
| `Tools/EffortClassifier.ts` | Classify TRIVIAL->DETERMINED |
| `Tools/ISCManager.ts` | Create/update/query ISC with capabilities |
| `Tools/CapabilityLoader.ts` | Load and filter capabilities by effort level |
| `Tools/CapabilitySelector.ts` | Select appropriate capabilities for ISC rows |
| `Tools/RalphLoopExecutor.ts` | Spawn persistent iteration loops |
| `Tools/TraitModifiers.ts` | Map effort levels to AgentFactory traits |
| `Tools/LearningCapture.ts` | Capture phase-based learnings |
| `Data/Capabilities.yaml` | Source of truth for capability matrix |
| `Phases/*.md` | Detailed documentation for each of the 7 phases |
| `Reference/*.md` | ISC format, capability matrix, effort matrix docs |

---

## Learning Loop

The Algorithm captures four signal types that feed back into improvement:

### Signal Types

| Signal | Captured By | Storage |
|--------|-------------|---------|
| **Ratings** | Stop hook detects "8/10", "great", etc. | `MEMORY/Signals/ratings.jsonl` |
| **Failures** | Stop hook detects errors, BLOCKED status | `MEMORY/Signals/failures.jsonl` |
| **Loopbacks** | AlgorithmDisplay detects phase regressions | `MEMORY/Signals/loopbacks.jsonl` |
| **Sentiment** | UserPromptSubmit hook analyzes tone | `MEMORY/Signals/sentiment.jsonl` |

### Phase-Based Learnings

Learnings are organized by Algorithm phase:

```
~/.claude/MEMORY/Learning/
├── OBSERVE/    # Context gathering insights
├── THINK/      # Analysis insights
├── PLAN/       # Planning insights
├── BUILD/      # Success criteria insights
├── EXECUTE/    # Implementation insights
├── VERIFY/     # Verification insights
└── ALGORITHM/  # Meta-learnings about the Algorithm itself
```

### Capturing Learnings

```bash
# Capture a learning from VERIFY phase
bun run ~/.claude/skills/Algorithm/Tools/LearningCapture.ts capture \
  -p VERIFY -i "Always check async state before assertions" -w "auth-bug"

# Capture meta-learning about the Algorithm
bun run ~/.claude/skills/Algorithm/Tools/LearningCapture.ts meta \
  --pattern "VERIFY fails on concurrent scenarios" \
  --recommendation "Add concurrent test setup to BUILD phase"

# View learning statistics
bun run ~/.claude/skills/Algorithm/Tools/LearningCapture.ts stats
```

### Loopback Detection

When a phase transition goes backward (e.g., VERIFY → THINK), the system:
1. Increments the iteration counter
2. Writes to `loopbacks.jsonl` with context
3. Announces via voice "Loopback iteration N"

### Analyzing Signals

Run `/atlas:analyze-signals` to see patterns and recommendations based on accumulated signals.

---

## The Purpose

**Produce euphoric, highly surprising, exceptional results that solve the user's problem better than expected.**

The ISC captures what "ideal" looks like. Effort determines available capabilities. Execute against it. Verify against it. Iterate until achieved.
