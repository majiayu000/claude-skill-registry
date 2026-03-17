---
name: handoff
description: Writes comprehensive handoff note at session end. Captures work done, files changed, remaining tasks, and next steps. Use before ending any work session or switching contexts.
allowed-tools: Read, Write, Glob
---

# Handoff

Make work portable across sessions. Write to `.context/handoff.md`.

## When to Use

- End of every work session
- Before switching tasks or contexts
- Before user leaves
- When compacting context

## Process

1. **Gather**: What was requested? What did we do? What changed?
2. **Document**: Files, agents, decisions, docs updated
3. **Verify**: How to confirm the work is correct
4. **Remaining**: What's incomplete, issues, blockers
5. **Prepare**: What does next session need?

## Output Location

Write to: `.context/handoff.md`

## Essential Sections

```markdown
# Session Handoff — [Date]

## Summary
[2-3 sentences: what was accomplished]

## Work Completed
- [Feature/fix]: [description]

## Files Changed
| File | Change | Description |
|------|--------|-------------|
| path | modified | what changed |

## Verification
[Commands to run, UI to check, tests to execute]

## Remaining
- [ ] [Incomplete task]
- **Issue**: [description + workaround]

## Next Session
1. Run `/session-start`
2. Load [specific docs]
3. Start with [first action]
```

## Quick Handoff (Short Sessions)

```markdown
# Quick Handoff — [Date]
**Did**: [one sentence]
**Changed**: [file list]
**Verify**: [one command/action]
**Next**: [what to do]
```

## Quality Check

- [ ] Summary is specific, not vague
- [ ] All changed files listed
- [ ] Verification steps are actionable
- [ ] Remaining work is explicit
- [ ] Next session can start immediately

## Related

- Full template: See [reference/full-template.md](reference/full-template.md)
- Compaction handoff: See [reference/compact-handoff.md](reference/compact-handoff.md)
- Consumed by: `/session-start`
