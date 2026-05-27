---
name: audio-engineering-patterns
description: Audio production concepts, DSP fundamentals, mixing/mastering techniques, and DAW workflows. Bridges modular synthesis philosophy with practical audio engineering. Triggers on audio production, mixing, sound design, DSP, or music technology requests.
license: MIT
---

# Audio Engineering Patterns

Technical foundations for audio production and sound design.

## Signal Flow Fundamentals

### The Audio Chain

```
Source → Processing → Summing → Output

[Mic/Synth] → [EQ/Comp/FX] → [Mix Bus] → [Master] → [Playback]
```

### Gain Staging

Maintain optimal levels at each stage:

| Stage | Target Level | Headroom |
|-------|--------------|----------|
| Recording | -18 to -12 dBFS | 12-18 dB |
| Processing | -18 to -12 dBFS | 12-18 dB |
| Mix Bus | -6 to -3 dBFS | 3-6 dB |
| Master | -1 to -0.3 dBFS | True peak limit |

**Rule**: If a plugin sounds bad, check your input level first.

---

## Frequency Fundamentals

### The Spectrum

| Range | Frequency | Character | Instruments |
|-------|-----------|-----------|-------------|
| Sub Bass | 20-60 Hz | Felt, not heard | Kick, bass, 808 |
| Bass | 60-250 Hz | Foundation, warmth | Bass, low vocals |
| Low Mids | 250-500 Hz | Body, mud | Guitars, vocals |
| Mids | 500-2000 Hz | Presence, honk | Vocals, snare |
| Upper Mids | 2-4 kHz | Clarity, harshness | Vocals, guitars |
| Presence | 4-6 kHz | Definition, sibilance | Vocals, cymbals |
| Brilliance | 6-10 kHz | Air, shimmer | Cymbals, strings |
| Air | 10-20 kHz | Sparkle, hiss | Room, breath |

### EQ Patterns

**Subtractive First**:
1. Find problem frequencies (boost, sweep, identify)
2. Cut problems (narrow Q)
3. Boost characteristics (wide Q)

**Common Problem Areas**:
| Issue | Frequency | Action |
|-------|-----------|--------|
| Mud | 200-400 Hz | Cut |
| Boxiness | 400-600 Hz | Cut |
| Honk | 800-1000 Hz | Cut |
| Harshness | 2-4 kHz | Cut or dip |
| Sibilance | 5-8 kHz | De-ess or cut |

---

## Dynamics Processing

### Compression Parameters

| Parameter | Function | Typical Range |
|-----------|----------|---------------|
| Threshold | When compression starts | -30 to 0 dB |
| Ratio | How much compression | 2:1 to 20:1 |
| Attack | How fast it engages | 0.1-100 ms |
| Release | How fast it lets go | 50-1000 ms |
| Knee | Soft/hard transition | 0-12 dB |
| Makeup | Compensate for gain reduction | As needed |

### Compression Archetypes

| Style | Attack | Release | Ratio | Use |
|-------|--------|---------|-------|-----|
| Transparent | Fast | Auto | 2-3:1 | Vocals, mix bus |
| Punchy | Slow | Medium | 4-6:1 | Drums, bass |
| Glue | Medium | Slow | 2-4:1 | Mix bus, groups |
| Limiting | Fast | Fast | 10:1+ | Peaks, protection |
| Pumping | Slow | Fast | High | Creative effect |

### Sidechain Patterns

```
Trigger Source → Sidechain Input → Compressor → Target

[Kick] → [SC Input] → [Comp on Bass] → [Ducked Bass]
```

Use for:
- Kick/bass separation
- Vocal ducking
- Rhythmic pumping
- De-essing (high-pass SC)

---

## Spatial Processing

### Reverb Types

| Type | Character | Use |
|------|-----------|-----|
| Room | Small, tight | Drums, guitars |
| Hall | Large, long | Orchestral, pads |
| Plate | Dense, bright | Vocals, snare |
| Chamber | Warm, smooth | Strings, vocals |
| Spring | Bouncy, lo-fi | Guitars, vintage |
| Convolution | Realistic spaces | Film, realism |
| Algorithmic | Controllable | Everything |

### Reverb Parameters

| Parameter | Effect |
|-----------|--------|
| Pre-delay | Separation from source (20-80ms typical) |
| Decay/RT60 | Length of tail |
| Size | Room dimensions |
| Damping | High-frequency absorption |
| Diffusion | Density of reflections |
| Mix/Wet | Blend with dry signal |

### Delay Patterns

| Pattern | Timing | Use |
|---------|--------|-----|
| Slapback | 75-150 ms | Vocals, rockabilly |
| Doubling | 20-50 ms | Width, thickness |
| Rhythmic | Tempo-synced | Groove, production |
| Ping-pong | L/R alternating | Width, movement |
| Ambient | Long, diffused | Atmosphere |

**Tempo Sync Formula**:
```
ms = 60000 / BPM

1/4 note = 60000 / BPM
1/8 note = 30000 / BPM
1/16 note = 15000 / BPM
Dotted = value × 1.5
Triplet = value × 0.667
```

---

## Mix Architecture

### Bus Structure

```
                    ┌─────────────┐
                    │  Master Bus │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Drum Bus │    │Music Bus │    │Vocal Bus │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │K│S│H│OH│     │B│G│K│Pd│     │Ld│BV│Fx│
    └─────────┘     └─────────┘     └─────────┘
```

### Mix in Mono First

1. Get balance right in mono
2. Check phase relationships
3. Add stereo width last
4. Always reference in mono

### Static Mix Workflow

1. **Faders only**: Get rough balance
2. **Pan**: Create space left/right
3. **EQ**: Carve frequency space
4. **Compression**: Control dynamics
5. **Reverb/Delay**: Add depth
6. **Automation**: Movement and interest

---

## Mastering Fundamentals

### Chain Order

```
EQ → Compression → Saturation → Stereo Enhancement → Limiting
```

### Target Levels

| Platform | Target LUFS | True Peak |
|----------|-------------|-----------|
| Streaming (general) | -14 LUFS | -1 dB |
| Apple Music | -16 LUFS | -1 dB |
| YouTube | -14 LUFS | -1 dB |
| Club/DJ | -6 to -9 LUFS | -0.3 dB |
| Podcast | -16 LUFS | -1 dB |
| Broadcast | -24 LUFS | -2 dB |

### Metering

| Meter Type | Measures | Use For |
|------------|----------|---------|
| Peak | Instantaneous max | Clipping prevention |
| RMS | Average level | Perceived loudness |
| LUFS | Perceptual loudness | Streaming compliance |
| Phase | L/R correlation | Mono compatibility |
| Spectrum | Frequency content | Balance verification |

---

## DSP Fundamentals

### Basic DSP Operations

| Operation | Effect |
|-----------|--------|
| Gain | Multiply signal amplitude |
| Sum | Add signals together |
| Delay | Time offset (samples) |
| Filter | Frequency-dependent gain |
| Convolution | Apply impulse response |

### Filter Types

| Type | Effect | Use |
|------|--------|-----|
| Low-pass (LPF) | Removes highs | Warmth, lo-fi |
| High-pass (HPF) | Removes lows | Clarity, cleanup |
| Band-pass (BPF) | Isolates range | Radio, telephone |
| Notch | Removes specific freq | Feedback, hum |
| All-pass | Phase shift only | Phasers |
| Comb | Periodic peaks/notches | Flanging |

### Common Sample Rates

| Rate | Use | Nyquist |
|------|-----|---------|
| 44.1 kHz | CD, streaming | 22.05 kHz |
| 48 kHz | Video, broadcast | 24 kHz |
| 88.2 kHz | High-res (2× 44.1) | 44.1 kHz |
| 96 kHz | High-res production | 48 kHz |

---

## Sound Design Patterns

### Synthesis Types

| Type | Method | Character |
|------|--------|-----------|
| Subtractive | Filter harmonics | Classic analog |
| Additive | Sum partials | Precise, digital |
| FM | Modulate frequency | Complex, metallic |
| Wavetable | Morph waveforms | Evolving, digital |
| Granular | Micro-samples | Textural, ambient |
| Physical Modeling | Simulate physics | Realistic |
| Sampling | Recorded audio | Any source |

### Layering Strategy

```
Layer 1: Sub (20-80 Hz) - Foundation
Layer 2: Body (100-400 Hz) - Weight
Layer 3: Character (400-2000 Hz) - Identity
Layer 4: Presence (2-6 kHz) - Cut-through
Layer 5: Air (8-16 kHz) - Sparkle
```

### Movement Techniques

- LFO modulation (filter, pitch, amplitude)
- Envelope shaping (attack, decay curves)
- Automation (any parameter over time)
- Randomization (subtle variation)
- Sidechain (rhythmic pumping)

---

## References

- `references/frequency-chart.md` - Detailed frequency guide
- `references/plugin-chains.md` - Common processing chains
- `references/daw-shortcuts.md` - DAW workflow tips
