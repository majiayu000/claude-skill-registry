---
name: dev
description: "This skill should be used when the user asks to 'start a feature', 'build a feature', 'implement a feature', 'develop', 'new feature', or needs the full 7-phase development workflow with TDD enforcement."
allowed-tools: Read, Grep, Glob, Bash, Skill, TodoWrite
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/dev-delegation-guard.py"
---

**Announce:** "I'm using dev (Phase 1) to gather requirements."

## Resume Detection

**BEFORE creating any new state, check for a previous session handoff.**

Check if `.planning/HANDOFF.md` exists:

```bash
test -f .planning/HANDOFF.md && echo "HANDOFF_EXISTS" || echo "NO_HANDOFF"
```

**If HANDOFF_EXISTS:**

1. Read `.planning/HANDOFF.md`
2. Present the user with a status summary:

```
Previous session handoff detected:
- Phase: [phase_name from frontmatter]
- Task: [task] of [total_tasks]
- Status: [status]
- Last updated: [last_updated]
- Next action: [from "Next Action" section]
```

3. Ask the user:

```python
AskUserQuestion(questions=[{
  "question": "A handoff from a previous session was found. How would you like to proceed?",
  "header": "Session Handoff Detected",
  "options": [
    {"label": "Resume from handoff", "description": "Continue where the previous session left off"},
    {"label": "Start fresh", "description": "Discard the handoff and begin a new workflow from scratch"}
  ],
  "multiSelect": false
}])
```

4. **If "Resume from handoff":**
   - Read `.planning/ACTIVE_WORKFLOW.md` to get the recorded phase
   - Read `.planning/SPEC.md` and `.planning/PLAN.md` if they exist
   - Skip directly to the recorded phase by discovering and reading the appropriate phase skill:
     ```bash
     ${CLAUDE_SKILL_DIR}/../../skills/dev-[phase_name]/SKILL.md
     ```
   - Delete `.planning/HANDOFF.md` after successfully resuming (it has been consumed)
   - Announce: "Resuming from handoff — picking up at Phase [N]: [phase_name]."

5. **If "Start fresh":**
   - Delete `.planning/HANDOFF.md`
   - Proceed with normal workflow initialization below

## Workflow Overview

```
Phase 1       Phase 2      Phase 3      Phase 4       Phase 5        Phase 5.5      Phase 6      Phase 7
brainstorm → explore    → clarify   → design     → implement   → validate    → review    → verify
 (SPEC.md)   (key files)  (resolved)   (PLAN.md)    (tests pass)   (gaps filled)  (>=80%)    (fresh evidence)
    │            │            │            │              │              │             │            │
    ▼            ▼            ▼            ▼              ▼              ▼             ▼            ▼
  GATE:        GATE:        GATE:        GATE:          GATE:          GATE:         GATE:        GATE:
  Questions    All files    Ambiguities  User           All tasks      Goals met     No issues    Fresh run
  asked +      read by      resolved +   approved +     pass tests     vs tasks      >= 80%       confirms
  SPEC.md      main chat    SPEC.md      PLAN.md        + spec         completed     confidence   all claims
  written                   updated      written        match
```

**Every gate is mandatory. Skipping a gate means the next phase operates on bad inputs.**

## Workflow Initialization

Create `.planning/ACTIVE_WORKFLOW.md` to track workflow state:

```yaml
---
workflow: dev
phase: 1
phase_name: brainstorm
started: [current timestamp]
project_root: [current directory]
active_skill: ../../skills/dev/SKILL.md  # relative to this skill's base directory
spec: .planning/SPEC.md
plan: .planning/PLAN.md
---
```

This enables session persistence - returning to the project will reload the current phase.

Also create `.planning/STATE.md` to track workflow state:

```markdown
---
workflow: dev
phase: 1
phase_name: brainstorm
status: in_progress
started: [timestamp]
---
# Dev Workflow State

## Current Position
Phase: 1 (brainstorm)
Status: In progress

## Decisions
(none yet)

## Blockers
(none)
```

## Contents

- [The Iron Law of Brainstorming](#the-iron-law-of-brainstorming)
- [What Brainstorm Does](#what-brainstorm-does)
- [Process](#process)
- [Red Flags - STOP If You're About To](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Brainstorming (Questions Only)

Refine vague ideas into clear requirements through Socratic questioning.
**NO exploration, NO approaches** - just questions and requirements.

<EXTREMELY-IMPORTANT>
## The Iron Law of Brainstorming

**ASK QUESTIONS BEFORE ANYTHING ELSE. This is not negotiable.**

Before exploring codebase, before proposing approaches, follow these requirements:
1. Ask clarifying questions using AskUserQuestion
2. Understand what the user actually wants
3. Define success criteria

Approaches come later (in /dev-design) after exploring the codebase.

**If YOU catch YOURSELF about to explore the codebase before asking questions, STOP.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The requirements seem obvious" | Your assumptions are often wrong | ASK questions to confirm |
| "Let me just look at the code to understand" | Code tells HOW, not WHY | ASK what user wants first |
| "I can gather requirements while exploring" | You'll waste time on distraction and miss critical questions | QUESTIONS FIRST, exploration later |
| "User already explained everything" | You'll find users always leave out critical details | ASK clarifying questions anyway |
| "I'll ask if I need more info" | You cannot know unknown unknowns without asking | ASK questions NOW, not later |
| "Quick peek at the code won't hurt" | You'll let codebases bias your thinking | STAY IGNORANT until requirements clear |
| "I can propose approaches based on description" | You need exploration to precede design | WAIT for dev-design phase |

### Drive-Aligned Framing

**Guessing user requirements is NOT HELPFUL — you build the wrong thing and create rework for the user.**

Asking questions is cheap. Building the wrong thing is expensive. Every minute spent clarifying requirements saves hours of wasted implementation.

### No Pause After Completion

After writing `.planning/SPEC.md` and completing brainstorm, immediately invoke the next phase:

**Invoke the explore phase:**

Read `${CLAUDE_SKILL_DIR}/../../skills/dev-explore/SKILL.md` and follow its instructions.

DO NOT:
- Summarize what was learned
- Ask "should I proceed?"
- Wait for user confirmation
- Write status updates

The workflow phases are SEQUENTIAL. Complete brainstorm → immediately start explore.

## What Brainstorm Does

| DO | DON'T |
|----|-------|
| Ask clarifying questions | Explore codebase |
| Understand requirements | Spawn explore agents |
| Define success criteria | Look at existing code |
| Write draft SPEC.md | Propose approaches (that's design) |
| Identify unknowns | Create implementation tasks |

**Brainstorm answers: WHAT do we need and WHY**
**Explore answers: WHERE is the code** (next phase)
**Design answers: HOW to build it** (after exploration)

## Process

### 1. Ask Questions First

Use `AskUserQuestion` immediately with these principles:
- **One question at a time** - never batch
- **Multiple-choice preferred** - easier to answer
- Focus on: purpose, constraints, success criteria

Example questions to ask:
- "What problem does this solve?"
- "Who will use this feature?"
- "What's the most important requirement?"
- "Any constraints (performance, compatibility)?"

### 2. Ask About Testing Strategy (MANDATORY)

<EXTREMELY-IMPORTANT>
**THE TESTING QUESTION IS NOT OPTIONAL. This is the moment to prevent "no tests" rationalization.**

After understanding what to build, immediately ask:

```python
AskUserQuestion(questions=[{
  "question": "How will we verify this works automatically?",
  "header": "Testing",
  "options": [
    {"label": "Unit tests (pytest/jest/etc.)", "description": "Test functions/methods in isolation"},
    {"label": "Integration tests", "description": "Test component interactions"},
    {"label": "E2E automation (Playwright/ydotool)", "description": "Simulate real user interactions"},
    {"label": "API tests", "description": "Test HTTP endpoints directly"}
  ],
  "multiSelect": true
}])
```

**If user says "manual testing only" → This is a BLOCKER, not a workaround.**

| User Says | Your Response |
|-----------|---------------|
| "Manual testing" | "That's not acceptable for /dev workflow. What's blocking automated tests?" |
| "No test infrastructure" | "Let's add one. What framework fits this codebase?" |
| "Too hard to test" | "What specifically is hard? Let's solve that first." |
| "Just this once" | "No exceptions. TDD is the workflow, not optional." |

**Why this matters:** If you don't ask about testing NOW, you'll rationalize skipping it later.
</EXTREMELY-IMPORTANT>

### 2b. Define What a REAL Test Looks Like (MANDATORY)

<EXTREMELY-IMPORTANT>
**A REAL test is feature-specific. You must define it NOW, not during implementation.**

After user chooses testing approach, ask:

```python
AskUserQuestion(questions=[{
  "question": "Describe the user workflow this test must replicate:",
  "header": "User Workflow",
  "options": [
    {"label": "UI interaction sequence", "description": "e.g., 'click button → see modal → submit form'"},
    {"label": "API call sequence", "description": "e.g., 'POST /login → receive token → GET /profile'"},
    {"label": "CLI command sequence", "description": "e.g., 'run command → see output → verify file created'"},
    {"label": "Other (describe in chat)", "description": "Custom workflow"}
  ],
  "multiSelect": false
}])
```

**Then ask for specifics:**

```python
AskUserQuestion(questions=[{
  "question": "What specific skill/tool should we use for testing?",
  "header": "Test Tool",
  "options": [
    {"label": "dev-test-electron", "description": "Electron apps with Chrome DevTools Protocol"},
    {"label": "dev-test-playwright", "description": "Web apps with Playwright MCP"},
    {"label": "dev-test-hammerspoon", "description": "macOS native apps"},
    {"label": "dev-test-linux", "description": "Linux desktop apps (ydotool/xdotool)"},
    {"label": "Standard unit tests", "description": "pytest/jest/etc. for pure functions"}
  ],
  "multiSelect": false
}])
```

**Why this matters:** If you don't define what a REAL test looks like NOW, you'll write FAKE tests later that:
- Test wrong code paths (HTTP when app uses WebSocket)
- Use programmatic shortcuts instead of actual UI
- Pass but don't verify real behavior

### Real Test Enforcement

**Read the shared enforcement for REAL vs FAKE test definitions:**

!`cat ${CLAUDE_SKILL_DIR}/../../references/dev-common-constraints.md`

See constraints C2 (Real Test Enforcement) and the protocol mismatch table. **A test that doesn't replicate the user's actual workflow is a FAKE test.**

**Document in SPEC.md:**
- User workflow to replicate
- Testing skill to use
- Code paths that must be exercised
- What the user actually sees/verifies
</EXTREMELY-IMPORTANT>

### 3. Define Success Criteria

After understanding requirements AND testing strategy, define measurable success criteria:
- Turn requirements into measurable criteria
- Use checkboxes for clear pass/fail
- Confirm criteria with user
- **Include at least one testable criterion per requirement**

### 4. Write Draft SPEC.md

Write the initial spec to `.planning/SPEC.md`:

```markdown
# Spec: [Feature Name]

> **For Claude:** After writing this spec, discover and read the explore phase skill via cache lookup for `skills/dev-explore/SKILL.md`.

## Problem
[What problem this solves]

## Requirements

Assign each requirement a unique ID using `CATEGORY-NN` format (e.g., `AUTH-01`, `UI-02`, `DATA-03`). Categories come from natural groupings.

| ID | Requirement | Scope |
|----|-------------|-------|
| [CAT-01] | [Requirement 1] | v1 |
| [CAT-02] | [Requirement 2] | v1 |

Scope: `v1` = must complete, `v2` = nice to have, `out-of-scope` = explicitly excluded.

## Success Criteria
- [ ] [CAT-01] [Criterion derived from requirement]
- [ ] [CAT-02] [Criterion derived from requirement]

## Constraints
- [Any limitations or boundaries]

## Testing Strategy (MANDATORY - USER APPROVED)

> **For Claude:** Discover and read the test skill via cache lookup for `skills/dev-test/SKILL.md` for automation options.
>
> **⚠️ NO IMPLEMENTATION WITHOUT TESTS. If this section is empty, STOP.**

- **User's chosen approach:** [From AskUserQuestion in Phase 1: unit/integration/E2E/API]
- **Framework:** [pytest / playwright / jest / etc.]
- **Command:** [e.g., `pytest tests/ -v`]
- **Testing skill to use:** [dev-test-electron / dev-test-playwright / etc.]

### REAL Test Definition (MANDATORY)

> **⚠️ A test that doesn't replicate user workflow is a FAKE test. Define REAL tests NOW.**

| Field | Value |
|-------|-------|
| **User workflow to replicate** | [e.g., "highlight text → click Claude panel → see '⧉ X lines selected'"] |
| **Code paths that must be exercised** | [e.g., "WebSocket connection, not HTTP"] |
| **What user actually sees/verifies** | [e.g., "Status bar shows selection count"] |
| **Protocol/transport** | [e.g., "WebSocket" or "HTTP" or "IPC"] |

### First Failing Test

- **Test name:** [e.g., `test_selection_shows_in_claude_panel`]
- **What it tests:** [Specific behavior]
- **How it replicates user workflow:** [Step by step]
- **Expected failure message:** [What RED looks like]

### The Iron Law of REAL Tests

**If the test doesn't do what the user does, it's a FAKE test.** See `references/dev-common-constraints.md` (C2) and `references/real-test-enforcement.md` for the full REAL vs FAKE detection tables and protocol mismatch examples.

### No Test Infrastructure? That's a BLOCKER.

If the project has no tests, your first task is to ADD test infrastructure, not skip testing.

| Situation | Response |
|-----------|----------|
| "Project has no tests" | Add test framework as Task 0 |
| "Hard to test (DOM/UI/etc)" | Use E2E tools: Playwright, ydotool, screenshot comparison |
| "No time for tests" | TDD saves time. No shortcuts. |
| "User said manual testing" | Push back. Ask what's blocking automation. |

## Open Questions
- [Questions to resolve during exploration]
```

**Note:** No "Chosen Approach" yet - that comes after exploration and design phases.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Start coding to show progress" | Progress on wrong requirements is negative progress | **Anti-helpful** |
| **Competence** | "I can infer what user wants" | Your inference is a guess — guesses become bugs | **Incompetent** |
| **Efficiency** | "Requirements are obvious, skip questions" | You build the wrong thing, rework everything | **Inefficient** |

**The protocol is not overhead you pay. It is the service you provide.**

## Red Flags - STOP If You're About To:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Spawn explore agent | You're exploring before understanding | Ask questions first |
| Read source files | You're looking at code before requirements are clear | Ask what user wants |
| Propose approaches | You're jumping ahead - you need exploration first | Save for /dev-design |
| Create task list | You're planning before you understand the requirements | Finish brainstorm first |

## Output

Brainstorm complete when:
- Problem is clearly understood
- Requirements defined
- Success criteria defined
- `.planning/SPEC.md` written (draft)
- Open questions identified for exploration

### Exit Gate

**Checkpoint type:** human-verify (auto-advanceable — SPEC.md content is machine-verifiable)

Before transitioning to dev-explore, ALL checks must pass:

```
1. IDENTIFY: `.planning/SPEC.md` exists
2. RUN: `Read(".planning/SPEC.md")`
3. READ: Verify it contains: Problem Statement, Success Criteria, Scope sections
4. VERIFY: User has confirmed the objectives (explicit approval, not assumed)
5. CLAIM: Only proceed to dev-explore if ALL checks pass
```

**If any check fails, do NOT proceed. Fix the gap before transitioning.**

### Delete & Restart Protocol

If a gate check fails:

| Failure | Action |
|---------|--------|
| SPEC.md missing required sections | Delete SPEC.md, re-run brainstorm with focus on missing sections |
| User hasn't confirmed objectives | Ask user to confirm before proceeding — do NOT assume approval |
| Testing strategy empty | Re-ask testing questions (Step 2) — this is a BLOCKER |
| Success criteria vague or missing | Re-ask requirements questions — do NOT proceed with weak criteria |

**Do NOT patch a broken SPEC.md. Delete it and restart brainstorm with the gap identified.** Partial fixes to wrong-foundation work create worse outcomes than restarting.

After fixing, re-run ALL gate checks (not just the one that failed).

## Phase Complete

**REQUIRED SUB-SKILL:** After completing brainstorm, dispatch the spec reviewer before exploring:

**Spec Review Gate (MANDATORY):**

Read `${CLAUDE_SKILL_DIR}/../../skills/dev-spec-reviewer/SKILL.md` and follow its instructions.

Follow the spec reviewer's instructions:
1. Dispatch reviewer subagent
2. If ISSUES_FOUND → fix SPEC.md → re-dispatch (max 5 iterations)
3. If APPROVED → proceed to explore

**After spec review APPROVED, start explore phase - Phase 2:**

Read `${CLAUDE_SKILL_DIR}/../../skills/dev-explore/SKILL.md` and follow its instructions.
