---
name: retro-create
description: Post-invocation retrospective. Tracks skill issues and applies fixes automatically.
---

## Purpose

After any skill completes, review the session for issues and improve the skill to prevent recurrence.

## Trigger

Run automatically after every skill invocation completes (success or failure).

## What to look for

1. **Failed commands** — commands that errored and required retrying or workarounds
2. **User corrections** — the user stepped in to redirect, correct, or override
3. **Wrong assumptions** — the skill assumed something that was not true (versions, paths, flags)
4. **Missing steps** — manual steps the user had to perform that the skill should have handled
5. **Outdated instructions** — references to APIs, flags, or behaviors that have changed

## Protocol

For each issue found:

1. **Log** — append an entry to `<skill-dir>/retro.md` (create the file if it does not exist)
2. **Root-cause** — identify which file (SKILL.md, reference, template) contains the gap
3. **Fix immediately** — edit the skill file directly to prevent recurrence. This is the default action.
4. **Log only if unsafe** — record the issue with `status: open` only when the fix would change skill behavior in ways that cannot be verified in the current session. Require a `resolution-hint` on every open entry.

After logging any `status: open` entry, append:
> **Open issues remain.** Run /retro-resolve to process them.

## retro.md entry format

```
## YYYY-MM-DD — <brief title>

- **type**: failed-command | user-correction | wrong-assumption | missing-step | outdated-instruction
- **skill**: <skill-name>
- **context**: <what happened>
- **root-cause**: <why it happened>
- **fix**: <what was changed> | `status: open` if not yet fixed
- **resolution-hint**: <what the fix should look like> (required for open entries)
- **files-changed**: <list of files edited, or "none">
```

## Constraints

- Do not modify skill behavior or semantics — only fix gaps, errors, and omissions
- Keep entries concise (3-5 lines per field max)
- Do not duplicate fixes already present in skill files
- If a fix would change skill behavior significantly, log as `status: open` and note the concern
- Prefer fixing over logging. If you can describe the fix in `resolution-hint`, you can probably just apply it.
- Never log as `status: open` simply because the session is long or context is low.
