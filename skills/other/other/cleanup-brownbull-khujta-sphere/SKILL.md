---
name: cleanup
description: Project organization expert - analyzes project state, detects redundancy, consolidates files, removes obsolete content, maintains structure integrity
tier: 1-2
phase: ["mvp", "growth", "scale"]
version: 3.0.0
---

# Cleanup & Organization Expert - V3

## Purpose

**Phase-aware project organization skill** that analyzes and maintains clean, well-structured codebases. Understands project conventions, identifies redundancy, consolidates files, and removes obsolete content while respecting your current development phase.

## Key Capabilities

- **Analyze project state** - Understand current folder structure
- **Detect redundancy** - Find duplicate and overlapping content
- **Consolidate files** - Merge redundant documentation
- **Remove obsolete content** - Identify and delete deprecated files
- **Phase-appropriate cleanup** - Different standards per phase
- **Generate reports** - Detailed operation logs

## When to Invoke

Use this skill when:
- Project has accumulated duplicate/scattered files
- Multiple files contain redundant content
- Files need reorganization
- Obsolete files need removal
- After major refactoring
- Before shipping to next phase

**Command**: `/cleanup` or invoke via Skill tool

## Phase-Appropriate Cleanup

### Prototype Phase
- **Minimal cleanup** - Keep it loose
- Remove only obvious duplicates
- Don't enforce strict organization
- Focus: Keep it shipping

### MVP Phase
- **Basic organization** - Some structure
- Consolidate major duplicates
- Remove clearly obsolete files
- Focus: Maintain clarity

### Growth Phase
- **Structured cleanup** - Enforce conventions
- Detect and merge redundant docs
- Organize by standards
- Focus: Maintainability

### Scale Phase
- **Complete organization** - Full enforcement
- Comprehensive redundancy detection
- Strict folder structure
- Focus: Enterprise quality

## Workflow

### 1. Analyze Current State

**Understand project phase**:
```bash
# Check current phase
cat .khujta/phase.json
```

**Scan project structure**:
- Read project documentation (CLAUDE.md, README.md)
- Identify key folders (ai-state/, docs/, src/, tests/)
- Map current file locations
- Detect patterns and conventions

**Generate state report**:
- Total files by type/category
- Misplaced files (wrong location)
- Duplicate/redundant content
- Obsolete file candidates
- Phase compliance status

### 2. Detect Redundancy

**Content Similarity Analysis**:
- Compare file contents pairwise
- Calculate similarity scores (0-100%)
- Identify duplicate/near-duplicate clusters
- Group files by content similarity

**Pattern Recognition**:
- Versioned files (file_v1.md, file_v2.md, file_final.md)
- Dated files (notes_2025_10.md, notes_2025_11.md)
- Topic variants (auth.md, authentication.md, login.md)

**Redundancy Scoring**:
- HIGH (9-10): Immediate consolidation recommended
- MEDIUM (6-8): User review suggested
- LOW (3-5): Optional optimization

**Phase-Appropriate Thresholds**:
- Prototype: Only flag 95%+ similarity (near-identical)
- MVP: Flag 80%+ similarity
- Growth: Flag 70%+ similarity
- Scale: Flag 60%+ similarity

### 3. Categorize Files

**Decision tree per phase**:

```
FILE → Check phase requirements
       ├─ Prototype → Skip unless obvious duplicate
       ├─ MVP → Basic categorization
       ├─ Growth → Structured organization
       └─ Scale → Strict enforcement

     → Is it redundant?
       ├─ YES → Flag for merge/consolidate
       └─ NO → Is it in correct location?
               ├─ YES → Skip
               └─ NO → Flag for move

     → Is it obsolete?
       ├─ YES → Flag for deletion
       └─ NO → Keep
```

### 4. Plan Operations

**Group operations by type**:
1. **MERGE** - Consolidate redundant files
2. **MOVE** - Relocate misplaced files
3. **DELETE** - Remove obsolete files
4. **RENAME** - Standardize naming

**Phase-Appropriate Planning**:
- **Prototype**: Only merges and deletes
- **MVP**: Add basic moves
- **Growth**: Full organization
- **Scale**: Strict enforcement + renames

**Safety checks**:
- Verify destinations exist
- Check for overwrite conflicts
- Confirm deletion safety
- Preserve unique content

### 5. Execute with Approval

**Present operation plan**:
```markdown
## Cleanup Plan for [Phase] Phase

**Current State**:
- 156 files total
- 8 redundant files detected
- 5 misplaced files
- 3 obsolete files

**Proposed Operations**:

### MERGE (3 operations)
1. setup_v1.md + setup_v2.md → setup.md
   Similarity: 85% | Recommendation: Keep latest

### MOVE (5 operations)
1. old_spec.md → ai-state/archive/
2. test_results.md → ai-state/regressions/

### DELETE (3 operations)
1. BACKUP_file.md (obsolete, 92 days old)
2. temp_notes.txt (temporary file)

**Approve? (yes/no/skip-deletes)**
```

**Execute approved operations**:
- Perform in safe order: MERGE → MOVE → DELETE
- Log each operation with timestamp
- Handle errors gracefully
- Update operations log

### 6. Generate Report

**Create cleanup report**:
```markdown
# Cleanup Report - [Date]

## Summary
- Phase: [prototype/mvp/growth/scale]
- Operations: 11 total (3 merge, 5 move, 3 delete)
- Files reduced: 156 → 148
- Duration: 2 minutes

## Detailed Operations

### Merges (3)
✅ Merged setup_v1.md + setup_v2.md → setup.md
✅ Consolidated auth docs → authentication.md
✅ Merged test results → TEST_RESULTS.md

### Moves (5)
✅ Moved old_spec.md → ai-state/archive/
...

### Deletions (3)
✅ Deleted BACKUP_file.md
...

## Impact
- Clarity: Improved documentation findability
- Maintenance: Fewer files to update
- Storage: 45KB saved

## Recommendations
- Consider archiving files older than 90 days
- Set up automated cleanup hook
```

**Save report**: `ai-state/cleanup/cleanup_report_YYYYMMDD.md`

## File Organization Standards

**Standard locations for Khujta Sphere V3**:

| Content Type | Location | Phase |
|-------------|----------|-------|
| Phase config | `.khujta/phase.json` | All |
| Operations log | `ai-state/operations.log` | All |
| Task files | `ai-state/active/tasks.yaml` | All |
| Test debt | `ai-state/debt/` | MVP+ |
| Regressions | `ai-state/regressions/` | MVP+ |
| Knowledge | `ai-state/knowledge/` | Growth+ |
| Standards | `ai-state/standards/` | Growth+ |
| Human docs | `ai-state/human-docs/` | Scale |

## Obsolescence Detection

**Files are likely obsolete if**:
- Contains "OLD", "BACKUP", "DEPRECATED", "TEMP" in name
- Creation date > 90 days + no modifications
- Duplicates content in primary files
- References outdated architecture
- Not referenced by any other file

**Phase-Appropriate Deletion**:
- **Prototype**: Delete only TEMP and BACKUP files
- **MVP**: Add files >90 days old
- **Growth**: Add unreferenced files
- **Scale**: Comprehensive cleanup

**Manual review required**:
- Configuration files
- Data files (CSVs, JSONs)
- Files > 100 lines
- Files with "IMPORTANT" markers

## Safety Guidelines

**CRITICAL RULES**:
1. **ALWAYS get user approval** before executing
2. **NEVER delete without showing** what will be removed
3. **ALWAYS preserve unique content** during merges
4. **ALWAYS generate operation report** for audit
5. **Respect phase requirements** - don't over-organize in prototype

**Dry-run mode**: Present plan WITHOUT executing (default)

**Execution mode**: Only after explicit user approval

## Example Usage

### Prototype Phase Example

**User**: `/cleanup`

**Response**:
```
## Cleanup Analysis (Prototype Phase)

**Current State**: 45 files
**Phase Policy**: Minimal cleanup only

**Redundancy Detection**:
- 2 obvious duplicates found (98% similarity)
- Keeping relaxed - prototype phase allows disorder

**Proposed Operations**:

MERGE (2 operations):
1. notes.md + notes_copy.md → notes.md (identical)

DELETE (1 operation):
1. TEMP_scratch.txt (temporary file)

**Phase Note**: Skipping organization - you're in prototype mode!
Ship fast, clean later.

Approve? (yes/no)
```

### Scale Phase Example

**User**: `/cleanup`

**Response**:
```
## Cleanup Analysis (Scale Phase)

**Current State**: 156 files
**Phase Policy**: Comprehensive cleanup + strict organization

**Redundancy Detection**:
HIGH (3 groups): 85% avg similarity
MEDIUM (2 groups): 70% avg similarity

**Organization Issues**:
- 12 files in wrong locations
- 3 files missing standard naming
- 5 files exceed age threshold (>90 days)

**Proposed Operations**:

MERGE (5 operations):
[... detailed list ...]

MOVE (12 operations):
[... relocations to proper folders ...]

RENAME (3 operations):
[... standardize naming ...]

DELETE (5 operations):
[... obsolete files ...]

**Impact**:
156 → 131 files (16% reduction)
Full standards compliance achieved

Approve? (yes/no/skip-deletes/modify)
```

## Integration with V3 Framework

**Works with**:
- `/test-cleanup` command (test-specific cleanup)
- `operations-logger` skill (logs all operations)
- Phase validator hook (respects phase limits)
- Quality gate hook (maintains standards)

**Complementary commands**:
- `/test-cleanup` - Clean test files specifically
- `/test-phase [phase]` - Switch phase before cleanup
- `/regression-quick` - Verify after cleanup

## Escape Hatches

If cleanup is blocking you:
- `/skip-cleanup` - Defer organization
- `/simple-cleanup` - Only obvious duplicates
- `/prototype-mode` - Switch to minimal requirements

## Quality Standards

Cleanup operations must meet (phase-appropriate):

**Prototype (6.0/10)**:
- Remove obvious duplicates only
- Don't enforce strict organization
- Preserve flexibility

**MVP (7.0/10)**:
- Basic redundancy consolidation
- Simple folder organization
- Keep it straightforward

**Growth (7.5/10)**:
- Structured organization
- Comprehensive redundancy detection
- Standards enforcement

**Scale (8.0/10)**:
- Full standards compliance
- Complete redundancy elimination
- Enterprise-grade organization

## Output Example

```markdown
# Cleanup Operation Report

**Date**: 2025-11-06T14:30:00Z
**Phase**: MVP
**Duration**: 3 minutes

## Summary
- Files analyzed: 156
- Operations executed: 11
- Files after cleanup: 148
- Reduction: 5.1%

## Operations

### Merged (3)
✅ setup_v1.md + setup_v2.md → setup.md
   Similarity: 85% | Unique content preserved

### Moved (5)
✅ old_spec.md → ai-state/archive/specs/
✅ test_results_20251105.md → ai-state/regressions/

### Deleted (3)
✅ BACKUP_config.md (obsolete backup)
✅ TEMP_notes.txt (temporary, 92 days old)
✅ old_implementation.md (replaced by current version)

## Impact
- ✅ Documentation clarity improved
- ✅ Easier to find authoritative sources
- ✅ Reduced maintenance overhead

## Next Cleanup Suggested
- In 30 days (or after next major refactoring)
- Consider setting up automated cleanup hook

**Status**: ✅ COMPLETE
```

---

**Version**: 3.0.0
**Tier**: 1-2 (MVP, Growth, Scale)
**Skill Type**: Project Organization & Maintenance
**Last Updated**: 2025-11-06