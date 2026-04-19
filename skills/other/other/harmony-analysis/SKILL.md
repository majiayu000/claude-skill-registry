---
name: harmony-analysis
description: Harmonic analysis, voice leading, chord function, and modulation techniques for tonal music. Covers triads, seventh chords, Roman numeral analysis, figured bass, voice leading rules, cadence types, secondary dominants, modulation techniques, chromatic harmony (Neapolitan, augmented sixth chords), jazz lead sheet notation, and functional vs. linear harmonic thinking. Use when analyzing chord progressions, writing voice leading, identifying key areas, or interpreting harmonic function in any tonal style.
type: skill
category: music
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/music/harmony-analysis/SKILL.md
superseded_by: null
---
# Harmony Analysis

Harmony is the vertical dimension of music — the simultaneous sounding of pitches and the principles governing how those sonorities connect across time. Harmonic analysis decodes the function of each chord within a key, traces the path of individual voices between chords, and reveals the large-scale tonal architecture of a piece. This skill covers diatonic and chromatic harmony, voice leading rules, cadence identification, modulation techniques, and the translation between classical and jazz chord notation systems.

**Agent affinity:** rameau (harmonic function, fundamental bass theory), bach (voice leading, chorale harmonization)

**Concept IDs:** harmony, chord-progressions, song-form

## Part I — Chord Vocabulary

### Triads

A triad is a three-note chord built in thirds above a root. Four qualities exist in tonal music:

| Quality | Intervals | Example on C | Symbol |
|---|---|---|---|
| Major | M3 + m3 (P5 total) | C-E-G | C or CM |
| Minor | m3 + M3 (P5 total) | C-Eb-G | Cm or c |
| Diminished | m3 + m3 (d5 total) | C-Eb-Gb | Cdim or c-degrees |
| Augmented | M3 + M3 (A5 total) | C-E-G# | Caug or C+ |

In a major key, the diatonic triads are: I (major), ii (minor), iii (minor), IV (major), V (major), vi (minor), vii-degrees (diminished). This distribution of qualities is not arbitrary — it arises from the pattern of whole and half steps in the major scale.

### Seventh Chords

Adding a third above the triad's fifth produces a seventh chord. The five principal types:

| Type | Construction | Diatonic location (major key) | Jazz symbol |
|---|---|---|---|
| Major seventh | Major triad + M7 | I7, IV7 | Cmaj7, C-triangle-7 |
| Dominant seventh | Major triad + m7 | V7 | C7 |
| Minor seventh | Minor triad + m7 | ii7, iii7, vi7 | Cm7, C-7 |
| Half-diminished seventh | Dim triad + m7 | vii-ø-7 | Cm7b5, C-ø-7 |
| Fully diminished seventh | Dim triad + d7 | vii-degrees-7 (minor key) | Cdim7, C-degrees-7 |

The dominant seventh is the most harmonically active of these — its tritone (between the third and seventh of the chord) creates a strong pull toward resolution.

### Inversions

Triads have three positions; seventh chords have four:

| Triad position | Bass note | Figured bass | Seventh chord position | Bass note | Figured bass |
|---|---|---|---|---|---|
| Root position | Root | 5/3 (or blank) | Root position | Root | 7 |
| First inversion | Third | 6 or 6/3 | First inversion | Third | 6/5 |
| Second inversion | Fifth | 6/4 | Second inversion | Fifth | 4/3 |
| — | — | — | Third inversion | Seventh | 4/2 or 2 |

Second-inversion triads (6/4 chords) are unstable and appear in three standard contexts: cadential 6/4 (I-6/4 resolving to V), passing 6/4 (connecting two root-position or first-inversion chords), and pedal 6/4 (upper voices move over a stationary bass).

## Part II — Roman Numeral Analysis

Roman numeral analysis identifies each chord by its scale-degree root and quality relative to the prevailing key. This is the standard analytical language of Western tonal music.

**Notation conventions:**
- Uppercase Roman numeral = major triad (I, IV, V)
- Lowercase Roman numeral = minor triad (ii, iii, vi)
- Superscript circle = diminished (vii-degrees)
- Superscript plus = augmented (III+)
- Arabic numerals indicate inversions (figured bass shorthand)
- Slash notation for applied (secondary) chords: V/V means "V of V"

**Worked analysis: Bach Chorale "Ich bin's, ich sollte bussen" (St. Matthew Passion, No. 16)**

Key: E major

```
Soprano:  E   | D#  | E   F# | G#  | F#  E   | D#  | E
Alto:     B   | B   | B   D# | E   | D#  C#  | B   | B
Tenor:    G#  | F#  | G#  A  | B   | B   A   | F#  | G#
Bass:     E   | B   | E   D# | C#  | D#  A   | B   | E
Roman:    I   | V   | I  V6/5/iv| vi  |V6/4/V IV| V   | I
```

Measure-by-measure:
1. **I** — Tonic establishes the key.
2. **V** — Dominant in root position; standard tonic-to-dominant motion.
3. **I to V6/5 of vi** — The tonic resolves, then a secondary dominant (applied chord) targets vi.
4. **vi** — The secondary dominant resolves to its target; this is a tonicization, not a modulation (the key does not change).
5. **Cadential 6/4 to IV** — The cadential 6/4 functions as a dominant preparation; IV provides plagal color.
6. **V** — The dominant, prepared by IV.
7. **I** — Authentic cadence. The progression V-I closes the phrase.

This chorale phrase demonstrates three fundamental harmonic principles: (1) tonic-dominant polarity frames the phrase, (2) secondary dominants create momentary tonal tension without leaving the key, and (3) the cadential 6/4 is a voice-leading event over dominant harmony, not an independent tonic chord.

## Part III — Voice Leading

Voice leading governs how individual voices (soprano, alto, tenor, bass) move from one chord to the next. Good voice leading produces smooth, singable lines and avoids forbidden parallels.

### The Four Rules

1. **No parallel fifths.** Two voices moving in parallel perfect fifths (e.g., C-G to D-A) produce a hollow, medieval sound that undermines harmonic independence. This was the first prohibition codified in Renaissance counterpoint.

2. **No parallel octaves.** Two voices moving in parallel octaves (or unisons) reduce four-part texture to three effective voices. The doubling adds power but removes independence.

3. **Resolve the leading tone.** In a V-I progression, the seventh scale degree (the leading tone) must resolve up by step to the tonic, especially when in the soprano. Exception: in inner voices, the leading tone may descend to the fifth of the tonic chord to achieve a complete chord.

4. **Resolve the chordal seventh.** In any seventh chord, the seventh (the dissonant note) resolves down by step. In V7-I, the seventh of V (the fourth scale degree) resolves down to the third of I.

### Voice Leading Principles (Beyond the Rules)

- **Common tones.** When two successive chords share a note, keep it in the same voice. This is the simplest form of smooth voice leading.
- **Stepwise motion.** Move the remaining voices by the smallest possible interval. Leaps larger than a fourth should be followed by stepwise motion in the opposite direction.
- **Contrary motion with the bass.** When the bass leaps, the upper voices should move in contrary motion (opposite direction) to achieve balance.
- **Spacing.** Adjacent upper voices (soprano-alto, alto-tenor) should be no more than an octave apart. The tenor-bass gap may be larger (up to two octaves in orchestral writing).

### Worked Example — Harmonizing V7 to I in C Major

```
Soprano:  B  ->  C    (leading tone resolves up to tonic)
Alto:     F  ->  E    (chordal seventh resolves down by step)
Tenor:    D  ->  C    (common tone available, but stepwise descent
                        to tonic also valid; here resolves down)
Bass:     G  ->  C    (root motion: V to I, descending fifth)
```

Result: V7 (G-B-D-F) resolves to I (C-C-E-C). The I chord is incomplete (tripled root, no fifth) — this is normal and expected when properly resolving all tendency tones.

## Part IV — Cadences

A cadence is a harmonic arrival point that articulates phrase structure. Four principal types:

### Authentic Cadence (AC)

**V (or V7) to I.** The strongest cadence. A **perfect authentic cadence** (PAC) has: root-position V, root-position I, and the tonic in the soprano on the final chord. An **imperfect authentic cadence** (IAC) weakens one of these conditions (inverted V, inverted I, or non-tonic note in soprano).

**Harmonic weight:** Conclusive. Used at the ends of sections and pieces.

### Half Cadence (HC)

**Any chord to V.** The phrase ends on the dominant, creating an open, unresolved feeling — like a comma in prose. Common approaches: I-V, ii-V, IV-V, vi-V.

**Harmonic weight:** Suspensive. Demands continuation.

### Deceptive Cadence (DC)

**V to vi (or another non-tonic chord).** The ear expects I after V; the substitution of vi creates surprise. The deceptive cadence works because vi shares two of three notes with I (in C major: I = C-E-G, vi = A-C-E), so the resolution is smooth despite being unexpected.

**Voice leading implication:** The leading tone still resolves up to tonic. The bass, instead of moving to the tonic, moves to the sixth scale degree.

### Plagal Cadence (PC)

**IV to I.** The "Amen" cadence. Weaker than authentic because it lacks the leading-tone drive of V. Often follows a PAC as a post-cadential extension.

## Part V — Secondary Dominants and Tonicization

A secondary dominant (or applied dominant) is a major triad or dominant seventh chord that functions as V (or V7) of a diatonic chord other than I. It temporarily "tonicizes" the target chord without establishing a new key.

**Available secondary dominants in C major:**

| Symbol | Chord | Target | Resolves to |
|---|---|---|---|
| V/ii | A-C#-E (or A7) | ii (Dm) | D minor |
| V/iii | B-D#-F# (or B7) | iii (Em) | E minor |
| V/IV | C-E-G-Bb (C7) | IV (F) | F major |
| V/V | D-F#-A (or D7) | V (G) | G major |
| V/vi | E-G#-B (or E7) | vi (Am) | A minor |

**V/vii-degrees is theoretically possible but practically absent** because the target (vii-degrees, a diminished triad) is too unstable to function as a convincing temporary tonic.

**Identification rule:** When an accidental appears in a chord that is not part of the current key signature, check whether that chord functions as V or V7 of the chord that follows. If yes, it is a secondary dominant.

**Worked example.** In C major, the progression C - A7 - Dm - G7 - C is analyzed as I - V7/ii - ii - V7 - I. The A7 chord (A-C#-E-G) contains C#, which is not in C major. It resolves to Dm (ii), confirming it as V7/ii.

## Part VI — Modulation

Modulation is the process of changing from one key to another. Unlike tonicization (a brief visit), modulation establishes a new key through cadential confirmation.

### Pivot Chord Modulation (Common Chord)

The most common technique. A chord that is diatonic in both the old key and the new key serves as the pivot — the hinge between tonal centers.

**Worked example.** Modulation from C major to G major.

```
C major:    I    IV   V    I   |  (pivot)  |  ii   V7    I
G major:                       |  IV       |  ii   V7    I
Chords:     C    F    G    C   |  C        |  Am   D7    G
```

The C major chord is simultaneously I in C major and IV in G major. After the pivot, the cadence ii-V7-I in G major confirms the new key.

**Finding pivots:** List the diatonic chords of both keys; any chord appearing in both lists is a potential pivot. Closely related keys (differing by one accidental) share the most pivot chords.

### Chromatic Modulation (Direct)

No pivot chord. The modulation is signaled by a chromatic alteration — a note that does not belong to either key appears, and the music proceeds directly into the new key.

**Typical signal:** A chromatic bass line moves by half step into the new dominant or tonic.

### Enharmonic Modulation

A chord is reinterpreted enharmonically to serve a different function in the new key. Two classic vehicles:

1. **Diminished seventh reinterpretation.** A fully diminished seventh chord has four possible enharmonic spellings (any of its four notes can be the root). This means one diminished seventh chord can resolve to four different keys.

2. **German augmented sixth = dominant seventh.** The German augmented sixth chord (e.g., Ab-C-Eb-F# in C major) is enharmonically equivalent to a dominant seventh chord (Ab-C-Eb-Gb = Ab7). Respelling F# as Gb reinterprets the chord as V7 of Db, enabling a remote modulation.

## Part VII — Chromatic Harmony

### Neapolitan Chord (bII or N)

A major triad built on the lowered second scale degree: in C major, Db-F-Ab. Almost always appears in first inversion (bII6), functioning as a subdominant substitute that intensifies the approach to the dominant.

**Standard progression:** bII6 - V - I.

**Voice leading:** The bass (F, the fourth scale degree) moves to the leading tone (B) in V. The root of the Neapolitan (Db) resolves down chromatically to C (or to B if moving to V).

### Augmented Sixth Chords

Three types, all containing the interval of an augmented sixth between the bass and an upper voice. This interval resolves outward by half steps to an octave on the dominant.

| Type | Notes (in C minor) | Extra note(s) | Resolution |
|---|---|---|---|
| Italian (It+6) | Ab - C - F# | (none beyond 3rd) | Ab->G, F#->G = octave on G |
| French (Fr+6) | Ab - C - D - F# | adds the 2nd (D) | Same outer resolution; D also resolves to D or moves to B |
| German (Ger+6) | Ab - C - Eb - F# | adds the b5th (Eb) | Same outer resolution; Eb can move to D (via cad. 6/4) |

**The German augmented sixth resolves to V via a cadential 6/4** to avoid parallel fifths between Ab-Eb (resolving to G-D).

## Part VIII — Jazz Chord Symbols (Lead Sheet Notation)

Jazz and popular music use a different notation system from Roman numerals. Where Roman numerals show function within a key, jazz symbols show absolute chord identity.

**Reading jazz symbols:**

| Symbol | Meaning | Notes (on C) |
|---|---|---|
| C | Major triad | C-E-G |
| Cm or C- | Minor triad | C-Eb-G |
| C7 | Dominant seventh | C-E-G-Bb |
| Cmaj7 or C-triangle | Major seventh | C-E-G-B |
| Cm7 or C-7 | Minor seventh | C-Eb-G-Bb |
| Cdim7 or C-degrees-7 | Fully diminished seventh | C-Eb-Gb-Bbb(=A) |
| C-ø-7 or Cm7b5 | Half-diminished seventh | C-Eb-Gb-Bb |
| C+ or Caug | Augmented triad | C-E-G# |
| Csus4 | Suspended fourth | C-F-G |
| C9, C11, C13 | Extended dominant | Add 9th, 11th, or 13th above dominant 7th |
| Cmaj9 | Extended major | Major 7th + 9th |
| C7#9 | Altered dominant | Dominant 7th + raised 9th ("Hendrix chord") |

**Slash chords.** C/E means C major with E in the bass (first inversion). Db/F is the Neapolitan sixth. Slash chords are not a separate chord type — they indicate inversions or pedal tones.

## Part IX — Functional Harmony vs. Linear Harmony

### Functional Harmony (Rameau's Model)

Every chord serves one of three functions:

- **Tonic function (T):** Stability, home. Chords: I, vi, iii.
- **Predominant function (PD):** Departure from tonic, preparation for dominant. Chords: IV, ii, (vi in some contexts).
- **Dominant function (D):** Tension demanding resolution to tonic. Chords: V, vii-degrees.

Standard functional progression: T -> PD -> D -> T. The functional model explains why ii-V-I is the strongest cadential progression — it moves through all three functional areas in sequence.

### Linear (Chromatic) Harmony

Not all harmonic motion is function-driven. In chromatic or late-Romantic music (Wagner, Strauss, Debussy), chords often connect through voice-leading logic rather than functional relationships. The augmented triad, for example, functions as a chromatic passing chord between two diatonic chords, connected by semitone voice leading rather than root motion.

**When functional analysis fails:** If Roman numeral labels become forced or arbitrary, switch to a voice-leading or set-class analysis. Music by Debussy, early Schoenberg, or Scriabin often rewards linear analysis over functional.

## When to Use This Skill

- Analyzing chord progressions in any tonal style (Baroque through jazz)
- Harmonizing a melody with appropriate chord choices
- Identifying and resolving tendency tones in voice leading
- Determining key areas and modulation paths in a score
- Translating between Roman numeral analysis and jazz lead sheet notation
- Writing four-part chorale-style harmony

## When NOT to Use This Skill

- For contrapuntal analysis (fugue, canon, species counterpoint) — use **counterpoint** skill
- For rhythmic or metric analysis — use **rhythm-meter** skill
- For large-scale formal analysis (sonata form, rondo) — use **form-analysis** skill
- For instrumentation and timbral choices — use **orchestration** skill
- For atonal or twelve-tone music — functional harmony does not apply; pitch-class set analysis is more appropriate

## Cross-References

- **rameau agent:** Harmonic function and fundamental bass theory. Named for Jean-Philippe Rameau, who formulated the theory of chord inversion and fundamental bass in *Traite de l'harmonie* (1722), establishing the framework that all subsequent tonal harmonic analysis builds upon.
- **bach agent:** Voice leading and chorale harmonization. Named for J.S. Bach, whose 371 chorales remain the primary teaching corpus for four-part voice leading.
- **clara-schumann agent:** Performance interpretation of harmonic structure; how harmonic analysis informs expressive decisions in performance.
- **coltrane agent:** Jazz harmonic structures, substitution patterns, and extended harmony.
- **counterpoint skill:** Contrapuntal voice-leading techniques that complement harmonic analysis.
- **form-analysis skill:** Large-scale harmonic structure as it shapes formal design.
- **ear-training skill:** Aural identification of chord qualities, inversions, and cadences.

## References

- Rameau, J.-P. (1722). *Traite de l'harmonie reduite a ses principes naturels*. Paris.
- Aldwell, E., Schachter, C., & Cadwallader, A. (2019). *Harmony and Voice Leading*. 5th edition. Cengage.
- Kostka, S., Payne, D., & Almen, B. (2018). *Tonal Harmony*. 8th edition. McGraw-Hill.
- Laitz, S. G. (2016). *The Complete Musician*. 4th edition. Oxford University Press.
- Levine, M. (1995). *The Jazz Theory Book*. Sher Music.
- Bach, J. S. *371 Chorales*. Various editions. (Riemenschneider numbering standard.)
- Piston, W. (1987). *Harmony*. 5th edition, revised by DeVoto. W.W. Norton.
