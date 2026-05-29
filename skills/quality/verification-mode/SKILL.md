---
name: verification-mode
description: Verification mode that stops and analyzes on failures, workarounds, or resolution issues
user-invocable: false
allowed-tools: Read
---

# Verification Skill

When this skill is loaded, you are in VERIFICATION MODE. This modifies your behavior for ALL subsequent operations. You MUST follow the verification protocols below.

Verification mode ensures quality by stopping execution on any failure, workaround, or resolution issue to perform root cause analysis before proceeding.

## CRITICAL: Process vs Data Priority

**In verification mode, the PROCESS takes priority over the TASK.**

| Aspect | Normal Mode | Verification Mode |
|--------|-------------|-------------------|
| **Priority** | Complete the task | Validate the process |
| **On error** | Fix the data/result, continue | Fix the PROCESS (agent/skill/command) |
| **Success metric** | Task completed | Process works correctly |
| **Retry behavior** | Acceptable if result correct | STOP - investigate why retry was needed |

### Example: Wrong Approach vs Right Approach

**Scenario**: Agent produces invalid output, retries, second attempt succeeds.

❌ **Wrong (Normal Mode thinking)**:
> "The retry succeeded, the output is correct now. Continuing..."

✅ **Right (Verification Mode thinking)**:
> "STOP. The agent failed on first attempt. WHY? The process is broken.
> I must fix the AGENT/SKILL that produced the invalid output, not just accept the retry."

### The Core Question

When an error occurs, ask:

> "Which COMPONENT (agent, skill, command, script) caused this, and how do I fix IT?"

NOT:

> "How do I fix the data so I can continue?"

## What This Skill Provides

- **Failure Detection** - Stop on script failures, tool errors, or unexpected outputs
- **Resolution Analysis** - Stop when resolving paths, references, or dependencies fails
- **Workaround Detection** - Stop when using alternative approaches instead of intended methods
- **Root Cause Analysis** - Structured analysis of what failed and why
- **User Presentation** - Clear presentation of findings before proceeding

## When to Activate This Skill

Activate this skill when:
- **Testing new workflows** - Verifying skills, commands, or agents work correctly
- **Debugging issues** - Finding root causes of failures
- **Quality assurance** - Ensuring scripts and tools function as documented
- **Integration testing** - Verifying component interactions

## Activation Scopes

The skill supports different verification scopes via the `scope` parameter:

### Base Verification (default)

```
Skill: pm-plugin-development:verification-mode
```

Applies: Script failures, resolution failures, workaround detection

### Planning Verification

```
Skill: pm-plugin-development:verification-mode
scope: planning
```

Applies: All base checks PLUS:
- No direct .plan file access (must use manage-* scripts)
- Work-log population after each operation
- Status consistency after phase transitions
- **Post-Phase Verification Protocol (4 steps) after EVERY phase completes**
- **Workflow Skill API Contract Verification (Step 3) is MANDATORY**

Use this scope when testing `/plan-marshall` or any planning-related skills.

**CRITICAL**: After each phase completes, you MUST execute ALL 4 steps of the Post-Phase Verification Protocol, including verifying artifacts against workflow skill API contracts. See "After Each Phase Completes" section below.

## Verification Mode Behavior

**CRITICAL**: When this skill is loaded, you MUST modify your behavior as follows:

### On Script Failure

When any script returns non-zero exit code or produces error output:

1. **STOP** - Do not continue with the workflow
2. **ANALYZE** - Perform failure analysis (see standards/failure-analysis.md)
3. **PRESENT** - Show analysis to user with structured format
4. **WAIT** - Ask user how to proceed before continuing

### On Resolution Failure

When resolving paths, skill references, or dependencies fails:

1. **STOP** - Do not use fallback or alternative paths
2. **ANALYZE** - Perform resolution analysis (see standards/resolution-analysis.md)
3. **PRESENT** - Show what failed to resolve and why
4. **WAIT** - Ask user for guidance before proceeding

### On Workaround Usage

When you would use an alternative approach instead of the documented method:

1. **STOP** - Do not silently use the workaround
2. **DETECT** - Recognize you are about to use a workaround
3. **ANALYZE** - Explain why the intended method failed
4. **PRESENT** - Show both intended method and workaround
5. **WAIT** - Ask user to approve workaround or fix the issue

## Analysis Output Format

All analyses MUST use this structured format:

```
## [TYPE] Analysis Required

### Issue Detected
[Clear description of what triggered the stop]

### Context
- **Operation**: [What was being attempted]
- **Component**: [Which script/skill/command]
- **Expected**: [What should have happened]
- **Actual**: [What actually happened]

### Root Cause Analysis
[Analysis of why this occurred]

### Impact Assessment
| Aspect | Impact |
|--------|--------|
| Blocking | Yes/No |
| Data Loss Risk | Yes/No |
| Workaround Available | Yes/No |

### Options
1. [Option 1 with consequences]
2. [Option 2 with consequences]
3. [Option 3 with consequences]

### Recommendation
[Your recommended next step]

---
**Verification Mode Active** - Awaiting user decision before proceeding.
```

## Workflow

### Step 1: Acknowledge Verification Mode

When this skill is loaded, immediately acknowledge:

```
Verification Mode Active - All operations will stop on failures, resolution issues, or workarounds for analysis.
```

If `scope: planning` was specified, add:

```
Planning Scope Active - Additional checks: .plan access patterns, work-log population, status consistency.
```

### Step 2: Execute with Vigilance

For each operation:
1. Check if it's a script execution, resolution, or potential workaround
2. Monitor for failure conditions
3. Apply appropriate verification protocol if triggered

### Step 3: Analyze Failures

When verification protocol triggers:
1. Load appropriate analysis standard
2. Perform structured analysis
3. Format output per template
4. Present to user and wait

### Step 4: Resume After User Decision

Only after user provides direction:
1. Execute user's chosen option
2. Continue verification mode for subsequent operations
3. Track all verification stops in session

## Standards Organization

```
standards/
├── failure-analysis.md      (Script and tool failure analysis)
├── resolution-analysis.md   (Path and reference resolution issues)
├── workaround-detection.md  (Detecting and analyzing workarounds)
└── planning-compliance.md   (Planning command/skill access patterns)
```

## Verification Triggers

### Script Failures
- Non-zero exit code
- Error output (stderr)
- Unexpected output format
- Missing expected output
- Timeout conditions

### Resolution Failures
- Path not found
- Skill not found
- Reference not resolved
- Dependency missing
- Configuration missing

### Workaround Indicators
- Using alternative path
- Falling back to different method
- Skipping documented step
- Substituting different tool
- Manual intervention where automation expected

### Planning Compliance Violations (scope: planning only)

These checks apply ONLY when `scope: planning` is specified:

**Single Allowed `.plan` Access Pattern**:
```bash
python3 .plan/execute-script.py {notation} {subcommand} {args...}
```

This is the ONLY allowed way to interact with `.plan` files. All other access is a violation.

**Prohibited `.plan` Access** (ALL violations):
- Direct Read/Write/Edit of ANY `.plan/**` file (except via execute-script.py invocation)
- Direct Read/Write/Edit of `.plan/plans/*/status.toon`
- Direct Read/Write/Edit of `.plan/plans/*/references.toon`
- Direct Read/Write/Edit of `.plan/plans/*/work.log`
- Direct Read/Write/Edit of `.plan/marshall-state.toon`
- Direct Read/Write/Edit of `.plan/logs/*.log`
- Direct Read/Write/Edit of `.plan/lessons-learned/*.md`
- Direct access to goals/tasks directories
- Glob patterns targeting `.plan/**`
- Bash find/ls/cat commands accessing `.plan/` structure
- Missing work.log entry after significant operation
- Status not updated after phase transition
- Artifacts created without manage-* scripts

**Rationale**: All `.plan` access must go through manage-* scripts to ensure:
- Consistent audit trail via script execution logging
- Validation and error handling
- Single source of truth for file format changes

## Tool Access

**Read**: Load analysis standards on-demand

No other tools required - this skill modifies behavioral patterns.

## Integration Pattern

This skill is designed to be loaded alongside other skills:

```
Skill: pm-plugin-development:verification-mode
Skill: pm-workflow:phase-3-outline
```

When both are loaded, verification mode applies to all solution-outline operations.

## Quality Indicators

Verification mode is working correctly when:
- [ ] All script failures produce structured analysis
- [ ] Resolution issues are caught before fallbacks
- [ ] Workarounds are flagged before execution
- [ ] User is always asked before proceeding
- [ ] No silent failures or alternative paths taken

## Example Session

```
User: Run the init phase for my-plan

Claude: Verification Mode Active - All operations will stop on failures, resolution issues, or workarounds for analysis.

Executing plan-init for my-plan...

## SCRIPT FAILURE Analysis Required

### Issue Detected
Script pm-workflow:plan-marshall:manage-lifecycle returned non-zero exit code (1)

### Context
- **Operation**: Create plan status
- **Component**: pm-workflow:plan-manage
- **Expected**: status: success with plan created
- **Actual**: status: error with invalid_domain

### Root Cause Analysis
The domain "java-main" is not a valid domain identifier.
Script expects one of: java, javascript, plugin, generic.

### Impact Assessment
| Aspect | Impact |
|--------|--------|
| Blocking | Yes |
| Data Loss Risk | No |
| Workaround Available | Yes |

### Options
1. Fix the calling code to use valid domain identifier
2. Manually run with correct domain
3. Extend VALID_DOMAINS if new domain needed

### Recommendation
Fix option 1 - Update calling code to use valid domain "java"

---
**Verification Mode Active** - Awaiting user decision before proceeding.
```

## Planning-Specific Verification (scope: planning)

When `scope: planning` is specified, apply these additional checks for planning commands:

### Before Each Operation
1. Check if operation will access .plan files directly
2. Verify manage-* script is being used instead

### After Each Phase Completes (MANDATORY)

**CRITICAL**: Execute the **Post-Phase Verification Protocol** after EVERY phase transition (1-init→3-outline, 4-plan→5-execute, 5-execute→6-verify). This is NOT optional.

Load and follow the protocol from `standards/planning-compliance.md`:

```bash
Read: marketplace/bundles/pm-plugin-development/skills/verification-mode/standards/planning-compliance.md
```

The protocol has **4 steps** - ALL are MANDATORY:

| Step | Check | Action |
|------|-------|--------|
| 1 | Chat History Error Check | Scan for tool failures, error messages |
| 2 | Script Execution Log Check | See command below, look for ERROR entries |
| 3 | **Workflow Skill API Contract Verification** | **CRITICAL** - See commands below |
| 4 | Status Consistency Check | See command below |

**Step 2 Command**:
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log read --plan-id {plan_id} --type script
```

**Step 4 Command**:
```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle read --plan-id {plan_id}
```

**Step 3 Contract Verification Details**:

| Completed Phase | Contract |
|-----------------|----------|
| 1-init | domain-frontmatter-contract.md |
| 3-outline | deliverable-contract.md |
| 4-plan | task-contract.md |
| 5-execute | task verification criteria |

**Exact Verification Commands** (copy-paste ready):

**1-Init Phase** - Verify references.toon:
```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references read --plan-id {plan_id}
```

**2-Outline Phase** - Validate solution outline:
```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline validate --plan-id {plan_id}
```

**3-Plan Phase** - List and verify each task:
```bash
# List all tasks
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks list --plan-id {plan_id}

# Get each task by number (replace {N} with 1, 2, 3, etc.)
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks get --plan-id {plan_id} --number {N}

# Verify work-log has entry for each task creation
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log read --plan-id {plan_id} --type work
# Check output contains "[ARTIFACT]" entries for each TASK-N created
```

**Execute Phase** - Run task verification commands:
```bash
# Get task to retrieve verification.commands
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks get --plan-id {plan_id} --number {N}

# Then execute each command from the task's verification.commands array
```

**If ANY step fails** → STOP, analyze, present to user, wait for decision.

### After Each Operation (Non-Phase)
1. Query work-log for recent entry matching operation
2. Query status for consistency with expected phase
3. Report any discrepancies

### Example Planning Violation

```
User: Continue executing the current plan

Claude: Verification Mode Active

Checking plan status...

## PLANNING COMPLIANCE Violation Detected

### Issue Detected
Direct .plan file access bypassing manage-* API

### Context
- **Operation**: Read
- **Target**: .plan/plans/jwt-auth/status.toon
- **Expected**: Use `python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle read --plan-id jwt-auth`
- **Actual**: Direct file read attempted

### Root Cause Analysis
Command is reading status.toon directly instead of using
`python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle read`.
This bypasses audit trail and validation.

### Impact Assessment
| Aspect | Impact |
|--------|--------|
| Blocking | No - but should not proceed |
| Data Loss Risk | No (read-only) |
| Audit Trail | Not broken but inconsistent pattern |
| Maintainability | Poor - mixed access patterns |

### Options
1. **Use pm-workflow:plan-marshall:manage-lifecycle**: Consistent abstraction layer
2. **Proceed with warning**: Log deviation but continue

### Recommendation
Use `python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle read` for all status access

---
**Verification Mode Active** - Awaiting user decision before proceeding.
```

### Example Post-Operation Audit

```
User: (approved using pm-workflow:plan-marshall:manage-lifecycle)

Claude: Task TASK-001 completed successfully.

## POST-OPERATION Audit Verification

### Operation Completed
Marked TASK-001 as complete, transitioned to TASK-002

### Work-Log Check
```toon
entries[1]{timestamp,type,phase,summary}:
2025-12-07T14:30:00Z,outcome,execute,Completed TASK-001: Implement JWT generator
```

### Status Check
```toon
current_phase: 5-execute
phases[7]{name,status}:
1-init,done
2-refine,done
3-outline,done
4-plan,done
5-execute,in_progress
6-verify,pending
7-finalize,pending
```

### Verification Result
| Check | Status | Notes |
|-------|--------|-------|
| Work-log entry exists | Pass | Entry within last 5 seconds |
| Correct type | Pass | outcome matches task completion |
| Correct phase | Pass | 5-execute phase |
| Meaningful summary | Pass | Describes completed task |
| Status consistent | Pass | 5-execute phase in_progress |

### Assessment
PASS - All audit trail and status checks verified
```

## Deactivation

Verification mode remains active for the entire session once loaded.

To run without verification:
- Start a new session without loading this skill
- Or explicitly acknowledge: "Disable verification mode for this operation"

## Related Skills

### Deep Failure Analysis

For post-hoc analysis of script failures with origin tracing and fix proposals:

```
Skill: pm-plugin-development:analyze-script-failures
```

Or invoke via command:
```
/pm-plugin-development:tools-analyze-script-failures
```

**When to use**: After verification mode catches a failure, use analyze-script-failures to:
- Trace which component (command/agent/skill) triggered the failure
- Analyze how instructions led to the incorrect script call
- Get specific code fix proposals
- Record findings as lessons learned

**Difference**: Verification mode stops and analyzes in real-time; analyze-script-failures performs deep post-hoc analysis with origin tracing.
