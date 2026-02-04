---
name: cleanup
description: Project organization expert - analyzes folder state, detects redundancy, moves files to proper locations, consolidates duplicate content, appends to accumulator files, removes obsolete content, and generates detailed operation reports. Maintains project structure integrity.
version: 1.1.0
---

# GabeDA Cleanup & Organization Expert

## Purpose

This skill **analyzes and organizes project folders** to maintain clean, well-structured codebases. It understands project conventions, identifies redundancy, consolidates accumulator files, and removes obsolete content.

**Key Capabilities:**
- Analyze current folder/project state
- **Detect redundant and duplicate content across files** ⭐ NEW
- **Suggest document consolidation and merging** ⭐ NEW
- Move files to proper locations per project conventions
- Append content to accumulator/living documents
- Identify and remove obsolete files
- Generate detailed operation and merge suggestion reports

## When to Invoke

**Use this skill when:**
- Project has accumulated duplicate/scattered files
- **Multiple files contain redundant or overlapping content** ⭐ NEW
- **Need suggestions for document consolidation/merging** ⭐ NEW
- Files need reorganization per documentation standards
- Content should be consolidated into living documents
- Obsolete files need identification and removal
- Need audit trail of file operations

**Input required:** Path(s) to folders needing cleanup

## Workflow

### 1. Analyze Current State

**Understand project structure:**
- Read project documentation standards (CLAUDE.md, DOCUMENTATION_STANDARD.md)
- Identify living documents (10 accumulators in ai/ and docs/)
- Map current file locations and relationships
- Detect redundancy patterns

**Generate state report:**
- Total files by type/category
- Misplaced files (wrong folder)
- Duplicate/redundant content
- Accumulator opportunities (content that should be appended)
- Obsolete file candidates

### 2. Detect Redundancy (⭐ NEW)

**Analyze files for redundant content:**

**Content Similarity Analysis:**
- Compare file contents pairwise
- Calculate similarity scores (0-100%)
- Identify duplicate/near-duplicate clusters
- Group files by content similarity

**Pattern Recognition:**
- Detect versioned files (file_v1.md, file_v2.md, file_final.md)
- Detect dated files (notes_2025_10.md, notes_2025_11.md)
- Detect topic variants (auth.md, authentication.md, login_guide.md)

**Topic Modeling:**
- Extract topics from file headings
- Group files covering same topics
- Identify fragmented information

**Reference Analysis:**
- Count references to each file
- Identify authoritative sources (heavily referenced)
- Find orphan files (unreferenced duplicates)

**Redundancy Scoring:**
- Assign redundancy score (0-10) to file groups
- HIGH (9-10): Immediate consolidation recommended
- MEDIUM (6-8): User review suggested
- LOW (3-5): Optional optimization

**Generate merge suggestions:**
- Present redundancy groups by priority
- Propose consolidation strategies (MERGE/CONSOLIDATE/HIERARCHICAL/APPEND)
- Estimate impact (file reduction, clarity improvement)
- Request user approval before proceeding

**Reference:** [cleanup/references/redundancy_detection.md](references/redundancy_detection.md)

**Template:** [cleanup/assets/templates/merge_suggestion_template.md](assets/templates/merge_suggestion_template.md)

### 3. Categorize Files

**Decision tree for each file:**

```
FILE → Is it a living document?
       ├─ YES → Check if properly named/located
       │        ├─ YES → Skip (already correct)
       │        └─ NO → Flag for rename/move
       │
       └─ NO → Should content go into living doc?
               ├─ YES → Flag for append + delete
               │
               └─ NO → Is file obsolete?
                       ├─ YES → Flag for deletion
                       └─ NO → Is file in wrong folder?
                               ├─ YES → Flag for move
                               └─ NO → Skip (correct)
```

**Reference:** [cleanup/references/file_categorization_rules.md](references/file_categorization_rules.md)

### 4. Plan Operations

**Group operations by type:**
1. **MERGE** - Consolidate redundant files (⭐ NEW)
2. **MOVE** - Files to relocate (with destination)
3. **APPEND** - Content to merge into living docs
4. **DELETE** - Obsolete files to remove
5. **RENAME** - Files needing name standardization

**Safety checks:**
- Verify destinations exist
- Check for overwrite conflicts
- Validate accumulator file format compatibility
- Confirm deletion safety (no external references)
- Ensure unique content preserved during merges (⭐ NEW)

### 5. Execute with User Approval

**Present operation plan:**
- Show all proposed operations in clear table format
- Highlight potential risks (overwrites, deletions)
- Explain rationale for each operation

**Request approval:**
- **CRITICAL:** NEVER execute operations without explicit user approval
- User reviews plan and confirms: "proceed", "skip deletions", "cancel", etc.

**Execute approved operations:**
- Perform operations in safe order: MERGE → MOVE → APPEND → DELETE
- Log each operation with timestamp
- Handle errors gracefully (report, don't abort entire batch)

### 6. Generate Report

**Create operation report** using template: [cleanup/assets/templates/cleanup_report_template.md](assets/templates/cleanup_report_template.md)

**Report sections:**
- **Summary:** Total operations by type, files affected
- **Detailed log:** Each operation with source/destination/timestamp
- **Errors:** Any failures encountered
- **State comparison:** Before/after folder structure
- **Recommendations:** Further cleanup opportunities

**Save report:** `cleanup_report_YYYYMMDD_HHMM.md` in project root or user-specified location

## Living Documents (10 Accumulators)

**These files accumulate content - APPEND, don't replace:**

### ai/ Folder (AI Skill Accumulators)
1. `ai/CHANGELOG.md` - All code changes
2. `ai/ISSUES.md` - Bug fixes and resolutions
3. `ai/PROJECT_STATUS.md` - Sprint status and metrics
4. `ai/FEATURE_IMPLEMENTATIONS.md` - New features added
5. `ai/TESTING_RESULTS.md` - Test execution results
6. `ai/SKILLS_MANAGEMENT.md` - AI skills evolution
7. `ai/testing/TEST_MANIFEST.md` - Complete test catalog

### docs/ Folder (Human-Readable)
8. `ai/architect/ARCHITECTURE_DECISIONS.md` - Design decisions (ADRs)
9. `ai/guides/NOTEBOOK_IMPROVEMENTS.md` - Notebook refactoring log
10. `ai/planning/FUTURE_ENHANCEMENTS.md` - Future TODOs

**Reference:** [cleanup/references/accumulator_patterns.md](references/accumulator_patterns.md)

## File Organization Rules

**Standard locations per DOCUMENTATION_STANDARD.md:**

| Content Type | Proper Location | Examples |
|--------------|-----------------|----------|
| AI skill context | `ai/[skill-name]/` | feature_implementation_guide.md |
| AI conventions | `ai/conventions/` | constants.md, context_reuse.md |
| AI specs | `ai/specs/` | Technical specifications |
| AI standards | `ai/standards/` | 8-metric evaluation standards |
| Human guides | `docs/guides/` | TESTING.md, COLUMN_SCHEMA_USAGE.md |
| Architecture | `docs/architecture/` | ARCHITECTURE_DECISIONS.md |
| Business docs | `docs/business/` | User personas, use cases |
| Test files | `test/[category]/` | unit/, integration/, validation/ |
| Source code | `src/` | Core application code |
| Backend code | `backend/` | Django/DRF application |
| Frontend code | `frontend/` | React/Vite application |

**Reference:** [cleanup/references/folder_structure_guide.md](references/folder_structure_guide.md)

## Obsolescence Detection

**Files are likely obsolete if:**
- Contains "OLD", "BACKUP", "DEPRECATED" in name
- Duplicates content in living documents
- Replaced by newer versioned file
- References outdated architecture (pre-refactoring)
- Not referenced by any other file in project
- Creation date > 90 days + no recent modifications

**Manual review required before deletion:**
- Configuration files
- Data files (CSVs, JSONs)
- Files > 100 lines
- Any file with "IMPORTANT" or "CRITICAL" markers

**Reference:** [cleanup/references/obsolescence_criteria.md](references/obsolescence_criteria.md)

## Safety Guidelines

**CRITICAL RULES:**

1. **ALWAYS get user approval** before executing operations
2. **NEVER delete** without showing what will be deleted
3. **NEVER overwrite** without warning about conflicts
4. **ALWAYS preserve** original content (copy before transform)
5. **ALWAYS generate** operation report for audit trail

**Dry-run mode:** Present plan WITHOUT executing (default behavior)

**Execution mode:** Only after explicit user approval

## Example Usage

**User:** "Clean up the ai/ folder"

**Cleanup skill response:**

```
## Analysis Complete: ai/ Folder

**Current State:**
- 156 files total
- 12 living documents (correct)
- 8 misplaced files detected
- 3 files should append to accumulators
- 5 obsolete files identified

**Proposed Operations:**

### MOVE (8 files)
1. ai/old_feature_spec.md → ai/specs/archive/
2. ai/test_results_20251020.md → ai/testing/archive/
   [... 6 more]

### APPEND (3 files)
1. ai/bug_fix_notes.md → ai/ISSUES.md (append content, then delete source)
2. ai/new_model_added.md → ai/FEATURE_IMPLEMENTATIONS.md
3. ai/sprint4_update.md → ai/PROJECT_STATUS.md

### DELETE (5 files)
1. ai/BACKUP_old_spec.md (obsolete - content in specs/)
2. ai/temp_notes.txt (temporary file, 92 days old)
   [... 3 more]

**Approve operations? (respond: 'proceed', 'skip deletions', 'cancel')**
```

**More examples:** [cleanup/assets/examples/cleanup_scenarios.md](assets/examples/cleanup_scenarios.md)

---

## Example Usage with Redundancy Detection (⭐ NEW)

**User:** "Clean up the docs/ folder and suggest any document consolidation"

**Cleanup skill response:**

```
## Analysis Complete: docs/ Folder

**Current State:**
- 25 documentation files analyzed
- 3 living documents (correct)
- 1 README (correct)

**Redundancy Detection Results:**

### HIGH Redundancy (Score: 9/10)
**Group 1: Setup Guides (3 files)**
- setup_guide_v1.md (150 lines, modified 2025-09-15)
- setup_guide_v2.md (180 lines, modified 2025-10-01)
- setup_guide_final.md (200 lines, modified 2025-10-25) ← Most recent

Content similarity: 85% overlap
Suggestion: MERGE → Keep setup_guide_final.md, delete v1 and v2

### MEDIUM Redundancy (Score: 7/10)
**Group 2: Authentication Documentation (2 files)**
- api_authentication.md (120 lines, referenced by 3 files)
- auth_endpoints.md (95 lines, not referenced)

Content similarity: 70% overlap
Topic: Both cover authentication/login endpoints
Suggestion: CONSOLIDATE → Merge into single authentication.md

### Proposed Consolidation Operations:

**MERGE (Group 1):**
1. Keep: setup_guide_final.md
2. Extract unique content from v1 and v2 (if any)
3. Delete: setup_guide_v1.md, setup_guide_v2.md
4. Impact: 3 files → 1 file

**CONSOLIDATE (Group 2):**
1. Create: authentication.md
2. Merge content from both files
3. Update 3 references to point to new file
4. Delete source files
5. Impact: 2 files → 1 file

**Total Impact:**
- File reduction: 25 → 20 files (5 files consolidated, 20% reduction)
- Improved clarity: Single authoritative source for each topic
- Easier maintenance: Fewer files to keep updated

**Do you approve these consolidations?**
(respond: 'approve-all', 'approve group 1 only', 'modify', 'skip')
```

**User response:** "approve-all"

**Cleanup skill executes consolidation + generates report with before/after comparison**

## Quality Standards

**Cleanup operations must meet:**

✅ **Correctness (25%)** - Files moved to proper locations per standards
✅ **Safety (25%)** - No data loss, user approval obtained
✅ **Completeness (20%)** - All redundancy/obsolescence addressed
✅ **Auditability (20%)** - Detailed operation report generated
✅ **Reversibility (10%)** - Operations can be undone if needed

**Minimum score: 8.0/10** before executing operations.

## Related Skills

**Use other skills for:**
- **executive** - Decide project-level organization strategy
- **architect** - Understand code architecture for proper categorization
- **business** - Identify which documents are accumulator vs reference
- **insights** - Organize notebook files and analysis outputs
- **marketing** - Organize marketing assets and templates
- **ux-design** - Organize design assets and wireframes

## Bundled Resources

**References:**
- [file_categorization_rules.md](references/file_categorization_rules.md) - Decision logic for categorizing files
- [accumulator_patterns.md](references/accumulator_patterns.md) - How to append to living documents
- [folder_structure_guide.md](references/folder_structure_guide.md) - Standard project organization
- [obsolescence_criteria.md](references/obsolescence_criteria.md) - Rules for identifying obsolete files
- [redundancy_detection.md](references/redundancy_detection.md) - ⭐ NEW: Detect and consolidate redundant content

**Templates:**
- [cleanup_report_template.md](assets/templates/cleanup_report_template.md) - Standard operation report format
- [operation_plan_template.md](assets/templates/operation_plan_template.md) - Pre-execution approval format
- [merge_suggestion_template.md](assets/templates/merge_suggestion_template.md) - ⭐ NEW: Document merge suggestions

**Examples:**
- [cleanup_scenarios.md](assets/examples/cleanup_scenarios.md) - Real cleanup examples with rationale

---

**Version:** 1.1.0
**Last Updated:** 2025-10-30
**Skill Type:** Project Organization & Redundancy Detection
