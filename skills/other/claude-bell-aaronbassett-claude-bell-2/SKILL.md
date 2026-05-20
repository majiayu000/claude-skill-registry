---
name: claude-bell
description: Use when you need to alert the user outside the terminal, get confirmation before proceeding, or collect text input. Triggers include task completion, errors requiring attention, destructive operations needing approval, or questions requiring user decision.
---

# Claude Bell

Send macOS notifications to communicate with users outside the terminal.

## When to Use

**Use for:**
- Task completion (build done, tests passed, deploy finished)
- Errors requiring attention
- Confirmation before destructive operations
- Collecting text input (release notes, commit messages)
- Status updates during long operations

**Don't use for:**
- Routine progress updates (use terminal)
- Information user is actively watching
- Rapid-fire notifications (spam)

## Quick Reference

| Pattern | Command |
|---------|---------|
| Alert | `cb -t "Done" -m "Build complete"` |
| Alert with sound | `cb -t "Done" -m "Build complete" --sound Glass` |
| Yes/No | `cb -t "Deploy?" -a "Yes,No" --default "No"` |
| Multiple choice | `cb -t "Action" -a "A,B,C,Cancel" --default "Cancel"` |
| Text input | `cb -t "Notes" -r "Enter notes..." --timeout 5m` |
| Template | `cb --template build-done --var 'project:myapp'` |

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Proceed with returned value |
| 1 | Timeout | Use `--default` value |
| 2 | Dismissed | Use `--default` value |
| 3 | User error | Check arguments |
| 4 | System error | Check permissions (`cb doctor`) |
| 5 | App error | Report bug |

## Critical Rules

1. **Always provide `--default`** for interactive notifications
2. **Always check exit code** - don't assume success
3. **Use `--timeout`** for non-critical prompts
4. **Don't spam** - one notification per logical event

## References

- `references/cli.md` - Full CLI documentation
- `references/examples.md` - Workflow patterns
- `references/setup.md` - Installation & setup (read only when user requests setup)
- `references/troubleshooting.md` - Diagnosing issues
