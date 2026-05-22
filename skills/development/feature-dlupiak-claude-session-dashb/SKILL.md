---
name: feature
description: "Full SDLC pipeline: design → plan → implement → review → test → ship. Use this skill when the user wants to BUILD A NEW FEATURE that spans multiple files across scanner, server functions, and UI layers — anything requiring architecture design, an implementation plan, and coordinated changes across a vertical slice. Trigger on: /feature command, 'build/implement/add [feature]' requests involving new server functions + UI components, multi-step feature work needing TDD and code review. Do NOT trigger for: bug fixes, refactors, small UI tweaks, single-file changes, CI fixes, test runs, or PR reviews."
user-invocable: true
argument-hint: "<story-id> [description]"
---

# Feature Development Pipeline

You are orchestrating the SDLC pipeline for **$ARGUMENTS.story-id**. You are the ORCHESTRATOR — you delegate ALL work to specialized agents and chain their outputs together. You NEVER write production code, tests, architecture, or reviews yourself.

## Why This Structure Matters

Each step builds on the previous one's output. The architect's design feeds the plan, the plan feeds the implementer, the implementer's output feeds the reviewer. Breaking this chain means agents work blind and produce lower quality results. Every agent prompt must include the relevant context from prior steps.

## Variables You Maintain

Track these throughout the pipeline — they form the context chain:
- `DESIGN` — architect's design document content
- `PLAN` — implementation plan with bite-sized tasks
- `WORKTREE` — path to the worktree (../dashboard-$ARGUMENTS.story-id)
- `TASK_REPORTS` — accumulating list of implementer reports per task
- `REVIEW_FINDINGS` — review results that need addressing

---

## Step 0: Resume or Start

```bash
git worktree list | grep "$ARGUMENTS.story-id" || echo "NO_WORKTREE"
```

- **Worktree exists**: Ask "Resume or start fresh?"
  - Resume: `cd` to worktree, `TaskList` to show state, skip to first incomplete step.
  - Fresh: `git worktree remove ../dashboard-$ARGUMENTS.story-id --force`, proceed to Step 1.
- **No worktree**: Proceed to Step 1.

---

## Step 1: Design (dispatch `architect`)

The architect explores context and collaborates with the user to produce a design.

```
Agent(subagent_type: "architect", prompt: "
  Design feature $ARGUMENTS.story-id: $ARGUMENTS.description

  Use the superpowers:brainstorming skill. It will guide you through:
  1. Exploring project context
  2. Asking clarifying questions one at a time
  3. Proposing 2-3 approaches with trade-offs
  4. Presenting design section by section for approval

  The design document MUST include:
  - Problem statement and user impact
  - Chosen approach with rationale
  - Affected vertical slices and files
  - Data flow (ASCII diagram — from ~/.claude files through scanner/parser to server fn to UI)
  - Task Breakdown table: | Task | Complexity | Files | Dependencies |

  Save to: docs/designs/design-$ARGUMENTS.story-id.md
  Return the FULL design document content.
")
```

**After return**: Present the design summary to the user. Store `DESIGN` = architect's output.

**HARD GATE: DO NOT proceed until user explicitly approves the design.**

---

## Step 2: Implementation Plan (dispatch `architect`)

Convert the approved design into bite-sized implementation tasks.

```
Agent(subagent_type: "architect", prompt: "
  Use the superpowers:writing-plans skill to create the plan.

  Create an implementation plan for $ARGUMENTS.story-id.

  Here is the approved design:
  ---
  $DESIGN
  ---

  Requirements:
  - Each task should be 2-5 minutes of work
  - Follow TDD: failing test → verify fail → implement → verify pass → commit
  - Include exact file paths, complete code snippets, and test commands
  - Reference existing codebase patterns (read relevant files first)
  - Tasks should be mostly independent where possible

  Save to: docs/plans/$(date +%Y-%m-%d)-$ARGUMENTS.story-id.md
  Return the FULL plan content.
")
```

Store `PLAN` = architect's output. Present the task list to user for awareness (no approval gate needed here).

---

## Step 3: Create Git Worktree

```bash
BRANCH_SUFFIX=$(echo "$ARGUMENTS.description" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-30)
git worktree add ../dashboard-$ARGUMENTS.story-id -b "feature/$ARGUMENTS.story-id-${BRANCH_SUFFIX}"
```

Copy design and plan docs into the worktree:
```bash
mkdir -p ../dashboard-$ARGUMENTS.story-id/docs/designs ../dashboard-$ARGUMENTS.story-id/docs/plans
cp docs/designs/design-$ARGUMENTS.story-id.md ../dashboard-$ARGUMENTS.story-id/docs/designs/ 2>/dev/null || true
cp docs/plans/*$ARGUMENTS.story-id*.md ../dashboard-$ARGUMENTS.story-id/docs/plans/ 2>/dev/null || true
```

Store `WORKTREE` = ../dashboard-$ARGUMENTS.story-id. All subsequent agents work from this path.

---

## Step 4: Implementation (subagent-driven-development)

One fresh subagent per task, two-stage review after each.

### 4a. Set up task tracking

Create a TaskCreate entry for every task from `PLAN`. This gives the user visibility.

### 4b. Per-task loop

For each task in the plan (sequentially — never parallel implementation):

**1. Dispatch implementer subagent:**

```
Agent(subagent_type: "implementer", prompt: "
  You are implementing Task N: [task name] for feature $ARGUMENTS.story-id.

  ## Task Description
  [FULL TEXT of this task from PLAN — paste it here, do NOT make the subagent read the file]

  ## Context
  - Feature: $ARGUMENTS.story-id — $ARGUMENTS.description
  - Working directory: $WORKTREE/apps/web
  - Design summary: [relevant excerpt from DESIGN for this task]
  - Previous tasks completed: [list what's done so far, with brief summaries]
  - This task depends on: [what it builds on]

  ## Your Job
  Use the superpowers:test-driven-development skill.
  After each task: use superpowers:verification-before-completion before claiming done.
  If you hit a bug or unexpected failure: use superpowers:systematic-debugging.
  Run typecheck and lint after implementation: cd $WORKTREE/apps/web && npm run typecheck && npm run lint
  Commit with a descriptive message.

  If anything is unclear — ask questions before starting.

  ## Report Format
  Return: what you implemented, tests written and results, files changed, self-review findings, any concerns.
")
```

**2. Dispatch spec compliance reviewer:**

```
Agent(subagent_type: "reviewer", prompt: "
  Review spec compliance for Task N of $ARGUMENTS.story-id.

  ## What Was Requested
  [FULL task text from PLAN]

  ## What Implementer Claims
  [Paste the implementer's report from step 1]

  ## Your Job
  Do NOT trust the implementer's report. Read the actual code at $WORKTREE and verify:
  - All requirements implemented (nothing missing)
  - No extra/unneeded work (nothing added beyond spec)
  - No misunderstandings of requirements

  Report: ✅ Spec compliant OR ❌ Issues: [specific list with file:line references]
")
```

→ If ❌: dispatch implementer to fix specific issues, then re-review spec compliance.

**3. Dispatch code quality reviewer:**

```
Agent(subagent_type: "reviewer", prompt: "
  Review code quality for Task N of $ARGUMENTS.story-id.

  Working directory: $WORKTREE
  What was implemented: [from implementer report]
  Requirements: [task text from PLAN]

  Run: git diff HEAD~1 to see the changes for this task.

  Check against project standards:
  - TypeScript: no 'any', proper error handling, Zod validation at boundaries
  - React: TanStack Query for data fetching, no useEffect fetching, proper state
  - Architecture: vertical slice compliance, no /services or /utils
  - Security: no exposed secrets, input validation
  - Tests: testing behavior not implementation, good coverage

  Report: Strengths, Issues (CRITICAL/WARNING/INFO), Assessment (approve/needs-work)
")
```

→ If CRITICAL/WARNING: dispatch implementer to fix, then re-review quality.

**4. Mark task complete** — TaskUpdate status to completed.

**5. Move to next task** — include completed task summary in the next implementer's context.

### 4c. After all tasks complete

Run full verification yourself (superpowers:verification-before-completion — evidence before claims):

```bash
cd $WORKTREE/apps/web && npm run typecheck
cd $WORKTREE/apps/web && npm run lint
cd $WORKTREE/apps/web && npm run test
cd $WORKTREE/apps/web && npm run build
```

Read and report the actual output. If anything fails, dispatch the implementer with the specific error output. Repeat until all four pass.

---

## Step 5: Final Holistic Review (dispatch `reviewer`)

After all tasks pass individually, review the feature as a whole:

```
Agent(subagent_type: "reviewer", prompt: "
  Final review for feature $ARGUMENTS.story-id: $ARGUMENTS.description

  Working directory: $WORKTREE
  Run: git diff main...HEAD

  This is a holistic review of the ENTIRE feature. Individual tasks have already passed spec and quality reviews. Focus on:
  - Cross-task integration: do the pieces fit together correctly?
  - Consistency: naming, patterns, error handling across all new code
  - Missing pieces: anything the task-level reviews might have missed?
  - Architecture: does the overall implementation match the design?
  - Security: end-to-end data flow, no path traversal, no secrets exposed

  Design document for reference:
  ---
  $DESIGN
  ---

  Return: CRITICAL / WARNING / INFO findings with file:line references.
")
```

If CRITICAL: dispatch implementer to fix → re-review.

---

## Step 6: Ship

**User confirmation required.** Present a summary:
- Branch name and commit count
- Files changed (git diff --stat main...HEAD)
- All quality gates: ✅ typecheck, ✅ lint, ✅ test, ✅ build
- Review status: all findings resolved
- Proposed PR title and description

Ask: "Ready to ship? (yes/no)"

- **No**: Ask what needs to change.
- **Yes**: Invoke the `/ship` skill from the worktree directory. It handles commit, push, PR, CI check, merge, and worktree cleanup.

---

## Critical Rules

1. **NEVER** write production code, tests, designs, or reviews yourself — always dispatch an agent
2. **NEVER** proceed past Step 1 without explicit user approval of the design
3. **ALWAYS** paste full context into agent prompts — design excerpts, plan task text, previous reports
4. **ALWAYS** run verification commands yourself and read the output before claiming success
5. **ALWAYS** use TaskCreate/TaskUpdate to track each plan task through the pipeline
6. If an agent fails or produces poor results, dispatch it again with the error output and specific corrective instructions — don't try to fix it yourself
