---
name: polish-entries
description: Systematic review and improvement of dictionary entries. Use when starting a polishing session to review entries for accuracy, completeness, and consistency.
---

# Dictionary Polishing Session

This skill guides systematic review and improvement of dictionary entries. Use it to start a polishing session.

## Starting a Session

### 1. Load Current State

Read these files to understand current progress:

```bash
# Required reading at session start
cat polishing/progress.json      # See review status
cat polishing/queue.json         # Check prioritized entries
cat polishing/issues.json        # Review known patterns/issues
```

Also read the most recent session log in `polishing/sessions/` to get context from the previous session.

### 2. Select Task Type

Available review tasks (in `polishing/tasks/`):

| Task | Focus | When to Use |
|------|-------|-------------|
| `full-review` | Complete entry check | General quality assurance |
| `cross-references` | Reference validation | After batch imports |
| `examples` | Example quality | Content improvement |
| `notes-consistency` | Notes formatting | Standardization pass |
| `definitions` | Definition clarity | Semantic accuracy |
| `tags` | Tag accuracy | Metadata validation |
| `furigana` | Furigana completeness | After new entries |

Read the appropriate task file for detailed instructions.

### 3. Select Entries

Choose entries based on priority:

1. **High priority**: Entries in `queue.json` high_priority
2. **Medium priority**: Entries never reviewed
3. **Low priority**: Entries with stale reviews (>90 days)
4. **Random sampling**: 5% of reviewed entries for spot-checks

Default batch size: 20 entries per session.

## Session Workflow

### Phase 1: Review Entries

For each entry in the batch:

1. Read the entry file
2. Apply the task-specific checklist
3. **Check example sentences** against the `example-sentences` skill requirements:
   - Verify minimum count for the entry's tier (5 for basic/core, 3 for general)
   - Verify vocabulary restrictions for basic/core tier examples
   - Verify progressive length (shorter to longer)
   - Add, revise, or reorder examples as needed
4. Make other improvements directly to the entry
5. Update the `modified` timestamp if changes made
6. Record the review in your session notes

### Phase 2: Record Changes

Track all changes made:

```json
{
  "entry_id": "00100_example",
  "reviewed_at": "2026-01-20T10:00:00Z",
  "status": "current",
  "changes": [
    "Added missing furigana to headword",
    "Reformatted notes with section headers"
  ],
  "issues": [],
  "notes": "Good entry, minor formatting fixes"
}
```

### Phase 3: Update Tracking Files

At session end, update:

1. **progress.json**: Add/update entry records, update statistics
2. **issues.json**: Add new issues, patterns, improvement ideas
3. **queue.json**: Remove reviewed entries, add flagged entries
4. **sessions/**: Create session log file

### Phase 4: Validate, Build, and Summarize

```bash
# Run validation
python3 build/validate.py
python3 build/validate_tags.py

# Update indexes if entries changed
python3 build/update_indexes.py

# Build static website so user can review changes
python3 build/build_flat.py
```

Provide summary to user including:
- Number of entries reviewed
- Number of entries modified
- Types of changes made
- Issues requiring attention
- Patterns observed
- Recommendations for next session

## Session Log Format

Create a session log file: `polishing/sessions/session_YYYYMMDD_NNN.json`

Include:
- Session metadata (started, ended, task type)
- List of entries reviewed with status
- Changes made with descriptions
- Issues found
- Patterns observed
- Continuation notes for next session

See `polishing/session_template.json` for the complete format.

## Quality Standards

Apply these standards during review:

### Required for All Entries
- Valid ID format matching filename
- Headword with furigana on all kanji
- Reading in hiragana only (long vowel marker ー is also allowed)
- Appropriate part_of_speech
- Clear, accurate gloss
- Complete metadata with required tags

### Content Quality
- Definitions distinguish senses clearly
- Examples illustrate actual usage
- Notes provide genuinely helpful information
- Cross-references point to valid entries (or targets added to candidates)
- No redundant or contradictory information

### Example Requirements (IMPORTANT)

**See `example-sentences` skill for complete guidelines.** During polishing, verify:

#### Minimum Example Counts
| Tier | Required per Sense |
|------|-------------------|
| Basic | 5 examples |
| Core | 5 examples |
| General | 3 examples |

#### Progressive Length
Examples should progress from shorter to longer within each sense.

#### Vocabulary Restrictions
| Tier | Examples 1-2 | Examples 3+ |
|------|-------------|-------------|
| Basic | Basic vocab only | Basic + Core only |
| Core | Basic + Core only | No restriction |
| General | No restriction | No restriction |

#### When Examples Don't Meet Guidelines
1. **Insufficient count**: Add new examples to meet minimum
2. **Wrong vocabulary tier**: Revise examples to use appropriate vocabulary
3. **No length progression**: Reorder or revise examples
4. **Missing sense coverage**: Add examples for uncovered senses

**Note:** Existing examples should be preserved if they are high quality. Add to them rather than replacing unless there are quality issues.

### Cross-Reference Target Handling
When a cross-reference points to an entry that does not exist yet, add the target to `candidate_words.json`:
```bash
python3 build/manage_candidates.py add "headword" "reading" "brief note"
```
The script automatically checks for duplicates and will refuse to add if the word already exists.

### Consistency
- Formatting matches project conventions
- Tag usage aligns with taxonomy
- Similar entries structured similarly
- Terminology consistent across entries

## Issue Tracking

When you find issues:

### Minor Issues (fix immediately)
- Missing furigana
- Formatting inconsistencies
- Minor typos
- **Example sentence deficiencies** (insufficient count, vocabulary tier violations, length progression issues)

### Medium Issues (flag for review)
- Questionable accuracy
- Missing content
- Broken references

### Major Issues (add to issues.json)
- Systematic patterns across entries
- Schema or validation problems
- Architectural concerns

## Continuation Notes

At session end, write clear continuation notes:

```json
{
  "next_entry": "00120_next",
  "pending_tasks": [
    "Complete cross-reference validation for particle entries"
  ],
  "context_for_next_session": "Focused on verb entries. Many early entries lack TRANSITIVITY section. Consider batch update."
}
```

## Commands Reference

```bash
# Validation
python3 build/validate.py
python3 build/validate_tags.py
python3 build/verify_furigana.py <entry_id>

# Indexes
python3 build/update_indexes.py

# Build (if needed for preview)
python3 build/build_flat.py

# Timestamp for modified field
python3 build/get_timestamp.py
```

## Important Reminders

1. **Update timestamps**: When modifying entries, update the `modified` field
2. **One entry at a time**: Review and edit each entry individually
3. **Track everything**: All changes go in the session log
4. **Validate frequently**: Run validation after each batch
5. **Summarize for user**: Provide clear summary before any commits
6. **Ask if unsure**: If accuracy is uncertain, flag for human review
