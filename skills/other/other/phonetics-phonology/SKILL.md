---
name: phonetics-phonology
description: Sound systems of human language -- phoneme inventories, the International Phonetic Alphabet, articulatory and acoustic phonetics, phonological rules, suprasegmental features (stress, tone, intonation), and ear training for non-native sound perception. Covers place and manner of articulation, voicing contrasts, vowel space, minimal pair analysis, allophonic variation, phonotactic constraints, connected speech phenomena (assimilation, elision, liaison), and prosody across language families. Use when analyzing pronunciation, teaching sound systems, performing phonemic transcription, or diagnosing intelligibility problems in any language.
type: skill
category: languages
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/languages/phonetics-phonology/SKILL.md
superseded_by: null
---
# Phonetics & Phonology

Every human language is built on a finite inventory of contrastive sounds. Phonetics studies how those sounds are physically produced (articulatory), transmitted (acoustic), and perceived (auditory). Phonology studies how sounds function within a particular language -- which distinctions are meaningful, which are automatic, and how sounds interact with each other in sequence. This skill treats language-universal principles rather than any single language's system, making it applicable to any language a learner encounters.

**Agent affinity:** crystal (phonetic description, language diversity), chomsky-l (phonological rules, underlying representations)

**Concept IDs:** lang-phoneme-inventory, lang-ipa-notation, lang-ear-training, lang-suprasegmentals

## The Sound Landscape at a Glance

| Domain | Focus | Key Tools |
|---|---|---|
| Articulatory phonetics | How sounds are produced | Place/manner/voicing, vocal tract diagrams |
| Acoustic phonetics | Sound waves and formants | Spectrograms, F1/F2 vowel plots, VOT |
| Auditory phonetics | How sounds are perceived | Categorical perception, ear training drills |
| Phonemics | Contrastive sound units | Minimal pairs, complementary distribution |
| Phonotactics | Legal sound sequences | Onset/coda constraints, syllable structure |
| Prosody | Suprasegmental features | Stress, tone, intonation contours |

## Articulatory Phonetics: Producing Sounds

### Consonant Classification

Every consonant is classified along three dimensions:

1. **Voicing.** Whether the vocal folds vibrate (voiced: [b, d, g]) or not (voiceless: [p, t, k]).
2. **Place of articulation.** Where in the vocal tract the constriction occurs: bilabial (both lips), labiodental (lip + teeth), dental, alveolar, postalveolar, retroflex, palatal, velar, uvular, pharyngeal, glottal.
3. **Manner of articulation.** How the airstream is modified: plosive/stop (complete closure then release), fricative (narrow channel producing turbulence), affricate (stop + fricative), nasal (oral closure, air through nose), lateral (air around sides of tongue), approximant (narrowing without turbulence), trill, tap/flap.

**Example.** English [t] is a voiceless alveolar plosive. Japanese [ts] in "tsunami" is a voiceless alveolar affricate. The distinction matters: substituting one for the other changes meaning or intelligibility in context.

### Vowel Classification

Vowels are classified by tongue position along two axes, plus lip rounding:

- **Height** (close/high to open/low): close [i, u], close-mid [e, o], open-mid [ɛ, ɔ], open [a, ɑ]
- **Backness** (front to back): front [i, e, ɛ], central [ə, ɐ], back [u, o, ɑ]
- **Rounding** (rounded or unrounded): French [y] is a close front rounded vowel -- close and front like [i] but with rounded lips

The IPA vowel trapezoid plots these dimensions, and formant analysis (F1 for height, F2 for backness) provides acoustic confirmation.

### Voice Onset Time (VOT)

VOT measures the delay between the release of a stop consonant and the onset of voicing for the following vowel. It distinguishes:

- **Prevoiced** (negative VOT): vocal folds vibrate before release. Spanish [b], French [d].
- **Short-lag** (VOT near zero): voicing begins at release. English [b], Mandarin unaspirated [p].
- **Long-lag** (positive VOT): significant aspiration before voicing. English [pʰ], Mandarin aspirated [pʰ].

This is a major source of cross-linguistic interference: a Spanish speaker's unaspirated [p] sounds like English [b] to an English listener, and vice versa.

## The International Phonetic Alphabet (IPA)

The IPA provides a universal transcription system where one symbol corresponds to one sound. This skill assumes familiarity with IPA as a meta-tool for describing any language.

### Transcription Types

- **Broad (phonemic) transcription** uses slashes: /kæt/. It records only contrastive distinctions. Two sounds that are phonemically distinct in the language get different symbols.
- **Narrow (phonetic) transcription** uses brackets: [kʰæt]. It records phonetic detail including allophonic variation -- the aspiration on English [kʰ] that is not contrastive but is physically present.

### Minimal Pair Analysis

A **minimal pair** is two words that differ by exactly one sound in the same position and have different meanings: "bat" /bæt/ vs. "pat" /pæt/. Minimal pairs prove that two sounds are separate phonemes. If no minimal pair can be found, the sounds may be allophones of the same phoneme.

**Worked example.** In English, [l] and [ɫ] (clear and dark L) are allophones: "leaf" [liːf] vs. "feel" [fiːɫ]. No minimal pair distinguishes them because they are in complementary distribution (clear before vowels, dark before consonants or word-finally). In Russian, [l] and [ɫ] ARE separate phonemes: "лук" /luk/ (onion) vs. "лук" /ɫuk/ would be meaningful (Cyrillic spelling distinguishes palatalized from non-palatalized).

## Phonological Rules and Processes

### Common Cross-Linguistic Processes

| Process | Description | Example |
|---|---|---|
| **Assimilation** | A sound becomes more like a neighboring sound | English "input" /ɪnpʊt/ often pronounced [ɪmpʊt] -- /n/ becomes [m] before bilabial /p/ |
| **Elision** | A sound is deleted | French "je ne sais pas" -> [ʃɛpa] in rapid speech |
| **Epenthesis** | A sound is inserted | Japanese borrows "strike" as "sutoraiku" -- vowels inserted to fit CV syllable structure |
| **Metathesis** | Sounds swap positions | English "ask" pronounced [æks] in some dialects |
| **Lenition** | A sound weakens | Spanish intervocalic /b/ -> [β] (fricative): "lobo" [loβo] |
| **Fortition** | A sound strengthens | Korean word-initial lenis stops become tense after nasals |
| **Nasalization** | Vowel acquires nasal quality | French nasal vowels: "bon" [bɔ̃] |
| **Palatalization** | Consonant shifts toward palatal place | Russian consonants before front vowels: /t/ -> [tʲ] |
| **Vowel harmony** | Vowels in a word agree on a feature | Turkish: "evler" (houses) but "odalar" (rooms) -- front/back harmony |

### Rule Notation

Phonological rules are written as: A -> B / C __ D

"A becomes B in the context of C preceding and D following."

**Example.** English aspiration rule: voiceless stops become aspirated word-initially before a stressed vowel.

/p, t, k/ -> [pʰ, tʰ, kʰ] / # __ V[+stress]

This explains why "pin" has [pʰ] but "spin" has unaspirated [p] -- the /p/ in "spin" is not word-initial.

## Suprasegmental Features

### Stress

Stress is relative prominence of a syllable through louder volume, higher pitch, longer duration, or fuller vowel quality. Languages differ in whether stress is:

- **Fixed** (predictable from word structure): French (final), Polish (penultimate), Czech (initial)
- **Free** (unpredictable, must be learned per word): English, Russian, Italian

In free-stress languages, stress can be contrastive: English "CONtract" (noun) vs. "conTRACT" (verb); Russian "мука" /mukÁ/ (flour) vs. /múka/ (torment).

### Tone

Tone uses pitch to distinguish word meaning. Approximately 60-70% of the world's languages are tonal.

- **Level tones:** Mandarin has four tones (high, rising, dipping, falling) plus neutral. "ma" means "mother" (T1), "hemp" (T2), "horse" (T3), or "scold" (T4) depending on tone.
- **Contour tones:** Thai, Vietnamese, Cantonese use complex pitch contours (rising, falling, low-rising, high-falling, etc.).
- **Register tones:** Many Bantu languages use high vs. low tone with grammatical as well as lexical function.

### Intonation

Intonation is the pitch pattern over an entire phrase or sentence. Unlike tone, it is not lexical but grammatical and pragmatic:

- Rising intonation for yes/no questions in many European languages
- Falling intonation for statements
- Rise-fall for emphasis or surprise
- Language-specific patterns: Japanese uses pitch accent (one mora per word carries a pitch drop), which differs from both stress and tone

## Ear Training

Perceiving non-native sounds is a trained skill, not an innate ability. The critical period hypothesis suggests children acquire phonemic distinctions more easily, but adults can train perception through:

1. **Discrimination drills.** Listen to pairs of sounds and judge "same or different." Start with maximally different contrasts and narrow.
2. **Identification drills.** Listen to a sound and select the correct category from a set.
3. **Minimal pair production.** Practice producing contrasts until a native speaker confirms differentiation.
4. **High-variability training.** Hear the same contrast produced by multiple speakers in multiple phonetic contexts. This forces the brain to extract the invariant feature rather than memorizing one exemplar.

Research by Flege (1995) and Best & Tyler (2007) shows that adult learners can acquire new phonemic categories, but the difficulty depends on the relationship between L1 and L2 sounds. The hardest case is when an L2 contrast falls within a single L1 category -- the learner must split an existing category, not create a new one.

## Connected Speech Phenomena

Fluent speech is not a sequence of isolated sounds. Sounds in running speech interact in ways that isolated-word pronunciation does not predict:

- **Linking.** English "an apple" -> [ən.æp.əl], the /n/ links to the following vowel.
- **Intrusive sounds.** British English "law and order" -> [lɔːr.ænd.ɔːdə] -- an intrusive [r] appears between two vowels.
- **Weak forms.** English function words reduce in unstressed position: "and" -> [ən] or [n], "to" -> [tə].
- **Chunking.** Listeners parse speech into prosodic phrases, not individual words. The phrase boundary in "I scream" vs. "ice cream" is marked by stress and juncture, not by silence.

Understanding connected speech is critical for listening comprehension. Learners trained on isolated words often fail to parse natural-speed speech because they have never encountered the connected forms.

## Practical Applications

### Pronunciation Assessment

When assessing a learner's pronunciation, distinguish between:

- **Errors that affect intelligibility** (wrong phoneme: "ship" vs. "sheep") -- these must be corrected
- **Errors that mark a foreign accent but do not impede understanding** (slightly different VOT, non-native vowel quality) -- these may be acceptable depending on goals
- **Errors that violate phonotactic rules** (consonant clusters the L2 does not permit) -- these often trigger epenthesis or deletion, producing a characteristic accent pattern

### Language Comparison

When a learner starts a new language, compare its sound system to known languages:

1. Which phonemes are shared? These transfer directly.
2. Which L2 phonemes are absent from L1? These require new category creation.
3. Which L1 distinctions are not used in L2? These may cause hypercorrection.
4. What are the phonotactic differences? (Japanese has no consonant clusters; English allows /str-/.)
5. What suprasegmental system does L2 use? (Stress, tone, pitch accent, or none?)

## Cross-References

- **chomsky-l agent:** Universal phonological features and markedness theory. The claim that all languages draw from a universal feature set.
- **crystal agent:** Phonetic description of endangered and diverse languages. Language documentation relies on precise phonetic transcription.
- **krashen agent:** Input hypothesis applied to phonology -- comprehensible input must include the target sound system.
- **grammar-syntax skill:** Sound changes at morpheme boundaries (morphophonology) connect phonology to grammar.
- **vocabulary-acquisition skill:** Phonological form is the first thing encoded when learning a new word.

## References

- Ladefoged, P. & Johnson, K. (2015). *A Course in Phonetics*. 7th edition. Cengage.
- Roach, P. (2009). *English Phonetics and Phonology*. 4th edition. Cambridge University Press.
- Flege, J. E. (1995). "Second language speech learning: Theory, findings, and problems." In W. Strange (Ed.), *Speech Perception and Linguistic Experience*. York Press.
- Best, C. T. & Tyler, M. D. (2007). "Nonnative and second-language speech perception." In O.-S. Bohn & M. J. Munro (Eds.), *Language Experience in Second Language Speech Learning*. John Benjamins.
- International Phonetic Association. (2015). *Handbook of the International Phonetic Association*. Cambridge University Press.
