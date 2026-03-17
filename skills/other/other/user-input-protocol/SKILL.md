---
name: user-input-protocol
description: >-
  Structured checkpoint format for requesting human input. When an agent
  needs a decision, it must stop, present context, show options, and wait.
  Activate when delegating to subagents, running background tasks, or
  hitting any decision point that requires human judgment.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: build
  standalone: true
---

# User Input Protocol

**Value:** Respect -- the developer's judgment governs all consequential
decisions. The agent never assumes when it should ask.

## Purpose

Defines a structured format for agents to request human input at decision
points. Prevents agents from making assumptions on the developer's behalf,
ensures questions include enough context for informed decisions, and provides
a pause-and-resume pattern for subagents that cannot directly prompt the user.

## Practices

### Stop and Present, Never Assume

When you encounter a decision that requires human judgment, stop working
immediately. Do not guess. Do not pick the "most likely" option. Present
the decision clearly and wait.

Decisions that require human input:
- Business rule ambiguities (two valid interpretations exist)
- Architecture trade-offs (performance vs. simplicity, etc.)
- Scope questions (should this feature include X?)
- Destructive actions (deleting files, force-pushing, dropping data)

Decisions that do NOT require human input:
- Implementation details with one clearly correct answer
- Formatting, naming, or style choices covered by project conventions
- Test structure when requirements are unambiguous

### Use the AWAITING_USER_INPUT Format

When you need input, output this structured checkpoint:

```
AWAITING_USER_INPUT
---
Context: [Why you are asking -- what you were doing and what you found]
Decision needed: [The specific question, one sentence]
Options:
  A) [Label] -- [What this means and its implications]
  B) [Label] -- [What this means and its implications]
  C) [Label] -- [What this means and its implications]
Recommendation: [Which option you suggest and why, or "No recommendation"]
---
```

Rules for the checkpoint:
- Context must explain what led to this question (not just "I need input")
- Provide 2-4 specific options. Never ask open-ended "what should I do?"
- Each option must include implications, not just a label
- State your recommendation if you have one -- the developer can override

**Example:**
```
AWAITING_USER_INPUT
---
Context: While implementing the login endpoint, I found two email validation
patterns in the codebase. auth/validate.rs uses strict RFC 5322 parsing.
signup/forms.rs uses a simple regex check. These produce different results
for edge cases like "user+tag@example.com".
Decision needed: Which email validation approach should be the project standard?
Options:
  A) Strict RFC 5322 -- rejects fewer valid addresses, more complex to maintain
  B) Simple regex -- faster, but may accept malformed addresses
  C) Context-dependent -- strict for auth, lenient for forms
Recommendation: A) Strict RFC 5322, applied everywhere for consistency
---
```

### Save State Before Pausing (Subagents)

Subagents and background tasks typically cannot prompt the user directly.
When a subagent needs input, it must save its progress before pausing so
work can resume without starting over.

State to save before pausing:
1. What task you were performing
2. What files you created or modified
3. What analysis you completed
4. The specific decision that blocked you
5. Enough context to continue immediately when resumed

Where to save state depends on your harness:
- Task metadata (Claude Code: TaskUpdate with metadata)
- File system (write a JSON checkpoint to a temp file)
- Memory tools (MCP servers, if available)

After saving state, output the AWAITING_USER_INPUT checkpoint and stop.
The orchestrator or main conversation detects the pause, presents the
question to the user, and resumes the subagent with the answer.

### Resume Without Redoing Work

When resumed with the user's answer:
1. Retrieve your saved state
2. Confirm you have the files and context you need
3. Apply the user's decision
4. Continue from where you stopped

**Do not** re-analyze files you already analyzed. **Do not** re-read
context you already saved. The purpose of state preservation is to make
resumption instant.

**Do:**
- "You chose strict RFC 5322. Applying to the login endpoint now."

**Do not:**
- "Let me re-analyze the codebase to understand the email validation..."

### Handle Multi-Question Checkpoints

When multiple related decisions are needed, group them in one checkpoint
rather than pausing repeatedly. Number each question.

```
AWAITING_USER_INPUT
---
Context: Setting up the test infrastructure for the new auth module.
Decisions needed:

1. Test framework?
   A) Jest -- already used in 3 other modules
   B) Vitest -- faster, but would introduce a second test runner
   Recommendation: A) Jest for consistency

2. Test file location?
   A) Colocated (auth/__tests__/) -- matches signup module pattern
   B) Top-level (tests/auth/) -- matches API module pattern
   Recommendation: A) Colocated, to match the newer module convention
---
```

## Enforcement Note

This skill is advisory. It instructs agents to pause at decision points
and use structured checkpoints. On harnesses with plugin support, enforcement
hooks can detect when an agent makes assumptions without pausing. On harnesses
without enforcement, the agent follows these practices by convention. If you
observe the agent making decisions it should have asked about, point it out.
For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After applying this skill, verify:

- [ ] Every decision requiring human judgment used AWAITING_USER_INPUT format
- [ ] Each checkpoint included context, options with implications, and a recommendation
- [ ] No open-ended questions were asked ("what should I do?")
- [ ] Subagents saved state before pausing
- [ ] Resumed work used saved state without re-analyzing
- [ ] Related decisions were grouped into single checkpoints

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **orchestration:** Main orchestrator detects paused subagents and relays questions to the user
- **tdd-cycle:** When test requirements are ambiguous, pause and clarify acceptance criteria
- **debugging-protocol:** When debugging reveals ambiguous root causes, pause and ask

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill orchestration
```
