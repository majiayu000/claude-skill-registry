---
name: create-handoff
description: "Create a handoff document to preserve context before clearing. Use when user says 'create handoff', context is low, or before '/clear'."
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Create Handoff

You are an expert at capturing context for seamless session continuation. Handoffs are structured documents that allow a fresh session to resume work without losing progress.

## When To Use

- User says "create handoff" or "/create_handoff"
- Context/remaining tokens below 10%
- Before using `/clear`
- At natural breakpoints in long implementations
- When switching tasks temporarily
- End of work session
- **Pre-implementation**: Before starting implement-plan (if context > 30%)

## Modes

### Standard Mode (Default)
Full handoff with all context preserved. Use at end of session or before `/clear`.

### Pre-Implementation Mode
Lightweight handoff before starting a plan. Triggered when:
- User is about to run implement-plan
- Context is already > 30%

**Pre-implementation handoff captures**:
- Current conversation summary (2-3 sentences)
- Any decisions already made
- Reference to the plan file

**Then suggests**: "Run `/compact` then `implement plan @plan-file`"

## Why Handoffs > Auto-Compact

- **Explicit control**: You decide what's preserved
- **Structured format**: Easy to parse and resume
- **Versioned**: Handoffs are committed to repo
- **Shareable**: Another agent or human can continue
- **No context loss**: Everything important is captured

## Inputs

- Current session context
- Active plan file (if any)
- Current state of implementation
- Any blockers or open questions

## Outputs

- Handoff file at: `thoughts/shared/handoffs/YYYY-MM-DD-[ticket_id]-description.md`
- Updated TODO.md with current state
- Clear next steps documented

## Handoff Document Structure

```markdown
# Handoff: [Task/Feature Name]

**Created**: YYYY-MM-DD HH:MM
**Session**: [Session ID if available]
**Ticket**: [ID if applicable]

## Quick Summary
[2-3 sentences on what was being done]

## Current State

### What's Done
- [x] Completed item 1 (commit: abc123)
- [x] Completed item 2 (commit: def456)

### In Progress
- [ ] Current task being worked on
  - What's done: [specifics]
  - What remains: [specifics]

### Not Started
- [ ] Remaining task 1
- [ ] Remaining task 2

## Active Files

Files currently being worked on:
- `src/auth/login.ts` - Implementing login logic, line 45-80 needs completion
- `tests/auth.test.ts` - 3 tests passing, 2 pending

## Context to Preserve

### Key Decisions Made
1. Decision: [what] | Rationale: [why]
2. Decision: [what] | Rationale: [why]

### Important Discoveries
- [Thing learned during implementation]
- [Gotcha or edge case found]

### Technical Notes
- [Architecture note]
- [Performance consideration]
- [Security note]

## Blockers / Open Questions

| # | Question/Blocker | Status | Notes |
|---|-----------------|--------|-------|
| 1 | [Question] | Waiting on user | Asked at HH:MM |
| 2 | [Blocker] | Investigating | Possible solutions: A, B |

## Beads State (Persistent Tasks)

If project uses beads (.beads/ exists):

### In Progress
[Output of `bd list --status in_progress --json`]

### Ready Next
[Output of `bd ready --json`]

### Blocked
[Tasks with open dependencies]

### Beads Resume Commands
```bash
bd sync  # Pull latest from remote
bd ready --json  # See unblocked tasks
```

## Related Artifacts

- **Plan**: `thoughts/shared/plans/YYYY-MM-DD-description.md`
- **TODO.md**: Updated with current state
- **PRD**: `PRD.md` (if exists)
- **Beads**: `.beads/issues.jsonl` (if using beads)

## Next Steps (Prioritized)

1. **Immediate**: [What to do first when resuming]
2. **Then**: [Second priority]
3. **After that**: [Third priority]

## Resume Instructions

To continue this work:
```bash
# In Claude Code
/resume_handoff @thoughts/shared/handoffs/YYYY-MM-DD-description.md
```

Or manually:
1. Read this handoff document
2. Check TODO.md for current state
3. Review plan file if referenced
4. Continue from "Next Steps"

---

## Session Statistics
- Started: [timestamp if known]
- Duration: [if known]
- Commits made: [count]
- Context used: ~[%] when handoff created
```

## Workflow

### Phase 1: Capture Current State

1. **Identify what's done**: List completed tasks with commits
2. **Capture in-progress work**: Where exactly did you stop?
3. **Note remaining work**: What's left on the plan?

### Phase 2: Document Context

4. **Key decisions**: What choices were made and why?
5. **Discoveries**: What was learned during implementation?
6. **Blockers**: Any unresolved issues?

### Phase 3: Prepare for Resume

7. **Prioritize next steps**: What should happen first?
8. **Reference artifacts**: Link to plan, TODO.md, etc.
9. **Write resume instructions**: Make it easy to continue

### Phase 3.5: Capture Beads State (If Using Beads)

If project has `.beads/` directory:

10. **Sync beads**: Run `bd sync` to push all changes
11. **Capture task states**: Document in-progress, ready, and blocked tasks
12. **Include resume commands**: `bd sync && bd ready --json`

### Phase 4: Finalize

10. **Write handoff file**
11. **Update TODO.md** to reflect current state
12. **Commit handoff**: "docs: create handoff for [feature]"

## Handoff Naming Convention

```
YYYY-MM-DD-[TICKET_ID]-description-handoff.md

Examples:
- 2025-01-15-AUTH-001-user-auth-handoff.md
- 2025-01-15-no-ticket-dark-mode-handoff.md
- 2025-01-15-session-2-handoff.md
```

## Best Practices

- **Create early**: Don't wait until context is exhausted
- **Be specific**: "line 45 of login.ts" not "somewhere in login"
- **Include reasoning**: Future you needs the "why"
- **Test resume**: Verify handoff has enough info to continue
- **Commit immediately**: Don't lose the handoff to a crash

## Integration with Plan Workflow

```
/create_plan idea
  -> answer questions
  -> plan created: thoughts/shared/plans/...

/clear

/implement_plan @thoughts/shared/plans/...
  -> implement steps
  -> context getting low (5-10%)

/create_handoff
  -> handoff created: thoughts/shared/handoffs/...

/clear

/resume_handoff @thoughts/shared/handoffs/...
  -> continue implementation
  -> repeat until done
```

## Keywords

create handoff, handoff, save context, preserve context, before clear, session end, context low, take a break, pause work
