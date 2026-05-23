---
name: resume-handoff
description: "Resume work from a handoff document. Use when user says 'resume handoff', 'continue from handoff', or references a handoff file."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Resume Handoff

You are an expert at seamlessly continuing work from a handoff document. You restore context quickly and continue implementation without losing momentum.

## When To Use

- User says "resume handoff" or "/resume_handoff"
- User says "continue from handoff" or just "continue"
- User references a handoff file with "@thoughts/shared/handoffs/..."
- User references a running state with "@thoughts/shared/runs/..."
- After a `/clear` or `/compact`
- Starting a new session to continue previous work

## Inputs

**Priority order** (check in this order):
1. **Running state file** - `thoughts/shared/runs/YYYY-MM-DD-{plan}.md` (mid-implementation)
2. **Handoff file** - `thoughts/shared/handoffs/YYYY-MM-DD-description.md` (full context)

## Resume Modes

### From Running State (Implementation in Progress)
When resuming from `thoughts/shared/runs/`:
- Minimal context restoration (just task groups + current position)
- Jump directly to next task group
- Continue implement-plan workflow

### From Handoff (Full Context)
When resuming from `thoughts/shared/handoffs/`:
- Full context restoration (decisions, discoveries, blockers)
- May need to re-read more files
- Standard resume workflow

## Outputs

- Restored context and understanding
- TODO.md updated with current priorities
- Immediate continuation of work
- Progress on next steps

## Workflow

### Phase 0: Check Beads State (Always First)

```bash
# Always sync beads first
bd sync

# Check for in-progress work
bd list --status in_progress --json

# Check for ready work
bd ready --json
```

**If beads has in-progress or ready tasks** → Resume from Beads (fast path)
**If beads is empty** → Resume from Handoff (full path)

### Resume from Beads (Fast Path)

When resuming with beads state:

```bash
bd sync
bd ready --json      # Shows next unblocked task
bd list --status in_progress --json  # Any in-progress?
```

```
1. Sync beads state
2. Check in-progress tasks (pick up where left off)
3. Check ready tasks (next unblocked work)
4. Announce: "Resuming: [task title]"
5. Continue with implement-plan workflow
```

**Output format**:
```markdown
## Resuming from Beads

### In Progress
- bd-a1b2: "Login endpoint" (started earlier)

### Ready Next
- bd-c3d4: "Logout endpoint"
- bd-e5f6: "Register endpoint"

### Blocked (waiting on above)
- bd-g7h8: "Integration tests" [blocked by: bd-c3d4]

Continuing with bd-a1b2...
```

---

### Resume from Handoff (Full Path)

### Phase 1: Context Restoration (First 30 Seconds)

```markdown
1. Read handoff document completely
2. Parse and understand:
   - What was done (completed items)
   - What was in progress (current state)
   - Key decisions made
   - Open blockers/questions
3. Read referenced artifacts:
   - Plan file (if referenced)
   - TODO.md
   - Active files mentioned
```

### Phase 1.5: Sync Beads State (If Using Beads)

If project has `.beads/` directory:

```bash
# Pull latest state (may have changed since handoff)
bd sync

# See what's ready to work on
bd ready --json

# Cross-reference with handoff's beads state
# Note any changes since handoff was created
```

### Phase 2: State Verification

```markdown
4. Verify current state matches handoff:
   - Check commits exist
   - Confirm files are in expected state
   - Note any drift since handoff
   - If using beads: check for task state changes

5. Check for user responses:
   - Were blockers resolved?
   - Any new instructions?
   - Decisions filled in?
```

### Phase 3: Resume Announcement

```markdown
6. Announce resumption:
   "Resuming [Task Name] from handoff dated [date]

   **Previous Progress:**
   - [x] Item 1
   - [x] Item 2

   **Continuing With:**
   - [ ] Next item (priority 1)

   **Open Questions:**
   - [Any pending questions]

   Proceeding with [first next step]..."
```

### Phase 4: Continue Implementation

```markdown
7. Start with first item in "Next Steps"
8. Follow implement-plan workflow:
   - Mark in_progress in TODO.md
   - Implement
   - Test
   - Commit
   - Mark complete
9. Continue through remaining steps
```

## Resume Checklist

Before continuing work, verify:

- [ ] Handoff document read completely
- [ ] Plan file reviewed (if referenced)
- [ ] TODO.md reflects current state
- [ ] Active files inspected
- [ ] No conflicting changes since handoff
- [ ] Blockers addressed or acknowledged
- [ ] User has provided any needed input
- [ ] Beads synced (if using beads: `bd sync`)
- [ ] Ready tasks reviewed (if using beads: `bd ready --json`)

## Handling Common Scenarios

### Scenario: Blockers Still Pending
```markdown
If handoff listed blockers that aren't resolved:
1. Highlight pending blockers
2. Ask user for resolution
3. Continue with non-blocked items if possible
4. Create new handoff if can't proceed
```

### Scenario: State Has Changed
```markdown
If repo state differs from handoff:
1. Note the differences
2. Determine if changes conflict or complement
3. Ask user for guidance if unclear
4. Update handoff understanding accordingly
```

### Scenario: Plan Was Updated
```markdown
If referenced plan has new changes:
1. Re-read the plan
2. Identify new steps or modified requirements
3. Update TODO.md to reflect changes
4. Proceed with updated understanding
```

### Scenario: Multiple Handoffs Exist
```markdown
If multiple handoff files:
1. List available handoffs with dates
2. Ask user which to resume
3. Or resume most recent by default
```

## Output Format

When resuming, always output:

```markdown
## Resuming: [Task Name]

**Handoff from**: YYYY-MM-DD
**Time since handoff**: [X hours/days]

### Progress Restored
| Status | Item |
|--------|------|
| Done | Item 1 |
| Done | Item 2 |
| **Resuming** | Item 3 |
| Pending | Item 4 |

### Context Restored
- [Key decision 1]
- [Key decision 2]

### Blockers Status
- [Blocker 1]: [Resolved/Still pending]

### Immediate Next Action
[What you're about to do]

---
Proceeding...
```

## Finding Handoff Files

If user doesn't specify a handoff:

```bash
# List recent handoffs
ls -la thoughts/shared/handoffs/

# Show most recent
ls -t thoughts/shared/handoffs/ | head -1

# Search by keyword
grep -l "keyword" thoughts/shared/handoffs/*.md
```

## Integration with Thinking Modes

When resuming complex work:
- **Simple continuation**: Regular mode
- **After long break**: Think Hard about context
- **Complex architecture**: Ultrathink before continuing
- **Multiple blockers**: Super Think to prioritize

## Best Practices

- **Read completely first**: Don't skim the handoff
- **Verify before acting**: Confirm state matches expectations
- **Announce clearly**: Let user know what's being resumed
- **Update handoff**: If continuing for long, create new handoff
- **Commit frequently**: Don't lose progress again

## Keywords

resume handoff, continue handoff, pick up where left off, restore context, continue work, after clear, resume session, continue from
