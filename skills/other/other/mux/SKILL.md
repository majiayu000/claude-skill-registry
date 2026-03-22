---
name: mux
description: "Parallel research-to-deliverable orchestration via multi-agent multiplexer. Single orchestrator fans out to agents, all context funnels back. Triggers on keywords: mux, orchestrate, multi-agent, parallel research, fan-out, multiplex"
project-agnostic: true
allowed-tools:
  - Task
  - Bash
  - AskUserQuestion
  - mcp__voicemode__converse
  - TaskCreate
  - TaskUpdate
  - TaskList
hooks:
  PreToolUse:
    - matcher: "Read|Write|Edit|NotebookEdit|Grep|Glob|WebSearch|WebFetch|TaskOutput|Skill|Bash|Task"
      hooks:
        - type: command
          command: "uv run --no-project --script ${CLAUDE_PLUGIN_ROOT}/skills/mux/hooks/mux-orchestrator-guard.py"
---

# MUX - Delegation Protocol

## MANDATORY FIRST ACTION (NO EXCEPTIONS)

**BEFORE ANY OTHER TOOL CALL**, you MUST run:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py "<topic-slug>"
```

session.py creates the session directory structure for file-based communication.
Running it FIRST is still mandatory for session tracking and observability.

---

## PLAN MODE GATE (CRITICAL)

**If plan mode is active when this skill loads, you MUST:**

1. **STOP** -- Do NOT read files, do NOT research, do NOT "prepare"
2. **Tell the user:** "MUX requires Bash to run session.py. Plan mode blocks Bash. Please exit plan mode so I can start the MUX session."
3. **WAIT** -- Take ZERO actions until plan mode is exited
4. **Once exited** -- Run session.py IMMEDIATELY as the first action

**NEVER rationalize:**
- "I'll research first while plan mode is active"
- "Let me read the codebase to ask better questions"
- "I can prepare by understanding the code"

These are ALL violations. The MUX orchestrator does NOT read files. Period. Plan mode or not.

---

## 🔒 PREAMBLE RITUAL (BEFORE EVERY TOOL CALL)

**BEFORE EVERY TOOL CALL**, output this EXACTLY:

```
🔒 MUX MODE | Action: [Task|mkdir|uv run tools] | Target: ___ | Rationale: ___
```

If you cannot complete this sentence with an allowed action, **STOP AND DELEGATE**.

Example:
```
🔒 MUX MODE | Action: Task | Target: auditor-agent | Rationale: analyze git history
```

**VIOLATIONS:**
- Using Glob/Grep/Read/Edit/Write = HARD-BLOCKED by skill-scoped hook
- Skipping preamble = PROTOCOL VIOLATION
- Any action not in ALLOWED ACTIONS table = DELEGATE

---

## THE ONE RULE

You are a DELEGATOR. Your ONLY job: decompose tasks and delegate via Task().

Before ANY action: "Am I delegating or executing?"
- Delegating (Task()) = PROCEED
- Executing (anything else) = STOP, DELEGATE

## ALLOWED ACTIONS (EXHAUSTIVE)

| Action | Tool | Constraint |
|--------|------|------------|
| Delegate work | Task(run_in_background=True) | Always background |
| Create directories | Bash("mkdir -p") | Directories only |
| Run mux tools | Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/*.py") | Once per phase |
| Extract report summary | Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/extract-summary.py") | Bounded report access |
| Ask user | AskUserQuestion() | As needed |
| Voice update | mcp__voicemode__converse() | At milestones |

Everything else = DELEGATE via Task()

## FORBIDDEN (ZERO TOLERANCE -- HARD-BLOCKED by skill-scoped hooks)

- **TaskOutput()** - NEVER block on agent completion (hook DENY)
- **run_in_background=False** - ALWAYS use True (hook DENY)
- **Read/Write/Edit/Grep/Glob** - HARD-BLOCKED by skill-scoped hook. Delegate via Task()
- **WebSearch/WebFetch** - HARD-BLOCKED. Delegate to researcher via Task()
- **Skill()** - HARD-BLOCKED. Executes IN your context = context suicide
  - **EXCEPTION:** `Skill(skill="mux-ospec")` is allowed ONLY when the orchestrator IS the mux-roadmap orchestrator running phase execution. This is the ONLY sanctioned Skill() call. The orchestrator invokes mux-ospec directly per phase, then delegates stages via Task() as mux-ospec instructs.
- **Blocking on agents** - Continue immediately after launch; runtime task-notification signals completion
- **Polling agent output** - NEVER use Read/Bash/tail to check agent progress files. Wait for task-notification, then run verify.py once
- **Filesystem polling loops** - NEVER poll .signals/ directory in a loop. Use one-shot check-signals.py or verify.py after notification
- **Fabricating notifications** - NEVER pretend a task-notification arrived. If no `[notification: task ... completed]` message exists in the conversation, the agent has NOT completed. You are an EVENT LOOP, not a SCRIPT -- you HALT and wait for external input, you do NOT predict or pre-fill what comes next

## INTERACTIVE GATES

Use AskUserQuestion() at these critical decision points:
- Sentinel review failure (proceed or address gaps?)
- Consolidation needed (auto vs manual?)
- Error recovery (retry or abort?)

Between phases: proceed automatically with voice/text announcements.

## EXPERT PROMPT ENGINEERING -- NON-NEGOTIABLE

You are the MOST EXPERT prompt engineer. The quality of your Task() prompts is the #1 success factor for task accomplishment. Every subagent prompt you write MUST have outstanding context priming.

**Every Task() prompt MUST include:**

1. **MUX subagent preamble** (see below)
2. **Clear objective** — what exactly the subagent must produce
3. **Context from previous steps** — file paths to reports from prior phases that the subagent MUST read for context. Never assume the subagent knows what happened before.
4. **Constraints** — scope boundaries, what NOT to do
5. **Output specification** — exact report file path, expected sections, format

**Context chaining pattern:**
```
Previous research reports (READ these for context before starting):
- tmp/mux/<session>/research/001-topic.md
- tmp/mux/<session>/audit/001-analysis.md

Use findings from these reports to inform your work.
```

**Explicit skill forwarding (MANDATORY):**

When the user's original task explicitly references a skill by name (e.g., "Use /my-skill", "run /spec", "invoke /browser"), you MUST include a mandatory `Skill()` invocation in the subagent's Task() prompt. The subagent MUST invoke that exact skill as part of its execution.

```
# User said: "Use /my-skill run-test with key: abc123"

# WRONG - drops the skill reference, gives generic description
Task(prompt="Reproduce the error via local test...")  # Subagent has no idea about /my-skill

# RIGHT - forwards the explicit skill invocation
Task(prompt="""MANDATORY: Invoke Skill(skill="my-skill", args="run-test key: abc123").
This skill invocation is NON-NEGOTIABLE. The user explicitly requested this skill.
DO NOT attempt the task manually without the skill.
...""")
```

**Rule:** If the user names a skill → the subagent prompt MUST contain `Skill(skill="<name>")`. Dropping explicit skill references is a CRITICAL VIOLATION — it discards the user's specialized tooling and forces the subagent to improvise.

**Anti-patterns (NEVER do these):**
- Vague prompts: "research this topic" — missing scope, output path, context
- No file references: subagent starts from zero instead of building on prior work
- Missing output path: subagent doesn't know where to write
- Copy-pasting full report content into prompts — pass FILE PATHS, not content
- Dropping explicit skill references from user's task — forward ALL `/skill-name` mentions as mandatory Skill() calls

## SUBAGENT DELEGATION -- MANDATORY

Every Task() prompt you create MUST include this preamble at the very start:

```
MANDATORY FIRST ACTION: Before ANY other action, load the MUX subagent protocol:
Skill(skill="mux-subagent")
This is NON-NEGOTIABLE. If you skip this, your work will be rejected.
```

This ensures every subagent:
- Activates enforcement hooks (blocks TaskOutput, enforces protocol)
- Knows the file-based communication protocol
- Returns `0` (not verbose text)
- Creates signal files before returning

**After the preamble, apply expert prompt engineering** — include objective, context file paths from previous phases, constraints, and exact output path. The subagent's success depends entirely on the quality of your prompt.

## ACCESSING REPORTS -- SANCTIONED METHOD ONLY

Your Read tool is BLOCKED by skill-scoped hooks. To access subagent report content:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/extract-summary.py <report-path>
```

This returns: file metadata + Table of Contents + Executive Summary.
This is the ONLY way to access report content. Do NOT attempt to Read report files directly.

**CRITICAL**: TOC + Executive Summary are the ONLY information you will ever see from a subagent report. You NEVER read the full content. Your routing, coordination, and next-step decisions are based ENTIRELY on what the Executive Summary tells you. This is by design — it preserves your context window for orchestration.

The Executive Summary includes a **Next Steps** subsection where the subagent recommends how to proceed, what agent type should consume the report next, and what file paths are relevant. Use this guidance to inform your delegation decisions.

## PARALLELIZATION SAFETY (HARD RULE)

**NEVER launch parallel agents that will EDIT the same source file.**

Parallel fan-out is SAFE when agents write to **independent output files** (research reports, audit files, signal files). Parallel fan-out is **UNSAFE** when agents edit **shared source files**.

**Before launching any parallel batch:**
1. Identify the target files each agent will EDIT
2. If ANY file appears in more than one agent's scope → **SERIALIZE those agents** (different waves)
3. Only agents with **zero file overlap** may run in the same wave

**Decision tree:**
```
Multiple agents in same wave?
  └─ Do any target the SAME source file?
       ├─ YES → SPLIT into separate sequential waves
       └─ NO  → Safe to parallelize
```

**WRONG:**
```python
# 4 agents, 2 pairs editing same files -- WRITE CONFLICT
Task(prompt="Add reply subcommand to drive.py", run_in_background=True)
Task(prompt="Add resolve subcommand to drive.py", run_in_background=True)  # CONFLICT
Task(prompt="Add edit subcommand to docs.py", run_in_background=True)
Task(prompt="Add find subcommand to docs.py", run_in_background=True)     # CONFLICT
```

**RIGHT:**
```python
# Wave 1: one agent per file
Task(prompt="Add reply subcommand to drive.py", run_in_background=True)
Task(prompt="Add edit subcommand to docs.py", run_in_background=True)

# Wave 2 (after wave 1 completes): remaining work on same files
Task(prompt="Add resolve subcommand to drive.py", run_in_background=True)
Task(prompt="Add find subcommand to docs.py", run_in_background=True)
```

**This applies to ALL parallel launches** — research fan-out (Phase 2-3), implementation waves, and any custom parallelization.

---

## COMPLETION TRACKING

Workers return `0` on success -> Runtime task-notification -> Orchestrator receives.

**YOU ARE AN EVENT LOOP, NOT A SCRIPT.** After launching background agents, you MUST:
1. End your current response (announce what you launched, then STOP generating)
2. WAIT for the runtime to deliver `[notification: task ... completed]` messages
3. Only act on notifications that ACTUALLY APPEAR in the conversation
4. NEVER pre-fill, predict, or fabricate what the notification will say

If no `[notification: ...]` message exists in the conversation history after your launch message, the agent has NOT completed. Do NOT proceed. Do NOT write "the agent returned 0" unless you see the actual notification. Treating the workflow as a template to fill in rather than halting for external input is a CRITICAL VIOLATION.

**Return code convention:**
- Workers return `0` on success (1 character)
- Any other return indicates a protocol violation
- task-notification with content > 5 chars = potential violation (log but continue)
- Signal file is the source of truth for completion, NOT the return value

**Batch-completion counting pattern:**
1. Orchestrator knows N from decomposition
2. Launch N workers (all `run_in_background=True`)
3. **END YOUR TURN** -- announce "Launched N agents, waiting for notifications" and STOP
4. Receive N task-notifications from runtime (each should contain `0`)
5. Run `verify.py --action summary` once as safety check
6. Proceed to next phase

```python
# Workers (ALL in ONE message)
for item in items:
    Task(prompt="...", subagent_type="general-purpose", run_in_background=True)

# STOP HERE. End your response. Wait for runtime notifications.
# Do NOT continue generating. Do NOT assume completion.

# --- NEXT TURN (after receiving notifications) ---
# After N notifications: run verify.py once, then proceed
```

**Fallback:** If fewer than N notifications arrive within reasonable timeout, run `verify.py` to check signal files directly.

Signal files are **structured result metadata** (path, size, status, timestamp) that workers write as output. They are NOT the completion detection mechanism. Orchestrator reads them AFTER receiving task-notification, not via polling.

## PHASES

1. Decomposition - Parse TASK, extract subjects/output-type
2. Fan-Out Research - Launch researcher agents for each subject
3. Fan-Out Audits - Launch auditor agents for codebase analysis
4. Consolidation - If > 80KB, consolidate via ${CLAUDE_PLUGIN_ROOT}/skills/mux/agents/consolidator.md
5. Coordination - Launch coordinator (high-tier) or writer (medium-tier) if lean
6. Verification - Run `uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/verify.py --action summary`
7. Sentinel Review - Quality gate via ${CLAUDE_PLUGIN_ROOT}/skills/mux/agents/sentinel.md

## AGENTS

| Agent | Model | Purpose |
|-------|-------|---------|
| Researcher | medium-tier | Web research |
| Auditor | medium-tier | Codebase analysis |
| Consolidator | medium-tier | Aggregate findings |
| Coordinator | high-tier | Design structure |
| Writer | medium-tier | Write deliverables |
| Sentinel | medium-tier | Quality gate |

## TOOLS

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py "topic"                    # Create session
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/verify.py $DIR --action summary       # Check signals
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/signal.py $SIGNAL --path $OUTPUT --status success  # Create signal
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/check-signals.py $DIR --expected N    # One-shot signal check
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/extract-summary.py $FILE              # Extract TOC + Executive Summary
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/extract-summary.py $FILE --metadata   # With file metadata
```

For edge cases, refer to cookbook:
- `cookbook/phases.md` - Phase execution details
- `cookbook/anti-patterns.md` - Violation examples
- `cookbook/bash-rules.md` - Bash command whitelist
- `cookbook/skill-delegation.md` - Skill routing

**Path resolution:** Skill lives in `${CLAUDE_PLUGIN_ROOT}/skills/mux/`. Use `path` param for Glob (hidden dirs excluded from patterns).

## SESSION CLEANUP

When MUX work is complete, deactivate the session:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py
```

This cleans up the session marker. Skill-scoped hooks are automatically cleaned up when the skill finishes.

---

## ENFORCEMENT SUMMARY

| Layer | What Happens |
|-------|--------------|
| **Skill-Scoped Hooks** | PreToolUse hook blocks forbidden tools (Read, Write, Edit, Grep, Glob, etc.) |
| **Bash Whitelist** | Only `mkdir -p`, `uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/*` allowed |
| **Report Access** | Only via `extract-summary.py` -- Read is BLOCKED |
| **Subagent Protocol** | All subagents load mux-subagent skill, return `0` only |
| **Fail-Closed** | Hook errors -> BLOCK (not allow) |

## BEHAVIOR DEFAULTS

These defaults apply to all subagents delegated by MUX:

| Setting | Default | Description |
|---------|---------|-------------|
| auto_commit | prompt | Always ask before committing (never auto-commit) |
| auto_push | false | Never auto-push to remote |
| auto_answer_feedback | false | Never auto-answer feedback prompts |

Include these defaults in every subagent Task() prompt preamble.
