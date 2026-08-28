---
name: phx-freeze
description: Apply an advisory edit scope in this session. Use for read-only or directory-scoped
  work; no enforcement hook is installed.
---
# Freeze — advisory edit scope

Apply a current-session instruction that limits which files this agent may edit.
This generated runtime does not install an enforcement hook, so the scope is
advisory rather than a technical lock. Never claim that edits are blocked by the
runtime.

## Usage

```text
/phx-freeze
/phx-freeze lib/app_web priv/repo
/phx-freeze status
/phx-freeze off
```

Treat the text after the skill invocation as follows:

| Invocation | Current-session behavior |
|---|---|
| No arguments | Do not edit files; investigation and reporting remain read-only. |
| Path prefixes | Edit only files under the listed project-relative prefixes. |
| `status` | Report the advisory scope currently established in this conversation. |
| `off` | Clear the advisory scope for subsequent work. |

Do not create `.claude/.freeze`. That sentinel belongs to the canonical Claude
Code plugin and could affect a later Claude Code session even though this runtime
cannot enforce or clear it reliably.

## Iron Laws

1. **Never describe this scope as enforced** — it is a binding instruction for
   the current agent, not a runtime or security boundary.
2. **Never create or modify `.claude/.freeze` in a generated runtime** — no
   matching enforcement component is installed here.
3. **Honor the active scope until the user clears it or the focused task ends** —
   ask before editing outside listed prefixes.
4. **Keep paths project-relative** — `lib/foo` includes that directory and its
   descendants, not a sibling such as `lib/foobar`.
