---
name: resolve-duplicates
description: Guidelines for identifying duplicate dictionary entries, selecting which to keep, and safely removing unneeded ones.
---

# Resolving Duplicate Entries

Use this skill when duplicate entries are detected during validation, or when you suspect multiple entries exist for the same word.

## What Counts as a Duplicate?

Duplicates are entries with the **same reading AND same headword**. The validation script (`build/validate.py`) checks for this:

```python
key = (reading, headword)  # Duplicates share both values
```

**NOT duplicates** (these are valid separate entries):
- Same reading, different headword (homophones): {橋|はし} vs {箸|はし} vs {端|はし}
- Same headword written differently: {行く|いく} vs {行く|ゆく} (different readings)
- Related but distinct words: {見る|みる} vs {見える|みえる}

## Step 1: Identify Duplicates

Run validation to find duplicates:

```bash
python3 build/validate.py 2>&1 | grep -i "duplicate"
```

Or search manually:

```bash
# Find entries with the same reading
grep -r '"reading": "たべる"' entries/

# Find entries with similar headwords
grep -r '食べる' entries/
```

## Step 2: Compare the Duplicate Entries

Read both (or all) entries carefully. Check:

1. **Are they truly the same lexical item?**
   - Same part of speech?
   - Same core meaning?
   - If they cover different senses of a polysemous word, they should be ONE entry with multiple definitions, not separate entries.

2. **If they're NOT the same** (rare):
   - Different parts of speech (noun vs verb homographs)
   - Genuinely different words that happen to share writing
   - In this case, differentiate by adjusting headwords or adding disambiguating notes

## Step 3: Select Which Entry to Keep

Choose the entry with **better quality**. Evaluate:

| Criterion | Higher Priority |
|-----------|-----------------|
| **Definition depth** | More complete explanations |
| **Example quality** | Natural, varied, useful examples |
| **Notes richness** | Covers usage, collocations, learner traps |
| **Cross-references** | Links to related entries |
| **Vocabulary tier** | Has appropriate tier assigned (if any) |
| **Furigana** | All kanji properly annotated |

**Tie-breaker**: Keep the entry with the **lower ID number** (older entry).

## Step 4: Merge Content (If Needed)

Before deleting, check if the inferior entry has unique content worth preserving:

- Unique examples not in the better entry
- Additional usage notes or collocations
- Cross-references to other entries
- Different vocabulary tier assignment (choose the more accurate one)

If so, **edit the keeper entry first** to incorporate the valuable content:

```bash
# Read both entries
cat entries/00000/00123_taberu.json
cat entries/04500/04567_taberu.json

# Edit the keeper to add any missing valuable content
# Then delete the duplicate
```

## Step 5: Delete the Duplicate

Use the `delete-entry` skill for safe deletion. The process:

1. **Delete the entry file**:
   ```bash
   rm entries/path/to/duplicate_entry.json
   ```

2. **Update indexes**:
   ```bash
   python3 build/update_indexes.py
   ```

3. **Rebuild the flat file**:
   ```bash
   python3 build/build_flat.py
   ```

4. **Verify deletion**:
   ```bash
   python3 build/validate.py
   ```

## Complete Workflow Example

```bash
# 1. Find duplicates
python3 build/validate.py 2>&1 | grep "Duplicate"

# 2. Read both entries (example)
cat entries/00000/00123_taberu.json
cat entries/04500/04567_taberu.json

# 3. Decide: Keep 00123_taberu (better examples), delete 04567_taberu

# 4. Check if 04567_taberu has content worth merging
# (If yes, edit 00123_taberu first to add the content)

# 5. Delete the duplicate
rm entries/04500/04567_taberu.json

# 6. Update indexes and rebuild
python3 build/update_indexes.py
python3 build/build_flat.py

# 7. Validate
python3 build/validate.py
```

## Handling Cross-References to Deleted Entries

If other entries reference the deleted duplicate:

1. **Search for references**:
   ```bash
   grep -r '"reading": "たべる"' entries/ --include="*.json" | grep cross_references
   ```

2. **Update references** to point to the kept entry's details (or remove if no longer relevant)

3. The `delete-entry` skill provides detailed guidance on this.

## Prevention

To avoid creating duplicates in the future:

1. **Always search before creating**:
   ```bash
   grep -r '"reading": "newword"' entries/
   grep -r 'headword_kanji' entries/
   ```

2. **Check candidate_words.json** - words there may already have entries

3. **Run validation frequently** during entry creation sessions

## Checklist

- [ ] Duplicates identified (same reading AND headword)
- [ ] Confirmed entries are for the same lexical item
- [ ] Selected which entry to keep (better quality)
- [ ] Merged any valuable unique content to keeper
- [ ] Deleted duplicate entry file
- [ ] Updated any cross-references pointing to deleted entry
- [ ] Ran `update_indexes.py`
- [ ] Ran `build_flat.py`
- [ ] Validation passes with no duplicate errors
