---
name: dev-implement
version: 1.0
description: “REQUIRED Phase 5 of /dev workflow. Orchestrates per-task ralph loops with delegated TDD implementation.”
---

**Announce:** “I’m using dev-implement (Phase 5) to orchestrate implementation.”

## Where This Fits

```
Main Chat (you)                    Task Agent
─────────────────────────────────────────────────────
dev-implement (this skill)
  → dev-ralph-loop (per-task loops)
    → dev-delegate (spawn agents)
      → Task agent ──────────────→ follows dev-tdd
                                   uses dev-test tools
```

**Main chat orchestrates.** Task agents implement.

## Contents

- [Prerequisites](#prerequisites)
- [Implementation Strategy Choice](#implementation-strategy-choice)
- [The Iron Law of Delegation](#the-iron-law-of-delegation)
- [The Process](#the-process) (Sequential)
- [Sub-Skills Reference](#sub-skills-reference)
- [If Max Iterations Reached](#if-max-iterations-reached)
- [Agent Team Implementation (Parallel)](#agent-team-implementation-parallel)
- [Phase Complete](#phase-complete)

# Implementation (Orchestration)

<EXTREMELY-IMPORTANT>
## Prerequisites

**Do NOT start implementation without these:**

1. `.claude/SPEC.md` exists with final requirements
2. `.claude/PLAN.md` exists with chosen approach
3. **User explicitly approved** in /dev-design phase
4. **PLAN.md Testing Strategy section is COMPLETE** (all boxes checked)

If any prerequisite is missing, STOP and complete the earlier phases.

**Check PLAN.md for:** files to modify, implementation order, testing strategy.

### Pre-Flight Testing Check (MANDATORY)

Before starting ANY task, verify PLAN.md Testing Strategy:

```
[ ] Framework specified (not empty, not “TBD”)
[ ] Test Command specified (runnable command)
[ ] First Failing Test described (specific test name)
[ ] Test File Location specified (actual path)
```

**If ANY box is unchecked → STOP. Go back to design phase.**

This is your LAST CHANCE to catch missing test strategy before writing code.
</EXTREMELY-IMPORTANT>

## Implementation Strategy Choice

After prerequisites pass, check PLAN.md for parallelization potential:

**Skip this choice when:**
- PLAN.md has fewer than 4 tasks
- All tasks are dependent (every task is `after N` with no independent groups)
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not available

**Otherwise, ask the user:**

```python
AskUserQuestion(questions=[{
  "question": "How should we implement the tasks in PLAN.md?",
  "header": "Strategy",
  "options": [
    {"label": "Sequential (Default)", "description": "One ralph loop per task, complete N before N+1. Safest, no merge conflicts."},
    {"label": "Agent team (parallel)", "description": "Spawn teammate per independent task group. Faster for 4+ independent tasks. Requires reconciliation."}
  ],
  "multiSelect": false
}])
```

**If Sequential:** Proceed to [The Process](#the-process) below (current behavior).

**If Agent team:** Skip to [Agent Team Implementation (Parallel)](#agent-team-implementation-parallel).

<EXTREMELY-IMPORTANT>
## The Iron Law of TDD (Final Enforcement)

**YOU CANNOT WRITE IMPLEMENTATION CODE WITHOUT A FAILING TEST FIRST.**

This is not a suggestion. This is the workflow. Every task follows:

```
1. READ the test description from PLAN.md
2. WRITE the test file
3. RUN the test → SEE RED (failure)
4. ONLY THEN write implementation
5. RUN the test → SEE GREEN (pass)
```

### Rationalization Prevention (Implementation Phase)

If you catch yourself thinking these, STOP IMMEDIATELY:

| Thought | Reality | Action |
|---------|---------|--------|
| “No test infra, I’ll just implement” | You should have caught this in explore/clarify | STOP. Go back. Add Task 0. |
| “SPEC.md says manual testing” | SPEC.md is wrong | STOP. Fix SPEC.md. Ask user. |
| “This task is too simple for tests” | Simple tasks benefit MOST from tests | Write the test anyway. |
| “I’ll add tests after this works” | That’s not TDD. That’s lying. | DELETE your code. Write test first. |
| “User is waiting, I’ll be quick” | User wants WORKING code, not fast code | Take time. Write test first. |
| “The subagent skipped tests” | Your job is to catch that | REJECT the work. Redo with tests. |
| “Just this one exception” | No exceptions. Ever. | Write the test. |

**If you wrote code without a failing test first, DELETE IT and start over.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**MAIN CHAT MUST NOT WRITE CODE. This is not negotiable.**

Main chat orchestrates. Subagents implement. If you catch yourself about to use Write or Edit on a code file, STOP.

| Allowed in Main Chat | NOT Allowed in Main Chat |
|---------------------|--------------------------|
| Spawn Task agents | Write/Edit code files |
| Review Task agent output | Direct implementation |
| Write to .claude/*.md files | “Quick fixes” |
| Run git commands | Any code editing |
| Start ralph loops | Bypassing delegation |

**If you’re about to edit code directly, STOP and spawn a Task agent instead.**

### Rationalization Prevention

These thoughts mean STOP—you’re rationalizing:

| Thought | Reality |
|---------|---------|
| “It’s just a small fix” | Small fixes become big mistakes. Delegate. |
| “I’ll be quick” | Quick means sloppy. Delegate. |
| “The subagent will take too long” | Subagent time is cheap. Your context is expensive. |
| “I already know what to do” | Knowing ≠ doing it well. Delegate. |
| “Let me just do this one thing” | One thing leads to another. Delegate. |
| “This is too simple for a subagent” | Simple is exactly when delegation works best. |
| “I’m already here in the code” | Being there ≠ writing there. Delegate. |
| “The user is waiting” | User wants DONE, not fast. They won’t debug your shortcuts. |
| “This is just porting/adapting code” | Porting = writing = code. Delegate. |
| “I already have context loaded” | Fresh context per task is the point. Delegate. |
| “It’s config, not real code” | JSON/YAML/TOML = code. Delegate. |
| “I need to set things up first” | Setup IS implementation. Delegate. |
| “This is boilerplate” | Boilerplate = code = delegate. |
| “PLAN.md is detailed, just executing” | Execution IS implementation. Delegate. |

### The Meta-Rationalization

**If you’re treating these rules as “guidelines for complex work” rather than “invariants for ALL work”, you’ve already failed.**

Simple work is EXACTLY when discipline matters most—because that’s when you’re most tempted to skip it.
</EXTREMELY-IMPORTANT>

## The Process

```
For each task N in PLAN.md:
    1. Determine loop type:
       - Visual task? → Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/visual-verify/SKILL.md")
       - Standard task? → Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-ralph-loop/SKILL.md")

    2. Inside loop: spawn Task agent
       → Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-delegate/SKILL.md")

    3. Task agent follows TDD (dev-tdd) using testing tools (dev-test)
       Visual tasks: also render output and vision-check with look-at

    4. Verify tests pass (+ visual check passes for visual tasks), output promise

    5. Move to task N+1, start NEW loop
```

### Visual Task Detection

If a PLAN.md task involves rendered visual output, use **visual-verify** instead of plain ralph-loop. Visual-verify adds render → look-at → fix steps inside each iteration.

**Signals a task is visual:** task mentions "render", "slide", "chart", "figure", "layout", "UI", "screenshot", "visual", "diagram", or produces any file meant to be seen by humans (PNG, PDF, SVG).

```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/visual-verify/SKILL.md")
```

### Step 1: Start Ralph Loop for Each Task

**REQUIRED SUB-SKILL:**
```
Read(“${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-ralph-loop/SKILL.md”)
```

Key points from dev-ralph-loop:
- ONE loop PER TASK (not one loop for feature)
- Each task gets its own completion promise
- Don’t move to task N+1 until task N’s loop completes

### Step 2: Inside Loop - Spawn Task Agent

**REQUIRED SUB-SKILL:**
```
Read(“${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-delegate/SKILL.md”)
```

Key points from dev-delegate:
- Implementer → Spec reviewer → Quality reviewer
- Task agent follows dev-tdd protocol
- Task agent uses dev-test tools

### Step 3: Verify and Complete (MANDATORY - DO NOT SKIP)

<EXTREMELY-IMPORTANT>
**YOU MUST VERIFY EACH OF THESE. “Task complete” without verification is LYING.**

After Task agent returns, **you must personally verify** (not trust the agent’s report):

#### 3a. Read the Actual Code
```
Read the implementation file(s) the agent claims to have written.
Compare to SPEC.md requirements line by line.
```
- [ ] Code matches spec (not a different approach)
- [ ] No substitutions (e.g., spec says IPC, code uses DOM = FAIL)

#### 3b. Check Test Reality
```
Read the test file(s). Look for .skip(), mock-only tests, or tests that don’t call real code.
```
- [ ] Tests EXECUTE code (not grep/mock-only)
- [ ] Tests are NOT skipped (SKIP ≠ PASS)
- [ ] Integration tests exist and run (not just unit tests)

#### 3c. Run Tests Yourself
```
Actually run the test command. Read the output.
```
- [ ] Test command runs without error
- [ ] Tests actually pass (not “66 pass, 0 fail” with 50 skipped)
- [ ] Test output shows real assertions (not just “test exists”)

#### 3d. Verify Real Integration (FOR EXTERNAL SYSTEMS)
```
If the feature integrates with an external system (Electron app, API, database),
you MUST verify it works against the real system, not just mocks.
```
- [ ] External system is actually running
- [ ] Feature actually works (not just “code runs without error”)
- [ ] Output is visible in the external system

**If ANY check fails → REJECT the work. Do NOT mark task complete.**

### Rationalization Prevention (Verification Phase)

| Thought | Reality | Action |
|---------|---------|--------|
| “The agent said tests pass” | Agents lie. Verify yourself. | Run the tests. |
| “66 tests passing is enough” | Count skipped tests. Read test code. | Check for fake tests. |
| “I’ll verify at the end” | You’ll forget. Bugs compound. | Verify NOW. |
| “The spec said X, code does Y, but Y is close enough” | Close enough = wrong. | Reject and redo. |
| “Integration test is skipped but unit tests pass” | Unit tests don’t prove integration works. | Require real integration test. |
| “External system isn’t running, but code is correct” | Untested code is broken code. | Start the system and test. |

**If ALL pass → output the promise.** If ANY fail → iterate.

## Spec Deviation Detection (CRITICAL)

<EXTREMELY-IMPORTANT>
**The most common failure mode: Subagent implements DIFFERENT approach than spec.**

Examples of spec deviations:
- Spec says “IPC channels” → Code uses DOM selectors
- Spec says “WebSocket” → Code uses HTTP polling
- Spec says “use library X” → Code uses library Y
- Spec says “reuse existing function” → Code duplicates logic

### How to Catch Deviations

After EVERY implementation, ask yourself:

```
1. What APPROACH did SPEC.md specify?
   (Read SPEC.md, find the specific approach)

2. What APPROACH did the code actually use?
   (Read the actual implementation code)

3. Are they THE SAME?
   (Not “similar” or “equivalent” - THE SAME)
```

If they differ → REJECT. The spec was approved by the user. Changing the approach without approval is a spec violation.

### Why Subagents Deviate

| Subagent Thinks | Reality |
|-----------------|---------|
| “This approach is easier” | Easier ≠ correct. Follow the spec. |
| “This is equivalent” | User chose the spec approach for a reason. |
| “I couldn’t figure out the spec approach” | Ask questions. Don’t substitute. |
| “The spec approach doesn’t work” | Report failure. Don’t silently change. |

### The Deviation Test

Before marking any task complete, verify:

```
SPEC.md says: [exact quote of approach]
Code does: [actual approach used]
Match: YES / NO

If NO → REJECT and redo with correct approach
```
</EXTREMELY-IMPORTANT>

## Sub-Skills Reference

| Skill | Purpose | Used By |
|-------|---------|---------|
| `dev-ralph-loop` | Per-task loop pattern | Main chat |
| `dev-delegate` | Task agent templates | Main chat |
| `dev-tdd` | TDD protocol (RED-GREEN-REFACTOR) | Task agent |
| `dev-test` | Testing tools (pytest, Playwright, etc.) | Task agent |

## Failure Recovery Protocol

**Pattern from oh-my-opencode: After 3 consecutive implementation failures, escalate.**

### 3-Failure Trigger

If you attempt 3 implementations and ALL fail tests:

```
Iteration 1: Implement approach A → tests fail
Iteration 2: Implement approach B → tests fail
Iteration 3: Implement approach C → tests fail
→ TRIGGER RECOVERY PROTOCOL
```

### Recovery Steps

1. **STOP** all further implementation attempts
   - No more “let me try a different approach”
   - No guessing or throwing code at the problem

2. **REVERT** to last known working state
   - `git checkout <last-passing-commit>`
   - Or revert specific files
   - Document what was attempted in `.claude/RECOVERY.md`

3. **DOCUMENT** what was attempted
   - All 3 approaches tried
   - Test failures for each
   - Why each approach failed
   - What this reveals about the problem

4. **CONSULT** with user BEFORE continuing
   - “I’ve tried 3 approaches. All fail tests. Here’s what I’ve learned...”
   - Present test failure patterns
   - Request: requirements clarification, design input, or different strategy

5. **ASK USER** for direction
   - Option A: Re-examine requirements (may need /dev-clarify)
   - Option B: Try completely different design (may need /dev-design)
   - Option C: Investigate why tests fail (may need /dev-edit)
   - Option D: User provides domain knowledge

**NO PASSING TESTS = NOT COMPLETE** (hard rule)

### Recovery Checklist

Before continuing after multiple failures:

- [ ] All 3 approaches documented with test failures
- [ ] Pattern in failures identified (same tests? different errors?)
- [ ] Current code reverted to clean state
- [ ] User consulted with specific question
- [ ] Clear direction from user before proceeding

### Anti-Patterns After Failures

**DON’T:**
- Keep trying “just one more thing”
- Make larger and larger changes
- Skip TDD “to get it working first”
- Suppress test failures (“I’ll fix them later”)
- Blame the tests (“tests are wrong”)

**DO:**
- Stop and analyze the failure pattern
- Revert to clean state
- Document what each approach revealed
- Consult user with specific findings
- Get clear direction before continuing

### Example Recovery Flow

```
Loop 1: Implement with synchronous approach → Tests timeout
Loop 2: Implement with async/await → Tests hang
Loop 3: Implement with promises → Tests fail assertion

→ RECOVERY PROTOCOL:
1. STOP (no loop 4)
2. REVERT: git checkout HEAD -- src/feature.ts tests/
3. DOCUMENT in .claude/RECOVERY.md:
   - Pattern: All async implementations cause timing issues
   - Tests expect synchronous behavior
   - Hypothesis: Requirements may need async, tests don’t handle it
4. ASK USER:
   “I’ve tried 3 async implementations. All cause timing issues.
    Tests expect synchronous behavior.

    This suggests either:
    A) Feature should actually be synchronous (simpler)
    B) Tests need updating for async behavior

    Which direction should I take?”
```

### When to Trigger Recovery

Trigger after 3 failures when:
- Same test keeps failing despite different approaches
- Different tests fail in pattern (suggests wrong approach)
- Tests pass locally but fail in CI
- Implementation works but breaks unrelated tests

Don’t wait for max iterations - trigger early when pattern emerges.

## If Max Iterations Reached

Ralph exits after max iterations. **Still do NOT ask user to manually test.**

Main chat should:
1. **Summarize** what’s failing (from LEARNINGS.md)
2. **Report** which automated tests fail and why
3. **Ask user** for direction:
   - A) Start new loop with different approach
   - B) Add more logging to debug
   - C) User provides guidance
   - D) User explicitly requests manual testing

**Never default to “please test manually”.** Always exhaust automation first.

## No Pause Between Tasks

<EXTREMELY-IMPORTANT>
**After completing task N, IMMEDIATELY start task N+1 in the SAME RESPONSE. Do NOT pause.**

### Post-Promise Checklist (mandatory, same response)

1. **Update PLAN.md** - Mark task `[x]` complete
2. **Log to LEARNINGS.md** - What was done
3. **Start next task’s ralph loop** - No waiting

| Thought | Reality |
|---------|---------|
| “Task done, let me check in with user” | NO. User wants ALL tasks done. Keep going. |
| “User might want to review” | User will review at the END. Continue. |
| “Natural pause point” | Only pause when ALL tasks complete or blocked. |
| “Let me summarize progress” | Summarize AFTER all tasks. Keep moving. |
| “User has been waiting” | User is waiting for COMPLETION, not updates. |
| “Should I continue?” | YES. Never ask. Just continue. |
| “I’ll update PLAN.md later” | NO. Update it NOW before next task. |

### Valid Stopping Points (only these three)

1. ALL tasks in PLAN.md are marked `[x]` complete
2. You hit a blocker requiring user input (state exactly what you need)
3. User explicitly interrupted

The promise signals task completion. After outputting promise, update PLAN.md, then IMMEDIATELY start next task’s loop.

**Pausing between tasks is procrastination disguised as courtesy.**
</EXTREMELY-IMPORTANT>

## Agent Team Implementation (Parallel)

Use this section when the user chose "Agent team (parallel)" in the strategy choice above.

> **Prerequisite:** Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled. If unavailable, fall back to sequential.

### 1. Prerequisites Check

Before spawning any teammates:

1. **Verify PLAN.md** exists with task list and `Deps` column annotations
2. **Group tasks by independence:**
   - Tasks with `Deps: —` (no dependencies) can run in parallel
   - Tasks with `Deps: after N` form dependency chains — keep these sequential within one teammate
   - Group dependent chains into a single teammate assignment
3. **Verify file scope separation:**
   - Each independent task/group should touch different files
   - If two independent tasks modify the same file, merge them into one group (prevents merge conflicts)
4. **Confirm at least 2 independent groups exist** — otherwise fall back to sequential

Example grouping from a PLAN.md:
```
Task 0: Test infra (Deps: —)       → Teammate A (must complete before others start)
Task 1: Types (Deps: after 0)      → Teammate B (after A completes)
Task 2: Service (Deps: after 1)    ─┐
Task 3: Route handler (Deps: after 1) → Teammate C (Task 2 + 3 if they share files)
Task 4: CLI command (Deps: —)      → Teammate D (independent, parallel with B/C)
```

**Foundation tasks** (like test infra or shared types) that everything depends on must complete BEFORE spawning parallel teammates. Run these sequentially first using normal ralph loops.

### 2. Create Shared Task List and Enter Delegate Mode

1. **Run foundation tasks first** (any task that all others depend on) using normal sequential ralph loops
2. After foundation tasks complete, create one `TaskCreate` per independent task/group:
   - Subject: `Implement: [Task Name(s)]`
   - Description: task details, file scope, test command
3. Press **Shift+Tab** to enter delegate mode — the lead coordinates, does NOT implement
4. Spawn one teammate per task/group

### 3. Spawn Prompt Template

Each teammate receives this self-contained prompt. **Teammates start with a blank conversation and do NOT auto-load skills.** The prompt must contain everything they need.

**Before spawning, substitute these variables:**
- `TASK_NAME` → task name(s) from PLAN.md
- `TASK_DETAILS` → full task text pasted from PLAN.md (not a file reference)
- `SPEC_CONTEXT` → relevant section of SPEC.md pasted inline
- `TEST_FRAMEWORK` → from PLAN.md Testing Strategy (e.g., pytest, jest)
- `TEST_COMMAND` → from PLAN.md Testing Strategy (e.g., `pytest tests/ -v`)
- `TEST_FILE` → test file path for this task
- `FILE_SCOPE` → specific files this teammate may modify (prevents merge conflicts)
- `PLUGIN_ROOT` → resolved value of `${CLAUDE_PLUGIN_ROOT}`

```
You are implementing one task as part of a development team. You have EXCLUSIVE
ownership of the files listed in FILE SCOPE. Do not modify files outside your scope.

## Your Assignment

Task: {TASK_NAME}

### Task Details (from PLAN.md)
{TASK_DETAILS}

### Requirements Context (from SPEC.md)
{SPEC_CONTEXT}

## File Scope (EXCLUSIVE — do not touch files outside this list)

{FILE_SCOPE}

If you discover you need to modify a file NOT in your scope, STOP and message the
lead: "Need to modify [file] which is outside my scope. Reason: [why]."

## Iron Laws of TDD (Non-Negotiable)

**YOU MUST WRITE THE FAILING TEST FIRST. YOU MUST SEE IT FAIL.**

1. **RED**: Write a failing test FIRST
   - Run it with: {TEST_COMMAND}
   - SEE IT FAIL — read the actual output
   - Document: "RED: [test] fails with [error]"

2. **GREEN**: Write MINIMAL code to pass
   - Run test again — SEE IT PASS
   - Document: "GREEN: [test] passes"

3. **REFACTOR**: Clean up while staying green

**If you write code before seeing RED, DELETE IT and start over.**

### What Counts as a REAL Test

| REAL (execute + verify) | NOT A TEST (never do this) |
|-------------------------|---------------------------|
| Test calls function and checks return value | grep for function exists |
| Test makes HTTP request and checks response | ast-grep finds pattern |
| Test clicks UI element and checks result | Log says "success" |

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "This is too simple for tests" | Simple tasks benefit MOST from tests |
| "I'll add tests after" | That's not TDD. Write test first. |
| "No test infra exists" | Foundation task should have set it up. If not, message lead. |

## Step 1: Load Skills

```
Read("{PLUGIN_ROOT}/lib/skills/dev-tdd/SKILL.md")
```

If a testing skill is specified in PLAN.md (dev-test-electron, dev-test-playwright, etc.),
load that too.

## Step 2: Implement with TDD

Follow RED-GREEN-REFACTOR for each piece of functionality in your task:

1. Write failing test in {TEST_FILE}
2. Run {TEST_COMMAND} — see RED
3. Write minimal implementation
4. Run {TEST_COMMAND} — see GREEN
5. Refactor if needed

## Step 3: Commit

After all tests pass:
```
git add [your files only]
git commit -m "feat: [task description]"
```

## Step 4: Message the Lead

After committing, send a message to the lead with:

```
Finished: {TASK_NAME}

Files modified:
- [list each file with brief description of change]

Test results:
- [paste test command output summary — pass count, fail count]

Interface assumptions:
- [any assumptions about types, APIs, or contracts from other tasks]
- [or "None" if fully self-contained]

Commit: [SHA]
```

The lead uses these messages to detect interface conflicts between teammates.
Do NOT message other teammates directly — the lead coordinates all cross-task communication.

## Step 5: Self-Verification Checklist

Before marking your task complete, verify ALL of the following:

- [ ] All tests pass (run {TEST_COMMAND} one final time)
- [ ] Only files in FILE SCOPE were modified
- [ ] Implementation matches SPEC.md requirements (re-read spec context above)
- [ ] No `any` / `@ts-ignore` / type suppression / .skip() in tests
- [ ] Changes committed with descriptive message
- [ ] Lead messaged with files, test results, and interface assumptions

Only mark your task complete after all boxes pass.

## If You Encounter Issues

- **Need a file outside scope:** Message lead, do NOT modify it
- **Test infra missing:** Message lead: "Test infrastructure not available: [details]"
- **Blocked by another task's output:** Message lead: "Blocked — need [interface/type/file] from [other task]"
- **Unclear requirement:** Message lead with specific question. Do NOT guess.
```

### 4. Lead Monitoring

While teammates implement:

- **Watch the shared task list** for completion status and messages
- **If a teammate reports an interface question:** Relay the answer to ALL affected teammates (e.g., "The shared User type should use `{ id: string, email: string }`")
- **If a teammate requests an out-of-scope file:** Decide whether to expand scope or reassign the file
- **If a teammate has been working significantly longer than others:** Message them for status
- **Do NOT implement any tasks yourself** — your job is coordination and reconciliation

### 5. Reconciliation Protocol (3 Passes)

After ALL teammates mark their tasks complete, the lead performs three passes:

<EXTREMELY-IMPORTANT>
**Pass 1 — Merge & Conflicts:**

1. Pull all teammate commits to the working branch
2. If git reports merge conflicts:
   - Read both sides of each conflict
   - Resolve by combining both implementations (do NOT discard either side)
   - If teammates touched the same file despite file scope rules, manually review the entire file
3. After resolving, run the full test suite to verify merge didn't break anything

**Pass 2 — Integration Tests:**

1. Run the FULL test suite (not just per-task tests):
   ```
   [TEST_COMMAND from PLAN.md]
   ```
2. Teammates tested in isolation — integration may reveal:
   - Type mismatches between task boundaries
   - Import conflicts or circular dependencies
   - Shared state assumptions that conflict
3. If integration tests fail:
   - Identify which teammate's code causes the failure
   - Spawn a fix agent (using dev-delegate) targeting the specific integration issue
   - Re-run full suite after fix

**Pass 3 — Spec Compliance:**

1. Read SPEC.md requirements
2. Read each teammate's implementation against the spec
3. Verify no spec deviations across ALL tasks (same check dev-delegate's spec reviewer does, but across the full feature)
4. Check that teammate interface assumptions are consistent (compare the "Interface assumptions" from each teammate's completion message)

**If ANY pass fails → fix before proceeding. Do NOT skip reconciliation passes.**
</EXTREMELY-IMPORTANT>

### 6. When to Use Agent Teams

**Use when:**
- 4+ tasks in PLAN.md with at least 2 independent groups
- Independent tasks touch different files
- Tasks are self-contained (each has own test file and implementation file)

**Do NOT use when:**
- Tasks are tightly coupled (each depends on the previous)
- Multiple tasks modify the same files
- Fewer than 4 tasks (overhead exceeds benefit)
- Tasks require shared state that's built incrementally
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not available

## Phase Complete

**REQUIRED SUB-SKILL:** After ALL tasks complete with passing tests:
```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-review/SKILL.md")
```

Do NOT proceed until automated tests pass for every task.
