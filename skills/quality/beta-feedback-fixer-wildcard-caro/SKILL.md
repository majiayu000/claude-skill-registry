---
name: beta-feedback-fixer
description: "Use when fixing issues identified in beta tester feedback. Guides systematic root cause analysis, worktree-based fixes, regression testing, and release preparation. Invoke with structured beta reports or issue lists."
version: 1.0.0
allowed-tools: "Bash, Read, Write, Edit, Grep, Glob, Task, TodoWrite"
---

# Beta Feedback Fixer Skill

## What This Skill Does

This skill automates the workflow for systematically fixing issues identified in beta tester feedback. It guides you through:

- Parsing structured beta testing reports
- Classifying issues by severity (P0/P1/P2)
- Performing root cause analysis
- Creating isolated worktrees for fixes
- Implementing fixes with regression tests
- Preparing next beta releases

**Core principle**: Fix issues systematically with proper isolation, testing, and documentation.

## When to Use This Skill

Activate this skill when:
- User provides a beta testing report with identified issues
- User asks to "fix beta feedback" or "resolve P0 issues"
- User wants to systematically address tester complaints
- User has a list of bugs from QA/testing cycles
- User needs to prepare the next beta release after fixes

**Example triggers:**
- "Fix these P0 issues from beta testing"
- "Address the beta tester feedback"
- "Resolve these critical bugs: [list]"
- "Prepare beta.2 with these fixes"

## Core Workflow

### Phase 1: Report Parsing & Issue Extraction

Parse structured beta testing reports and extract actionable issues.

**Supported formats:**
- Markdown reports (`.claude/releases/BETA-*-REPORT.md`)
- YAML test results
- GitHub issue lists
- Plain text with structured sections

**Extract for each issue:**
- Issue ID (if available)
- Title/description
- Severity/priority
- Expected behavior
- Actual behavior
- Reproduction steps
- Category (bug, docs, performance, etc.)

**Output**: Issue list with metadata

Example:
```markdown
## Extracted Issues

### Issue #402: Telemetry prompt spam (P0)
- **Category**: Bug - Config persistence
- **Expected**: Prompt shows once, persists choice
- **Actual**: Prompt shows on every command
- **Repro**: Run `caro "list files"` twice
```

### Phase 2: Severity Classification

Classify each issue by severity using this framework:

**P0 (Critical)** - Blocks release:
- Security vulnerabilities
- Data loss or corruption
- Complete feature breakage
- Unusable core functionality
- Output format corruption (JSON/YAML)

**P1 (High)** - Significant impact:
- Major UX degradation
- Performance regression >50%
- Missing critical features
- Workaround exists but difficult

**P2 (Medium)** - Minor impact:
- Cosmetic issues
- Documentation errors
- Minor UX annoyances
- Non-critical missing features

**Triage rules:**
1. Fix P0 issues first (required for release)
2. Group related issues (shared root cause)
3. Address P1 if time permits
4. Defer P2 to future releases

### Phase 3: Root Cause Analysis

For each issue, perform systematic root cause analysis:

**Step 1: Locate relevant code**
```bash
# Search for error messages
grep -r "error message text" src/

# Find relevant modules
find src/ -name "*telemetry*" -o -name "*config*"

# Check recent changes
git log --oneline --since="2 weeks ago" -- src/main.rs
```

**Step 2: Trace execution path**
- Add logging if needed
- Follow code flow from user action to bug
- Identify the exact line where behavior diverges

**Step 3: Identify root cause category**

Use these categories:

1. **Empty Implementation** (empty TODO branches)
   - Code path exists but not implemented
   - Example: Consent prompt result captured but never saved

2. **Missing Config Persistence**
   - User preferences not saved to disk
   - Config loaded but not written back

3. **Pattern Matching Issues**
   - Static patterns in wrong order (specific after general)
   - Regex too broad or too narrow
   - Missing required pattern

4. **Output Format Awareness**
   - Interactive prompts in non-interactive mode
   - Writing to stdout instead of stderr

5. **Documentation Mismatch**
   - Docs claim feature doesn't exist
   - Examples show wrong syntax

**Step 4: Document findings**

Use the root cause template (see `templates/root-cause-template.md`).

### Phase 4: Worktree Creation

Create an isolated environment for fixes:

```bash
# Create worktree
git worktree add .worktrees/fix-beta-X-p0-issues -b fix/beta-X-p0-issues

# Navigate to worktree
cd .worktrees/fix-beta-X-p0-issues

# Verify clean baseline
cargo test
```

**Branch naming convention**: `fix/beta-X-p0-issues`
- X = beta version number (1, 2, 3)
- Use "p0" for critical fixes, "p1" for high priority

### Phase 5: Implementation & Testing

Fix issues systematically with regression tests:

**For each issue:**

1. **Write regression test first** (TDD approach)
   ```rust
   #[tokio::test]
   async fn test_issue_402_telemetry_persistence() {
       // Setup: Fresh config
       let config_path = temp_config();

       // Execute: Run command twice
       run_command("list files", &config_path);
       run_command("list files", &config_path);

       // Assert: Config saved, first_run=false
       let config = load_config(&config_path);
       assert_eq!(config.telemetry.first_run, false);
   }
   ```

2. **Implement the fix**
   - Minimal change to fix the root cause
   - Preserve existing behavior
   - Add comments explaining the fix

3. **Verify fix works**
   ```bash
   # Run regression test
   cargo test test_issue_402

   # Run full test suite
   cargo test

   # Manual verification
   caro "list files"  # First run
   caro "list files"  # Should not show prompt
   ```

4. **Commit atomically**
   ```bash
   git add src/main.rs tests/beta_regression.rs
   git commit -m "fix(telemetry): Persist consent choice to config

   Fixes: #402, #403

   Root cause: Config was loaded but never saved after consent.
   Added config_manager.save() call after updating first_run flag.

   Regression test: test_issue_402_telemetry_persistence"
   ```

**Fix priority**: P0 first, then P1, then P2

**Commit granularity**: One logical fix per commit (may fix multiple related issues)

### Phase 6: PR & Release Preparation

After all fixes are implemented:

**1. Create comprehensive PR**

Use this template:
```markdown
## Summary

Fixes all X critical P0 issues from beta.Y testing.

**Fixes**: #402, #403, #404, #405, #406

## Issues Fixed

### Issue #402 & #403: [Title]
- ✅ FIXED: [What now works]
- Root cause: [Brief explanation]
- Fix: [What was changed]

[Repeat for each issue]

## Test Coverage

### Regression Tests
- ✅ test_issue_402_...
- ✅ test_issue_403_...

All X tests pass ✅

### Full Test Suite
- ✅ Y library tests pass
- ✅ No regressions

## Impact

**Before**: [Metrics/behavior]
**After**: [Metrics/behavior]

## Manual Verification

```bash
# Steps to manually verify fixes
```
```

**2. Bump version for next beta**

```bash
# Update Cargo.toml
version = "1.1.0-beta.X"

# Update CHANGELOG.md
## [1.1.0-beta.X] - YYYY-MM-DD

### Fixed
- Issue #402: [description]
- Issue #403: [description]
...

# Create git tag
git tag -a v1.1.0-beta.X -m "Release beta.X - Critical fixes"

# Push
git push origin fix/beta-Y-p0-issues
git push origin v1.1.0-beta.X
```

**3. Create beta testing instructions**

Update `.claude/releases/BETA-TESTING-INSTRUCTIONS-vX.md`:
- Document what was fixed
- Create focused test plan for verifying fixes
- Include regression testing checklist

## Templates & Checklists

### Root Cause Analysis

Use `templates/root-cause-template.md` to document each issue's RCA.

### Regression Test Structure

Use `templates/regression-test.md` for test boilerplate.

### Commit Messages

Format:
```
{type}({scope}): {brief description}

{Detailed explanation of root cause and fix}

Fixes: #{issue_id}

{Additional context, testing notes, verification steps}
```

Types: fix, feat, docs, test, refactor
Scopes: telemetry, config, backend, docs, safety

### PR Checklist

- [ ] All P0 issues have fixes
- [ ] Each fix has regression test
- [ ] All tests pass (cargo test)
- [ ] Manual verification completed
- [ ] Commit messages are descriptive
- [ ] PR description includes root causes
- [ ] CHANGELOG.md updated
- [ ] Version bumped if creating new beta

## Common Root Cause Patterns

Based on real beta testing experience, watch for these patterns:

### 1. Empty TODO Branches
**Symptom**: Code path exists but does nothing
**Location**: if/else with TODO comments
**Fix**: Implement the missing logic

```rust
// BEFORE (broken)
if user_config.telemetry.first_run {
    if prompt_consent() {
        // TODO: Save config
    }
}

// AFTER (fixed)
if user_config.telemetry.first_run {
    let consent = prompt_consent();
    user_config.telemetry.enabled = consent;
    user_config.telemetry.first_run = false;
    config_manager.save(&user_config)?;
}
```

### 2. Pattern Ordering Issues
**Symptom**: Wrong command generated, generic instead of specific
**Location**: Static pattern matcher
**Fix**: Move specific patterns before general patterns

```rust
// BEFORE (wrong order)
Pattern 1: "files modified" (3 keywords)
Pattern 46: "python files modified" (4 keywords)

// AFTER (correct order)
Pattern 1: "python files modified" (4 keywords - specific)
Pattern 2: "files modified" (3 keywords - general)
```

### 3. Missing Config Persistence
**Symptom**: User settings don't persist across runs
**Location**: Config loading without saving
**Fix**: Call save() after updating config

### 4. Output Format Awareness
**Symptom**: Interactive prompts pollute JSON/YAML output
**Location**: Prompts run unconditionally
**Fix**: Skip interactive prompts when output format is machine-readable

```rust
// BEFORE (broken)
prompt_consent();  // Always runs

// AFTER (fixed)
let is_interactive = matches!(cli.output, None | Some(OutputFormat::Plain));
if is_interactive {
    prompt_consent();
}
```

### 5. Documentation Drift
**Symptom**: Docs claim feature doesn't exist when it does
**Location**: Beta testing instructions, README
**Fix**: Update docs to match reality

## Best Practices

### Root Cause Analysis
- Don't assume - verify with code inspection
- Trace full execution path
- Document findings before fixing
- Look for related issues (shared root cause)

### Implementation
- Write regression test first (TDD)
- Minimal fix for root cause
- Preserve existing behavior
- Add explanatory comments

### Testing
- Run regression test for each fix
- Run full test suite after all fixes
- Manual verification using reproduction steps
- Test edge cases

### Committing
- Atomic commits (one logical fix)
- Descriptive commit messages
- Reference issue IDs
- Include verification steps

### PR Creation
- Comprehensive description
- Root cause for each issue
- Test coverage summary
- Manual verification steps

## Example Session

```
User: Fix these P0 issues from beta.1 testing:
- Issue #402: Telemetry prompt spam
- Issue #403: Telemetry can't be disabled
- Issue #404: JSON output invalid

Claude: [Invokes beta-feedback-fixer skill]

I'll systematically fix these P0 issues. Let me start by parsing the issues...

### Extracted Issues

**Issue #402**: Telemetry consent prompt (P0 - Bug)
- Expected: Prompt once, persist choice
- Actual: Prompts every command
- Related: #403 (same root cause)

**Issue #404**: JSON output invalid (P0 - Output)
- Expected: Valid JSON
- Actual: Prompt text in JSON output

### Root Cause Analysis

Issue #402/#403:
- File: src/main.rs:627-636
- Root cause: Empty TODO branches - consent never saved
- Fix: Add config_manager.save() call

Issue #404:
- File: src/main.rs:620
- Root cause: Prompt runs before checking output format
- Fix: Skip prompt when --output json/yaml

### Creating Worktree

Creating .worktrees/fix-beta-1-p0-issues...
Running baseline tests...
All tests pass ✅

### Implementation

[Writes regression test for #402]
[Implements fix in src/main.rs]
[Runs tests]
[Commits]

[Fixes #404]
[Commits]

### PR & Release Preparation

Creating PR #407...
Updating version to 1.1.0-beta.2...
Creating beta.2 testing instructions...

✅ Done! PR ready for review.
```

## References

- `references/issue-analysis.md` - Detailed RCA techniques
- `references/fix-workflow.md` - Step-by-step fix process
- `references/release-preparation.md` - Beta release procedures
- `templates/root-cause-template.md` - RCA documentation template
- `templates/regression-test.md` - Test code template
