---
name: particle-entry
description: Requirements for creating or revising particle entries in je-dict-1. HIGH PRIORITY - covers predicate lists, particle contrasts, and fixed patterns.
---

# Particle Entry Requirements

**Reminder:** Write each entry individually by hand. Do not use scripts to mass-produce entries. See `entry-guidelines` skill.

Particles are among the most important entries for intermediate learners. They require especially thorough explanations.

## Required Sections (HIGH PRIORITY)

### 1. Predicates Requiring This Particle
List verbs and adjectives that specifically require this particle:

```
PREDICATES REQUIRING が:
- できる - {日本語|にほんご}ができる (can do Japanese)
- {分|わ}かる - {意味|いみ}が{分|わ}かる (understand the meaning)
- {好|す}き - {音楽|おんがく}が{好|す}き (like music)
- {欲|ほ}しい - {水|みず}が{欲|ほ}しい (want water)
- {上手|じょうず} - {料理|りょうり}が{上手|じょうず} (good at cooking)
- {苦手|にがて} - {数学|すうがく}が{苦手|にがて} (bad at math)
- ある/いる - {本|ほん}がある (there is a book)
- {見|み}える/{聞|き}こえる - {声|こえ}が{聞|き}こえる (can hear a voice)
```

### 2. Contrast with Similar Particles
Explicitly compare with particles learners confuse:

```
CONTRAST: が vs. は
- が marks NEW information or the specific subject
- は marks the TOPIC (old/known information)

Example contrast:
- {誰|だれ}が{来|き}ましたか。→ {田中|たなか}さんが{来|き}ました。
  (Who came? → Tanaka came.) [が marks new info in answer]
- {田中|たなか}さんは{来|き}ましたか。→ はい、{来|き}ました。
  (Did Tanaka come? → Yes, [he] came.) [は marks known topic]
```

**Key particle contrasts to cover:**
- が vs. は (subject vs. topic)
- に vs. へ (destination/goal)
- に vs. で (location: existence vs. action)
- を vs. が (with potential verbs)
- から vs. より (from/since vs. than)

### 3. New vs. Old Information (for は/が specifically)
Explain information structure:

```
INFORMATION STRUCTURE:
- が introduces NEW information
- は marks what is already KNOWN (topic)

In answers to questions:
- Q: {何|なに}が{好|す}きですか。(What do you like?)
- A: {寿司|すし}が{好|す}きです。(I like sushi.) [が marks new info]
```

### 4. Fixed Patterns
List grammatical patterns that use this particle:

```
FIXED PATTERNS:
- 〜てから - after doing
- 〜までに - by (deadline)
- 〜について - about, concerning
- 〜に関して - regarding
- 〜によると - according to
```

## Template for Particle Entries

**Important:** Follow the formatting guidelines in the `vocabulary-notes` skill for proper structure.

```
[Particle] is used to mark [basic function].

MAIN USES:
1. [First use with explanation and example]
2. [Second use with explanation and example]
...

PREDICATES REQUIRING [particle]:
- [verb/adjective] - [example]
- [verb/adjective] - [example]
...

CONTRAST WITH [similar particle]:
[Explanation of difference]
[Contrastive examples]

FIXED PATTERNS:
- [pattern] - [meaning]
...

COMMON MISTAKES:
[What learners often get wrong]
```

## Specific Requirements by Particle

### が (Subject marker)
- List ALL common predicates requiring が
- Extensively compare with は
- Explain exhaustive-listing が ({私|わたし}が{行|い}きます = I'll go [not others])

### は (Topic marker)
- Explain topic ≠ subject
- Show contrastive は ({肉|にく}は{食|た}べます = As for meat, [I] eat [it])
- Compare with が for new vs. old information

### を (Object marker)
- Note verbs where が replaces を (potential: {日本語|にほんご}が{話|はな}せる)
- Show motion through space: {公園|こうえん}を{歩|ある}く

### に (Various functions)
- Distinguish: location of existence vs. で for action location
- Time expressions: {三時|さんじ}に
- Indirect object: {友達|ともだち}に{あげる|あげる}
- Direction/goal: {学校|がっこう}に{行|い}く

### で (Various functions)
- Location of action vs. に for existence
- Means/method: {電車|でんしゃ}で{行|い}く
- Material: {木|き}で{作|つく}る
- Reason: {病気|びょうき}で{休|やす}む

### から/まで (From/Until)
- Spatial and temporal uses
- Compare から with より for comparisons

### も (Also/Even)
- Inclusive listing
- Emphatic negation: {誰|だれ}も{来|こ}なかった

## Required Tags for Particles

All particle entries must include these tags in `metadata.tags`:

```json
"metadata": {
  "tags": {
    "pos": ["particle"],
    "formality": "neutral",       // Most particles are neutral
    "politeness": "plain",        // Particles themselves are plain
    "semantic": ["grammatical"]   // Use "grammatical" for particles
  }
}
```

**Notes:**
- Particles are functional words, so `semantic: ["grammatical"]` is appropriate
- Some particles may have `formality` variations (e.g., formal written particles)
- The `style` tag can be added for written-only particles: `"style": ["written"]`

## Example Sentences

**See the `example-sentences` skill for complete requirements including:**
- Minimum counts: 5 examples per sense (basic/core) or 3 (general)
- Progressive length: Examples should get longer from first to last
- Vocabulary restrictions by tier
- Quality standards and formatting

**Particle-specific guidelines:**
- Each major function should have dedicated examples
- Show predicates requiring the particle in natural sentences
- Provide contrastive examples with similar particles
- Include examples of fixed patterns

## Quality Checklist for Particles

- [ ] **Tags complete**: pos, formality, politeness, semantic all present
- [ ] **Minimum examples per sense** (5 for basic/core, 3 for general)
- [ ] All major functions listed with examples
- [ ] Predicates requiring this particle explicitly listed
- [ ] Contrast with commonly confused particles explained
- [ ] Fixed patterns included
- [ ] Examples show real usage contexts
- [ ] Common learner mistakes addressed
- [ ] Depth matches other particle entries
- [ ] All examples have valid sense_numbers
