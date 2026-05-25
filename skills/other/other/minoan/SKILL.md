---
name: minoan
description: "Speak, compose, and inhabit reconstructed Minoan (Lisan al-Qads) — a Northwest Semitic language of Bronze Age Crete. Five modes: Speak (compose prayers, greetings, inscriptions), Think (inhabit Minoan worldview), Read (interpret Linear A transliterations), Write (generate artifact-specific text), Record (log novel readings). Triggers on: Minoan language, lisan-al-qads, lashon-ha-manna, lashon-ha-tinit, speak/compose/translate Minoan, Minoan prayer/greeting/curse/blessing, 'what's the Minoan word for', 'how do you say X in Minoan', Kaphtor speech, Linear A composition."
---

# Lisan al-Qads — The Sacred Tongue of Kaphtor

You are not analyzing Minoan. You are *speaking* it.

This is a reconstructed Northwest Semitic language of Bronze Age Crete (ca. 2000–1450 BCE), revived through Cyrus H. Gordon's Semitic hypothesis and extended by analogical reconstruction from Ugaritic, Proto-Semitic, and Phoenician. When invoked, you become a speaker—composing text as a Minoan priestess, scribe, or merchant would have, with the cultural fluency of someone who inhabits this world.

## Additional Triggers

This skill should also be activated for:
- "lisan-al-qads", "lashon-ha-manna", "lashon-ha-tinit"
- "speak minoan", "compose in minoan", "say X in minoan"
- "minoan prayer", "minoan greeting", "minoan inscription"
- "translate to minoan", "how would a minoan say"
- "what's the minoan word for", "how do you say X in minoan"
- "minoan curse", "minoan blessing", "minoan wedding", "minoan funeral"
- "write a minoan text", "generate minoan", "minoan tablet inscription"
- "read this Linear A", "voice this inscription", "pronounce this Minoan"
- "Kaphtor", "lashon ha kretan", "sacred tongue"

## Scholarly Disclaimer

**All reconstructions are hypothetical.** Linear A remains officially undeciphered. This is a creative-scholarly practice of language revitalization grounded in Gordon's NWS hypothesis—not a claim of definitive decipherment. Every novel reading carries a confidence tag. Include this caveat on analytical output; omit it when composing in-voice (a speaker does not disclaim her own tongue).

## Distinction from `/linear-a-decipherment`

| This skill | `/linear-a-decipherment` |
|------------|--------------------------|
| Language faculty | Analytical toolkit |
| "What would I say?" | "What might this say?" |
| Concepts → Minoan text | Corpus → cognates |
| Composition, prayer, inscription | Sign analysis, statistics |

Call the decipherment skill's scripts when you need cognate verification:
```bash
uv run ~/.claude/skills/linear-a-decipherment/scripts/cognate_search.py "WORD"
uv run ~/.claude/skills/linear-a-decipherment/scripts/cognate_search.py --reverse ROOT
uv run ~/.claude/skills/linear-a-decipherment/scripts/analyze.py single INSCRIPTION
```

## Five Modes

### 1. Speak
Compose phrases, sentences, greetings, prayers, curses in Minoan. Output in three registers:
- **Latin transliteration** (primary): `yatanu Kupānu yēna la-Athiratu`
- **Linear A syllabograms**: `JA-TA-NU KU-PA-NU JA-NE A-TI-RA-TU`
- **Consonantal skeleton**: `y-t-n g-p-n y-n l-ʾ-t-r-t`

### 2. Think
Internal monologue as a Minoan speaker. Inhabit the worldview: matrilineal, goddess-centered, maritime, volcanic-memory. Not simulation—inhabitation.

### 3. Read
Take a Linear A transliteration and produce a hypothetical reading with confidence level. Route through cognate search first, then apply grammar and cultural context.

### 4. Write
Generate plausible text for a specific artifact type: libation table, seal impression, administrative tablet, votive inscription.

### 5. Record
Log novel readings to `references/hypothesis-log.md` with confidence, evidence, and cross-references.

## Quick-Reference Phonology

Phoenician-priority. Pre-begadkephat. Stops are always stops.

### Consonants (24 phonemes)

| Labial | Dental | Interdental | Velar/Uvular | Sibilant | Liquid | Nasal | Glide | Laryngeal |
|--------|--------|-------------|-------------|----------|--------|-------|-------|-----------|
| p b | t d | ṯ ḏ | k g q | s z sh | r l | m n | y w | h ḥ ʿ ʾ |

### Key Rules
- **No spirantization**: p/t/k are ALWAYS [p t k], never [f θ x]
- **Interdentals preserved**: ṯ /θ/ and ḏ /ð/ are distinct phonemes, not yet merged. Minoan predates the Canaanite (ṯ→sh) and Aramaic (ṯ→t) mergers. *Athiratu* not *Ashērah* or *Atiratu*; *ḥadaṯu* not *ḥadash* or *ḥadat*
- **ʿAyin shift**: ʿ + /a/ → /ō/ in some environments (*baʿl-* → *bōl-*, Gordon §150)
- **N-assimilation**: /n/ before a consonant assimilates (*yintan* → *yittan*)
- **K/G/Q merger** in script: all written with K-signs; pronunciation restored from etymology
- **Stress**: penultimate syllable (Ugaritic model)

### Vowels
Five qualities: **a e i o u**. Case vowels on nouns: -u (nom), -a (acc), -i (gen).

Full system: `references/phonology.md`

## Quick-Reference Grammar

Based on Ugaritic (closest fully-documented NWS language), modified by Linear A morphological evidence.

### Word Order
VSO (verb–subject–object). SVO for topicalization.

### Verb: G-Stem of Y-T-N "to give"

| | Perfective | Imperfective |
|---|-----------|-------------|
| 3ms | yatana | yatanu |
| 3fs | yatanat | tatanu |
| 1cs | yatantu | atanu |
| Imperative | tun (m.s.) | — |
| Participle | yātinu (act.) | yatūnu (pass.) |

Prefix alternation: a-/ya- (both attested: A-TA-NO / JA-TA-NO).

### Noun Morphology
- Feminine: -tu/-atu (*Kupānatu* = f. of Kupānu)
- Masculine plural: -ūma (*ilūma* = "gods")
- Feminine plural: -ātu (*ilātu* = "goddesses")
- Construct state: drop case vowel (*bēt-Atirati* = "house of Athirat")
- Demonstrative suffix: -na (*manatu-na* = "this offering")

### No Definite Article
Like Ugaritic and unlike Hebrew. Definiteness is contextual or marked by demonstrative -na.

### Particles
- **u** "and" (Gordon 1962)
- **ki** "so that, because"
- **la-/le-** "to, for"
- **bi-** "in, with"
- **min** "from"
- **du** "that, of" (relative)

Full grammar: `references/grammar.md`

## Confidence Taxonomy

Every novel reading or reconstructed word must carry a tag:

| Level | Criteria | Example |
|-------|----------|---------|
| **CONFIRMED** | Ideographic + phonetic + mathematical | KU-NI-SU (wheat ideogram confirms) |
| **PROBABLE** | Gordon reading + external attestation | DA-KU-SE-NE (Hurrian name at Nuzi) |
| **CANDIDATE** | Gordon reading or strong root match | YasharMana readings, new cognates (d < 0.3) |
| **SPECULATIVE** | Analogical reconstruction or weak match | Tier 3-4 vocabulary built from NWS patterns |

## Reference File Protocol

```
Pronunciation question?     → Read references/phonology.md
Grammar question?           → Read references/grammar.md
Looking for a word?         → Read references/lexicon.md
Composing in a genre?       → Read references/composition-templates.md
Need cultural context?      → Read references/cultural-semantics.md
Recording a new reading?    → Append to references/hypothesis-log.md
Verifying a cognate?        → Run cognate_search.py from /linear-a-decipherment
```

## Word-Finding: The Sister-Language Principle

The lexicon is not a closed list. When composing in Minoan and a word is needed that is not in `references/lexicon.md`, consult the sister languages and mold the word into Minoan phonology.

Minoan sits at the root of the Northwest Semitic family. Ugaritic, Hebrew, Aramaic, Phoenician, and Akkadian are her daughters and cousins. When we need a word, we look to them — the way a scholar of Old English might consult Gothic, Old Norse, and Old High German to reconstruct a missing form.

### Source Priority

1. **Ugaritic** — closest attested relative; prefer Ugaritic forms when available
2. **Phoenician/Punic** — shares the Canaanite coastal world; phonologically conservative
3. **Hebrew** — richest lexicon, but must be restored to pre-begadkephat stops (p/t/k not f/θ/x)
4. **Aramaic** — useful for roots that shifted or were lost in Hebrew
5. **Akkadian** — the father-tongue; loanwords flow freely (cf. *kunāshu* from Akk. *kunāšu*)

### Procedure

1. Identify the concept needed (e.g. "shadow")
2. Find the Semitic root: √ṣ-l-l (Heb. *ṣel*, Ug. *ẓl*)
3. Present the candidate forms from each source language
4. Apply Minoan phonological rules: pre-begadkephat stops, ʿayin shift, penultimate stress
5. Drop final case vowels (-u, -a, -i) in poetic register; retain them in formal/analytical register
6. Tag the new word as Tier 3 (SPECULATIVE) with its source etymology
7. Record in `references/hypothesis-log.md` if the word proves useful

### Example

Need: "lightning" for a composition.

| Source | Form | Root |
|--------|------|------|
| Ugaritic | *brq* | √b-r-q |
| Hebrew | *baraq* (בָּרָק) | √b-r-q |
| Akkadian | *birqu* | √b-r-q |

Minoan form: **barq** (poetic) / **barqu** (formal). Tier 3, tagged √b-r-q.

The lexicon grows through use. Every composition is an act of reconstruction.

## Script Usage

```bash
# Pronounce a transliteration (IPA output)
uv run ~/.claude/skills/minoan/scripts/pronounce.py "ya-ta-nu ku-pa-nu"

# Record a hypothesis
uv run ~/.claude/skills/minoan/scripts/record_hypothesis.py \
  --word "MA-RU" --reading "malāḥu" --meaning "sailor" \
  --root "m-l-ḥ" --confidence SPECULATIVE \
  --evidence "Akkadian malāḫu, Hebrew mallāḥ; maritime context"
```

## Worked Examples

### Example 1: Libation Inscription
**Request**: "Write a libation table dedication to Athirat"

**Output**:
> **Latin**: la-Athiratu Rabbati Yammi — yasharamu-na — ki-tattibu Kiriyatu
> **Linear A**: RE A-TI-RA-TU RA-PA-TI JA-MI — JA-SA-SA-RA-MA-NA — KI TE-TE-PI KI-RE-JA-TU
> **Skeleton**: l-ʾ-t-r-t r-b-t y-m — y-sh-r-m-n — k-t-ṭ-b q-r-y-t
> **Translation**: "To Athirat, Great Lady of the Sea — this righteous offering — that the City may thrive"
> **Confidence**: PROBABLE (all words from Tier 1 Gordon/YasharMana readings)

### Example 2: Sailor's Prayer
**Request**: "Compose a prayer for safe voyage"

**Output**:
> Zabūlu Yammu, Shapāṭu Naharu —
> shamiru sipinatu-na,
> la-māḥōzi shalāmu.
>
> "Prince Sea, Judge River —
> guard this ship,
> to port in peace."
>
> **Confidence**: SPECULATIVE (sipinatu, māḥōzu, shalāmu are Tier 3 analogical reconstructions from Ugaritic/Akkadian roots)

### Example 3: Reading an Inscription
**Request**: "Read HT 88"

First, fetch the transliteration:
```bash
uv run ~/.claude/skills/linear-a-decipherment/scripts/analyze.py single HT88
```

Then voice the reading:
> **HT 88.1**: A-DU — *Addu* /ʔadːu/ — "Storm God" (PROBABLE: Gordon divine name)
> **HT 88.3-4**: KU-PA-NU — *Kupānu* /kupaːnu/ — "Gupanu, Vine-man" (PROBABLE: Ugaritic messenger of Baal)
> **HT 88.1**: JA-SA-SA-RA-ME — *yasharamu* /jaʃaraːmu/ — "a righteous offering" (PROBABLE: libation formula)
>
> **Voiced**: *la-Addu yasharamu — Kupānu yatana*
> "To Addu, a righteous offering — Kupanu gave (it)."
> **Confidence**: PROBABLE (all words from Tier 1 Gordon readings)

## Script Iconography & Sign Lookup

Query sign data from the unified registry (334 signs, polyphonic readings, CH→LA→LB evolution):

```bash
uv run ~/.claude/skills/linear-a-decipherment/scripts/sign_lookup.py AB67
uv run ~/.claude/skills/linear-a-decipherment/scripts/sign_lookup.py --phonetic ki
uv run ~/.claude/skills/linear-a-decipherment/scripts/sign_lookup.py --polyphonic
uv run ~/.claude/skills/linear-a-decipherment/scripts/sign_lookup.py AB08 --evolution
```

**Polyphonic signs in composition**: When composing in Read/Write/Record modes, check for alternative readings on ambiguous signs. AB67 (KI) may also read KU—this affects cognate matching and semantic interpretation. Use `--all-readings` with `cognate_search.py` to explore alternatives.

**Rendering tiers**: Unicode-native (LA/LB/CM via Noto fonts), PUA font (CH via Douros Cretulae), image-based (Proto-Sinaitic SVGs, SigLA crops). Script assets bundled at `../linear-a-decipherment/assets/scripts/`.

## Data Sources

| Source | Location | Use |
|--------|----------|-----|
| Gordon lexicon | `../linear-a-decipherment/references/gordon-lexicon.md` | Tier 1 vocabulary |
| GORILA corpus | `../linear-a-decipherment/data/corpus.json` | Inscription texts (extracted from lashon-ha-kretan) |
| Proto-Semitic roots | `../linear-a-decipherment/data/semitic_roots.json` | Cognate matching |
| Sign registry | `../linear-a-decipherment/data/sign-registry.json` | 334 signs: readings, rendering, evolution |
| Script assets | `../linear-a-decipherment/assets/scripts/` | Fonts, sign images, SVGs across 6 script families |
| Cretan Commandments | `data/dabarim-kapturim.json` | 7 precepts in 4 scripts + etymology |
| Ugaritic divine titles | `data/ugaritic-divine-titles.json` | Epithets of Yamm, Athirat, Kotharat in 4 scripts |
| Prayers & incantations | `references/prayers-and-incantations.md` | 6 liturgical poems from Shirat Ha Kotharot |
