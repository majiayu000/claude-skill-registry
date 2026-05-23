---
name: bookstrap-edit-path
description: Execute editing workflow orchestration - reviews and polishes completed sections
invoke: skill
category: orchestration
---

# Edit Path Orchestrator

Execute the editing workflow end-to-end, reviewing and polishing completed sections.

## What It Does

This orchestrator command:

1. **Queries completed draft sections** from the database
2. **Invokes the editor agent** for review passes
3. **Generates edit reports** with actionable feedback
4. **Applies fixes** (if instructed)
5. **Marks sections as edited**
6. **Tracks editorial progress**

## Usage

```bash
/bookstrap-edit-path
```

### Optional Parameters

```bash
/bookstrap-edit-path --chapter 3
/bookstrap-edit-path --mode standard
/bookstrap-edit-path --apply-fixes
/bookstrap-edit-path --section section_123
```

## Edit Modes

### Quick Pass (Surface Issues)
- Voice spot-checks (sample sections)
- Critical timeline queries only
- Obvious grammar/clarity issues
- ~15 minutes per chapter

### Standard Review (Comprehensive - Default)
- Full voice consistency check
- All consistency queries
- Line-level editing suggestions
- Citation coverage audit
- ~45 minutes per chapter

### Deep Edit (Publication-Ready)
- Standard review plus:
- Fact-checking against sources
- Character arc mapping
- Pacing analysis
- Style refinement
- Multiple passes
- ~2 hours per chapter

## Workflow

### 1. Query Sections for Review

```sql
SELECT * FROM section
WHERE status = 'draft'
ORDER BY sequence ASC;
```

Or for specific chapter:

```sql
SELECT * FROM section
WHERE status = 'draft'
AND chapter = $chapter
ORDER BY sequence ASC;
```

### 2. Run Editorial Checks

#### a. Timeline Consistency Check

```python
from scripts.editor_methods import EditorMethods

violations = editor.timeline_consistency_check(chapter)

# Returns:
# {
#   'character_state': [...],
#   'location_introduction': [...],
#   'event_sequence': [...],
#   'character_relationships': [...]
# }
```

#### b. Voice Consistency Check

```python
brd_voice = extract_voice_requirements('BRD.md')

voice_issues = editor.voice_consistency_check(
    section_ids,
    brd_voice
)
```

#### c. Citation Verification

```python
citation_issues = editor.citation_verification(
    chapter=chapter,
    min_citations_per_1000_words=2
)

# Returns:
# {
#   'uncited_sections': [...],
#   'weak_coverage': [...],
#   'low_reliability_sources': [...],
#   'conflicting_info': [...]
# }
```

### 3. Generate Edit Report

```python
report = editor.generate_edit_report(
    chapter=chapter,
    output_file=f'logs/edit-report-chapter-{chapter}.md'
)
```

Report includes:
- **Critical issues** (must fix)
- **Warnings** (should fix)
- **Suggestions** (consider improving)
- **Line-level edits** (specific changes)
- **Prioritized action items**

### 4. Apply Fixes (Optional)

If `--apply-fixes` flag set, automatically apply objective fixes:

- **Grammar corrections**
- **Consistency alignments** (if unambiguous)
- **Citation additions** (where sources obvious)

DO NOT auto-fix:
- Voice/style changes
- Content restructuring
- Subjective improvements

### 5. Update Section Status

After review (and optional fixes):

```sql
UPDATE section:[id] SET
    status = 'edited',
    edited_at = time::now(),
    edit_report = $report_path;
```

### 6. Report Progress

```
EDIT PATH COMPLETE
==================

Chapter: [number]
Sections reviewed: [count]
Total words: [count]

ISSUES FOUND
------------
Critical: [count]
  - Timeline violations: [count]
  - Uncited sections: [count]

Warnings: [count]
  - Voice inconsistencies: [count]
  - Weak citations: [count]
  - Low reliability sources: [count]

Suggestions: [count]
  - Pacing improvements: [count]
  - Character development: [count]

EDIT REPORT
-----------
Saved to: logs/edit-report-chapter-[N].md

NEXT STEPS
----------
1. Review edit report for critical issues
2. Fix timeline violations manually
3. Add missing citations
4. Run /bookstrap-edit-path --chapter [N] again to verify fixes
5. When satisfied, run /bookstrap-export-chapter [N]
```

## Error Handling

### Database Query Failures

If consistency queries fail:
- **Log the error**
- **Continue with remaining checks**
- **Report incomplete review** in summary

### BRD Not Found

If BRD.md cannot be loaded:
- **Skip voice consistency check**
- **Continue with other checks**
- **Warn user** to create BRD

### No Sections to Review

If no draft sections found:
- **Report status**
- **Suggest running** `/bookstrap-write-path` first

## Configuration

Respects settings from `bookstrap.config.json`:

```json
{
  "orchestration": {
    "edit_path": {
      "default_mode": "standard",
      "auto_apply_fixes": false,
      "require_brd": true,
      "min_citation_density": 2.0,
      "save_reports": true,
      "report_directory": "logs/editorial"
    }
  }
}
```

## Example Output

```
Starting edit path orchestration (standard mode)...

Loading BRD requirements...
Found voice requirements: conversational tone, third-person past tense

Reviewing Chapter 3 (5 sections, 6,234 words)

Running consistency checks...
├─ Timeline consistency... 2 violations found
├─ Voice consistency... 1 section flagged
├─ Citation verification... 1 uncited section, 2 weak coverage
└─ Checks complete

Generating edit report...
Report saved to: logs/edit-report-chapter-3.md

EDIT PATH COMPLETE
==================

Chapter: 3
Sections reviewed: 5
Total words: 6,234

ISSUES FOUND
------------
Critical: 3
  - Timeline violations: 2
    * Section 3.3: Character Erik appears but died in previous chapter
    * Section 3.4: Location used before introduction
  - Uncited sections: 1
    * Section 3.5: No source citations

Warnings: 3
  - Voice inconsistencies: 1
    * Section 3.2: Tone shifts from conversational to academic
  - Weak citations: 2
    * Section 3.1: Only 1.2 citations per 1000 words
    * Section 3.3: Only 1.5 citations per 1000 words

Suggestions: 0

CRITICAL FIXES NEEDED
---------------------

1. Section 3.3: Remove Erik or adjust death sequence
   Query: UPDATE character:erik SET death_sequence = 16;

2. Section 3.4: Add location introduction earlier
   Suggestion: Introduce location in Section 2.4

3. Section 3.5: Add source citations
   Recommendation: Run /bookstrap-query to find relevant sources

NEXT STEPS
----------
1. Fix critical timeline issues (see edit report)
2. Add citations to Section 3.5
3. Review voice inconsistency in Section 3.2
4. Re-run /bookstrap-edit-path --chapter 3 to verify fixes
5. When clean, export with /bookstrap-export-chapter 3

EDIT REPORT DETAILS
-------------------
Full report: logs/edit-report-chapter-3.md
```

## Integration with Other Commands

### Before

- `/bookstrap-write-path` - Complete sections to review
- `/bookstrap-status` - Check which sections are ready for editing

### During

- May reference `/bookstrap-query` to find sources for citations

### After

- Re-run `/bookstrap-edit-path` to verify fixes
- `/bookstrap-export-chapter` - Export polished chapter
- `/bookstrap-export-book` - Export entire manuscript

## Review Workflow

### First Pass (Draft Review)

```bash
# Review all draft sections
/bookstrap-edit-path --mode quick

# Fix critical issues manually

# Full review
/bookstrap-edit-path --mode standard
```

### Second Pass (Refinement)

```bash
# After fixing critical issues
/bookstrap-edit-path --mode standard

# Verify fixes
# Apply final polish
```

### Final Pass (Publication Ready)

```bash
# Deep edit for publication
/bookstrap-edit-path --mode deep

# Review edit report carefully
# Apply all suggestions
# Re-run until clean
```

## Best Practices

1. **Run after completing sections** to catch issues early
2. **Fix critical issues first** (timeline, citations)
3. **Review edit reports thoroughly** before making changes
4. **Re-run after fixes** to verify resolution
5. **Use appropriate mode** for stage of manuscript
6. **Save edit reports** for reference
7. **Don't auto-fix style** - preserve author voice

## Implementation Notes

This orchestrator is implemented as a skill that:
- Uses `editor_methods.py` for all checks
- Generates comprehensive markdown reports
- Can apply objective fixes if configured
- Updates section status to 'edited'
- Reports progress and issues to user

The orchestrator does NOT make subjective edits - it provides actionable feedback.
