---
name: ralph-specum-switch
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-switch`, or explicitly asks Ralph Specum in Codex to switch the active spec.
metadata:
  surface: helper
  action: switch
---

# Ralph Specum Switch

Use this to switch the active spec.

## Contract

- Read `.claude/ralph-specum.local.md` when present
- Parse `specs_dirs` from frontmatter to discover all spec roots
- Treat the first `specs_dirs` entry as the default root
- Default specs root is `./specs`
- `.current-spec` lives in the default specs root
- Do not guess on ambiguous names

## Action

1. Resolve the requested target by full path or exact name.
2. If no target was provided, list available specs grouped by root.
3. If the name is ambiguous across roots, stop and require a full path.
4. Update `.current-spec`:
   - bare name for the default root
   - full path for non-default roots
5. Read the target spec state and summarize phase, progress, approval state, and present files.
