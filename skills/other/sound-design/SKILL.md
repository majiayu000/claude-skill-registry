---
name: sound-design
description: "Create and manipulate sounds through synthesis, sampling, and audio processing for music, film, games, and multimedia. Use for designing custom sounds, synthesizing new timbres, creating sound effects, building audio textures, implementing synthesis techniques (subtractive, FM, wavetable, granular), processing samples, and developing unique sonic identities for creative projects."
---

# Sound Design

Create original sounds and sonic textures through synthesis, sampling, and creative audio manipulation.

## Overview

Sound design is the art and science of creating, shaping, and manipulating audio to produce specific sonic results. This skill covers synthesis fundamentals, sound manipulation techniques, effects processing, sampling workflows, and practical applications across music production, film, games, and multimedia projects.

## Fundamental Sound Properties

### Core Elements

**Pitch:**
- Perceived frequency of sound wave (measured in Hz)
- Musical notes correspond to specific frequencies
- A440 = 440 Hz (standard tuning reference)
- Doubling frequency = one octave higher

**Amplitude:**
- Strength or volume of sound wave
- Measured in decibels (dB)
- Determines dynamics and loudness
- Affects perceived energy and impact

**Timbre:**
- Unique tonal character or "color" of sound
- Distinguishes instruments playing same pitch
- Determined by harmonic content and overtones
- Shaped by waveform, filtering, and modulation

### Frequency Spectrum

All sound exists on frequency spectrum, influencing tone and character:

| Frequency Range | Characteristics | Musical Elements |
|----------------|-----------------|------------------|
| Sub-bass (20-60 Hz) | Felt more than heard, physical impact | Kick drum fundamental, sub-bass synths |
| Bass (60-250 Hz) | Warmth, power, foundation | Bass guitar, bass synths, low toms |
| Low-mids (250-500 Hz) | Body, fullness | Guitar body, snare body, vocal warmth |
| Mids (500 Hz-2 kHz) | Presence, clarity | Vocals, guitars, most instruments |
| Upper-mids (2-4 kHz) | Definition, attack | Vocal consonants, snare crack, clarity |
| Presence (4-6 kHz) | Brightness, edge | Cymbals, vocal sibilance, clarity |
| Brilliance (6-20 kHz) | Air, sparkle, shimmer | Cymbals, hi-hats, acoustic detail |

## Synthesis Techniques

### Subtractive Synthesis

**Concept:**
Start with harmonically rich waveform, then remove frequencies using filters and envelope shapers.

**Workflow:**
1. Select oscillator waveform (saw, square, triangle)
2. Apply filter to remove unwanted frequencies
3. Shape amplitude and filter with envelopes
4. Add modulation (LFOs, additional envelopes)
5. Apply effects

**Best For:**
- Classic analog-style sounds
- Basses, leads, pads
- Warm, organic timbres
- Beginner-friendly synthesis

---

### Additive Synthesis

**Concept:**
Build complex sounds by layering individual sine waves (harmonics).

**Workflow:**
1. Start with fundamental frequency (sine wave)
2. Add harmonics at integer multiples
3. Adjust amplitude of each harmonic
4. Modulate harmonics over time
5. Create evolving, complex timbres

**Best For:**
- Precise harmonic control
- Organ and bell-like sounds
- Evolving textures
- Spectral sound design

**Challenges:**
- Complex to program manually
- Requires many oscillators
- CPU-intensive

---

### FM (Frequency Modulation) Synthesis

**Concept:**
Modulate frequency of one oscillator (carrier) with another oscillator (modulator) to create complex, inharmonic timbres.

**Key Parameters:**
- **Carrier:** Oscillator producing audible sound
- **Modulator:** Oscillator modulating carrier frequency
- **Modulation Index:** Amount of modulation applied
- **Ratio:** Frequency relationship between carrier and modulator

**Workflow:**
1. Set carrier frequency (fundamental pitch)
2. Set modulator frequency (often ratio of carrier)
3. Adjust modulation index for complexity
4. Add additional operators for richer sounds
5. Shape with envelopes

**Best For:**
- Metallic, bell-like tones
- Electric pianos and keyboards
- Aggressive, digital sounds
- Complex, evolving timbres

**Popular Tools:**
- Native Instruments FM8
- Ableton Operator
- Arturia DX7 V

---

### Wavetable Synthesis

**Concept:**
Use pre-recorded or pre-defined wavetables (collections of waveforms) that can be morphed and modulated.

**Workflow:**
1. Select wavetable
2. Modulate wavetable position (morph between waveforms)
3. Apply filters and effects
4. Modulate with LFOs and envelopes
5. Layer multiple wavetable oscillators

**Best For:**
- Modern electronic music
- Evolving pads and textures
- Aggressive leads and basses
- Complex, digital sounds

**Popular Tools:**
- Xfer Serum (industry standard)
- Native Instruments Massive X
- Arturia Pigments

---

### Granular Synthesis

**Concept:**
Break sound into tiny segments (grains) and rearrange, layer, or process them to create new textures.

**Key Parameters:**
- **Grain Size:** Duration of each grain (1-100ms)
- **Grain Density:** Number of grains per second
- **Grain Position:** Playback position in source audio
- **Pitch/Time:** Independent control of pitch and playback speed

**Best For:**
- Atmospheric textures and soundscapes
- Time-stretching without artifacts
- Experimental and ambient music
- Transforming existing audio

**Popular Tools:**
- Granulator II (Ableton)
- Output Portal
- Steinberg Padshop

---

### Physical Modeling Synthesis

**Concept:**
Simulate physical properties of acoustic instruments or sound-producing objects using mathematical models.

**Applications:**
- Realistic instrument emulation
- String, wind, and percussion modeling
- Unique, expressive sounds
- Responsive to playing dynamics

**Popular Tools:**
- Applied Acoustics Chromaphone
- Modartt Pianoteq
- Native Instruments Reaktor

---

## Synthesis Building Blocks

### Waveforms (Oscillators)

Basic building blocks of synthesis:

**Sine Wave:**
- Purest waveform, single frequency
- No harmonics, only fundamental
- Smooth, mellow sound
- Foundation of additive synthesis

**Triangle Wave:**
- Contains odd harmonics
- Softer than square wave
- Mellow, flute-like character

**Square Wave:**
- Rich in odd harmonics
- Hollow, woody character
- Classic for bass and lead sounds
- Pulse Width Modulation (PWM) adds movement

**Sawtooth Wave:**
- Contains all harmonics (even and odd)
- Bright, buzzy character
- Most harmonically rich basic waveform
- Versatile for basses, leads, pads

**Noise:**
- Random waveform, all frequencies
- White noise: Equal energy across spectrum
- Pink noise: Equal energy per octave
- Used for percussion, wind, atmospheres

---

### Envelopes (ADSR)

Control how parameters change over time:

**Attack:**
- Time to reach peak level after trigger
- Fast attack: Percussive, immediate
- Slow attack: Gradual fade-in, pad-like

**Decay:**
- Time to fall from peak to sustain level
- Shapes initial character of sound

**Sustain:**
- Level held while note is pressed
- Not a time parameter (it's a level)
- Determines body of sound

**Release:**
- Time to fade to silence after note release
- Short release: Staccato, tight
- Long release: Lingering, ambient

**Applications:**
- Amplitude envelope: Volume over time
- Filter envelope: Brightness over time
- Pitch envelope: Pitch changes over time

---

### Filters

Shape timbre by removing or emphasizing frequencies:

**Low-Pass Filter (LPF):**
- Allows low frequencies, removes highs
- Most common filter type
- Creates warmth, removes brightness
- Cutoff frequency determines transition point

**High-Pass Filter (HPF):**
- Allows high frequencies, removes lows
- Thins sound, removes rumble
- Creates airy, thin textures

**Band-Pass Filter (BPF):**
- Allows specific frequency range
- Removes frequencies above and below
- Creates focused, telephone-like sounds

**Notch Filter:**
- Removes specific frequency range
- Opposite of band-pass
- Surgical frequency removal

**Resonance (Q):**
- Emphasizes frequencies at cutoff point
- Adds character and edge
- High resonance creates self-oscillation

---

### Low-Frequency Oscillators (LFOs)

Modulate parameters rhythmically or randomly:

**Common LFO Targets:**
- Pitch: Vibrato effect
- Amplitude: Tremolo effect
- Filter cutoff: Rhythmic brightness changes
- Pan: Auto-panning, stereo movement

**LFO Waveforms:**
- Sine: Smooth, musical modulation
- Triangle: Linear up/down movement
- Square: On/off switching
- Sawtooth: Ramp up or down
- Random: Unpredictable, organic movement

**Sync Options:**
- Free-running: Independent of tempo
- Tempo-synced: Locked to DAW tempo (1/4 note, 1/8 note, etc.)

---

### Modulation

Use one parameter to control another for dynamic, evolving sounds:

**Modulation Sources:**
- LFOs
- Envelopes
- Velocity (how hard key is pressed)
- Aftertouch (pressure after key press)
- Mod wheel
- Random generators

**Modulation Destinations:**
- Pitch (vibrato, pitch drift)
- Filter cutoff (wah, brightness changes)
- Amplitude (tremolo, volume swells)
- Pan (stereo movement)
- Effect parameters (delay time, reverb size)

---

## Sound Design Workflow

### Starting from Scratch

1. **Define Goal:**
   - What type of sound? (Bass, lead, pad, FX)
   - What character? (Warm, aggressive, ethereal, percussive)
   - What context? (Genre, mix position, emotional tone)

2. **Select Synthesis Method:**
   - Subtractive: Warm, analog-style sounds
   - FM: Metallic, digital, complex
   - Wavetable: Modern, evolving, aggressive
   - Granular: Atmospheric, experimental

3. **Choose Waveform(s):**
   - Saw: Bright, full, versatile
   - Square: Hollow, retro
   - Sine: Pure, sub-bass
   - Noise: Texture, percussion

4. **Shape with Filters:**
   - Low-pass for warmth
   - High-pass to remove mud
   - Resonance for character

5. **Apply Envelopes:**
   - Amplitude envelope for volume shape
   - Filter envelope for brightness evolution
   - Pitch envelope for transient character

6. **Add Modulation:**
   - LFOs for movement and rhythm
   - Velocity for dynamic response
   - Mod wheel for performance control

7. **Layer and Process:**
   - Layer multiple oscillators for richness
   - Detune for width and thickness
   - Add effects (reverb, delay, distortion)

8. **Refine and Iterate:**
   - A/B compare with reference sounds
   - Adjust in context of mix
   - Save variations and presets

---

### Reverse Engineering Presets

**Learning Technique:**
1. Load preset sound
2. Disable all effects
3. Reset modulation and LFOs
4. Identify core waveforms and oscillators
5. Analyze filter settings
6. Examine envelope shapes
7. Re-enable modulation one parameter at a time
8. Attempt to recreate from scratch

**Benefits:**
- Understand sound construction
- Learn synthesis techniques
- Develop sonic vocabulary
- Build confidence in sound design

---

## Effects and Processing

### Essential Effects

**Distortion/Saturation:**
- Adds harmonics and warmth
- Increases perceived loudness
- Creates aggression and edge
- Types: Overdrive, fuzz, bitcrusher, waveshaping

**Compression:**
- Controls dynamic range
- Adds sustain and body
- Glues layers together
- Sidechain for rhythmic pumping

**Reverb:**
- Creates sense of space
- Adds depth and dimension
- Types: Room, hall, plate, spring, convolution

**Delay:**
- Rhythmic repetitions
- Creates width and depth
- Types: Digital, analog, tape, ping-pong

**Chorus/Flanger/Phaser:**
- Adds movement and width
- Thickens and enriches sound
- Creates swirling, modulated textures

**Stereo Imaging:**
- Widens or narrows stereo field
- Separates elements in mix
- Creates space and dimension

---

## Layering Techniques

### Frequency Splitting

**Concept:**
Layer sounds occupying different frequency ranges.

**Example (Bass Sound):**
- Layer 1: Sub-bass (sine wave, 40-80 Hz)
- Layer 2: Mid-bass (saw wave, 80-300 Hz)
- Layer 3: High-end (noise or distorted layer, 2-8 kHz)

---

**Note:** This file was automatically condensed to meet the 500-line requirement. Additional content has been moved to the references/ folder.
