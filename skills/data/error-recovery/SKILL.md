---
name: error-recovery
description: Use when encountering failures - assess severity, preserve evidence, execute rollback decision tree, and verify post-recovery state
---

# Error Recovery

## Overview

Handle failures gracefully with structured recovery.

**Core principle:** When things break, don't panic. Assess, preserve, recover, verify.

**Announce at start:** "I'm using error-recovery to handle this failure."

## The Recovery Protocol

```
Error Detected
      │
      ▼
┌─────────────┐
│ 1. ASSESS   │ ← Severity? Scope? Impact?
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 2. PRESERVE │ ← Capture evidence before it's lost
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 3. RECOVER  │ ← Follow decision tree
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 4. VERIFY   │ ← Confirm clean state
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 5. DOCUMENT │ ← Record what happened
└─────────────┘
```

## Step 1: Assess Severity

### Severity Levels

| Level | Description | Examples |
|-------|-------------|----------|
| **Critical** | System unusable, data at risk | Build completely broken, tests cause data loss |
| **Major** | Significant functionality broken | Feature doesn't work, many tests failing |
| **Minor** | Isolated issue, workaround exists | Single test flaky, style error |
| **Info** | Warning only, not blocking | Deprecation notice, performance hint |

### Assessment Questions

```markdown
## Error Assessment

**Error:** [Description of error]
**Location:** [Where it occurred]

### Severity Checklist
- [ ] Is the system still functional?
- [ ] Is any data at risk?
- [ ] Are other features affected?
- [ ] Is this blocking progress?

### Scope
- Files affected: [list]
- Features affected: [list]
- Users affected: [none/some/all]
```

## Step 2: Preserve Evidence

**Capture BEFORE attempting fixes:**

### Error Logs

```bash
# Capture error output
pnpm test 2>&1 | tee error-log.txt

# Or from failed command
./failing-command 2>&1 | tee error-log.txt
```

### Stack Traces

```markdown
## Stack Trace

```
Error: Connection refused
    at Database.connect (src/db/connection.ts:45)
    at UserService.init (src/services/user.ts:23)
    at main (src/index.ts:12)
```
```

### State Capture

```bash
# Git state
git status
git diff

# Environment state
env | grep -E "NODE|NPM|PATH"

# Dependency state
pnpm list
```

### Screenshot (if visual)

For UI errors, capture screenshots before changes.

## Step 3: Recover

### Decision Tree

```
What type of failure?
         │
    ┌────┴────┬────────────┬────────────┐
    │         │            │            │
  Code      Build      Environment   External
  Error     Error        Issue       Service
    │         │            │            │
    ▼         ▼            ▼            ▼
  ┌────┐   ┌────┐      ┌────┐      ┌────┐
  │Git │   │Clean│     │Re-  │     │Wait/│
  │reco│   │build│     │init │     │Retry│
  │very│   │     │     │     │     │     │
  └────┘   └────┘      └────┘      └────┘
```

### Code Error Recovery

**Single file broken:**

```bash
# Revert just that file
git checkout HEAD -- path/to/file.ts
```

**Feature broken (multiple files):**

```bash
# Find last good commit
git log --oneline

# Revert to that commit (soft reset keeps changes staged)
git reset --soft [GOOD_COMMIT]

# Or hard reset (discards changes)
git reset --hard [GOOD_COMMIT]
```

**Working directory is a mess:**

```bash
# Stash current changes
git stash

# Verify clean state
git status

# Optionally recover stash later
git stash pop
```

### Build Error Recovery

```bash
# Clean build artifacts
rm -rf node_modules dist build .cache

# Reinstall dependencies
pnpm install --frozen-lockfile  # Clean install from lock file

# Rebuild
pnpm build
```

### Environment Error Recovery

```bash
# Check environment
env | grep -E "NODE|PNPM"

# Reset Node modules
rm -rf node_modules
pnpm install --frozen-lockfile

# If using nvm, verify version
nvm use

# Re-run init script
./scripts/init.sh
```

### External Service Error

```bash
# Check if service is up
curl -I https://service.example.com/health

# If down, wait and retry
sleep 60
curl -I https://service.example.com/health

# If still down, check status page
# Document as external blocker
```

## Step 4: Verify

After recovery, verify clean state:

### Basic Verification

```bash
# Clean working directory
git status
# Expected: "nothing to commit, working tree clean" or known changes

# Tests pass
pnpm test

# Build succeeds
pnpm build

# Types check
pnpm typecheck
```

### Functionality Verification

```bash
# Run the specific thing that was broken
pnpm test --grep "specific test"

# Or verify the feature manually
```

## Step 5: Document

### Issue Comment

```bash
gh issue comment [ISSUE_NUMBER] --body "## Error Recovery

**Error encountered:** [Description]

**Severity:** Major

**Evidence:**
\`\`\`
[Error output]
\`\`\`

**Recovery actions:**
1. [Action 1]
2. [Action 2]

**Verification:**
- [x] Tests pass
- [x] Build succeeds

**Root cause:** [If known]

**Prevention:** [If applicable]
"
```

### Knowledge Graph

```javascript
// Store for future reference
mcp__memory__add_observations({
  observations: [{
    entityName: "Issue #[NUMBER]",
    contents: [
      "Encountered [error type] on [date]",
      "Caused by: [root cause]",
      "Resolved by: [recovery action]"
    ]
  }]
});
```

## Common Recovery Patterns

### "Tests were passing, now failing"

```bash
# What changed?
git diff HEAD~3

# Did dependencies change?
git diff HEAD~3 pnpm-lock.yaml

# Clean reinstall
rm -rf node_modules && pnpm install --frozen-lockfile
```

### "Works locally, fails in CI"

```bash
# Check for environment differences
# - Node version
# - OS differences
# - Env vars

# Run with CI-like settings
CI=true pnpm test
```

### "Build was working, now broken"

```bash
# Check TypeScript errors
pnpm typecheck

# Check for circular dependencies
pnpm dlx madge --circular src/

# Clean build
rm -rf dist && pnpm build
```

### "I broke everything"

```bash
# Don't panic
# Find last known good state
git log --oneline

# Reset to that state
git reset --hard [GOOD_COMMIT]

# Verify
pnpm test

# Start again more carefully
```

## Escalation

If recovery fails after 2-3 attempts:

```markdown
## Escalation: Unrecoverable Error

**Issue:** #[NUMBER]

**Error:** [Description]

**Recovery attempts:**
1. [Attempt 1] - [Result]
2. [Attempt 2] - [Result]

**Current state:** [Broken/Partially working]

**Evidence preserved:** [Links to logs, screenshots]

**Requesting help with:** [Specific question]
```

Mark issue as Blocked and await human input.

## Checklist

When error occurs:

- [ ] Severity assessed
- [ ] Evidence preserved (logs, state, screenshots)
- [ ] Recovery action selected
- [ ] Recovery executed
- [ ] Clean state verified
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Issue documented

## Integration

This skill is called by:
- `issue-driven-development` - When errors occur
- `ci-monitoring` - CI failures

This skill may trigger:
- `research-after-failure` - If cause is unknown
- Issue update via `issue-lifecycle`
