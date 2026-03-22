---
name: mux-roadmap
description: "Multi-track roadmap orchestration via MUX skill with file-based state management for cross-session continuity. Triggers on keywords: mux roadmap, roadmap, orchestrate roadmap, multi-track"
project-agnostic: true
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Skill
  - AskUserQuestion
  - mcp__voicemode__converse
---

# MUX Roadmap Orchestrator

# Purpose

Multi-track roadmap orchestration via MUX skill with file-based state management for cross-session continuity.

- Invokes MUX skill as FIRST action (mandatory - activates session + enforcement hooks)
- Delegates ALL understanding, scoping, and decomposition to high-tier subagents (orchestrator NEVER reads spec/source files)
- Executes phases sequentially within tracks via mux-ospec (task-notification pattern)
- Maintains CONTINUE.md as single source of truth for cross-session resume
- Uses YAML signal files for granular phase/track state tracking
- Provides mandatory progress updates after every phase and track completion
- Post-track lifecycle: High-tier Fixer -> Sentinel E2E -> QA Gate
- Built-in QA gate as spec-driven phases with threshold escalation (80%+ initial, 90%+ re-execution)

**Invocation:** `/mux-roadmap <PATH> [MODE] [FLAGS]`

**Modes:**
- `start` - New session. PATH = roadmap/spec file. Decomposes, confirms, executes.
- `continue` - Resume session. PATH = existing CONTINUE.md file. Reads state, confirms, resumes.

---

# Variables

## From $ARGUMENTS

Parse `$ARGUMENTS` as: `<PATH> [MODE] [FLAGS]`

- `PATH` - Required. In `start` mode: path to roadmap/spec file. In `continue` mode: path to session CONTINUE.md.
- `MODE` - Optional. Default: `start`. Either `start` or `continue`. If PATH ends with `CONTINUE.md`, auto-detect `continue`.
- `FLAGS` - Optional:
  - `--wait-after-plan` - Wait for user confirmation after each PLAN stage before proceeding to IMPLEMENT. Default: autonomous (proceed through all stages without waiting).

---

# Instructions

## FIRST ACTION (MANDATORY - ZERO EXCEPTIONS)

Your ABSOLUTE FIRST action, before reading any file, running any command, or analyzing anything:

```
Skill(skill="mux", args="Orchestrate multi-track roadmap. PATH: <PATH>. Mode: <MODE>. Follow roadmap orchestration protocol from loaded prompt context. Delegate ALL spec reading and decomposition to high-tier subagent. Execute phases via mux-ospec.")
```

This triggers:
1. MUX SKILL.md loads (session init, forbidden tools, preamble ritual, hook enforcement)
2. `uv run tools/session.py "<roadmap-slug>"` creates session + activates hooks
3. Read, Write, Edit, Grep, Glob, WebSearch are now **BLOCKED** by hooks
4. You are forced to DELEGATE everything via Task()

**IF YOU SKIP THIS:** You will read files yourself, eat context, and fail. The failing session proves this.

## After MUX Session Initializes

MUX rules are now active (loaded via Skill(mux)). All MUX protocol rules apply without exception.

**Additional mux-roadmap rules:**
- `--wait-after-plan`: When set, after each phase's PLAN stage completes, pause and present the plan summary to the user via AskUserQuestion before proceeding to IMPLEMENT. Default behavior (no flag) is fully autonomous.

Then follow the mode-specific workflow below.

---

## Mode: `start`

### Step 0: Delegate Decomposition (MANDATORY - DO NOT DO THIS YOURSELF)

Launch a **Strategy Analyst** agent (high-tier, background) to:
1. Read the roadmap spec
2. Identify tracks, phases, dependencies (DAG)
3. Auto-detect project toolchain (type check, test commands)
4. If per-phase spec files do NOT exist: create them from the monolithic spec
5. Return a structured decomposition summary

Use the Strategy Analyst Prompt from the Workflows section below.

**YOU DO NOT READ THE SPEC.** You receive ONLY the summary from the agent.

After the Strategy Analyst returns, present the decomposition to the user:

```
## Decomposition

**Roadmap:** <PATH>
**Branch:** <detected-branch>
**Modifier:** <detected-modifier>
**Type Check:** <detected-cmd>
**Test:** <detected-cmd>
**Session:** <SESSION_DIR>

### Tracks & Phases

**Track A - <title>** (N phases)
| Order | Phase | Spec Path | Depends On |
|-------|-------|-----------|------------|
| 1 | NNN | <path> | - |
| 2 | NNN | <path> | Phase NNN |

**Track B - <title>** (M phases)
| Order | Phase | Spec Path | Depends On |
|-------|-------|-----------|------------|
| 1 | NNN | <path> | Track A |

### Dependency DAG

Track A --> Track B --> Track C

### Execution Plan

- Sequential within tracks
- Track dependencies enforced
- Independent tracks can run in parallel

Confirm this decomposition before I proceed?
```

Wait for user confirmation via AskUserQuestion. Do NOT proceed without it.

### Step 1: Initialize Session Directory

After user confirms:

```bash
mkdir -p tmp/mux/<session-slug>/signals
mkdir -p tmp/mux/<session-slug>/signals/refinements
# One per track:
mkdir -p tmp/mux/<session-slug>/track-a/signals
mkdir -p tmp/mux/<session-slug>/track-a/refinements
# ... repeat for each track
```

Delegate CONTINUE.md creation to a Task(medium-tier) writer agent using the template from the Report section.

### Step 2: Execute Phases

Follow the Execution Loop from the Workflows section.

---

## Mode: `continue`

### Step 0: Delegate State Reading

Launch an **Explore agent** (low-tier, background) to:
1. Read CONTINUE.md at PATH
2. Read all signal files in the session directory
3. Return: current state summary, pending refinements, next action

**YOU DO NOT READ CONTINUE.md YOURSELF.** You receive the summary.

Present resume state to user:

```
## Resume State

**Session:** <session-dir>
**Branch:** <BRANCH>
**Last Updated:** <timestamp>

### Current Progress

- Track A: <state> (<X>/<Y>)
- Track B: <state> (<X>/<Y>)

### Pending Refinements

<list or "None">

### Next Action

<from CONTINUE.md>

Confirm resume?
```

Wait for user confirmation. If any track is `NEEDS_REFINEMENT`, surface refinement to user FIRST.

### Step 1: Resume Execution

Follow the Execution Loop from the Workflows section, starting from the next pending phase.

---

# Workflows

## Architecture

```
YOU (MUX Head Coordinator - high-tier)
 |
 |  CONSTRAINTS:
 |  - MUX hooks BLOCK Read/Write/Edit/Grep/Glob/WebSearch
 |  - Preamble ritual before every action
 |  - EVERY action via Task(run_in_background=True)
 |  - Continue immediately (never block)
 |
 +- [START ONLY] Strategy Analyst (high-tier, bg)
 |   +- Reads spec, identifies tracks/phases/DAG
 |   +- Creates per-phase specs if needed
 |   +- Auto-detects toolchain
 |   +- Returns decomposition summary
 |
 +- PER PHASE: Orchestrator invokes Skill(skill="mux-ospec", args="<modifier> <spec-path>") DIRECTLY
 |   |
 |   |  Orchestrator loads mux-ospec into its own context, then delegates stages:
 |   |  GATHER -> CONFIRM SC -> PLAN -> IMPLEMENT -> REVIEW -> FIX -> TEST -> DOCUMENT -> SENTINEL
 |   |  Each stage via Task() subagent as mux-ospec instructs
 |   |
 |   +- mux-ospec stages return completion -> Orchestrator continues to next stage
 |   +- Stage returns NEEDS_REFINEMENT -> Orchestrator resolves or escalates
 |   +- Stage returns FAILED -> Orchestrator delegates investigation + fix
 |
 +- [If NEEDS_REFINEMENT]:
 |   +- Task(high-tier, bg) -> Refinement Resolver
 |   +- Within authority -> resolve autonomously, proceed to next stage
 |   +- Outside authority -> AskUserQuestion, delegate update, proceed
 |
 +- After each phase: delegate CONTINUE.md update + print progress
 |
 +- After track completes:
 |   +- High-tier Fixer (high-tier, bg) -> fix TS/runtime errors
 |   +- Sentinel E2E Self-Healing Loop
 |   |   +- S1: Test Case Writers (high-tier x N, parallel)
 |   |   +- S1.5: Test Case Consolidation (medium-tier, dedup)
 |   |   +- S2: Test Executor (low-tier, sequential, batched if >100 cases)
 |   |   +- S3: Report Auditor (medium-tier)
 |   |   +- S4: Consolidator (medium-tier)
 |   |   +- Self-Remediation Loop (max 10 cycles, full S2 re-run after deep fixes)
 |   +- QA Gate (after ALL tracks complete) — spec-driven phases
 |       +- Spec N: QA Test Case Creation (via /spec CREATE + PLAN + IMPLEMENT)
 |       +- Spec N+1: QA Execution (via /spec + Playwright, live bug fixing)
 |       +- GO/NO-GO Verdict (80%+ initial, 90%+ re-execution threshold)
 |       +- [If NO-GO] Spec N+2: P0 Fix + Spec N+3: Re-execution
```

## Strategy Analyst Prompt

For `start` mode, launch this agent to decompose the roadmap spec. This agent does ALL the reading so the orchestrator preserves context.

````python
Task(
    prompt=f"""You are the Strategy Analyst for a multi-track roadmap orchestration.

## YOUR TASK

Read the roadmap spec and produce a structured decomposition.

SPEC PATH: {spec_path}
PROJECT ROOT: {project_root}

## EXECUTION

1. Read the roadmap spec file at SPEC PATH
2. Identify all logical TRACKS (groupings of related work)
3. Within each track, identify PHASES (sequential implementation units)
4. Map the dependency DAG (which tracks/phases block which)
5. Auto-detect project toolchain:
   - Look for package.json -> determine test cmd + type check
   - Look for pyproject.toml -> determine test cmd (pytest) + type check (pyright)
   - Check current git branch: git branch --show-current
6. Check if per-phase spec files already exist in the spec directory
7. If per-phase specs do NOT exist:
   - Create them from the monolithic spec
   - Each phase spec should contain ONLY the relevant section
   - Follow the project's spec file naming convention
   - Path pattern: <spec-dir>/phase-NNN-<slug>.md

## OUTPUT

Write your decomposition to: {session_dir}/decomposition.md

Format:
```yaml
branch: "<detected-branch>"
modifier: "full"
type_check_cmd: "<detected>"
test_cmd: "<detected>"
tracks:
  - letter: A
    title: "<track title>"
    phases:
      - number: "001"
        title: "<phase title>"
        spec_path: "<path to per-phase spec>"
        depends_on: []
      - number: "002"
        title: "<phase title>"
        spec_path: "<path>"
        depends_on: ["001"]
  - letter: B
    title: "<track title>"
    phases:
      - number: "003"
        title: "<phase title>"
        spec_path: "<path>"
        depends_on: ["Track A"]
dag: "Track A --> Track B --> Track C"
notes: "<any important observations>"
specs_created: true/false
specs_created_list:
  - "<path1>"
  - "<path2>"
```

Signal when done:
```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/signal.py {session_dir}/.signals/decomposition.done --status success --meta path={session_dir}/decomposition.md
```

CRITICAL:
- Be thorough in reading the spec - identify ALL phases, not just obvious ones
- Respect the spec's own phase numbering if it has one
- Create MINIMAL per-phase specs (just the relevant section, not the whole doc)
- Auto-detect toolchain from project files, do not guess

FINAL: Return EXACTLY: done""",
    subagent_type="general-purpose",
    model="high-tier",
    run_in_background=True
)
````

After the Strategy Analyst signals done, delegate reading the decomposition summary to a low-tier agent (do NOT read it yourself):

```python
Task(
    prompt=f"Read {session_dir}/decomposition.md and return its FULL content.",
    subagent_type="Explore",
    model="low-tier"
)
```

Parse the YAML summary, present to user, confirm.

## Phase Execution Pattern (v4 - ORCHESTRATOR INVOKES mux-ospec)

For EVERY phase, the ORCHESTRATOR (not a phase agent) invokes mux-ospec directly:

```
# Orchestrator action:
Skill(skill="mux-ospec", args="{modifier} {spec_path}")
```

This loads the mux-ospec workflow into the orchestrator's context. The orchestrator then delegates each stage (GATHER, PLAN, IMPLEMENT, REVIEW, TEST, etc.) via Task() subagents as mux-ospec instructs.

**Architecture (CORRECT - 2 levels):**
```
Orchestrator -> Skill(mux-ospec) directly -> Task(stage workers)
```

**Architecture (BROKEN - 3 levels):**
```
Orchestrator -> Task(Phase Agent) -> Skill(mux-ospec) -> Task(stage workers)
```

At depth 3, Skill() invocation fails or the phase agent implements directly instead of invoking the skill.

## MANDATORY VERIFICATION (after mux-ospec stages complete)

Run these checks IN ORDER. If ANY fails, escalate via refinement:

1. PLAN commit exists:
   git log --oneline -10 | grep "spec({NNN}): PLAN"
   If missing: Write refinement doc, escalate

2. Spec file has content:
   {spec_path} must have >50 lines in AI Section
   If empty/missing: Write refinement doc, escalate

3. IMPLEMENT commit exists:
   git log --online -10 | grep -E "(feat|fix|refactor)\("
   If missing: Write refinement doc, escalate

4. Type check passes:
   {type_check_cmd}
   If errors: attempt fix (up to 3 tries), then refinement

5. Tests pass:
   {test_cmd}
   If failures: attempt fix (up to 3 tries), then refinement

## SIGNAL

Write signal file at:
  {session_dir}/track-{x}/signals/phase-{NNN}.signal

Format:
  phase: "{NNN}"
  title: "{phase-title}"
  spec_path: "{spec_path}"
  state: PHASE_COMPLETE
  stage: DONE
  stage_status: DONE
  commit: "<latest-hash>"
  updated_at: "<ISO timestamp>"
  error: ""
  refinement_ref: ""

## COMPLETION

Phase complete. Update CONTINUE.md, proceed to next phase.

## FAILURE

Write refinement doc at:
  {session_dir}/track-{x}/refinements/phase-{NNN}-refinement.md
Escalate or resolve autonomously.

## Post-Track Lifecycle

After each track completes all phases, execute this pipeline before moving to the next track.

### High-tier Fixer

Triggered after each track completes. Performs a comprehensive TS/runtime error sweep.

```python
Task(
    prompt=f"""You are the High-tier Fixer for Track {track_letter}.

## TASK

Read ALL new/modified files from this track's phases. Run {type_check_cmd}. Fix ALL type errors and runtime issues.

## EXECUTION

1. git diff --name-only {track_start_commit}..HEAD -- find all changed files
2. Run {type_check_cmd}
3. Fix ALL errors (type errors, missing imports, broken references)
4. Run {test_cmd} -- verify no regressions
5. Repeat until: 0 type errors AND all tests green

## COMMIT

If fixes applied:
  git add <fixed-files> && git commit -m "fix(track-{track_letter}): resolve type/runtime errors"

## COMPLETION

Return EXACTLY: HIGH_TIER_FIXER_COMPLETE with summary of fixes (or NO_FIXES_NEEDED)""",
    subagent_type="general-purpose",
    model="high-tier",
    run_in_background=True
)
```

Must pass: 0 type errors, all tests green.

### Sentinel E2E Self-Healing Loop

Full end-to-end test pipeline with self-remediation.

#### S1 -- Test Case Writers (parallel high-tier agents)

```python
# Launch N writers in parallel, one per logical feature area
Task(
    prompt=f"""You are Sentinel S1 - Test Case Writer for Track {track_letter}.

## TASK

Read all specs from completed phases. Read all new source files. Write natural-language test cases covering EVERY new capability.

## EXECUTION

1. Read all phase specs: {spec_paths}
2. Read all new/modified source files (git diff --name-only {track_start_commit}..HEAD)
3. Write test cases in natural language:
   - One test case per capability/interaction
   - Include: preconditions, steps, expected result
   - Cover: happy path, error states, edge cases, keyboard interactions
4. Output: {session_dir}/sentinel/test-cases.md

## FORMAT

### TC-001: <Title>
**Preconditions:** <setup required>
**Steps:**
1. <action>
2. <action>
**Expected:** <observable result>
**Priority:** P0|P1|P2

FINAL: Return EXACTLY: S1_COMPLETE with test case count""",
    subagent_type="general-purpose",
    model="high-tier",
    run_in_background=True
)
```

#### S1.5 -- Test Case Consolidation (medium-tier)

After S1 completes, deduplicate and consolidate raw test cases before S2 execution. Without this step, S2 wastes tokens on redundant tests.

```python
Task(
    prompt=f"""You are Sentinel S1.5 - Test Case Consolidator for Track {track_letter}.

## TASK

Deduplicate and consolidate raw test cases from S1 writers. Multiple writers produce overlapping cases.

## EXECUTION

1. Read {session_dir}/sentinel/test-cases.md
2. Identify duplicate and overlapping test cases
3. Merge cases that test the same capability into single comprehensive cases
4. Remove redundant precondition setups
5. Preserve all unique edge cases and error states
6. Re-number consolidated cases sequentially (TC-001, TC-002, ...)
7. Overwrite {session_dir}/sentinel/test-cases.md with consolidated version

## OUTPUT

Report: original count, consolidated count, reduction percentage.

FINAL: Return EXACTLY: S1_5_COMPLETE with counts (e.g., "364 -> 160, 56% reduction")""",
    subagent_type="general-purpose",
    model="medium-tier",
    run_in_background=True
)
```

#### S2 -- Test Executor (low-tier, sequential)

```python
Task(
    prompt=f"""You are Sentinel S2 - Test Executor for Track {track_letter}.

## TASK

Execute ALL test cases from {session_dir}/sentinel/test-cases.md via real browser interactions.

## EXECUTION

1. Read {session_dir}/sentinel/test-cases.md
2. Start dev server: {dev_server_cmd}
3. Open Playwright browser: navigate to http://localhost:{dev_port}
4. FIRST STEP (MANDATORY): Programmatic app init via browser_evaluate
   - Use {programmatic_app_init} to set up required app state
   - This MUST happen before any content-dependent test
   - If programmatic init is non-trivial, produce a reusable guide at:
     {session_dir}/sentinel/e2e-setup-guide.md (created on first S2 run, reused on retries)
5. Execute each test case AS A HUMAN WOULD:
   - Click, type, navigate, verify visually
   - NO shortcuts - interact through the UI
6. Collect evidence per test:
   - Screenshot (before/after)
   - Console logs
   - Network requests (if relevant)
7. Mark each: PASS / FAIL / PARTIAL (with reason)

## OUTPUT

Write: {session_dir}/sentinel/test-execution-report.md

### TC-001: <Title>
**Result:** PASS|FAIL|PARTIAL
**Evidence:** <screenshot filename>
**Console:** <errors if any>
**Notes:** <observations>

## IMPORTANT

- ALWAYS specify dev server: {dev_server_cmd} at http://localhost:{dev_port}
- Use low-tier model. Escalate to medium-tier only for ambiguous test cases.
- NEVER use high-tier for execution.
- Use Skill(skill="playwright-cli") for browser automation — NOT raw MCP playwright tools.
- Use Skill(skill="test-e2e") for structured test execution.
- NEVER call browser_snapshot, browser_click, browser_evaluate MCP tools directly (causes context exhaustion).
- playwright-cli uses Bash commands (e.g., `playwright-cli snapshot`, `playwright-cli click`) — far more token-efficient.

FINAL: Return EXACTLY: S2_COMPLETE with pass/fail/partial counts""",
    subagent_type="general-purpose",
    model="low-tier",
    run_in_background=True
)
```

#### S3 -- Report Auditor (medium-tier)

```python
Task(
    prompt=f"""You are Sentinel S3 - Report Auditor for Track {track_letter}.

## TASK

Cross-reference test execution report against test cases. Flag discrepancies.

## EXECUTION

1. Read {session_dir}/sentinel/test-cases.md
2. Read {session_dir}/sentinel/test-execution-report.md
3. Flag:
   - Missed tests (in cases but not executed)
   - Overstated passes (marked PASS but evidence shows issues)
   - False negatives (marked FAIL but might be environment issue)
   - Undertested areas (capability not covered by any test)

## OUTPUT

Write: {session_dir}/sentinel/audit-corrections.md

FINAL: Return EXACTLY: S3_COMPLETE with correction count""",
    subagent_type="general-purpose",
    model="medium-tier",
    run_in_background=True
)
```

#### S4 -- Consolidator (medium-tier)

```python
Task(
    prompt=f"""You are Sentinel S4 - Consolidator for Track {track_letter}.

## TASK

Produce a prioritized, deduplicated fix list from audit corrections and test failures.

## EXECUTION

1. Read {session_dir}/sentinel/test-execution-report.md
2. Read {session_dir}/sentinel/audit-corrections.md
3. Merge, deduplicate, prioritize:
   - P0: Blocking failures (crashes, data loss, broken core flows)
   - P1: Degraded experience (visual glitches, slow, wrong but functional)
   - P2: Polish (minor UI, edge cases)

## OUTPUT

Write: {session_dir}/sentinel/fixes-and-refinements.md

FINAL: Return EXACTLY: S4_COMPLETE with fix count by priority""",
    subagent_type="general-purpose",
    model="medium-tier",
    run_in_background=True
)
```

#### Self-Remediation Loop (max 10 cycles)

After S4 produces the fix list, enter the self-healing loop:

```
FOR cycle = 1 to 10:
  1. Diagnostician (high-tier, bg)
     - Read fixes-and-refinements.md
     - Read relevant source files
     - Produce fix-report-cycle-{N}.md with root cause + fix instructions

  2. Implementer (high-tier, bg)
     - Read fix report
     - Apply fixes
     - Run {type_check_cmd} + {test_cmd}
     - Commit: fix(sentinel-{track}): cycle {N} - <summary>

  3. Re-runner (high-tier, bg)
     - Re-execute ONLY FAILED test cases via Playwright
     - EXCEPTION: If Implementer modified architectural components (providers, layouts,
       state management, routing), re-run FULL S2 (not just failed tests) — deep fixes
       can cause regressions in previously passing tests
     - Update test-execution-report.md with new results

  EXIT CONDITIONS:
  - ALL test cases PASS -> SENTINEL_COMPLETE
  - No improvement for 2 consecutive cycles -> ESCALATE to user with full evidence

  Classify remaining failures:
  - FIXED -- resolved, verified via E2E
  - KNOWN_LIMITATION -- investigated N cycles, root cause identified but not fixable
    (e.g., third-party library internal event handling race)
  - ENVIRONMENT_LIMITATION -- headless browser or test environment constraint, not a real bug
END FOR
```

### QA Gate (Built-In, After ALL Tracks)

Triggered automatically after all tracks + sentinels complete. This is the final production readiness check.

**QA is implemented as formal spec-driven phases**, each following the full GATHER/PLAN/IMPLEMENT/REVIEW/TEST lifecycle with commit discipline:

```
Spec N:   QA Test Case Creation (CREATE + PLAN + IMPLEMENT)
Spec N+1: QA Execution (IMPLEMENT via Playwright)
[If NO-GO]:
Spec N+2: P0 Fix (fix all P0 blockers)
Spec N+3: QA Re-execution (re-run with raised threshold)
```

#### 1. QA Test Case Creation (Spec N)

Spec-driven via `/spec CREATE + PLAN + IMPLEMENT + REVIEW + TEST`:

- Write ALL core test cases any user (beginner/mid/expert) would trigger
- Plain language, simple steps, markdown files
- Organized by category:
  - P0: Blocking (crashes, data loss, broken core flows)
  - P1: Experience (visual, performance, usability)
  - P2: Nice-to-have (edge cases, polish)
  - Keyboard collisions
  - Critical user flows
  - Visual quality
- Pass/fail criteria in each file
- Commit: `spec(N): IMPLEMENT - qa-test-case-creation`

#### 2. QA Execution (Spec N+1)

E2E via Playwright:

- Execute all test cases via browser interactions
- Collect evidence per test (screenshots, console, network)
- **Live bug fixing during execution**: when bugs are found during test execution, fix and commit immediately (do not defer). Reference commit hashes in the execution report.
- Output: execution report with pass/fail/skip counts
- Commit: `spec(N+1): IMPLEMENT - qa-execution`

#### 3. GO/NO-GO Verdict

- Initial threshold: **80%+ pass rate = GO**
- **Threshold escalation**: for re-execution rounds after P0 fixes, threshold may be raised to **90%+** to ensure fixes didn't introduce regressions
- Any **P0 failure = automatic NO-GO** regardless of pass rate
- Skip justified ONLY by environment limitations (headless browser constraints)

#### 4. P0 Fix Loop (if NO-GO) — Spec N+2, N+3

Each fix-and-retest cycle is a formal spec:

```
WHILE verdict == NO-GO:
  Spec N+2: Fix all P0 blocking failures
    - Commit: spec(N+2): IMPLEMENT - qa-p0-fixes
  Spec N+3: Re-execute (raised threshold: 90%+)
    - Re-execute affected categories AND regression sweep
    - Commit: spec(N+3): IMPLEMENT - qa-re-execution
  Re-evaluate verdict
  EXIT: GO verdict OR escalate to user (unfixable P0)
END WHILE
```

## Execution Loop

```
FOR each track in dependency order:
  MUX MODE | Action: Bash mkdir -p | Target: track-{x} dirs | Rationale: prepare signal/refinement dirs

  FOR each phase in track (sequential):
    MUX MODE | Action: Skill(mux-ospec) | Target: Phase {NNN} | Rationale: load ospec workflow for this phase

    1. Orchestrator invokes: Skill(skill="mux-ospec", args="{modifier} {spec_path}")
    2. mux-ospec loads into orchestrator context, delegates stages via Task():
       - GATHER -> Task(medium-tier, bg)
       - PLAN -> Task(medium-tier, bg)
       - IMPLEMENT -> Task(medium-tier, bg)
       - REVIEW/TEST -> Task(medium-tier, bg)
    3. Print checkpoint after each stage:
       Checkpoint:
       - Stage {STAGE} launched (background)
       - Continuing immediately
    4. Continue immediately (DO NOT block)
    5. When stage notification arrives:
       IF STAGE_COMPLETE:
         a. Delegate CONTINUE.md update to Task(medium-tier)
         b. Print progress update (see Report section)
         c. Proceed to next stage or next phase if all stages done
       IF NEEDS_REFINEMENT:
         a. Delegate reading refinement doc to Task(low-tier/explore)
         b. Within authority -> delegate spec update, retry stage
         c. Outside authority -> AskUserQuestion, delegate update, retry stage
       IF FAILED:
         a. Delegate investigation via Task(high-tier)
         b. Delegate fix via Task(medium-tier)
         c. Retry stage (never skip)
    6. If no task-notification after extended time:
       a. Run verify.py to check worker status
       b. If worker stuck, mark FAILED, launch fresh agent
       c. If worker still active, continue waiting
    7. If --wait-after-plan flag set:
       After PLAN stage completes, present plan summary via AskUserQuestion
       Wait for user confirmation before IMPLEMENT
  END FOR

  Post-track pipeline:
    a. High-tier Fixer for track TS/runtime sweep
    b. Sentinel E2E Self-Healing Loop (S1 -> S1.5 consolidation -> S2 -> S3 -> S4 -> remediation)
    c. Delegate CONTINUE.md update with track results

  Delegate track status update -> COMPLETED
  Print track completion update
END FOR

All tracks complete:
  1. High-tier Fixer for final TS/runtime sweep across ALL tracks
  2. Final Sentinel E2E across ALL tracks
  3. QA Gate (test case creation + execution + verdict)
  4. IF GO: print ROADMAP COMPLETE + deactivate MUX session
  5. IF NO-GO: P0 Fix Loop until GO or ESCALATE to user
```

## Checkpoint Pattern (after EVERY launch)

```
MUX MODE | Status: Phase {NNN} agent launched | Continuing immediately

Track {X} Phase {NNN} ({Title}) launched.

Checkpoint:
- Worker launched (high-tier, background)
- Continuing immediately

Overall Progress:
- Track A: COMPLETE ({P}/{P})
- Track B: IN_PROGRESS ({X}/{Y} - Phase {NNN} running)
- Track C: NOT_STARTED (blocked by Track B)

Waiting for notifications.
```

## Refinement Flow

```
Phase Agent returns NEEDS_REFINEMENT
  |
  v
Delegate reading refinement doc to Task(low-tier/explore)
  |
  v
Within authority (impl approach, API, tests, naming, perf)?
  |
  YES -> Resolve autonomously:
  |      1. Delegate spec update via Task(medium-tier, bg)
  |      2. Update phase signal -> {STAGE}_PENDING
  |      3. Launch NEW phase agent (fresh context)
  |
  NO -> Escalate:
         1. AskUserQuestion with options from refinement doc
         2. Delegate spec update via Task(medium-tier, bg)
         3. Update phase signal -> {STAGE}_PENDING
         4. Launch NEW phase agent (fresh context)
```

**Autonomous authority** (resolve without user):
- Implementation approach, API design, state management, test strategy
- Naming, error handling, file organization, performance optimization

**Must escalate** (AskUserQuestion required):
- Removing/deprioritizing phases
- Changing UX philosophy or scope
- Adding significant scope beyond spec
- Cross-track trade-offs that alter the roadmap

## Cross-Session Resume

```
Session N (context running low)
  |
  +-- PROACTIVELY delegate CONTINUE.md update
  +-- All signal files reflect current reality
  +-- Session ends naturally

User starts Session N+1
  |
  +-- /mux-roadmap tmp/mux/<session>/CONTINUE.md continue
  +-- MUX initializes, reads state via delegate
  +-- Confirms with user
  +-- Picks up from exact point of interruption
```

Update CONTINUE.md PROACTIVELY when:
- 3+ phase state changes processed
- Before delegating large batch of work
- When context limits may be approaching
- Before any user interaction

Authority when CONTINUE.md and signals disagree:
1. Signal files = ground truth for individual phase/track state
2. CONTINUE.md = ground truth for orchestration intent (what to do next)
3. If in doubt: delegate re-reading all signals, reconstruct CONTINUE.md

## Error Recovery

| Scenario | Action |
|----------|--------|
| Phase agent timeout | If no task-notification after extended time, run verify.py. If worker stuck, mark FAILED, launch fresh agent |
| Worker truly stuck | Mark stage FAILED, launch new phase agent |
| mux-ospec internal failure | Phase agent writes refinement, returns NEEDS_REFINEMENT |
| Type check fails 3x | NEEDS_REFINEMENT with error details |
| Tests fail 3x | NEEDS_REFINEMENT with failure analysis |
| Context exhaustion | Delegate CONTINUE.md update proactively, session ends, user resumes |
| Refinement unanswered | Stays NEEDS_REFINEMENT until next session |
| Sentinel S2 app crash | Launch high-tier Diagnostician, fix root causes, retry S2 |
| Sentinel no improvement 2 cycles | ESCALATE to user with full evidence |
| QA NO-GO verdict | Enter P0 Fix Loop, re-execute affected categories |
| QA P0 unfixable | Classify as KNOWN_LIMITATION, document, escalate for scope decision |
| S2 context exhaustion (>100 cases) | Enable batching: 50-80 cases per batch, preserve partial results |
| Deep fix causes new regressions | Full S2 re-run (not just failed tests) after architectural changes |
| Live bug found during QA execution | Fix and commit immediately, reference hash in execution report |

## Lessons Learned (HARDCODED - NEVER VIOLATE)

Proven failures from real multi-track orchestrations. Violating them WILL cause failure.

### 1. Orchestrator Must Not Read Spec Files

**What failed:** Orchestrator read the roadmap spec directly, ran git commands, listed directories, searched patterns. Consumed 55s and massive context before any delegation happened. No work done.

**Rule:** INVOKE MUX SKILL FIRST. MUX hooks block Read/Grep/Glob. Delegate ALL spec reading to Strategy Analyst high-tier agent. Orchestrator receives ONLY the decomposition summary.

### 2. No Sub-Coordinator Layer

**What failed:** Inserting a "track sub-coordinator" between head coordinator and phase agents. Sub-coordinator completed one phase and stopped, treating the phase agent's return as its own completion signal.

**Rule:** Head coordinator manages phase sequence DIRECTLY. No intermediate coordinator layer.

### 3. No Double Nesting

**What failed:** Sub-coordinator -> phase agent -> mux-ospec. Double nesting restricted Task() tool availability, making mux-ospec unable to delegate.

**Rule:** Maximum nesting: Head coordinator -> phase agent -> Skill(mux-ospec). Two levels only.

### 4. Phase Agents Must Not Bypass mux-ospec

**What failed:** Phase agents received too much implementation context in their prompt and implemented directly without invoking mux-ospec. Spec files were empty, no PLAN commits existed.

**Rule:** Phase agent prompt contains ZERO implementation context. Only the spec path and the Skill() call. Explicit prohibition: "DO NOT implement as fallback." Mandatory verification checkpoints after mux-ospec returns.

### 5. Always Launch NEW Phase Agent After Refinement

**What failed:** Attempting to resume a phase agent after refinement polluted context from the failed attempt.

**Rule:** After refinement resolution, always launch a FRESH phase agent. Never resume a failed one.

### 6. Sentinel Catches Runtime Errors Unit Tests Miss

**What failed:** Type check and unit tests passed, but real browser E2E revealed TDZ errors, broken lazy imports, missing providers — invisible to static analysis.

**Rule:** E2E via real browser (Playwright) is MANDATORY after each track. Unit tests + type check are necessary but NOT sufficient.

### 7. Test Executor Should Use Low-Tier Model

**What happened:** High-tier model wasted tokens on mechanical browser interactions (click, type, verify). No reasoning needed for execution.

**Rule:** S2 Test Executor uses low-tier by default. Escalate to medium-tier ONLY for ambiguous test cases requiring interpretation. NEVER use high-tier for test execution.

### 8. E2E Tests Require App State Initialization

**What failed:** Test executor tried to test content-dependent features without setting up required app state first. Tests failed because the app had no data to operate on.

**Rule:** App-specific setup (create workspace, project, seed data, etc.) MUST happen FIRST via `{programmatic_app_init}` before testing content-dependent features.

### 9. App Init Must Be Programmatic for Headless E2E

**What failed:** Test executor tried to use native file pickers and OS dialogs that are blocked in headless browser environments.

**Rule:** Use `browser_evaluate` for programmatic setup. Native file pickers, OS dialogs, and system-level interactions are blocked in headless environments. Always use programmatic alternatives.

### 10. Third-Party Library Internal Event Handling Race Conditions

**What happened:** `{editor_library}` intercepted keyboard events before app-level handlers could process them. Standard DOM event testing showed correct behavior but the library's internal handling diverged.

**Rule:** When `{editor_library}` or similar libraries intercept events before app-level handlers, test at the library extension level, not just the wrapper level. Classify persistent races as KNOWN_LIMITATION after investigation.

### 11. Stage-by-Stage More Reliable Than mux-ospec for Deep Nesting

**What happened:** mux-ospec at 3+ nesting levels lost Task() delegation ability. Direct `/spec STAGE` invocations worked reliably at any depth.

**Rule:** If mux-ospec fails at nesting depth, fall back to direct `/spec STAGE` invocations. More agent launches but each succeeds. Document the fallback in CONTINUE.md.

### 12. Dev Server Port Must Be Explicit in Every Executor Prompt

**What failed:** S2 executor launched dev server on default port, conflicting with existing processes. Other times, executor navigated to wrong port.

**Rule:** ALWAYS specify `{dev_server_cmd}` with explicit port in every S2 executor prompt. Every test executor prompt MUST state: "Dev server: `{dev_server_cmd}` at `http://localhost:{dev_port}`".

### 13. Multiple Root Causes Hide Behind Single Symptom

**What happened:** First fix resolved the visible symptom, but the underlying issue remained. Subsequent tests revealed the real problem was deeper (e.g., event propagation, not just missing handler).

**Rule:** Use high-tier with browser access to diagnose. Verify fix IN BROWSER, not just via type check/tests. A passing type check does not mean the fix is correct.

### 14. Voice Prompt Before User Gates (Optional)

**What happened:** User missed AskUserQuestion prompts during long autonomous runs because they stepped away.

**Rule:** If `{voice_tool}` is available: alert user audibly before AskUserQuestion. This is optional — only when voice tooling is configured.

### 15. Autonomous Execution Is Default

**What happened:** Orchestrator paused after every stage waiting for user confirmation, turning a 50-phase roadmap into an interactive session requiring constant attention.

**Rule:** Proceed through ALL stages without waiting. Only escalate: critical unresolvable blockers OR UX philosophy changes that need human judgment. `--wait-after-plan` flag overrides this for PLAN stages only.

### 16. CONTINUE Files Must Update After Every Stage

**What failed:** CONTINUE.md was stale by 3+ phases, causing resume sessions to repeat work or skip phases.

**Rule:** Delegate low-tier agent to update CONTINUE.md after EVERY stage (GATHER, PLAN, IMPLEMENT, REVIEW, TEST). Non-negotiable. This is the single source of truth for cross-session resume.

### 17. Every REVIEW Must Include Visual E2E Validation

**What failed:** REVIEW stage passed based on type check + unit tests, but visual rendering was broken (overlapping panels, invisible text, misaligned layouts).

**Rule:** Type check + unit tests are necessary but NOT sufficient. Playwright visual review is required. No REVIEW is complete until visual validation passes.

### 18. `--wait-after-plan` Overrides Autonomous Default

**Use case:** User wants to review each phase's PLAN before committing to IMPLEMENT. Useful for high-stakes or unfamiliar codebases.

**Rule:** When `--wait-after-plan` flag is set, pause after each PLAN stage and present the plan summary via AskUserQuestion. Wait for explicit user confirmation before proceeding to IMPLEMENT. Does NOT affect other stages.

### 19. Library Version-Specific Quirks Need Explicit Documentation

**What happened:** A library interpreted API parameters differently than expected (e.g., numeric values where strings were expected, different default behaviors between major versions). Time wasted debugging "correct" code.

**Rule:** When a library interprets API parameters differently than documented or expected, document the quirk immediately in Lessons Learned within the session CONTINUE.md. Include: library name, version, expected vs. actual behavior, workaround.

### 20. Sentinel S2 Batching for Large Test Suites

**What happened:** S2 executor ran 300+ test cases in a single session, exhausted context, and crashed mid-execution. Results for already-executed tests were lost.

**Rule:** When test case count exceeds ~100, S2 MUST execute in batches (50-80 cases per batch). Write partial results after each batch. On app crash mid-batch, retry the current batch only. Preserve completed batch results.

### 21. Hotfix Phases Must Have Single Canonical Track

**What happened:** A hotfix phase appeared in two different tracks' tracking tables, causing confusion about which track owned it and whether it was counted once or twice in progress.

**Rule:** Hotfix phases that span tracks MUST be tracked under a single canonical track. Other tracks may cross-reference with a note (e.g., "See Track G Phase 047") but MUST NOT list it as their own phase. Track phase counts in headers MUST match actual table rows.

### 22. All Templates Must Use Tier-Based Model Terminology

**What happened:** Prompts and CONTINUE files used provider-specific model names instead of tier-based terminology, violating the project's provider-agnostic convention.

**Rule:** All agent prompts, templates, and documentation MUST use tier-based terminology (low-tier, medium-tier, high-tier) instead of specific model names. See AGENTS.md Model Tier Terminology table.

### 23. NEVER Use High-Tier Model for Test Execution Agents

**What failed:** Test execution agent launched with high-tier model for Playwright browser automation. Churned through massive context/tokens on mechanical click-type-verify interactions. Multiple agents killed due to context exhaustion.

**Rule:** ALL test execution agents MUST use low-tier or medium-tier models. High-tier is for reasoning/planning ONLY.
- `model: low-tier` — mechanical browser interactions (click, verify, screenshot)
- `model: medium-tier` — complex test analysis or ambiguous test cases
- `model: high-tier` — NEVER for any Playwright/browser automation work

**Reinforces:** Lesson 7 (low-tier for test execution).

### 24. Use Playwright CLI Skills, NOT Raw MCP Tools

**What failed:** Test execution agent called raw MCP tools (`browser_snapshot`, `browser_click`, `browser_evaluate`) directly. `browser_snapshot` returns massive accessibility tree dumps (1000+ lines, ~4K tokens per snapshot). With 100+ tests, context exhausted in <20 tests.

**Rule:** Test execution agents MUST use the `playwright-cli` skill (token-efficient CLI alternative) instead of raw MCP tools:
- `Skill(skill="playwright-cli")` — browser automation via CLI commands through Bash
- `Skill(skill="test-e2e")` — structured test execution with definition files
- NEVER call `browser_snapshot`, `browser_click`, `browser_evaluate` MCP tools directly

Every test execution agent prompt MUST include:
```
Use Skill(skill="playwright-cli") for browser automation — NOT raw MCP playwright tools.
Use Skill(skill="test-e2e") for structured test execution.
NEVER call browser_snapshot, browser_click, browser_evaluate directly.
playwright-cli uses Bash commands (playwright-cli snapshot, playwright-cli click, etc.) which are far more token-efficient than MCP tool schemas.
```

### 25. Orchestrator Must Invoke mux-ospec Directly, Not Via Phase Agent

**What failed:** Phase agent (high-tier, bg) was launched with instructions to call `Skill(skill="mux-ospec", args="full <spec-path>")`. At that nesting depth (Head Coordinator -> Phase Agent -> Skill(mux-ospec)), the Skill invocation either fails, can't delegate properly, or the phase agent tries to implement directly instead of invoking the skill.

**Rule:** The MUX orchestrator / mux-roadmap orchestrator MUST invoke `/mux-ospec` directly for each phase, NOT delegate it to a phase agent that then tries to invoke it. This means the orchestrator calls `Skill(skill="mux-ospec", args="...")` itself, which loads the ospec workflow into the orchestrator's context. The orchestrator then delegates the individual ospec stages (GATHER, PLAN, IMPLEMENT, etc.) via Task() subagents as mux-ospec instructs.

**Architecture change:**
```
BEFORE (BROKEN):
  Head Coordinator -> Task(Phase Agent) -> Skill(mux-ospec) -> Task(stage workers)
  Three levels of nesting. Skill() at depth 2 fails.

AFTER (CORRECT):
  Head Coordinator -> Skill(mux-ospec) directly -> Task(stage workers)
  Two levels. Orchestrator loads ospec, delegates stages.
```

---

# Standing Instructions (Carried Into CONTINUE.md)

These instructions MUST be included in every CONTINUE.md update and carried forward across sessions:

- CONTINUE file updates after EVERY stage completion (non-negotiable)
- Dev server: `{dev_server_cmd}` at `http://localhost:{dev_port}` (non-negotiable)
- Resume prompt section always current in CONTINUE.md
- Standing instructions section self-referential (always include in CONTINUE updates)
- Updated test counts (unit + type + E2E) after every phase
- Commit references for all changes
- Session-specific lessons learned appended (never removed)

---

# Report

## Progress Updates (MANDATORY)

### After EVERY Phase Completion

```
PHASE_{NNN}_COMPLETE - {Phase Title} implemented.

Phase {NNN} Results:
- Commits: {hash}
- Tests: {N} passing ({+M} new, 0 regressions)
- Type check: 0 errors
- Key changes: {brief summary}

Overall Progress:
- Track A: COMPLETE ({P}/{P})
- Track B: IN_PROGRESS ({X}/{Y} - Phase {NNN} done, Phase {NNN+1} next)
- Track C: NOT_STARTED (blocked by Track B)
```

### After EVERY Track Completion

```
Track {X} ({Track Title}) COMPLETE - all {N} phases done.

Post-Track Pipeline:
- High-tier Fixer: {status}
- Sentinel E2E: {status}

Overall Progress:
- Track A: COMPLETE ({P}/{P})
- Track B: COMPLETE ({Q}/{Q})
- Track C: IN_PROGRESS (0/{R} - launching Phase {NNN})
```

### After ALL Tracks Complete

```
ROADMAP COMPLETE.

Final Status:
- Track A: COMPLETE ({P}/{P})
- Track B: COMPLETE ({Q}/{Q})
- Track C: COMPLETE ({R}/{R})

QA Gate:
- Test Cases: {N}
- Pass Rate: {pct}%
- Verdict: GO

Total phases: {N}
Session: <SESSION_DIR>
Branch: <BRANCH>
```

Then deactivate MUX session:
```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py
```

## CONTINUE.md Template

Delegate creation/updates to a Task(medium-tier) writer agent. Template:

````markdown
# CONTINUE - <Roadmap Title>

**Session:** `<SESSION_DIR>`
**Branch:** `<BRANCH>`
**Modifier:** `<MODIFIER>`
**Type Check:** `<TYPE_CHECK_CMD>`
**Test:** `<TEST_CMD>`
**Dev Server:** `<DEV_SERVER_CMD>` at `http://localhost:<DEV_PORT>`
**Last Updated:** <ISO timestamp>
**Resume:** `/mux-roadmap <SESSION_DIR>/CONTINUE.md continue`

---

## Current State

### Track A - <Title>
**Status:** {X}/{Y} phases complete

| Phase | Spec | Stage | Status | Commits | Notes |
|-------|------|-------|--------|---------|-------|
| NNN | `<spec-path>` | {stage} | {status} | `<hash>` | {notes} |

### Track B - <Title>
**Status:** {X}/{Y} phases complete

| Phase | Spec | Stage | Status | Commits | Notes |
|-------|------|-------|--------|---------|-------|
| ... | ... | ... | ... | ... | ... |

---

## Test Status

- **Unit Tests:** {N} passing (across {M} files), 0 failures
- **Type Check:** 0 errors
- **E2E Visual:** {PASS|FAIL|NOT_RUN} at phases {list}

## Post-Track Fixes

| Fix | Tests | Commit | Description |
|-----|-------|--------|-------------|

## Sentinel Results

### Track {X} Sentinel
- S1: {status} ({N} test cases)
- S2: {status} ({pass}/{total})
- S3: {status} ({N} corrections)
- S4: {status} ({N} fixes)
- Cycles: {N}
- Final: {SENTINEL_COMPLETE | ESCALATED}

## QA Gate

- Test Cases: {N} files, {M} cases (P0: {a}, P1: {b}, P2: {c})
- Execution: {pass}/{total} ({pct}%)
- Verdict: {GO | NO-GO}
- P0 Blockers: {list or "None"}

---

## Previous Work (Archive)

{Completed specs archived here to prevent CONTINUE.md from growing unbounded.
 Move specs here once their track is COMPLETE. Format: phase number, title, commit hash.}

## Pending Refinements

{List with paths, or "None"}

## Blockers

{List, or "None"}

## Next Action

{Exact next step}

## Status

- Track A: {state} ({X}/{Y})
- Track B: {state} ({X}/{Y})

---

## Workflow

### Architecture
[Copy from this prompt's Workflows > Architecture section]

### Phase Agent Prompt Template v3
[Copy from this prompt's Workflows > Phase Agent Prompt Template section]

### Lessons Learned
{Accumulated during this session - append, never remove}

## Standing Instructions

- CONTINUE file updates after EVERY stage completion (non-negotiable)
- Dev server: `{dev_server_cmd}` at `http://localhost:{dev_port}` (non-negotiable)
- Resume prompt section always current in CONTINUE.md
- Standing instructions section self-referential (always include in CONTINUE updates)
- Updated test counts (unit + type + E2E) after every phase
- Commit references for all changes

---

## Resume Prompt

```
/mux-roadmap <SESSION_DIR>/CONTINUE.md continue
```

## Resume
```
/mux-roadmap <SESSION_DIR>/CONTINUE.md continue
```
````

## Signal File Formats

### Track Status (`signals/track-{x}.status`)

```yaml
track: A
state: IN_PROGRESS    # NOT_STARTED | IN_PROGRESS | NEEDS_REFINEMENT | BLOCKED | COMPLETED | FAILED
current_phase: "NNN"
updated_at: "<ISO timestamp>"
summary: "Phase NNN done, launching NNN+1"
```

### Phase Signal (`track-{x}/signals/phase-{NNN}.signal`)

```yaml
phase: "NNN"
title: "<phase-title>"
spec_path: "<spec-path>"
state: PHASE_COMPLETE   # PLAN_PENDING | PLAN_DONE | IMPLEMENT_PENDING | IMPLEMENT_DONE | PHASE_COMPLETE | NEEDS_REFINEMENT | FAILED
stage: DONE
stage_status: DONE
commit: "<hash>"
updated_at: "<ISO timestamp>"
error: ""
refinement_ref: ""
```

### Phase State Machine

```
PLAN_PENDING -> PLAN_IN_PROGRESS -> PLAN_DONE
  -> IMPLEMENT_PENDING -> IMPLEMENT_IN_PROGRESS -> IMPLEMENT_DONE
    -> TEST_PENDING -> TEST_IN_PROGRESS -> TEST_DONE
      -> PHASE_COMPLETE

Any -> NEEDS_REFINEMENT -> {STAGE}_PENDING (after resolution)
Any -> FAILED
Any -> BLOCKED -> {STAGE}_PENDING (after unblocked)
```

### Refinement Request (`track-{x}/refinements/phase-{NNN}-{slug}.md`)

```markdown
# Refinement Request: {Title}

**Phase:** {NNN} - {title}
**Stage:** {PLAN|IMPLEMENT|TEST}
**Spec:** {spec_path}
**Requested at:** {ISO timestamp}
**Priority:** {P0|P1|P2}

## What Needs Refinement
{Precise description}

## Context
{Findings, code references}

## Options
1. **Option A:** - Pros / Cons
2. **Option B:** - Pros / Cons

## Suggested Default
{Recommendation or "No default - requires human decision."}

## Impact on Spec
{Which sections need updating}
```

### Session Directory Structure

```
tmp/mux/<session-slug>/
+-- .signals/
|   +-- decomposition.done       # Strategy analyst completion
+-- signals/
|   +-- track-a.status
|   +-- track-b.status
|   +-- refinements/
+-- track-a/
|   +-- signals/
|   |   +-- phase-001.signal
|   |   +-- phase-002.signal
|   +-- refinements/
+-- track-b/
|   +-- signals/
|   +-- refinements/
+-- sentinel/
|   +-- test-cases.md
|   +-- test-execution-report.md
|   +-- audit-corrections.md
|   +-- fixes-and-refinements.md
|   +-- fix-report-cycle-{N}.md
+-- qa/
|   +-- test-cases/
|   |   +-- p0-blocking.md
|   |   +-- p1-experience.md
|   |   +-- p2-polish.md
|   +-- execution-report.md
|   +-- verdict.md
+-- decomposition.md              # Strategy analyst output
+-- CONTINUE.md
```

---

# Examples

## Example 1: Start New Roadmap

**Invocation:**
```
/mux-roadmap specs/2026/02/feature-branch/001-feature-spec.md start
```

**Correct flow (what SHOULD happen):**
```
MUX MODE | Action: Skill(mux) | Target: roadmap orchestration | Rationale: mandatory first action

> Skill(skill="mux", args="Orchestrate multi-track roadmap. PATH: specs/2026/02/... Mode: start.")

MUX MODE | Action: uv run session.py | Target: session init | Rationale: mandatory MUX first action

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py 'feature-migration'")

MUX MODE | Action: Task (Strategy Analyst) | Target: decomposition | Rationale: delegate spec reading

> Task(high-tier, bg) - Strategy Analyst reads spec, creates per-phase specs, returns decomposition

(agent returns)

MUX MODE | Action: Task (explore) | Target: read decomposition | Rationale: get summary without reading file

> Task(low-tier) - reads decomposition.md, returns content

(presents to user)

Confirm this decomposition? 5 tracks, 11 phases.

(user confirms)

MUX MODE | Action: Bash mkdir | Target: session dirs | Rationale: prepare track directories
MUX MODE | Action: Task (phase agent) | Target: Phase 001 | Rationale: first phase of Track A

> Task(high-tier, bg) - Phase agent with Skill(mux-ospec)

Checkpoint:
- Worker launched (high-tier, background)
- Continuing immediately

Overall Progress:
- Track A: IN_PROGRESS (0/1 - Phase 001 running)
- Track B: NOT_STARTED
...

Waiting for notifications.
```

**WRONG flow (what the failing session did):**
```
> Read(specs/2026/02/.../001-spec.md)                         <-- VIOLATION: reading spec yourself
> Bash("git branch --show-current")                           <-- VIOLATION: no MUX session
> Bash("ls specs/2026/02/.../")                               <-- VIOLATION: listing files yourself
> Read(package.json)                                          <-- VIOLATION: reading project files
> Read(backlog.md)                                            <-- VIOLATION: more reading
55s of churning, massive context consumed, no delegation, no work done.
```

## Example 2: Resume Existing Session

**Invocation:**
```
/mux-roadmap tmp/mux/20260206-1430-migration/CONTINUE.md continue
```

**Correct flow:**
```
MUX MODE | Action: Skill(mux) | Target: roadmap resume | Rationale: mandatory first action

> Skill(skill="mux", args="RESUME multi-track roadmap. PATH: tmp/mux/.../CONTINUE.md. Mode: continue.")

MUX MODE | Action: uv run session.py | Target: session init | Rationale: mandatory MUX first action

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/session.py 'migration-resume'")

MUX MODE | Action: Task (explore) | Target: read CONTINUE.md | Rationale: delegate state reading

> Task(low-tier) - reads CONTINUE.md + signal files, returns state summary

Resume State:
- Track A: COMPLETE (4/4)
- Track B: IN_PROGRESS (2/4 - Phase 007 next)
Confirm resume?

(user confirms)

MUX MODE | Action: Task (phase agent) | Target: Phase 007 | Rationale: resume from next pending

> Task(high-tier, bg) - Phase agent

Checkpoint:
- Worker launched (high-tier, background)
- Continuing immediately

Waiting for notifications.
```

## Example 3: Phase Completion + Next Launch

```
(agent notification: Phase 007 complete)

PHASE_007_COMPLETE - Iterator System implemented.

Phase 007 Results:
- Commits: db590fa
- Tests: 766 passing (+22 new, 0 regressions)
- Type check: 0 errors
- Key changes: Pure state machine, full-screen UI, keyboard handler

Overall Progress:
- Track A: COMPLETE (4/4)
- Track B: IN_PROGRESS (3/4 - Phase 007 done, Phase 008 next)
- Track C: NOT_STARTED (blocked by Track B)

MUX MODE | Action: Task (phase agent) | Target: Phase 008 | Rationale: next in Track B

> Task(high-tier, bg) - Phase agent

Checkpoint:
- Worker launched (high-tier, background)
- Continuing immediately

Waiting for notifications.
```

## Example 4: Extended Wait + Verify

```
(no task-notification after extended time)

No notification for phase 011. Verifying worker status.

MUX MODE | Action: Bash verify.py | Target: phase 011 status | Rationale: no task-notification received

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/verify.py tmp/mux/<session>/track-c/signals/phase-011.signal")

Worker still active (97 tools, 126K tokens). Continuing to wait.
```

## Example 5: Track Completion + Next Track

```
(Phase 008 complete - last phase in Track B)

Track B (Property System) COMPLETE - all 4 phases done.

Overall Progress:
- Track A: COMPLETE (4/4)
- Track B: COMPLETE (4/4) - 785 tests passing
- Track C: IN_PROGRESS (0/4 - launching Phase 011)

MUX MODE | Action: Bash mkdir | Target: track-c dirs | Rationale: prepare for Track C

> mkdir -p tmp/mux/<session>/track-c/signals tmp/mux/<session>/track-c/refinements

MUX MODE | Action: Task (phase agent) | Target: Phase 011 | Rationale: first phase of Track C

> Task(high-tier, bg) - Phase agent

Checkpoint:
- Worker launched (high-tier, background)
- Continuing immediately

Overall Progress:
- Track A: COMPLETE (4/4)
- Track B: COMPLETE (4/4)
- Track C: IN_PROGRESS (0/4 - Phase 011 running)

Waiting for notifications.
```

## Example 6: Refinement Escalation

```
(Phase 006 returns NEEDS_REFINEMENT)

MUX MODE | Action: Task (explore) | Target: read refinement doc | Rationale: understand what needs resolution

> Task(low-tier) - reads refinement doc, returns summary

Phase 006 needs refinement: authentication approach unclear.
This affects UX philosophy - ESCALATING.

Options:
1. JWT tokens (stateless, better for API consumers)
2. Session-based (stateful, better for browser clients)

> AskUserQuestion

(user chooses JWT)

MUX MODE | Action: Task (spec update) | Target: update phase 006 spec | Rationale: apply user decision

> Task(medium-tier, bg) - updates spec with JWT approach

MUX MODE | Action: Task (phase agent) | Target: Phase 006 retry | Rationale: fresh agent with updated spec

> NEW Task(high-tier, bg) - Fresh phase agent
```

## Example 7: Full Roadmap Completion

```
ROADMAP COMPLETE.

Final Status:
- Track A: COMPLETE (4/4)
- Track B: COMPLETE (4/4)
- Track C: COMPLETE (4/4)

QA Gate:
- Test Cases: 117
- Pass Rate: 81%
- Verdict: GO

Total phases: 12
Session: tmp/mux/20260206-1430-migration/
Branch: feat/migration-v2

MUX MODE | Action: uv run deactivate.py | Target: cleanup | Rationale: MUX work complete

> Bash("uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/deactivate.py")
```

## Example 8: Post-Track High-tier Fixer

```
Track B complete. Launching High-tier Fixer.

MUX MODE | Action: Task (High-tier Fixer) | Target: Track B cleanup | Rationale: post-track TS/runtime sweep

> Task(high-tier, bg) - fix TS/runtime errors

(returns: 0 type errors, 3 files fixed, all tests green)

High-tier Fixer complete. Launching Sentinel E2E Loop.
```

## Example 9: Sentinel Self-Healing Cycle

```
S1 writers complete (42 test cases). Launching S2 executor.

MUX MODE | Action: Task (S2 executor) | Target: Sentinel E2E | Rationale: execute test cases via Playwright

> Task(low-tier, bg) - execute tests via Playwright

(S2 returns: 34 PASS, 6 FAIL, 2 PARTIAL)

> S3 auditor -> 3 corrections found
> S4 consolidator -> 5 fixes needed (2 P0, 2 P1, 1 P2)

Cycle 1: Diagnostician -> Implementer -> Re-runner
(2 P0 fixed, 1 P1 fixed, 2 remaining)

Cycle 2: Diagnostician -> Implementer -> Re-runner
(all PASS)

SENTINEL_COMPLETE - 2 cycles, 3 fixes applied.
```

## Example 10: QA Gate NO-GO -> Fix -> GO

```
QA Gate initiated. 117 test cases across 8 categories.

QA Execution: 82/117 PASS (70%). VERDICT: NO-GO.
P0 Blockers: 3 failures (data loss on save, crash on empty state, broken navigation).

Entering P0 Fix Loop.

MUX MODE | Action: Task (P0 fixer) | Target: 3 P0 blockers | Rationale: NO-GO verdict requires fix

> Task(high-tier, bg) - fix 3 P0 issues
(3 P0s fixed, committed)

> Re-execute affected categories only
QA Re-run: 95/117 PASS (81%). VERDICT: GO.

ROADMAP COMPLETE.
```

---

# BEGIN

Parse `$ARGUMENTS` now.

**Your FIRST action MUST be:** `Skill(skill="mux", args="Orchestrate multi-track roadmap. PATH: <PATH>. Mode: <MODE>. Follow roadmap orchestration protocol. Delegate ALL spec reading to Strategy Analyst high-tier agent.")`

Do NOT read any files first. Do NOT run git commands. Do NOT analyze anything. Invoke MUX.