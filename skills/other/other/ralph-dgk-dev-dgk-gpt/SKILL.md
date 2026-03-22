---
name: ralph
description: Persistent completion mode. Use when the user explicitly says `/ralph` or clearly wants you to keep iterating until the task is actually finished, repeating implement-verify-fix loops instead of stopping at partial progress.
---

# Ralph

Use this as a persistence override, not a separate methodology.

## Default

- Treat the task as incomplete until the requested outcome is verified.
- Repeat the loop: inspect -> implement -> verify -> fix -> verify again.
- If a check fails, continue with the next fix instead of stopping at the first attempt.
- If one approach stalls, switch approaches and keep going.
- Keep intermediate updates short and progress-focused.

## Do Not Stop For

- "Probably fixed"
- "Good enough"
- Partial completion
- A failed first or second attempt
- Needing one more verification pass

## Stop Only When

- The requested outcome is verified.
- A real external blocker prevents further progress.
- The user explicitly stops or redirects the work.

## Avoid

- Do not ask whether to continue after each failure.
- Do not declare success without running the relevant checks.
- Do not fall back to planning mode unless execution is genuinely blocked.

## Finish

Return:
- what was completed
- what was verified
- what is still blocked, if anything
