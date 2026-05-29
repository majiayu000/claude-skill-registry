---
name: delete-entry
description: Guidelines for safely deleting dictionary entries while properly updating indexes and cross-references.
---

# Safely Deleting Dictionary Entries

Use this skill when you need to remove an entry from the dictionary. This ensures all indexes and cross-references are properly updated.

## When to Delete an Entry

Valid reasons for deletion:
- **Duplicate entry** - Another entry exists for the same word (see `resolve-duplicates` skill)
- **Erroneous entry** - Entry contains fundamental errors that cannot be corrected
- **Out of scope** - Word doesn't belong in a learner's dictionary (too obscure, offensive, etc.)
- **Merged into another entry** - Content has been incorporated elsewhere

**Do NOT delete** entries just because they need improvement - use `revise-entries` skill instead.

## Pre-Deletion Checklist

Before deleting any entry:

1. [ ] **Confirm deletion is necessary** - Can the entry be fixed instead?
2. [ ] **Note the entry details** for later reference:
   - Entry ID (e.g., `00123_taberu`)
   - Reading (e.g., `たべる`)
   - Headword (e.g., `{食べる|たべる}`)
   - File path (e.g., `entries/00000/00123_taberu.json`)
3. [ ] **Check for cross-references** to this entry from other entries
4. [ ] **Decide if word should return to candidates** (if it still needs an entry later)

## Step 1: Find Cross-References to This Entry

Search for other entries that reference the entry you're deleting:

```bash
# Search by reading
grep -r '"reading": "たべる"' entries/ --include="*.json" -l

# Search by headword text (without furigana)
grep -r '食べる' entries/ --include="*.json" -l

# Search in cross_references arrays specifically
grep -r '"cross_references"' entries/ -A 20 | grep -B 5 '"reading": "たべる"'
```

## Step 2: Update Cross-References in Other Entries

For each entry that references the one being deleted:

### Option A: Remove the cross-reference
If the reference is no longer relevant:

```json
// Before
"cross_references": [
  {"type": "related", "reading": "たべる", "headword": "{食べる|たべる}", "label": "to eat"}
]

// After (remove the reference)
"cross_references": []
```

### Option B: Update to point to replacement entry
If a better entry exists (e.g., after merging duplicates):

```json
// Update the reading/headword/label to match the kept entry
"cross_references": [
  {"type": "related", "reading": "たべる", "headword": "{食べる|たべる}", "label": "to eat"}
]
```

### Option C: Keep as informational reference
If the cross-reference is still useful even without a target entry, you may keep it. The reference will simply not link to anything.

## Step 3: Delete the Entry File

```bash
# Remove the entry file
rm entries/{range}/{entry_id}.json

# Example:
rm entries/04500/04567_taberu.json
```

**Verify deletion**:
```bash
ls entries/04500/04567_taberu.json  # Should return "No such file"
```

## Step 4: Update Indexes

Run the index update script:

```bash
python3 build/update_indexes.py
```

This script automatically:
- Removes the entry from `entries_index.json`
- Updates entry counts
- Syncs with `candidate_words.json`

## Step 5: Optionally Re-add to Candidates

If the word should eventually have an entry (just not this flawed one):

1. Check if `update_indexes.py` already re-added it to candidates
2. If not, manually add to `candidate_words.json`:

```json
{
  "reading": "たべる",
  "headword": "食べる",
  "english": "to eat",
  "notes": "Previous entry deleted due to [reason]. Needs new entry."
}
```

## Step 6: Rebuild the Flat File

```bash
python3 build/build_flat.py
```

This updates the website data. Without this step, the deleted entry may still appear on the live site.

## Step 7: Validate

```bash
python3 build/validate.py
```

Confirm:
- No errors about missing files
- No broken cross-references (if you updated them)
- Entry count matches expected total

## Complete Workflow Example

```bash
# 1. Note the entry to delete
# ID: 04567_taberu, Reading: たべる, Path: entries/04500/04567_taberu.json

# 2. Find cross-references
grep -r '"reading": "たべる"' entries/ --include="*.json" -l

# 3. Update any cross-references found (edit those files)

# 4. Delete the entry
rm entries/04500/04567_taberu.json

# 5. Update indexes
python3 build/update_indexes.py

# 6. Rebuild flat file
python3 build/build_flat.py

# 7. Validate
python3 build/validate.py

# 8. Commit changes
git add entries/ docs/ *.json PROJECT_STATUS.md
git commit -m "Remove duplicate/erroneous entry: 04567_taberu"
git push
```

## Cross-Reference Format Reference

When updating cross-references, use this format:

```json
{
  "type": "related",       // or: pair, antonym, keigo, synonym, contrast, see_also
  "reading": "よむ",        // hiragana reading
  "headword": "{読む|よむ}", // with furigana (for disambiguation)
  "label": "to read"       // optional human-readable label
}
```

**Cross-reference types**:
- `pair` - Transitive/intransitive verb pairs
- `antonym` - Opposite meanings
- `keigo` - Honorific/humble equivalents
- `synonym` - Similar meanings
- `contrast` - Often confused words
- `related` - Semantically related
- `see_also` - General reference

## Troubleshooting

### "Entry still appears on website"
- Did you run `build_flat.py`?
- Clear browser cache or check `docs/flat_dictionary.json`

### "Validation shows broken cross-reference"
- Search for the deleted entry's reading in all files
- Update or remove stale references

### "Index counts don't match"
- Run `update_indexes.py` again
- Check for orphaned files in entries directory

## Safety Notes

1. **Always back up first** if deleting multiple entries:
   ```bash
   git stash  # or commit current state first
   ```

2. **Delete one at a time** when learning - run validation after each

3. **Never delete without checking cross-references** - broken links degrade dictionary quality

4. **Document deletions** in commit messages for future reference
