---
name: dev-delegate
version: 1.0
description: "Internal skill used by dev-implement during Phase 5 of /dev workflow. NOT user-facing - should only be invoked by dev-ralph-loop inside each implementation iteration. Handles Task agent spawning with TDD enforcement and two-stage review (spec compliance + code quality)."
---

**Announce:** "I'm using dev-delegate to dispatch implementation subagents."

## Contents

- [The Iron Law of Delegation](#the-iron-law-of-delegation)
- [Where This Fits](#where-this-fits)
- [The Process](#the-process)
- [Honesty Requirement](#honesty-requirement)
- [Rationalization Prevention](#rationalization-prevention)

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**EVERY IMPLEMENTATION MUST GO THROUGH A TASK AGENT. This is not negotiable.**

Main chat MUST NOT:
- Write code directly
- Make "quick fixes"
- Edit implementation files
- "Just do this one thing"

**If you're about to write code in main chat, STOP. Spawn a Task agent instead.**
</EXTREMELY-IMPORTANT>

## Where This Fits

```
Main Chat                          Task Agent
─────────────────────────────────────────────────────
dev-implement (orchestrates)
  → dev-ralph-loop (per-task loops)
    → dev-delegate (this skill)
      → spawns Task agent ──────→ follows dev-tdd
                                  uses dev-test tools
```

**Main chat** uses this skill to spawn Task agents.
**Task agents** follow `dev-tdd` (TDD protocol) and use `dev-test` (testing tools).

## Core Principle

**Fresh subagent per task + two-stage review = high quality, fast iteration**

- Implementer subagent does the work (following dev-tdd)
- Spec reviewer confirms it matches requirements
- Quality reviewer checks code quality
- Loop until both approve

## When to Use

Called by `dev-implement` inside each ralph loop iteration. Don't invoke directly.

## The Process

```
For each task:
    1. Dispatch implementer subagent
       - If questions → answer, re-dispatch
       - Implements, tests, commits
    2. Dispatch spec reviewer subagent
       - If issues → implementer fixes → re-review
    3. Dispatch quality reviewer subagent
       - If issues → implementer fixes → re-review
    4. Mark task complete
```

## Step 1: Dispatch Implementer

**Pattern:** Use structured delegation template from `lib/references/delegation-template.md`

Every delegation MUST include:
1. TASK - What to do
2. EXPECTED OUTCOME - Success criteria
3. REQUIRED SKILLS - Why this agent
4. REQUIRED TOOLS - What they'll need
5. MUST DO - Non-negotiable constraints
6. MUST NOT DO - Hard blocks
7. CONTEXT - Parent session state
8. VERIFICATION - How to confirm completion

Use this Task invocation (fill in brackets):

```
Task(subagent_type="workflows:dev-implementer", prompt="""
# TASK

Implement: [TASK NAME]

## EXPECTED OUTCOME

You will have successfully completed this task when:
- [ ] [Success criterion 1]
- [ ] [Success criterion 2]
- [ ] Tests pass (TDD enforced)
- [ ] No regressions in existing tests

## REQUIRED SKILLS

This task requires:
- [Language/framework]: [Why]
- Testing: TDD (test-first mandatory)
- [Other skills as needed]

## REQUIRED TOOLS

You will need:
- Read: Examine existing code
- Write: Create new files
- Edit: Modify existing files
- Bash: Run tests and verify

**Tools denied:** None (full implementation access)

## MUST DO

- [ ] Write test FIRST (TDD RED-GREEN-REFACTOR)
- [ ] Run test suite after each change
- [ ] Follow existing code patterns in [file]
- [ ] [Other non-negotiable requirements]

## MUST NOT DO

- ❌ Write code before test
- ❌ Skip test execution
- ❌ Use `any` / `@ts-ignore` / type suppression
- ❌ Commit broken code

## CONTEXT

### Task Description
[PASTE FULL TASK TEXT FROM PLAN.md - don't make subagent read file]

### Project Context
- Project: [brief description]
- Related files: [list from exploration]
- Test command: [from SPEC.md]

## TDD Protocol (MANDATORY)

<EXTREMELY-IMPORTANT>
**LOAD THIS SKILL FIRST:**

Before writing any code, you MUST load the TDD skill:

```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-tdd/SKILL.md")
```

This loads:
- Task reframing (your job is writing tests, not features)
- The Execution Gate (6 mandatory gates before E2E testing)
- GATE 5: READ LOGS (mandatory - cannot skip)
- The Iron Law of TDD (test-first approach)

**Load dev-tdd now before proceeding.**
</EXTREMELY-IMPORTANT>

Follow the RED-GREEN-REFACTOR cycle from dev-tdd:

1. **RED**: Write a failing test FIRST
   - Run it, SEE IT FAIL
   - Document: "RED: [test] fails with [error]"

2. **GREEN**: Write MINIMAL code to pass
   - Run test, SEE IT PASS
   - Document: "GREEN: [test] passes"

3. **REFACTOR**: Clean up while staying green

**If you write code before seeing RED, you're not doing TDD. Stop and restart.**

## Testing Tools

For test options (pytest, Playwright, ydotool), load dev-test skill after dev-tdd.

Tests must EXECUTE code and VERIFY behavior. Grepping is NOT testing.

## If Unclear
Ask questions BEFORE implementing. Don't guess.

## Output
Report:
- RED: What test failed and how
- GREEN: What made it pass
- Test command and output
- Commit SHA
- Any concerns
""")
```

**If implementer asks questions:** Answer clearly, then re-dispatch with answers included.

**If implementer finishes:** Proceed to spec review.

## Step 2: Dispatch Spec Reviewer

Use this Task invocation:

```
Task(subagent_type="general-purpose", prompt="""
Review spec compliance for: [TASK NAME]

## Original Requirements
[PASTE TASK TEXT FROM PLAN.md]

## Success Criteria (from SPEC.md)
[PASTE RELEVANT CRITERIA]

## CRITICAL: Do Not Trust the Report

The implementer finished suspiciously quickly. Their report may be incomplete,
inaccurate, or optimistic. You MUST verify everything independently.

**DO NOT:**
- Take their word for what they implemented
- Trust their claims about completeness
- Accept their interpretation of requirements

**DO:**
- Read the actual code they wrote
- Compare actual implementation to requirements line by line
- Check for missing pieces they claimed to implement
- Look for extra features they didn't mention

## Review Checklist
1. Does implementation meet ALL requirements?
2. Is anything MISSING from the spec?
3. Is anything EXTRA not in the spec?

## Output Format
- COMPLIANT: All requirements met, nothing extra (after verifying code yourself)
- ISSUES: List what's missing or extra with file:line references

Be strict. "Close enough" is not compliant. Verify by reading code.
""")
```

**If COMPLIANT:** Proceed to quality review.

**If ISSUES:** Have implementer fix, then re-run spec review.

## Step 3: Dispatch Quality Reviewer

Use this Task invocation:

```
Task(subagent_type="general-purpose", prompt="""
Review code quality for: [TASK NAME]

## Changes to Review
Files modified: [list files]
Commit range: [BASE_SHA]..[HEAD_SHA]

## Review Focus
1. Code correctness (logic errors, edge cases)
2. Test coverage (are tests meaningful?)
3. Code style (matches project conventions?)
4. No regressions introduced

## Confidence Scoring
Rate each issue 0-100. Only report issues >= 80 confidence.

## Output Format
### Strengths
- [what's good]

### Issues (Confidence >= 80)
#### [Issue Title] (Confidence: XX)
- Location: [file:line]
- Problem: [description]
- Fix: [suggestion]

### Verdict
APPROVED or CHANGES REQUIRED
""")
```

**If APPROVED:** Mark task complete, move to next task.

**If CHANGES REQUIRED:** Have implementer fix, then re-run quality review.

## Honesty Requirement

<EXTREMELY-IMPORTANT>
**Claiming "done" without subagent verification is LYING.**

When you say "Task complete", you are asserting:
- A Task agent implemented the change
- Spec reviewer confirmed compliance
- Quality reviewer approved

If ANY of these didn't happen, you are not "summarizing" or "moving on" - you are LYING about the state of the work.

**Dishonest claims destroy trust. Honest "still working" builds trust.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

These thoughts mean STOP—you're about to skip delegation:

| Thought | Reality |
|---------|---------|
| "I'll just fix this quickly" | Quick = sloppy = bugs. Delegate. |
| "The subagent will be slower" | Subagent time is cheap. Your context is expensive. |
| "I already know what to do" | Knowing ≠ doing correctly. Delegate. |
| "It's just one line" | One line can break everything. Delegate. |
| "I'm already looking at the code" | Looking ≠ editing. Delegate. |
| "User is waiting" | User wants CORRECT, not fast. Delegate. |
| "Skip review, it's obviously right" | "Obviously" is how bugs ship. Review. |
| "Spec review passed, skip quality" | Both reviews exist for a reason. Do both. |
| "Quality review found nothing, done" | Did spec review pass first? Check. |

## Red Flags

**Never:**
- Skip either review (spec OR quality)
- Proceed with unfixed issues
- Let implementer self-review replace actual review
- Start quality review before spec compliance passes
- Make subagent read plan file (provide full text)
- Rush past subagent questions

**If subagent fails:**
- Dispatch fix subagent with specific instructions
- Don't fix manually in main chat (context pollution)

## Example Flow

```
Me: Implementing Task 1: Add user validation

[Dispatch implementer with full task text]

Implementer: "Should validation happen client-side or server-side?"

Me: "Server-side only, in the API layer"

[Re-dispatch implementer with answer]

Implementer:
- Added validateUser() in api/users.ts
- Tests: 5/5 passing
- Committed: abc123

[Dispatch spec reviewer]

Spec Reviewer: ISSUES
- Missing: Email format validation (spec line 12)

[Tell implementer to fix]

Implementer:
- Added email regex validation
- Tests: 6/6 passing
- Committed: def456

[Re-dispatch spec reviewer]

Spec Reviewer: COMPLIANT

[Dispatch quality reviewer with commit range]

Quality Reviewer: APPROVED
- Strengths: Good test coverage, clear naming
- No issues >= 80 confidence

[Mark Task 1 complete, move to Task 2]
```

## Integration

**Main chat invokes:**
- `dev-implement` → `dev-ralph-loop` → `dev-delegate` (this skill)

**Task agents follow:**
- `dev-tdd` - TDD protocol (RED-GREEN-REFACTOR)
- `dev-test` - Testing tools (pytest, Playwright, ydotool)

After all tasks complete with passing tests, `dev-implement` proceeds to `dev-review`.
