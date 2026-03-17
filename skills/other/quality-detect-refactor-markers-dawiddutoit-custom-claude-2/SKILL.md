---
name: quality-detect-refactor-markers
description: |
  Finds all REFACTOR markers in codebase, validates associated ADRs exist, identifies stale markers
  (30+ days old), and detects orphaned markers (no ADR reference). Use during status checks, before
  feature completion, or for refactor health audits. Triggers on "check refactor status", "marker
  health", "what's the status", or PROACTIVELY before marking features complete. Works with
  Python (.py), TypeScript (.ts), and JavaScript (.js) files using grep patterns to locate markers
  and validate against ADR files in docs/adr/ directories.
allowed-tools:
  - Bash
  - Grep
  - Read
  - Glob
  - mcp__memory__search_memories
---

# detect-refactor-markers

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**Validation Flow** → [Find Markers](#step-1-find-all-refactor-markers) | [Validate ADRs](#step-3-validate-associated-adrs) | [Health Report](#step-5-generate-health-report)

**Help** → [Troubleshooting](#troubleshooting) | [Anti-Patterns](#anti-patterns) | [Best Practices](#best-practices)

**Reference** → [Health Categories](./references/health-categories-guide.md) | [Remediation Guide](./references/remediation-guide.md)

## Purpose

Monitors refactor health by detecting all active REFACTOR markers in the codebase, validating their associated ADRs exist, and identifying issues such as stale markers (>30 days old), orphaned markers (missing ADR), and completed-but-not-removed markers. Essential for maintaining clean refactor tracking, preventing technical debt accumulation, and ensuring refactor work is properly documented and completed.

## When to Use

Use this skill when:
- User asks "what's the status" or "how's the refactor going"
- Before marking a feature as complete (@feature-completer)
- During progress checks (@statuser)
- Performing architecture health audits (@architecture-guardian)
- User mentions "refactor" or "markers"
- Weekly health check (scheduled monitoring)
- Before starting a new refactor (check existing work)
- User asks to "check refactor status" or "audit markers"

### Core Sections (Detailed TOC)
- [Quick Start](#quick-start) - Check refactor marker health across codebase
- [Instructions](#instructions) - 5-step detection and validation process
  - [Step 1: Find All REFACTOR Markers](#step-1-find-all-refactor-markers) - Grep for file-level and method-level markers
  - [Step 2: Parse Marker Information](#step-2-parse-marker-information) - Extract ADR number, status, dates
  - [Step 3: Validate Associated ADRs](#step-3-validate-associated-adrs) - Check ADR file existence
  - [Step 4: Detect Stale Markers](#step-4-detect-stale-markers) - Calculate age and completion status
  - [Step 5: Generate Health Report](#step-5-generate-health-report) - Categorized report with recommendations
- [Health Categories](#health-categories) - Marker health classification
  - Healthy Marker ✅ - Valid ADR, age < 30 days
  - Stale Marker ⚠️ - Age > 30 days, needs review
  - Orphaned Marker ❌ - Missing ADR, needs cleanup
  - Should Be Removed 🔴 - ADR complete, markers remain
- [Usage Patterns](#usage-patterns) - Integration with agents and workflows
  - [Pattern 1: Status Check Integration (@statuser)](#pattern-1-status-check-integration-statuser)
  - [Pattern 2: Pre-Completion Check (@feature-completer)](#pattern-2-pre-completion-check-feature-completer)
  - [Pattern 3: Refactor Health Audit](#pattern-3-refactor-health-audit)
  - [Pattern 4: Proactive Monitoring](#pattern-4-proactive-monitoring)

### Supporting Resources
- [Health Categories Guide](./references/health-categories-guide.md) - Detailed health classification logic
- [Remediation Guide](./references/remediation-guide.md) - Step-by-step fix instructions
- [Edge Cases](#edge-cases) - Handling special scenarios
- [Integration Points](#integration-points) - Integration with other skills and agents
- [Anti-Patterns](#anti-patterns) - What NOT to do
- [Best Practices](#best-practices) - Recommended approaches
- [Success Criteria](#success-criteria) - Quality metrics
- [Troubleshooting](#troubleshooting) - Common issues and solutions
- [Output Format](#output-format) - Report structure examples
- [Requirements](#requirements) - Dependencies and project context

## Quick Start

Check refactor marker health across your codebase:

```bash
# Find all REFACTOR markers (file-level and method-level)
grep -rn "^# REFACTOR:" src/ --include="*.py"
grep -rn "# REFACTOR(" src/ --include="*.py"

# Validate ADR existence
test -f docs/adr/in_progress/027-service-result-migration.md && echo "ADR exists" || echo "ADR missing"

# Calculate marker age (if STARTED date present)
# Current date - STARTED date > 30 days = STALE
```

**Typical output:**
- ✅ Healthy: All markers have valid ADRs, age < 30 days
- ⚠️ Stale: Markers > 30 days old (needs review)
- ❌ Orphaned: Markers with missing ADRs (needs cleanup)
- 🔴 Should Remove: ADR complete but markers remain

## Instructions

### Step 1: Find All REFACTOR Markers

Use grep to locate both marker types:

**File-level markers:**
```bash
grep -rn "^# REFACTOR:" src/ --include="*.py" --include="*.ts" --include="*.js"
```

**Method-level markers:**
```bash
grep -rn "# REFACTOR(" src/ --include="*.py" --include="*.ts" --include="*.js"
```

**Extract from each match:**
- File path
- Line number
- ADR number (format: ADR-XXX)
- Status (if present: IN_PROGRESS, BLOCKED, REVIEW)
- STARTED date (if present: YYYY-MM-DD)

### Step 2: Parse Marker Information

**File-level marker format:**
```python
# REFACTOR: ADR-027 - ServiceResult Migration
# STATUS: IN_PROGRESS
# STARTED: 2025-10-10
# PERMANENT_RECORD: docs/adr/in_progress/027-service-result-migration.md
```

**Method-level marker format:**
```python
# REFACTOR(ADR-027): Migrate to ServiceResult pattern
def get_user(user_id: int):
    pass
```

**Parsing logic:**
- Extract ADR number using regex: `ADR-(\d+)`
- Extract status from `# STATUS:` line
- Extract start date from `# STARTED:` line (YYYY-MM-DD)
- Extract ADR path from `# PERMANENT_RECORD:` line
- Store unique ADR numbers for validation

### Step 3: Validate Associated ADRs

For each unique ADR number found:

**Check ADR existence:**
```bash
# Search for ADR file in all ADR directories
find docs/adr -name "*027-*.md" -type f
```

**Validation outcomes:**
- ✅ **Valid:** ADR file exists, marker is healthy
- ❌ **Orphaned:** ADR file not found (deleted, moved, or wrong number)

**ADR location patterns to check:**
```bash
docs/adr/in_progress/XXX-title.md     # Active refactors
docs/adr/implemented/XXX-title.md     # Completed refactors
docs/adr/deprecated/XXX-title.md      # Deprecated refactors
```

### Step 4: Detect Stale Markers

**Calculate marker age:**
```bash
# For markers with STARTED date
STARTED_DATE="2025-09-01"
CURRENT_DATE=$(date +%Y-%m-%d)
AGE_DAYS=$((( $(date -d "$CURRENT_DATE" +%s) - $(date -d "$STARTED_DATE" +%s) ) / 86400))

# Check if stale
if [ $AGE_DAYS -gt 30 ]; then
    echo "⚠️ STALE: Marker is $AGE_DAYS days old"
fi
```

**Staleness criteria:**
- Age > 30 days = ⚠️ STALE
- ADR status IN_PROGRESS but no recent updates = ⚠️ STALE
- Consider stale if work appears abandoned

**Check ADR completion status:**
```bash
# If ADR moved to implemented/ but markers remain
if [ -f docs/adr/implemented/027-*.md ]; then
    echo "🔴 Should be removed: ADR complete but markers present"
fi
```

### Step 5: Generate Health Report

**Report structure:**

```yaml
health: GOOD | ATTENTION_NEEDED | CRITICAL
active_refactors:
  - adr: ADR-XXX
    title: Title from ADR
    files: Count of files with markers
    markers: Total marker count
    age_days: Age since STARTED date
    status: IN_PROGRESS | BLOCKED | REVIEW
    adr_valid: true | false
stale_markers: []
orphaned_markers: []
should_be_removed: []
summary: Human-readable summary
```

**Health classification:**

- **GOOD:** All markers valid, no stale/orphaned, all ADRs active
- **ATTENTION_NEEDED:** Stale markers present (>30 days)
- **CRITICAL:** Orphaned markers or should-be-removed issues

## Health Categories

### Healthy Marker ✅
- ADR file exists and is valid
- ADR status matches marker status
- Age < 30 days (if STARTED date present)
- Active tracking in place
- No blocking issues

### Stale Marker ⚠️
- Age > 30 days since STARTED date
- Still shows IN_PROGRESS status
- No recent updates in ADR file
- Refactor taking longer than expected
- **Action:** Review progress, update ADR, or complete work

### Orphaned Marker ❌
- ADR file doesn't exist (404)
- ADR was deleted without removing markers
- Marker references non-existent ADR number
- Incorrect ADR number in marker
- **Action:** Find correct ADR or remove markers

### Should Be Removed 🔴
- ADR status is COMPLETE or IMPLEMENTED
- ADR moved to `docs/adr/implemented/`
- Markers still present in source code
- Refactor work done but cleanup incomplete
- **Action:** Remove all markers (use manage-refactor-markers)

## Usage Patterns

### Pattern 1: Status Check Integration (@statuser)

```
User: "What's my progress on the feature?"

@statuser workflow:
1. Check todo.md status (TodoRead)
2. Check quality metrics (pytest, pyright)
3. Invoke detect-refactor-markers skill
4. Include refactor health in status report

Report includes:
- Task completion percentage
- Quality gate status
- Refactor health status
- Blockers or issues
```

### Pattern 2: Pre-Completion Check (@feature-completer)

```
User: "Mark feature complete"

@feature-completer workflow:
1. Verify all tasks complete
2. Verify quality gates pass
3. Invoke detect-refactor-markers skill
4. Block completion if markers present

Decision logic:
- If active markers found: ❌ Block completion
  - Reason: "Cannot complete feature with active refactor markers"
  - Action: "Complete or remove markers first"
- If no markers: ✅ Allow completion
```

### Pattern 3: Refactor Health Audit

```
User: "How's the refactor going?" OR "Check refactor status"

Agent workflow:
1. Invoke detect-refactor-markers skill
2. Generate comprehensive health report
3. Recommend actions for each issue

Report sections:
- Active refactors summary
- Stale markers (prioritized by age)
- Orphaned markers (needs immediate cleanup)
- Completion suggestions
```

### Pattern 4: Proactive Monitoring

**Agents that should auto-invoke this skill:**
- @statuser (every status check)
- @architecture-guardian (architecture health audits)
- @feature-completer (before marking complete)
- @implementer (optional: before starting new refactor)

**Trigger conditions:**
- User asks for "status" or "progress"
- User asks to "complete" or "finish" feature
- User mentions "refactor" or "markers"
- Weekly health check (scheduled)

## Examples

The [Output Format](#output-format) section below shows comprehensive report examples including:
- Healthy refactor status
- Stale marker detection
- Orphaned marker detection
- Should-be-removed detection
- Multi-ADR scenarios

See [references/health-categories-guide.md](./references/health-categories-guide.md) for detailed health classification logic.

See [references/remediation-guide.md](./references/remediation-guide.md) for step-by-step fix instructions for each issue type.

## Edge Cases

### No Markers Found
```bash
# Grep returns no results
grep -rn "^# REFACTOR:" src/ --include="*.py"
# (no output)

Report:
✅ No active refactors (healthy state)
All code is clean, no ongoing migrations.
```

### Markers Without STARTED Date
```python
# Old marker format (missing STARTED field)
# REFACTOR: ADR-015 - Database Migration
# STATUS: IN_PROGRESS
# (no STARTED date)

Handling:
- Can't calculate age
- Report as "Unknown age (missing STARTED date)"
- Recommend adding STARTED date
```

### Method-Only Markers (No File-Level Marker)
```python
# Valid: Method markers can exist without file marker
# REFACTOR(ADR-027): Migrate to ServiceResult
def get_user():
    pass

# REFACTOR(ADR-027): Migrate to ServiceResult
def update_user():
    pass

Report:
✅ Valid markers (method-only is allowed)
File: src/services/user_service.py
Markers: 2 method-level (no file-level)
```

### Multiple ADRs in One File
```python
# Valid: Multiple refactors can overlap
# REFACTOR: ADR-027 - ServiceResult Migration
# STATUS: IN_PROGRESS
# STARTED: 2025-10-10

# REFACTOR(ADR-042): Payment Service Refactor
def process_payment():
    pass

Report:
✅ Multiple active refactors in file
File: src/services/payment_service.py
- ADR-027: ServiceResult Migration (file-level)
- ADR-042: Payment Refactor (1 method marker)
```

### ADR Moved Between Directories
```bash
# Marker references old path
# PERMANENT_RECORD: docs/adr/in_progress/027-service-result-migration.md

# But ADR actually at:
docs/adr/implemented/027-service-result-migration.md

Detection:
🔴 Should be removed: ADR moved to implemented/
Action: Remove markers (refactor complete)
```

## Integration Points

**With manage-refactor-markers skill:**
- detect-refactor-markers identifies issues
- manage-refactor-markers fixes them (remove, update)
- Workflow: detect → report → manage → verify

**With validate-refactor-adr skill:**
- Both validate ADR existence
- detect-refactor-markers: Batch validation (all markers)
- validate-refactor-adr: Single ADR validation (detailed)

**With @statuser agent:**
- Primary integration point
- Included in every status check
- Refactor health added to status reports

**With @architecture-guardian agent:**
- Architecture health audits
- Detects refactor debt accumulation
- Enforces completion policies

**With @feature-completer agent:**
- Blocks feature completion if markers present
- Ensures clean completion (no pending refactors)
- Validates all work finished

## Anti-Patterns

❌ **DON'T:** Ignore orphaned markers
- Reason: Pollutes codebase, confuses developers
- Impact: Technical debt accumulation
- Fix: Remove immediately

❌ **DON'T:** Let markers go stale without action
- Reason: Indicates stuck or abandoned work
- Impact: Blocks future refactors, unclear ownership
- Fix: Review progress, update ADR, or complete

❌ **DON'T:** Remove markers that still have work to do
- Reason: Loses tracking of incomplete migrations
- Impact: Partial refactors, inconsistent codebase
- Fix: Complete work first, then remove markers

❌ **DON'T:** Forget to check all file types
- Reason: TypeScript/JavaScript markers missed
- Impact: Incomplete health picture
- Fix: Always check .py, .ts, .js files

❌ **DON'T:** Skip ADR validation
- Reason: Assumes ADR exists without checking
- Impact: False health reports, orphaned markers undetected
- Fix: Always validate with `find` or `test -f`

## Best Practices

✅ **DO:** Run health checks regularly
- Frequency: Weekly or before feature completion
- Integration: Part of status checks
- Automation: @statuser auto-invokes

✅ **DO:** Clean up orphaned markers immediately
- Critical issues require immediate action
- Use manage-refactor-markers remove
- Validate cleanup with re-detection

✅ **DO:** Review stale markers monthly
- Assess if work should continue
- Update ADR status or complete work
- Close abandoned refactors

✅ **DO:** Validate ADRs exist before trusting markers
- Never assume ADR presence
- Use `find docs/adr -name "*XXX-*.md"`
- Report missing ADRs as critical

✅ **DO:** Remove markers when ADR complete
- Check `docs/adr/implemented/` directory
- Clean removal prevents technical debt
- Use manage-refactor-markers for batch removal

## Success Criteria

- ✅ All markers found (grep successful across all file types)
- ✅ ADR validation accurate (correct exists/missing determination)
- ✅ Staleness calculation correct (age > 30 days detection)
- ✅ Clear health report (categorized issues with counts)
- ✅ Actionable recommendations (specific next steps for each issue)
- ✅ Integration with agent workflows (status checks, completion gates)

## Troubleshooting

**Issue:** Grep finds no markers but you know they exist
```bash
# Possible causes:
# 1. Wrong directory (not in project root)
pwd  # Check current directory
cd /path/to/project/root

# 2. Wrong pattern (marker format different)
# Try broader search:
grep -rn "REFACTOR" src/

# 3. Markers in different file types
grep -rn "REFACTOR" src/ --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx"
```

**Issue:** ADR validation always reports "missing"
```bash
# Check ADR directory structure
ls -R docs/adr/

# Expected structure:
# docs/adr/in_progress/
# docs/adr/implemented/
# docs/adr/deprecated/

# If different structure, adjust validation paths
```

**Issue:** Age calculation fails
```bash
# Check date format in marker
# Expected: YYYY-MM-DD (2025-10-16)
# If different format, parsing will fail

# Verify date command works
date +%Y-%m-%d

# For macOS vs Linux compatibility:
# macOS: date -j -f "%Y-%m-%d" "2025-10-16" +%s
# Linux: date -d "2025-10-16" +%s
```

**Issue:** Multiple marker formats in codebase
```bash
# Handle variation:
# Format 1: # REFACTOR: ADR-027 - Title
# Format 2: # REFACTOR(ADR-027): Description
# Format 3: # REFACTOR [ADR-027] Title

# Use flexible regex:
grep -rn "REFACTOR.*ADR-[0-9]" src/

# Extract ADR number with sed:
sed -n 's/.*ADR-\([0-9]\+\).*/\1/p'
```

## Output Format

**Healthy Report:**
```yaml
health: GOOD
active_refactors:
  - adr: ADR-027
    title: ServiceResult Migration
    files: 2
    markers: 10
    age_days: 6
    status: IN_PROGRESS
    adr_valid: true
    adr_path: docs/adr/in_progress/027-service-result-migration.md
stale_markers: []
orphaned_markers: []
should_be_removed: []
summary: All refactors healthy. 1 active refactor (ADR-027) with 10 markers across 2 files.
```

**Unhealthy Report:**
```yaml
health: CRITICAL
active_refactors:
  - adr: ADR-027
    title: ServiceResult Migration
    files: 2
    markers: 10
    age_days: 6
    status: IN_PROGRESS
    adr_valid: true
stale_markers:
  - adr: ADR-015
    title: Database Migration
    file: src/infrastructure/database.py
    age_days: 45
    started: 2025-09-01
    status: IN_PROGRESS
    issue: Stale (>30 days without completion)
    action: Review progress, update ADR status, or complete work
orphaned_markers:
  - adr: ADR-042
    file: src/services/payment_service.py
    markers: 4
    issue: ADR file not found in any docs/adr directory
    possible_causes:
      - ADR deleted without removing markers
      - ADR moved to different directory
      - Incorrect ADR number in markers
    action: |
      1. Search for ADR: find docs/adr -name "*payment*"
      2. If found: Update marker ADR numbers
      3. If not found: Remove markers using manage-refactor-markers
should_be_removed:
  - adr: ADR-028
    title: Cache Layer Implementation
    files: 4
    markers: 12
    adr_status: COMPLETE
    adr_path: docs/adr/implemented/028-cache-layer.md
    issue: ADR complete and moved to implemented/ but markers remain
    action: Remove all markers using manage-refactor-markers remove
summary: |
  3 critical issues requiring attention:
  - 1 stale marker (ADR-015, 45 days old)
  - 1 orphaned marker set (ADR-042, 4 markers)
  - 1 should-be-removed set (ADR-028, 12 markers)

  Recommended priority:
  1. Remove orphaned ADR-042 markers (critical)
  2. Remove completed ADR-028 markers (cleanup)
  3. Review stale ADR-015 refactor (assess continuation)
```

## Requirements

**No external dependencies required.** This skill uses only built-in tools:
- `grep`: Find markers in source files
- `find`: Locate ADR files
- `test -f`: Validate file existence
- `date`: Calculate marker age

**Project context required:**
- `.claude/refactor-marker-guide.md`: Marker format reference
- `docs/adr/`: ADR directory structure
- Source files in `src/` directory

**See also:**
- [references/health-categories-guide.md](./references/health-categories-guide.md) - Health classification details
- [references/remediation-guide.md](./references/remediation-guide.md) - Fix instructions for each issue type
