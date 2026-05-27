---
name: counterpoint
description: Contrapuntal writing and analysis covering species counterpoint, fugue structure, canon types, and imitative techniques. Covers Fux's five species, cantus firmus construction, consonance and dissonance treatment, invertible counterpoint, fugue anatomy (subject, answer, countersubject, episode, stretto), canon varieties, and contrapuntal practice from Palestrina through Shostakovich. Use when writing or analyzing counterpoint, studying fugue structure, or understanding the linear dimension of polyphonic music.
type: skill
category: music
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/music/counterpoint/SKILL.md
superseded_by: null
---
# Counterpoint

Counterpoint is the art of combining independent melodic lines that sound together harmonically. Where harmonic analysis reads music vertically (chords at a moment in time), contrapuntal analysis reads music horizontally (melodies across time). The word derives from Latin *punctus contra punctum* — "note against note." Counterpoint is simultaneously the oldest and most rigorous discipline in Western music theory, with an unbroken pedagogical tradition from the Renaissance through the present day.

**Agent affinity:** rameau (harmonic dimension of counterpoint), bach (fugue, invention, chorale)

**Concept IDs:** harmony, chord-progressions, scales-intervals

## Part I — Species Counterpoint (Fux's Gradus)

Johann Joseph Fux codified species counterpoint in *Gradus ad Parnassum* (1725), structuring the discipline into five progressive species. The method starts with the simplest rhythmic relationship (note against note) and systematically introduces complexity. Nearly three centuries later, this remains the standard pedagogical framework.

### The Cantus Firmus

Every species exercise begins with a **cantus firmus** (CF) — a fixed melody, typically 8-12 notes, all whole notes, in a church mode. The student writes a counterpoint line against it.

**Properties of a good cantus firmus:**
- Mostly stepwise motion (conjunct), with no more than two consecutive leaps
- Range within a tenth
- A single climax (highest note), reached by step or small leap, not repeated
- Begins and ends on the modal final (tonic)
- No repeated notes (maintains rhythmic momentum)
- No augmented or diminished intervals (melodic)
- No chromatic motion

**Example cantus firmus in D Dorian:**

```
D - F - E - D - G - F - A - G - F - E - D
```

This CF moves mostly by step, has a single climax on A, spans an octave (D to D), and begins and ends on D.

### First Species — Note Against Note

One note of counterpoint for each note of the cantus firmus. All intervals between the two voices are consonances.

**Consonance table:**

| Interval | Type | Treatment |
|---|---|---|
| Unison | Perfect consonance | Only at beginning and end |
| Third | Imperfect consonance | Freely used, backbone of counterpoint |
| Fifth | Perfect consonance | Approached by contrary or oblique motion |
| Sixth | Imperfect consonance | Freely used |
| Octave | Perfect consonance | Approached by contrary or oblique motion |

**Rules:**
1. Begin and end on a perfect consonance (unison, fifth, or octave).
2. No parallel fifths or parallel octaves between successive intervals.
3. No direct (hidden) fifths or octaves — two voices moving in the same direction to a perfect consonance by leap in the upper voice.
4. Prefer contrary motion (voices move in opposite directions) and oblique motion (one voice holds while the other moves).
5. Imperfect consonances (thirds and sixths) should predominate. A string of perfect consonances sounds hollow.

**Worked example.** Counterpoint above the CF in D Dorian:

```
CF:    D  | F  | E  | D  | G  | F  | A  | G  | F  | E  | D
CP:    A  | A  | G  | F  | B  | A  | C  | B  | A  | G  | D (8ve below: octave)
Int:   5  | 3  | 3  | 3  | 3  | 3  | 3  | 3  | 3  | 3  | 8
```

The counterpoint begins on a fifth and ends on an octave. Motion between every pair of notes is either contrary or oblique. Imperfect consonances dominate. No parallel fifths or octaves appear.

### Second Species — Two Notes Against One

Two half notes in the counterpoint against each whole note of the cantus firmus. Dissonance enters the picture: the second half note in each bar may be a **passing tone** (dissonance approached and left by step in the same direction).

**Rules beyond first species:**
1. Downbeats must be consonant with the CF.
2. Upbeats may be dissonant only as passing tones (stepwise approach, stepwise departure, same direction).
3. No unisons on upbeats (weakens independence).
4. Begin with a half rest followed by a consonance.

### Third Species — Four Notes Against One

Four quarter notes against each whole note. Dissonance may appear on beats 2, 3, or 4 as passing tones or **neighbor tones** (step away from a consonance and step back to the same note). The first beat of each bar must be consonant.

**Neighbor tone (auxiliary):** A dissonance reached by step from a consonance and returning by step to the same consonance. The nota cambiata (changing tone) pattern — a descending step from a consonance to a dissonance, then a descending leap of a third to a consonance — is also permitted in third species.

### Fourth Species — Syncopated (Suspensions)

Tied whole notes across the barline create **suspensions** — the most expressive dissonance treatment in tonal counterpoint.

**Suspension mechanics:**

1. **Preparation:** The note is consonant on a weak beat.
2. **Suspension:** The note is held (tied) into the next strong beat, where it becomes dissonant against the CF.
3. **Resolution:** The suspended note moves down by step to a consonance.

**Standard suspension types:**

| Suspension | Intervals (against bass) | Resolution |
|---|---|---|
| 7-6 | Seventh resolves to sixth | Most common upper-voice suspension |
| 4-3 | Fourth resolves to third | Common in cadences |
| 9-8 | Ninth resolves to octave | Really a 2-1 in a higher octave |
| 2-3 (bass) | Second resolves to third | Bass suspension (resolves DOWN) |

**Rule:** If no suspension is possible on a given beat, tie a consonance across the barline instead (a consonant suspension, or "consonant syncopation"). Never break the syncopated rhythm arbitrarily.

### Fifth Species — Florid Counterpoint

Free combination of all previous species. The counterpoint mixes whole notes, half notes, quarter notes, and suspensions in a musically convincing line. This is the closest species approach to free composition.

**Guidelines:**
- Maintain rhythmic variety; do not settle into one species for too long
- The florid line should be singable and well-shaped as an independent melody
- Dissonance treatment follows the rules of whichever species is locally active
- Suspensions should be used at cadence points for maximum effect

## Part II — Consonance and Dissonance Treatment

The treatment of dissonance is what separates counterpoint from mere chord stacking. In strict counterpoint, every dissonance must be prepared, approached, and resolved according to specific rules. The rules are not arbitrary — they emerged from centuries of vocal practice and reflect what singers can tune reliably in ensemble.

### Hierarchy of Dissonance Treatment

| Treatment | Description | Species |
|---|---|---|
| Passing tone | Step-step, same direction | 2nd and above |
| Neighbor tone | Step away, step back to same note | 3rd and above |
| Suspension | Tied over barline, resolves down by step | 4th and above |
| Anticipation | Consonance arrived early, on weak beat | 5th (florid) |
| Escape tone | Step from consonance, leap away (rare) | 5th (florid) |
| Appoggiatura | Leap to dissonance, step resolution (free comp.) | Free composition |

**Critical principle:** In strict counterpoint, dissonances on strong beats must be suspensions. Dissonances on weak beats must be passing or neighbor tones. The appoggiatura (accented, non-prepared dissonance) belongs to free composition, not strict species work.

## Part III — Invertible Counterpoint

Two contrapuntal lines are in **invertible counterpoint** if they can swap registral positions — the upper voice becomes the lower voice and vice versa — and the result remains correct counterpoint.

### Invertible Counterpoint at the Octave

When lines swap by an octave, intervals transform: a third becomes a sixth, a fifth becomes a fourth, a sixth becomes a third. The critical issue: a fifth (consonant) becomes a fourth (dissonant in two-part writing). Therefore, invertible counterpoint at the octave avoids fifths between the voices.

**Interval transformation table (at the octave):**

| Original | Inversion | Status |
|---|---|---|
| Unison | Octave | OK |
| Second | Seventh | Dissonance -> dissonance |
| Third | Sixth | Consonance -> consonance |
| Fourth | Fifth | Dissonance -> consonance |
| Fifth | Fourth | Consonance -> DISSONANCE |
| Sixth | Third | Consonance -> consonance |
| Seventh | Second | Dissonance -> dissonance |

**Practical result:** Use thirds and sixths as the primary consonances; avoid fifths. This is why Bach's two-part inventions are built overwhelmingly on thirds and sixths.

### Invertible Counterpoint at the Tenth and Twelfth

At the tenth: thirds become octaves, sixths become fifths. Both are consonant. More freedom than octave inversion.

At the twelfth: thirds become thirds, sixths become sevenths (problematic). Used in specific fugal contexts where the dissonance can be controlled.

## Part IV — Fugue Structure

The fugue is the most developed contrapuntal form. It is not a fixed form (like sonata form) but a process — a procedure for developing a subject through systematic imitative entries and tonal contrast.

### Anatomy of a Fugue

| Section | Function | Characteristics |
|---|---|---|
| **Subject** | The main theme | A memorable melody, typically 1-4 bars, establishing the tonic key. Defines the fugue's character. |
| **Answer** | Imitative entry | The subject transposed to the dominant (fifth above). May be **real** (exact transposition) or **tonal** (adjusted to preserve tonic-dominant balance). |
| **Countersubject** | Accompanying line | A countermelody that sounds against the answer (and later entries). Designed in invertible counterpoint with the subject. |
| **Episode** | Development, transition | Modulatory passages between subject entries. Typically built from fragments (motives) of the subject or countersubject, developed by sequence. |
| **Stretto** | Climactic intensification | Subject entries overlap — the answer begins before the subject finishes. Creates density and urgency. Not all fugues use stretto. |
| **Pedal point** | Pre-cadential tension | A sustained or reiterated bass note (usually tonic or dominant) over which the upper voices continue in counterpoint. Common before the final cadence. |

### Exposition

The **exposition** is the opening section where the subject is presented in each voice in turn:

1. Voice 1 states the subject in the tonic.
2. Voice 2 enters with the answer in the dominant while Voice 1 continues with the countersubject.
3. Voice 3 enters with the subject in the tonic (if three voices) while Voices 1 and 2 continue with free counterpoint or second countersubject.
4. Voice 4 enters with the answer in the dominant (if four voices).

A **codetta** (short bridge) may connect entries when the end of one entry does not smoothly lead to the next.

### Real vs. Tonal Answer

A **real answer** transposes the subject exactly to the dominant. A **tonal answer** modifies intervals — typically adjusting a prominent tonic-dominant leap (C-G) to a dominant-tonic response (G-C) to keep the answer from modulating too far. The decision depends on whether the subject begins or prominently features the dominant note.

**Rule of thumb:** If the subject starts on or prominently leaps to the fifth scale degree, use a tonal answer. If the subject is stepwise and confined to the tonic triad, a real answer works.

### Worked Example — Bach, Well-Tempered Clavier, Book I, Fugue No. 2 in C Minor (BWV 847)

Three voices. Subject: a rapid, descending chromatic line in the soprano (C-B-C-D-Eb-F-D-Eb — compressed into one bar). The subject's chromaticism defines the fugue's character.

**Exposition:**
- Bar 1: Soprano states subject in C minor.
- Bar 3: Alto enters with tonal answer in G minor; soprano continues with countersubject (syncopated, ascending line — contrast to the descending subject).
- Bar 5: Bass enters with subject in C minor; alto and soprano continue in invertible counterpoint.

**Middle entries:** Episodes modulate to Eb major (relative major), F minor, and Ab major. Each episode sequences fragments of the subject's chromatic descent.

**Stretto (bar 20):** The subject enters in the bass before the soprano's statement is complete. The overlap compresses two bars of material into one, creating the climactic tension of the fugue.

**Final pedal:** A tonic pedal in the bass (bars 28-29) supports free counterpoint above, followed by the final authentic cadence in C minor.

## Part V — Canon

A canon is strict imitation — one voice is an exact (or near-exact) copy of another, offset in time and possibly transposed.

### Canon Types

| Type | Description | Example |
|---|---|---|
| **Canon at the unison** | Follower enters at the same pitch | "Row, Row, Row Your Boat" |
| **Canon at the fifth** | Follower enters a fifth higher (or fourth lower) | Pachelbel's Canon in D (bass + upper voices) |
| **Canon at the octave** | Follower enters an octave higher or lower | Common in keyboard music |
| **Inversion canon** | Follower mirrors the leader's intervals (up becomes down) | Bach, *Art of Fugue*, Contrapunctus XII |
| **Retrograde canon** | Follower plays the leader's melody backwards | Bach, *Musical Offering*, Canon 1a |
| **Augmentation canon** | Follower uses doubled note values | Subject in augmentation in *Art of Fugue* |
| **Diminution canon** | Follower uses halved note values | Ockeghem, *Missa Prolationum* |
| **Spiral (modulating) canon** | Each iteration modulates upward; after N iterations, returns to original key | Bach, *Musical Offering*, Canon per Tonos (modulates through all keys) |
| **Puzzle canon** | Only one voice is written; performer must derive the other(s) | Bach, *Musical Offering*, various |

### Canon as Constraint

Canon composition is a constraint-satisfaction problem: the leader must be written such that when the follower enters (at a given interval and delay), the resulting counterpoint is harmonically correct. This makes canon the most rigorous form of counterpoint — there is no freedom to adjust the follower independently.

**Composing a canon at the unison (practical method):**
1. Write the first two bars of the leader.
2. Enter the follower (offset by the chosen delay, say 2 bars).
3. Write bar 3 of the leader so it forms correct counterpoint with bar 1 of the follower (which is identical to bar 1 of the leader).
4. Continue, always checking that each new bar works both as melody and as counterpoint against the delayed copy.

## Part VI — Historical Contrapuntal Practice

### Palestrina (1525-1594) — The Renaissance Ideal

Giovanni Pierluigi da Palestrina's style codified the "rules" of strict counterpoint that Fux later systematized. Key characteristics:

- **Vocal idiom.** Every line must be singable. No augmented intervals, no leaps larger than an octave (minor sixth is the practical limit), large leaps recovered by step in the opposite direction.
- **Dissonance as momentary event.** Dissonances are passing tones, neighbor tones, or suspensions — always prepared and resolved. No accented dissonances (no appoggiaturas).
- **Consonance on strong beats.** The rhythmic hierarchy is sacred: strong beats are consonant, weak beats may be dissonant.
- **Text-driven rhythm.** Musical rhythm follows the natural stress of Latin text.
- **Mode, not key.** Palestrina writes in the eight church modes, not major/minor keys. Modal cadences (Phrygian, Dorian) shape the harmonic vocabulary.

### Bach (1685-1750) — Baroque Counterpoint

Bach's counterpoint absorbs and extends Palestrina's voice-leading principles within the tonal (key-based) system.

- **Tonal harmony as framework.** Bach's counterpoint implies chord progressions. Lines are independent but generate functional harmony when combined.
- **Invertible counterpoint is structural.** Bach routinely writes subjects and countersubjects that invert at the octave, tenth, or twelfth.
- **Fugue as process.** The 48 fugues of the Well-Tempered Clavier explore every combinatorial possibility: 2-5 voices, all keys, real and tonal answers, stretto, augmentation, inversion.
- **Dissonance treatment expanded.** Bach uses appoggiaturas, suspensions, and chromatic passing tones more freely than Palestrina, but always within a voice-leading logic that can be traced back to species principles.
- **The Art of Fugue (BWV 1080).** Bach's final contrapuntal work: a single subject developed through 14 fugues and 4 canons, exploring every fugal and canonic technique. The unfinished Contrapunctus XIV (quadruple fugue) breaks off at the entry of the B-A-C-H subject (Bb-A-C-B in German note names).

### Hindemith (1895-1963) — Modern Tonal Counterpoint

Paul Hindemith extended counterpoint into a tonal language that abandoned major/minor key centers while retaining a pitch hierarchy based on overtone relationships.

- **Interval ranking by consonance.** Hindemith ranked all intervals from most to least consonant using acoustics, not tradition: octave > fifth > fourth > major third > minor third > major second > minor second > tritone.
- **Two-voice framework.** The outer voices (soprano and bass) determine harmonic quality; inner voices fill in. This inverts the Palestrinian model where all voices are equally important.
- **Cadential substitutes.** Without functional harmony, Hindemith uses interval contractions (e.g., tritone resolving to a third) as cadential gestures.

### Shostakovich (1906-1975) — Fugue as Political Voice

Shostakovich's 24 Preludes and Fugues, Op. 87 (1950-51, inspired by Bach's WTC after attending the 1950 Bach bicentennial in Leipzig) apply fugal technique to a 20th-century tonal vocabulary.

- **Dissonance as structural.** Where Bach's dissonances resolve within a beat or two, Shostakovich sustains dissonance across entire phrases.
- **Rhythmic counterpoint.** Voices are differentiated by rhythm as much as by pitch — a technique that would be unthinkable in species counterpoint but expands the contrapuntal palette.
- **Fugue as autobiography.** The DSCH motif (D-Eb-C-B in German notation, Shostakovich's musical signature) appears as a fugue subject, embedding personal identity in contrapuntal structure.

## When to Use This Skill

- Writing or analyzing fugues, canons, and imitative textures
- Studying species counterpoint exercises (academic or creative)
- Analyzing Bach inventions, sinfonias, and fugues
- Understanding the linear (voice-leading) dimension of harmonic progressions
- Writing countermelodies and independent inner voices in any style
- Evaluating the relationship between historical contrapuntal rules and modern practice

## When NOT to Use This Skill

- For vertical harmonic analysis (chord progressions, Roman numerals) — use **harmony-analysis** skill
- For rhythmic analysis and meter — use **rhythm-meter** skill
- For orchestration and timbral choices — use **orchestration** skill
- For ear training and aural identification — use **ear-training** skill
- For large-scale formal analysis — use **form-analysis** skill

## Cross-References

- **bach agent:** Fugue composition, invention analysis, chorale harmonization. The primary agent for all contrapuntal work. Named for J.S. Bach, whose contrapuntal mastery is unmatched in Western music history.
- **rameau agent:** Harmonic function within contrapuntal textures. Rameau's harmonic theory and Bach's counterpoint represent complementary perspectives on the same music.
- **clara-schumann agent:** Performance interpretation of contrapuntal music — voicing, phrasing, and tempo decisions informed by contrapuntal analysis.
- **bartok agent:** 20th-century contrapuntal techniques, particularly Bartok's use of canon and fugue within folk-music-derived tonality.
- **harmony-analysis skill:** Harmonic analysis complements contrapuntal analysis — most tonal music rewards both vertical and horizontal reading.
- **form-analysis skill:** Fugue is a formal process; understanding fugal structure requires form-analysis concepts.
- **ear-training skill:** Aural identification of imitative entries, canonic passages, and voice independence.

## References

- Fux, J. J. (1725). *Gradus ad Parnassum*. Vienna. (Mann translation, 1965, W.W. Norton.)
- Jeppesen, K. (1939). *Counterpoint: The Polyphonic Vocal Style of the Sixteenth Century*. Prentice-Hall. (Reprint: Dover, 1992.)
- Kennan, K. (1999). *Counterpoint Based on Eighteenth-Century Practice*. 4th edition. Prentice-Hall.
- Gauldin, R. (1995). *A Practical Approach to Eighteenth-Century Counterpoint*. 2nd edition. Waveland Press.
- Mann, A. (1987). *The Study of Fugue*. Dover.
- Hindemith, P. (1942). *The Craft of Musical Composition*, Vol. 1. Schott/Associated Music Publishers.
- Bach, J. S. *The Well-Tempered Clavier*, BWV 846-893. *The Art of Fugue*, BWV 1080. *Two-Part Inventions*, BWV 772-786. *Three-Part Sinfonias*, BWV 787-801.
- Shostakovich, D. (1950-51). *24 Preludes and Fugues*, Op. 87.
