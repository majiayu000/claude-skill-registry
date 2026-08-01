---
name: session-documentation
description: '> Purpose: Enforce comprehensive documentation as part of work completion'
---

# Session Documentation Skill

> **Purpose:** Enforce comprehensive documentation as part of work completion
> **Created:** 2025-12-25
> **Trigger:** Feature completion, bug fixes, significant changes, session end, handoff requests

---

## Why This Skill Exists

Documentation debt compounds session over session. Without proactive documentation:
- Future sessions rebuild context from scratch (~50K tokens)
- Handoff errors occur (e.g., Block 10 constraints implemented but not registered)
- Users must prompt 3x for comprehensive docs

This skill ensures documentation is part of "done" - not an afterthought.

---

## When This Skill Activates

Activate automatically when:

1. **Feature implementation completed** - Any new capability added
2. **Bug fix committed** - Any issue resolved
3. **Significant code change** - More than trivial edits
4. **Session ending** - User says "done", "finished", "ending session"
5. **Handoff requested** - User asks for summary/handoff/status
6. **PR ready** - Before creating pull request

---

## Required Documentation Outputs

### Minimum Required (ALL must be present)

```markdown
## What Was Done
- [ ] Bullet list of completed tasks
- [ ] Files created/modified (with line ranges)
- [ ] Tests added/modified

## Why It Was Done
- [ ] Context/motivation
- [ ] Problem being solved
- [ ] Related issue/task reference

## How to Verify
- [ ] Commands to run
- [ ] Expected output
- [ ] Success criteria

## What Remains
- [ ] Incomplete tasks
- [ ] Known limitations
- [ ] Follow-up work needed
```

### Recommended (Include when applicable)

```markdown
## Decisions Made
- [ ] Design choices and rationale
- [ ] Alternatives considered and rejected
- [ ] Trade-offs accepted

## Gotchas and Warnings
- [ ] Common pitfalls
- [ ] Non-obvious behavior
- [ ] Dependencies or prerequisites

## Related Updates
- [ ] Documentation files updated
- [ ] CHANGELOG entry added
- [ ] README updated (if applicable)
```

### For Session Handoffs (REQUIRED at session end)

```markdown
## Session Summary

### Current State
- System status (working/broken/partial)
- Database state
- Container status

### Completed This Session
- Task 1 - commit hash
- Task 2 - commit hash

### Blocked Items
- Item 1 - reason
- Item 2 - reason

### Next Steps (Prioritized)
1. Highest priority
2. Second priority
3. Third priority

### Verification Commands
```bash
# Command to verify current state
```

### Key Files
| File | Purpose |
|------|---------|
| path/to/file | Description |
```

---

## Documentation Quality Checklist

Before marking documentation "complete," verify:

### Structure
- [ ] Clear headings and sections
- [ ] Bullet points for scanability
- [ ] Code blocks for commands/examples
- [ ] Tables for structured data

### Content
- [ ] Specific, not vague ("added X to Y" not "made changes")
- [ ] Actionable next steps
- [ ] Verifiable claims (commands to prove it works)
- [ ] No orphan references (linked docs exist)

### Completeness
- [ ] Someone unfamiliar could understand and continue
- [ ] No assumed knowledge not documented
- [ ] Edge cases and exceptions noted
- [ ] Future sessions won't ask "what did we do?"

---

## Output Locations

Documentation should be created in appropriate locations:

| Type | Location | Example |
|------|----------|---------|
| Session handoff | `docs/development/SESSION_HANDOFF_YYYYMMDD.md` | Ending a session |
| Feature docs | `docs/architecture/` or `docs/guides/` | New capability |
| Bug fix notes | Commit message + CHANGELOG | Issue resolution |
| Technical details | `docs/development/` | Implementation specifics |
| Postmortem | `docs/development/POSTMORTEM_*.md` | Session analysis |

---

## Anti-Patterns to Avoid

### Don't: Minimal Response
```
"Fixed the bug in scheduler.py"
```

### Do: Comprehensive Response
```markdown
## Bug Fix: Scheduler Timezone Mismatch

### What Was Done
- Fixed UTC/local timezone conversion in `scheduler.py:145-160`
- Added explicit timezone handling in `_calculate_hours()`
- Added test case for HST timezone edge case

### Files Modified
- `backend/app/scheduling/scheduler.py` (lines 145-160)
- `backend/tests/test_scheduler.py` (added test_hst_conversion)

### How to Verify
```bash
pytest backend/tests/test_scheduler.py::test_hst_conversion -v
```

### Root Cause
Scheduler assumed UTC but database stored local time (HST).
```

---

## Integration with Other Skills

This skill complements:

| Skill | Relationship |
|-------|--------------|
| `constraint-preflight` | Both verify "done" criteria |
| `code-review` | Documentation is part of review |
| `pr-reviewer` | PR descriptions require docs |
| `changelog-generator` | Feeds into release notes |

---

## Verification Script

Run this to check documentation exists:

```bash
# Check for recent session docs
find docs/development -name "SESSION_*.md" -mtime -1 | head -5

# Check for handoff docs
find docs/development -name "*HANDOFF*.md" -mtime -1 | head -5

# Check CHANGELOG updated
git log --oneline -5 | grep -i "changelog\|docs"
```

---

## Example: Full Session Documentation

```markdown
# Session Handoff: 2025-12-25

## Session Summary

### Current State
- Backend: Running (Docker)
- Frontend: Running (npm dev)
- Database: 87 assignments in Block 10

### Completed This Session
- [x] Fixed constraint registration gap (commit abc1234)
- [x] Added schema versioning feature (commit def5678)
- [x] Created Docker workaround docs (commit ghi9012)

### Blocked Items
- MCP tool `get_static_fallbacks` - needs backend endpoint
- Heatmap API mismatch - requires backend changes

### Next Steps (Prioritized)
1. Address heatmap API bug (frontend shows unsupported options)
2. Fix swap marketplace permissions for admin role
3. Create person profile for admin user

### Verification Commands
```bash
# Check constraints
docker exec backend python -c "from app.scheduling.constraints.manager import ConstraintManager; print(len(ConstraintManager.create_default().constraints))"

# Check schedule
curl -s http://localhost:8000/api/v1/schedule/block/10 | jq '.assignments | length'
```

### Key Files
| File | Purpose |
|------|---------|
| `backend/app/scheduling/constraints/manager.py` | Constraint registration |
| `docs/development/SESSION_HANDOFF_20251225.md` | This handoff |
| `scripts/verify_constraints.py` | Pre-flight verification |
```

---

## Enforcement

This skill should be enforced through:

1. **Habit** - Check documentation checklist before saying "done"
2. **Prompts** - If minimal docs given, prompt for expansion
3. **PR Review** - Documentation required for PR approval
4. **CI Check** - Verify handoff doc exists for session branches

---

## Related Documentation

- [CLAUDE_HANDOFF_CHECKLIST.md](../../../docs/development/CLAUDE_HANDOFF_CHECKLIST.md) - Handoff protocol
- [AI_RULES_OF_ENGAGEMENT.md](../../../docs/development/AI_RULES_OF_ENGAGEMENT.md) - Work rules
- [POSTMORTEM_BLOCK10_SESSION.md](../../../docs/development/POSTMORTEM_BLOCK10_SESSION.md) - Why this skill exists

---

*Remember: Documentation is not optional polish - it's how future sessions avoid starting from zero.*
