---
name: phase3-ticket-investigation
description: Investigate Phase 3 tickets to clarify scope and determine implementation vs. defer vs. close
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-31T04:35:41.544Z"
  updated_at: "2026-01-31T04:35:41.544Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Investigate Phase 3 tickets (Orchestration, CLI, Scheduling, Monitoring, Testing) to clarify scope and provide implementation recommendation.

# When To Use
- Manager assigns Phase 3 ticket investigation
- Ticket has empty/unclear body but tags indicate a Phase 3 component
- Need to decide if ticket should be scoped, deferred, or closed

# Procedure

## 1. Gather Context
- List all Phase 3 tickets: `loom ticket list --tag phase3`
- Read ROADMAP.md to understand Phase 3 goals and components
- Check each Phase 3 ticket status and body content

## 2. Check Component Status

### For Orchestration (vp-cf95)
- Check if ExecutionEngine exists in `src/vibe_piper/orchestration/`
- Verify orchestration tests in `tests/test_orchestration.py`
- Look for implementation commits in git log

### For CLI (vp-6cf1)
- Check CLI commands in `src/vibe_piper/cli/`
- Verify CLI tests in `tests/cli/`
- Check if commands are registered and working

### For Scheduling (vp-7d49)
- Check scheduling module in `src/vibe_piper/scheduling/`
- Verify scheduling tests in `tests/scheduling/`
- Check test pass rate

### For Monitoring (vp-f17e)
- Check monitoring module in `src/vibe_piper/monitoring/`
- Verify monitoring tests in `tests/monitoring/`
- Check implementation status (metrics, logging, health, etc.)

### For Testing (vp-0429)
- List existing testing infrastructure:
  - Unit tests: `ls tests/*.py`
  - Integration tests: `ls tests/integration/*.py`
  - Fixtures: check `tests/conftest.py`
  - Assertion helpers: check `tests/helpers/assertions.py`
  - Factory functions: check `tests/helpers/factories.py`
  - Fake data generators: check `tests/fixtures/fake_data.py`
- Check for snapshot testing:
  - `tests/helpers/snapshots.py` exists?
  - `tests/helpers/test_snapshots.py` exists?
  - `tests/snapshots/` directory exists?
- Check if snapshot-testing skill exists: `.opencode/skills/snapshot-testing/SKILL.md`

## 3. Analyze Roadmap Context
- Check ROADMAP.md Testing Layer section (around line 167-174)
- Note which components are marked ✅ vs ⏳ vs ⏸️
- Identify any components marked "in progress" or "missing"

## 4. Determine Recommendation

### Implement If:
- Component is called out as missing in ROADMAP
- Skill definition exists but implementation is missing
- Low effort (2-3 hours estimate)
- Independent of current sprint work
- High value (catches regressions, completes phase)

### Defer If:
- Current sprint has higher priority work
- Component can wait until after current sprint
- Priority is P2/P3

### Close If:
- Component already implemented elsewhere
- Component superseded by new approach
- No clear value add

## 5. Document Findings
- Create INVESTIGATION_NOTES.md with:
  - All Phase 3 ticket statuses
  - Existing infrastructure checklists
  - Roadmap context
  - Decision rationale
  - Recommended scope (if implementing)
- Commit investigation notes with clear message
- Update ticket body with:
  - Context (what was missing/incomplete)
  - Objective (what to implement)
  - Clear scope with tasks
  - Acceptance criteria checklist
  - Dependencies
  - Related tickets

## 6. Communicate to Manager
- Use `loom team send MiyagiDo manager` to summarize:
  - Investigation findings
  - Recommendation (implement/defer/close)
  - Scope (if implementing)
  - Estimated effort
  - Suggested timing (now vs. after sprint)
- Add note to ticket with progress update

# Outputs
- INVESTIGATION_NOTES.md with detailed findings
- Updated ticket body with clear scope
- Manager notification with summary
- Git commit with investigation documentation

# Example Investigation
```markdown
## Phase 3 Status
| Ticket | Component | Status | Notes |
|--------|-----------|--------|-------|
| vp-cf95 | Orchestration | CLOSED | Body empty |
| vp-6cf1 | CLI | CLOSED ✓ | 7 commands implemented |
| vp-7d49 | Scheduling | CLOSED ✓ | 19/25 tests passing |
| vp-f17e | Monitoring | CLOSED ✓ | 76 tests created |
| vp-0429 | Testing | OPEN | Snapshot testing missing |

## Testing Infrastructure
✅ Present: Unit tests, Integration tests, Fixtures, Helpers, Factories, Fake data
❌ Missing: Snapshot testing framework

## Decision
IMPLEMENT - snapshot testing is only missing Phase 3 Testing Layer component
```
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
