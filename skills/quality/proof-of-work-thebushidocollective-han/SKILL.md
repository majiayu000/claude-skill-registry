---
name: proof-of-work
description: Use automatically during development workflows when making claims about tests, builds, verification, or code quality requiring concrete evidence to ensure trust through transparency.
allowed-tools:
  - Write
  - Edit
  - Read
  - Bash
  - Grep
---

# Proof of Work

**Show, don't tell.** Never make claims about code verification without
providing concrete evidence.

## Core Principle

**Trust through transparency.** Every assertion about code quality, test
results, builds, or verification must be backed by actual command output,
not summaries or assumptions.

## Implementation Proof

When implementing features:

1. **USE Write/Edit tools to make changes**
   - Never just describe what should be written
   - Actually call Write tool to create files
   - Actually call Edit tool to modify files

2. **Show tool results**
   - After Write: "Successfully wrote /path/to/file.ex"
   - After Edit: "Successfully edited /path/to/file.ex"
   - Tool output is proof changes were made

3. **Verify changes exist**
   - Use Bash to verify files exist: `ls -la /path/to/file.ex`
   - Use Read to show content if needed
   - Actual file existence is proof

**Remember**: If you didn't use Write/Edit tools, it didn't happen.

## Agent Verification (CRITICAL)

**NEVER EVER trust agent completion reports without verification.**

This is a **zero-tolerance rule**.
Agent reports are NOT proof - they are **claims requiring verification**.

### The Critical Error

When you delegate work to a subagent:

1. Agent completes and reports "Successfully created X, modified Y,
   implementation complete"
2. **STOP - DO NOT TRUST THIS REPORT**
3. Agent reports mean NOTHING until you verify
4. Blindly trusting agent reports is a **catastrophic failure**

### Mandatory Verification After EVERY Agent

**After ANY agent completes, you MUST verify work was actually done:**

```bash
# 1. Verify files were actually modified
git status --short

# 2. Verify actual changes exist
git diff --name-only

# 3. Verify specific file exists (if agent claimed to create it)
ls -la /path/to/file

# 4. Verify file content (spot check)
cat /path/to/file | head -20
```

**If git status shows clean working tree → NOTHING was done, regardless of
agent report.**

### Red Flags in Agent Reports

### Never trust these claims without verification

| Agent Claim               | Required Verification                       |
| ------------------------- | ------------------------------------------- |
| "Successfully created X"  | `ls -la /path/to/X` - prove file exists     |
| "Modified files A, B, C"  | `git status` - prove files show as modified |
| "Changes made to Y"       | `git diff Y` - prove actual changes exist   |
| "Implementation complete" | `git diff --stat` - prove work was done     |
| "Added tests to Z"        | `cat Z` - prove tests actually exist        |
| "Updated configuration"   | `git diff config/` - prove config changed   |

### Verification Workflow (MANDATORY)

```text
1. Delegate to agent
2. Agent reports completion
3. ⚠️  STOP - DO NOT TRUST REPORT ⚠️
4. Run verification commands (git status, ls, cat, etc.)
5. If verification fails → Agent did NOT complete work
6. If verification passes → THEN report to user WITH PROOF
```

### Evidence Requirements for Agent Work

**❌ NEVER report to user:**

- "Agent created X" (without proving X exists)
- "Agent modified Y" (without showing git diff)
- "Implementation complete" (without showing git status)
- "Tests added" (without proving tests exist)

**✅ ALWAYS report with proof:**

```bash
# After agent completes, verify:
$ git status --short
M  apps/api/lib/users/worker.ex
A  apps/api/test/users/worker_test.exs

# Prove files exist:
$ ls -la apps/api/test/users/worker_test.exs
-rw-r--r--  1 user  staff  2847 Nov  7 14:32 apps/api/test/users/worker_test.exs

# Spot check content:
$ head -10 apps/api/test/users/worker_test.exs
defmodule YourApp.Users.UserTest do
  use YourApp.DataCase
  ...
```

**Then report:** "Agent completed. Verification proves 2 files modified
(evidence above)."

### Why This Matters

### Failure to verify agent work

- Destroys user trust
- Wastes user time
- Results in false claims
- Violates proof-of-work principle
- Is a **catastrophic error**

**The user must be able to trust your reports.** Agent reports without
verification are **worthless**.

### Agent Verification Remember

- **Agent reports are claims, not proof**
- **Verification is MANDATORY after EVERY agent**
- **If you didn't verify, you don't know if it happened**
- **Git status is ground truth, not agent reports**
- **Never report agent completion without showing verification**

**This is non-negotiable.** Failure to verify agent work is unacceptable.

## When to Apply

Apply this skill whenever claiming:

- Tests pass/fail
- Build succeeds/fails
- Linting clean/has issues
- Types check
- GraphQL compatibility verified
- CI pipeline status
- Code review findings
- Performance metrics
- Any verifiable development assertion

## Evidence Requirements

**❌ Never say without proof:**

- "Tests pass" / "Build succeeds" / "No linting issues"
- "Types check" / "Pipeline is green" / "Code is clean"

**✅ Always provide actual output:**

```bash
# Tests
$ mix test
Finished in 42.3 seconds
1,247 tests, 0 failures

# Linting
$ MIX_ENV=test mix lint
Running Credo... ✓ No issues found.

# Types
$ yarn ts:check
✓ 456 files checked, 0 errors

# CI Pipeline
$ glab ci status
Pipeline #12345: passed ✓
URL: https://gitlab.com/.../pipelines/12345
```

## Zero Tolerance for Assumptions

### Never assume or claim without running

❌ **WRONG:**

- "The tests should pass"
- "This probably works"
- "Based on my changes, tests will pass"
- "I expect the build succeeds"

✅ **RIGHT:**

- "I have not run the tests yet. Let me run them now."
- "Running `mix test` to verify..."
- [Shows complete output]

## Partial Verification Is Not Verification

**❌ NEVER claim success from partial runs:**

```bash
# Only ran 50 tests of 1,247
Running ExUnit tests...
50 tests, 0 failures
# STOPPED HERE - did not complete
```

"Tests pass" ❌ **FALSE - only partial run**

**✅ ALWAYS run to completion:**

```bash
# Full suite completed
Finished in 42.3 seconds
1,247 tests, 0 failures  # ALL tests ran
```

"Full test suite passes: 1,247 tests, 0 failures" ✅ **TRUE**

## Output Format

1. Show the command you ran
2. Show results, not summaries
3. Include counts (tests, files, errors)
4. Include URLs for CI/remote resources

## Complete Verification Example

```bash
$ MIX_ENV=test mix lint
✓ No issues found.

$ mix test
1,247 tests, 0 failures

$ yarn graphql:compat
✓ No breaking changes

$ glab ci status
Pipeline #12345: passed ✓
```

**Then claim:** "All verification passed (evidence above)."

## Red Flags

Stop and provide proof if you catch yourself saying:

- "Tests pass" (without showing output)
- "Build works" (without showing build log)
- "No errors" (without showing check results)
- "Pipeline is green" (without showing pipeline status)
- "Code is clean" (without showing lint output)
- "Types check" (without showing tsc output)

## Workflow Integration

**Implementation:** Run verification → Show complete output → Report with
evidence → Wait for approval

**Code review:** Reference line numbers (`file.ts:123`), quote issues,
show analyzer output

**Debugging:** Show full errors, stack traces, reproduction steps with
output

## Remember

- **Every claim needs proof** - No exceptions
- **Show complete output** - No summaries or excerpts for verification
- **Run commands yourself** - Never assume or infer results
- **Timestamps matter** - Show when verification ran
- **Links are proof** - Provide URLs for remote resources
- **Honesty over convenience** - Admit when you haven't verified

### Transparency builds trust. Evidence eliminates doubt
