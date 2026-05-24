---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session - dispatches fresh subagent for each task with code review between tasks, enabling fast iteration with quality gates
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with code review after each.

**Core principle:** Fresh subagent per task + review between tasks = high quality, fast iteration

**Autonomy principle:** Execute ALL tasks without stopping for user input. Only stop on 3 consecutive errors OR all tasks complete. Commits, reviews, and fixes are subagent responsibilities — orchestrator never pauses to ask permission.

**Orchestrator identity:** You are a DISPATCHER, not a researcher. You read TaskList, dispatch subagents, process their results, and loop. Subagents self-gather all context specified in the plan (task details, related files, external references). You NEVER read plan files, gather context, explore code, or check git state yourself.

## Overview

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Code review after each task (catch issues early)
- Faster iteration (no human-in-loop between tasks)

**When to use:**
- Staying in this session
- Tasks are mostly independent
- Want continuous progress with quality gates

**When NOT to use:**
- Need to review plan first (use executing-plans)
- Tasks are tightly coupled (manual execution better)
- Plan needs revision (brainstorm first)

## The Process

**File Organization:**
- Task result files save to `{{epic-or-user-story-folder}}/tasks/` subfolder
- This pattern applies to BOTH epic-level (`epic{{X}}-{{name}}/tasks/`) AND user-story-level (`us{{X.Y}}-{{name}}/tasks/`) implementations

### 1. Loop Through Task List

**The orchestrator loop — repeat until all tasks complete or 3 consecutive errors:**

```text
consecutive_errors = 0

1. Read TaskList
2. Find next task: first in_progress, then first pending (not blocked)
3. If no tasks remain → go to Step 6 (Final Review)
4. Mark task in_progress via TaskUpdate
5. Dispatch implementation subagent (Step 2)
6. Dispatch code-reviewer subagent (Step 3)
7. Cleanup processes (Step 3a)
8. Check verdict:
   - APPROVED → continue to step 9
   - FIX REQUIRED → dispatch fix subagent (Step 4) → GOTO step 6 (re-review)
9. MANDATORY: Close GitHub issue (Step 5) [if task has issue number - DO NOT skip this]
10. Mark task completed via TaskUpdate ← ONLY after APPROVED
11. GOTO 1
```

**CRITICAL: Task stays in_progress until code-reviewer returns APPROVED. Never mark complete on FIX REQUIRED.**

**Pre-flight check (once, before first loop):**
- Verify TaskList exists for plan
  - If not, use `/decompose-plan` skill to create it
- Do NOT read the plan file yourself — subagents extract their own task context

### 2. Execute Task with Subagent

For each task:

**Dispatch fresh subagent:**
- Select model based on task complexity (see Model Selection below)
- Do NOT specify model for agent-type subagents (code-reviewer, app-tech-lead) — they define their own model in `.claude/agents/`

**Model Selection:**

| Task Type | Model | When to Use |
|-----------|-------|-------------|
| Simple | `haiku` | Config updates, documentation, single-file changes, scaffolding |
| Standard | `sonnet` | Multi-file implementation, business logic, TDD, integration work |
| Complex | `sonnet` | Architectural changes, new components, debugging, performance work |

**Heuristics for orchestrator:**
- **Use haiku if:** Task description contains "update", "add field", "config", "documentation", "rename", OR touches ≤2 files with no logic changes
- **Use sonnet if:** Task involves TDD, multi-file coordination, new functionality, bug fixes, or "implement" in description
- **When unsure:** Default to sonnet (fix cycles cost more than slightly higher implementation cost)

```plaintext
Task tool (
 subagent_type: {{agent}} | general-purpose
  description: "Implement Task {{task-number}}: {{task name}}"
  prompt: |
    You are implementing Task {{task-number}} from {{plan-file-path}}.

    **Self-gather context (orchestrator does NOT provide this):**

    Extract your task from the plan:
    ```bash
    citation-manager extract header {{plan-file-path}} "{{task-header-name}}"
    ```

    Then follow any additional context-gathering steps specified in the task (e.g., pulling GH issues, reading related files).

    **GitHub Issue Context (if task has issue number):**
    ```bash
    gh issue view {{issue-number}} --json title,body,labels --template '{{.title}}

    {{.body}}'
    ```
    Extract acceptance criteria from the issue body. These are your requirements.

    Your job is to:
    1. Navigate to and work in {{worktree directory | feature-branch if worktree missing}}
    2. Implement exactly what the task specifies
    3. Write tests (following TDD if task says to)
    4. Verify implementation works
    5. Run diagnostic verification (MANDATORY - see below)
    6. Commit your work (include `Fixes: #{{issue-number}}` in footer if task has GH issue)
    7. Clean up test processes (MANDATORY - see below)
    8. Write results to file
    9. Report back

    CRITICAL - Test Process Cleanup (Step 6):
    Before writing results, you MUST clean up any test processes you spawned:

    ```bash
    # Check for running vitest processes (pgrep works in sandbox; ps does not)
    pgrep -fl vitest

    # If any found, kill them
    pkill -f "vitest" || true

    # Verify cleanup succeeded (should return nothing)
    pgrep -fl vitest
    ```

    NEVER skip this step. Orphaned test processes consume ~14GB memory each.

    CRITICAL - Diagnostic Verification (Step 5):
    Before committing, you MUST verify zero diagnostic errors.

    For TypeScript projects:
    ```bash
    npm run build -w {{workspace-package}}
    ```
    If build fails, fix ALL errors before committing. Do NOT commit with TypeScript errors.

    For non-TypeScript projects, use IDE diagnostics:
    ```
    mcp__ide__getDiagnostics(uri: "file://{{changed-file}}")
    ```

    NEVER skip this step. Tests pass at runtime but miss compile-time type errors.
    Task 4 baseline: subagent committed 3 TS errors (TS2532, TS2339) that tests didn't catch.

    **Rationalizations to reject:**
    - "Tests pass so it's correct" → Tests don't catch type errors. Build does.
    - "I'll fix types later" → Later = reviewer catches it = fix subagent = 2x cost.
    - "Build is slow" → 5 seconds vs full fix cycle. Build every time.

    CRITICAL - GitHub Issue Reference (Step 6):
    If task has a GitHub issue number, include in commit footer:
    ```
    Fixes: #{{issue-number}}
    ```
    Place BEFORE the Claude attribution footer. This links the commit to the issue.
    If no issue number, omit the Fixes footer.

  MANDATORY: Use the `writing-for-token-optimized-and-ceo-scannable-content` skill when writing your review results.

    CRITICAL: Write your results to {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-dev-results.md with:
    - Model used for implementation
    - Task number and name
    - What you implemented
    - Tests written and test results
    - Diagnostic verification results (build output or IDE diagnostics)
    - Files changed
    - Any issues encountered
    - Commit SHA

    Report: Summary + confirm results file written
  model: {{haiku|sonnet}}  # See Model Selection heuristics above
```

**Subagent reports back** with summary and results file location.

### 3. Review Subagent's Work

**Dispatch code-reviewer subagent:**
- Use `code-reviewer` agent type (defined in `.claude/agents/code-reviewer.md`)
- Do NOT specify a model override — the agent defines its own model (sonnet)

```plaintext
Task tool (code-reviewer):
  prompt: |
    You are reviewing Task {{task-number}} implementation.

    MANDATORY: Use the `writing-for-token-optimized-and-ceo-scannable-content` skill when writing your review.

    CRITICAL: This is a task-level review. Be concise.
    - Target 10-30 lines for approved tasks
    - Target 30-80 lines for tasks with issues

    **Self-gather context:**

    1. Extract task from plan:
    ```bash
    citation-manager extract header {{plan-file-path}} "{{task-header-name}}"
    ```

    2. Follow any additional context-gathering steps in the task (e.g., GH issues).

    3. Fetch GitHub issue acceptance criteria (if task has issue number):
    ```bash
    gh issue view {{issue-number}} --json title,body,labels --template '{{.title}}

    {{.body}}'
    ```
    Extract acceptance criteria — verify implementation against each one.

    4. Read implementation results:
    - Dev results: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-dev-results.md

    Your job:
    1. Read plan task to understand requirements
    2. Read GH issue acceptance criteria (if issue number provided)
    3. Read dev results to understand what was implemented
    4. Review code changes (BASE_SHA to HEAD_SHA)
    5. Verify implementation satisfies EACH acceptance criterion
    6. Identify issues (BLOCKING/Critical/Important/Minor)
    7. Clean up test processes (MANDATORY - see below)
    8. Write concise review results

    CRITICAL - Test Process Cleanup (Step 5):
    Before writing results, you MUST clean up any test processes you spawned:

    ```bash
    # Check for running vitest processes (pgrep works in sandbox; ps does not)
    pgrep -fl vitest

    # If any found, kill them
    pkill -f "vitest" || true

    # Verify cleanup succeeded (should return nothing)
    pgrep -fl vitest
    ```

    NEVER skip this step. Orphaned test processes consume ~14GB memory each.

    CRITICAL: Write concise review to {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-review-results.md with:
    - Model used for review
    - Brief summary (1-2 sentences)
    - Issues (only include categories with actual issues)
    - Verdict: APPROVED or FIX REQUIRED

    CRITICAL VERDICT RULE: If you found ANY issues (BLOCKING/Critical/Important/Minor), you MUST set verdict to FIX REQUIRED. NEVER approve tasks that have documented issues.

    CRITICAL - Acceptance Criteria Verification (if task has GH issue):
    Include in review results:

    **Acceptance Criteria Verification**
    | Criterion | Status | Notes |
    |-----------|--------|-------|
    | AC1: [from issue] | ✅ PASS / ❌ FAIL | [brief] |

    If ANY criterion fails → verdict MUST be FIX REQUIRED.

    CRITICAL - New Issues from Review:
    If you discover problems NOT in the original task scope, dispatch `github-assistant`
    agent to create GH issues with proper labels:

    ```plaintext
    Task tool (github-assistant):
      description: "Create GH issue for [problem]"
      prompt: |
        Create a GitHub issue using the `managing-github-issues` skill.

        Title: <type>(<scope>): <description>
        Body: [Problem description]. Found during review of Task {{task-number}} (#{{issue-number}}).
        Labels (REQUIRED):
        - Type: bug / enhancement / tech-debt
        - Component: component:<PascalCase>
        - Priority: priority:low / priority:medium / priority:high

        ```bash
        gh issue create \
          --title "<type>(<scope>): <description>" \
          --body "..." \
          --label "bug,component:MarkdownParser,priority:medium"
        ```
    ```

    Record created issues in review results:
    **New Issues Created:** #N — description

    Keep it brief:
    - Skip "Strengths" section for approved tasks (ZERO issues)
    - Skip empty issue categories (don't write "Critical: None")
    - No comprehensive analysis - this is task-level, not PR-level

    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]
```

**Code reviewer returns:** Summary + review results file location.

### 3a. Cleanup Background Processes

**MANDATORY: After each task review, before proceeding to fixes.**

Subagents may spawn vitest test processes (watch mode, UI mode) that don't cleanup automatically. Each orphaned process consumes ~14GB memory.

**Check for orphaned processes:**

```bash
# Check for running vitest processes
ps aux | grep -i vitest | grep -v grep
```

**If vitest processes found:**

```bash
# Kill vitest processes
pkill -f "vitest" || true

# Verify cleanup succeeded
ps aux | grep -i vitest | grep -v grep
# Should return nothing
```

**VERIFICATION REQUIRED:** Process list must be empty before proceeding to Step 4.

**Common sources:**
- Subagent used `npm run test:watch` instead of `npm test`
- Subagent ran tests in background without cleanup
- Test failures left worker processes hanging

**Red flags indicating you're about to skip this:**
- "No processes showing up now" → Verify EVERY time, evidence before assumptions
- "Cleanup can wait until end" → 14GB × 4 processes × N tasks = exponential waste
- "forceExit handles this" → Only works when vitest completes normally, not watch/UI modes
- "Process will timeout eventually" → No timeout configured, runs indefinitely

### 4. Apply Review Feedback

**If BLOCKING issues found:**
- See section 4a below (requires app-tech-lead escalation)
- Do NOT proceed to section 4b until BLOCKING resolved

**If Critical/Important/Minor issues found:**
- See section 4b below (standard fix workflow)

### 4a. Handle Blocking Issues (Architectural Decisions)

**CRITICAL: BLOCKING issues MUST be resolved by app-tech-lead subagent. NEVER escalate to user.**

**Foundational principle:** Architectural decisions require research, principle evaluation, and documentation. App-tech-lead subagent provides this. User escalation without context and recomendations breaks the workflow and annoys ceo/user by asking for their attention when you could do research to clarify the issue yourself. Once App-tech-lead does research and a MAJOR change is needed, then involve the user. Otherwise provide additional context to fixing agent.

Code-reviewer may identify BLOCKING when:
- Implementation made architectural choice not specified in plan
- Multiple valid approaches exist, choice affects codebase architecture
- Decision requires evaluation against architecture principles
- Cannot be "fixed" with code changes alone

**When code-reviewer returns BLOCKING issues:**

1. **MANDATORY - Launch `application-tech-lead` subagent**

   You MUST launch `application-tech-lead`. This is NOT optional. This is NOT a suggestion.

   **DO NOT:**
   - ❌ Ask user "What should I do?"
   - ❌ Ask user "Is Redux OK?"
   - ❌ "Escalate to user for architectural decision"
   - ❌ "Present options to user and wait for their choice"
   - ❌ Dispatch fix subagent to "just pick one"
   - ❌ Proceed to next task

   **Why NO user escalation:**
   - User expects app-tech-lead to handle architectural decisions
   - App-tech-lead provides research, evaluation, documentation
   - User escalation = undocumented decision without principle evaluation
   - Interrupts workflow unnecessarily

2. **Launch `application-tech-lead` with this task:**

   ```plaintext
   Task tool (application-tech-lead):
     description: "Resolve blocking architectural decision from Task N"
     prompt: |
       A code review identified a blocking architectural decision for Task {{task-number}}.

       CRITICAL: Extract task context from plan using citation tool:

       ```bash
       citation-manager extract header {{plan-file-path}} "{{task-header-name}}"
       ```

       Read context files:
       - Dev results: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-dev-results.md
       - Review results: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-review-results.md

       BLOCKING ISSUE:
       [paste full BLOCKING issue from code-reviewer]

       Your job:
       1. Read plan task to understand context
       2. Read dev results to understand what was implemented
       3. Read review results to understand the blocking issue
       4. Read architecture documentation to understand context
       5. Read PRD to understand requirements and scope
       6. Research options using Perplexity with "{{query}} best practices 2025"
       7. Evaluate options against architecture principles using evaluate-against-architecture-principles skill
       8. Update implementation plan with specific choice
       9. Write decision document
       10. Report back

    MANDATORY: Use the `writing-for-token-optimized-and-ceo-scannable-content` skill when writing your review.

       CRITICAL: Write your decision to {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-arch-decision.md with:
       - Task number and name
       - Decision date
       - BLOCKING issue summary
       - Options considered (2-3 options minimum)
       - Evaluation against architecture principles
       - Perplexity research findings
       - Recommendation with clear rationale
       - Plan update confirmation

       Critical: Your decision must be grounded in architecture principles, not just "best practice" popularity.
   ```

3. **After `application-tech-lead` returns:**
   - Review decision rationale
   - Verify plan updated with specific choice
   - Determine if change is MAJOR (see criteria below)

   **MAJOR Change Criteria:**
   - Adds new external dependency/library
   - Changes fundamental architecture pattern (state management, data flow, auth)
   - Adds new infrastructure (database, cache, queue)
   - Switches frameworks or core technologies
   - Impacts bundle size significantly (>10KB)
   - Requires team learning curve
   - High migration cost if reversed

   **If MAJOR change:**
   - Present decision to CEO/user with full context:
     - Options evaluated
     - Architecture principle evaluation
     - Perplexity research findings
     - App-tech-lead recommendation
     - Impact summary (bundle size, learning curve, migration cost)
   - Wait for CEO approval before proceeding
   - If approved: Continue to implementation
   - If rejected: Ask app-tech-lead to reconsider with CEO feedback

   **If minor change (built-in APIs, internal refactoring, no new dependencies):**
   - Proceed autonomously to implementation

   **Then proceed to implementation:**
   - Either: Approve existing implementation (if matches decision)
   - Or: Dispatch fix subagent to implement chosen approach
   - Re-run code-reviewer to verify BLOCKING resolved

4. **Then proceed to section 4b** for any remaining Critical/Important/Minor issues

### 4b. Handle Standard Issues (Implementation Fixes)

**If Critical/Important/Minor issues found:**
- Fix Critical issues immediately
- Fix Important issues before next task
- Note Minor issues

**Orchestrator Dynamic Decision (YOU):**

Before dispatching fix agent, determine which files to include:

1. Check if `task-{{task-number}}-arch-decision.md` exists (BLOCKING was resolved)
2. Build file list for fix agent:
   - Always include: plan task, dev results, review results
   - Conditionally include: arch decision (if exists)

**Dispatch follow-up subagent with context files:**

```plaintext
Task tool (general-purpose):
  description: "Fix Task {{task-number}} issues from review"
  prompt: |
    You are fixing issues found in code review for Task {{task-number}}.

    CRITICAL: Extract task context from plan using citation tool:

    ```bash
    citation-manager extract header {{plan-file-path}} "{{task-header-name}}"
    ```

    Read context files:
    - Plan task (via citation extraction above)
    - Dev results: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-dev-results.md
    - Review results: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-review-results.md
    {{#if arch-decision-exists}}
    - Arch decision: {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-arch-decision.md
    {{/if}}

    Issues to fix:
    [paste issues from review-results.md]

    Your job:
    1. Read plan task to understand requirements
    2. Read dev results to understand what was implemented
    3. Read review results to understand issues
    {{#if arch-decision-exists}}
    4. Read arch decision to understand architectural choice
    5. Implement fixes following architectural decision
    {{else}}
    4. Implement fixes for all issues
    {{/if}}
    6. Verify fixes work (run tests)
    7. Commit your work
    8. Write fix results

    CRITICAL: Write your results to {{epic-or-user-story-folder}}/tasks/task-{{task-number}}-fix-results.md with:
    - Task number and name
    - Issues addressed
    - Changes made
    - Test results
    - Files changed
    - Commit SHA

    Report: Summary + confirm results file written
  model: sonnet  # Fix agents always use sonnet — haiku fixes triggered this cycle
```

### 5. Close GitHub Issue and Mark Complete

1. **Close GitHub issue** (if task has issue number):

   Dispatch `github-assistant` agent:

   ```plaintext
   Task tool (github-assistant):
     description: "Close GH issue #{{issue-number}}"
     prompt: |
       Close GitHub issue #{{issue-number}} — Task {{task-number}} approved.

       ```bash
       gh issue close {{issue-number}} --comment "Resolved via commit $(git rev-parse HEAD). Task {{task-number}} reviewed and approved."
       ```

       Report: Confirm issue closed.
   ```

2. **Mark task completed** via TaskUpdate
3. **Reset** consecutive error counter to 0
4. **Next task** immediately — do NOT pause for user input

## Autonomous Execution Rules

### Never Stop For

- Commit confirmation ("ready to commit?")
- Task completion acknowledgment ("task done, proceed?")
- Review results sharing (just log and continue)
- Minor/Important issues (fix and continue)

### Stop Only When

1. **All tasks complete** — normal exit
2. **3 consecutive task failures** — subagent fails same task 3 times after fix attempts
3. **MAJOR architectural decision** — requires CEO approval (see 4a)

### Error Tracking

Error counter resets on each successful task. Increments on failed fix attempts:

- **APPROVED** → `consecutive_errors = 0`, next task
- **FIX REQUIRED** → dispatch fix → re-review
  - Re-review APPROVED → `consecutive_errors = 0`, next task
  - Re-review FAILED → `consecutive_errors += 1`
    - If `>= 3` → STOP, report to user
    - Else → attempt fix again

### Rationalizations for Stopping Early (REJECT These)

| Excuse | Reality |
|--------|---------|
| "Let me check with user first" | You have the plan. Execute it. |
| "Ready to commit?" | Commits are subagent responsibility. Keep going. |
| "Should I proceed?" | Yes. Always. Until done or 3 errors. |
| "User might want to review" | Code reviewer subagent handles review. Keep going. |
| "This task was complex, pause" | Complexity is not a stop condition. Next task. |
| "Separation of concerns — issue closure is external" | Issue closure is Step 5 of the workflow. Not optional. |
| "Issue lifecycle is separate from task completion" | Step 5 explicitly closes issue BEFORE marking complete. |

### Rationalizations for Doing Research (REJECT These)

The orchestrator is a dispatcher. It reads TaskList and dispatches subagents. It does NOT gather context.

| Excuse | Reality |
|--------|---------|
| "Let me read the plan first" | Subagent extracts its own task via citation-manager. |
| "Let me pull additional context" | Subagent self-gathers per plan instructions. |
| "Let me check what's been done" | TaskList status tells you. Subagent explores if needed. |
| "I need the BASE_SHA" | Subagent gets its own git state. |
| "Let me find the tasks folder" | Subagent discovers paths from plan context. |
| "I need to build context for the prompt" | The prompt template IS the context. Fill in placeholders only. |
| "Just a quick check" | Quick checks = 500+ tokens wasted. Subagent does it in its own context. |

**What orchestrator knows (from TaskList + task description):**
- Plan file path
- Task number and header name
- GH issue number
- Results folder path
- Task status and dependencies

**What orchestrator NEVER does:**
- ❌ Read plan files (Read tool)
- ❌ Gather task context (GH issues, related files, etc.)
- ❌ Explore codebase (Explore subagent for "preparation")
- ❌ Check git log/status/diff
- ❌ Read source files
- ❌ Check folder contents

**All of these are subagent responsibilities.** Orchestrator fills prompt template placeholders and dispatches.

### 6. Final Review

After all tasks complete, dispatch final `code-reviewer`:
- Reviews entire implementation
- Checks all plan requirements met
- Validates overall architecture

### 7. Complete Development

After final review passes:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## Example Workflow

```text
You: I'm using Subagent-Driven Development to execute the task list.

[Read TaskList → Task 3 is next (in_progress)]
[TaskUpdate: Task 3 → in_progress]

[Dispatch implementation subagent with: plan path, task header, GH issue #1]
  ← Subagent self-gathers: extracts task from plan, pulls GH issue, implements, commits
  → Returns: "Implemented, wrote task-3-dev-results.md, SHA abc123"

[Dispatch code-reviewer with: plan path, task header, GH issue #1, results folder]
  ← Reviewer self-gathers: extracts task, pulls issue, reads dev results, reviews diff
  → Returns: "APPROVED, wrote task-3-review-results.md"

[Cleanup vitest processes]
[TaskUpdate: Task 3 → completed]

[Read TaskList → Task 4 is next (pending, now unblocked)]
[TaskUpdate: Task 4 → in_progress]

[Dispatch implementation subagent with: plan path, task header, GH issue #28]
  → Returns: "Implemented, wrote task-4-dev-results.md, SHA def456"

[Dispatch code-reviewer]
  → Returns: "FIX REQUIRED — Critical: missing characterization test baseline"

[Dispatch fix subagent with: plan path, task header, GH issue, review issues]
  → Returns: "Fixed, wrote task-4-fix-results.md, SHA ghi789"

[Dispatch code-reviewer for re-review]
  → Returns: "APPROVED"

[Cleanup processes]
[TaskUpdate: Task 4 → completed]

... [loop continues until all tasks complete] ...

[Dispatch final code-reviewer for entire implementation]
[Use finishing-a-development-branch skill]
Done!
```

**Key pattern:** Orchestrator only uses TaskList, TaskUpdate, Task (dispatch), and cleanup Bash. All context gathering happens inside subagents.

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)

**vs. Executing Plans:**
- Same session (no handoff)
- Continuous progress (no waiting)
- Review checkpoints automatic

**Cost:**
- More subagent invocations
- But catches issues early (cheaper than debugging later)

## Red Flags

**Never:**
- Stop to ask user "ready to commit?" or "should I proceed?"
- Pause between tasks for user acknowledgment
- Skip code review between tasks
- Skip process cleanup after task review (Step 3a)
- Proceed with unfixed Critical issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Implement without reading plan task
- Read plan files, GH issues, or source code as orchestrator (subagents self-gather)
- Use Read, Grep, Glob, Bash, or Explore tools for context gathering (dispatcher only)

**Process cleanup rationalizations to reject:**
- "No processes showing up now" → Verify EVERY time with evidence
- "Cleanup can wait until end" → Memory waste compounds across tasks
- "forceExit handles this" → Only works when vitest exits normally
- "Process will timeout eventually" → No timeout configured, runs indefinitely

**If subagent fails task:**
- Dispatch fix subagent with specific instructions
- Don't try to fix manually (context pollution)

## Integration

**Required workflow skills:**
- **writing-plans** - REQUIRED: Creates the plan that this skill executes
- **code-reviewer** agent (`.claude/agents/code-reviewer.md`) - REQUIRED: Review after each task (see Step 3)
- **finishing-a-development-branch** - REQUIRED: Complete development after all tasks (see Step 7)

**Subagents must use:**
- **test-driven-development** - Subagents follow TDD for each task

**Alternative workflow:**
- **executing-plans** - Use for parallel session instead of same-session execution
