---
name: update-migration-log
description: Log migration details to MIGRATION_LOG.md only. Use after completing a file migration to record details, issues, and solutions. Does NOT modify CLAUDE.md or TASK_BOARD.md - those are managed by other skills. Focused solely on maintaining detailed migration history.
---

# Migration Logger

Log detailed migration history to MIGRATION_LOG.md.

## Core Responsibility

**Log to MIGRATION_LOG.md ONLY** - This skill:
- ✅ Updates: MIGRATION_LOG.md
- ❌ Does NOT modify: CLAUDE.md, TASK_BOARD.md, or other files

**Clear separation:**
- `update-migration-log` → Logs migration details to MIGRATION_LOG.md
- `update-task-board` → Updates TASK_BOARD.md based on logs
- CLAUDE.md → Entry point, rarely modified

## When to Use

Use this skill after:
- Completing a file migration
- Recording migration issues and solutions
- User asks to "log migration" or "update migration log"

**Do NOT use for:**
- Updating task status (use update-task-board)
- Updating CLAUDE.md (handled separately)
- General task completion (use update-task-board)

## Migration Entry Template

Use this template for all migration entries:

```markdown
### YYYY-MM-DD - [Original File] → [New Location]

**Status:** ✅ Completed / 🚧 In Progress / ⚠️ Issues
**Time Spent:** [e.g., 45 minutes]
**Complexity:** Low / Medium / High

**Source:** `[path/to/original/file.py]`
**Destination:** `[path/to/new/file.py]`

#### 📋 Migration Summary
- **Original Purpose:** [Brief description]
- **Target Architecture Layer:** [Problem/Algorithm/Data/Visualization]
- **Key Changes Made:** [2-3 sentence overview]

#### 🔧 Key Changes
- **Extracted hardcoded values:** [What was parameterized]
- **Decoupled from paper logic:** [How generalized]
- **Added/improved:** [Docstrings, type hints, etc.]

#### ⚠️ Issues & Solutions
**Issue 1:** [Description]
- **Solution:** [Fix implemented]
- **Impact:** [Effect on migration]

#### ✅ Verification
- [x] Code compilation
- [x] Import tests
- [ ] Runtime tests (if environment available)

#### 📝 Notes
- [Any important observations]
```

## MIGRATION_LOG.md Structure

### Required Sections

**1. Header**
```markdown
# VRP Toolkit - Migration Log

**Last Updated:** YYYY-MM-DD
**Total Files Migrated:** X/9
```

**2. Migration Progress Summary**
```markdown
## 📊 Migration Progress Summary

| Category | Completed | Total | Progress |
|----------|-----------|-------|----------|
| Core Files | X | 9 | XX% |
```

**3. Migration History** (newest first)
```markdown
## 📜 Migration History

### YYYY-MM-DD - file.py → new/location.py
[Entry details...]
```

## Workflow

### Step 1: Prepare Entry

Gather information about the migration:
- Original file location
- New file location
- Changes made
- Issues encountered
- Time spent
- Complexity level

### Step 2: Write Entry

1. Use migration entry template
2. Fill in all sections
3. Be specific about changes and issues
4. Include verification checklist results

### Step 3: Update MIGRATION_LOG.md

1. Update "Last Updated" date
2. Update "Total Files Migrated" count
3. Update progress table percentages
4. Add entry to top of "Migration History"
5. Keep entries in reverse chronological order (newest first)

### Step 4: Save

No further action needed - other skills will read this log.

## Entry Guidelines

### Summary Section

**Be concise but informative:**
- Original purpose: 1 sentence
- Target layer: One of Problem/Algorithm/Data/Visualization
- Key changes: 2-3 sentences covering main refactoring

**Example:**
```markdown
#### 📋 Migration Summary
- **Original Purpose:** Instance class for PDPTW with battery constraints
- **Target Architecture Layer:** Problem
- **Key Changes Made:** Extracted hardcoded depot location and vehicle capacity into parameters. Separated solution validation from instance definition. Added type hints and comprehensive docstrings.
```

### Key Changes Section

**List specific technical changes:**
- Parameters extracted from hardcoded values
- Decoupling from paper-specific logic
- Documentation improvements
- API changes

**Example:**
```markdown
#### 🔧 Key Changes
- **Extracted hardcoded values:** Depot location (0,0), vehicle capacity (15), max battery (100)
- **Decoupled from paper logic:** Removed SISR-specific validation, generalized time window checks
- **Added/improved:** Full docstrings for all public methods, type hints for function signatures
```

### Issues & Solutions Section

**Document problems encountered:**
- Import errors
- Circular dependencies
- API incompatibilities
- Logic errors

**For each issue:**
- Clear description
- Solution implemented
- Impact on migration

**Example:**
```markdown
#### ⚠️ Issues & Solutions
**Issue 1:** Circular import between Instance and Solution classes
- **Solution:** Moved Solution to separate module, used TYPE_CHECKING for type hints
- **Impact:** Required restructuring module organization

**Issue 2:** Hardcoded file paths in data loading
- **Solution:** Added config parameter for data directory path
- **Impact:** Minor - added one parameter to constructor
```

### Verification Section

**Checklist items:**
- [x] Code compilation (no syntax errors)
- [x] Import tests (can import without errors)
- [x] Runtime tests (if applicable)
- [x] Tutorial compatibility (if applicable)

Mark items complete only when verified.

## Integration with Other Skills

**Read by:**
- `update-task-board` - Uses entries to update TASK_BOARD.md
- `build-session-context` - Shows recent migrations
- `manage-skills` - Reads for project history

**Does NOT interact with:**
- CLAUDE.md (not this skill's job)
- TASK_BOARD.md (update-task-board handles)

## Example Entry

```markdown
### 2026-01-01 - instance.py → vrp_toolkit/problems/pdptw.py

**Status:** ✅ Completed
**Time Spent:** 2 hours
**Complexity:** High

**Source:** `SDR_stochastic/new version/instance.py`
**Destination:** `vrp-toolkit/vrp_toolkit/problems/pdptw.py`

#### 📋 Migration Summary
- **Original Purpose:** PDPTW instance class with battery constraints for SDR paper
- **Target Architecture Layer:** Problem
- **Key Changes Made:** Extracted all hardcoded values (depot, capacity, battery) into parameters. Separated instance definition from solving logic. Added comprehensive type hints and docstrings following Google style.

#### 🔧 Key Changes
- **Extracted hardcoded values:** Depot (0,0), vehicle capacity 15, max battery 100, charging rate 2.0
- **Decoupled from paper logic:** Removed SISR-specific validation, separated battery simulation from instance
- **Added/improved:** Complete docstrings, type hints, parameter validation in constructor

#### ⚠️ Issues & Solutions
**Issue 1:** Circular dependency with Solution class
- **Solution:** Moved Solution to separate module, used forward references
- **Impact:** Created cleaner module structure

**Issue 2:** Time window validation assumed specific format
- **Solution:** Generalized validation to accept any numeric time windows
- **Impact:** None - more flexible API

#### ✅ Verification
- [x] Code compilation
- [x] Import tests
- [x] Runtime tests with sample data
- [x] Tutorial compatibility verified

#### 📝 Notes
- Battery constraint logic may need future generalization for other problems
- Consider adding battery capacity as instance parameter vs vehicle parameter
```

## Maintenance Notes

**Keep MIGRATION_LOG.md:**
- Chronologically ordered (newest first)
- Detailed but focused
- Consistent formatting
- Evidence of progress

**Update frequency:**
- After each migration completes
- When significant issues are resolved
- When migration approach changes

## File References

- **Manages:** `.claude/MIGRATION_LOG.md`
- **Does NOT modify:** `.claude/CLAUDE.md`, `.claude/TASK_BOARD.md`
