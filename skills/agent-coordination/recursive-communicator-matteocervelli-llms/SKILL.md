---
name: recursive-communicator
description: Auto-activates when managing agent-to-agent communication for validation
  failures and recursive fix cycles between validation specialists and main agent.
allowed-tools: Read, Write
---

## Purpose

The **recursive-communicator** skill provides structured protocols for managing recursive communication loops between the validation orchestrator, validation specialists, and the main feature implementer agent. It handles failure notifications, fix requests, re-validation triggers, and loop termination to ensure validation issues are resolved systematically.

## When to Use

This skill auto-activates when you:
- Communicate validation failures to the main agent
- Request fixes from the main agent for validation issues
- Trigger re-validation after main agent fixes
- Manage recursive fix loops (failure → fix → re-check → repeat)
- Track iteration counts in recursive communication
- Prevent deadlocks in recursive loops
- Escalate unresolvable validation issues
- Log communication history for traceability

## Provided Capabilities

### 1. Failure Communication
- **Structured Failure Reports**: Format validation failures for main agent
- **Detailed Error Information**: Include file locations, line numbers, error messages
- **Suggested Fixes**: Provide specialist recommendations for resolving issues
- **Priority Tagging**: Mark critical vs. non-critical failures
- **Context Preservation**: Include all relevant context for debugging

### 2. Fix Request Management
- **Clear Fix Requests**: Explicitly request main agent to fix specific issues
- **Action Items**: Provide actionable list of fixes needed
- **Deadline Awareness**: Track iteration limits (max 5)
- **Fix Verification**: Confirm when main agent completes fixes
- **Re-validation Triggering**: Signal specialists to re-check after fixes

### 3. Re-validation Coordination
- **Re-check Signals**: Trigger specialist re-validation after fixes
- **Iteration Tracking**: Increment and track iteration counts
- **Status Updates**: Communicate re-validation status to all parties
- **Loop Continuation**: Determine if another iteration needed
- **Loop Termination**: Identify when to exit recursive loop

### 4. Deadlock Prevention
- **Max Iteration Limits**: Enforce maximum 5 iterations per specialist
- **Timeout Detection**: Identify stalled communication
- **Escalation Triggers**: Escalate after max iterations or timeout
- **User Intervention Requests**: Flag when human input needed
- **Graceful Degradation**: Handle unresolvable issues without blocking workflow

### 5. Communication Logging
- **Message History**: Log all communication between agents
- **Iteration History**: Track all iterations with timestamps
- **Fix History**: Document all fixes attempted
- **Status Transitions**: Log status changes (failed → fixing → re-checking → passed)
- **Audit Trail**: Maintain complete communication audit trail

## Usage Guide

### Step 1: Detect Validation Failure

When a validation specialist reports failure:

```markdown
**Validation Failure Detected**

**Specialist**: test-runner-specialist
**Phase**: Test Execution
**Issue**: 3 unit tests failing

**Failure Details**:
- test_validation_coordinator.py::test_sequential_invocation - AssertionError
- test_validation_coordinator.py::test_failure_tracking - KeyError
- test_validation_coordinator.py::test_workflow_completion - AttributeError

**Coverage**: 73.2% (target: ≥80%)

**Action Required**: Activate recursive-communicator skill
```

### Step 2: Format Failure Report

Use communication-protocol.md and message-templates.md to format structured report:

**Failure Report Structure**:
```markdown
## Validation Failure Report

**Report ID**: VFR-{issue-number}-{specialist-name}-{iteration}
**Generated**: [YYYY-MM-DD HH:MM:SS]
**Issue**: #{issue-number} - [Feature Name]
**Specialist**: [Specialist Name]
**Phase**: [Validation Phase]
**Iteration**: [Current] / [Max (5)]

---

### Failure Summary

**Status**: ❌ FAILED
**Failure Type**: [Test Failures / Quality Issues / Security Vulnerabilities / E2E Failures]
**Severity**: [Critical / High / Medium / Low]
**Impact**: Blocks progression to [Next Phase]

---

### Detailed Failures

#### Failure 1: [Test/Issue Name]
- **File**: [File path]
- **Line**: [Line number]
- **Error Type**: [AssertionError / TypeError / SecurityError / etc.]
- **Error Message**:
  ```
  [Full error message from specialist]
  ```
- **Context**: [Additional context about the failure]

#### Failure 2: [Test/Issue Name]
- **File**: [File path]
- **Line**: [Line number]
- **Error Type**: [Error type]
- **Error Message**:
  ```
  [Full error message]
  ```
- **Context**: [Additional context]

[... Additional failures ...]

---

### Suggested Fixes

#### Fix for Failure 1
**Recommendation**: [Specialist's suggestion for fixing the issue]
**Approach**: [Specific steps or code changes needed]
**Priority**: [Critical / High / Medium / Low]

#### Fix for Failure 2
**Recommendation**: [Specialist's suggestion]
**Approach**: [Specific steps]
**Priority**: [Priority level]

[... Additional fix suggestions ...]

---

### Required Actions

**Main Agent (@feature-implementer-main):**
1. Review failure details above
2. Implement suggested fixes (or alternative approach)
3. Verify fixes locally (if possible)
4. Signal completion to validation orchestrator
5. Await re-validation

**Expected Timeline**: [Estimated time to fix]
**Escalation**: If fixes cannot be completed, escalate to user

---

### Re-validation Plan

**After Fix Completion**:
1. Validation orchestrator will re-invoke [Specialist Name]
2. Specialist will re-run [Tests/Checks]
3. IF pass: Proceed to [Next Phase]
4. IF fail: Iteration [Current+1] / [Max (5)]
5. IF max iterations exceeded: Escalate to user intervention

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: Main Agent Fix Completion
```

### Step 3: Send Failure Report to Main Agent

Communicate failure report to @feature-implementer-main:

**Communication Protocol**:
```markdown
### Sending Failure Report

**To**: @feature-implementer-main
**From**: @validation-orchestrator (via recursive-communicator)
**Type**: Validation Failure Report
**Priority**: [High/Medium/Low based on severity]

**Message**:
---
@feature-implementer-main: Validation failure detected during [Phase] validation.

[Full Failure Report from Step 2]

Please review and fix the above issues. Signal completion when ready for re-validation.
---

**Status**: Sent
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Awaiting Response**: Yes
```

### Step 4: Wait for Main Agent Fix

Monitor main agent activity:

**Waiting State**:
```markdown
### Awaiting Main Agent Fix

**Current Status**: Waiting for Fix
**Specialist**: [Specialist Name] (paused)
**Iteration**: [Current] / [Max (5)]
**Time Elapsed**: [MM:SS since failure report sent]
**Timeout**: 30 minutes (escalate if exceeded)

**Main Agent Actions Expected**:
- [ ] Review failure report
- [ ] Analyze failure root causes
- [ ] Implement fixes
- [ ] Verify fixes locally (optional)
- [ ] Signal completion to validation orchestrator

**Monitoring**:
- Check main agent status every 2 minutes
- Log any main agent communications
- Detect timeout if >30 minutes without response
```

**Timeout Handling**:
```markdown
IF time_elapsed > 30 minutes WITHOUT main agent response:
  1. Log timeout event
  2. Send reminder to main agent
  3. IF still no response after reminder (5 minutes):
     a. Escalate to user intervention
     b. Flag as "unresponsive"
     c. Await user decision (abort / manual fix / extend timeout)
```

### Step 5: Receive Fix Completion Signal

When main agent signals fix completion:

**Fix Completion Confirmation**:
```markdown
### Main Agent Fix Completed

**Received From**: @feature-implementer-main
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Fix Duration**: [MM:SS from failure report to completion]

**Main Agent Report**:
[Summary of fixes implemented by main agent]

**Fixes Applied**:
- Fix 1: [Description of fix]
- Fix 2: [Description of fix]
- [... Additional fixes ...]

**Verification**:
- [ ] Main agent confirmed fixes applied
- [ ] Files modified: [List of changed files]
- [ ] Ready for re-validation

**Next Action**: Trigger re-validation (Step 6)
```

### Step 6: Trigger Re-validation

Re-invoke specialist for re-check:

**Re-validation Trigger**:
```markdown
### Triggering Re-validation

**Specialist**: [Specialist Name]
**Iteration**: [Current+1] / [Max (5)]
**Previous Status**: Failed
**Current Status**: Re-checking

**Re-invocation**:
@[specialist-name] re-check [validation type] for feature #{issue-number}
Iteration: [Current+1] / [Max (5)]
Previous failures: [List of failures from previous iteration]
Fixes applied: [List of fixes from main agent]

**Expected Outcomes**:
1. **PASS**: All previous failures resolved
   - Exit recursive loop
   - Proceed to next validation phase
   - Log success with iteration count

2. **FAIL** (some/all failures persist):
   - Increment iteration count
   - Return to Step 1 (detect failure)
   - IF iteration <= 5: Repeat recursive loop
   - IF iteration > 5: Escalate (Step 7)

**Status**: Re-validation in Progress
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
```

### Step 7: Handle Re-validation Result

Process specialist re-check output:

**Result: PASS** ✅
```markdown
### Re-validation Success

**Specialist**: [Specialist Name]
**Iteration**: [Final] / [Max (5)]
**Status**: ✅ PASSED

**Previous Failures**: [Count] failures
**Current Failures**: 0 failures
**Resolution**: All issues fixed by main agent

**Iteration History**:
- Iteration 1: [X] failures
- Iteration 2: [Y] failures
- ...
- Iteration [Final]: 0 failures (PASS)

**Total Fix Time**: [HH:MM:SS across all iterations]

**Action**: Exit recursive loop, proceed to [Next Phase]
**Communication**: Notify main agent of success
**Logging**: Log successful resolution and iteration count
```

**Result: FAIL** ❌
```markdown
### Re-validation Failure (Iteration [Current] / 5)

**Specialist**: [Specialist Name]
**Iteration**: [Current] / [Max (5)]
**Status**: ❌ STILL FAILING

**Previous Failures**: [Count from previous iteration]
**Current Failures**: [Count from current iteration]
**New Failures**: [Count of new failures introduced]
**Persistent Failures**: [Count still failing]

**Analysis**:
- Failures resolved: [List]
- Failures persisting: [List]
- New failures introduced: [List]

**Decision**:
IF iteration < 5:
  ✅ Continue recursive loop
  ✅ Return to Step 2 (format new failure report)
  ✅ Increment iteration: [Current+1] / 5
ELSE (iteration >= 5):
  ⛔ Max iterations exceeded
  ⛔ Proceed to Step 8 (escalation)
```

### Step 8: Escalate Unresolvable Issues

When max iterations (5) exceeded or timeout occurs:

**Escalation Report**:
```markdown
## Escalation: Unresolvable Validation Issue

**Escalation ID**: ESC-{issue-number}-{specialist-name}-{timestamp}
**Generated**: [YYYY-MM-DD HH:MM:SS]
**Issue**: #{issue-number} - [Feature Name]
**Specialist**: [Specialist Name]
**Phase**: [Validation Phase]
**Escalation Reason**: [Max Iterations Exceeded / Timeout / Deadlock / Other]

---

### Escalation Summary

**Status**: ⛔ UNRESOLVABLE (Requires User Intervention)
**Total Iterations**: [Max (5)]
**Total Time**: [HH:MM:SS across all iterations]
**Persistent Failures**: [Count]

---

### Iteration History

| Iteration | Failures | Fixes Applied | Result |
|-----------|----------|---------------|--------|
| 1 | [Count] | [Summary] | FAIL |
| 2 | [Count] | [Summary] | FAIL |
| 3 | [Count] | [Summary] | FAIL |
| 4 | [Count] | [Summary] | FAIL |
| 5 | [Count] | [Summary] | FAIL |

**Pattern Analysis**: [Analysis of why failures persist across iterations]

---

### Persistent Failures

[List of failures that remain unresolved after 5 iterations]

#### Failure 1: [Test/Issue Name]
- **File**: [File path]
- **Line**: [Line number]
- **Error**: [Error message]
- **Iterations Failed**: [1, 2, 3, 4, 5]
- **Fixes Attempted**:
  - Iteration 1: [Fix attempted]
  - Iteration 2: [Fix attempted]
  - ...
- **Why Unresolved**: [Analysis of why this failure persists]

[... Additional persistent failures ...]

---

### Recommended Actions

**Option 1: User Manual Fix**
- User reviews failures and provides manual fix
- Validation orchestrator re-runs after user fix
- Risk: Requires user expertise

**Option 2: Skip Validation**
- Mark validation as "failed but proceeding"
- Document known issues
- Risk: Deploy with known failures

**Option 3: Abort Feature**
- Stop implementation
- Return feature to design phase
- Risk: Wasted effort on implementation

**Option 4: Extend Max Iterations**
- Allow additional iterations (e.g., 3 more)
- Continue recursive loop
- Risk: Potentially infinite loop

---

**Escalated To**: User / Main Orchestrator
**Awaiting Decision**: [Option 1 / Option 2 / Option 3 / Option 4]
**Validation Workflow**: PAUSED

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
```

### Step 9: Log Communication History

Maintain complete audit trail:

**Communication Log Entry**:
```markdown
### Communication Log

**Entry ID**: LOG-{issue-number}-{specialist-name}-{iteration}-{timestamp}

**Participants**:
- Validation Orchestrator (@validation-orchestrator)
- Specialist (@[specialist-name])
- Main Agent (@feature-implementer-main)

**Communication Flow**:

**[Timestamp 1]** Specialist → Orchestrator: Validation failure detected
- Failures: [Count]
- Details: [Summary]

**[Timestamp 2]** Orchestrator → Main Agent: Failure report sent (Iteration 1/5)
- Report ID: VFR-{issue-number}-{specialist-name}-1
- Status: Awaiting Fix

**[Timestamp 3]** Main Agent → Orchestrator: Fix completion signal
- Duration: [MM:SS]
- Fixes: [Summary]

**[Timestamp 4]** Orchestrator → Specialist: Re-validation triggered (Iteration 2/5)
- Status: Re-checking

**[Timestamp 5]** Specialist → Orchestrator: Re-validation result (PASS)
- Status: ✅ All failures resolved
- Final iteration: 2/5

**[Timestamp 6]** Orchestrator → Main Agent: Success notification
- Status: Validation passed
- Proceed to: [Next Phase]

---

**Total Messages**: 6
**Total Iterations**: 2
**Total Duration**: [HH:MM:SS]
**Outcome**: Success
```

## Best Practices

### 1. Clear Communication
- Use structured message templates (from message-templates.md)
- Include all relevant context (files, lines, errors)
- Provide actionable fix suggestions
- Specify expected outcomes clearly

### 2. Iteration Tracking
- Always track current/max iterations
- Log every iteration with timestamp
- Document fixes attempted in each iteration
- Analyze patterns across iterations

### 3. Timeout Management
- Set reasonable timeouts (default: 30 minutes)
- Send reminders before escalation
- Log timeout events
- Escalate gracefully when timeout exceeded

### 4. Deadlock Prevention
- Enforce strict max iterations (5)
- Detect circular failures (same failure across iterations)
- Escalate when progress stalls
- Provide escape routes (skip validation, user intervention)

### 5. Comprehensive Logging
- Log all messages between agents
- Track status transitions
- Document fix attempts
- Maintain audit trail for troubleshooting

### 6. Graceful Escalation
- Provide context when escalating
- Offer multiple resolution options
- Include iteration history and analysis
- Make escalation actionable for user

## Resources

### communication-protocol.md
Comprehensive protocol for agent-to-agent communication including:
- Message formatting standards
- Communication flow patterns
- Status signaling conventions
- Timeout and escalation procedures
- Error handling protocols

### message-templates.md
Pre-defined message templates for common scenarios:
- Failure report template
- Fix request template
- Re-validation trigger template
- Success notification template
- Escalation report template
- Communication log template

## Example Usage

### Input (Validation Failure)

```markdown
**Specialist**: test-runner-specialist
**Status**: FAILED
**Failures**:
- 3 unit tests failing
- Coverage: 73.2% (target: 80%)

**Error Details**:
test_validation_coordinator.py::test_sequential_invocation - AssertionError
test_validation_coordinator.py::test_failure_tracking - KeyError
test_validation_coordinator.py::test_workflow_completion - AttributeError
```

### Output (Recursive Communication Flow)

```markdown
## Recursive Communication: Feature #47 (Iteration 1/5)

### Step 1: Failure Detection
**Status**: ❌ Test failures detected by test-runner-specialist
**Failures**: 3 tests, coverage below target

### Step 2: Failure Report Formatted
**Report ID**: VFR-47-test-runner-1
**Sent To**: @feature-implementer-main
**Content**: Detailed failure report with error messages and fix suggestions

### Step 3: Awaiting Fix
**Status**: Waiting for main agent fix
**Elapsed**: 00:08:32
**Timeout**: 30 minutes

### Step 4: Fix Completed
**Status**: Main agent fixed issues
**Duration**: 00:08:32
**Fixes**: Implementation logic errors in validation_coordinator.py

### Step 5: Re-validation Triggered
**Status**: Re-invoking test-runner-specialist (Iteration 2/5)
**Action**: Re-run tests with fixed implementation

### Step 6: Re-validation Result
**Status**: ❌ 1 test still failing (improvement from 3)
**Action**: Continue to Iteration 2

[Iteration 2 begins... follows same flow]

### Final Result (Iteration 3)
**Status**: ✅ ALL TESTS PASS, Coverage 87.3%
**Total Iterations**: 3/5
**Total Time**: 00:24:15
**Outcome**: Exit recursive loop, proceed to Code Quality phase
```

## Integration

This skill is used by:
- **validation-orchestrator** agent during Phase 5: Validation
- Activates automatically when validation failures occur
- Works in conjunction with **validation-coordinator** skill for workflow management
- Enables recursive communication pattern between validation specialists and main agent
- Critical for resolving validation issues before deployment

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when validation failures occur)
**Phase**: 5 (Validation)
**Created**: 2025-10-29