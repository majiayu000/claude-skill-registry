---
name: adjective-entry
description: Requirements for creating or revising adjective entries in je-dict-1. Covers forms, conjugations, predicate vs modifier usage, and similar word distinctions.
---

# Adjective Entry Requirements

**Reminder:** Write each entry individually by hand. Do not use scripts to mass-produce entries. See `entry-guidelines` skill.

When creating or revising ADJECTIVE entries (both i-adjectives and na-adjectives), include all of the following:

## Required Sections

### 1. Forms Information (MEDIUM PRIORITY)
Include derived forms where natural:

```
FORMS:
- Adverbial: {遠|とお}く (i-adj) / {静|しず}かに (na-adj)
- Noun form: {遠|とお}さ (where natural)
```

**Note:** Not all adjectives have natural noun forms. Only include if commonly used.

### 2. Conjugation Paradigm (MEDIUM PRIORITY)
Show key conjugations:

```
CONJUGATION:
- Negative: {遠|とお}くない / {静|しず}かではない
- Te-form: {遠|とお}くて / {静|しず}かで
- Past: {遠|とお}かった / {静|しず}かだった
```

### 3. Predicate vs. Modifier Usage (MEDIUM PRIORITY)
Indicate which form is more common:

```
USAGE PATTERN:
- More common as: Predicate / Modifier / Equal
- Example: この{道|みち}は{遠|とお}い (predicate) vs. {遠|とお}い{道|みち} (modifier)
```

### 4. Similar Words Section (MEDIUM PRIORITY)
For adjectives with semantic overlap, include distinctions:

```
SIMILAR WORDS:
- {楽|らく} vs. {簡単|かんたん} vs. {易|やさ}しい
  - {楽|らく}: comfortable, at ease (subjective feeling)
  - {簡単|かんたん}: simple, straightforward (objective complexity)
  - {易|やさ}しい}: gentle, easy to understand (approachable)
```

**Key adjective groups to distinguish:**
- {嬉|うれ}しい vs. {楽|たの}しい (happiness vs. enjoyment)
- {怖|こわ}い vs. {恐|おそ}ろしい (scared vs. terrifying)
- {大きい|おおきい} vs. {広|ひろ}い (big vs. spacious)
- {新|あたら}しい vs. {若|わか}い (new vs. young)
- {難|むずか}しい vs. {大変|たいへん} (difficult vs. hard/serious)

### 5. Register Label (MEDIUM PRIORITY)
Mark as: Casual / Neutral / Formal / Emphatic

Example: すごい - [Register: Casual/Emphatic]

## Low Priority Sections

### 6. Kanji Orthography Notes
When kanji vs. hiragana matters:

```
ORTHOGRAPHY:
- すごい is commonly written in hiragana; {凄|すご}い appears in formal writing
- {可愛|かわい}い vs. かわいい - both common
```

## Template for Notes Section

**Important:** Follow the formatting guidelines in the `vocabulary-notes` skill for proper structure.

```
[Adjective] is an [i-adjective/na-adjective].

FORMS:
- Adverbial: [form]
- Noun form: [form] (if natural)

SIMILAR WORDS:
- [word 1] vs. [word 2]: [distinction]

[Register notes if applicable]

[Any special usage patterns or restrictions]
```

## I-Adjective vs. Na-Adjective Specifics

### I-Adjectives
- End in い (but not all い-ending words are i-adjectives)
- Conjugate directly: {高|たか}い → {高|たか}くない
- Connect with くて: {高|たか}くて{広|ひろ}い

### Na-Adjectives
- Require な before nouns: {静|しず}かな{部屋|へや}
- Use で to connect: {静|しず}かで{広|ひろ}い
- Negative with ではない/じゃない

### Special Cases
- {きれい|綺麗} - na-adjective despite ending in い
- {嫌|きら}い - na-adjective
- Note these exceptions explicitly in entries

## Example Sentences

**See the `example-sentences` skill for complete requirements including:**
- Minimum counts: 5 examples per sense (basic/core) or 3 (general)
- Progressive length: Examples should get longer from first to last
- Vocabulary restrictions by tier
- Quality standards and formatting

### Sense Numbers in Examples

For adjectives with multiple senses, each example must include a `sense_numbers` field:

```json
"examples": [
  {
    "id": "00001_adj_ex1",
    "japanese": "...",
    "english": "...",
    "sense_numbers": [1]
  }
]
```

**Adjective-specific guidelines:**
- Examples demonstrating predicate vs. modifier usage typically share the same sense
- Different nuances of meaning (e.g., physical vs. emotional) may require separate senses
- Figurative or extended meanings should have their own sense numbers
- Show both predicate form (Xは{adj}) and modifier form ({adj}+noun)
- Demonstrate adverbial form usage where natural

## Required Tags for Adjectives

All adjective entries must include these tags in `metadata.tags`:

```json
"metadata": {
  "tags": {
    "pos": ["adjective-i"],           // adjective-i, adjective-na, adjective-no, adjective-taru
    "formality": "neutral",           // formal, neutral, informal, vulgar
    "politeness": "plain",            // honorific, humble, polite, plain
    "semantic": ["descriptive"]       // Choose appropriate category
  }
}
```

**POS tag values for adjectives:**
- `adjective-i`: い-adjectives (高い, 大きい, 美しい)
- `adjective-na`: な-adjectives (静か, 便利, きれい)
- `adjective-no`: の-adjectives (本当の, 普通の)
- `adjective-taru`: たる-adjectives (堂々たる, 悠々たる) - literary/formal

**Semantic categories for adjectives:**
- `emotion`: 嬉しい, 悲しい, 怖い (feelings)
- `size`: 大きい, 小さい, 長い, 高い (dimensions)
- `color`: 赤い, 青い, 白い (colors)
- `descriptive`: Fallback for adjectives not fitting specific categories

## Quality Checklist for Adjectives

- [ ] **All kanji have furigana** (headword, examples, AND notes)
- [ ] Verify: `python3 build/verify_furigana.py <entry_id>` shows "✓ OK"
- [ ] **Tags complete**: pos, formality, politeness, semantic
- [ ] Part of speech correctly identified (i-adj vs. na-adj)
- [ ] Adverbial form provided
- [ ] Key conjugations shown
- [ ] Similar words distinguished (if applicable)
- [ ] Examples show both predicate and modifier uses
- [ ] Register noted if not neutral
- [ ] Special cases (きれい, 嫌い type) flagged if applicable
- [ ] All examples have valid sense_numbers
