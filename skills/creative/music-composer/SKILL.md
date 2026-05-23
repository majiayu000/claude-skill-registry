---
name: music-composer
description: Expert in music composition across all genres, MIDI programming, audio synthesis, music theory, and arrangement. Use when composing music, creating MIDI files, generating melodies/harmonies/rhythms, arranging tracks, or working with musical concepts like scales, chords, progressions, and orchestration.
---

# Music Composer

Comprehensive music composition assistant with expertise in theory, MIDI programming, synthesis, and all musical genres from classical to electronic.

## Core Capabilities

### 1. Music Composition & Arrangement
- Generate melodies, harmonies, bass lines, and rhythmic patterns
- Create full arrangements with multiple instruments
- Orchestrate for various ensembles (orchestra, band, electronic, etc.)
- Develop chord progressions and harmonic structures
- Write counterpoint and polyphonic textures

### 2. MIDI Programming
- Create MIDI files programmatically using Python (mido library)
- Generate drum patterns, arpeggios, and sequences
- Implement realistic velocity curves and humanization
- Use scripts in `scripts/` for common MIDI tasks
- Export production-ready MIDI files

### 3. Genre Expertise
All genres supported - consult `references/genres.md` for specific characteristics:
- Classical (Baroque, Romantic, Contemporary)
- Jazz (Bebop, Modal, Fusion, Smooth)
- Electronic (Techno, House, Ambient, IDM, Dubstep)
- Rock & Metal (Progressive, Blues, Punk)
- Pop & R&B (Contemporary, Soul)
- World Music (Latin, African, Asian traditions)
- Film/Game Scoring

### 4. Music Theory & Analysis
Comprehensive theory support - see `references/theory.md`:
- Scales (Major, Minor, Modal, Exotic)
- Chord construction and voicings
- Harmonic progressions and functions
- Form and structure analysis
- Rhythmic concepts and time signatures

### 5. Audio Synthesis Guidance
Provide synthesis programming advice for:
- Subtractive synthesis (oscillators, filters, envelopes)
- FM synthesis (operators, algorithms)
- Wavetable and granular synthesis
- Effects chains and processing

## Quick Start Workflows

### Compose a Melody
```python
# Use the melody generator script
python scripts/generate_melody.py --key C --scale major --length 16 --output melody.mid
```

### Create a Chord Progression
```python
# Generate progression with voice leading
python scripts/generate_chords.py --progression "I-IV-V-I" --key G --output chords.mid
```

### Build a Drum Pattern
```python
# Create rhythmic pattern
python scripts/generate_drums.py --style "rock" --tempo 120 --bars 4 --output drums.mid
```

### Full Arrangement
Combine elements into complete composition:
1. Define structure (intro, verse, chorus, etc.)
2. Create chord progression for each section
3. Generate melody over chords
4. Add bass line following harmony
5. Program drums and percussion
6. Add additional instruments/textures
7. Export multi-track MIDI

## Working with Musical Requests

### "Compose a jazz ballad in Bb"
1. Choose jazz ballad chord progression (consult `references/progressions.md`)
2. Set tempo (60-80 BPM typically)
3. Create walking bass line
4. Add jazz piano voicings
5. Compose melody with jazz phrasing
6. Add subtle drums (brush pattern)
7. Export MIDI with proper track names

### "Create a techno track with a driving bassline"
1. Set tempo (125-135 BPM)
2. Create 4-on-the-floor kick pattern
3. Generate repetitive bassline (often single note or octaves)
4. Add hi-hats and percussion
5. Create synth leads/stabs
6. Layer atmospheric pads
7. Structure: Intro → Build → Drop → Break → Drop → Outro

### "Write a string quartet movement"
1. Choose form (Sonata, Rondo, Theme & Variations)
2. Compose main themes
3. Distribute among instruments (Violin I, Violin II, Viola, Cello)
4. Develop counterpoint and voice leading
5. Consider range and playability
6. Export with separate tracks for each instrument

## MIDI Technical Details

### General MIDI (GM) Program Numbers
Consult `references/gm_instruments.md` for complete list:
- 0: Acoustic Grand Piano
- 24: Acoustic Guitar (nylon)
- 32: Acoustic Bass
- 40: Violin
- 128+: Drum kits (channel 10)

### MIDI Note Numbers
Middle C = 60 (C4)
Range: 0-127 (C-1 to G9)

### Velocity Guidelines
- ppp: 8-20
- pp: 21-35
- p: 36-50
- mp: 51-65
- mf: 66-80
- f: 81-95
- ff: 96-110
- fff: 111-127

### Humanization Techniques
- Slight velocity variation (±5-10)
- Micro-timing adjustments (±10-30 ticks)
- Avoid perfectly quantized notes
- Vary note lengths slightly

## Music Theory Quick Reference

### Common Chord Progressions
- Pop: I-V-vi-IV (C-G-Am-F)
- Blues: I-I-I-I-IV-IV-I-I-V-IV-I-I
- Jazz: ii-V-I (Dm7-G7-Cmaj7)
- Rock: I-bVII-IV (C-Bb-F)

See `references/progressions.md` for comprehensive list.

### Scale Formulas
- Major: W-W-H-W-W-W-H
- Natural Minor: W-H-W-W-H-W-W
- Harmonic Minor: W-H-W-W-H-W+H-H
- Pentatonic Major: W-W-m3-W-m3

See `references/scales.md` for all modes and exotic scales.

## Best Practices

### Composition
- Start with a clear concept or emotion
- Consider the target context (film, game, standalone)
- Use repetition with variation
- Balance complexity and accessibility
- Think in terms of call-and-response

### MIDI Production
- Use appropriate velocity ranges for realism
- Pan instruments for spatial clarity
- Layer sounds for richness
- Leave headroom for mixing
- Include tempo and time signature changes when needed

### Arrangement
- Don't overcrowd the frequency spectrum
- Create contrast between sections
- Use dynamics effectively
- Consider the listener's attention span
- Build and release tension

## Resources Overview

### Scripts (`scripts/`)
- `generate_melody.py` - Melodic line generator
- `generate_chords.py` - Chord progression creator
- `generate_drums.py` - Rhythm pattern generator
- `midi_utils.py` - Shared MIDI utilities

### References (`references/`)
- `theory.md` - Complete music theory reference
- `genres.md` - Genre characteristics and conventions
- `scales.md` - All scale types and formulas
- `progressions.md` - Common chord progressions by genre
- `gm_instruments.md` - General MIDI instrument list
- `orchestration.md` - Instrument ranges and combinations

### Assets (`assets/`)
- `templates/` - MIDI templates for common setups
- `drum_patterns/` - Pre-made drum MIDI files

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
