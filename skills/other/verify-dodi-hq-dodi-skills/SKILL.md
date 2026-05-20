---
name: verify
description: Use before any completion claim, commit, or PR — requires running verification commands and confirming output before making success claims
---

# Verify

**Core principle:** Evidence before claims, always.

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate

Before claiming any status:

1. **IDENTIFY** — what command proves this claim?
2. **RUN** — execute it (fresh, complete)
3. **READ** — full output, check exit code
4. **CONFIRM** — does output support the claim?
5. **THEN** — make the claim with evidence

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build output: exit 0 | "Linter passed" |
| Bug fixed | Reproduce original symptom: fixed | "Code changed" |
| Agent completed | `git diff` shows changes | Agent says "success" |
| Requirements met | Line-by-line checklist | "Tests pass" |

## Red Flags — STOP

If you catch yourself thinking any of these, run the verification:

- "Should work now"
- "I'm confident"
- "Linter passed" (linter ≠ compiler)
- "Agent said success"
- "Just this once"

Run the command. Read the output. THEN claim the result.
