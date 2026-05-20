---
name: rhythm-meter
description: Rhythmic analysis, meter classification, groove mechanics, and cross-cultural rhythmic systems. Covers simple and compound meter, asymmetric meters, polyrhythm, polymetric structures, metric modulation, swing and groove analysis, syncopation patterns, hemiola, additive vs. divisive rhythm, African timeline patterns, Indian tala, and Messiaen's non-retrogradable rhythms. Use when analyzing rhythmic structure, identifying meter, studying groove, or working with non-Western rhythmic systems.
type: skill
category: music
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/music/rhythm-meter/SKILL.md
superseded_by: null
---
# Rhythm and Meter

Rhythm is the temporal organization of sound — the pattern of durations and accents that gives music its sense of motion and time. Meter is the recurring framework of strong and weak beats that organizes rhythm into predictable cycles. Together, they are the most fundamental dimension of music: a piece can exist without melody or harmony (a drum pattern), but it cannot exist without rhythm. This skill covers Western metric classification, cross-cultural rhythmic systems, groove analysis, and advanced rhythmic techniques from Bartok through Messiaen.

**Agent affinity:** bartok (asymmetric meters, folk-derived rhythm), coltrane (swing, jazz rhythm, polyrhythm)

**Concept IDs:** rhythm, meter, syncopation

## Part I — Meter Classification

### Beat and Division

Every meter has two layers: the **beat** (the pulse you tap your foot to) and the **division** (how each beat subdivides).

- **Simple meter:** Each beat divides into TWO equal parts. Time signatures: 2/4, 3/4, 4/4, 2/2.
- **Compound meter:** Each beat divides into THREE equal parts. Time signatures: 6/8, 9/8, 12/8.

The top number of a time signature tells you how many beat-units per measure. The bottom number tells you which note value gets one beat-unit.

**Distinguishing 3/4 from 6/8:** Both have six eighth notes per measure, but the metric stress differs:

```
3/4:   ONE two | THREE four | FIVE six      (3 beats, each divides in 2)
       >       | >         | >

6/8:   ONE two three | FOUR five six         (2 beats, each divides in 3)
       >             | >
```

3/4 is a simple triple meter (three beats per measure, each subdividing in two). 6/8 is a compound duple meter (two beats per measure, each subdividing in three). They sound fundamentally different despite containing the same number of eighth notes.

### Metric Hierarchy

Meter operates in nested levels:

1. **Division level:** The smallest regular pulse (eighth notes in 4/4, eighth-note triplets in compound meter).
2. **Beat level:** The primary pulse (quarter note in 4/4, dotted quarter in 6/8).
3. **Measure level:** Grouping of beats (strong-weak in duple, strong-weak-weak in triple).
4. **Hypermeter:** Grouping of measures into larger phrases. In most common-practice music, four-bar hypermeter is standard — the first measure of each four-bar group carries a hypermetric strong beat.

**Worked example of hypermetric analysis — "Happy Birthday":**

```
Measure: | 1        | 2        | 3        | 4        |
Hyper:   | STRONG   | weak     | STRONG   | weak     |
Text:    | Happy    | birthday | to       | you,     |
```

The melodic and harmonic arrivals align with hypermetric strong beats (measures 1 and 3). This four-bar grouping is so pervasive in Western music that deviations from it (Beethoven's five-bar phrases, Stravinsky's irregular groupings) are immediately perceptible.

## Part II — Asymmetric and Additive Meters

### Asymmetric Meter

Meters where beat lengths are unequal. The beats cannot be evenly divided into groups of two or three — instead, they combine groups of 2 and 3 in irregular patterns.

**Common asymmetric meters:**

| Time signature | Beat grouping | Character |
|---|---|---|
| 5/8 | 2+3 or 3+2 | Limping, energetic; common in folk music |
| 7/8 | 2+2+3 or 3+2+2 or 2+3+2 | Three unequal beats; Balkan dance rhythms |
| 11/8 | 3+2+3+3 or 2+3+3+3 | Complex; Brubeck's "Blue Rondo a la Turk" uses 2+2+2+3 |

**Bartok and Bulgarian rhythms.** Bela Bartok transcribed thousands of Hungarian, Romanian, Slovak, and Bulgarian folk songs. Bulgarian folk dance uses additive meters that Bartok called "Bulgarian rhythms" — irregular groupings of 2s and 3s at fast tempos where the shortest unit (the eighth note) is the pulse, not the "beat" in the Western sense.

**Worked example — Bartok, String Quartet No. 5, Scherzo (3rd movement):**

The movement alternates between 4/8 (2+2), 5/8 (3+2), 3/8, and 8/8 (3+2+3). These are not random — they follow the rhythmic patterns of Bulgarian folk dances that Bartok collected. The scherzo's trio section is in 3+3+2 / 8, a standard Bulgarian *Daichovo* dance rhythm.

### Additive vs. Divisive Rhythm

Two fundamentally different ways to construct rhythmic patterns:

**Divisive rhythm (Western default).** Start with a fixed measure, divide it into equal beats, subdivide beats into equal parts. The structure is top-down: measure -> beats -> subdivisions.

**Additive rhythm (African, Balkan, Indian).** Build up from a smallest unit. Group smallest units into patterns of 2s and 3s. The structure is bottom-up: smallest pulse -> grouped patterns -> larger cycle.

**Why the distinction matters:** In divisive rhythm, a 7/8 bar is "unusual." In additive rhythm, 2+2+3 is just a grouping — no more unusual than 2+2+2+2. The cognitive and kinesthetic experience differs: a musician trained in additive rhythm does not perceive 7/8 as "odd meter" but as a natural combination of short and long beats.

## Part III — Syncopation

Syncopation places accents on metrically weak beats or divisions, contradicting the expected metric stress pattern.

### Types of Syncopation

1. **Accent displacement.** A dynamic or agogic accent on a weak beat. The downbeat exists but is overshadowed.

```
Expected:  >  .  .  .  | >  .  .  .
Syncopated: .  .  >  .  | .  .  >  .
```

2. **Tied syncopation.** A note on a weak beat ties across the barline or across a strong beat, eliminating the attack on the strong beat.

```
4/4:  . quarter | HALF (tied across beat 3) | . quarter
```

3. **Rest syncopation.** A rest on a strong beat forces the ear to hear the preceding weak-beat note as the rhythmic anchor.

4. **Off-beat syncopation.** Notes placed consistently on the "and" (second eighth note of each beat) rather than on the beat itself. This is the foundation of ska and reggae rhythm.

### The Backbeat

The most important syncopation in popular music: snare drum accents on beats 2 and 4 in 4/4 time, displacing the "natural" strong beats (1 and 3). The backbeat defines rock, pop, funk, R&B, and most global popular music since the 1950s. Its origin is in African-American musical traditions — gospel, blues, and jazz.

## Part IV — Hemiola

Hemiola is the superimposition of a 3:2 (or 2:3) rhythmic ratio — three beats in the time of two, or two beats in the time of three. It temporarily regroups the metric organization without changing the time signature.

**Hemiola in 3/4 time (Baroque and Classical):**

```
Normal 3/4:   | ONE two three | ONE two three |
Hemiola:      | ONE two THREE | four FIVE six |  (regroups 6 quarter notes as 3 groups of 2)
```

The ear hears a shift from triple to duple meter across two bars.

**Worked example — Brahms, Symphony No. 3, 3rd movement:**

The movement is in 3/8. Brahms writes hemiolas throughout, grouping two bars of 3/8 into one bar of 3/4. The continuous alternation between triple and duple grouping creates the movement's characteristic rhythmic ambiguity. At one passage, the melody groups in twos while the accompaniment continues in threes — a vertical hemiola that produces simultaneous 2-against-3.

**Cross-cultural hemiola.** The 3:2 ratio appears in West African drumming (cross-rhythm between 6/8 and 3/4 groupings), Cuban son (clave pattern implies both duple and triple groupings), and South Indian *misra chapu* tala.

## Part V — Polyrhythm and Polymetric Structures

### Polyrhythm

Two or more simultaneous rhythmic patterns with different numbers of pulses in the same time span. The patterns share a common duration (the cycle) but divide it differently.

**2-against-3 (the fundamental polyrhythm):**

```
Voice 1 (2):  X  .  .  X  .  .     (2 attacks in 6 pulses)
Voice 2 (3):  X  .  X  .  X  .     (3 attacks in 6 pulses)
Composite:    X  .  X  X  X  .     (resultant pattern)
```

**3-against-4:**

```
Voice 1 (3):  X  .  .  .  X  .  .  .  X  .  .  .   (12 pulses)
Voice 2 (4):  X  .  .  X  .  .  X  .  .  X  .  .   (12 pulses)
Composite:    X  .  .  X  X  .  X  .  .  X  .  .
```

**Practice method for 2:3.** Say "pass the bread" evenly while tapping the table on "pass" and "bread." Your voice divides the time into 3 syllables; your taps divide it into 2. The polarity between them is the polyrhythm.

### Polymeter (Polymetric Structures)

Simultaneous meters with different beat groupings that cycle independently. Unlike polyrhythm (which shares a common cycle), polymetric structures have independent cycles that realign only after a longer period.

**Worked example — 3/4 against 4/4:**

```
3/4:  | 1  2  3 | 1  2  3 | 1  2  3 | 1  2  3 |
4/4:  | 1  2  3  4 | 1  2  3  4 | 1  2  3  4 |
```

The two meters realign after 12 beats (LCM of 3 and 4). During those 12 beats, each meter's downbeat falls in a different place, creating systematic cross-accent.

## Part VI — Metric Modulation (Elliott Carter)

Metric modulation changes tempo by reinterpreting a rhythmic value in the old tempo as a different value in the new tempo. The composer Elliott Carter (1908-2012) pioneered this technique, creating music where tempo changes are precisely notated and structurally motivated rather than approximate.

**Mechanism:** A subdivision or grouping in the old tempo becomes the beat in the new tempo.

**Worked example.** Tempo 1: quarter = 120. Eighth-note triplets at this tempo have a rate of 360 per minute. If those triplets become the new quarter note, the new tempo is quarter = 360... but that is too fast. Instead, group two triplet eighths as the new quarter: new tempo = 180 (= 360/2).

**Notation shorthand:** The score might indicate "eighth-note triplet = new eighth note" with a precise metronome equivalence.

**Musical effect:** Metric modulation creates the sensation of continuous temporal transformation — the music accelerates or decelerates without the "gear-shift" feeling of a traditional tempo change. The old pulse dissolves into the new one through a shared subdivision.

## Part VII — Swing and Groove

### Swing Feel

Swing is a rhythmic feel in which nominally equal subdivisions are performed with unequal durations — the first eighth note of each pair is lengthened and the second is shortened. The ratio is not fixed:

| Swing ratio | Character | Style |
|---|---|---|
| 1:1 | Straight (no swing) | Classical, rock, pop |
| ~1.5:1 | Light swing | Bossa nova, cool jazz |
| ~2:1 | Medium swing | Standard jazz swing |
| 3:1 | Hard swing (triplet feel) | New Orleans, heavy shuffle |

The exact ratio depends on tempo, style, and individual interpretation. Faster tempos tend toward lighter swing; slower tempos permit harder swing.

### Groove Analysis

A **groove** is a repeating rhythmic pattern that establishes the feel of a piece. Groove analysis identifies:

1. **The rhythmic skeleton:** Which beats and subdivisions carry attacks?
2. **Micro-timing deviations:** How do attacks differ from strict metronomic placement?
3. **Dynamic contour:** Which notes are louder/softer within the pattern?
4. **Timbral variation:** Hi-hat open vs. closed, ghost notes on snare, etc.

**Worked example — James Brown, "Funky Drummer" (Clyde Stubblefield, 1970):**

The drum pattern is in 4/4, 16th-note subdivision. Key features:
- Kick drum on beat 1 and the "and" of beat 2 — creates forward momentum
- Snare on 2 and 4 (backbeat) with ghost notes on nearly every other 16th note
- Hi-hat in steady 16th notes with open hits on upbeats
- The ghost notes (extremely quiet snare taps between backbeats) create a continuous 16th-note texture. Removing the ghost notes destroys the groove — the feel depends on the quiet notes as much as the loud ones.

This pattern has been sampled over 1,000 times, making it the most-used drum break in recorded music history.

## Part VIII — African Rhythmic Concepts

### The Timeline Pattern (Bell Pattern)

West African ensemble music is organized around a **timeline** — a repeating asymmetric pattern played on an iron bell (gankogui, agogo) that serves as the temporal reference for all other parts. The timeline is not a "melody" — it is the structural spine of the polyrhythmic texture.

**The standard pattern (12/8 bell):**

```
x . x . x x . x . x . x     (7 attacks in 12 pulses)
1 . 2 . 3 4 . 5 . 6 . 7
```

This pattern (also called the "standard asymmetric timeline") generates multiple simultaneous metric interpretations: it can be heard in 12/8, 6/4, or 3/4 depending on which attacks the listener treats as downbeats. The ambiguity is intentional — it allows each drummer in the ensemble to lock onto a different metric layer.

### Clave

The Afro-Cuban **clave** is a two-bar rhythmic pattern that functions as the timeline in Cuban, Puerto Rican, and related musical traditions.

**Son clave (3-2):**

```
Bar 1:  x . . x . . x . . . . .    (3 attacks — the "3 side")
Bar 2:  . . x . . x . . . . . .    (2 attacks — the "2 side")
```

**Rumba clave (3-2):** Same as son clave but the third attack in bar 1 is shifted one pulse later, creating a more syncopated feel.

**The clave rule:** In Afro-Cuban music, every rhythm in the ensemble must be "in clave" — aligned with the clave pattern. Playing rhythms that contradict the clave is the most serious musical error possible in these traditions.

## Part IX — Indian Tala System

Indian classical music uses a system of rhythmic cycles called **tala** (or taal). A tala is a fixed cycle of beats, organized into sections called **vibhag**, with each beat called a **matra**.

**Key concepts:**

- **Sam:** The first beat of the cycle. The most important rhythmic point — melodic phrases resolve to sam the way Western phrases resolve to tonic.
- **Khali:** An "empty" or unstressed section of the cycle, indicated by a wave of the hand. Creates contrast with the stressed sections.
- **Theka:** The basic drum pattern that defines the tala. Played on the tabla (North Indian) or mridangam (South Indian).

**Common Hindustani (North Indian) talas:**

| Tala | Matras (beats) | Division | Character |
|---|---|---|---|
| Teental (Tintal) | 16 | 4+4+4+4 | Most common; versatile, balanced |
| Jhaptal | 10 | 2+3+2+3 | Asymmetric; used in lighter forms |
| Rupak | 7 | 3+2+2 | First beat is khali (unstressed!) — unusual |
| Ektal | 12 | 2+2+2+2+2+2 | Slow; used in khayal singing |

**Critical distinction from Western meter:** In Rupak tala (7 beats), the first beat (sam) falls on the khali (unstressed) section. This is unthinkable in Western music, where the downbeat is always the strongest beat. The Indian system separates the concept of "beginning of cycle" from "strongest beat" — a fundamentally different temporal architecture.

## Part X — Messiaen's Rhythmic Innovations

Olivier Messiaen (1908-1992) developed several rhythmic techniques that extended and transcended traditional Western meter.

### Non-Retrogradable Rhythms

A rhythm that reads the same forwards and backwards — the rhythmic equivalent of a palindrome.

**Example:**

```
Duration sequence:  3  2  1  2  3
(Read backwards:    3  2  1  2  3  — identical)
```

Messiaen used non-retrogradable rhythms to express theological ideas about eternity and the transcendence of linear time. The rhythm has no directionality — it exists outside the normal forward flow of time.

### Added Values

A small rhythmic value (typically a sixteenth note or dot) added to an otherwise regular rhythm, creating an asymmetric pattern from a symmetric base.

**Example:** A regular rhythm of three quarter notes (3 + 3 + 3 sixteenths) becomes 3 + 4 + 3 (adding one sixteenth to the middle note) or 4 + 3 + 3 (adding to the first). The added value disrupts metric regularity without creating a new meter — the music floats between meters.

### Rhythmic Modes (Deci-Talas)

Messiaen cataloged 120 rhythmic patterns from the Indian *Sangita Ratnakara* (13th-century treatise by Sarngadeva) and incorporated them into his compositions. These "deci-talas" served as rhythmic source material in the same way that modes serve as melodic source material.

**Application in *Quatuor pour la fin du temps* ("Quartet for the End of Time," 1941):**

In the first movement ("Liturgie de cristal"), the cello plays a repeating rhythmic pattern of 15 durations while the piano plays a repeating pattern of 17 durations. Since 15 and 17 are coprime, the two patterns do not realign until 15 x 17 = 255 iterations. The music creates a sense of eternal unfolding — the rhythmic cycle is so long that human perception cannot detect the repetition.

## When to Use This Skill

- Identifying and classifying meter (simple, compound, asymmetric)
- Analyzing syncopation patterns in any style
- Understanding polyrhythm and polymetric structures
- Studying groove and micro-timing in popular music and jazz
- Working with non-Western rhythmic systems (African, Indian, Balkan)
- Analyzing metric modulation in 20th-century concert music
- Writing rhythmic patterns for composition or arranging

## When NOT to Use This Skill

- For harmonic analysis — use **harmony-analysis** skill
- For contrapuntal writing and analysis — use **counterpoint** skill
- For large-scale formal analysis — use **form-analysis** skill
- For instrument ranges and timbral choices — use **orchestration** skill
- For aural skills development — use **ear-training** skill

## Cross-References

- **bartok agent:** Asymmetric meters, Bulgarian rhythms, folk-music-derived rhythmic patterns. Named for Bela Bartok, whose ethnomusicological fieldwork and compositional integration of irregular meters transformed the Western rhythmic vocabulary.
- **coltrane agent:** Jazz rhythm, swing feel, polyrhythmic improvisation. Named for John Coltrane, whose rhythmic innovations (sheets of sound, polyrhythmic superimpositions) expanded jazz rhythm beyond swing conventions.
- **messiaen agent:** Non-retrogradable rhythms, added values, deci-talas, color-rhythm synesthesia. Named for Olivier Messiaen, who drew equally from Indian rhythmic theory and Catholic theology to create a unique rhythmic language.
- **kodaly agent:** Rhythmic pedagogy, body percussion, rhythmic syllables for ear training.
- **harmony-analysis skill:** Harmonic rhythm (the rate of chord change) connects harmonic and rhythmic analysis.
- **form-analysis skill:** Formal boundaries often coincide with rhythmic/metric changes — meter shifts signal new sections.
- **ear-training skill:** Rhythmic dictation and metric identification exercises.

## References

- Lerdahl, F., & Jackendoff, R. (1983). *A Generative Theory of Tonal Music*. MIT Press.
- London, J. (2012). *Hearing in Time*. 2nd edition. Oxford University Press.
- Agawu, K. (2003). *Representing African Music*. Routledge.
- Clayton, M. (2000). *Time in Indian Music*. Oxford University Press.
- Bartok, B. (1931). *Hungarian Folk Music*. Oxford University Press.
- Carter, E. Collected works and interviews. (See Schiff, D., 1998, *The Music of Elliott Carter*. 2nd ed. Cornell University Press.)
- Messiaen, O. (1944). *Technique de mon langage musical*. Leduc.
- Pressing, J. (1983). "Cognitive Isomorphisms Between Pitch and Rhythm in World Musics." *Studies in Music*, 17, 38-61.
- Iyer, V. (2002). "Embodied Mind, Situated Cognition, and Expressive Microtiming in African-American Music." *Music Perception*, 19(3), 387-414.
