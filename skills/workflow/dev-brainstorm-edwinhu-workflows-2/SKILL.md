---
name: dev-brainstorm
description: "REQUIRED Phase 1 of /dev workflow. Uses Socratic questioning to understand requirements before exploration."
---

**Announce:** "I'm using dev-brainstorm (Phase 1) to gather requirements."

## Workflow Initialization

Create `.claude/ACTIVE_WORKFLOW.md` to track workflow state:

```yaml
---
workflow: dev
phase: 1
phase_name: brainstorm
started: [current timestamp]
project_root: [current directory]
active_skill: ${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-brainstorm/SKILL.md
spec: .claude/SPEC.md
plan: .claude/PLAN.md
---
```

This enables session persistence - returning to the project will reload the current phase.

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

### Honesty Framing

**Guessing user requirements is LYING about what they want.**

Asking questions is cheap. Building the wrong thing is expensive. Every minute spent clarifying requirements saves hours of wasted implementation.

### No Pause After Completion

After writing `.claude/SPEC.md` and completing brainstorm, immediately invoke the next phase:

**Invoke the explore phase:**

```bash
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-explore/SKILL.md")
```

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

### The Iron Law of REAL Tests

**A test that doesn't replicate the user's actual workflow is a FAKE test.**

| REAL Test | FAKE Test (looks like a test, isn't) |
|-----------|--------------------------------------|
| Simulates actual user action | Calls function programmatically |
| Uses same protocol as production | Uses different protocol |
| Verifies what user sees | Verifies internal state only |
| Follows user's exact sequence | Takes shortcuts |
| Uses skill user specified | Ignores skill, writes own thing |

### Protocol Mismatch Examples (Common Fake Test Trap)

| Production Uses | FAKE Test Uses | Result |
|-----------------|----------------|--------|
| WebSocket | HTTP | Wrong code path |
| GraphQL | REST mock | Wrong serialization |
| Async/await | Sync calls | Race conditions hidden |
| IPC (Electron) | Direct import | Process boundary skipped |
| CLI invocation | Function call | Argument parsing skipped |

**The test must use the SAME protocol/transport as production.**

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

Write the initial spec to `.claude/SPEC.md`:

```markdown
# Spec: [Feature Name]

> **For Claude:** After writing this spec, use `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-explore/SKILL.md")` for Phase 2.

## Problem
[What problem this solves]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Constraints
- [Any limitations or boundaries]

## Testing Strategy (MANDATORY - USER APPROVED)

> **For Claude:** Use `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-test/SKILL.md")` for automation options.
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

**If the test doesn't do what the user does, it's a FAKE test.**

| ✅ REAL TEST | ❌ FAKE TEST (looks like test, isn't) |
|--------------|---------------------------------------|
| Uses same protocol as production | Tests different protocol |
| Clicks actual UI elements | Calls functions programmatically |
| Verifies what user sees | Verifies internal state only |
| Follows user's exact sequence | Takes shortcuts |
| Uses skill user specified | Ignores skill, writes own thing |
| Fails when feature is broken | Passes even when feature is broken |

### Fake Test Detection (Red Flags)

**If you catch yourself doing these, STOP - you're writing a FAKE test:**

| What You're Doing | Why It's Fake | Do Instead |
|-------------------|---------------|------------|
| Using different protocol than production | Wrong code path | Use same protocol |
| Calling function directly instead of user action | Skipping user workflow | Simulate actual user action |
| Changing assertions to make tests pass | Hiding bugs | Question if test is valid |
| Ignoring the testing skill user specified | "I know better" arrogance | Use the specified skill |
| Testing internal state, not user-visible output | Missing the point | Test what user sees |
| Mocking the thing you're supposed to test | Defeats the purpose | Test actual behavior |
| Skipping async/await when production uses it | Race conditions hidden | Match async behavior |

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
- `.claude/SPEC.md` written (draft)
- Open questions identified for exploration

## Phase Complete

**REQUIRED SUB-SKILL:** After completing brainstorm, immediately invoke the explore phase:

**Start explore phase - Phase 2:**

```bash
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-explore/SKILL.md")
```
