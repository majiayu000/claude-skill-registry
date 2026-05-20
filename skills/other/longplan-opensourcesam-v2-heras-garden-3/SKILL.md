---
name: longplan
description: Autonomous multi-step work with dual-reviewer supervision (1A2A workflow) and compound engineering principles
---

# Longplan (Port)

Use this when the user requests `/longplan`.

Follow `.claude/commands/longplan.md`. If a step requires tools not
available, note the adaptation and proceed with the closest equivalent.

## When to Use This vs Alternatives

| Your Situation | Use This | Not These |
|----------------|----------|-----------|
| Complex multi-step feature, 30+ min work | `/longplan` | `/ralph` (asset gen only) |
| Plan exists, stay in session, 5-10+ subagents | `/longplan` | `executing-plans` (new session) |
| Need plan + autonomous execution | `/longplan` | `subagent-driven-development` (plan required) |
| Debug/investigate first | Use `systematic-debugging` | Any execution skill |

**Relationship to other skills:**
- vs `ralph`: `ralph` is for batch asset generation (tiles, sprites). `/longplan` is for complex features.
- vs `executing-plans`: Use that for parallel session (separate window). `/longplan` stays in this session.
- vs `subagent-driven-development`: That skill executes existing plans with fresh subagent per task + 2 reviewers.

## Autonomous Work Mode (2A Phase)

**When working without human interaction during 2A phase:**

### Self-Checkpoints (Every 30 min or 5 file operations)
- [ ] Re-verify alignment with plan file
- [ ] Run quick tests if available
- [ ] Update progress tracking (checkpoint in plan file)
- [ ] Clear context if approaching token limit

### Blocker Response (Without Asking User)
1. **Try 2-3 alternative approaches** (5 min)
2. **Spawn MiniMax subagent** for research/sanity check (5 min)
3. **Try subagent suggestions** (5 min)
4. **Document and skip to next task** - circle back later
5. **ONLY after 30+ min of real attempts** → consider user escalation

### Quality Gates (Self-Enforced Before Declaring Done)
- [ ] All explicit success criteria from plan are met
- [ ] Time commitment fulfilled (check `.session_manifest.json`)
- [ ] Visual proof captured (screenshots for visual work)
- [ ] Narrative consistency verified (for story/dialogue work)
- [ ] Tests pass (if applicable)

**Remember:** Checkpointing (clearing context) is NOT stopping. It's managing token budget to continue working.

## Compound Engineering: Multi-Agent Delegation

**Core Philosophy:** Each unit of work should make future work easier.

This means every task should:
1. Solve the immediate problem
2. Make similar future problems easier to solve
3. Leave behind documentation, patterns, or tools that accelerate subsequent work

**Reference:** See `docs/agent-instructions/COMPOUND_ENGINEERING.md` for detailed compound engineering principles.

### Massive Parallel Delegation (Token-Efficient Architecture)

The key to velocity is parallelizing work across multiple subagents rather than doing everything sequentially. **The main agent's job is orchestration, not execution.**

**Use Kimi Supervisor for efficient exploration (with cross-model review):**

```
Main Agent (Claude - Orchestrator):
  → Invoke /skill kimi-supervisor for research
  → Claude spawns Kimi K2.5:
    - Kimi explores codebase (Glob/Grep/Read tools)
    - Kimi reads multiple files in parallel
    - Kimi synthesizes findings (1-2k tokens)
  → Claude spawns MiniMax for review:
    - MiniMax verifies Kimi's synthesis
    - Checks for hallucinations and errors
    - Returns APPROVED / concerns
  → Claude receives verified summary (1-2k tokens vs 10k+ raw)
  → Claude implements changes based on verified research
```

**Token efficiency:**
- Traditional: Claude reads 10 agent outputs (~10k tokens) = $150
- Kimi Supervisor: Claude reads verified summary (~1-2k tokens) = $10
- **Savings: ~93% on exploration phases**

**When to use Kimi Supervisor:**
- Research tasks requiring 2+ parallel agents
- Codebase exploration across multiple domains
- Pattern analysis with synthesis needed
- Batch operations (file reading, image analysis)

**When to use direct agents:**
- Single straightforward queries (no coordination overhead)
- Code implementation (you write code directly)
- Small verification tasks
- Asset generation (use MiniMax MCP directly)

**Delegation strategy (Wave approach):**
1. **Wave 1 (Research):** Claude spawns Kimi → Kimi explores → MiniMax reviews → Claude gets verified summary
2. **Wave 2 (Implementation):** Claude implements based on verified research
3. **Wave 3 (Validation):** Claude spawns agents to validate implementation
4. **Each wave compounds:** Research enables faster implementation, implementation enables faster validation

**Real-world example:**
- **Task:** Analyze dialogue patterns across 12 quest files
- **Without Kimi Supervisor:** Claude reads 12 files (15k tokens @ $15/M) = $0.225
- **With Kimi Supervisor:**
  - Kimi reads 12 files (15k tokens @ $0.30/M) = $0.0045
  - Kimi synthesizes to 2k tokens
  - MiniMax reviews (2k tokens @ $0.20/M) = $0.0004
  - Claude reads summary (2k tokens @ $15/M) = $0.03
  - **Total: $0.035 (84% savings)**

### Skip-Around Pattern for Stuck Tasks

**When stuck on a task:**

1. Document the challenge (1-2 lines in plan file)
2. Move to next todo item immediately
3. Circle back to stuck items after progress elsewhere
4. Try 2-3 alternatives before documenting as pending

**What counts as "stuck":**
- One approach failing (try alternatives)
- Slow operations (time ≠ stop)
- Uncertain about next step (make reasonable assumption, continue)
- Sequential advancement taking time (skip to next, circle back)

**What does NOT count as "stuck":**
- HARD STOPS (creating .md files, git push, editing CONSTITUTION.md)

### Autonomous Work (2A Phase) - Keep Working

**Core Rule:** Work continuously without stopping for summaries.

**DO:**
- Work through todos systematically
- Update plan file with quick notes
- Skip around stuck tasks
- Try 2-3 alternatives before documenting blockers
- Delegate to multiple subagents in parallel
- Continue working until blocked or complete

**DO NOT:**
- Stop to provide progress summaries
- Stop to "check in" with user
- Stop when one approach fails (try alternatives)
- Stop when work is slow or challenging
- Ask "should I continue?" (unless HARD STOP)

**Only stop for HARD STOPS:**
- Creating NEW .md files (not edits)
- Editing `.cursor/` directory
- Git push, force push, or branch operations
- Editing CONSTITUTION.md
- Actions outside approved scope
- Explicit user request to stop/pause

**EXCEPTION:** If blocked, MUST follow troubleshoot-and-continue protocol first:
1. Try 3 different approaches
2. Spawn MiniMax subagent for help
3. Try subagent suggestions
4. Document in plan file
5. THEN consider if still truly blocked

**CRITICAL: Completion Criteria Enforcement**

NEVER declare a task "complete" until ALL completion criteria are met:

```
BEFORE declaring done, verify:
□ All explicit success criteria from plan are satisfied
□ Visual quality gates passed (if applicable)
□ Narrative consistency verified (if applicable)
□ Time commitment fulfilled (if user specified duration)
□ No premature "good enough" declarations
```

**Visual Quality Gates (for game/assets):**
- Screenshots of actual rendered game MUST be captured
- Quality MUST surpass reference images (e.g., Harvest Moon comparison)
- NO declaring visual work done without visual proof

**Narrative Consistency Gates (for dialogue/story):**
- Dialogue MUST be checked against Storyline.md
- All choices and branches MUST align with narrative doc
- NO declaring narrative work done without cross-reference

**Time Commitment Enforcement:**
- If user says "work for 1 hour" → Work the FULL hour unless HARD STOP
- Track start time, do not stop early
- Set timer/alarm if needed to ensure full duration
- Early completion does NOT equal early stopping

**Compound Engineering Prevention:**
Document these anti-patterns to prevent recurrence:
- ❌ "I think this is good enough" → ✅ Criteria met + evidence
- ❌ "I'll stop early and summarize" → ✅ Continue until time/criteria complete
- ❌ "No blockers so I'll finish" → ✅ Finish criteria check first

**Todo Quote for Reinforcement:**
Append to each autonomous todo task:
"Remember: Skip around stuck tasks. Try 2-3 alternatives. Move to next todo. Circle back. Keep working. Do not make major repo changes unless approved. DO NOT STOP EARLY - complete all criteria first."

**MiniMax Subagent Quote (REQUIRED when blocked):**
"BLOCKED? Spawn MiniMax subagent BEFORE stopping: Task(subagent_name='minimax-mcp', prompt='Help with: [problem]. Return specific solutions.'). Try all suggestions before considering user interruption."

**Todo Quote for Reinforcement:**
Append to each autonomous todo task:
"Remember: Skip around stuck tasks. Try 2-3 alternatives. Move to next todo. Circle back. Keep working. Do not make major repo changes unless approved."
