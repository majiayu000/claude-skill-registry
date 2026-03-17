---
name: next
description: Quickly present 2-4 actionable next steps. Lighter than /debrief - no reconstruction, just options.
---

# Next

The user knows where they are. They just need directions.

## On Activation

1. **Quick scan** - unfinished work, logical next steps, pending items, quick wins
2. **Check TaskList** - if tasks exist, surface unblocked ones
3. **Present 2-4 options** via `AskUserQuestion` - they tap, you execute

No status tables. No reconstruction. Just options.

## Option Quality

Start each option with a verb. Be concrete.

**Good:**

- "Finish the auth refactor in `api.ts`"
- "Run tests and fix failures"
- "Add error handling to the new endpoint"

**Bad:**

- "Continue working" (vague)
- "Maybe look at tests?" (uncertain)
- "We could do several things..." (narrative)

## Example Output

```
AskUserQuestion:
  question: "What's next?"
  header: "Next"
  options:
    - label: "Add tests for UserService"
      description: "Cover the new authentication methods"
    - label: "Wire up the frontend"
      description: "Connect login form to the new endpoint"
    - label: "Clean up TODO comments"
      description: "Quick win - 3 items flagged earlier"
```

## When Context is Empty

If there's nothing to go on:

- Ask what they'd like to work on
- Offer to explore the codebase
- Suggest reviewing recent git activity

## Anti-patterns

- Status tables (that's /debrief)
- Reconstructing what happened (that's /debrief)
- More than 4 options (decision paralysis)
- Fewer than 2 options (not useful)
- Making them type when they could tap

---

Enter next mode now. Scan context, check TaskList, present 2-4 options via AskUserQuestion. No preamble.
