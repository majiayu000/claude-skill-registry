---
name: example-sentences
description: Requirements for creating and revising example sentences in je-dict-1. Covers minimum counts, progressive length, vocabulary restrictions by tier, and quality standards.
---

# Example Sentence Guidelines

This skill defines the standards for example sentences across all dictionary entries. All entry-creation and revision activities must follow these guidelines.

---

## Minimum Example Counts by Tier

### Basic and Core Tiers

Every sense of every entry in the basic and core tiers must have **at least 5 example sentences**.

| Tier | Minimum Examples per Sense |
|------|---------------------------|
| Basic | 5 |
| Core | 5 |

### General Tier

Every sense of every entry in the general tier must have **at least 3 example sentences**.

| Tier | Minimum Examples per Sense |
|------|---------------------------|
| General | 3 |

**Multi-sense entries:** The requirements apply per sense. An entry with 3 senses in the basic tier needs at least 15 examples total (5 per sense).

---

## Progressive Length Requirement

Examples within each sense should progress from shorter to longer:

1. **Example 1**: Short and simple - demonstrates the word clearly
2. **Example 2**: Slightly longer - shows basic context
3. **Example 3**: Medium length - natural usage with fuller context
4. **Example 4** (basic/core): Longer sentence with more complex structure
5. **Example 5** (basic/core): Longest - may consist of 2-3 short sentences or one longer sentence with relative clauses, compound structures, etc.

**Key principle:** Early examples help learners recognize the word; later examples show how the word functions in natural, flowing Japanese.

### Length Guidelines

| Example | Target Length (Japanese) |
|---------|-------------------------|
| 1 | 5-15 characters |
| 2 | 10-20 characters |
| 3 | 15-30 characters |
| 4 | 25-45 characters |
| 5+ | 35-70 characters (or 2-3 short sentences) |

These are guidelines, not strict rules. Natural expression takes priority over hitting exact character counts.

---

## Vocabulary Restrictions by Tier

### Basic Tier Entries

For entries in the **basic** vocabulary tier:

| Examples | Vocabulary Restriction |
|----------|----------------------|
| 1-2 | **Basic tier only** - Use only words from the basic tier |
| 3-5 | **Basic + Core tiers** - May use basic and core vocabulary |

**Critical:** Basic tier examples must contain **no general-tier or unlisted vocabulary**. This ensures learners at the basic level can fully understand all examples without encountering unknown words.

### Core Tier Entries

For entries in the **core** vocabulary tier:

| Examples | Vocabulary Restriction |
|----------|----------------------|
| 1-2 | **Basic + Core tiers** - Use only basic or core vocabulary |
| 3-5 | **No restriction** - May use any vocabulary |

**Recommendation:** Even for unrestricted examples (3-5), avoid vocabulary that is not in the dictionary. Learners should be able to look up any unfamiliar word.

### General Tier Entries

For entries in the **general** vocabulary tier:

| Examples | Vocabulary Restriction |
|----------|----------------------|
| 1-3+ | **No restriction** - May use any vocabulary |

**Recommendation:** Avoid obscure vocabulary not in the dictionary. Use common, natural expressions that learners are likely to encounter.

---

## Vocabulary Tier Verification

When creating examples for basic and core tier entries, verify vocabulary tier compliance:

```bash
# Check if a word is in the dictionary and its tier
python3 build/check_duplicate.py "word" "reading"
```

For systematic verification during polishing:
- Read the example sentence
- Identify all content words (nouns, verbs, adjectives, adverbs)
- Verify each word is in the appropriate tier
- Replace non-compliant words with tier-appropriate alternatives

**Common substitution patterns:**

| Non-compliant | Basic alternative | Core alternative |
|--------------|-------------------|------------------|
| {購入|こうにゅう}する | {買|か}う | {買|か}う |
| {使用|しよう}する | {使|つか}う | {使|つか}う |
| {非常|ひじょう}に | とても | とても/{大変|たいへん} |
| {困難|こんなん} | {難|むずか}しい | {難|むずか}しい |

---

## Sense Numbers Requirement

Every example **must** include a `sense_numbers` field linking it to the definition(s) it illustrates.

```json
"examples": [
  {
    "id": "00001_word_ex1",
    "japanese": "...",
    "english": "...",
    "sense_numbers": [1],
    "has_audio": false,
    "notes": null
  }
]
```

### Rules

- **Single-sense entries**: Use `[1]` for all examples
- **Multi-sense entries**: Each example must specify which sense(s) it demonstrates
- **Examples illustrating multiple senses**: Use `[1, 2]` format
- **Must reference valid senses**: Numbers must match `sense_number` values in definitions

### Distribution for Multi-Sense Entries

For entries with multiple senses in basic/core tiers:
- Each sense needs at least 5 examples
- Distribute examples to cover all senses adequately
- Some examples may illustrate multiple senses (use `[1, 2]` notation)

---

## Quality Standards

### Essential Requirements

1. **Natural Japanese**: Examples should sound like something a native speaker would say
2. **Clear context**: The usage should be understandable from the example
3. **Complete furigana**: All kanji must have `{kanji|reading}` markup
4. **Accurate translation**: English captures meaning without being overly literal

### Content Quality

1. **First example should be simple** - Demonstrate the word clearly without complexity
2. **Progress to natural complexity** - Later examples show real-world usage
3. **Include fixed phrases** - High-frequency collocations aid memory (at least one per sense)
4. **Show grammatical connections** - Demonstrate how words connect with particles, etc.
5. **Annotate non-obvious grammar** - Use `notes` field for explanations when needed

### What to Demonstrate

Examples should illustrate:
- Common collocations and set phrases
- Typical particle patterns (for verbs)
- Predicate vs. modifier usage (for adjectives)
- Register-appropriate contexts
- Both literal and figurative meanings (if applicable)

---

## Example Format Reference

```json
{
  "id": "00396_taberu_ex1",
  "japanese": "{朝|あさ}ごはんを{食|た}べる。",
  "english": "To eat breakfast.",
  "sense_numbers": [1],
  "has_audio": false,
  "notes": null
}
```

### ID Format

Pattern: `{entry_id}_ex{N}`

- `entry_id`: The entry's ID (e.g., `00396_taberu`)
- `N`: Sequential number starting from 1

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique example ID |
| `japanese` | Yes | Japanese sentence with furigana |
| `english` | Yes | Natural English translation |
| `sense_numbers` | Yes | Array of sense numbers illustrated |
| `has_audio` | Yes | Boolean (usually `false`) |
| `notes` | Yes | Explanatory note or `null` |

---

## Common Issues to Avoid

1. **Missing furigana**: `お金が余った` instead of `お{金|かね}が{余|あま}った`
2. **Overly literal translations**: "As for me, I eat sushi" instead of "I eat sushi"
3. **Wrong sense_numbers**: Example linked to wrong definition
4. **Unnatural constructions**: Grammatically correct but rarely used patterns
5. **Vocabulary tier violations**: Using general-tier words in basic-tier examples 1-2
6. **Insufficient examples**: Not meeting minimum counts per sense
7. **No length progression**: All examples being similar length

---

## Polishing Checklist for Examples

When reviewing or revising examples, verify:

### Count and Distribution
- [ ] Minimum examples per sense met (5 for basic/core, 3 for general)
- [ ] All senses have adequate example coverage
- [ ] Examples are properly distributed across senses

### Progressive Length
- [ ] Examples progress from shorter to longer within each sense
- [ ] Final examples are substantially longer or multi-sentence

### Vocabulary Restrictions
- [ ] Basic tier: Examples 1-2 use only basic vocabulary
- [ ] Basic tier: Examples 3-5 use only basic+core vocabulary
- [ ] Core tier: Examples 1-2 use only basic+core vocabulary
- [ ] No unlisted vocabulary in restricted examples

### Quality
- [ ] All examples sound natural
- [ ] All kanji have complete furigana
- [ ] Translations are accurate and natural
- [ ] sense_numbers are correct for each example
- [ ] At least one example shows a common collocation
- [ ] Grammar patterns are demonstrated clearly

### Format
- [ ] IDs follow `{entry_id}_ex{N}` pattern
- [ ] IDs are sequential (ex1, ex2, ex3...)
- [ ] All required fields present
- [ ] `has_audio` is accurate
- [ ] `notes` field present (null if not needed)

---

## Adding Examples to Existing Entries

When adding examples to bring an entry into compliance:

1. **Read the existing entry** to understand current examples
2. **Identify gaps**: Which senses need more examples? What lengths are missing?
3. **Check vocabulary tier**: Determine what vocabulary can be used
4. **Write new examples** following progressive length guidelines
5. **Verify compliance** with all requirements
6. **Update `modified` timestamp** in metadata

### Example Addition Template

For a basic-tier entry with one sense needing 5 examples:

```
Example 1: [short, basic vocab only]
Example 2: [short-medium, basic vocab only]
Example 3: [medium, basic+core vocab]
Example 4: [medium-long, basic+core vocab]
Example 5: [long or multi-sentence, basic+core vocab]
```

---

## Summary Table

| Tier | Min Examples/Sense | Ex 1-2 Vocab | Ex 3+ Vocab |
|------|-------------------|--------------|-------------|
| Basic | 5 | Basic only | Basic + Core |
| Core | 5 | Basic + Core | Any (prefer dictionary words) |
| General | 3 | Any | Any (prefer dictionary words) |
