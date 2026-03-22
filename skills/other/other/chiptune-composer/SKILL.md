---
name: chiptune-composer
description: Compose full-length (~1.5 minute) chiptune songs in the audio tracker's compact JSON format. Supports RPG battle themes, town music, overworld adventures, classical arrangements, ambient dungeon tracks, and more. This skill should be used when creating songs for the audio tracker, composing game music, or generating .json song files.
argument-hint: <style> [key] [bpm] [description]
allow-model-invocation: true
---

# Chiptune Composer

Compose a full-length chiptune song using **$ARGUMENTS**.

Output a complete `.json` song file in the compact event format defined by `music/audio-tracker/AI-SONG-FORMAT.md`. The song should be ~1.5 minutes long (~90 seconds) with full structural development — not a short loop.

## Phase 0 — Parse Request & Plan

1. Parse the argument for style, key, BPM, and description hints.
2. Read `music/audio-tracker/AI-SONG-FORMAT.md` for the compact event format spec.
3. Read `music/audio-tracker/songs/index.json` to see existing songs and avoid duplicates.
4. Read one existing song JSON (e.g., `boss-battle.json` or `canon-in-d.json`) to calibrate output density and formatting.
5. Select the appropriate style profile from the **Style Profiles** section below.
6. Plan the song structure:
   - Key, mode, BPM, time feel
   - Song form (e.g., AABA, ABACBA, Intro-Verse-Chorus-Bridge-Chorus-Outro)
   - Number of unique patterns needed (typically 5-12 for a ~1.5 min track)
   - Instrument palette (4 channels: melody, harmony/countermelody, bass, percussion)
   - Harmonic plan: chord progression per section, modulation points
   - Melodic motif(s): the 3-6 note seed that unifies the track
7. Present the plan and discuss before composing.

## Phase 1 — Compose

Build the song JSON section by section. For each section:

1. **Establish the harmonic foundation** — write bass channel events first (chord roots, walking bass, ostinato, or pedal point depending on style).
2. **Add percussion** — lay down the rhythmic backbone appropriate to the style and tempo.
3. **Write the melody** — compose the lead channel using the motif, developing it through repetition, sequence, inversion, augmentation, or diminution.
4. **Add countermelody/harmony** — fill the second pitched channel with supporting material (arpeggiated chords, counter-lines, echo effects, or pad sustains).

### Composition Rules

- **Motif-first**: Define a 3-6 note melodic cell. Every section should derive from or relate to this motif.
- **Vary repeats**: Never copy a section identically more than twice in the sequence. Add ornaments, octave shifts, or rhythmic variations.
- **Voice independence**: Melody and harmony channels should have contrary or oblique motion most of the time. Avoid parallel octaves/fifths between channels.
- **Register separation**: Keep bass in MIDI 36-55, melody in 60-84, harmony flexible but avoid crossing the melody.
- **Phrase structure**: Use 4-bar or 8-bar phrases (16 or 32 rows at rpb=4). End phrases with clear cadences.
- **Dynamic arc**: Build intensity across the song. Use sparser textures for intros and bridges, denser for climaxes.
- **Pattern length contract**: Always set `patterns[].len` explicitly (usually 16 or 32) and treat it as fixed. Use cross-boundary `d` sustains to tie into the next pattern; do not rely on implicit pattern-length inference.

### Pattern Transition Techniques

Smooth transitions between patterns are critical — abrupt simultaneous channel switches create a jarring "seam" effect. Use these techniques to create musical flow across pattern boundaries:

- **Cross-boundary sustains**: End patterns with notes whose `d` extends past the pattern length. The engine handles this via timed note-off scheduling — a note at row 28 with `d: 8` in a 32-row pattern will sustain 4 rows into the next pattern. Use this on melody or pad channels to glue sections together.

- **Pickup notes / anacrusis**: Place 1-2 melody notes in the last 1-2 rows of the preceding pattern to lead into the downbeat of the next section. This is the most natural transition technique — the listener's ear follows the pickup into the new phrase. Example: in a 32-row pattern, add a note at row 30 or 31 that anticipates the melody of the next pattern.

- **Transition patterns**: Write short 8-16 row bridge patterns (drum fills, bass walk-ups, scalar runs, cymbal rolls) to insert between major sections. These don't need to be unique per transition — a single 8-row fill pattern can be reused at multiple section boundaries.

- **Staggered channel changes**: Use independent per-channel sequencing instead of switching all 4 channels simultaneously. For example, `[5, 3, 3, 3]` keeps bass/drums/harmony on the old pattern while melody switches, then `[5, 5, 5, 5]` on the next row completes the transition. Not every row needs this — reserve it for the biggest section changes (intro→verse, verse→chorus, bridge→final chorus).

- **Harmonic preparation**: In the last 2-4 rows of a pattern, prepare the harmony of the next section. Use dominant→tonic resolution, leading tone movement, or bass walk-ups to the new root. A bass channel walking up chromatically in the last 4 rows (e.g., E→F→F#→G to arrive at G) creates a smooth harmonic bridge.

- **Avoid hard cuts on all channels**: Don't place `n: -1` note-offs on the final row of every channel simultaneously. Instead, let some channels ring through (via cross-boundary `d`) while others cut, creating a staggered fade rather than an abrupt wall of silence.

- **Drum fills at section boundaries**: Replace the last 4-8 rows of a percussion pattern with a fill (rapid snare hits, tom rolls, accelerating hi-hats) to signal an upcoming section change. This is the most universally effective transition — listeners instinctively recognize drum fills as section markers.

### Pattern & Sequence Math

For a ~1.5 minute song (~90 seconds):
- At 120 BPM, rpb=4, 32-row patterns: each pattern = 4 bars = 8 seconds. Need ~11-12 sequence entries.
- At 80 BPM, rpb=4, 32-row patterns: each pattern = 4 bars = 12 seconds. Need ~7-8 sequence entries.
- At 160 BPM, rpb=4, 32-row patterns: each pattern = 4 bars = 6 seconds. Need ~15 sequence entries.

Reuse patterns via the sequence array — compose 8-20 unique patterns, arrange them into a full song via sequencing.

## Phase 1b — Relay Mode (for epic-length compositions)

For songs longer than 3 minutes, or when the user requests multiple parallel/sequential compositions, use the **Haiku Relay Pattern** instead of composing in a single agent. This was proven with a 130-pattern, 5.2-minute power metal epic.

### How It Works

1. **Opus plans the architecture**: Define instruments, section descriptions (10-30 sections), key/mode/energy per section, and the number of patterns each agent should compose (~13 patterns ≈ 30 seconds at most tempos).

2. **Write the master plan** to `music/audio-tracker/songs/_chunks-{song-name}/instruments.json` with the instrument array and section descriptions.

3. **Launch sequential Haiku agents**, each composing one section. Each agent receives:
   - The instrument definitions (constant)
   - Its section description (from the plan)
   - **The handoff payload** from the previous agent — the sustaining notes at the end of the last pattern

4. **Extract handoff notes** between agents using `music/audio-tracker/songs/_ttfaf-chunks/extract_handoff.py`:
   ```bash
   python3 extract_handoff.py chunk-NN.json
   ```
   This outputs the last sounding note per channel (note, instrument, volume, whether it sustains past the pattern boundary).

5. **Each agent's prompt must include**:
   - "These notes are ALREADY RINGING when your section begins: Ch0: X, Ch1: Y, Ch2: Z, Ch3: W"
   - "Let them ring 2-4 rows before your new notes take over"
   - The specific handoff notes to leave sustaining at the END of their last pattern (so the next agent can continue seamlessly)
   - "This is 100% original composition" (avoids copyright refusal for cover-inspired work)

6. **Merge all chunks** at the end:
   ```bash
   python3 merge.py  # in the chunks directory
   ```
   This remaps pattern IDs and stitches sequences into one song.

### Relay Prompt Template

```
You are composing Section N of M of an ORIGINAL [genre] chiptune epic called "[Title]." 100% original composition.

## INCOMING HANDOFF — Already ringing:
- Ch0: [note] (MIDI [num]), inst [idx] — sustaining
- Ch1: [note] (MIDI [num]), inst [idx] — sustaining
- Ch2: [note] (MIDI [num]), inst [idx] — sustaining
- Ch3: [description]

Let ring 2-4 rows before new notes.

## YOUR SECTION: "[Section Name]" — Section N of M
[Description of what this section should sound like]

**Key**: [key/mode]
**Energy**: [X/10]
**Patterns**: 13 (IDs 0-12), 32 rows, [BPM] BPM, rpb=4

## INSTRUMENTS
[List with indices]

## COMPOSE
[Detailed per-pattern guidance]

### HANDOFF (Pattern 12):
- Ch0: row 28, n:[note], inst [idx], d:8
- Ch1: row 28, n:[note], inst [idx], d:8
- Ch2: row 24, n:[note], inst [idx], d:12
- Ch3: [drum fill or crash description]

## OUTPUT: Write to `music/audio-tracker/songs/_chunks-{name}/chunk-NN.json`
```

### When to Use Relay Mode
- User requests a song longer than 3 minutes
- User asks for "epic", "through-composed", or "suite" style compositions
- User wants to compose in a specific genre that benefits from many distinct sections (power metal, progressive rock, symphony)
- User explicitly asks for parallel or sequential agent composition

## Phase 2 — Output

1. Write the complete JSON to `music/audio-tracker/songs/{kebab-case-title}.json`.
2. Update `music/audio-tracker/songs/index.json` to add the new song entry.
3. Verify the JSON is valid and all pattern IDs referenced in the sequence exist.
4. Run the boundary gap fixer to extend note durations at pattern transitions:
   ```bash
   python3 music/audio-tracker/tools/fix-boundary-gaps.py --fix music/audio-tracker/songs/{kebab-case-title}.json
   ```
   This detects silent gaps where a note's `d` ends before the pattern boundary and the next pattern doesn't start on row 0, then extends durations to sustain through.
5. Spot-check transition continuity:
   - Avoid all 4 channels going silent on the final 1-2 rows unless intentional.
   - Verify each major section boundary has at least one glue technique (cross-boundary sustain, pickup, fill, or staggered channel switch).

## Available Wave Types

The synth engine supports these wave types for instruments:
- `square` — 50% duty cycle pulse (NES Pulse 50%), warm and full
- `pulse25` — 25% duty cycle pulse (NES Pulse 25%), reedy and bright
- `pulse12` — 12.5% duty cycle pulse, thin and nasal
- `triangle` — triangle wave (NES-style bass), no volume envelope, thumpy
- `sawtooth` — sawtooth wave (SNES-style lead), rich harmonics
- `sine` — pure sine, good for pads and sub-bass
- `noise` — white noise for percussion
- `fm` — FM synthesis, use for guitars, harps, bells, and plucked strings

**Do NOT use `"wave": "pluck"`** — the Karplus-Strong pluck synthesis sounds bad. Always use `"wave": "fm"` instead for guitar, harp, and plucked-string instruments.

### Instrument Parameters

```json
{
  "name": "Display Name",
  "wave": "square|pulse25|pulse12|triangle|sawtooth|sine|noise|fm",
  "a": 0.01,          // attack time (seconds)
  "d": 0.1,           // decay time
  "s": 0.6,           // sustain level (0-1)
  "r": 0.1,           // release time
  "vol": 0.7,         // master volume (0-1)
  "detune": 0,         // cents detune (optional)
  "detuneOsc": false,  // enable 2nd detuned oscillator (optional)
  "detuneAmount": 7,   // detune amount for 2nd osc (optional)
  "filterType": "none|lowpass|highpass|bandpass",  // optional
  "filterFreq": 2000,  // filter cutoff Hz (optional)
  "filterQ": 1,        // filter resonance (optional)
  "fmRatio": 2,        // FM only: modulator/carrier freq ratio (1=warm, 2=bell, 3+=metallic)
  "fmDepth": 200,      // FM only: modulation depth in Hz (80=mellow, 200=bright, 500=harsh)
  "fmWave": "sine"     // FM only: modulator waveform
}
```

### FM Guitar/String Recipes

Use these proven FM presets for guitar and plucked-string instruments:

```jsonc
// Nylon Guitar — warm, mellow
{ "wave": "fm", "fmRatio": 1, "fmDepth": 120, "fmWave": "sine",
  "filterType": "lowpass", "filterFreq": 2200, "filterQ": 0.8,
  "a": 0.002, "d": 0.45, "s": 0.05, "r": 0.3, "vol": 0.7 }

// 12-String Guitar — chorus shimmer (detuned pair)
{ "wave": "fm", "fmRatio": 1, "fmDepth": 140, "fmWave": "sine",
  "detuneOsc": true, "detuneAmount": 7,
  "a": 0.002, "d": 0.4, "s": 0.05, "r": 0.25, "vol": 0.55 }

// Crystal Harp / Pizzicato — bright, bell-like
{ "wave": "fm", "fmRatio": 2, "fmDepth": 200, "fmWave": "sine",
  "a": 0.001, "d": 0.6, "s": 0.05, "r": 0.4, "vol": 0.6 }

// Pluck Bass — deep, warm
{ "wave": "fm", "fmRatio": 1, "fmDepth": 80, "fmWave": "sine",
  "filterType": "lowpass", "filterFreq": 1600, "filterQ": 0.8,
  "a": 0.003, "d": 0.3, "s": 0.1, "r": 0.18, "vol": 0.55 }
```
```

### Organ Stop Presets

For cathedral, church, gothic, or organ-style compositions, use these proven instrument recipes (originated from Gemini's Cyber-Cathedral Requiem):

```json
// Principal — bright, reedy pipe sound (melody/harmony)
{ "name": "Organ Principal", "wave": "pulse25", "a": 0.02, "d": 0.1, "s": 0.7, "r": 0.2, "vol": 0.6, "filterType": "lowpass", "filterFreq": 2500 }

// Pedal — deep 16' bass foundation
{ "name": "Organ Pedal", "wave": "triangle", "a": 0.05, "d": 0.2, "s": 0.9, "r": 0.3, "vol": 0.9 }

// Reeds — trumpet/oboe stop, detuned for width
{ "name": "Organ Reeds", "wave": "square", "a": 0.1, "d": 0.2, "s": 0.7, "r": 0.4, "vol": 0.5, "detuneOsc": true, "detuneAmount": 7 }

// Flute — soft, ethereal 4' flute stop
{ "name": "Organ Flute", "wave": "sine", "a": 0.4, "d": 0.5, "s": 0.6, "r": 0.8, "vol": 0.5, "detuneOsc": true, "detuneAmount": 4 }
```

Typical organ channel layout: Ch0 = Principal (melody), Ch1 = Reeds or Flute (harmony), Ch2 = Pedal (bass), Ch3 = percussion or a second Principal for counterpoint.

### Percussion Conventions

Noise instruments ignore pitch, but use these MIDI note conventions for readability:
- **48** = kick drum (lowpass filter, filterFreq ~150-200, short decay)
- **60** = snare (bandpass filter, filterFreq ~1000-1500, medium decay)
- **72** = hi-hat (highpass filter, filterFreq ~6000, very short decay)
- **64** = open hi-hat (highpass, longer decay)
- **56** = tom (can use triangle wave with short decay instead)

## Style Profiles

Read `references/style-profiles.md` for detailed harmonic, melodic, and structural conventions for each style:

- **RPG Battle** — fast, minor, chromatic, driving
- **RPG Boss** — intense, complex meter possible, chromaticism + syncopation
- **Overworld/Adventure** — Lydian/major, memorable melody, moderate-fast
- **Town/Village** — gentle, waltz or 4/4, pentatonic or jazz voicings
- **Dungeon/Cave** — sparse, dissonant, tritones, drones
- **Shop/Inn** — light, major, short loops, cozy
- **Victory Fanfare** — Mixolydian, brass-like, triumphant
- **Classical Arrangement** — adapt a known classical piece to 4 channels
- **Ambient/Atmospheric** — slow, evolving textures, pedal points
- **Synthwave/Neon** — driving 4-on-floor, detuned sawtooth, 120-130 BPM

## MIDI Note Reference

```
C2=36  D2=38  E2=40  F2=41  G2=43  A2=45  B2=47
C3=48  D3=50  E3=52  F3=53  G3=55  A3=57  B3=59
C4=60  D4=62  E4=64  F4=65  G4=67  A4=69  B4=71
C5=72  D5=74  E5=76  F5=77  G5=79  A5=81  B5=83
C6=84
```

Sharps/flats: add 1 for sharp, subtract 1 for flat (e.g., F#3=54, Bb4=70, Eb4=63).
