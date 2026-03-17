---
name: quality-engineer-manager
description: Quality Engineer Manager skill for orchestrating release validation, beta testing coordination, feedback analysis, and release sign-off decisions
---

# Quality Engineer Manager Skill

## What This Skill Does

This skill encapsulates the **Quality Engineering Manager** role, responsible for:
- **Release Validation**: Monitor CI/CD pipelines and verify release artifacts
- **Beta Testing Coordination**: Dispatch beta testers, collect feedback, analyze results
- **Issue Triage**: Root cause analysis, prioritization, and development dispatch
- **Knowledge Management**: Document learnings to prevent regressions
- **Release Sign-Off**: Final decision to ship, hotfix, or abort

**Key Principle**: Every release goes through systematic validation before being approved for users.

## When to Use This Skill

Activate this skill when the user:
- Requests a release sign-off (e.g., "test v1.0.4", "validate the release")
- Wants to coordinate beta testing for a release
- Needs to analyze beta tester feedback and prioritize fixes
- Asks for release quality assessment
- Wants to document known issues and resolutions

**Example Triggers:**
- "Test the v1.0.4 release"
- "Coordinate beta testing for this release"
- "Analyze the beta feedback and create a fix plan"
- "Sign off on the release" or "Is this release ready?"
- "Create a hotfix plan based on beta testing"

## Core Workflow

### Phase 1: Release Validation (CI/CD)

When a release is triggered, systematically validate:

1. **Monitor Publish Workflow**
   ```bash
   gh run list --workflow=publish.yml --limit 1
   gh run watch <run-id>
   ```

2. **Monitor Release Workflow**
   ```bash
   gh run list --workflow=release.yml --limit 1
   gh run watch <run-id>
   ```

3. **Identify Failures**
   - Check workflow logs: `gh run view <run-id> --log-failed`
   - Categorize failure type: formatting, linting, tests, build, packaging
   - Extract error messages and stack traces

4. **Root Cause Analysis**
   - Read relevant source files
   - Check recent changes: `git log --oneline -10`
   - Compare with known issues database
   - Determine if issue is new or regression

5. **Fix & Re-trigger**
   - Apply fix
   - Commit with clear message
   - Update git tag: `git tag -f -a vX.Y.Z -m "Release vX.Y.Z" && git push -f origin vX.Y.Z`
   - Monitor new workflow run

6. **Verify Artifacts**
   ```bash
   # Verify crates.io publication
   curl -s https://crates.io/api/v1/crates/caro/X.Y.Z | jq -r '.version.num'

   # Verify GitHub release assets
   gh release view vX.Y.Z --json assets -q '.assets[] | .name'
   ```

### Phase 2: Beta Testing Coordination

After release artifacts are available:

1. **Dispatch Beta Testers**
   - Use the `unbiased-beta-tester` skill with different profiles
   - Test critical user journeys:
     - Fresh installation (no Rust, no cargo)
     - Cargo installation (with Rust)
     - First-run experience (model download)
     - Basic command generation
     - Error handling and recovery

2. **Collect Feedback**
   - Capture all tester outputs
   - Document friction points
   - Note unexpected behaviors
   - Record success/failure for each journey

3. **Analyze Results**
   - Categorize issues by severity:
     - **P0 (Critical)**: Blocks primary use case
     - **P1 (High)**: Breaks common workflow
     - **P2 (Medium)**: Degrades experience
     - **P3 (Low)**: Minor polish issue
   - Identify patterns across testers
   - Check against known issues database

#### Bundle Validation (Optional)

For releases with model bundles, use the systematic bundle validation command:

```bash
# Minimal validation (3 profiles, 2 bundles)
/qa-bundle-validation version=vX.Y.Z profiles=minimal bundles=sample

# Standard validation (5 original profiles)
/qa-bundle-validation version=vX.Y.Z profiles=original bundles=all

# Comprehensive validation (all 10 profiles)
/qa-bundle-validation version=vX.Y.Z profiles=all bundles=all
```

**When to Use Bundle Validation:**
- After Phase 6 (Model Bundling) completes
- When bundles are critical for user experience
- For minor/major version releases
- When bundle structure has changed

**Bundle Validation Process:**
1. Verifies all bundle assets exist on GitHub release
2. Dispatches selected beta testers with specific bundles
3. Tests offline installation and model loading
4. Validates license compliance
5. Collects structured results
6. Generates bundle-specific QA sign-off report

**Output:**
- Coverage matrix showing which bundles were tested
- Issue breakdown by severity
- Bundle-specific sign-off decision
- Documentation updates for known issues

See `.claude/commands/qa-bundle-validation.md` for complete workflow details.

### Phase 3: Issue Triage & Development Dispatch

For each identified issue:

1. **Triage Decision**
   - **Hotfix Required**: P0 issue, blocks release → initiate hotfix workflow
   - **Schedule for Next Release**: P1-P2, workaround exists
   - **Backlog**: P3, polish item
   - **Won't Fix**: Edge case, not worth effort

2. **Create Development Tasks**
   - File GitHub issues with:
     - Clear reproduction steps
     - Expected vs actual behavior
     - Priority label
     - Milestone assignment
   - Link related issues
   - Reference known issue documentation

3. **Dispatch Work**
   - For hotfixes: create worktree and implement immediately
   - For scheduled fixes: add to milestone backlog
   - Document in known issues for regression prevention

### Phase 4: Knowledge Management

**CRITICAL**: Document learnings to prevent regressions.

1. **Update Known Issues Database**
   - See `references/known-issues.md` template
   - For each resolved issue, document:
     - Symptoms
     - Root cause
     - Resolution
     - Prevention strategy

2. **Update Beta Tester Profiles**
   - Add new test scenarios based on found issues
   - Update environment configurations that caused problems
   - Enhance validation scripts

3. **Update CI/CD Documentation**
   - Document new failure modes
   - Add troubleshooting steps
   - Update runbooks

### Phase 5: Release Sign-Off

Final decision matrix:

| Condition | Decision | Action |
|-----------|----------|--------|
| No P0/P1 issues, all critical paths working | **✅ SHIP IT** | Announce release, close milestone |
| P0 issue found, quick fix available | **🔧 HOTFIX** | Trigger hotfix workflow, re-test |
| P0 issue found, complex fix needed | **❌ ABORT** | Revert tag, create fix milestone |
| Multiple P1 issues | **⚠️ CONDITIONAL** | Assess workarounds, user impact |

**Sign-Off Checklist:**
- [ ] Publish workflow succeeded (crates.io verification)
- [ ] Release workflow succeeded (all platform binaries)
- [ ] At least 2 beta tester profiles tested successfully
- [ ] No P0 issues discovered
- [ ] Known issues documented
- [ ] CHANGELOG updated
- [ ] Release notes reviewed

### Phase 6: Model Bundling (Post-Release)

**IMPORTANT**: Model bundling runs AFTER release sign-off, as a separate workflow.

#### When to Trigger Bundling

Only trigger model bundling when:
1. Release has been signed off (✅ SHIP IT decision)
2. All platform binaries are available on GitHub release
3. No P0/P1 issues blocking the release

#### Bundling Workflow

The `bundle.yml` workflow creates 10 bundles (5 platforms × 2 models):
- Platforms: linux-amd64, linux-arm64, macos-intel, macos-silicon, windows-amd64
- Models: Qwen 1.5B (~1.1GB), SmolLM 135M (~145MB)

**Trigger Command:**
```bash
# From GitHub UI (recommended until workflow is indexed):
# https://github.com/wildcard/caro/actions/workflows/bundle.yml
# Click "Run workflow", enter version (e.g., v1.0.4)

# Or via CLI (after workflow is indexed):
gh workflow run bundle.yml -f version=v1.0.4 -f skip_verification=false
```

**What the Workflow Does:**
1. Verifies release exists on GitHub
2. Downloads pre-built binaries from release (5 platforms)
3. Downloads models from HuggingFace using `hf` CLI
4. Creates license files and THIRD_PARTY_NOTICES.txt (Apache 2.0 compliance)
5. Bundles: binary + model + licenses into tar.gz
6. Uploads 10 bundles to the GitHub release

**Expected Artifacts:**
```
caro-VERSION-PLATFORM-with-MODEL.tar.gz
caro-VERSION-PLATFORM-with-MODEL.tar.gz.sha256
```

**Bundling Validation Checklist:**
- [ ] All 10 bundles created successfully
- [ ] Each bundle includes: binary, models/, licenses/, THIRD_PARTY_NOTICES.txt
- [ ] Bundle sizes correct (~1.1GB for Qwen, ~150MB for SmolLM)
- [ ] SHA256 checksums generated
- [ ] Bundles uploaded to GitHub release

**If Bundling Fails:**
- Check HuggingFace token (CARO_BUNDLE_HF_TOKEN secret)
- Verify binary names match release artifacts
- Check workflow logs for model download failures
- Non-critical: Can defer to next release if needed

## CI/CD Troubleshooting Reference

When debugging CI/CD failures, consult these common patterns from known issues:

### GitHub Actions YAML Gotchas

**Issue #7: Heredoc Syntax Incompatibility**
- **Problem**: YAML `run: |` blocks conflict with shell heredoc (`<<EOF`) syntax
- **Symptoms**: "Mapping values are not allowed in this context" parse error
- **Solution**: Use `printf '%s\n'` instead of heredocs for multi-line file creation
- **Prevention**: Never use heredocs (`<<EOF`, `<<'EOF'`, `<<-EOF`) in GitHub Actions `run: |` blocks

```yaml
# Bad - causes YAML parse error
- run: |
    cat <<EOF > file.txt
    Line 1: content
    EOF

# Good - use printf instead
- run: |
    printf '%s\n' \
      "Line 1: content" \
      > file.txt
```

**Issue #8: Alpine Containers Lack Tools**
- **Problem**: Alpine Linux minimal images don't include gh CLI, curl, etc.
- **Symptoms**: `gh: command not found` or `curl: not found`
- **Solution**: Manually install tools from official sources
- **Prevention**: Always verify tool availability in container images before use

```yaml
- name: Install dependencies
  run: |
    apk add --no-cache curl tar gzip bash
    # Install gh CLI for Alpine
    curl -fsSL https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_linux_amd64.tar.gz -o gh.tar.gz
    tar -xzf gh.tar.gz
    mv gh_2.63.2_linux_amd64/bin/gh /usr/local/bin/
```

**Issue #9: GitHub Permissions Too Restrictive**
- **Problem**: Default GITHUB_TOKEN is read-only, release uploads fail
- **Symptoms**: `HTTP 403: Resource not accessible by integration`
- **Solution**: Add explicit `contents: write` permission at workflow level
- **Prevention**: Always audit required permissions before adding new workflow functionality

```yaml
name: Bundle Models

on:
  workflow_dispatch:
    # ...

permissions:
  contents: write  # Required for gh release upload

jobs:
  bundle:
    runs-on: ubuntu-latest
    # ...
```

### Quick Debugging Commands

```bash
# View failed workflow logs
gh run list --workflow=<workflow-name> --limit 1
gh run view <run-id> --log-failed

# Re-run failed jobs only
gh run rerun <run-id> --failed

# Validate workflow YAML syntax locally
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/bundle.yml'))"

# Check release assets
gh release view vX.Y.Z --json assets -q '.assets[] | .name'

# Verify crates.io publication
curl -s https://crates.io/api/v1/crates/caro/X.Y.Z | jq -r '.version.num'
```

### When to Consult Known Issues Database

Before debugging any CI/CD failure:
1. Check `references/known-issues.md` for similar symptoms
2. Look for issue numbers mentioned in error logs
3. Review prevention strategies from resolved issues
4. Update database with any new issues discovered

### Debugging Decision Tree

```
CI/CD Failure Detected
    |
    ├─> YAML syntax error? → See Issue #7 (heredoc)
    ├─> Tool not found? → See Issue #8 (Alpine containers)
    ├─> Permission denied? → See Issue #9 (GITHUB_TOKEN)
    ├─> Test failure? → See known-issues.md for test-specific issues
    └─> Unknown? → Check workflow logs, consult known-issues.md
```

## Today's Successful Process (v1.0.4 Example)

Here's what we did to successfully release v1.0.4:

### Issue 1: Formatting Errors
```
Symptom: cargo fmt check failed in publish workflow
Root Cause: Code not formatted with rustfmt
Fix: cargo fmt --all && git commit
Prevention: Pre-commit hook for rustfmt
```

### Issue 2: Clippy Warnings
```
Symptom: clippy --deny warnings failed
Issues Found:
  - Unused import (Context in doctor.rs)
  - .last() should be .next_back() for DoubleEndedIterator
  - match should use matches! macro
  - Unnecessary u64 cast

Fix: Applied all clippy suggestions
Prevention: Run clippy in development, add to pre-push hook
```

### Issue 3: Dead Code Warnings
```
Symptom: Fields in ValidationResult struct never read
Root Cause: Debug/troubleshooting fields in test struct
Fix: Added #[allow(dead_code)] to unused fields
Prevention: Use #[allow(dead_code)] for intentional debug fields
```

### Issue 4: Flaky Test (test_shell_detector_uses_env_variable)
```
Symptom: Test failed expecting Bash but got Zsh
Root Cause: Test logic didn't mirror actual detection logic
Fix: Updated test to mirror exact ShellType::detect() logic
Prevention: Ensure tests mirror implementation, not assumptions
```

### Issue 5: Model Bundling Failures (Non-Critical)
```
Symptom: Python pip install failed on macOS, HF auth on Linux
Root Cause: CI environment Python version mismatch, missing HF token
Impact: Model bundles not created (but not critical - users can download)
Decision: Ship anyway - users download models automatically on first use
Future Fix: Add HF token to GitHub secrets, use system Python
```

### Final Sign-Off Decision
```
✅ SHIP v1.0.4
Rationale:
- All critical binaries published
- Package on crates.io verified
- Model bundling failure is non-critical (workaround exists)
- No P0/P1 issues blocking primary use cases
```

## Integration with Beta Tester Skill

The QE Manager dispatches beta testers like this:

```bash
# Invoke beta tester skill with specific profile
/unbiased-beta-tester profile=terminal-novice os=macos test=first-run
```

Then collect results and analyze:
- Did installation succeed?
- Did first command work?
- Were error messages helpful?
- Did user hit any dead ends?

## References

- **Known Issues Database**: `references/known-issues.md` - Historical issues and resolutions
- **Release Runbook**: `references/release-runbook.md` - Step-by-step release process
- **Hotfix Workflow**: `references/hotfix-workflow.md` - Emergency fix procedures
- **Beta Testing Playbook**: `references/beta-testing-playbook.md` - Testing scenarios

## Example Usage

### Example 1: Release Sign-Off Request

**User:** "Test the v1.0.4 release and sign off if ready"

**QE Manager Response:**
```
# Quality Engineering Sign-Off: v1.0.4

## Phase 1: CI/CD Validation

Checking publish workflow...
✅ Published to crates.io (verified: 1.0.4)

Checking release workflow...
✅ All platform binaries uploaded:
   - Linux (amd64, arm64)
   - macOS (Intel, Silicon)
   - Windows (amd64)

⚠️ Model bundling partially failed (non-critical)

## Phase 2: Beta Testing

Dispatching beta testers with 3 profiles...
[Runs beta tester skill for each profile]

Results:
- Terminal Novice (macOS): ✅ Success
- Power User (Linux): ✅ Success
- Corporate Locked-Down: ⚠️ Proxy issues (P2)

## Phase 3: Issue Analysis

P0 Issues: None
P1 Issues: None
P2 Issues: 1 (proxy configuration documentation)
P3 Issues: 2 (polish items)

## Phase 4: Sign-Off Decision

✅ **APPROVED FOR RELEASE**

Rationale:
- All critical paths validated
- No blockers for primary use cases
- P2 issue has workaround (manual proxy config)
- Documentation improvements can follow in v1.0.5

Next Steps:
- Update known issues with proxy configuration guidance
- Schedule P2/P3 fixes for v1.0.5 milestone
```

### Example 2: Hotfix Required

**User:** "Beta testing found a crash on Windows"

**QE Manager Response:**
```
# Hotfix Assessment: Windows Crash

## Severity: P0 (Critical)
- Affects: All Windows users
- Impact: Application crashes on startup
- Workaround: None

## Root Cause Analysis
[Investigates using logs, reproduces locally]

Identified: Missing DLL dependency in Windows build

## Hotfix Decision: ✅ REQUIRED

Creating hotfix plan:
1. Create hotfix branch from v1.0.4 tag
2. Add Windows DLL to release artifacts
3. Test on Windows environments
4. Release as v1.0.5 within 24h

## Development Dispatch
Creating GitHub issue #XXX: [HOTFIX] Windows crash - missing DLL
Assigning to: Immediate action required
Milestone: v1.0.5 (hotfix)

[Proceeds to coordinate hotfix implementation]
```

## Best Practices

### For Release Validation
1. Always verify artifacts, don't assume success from green checkmark
2. Test install from published package, not local build
3. Check multiple platforms when possible
4. Document non-critical failures and their impact

### For Beta Testing
1. Use diverse tester profiles (novice, expert, restricted environment)
2. Test the actual release artifacts, not development builds
3. Focus on critical user journeys first
4. Document every friction point, even if not a "bug"

### For Issue Triage
1. Prioritize based on user impact, not implementation difficulty
2. Always assess workarounds before declaring "blocker"
3. Group related issues to avoid fix fragmentation
4. Consider rollback as a valid option for severe issues

### For Knowledge Management
1. Document resolutions immediately while context is fresh
2. Link issues to commits that fixed them
3. Update prevention strategies based on root causes
4. Share learnings across team (update skills, docs, CI)

## Remember

**The QE Manager's job is to protect users from broken releases while enabling fast iteration.**

- Be thorough but pragmatic
- Perfect is the enemy of shipped
- Every issue is a learning opportunity
- Prevention is better than detection
- Clear documentation saves future debugging time
