---
name: cross-reference-entry
description: Guidelines for adding and maintaining cross-references between dictionary entries. Covers reference types, format requirements, and extraction from notes.
---

# Cross-Reference Entry Guidelines

When creating or revising entries, add cross-references to related vocabulary. This improves navigation and helps learners understand word relationships.

## Cross-Reference Types

### 1. `pair` - Transitivity Pairs (HIGH PRIORITY)
Use for verb transitivity pairs ({自動詞|じどうし}/{他動詞|たどうし}).

```json
{
  "type": "pair",
  "reading": "しまる",
  "headword": "{閉|し}まる",
  "label": "intransitive"
}
```

**Labels:** `intransitive` or `transitive`

**Common pairs:**
- 開く/開ける, 閉まる/閉める, 始まる/始める
- 出る/出す, 入る/入れる, 付く/付ける
- 決まる/決める, 変わる/変える, 上がる/上げる

### 2. `antonym` - Opposites (HIGH PRIORITY)
Use for direct opposites.

```json
{
  "type": "antonym",
  "reading": "あける",
  "headword": "{開|あ}ける",
  "label": "to open"
}
```

**Label:** Brief gloss of target word

### 3. `keigo` - Honorific/Humble Forms (HIGH PRIORITY)
Use for formal speech equivalents.

```json
{
  "type": "keigo",
  "reading": "めしあがる",
  "headword": "{召|め}し{上|あ}がる",
  "label": "honorific"
}
```

**Labels:** `honorific` or `humble`

**Common keigo links:**
- 食べる → 召し上がる (hon.), いただく (hum.)
- 行く → いらっしゃる (hon.), 参る (hum.)
- 言う → おっしゃる (hon.), 申す (hum.)
- 見る → ご覧になる (hon.), 拝見する (hum.)

### 4. `synonym` - Similar Meaning (MEDIUM PRIORITY)
Use for words with similar meaning but different nuance.

```json
{
  "type": "synonym",
  "reading": "りかいする",
  "headword": "{理解|りかい}する",
  "label": "formal"
}
```

**Label:** Distinguishing characteristic (e.g., "formal", "written", "casual")

### 5. `contrast` - Easily Confused (MEDIUM PRIORITY)
Use for words learners often confuse.

```json
{
  "type": "contrast",
  "reading": "が",
  "headword": "が",
  "label": "subject marking"
}
```

Especially important for:
- Particles: は vs が, に vs で, に vs へ
- Similar verbs: 聞く vs 聴く, 見る vs 見える vs 見せる

### 6. `related` - Semantically Connected (LOW PRIORITY)
Use for derived words, compounds, or thematically related vocabulary.

```json
{
  "type": "related",
  "reading": "たべもの",
  "headword": "{食|た}べ{物|もの}",
  "label": "food (noun)"
}
```

### 7. `see_also` - General Reference (LOW PRIORITY)
Use for general cross-references that don't fit other categories.

```json
{
  "type": "see_also",
  "reading": "しょくじ",
  "headword": "{食事|しょくじ}",
  "label": null
}
```

## Format Requirements

Each cross-reference object requires:

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | One of: pair, synonym, antonym, keigo, related, see_also, contrast, homophone |
| `target_id` | No | Hard-coded entry ID for direct resolution (takes priority over reading/headword) |
| `reading` | Yes | Hiragana reading (fallback lookup key when no target_id) |
| `headword` | Yes* | Display form with furigana (required for homonym disambiguation) |
| `label` | No | Short descriptor |

*Headword is **required** for proper resolution. Without it, cross-references cannot be disambiguated between homonyms.

**Note:** Valid cross-reference types are defined centrally in `build/constants.py` and shared across the schema, validation, and build scripts.

## Hybrid Cross-Reference System

The dictionary uses a **hybrid system** that supports both:
1. **Hard-coded `target_id`** - Direct reference to an entry ID (unambiguous)
2. **Forward references** - References by reading/headword to entries that may not exist yet

### Resolution Priority

When resolving a cross-reference:
1. If `target_id` present AND entry exists → **resolved** (use ID directly)
2. If `target_id` present AND entry missing → **ERROR** (stale reference)
3. If no `target_id` → resolve by reading/headword (may be pending if target doesn't exist)

### When to Use `target_id`

**Use `target_id` when:**
- The target entry exists in the dictionary
- You want guaranteed, unambiguous resolution
- The reference was previously validated

**Don't manually add `target_id` when:**
- Creating forward references to entries that don't exist yet
- You're unsure which homonym is correct

Instead, use the `harden_references.py` script to automatically add `target_id` to resolvable references.

### Example with target_id

```json
{
  "type": "pair",
  "target_id": "00754_shimaru",
  "reading": "しまる",
  "headword": "{閉|し}まる",
  "label": "intransitive"
}
```

### Example forward reference (no target_id)

```json
{
  "type": "antonym",
  "reading": "ひらく",
  "headword": "{開|ひら}く",
  "label": "to open"
}
```

## Homonym Disambiguation

**CRITICAL**: Many Japanese words share the same reading but have different kanji (homonyms). The headword field is essential for correct resolution.

Example: The reading かんじょう has multiple entries:
- {感情|かんじょう} - emotion, feeling
- {勘定|かんじょう} - bill, calculation

If you reference かんじょう without specifying the headword, the system cannot determine which entry you mean.

**Always include the headword** to ensure cross-references link to the correct entry.

```json
// CORRECT - specifies headword for disambiguation
{
  "type": "synonym",
  "reading": "かんじょう",
  "headword": "{勘定|かんじょう}",
  "label": "bill, calculation"
}

// INCORRECT - no headword, may link to wrong homonym
{
  "type": "synonym",
  "reading": "かんじょう",
  "label": "bill, calculation"
}
```

**Validation detects homonym mismatches**: When you specify a headword that doesn't match any existing entry with that reading (e.g., 勘定 when only 感情 exists), the validator will warn you. This indicates either:
1. The target entry doesn't exist yet (forward reference - OK)
2. The headword is incorrect (fix it)

## Priority Order

When adding references to entries, prioritize:

1. **HIGH** - Always add if applicable:
   - Transitivity pairs (pair)
   - Keigo equivalents (keigo)
   - Direct antonyms (antonym)

2. **MEDIUM** - Add when natural:
   - Close synonyms with clear distinction (synonym)
   - Particle contrasts (contrast)
   - Related compounds (related)

3. **LOW** - Add sparingly:
   - Thematic groupings
   - General see_also references

## Extracting from Notes

The notes field often contains vocabulary that should be cross-referenced. Look for:

### Patterns to Extract

1. **Pair verbs:**
   - "Pair: {閉|し}まる" or "PAIR VERB: ..."
   - "The intransitive counterpart is ..."

2. **Antonyms:**
   - "Opposite: {開|あ}ける"
   - "Antonym: ..."

3. **Keigo:**
   - "{召|め}し{上|あ}がる (honorific)"
   - "Humble form: いただく"

4. **Related words:**
   - Words in furigana notation within COMMON PATTERNS
   - Nouns derived from verbs: 食べる → 食べ物

### Automated Extraction

Run the extraction script to find potential references:

```bash
# Dry run - see proposed changes
python3 build/extract_references.py

# Apply changes
python3 build/extract_references.py --apply

# Single entry
python3 build/extract_references.py --id 00396_taberu
```

**Note:** The extraction script now performs immediate resolution. When a target entry exists, the extracted reference automatically includes `target_id`.

### Hardening References

The `harden_references.py` script scans entries and adds `target_id` to resolvable cross-references. This "hardens" forward references into direct ID-based references once the target entry exists.

```bash
# Dry run - see what would change
python3 build/harden_references.py

# Apply changes
python3 build/harden_references.py --apply

# Single entry
python3 build/harden_references.py --id 00485_shimeru
```

**When to run:**
- After adding new entries that are targets of existing forward references
- Periodically to ensure all resolvable references have `target_id`
- Before releases to maximize resolution coverage

**The script will:**
- Add `target_id` to unambiguously resolvable references
- WARN about ambiguous references (multiple candidates, need headword)
- ERROR on stale `target_id` references (target no longer exists)
- Skip forward references (legitimate refs to non-existent entries)

## Handling Non-Existent Entries

**Important:** You can add references to entries that don't exist yet.

- Use `reading` as the primary key (required)
- Include `headword` for display purposes
- The link will be marked as "pending" in the web interface
- When the target entry is created, the link automatically becomes active

This allows you to:
- Plan future entries
- Track vocabulary relationships before full coverage
- Show learners related vocabulary even if not yet in dictionary

## Validation

After adding references, validate:

```bash
python3 build/validate.py --id {entry_id}
```

The validator checks:
- Required fields present (type, reading)
- Valid type values
- Reading is valid hiragana
- No self-references
- **Homonym mismatches** - warns when a headword is specified but doesn't match any existing entry with that reading
- **Stale target_id** - ERRORS when `target_id` points to a non-existent entry
- **Hardenable references** - warns when a reference could be hardened (target exists but no `target_id`)

### Validation Messages

| Type | Meaning | Action |
|------|---------|--------|
| ERROR: Stale target_id | `target_id` points to deleted entry | Remove or update `target_id` |
| WARNING: Hardenable | Reference resolvable but missing `target_id` | Run `harden_references.py --apply` |
| WARNING: Homonym mismatch | Headword doesn't match any entry with that reading | Verify correct homonym or wait for entry creation |

## Example Entry

Before:
```json
{
  "id": "00485_shimeru",
  "cross_references": []
}
```

After:
```json
{
  "id": "00485_shimeru",
  "cross_references": [
    {
      "type": "pair",
      "reading": "しまる",
      "headword": "{閉|し}まる",
      "label": "intransitive"
    },
    {
      "type": "antonym",
      "reading": "あける",
      "headword": "{開|あ}ける",
      "label": "to open"
    }
  ]
}
```

## Quality Checklist

- [ ] Transitivity pair linked (for verbs)
- [ ] Keigo forms linked (for common verbs)
- [ ] Antonyms linked (if obvious opposite exists)
- [ ] References in notes are also in cross_references
- [ ] Each reference has correct type
- [ ] Reading is valid hiragana
- [ ] Headword uses proper furigana notation
- [ ] Labels are concise and consistent
