---
name: audio-engineering
description: Audio engineering — mastering, mixing, EQ, compression, loudness standards, synthesis, podcast production, music theory, spectrum analysis.
activationKeywords:
  - audio
  - mastering
  - mixing
  - EQ
  - equalization
  - compressor
  - compression
  - limiter
  - loudness
  - LUFS
  - true peak
  - EBU
  - podcast
  - waveform
  - spectrum
  - synthesis
  - synthesizer
  - FM synthesis
  - subtractive
  - granular
  - modular
  - BPM
  - tempo
  - key detection
  - music theory
  - chord
  - scale
  - sox
  - ableton
  - DAW
  - reverb
  - delay
  - noise reduction
  - normalization
  - dithering
  - sample rate
  - bit depth
type: skill
category: media
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/media/audio-engineering/SKILL.md
superseded_by: null
---
# Audio Engineering Skill

*Built on research from 30 Music cluster projects, 360 PNW musicians deep-dived (S36/SPS), Ableton Live research (ABL), Deep Audio (DAA), Dead Frequencies (DFQ), and High Fidelity amplifier analysis (HFR/HFE).*

Expert-level audio engineering covering mastering, mixing, loudness standards, synthesis, podcast production, music theory, and spectrum analysis. Works alongside the `ffmpeg-media` skill for codec/format operations.

## Loudness Standards

### Target Levels by Platform

| Platform | Target LUFS | True Peak | Standard |
|----------|------------|-----------|----------|
| Spotify | -14 LUFS | -1 dBTP | AES streaming |
| Apple Music | -16 LUFS | -1 dBTP | Sound Check |
| YouTube | -14 LUFS | -1 dBTP | ITU-R BS.1770 |
| Podcast (Apple) | -16 LUFS | -1 dBTP | Apple spec |
| Podcast (Spotify) | -14 LUFS | -1 dBTP | Spotify spec |
| Broadcast TV | -24 LUFS | -2 dBTP | EBU R128 |
| Broadcast US | -24 LKFS | -2 dBTP | ATSC A/85 |
| CD master | -9 to -12 LUFS | -0.3 dBTP | Red Book |
| Film/Cinema | -24 LUFS | -1 dBTP | SMPTE RP 200 |

### Measurement Commands
```bash
# Measure integrated loudness (LUFS) with ffmpeg
ffmpeg -i input.wav -af loudnorm=print_format=json -f null - 2>&1 | grep -A20 "Parsed_loudnorm"

# Full EBU R128 scan
ffmpeg -i input.wav -af ebur128=peak=true -f null - 2>&1 | tail -20

# Loudness normalization to -14 LUFS (two-pass for accuracy)
# Pass 1: measure
ffmpeg -i input.wav -af loudnorm=I=-14:LRA=11:TP=-1:print_format=json -f null - 2>&1 > /tmp/loudnorm.json
# Pass 2: apply (use measured values from pass 1)
ffmpeg -i input.wav -af loudnorm=I=-14:LRA=11:TP=-1:measured_I=-18.5:measured_LRA=9.2:measured_TP=-0.5:measured_thresh=-28.3 output.wav
```

### With sox
```bash
# Normalize peak to -1 dBFS
sox input.wav output.wav gain -n -1

# Compressor (threshold -20dB, ratio 4:1, attack 5ms, release 50ms)
sox input.wav output.wav compand 0.005,0.05 -20,-20,-10,-10,0,-6

# 3-band EQ (low shelf +3dB at 200Hz, mid cut -2dB at 2kHz, high shelf +1dB at 8kHz)
sox input.wav output.wav bass +3 200 equalizer 2000 1q -2 treble +1 8000

# Noise reduction (profile then reduce)
sox noisy.wav -n noiseprof /tmp/noise.prof
sox noisy.wav clean.wav noisered /tmp/noise.prof 0.21

# Generate tone (440Hz sine, 3 seconds)
sox -n -r 44100 -c 1 tone.wav synth 3 sine 440

# Spectrum analysis (generate spectrogram PNG)
sox input.wav -n spectrogram -o spectrum.png
```

## Mastering Chain

### Standard Mastering Signal Flow
```
Input → EQ (corrective) → Compression → EQ (tonal) → Stereo Width → Limiting → Dithering → Output
```

### With ffmpeg Filters
```bash
# Full mastering chain: EQ → compression → limiting → loudness normalization
ffmpeg -i mix.wav -af "\
  equalizer=f=80:t=h:w=100:g=2,\
  equalizer=f=3000:t=h:w=1000:g=-1.5,\
  equalizer=f=12000:t=h:w=2000:g=1,\
  acompressor=threshold=-18dB:ratio=3:attack=10:release=100:knee=6,\
  alimiter=limit=-1dBFS:level=false,\
  loudnorm=I=-14:LRA=11:TP=-1\
" -ar 44100 -sample_fmt s16 mastered.wav

# Dithering (16-bit with triangular dither for CD)
ffmpeg -i master_24bit.wav -af "dither=method=triangular" -sample_fmt s16 -ar 44100 cd_master.wav
```

## EQ Reference

### Frequency Bands and Characteristics

| Band | Range | Character | Common Uses |
|------|-------|-----------|-------------|
| Sub-bass | 20-60 Hz | Felt, not heard | Kick fundamental, sub bass |
| Bass | 60-250 Hz | Warmth, body | Bass guitar, kick punch, vocal warmth |
| Low-mid | 250-500 Hz | Muddiness zone | Cut here to clean up mixes |
| Mid | 500-2000 Hz | Body, presence | Vocal clarity, guitar body |
| Upper-mid | 2-4 kHz | Presence, bite | Vocal intelligibility, guitar attack |
| Presence | 4-6 kHz | Definition, edge | Consonant clarity, string attack |
| Brilliance | 6-12 kHz | Air, shimmer | Cymbals, vocal air, acoustic sparkle |
| Ultra-high | 12-20 kHz | Air, sparkle | Subtle sheen (careful: sibilance) |

### Common Problem Frequencies
- **200-300 Hz** — boominess in vocals, acoustic guitar
- **400-600 Hz** — cardboard/boxy sound
- **1-2 kHz** — nasal, telephone quality
- **3-5 kHz** — harshness, listening fatigue
- **6-8 kHz** — sibilance (de-ess here)

## Compression Reference

### Settings by Source

| Source | Threshold | Ratio | Attack | Release | Knee |
|--------|-----------|-------|--------|---------|------|
| Vocals | -18 to -12 dB | 2:1 to 4:1 | 5-15 ms | 40-80 ms | Soft |
| Drums (bus) | -15 to -10 dB | 3:1 to 6:1 | 10-30 ms | 50-100 ms | Hard |
| Bass | -15 to -8 dB | 3:1 to 8:1 | 10-30 ms | 100-200 ms | Hard |
| Acoustic guitar | -20 to -12 dB | 2:1 to 4:1 | 10-25 ms | 100-150 ms | Soft |
| Mix bus | -20 to -15 dB | 1.5:1 to 2:1 | 10-30 ms | 100-300 ms | Soft |
| Podcast | -20 to -15 dB | 3:1 to 5:1 | 5-10 ms | 50-100 ms | Soft |

### Compression Types
- **VCA** — fast, transparent, precise (SSL, dbx 160)
- **Optical** — smooth, musical, slow (LA-2A, CL 1B)
- **FET** — aggressive, colorful, fast (1176, Distressor)
- **Variable-mu** — warm, glue, gentle (Fairchild 670, Manley Vari-Mu)

## Synthesis Reference

### Synthesis Types

| Type | How It Works | Character | Classic Synths |
|------|-------------|-----------|----------------|
| Subtractive | Oscillator → Filter → Amplifier | Warm, analog, rich | Minimoog, Prophet-5, Juno-106 |
| FM | Operators modulating each other's frequency | Metallic, bell-like, bright | DX7, FM8 |
| Wavetable | Morphing between stored waveforms | Evolving, complex, modern | PPG Wave, Serum, Vital |
| Granular | Tiny audio grains layered and scattered | Atmospheric, textural, ambient | Granulator, Pigments |
| Additive | Sum of individual sine wave partials | Precise, organ-like | Kawai K5, Razor |
| Physical modeling | Mathematical model of physical instrument | Realistic, expressive | Chromaphone, Pianoteq |
| Sample-based | Recorded audio, pitch-shifted and layered | Realistic, natural | Kontakt, Sampler |

### ADSR Envelope Quick Reference
- **Pad**: A=500ms, D=200ms, S=0.8, R=1000ms
- **Pluck**: A=1ms, D=200ms, S=0, R=100ms
- **Bass**: A=5ms, D=100ms, S=0.6, R=50ms
- **Lead**: A=10ms, D=50ms, S=0.7, R=200ms
- **Kick drum**: A=0ms, D=150ms, S=0, R=50ms

## Music Theory Quick Reference

### Circle of Fifths (Major Keys)
```
        C
    F       G
  Bb          D
    Eb      A
       Ab/E
```

### Common Chord Progressions
| Name | Numerals | Example in C | Use |
|------|----------|-------------|-----|
| Pop | I-V-vi-IV | C-G-Am-F | 80% of pop music |
| Blues | I-IV-V | C-F-G | Blues, rock |
| Jazz ii-V-I | ii-V-I | Dm7-G7-Cmaj7 | Jazz standard |
| Andalusian | i-VII-VI-V | Am-G-F-E | Flamenco, dramatic |
| Canon | I-V-vi-iii-IV-I-IV-V | C-G-Am-Em-F-C-F-G | Pachelbel, ballads |
| Minor blues | i-iv-V | Am-Dm-E | Minor blues |

### Scales
- **Major (Ionian)**: W-W-H-W-W-W-H
- **Natural Minor (Aeolian)**: W-H-W-W-H-W-W
- **Pentatonic Major**: 1-2-3-5-6
- **Pentatonic Minor**: 1-b3-4-5-b7
- **Blues**: 1-b3-4-#4-5-b7
- **Dorian**: W-H-W-W-W-H-W (minor with raised 6th — jazz, funk)
- **Mixolydian**: W-W-H-W-W-H-W (major with flat 7th — blues rock)

## Podcast Production Workflow

### Recording
```bash
# Record from default mic (sox)
sox -d -r 44100 -c 1 -b 16 recording.wav

# Record with ffmpeg (specify ALSA device on Linux)
ffmpeg -f alsa -i default -ar 44100 -ac 1 recording.wav
```

### Processing Chain
```bash
# 1. Noise reduction
sox recording.wav -n trim 0 0.5 noiseprof /tmp/noise.prof
sox recording.wav clean.wav noisered /tmp/noise.prof 0.21

# 2. Normalize + compress + EQ for voice
ffmpeg -i clean.wav -af "\
  highpass=f=80,\
  lowpass=f=12000,\
  equalizer=f=3000:t=h:w=1000:g=2,\
  acompressor=threshold=-20dB:ratio=4:attack=5:release=50,\
  loudnorm=I=-16:TP=-1\
" -ar 44100 podcast_ready.wav

# 3. Export MP3 for distribution
ffmpeg -i podcast_ready.wav -c:a libmp3lame -b:a 128k \
  -metadata title="Episode Title" \
  -metadata artist="Show Name" \
  -metadata album="Podcast Name" \
  -metadata genre="Podcast" \
  episode.mp3

# 4. Generate waveform for show notes
ffmpeg -i episode.mp3 -filter_complex "showwavespic=s=1920x200:colors=0x1a1a2e" -frames:v 1 waveform.png
```

### ID3 Tags
```bash
# Set all metadata
ffmpeg -i episode.mp3 -c copy \
  -metadata title="EP 42: The Memory Architecture" \
  -metadata artist="GSD Podcast" \
  -metadata album="Getting Shit Done" \
  -metadata track="42" \
  -metadata date="2026" \
  -metadata comment="LOD-tiered memory system deep dive" \
  tagged.mp3
```

## BPM and Key Detection

### With ffmpeg/aubio
```bash
# Install aubio for beat/pitch detection
# apt install aubio-tools

# BPM detection
aubiotempo input.wav

# Pitch/key detection
aubiopitch -i input.wav -p yinfft

# Onset detection (transient markers)
aubioonset input.wav
```

### With sox
```bash
# Generate stats (includes RMS, peak, DC offset)
sox input.wav -n stats 2>&1
```

## Sample Rate / Bit Depth Reference

| Format | Sample Rate | Bit Depth | Use |
|--------|-------------|-----------|-----|
| CD | 44.1 kHz | 16-bit | Consumer playback |
| DVD | 48 kHz | 24-bit | Video soundtrack |
| Hi-Res | 96 kHz | 24-bit | Audiophile streaming |
| Studio | 96-192 kHz | 32-bit float | Recording/mixing |
| Podcast | 44.1 kHz | 16-bit | Voice distribution |
| Phone/VoIP | 8-16 kHz | 16-bit | Voice calls |

### Conversion
```bash
# Downsample from 96kHz/24-bit to 44.1kHz/16-bit with dither
sox input_96_24.wav -r 44100 -b 16 output_441_16.wav dither -s

# Same with ffmpeg
ffmpeg -i input_96_24.wav -ar 44100 -sample_fmt s16 -af "dither=method=triangular" output.wav
```

## Related Skills & Agents

- **ffmpeg-media** — codec/format operations, video+audio conversion
- **ffmpeg-processor** agent — media processing specialist
- **gource-visualizer** — repository visualization with audio sync capability
- Audio research: ABL, DAA, DFQ, HFR, HFE, S36/SPS (360 musicians)

## When This Skill Activates

- Audio mastering, mixing, EQ, compression
- Loudness measurement and normalization (LUFS, EBU R128)
- Podcast recording, editing, production
- Music theory questions (chords, scales, progressions)
- Synthesis design (FM, subtractive, granular, wavetable)
- Spectrum analysis and audio visualization
- Sample rate/bit depth conversion
- Noise reduction and audio cleanup
- BPM/key detection
