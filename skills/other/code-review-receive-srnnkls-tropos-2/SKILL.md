---
name: code-review-receive
description: Technical evaluation of code review feedback. Use when receiving review feedback - requires verification before implementing, no performative agreement, push back when technically wrong.
---

# Code Review Reception

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

---

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

---

## Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)
- Any performative agreement

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

---

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Feedback: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

WRONG: Implement 1,2,3,6 now, ask about 4,5 later
RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5."
```

---

## YAGNI Check

When reviewer suggests adding features:

```
IF reviewer suggests "implementing properly":
  Search codebase for actual usage

  IF unused: "This isn't called anywhere. Remove it (YAGNI)?"
  IF used: Then implement properly
```

---

## When to Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with prior architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Escalate if architectural

---

## Implementation Order

For multi-item feedback:

1. Clarify anything unclear FIRST
2. Then implement in order:
   - Blocking issues (breaks, security)
   - Simple fixes (typos, imports)
   - Complex fixes (refactoring, logic)
3. Test each fix individually
4. Verify no regressions

---

## Acknowledging Correct Feedback

When feedback IS correct:

```
DO:    "Fixed. [Brief description of what changed]"
DO:    "Good catch - [specific issue]. Fixed in [location]."
DO:    [Just fix it and show in the code]

DON'T: "You're absolutely right!"
DON'T: "Thanks for catching that!"
DON'T: ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it.

---

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:

```
DO:    "Verified and you're correct. My understanding was wrong. Fixing."
DON'T: Long apology or defending why you pushed back
```

State the correction factually and move on.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |

---

## Integration

**Use with:**
- `task-dispatch` - Handle review between tasks
- `code-test` - Test each fix individually
- `completion-verify` - Verify fixes actually work
