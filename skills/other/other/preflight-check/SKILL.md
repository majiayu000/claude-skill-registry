---
name: preflight-check
version: "1.0.0"
description: |
  Validate environment configuration before work-issue execution to prevent mid-workflow interruptions.
  TRIGGER when: called by work-issue at Phase 0, or user manually runs preflight check.
  DO NOT TRIGGER when: user wants general project status (use /overview).
allowed-tools: Bash(git *), Bash(gh *), Bash(npm *), Bash(test *), Bash(mkdir *), Read, Write, Glob, Grep
disable-model-invocation: false
user-invocable: true
---

# Preflight Check - Pre-execution Environment Validator for work-issue

Validate environment configuration before work-issue execution to prevent mid-workflow interruptions.

## Overview

This skill performs comprehensive environment checks before work-issue begins, automatically fixing common issues to ensure smooth execution.

**What it does:**
1. **Permission configuration check** - Validates .claude/settings.json permissions
2. **Framework configuration check** - Ensures .claude/, .prot/ directories exist
3. **Git environment check** - Verifies Git repository, branch status, clean working directory
4. **GitHub environment check** - Confirms gh CLI installation and authentication
5. **Project structure check** - Validates package.json, src/, .gitignore
6. **Dependency tools check** - Checks Node.js, npm, node_modules
7. **Quality tools check** - Verifies test and lint scripts
8. **Auto-fix mechanism** - Automatically resolves common issues
9. **Parallel execution** - Optimized for 2-5 second completion

**Why it's needed:**
work-issue frequently fails mid-execution due to:
- Missing permissions (git push, gh pr create)
- Unconfigured framework directories
- Dirty working directory
- Missing dependencies (node_modules)
- Unauthenticated gh CLI

This skill catches and fixes these issues BEFORE work-issue starts, preventing 30-60 minute workflow interruptions.

**When to use:**
- Automatically called by work-issue at Phase 0 (before /start-issue)
- Manually: `/preflight-check` to validate environment
- After fresh project clone
- Before batch processing multiple issues

## Arguments

```bash
/preflight-check [options]
```

**Options:**
- `--fix` - Enable auto-fix mode (default: true)
- `--no-fix` - Report issues without fixing
- `--strict` - Fail on warnings (not just errors)
- `--category <category>` - Check specific category only

**Categories:**
- `permissions` - Permission configuration
- `framework` - Framework directories
- `git` - Git environment
- `github` - GitHub CLI
- `project` - Project structure
- `dependencies` - Node.js and npm
- `quality` - Test and lint tools

## AI Execution Instructions

**CRITICAL: Parallel execution and auto-fix priority**

When executing `/preflight-check`, AI MUST follow this pattern:

### Step 1: Create Check Tasks

```python
categories = [
    "permissions", "framework", "git", "github",
    "project", "dependencies", "quality"
]

for category in categories:
    TaskCreate(
        subject=f"Check {category}",
        description=f"Validate {category} configuration",
        activeForm=f"Checking {category}..."
    )
```

### Step 2: Execute Checks in Parallel

```python
# Group independent checks for parallel execution
parallel_groups = [
    ["permissions", "framework", "git"],  # Group 1
    ["github", "project"],                # Group 2
    ["dependencies", "quality"]           # Group 3
]

for group in parallel_groups:
    # Execute group in parallel
    results = execute_parallel(group)
    collect_issues(results)
```

### Step 3: Apply Auto-Fixes

```python
# Priority 1: Fast auto-fix (no confirmation)
for issue in priority_1_issues:
    auto_fix(issue)  # mkdir, touch, git fetch

# Priority 2: Requires confirmation
for issue in priority_2_issues:
    if confirm_fix(issue):
        auto_fix(issue)  # configure-permissions, git stash, npm install

# Priority 3: Manual fix required
for issue in priority_3_issues:
    report_manual_fix(issue)  # gh auth login, git init
```

### Step 4: Generate Report

```python
report = {
    "success": [✅ checks that passed],
    "auto_fixed": [🔧 checks that were fixed],
    "blocked": [❌ checks that require manual fix],
    "warnings": [⚠️ non-critical issues]
}

print_report(report)
```

## Workflow Steps

Copy this checklist when executing:

```
Preflight Check Progress:
- [ ] Step 1: Check permissions configuration
- [ ] Step 2: Check framework directories
- [ ] Step 3: Check Git environment
- [ ] Step 4: Check GitHub CLI
- [ ] Step 5: Check project structure
- [ ] Step 6: Check dependencies
- [ ] Step 7: Check quality tools
- [ ] Step 8: Apply auto-fixes
- [ ] Step 9: Generate report
```

Execute these steps with parallel optimization.

### Step 1: Check Permissions Configuration (Priority 1)

**Checks:**
- `.claude/settings.json` exists
- `git push` permission configured
- `gh pr create` permission configured
- `gh pr merge` permission configured

**Auto-fix:**
```bash
if [ ! -f .claude/settings.json ] || missing_permissions; then
    /configure-permissions --safe
fi
```

**Priority:** ⭐⭐⭐⭐⭐ (Critical - blocks work-issue auto mode)

### Step 2: Check Framework Directories (Priority 2)

**Checks:**
- `.claude/` directory exists
- `.prot/` directory exists
- `.claude/plans/` directory exists
- `.claude/skills/` directory exists

**Auto-fix:**
```bash
mkdir -p .claude/plans/active .claude/plans/archive
mkdir -p .claude/skills
mkdir -p .prot/pillars
```

**Priority:** ⭐⭐⭐ (Important - framework dependencies)

### Step 3: Check Git Environment (Priority 1)

**Checks:**
- Current directory is Git repository
- On `main` or `master` branch
- Working directory clean (no uncommitted changes)
- Remote configured (origin)

**Auto-fix:**
```bash
# If dirty working directory
if [ -n "$(git status --short)" ]; then
    git stash push -m "Preflight auto-stash $(date +%Y-%m-%d-%H%M%S)"
fi

# If remote not configured
if ! git remote get-url origin; then
    # Cannot auto-fix - require manual setup
    echo "❌ Git remote 'origin' not configured"
fi
```

**Priority:** ⭐⭐⭐⭐ (Critical - blocks branch creation)

### Step 4: Check GitHub CLI (Priority 1)

**Checks:**
- `gh` CLI installed
- `gh` authenticated
- Can access repository

**Auto-fix:**
```bash
# Check authentication
if ! gh auth status 2>/dev/null; then
    echo "❌ GitHub CLI not authenticated"
    echo "Fix: gh auth login"
    exit 1  # Cannot auto-fix
fi
```

**Priority:** ⭐⭐⭐⭐ (Critical - blocks PR operations)

### Step 5: Check Project Structure (Priority 2)

**Checks:**
- `package.json` exists (warning if missing)
- `src/` directory exists
- `.gitignore` exists

**Auto-fix:**
```bash
# Create .gitignore if missing
if [ ! -f .gitignore ]; then
    cat > .gitignore <<EOF
node_modules/
.DS_Store
*.log
.env
EOF
fi
```

**Priority:** ⭐⭐⭐ (Important - project conventions)

### Step 6: Check Dependencies (Priority 2)

**Checks:**
- Node.js installed
- npm installed
- `node_modules/` exists and up-to-date

**Auto-fix:**
```bash
# If node_modules missing or stale
if [ ! -d node_modules ] || package.json newer than node_modules; then
    echo "🔧 Running npm install..."
    npm install
fi
```

**Priority:** ⭐⭐⭐ (Important - blocks code execution)

### Step 7: Check Quality Tools (Priority 3)

**Checks:**
- `npm test` script exists (warning only)
- `npm run lint` script exists (warning only)

**Auto-fix:**
None - warnings only

**Priority:** ⭐ (Nice to have)

### Step 8: Apply Auto-Fixes

**Priority levels:**

| Priority | Description | Examples | Requires Confirmation |
|----------|-------------|----------|----------------------|
| **P1 - Fast** | Instant, safe fixes | mkdir, touch, git fetch | ❌ No |
| **P2 - Slow** | Time-consuming but safe | configure-permissions, git stash, npm install | ✅ Yes |
| **P3 - Manual** | Cannot auto-fix | gh auth login, git init, install Node.js | N/A |

**Implementation:**
```python
def apply_auto_fixes(issues, auto_fix_enabled):
    fixed = []
    blocked = []

    for issue in issues:
        if issue.priority == "P1":
            # Fast auto-fix - no confirmation
            fix_result = auto_fix(issue)
            fixed.append((issue, fix_result))

        elif issue.priority == "P2" and auto_fix_enabled:
            # Slow auto-fix - confirm first
            print(f"🔧 Auto-fix available: {issue.description}")
            print(f"   Command: {issue.fix_command}")
            print(f"   Estimated time: {issue.fix_duration}")

            if confirm("Apply fix? [Y/n]"):
                fix_result = auto_fix(issue)
                fixed.append((issue, fix_result))
            else:
                blocked.append(issue)

        elif issue.priority == "P3":
            # Manual fix required
            blocked.append(issue)

    return fixed, blocked
```

### Step 9: Generate Report

**Report format:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preflight Check Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed (5/7):
  ✅ Permissions configured
  ✅ Framework directories exist
  ✅ Git repository valid
  ✅ GitHub CLI authenticated
  ✅ Project structure valid

🔧 Auto-Fixed (2/7):
  🔧 Git working directory stashed
  🔧 Dependencies installed (npm install, 45s)

❌ Blocked (0/7):
  (none)

⚠️ Warnings (2):
  ⚠️ npm test script not found (recommended)
  ⚠️ npm run lint script not found (recommended)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: ✅ READY
Time: 3.2s (parallel execution)

Proceed with: /work-issue [issue-number]
```

**If blocked:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: ❌ BLOCKED

Fix required:
  ❌ GitHub CLI not authenticated
     Fix: gh auth login

Re-run after fixing: /preflight-check
```

## Error Handling

**Cannot auto-fix:**
```
❌ Preflight Check Failed

Category: GitHub CLI
Issue: Not authenticated
Fix: gh auth login

After fixing, re-run: /preflight-check
```

**Auto-fix failed:**
```
⚠️ Auto-fix attempt failed

Category: Dependencies
Issue: npm install failed
Error: ENOENT: package.json not found

Manual fix required. Check project structure.
```

**Partial success:**
```
⚠️ Preflight Check Completed with Warnings

✅ 5/7 checks passed
🔧 2/7 auto-fixed
⚠️ 2 warnings (non-blocking)

Status: READY (proceed with caution)
```

## Integration with work-issue

**work-issue workflow:**
```
Phase 0: /preflight-check (NEW - this skill)
  ├─ If ✅ READY → Continue
  ├─ If ❌ BLOCKED → Stop, show fix commands
  └─ If ⚠️ WARNINGS → Warn user, optionally continue

Phase 1: /start-issue
Phase 1.5: /eval-plan
Phase 2: /execute-plan
Phase 2.5: /review
Phase 3: /finish-issue
```

**Updated work-issue SKILL.md integration:**
```markdown
## Workflow Steps

### Phase 0: Preflight Check (NEW)

**Execute**: `/preflight-check`

**Validates:**
- Permissions configured
- Framework directories exist
- Git environment clean
- GitHub CLI authenticated
- Dependencies installed

**Output**: ✅ READY or ❌ BLOCKED

**Time**: 2-5 seconds

**If blocked**: Fix issues and re-run
```

## Performance

| Check Category | Time (Serial) | Time (Parallel) | Savings |
|----------------|---------------|-----------------|---------|
| Permissions | 0.5s | 0.5s | - |
| Framework | 0.3s | 0.3s | - |
| Git | 1.2s | 0.5s | 0.7s |
| GitHub | 1.5s | 1.5s | - |
| Project | 0.4s | 0.4s | - |
| Dependencies | 0.8s | 0.8s | - |
| Quality | 0.5s | 0.5s | - |
| **Total** | **8-10s** | **3-5s** | **50% faster** |

**Optimization strategy:**
- Group 1 (Parallel): Permissions, Framework, Git
- Group 2 (Parallel): GitHub, Project
- Group 3 (Parallel): Dependencies, Quality
- Apply auto-fixes sequentially (safety)

## Examples

### Example 1: Clean Environment

```bash
/preflight-check

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preflight Check Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All checks passed (7/7)

Status: ✅ READY
Time: 2.8s

Proceed with: /work-issue [issue-number]
```

### Example 2: First-Time Setup (Auto-Fix)

```bash
/preflight-check

Checking environment...

🔧 Auto-fixing issues:
  🔧 Permissions not configured → Running /configure-permissions --safe (2s)
  🔧 .claude/plans/ missing → Creating directories (0.1s)
  🔧 node_modules missing → Running npm install (45s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preflight Check Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed (4/7)
🔧 Auto-Fixed (3/7):
  🔧 Permissions configured
  🔧 Framework directories created
  🔧 Dependencies installed

Status: ✅ READY
Time: 49s (including auto-fixes)

Proceed with: /work-issue [issue-number]
```

### Example 3: Blocked State

```bash
/preflight-check

Checking environment...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preflight Check Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed (5/7)
❌ Blocked (2/7):
  ❌ GitHub CLI not authenticated
     Fix: gh auth login

  ❌ Git remote 'origin' not configured
     Fix: git remote add origin <url>

Status: ❌ BLOCKED
Time: 3.1s

Fix issues above and re-run: /preflight-check
```

### Example 4: Category-Specific Check

```bash
/preflight-check --category git

Checking Git environment...

✅ Git Environment Check

  ✅ Git repository: /Users/woo/dev/ai-dev
  ✅ Current branch: main
  ✅ Working directory: clean
  ✅ Remote configured: origin (https://github.com/aifuun/ai-dev.git)

Status: ✅ READY
Time: 0.5s
```

## Best Practices

1. **Run before batch processing** - Ensures all issues can execute smoothly
2. **Enable auto-fix** - Saves time by resolving common issues automatically
3. **Fix blocked issues immediately** - Don't ignore ❌ blocked checks
4. **Heed warnings** - ⚠️ warnings indicate missing best practices
5. **Re-run after fixes** - Verify fixes resolved the issues

## Related Skills

- **/configure-permissions** - Called by this skill to fix permission issues
- **/work-issue** - Calls this skill at Phase 0
- **/overview** - Shows comprehensive project status

---

**Version:** 1.0.0
**Last Updated:** 2026-03-18
**Changelog:**
- v1.0.0 (2026-03-18): Initial release - pre-execution environment validator (Issue #246)

**Pattern:** Validation skill (pre-execution checks)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
