---
name: Audio Layering & Somatic Cue
tier: 1
load_policy: always
description: Nervous system engineering for safe, embodied trance experiences
version: 1.0.0
---

# Audio Layering & Somatic Cue Skill

> **This Is Nervous-System Engineering, Not "Background Music"**

This Skill controls how the **body** experiences the journey.

You can have perfect language and perfect symbolism—and still fail if the body does not feel safe.

---

## Purpose

Regulate the listener's physiological state to support safe, embodied trance experiences through breath, sound, and somatic awareness.

This Skill manages four biological systems:

1. **Breath rhythm** — Pacing and autonomic regulation
2. **Muscle tone** — Relaxation without disconnection
3. **Arousal level** — Depth without overwhelm
4. **Orientation** — Body presence vs dissociation

---

## Core Question

At all times, the listener's nervous system asks:

> "Am I safe right now?"

Audio + somatic cues answer this question continuously, below conscious awareness.

---

## Must Always

- Keep voice dominant over music/effects
- Anchor in breath and body before imagery
- Reintroduce physical awareness regularly
- Match audio pacing to desired nervous system state
- Include body orientation during emergence

---

## Never

- Use rhythms that override natural breath
- Stack silence + deep imagery without somatic anchor
- Create audio that induces dissociation
- Allow music to dominate voice
- Forget body during deep visualization

---

## Sub-Skills

### Breath Regulation (`breath-regulation/`)
- `inhale-exhale-pacing.md` — Breath timing for calming
- `breath-language-mapping.md` — Speech ↔ breath synchronization
- `coherence-ratios.md` — HRV-optimized breathing patterns

### Somatic Anchoring (`somatic-anchoring/`)
- `heaviness.md` — Gravitational grounding cues
- `warmth.md` — Temperature-based comfort
- `grounded-contact.md` — Physical surface awareness
- `posture-awareness.md` — Body position consciousness

### Arousal Control (`arousal-control/`)
- `calming-curves.md` — Progressive relaxation trajectories
- `intensity-ceilings.md` — Maximum depth safety limits
- `overload-prevention.md` — Emotional flooding guards

### Audio Layering (`audio-layering/`)
- `voice-vs-music-balance.md` — Mix priority rules
- `frequency-bands.md` — Spectral allocation
- `rhythm-constraints.md` — BPM and tempo safety
- `silence-usage.md` — Pause strategy

### Exit Reintegration (`exit-reintegration/`)
- `sensory-return.md` — Awareness restoration
- `body-orientation.md` — Physical reconnection
- `temporal-awareness.md` — Time re-grounding

### Validation (`validation/`)
- `dissociation-red-flags.md` — Warning pattern detection
- `pacing-checks.md` — Rhythm verification
- `loudness-consistency.md` — Level validation

---

## Breath Regulation

### The Golden Rule

**Exhale longer than inhale = parasympathetic activation**

Suggested ratios:
- Light relaxation: 4-4 (equal)
- Moderate depth: 4-6 (1:1.5)
- Deep relaxation: 4-8 (1:2)

### Breath-Paced Speech

Phrases should end on exhale, pauses placed where exhale naturally occurs:

```xml
<prosody rate="1.0" pitch="-1st">
  Breathing in... <break time="1.5s"/>
  and letting go... <break time="3s"/>
  with each exhale... <break time="2s"/>
  releasing... <break time="2s"/>
  more deeply.
</prosody>
```

---

## Somatic Anchoring

### The Anti-Dissociation Core

Somatic cues keep consciousness inside the body.

#### Approved Anchors

| Anchor | SSML Example |
|--------|--------------|
| Warmth | "A gentle warmth spreading through your chest..." |
| Heaviness | "Your arms growing pleasantly heavy..." |
| Contact | "The surface beneath you, supporting..." |
| Breath | "The rise and fall of your breathing..." |
| Weight | "The weight of your body, resting..." |

#### Forbidden Anchors

| Pattern | Why Dangerous |
|---------|---------------|
| "Floating away" | Dissociation trigger |
| "Melting into nothing" | Body dissolution |
| "Leaving your body behind" | Explicit dissociation |
| "Becoming pure light" | Body transcendence |

### Insertion Frequency

| Session Phase | Somatic Cue Frequency |
|---------------|----------------------|
| Pre-talk | Every 2-3 minutes |
| Induction | Every 1-2 minutes |
| Deepening | Every 1-2 minutes |
| Journey | Every 2-3 minutes |
| Helm (deep) | Every 1-2 minutes |
| Integration | Every 2 minutes |
| Emergence | Continuous |

---

## Audio Layering Rules

### Voice Dominance Principle

**Voice ≥ foreground at all times**

| Element | Level | Role |
|---------|-------|------|
| Voice | -6 dB reference | Always dominant |
| Binaural | -6 to -9 dB | Support, never compete |
| Ambient | -12 to -18 dB | Atmosphere only |
| SFX | Variable | Momentary emphasis |

### Frequency Band Separation

- **Voice**: Mid-range protected (200Hz - 4kHz)
- **Binaural**: Low (base 100-400Hz)
- **Ambient**: High and low, avoiding mid
- **SFX**: Momentary, any band

### Rhythm Constraints

| Constraint | Rule |
|------------|------|
| No hypnotic drumming | Without body anchors |
| No sudden tempo changes | Gradual transitions only |
| No percussive spikes | Unpredictable startle |
| BPM ceiling | 60-70 BPM max for deep work |

### Silence Strategy

Silence is a tool, not absence:

```
Silence ≠ Absence
Silence = Integration window
```

**Rules:**
- Never silence + deep imagery + no body cue
- Maximum intentional silence: 5 seconds
- Longer pauses need ambient continuation
- Silence always followed by grounding

---

## Arousal Regulation

### The Window of Tolerance

Keep listener within their capacity for experience:

```
Too High (Hyperarousal)
↑ anxiety, overwhelm, panic
─────────────────────────────
OPTIMAL ZONE (Safe trance)
─────────────────────────────
↓ numbness, dissociation, collapse
Too Low (Hypoarousal)
```

### Regulation Techniques

| Direction | Audio Technique | Somatic Cue |
|-----------|-----------------|-------------|
| Calm down | Slower tempo, lower frequencies | Breath exhale, heaviness |
| Lift up | Slightly brighter tone, more SFX | Body movement, sensory detail |
| Stabilize | Steady ambient, consistent voice | Ground contact, breath awareness |

---

## Exit & Reintegration

### Non-Negotiable Components

Every session must restore:

1. **Body awareness** — Physical sensation return
2. **Sensory orientation** — Sound, touch, temperature
3. **Time awareness** — Normal clock sense
4. **Emotional neutrality** — Not left in intensity

### Exit Sequence Audio

```
Deep ambient → gradually brighten
Low frequencies → add mid/high
Slow tempo → slightly increase
Reverb → reduce to drier sound
```

---

## Integration With Other Skills

| Skill | Relationship |
|-------|--------------|
| `hypnotic-language/` | Provides text that audio accompanies |
| `symbolic-mapping/` | Imagery requires body anchor |
| `psychological-stability/` | Tier 2 triggers when arousal exceeds window |

---

## Production Integration

### Before SSML Generation

- Set breath cadence targets
- Define somatic anchor frequency
- Choose audio density profile

### During SSML Generation

- Insert body-check phrases
- Control pause timing
- Avoid forbidden imagery patterns

### After TTS

- Check speech rate compatibility
- Flag intensity spikes

### After Mix

- Validate loudness (-14 LUFS target)
- Ensure voice dominance
- Check transitions

---

## Quality Rubric

Before approving any audio:

| Criterion | Check |
|-----------|-------|
| Voice clarity | Can every word be understood? |
| Body anchoring | Are somatic cues frequent enough? |
| Arousal regulation | Does intensity stay in safe range? |
| Emergence | Is return to normal complete? |
| Dissociation | Any red flag patterns? |

---

## Related Resources

- **Serena Memory**: `audio_production_methodology`
- **Knowledge**: `knowledge/binaural_presets.yaml`
- **Knowledge**: `knowledge/psychology/polyvagal_theory.yaml`
- **Validation**: `scripts/utilities/validate_binaural.py`
