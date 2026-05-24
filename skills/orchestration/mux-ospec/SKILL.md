---
name: mux-ospec
description: "Orchestrates the spec workflow via MUX delegation, combining parallel research-to-deliverable orchestration with spec stage-based execution. Triggers on keywords: mux ospec, ospec"
argument-hint: "[modifier] [spec_path|inline_prompt]"
project-agnostic: true
requires-skills:
  - spec
allowed-tools:
  - Task
  - Bash
  - AskUserQuestion
  - mcp__voicemode__converse
---

# MUX Spec Orchestrator

## DEPENDENCY GUARD (MANDATORY)

This skill declares `requires-skills: spec` in frontmatter.

If runtime reports missing dependency, STOP and report:

```
DEPENDENCY_MISSING: mux-ospec requires the `spec` skill from ac-workflow.
Install: claude plugin install ac-workflow@agentic-plugins
```

Do NOT attempt manual stage execution as a fallback.

# MUX-OSPEC - O_Spec Workflow Orchestrator

## MANDATORY FIRST ACTION (NO EXCEPTIONS)

**BEFORE ANY OTHER TOOL CALL**, you MUST run:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py "mux-ospec-{topic}"
```

This creates the session AND activates MUX enforcement hooks.
**If you skip this, hooks will block all subsequent tool calls.**

---

## MUX PROTOCOL (MANDATORY)

Run session.py FIRST (see MANDATORY FIRST ACTION above). Then comply with MUX delegation protocol:

- You are a DELEGATOR. ONLY delegate via Task(run_in_background=True)
- Read/Write/Edit/Grep/Glob blocked by allowed-tools frontmatter
- Completion: workers return `0` -> runtime task-notification -> proceed
- After receiving task-notification, delegate signal reading to Task(haiku/explore) for routing data
- Run verify.py once as safety check before proceeding to next phase
- Continue immediately after launch (never block)

For full protocol details: `${CLAUDE_PLUGIN_ROOT}/skills/mux/SKILL.md`

## OSPEC-SPECIFIC RULES

**You NEVER interpret stage results.** When a stage agent completes:
- Delegate reading signal/output to Task(haiku/explore)
- Receive ONLY routing data: status, grade, commit hash
- Route to next stage based on returned routing data
- NEVER read signal files, review reports, or stage outputs yourself

**You NEVER skip intermediate stages.** The workflow sequence is STRICT:
- `full`: GATHER -> CONSOLIDATE -> CONFIRM SC -> PLAN (all three intermediate steps MANDATORY)
- `lean`/`leanest`: CONFIRM SC -> PLAN (SC gate MANDATORY)
- Jumping from GATHER directly to PLAN is a CRITICAL VIOLATION
- CONFIRM SC requires explicit user approval via AskUserQuestion before proceeding

## CRITICAL: NO DESCRIPTION WITHOUT ACTION

VIOLATION: Responding with "I will delegate via Task()" without actual Task() call
CORRECT: Immediately invoke Task() with no preamble

If you find yourself writing "I will..." or "The next step is...", STOP. Make the tool call instead.

---

## INPUT & PATHS

Parse $ARGUMENTS: MODIFIER (full/lean/leanest), SPEC_PATH or INLINE_PROMPT, FLAGS (--cycles=N, --phased)

**CREATE Detection**: If SPEC_PATH does not resolve to an existing file, or first argument is "CREATE", or arguments contain "create spec"/"new spec"/"generate spec", treat as CREATE stage input. The remaining text becomes the inline prompt for /spec CREATE.

MUX tools are available at `${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/` relative to the project root.

```
MUX_TOOLS="${CLAUDE_PLUGIN_ROOT}/skills/mux/tools"
```

Spec path resolution uses the plugin-local resolver:
```bash
# Resolve spec path (plugin-local, no global dependency)
source "${CLAUDE_PLUGIN_ROOT}/scripts/spec-resolver.sh"
SPEC_PATH=$(resolve_spec_path "$SPEC_PATH")
```

**CRITICAL PATH RULE: `{session}` is ALWAYS a RELATIVE path from project root (e.g., `tmp/mux/20260209-1430-topic`). It is NEVER absolute. The `tmp/` prefix refers to a project-local directory, NOT the system `/tmp/`. When passing `{session}` or any signal path to subagents, include this warning: "Path is RELATIVE to project root. Do NOT prepend '/'."**

## WORKFLOW BY MODIFIER

| Modifier | Stages |
|----------|--------|
| `full` | CREATE (optional) -> GATHER -> CONSOLIDATE -> [CONFIRM SC] -> PHASE_LOOP -> TEST -> DOCUMENT -> SENTINEL |
| `lean` | CREATE (optional) -> [CONFIRM SC] -> PHASE_LOOP -> TEST -> DOCUMENT -> SELF-VALIDATION |
| `leanest` | CREATE (optional) -> [CONFIRM SC] -> PHASE_LOOP -> TEST -> SELF-VALIDATION |

## PHASE EXECUTION

Each stage = one Task() subagent whose FIRST and MANDATORY action is `/spec <STAGE>`.
mux-ospec knows NOTHING about how stages work internally. It only knows the ORDER.

### CREATE Stage (optional, all modes)

**Goal**: Create NEW spec file from scratch based on user request.

**Trigger**: User provides inline spec request OR explicitly requests spec creation.

**Detection**:
- Arguments contain spec description (not existing path)
- User says "create spec", "new spec", or "generate spec"
- No SPEC_PATH resolves to an existing file

**Workflow**:
1. USER provides spec request (HLO, MLO, details)
2. DELEGATE to Task with CREATE instruction
3. Worker invokes Skill(skill="spec", args="CREATE {inline_prompt}")
4. Worker returns "done"
5. ORCHESTRATOR delegates signal reading
6. ORCHESTRATOR receives path to created spec
7. ORCHESTRATOR proceeds to next stage (GATHER or PHASE_LOOP)

**Task Template**:

```python
Task(prompt=f"""Your FIRST and MANDATORY action:
Skill(skill="spec", args="CREATE {inline_prompt}")

DO NOT read files, plan, or analyze before invoking this Skill.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. git log --oneline -5 | grep -i "spec.*CREATE"
2. Spec file exists at returned path

Signal: uv run {MUX_TOOLS}/signal.py {{session}}/.signals/create.done --status success --meta path="$(cat {{session}}/.signals/spec-path.txt)"

RETURN: "STAGE_CREATE_COMPLETE"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

**Signal Protocol**:
- Signal path: `{session}/.signals/create.done`
- Metadata: `path=<absolute_path_to_created_spec>`
- Status: success | failed
- Error: description if failed

**Template Structure** (via /spec CREATE):
- Human Section: HLO, MLO, Details, Behavior (optional)
- AI Section: Research, Plan, Plan Review, Implement, Test Evidence & Outputs, Updated Doc, Post-Implement Review
- Path convention: `specs/<YYYY>/<MM>/<bundle>/<NNN>-<short-title>.md`
- Smart path defaulting: Checks git history for recent specs, proposes next number OR new bundle

### GATHER (full only)

MUX parallel research - NOT a /spec stage. Uses MUX fan-out pattern.

```python
Task(prompt="""You are a MUX research orchestrator for: {spec_context}

YOUR FIRST AND ONLY ACTION: Orchestrate research via parallel Task() delegation.
Subjects: [Web research, Codebase audit, Pattern analysis]
Consolidate to: {session}/research/consolidated.md

DO NOT read source files yourself. DO NOT write consolidated output yourself.
If research fails, RETURN "STAGE_FAILED".

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/gather.done --status success
RETURN: "STAGE_GATHER_COMPLETE"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

### CONSOLIDATE (full only)

Synthesize parallel GATHER research into single consolidated output. NOT a /spec stage.

**CRITICAL: This is a MANDATORY step between GATHER and CONFIRM SC in full mode. Do NOT skip to CONFIRM SC or PLAN.**

```python
Task(prompt="""You are a research consolidation agent for: {spec_context}

YOUR TASK: Read all research outputs from {session}/research/ and synthesize into {session}/research/consolidated.md

The consolidated output MUST include:
1. Key findings from all research subjects
2. SUCCESS_CRITERIA section (extracted/synthesized from research)
3. Risk assessment and dependencies

DO NOT read source code yourself. Only synthesize from research outputs.
If consolidation fails, RETURN "STAGE_FAILED".

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/consolidate.done --status success
RETURN: "STAGE_CONSOLIDATE_COMPLETE"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

### CONFIRM SC (all modes - MANDATORY GATE)

**YOU MUST NOT PROCEED TO PLAN WITHOUT COMPLETING THIS GATE. NO EXCEPTIONS.**

Refinement loop - present SC to user, iterate if needed.

**Full mode**: Extract SC from consolidated research output.
**Lean/leanest modes**: Extract SC directly from spec file.

```python
# 1. Delegate reading SC summary
# Full mode: read from research/consolidated.md
# Lean/leanest modes: read from spec file's Human Section
source_file = "{session}/research/consolidated.md" if modifier == "full" else "{spec_path}"

Task(prompt=f"Read {source_file}. Return ONLY the SUCCESS_CRITERIA section.",
     subagent_type="Explore", model="haiku", run_in_background=True)

# 2. Present to user
AskUserQuestion(question="Review SUCCESS_CRITERIA. Approve or refine?",
    options=[
        {"label": "Approve", "description": "SC accepted, proceed to PLAN"},
        {"label": "Refine", "description": "Adjust SC before proceeding"}
    ])

# 3. If REFINE: delegate SC update, re-present
# Loop until approved or max 3 iterations
```

### PHASE_LOOP (PLAN -> IMPLEMENT -> REVIEW -> FIX)

For each phase N, delegate ONE stage at a time. Each stage agent's FIRST action = `/spec <STAGE>`.

#### PLAN

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="PLAN {spec_path}")

DO NOT read files, write code, or do anything before invoking this Skill.
DO NOT plan as a fallback if the Skill fails.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. git log --oneline -5 | grep -i "spec.*PLAN" (commit must exist)
2. Spec file has >50 lines in AI Section

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/phase-{N}-plan.done --status success --meta commit="$(git rev-parse --short HEAD)"
RETURN: "STAGE_PLAN_COMPLETE"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

#### IMPLEMENT

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="IMPLEMENT {spec_path}")

DO NOT read the spec to "understand" it first. DO NOT write code yourself.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. git log --oneline -10 | grep -E "(feat|fix|refactor)\\(" (commit must exist)
2. Type check passes: {type_check_cmd}
3. No test regressions: {test_cmd}

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/phase-{N}-implement.done --status success --meta commit="$(git rev-parse --short HEAD)"
RETURN: "STAGE_IMPLEMENT_COMPLETE"
""", subagent_type="general-purpose", model="sonnet", run_in_background=True)
```

#### REVIEW

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="REVIEW {spec_path}")

ENHANCEMENT: Also read the spec-reviewer agent definition at ${CLAUDE_PLUGIN_ROOT}/skills/mux-ospec/agents/spec-reviewer.md for additional review criteria beyond /spec defaults.

DO NOT invent your own review criteria. DO NOT fix issues (only report them).
CRITICAL: Be ruthlessly honest. ONLY grade PASS if ALL checks pass. WARN is NOT "good enough" - it triggers a FIX cycle.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. Review report exists with explicit grade: PASS, WARN, or FAIL

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/phase-{N}-review-{cycle}.done --status success --meta grade="{PASS|WARN|FAIL}"
RETURN: "STAGE_REVIEW_COMPLETE grade={PASS|WARN|FAIL}"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

#### FIX

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="FIX {spec_path}")

ENHANCEMENT: Also read the spec-fixer agent definition at ${CLAUDE_PLUGIN_ROOT}/skills/mux-ospec/agents/spec-fixer.md for context-preserving fix protocol.
REVIEW REPORT: {session}/reviews/phase-{N}-review-{cycle}.md

DO NOT invent fixes outside the review findings. DO NOT delete working code.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. git log --oneline -5 | grep -i "fix" (commit must exist)
2. Type check passes: {type_check_cmd}

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/phase-{N}-fix-{cycle}.done --status success --meta commit="$(git rev-parse --short HEAD)"
RETURN: "STAGE_FIX_COMPLETE"
""", subagent_type="general-purpose", model="sonnet", run_in_background=True)
```

### TEST

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="TEST {spec_path}")

ENHANCEMENT: Also read the spec-tester agent definition at ${CLAUDE_PLUGIN_ROOT}/skills/mux-ospec/agents/spec-tester.md for adaptive test execution and framework detection.

DO NOT write tests yourself. DO NOT skip execution. DO NOT fabricate results.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. Tests actually ran (check output for pass/fail counts)

CRITICAL: ONLY grade=PASS is acceptable. WARN (lint warnings, >50% skipped, no tests found) = FAIL.
Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/test.done --status success --meta grade="{PASS|WARN|FAIL}",tests_run={N},tests_passed={N}
RETURN: "STAGE_TEST_COMPLETE grade={PASS|WARN|FAIL}"
""", subagent_type="general-purpose", model="sonnet", run_in_background=True)
```

### DOCUMENT (full/lean)

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="DOCUMENT {spec_path}")

DO NOT read source files to summarize them. DO NOT write docs yourself.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. git log --oneline -5 | grep -i "spec.*DOCUMENT" (commit must exist)

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/document.done --status success --meta commit="$(git rev-parse --short HEAD)"
RETURN: "STAGE_DOCUMENT_COMPLETE"
""", subagent_type="general-purpose", model="sonnet", run_in_background=True)
```

### SENTINEL (full) / SELF-VALIDATION (lean/leanest)

```python
Task(prompt="""THINK VERY HARD; TAKE YOUR TIME.

Your FIRST and MANDATORY action:
Skill(skill="spec", args="SENTINEL {spec_path}")

ENHANCEMENT: Also read the sentinel agent definition at ${CLAUDE_PLUGIN_ROOT}/skills/mux-ospec/agents/validator.md for cross-phase coordination review criteria.

DO NOT approve incomplete work. DO NOT override the grade.
CRITICAL: ONLY grade=PASS completes the workflow. WARN is NOT acceptable.
If you get "Permission to use Skill has been denied", return EXACTLY: PERMISSION_DENIED: Skill
If Skill fails for other reasons: RETURN "STAGE_FAILED"

After Skill completes, verify:
1. All SC items explicitly graded
2. Overall grade is explicit: PASS, WARN, or FAIL
3. If grade is WARN or FAIL, report it accurately - orchestrator will handle escalation

Signal: uv run {MUX_TOOLS}/signal.py {session}/.signals/sentinel.done --status success --meta grade="{PASS|WARN|FAIL}"
RETURN: "STAGE_SENTINEL_COMPLETE grade={PASS|WARN|FAIL}"
""", subagent_type="general-purpose", model="opus", run_in_background=True)
```

## TOOLS

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py "mux-ospec-{topic}"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/signal.py $SIGNAL --path $OUTPUT --status success
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/check-signals.py $DIR --expected N
```

## LESSONS LEARNED (HARDCODED - NEVER VIOLATE)

### 1. Orchestrator Must Not Read Spec Files

**What failed:** Orchestrator read the spec file directly, ran git commands, listed directories, searched patterns. Consumed 55s and massive context before any delegation happened. No work done. Spec file remained empty. No PLAN commit. No IMPLEMENT commit.

**Rule:** RUN session.py FIRST. Session init activates hooks that BLOCK Read/Grep/Glob. Delegate ALL spec reading to stage agents. Orchestrator receives ONLY signal notifications and stage completion status. If you find yourself reading ANY file, you are VIOLATING this rule.

### 2. Stage Agents Must Invoke /spec as FIRST Action

**What failed:** PLAN agent received spec path and wrote its own plan without invoking `/spec PLAN`. Spec file empty. No commit. Agent "helped" by doing the work itself.

**Rule:** Every stage agent's FIRST and MANDATORY action = `Skill(skill="spec", args="<STAGE> <spec_path>")`. No reading, no writing, no thinking before invoking /spec. The Skill IS the work.

### 3. Stage Agent Returns Without Artifacts

**What failed:** Agent returned "STAGE_PLAN_COMPLETE" without producing commits, signals, or output files. Git log unchanged. Agent claimed success falsely.

**Rule:** Orchestrator delegates signal reading after every return. Signal must contain status + metadata (commit hash, grade). Missing signal or missing metadata = STAGE_FAILED. Delegate verification to signal reader, never trust agent return value alone.

### 4. Direct Skill() Invocation Killed Orchestrator

**What failed:** Orchestrator called Skill(skill="spec", args="PLAN ...") directly. Entire spec workflow loaded into orchestrator context. Context died before IMPLEMENT.

**Rule:** NEVER invoke Skill() directly. Always delegate: Task(prompt="Invoke Skill(...)").

### 5. Always Launch NEW Stage Agent After Failure

**What failed:** Attempting to resume a stage agent after STAGE_FAILED polluted context from the failed attempt. Agent carried stale state and repeated the same error.

**Rule:** After any STAGE_FAILED or review cycle fix, always launch a FRESH stage agent. Never resume a failed one. Fresh context = clean execution.

### 6. Orchestrator Must Not Interpret Stage Results

**What failed:** Orchestrator read signal files and review reports directly to determine routing (PASS/WARN/FAIL). This consumed context with review details the orchestrator doesn't need, and violated the delegation principle.

**Rule:** After EVERY stage notification, delegate reading the signal file to Task(haiku/explore). Receive ONLY structured routing data: status, grade, commit, error. Route based on routing data. NEVER read signal files, review reports, test outputs, or any stage artifacts yourself.

### 7. CREATE Stage Must Delegate to /spec CREATE

**What to avoid:** Orchestrator creates spec file directly, applies templates manually, or resolves paths itself.

**Rule:** Delegate to Task() which invokes Skill(skill="spec", args="CREATE {prompt}"). Never create spec files directly from the orchestrator.

**Reason:** /spec CREATE has smart path defaulting, template application, commit handling. Bypassing it loses path convention enforcement, template structure, and git commit standards.

### 8. Same-File Parallel Agents Cause Write Conflicts

**What failed:** IMPLEMENT stage decomposed work into P0/P1 waves. P0 launched 4 parallel agents: 2 editing `drive.py` + 2 editing `docs.py`. Both pairs clobbered each other's writes. Orchestrator detected the conflict ("Conflict risk: 2 agents editing drive.py + 2 agents editing docs.py") but proceeded anyway because no hard rule stopped it.

**Rule:** NEVER launch parallel agents that EDIT the same source file. Before any parallel batch, check target file overlap. If ANY file appears in >1 agent's scope, SPLIT into sequential waves with one agent per file per wave. "Merge/reconciliation after" is NOT acceptable — prevent the conflict, don't plan to recover from it.

**Applies to:** IMPLEMENT waves, phase-decomposition waves, any fan-out that edits source files.

### 9. Never Skip CONSOLIDATE or CONFIRM SC Gates

**What failed:** In `full` mode, orchestrator went GATHER -> PLAN, skipping both CONSOLIDATE and CONFIRM SC. User had to manually intervene ("DO NOT SKIP THE SC CONFIRMATION!"). Root cause: Checkpoint Pattern and Report templates did not list CONSOLIDATE or CONFIRM_SC stages, so the orchestrator "forgot" about them when printing progress and routing to the next stage.

**Rule:** After GATHER completes in `full` mode, the NEXT stage is ALWAYS CONSOLIDATE. After CONSOLIDATE, the NEXT stage is ALWAYS CONFIRM SC. After CONFIRM SC (user approval), THEN and ONLY THEN proceed to PLAN. Skipping any of these is a CRITICAL VIOLATION. The Workflow Progress tracker MUST show these stages at all times.

### 10. Explicit Skill References Must Be Forwarded to Subagents

**What failed:** User explicitly said "Use /my-skill run-test with ..." but MUX orchestrator launched the subagent with a generic task description ("Reproduce error via local test"). The skill reference was dropped. Subagent had no idea about /my-skill and improvised without the user's specialized tooling.

**Rule:** When the user's task explicitly references a skill by name (e.g., "Use /my-skill", "run /spec", "invoke /browser"), the orchestrator MUST include a mandatory `Skill(skill="<name>", args="...")` invocation in the subagent's Task() prompt. Dropping explicit skill references is a CRITICAL VIOLATION — it discards the user's specialized tooling. The subagent prompt must make clear the Skill() call is NON-NEGOTIABLE and must not be skipped or replaced with manual execution.

### 11. ONLY PASS Proceeds in Quality Gates (ZERO TOLERANCE)

**What failed:** Orchestrator accepted WARN grades in REVIEW, TEST, SELF-VALIDATION, and SENTINEL stages, proceeding "with warnings." This allowed substandard work through quality gates, violating the spec contract. WARN was treated as "good enough" when it explicitly signals unresolved issues.

**Rule:** In REVIEW, TEST, SELF-VALIDATION, and SENTINEL stages, ONLY a PASS grade allows progression. WARN and FAIL both trigger FIX cycles. If max cycles are exhausted without achieving PASS, the orchestrator MUST escalate to the user via AskUserQuestion — NEVER proceed with a non-PASS grade. This is NON-NEGOTIABLE. "Proceed with warning" is a CRITICAL VIOLATION.

## ERROR RECOVERY

| Scenario | Action |
|----------|--------|
| CREATE fails | Escalate to user - spec path or prompt may need adjustment |
| Stage agent timeout | If no task-notification after extended time, run verify.py to check signals. If worker truly stuck, mark STAGE_FAILED, launch fresh agent |
| Skill(spec) internal failure | Stage agent returns STAGE_FAILED with error details |
| Type check fails 3x | STAGE_FAILED with error details, escalate to user |
| Tests fail 3x | STAGE_FAILED with failure analysis, escalate to user |
| Context exhaustion | Stage agent dies mid-work. Relaunch from last signal checkpoint |
| Review cycle WARN/FAIL after max cycles | STAGE_FAILED. Escalate to user - ONLY PASS proceeds |
| Signal file missing after "done" | Treat as STAGE_FAILED, relaunch fresh agent |
| Skill permission denied | Subagent returns PERMISSION_DENIED. Escalate to user: "Background agents cannot surface permission prompts. Run Claude Code with `--dangerously-skip-permissions` or add `Skill` to allowed tools in `.claude/settings.json`" |

## SESSION CLEANUP

When mux-ospec work is complete, deactivate the session:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py
```

This removes the mux-active observability marker. Skill-scoped hooks are
automatically cleaned up when the skill finishes.

## COOKBOOK

- `cookbook/ospec-workflow.md` - Stage sequences, model tiers, TDD enforcement
- `cookbook/ospec-phases.md` - Detailed phase execution
- `cookbook/stage-patterns.md` - Stage delegation templates
- `cookbook/review-cycles.md` - N-cycle review pattern
- `cookbook/session-structure.md` - Directory layout
- `cookbook/signal-protocol.md` - Signal file format
- `cookbook/state-persistence.md` - Resume capability
- `cookbook/anti-patterns.md` - Violation examples with WRONG/RIGHT patterns
- `cookbook/skill-delegation.md` - Skill routing table
- `cookbook/bash-rules.md` - Bash command whitelist
- `cookbook/error-recovery.md` - Error handling and retry patterns
- `cookbook/phase-decomposition.md` - DAG-based phase decomposition
- `cookbook/stack-priming.md` - Stack-specific context injection
- `cookbook/test-commands.md` - Framework-specific test commands
- `cookbook/refinement.md` - Refinement loop protocol and question patterns

---

## ENFORCEMENT SUMMARY

| Layer | What Happens |
|-------|--------------|
| **Session Init** | MUST run session.py FIRST - creates enforcement marker |
| **Forbidden Tools** | Read/Write/Edit/Grep/Glob blocked by allowed-tools frontmatter |
| **Bash Whitelist** | Only `mkdir -p`, `ls`, `uv run tools/*` allowed |
| **Subagent Protocol** | Workers return `0` -> runtime task-notification -> proceed |
| **Fail-Closed** | Hook errors -> BLOCK (not allow) |

## BEHAVIOR DEFAULTS

These defaults apply to all subagents delegated by mux-ospec:

| Setting | Default | Description |
|---------|---------|-------------|
| auto_commit | prompt | Always ask before committing (never auto-commit) |
| auto_push | false | Never auto-push to remote |
| auto_answer_feedback | false | Never auto-answer feedback prompts |

Include these defaults in every stage agent Task() prompt preamble.

---

## SIGNAL READER PROMPT TEMPLATE

After EVERY stage notification, delegate reading the signal to get routing data.
**The orchestrator NEVER reads signal files directly.**

**CRITICAL: Signal paths are RELATIVE to the project root (e.g., `tmp/mux/20260209-1430-topic/.signals/phase-1-plan.done`).
They must NEVER be converted to absolute paths. Do NOT prepend `/` — `tmp/` is NOT `/tmp/`.**

```python
Task(
    prompt=f"""Read the signal file at {signal_path}.

IMPORTANT: This path is RELATIVE to the project root. Use it exactly as given.
Do NOT prepend '/' or convert to an absolute path. 'tmp/' is a project-local directory, NOT '/tmp/'.

Return ONLY this structured routing data, nothing else:

status: <success|failed>
grade: <PASS|WARN|FAIL|N/A>
commit: <hash|N/A>
error: <description|none>
metadata: <key=value pairs from signal>

Do NOT summarize, interpret, or add commentary. Raw routing data only.""",
    subagent_type="Explore",
    model="haiku",
    run_in_background=True
)
```

## EXECUTION LOOP

```
1. Parse $ARGUMENTS -> MODIFIER, SPEC_PATH, FLAGS
2. Run session.py (MANDATORY FIRST)
   NOTE: session.py returns SESSION_DIR as a RELATIVE path (e.g., tmp/mux/20260209-1430-topic).
   ALL signal paths derived from {session} are RELATIVE to project root.
   NEVER prepend '/' — 'tmp/' is a project-local directory, NOT '/tmp/'.
3. mkdir -p {session}/.signals

PERMISSION_DENIED HANDLING (applies to ALL stages below):
  IF any subagent returns "PERMISSION_DENIED: Skill":
    STOP workflow. Report to user:
    "Background agents cannot surface permission prompts.
     Run Claude Code with --dangerously-skip-permissions
     or add Skill to allowed tools in .claude/settings.json"
    Do NOT retry. Do NOT launch new agents. The permission issue is session-wide.

CREATE (optional, all modes):
  Detection: IF SPEC_PATH does not resolve to existing file
             OR arguments contain "create spec" / "new spec" / "generate spec"
             OR first argument is "CREATE"
  IF CREATE detected:
    MUX MODE | Action: Task (CREATE) | Target: spec creation | Rationale: no existing spec
    Launch CREATE agent (opus, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read create.done
      IF status=success -> extract SPEC_PATH from metadata.path, proceed to next stage
      IF status=failed -> STAGE_FAILED, escalate to user

IF modifier == "full":
  GATHER:
    MUX MODE | Action: Task (gather) | Target: research | Rationale: parallel research
    Launch gather agent (opus, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read gather.done
      IF status=success -> proceed to CONSOLIDATE (MANDATORY - do NOT skip to PLAN)
      IF status=failed -> STAGE_FAILED, escalate to user

  CONSOLIDATE (MANDATORY after GATHER - do NOT skip):
    MUX MODE | Action: Task (consolidate) | Target: research synthesis | Rationale: gather complete
    Launch consolidate agent (opus, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read consolidate.done
      IF status=success -> proceed to CONFIRM SC (MANDATORY - do NOT skip to PLAN)
      IF status=failed -> STAGE_FAILED, escalate to user

CONFIRM SC (all modes - MANDATORY gate before PLAN - NEVER SKIP):
  **STOP. You MUST present SC to user and get approval before proceeding to PHASE_LOOP/PLAN.**
  Source determination:
    IF modifier == "full": source = {session}/research/consolidated.md
    ELSE (lean/leanest): source = {spec_path}

  MUX MODE | Action: Task (read SC) | Target: extract SUCCESS_CRITERIA | Rationale: prepare for user review
  Delegate Task(haiku/explore): read SUCCESS_CRITERIA section from source

  MUX MODE | Action: AskUserQuestion | Target: SC approval | Rationale: alignment gate before planning
  Present SC to user, options: Approve or Refine

  IF user selects Refine:
    Loop (max 3 iterations):
      Delegate SC update to Task(opus, bg)
      Re-extract SC summary
      Re-present to user
      IF approved -> break

  IF approved -> proceed to PHASE_LOOP

PHASE_LOOP (for each phase N):
  PLAN:
    MUX MODE | Action: Task (PLAN) | Target: Phase {N} PLAN | Rationale: next stage
    Launch PLAN agent (opus, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read phase-{N}-plan.done
      IF status=success -> proceed to REFINEMENT GATE
      IF status=failed -> launch NEW PLAN agent (fresh context)

  REFINEMENT GATE (after PLAN, before IMPLEMENT):
    Extract plan summary: delegate Task(haiku/explore) to run
      uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/extract-summary.py {plan-report}
    IF summary contains unresolved decisions OR user requested refinement:
      Present refinement questions via AskUserQuestion() using
        structured format from cookbook/refinement.md
      IF user approves -> proceed to IMPLEMENT
      IF user provides direction:
        Delegate plan update to FRESH Task(opus, bg)
        When task-notification arrives:
          Re-extract summary, re-present
        Loop until approved or max 3 iterations
    ELSE -> proceed to IMPLEMENT


  IMPLEMENT:
    MUX MODE | Action: Task (IMPLEMENT) | Target: Phase {N} IMPLEMENT | Rationale: plan done
    Launch IMPLEMENT agent (sonnet, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read phase-{N}-implement.done
      IF status=success -> proceed to REVIEW
      IF status=failed -> launch NEW IMPLEMENT agent (fresh context)

  REVIEW (cycle loop):
    MUX MODE | Action: Task (REVIEW) | Target: Phase {N} REVIEW cycle {C} | Rationale: impl done
    Launch REVIEW agent (opus, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read phase-{N}-review-{C}.done
      Parse grade from returned routing data
      IF grade=PASS -> proceed to TEST (or next phase)
      IF grade=WARN/FAIL + cycle < max:
        Launch FIX agent (sonnet, bg)
        When task-notification arrives:
          Delegate signal reading to Task(haiku/explore): read phase-{N}-fix-{C}.done
          Launch NEW REVIEW agent (fresh context, cycle C+1)
      IF grade=WARN/FAIL + cycle >= max -> STAGE_FAILED, escalate to user (ONLY PASS proceeds)

TEST:
  MUX MODE | Action: Task (TEST) | Target: test execution | Rationale: review passed
  Launch TEST agent (sonnet, bg)
  Print checkpoint
  Continue immediately
  When task-notification arrives:
    Delegate signal reading to Task(haiku/explore): read test.done
    IF grade=PASS -> proceed
    IF grade=WARN/FAIL -> STAGE_FAILED, escalate to user (ONLY PASS proceeds)

IF modifier != "leanest":
  DOCUMENT:
    MUX MODE | Action: Task (DOCUMENT) | Target: documentation | Rationale: tests passed
    Launch DOCUMENT agent (sonnet, bg)
    Print checkpoint
    Continue immediately
    When task-notification arrives:
      Delegate signal reading to Task(haiku/explore): read document.done
      IF status=success -> proceed
      IF status=failed -> escalate

SENTINEL (full) / SELF-VALIDATION (lean/leanest):
  MUX MODE | Action: Task (SENTINEL) | Target: final validation | Rationale: all stages done
  Launch SENTINEL agent (opus, bg)
  When task-notification arrives:
    Delegate signal reading to Task(haiku/explore): read sentinel.done
    IF grade=PASS -> WORKFLOW COMPLETE
    IF grade=WARN/FAIL -> STAGE_FAILED, escalate to user (ONLY PASS completes workflow)

CLEANUP:
  uv run deactivate.py
  Print final report
```

## CHECKPOINT PATTERN (after EVERY launch)

```
MUX MODE | Status: {STAGE} agent launched | Continuing immediately

{STAGE} stage for Phase {N} launched.

Checkpoint:
- Worker launched ({model}, background)
- Continuing immediately

Workflow Progress:
- CREATE: {COMPLETE|SKIPPED|IN_PROGRESS}
- GATHER: {COMPLETE|SKIPPED|IN_PROGRESS}
- CONSOLIDATE: {COMPLETE|SKIPPED|IN_PROGRESS} (full only)
- CONFIRM SC: {APPROVED|PENDING|IN_PROGRESS} (MANDATORY gate)
- PLAN: {COMPLETE|IN_PROGRESS|PENDING}
- IMPLEMENT: {COMPLETE|IN_PROGRESS|PENDING}
- REVIEW: {COMPLETE|IN_PROGRESS cycle {C}/{max}|PENDING}
- TEST: {COMPLETE|IN_PROGRESS|PENDING}
- DOCUMENT: {COMPLETE|IN_PROGRESS|PENDING|SKIPPED}
- SENTINEL: {COMPLETE|IN_PROGRESS|PENDING}

Waiting for task-notification.
```

---

# Report

## Progress Updates (MANDATORY)

### After EVERY Stage Completion

```
STAGE_{STAGE}_COMPLETE - {description}.

Stage Results:
- Signal: {signal_path}
- Commits: {hash} (if applicable)
- Duration: ~{N}min
- Key output: {brief summary}

Workflow Progress:
- CREATE: {state}
- GATHER: {state}
- CONSOLIDATE: {state}
- CONFIRM SC: {state}
- PLAN: {state}
- IMPLEMENT: {state}
- REVIEW: {state} (cycle {C}/{max})
- TEST: {state}
- DOCUMENT: {state}
- SENTINEL: {state}
```

### After Review Cycle

```
REVIEW cycle {C} grade: {PASS|WARN|FAIL}

Review Results:
- Compliance: {grade} ({N} gaps)
- Quality: {grade} ({N} issues)
- Action: {EARLY EXIT to TEST | FIX + re-review | ESCALATE to user}

Workflow Progress:
- REVIEW: cycle {C}/{max} - {grade}
```

### After WORKFLOW COMPLETE

```
WORKFLOW COMPLETE.

Final Status:
- CREATE: {COMPLETE|SKIPPED}
- GATHER: {COMPLETE|SKIPPED}
- CONSOLIDATE: {COMPLETE|SKIPPED}
- CONFIRM SC: APPROVED
- PLAN: COMPLETE (commit: {hash})
- IMPLEMENT: COMPLETE (commit: {hash})
- REVIEW: COMPLETE ({C} cycles, final grade: {grade})
- TEST: COMPLETE ({N} passing, {M} new)
- DOCUMENT: {COMPLETE|SKIPPED}
- SENTINEL: COMPLETE (grade: {grade})

Spec: {SPEC_PATH}
Session: {session}
Branch: {branch}
```

Then deactivate MUX session:
```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py
```

---

# Examples

## Example 1: Full Workflow Start

**Invocation:**
```
/mux-ospec full specs/2026/02/feat/001-feature.md
```

**Correct flow (what SHOULD happen):**
```
MUX MODE | Action: uv run session.py | Target: session init | Rationale: mandatory first action

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py 'mux-ospec-feature'")

MUX MODE | Action: Bash mkdir | Target: session dirs | Rationale: prepare signal directory

> Bash("mkdir -p {session}/.signals")

MUX MODE | Action: Task (GATHER) | Target: research | Rationale: full modifier requires GATHER

> Task(opus, bg) - GATHER research orchestrator

Checkpoint:
- Worker launched (opus, background)
- Continuing immediately

Workflow Progress:
- CREATE: SKIPPED
- GATHER: IN_PROGRESS
- CONSOLIDATE: PENDING
- CONFIRM SC: PENDING
- PLAN: PENDING
- IMPLEMENT: PENDING
- REVIEW: PENDING
- TEST: PENDING
- DOCUMENT: PENDING
- SENTINEL: PENDING

Waiting for task-notification.
```

**WRONG flow (what the failing session did):**
```
> Read(specs/2026/02/feat/001-feature.md)           <-- VIOLATION: reading spec yourself
> Bash("git branch --show-current")                   <-- VIOLATION: no session init
> Grep("function.*handler", path="src/")              <-- VIOLATION: searching codebase yourself
> Read(src/handler.ts)                                <-- VIOLATION: reading source files
> Skill(skill="spec", args="PLAN ...")                <-- VIOLATION: direct Skill() (must delegate via Task)
55s of churning, massive context consumed, no delegation, no signals, context died before IMPLEMENT.
```

**ALSO WRONG (bloated stage prompt):**
```
> Task(prompt="You are executing PLAN... ABSOLUTE CONSTRAINTS... 40 lines of instructions...")
                                                       <-- VIOLATION: stage prompt contains implementation knowledge
                                                       <-- Stage agent should ONLY invoke /spec PLAN, nothing else
```

## Example 2: PLAN Stage Launch (thin wrapper)

```
(GATHER complete, CONSOLIDATE complete, SC APPROVED by user)

MUX MODE | Action: Task (PLAN) | Target: Phase 1 PLAN | Rationale: SC approved

> Task(opus, bg) - prompt: "THINK VERY HARD; TAKE YOUR TIME.
>   Your FIRST and MANDATORY action: Skill(skill='spec', args='PLAN specs/.../001-feature.md')
>   DO NOT read files first. If Skill fails: RETURN STAGE_FAILED.
>   After Skill: verify commit + spec content. Signal + RETURN STAGE_PLAN_COMPLETE"

Checkpoint:
- Worker launched (opus, background)
- Continuing immediately

Workflow Progress:
- GATHER: COMPLETE
- CONSOLIDATE: COMPLETE
- CONFIRM SC: APPROVED
- PLAN: IN_PROGRESS
- IMPLEMENT: PENDING
- REVIEW: PENDING
- TEST: PENDING
- DOCUMENT: PENDING
- SENTINEL: PENDING

Waiting for task-notification.
```

## Example 3: Stage Completion + Next Stage

```
(task-notification: PLAN worker returned 0)

MUX MODE | Action: Task (signal reader) | Target: read PLAN signal | Rationale: get routing data

> Task(haiku/explore) - "Read {session}/.signals/phase-1-plan.done (RELATIVE path from project root, do NOT prepend '/'). Return routing data only."

(haiku returns: status=success, commit=a1b2c3d)

STAGE_PLAN_COMPLETE confirmed. Launching IMPLEMENT.

MUX MODE | Action: Task (IMPLEMENT) | Target: Phase 1 IMPLEMENT | Rationale: PLAN confirmed

> Task(sonnet, bg) - prompt: "THINK VERY HARD; TAKE YOUR TIME.
>   Your FIRST and MANDATORY action: Skill(skill='spec', args='IMPLEMENT specs/.../001-feature.md')
>   DO NOT read spec first. If Skill fails: RETURN STAGE_FAILED.
>   After Skill: verify commit + type check + tests. Signal + RETURN STAGE_IMPLEMENT_COMPLETE"

Checkpoint:
- Worker launched (sonnet, background)
- Continuing immediately

Workflow Progress:
- GATHER: COMPLETE
- CONSOLIDATE: COMPLETE
- CONFIRM SC: APPROVED
- PLAN: COMPLETE (commit: a1b2c3d)
- IMPLEMENT: IN_PROGRESS
- REVIEW: PENDING
- TEST: PENDING
- DOCUMENT: PENDING
- SENTINEL: PENDING

Waiting for task-notification.
```

## Example 4: Review Cycle with Fix (refinement loop)

```
(task-notification: REVIEW worker returned 0)

MUX MODE | Action: Task (signal reader) | Target: read REVIEW signal | Rationale: get routing data

> Task(haiku/explore) returns: status=success, grade=WARN

REVIEW grade=WARN. Cycle 1/3. Launching FIX.

MUX MODE | Action: Task (FIX) | Target: Phase 1 FIX cycle 1 | Rationale: grade=WARN

> Task(sonnet, bg) - prompt: "THINK VERY HARD; TAKE YOUR TIME.
>   Your FIRST and MANDATORY action: Skill(skill='spec', args='FIX specs/.../001-feature.md')
>   ENHANCEMENT: Also read agents/spec-fixer.md for fix protocol.
>   REVIEW REPORT: {session}/reviews/phase-1-review-1.md
>   If Skill fails: RETURN STAGE_FAILED. Signal + RETURN STAGE_FIX_COMPLETE"

(task-notification: FIX worker returned 0)

MUX MODE | Action: Task (signal reader) | Target: read FIX signal | Rationale: confirm fix

> Task(haiku/explore) returns: status=success, commit=b2c3d4e

MUX MODE | Action: Task (REVIEW) | Target: Phase 1 REVIEW cycle 2 | Rationale: fix confirmed

> NEW Task(opus, bg) - FRESH review agent (Skill(spec, REVIEW))

(task-notification: REVIEW worker returned 0)

> Task(haiku/explore) returns: status=success, grade=PASS

Grade=PASS -> proceed to TEST
```

## Example 5: STAGE_FAILED + Relaunch

```
(task-notification: IMPLEMENT worker returned non-zero)

IMPLEMENT STAGE_FAILED - Skill(spec) invocation failed. Error: spec file not found.

MUX MODE | Action: AskUserQuestion | Target: user decision | Rationale: STAGE_FAILED requires escalation

> AskUserQuestion: "IMPLEMENT failed: spec file not found at {path}. Options: 1) Fix path and retry, 2) Abort workflow"

(user provides corrected path)

MUX MODE | Action: Task (IMPLEMENT) | Target: Phase 1 IMPLEMENT retry | Rationale: user corrected path

> NEW Task(sonnet, bg) - FRESH implement agent (never resume failed one)

Checkpoint:
- Worker launched (sonnet, background) - FRESH agent
- Continuing immediately
```

## Example 6: Full Workflow Completion

```
WORKFLOW COMPLETE.

Final Status:
- CREATE: SKIPPED
- GATHER: COMPLETE
- CONSOLIDATE: COMPLETE
- CONFIRM SC: APPROVED
- PLAN: COMPLETE (commit: a1b2c3d)
- IMPLEMENT: COMPLETE (commit: e4f5g6h)
- REVIEW: COMPLETE (2 cycles, final grade: PASS)
- TEST: COMPLETE (47 passing, +12 new)
- DOCUMENT: COMPLETE (commit: i7j8k9l)
- SENTINEL: COMPLETE (grade: PASS)

Spec: specs/2026/02/feat/001-feature.md
Session: tmp/mux/20260207-1430-feature/
Branch: feat/001-feature

MUX MODE | Action: uv run deactivate.py | Target: cleanup | Rationale: workflow complete

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py")
```

---

# BEGIN

Parse `$ARGUMENTS` now.

**Your FIRST action MUST be:** `Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py 'mux-ospec-{topic}'")`

Do NOT read any files first. Do NOT run git commands. Do NOT analyze anything. Do NOT read the spec. Run session.py FIRST, then follow the EXECUTION LOOP above.
