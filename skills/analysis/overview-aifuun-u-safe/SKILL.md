---
name: overview
description: |
  Display comprehensive project overview including git state, framework configuration, active work, and code quality metrics.
  TRIGGER when: user wants to see project overview ("show overview", "project overview", "current state", "what's the status").
version: "3.0.0"
  DO NOT TRIGGER when: user wants git-specific info only (use git commands), or wants to create/modify (not viewing overview).
---

# Overview - Project Status and Health Check

Display comprehensive project status combining git state, framework analysis, active work, and code quality metrics.

## Overview

This skill provides a complete snapshot of your project's current state:

**What it does:**
1. Shows git status (branch, commits, changes)
2. Analyzes framework configuration (profile, Pillars, rules)
3. Lists active work (plans, open issues)
4. Detects code patterns (nominal types, airlock, saga, etc.)
5. Calculates health score (0-100)
6. Generates both terminal output and HTML report

**Why it's needed:**
Get a quick understanding of project state without running multiple commands. Useful when starting work, before PRs, or for project health checks.

**When to use:**
- Starting a work session
- Before creating a PR
- Project health check
- Team status updates

## Workflow

### Step 1: Create Todo List

**Initialize overview collection tracking**:

```
Task #1: Collect git state
Task #2: Analyze framework configuration (blocked by #1)
Task #3: List active work (blocked by #1)
Task #4: Detect code patterns (blocked by #1)
Task #5: Generate terminal output (blocked by #2-4)
Task #6: Generate HTML report (blocked by #5)
```

After creating tasks, proceed with overview collection.

## Status Dimensions

### 1. Git State

Current git information:
```
- Branch name
- Latest commit (hash + message)
- Staged changes count
- Unstaged changes count
- Untracked files count
- Recent commit history (last 10)
```

### 2. Framework Configuration

Framework setup and components:
```
- Profile (minimal/node-lambda/react-aws/custom)
- Enabled Pillars count and list
- Rules count (by category)
- Commands count
- Installation date
```

### 3. Active Work

Current work in progress:
```
- Active plans (in .claude/plans/active/)
- Open GitHub issues (if gh CLI available)
- Current branch type (feature/fix/hotfix)
```

### 4. Code Quality

Pattern detection and quality metrics:
```
Patterns detected:
- Nominal types (branded IDs)
- Airlock validation (schema guards)
- Saga patterns (transaction compensation)
- Headless UI (logic separation)
- Test coverage

Health Score (0-100):
- Framework installed: +20
- Has tests: +20
- Uses nominal types: +15
- Uses airlock: +15
- Has active plans: +10
- Clean git status: +10
- Documentation exists: +10
```

### 5. Recent History

Recent development activity:
```
- Last 10 commits with timestamps
- Commit messages and authors
- Development velocity indicators
```

## Output Formats

### Terminal Output (Default)

Quick text overview displayed in terminal:

```markdown
# 📊 Project Status - ai-dev

## 🔀 Git
**Branch**: feature/60-create-status-skill
**Commit**: c73f08c - "feat: create review skill"
**Status**: 2 staged, 0 unstaged, 1 untracked

## ⚙️ Framework
**Profile**: react-aws
**Pillars**: 7 enabled (A, B, K, L, M, Q, R)
**Health Score**: 85/100

## 📋 Active Work
**Plans**: 2 active
- issue-60-plan.md
- issue-60-execution-plan.md

**Issues**: 1 open
- #60: Create status skill

## 📈 Recent Commits (Last 5)
- c73f08c feat: create review skill (2 hours ago)
- e8ce836 feat: rebuild start-issue skill (4 hours ago)
- 8dffaf8 feat: rebuild finish-issue skill (1 day ago)

## ✨ Code Quality
**Patterns**: nominal-types, testing
**Health**: 85/100 (Good)
**Recommendations**:
- [Low] Commit staged changes

---

📄 Full report: docs/reports/ai-dev-status-2026-03-05T17-53-00.html
```

### HTML Report (Optional)

Full 5-tab HTML report saved to `docs/reports/`:

**Tab 1 - Overview**: Quick stats and summary
**Tab 2 - Status**: Git state and active work
**Tab 3 - Architecture**: Framework configuration
**Tab 4 - Quality**: Health score and patterns
**Tab 5 - History**: Recent commits timeline

## Usage

**Default (terminal output)**:
```bash
/overview
# or directly: ./script/overview.py
```

**HTML report**:
```bash
/overview --format=html
# or: ./script/overview.py --format=html
```

**JSON output**:
```bash
/overview --format=json
# or: ./script/overview.py --format=json
```

**Save to file**:
```bash
./script/overview.py --format=json --output=status.json
./script/overview.py --format=html --output=report.html
```

**Generate HTML without opening**:
```bash
./script/overview.py --format=html --no-open
```

## Flags

- `--format=terminal|html|json` - Output format (default: terminal)
- `--output=FILE` - Save output to file (optional)
- `--no-open` - Don't auto-open HTML reports in browser
- `--project-root=DIR` - Specify project root (default: current directory)

## Integration

**With other skills**:
```
/overview        # Check current state
/review          # Review code quality
/finish-issue    # Complete current work
```

**In workflows**:
```
# Morning routine
/overview        # See what's in progress
/next            # Get next task

# Before PR
/overview        # Health check
/review          # Code review
/finish-issue    # Create PR
```

## Health Score Details

Calculated from multiple factors:

| Factor | Points | Check |
|--------|--------|-------|
| Framework installed | 20 | .framework-install exists |
| Test files present | 20 | Has *.test.* or *.spec.* files |
| Nominal types used | 15 | Finds branded type patterns |
| Airlock validation | 15 | Finds schema validation |
| Active plans | 10 | Has files in .claude/plans/active/ |
| Clean git status | 10 | No uncommitted changes |
| Documentation | 10 | README.md exists and > 100 lines |

**Score ranges**:
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- 0-59: Needs improvement

## Error Handling

Gracefully handles missing tools:
- No git → Shows "Git not available"
- No gh CLI → Skips issues section
- Framework not installed → Shows "Not installed"
- Write permission error → Clear error message

## Examples

### Example 1: Quick Overview Check

**User says:**
> "show me the current status"

**Output:**
Terminal display with git state, framework info, active work, and health score.

### Example 2: Generate Report for Team

**User says:**
> "generate an overview report in HTML"

**Output:**
HTML file created in docs/reports/ with full 5-tab report, opened in browser.

### Example 3: Fast Terminal Check

**User says:**
> "quick overview, no HTML"

**Output:**
Terminal-only output, skips HTML generation for speed.

## Output Location

HTML reports saved to:
```
docs/reports/<project-name>-overview-<timestamp>.html
```

Example: `docs/reports/ai-dev-overview-2026-03-07T19-53-00.html`

## Best Practices

1. **Run at session start** - Know what's in progress
2. **Before PRs** - Health check before finishing
3. **After pulling main** - See what changed
4. **For team updates** - Generate HTML report
5. **Regular health checks** - Track project quality

## Task Management

**After each step**, update task progress:

```
Git state collected → Update Task #1
Framework analyzed → Update Task #2
Active work listed → Update Task #3
Patterns detected → Update Task #4
Terminal output displayed → Update Task #5
HTML report generated → Update Task #6
```

### Task #5: Generate Terminal Output

Display collected status information in terminal format with health score and recommendations.

### Task #6: Generate HTML Report

**Execute the Python overview script:**

```bash
.claude/skills/overview/script/overview.py --format=html
```

This will:
1. Collect all overview data using Python collectors (Phase 3, ADR-003)
2. Calculate health score using Python health calculator (Phase 4, ADR-003)
3. Generate comprehensive HTML report using Python formatter (Phase 4, ADR-003)
4. Save to `docs/reports/<project-name>-overview-<timestamp>.html`

**Available options:**
- `--format=terminal|html|json` - Output format (default: terminal)
- `--output=FILE` - Save to specific file
- `--no-open` - Generate HTML but don't open browser
- `--help` - Show usage information

**Note:** Fully migrated to Python per ADR-003 (Phases 3-4 complete). All data collection, health calculation, and formatting use Python modules with type hints and comprehensive docstrings.

Provides visibility into status collection progress.

## Final Verification

**Before declaring overview complete**, verify:

```
- [ ] All 6 tasks completed
- [ ] Git state retrieved (Task #1)
- [ ] Framework config detected (Task #2)
- [ ] Active work listed (Task #3)
- [ ] Code patterns detected (Task #4)
- [ ] Terminal output displayed (Task #5)
- [ ] HTML report generated (Task #6)
```

**HTML report check:**
```bash
ls -lh docs/reports/*.html | tail -1
```

Missing items indicate incomplete overview collection.

## Related Skills

- **/start-issue** - Begin work on issue
- **/finish-issue** - Complete and close issue
- **/review** - Code quality review
- **/next** - Get next task from plan

---

**Version:** 3.0.0
**Last Updated:** 2026-03-10
**Changelog:**
- v3.0.0 (2026-03-10): Comprehensive project status and health check
**Pattern:** Tool-Reference (displays status information)
**Compliance:**
- ADR-001 Section 4 ✅ (Official skill patterns)
- ADR-003 ✅ (Python-only policy - Phases 3-4 complete)
