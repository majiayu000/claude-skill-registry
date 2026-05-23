---
name: make-plan
description: Use when solution space exploration is complete and you're ready to create
  an implementation plan. Enforces "simple over easy" - the fundamentally right solution,
  not the path of least resistance. Triggers after /discover-solution-space, when
  a solution has been chosen, or when asked to "make a plan" or "create a plan".
argument-hint: <optional: solution choice or constraint>
---

# Make Plan

Create a comprehensive implementation plan and enter plan mode for execution.

## Position in Workflow

Step 3 of development workflow:
1. `/research` - Understand problem, explore implementation
2. `/discover-solution-space` - Explore solutions
3. `/make-plan` - Create implementation plan (THIS)
4. Code, review, ship

## Core Principle

**First principles. Simple over easy. Go deep.**

You have a bias toward finishing quickly. Resist it.

Never cut corners or take the path of least resistance. Prefer the fundamentally right solution even if it requires significantly more work. The cost of a suboptimal solution compounds over time. Rushed plans degrade codebases.

**Simple ≠ Easy:**
- **Easy**: Less work now, more pain later (shortcuts, hacks, "good enough")
- **Simple**: More work now, less pain forever (clean, maintainable, right)

Always choose simple. Always go deep enough to find it.

## Input

**Default:** Use chosen solution from current conversation context.

**If argument provided:** Additional constraint or clarification for the plan.

## Workflow

### 1. Verify Ready State

Before planning, confirm:
- Research is complete (problem understood)
- Solution space was explored
- A solution has been chosen

If missing context, ask: "I need [research/solution choice] before creating a plan. Should I run `/research` or `/discover-solution-space` first?"

### 2. Specify Behavior Explicitly

**This is the most critical step.** Be exhaustive.

For each feature/change, document:

#### Desired Behavior
- What SHOULD happen in normal cases
- Expected outputs for typical inputs
- Success criteria

#### Undesired Behavior
- What MUST NOT happen
- Edge cases to handle gracefully
- Error conditions and their responses

#### Usage Patterns
- Common usage patterns (happy path)
- Unhappy paths (errors, edge cases, invalid input)
- Boundary conditions

**Example format:**
```
## Behavior: User Authentication

### Desired
- Valid credentials → session created, redirect to dashboard
- Session expires after 24h of inactivity
- Invalid credentials → clear error message, no session

### Undesired
- NEVER store password in plain text
- NEVER expose session token in URL
- NEVER allow infinite login attempts

### Edge Cases
- Expired password → prompt reset before login
- Concurrent sessions → configurable limit
- Network timeout during auth → retry with backoff
```

### 3. Go Deep - Gather Sufficient Context

**Do not plan without full understanding.** Read more code than feels necessary. Understand the implications of each decision.

Before finalizing any part of the plan:
- Read all related files, not just the obvious ones
- Understand how similar problems were solved elsewhere in the codebase
- Trace the full impact of proposed changes
- Identify hidden dependencies and side effects

**You are not ready to plan if:**
- You haven't read the files your changes will affect
- You don't understand the existing patterns in this area
- You're making assumptions instead of verifying

### 4. Apply First Principles Check

For each part of the plan, challenge ruthlessly:

| Question | Purpose |
|----------|---------|
| Is this necessary? | Avoid bloat |
| Is there a simpler approach? | Simple > easy |
| Does this fight the codebase? | Respect existing patterns |
| What would we regret in 6 months? | Long-term thinking |
| Are we cutting corners? | No shortcuts |
| Do I have enough context? | Go deeper if uncertain |

**Red flags - STOP and reconsider:**
- "This is faster but..." → You're choosing easy over simple
- "We can clean this up later..." → You won't. Do it right now.
- "Good enough for now..." → It will become permanent tech debt
- Adding TODO comments for "later" → Later never comes
- Skipping error handling "for simplicity" → That's not simplicity, it's negligence
- "I think this should work..." → You don't know. Go read more code.
- Feeling rushed → Slow down. Bad plans cost more than slow plans.

### 5. Design Tests

Write test specifications BEFORE implementation details:

**Test design principles:**
- Test behavior, not implementation
- Cover happy paths AND edge cases
- One assertion per test (when practical)
- Tests should be fast and isolated

**Format:**
```
## Tests

### Unit Tests
- `test_valid_credentials_creates_session` - happy path
- `test_invalid_credentials_returns_error` - error case
- `test_expired_password_prompts_reset` - edge case

### Integration Tests
- `test_full_login_flow_with_redirect`
- `test_session_timeout_behavior`
```

### 6. Enter Plan Mode

After documenting behavior and tests, switch to plan mode:

**Say:** "Entering plan mode to create the implementation plan."

Then use the `EnterPlanMode` tool.

## Output Format (Before Plan Mode)

```markdown
## Implementation Plan: [Feature Name]

### Chosen Solution
[Brief restatement of chosen approach from /discover-solution-space]

### Behavior Specification

#### [Component/Feature 1]

**Desired:**
- [What should happen]

**Undesired:**
- [What must not happen]

**Edge Cases:**
- [Boundary conditions and handling]

#### [Component/Feature 2]
[Same structure]

### Tests

#### Unit Tests
- `test_name` - [what it verifies]

#### Integration Tests
- `test_name` - [what it verifies]

### First Principles Check
- [Confirmation that no shortcuts are taken]
- [Confirmation of simplest viable approach]
- [Alignment with existing patterns]

---

Entering plan mode to create implementation steps.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Insufficient context gathering | Read ALL related files before planning |
| Vague behavior specs | Write explicit examples for each case |
| Only happy path | Always include unhappy paths and edge cases |
| Tests as afterthought | Design tests BEFORE implementation |
| Shortcut rationalization | Apply first principles check ruthlessly |
| Rushing to plan mode | Complete behavior spec first |
| Missing "undesired" section | Explicitly state what must NOT happen |
| Planning with assumptions | Verify by reading code, don't assume |
| Choosing easy over simple | More work now = less pain forever |

## What NOT to Do

- Do NOT plan without reading all affected code
- Do NOT make assumptions - verify by reading
- Do NOT skip behavior specification
- Do NOT leave edge cases undefined
- Do NOT take shortcuts for "simplicity"
- Do NOT skip the first principles check
- Do NOT enter plan mode without tests designed
- Do NOT proceed if solution wasn't explicitly chosen
- Do NOT rush - bad plans cost more than slow plans
- Do NOT rationalize shortcuts with "we can fix it later"
