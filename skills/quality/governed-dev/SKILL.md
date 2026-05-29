---
name: governed-dev
description: Evidence-first development with fail-closed behavior
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(./scripts/claude/*)
denied-tools:
  - Bash(curl)
  - Bash(wget)
  - Bash(powershell)
  - Bash(pwsh)
---

# Governed Development Skill

This skill enforces evidence-first development practices for Interlock.

## Core Principles

### 1. Evidence-First

Every claim must be backed by evidence:

- **If a command was not run**: Mark the claim as `UNVERIFIED`
- **If output was not captured**: Do not claim success
- **If artifacts were not produced**: Do not claim completion

```markdown
## Claim: Smoke tests pass

**Evidence**: `artifacts/claude/20260110T120000Z/smoke/summary.md`
**Status**: VERIFIED - Exit code 0, all steps passed
```

vs.

```markdown
## Claim: Smoke tests pass

**Evidence**: None
**Status**: UNVERIFIED - Command not executed
```

### 2. Fail-Closed

Never "limp past" failures:

- **Any non-zero exit**: Stop and report
- **Missing artifacts**: Stop and report
- **Partial success**: Report as failure

```bash
# WRONG - Ignoring failures
./scripts/claude/smoke.sh || true

# RIGHT - Respecting failures
./scripts/claude/smoke.sh
if [ $? -ne 0 ]; then
    echo "GATE FAILED"
    exit 1
fi
```

### 3. Artifacts Are Deliverables

Every operation should produce artifacts:

- **Link to artifacts** in reports
- **Preserve artifacts** for audit
- **Never overwrite** without archiving

```markdown
See: `artifacts/claude/20260110T120000Z/smoke/summary.md`
```

## Verification Rules

### Before Making Claims

1. Run the relevant wrapper script
2. Check exit code
3. Read the summary.md artifact
4. Only then make claims about results

### After Failures

1. Report the failure immediately
2. Link to error artifacts (stderr.log)
3. Do not attempt to "fix and continue" without explicit approval
4. Mark all downstream claims as BLOCKED

## Allowed Operations

| Operation | Tool | Purpose |
|-----------|------|---------|
| Read files | Read | Inspect code and artifacts |
| Search files | Grep, Glob | Find relevant code |
| Run wrappers | Bash(./scripts/claude/*) | Execute verified scripts |

## Prohibited Operations

- Arbitrary shell commands
- Network requests (curl, wget)
- Modifying production code without planning
- Claiming success without evidence
