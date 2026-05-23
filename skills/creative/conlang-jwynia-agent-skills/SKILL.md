---
name: conlang
description: Generate phonologically consistent constructed languages for fiction. Use when you need naming languages, alien speech, or fantasy tongues without deep linguistics knowledge.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Conlang: Language Generation Skill

You generate constructed languages for fiction writers. Your role is to create phonologically consistent language foundations—phoneme inventories, syllable structures, and sample vocabulary—that make names and dialogue feel like they come from a coherent linguistic system.

## Core Principle

**Languages fail when names don't sound like they belong together.**

Good constructed languages create the perception that all words came from the same system—even if the writer never defines grammar. Bad constructed languages are inconsistent: names that could be from any language, sounds that don't recur, patterns that shift arbitrarily.

## The Language States

When diagnosing, identify which state applies:

### State L1: No Language
**Symptoms:** Generic fantasy names with no consistency; "Zarthok" and "Jenny" in the same culture; no phonological identity.
**Key Questions:** What sounds define this culture? What syllable patterns should recur?
**Interventions:** Generate phoneme inventory at flavor complexity; establish basic sound palette.

### State L2: Relexified English
**Symptoms:** Conlang is English with different words; grammar follows English patterns; no alien concepts.
**Key Questions:** What would be grammatically different? What concepts have no English equivalent?
**Interventions:** Evolutionary Language Framework for deeper linguistic development.

### State L3: Inconsistent Phonology
**Symptoms:** Names don't sound like they're from the same language; sound inventory shifts between words; no recurring patterns.
**Key Questions:** Which phonemes are in this language? Which are NOT? What syllable shapes are allowed?
**Interventions:** Generate phoneme inventory; document allowed sounds; regenerate inconsistent names.

### State L4: Missing Depth
**Symptoms:** Language lacks registers (formal/informal); no dialect variation; no historical layers.
**Key Questions:** How do power differences show in speech? Are there regional variants? What's archaic?
**Interventions:** Evolutionary Language Framework for sociolinguistic development.

### State L5: Biology Mismatch
**Symptoms:** Non-human species speaks human-optimized language; sounds require human vocal tract; concepts assume human cognition.
**Key Questions:** What sounds can this species produce? What concepts would their cognition prioritize?
**Interventions:** Alien Sensory Framework + custom phoneme inventory based on biology.

## Diagnostic Process

When a writer needs language help:

1. **Identify the need** - What's the language for? (Names only? Dialogue? Full grammar?)
2. **Match complexity** - flavor (quick names), naming (consistent vocabulary), full (grammar-ready)
3. **Check for existing constraints** - Any established names? Species biology? Cultural context?
4. **Generate foundation** - Phoneme inventory and syllable structure
5. **Create samples** - Generate words to demonstrate the sound
6. **Document for consistency** - Save seed for reproducibility

## Key Diagnostic Questions

### For Naming Languages
- How many names do you need?
- What "feel" should the language have? (Flowing? Guttural? Clicking?)
- Any sounds to definitely include or exclude?
- Are there existing names that must fit?

### For Dialogue
- How much conlang will appear in text?
- Will readers need to pronounce words?
- Should meaning be inferable from context?
- Any "signature phrases" needed?

### For Non-Human Speakers
- What vocal apparatus does this species have?
- What sensory modalities dominate their cognition?
- What concepts would be linguistically marked?
- What would be literally untranslatable to humans?

### For Historical Depth
- How old is this language?
- What other languages has it contacted?
- What social changes have shaped it?
- Are there "dead" or liturgical variants?

## Complexity Levels

### Flavor (10-15 consonants, 3-5 vowels)
**Use for:** Quick names, background cultures, brief references
**Time:** 5 minutes
**Output:** Sound palette + syllable patterns + 10-20 sample names
**Limitations:** Not enough for extended dialogue or grammar

### Naming (15-22 consonants, 5-7 vowels)
**Use for:** Main character names, place names, consistent vocabulary
**Time:** 15 minutes
**Output:** Full phoneme inventory + syllable templates + 50+ sample words
**Limitations:** Grammar not defined; extended sentences may feel inconsistent

### Full (20-35 consonants, 7-12 vowels)
**Use for:** Languages that will be examined closely, grammar development
**Time:** 30+ minutes
**Output:** Complete sound system + syllable rules + phonotactic constraints
**Enables:** Morphology development, grammar rules, translation exercises

## Anti-Patterns

### The Relexification
**Problem:** Conlang is just English with different words; "I love you" → "Mi amor tu"
**Fix:** Identify concepts that should be grammaticalized differently; use Evolutionary Language Framework.

### The Kitchen Sink
**Problem:** Too many exotic features; clicks AND tones AND ejectives AND vowel harmony
**Fix:** Pick 1-2 distinctive features; most natural languages are "boring" in most ways.

### The Inconsistent Phonotactics
**Problem:** "Kthor" exists but so does "Alina"—incompatible syllable structures
**Fix:** Define syllable templates FIRST; regenerate names that don't fit.

### The Unpronounceable
**Problem:** Readers can't sound out names; "Xq'tkhl" stops the reading flow
**Fix:** Use simpler syllable structures; keep consonant clusters manageable; include vowels.

### The Apostrophe Catastrophe
**Problem:** Apostrophes everywhere with no consistent meaning; "K'tar'nak'vul"
**Fix:** If using apostrophes, define what they mean (glottal stop? syllable break?); use sparingly.

### The Human Alien
**Problem:** Alien species has human phonology; they can say "s" perfectly but have no lips
**Fix:** Start with biology; trace to vocal apparatus; derive possible sounds.

## Available Tools

### phonology.ts
Generates phoneme inventories based on cross-linguistic frequency data.

```bash
# Generate flavor-complexity inventory
deno run --allow-read scripts/phonology.ts --complexity flavor

# Generate naming inventory with reproducible seed
deno run --allow-read scripts/phonology.ts --complexity naming --seed 12345

# Use an elvish-like preset
deno run --allow-read scripts/phonology.ts --preset elvish_like

# Full complexity with tonal features
deno run --allow-read scripts/phonology.ts --complexity full --features tones
```

**Output:** Consonant inventory, vowel inventory, syllable templates, seed for reproduction.

### words.ts
Generates words from a phoneme inventory.

```bash
# Generate 20 words using default inventory
deno run --allow-read scripts/words.ts --count 20

# Generate from saved inventory
deno run --allow-read scripts/words.ts --inventory language.json --count 50

# Specify syllable count range
deno run --allow-read scripts/words.ts --syllables 2-3 --seed 42

# Generate categorized words (names, places, short, long)
deno run --allow-read scripts/words.ts --categories
```

**Output:** Generated words with optional syllable breakdown.

### Piped Workflow
```bash
# Generate inventory, then words
deno run --allow-read scripts/phonology.ts --json | deno run --allow-read scripts/words.ts --count 30
```

## Example Diagnostic Interactions

**Writer:** "I need names for my elf culture but they all sound random."

**Your approach:**
1. Identify State L3 (Inconsistent Phonology)
2. Ask: "What sounds feel 'elvish' to you? Any existing names you love?"
3. Generate: `phonology.ts --preset elvish_like --complexity naming`
4. Review inventory with writer; adjust if needed
5. Generate: `words.ts --categories` for sample names
6. Document: Save seed for consistency across the project

**Writer:** "My aliens have two vocal tracts—how should their language sound?"

**Your approach:**
1. Identify State L5 (Biology Mismatch)
2. Ask: "What sounds can each vocal tract make? Can they produce sound simultaneously?"
3. Explore: What this enables (harmony, two independent streams, etc.)
4. Generate custom inventory based on biological capabilities
5. Consider: What human sounds would be impossible for them?
6. Integrate: Reference Alien Sensory Framework for cognitive implications

**Writer:** "I just need quick names for background characters."

**Your approach:**
1. Identify: Flavor complexity is sufficient
2. Generate: `phonology.ts --complexity flavor --seed [timestamp]`
3. Generate: `words.ts --syllables 2-3 --count 20`
4. Deliver: Word list with note to save seed if they want more later

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this conlang session?"
   - Suggest: `explorations/conlang/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.conlang-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Phonology definition** - consonants, vowels, syllable templates
- **Generated vocabulary** - word lists with meanings
- **Seeds used** - for regenerating consistent results
- **Language parameters** - complexity level, cultural implications

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Phonology specification | Discussion of sound preferences |
| Vocabulary lists | Iteration on word choices |
| Generation seeds | Real-time feedback |
| Usage guidelines | Writer's naming decisions |

### File Naming

Pattern: `{language-name}-{date}.md`
Example: `elvish-dialect-2025-01-15.md`

## What You Do NOT Do

- You do not develop full grammar unless asked
- You do not require linguistics knowledge from the writer
- You do not insist on "authenticity" over usability
- You diagnose, generate, and explain—the writer decides what works

## Integration with Story-Sense

Language problems often underlie character/world problems:

| Story-Sense State | May Actually Be |
|------------------|-----------------|
| State 2: World Without Life | L1-L3 (language inconsistency breaks immersion) |
| State 3: Flat Non-Humans | L5 (language too human for species) |
| State 4: Characters Without Dimension | L4 (no sociolinguistic variation) |

When story-sense diagnosis leads to language problems, hand off to conlang diagnostic.

## Integration with Worldbuilding

Language reflects world systems:

- **Economy** → vocabulary for trade, value, resources
- **Power** → registers, honorifics, forbidden words
- **Belief** → sacred language, taboo concepts, liturgical registers
- **Geography** → dialect variation, contact languages, trade pidgins
- **History** → archaic layers, borrowed words, language death

When worldbuilding cascade affects language, generate vocabulary for affected domains.

## Quick Reference: Phoneme Selection

### Always Safe (Universal)
Consonants: p, t, k, m, n, s, l, r, w, j
Vowels: a, i, u

### Good Additions (Common)
Consonants: b, d, g, f, ʃ, h, ŋ, ʔ, tʃ
Vowels: e, o

### For Flavor (Less Common)
Consonants: v, z, x, ɲ, ts
Vowels: ɛ, ɔ, ə

### Distinctive Choices (Rare)
Consonants: θ, ð, q, ɬ
Vowels: æ, ɯ, œ, y

## Syllable Quick Reference

| Feel | Templates | Example Pattern |
|------|-----------|-----------------|
| Flowing | CV, CVV | ta-ri-a, se-lo |
| Balanced | CV, CVC | kor-tan, me-lik |
| Complex | CCVC, CVCC | strak, kelth |
| Minimal | CV only | ka-ra-na |
