---
name: dev-clarify
description: "Asks targeted clarification questions based on codebase exploration findings."
user-invocable: false
disable-model-invocation: true
---

**Announce:** "I'm using dev-clarify (Phase 3) to resolve ambiguities."

## Contents

- [The Iron Law of Clarification](#the-iron-law-of-clarification)
- [What Clarify Does](#what-clarify-does)
- [Process](#process)
- [Question Categories](#question-categories)
- [Red Flags](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Post-Exploration Clarification

Ask targeted questions based on what exploration revealed.
**Prerequisite:** Exploration phase complete, key files read.

<EXTREMELY-IMPORTANT>
## The Iron Law of Clarification

**ASK BEFORE DESIGNING. This is not negotiable.**

After exploration, you now know:
- What exists in the codebase
- What patterns are used
- What integrations are needed

Use this knowledge to ask **informed questions** about:
- Edge cases the code will need to handle
- Integration points with existing systems
- Behavior in ambiguous scenarios

**If you catch yourself about to design without resolving ambiguities, STOP.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The pattern choice is obvious" | Multiple patterns exist for a reason | ASK which to follow |
| "I can decide edge cases myself" | Your assumptions don't match user expectations | ASK for clarification |
| "This is a small detail" | Small details cause big bugs | ASK about edge cases now |
| "I'll handle integration points during implementation" | Wrong integration breaks everything | CLARIFY integration NOW |
| "The exploration gave me enough info" | Code tells you HOW, not WHAT SHOULD happen | ASK for requirements, not just patterns |
| "I can make a reasonable assumption" | Reasonable != correct | ASK, don't assume |
| "Asking too many questions annoys users" | Building wrong thing annoys users more | ASK clarifying questions |

### Drive-Aligned Framing

**Assuming user requirements without asking is NOT HELPFUL — you build the wrong thing and create hours of rework.**

You explored the codebase and found patterns. But patterns show HOW things work, not WHAT the user wants. Clarification bridges this gap.

Asking costs minutes. Wrong assumptions cost hours of rework.

### No Pause After Completion

After updating `.planning/SPEC.md` with all clarified requirements, IMMEDIATELY invoke:

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-design/SKILL.md` and follow its instructions.

DO NOT:
- Summarize what you learned
- Ask "should I proceed to design?"
- Wait for user confirmation
- Write status updates

The workflow phases are SEQUENTIAL. Complete clarify → immediately start design.

## What Clarify Does

| DO | DON'T |
|----|-------|
| Ask questions based on exploration | Ask vague/generic questions |
| Reference specific code patterns found | Repeat questions from brainstorm |
| Clarify integration points | Propose approaches (that's design) |
| Resolve edge cases | Make assumptions |
| Update SPEC.md with answers | Skip to implementation |

**Clarify answers: WHAT EXACTLY should happen in specific scenarios**
**Design answers: HOW to build it** (next phase)

## Process

### 1. Review Exploration Findings

Before asking questions, review:
- Key files you read
- Patterns discovered
- Architecture insights
- Integration points identified

### 2. Identify Ambiguities

Common areas needing clarification after exploration:

**Integration Points:**
- "The existing auth system uses JWT. Should the new feature use the same token or create a new session type?"

**Edge Cases:**
- "What happens if [condition discovered in code]?"

**Scope Boundaries:**
- "The existing feature handles X. Should the new feature also handle X or is that out of scope?"

**Behavior Choices:**
- "I found two patterns in the codebase for this. Pattern A in `file.ts:23` and Pattern B in `other.ts:45`. Which should we follow?"

### 3. Ask Questions with AskUserQuestion

Present questions with context from exploration:

```
AskUserQuestion(questions=[{
  "question": "The auth middleware at src/middleware/auth.ts:78 validates tokens synchronously. The new endpoint needs user data. Should we: validate synchronously (faster, simpler) or fetch fresh user data (slower, always current)?",
  "header": "Auth pattern",
  "options": [
    {"label": "Sync validation (Recommended)", "description": "Faster, uses cached token claims, matches existing patterns"},
    {"label": "Fresh fetch", "description": "Slower, always current, needed if user data changes frequently"}
  ],
  "multiSelect": false
}])
```

**Key principles:**
- Reference specific files/lines from exploration
- Lead with recommendation based on codebase patterns
- Explain trade-offs clearly
- One question at a time for complex topics

### Smart-Discuss: Batch Ambiguities

When multiple ambiguities are discovered during exploration, batch them into ONE AskUserQuestion call instead of asking sequentially:

**Sequential (slow — 5 round-trips):**
1. "Should we use REST or GraphQL?" → wait
2. "Should auth be JWT or session?" → wait
3. "Should we support pagination?" → wait
...

**Batched (fast — 1 round-trip):**
```python
AskUserQuestion(questions=[
  {"question": "API style?", "options": [{"label": "REST"}, {"label": "GraphQL"}]},
  {"question": "Auth mechanism?", "options": [{"label": "JWT"}, {"label": "Session-based"}]},
  {"question": "Pagination?", "options": [{"label": "Yes, cursor-based"}, {"label": "Yes, offset"}, {"label": "Not needed"}]}
], multiSelect=false)
```

**When to batch:** After reading exploration findings, if 3+ questions arise, batch them. Present all ambiguities at once with options and pros/cons for each.

**When NOT to batch:** If a question's answer changes what other questions to ask (dependent questions), ask the blocking question first, then batch the rest.

### 4. Update SPEC.md

After each answer, update `.planning/SPEC.md`:
- Add clarified requirements
- Document decisions made
- Note trade-offs accepted

```markdown
## Clarified Requirements

### Auth Pattern
- Decision: Sync validation
- Rationale: Matches existing patterns, user data changes infrequently
- Reference: src/middleware/auth.ts:78

### Edge Case: Expired Token
- Decision: Return 401, let client refresh
- Rationale: Consistent with other endpoints
```

## Question Categories

### Must Ask (based on exploration)
- Integration points with existing systems
- Patterns to follow (when multiple exist)
- Edge cases revealed by code reading
- **Testing strategy (if not resolved in brainstorm/explore)**

### Testing Strategy Clarification (MANDATORY IF MISSING)

<EXTREMELY-IMPORTANT>
**If exploration found no test infrastructure, this MUST be resolved now.**

Before proceeding to design, ensure testing strategy is clear:

```python
AskUserQuestion(questions=[{
  "question": "No test infrastructure was found. How should we verify this feature works?",
  "header": "Testing",
  "options": [
    {"label": "Add pytest/jest as Task 0 (Recommended)", "description": "Set up test framework before implementing feature"},
    {"label": "Add E2E tests with Playwright", "description": "Browser automation to test user interactions"},
    {"label": "Add E2E tests with ydotool", "description": "Desktop automation for native apps"},
    {"label": "Other (describe in chat)", "description": "Propose alternative testing approach"}
  ],
  "multiSelect": false
}])
```

**"Manual testing" is NOT an acceptable answer.** If user insists on manual testing:

1. Explain: "TDD requires automated tests. Manual testing means we can't do TDD."
2. Ask: "What's blocking automated tests? Let's solve that."
3. If truly impossible: "Then we need to exit /dev workflow and use a different approach."

**Do NOT proceed to design without a clear automated testing strategy.**
</EXTREMELY-IMPORTANT>

### Follow-up Testing Questions

After user chooses testing approach, clarify specifics:

```python
AskUserQuestion(questions=[{
  "question": "What's the FIRST test you want to see fail?",
  "header": "First Test",
  "options": [
    {"label": "Happy path - feature works correctly", "description": "Test the main success scenario"},
    {"label": "Error case - feature handles bad input", "description": "Test error handling"},
    {"label": "Edge case - specific boundary condition", "description": "Test a known edge case"},
    {"label": "Integration - feature works with existing code", "description": "Test system integration"}
  ],
  "multiSelect": false
}])
```

**Why this matters:** Defining the first test BEFORE implementation is the essence of TDD.

### User Workflow Replication (MANDATORY FOR REAL TESTS)

<EXTREMELY-IMPORTANT>
**If the test doesn't replicate the user's workflow, it's a FAKE test.**

Based on code path discovery from exploration, clarify the exact workflow:

```python
AskUserQuestion(questions=[{
  "question": "Let me confirm the user workflow the test must replicate:",
  "header": "Workflow",
  "options": [
    {"label": "Confirm workflow", "description": "[State the discovered workflow, e.g., 'highlight → click panel → see status']"},
    {"label": "Modify workflow", "description": "The workflow is different - let me describe it"},
    {"label": "Add steps", "description": "The workflow has additional steps I should know"}
  ],
  "multiSelect": false
}])
```

**Then verify the test approach matches:**

```python
AskUserQuestion(questions=[{
  "question": "The test must use [discovered protocol, e.g., WebSocket]. Is this correct?",
  "header": "Protocol",
  "options": [
    {"label": "Yes, use [protocol]", "description": "Test must use the same protocol as production"},
    {"label": "No, different protocol", "description": "Explain the correct protocol"}
  ],
  "multiSelect": false
}])
```

### Verify Test Will Be REAL

After clarifying workflow and protocol, verify:

```
[ ] Test workflow matches user workflow exactly
[ ] Test uses same protocol as production
[ ] Test interacts with same UI elements user sees
[ ] Test verifies same output user verifies
[ ] Testing skill is appropriate for this workflow
```

If any of these don't match, the test will be FAKE. Clarify now.

### Test Strategy Validation

Before proceeding to design, verify the testing strategy passes real-test enforcement. See `references/real-test-enforcement.md` for what constitutes a REAL vs FAKE test.

**If the test approach doesn't match what you discovered, STOP and clarify.**
</EXTREMELY-IMPORTANT>

### Optional (if unclear)
- Performance requirements
- Error handling preferences
- Backward compatibility needs

### Don't Ask (already decided)
- What the feature does (that's brainstorm)
- Whether to build it (user already decided)
- Architecture approach (that's design)

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "I don't want to bother the user with questions" | You build the wrong thing — your courtesy was sabotage | **Anti-helpful** |
| **Competence** | "I can infer edge cases from the code" | Code shows HOW, not WHAT SHOULD happen — your inference was a guess | **Incompetent** |
| **Efficiency** | "Assumptions are faster than questions" | Wrong assumptions mean rework — your speed was waste | **Inefficient** |

**The protocol is not overhead you pay. It is the service you provide.**

## Red Flags - STOP If You're About To:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Ask without exploration context | Questions will be generic | Reference specific code findings |
| Propose architecture | Too early, still clarifying | Ask questions, save design for next phase |
| Make assumptions | Leads to rework | Ask and get explicit answer |
| Skip to design | Ambiguities cause bugs | Resolve all questions first |

## Output

Clarification complete when:
- All integration points clarified
- Edge cases resolved
- Pattern choices made
- `.planning/SPEC.md` updated with final requirements
- No remaining ambiguities
- **Automated testing strategy confirmed (MANDATORY)**

### Exit Gate

**Checkpoint type:** human-verify

### Testing Strategy Gate Check

**Checkpoint type:** decision (user chooses testing approach — cannot auto-advance)

Before proceeding to design, verify in SPEC.md:

```
[ ] Testing approach documented (unit/integration/E2E)
[ ] Test framework specified (pytest/jest/playwright/etc.)
[ ] First test described (what will fail first)
[ ] Test command documented (how to run tests)
```

**If any box is unchecked → STOP. Do not proceed to design.**

### REAL Test Gate Check (MANDATORY)

Before proceeding to design, verify REAL test criteria:

```
[ ] User workflow confirmed and documented
[ ] Protocol/transport verified (same as production)
[ ] UI elements to test identified
[ ] Testing skill specified (dev-test-electron/playwright/etc.)
[ ] Test approach matches discovered code paths
```

**If any box is unchecked → You WILL write fake tests. Clarify now.**

### Fake Test Prevention Gate

See `references/real-test-enforcement.md` for detection tables and the Iron Law of REAL Tests.

Ask yourself:
1. Does the test do what the user does? (Not a shortcut)
2. Does the test use the same protocol? (Not a mock)
3. Does the test verify what the user sees? (Not internal state)

If ANY answer is "no" or "not sure" → STOP. Clarify before design.

This is the last checkpoint before implementation planning. Fake tests caught here save hours of wasted implementation.

## Phase Complete

**REQUIRED SUB-SKILL:** After completing clarification, IMMEDIATELY invoke:

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-design/SKILL.md` and follow its instructions.
