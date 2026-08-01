---
name: ca-doctor
description: Verify the active host install, package, command ownership, enforcement, and harmless live-fire probe. Read-only.
argument-hint: (none)
---

# $ca-doctor — install health

Silent dormancy is the worst failure shape this plugin has: the gates look installed but never fire.
This command proves the active host is healthy and reports every non-OK finding with an exact
remediation.

## Flow

1. Resolve the plugin root from this loaded skill path, then run its `hooks/doctor.py` with Python 3
   and present the report verbatim. Do not try an empty plugin-root environment variable first.
2. In an arbiter-enabled repo, attempt `git add --all --dry-run` via the shell tool. `[H-03]` means
   hooks are firing; execution means **CRITICAL: gates dormant**.

## Remediation ladder

1. Restart Codex so hooks register at session start.
2. Remove and re-add `ca-codex@codearbiter`, then approve the changed hook set in `/hooks`.
3. If dormancy was intended, `$ca-init` opts the repository in.

## When NOT to use

- Scaffold state only → `$ca-init --check`.
- Project progress, not install health → `$ca-status`.

## Hard gate

Read-only. MUST NOT create markers, stage files, grant trust, weaken a block, or retry the live-fire
probe with different spelling. MUST surface a failed probe as CRITICAL, never as a footnote.
