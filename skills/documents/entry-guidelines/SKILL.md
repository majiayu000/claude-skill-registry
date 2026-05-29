---
name: entry-guidelines
description: General quality standards for all je-dict-1 dictionary entries. Use when creating or revising any entry type.
---

# Dictionary Entry Quality Guidelines

When creating or revising dictionary entries for je-dict-1, follow these quality standards:

## CRITICAL: Write Each Entry Individually

**DO NOT use Python scripts or automation to mass-produce entries.**

Each dictionary entry must be written individually by hand, using:
- Your own linguistic knowledge
- The guidelines in this skill and related skills (`verb-entry`, `adjective-entry`, `particle-entry`, `other-entries`, `vocabulary-notes`)
- Careful consideration of each word's unique characteristics

**Why this matters:**
- Each word has nuances that require individual attention
- Examples must be natural and contextually appropriate
- Notes should address learner-specific challenges for that word
- Mass-produced entries lack the quality and depth learners need

**The correct workflow:**
1. Select a word from `candidate_words.json` or user request
2. Research/consider the word's usage, collocations, and common patterns
3. Write the entry JSON directly using the Write tool
4. Validate: `python3 build/validate.py`
5. Repeat for each entry

**After finishing all entries for a session:**
```bash
python3 build/validate.py           # Validate all entries
python3 build/update_indexes.py     # Update indexes and sync candidates
python3 build/build_flat.py         # Rebuild website (REQUIRED for GitHub Pages)
git add entries/ docs/ *.json PROJECT_STATUS.md
git commit -m "Add N new dictionary entries"
git push
```
The `build_flat.py` step is critical - without it, new entries won't appear on the live site. The build uses an atomic process (builds to temp directory, then swaps) to prevent broken states if the build fails.

**Never create scripts that generate entry content programmatically.**

## Before Creating a New Entry

**IMPORTANT**: Always check if an entry already exists before creating a new one.

1. **Run the duplicate check script**:
   ```bash
   python3 build/check_duplicate.py "食べる" "たべる"
   ```

   - If it says "OK: ... is not in the dictionary or candidates" → Safe to create entry
   - If it says "DUPLICATE: ..." → SKIP this word, do NOT create a duplicate

2. **Batch checking** (optional, to plan which candidates to work on):
   ```bash
   python3 build/check_duplicate.py --batch "食べる:たべる" "飲む:のむ" "書く:かく"
   ```

3. **If the word was in candidate_words.json**: It will be automatically removed when you run `python3 build/update_indexes.py` after creating the entry.

4. **Only create new entries** for words that pass the duplicate check.

This prevents duplicate entries and wasted effort on entries that must later be deleted.

## Content Guidelines

1. **Explain before exemplifying** - Definition first, then examples
2. **One meaning = one example minimum** - Every sense needs illustration
3. **Show grammatical connections** - Always demonstrate how words connect
4. **Prefer natural Japanese** - Avoid textbook stiffness
5. **Highlight non-obvious distinctions** - Focus on what learners cannot infer from English

## Consistency Guidelines

1. **Consistent depth across similar entries** - Don't over-explain one verb while under-explaining another
2. **Consistent structure within entry types** - All verbs should have same sections
3. **Consistent terminology** - Use same labels throughout (USAGE NOTES, not sometimes Notes)

## Example Sentence Guidelines

**See the `example-sentences` skill for complete guidelines on:**
- Minimum example counts per tier (5 for basic/core, 3 for general)
- Progressive length requirements
- Vocabulary restrictions by tier
- Quality standards and formatting

### Key Requirements Summary

1. **Minimum counts**: Basic/core tiers need 5 examples per sense; general tier needs 3
2. **Progressive length**: Examples should get longer from first to last
3. **Vocabulary restrictions**: Basic tier examples must use tier-appropriate vocabulary
4. **Always include sense_numbers**: Every example must specify which definition sense(s) it illustrates

### Sense Numbers Requirement

Every example sentence **must** have a `sense_numbers` field that links it to the definition(s) it illustrates:

```json
"examples": [
  {
    "id": "00001_word_ex1",
    "japanese": "...",
    "english": "...",
    "sense_numbers": [1]
  }
]
```

**Rules:**
- **Single-sense entries**: Use `[1]` for all examples
- **Multi-sense entries**: Each example must specify which sense(s) it demonstrates
- **Examples illustrating multiple senses**: Use `[1, 2]` format
- **Must reference valid senses**: Numbers must match `sense_number` values in definitions

The validation script checks that all examples in multi-sense entries have valid sense_numbers.

## Furigana Requirements (CRITICAL)

**All kanji MUST have furigana in ALL fields, including notes.**

Format: `{漢字|かんじ}`

This applies to:
- Headwords
- Example sentences
- **Notes field** (idioms, collocations, cultural notes, etc.)
- All explanatory text

**Common mistakes to avoid:**
```
✗ WRONG: 暖簾に腕押し
✓ RIGHT: {暖簾|のれん}に{腕押|うでお}し

✗ WRONG: 安堵の息をつく
✓ RIGHT: {安堵|あんど}の{息|いき}をつく

✗ WRONG: Sometimes written as 家鴨
✓ RIGHT: Sometimes written as {家鴨|あひる}
```

Use compound readings for jukugo: `{友達|ともだち}` not `{友|とも}{達|だち}`

**Verify before finalizing:**
```bash
python3 build/verify_furigana.py <entry_id>
```

## Entry Structure

Every entry must include:
- `id`: Format `{5-digit-number}_{romaji}` (e.g., `00396_taberu`)
- `headword`: With furigana notation
- `reading`: **Hiragana only** (see Reading Format below)
- `part_of_speech`: Consistent terminology
- `gloss`: Brief English equivalent
- `definitions`: Array with sense_number, gloss, explanation
- `examples`: 2-3 minimum, with id, Japanese, English, sense_numbers, and optional notes
- `notes`: Usage notes, grammar patterns, common mistakes (see `vocabulary-notes` skill for formatting requirements)
- `metadata`: Including vocabulary_tier (**always "general" for new entries**), created, modified timestamps

## Reading Format (CRITICAL)

**All readings MUST be in hiragana, never katakana.**

This applies to ALL entries, including:
- Loanwords (katakana headwords like スキー, ストレージ)
- Abbreviations (DM, PC, etc.)
- Any word regardless of how the headword is written

**Examples:**
```
✓ CORRECT:
  headword: "スキー"
  reading: "すきー"

✓ CORRECT:
  headword: "DM"
  reading: "でぃーえむ"

✗ WRONG:
  headword: "スキー"
  reading: "スキー"  ← Katakana readings cause duplicates!
```

**Why this matters:**
- Katakana readings cause duplicate entries (same word with two different reading formats)
- The dictionary uses readings for indexing and deduplication
- Consistent hiragana readings ensure proper sorting and lookup

**Note:** The long vowel mark `ー` is acceptable in hiragana readings (e.g., `すきー`, `すとれーじ`) since there is no hiragana equivalent.

The validation script (`validate.py`) will report errors for entries with katakana readings.

## File Placement (CRITICAL)

**Entries MUST be placed in the correct numeric range directory.**

The path follows this pattern: `entries/{range}/{entry_id}.json`

The **range directory** is determined by the numeric portion of the entry ID, rounded down to the nearest 500:
- IDs 00000-00499 → `entries/00000/`
- IDs 00500-00999 → `entries/00500/`
- IDs 01000-01499 → `entries/01000/`
- etc.

### Examples

- Entry `00396_taberu` → `entries/00000/00396_taberu.json`
- Entry `00538_aruku` → `entries/00500/00538_aruku.json`
- Entry `01186_mukau` → `entries/01000/01186_mukau.json`
- Entry `06237_fumikiru` → `entries/06000/06237_fumikiru.json`

### How to Get the Correct Path

**ALWAYS run this command** to determine the correct path before writing:

```bash
python3 build/get_entry_path.py <reading> <entry_id>
```

Example:
```bash
python3 build/get_entry_path.py ふみきる 06237_fumikiru
# Output: entries/06000/06237_fumikiru.json

python3 build/get_entry_path.py こうりつてき 06240_kouritsuteki
# Output: entries/06000/06240_kouritsuteki.json
```

The `validate.py` script checks for directory mismatches and will report errors.

## Metadata Timestamps

**CRITICAL**: Timestamps MUST be actual current UTC time. The website converts UTC to JST (+9 hours) for display. Incorrect timestamps will show as wrong dates/times (often appearing hours or days in the future).

### How to Get the Correct Timestamp

**ALWAYS run this command** to get the current UTC timestamp before writing each entry:

```bash
python3 build/get_timestamp.py
```

This outputs the current UTC time, e.g.: `2026-01-12T10:45:30Z`

Copy this exact output into both `created` and `modified` fields (for new entries) or just `modified` (for revisions).

### Why This Matters

- The `Z` suffix means UTC (not local time, not JST)
- The build script adds 9 hours to convert to JST for display
- If you write `16:00:00Z` when actual UTC is `10:00`, it displays as **01:00 JST next day** (wrong!)
- If you write `10:00:00Z` when actual UTC is `10:00`, it displays as **19:00 JST same day** (correct!)

### Common Mistakes to Avoid

1. **DO NOT** guess or estimate the timestamp
2. **DO NOT** use your perception of current time - always run the script
3. **DO NOT** use round hours like `12:00:00Z` or `15:00:00Z` (these are almost certainly wrong)
4. **DO NOT** copy timestamps from other entries
5. **DO NOT** write JST time with a Z suffix (this causes 9-hour errors)

### Validation

Run `python3 build/validate.py` to check for:
- Future timestamps (timestamp more than 24 hours ahead of current UTC time)
- Suspiciously round timestamps (exactly `:00:00` seconds, likely not from the script)

Note: The validator allows a 24-hour grace period for timestamps to accommodate CI/CD clock drift.

## Vocabulary Tier Policy

**All new entries must be assigned to the "general" tier.**

As of January 2026, the vocabulary tier realignment is complete:
- **Basic tier** (795 entries): Fixed - contains foundational vocabulary
- **Core tier** (1,998 entries): Fixed - contains essential adult communication vocabulary
- **General tier** (4,566+ entries): All other vocabulary, including all new entries

**Do NOT assign new entries to basic or core tiers** unless explicitly instructed by the user. The basic and core tiers have been curated to meet specific word count targets and maintain semantic group integrity.

In `metadata.vocabulary_tier`, always use `"general"`:
```json
"metadata": {
  "vocabulary_tier": "general",
  "created": "...",
  "modified": "..."
}
```

## Metadata Tags (REQUIRED)

All entries must have properly structured tags in `metadata.tags`. This enables search, filtering, and export functionality.

### Required Tag Categories

```json
"metadata": {
  "vocabulary_tier": "general",
  "tags": {
    "pos": ["noun"],                    // REQUIRED: Part of speech (array)
    "formality": "neutral",             // REQUIRED: formal/neutral/informal/vulgar
    "politeness": "plain",              // REQUIRED: honorific/humble/polite/plain
    "semantic": ["food"]                // REQUIRED: Semantic category (array)
  },
  "created": "...",
  "modified": "..."
}
```

### Part of Speech (`pos`)

Valid values: `noun`, `verb-godan`, `verb-ichidan`, `verb-suru`, `verb-kuru`, `verb-irregular`, `adjective-i`, `adjective-na`, `adjective-no`, `adjective-taru`, `adverb`, `particle`, `conjunction`, `interjection`, `pronoun`, `counter`, `prefix`, `suffix`, `expression`, `pre-noun-adjectival`, `number`, `onomatopoeia`, `auxiliary`

- Use arrays for multi-function words: `["noun", "verb-suru"]`
- The array should list the most common/primary POS first

### Formality

- `formal`: Used in formal/written contexts (敬語, 硬い表現)
- `neutral`: Standard usage appropriate for most contexts (default)
- `informal`: Casual/colloquial usage (くだけた表現)
- `vulgar`: Strong/offensive language (use sparingly)

### Politeness (Keigo Classification)

- `honorific`: 尊敬語 - Elevates the subject (いらっしゃる, おっしゃる)
- `humble`: 謙譲語 - Lowers the speaker (申す, 参る)
- `polite`: 丁寧語 - General polite forms (です/ます base forms)
- `plain`: 普通体 - Plain/dictionary forms (default for most entries)

### Semantic Categories

Choose the most appropriate category(ies) for the word's meaning:

**Specific categories** (use when applicable):
- Time: `time-day-of-week`, `time-month`, `time-season`, `time-period`, `time-general`
- Nature: `animal-mammal`, `animal-bird`, `animal-fish`, `animal-insect`, `animal-general`, `plant-tree`, `plant-flower`, `plant-general`, `weather`, `geography`
- Human: `body-part`, `body-internal`, `family`, `person`, `occupation`
- Objects: `food`, `clothing`, `building`, `transportation`, `tool`, `furniture`, `electronics`
- Abstract: `emotion`, `color`, `number`, `direction`, `size`, `quantity`
- Actions: `movement`, `communication`, `cognition`, `existence`, `consumption`
- Social: `greeting`, `education`, `work`, `leisure`

**Fallback categories** (when no specific category fits):
- `general`: For nouns without a specific semantic category
- `action`: For verbs not fitting other action categories
- `descriptive`: For adjectives and adverbs
- `grammatical`: For particles and conjunctions
- `expression`: For fixed expressions and interjections
- `onomatopoeia`: For mimetic words

### Optional Tag Categories

```json
"tags": {
  // ... required tags above ...
  "transitivity": "transitive",     // For verbs: transitive/intransitive/both
  "style": ["spoken"],              // written/spoken/literary/archaic/slang
  "domain": ["business"]            // business/academic/technical/legal/medical/etc.
}
```

- `transitivity`: Required for verbs - indicates if verb takes a direct object
- `style`: Use when word is strongly associated with a medium
- `domain`: Use when word is specialized/technical

### Tag Selection Tips

1. **Be specific when possible**: Use `food` not `general` for 寿司
2. **Multiple tags allowed**: 朝ご飯 can be `["food", "time-period"]`
3. **Match the primary meaning**: Tag based on the word's core meaning
4. **Check similar entries**: Ensure consistency with related words

## Quality Checklist

Before finalizing any entry, verify:
- [ ] **File placed in correct directory** (use `python3 build/get_entry_path.py <reading> <entry_id>`)
- [ ] **All kanji have furigana** (headword, examples, AND notes)
- [ ] Verify: `python3 build/verify_furigana.py <entry_id>` shows "✓ OK"
- [ ] **Tags are complete**: pos, formality, politeness, semantic all present
- [ ] Examples progress from simple to complex
- [ ] At least one collocation or fixed phrase is shown
- [ ] Grammar patterns are explicitly demonstrated
- [ ] Notes cover common learner mistakes
- [ ] Notes are properly formatted (see `vocabulary-notes` skill)
- [ ] Depth matches similar entries in the dictionary
- [ ] All examples have valid sense_numbers
- [ ] Run `python3 build/validate.py` to catch any directory or other errors
