---
name: implement-phase
description: Execute a single phase from an implementation plan with all quality gates. This skill is the unit of work for implement-plan, handling implementation, verification, code review, ADR compliance, and plan synchronization for ONE phase. Triggers when implement-plan delegates a phase, or manually with "/implement-phase" and a phase reference.
context: fork
user-invocable: false
argument-hint: "[plan-path] [phase-number]"
---

# Implement Phase

Execute a **single phase** from an implementation plan with comprehensive quality gates. This skill is designed to be called by `implement-plan` but can also be invoked directly.

---

## CRITICAL: Orchestrator Pattern (MANDATORY)

> **THIS SESSION IS AN ORCHESTRATOR. YOU MUST NEVER IMPLEMENT CODE DIRECTLY.**

### What This Means

| DO (Orchestrator) | DO NOT (Direct Implementation) |
|-------------------|--------------------------------|
| Spawn subagents to write code | Write code yourself |
| Spawn subagents to create files | Use Write/Edit tools directly |
| Spawn subagents to run tests | Run tests yourself |
| Spawn subagents to fix issues | Fix code yourself |
| Read files to understand context | Read files to copy/paste code |
| Track progress with Task tools | Implement while tracking |
| Coordinate and delegate | Do the work yourself |

### Enforcement

```
⛔ VIOLATION: Using Write/Edit/NotebookEdit tools directly
⛔ VIOLATION: Creating files without spawning a subagent
⛔ VIOLATION: Fixing code without spawning a subagent
⛔ VIOLATION: Running implementation commands directly

✅ CORRECT: Task(subagent): "Create the AuthService at src/auth/..."
✅ CORRECT: Task(subagent): "Fix the lint errors in src/auth/..."
✅ CORRECT: Task(subagent): "Run npm test and report results..."
```

### Why Orchestration?

1. **Context preservation** - Main session retains full plan context
2. **Parallelization** - Independent tasks run concurrently
3. **Clean separation** - Orchestration logic separate from implementation
4. **Better error handling** - Failures don't pollute main context

### Subagent Spawning Pattern

```
Task (run_in_background: true): "Create [file] implementing [feature].

Context: Phase [N] - [Name]
Requirements:
- [Requirement 1]
- [Requirement 2]

RESPONSE FORMAT: Be concise. Return only:
- STATUS: PASS/FAIL
- FILES: created/modified files
- ERRORS: any issues (omit if none)
Write verbose output to logs/[task].log"
```

### Subagent Communication Protocol (CRITICAL)

> **Subagents MUST be concise. Context preservation is paramount.**

Every subagent prompt MUST include the response format instruction. Verbose responses waste orchestrator context.

**Required Response Format Block** (include in EVERY subagent prompt):

```
RESPONSE FORMAT: Be concise. Return ONLY:
- STATUS: PASS/FAIL
- FILES: list of files created/modified
- ERRORS: brief error description (omit if none)

DO NOT include:
- Step-by-step explanations of what you did
- Code snippets (they're in the files)
- Suggestions for next steps
- Restating the original task

For large outputs, WRITE TO DISK:
- Test results → logs/test-[feature].log
- Build output → logs/build-[phase].log
- Error traces → logs/error-[task].log
Return only: "Full output: logs/[filename].log"
```

**Good vs Bad Subagent Responses**:

```
❌ BAD (wastes context):
"I have successfully created the SummaryAgentService. First, I analyzed
the requirements and determined that we need to implement three methods:
summarize(), retry(), and handleError(). I created the file at
src/agents/summary-agent/summary-agent.service.ts with the following
implementation: [300 lines of code]. The service uses dependency
injection to receive the OllamaService. I also updated the module file
to register the service. You should now be able to run the tests..."

✅ GOOD (preserves context):
"STATUS: PASS
FILES: src/agents/summary-agent/summary-agent.service.ts (created),
       src/agents/summary-agent/summary-agent.module.ts (modified)
ERRORS: None"
```

**Disk-Based Communication for Large Data**:

| Data Type | Write To | Return |
|-----------|----------|--------|
| Test output (>20 lines) | `logs/test-[name].log` | "Tests: 47 passed. Full: logs/test-auth.log" |
| Build errors | `logs/build-[phase].log` | "Build FAIL. Details: logs/build-phase2.log" |
| Lint results | `logs/lint-[phase].log` | "Lint: 3 errors. See logs/lint-phase2.log" |
| Stack traces | `logs/error-[task].log` | "Error in X. Trace: logs/error-task.log" |
| Generated code review | `logs/review-[phase].md` | "Review complete. Report: logs/review-phase2.md" |

---

## Architecture

```
implement-plan (orchestrates full plan)
    │
    └── implement-phase (this skill - one phase at a time)
            │
            ├── 1. Implementation (subagents)
            ├── 2. Exit Condition Verification (build, lint, unit tests)
            ├── 3. Automated Integration Testing (Claude tests via API/Playwright)
            ├── 4. Code Review (code-review skill)
            ├── 5. ADR Compliance Check
            ├── 6. Plan Synchronization
            ├── 7. Prompt Archival (if prompt provided)
            └── 8. Phase Completion Report
```

## Design Principles

### Single Responsibility
This skill does ONE thing: execute a single phase completely and correctly.

### Extensibility
The phase execution pipeline is designed as a sequence of **steps**. New steps can be added without modifying the core logic. See [Phase Steps](#phase-steps-extensible).

### Quality Gates
Each step is a gate. If any gate fails, the phase cannot complete.

### Composability
This skill orchestrates other skills (code-review, adr) and can be extended to include more.

## Mandatory Exit Conditions

> **These conditions are NON-NEGOTIABLE. A phase cannot complete until ALL are satisfied.**

| Condition | Requirement | Rationale |
|-----------|-------------|-----------|
| **verification-loop PASS** | All 6 checks pass (Build, Type, Lint, Test, Security, Diff) | Code must compile, type-check, pass linting, tests, and security checks |
| **Integration tests PASS** | All API/UI tests pass | Feature must work end-to-end |
| **Code review PASS** | Clean PASS status (not PASS_WITH_NOTES) | No outstanding issues |
| **All recommendations fixed** | Every recommendation addressed | Recommendations are blocking, not optional |
| **ADR compliance PASS** | Follows existing ADRs, new decisions documented | Architectural consistency |
| **Plan verified** | All work items confirmed complete | Specification fulfilled |

### Why Recommendations Are Mandatory

```
❌ WRONG: "It's just a recommendation, we can fix it later"
❌ WRONG: "PASS_WITH_NOTES is good enough"
❌ WRONG: "We'll address it in the next phase"

✅ CORRECT: "Recommendations are blocking issues"
✅ CORRECT: "Only clean PASS allows phase completion"
✅ CORRECT: "Fix it now or the phase cannot complete"
```

**The Clean Baseline Principle requires:**
- Each phase ends with zero outstanding issues
- The next phase inherits a clean codebase
- Technical debt is not accumulated across phases
- Recommendations, if worth noting, are worth fixing

## Input Context

When invoked, this skill expects:

```
Plan Path: [path to plan file]
Phase: [number or name]
Task ID: [task_id from implement-plan's TaskList]
Prompt Path: [optional - path to pre-generated prompt from prompt-generator]
Changed Files: [optional - auto-detected if not provided]
Skip Steps: [optional - list of steps to skip, e.g., for testing]
TDD Mode: [enabled/disabled - from plan metadata, CLI flag, or global settings]
Coverage Threshold: [percentage - default 80%, applies when TDD mode enabled]
```

### Prompt Integration

If a **Prompt Path** is provided (from `prompt-generator` skill):

1. **Read the prompt file** - Contains detailed orchestration instructions
2. **Use prompt as primary guidance** - Follows established patterns and conventions
3. **Plan file as reference** - For exit conditions and verification steps
4. **Archive on completion** - Move prompt to `completed/` subfolder

```
# Prompt provides:
- Detailed orchestration workflow
- Subagent delegation patterns
- Specific task breakdowns
- Error handling guidance

# Plan provides:
- Exit conditions (source of truth)
- Success criteria
- Dependencies
```

## Phase Execution Pipeline

### ⚡ AUTO-CONTINUE RULES (READ THIS FIRST)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     AUTOMATIC CONTINUATION ENGINE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   RULE 1: After completing ANY step, IMMEDIATELY start the next step.   │
│   RULE 2: Do NOT output "waiting for input" or ask to continue.         │
│   RULE 3: Do NOT summarize and stop. Summarize and CONTINUE.            │
│   RULE 4: The ONLY valid stop point is after Step 8 completion.         │
│                                                                          │
│   EXECUTION ALGORITHM:                                                   │
│                                                                          │
│   current_step = 1                                                       │
│   while current_step <= 8:                                               │
│       result = execute_step(current_step)                                │
│       if result == PASS:                                                 │
│           current_step += 1          # AUTO-CONTINUE                     │
│       elif result == FAIL:                                               │
│           fix_and_retry(current_step) # Stay on step, fix, retry         │
│       elif result == BLOCKED:                                            │
│           return BLOCKED             # Only valid early exit             │
│   return COMPLETE                    # Only stop here                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### WHAT TO DO AFTER EACH STEP

| After Step | Status | YOUR IMMEDIATE ACTION |
|------------|--------|----------------------|
| Step 1 | PASS | **Execute Step 2 NOW** (invoke verification-loop) |
| Step 2 | PASS | **Execute Step 3 NOW** (run integration tests) |
| Step 3 | PASS | **Execute Step 4 NOW** (invoke code-review skill) |
| Step 4 | PASS | **Execute Step 5 NOW** (check ADR compliance) |
| Step 5 | PASS | **Execute Step 6 NOW** (verify plan sync) |
| Step 6 | PASS | **Execute Step 7 NOW** (archive prompt) |
| Step 7 | PASS | **Execute Step 8 NOW** (generate completion report) |
| Step 8 | DONE | **STOP** - Present report, await user |

**On FAIL at any step:** Fix the issue, re-run the SAME step, get PASS, then continue.

### NEVER DO THESE

```
❌ "Step 2 complete. Let me know when you want to continue."
❌ "Verification passed. Would you like me to proceed to Step 3?"
❌ "Code review done. Waiting for your input."
❌ "I've completed the exit conditions. What's next?"
❌ Outputting results without immediately starting the next step
❌ Asking permission to continue between steps 1-7
```

### ALWAYS DO THESE

```
✅ "Step 2 PASS. Executing Step 3: Integration Testing..."
✅ "Code review PASS. Now checking ADR compliance..."
✅ "Exit conditions verified. Running integration tests now..."
✅ Immediately invoke the next step's tools/skills after reporting status
✅ Chain steps together without pause
```

---

### Continuous Execution Details

> **The entire pipeline (Steps 1-8) MUST execute as one continuous flow.**

After EACH step completes (including skill invocations), **IMMEDIATELY proceed to the next step** WITHOUT waiting for user input.

**Pause Points (ONLY these):**

| Scenario | Action |
|----------|--------|
| Step returns BLOCKED status | Stop and present blocker to user |
| Step 8 (Completion Report) done | Await user confirmation before next phase |
| Maximum retries exhausted | Present failure and options to user |

**DO NOT PAUSE after:**
- Implementation complete → Continue to Step 2
- Exit conditions pass → Continue to Step 3
- Integration tests pass → Continue to Step 4
- Code review returns PASS → Continue to Step 5
- ADR compliance returns PASS → Continue to Step 6
- Plan sync complete → Continue to Step 7
- Prompt archived → Continue to Step 8
- Any successful step completion → Continue to next step
- Fix loop completes with PASS → Continue to next step

**Fix Loops (internal, no user pause):**
- Verification fails → Fix code, re-run verification, expect PASS
- Integration tests fail → Fix code, re-run tests, expect PASS
- Code review returns PASS_WITH_NOTES → Fix notes, re-run Step 4, expect PASS
- Code review returns NEEDS_CHANGES → Fix issues, re-run Step 4, expect PASS
- Any step has fixable issues → Spawn fix subagents, re-run step

**Continuous Flow Example:**
```
Step 1: Implementation → PASS
        ↓ (immediately)
Step 2: Exit Conditions → PASS
        ↓ (immediately)
Step 3: Automated Integration Testing → PASS
        ↓ (immediately)
Step 4: Code Review Skill → PASS_WITH_NOTES
        ↓ (fix loop - spawn subagents to fix notes)
        → Re-run Code Review → PASS
        ↓ (now continue)
Step 5: ADR Compliance → PASS
        ↓ (immediately)
Step 6: Plan Sync → PASS
        ↓ (immediately)
Step 7: Prompt Archival → PASS
        ↓ (immediately)
Step 8: Completion Report → Present to user
        ↓ (NOW wait for user confirmation)
```

**Goal: Clean PASS on all steps.** PASS_WITH_NOTES means there's work to do.

---

### Blocking Elements (ONLY Valid Reasons to Stop)

> **A blocking element is something YOU cannot fix autonomously.**

Do NOT stop for fixable issues. Only stop when you genuinely cannot proceed without user intervention.

**Valid Blocking Elements:**

| Blocker | Example | Action |
|---------|---------|--------|
| **Permission denied** | Subagent cannot write to protected directory | Ask user to adjust permissions or run in correct mode |
| **Infrastructure unavailable** | Cannot reach required LLM inference server | Report the connectivity issue, ask user to verify infrastructure |
| **Missing credentials** | API key not configured, auth token expired | Ask user to provide/refresh credentials |
| **External service down** | Third-party API returning 503 | Report the outage, ask if user wants to wait or skip |
| **Ambiguous requirements** | Plan says "integrate with payment system" but doesn't specify which | Ask user to clarify before proceeding |
| **Destructive operation** | Phase requires dropping production database | Confirm with user before executing |

**NOT Blocking (fix these yourself):**

| Issue | Action |
|-------|--------|
| Test fails | Fix the code, re-run test |
| Lint errors | Fix the code, re-run lint |
| Build errors | Fix the code, re-build |
| Type errors | Fix the types, re-check |
| Code review feedback | Fix the issues, re-run review |
| API returns error | Debug and fix the implementation |
| UI element not found | Fix selector or implementation |

**Blocker Protocol:**

When you hit a genuine blocker:

```
⛔ BLOCKED: [Brief description]

Phase: [N] - [Name]
Step: [Current step]
Blocker Type: [Permission | Infrastructure | Credentials | External | Ambiguous | Destructive]

Details:
[Specific details about what failed and why]

What I Need:
[Specific action required from user]

Options:
A) [Resolve the blocker and continue]
B) [Skip this verification and proceed with risk]
C) [Abort phase]
```

**Resume After Blocker:**

Once the user resolves the blocker, resume from the blocked step (not from Step 1).

---

### Step Completion Checklist (MANDATORY)

> **Before reporting phase complete, ALL steps must be executed.**

Use this checklist internally. If any step is missing, execute it before completing:

```
PHASE COMPLETION VERIFICATION:
- [ ] Step 1: Implementation - Subagents spawned, work completed
- [ ] Step 2: Exit Conditions - Build, runtime, unit tests all verified
- [ ] Step 3: Integration Testing - YOU tested via API calls or Playwright
- [ ] Step 4: Code Review - Achieved PASS (not PASS_WITH_NOTES)
- [ ] Step 5: ADR Compliance - Checked against relevant ADRs
- [ ] Step 6: Plan Sync - Work items verified, phase status updated
- [ ] Step 7: Prompt Archival - Archived or explicitly skipped (no prompt)
- [ ] Step 8: Completion Report - Generated and presented

⛔ VIOLATION: Stopping before Step 8
⛔ VIOLATION: Waiting for user input between Steps 1-7
⛔ VIOLATION: Reporting "phase complete" with unchecked steps
⛔ VIOLATION: Proceeding with PASS_WITH_NOTES without fixing notes
⛔ VIOLATION: Asking user to "manually test" instead of testing yourself
```

**Self-Check Protocol:**

After invoking a skill (like code-review), ask yourself:
1. Did the skill complete? → Check the result status
2. Did it return PASS? → CONTINUE to next step immediately
3. Did it return PASS_WITH_NOTES? → Spawn fix subagents, re-run step, expect PASS
4. Did it return NEEDS_CHANGES? → Spawn fix subagents, re-run step, expect PASS
5. Am I at Step 8? → If no, execute next step immediately
6. Did I test the feature myself? → If no, go back to Step 3

**The goal is always a clean PASS.** PASS_WITH_NOTES is not "good enough" - fix the notes.

---

### Progress Tracker (MANDATORY OUTPUT)

> **After EVERY step, you MUST output a Progress Tracker before doing ANYTHING else.**

This is not optional. The Progress Tracker forces explicit acknowledgment of state and next action.

**Format (output after each step completes):**

```
┌─────────────────────────────────────────┐
│ PROGRESS: Step [N] → Step [N+1]         │
├─────────────────────────────────────────┤
│ ✅ Step 1: Implementation    [DONE/SKIP]│
│ ✅ Step 2: Exit Conditions   [DONE/SKIP]│
│ ✅ Step 3: Integration Test  [DONE/SKIP]│
│ ✅ Step 4: Code Review       [DONE/SKIP]│
│ ⏳ Step 5: ADR Compliance    [CURRENT]  │
│ ⬚ Step 6: Plan Sync         [PENDING]  │
│ ⬚ Step 7: Prompt Archival   [PENDING]  │
│ ⬚ Step 8: Completion Report [PENDING]  │
├─────────────────────────────────────────┤
│ NEXT ACTION: [Describe what you do next]│
└─────────────────────────────────────────┘
```

**Rules:**
1. Output this tracker IMMEDIATELY after each step completes
2. Mark the CURRENT step you are about to execute
3. The NEXT ACTION must describe executing the next step (not waiting for user)
4. If NEXT ACTION says anything other than executing a step, you are VIOLATING the protocol

**Example - After Step 4 Code Review Returns PASS:**

```
┌─────────────────────────────────────────┐
│ PROGRESS: Step 4 → Step 5               │
├─────────────────────────────────────────┤
│ ✅ Step 1: Implementation    [DONE]     │
│ ✅ Step 2: Exit Conditions   [DONE]     │
│ ✅ Step 3: Integration Test  [DONE]     │
│ ✅ Step 4: Code Review       [DONE]     │
│ ⏳ Step 5: ADR Compliance    [CURRENT]  │
│ ⬚ Step 6: Plan Sync         [PENDING]  │
│ ⬚ Step 7: Prompt Archival   [PENDING]  │
│ ⬚ Step 8: Completion Report [PENDING]  │
├─────────────────────────────────────────┤
│ NEXT ACTION: Check ADR compliance now   │
└─────────────────────────────────────────┘
```

**⛔ VIOLATION Examples:**
- Not outputting the Progress Tracker after a step
- NEXT ACTION: "Waiting for user confirmation" (before Step 8)
- NEXT ACTION: "Let me know if you want me to continue"
- NEXT ACTION: "Please manually verify the feature works"
- Skipping to Step 8 without completing Steps 5-7

---

## Execution Contract (READ BEFORE STARTING)

> **⚠️ THIS IS A BINDING CONTRACT. VIOLATION = FAILURE.**

Before executing ANY step, internalize these rules:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION CONTRACT                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  I WILL execute Steps 1-8 as ONE continuous operation.                   │
│  I WILL NOT stop between steps (except Step 8 or BLOCKED).               │
│  I WILL invoke the next step's tools IMMEDIATELY after each step.        │
│  I WILL output a Progress Tracker after EVERY step.                      │
│  I WILL test the feature MYSELF in Step 3 (not ask the user).            │
│  I WILL NOT stop after Step 4 (code review) - there are 4 more steps.    │
│  I WILL NOT ask the user if they want me to continue.                    │
│  I WILL NOT ask the user to manually verify anything.                    │
│  I WILL only stop at Step 8 after presenting the Completion Report.      │
│  I WILL only stop early for genuine BLOCKING elements I cannot fix.      │
│                                                                          │
│  AFTER EACH STEP OUTPUT:                                                 │
│  ├── Output status (PASS/FAIL)                                           │
│  ├── Output Progress Tracker                                             │
│  └── IMMEDIATELY execute next step (no pause, no waiting)                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

If you find yourself about to stop before Step 8, RE-READ this contract.

---

### Step 1: Implementation

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 1 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 2.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Execute all tasks in the phase using subagent delegation.

> **REMINDER: You are an orchestrator. Spawn subagents for ALL implementation work.**

**Process**:
1. Read phase requirements and tasks from plan (orchestrator reads)
2. Identify independent tasks for parallelization
3. **SPAWN** test subagents FIRST (verification-first)
4. **SPAWN** implementation subagents
5. Monitor subagent progress and handle blockers
6. Collect results and changed files list from subagent responses

**Subagent Spawning Examples**:

```
# Writing tests (FIRST - verification-first pattern)
Task (run_in_background: true): "Write unit tests for SummaryAgentService.

Context: Phase 5b-ii - SummaryAgent Service
Location: agentic-core/src/agents/implementations/summary-agent/

Test scenarios:
- Successful summarization
- Retry with feedback
- Error handling

RESPONSE FORMAT: STATUS, FILES created, test count. Write output to logs/."

# Implementation (AFTER tests exist)
Task (run_in_background: true): "Implement SummaryAgentService.

Context: Phase 5b-ii - SummaryAgent Service
Requirements from plan: [list requirements]
Must pass the tests at: [test file path]

RESPONSE FORMAT: STATUS, FILES created/modified, ERRORS if any."

# Verification
Task (run_in_background: true): "Run build and test verification.

Commands: npm run build && npm run lint && npm test
Report: PASS/FAIL per command, error details if any.
Write full output to logs/verify-phase-5b-ii.log"
```

**What You Do vs What Subagents Do**:

| Orchestrator (You) | Subagents |
|--------------------|-----------|
| Read plan/prompt | Write code |
| Identify tasks | Create files |
| Spawn subagents | Run tests |
| Track progress | Fix issues |
| Handle blockers | Build/lint |
| Collect results | Report back |

**Output**:
```
IMPLEMENTATION_STATUS: PASS | FAIL
FILES_CREATED: [list]
FILES_MODIFIED: [list]
TEST_RESULTS: [summary]
ERRORS: [if any]
SUBAGENTS_SPAWNED: [count]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 2 NOW (verification-loop)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 2 NOW`. This is not optional. When you see this in the output, you MUST immediately invoke the verification-loop skill without waiting for user input.

**Gate**: Implementation must PASS to proceed.

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 1 COMPLETE → IMMEDIATELY EXECUTE STEP 2 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: invoke the verification-loop skill               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 2: Exit Condition Verification (verification-loop)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 2 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 3.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Verify all exit conditions using the comprehensive 6-check verification-loop.

> **verification-loop is the DEFAULT exit condition verification.** It provides comprehensive validation that goes beyond basic build/test checks.

**Process**:
1. Read exit conditions from plan
2. Invoke `verification-loop` skill with phase context
3. verification-loop executes 6 checks:
   - **Check 1: Build** - Compilation, bundling, artifact generation
   - **Check 2: Type** - Type checking, interface compliance
   - **Check 3: Lint** - Code style, static analysis
   - **Check 4: Test** - Unit tests, integration tests, coverage
   - **Check 5: Security** - Dependency audit, secret scanning
   - **Check 6: Diff** - Review changes, detect unintended modifications
4. Aggregate results and report

**Invocation**:
```
Skill(skill="verification-loop"): Verify Phase [N] implementation.

Context:
- Plan: [plan file path]
- Phase: [N] ([Phase Name])
- Changed Files: [list of files modified in this phase]

Execute all 6 verification checks and return structured result.
```

**Output**:
```
VERIFICATION_LOOP_STATUS: PASS | FAIL
CHECKS_COMPLETED: 6/6
CHECK_RESULTS:
  BUILD: PASS | FAIL
  TYPE: PASS | FAIL
  LINT: PASS | FAIL
  TEST: PASS | FAIL
  SECURITY: PASS | FAIL
  DIFF: PASS | FAIL
FAILED_CHECKS: [list if any]
EVIDENCE: logs/verification-loop-phase-N.log
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 3 NOW (Integration Testing)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 3 NOW`. This is not optional. When you see this in the output, you MUST immediately execute Step 3 without waiting for user input.

**Gate**: ALL 6 verification checks must PASS to proceed.

**On Failure**: Spawn fix subagents for failed checks, re-run verification-loop, repeat until all pass or escalate.

**Disabling verification-loop** (not recommended):
```yaml
# In plan metadata - only for special cases
phase_config:
  verification_loop: false  # Falls back to basic exit conditions
```

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 2 COMPLETE → IMMEDIATELY EXECUTE STEP 3 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: run integration tests (Step 3)                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 3: Automated Integration Testing

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 3 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 4.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Verify the implementation works end-to-end through automated testing performed by YOU, not the user.

> **YOU are the tester.** Do not ask the user to manually verify. Use tools to test the system yourself.

> **For UI Testing**: Use the `browser-verification-agent` - spawn ONE agent per test scenario for context preservation. The agent wraps Playwright MCP and returns structured evidence.

**Process**:
1. Determine the testing approach based on implementation type:
   - **Backend/API**: Use curl, httpie, or spawn subagent to make API calls
   - **Frontend/UI**: Spawn `browser-verification-agent` for each test scenario
   - **CLI tools**: Execute commands and verify output
   - **Libraries**: Write and run integration test scripts
2. Spawn testing subagents for each verification scenario (ONE test per agent for UI)
3. Capture results and any failures
4. On failure: spawn fix subagents, re-test

**Testing by Implementation Type**:

| Type | Testing Method | Tools/Agents |
|------|----------------|--------------|
| REST API | Make HTTP requests, verify responses | curl, httpie, fetch |
| GraphQL | Execute queries/mutations | curl with GraphQL payload |
| Web UI | Navigate, interact, assert | `browser-verification-agent` |
| Database | Query and verify data | psql, mysql, prisma |
| Background jobs | Trigger and verify completion | API calls + polling |
| File processing | Provide input, check output | Bash, Read tool |

**Subagent Examples**:

```
# API Testing (general-purpose subagent)
Task: "Test the new /api/users endpoint.

Make these API calls and report results:
1. POST /api/users with valid payload - expect 201
2. POST /api/users with invalid email - expect 400
3. GET /api/users/:id - expect 200 with user data
4. GET /api/users/nonexistent - expect 404

RESPONSE FORMAT: STATUS, test results summary, ERRORS if any."

# UI Testing (browser-verification-agent) - ONE test per agent spawn
Task(subagent_type="browser-verification-agent"): "Verify login with valid credentials.

base_url: http://localhost:3000
test_description: Navigate to /login, enter 'test@example.com' in email field,
                  enter 'password123' in password field, click Login button
expected_outcome: URL changes to /dashboard, welcome message visible
session_context: fresh"

Task(subagent_type="browser-verification-agent"): "Verify login with invalid credentials.

base_url: http://localhost:3000
test_description: Navigate to /login, enter 'test@example.com' in email field,
                  enter 'wrongpassword' in password field, click Login button
expected_outcome: Error message 'Invalid credentials' is displayed, URL stays on /login
session_context: fresh"
```

**UI Testing Response Format** (from browser-verification-agent):
```
STATUS: PASS | FAIL | FLAKY | BLOCKED
SCREENSHOT: logs/screenshots/2026-01-23-143022-login-test.png
OBSERVED: [what actually happened]
EXPECTED: [echo of expected_outcome]
ERRORS: [if any]
```

**Aggregated Output** (for Step 3 completion):
```
INTEGRATION_TEST_STATUS: PASS | FAIL
TESTS_RUN: [count]
TESTS_PASSED: [count]
TESTS_FAILED: [count]
FAILURE_DETAILS: [if any]
EVIDENCE: [log files, screenshots]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 4 NOW (Code Review)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 4 NOW`. This is not optional. When you see this in the output, you MUST immediately invoke the code-review skill without waiting for user input.

**Gate**: Integration tests must PASS to proceed.

**On Failure**:
1. Analyze failure root cause
2. Spawn fix subagents
3. Re-run failed tests
4. Repeat until pass or hit blocking element

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 3 COMPLETE → IMMEDIATELY EXECUTE STEP 4 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: invoke the code-review skill                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 4: Code Review

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 4 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 5.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Validate implementation quality across all dimensions.

**Process**:
1. Invoke `code-review` skill with phase context
2. Provide: plan path, phase number, changed files
3. Receive structured review result

**Output**:
```
CODE_REVIEW_STATUS: PASS | PASS_WITH_NOTES | NEEDS_CHANGES
BLOCKING_ISSUES: [count]
RECOMMENDATIONS: [list]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 5 NOW (ADR Compliance)
```

> **CRITICAL**: When CODE_REVIEW_STATUS is PASS, the output MUST include `NEXT_STEP: EXECUTE STEP 5 NOW`. This is not optional. When you see this in the output, you MUST immediately check ADR compliance without waiting for user input.

**Gate**: Code review must be **PASS** to proceed. PASS_WITH_NOTES is NOT acceptable.

> ⚠️ **MANDATORY: All Recommendations Must Be Fixed**
>
> This is a **non-negotiable exit condition**. PASS_WITH_NOTES means there are recommendations that MUST be addressed before the phase can complete.
>
> - Recommendations are NOT optional suggestions
> - Recommendations are NOT "nice to have"
> - Recommendations are **blocking issues** that must be resolved
> - The only acceptable code review status is **PASS**

**On PASS_WITH_NOTES or NEEDS_CHANGES**:
1. Spawn fix subagents to address ALL issues (blocking issues AND recommendations)
2. Re-run code review
3. Repeat until clean **PASS** (max 3 retries)
4. Escalate to user only if max retries exhausted

**Why are recommendations mandatory?**
- Recommendations indicate pattern violations, missing tests, or technical debt
- Leaving them unfixed accumulates debt that compounds across phases
- The "Clean Baseline Principle" requires each phase to end clean
- Future phases inherit our mess if we don't fix it now
- Consistency: if it's worth noting, it's worth fixing

---

> ⚠️ **CRITICAL TRANSITION POINT - DO NOT STOP HERE** ⚠️
>
> After code-review skill returns, you MUST continue. This is the #1 failure point.
> - Code review returned PASS? → Output Progress Tracker → Execute Step 5 NOW
> - Code review returned PASS_WITH_NOTES? → Fix issues → Re-run → Get PASS → Execute Step 5
> - DO NOT report to user and wait. DO NOT ask if they want to continue.
> - The phase is NOT complete. You have 4 more steps to execute.

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 4 COMPLETE → IMMEDIATELY EXECUTE STEP 5 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: check ADR compliance                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 5: ADR Compliance Check

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 5 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 6.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Ensure architectural decisions are followed and documented.

**Process**:
1. Read `docs/decisions/INDEX.md` to identify relevant ADRs
2. Check implementation against applicable ADRs
3. Identify any new architectural decisions made during implementation
4. If new decisions found, invoke `adr` skill to document them

**Output**:
```
ADR_COMPLIANCE_STATUS: PASS | NEEDS_DOCUMENTATION
APPLICABLE_ADRS: [list]
COMPLIANCE_RESULTS: [per-ADR status]
NEW_DECISIONS_DOCUMENTED: [list of new ADR numbers, if any]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 6 NOW (Plan Synchronization)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 6 NOW`. This is not optional. When you see this in the output, you MUST immediately verify plan synchronization without waiting for user input.

**Gate**: ADR compliance must PASS to proceed.

**On NEEDS_DOCUMENTATION**: Invoke `adr` skill for each undocumented decision.

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 5 COMPLETE → IMMEDIATELY EXECUTE STEP 6 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: verify plan synchronization                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 6: Plan Synchronization

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 6 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 7.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Verify work items completed and update plan status.

**Process**:
1. Verify all work items for this phase were completed
2. Add ADR references if new ADRs were created
3. Note any deviations from original plan
4. Mark phase status as complete (add ✅ to phase header)

**Note**: Per ADR-0001, plans are specification documents. Progress is tracked via Task tools, not by modifying checkboxes in the plan file.

**Output**:
```
PLAN_SYNC_STATUS: PASS | FAIL
WORK_ITEMS_VERIFIED: [count]
DEVIATIONS_NOTED: [count]
ADR_REFERENCES_ADDED: [count]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 7 NOW (Prompt Archival)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 7 NOW`. This is not optional. When you see this in the output, you MUST immediately archive the prompt (or skip if none) without waiting for user input.

**Gate**: Plan sync must complete successfully.

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 6 COMPLETE → IMMEDIATELY EXECUTE STEP 7 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: archive the prompt (if provided)                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 7: Prompt Archival

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 7 - This is part of a continuous 8-step pipeline.            ║
║    When this step completes with PASS, IMMEDIATELY execute Step 8.            ║
║    Do NOT stop. Do NOT wait for user input.                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Archive the phase prompt to the completed folder (if prompt was provided).

**Process**:
1. Check if a prompt file was used for this phase
2. If yes, move to `completed/` subfolder:
   ```bash
   # Create completed folder if it doesn't exist
   mkdir -p docs/prompts/completed

   # Move the prompt file
   mv docs/prompts/phase-2-data-pipeline.md docs/prompts/completed/
   ```
3. Log the archival

**Output**:
```
PROMPT_ARCHIVAL_STATUS: PASS | SKIPPED | FAIL
PROMPT_FILE: [original path]
ARCHIVED_TO: [new path in completed/]
─────────────────────────────────────────────────
⚡ NEXT_STEP: EXECUTE STEP 8 NOW (Completion Report)
```

> **CRITICAL**: The output MUST include `NEXT_STEP: EXECUTE STEP 8 NOW`. This is not optional. When you see this in the output, you MUST immediately generate the completion report without waiting for user input.

**Gate**: Non-blocking (failure logged but doesn't stop completion).

**Why Archive?**
- Prevents re-using the same prompt accidentally
- Creates a record of completed work
- Keeps the prompts folder clean for pending work
- Allows review of what instructions were used

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ✅ STEP 7 COMPLETE → IMMEDIATELY EXECUTE STEP 8 NOW                           ║
║    Do NOT output results and wait. Do NOT ask "shall I continue?"             ║
║    Your next action MUST be: generate the completion report                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 8: Phase Completion Report

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ ⏩ ENTERING STEP 8 (FINAL STEP) - This completes the pipeline.                ║
║    After generating the completion report, the phase is DONE.                 ║
║    You may NOW stop and await user input for the next phase.                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Responsibility**: Generate summary for orchestrator and user.

**Output Format**:
```
═══════════════════════════════════════════════════════════════
● PHASE [N] COMPLETE: [Phase Name]
═══════════════════════════════════════════════════════════════

Implementation:
  Files Created: [count] ([file list])
  Files Modified: [count] ([file list])
  Tests: [X passing, Y failing]

Exit Conditions:
  Build: ✅ PASS
  Runtime: ✅ PASS
  Unit Tests: ✅ PASS

Integration Testing (performed by Claude):
  API Tests: ✅ [X/Y passed] (or N/A)
  UI Tests: ✅ [X/Y passed] (or N/A)
  Evidence: logs/integration-test-phase-N.log

Code Review:
  Status: ✅ PASS (all recommendations addressed)
  Blocking Issues: 0
  Recommendations Fixed: [count]

ADR Compliance:
  Status: ✅ PASS
  Applicable ADRs: [list]
  New ADRs Created: [list or "None"]

Plan Updated:
  Work Items Verified: [count]
  Phase Status: ✅ Complete
  Task Status: completed (via TaskUpdate)

Prompt:
  Status: ✅ Archived (or ⏭️ Skipped - no prompt provided)
  Archived To: docs/prompts/completed/phase-2-data-pipeline.md

User Verification (only if truly not automatable):
  [None - all verification automated]
  OR
  - [ ] [Physical hardware check]
  - [ ] [Third-party dashboard verification]

Learnings Captured:
  Status: ✅ Extracted
  Patterns Found: [count]
  Saved To: ~/.claude/skills/learned/

═══════════════════════════════════════════════════════════════
PHASE STATUS: ✅ COMPLETE - Ready for next phase
═══════════════════════════════════════════════════════════════
```

> **Note on User Verification**: This section should almost always be empty. Claude performs integration testing in Step 3. Only include items here that genuinely require human eyes (e.g., "verify email arrived in inbox", "check physical device display").

**🛑 STOP POINT**: This is the ONLY valid stopping point in the entire pipeline.

After outputting the Completion Report:
1. Output final Progress Tracker showing all steps ✅ DONE
2. **Invoke continuous-learning skill** to capture patterns from this phase
3. Present the report to the user
4. NOW (and ONLY now) await user confirmation before proceeding to next phase

### Continuous Learning at Phase Boundary

> **Phase completion is a natural learning boundary.** Always invoke continuous-learning here.

**Why invoke here?**
- User may `/clear` or `/compact` before next phase
- Patterns from implementation are fresh and detailed
- Captures decisions, fixes, and approaches while context is complete
- Prevents loss of valuable learnings

**Invocation:**
```
Skill(skill="continuous-learning"): Extract patterns from Phase [N] completion.

Context:
- Phase: [N] ([Phase Name])
- Files Changed: [list]
- Key Decisions: [any architectural choices made]
- Issues Resolved: [problems fixed during implementation]
- Approaches Used: [patterns and techniques applied]

Extract valuable patterns for future sessions.
```

**Output** (appended to completion report):
```
Learnings Captured:
  Patterns Extracted: [count]
  Saved To: ~/.claude/skills/learned/
```

```
YOU HAVE REACHED THE END OF THE PHASE PIPELINE.
THIS IS THE ONLY PLACE WHERE YOU MAY STOP AND WAIT FOR USER INPUT.
```

---

## Progress Tracking

Progress is tracked via **Task tools**, not checkboxes. See [ADR-0001](../../docs/decisions/ADR-0001-separate-plan-spec-from-progress-tracking.md).

- Task status is managed by implement-plan (in_progress when starting, completed when done)
- Plan files remain pure specification documents
- Step 6 verifies work items but does not modify plan checkboxes

---

## Phase Steps (Extensible)

The execution pipeline is defined as an ordered list of steps. This design allows easy extension:

```
PHASE_STEPS = [
  { name: "implementation", required: true, skill: null },
  { name: "exit_conditions", required: true, skill: null },
  { name: "integration_testing", required: true, skill: null },  // Claude tests via API/Playwright
  { name: "code_review", required: true, skill: "code-review" },
  { name: "adr_compliance", required: true, skill: "adr" },
  { name: "plan_sync", required: true, skill: null },
  { name: "prompt_archival", required: false, skill: null },
  { name: "completion_report", required: true, skill: null },
]
```

### Adding New Steps

To add a new step (e.g., security scan, performance check):

1. Define the step with its gate criteria
2. Add to the pipeline at appropriate position
3. Implement the step logic or delegate to a skill

**Example - Adding Security Scan**:
```
{ name: "security_scan", required: false, skill: "security-scan" }
```

### Conditional Steps

Steps can be conditional based on:
- Phase type (e.g., only run security scan on auth phases)
- Configuration flags
- Plan metadata

```
if (phase.metadata.security_sensitive) {
  run_step("security_scan")
}
```

## Optional Skill Steps

Optional steps can be added to the phase execution pipeline when needed. These steps are **not run by default** and must be explicitly enabled via plan metadata or configuration.

### Optional Steps Overview

| Step | Skill | Purpose | Default |
|------|-------|---------|---------|
| Security Review | `security-review` | Comprehensive OWASP security audit | Disabled |

> **Note**: `verification-loop` is NOT optional - it is the default exit condition verification in Step 2.

**Key characteristics:**
- Not included in standard pipeline execution
- Enabled via plan metadata `optional_steps` configuration
- Can be enabled globally or per-phase
- Integrate at specific points in the pipeline

### Security Review Step

**Skill**: `security-review`

**Purpose**: Comprehensive security audit for implementations that handle sensitive operations, user data, or security-critical code paths.

**When to enable:**
- Authentication and authorization code
- User input handling and validation
- API endpoints exposed to external clients
- Secrets management and credential handling
- Payment processing or financial transactions
- Personal data processing (PII, PHI)
- Cryptographic operations

**How to enable:**
```yaml
# In plan metadata
phase_config:
  optional_steps:
    security_review: true
```

**Integration point**: After Step 4 (Code Review), before Step 5 (ADR Compliance)

```
Step 1: Implementation
Step 2: Exit Conditions
Step 3: Integration Testing
Step 4: Code Review
Step 4.5: Security Review ← INSERTED HERE
Step 5: ADR Compliance
Step 6: Plan Sync
Step 7: Prompt Archival
Step 8: Completion Report
```

**Expected output format:**
```
SECURITY_REVIEW_STATUS: PASS | FAIL | NEEDS_REMEDIATION
VULNERABILITIES_FOUND: [count]
SEVERITY_BREAKDOWN:
  CRITICAL: [count]
  HIGH: [count]
  MEDIUM: [count]
  LOW: [count]
ISSUES:
  - [severity] [category]: [description]
RECOMMENDATIONS: [list]
COMPLIANCE_CHECKS: [list of standards checked, e.g., OWASP Top 10]
```

**Gate behavior**: Security review must PASS to proceed. NEEDS_REMEDIATION triggers fix subagents, then re-review.

### Enabling Security Review

Security review can be enabled for phases that handle sensitive operations.

**Example configuration:**
```yaml
# In plan metadata
phase_config:
  optional_steps:
    security_review: true
```

**Execution order with security review enabled:**
```
Step 1: Implementation
Step 2: Exit Conditions (verification-loop - always runs)
Step 3: Integration Testing
Step 4: Code Review
Step 4.5: Security Review (if enabled)
Step 5: ADR Compliance
Step 6: Plan Sync
Step 7: Prompt Archival
Step 8: Completion Report
```

**Per-phase overrides:**
```yaml
# Enable globally but override for specific phases
phase_config:
  optional_steps:
    security_review: true

phases:
  - name: "Database Schema"
    # Inherits security_review: true from global config

  - name: "Static Content"
    optional_steps:
      security_review: false  # Override: skip for this phase
```

## Invocation

### From implement-plan (primary use)

```
Skill(skill="implement-phase"): Execute Phase 2 of the implementation plan.

Context:
- Plan: docs/plans/auth-implementation.md
- Phase: 2 (Authentication Service)
- Previous Phase Status: Complete

Execute all quality gates and return structured result.
```

### Manual Invocation

```
/implement-phase docs/plans/my-plan.md phase:3
```

Or interactively:
```
/implement-phase

> Which plan? docs/plans/auth-implementation.md
> Which phase? 2
```

## Return Value

When called by implement-plan, return structured result:

```
PHASE_RESULT:
  phase_number: 2
  phase_name: "Authentication Service"
  task_id: [task_id from input context]
  task_status: "completed"
  status: COMPLETE | FAILED | BLOCKED

  steps:
    implementation: PASS
    exit_conditions: PASS
    integration_testing: PASS
    code_review: PASS
    adr_compliance: PASS
    plan_sync: PASS
    prompt_archival: PASS | SKIPPED

  files_changed:
    created: [list]
    modified: [list]

  integration_tests:
    api_tests: { passed: X, failed: 0 }
    ui_tests: { passed: Y, failed: 0 }
    evidence: "logs/integration-test-phase-2.log"

  new_adrs: [list or empty]

  prompt:
    used: true | false
    original_path: "docs/prompts/phase-2-data-pipeline.md"
    archived_to: "docs/prompts/completed/phase-2-data-pipeline.md"

  code_review_details:
    blocking_issues_found: [count]
    blocking_issues_fixed: [count]
    recommendations_found: [count]
    recommendations_fixed: [count]  # Must equal recommendations_found

  user_verification:  # Should usually be empty
    []
    # Only include items that truly cannot be automated, e.g.:
    # - "Verify physical device display"
    # - "Check email arrived in inbox"

  learnings:
    patterns_extracted: [count]
    saved_to: "~/.claude/skills/learned/"

  ready_for_next: true | false
  blocker: null | "description of blocker"
```

## Error Handling

### Step Failures

When a step fails:

1. **Log failure details** with full context
2. **Attempt automatic fix** if possible (spawn fix subagent)
3. **Re-run the step** after fix
4. **Escalate to user** if fix fails or requires decision

### Maximum Retries

Each step has a retry limit (default: 3). After exhausting retries:

```
⛔ PHASE BLOCKED: [Step Name] failed after 3 attempts

Last Error: [error details]

Options:
A) Retry with different approach
B) Skip this step (if non-blocking)
C) Abort phase and return to plan

How should I proceed?
```

### Blocker Protocol

When a blocker is encountered:

1. **STOP** all pending work
2. **PRESERVE** state for resume
3. **REPORT** to orchestrator with full context
4. **AWAIT** decision

## Integration with Other Skills

### code-review

Called in Step 3. Receives phase context, returns structured review.

### adr

Called in Step 4 when:
- New architectural decisions need documentation
- Compliance check identifies undocumented decisions

### Future Integrations

The extensible step design allows adding:
- `security-scan` - Security vulnerability scanning
- `performance-check` - Performance regression testing
- `documentation-update` - Auto-update relevant docs
- `changelog-entry` - Add to CHANGELOG.md

## Configuration

Phase behavior can be configured via plan metadata or global settings:

```yaml
# In plan file
phase_config:
  strict_mode: true          # Fail on any warning
  skip_steps: []             # Steps to skip
  additional_steps: []       # Extra steps to run
  retry_limit: 3             # Max retries per step
  tdd_mode: false            # Enable TDD (Test-Driven Development) mode
  coverage_threshold: 80     # Minimum code coverage percentage (TDD mode)

# Global settings (~/.claude/settings.json)
implement_phase:
  default_retry_limit: 3
  always_run_security: false
  require_adr_for_decisions: true
  default_tdd_mode: false
  default_coverage_threshold: 80
```

## TDD Mode (Optional)

### TDD Mode Overview

TDD (Test-Driven Development) mode inverts the traditional implementation flow by requiring tests to be written before implementation code. This approach ensures:

- **Higher test coverage**: Tests are not an afterthought
- **Better design**: Writing tests first forces cleaner interfaces
- **Confidence**: Every line of production code exists to make a test pass
- **Documentation**: Tests serve as executable specifications

**When to enable TDD mode:**
- Building new features with well-defined requirements
- Implementing business logic with clear acceptance criteria
- Working on code that requires high reliability
- When the plan specifies TDD as a requirement

**How it modifies the implementation flow:**
In normal mode, Step 1 spawns implementation subagents first, then test subagents. In TDD mode, this order is reversed, and an additional verification step ensures tests fail before implementation.

### Enabling TDD Mode

**Via plan metadata:**
```yaml
# In plan file metadata section
phase_config:
  tdd_mode: true
  coverage_threshold: 80  # Optional, defaults to 80%
```

**Via command line flag:**
```
/implement-phase docs/plans/my-plan.md phase:3 --tdd
```

**Via global settings:**
```yaml
# ~/.claude/settings.json
implement_phase:
  default_tdd_mode: true
  default_coverage_threshold: 80
```

### RED → GREEN → REFACTOR Cycle

TDD follows the classic three-phase cycle:

```
┌─────────────────────────────────────────────────────────────┐
│                    TDD CYCLE                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌───────┐         ┌───────┐         ┌──────────┐        │
│    │  RED  │ ──────► │ GREEN │ ──────► │ REFACTOR │        │
│    └───────┘         └───────┘         └──────────┘        │
│        │                                     │              │
│        └─────────────────────────────────────┘              │
│                    (repeat)                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ RED:      Write a failing test that defines desired behavior│
│ GREEN:    Write minimal code to make the test pass          │
│ REFACTOR: Improve code quality while keeping tests green    │
└─────────────────────────────────────────────────────────────┘
```

**RED Phase:**
- Write test(s) that describe the expected behavior
- Tests MUST fail initially (this proves they test something real)
- If tests pass immediately, either the test is wrong or the feature already exists

**GREEN Phase:**
- Write the minimum code necessary to make the test pass
- Do not add extra functionality "just in case"
- Ugly code is acceptable at this stage - it will be refactored

**REFACTOR Phase:**
- Improve code structure, naming, and design
- Remove duplication
- Tests must remain green throughout refactoring
- If tests fail, you've broken something - revert and try again

### Step 1 Modifications for TDD

**Normal Flow (TDD disabled):**
```
Step 1: Implementation
├── 1a. Read phase requirements
├── 1b. Spawn IMPLEMENTATION subagents
├── 1c. Spawn TEST subagents
└── 1d. Verify tests pass
```

**TDD Flow (TDD enabled):**
```
Step 1: Implementation (TDD Mode)
├── 1a. Read phase requirements
├── 1b. Spawn TEST subagents FIRST (RED)
├── 1c. Verify tests FAIL (proves tests are valid)
├── 1d. Spawn IMPLEMENTATION subagents (GREEN)
├── 1e. Verify tests PASS
├── 1f. Spawn REFACTOR subagents (optional)
└── 1g. Verify tests still PASS
```

**Subagent Spawning Order Changes:**

| Step | Normal Mode | TDD Mode |
|------|-------------|----------|
| First | Implementation code | Test code |
| Second | Test code | Verify tests fail (RED) |
| Third | Verify tests pass | Implementation code (GREEN) |
| Fourth | - | Verify tests pass |
| Fifth | - | Refactor (optional) |

**TDD Subagent Examples:**

```
# Step 1b: Write failing tests FIRST (RED)
Task (run_in_background: true): "Write unit tests for UserAuthService.

Context: Phase 3 - User Authentication (TDD Mode - RED phase)
Location: src/auth/user-auth.service.spec.ts

Test scenarios (from requirements):
- authenticateUser() returns token for valid credentials
- authenticateUser() throws UnauthorizedError for invalid password
- authenticateUser() throws NotFoundError for unknown user
- refreshToken() extends session for valid refresh token

IMPORTANT: Implementation does NOT exist yet. Tests MUST fail.
Write tests that will drive the implementation.

RESPONSE FORMAT: STATUS, FILES created, test count, ERRORS if any."

# Step 1c: Verify tests fail
Task: "Run tests and verify they FAIL.

Command: npm test -- --testPathPattern=user-auth.service.spec.ts
Expected: Tests should FAIL (RED phase of TDD)

If tests PASS, there is a problem - either tests are wrong or feature already exists.

RESPONSE FORMAT: STATUS (expect FAIL), test count, failure summary."

# Step 1d: Write minimal implementation (GREEN)
Task (run_in_background: true): "Implement UserAuthService to pass tests.

Context: Phase 3 - User Authentication (TDD Mode - GREEN phase)
Location: src/auth/user-auth.service.ts
Tests at: src/auth/user-auth.service.spec.ts

Write MINIMAL code to make all tests pass. Do not add extra functionality.
Follow the interface defined by the tests.

RESPONSE FORMAT: STATUS, FILES created/modified, ERRORS if any."
```

### Coverage Verification

TDD mode enforces a minimum code coverage threshold (default: 80%).

**How coverage is checked:**
1. After Step 1 completes, spawn a coverage verification subagent
2. Run tests with coverage reporting enabled
3. Parse coverage report and compare against threshold
4. Fail the phase if coverage is below threshold

**Coverage Subagent Example:**
```
Task: "Verify code coverage meets TDD threshold.

Commands:
1. npm test -- --coverage --coverageReporters=text
2. Parse coverage percentage from output

Threshold: 80%
Scope: Files created/modified in this phase

RESPONSE FORMAT:
STATUS: PASS | FAIL
COVERAGE: [percentage]%
UNCOVERED_LINES: [count]
DETAILS: [brief summary or path to full report]"
```

**Handling coverage failures:**
1. Identify uncovered lines/branches
2. Spawn subagent to add missing tests
3. Re-run coverage check
4. Repeat until threshold met or max retries exhausted

```
COVERAGE_STATUS: FAIL
COVERAGE: 72%
THRESHOLD: 80%
UNCOVERED:
  - src/auth/user-auth.service.ts: lines 45-52 (error handling)
  - src/auth/user-auth.service.ts: lines 78-80 (edge case)

ACTION: Spawning subagent to add tests for uncovered code paths...
```

### TDD Mode Checklist

Before marking Step 1 as complete in TDD mode, verify:

```
TDD VERIFICATION CHECKLIST:
- [ ] Tests written BEFORE implementation code
- [ ] Tests failed initially (RED phase verified)
- [ ] Minimal code written to pass tests (GREEN phase)
- [ ] Refactoring done with passing tests (REFACTOR phase)
- [ ] Coverage threshold met (default: 80%)
- [ ] No implementation code without corresponding tests
```

**Step 1 Output (TDD Mode):**
```
IMPLEMENTATION_STATUS: PASS
TDD_MODE: enabled
TDD_PHASES:
  RED: VERIFIED (tests failed as expected)
  GREEN: PASS (all tests now passing)
  REFACTOR: PASS (tests still green)
COVERAGE: 85% (threshold: 80%)
FILES_CREATED: [list]
FILES_MODIFIED: [list]
TEST_RESULTS: 12 passing, 0 failing
ERRORS: None
```

## Best Practices

### For implement-plan Authors

1. Provide complete phase context when calling
2. Trust the structured return value
3. Handle BLOCKED status appropriately
4. Present manual verification steps to user

### For Direct Users

1. Ensure plan file is up-to-date before running
2. Have ADR INDEX.md available
3. Review manual verification steps carefully
4. Check recommendations even on PASS_WITH_NOTES

### For Step Developers

1. Each step must have clear PASS/FAIL criteria
2. Steps should be idempotent (safe to re-run)
3. Provide detailed error messages
4. Log sufficient context for debugging
