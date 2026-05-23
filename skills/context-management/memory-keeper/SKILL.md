---
name: Memory Keeper (Proactive Context Maintenance)
description: Automatically detect and maintain memory freshness by monitoring context staleness, significant code changes, task completions, and phase transitions. Proactively suggests and executes memory sync operations with user confirmation. Use when the user says "sync memory", "update context", or when the Skill detects that context is stale (>2 hours), significant changes have occurred (new commits), tasks completed, or major milestones reached. Replaces passive "context is stale" warnings with active maintenance.
allowed-tools: Read, Write, Bash
---

# Memory Keeper - Proactive Context Maintenance

## Purpose

This Skill replaces passive staleness warnings ("Your context is 11 hours old") with **proactive maintenance**. Instead of warning you context is stale, it:

1. **Detects** when sync is needed
2. **Diagnoses** what changed
3. **Suggests** sync with specific details
4. **Confirms** with you
5. **Executes** `/memory-sync` automatically

**Result**: Your memory files stay fresh without manual intervention.

---

## When This Skill Activates

**User-Initiated Triggers**:
- "Sync memory"
- "Update context"
- "Capture learnings"
- "Memory sync"

**Auto-Triggered (Proactive Detection)**:
- Context is stale (>2 hours)
- Task completed (advanced from one task to next)
- Major milestone reached (all tasks complete)
- Phase transition detected
- Significant code changes detected
- Test suite completed
- Standards check passed
- **Constitutional violations detected** (NEW v2.0.0)
- **Cross-file inconsistency detected** (NEW v2.0.0)
- **Quality gate failure** (NEW v2.0.0)
- **Cross-project memory drift** (NEW v2.0.0)

---

## How It Works

### Continuous Monitoring (Passive)

The Skill continuously monitors (when not actively doing other work):

**What It Watches**:
1. `active_context.md` modification time
2. Git commit history
3. Task completion status in `tasks_plan.md`
4. Test execution events
5. Phase transition markers

**Watch Intervals**:
- Every 30 minutes (check staleness)
- After task completion
- After test execution
- After /memory-sync is available

### Staleness Detection

**Freshness Categories**:

| Age | Status | Action |
|-----|--------|--------|
| <1 hour | ✅ Current | No action needed |
| 1-2 hours | 🟡 Getting stale | Suggest sync |
| 2-24 hours | 🔴 Stale | Recommend sync |
| >24 hours | 🔴🔴 Very stale | Urge sync immediately |

### Change Detection (Enhanced v2.0.0)

Monitor for significant changes requiring memory update:

**Code Changes**:
```bash
git log --oneline -10 | grep -E "feat:|fix:|refactor:"
# If N commits since last active_context update → Suggest sync
```

**Task Changes**:
```bash
# If task marked as [x] since last sync → Suggest capture
# If new phase reached → Suggest update
```

**Test Events**:
```bash
# If tests just completed → Suggest capture
# If all tests passing → Suggest validation capture
```

**Constitutional Compliance Changes (NEW v2.0.0)**:
```bash
# Monitor for constitutional violations
if [ -f .claude/audit/$(date +%Y-%m-%d).json ]; then
  # Check recent audit entries
  violations=$(jq '[.entries[] | select(.decision == "BLOCKED")] | length' .claude/audit/$(date +%Y-%m-%d).json)

  if [ "$violations" -gt 0 ]; then
    # Suggest memory sync to record violations and remediation
    trigger_sync "constitutional_violation"
  fi
fi
```

**Cross-File Consistency (NEW v2.0.0)**:
```bash
# Run memory-consistency validator
.claude/validators/core/memory-consistency.sh
exit_code=$?

if [ $exit_code -eq 2 ]; then
  # HIGH severity: Missing required file
  trigger_sync "missing_required_file"
elif [ $exit_code -eq 4 ]; then
  # LOW severity: Broken reference
  trigger_sync "broken_reference"
fi
```

**Quality Gate Failures (NEW v2.0.0)**:
```bash
# Check for recent quality gate failures
if [ -f .claude/cache/validator-results/ ]; then
  failed_gates=$(find .claude/cache/validator-results/ -name "*.json" -mmin -60 | \
    xargs jq -r 'select(.status == "FAIL") | .principle_name')

  if [ -n "$failed_gates" ]; then
    # Update tasks_plan.md with blockers
    trigger_sync "quality_gate_failure"
  fi
fi
```

**Cross-Project Drift (NEW v2.0.0)**:
```bash
# Detect if same project accessed from different directory
project_id=$(git rev-parse --show-toplevel | md5sum | cut -d' ' -f1)
last_access_dir=$(jq -r ".projects[] | select(.id == \"$project_id\") | .last_directory" ~/.claude/state/projects.json)

if [ -n "$last_access_dir" ] && [ "$last_access_dir" != "$(pwd)" ]; then
  # Warn about cross-project drift
  trigger_sync "cross_project_drift"
fi
```

### Proactive Suggestion Workflow

**Scenario 1: Regular Staleness Check**

```
Every 30 minutes, check:
├─ Is active_context.md > 2 hours old?
├─ Have there been commits since last update?
└─ Are tasks progressing?

If YES to any:
  Suggest: "Context is 3 hours old. Sync memory to capture progress?"
  User chooses: [Yes] [No] [Later]
```

**Scenario 2: After Task Completion**

```
When @agent-implementer completes a task:
├─ Task marked as [x]
├─ active_context.md needs update
└─ Learnings should be captured

Suggest: "T001 complete! Sync memory to capture learnings?
   This will update:
   - Task progress (0/26 → 1/26)
   - Time tracking
   - Lessons learned
   - Next task hint
"
```

**Scenario 3: After Phase Transition**

```
When all tasks complete:
├─ Phase transitions from 4 → 5 (Validation)
├─ Tests should be run
└─ Memory should record milestone

Suggest: "All tasks complete! Ready for validation phase.
   Sync memory to mark milestone?
"
```

### Execution with Confirmation

**User Confirms Yes:**

```
Executing: /memory-sync

This will:
1. Update active_context.md
2. Capture current feature state
3. Record task progress
4. Log implementation insights
5. Update lessons-learned.md
6. Mark staleness as resolved

Running...
✅ Memory synced successfully
```

**User Chooses No:**

```
Postponed: Memory sync deferred
Next: Will suggest again when > 3 hours old
```

**User Chooses Later:**

```
Postponed: Will ask in 30 minutes
Can also manually trigger: "sync memory"
```

---

## Examples

### Example 1: Regular Staleness Detection

**Skill Detection**: 2 hours 30 minutes since last sync

**Skill Behavior**:
```
📝 MEMORY FRESHNESS CHECK

Current Status:
├─ Context: 2.5 hours old (was fresh at 10:00 AM)
├─ Last Activity: Feature 006, Phase 4 task completion
├─ Git Commits: 3 commits since last sync
└─ Changes: Task progress (5% → 12%), implementation ongoing

🎯 RECOMMENDATION:
   Time to sync memory and capture progress

   This will update:
   - active_context.md (current feature state)
   - task progress tracker (5 tasks → 6 tasks complete)
   - implementation insights (patterns, issues found)
   - lessons-learned.md (what we discovered)

   Estimated time: 2 minutes

💡 OPTIONS:
   [Yes] - Sync now (recommended)
   [No] - Skip for now
   [Later] - Ask again in 30 min
   [Dismiss] - Until next event
```

**User Actions**:
- If "Yes" → Runs `/memory-sync` automatically
- If "No" → Stops, resumes monitoring
- If "Later" → Waits 30 minutes, checks again
- If "Dismiss" → Waits for next significant event

---

### Example 2: Task Completion Event

**Scenario**: User completes first task via @agent-implementer

**Skill Detection**: Task marked `[x]` in tasks_plan.md

**Skill Behavior**:
```
✅ TASK COMPLETION DETECTED

T001: Create migration for redaction_events table
├─ Status: COMPLETE ✓
├─ Time: 12 minutes (estimated 10)
└─ Quality: Tests passing, standards met

🎯 CAPTURE THIS PROGRESS:
   Sync memory to record:
   - Task completion (1/26 done)
   - Time tracking (progress evaluation)
   - Implementation patterns discovered
   - Any issues encountered
   - Lessons for remaining 25 tasks

📊 CURRENT PROGRESS:
   Completed: 1/26 (4%)
   In Progress: 0
   Estimated Remaining: 6.5 hours - 0.2 = 6.3 hours

💡 QUICK ACTIONS:
   [Sync Memory] - Update context (1 min)
   [Continue] - Keep working, sync later
   [Summary] - Show what will be synced
```

**Example Output if Synced**:
```
✅ Memory synced
Task progress captured: 1/26 complete (4%)
Learnings recorded: Database migration completed successfully
Next task: T002 (Create RedactionEvent model with factory)
Time tracking: 0.2 hours used, 6.3 hours remaining
```

---

### Example 3: After Phase 4 (All Tests Passing)

**Scenario**: All 26 tasks complete, tests passing

**Skill Detection**: All `[x]` in tasks_plan.md, test suite passed

**Skill Behavior**:
```
🎉 MAJOR MILESTONE REACHED

All Implementation Tasks Complete!

✅ Completed:
├─ Phase 4: All 26 tasks (100%)
├─ Tests: All passing (coverage >90%)
├─ Standards: PHPStan Level 8, ESLint clean
└─ Time: 6.5 hours (on estimate)

📍 READY FOR PHASE 5 - VALIDATION

🎯 CAPTURE THIS MILESTONE:
   Sync memory to record:
   - Feature completion (100%)
   - Overall time tracking
   - Major lessons learned during implementation
   - Patterns that worked well
   - Issues encountered and resolved
   - Recommendations for similar features

📊 TIME SUMMARY:
   Spec → Planning → Tasks: 3 hours
   Implementation: 6.5 hours
   Total: 9.5 hours

💡 NEXT PHASE:
   1. Sync memory (capture milestone)
   2. Run /test-run (final validation)
   3. Run /standards-check (final quality check)
   4. Then: PR creation or deployment

   [Sync Memory] - Record milestone
   [Validate Now] - Run full test suite
   [Continue] - I'll handle validation manually
```

---

### Example 4: Multi-Project Memory Tracking

**User**: Switches between projects

**Skill Detection**: Different git repository detected

**Skill Behavior**:
```
🔄 PROJECT SWITCH DETECTED

From: /Users/dev/dev_IECPN (IECPN Dashboard)
To:   /Users/dev/api-refactor (API Refactor)

📝 OUTGOING PROJECT STATUS:
   dev_IECPN:
   ├─ Feature: #006 PHI Logging
   ├─ Phase: 4 - Implementation (6% complete)
   ├─ Memory: 2.5 hours stale
   └─ Recommendation: Run /memory-sync before switching

📝 INCOMING PROJECT STATUS:
   api-refactor:
   ├─ Feature: #012 API Gateway
   ├─ Phase: 2 - Planning (plan.md exists)
   ├─ Memory: Current (1 hour old)
   └─ Status: Ready to start /tasks

💡 OPTIONS:
   [Sync dev_IECPN First] - Update before switch (recommended)
   [Switch Now] - I'll handle sync later
   [Sync Both] - Sync before AND after switch

→ Recommended: Sync dev_IECPN first to preserve progress
```

---

### Example 5: Constitutional Violation Detection (NEW v2.0.0)

**Scenario**: Validator detects security violation during commit

**Skill Detection**: Audit log shows blocked commit with CRITICAL violation

**Skill Behavior**:
```
⚠️  CONSTITUTIONAL VIOLATION DETECTED

Event: pre-commit hook blocked commit
Time: 2 minutes ago
Severity: CRITICAL

Violation Details:
   Principle I - Security First: FAILED
   Validator: sql-injection.sh
   Issue: String concatenation in SQL query detected
   Location: backend/services/quiz.py:127

🎯 MEMORY UPDATE RECOMMENDED

This will:
   1. Record violation in error-documentation.md
   2. Document remediation steps
   3. Update active_context.md with blocker
   4. Mark affected task as blocked in tasks_plan.md
   5. Add lesson to lessons-learned.md (SQL injection prevention)

📊 IMPACT ANALYSIS:
   Current Phase: 4 - Implementation (blocked)
   Tasks Affected: T006 (Implement quiz service)
   Estimated Fix Time: 15 minutes
   Constitutional Compliance: 6/7 principles (85%)

💡 OPTIONS:
   [Sync Memory] - Record violation and remediation (recommended)
   [Fix First] - Fix issue, then sync
   [Dismiss] - I'll handle documentation manually

→ Recommended: Sync now to preserve context of issue
```

---

### Example 6: Cross-File Inconsistency Detection (NEW v2.0.0)

**Scenario**: Memory-consistency validator detects broken references

**Skill Detection**: Validator exits with code 2 (HIGH severity)

**Skill Behavior**:
```
❌ MEMORY CONSISTENCY ISSUE

Validator: memory-consistency.sh
Severity: HIGH
Exit Code: 2

Issues Detected:
   1. Broken reference in tasks_plan.md
      → Links to architecture.md#service-layer
      → Section does not exist in architecture.md

   2. Orphaned glossary term: "RedactionEvent"
      → Defined in glossary.md
      → Not used in any other memory files

   3. Duplicate heading across files
      → "Database Schema" appears in:
         - architecture.md (line 234)
         - technical.md (line 156)

🎯 MEMORY SYNC RECOMMENDED

This will:
   1. Fix broken references (update or remove)
   2. Clean up orphaned terms
   3. Consolidate duplicate information
   4. Run consistency check again
   5. Update active_context.md with fixes

⏱️  Estimated: 5 minutes

💡 OPTIONS:
   [Auto-Fix] - Automatically resolve issues (recommended)
   [Manual Fix] - I'll fix each issue manually
   [Run Validator] - Show detailed diagnostic first

→ Recommended: Auto-fix to restore consistency
```

---

### Example 7: Quality Gate Failure Tracking (NEW v2.0.0)

**Scenario**: Test coverage drops below quality gate threshold

**Skill Detection**: Coverage gate validation fails

**Skill Behavior**:
```
⚖️  QUALITY GATE FAILURE

Gate: Gate 4 - Coverage Gate
Status: FAILED
Time: Just now

Failure Details:
   Required: Test coverage >80%
   Actual: 72% (dropped from 85%)
   Cause: 3 new files added without tests

Files Needing Tests:
   1. backend/services/redaction.py (0% coverage)
   2. backend/models/redaction_event.py (45% coverage)
   3. backend/utils/phi_detector.py (0% coverage)

🎯 MEMORY UPDATE RECOMMENDED

This will:
   1. Update tasks_plan.md with blocker
   2. Add remediation tasks (write tests for 3 files)
   3. Record in error-documentation.md
   4. Update active_context.md with quality gate status
   5. Estimate additional time needed (90 min)

📊 IMPACT:
   Phase Transition: BLOCKED (cannot move to validation)
   Tasks Affected: Phase D (testing)
   Additional Work: 3 test files (~90 minutes)

💡 OPTIONS:
   [Sync & Block] - Update memory, block phase transition
   [Add Tasks] - Auto-generate test tasks in tasks_plan.md
   [Dismiss] - I'll handle this manually

→ Recommended: Auto-generate test tasks to unblock
```

---

## Integration with Other Skills

**Relationship to context-navigator**:
- `context-navigator`: Shows staleness problem
- `memory-keeper`: Fixes staleness problem
- Flow: See stale context → memory-keeper offers to fix

**Relationship to quick-start**:
- `quick-start`: Needs fresh memory
- `memory-keeper`: Ensures fresh memory available
- Flow: Before coding → memory-keeper offers refresh → then quick-start

**Relationship to phase-guide**:
- `phase-guide`: Detects phase transitions
- `memory-keeper`: Syncs after transitions
- Flow: Phase transition → memory-keeper captures milestone

---

## Proactive vs Manual

### Proactive (This Skill)

```
Time: Every 30 minutes or on events
Trigger: Automatic staleness detection
User: Gets proactive suggestion
Action: Confirm sync or skip
Result: Context stays fresh
```

### Manual (Slash Command)

```
Time: When user explicitly requests
Trigger: `/memory-sync` command
User: Explicitly runs command
Action: Sync executes immediately
Result: Context updated on demand
```

**When to Use Which**:
- **Proactive** (memory-keeper): Daily work, passive monitoring
- **Manual** (/memory-sync): Explicit sync needed, debugging, prep for PR

---

## Smart Defaults

### Default Sync Triggers

**Automatic Sync Recommended If**:
- Context > 3 hours old AND user idle
- Phase transition detected
- All tasks completed
- Major test milestone reached

**Automatic Sync NOT Recommended If**:
- User actively typing/coding
- In middle of implementation task
- Just ran tests (test output still relevant)
- Within 5 minutes of last sync

### User Preferences (Future)

Could remember user preferences:
- "Always sync after task completion"
- "Remind every 1 hour (not 2)"
- "Disable proactive - sync manually only"
- "Sync on phase transition always"

---

## Performance

This Skill performs:
- File modification time checks (fast)
- Git log queries (fast)
- Pattern matching for task status (fast)
- State monitoring (passive, low overhead)
- Constitutional violation monitoring (NEW v2.0.0)
- Cross-file consistency validation (NEW v2.0.0)
- Quality gate status checking (NEW v2.0.0)

**Execution time**: <150ms for checks (with v2.0.0 features)
**Execution time**: <100ms for checks (v1.0.0 mode)
**Background monitoring**: Minimal overhead (~50ms every 30 minutes)
**No side effects until user confirms**: Safe to monitor constantly

---

## Graceful Degradation (NEW v2.0.0)

This skill is **backward compatible** and adapts to available features:

**Without Constitution** (v1.0.0 mode):
- Constitutional violation monitoring: Disabled
- Quality gate checking: Skipped
- All other monitoring active
- No errors or warnings

**Without Audit Logs**:
```
Constitutional Monitoring: Not available (no .claude/audit/)
Status: v1.0.0 mode (staleness and git monitoring only)
```

**Without Validators**:
- Cross-file consistency checking: Skipped
- Quality gate validation: Skipped
- Basic staleness monitoring continues

**Without Cross-Project State**:
- No ~/.claude/state/projects.json → Skip drift detection
- Single-project mode continues normally
- Creates state file on first multi-project use

**Partial Feature Availability**:
```
✅ Available Monitors:
   ✓ Staleness detection (core)
   ✓ Git change detection (core)
   ✓ Task completion tracking (core)
   ✓ Constitutional compliance (if constitution exists)
   ❌ Cross-file consistency (validators missing)
   ❌ Quality gate tracking (cache missing)

Status: Partial monitoring active
```

This ensures:
1. Works in all environments (minimal to full-featured)
2. No breaking changes from v1.0.0
3. Incremental feature adoption
4. Core functionality always available

---

## Troubleshooting

**Issue**: Skill offers to sync too frequently

**Cause**: Default 2-hour threshold might be too aggressive for your workflow

**Fix**: Mention your preference:
- "Only suggest sync every 4 hours"
- "Sync on task completion only"

---

**Issue**: Skill suggests sync at inconvenient time

**Cause**: Staleness threshold triggered mid-task

**Fix**: Choose "Later" option to defer

---

**Issue**: Too many constitutional violation suggestions (NEW v2.0.0)

**Cause**: Validators triggering frequently

**Fix**:
- Fix underlying violations
- Adjust validator severity in constitution
- Disable specific validators temporarily

---

**Issue**: Cross-file consistency checks slow down monitoring (NEW v2.0.0)

**Cause**: Memory-consistency validator running too frequently

**Fix**:
- Reduce check frequency (default: every 30 min → every 2 hours)
- Cache validator results longer

---

## What This Skill Does NOT Do

- ❌ Does NOT force sync without permission
- ❌ Does NOT interrupt active coding
- ❌ Does NOT modify code (only memory files)
- ❌ Does NOT replace manual `/memory-sync` (still available)
- ❌ Does NOT fix constitutional violations (only detects and suggests sync) (NEW v2.0.0)
- ❌ Does NOT auto-resolve cross-file inconsistencies (suggests manual/auto-fix) (NEW v2.0.0)
- ❌ Does NOT modify quality gates (only tracks failures) (NEW v2.0.0)

This Skill maintains memory freshness and detects issues. You remain in control.

---

## Vision: Invisible Maintenance

Ideal scenario: **You never manually think about memory sync again**

- Skill detects when needed
- Offers at good moments
- You confirm with one action
- Context stays fresh automatically
- Focus on coding, not maintenance

---

## Future Enhancements

Potential expansions (not in initial release):
- [ ] Cross-project memory sync (sync all at once)
- [ ] Memory diff visualization (see exactly what will sync)
- [ ] Historical memory tracking (version history)
- [ ] Team memory coordination (sync notifications)
- [ ] Selective sync (sync specific memory sections)
