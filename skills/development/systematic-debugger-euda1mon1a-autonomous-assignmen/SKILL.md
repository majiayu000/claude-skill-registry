---
name: systematic-debugger
description: Systematic debugging skill for complex issues. Use when encountering bugs, test failures, or unexpected behavior. Enforces explore-plan-debug-fix workflow to prevent premature fixes.
model_tier: opus
parallel_hints:
  can_parallel_with: [search-party, code-review]
  must_serialize_with: [automated-code-fixer]
  preferred_batch_size: 1
context_hints:
  max_file_context: 100
  compression_level: 0
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "security.*vulnerability"
    reason: "Security issues require security-audit skill involvement"
  - pattern: "database.*corruption"
    reason: "Data corruption requires human intervention"
  - keyword: ["ACGME", "compliance", "violation"]
    reason: "Compliance issues require domain expert review"
---

# Systematic Debugger

A methodical debugging skill that prevents jumping to fixes and ensures thorough root cause analysis.

## When This Skill Activates

- Bug reports or issue investigations
- Test failures requiring debugging
- Unexpected behavior in scheduling logic
- ACGME compliance violations
- Data inconsistencies
- Performance issues requiring investigation

## Core Philosophy: NEVER Fix First

**CRITICAL: The most common debugging mistake is implementing a fix before understanding the problem.**

This skill enforces a strict four-phase workflow:

```
EXPLORE → PLAN → DEBUG → FIX
   ↓         ↓        ↓       ↓
 Read    Think    Test    Implement
 Observe  Hard   Reproduce  Minimal
 DON'T   Analyze  Validate  Verify
 CHANGE  Hypothesize        Commit
```

## Phase 1: Exploration (NO CHANGES)

**Goal:** Understand the problem without making any modifications.

### Prompt Template
```
Read the [component] logic and examine the error context.
Don't fix anything yet, just understand the system.
```

### What to Examine
1. **Error logs and stack traces**
   ```bash
   # Check recent logs
   grep -i "error\|exception" backend/logs/*.log | tail -50
   docker-compose logs backend --tail=100
   ```

2. **Relevant source code**
   - Read the actual implementation
   - Trace data flow through the system
   - Note boundary conditions

3. **Related tests**
   ```bash
   # Tests document expected behavior
   pytest tests/[relevant]/ --collect-only
   cat tests/[relevant]/test_*.py
   ```

4. **Recent changes**
   ```bash
   git log --oneline -20 -- [relevant_path]/
   git diff HEAD~5 -- [relevant_path]/
   ```

### Exploration Questions
- What is the expected behavior?
- What is the actual behavior?
- What data/conditions trigger the issue?
- What constraints should apply?

## Phase 2: Planning with Extended Thinking

**Goal:** Form hypotheses and design a debugging approach.

### Trigger Deeper Reasoning
Use these phrases (in order of computational budget):
- `"think"` - Light analysis
- `"think hard"` - Moderate analysis
- `"think harder"` - Deep analysis
- `"ultrathink"` - Maximum reasoning

### Prompt Template
```
Think hard about what could cause [symptom].
Create a hypothesis list with root cause analysis.
Propose diagnostics for each. Don't write code yet.
```

### Hypothesis Template

| # | Hypothesis | Evidence For | Evidence Against | Test Method |
|---|------------|--------------|------------------|-------------|
| 1 | [theory] | [supporting] | [contradicting] | [validation] |
| 2 | [theory] | [supporting] | [contradicting] | [validation] |

### Ranking Criteria
- **Likelihood** - Based on evidence
- **Impact** - Severity if true
- **Testability** - Ease of validation

## Phase 3: Debugging

**Goal:** Validate hypotheses and isolate root cause.

### TDD Approach
```bash
# Write failing test first
cd backend

# Create test that reproduces the bug
cat > tests/regression/test_bug_investigation.py << 'EOF'
"""Regression test for current investigation."""
import pytest

class TestCurrentBug:
    async def test_reproduces_issue(self, db):
        """This should FAIL before fix is applied."""
        # Setup conditions
        # Execute operation
        # Assert expected (correct) behavior
        pass
EOF

# Run and confirm failure
pytest tests/regression/test_bug_investigation.py -v
```

### Strategic Logging
```python
# Add temporarily to observe runtime
import logging
logger = logging.getLogger(__name__)

logger.info(f"DEBUG INPUT: {locals()}")
logger.info(f"DEBUG RESULT: {result}")
```

### Binary Search Isolation
```
1. Comment out half the logic
2. Run test
3. Based on pass/fail, narrow down
4. Repeat until isolated
```

## Phase 4: Fix and Verify

**Goal:** Implement minimal fix with comprehensive verification.

### Fix Guidelines
- Minimal changes only
- Don't refactor unrelated code
- Don't add "improvements"
- Preserve existing behavior

### Verification Checklist
```bash
cd backend

# 1. Failing test now passes
pytest tests/regression/test_bug_investigation.py -v

# 2. Related tests pass
pytest tests/[relevant]/ -v

# 3. ACGME compliance maintained
pytest -m acgme -v

# 4. Full suite passes
pytest --cov=app -v

# 5. No linting errors
ruff check app/ tests/
```

### Commit with Context
```bash
git commit -m "$(cat <<'EOF'
fix: [issue description]

Root cause: [what caused the bug]
Fix: [what the fix does]

Adds regression test to prevent recurrence.
EOF
)"
```

## Domain-Specific Debugging

### Scheduling Issues
| Issue | Check First |
|-------|-------------|
| Double-booking | `scheduling/conflicts/` |
| ACGME violation | `services/constraints/acgme.py` |
| Rotation overlap | `scheduling/engine.py` |
| Supervision gaps | `scheduling/constraints/faculty.py` |

### Known Gotchas
| Trap | Reality |
|------|---------|
| Timezone | Scheduler runs UTC, displays HST |
| Work hours | Reset at midnight LOCAL, not UTC |
| Race conditions | Need `with_for_update()` |
| Test isolation | Check conftest fixtures |
| activity_type mismatch | `"clinic"` ≠ `"outpatient"` - check seed data for canonical values |
| Doc/code mismatch | Comments may say "outpatient" while code uses "clinic" - verify both |

### Lesson Learned: PR #442 (2025-12-26)

**Issue:** Code comment said "OUTPATIENT HALF-DAY OPTIMIZATION" but filter used `"clinic"`.

**Root cause:** The activity_type values in seed data distinguish:
- `"outpatient"` = elective/selective rotations (Neurology, ID, etc.)
- `"clinic"` = FM Clinic only (has separate capacity constraints)

**Prevention:** When fixing filters, always verify against:
1. Seed data (`scripts/seed_templates.py`)
2. Database model comments
3. BLOCK_10_ROADMAP canonical activity_type list

**Lesson:** Evaluate PRs fully before merging. This PR was caught during evaluation
and prevented a production bug where the solver would find zero templates.

## Context Management

When debugging spans multiple sessions:

### Document & Clear
```bash
# 1. Save state
cat > debug-session-notes.md << 'EOF'
# Debug Session: [Issue]
## Symptom: [what's happening]
## Hypotheses: [ranked list]
## Tried: [what we did]
## Findings: [what we learned]
## Next: [what to do]
EOF

# 2. /clear to reset context

# 3. Resume with:
# "Read debug-session-notes.md and continue debugging"
```

## Escalation Triggers

**STOP and escalate when:**
1. Root cause unclear after 3 iterations
2. Fix requires model/migration changes
3. ACGME compliance logic affected
4. Security-sensitive code involved
5. Multiple interconnected failures

## Integration with Commands

- `/project:debug-scheduling [issue]` - Scheduling-specific workflow
- `/project:debug-tdd [bug]` - Test-driven debugging
- `/project:debug-explore [symptom]` - Pure exploration mode

## Course Correction

| Action | How |
|--------|-----|
| Interrupt | **Escape** |
| Go back | **Double-tap Escape** |
| Revert | Say: `"Undo changes"` |
| Plan first | Say: `"Make a plan first"` |

## Example Session

```
User: "Residents are getting double-booked"

[Phase 1: Explore]
Claude: Let me examine the overlap detection logic without making changes...
        - Reading scheduling/conflicts/analyzer.py
        - Checking recent test failures
        - Examining error logs

[Phase 2: Plan]
Claude: Think hard about possible causes:
        1. Date boundary issue (70% likely) - Test with overnight rotation
        2. Missing overlap check (20% likely) - Review validator
        3. Race condition (10% likely) - Check locking

[Phase 3: Debug]
Claude: Writing failing test to reproduce...
        - Test created, confirmed failure
        - Adding logging to observe date handling
        - Root cause: exclusive vs inclusive end date comparison

[Phase 4: Fix]
Claude: Implementing fix for date comparison...
        - Changed `<` to `<=` for end date
        - All tests pass including regression test
        - ACGME tests pass
        - Committing with explanation
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  SYSTEMATIC DEBUGGING WORKFLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: EXPLORATION (NO CHANGES!)                             │
│  ┌────────────────────────────────────────────────────┐         │
│  │ Read code → Check logs → Review tests              │         │
│  │ Examine recent changes → Map data flow             │         │
│  │ ⚠️ DO NOT FIX ANYTHING YET                         │         │
│  └────────────────────────────────────────────────────┘         │
│                         ↓                                       │
│  PHASE 2: PLANNING (THINK HARD)                                 │
│  ┌────────────────────────────────────────────────────┐         │
│  │ List hypotheses → Rank by likelihood               │         │
│  │ Design tests for each → Predict outcomes           │         │
│  │ Use "think hard" or "ultrathink" prompts           │         │
│  └────────────────────────────────────────────────────┘         │
│                         ↓                                       │
│  PHASE 3: DEBUGGING (TEST & VALIDATE)                           │
│  ┌────────────────────────────────────────────────────┐         │
│  │ Write failing test → Add logging → Binary search   │         │
│  │ Validate hypotheses → Isolate root cause           │         │
│  │ ✓ Now we know the problem                          │         │
│  └────────────────────────────────────────────────────┘         │
│                         ↓                                       │
│  PHASE 4: FIX & VERIFY (MINIMAL CHANGES)                        │
│  ┌────────────────────────────────────────────────────┐         │
│  │ Implement minimal fix → Run tests                  │         │
│  │ Verify ACGME compliance → Full test suite          │         │
│  │ Commit with context → Update docs                  │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Concrete Usage Examples

### Example 1: Double-Booking Bug (Complete Session)

**User Report:** "Residents are getting double-booked on the same day"

**Phase 1: Exploration**
```bash
# Read conflict detection logic (NO CHANGES)
cat backend/app/scheduling/conflicts/analyzer.py

# Check recent errors
docker-compose logs backend | grep -i "conflict\|double" | tail -20

# Review overlap detection tests
cat backend/tests/test_conflict_detection.py

# Check recent changes
git log --oneline -10 -- backend/app/scheduling/
```

**Phase 2: Planning (Think Hard)**
```
Hypotheses ranked by likelihood:

| # | Hypothesis | Evidence For | Evidence Against | Test |
|---|------------|--------------|------------------|------|
| 1 | Date boundary issue (70%) | Errors mention overnight shifts | Works for single-day rotations | Create test with midnight boundary |
| 2 | Missing overlap validator (20%) | Some conflicts not caught | Most conflicts work fine | Check validator registration |
| 3 | Race condition (10%) | Intermittent failures | Happens in single-threaded tests | Add database locking test |
```

**Phase 3: Debugging**
```python
# Write failing test (TDD approach)
# backend/tests/regression/test_double_booking_bug.py

import pytest
from datetime import date
from app.scheduling.conflicts import ConflictDetector

class TestDoublBookingBug:
    async def test_overnight_rotation_overlap(self, db):
        """Regression test for double-booking bug.

        This SHOULD FAIL before fix is applied.
        """
        # Setup: Resident assigned to 24-hour call (today 0800 to tomorrow 0800)
        assignment1 = create_assignment(
            person_id="PGY1-01",
            start_time=datetime(2026, 3, 12, 8, 0),
            end_time=datetime(2026, 3, 13, 8, 0)  # Next day
        )

        # Action: Try to assign same resident to clinic tomorrow at 0800
        assignment2 = create_assignment(
            person_id="PGY1-01",
            start_time=datetime(2026, 3, 13, 8, 0),  # Exact end of call
            end_time=datetime(2026, 3, 13, 17, 0)
        )

        # Assert: Should detect conflict (currently fails - uses < instead of <=)
        detector = ConflictDetector()
        conflicts = await detector.detect_overlaps(db, [assignment1, assignment2])

        assert len(conflicts) > 0, "Should detect overlap at boundary"
```

```bash
# Run test - expect failure
cd backend
pytest tests/regression/test_double_booking_bug.py -v

# Output: FAILED - No conflict detected (BUG CONFIRMED)
```

**Adding diagnostic logging:**
```python
# Temporarily add to backend/app/scheduling/conflicts/analyzer.py
import logging
logger = logging.getLogger(__name__)

def check_overlap(self, a1, a2):
    logger.info(f"DEBUG: Comparing {a1.start_time} to {a2.end_time}")
    logger.info(f"DEBUG: Current logic: a1.start < a2.end = {a1.start_time < a2.end_time}")
    # ... rest of logic
```

```bash
# Run with logging
LOG_LEVEL=DEBUG pytest tests/regression/test_double_booking_bug.py -v -s

# Output shows: "a1.start < a2.end = False" (boundary issue confirmed!)
```

**Root cause identified:** Using `<` instead of `<=` for end time comparison.

**Phase 4: Fix & Verify**
```python
# Minimal fix in backend/app/scheduling/conflicts/analyzer.py
def check_overlap(self, a1: Assignment, a2: Assignment) -> bool:
    """Check if two assignments overlap in time."""
    # OLD: return a1.start_time < a2.end_time and a2.start_time < a1.end_time
    # NEW: Use <= for inclusive boundary
    return a1.start_time <= a2.end_time and a2.start_time <= a1.end_time
```

```bash
# Verify fix
pytest tests/regression/test_double_booking_bug.py -v  # PASS
pytest tests/test_conflict_detection.py -v              # All PASS
pytest -m acgme -v                                      # All PASS
pytest --cov=app.scheduling.conflicts -v                # Coverage maintained

# Remove debug logging
# Commit with context
git add backend/app/scheduling/conflicts/analyzer.py
git add backend/tests/regression/test_double_booking_bug.py
git commit -m "$(cat <<'EOF'
fix: prevent double-booking at exact shift boundaries

Root cause: Overlap detection used exclusive comparison (<) instead
of inclusive (<=) for end times, allowing assignments at exact
boundary times like call ending at 0800 and clinic starting at 0800.

Fix: Changed to inclusive comparison (<=) to catch boundary overlaps.

Adds regression test to prevent recurrence.
EOF
)"
```

### Example 2: Failed Hypothesis Recovery

**Scenario:** First hypothesis was wrong. What now?

**Initial hypothesis:** "ACGME work hour calculation is off by one"

```python
# Phase 3: Tested hypothesis
pytest tests/test_acgme_work_hours.py -v -k "calculation"
# All tests PASS - hypothesis WRONG
```

**Recovery workflow:**
1. **Document what we learned:**
   ```markdown
   ## Hypothesis 1: FAILED
   - Tested: Work hour calculation logic
   - Result: All unit tests pass, calculation is correct
   - Insight: Bug must be elsewhere in the chain
   ```

2. **Return to Phase 2 with new information:**
   ```
   Updated hypotheses:

   | # | Hypothesis | New Evidence |
   |---|------------|--------------|
   | 2 | Data aggregation bug (60%) | Calculation correct but totals wrong |
   | 3 | Timezone conversion issue (30%) | UTC vs local time mismatch |
   | 4 | Caching stale data (10%) | Old values persisting |
   ```

3. **Test next hypothesis:**
   ```python
   # Test hypothesis 2: Aggregation
   # Add logging to aggregation function
   # Check if daily hours sum correctly to weekly total
   ```

4. **Keep iterating until root cause found**

**Key lesson:** Failed hypotheses are NOT failures - they narrow the search space.

## Failure Mode Handling

### Failure Mode 1: Can't Reproduce the Bug

**Symptoms:**
- Tests pass locally but fail in CI
- Bug only appears intermittently
- Error logs don't show the issue

**Recovery:**
```bash
# 1. Gather more context
git log --all --grep="[keyword]" --oneline
docker-compose logs backend --since 24h > full_logs.txt

# 2. Check for environment differences
diff .env.example .env  # Local vs CI config differences?

# 3. Try to reproduce in CI-like environment
docker-compose down
docker-compose up -d --build  # Fresh environment
pytest tests/  # Run in container

# 4. Add more instrumentation
# Increase logging, add timing information, capture state
```

### Failure Mode 2: Too Many Possible Causes

**Symptoms:**
- 5+ equally plausible hypotheses
- Complex multi-component interaction
- Unclear where to start

**Recovery:**
1. **Use binary search on commits:**
   ```bash
   git bisect start
   git bisect bad HEAD
   git bisect good <last_known_good_commit>
   # Git will checkout midpoint - test and mark good/bad
   ```

2. **Simplify the system:**
   ```python
   # Comment out half the logic, see if bug persists
   # Narrow down which component is involved
   ```

3. **Use `/search-party` skill for parallel exploration:**
   ```
   "Deploy search-party to investigate:
   - Component A: Authentication flow
   - Component B: Database queries
   - Component C: Validation logic"
   ```

### Failure Mode 3: Fix Breaks Other Tests

**Symptoms:**
- Regression test passes
- Unrelated tests now fail
- Fix has unexpected side effects

**Recovery:**
```bash
# 1. Identify what broke
pytest -v --lf  # Run last failed tests

# 2. Understand the dependency
# Why did the fix affect this test?
cat tests/test_broken_by_fix.py

# 3. Options:
# A. Fix was too broad - narrow scope
# B. Tests had wrong assumptions - update tests
# C. Actual regression - revert and rethink

# 4. If unclear, escalate to human
```

### Failure Mode 4: Stuck in Exploration Loop

**Symptoms:**
- Reading code for >20 minutes
- Not moving to hypothesis phase
- Gathering more info than needed

**Recovery:**
```
STOP. Force yourself to Phase 2.

Even if incomplete understanding, write down:
1. What you know
2. What you don't know
3. Top 3 guesses

Then ASK: "What's the simplest test to validate guess #1?"
```

**Escape command:**
```
"Make a plan first - stop exploring and form hypotheses based on
what we've learned so far"
```

## Integration with Other Skills

### With automated-code-fixer

**Workflow:**
1. Systematic-debugger identifies root cause
2. Writes failing regression test
3. Hands off to automated-code-fixer: "Fix the code to make this test pass"
4. Fixer implements minimal change
5. Systematic-debugger verifies all tests pass

**Example:**
```
User: "Residents double-booked"
[systematic-debugger activated]
→ Explores, plans, writes failing test
→ Root cause: date comparison bug in analyzer.py line 45

Claude: "I've identified the issue. Handing off to automated-code-fixer
to implement the fix."

[automated-code-fixer activated]
→ Changes < to <= on line 45
→ Runs tests, all pass
→ Creates commit
```

### With test-writer

**Workflow:**
1. Systematic-debugger finds bug
2. Needs edge case tests for Phase 3
3. Delegates to test-writer: "Generate tests for these scenarios"
4. Test-writer creates comprehensive test suite
5. Systematic-debugger uses tests to validate fix

### With security-audit

**When to integrate:**
- Bug involves authentication/authorization
- Error messages might leak sensitive data
- SQL injection or XSS potential

**Workflow:**
```
[systematic-debugger identifies security-related bug]
→ Pauses debugging workflow
→ Invokes security-audit skill
→ Security-audit reviews proposed fix for vulnerabilities
→ Returns to systematic-debugger with security clearance
→ Implements fix with security best practices
```

### With code-review

**Post-fix integration:**
```
[systematic-debugger completes fix]
→ Runs verification tests
→ Invokes code-review skill
→ Code-review checks fix quality, style, architecture
→ Approves or requests improvements
→ Commit only after code-review passes
```

## Validation Checklist

### Phase 1: Exploration Complete When...
- [ ] Read relevant source code (no changes made)
- [ ] Examined error logs and stack traces
- [ ] Reviewed related tests
- [ ] Checked recent git history
- [ ] Can answer: "What should happen?" and "What actually happens?"
- [ ] Have NOT made any code changes yet

### Phase 2: Planning Complete When...
- [ ] Listed at least 2 hypotheses
- [ ] Ranked hypotheses by likelihood with reasoning
- [ ] Defined testable predictions for each hypothesis
- [ ] Identified which hypothesis to test first
- [ ] Have a clear "what would disprove this?" for top hypothesis
- [ ] Still have NOT made code changes

### Phase 3: Debugging Complete When...
- [ ] Written failing test that reproduces the bug
- [ ] Confirmed test fails with current code
- [ ] Added diagnostic logging if needed
- [ ] Validated or invalidated top hypothesis
- [ ] Isolated root cause with evidence
- [ ] Can explain in one sentence: "The bug is caused by..."

### Phase 4: Fix Complete When...
- [ ] Implemented minimal fix (no refactoring)
- [ ] Regression test now passes
- [ ] Related test suite passes
- [ ] ACGME tests pass (if applicable)
- [ ] Full test suite passes
- [ ] No linting errors
- [ ] Removed temporary debug code
- [ ] Commit message explains root cause and fix
- [ ] Documentation updated if needed

### Escalation Validation

**Escalate to human if ANY of these are true:**
- [ ] Root cause unclear after 3 hypothesis iterations
- [ ] Fix requires database migration
- [ ] Fix modifies ACGME compliance logic
- [ ] Fix touches authentication/authorization
- [ ] Multiple interconnected components involved
- [ ] Production data at risk
- [ ] Fix breaks >3 existing tests

## References

- [DEBUGGING_WORKFLOW.md](../../../docs/development/DEBUGGING_WORKFLOW.md) - Full methodology
- [CI_CD_TROUBLESHOOTING.md](../../../docs/development/CI_CD_TROUBLESHOOTING.md) - CI failure patterns
