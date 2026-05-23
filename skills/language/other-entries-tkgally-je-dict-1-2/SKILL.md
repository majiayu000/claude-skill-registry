---
name: other-entries
description: Requirements for creating nouns, counters, adverbs, and expressions in je-dict-1. Covers collocations, counting patterns, register, and cultural notes.
---

# Other Entry Types: Nouns, Counters, Adverbs, Expressions

**Reminder:** Write each entry individually by hand. Do not use scripts to mass-produce entries. See `entry-guidelines` skill.

Guidelines for entry types not covered by verb, adjective, or particle skills.

**Important:** All notes must follow the formatting guidelines in the `vocabulary-notes` skill (line breaks between sections, bullet points for lists).

---

## NOUN Entries

### Required Information (MEDIUM PRIORITY)

#### 1. Common Collocations
Show typical verb pairings:

```
COMMON COLLOCATIONS:
- {電話|でんわ}をかける (make a phone call)
- {電話|でんわ}に{出|で}る (answer the phone)
- {電話|でんわ}を{切|き}る (hang up the phone)
```

#### 2. Scope Clarification (when needed)
Clarify when Japanese meaning differs from English:

```
SCOPE NOTE:
{手|て} includes both hand and arm up to the shoulder in Japanese,
unlike English "hand" which stops at the wrist.
```

### Low Priority Information

#### 3. Counter Reference
Note which counter(s) to use:

```
COUNTER: {匹|ひき} (for small animals)
```

### Template for Noun Notes

```
[Noun] refers to [definition].

Common expressions:
- [collocation 1]
- [collocation 2]

[Scope clarification if meaning differs from English equivalent]

[Any cultural notes if relevant]
```

---

## COUNTER Entries

### Required Information (MEDIUM PRIORITY)

#### 1. Full Counting Pattern (1-10)
Always include a complete table:

```
COUNTING PATTERN:
1: {一匹|いっぴき}     6: {六匹|ろっぴき}
2: {二匹|にひき}      7: {七匹|ななひき}
3: {三匹|さんびき}    8: {八匹|はっぴき}
4: {四匹|よんひき}    9: {九匹|きゅうひき}
5: {五匹|ごひき}     10: {十匹|じゅっぴき}
```

#### 2. Irregular Readings
Highlight all exceptions clearly:

```
IRREGULAR READINGS:
- 1: いっ~ (sokuon + sound change)
- 3: さんび~ (rendaku)
- 6: ろっ~ (sokuon + sound change)
- 8: はっ~ (sokuon + sound change)
- 10: じゅっ~ (sokuon)
```

#### 3. What It Counts
List what objects/beings use this counter:

```
USED FOR:
- Small animals (dogs, cats, fish, insects)
- NOT used for: birds ({羽|わ}), large animals ({頭|とう})
```

#### 4. Sound Change Patterns
Explain the phonetic rules:

```
SOUND CHANGES:
- After 1, 6, 8, 10: ひき → ぴき (sokuon + h→p)
- After 3: ひき → びき (rendaku)
```

---

## ADVERB Entries

### Required Information

#### 1. Sentence Position
Note where the adverb typically appears:

```
POSITION:
- Usually appears before the verb
- Can appear at sentence start for emphasis
```

#### 2. What It Modifies
Clarify if it modifies verbs, adjectives, or both:

```
MODIFIES:
- Verbs: とても{走|はし}る ✗ (unnatural)
- Adjectives: とても{高|たか}い ✓
- Na-adjectives: とても{静|しず}か ✓
```

#### 3. Register
Many adverbs are register-specific:

```
REGISTER: Casual
- すごく is casual; use とても or {非常|ひじょう}に in formal contexts
```

#### 4. Similar Adverbs
Distinguish from near-synonyms:

```
SIMILAR WORDS:
- とても vs. すごく vs. {非常|ひじょう}に
  - とても: neutral, general intensifier
  - すごく: casual, emphatic
  - {非常|ひじょう}に: formal, written
```

---

## EXPRESSION Entries

### Required Information

#### 1. Situational Context
Explain WHEN to use the expression:

```
WHEN TO USE:
- Said when leaving home/office
- The person staying behind responds with いってらっしゃい
```

#### 2. Register
Expressions are often register-specific:

```
REGISTER: Polite/Neutral
- Used in both casual and polite situations
- More formal: {行|い}ってまいります
```

#### 3. Response Pairs
Many expressions have expected responses:

```
EXCHANGE PATTERN:
A: いただきます (before eating)
B: どうぞ (go ahead) [optional response]

A: ごちそうさまでした (after eating)
B: お{粗末|そまつ}さまでした (humble response, optional)
```

#### 4. Cultural Notes
Explain cultural significance:

```
CULTURAL NOTE:
いただきます literally means "I humbly receive" and expresses
gratitude for the food, the people who prepared it, and the
ingredients themselves. It is said with hands together.
```

---

## Example Sentences

**See the `example-sentences` skill for complete requirements including:**
- Minimum counts: 5 examples per sense (basic/core) or 3 (general)
- Progressive length: Examples should get longer from first to last
- Vocabulary restrictions by tier
- Quality standards and formatting

### Sense Numbers in Examples

All examples must include a `sense_numbers` field linking them to the definition(s) they illustrate:

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

**Guidelines by entry type:**

**Nouns:**
- Concrete vs. abstract meanings may require separate senses
- Different domains of use (technical, everyday) may warrant separate senses
- Show common verb collocations in examples

**Counters:**
- Usually single-sense; use `[1]` for all examples
- Different counting contexts typically share the same sense
- Include examples showing sound change patterns (1, 3, 6, 8, 10)

**Adverbs:**
- Degree vs. frequency meanings need separate senses
- Emphatic uses may be a separate sense from neutral uses
- Show typical sentence positions

**Expressions:**
- Fixed expressions typically have one sense
- Variations in formality level may be noted within the same sense
- Show exchange patterns where applicable

---

## Required Tags by Entry Type

All entries must include tags in `metadata.tags`. See `entry-guidelines` skill for full details.

### Nouns

```json
"tags": {
  "pos": ["noun"],              // Use ["noun", "verb-suru"] for suru-verbs
  "formality": "neutral",       // formal/neutral/informal/vulgar
  "politeness": "plain",        // honorific/humble/polite/plain
  "semantic": ["food"]          // Choose appropriate category
}
```

**Semantic categories for nouns:** `food`, `clothing`, `building`, `transportation`, `tool`, `furniture`, `electronics`, `body-part`, `body-internal`, `family`, `person`, `occupation`, `animal-*`, `plant-*`, `weather`, `geography`, `time-*`, `emotion`, `color`, `number`, `direction`, `size`, `quantity`, `work`, `education`, `leisure`, or `general` (fallback).

### Counters

```json
"tags": {
  "pos": ["counter"],
  "formality": "neutral",
  "politeness": "plain",
  "semantic": ["number"]        // Counters are typically "number"
}
```

### Adverbs

```json
"tags": {
  "pos": ["adverb"],
  "formality": "neutral",       // Many adverbs are register-specific
  "politeness": "plain",
  "semantic": ["descriptive"]   // Use "descriptive" for adverbs
}
```

### Expressions

```json
"tags": {
  "pos": ["expression"],
  "formality": "neutral",       // Expressions often have specific register
  "politeness": "plain",        // May be "polite" for greetings
  "semantic": ["greeting"]      // Or "expression" as fallback
}
```

---

## Quality Checklists

**For ALL entry types below:**
- [ ] **All kanji have furigana** (headword, examples, AND notes)
- [ ] Verify: `python3 build/verify_furigana.py <entry_id>` shows "✓ OK"
- [ ] **Tags complete**: pos, formality, politeness, semantic all present

### For Nouns
- [ ] Common verb collocations listed
- [ ] Scope clarified if different from English
- [ ] Counter mentioned if non-obvious
- [ ] Examples show natural usage
- [ ] All examples have valid sense_numbers

### For Counters
- [ ] Full 1-10 counting pattern provided
- [ ] All irregular readings highlighted
- [ ] Sound change rules explained
- [ ] What it counts clearly stated
- [ ] What it does NOT count mentioned
- [ ] All examples have valid sense_numbers

### For Adverbs
- [ ] Typical sentence position noted
- [ ] What it modifies specified
- [ ] Register labeled
- [ ] Distinguished from similar adverbs
- [ ] All examples have valid sense_numbers

### For Expressions
- [ ] Situational context explained
- [ ] Register specified
- [ ] Response pairs included (if applicable)
- [ ] Cultural significance noted (if applicable)
- [ ] All examples have valid sense_numbers
