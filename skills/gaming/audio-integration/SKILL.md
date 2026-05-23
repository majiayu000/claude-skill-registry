---
name: Audio Integration
description: |
  Use this skill when integrating audio into a game - mixing, prioritization, spatial audio, ducking, and audio states.

  **Triggers:** "audio mixing", "ducking", "sidechain", "audio priority", "spatial audio", "3D audio", "reverb zones", "audio bus", "loudness", "audio states".

  **Load references when:**
  - Bus structure templates → `references/bus-templates.md`
  - Ducking configurations → `references/ducking-recipes.md`
  - Spatial audio patterns → `references/spatial-audio.md`
  - Audio state machines → `references/audio-states.md`
version: 1.1.0
---

# Audio Integration

How audio elements work together in a game: mixing, prioritization, spatial positioning, and dynamic systems.

## Mix Architecture

### Standard Bus Structure
```
                    [Master Bus]
           ┌────────────┼────────────┐
        [Music]       [SFX]       [Voice]
           │            │
    ┌──────┴──────┐  ┌──┴───┬─────┐
[Ambient] [Combat] [UI] [World] [Creatures]
```

### Bus Purposes

| Bus | Contents | Processing |
|-----|----------|------------|
| Master | Everything | Final limiter |
| Music | All music | Ducking input |
| SFX | All effects | Compression |
| Voice | Dialogue | De-esser, comp |
| UI | Interface | Dry, consistent |

→ See `references/bus-templates.md` for full configurations.

---

## Mix Priorities

Not all sounds are equal:

| Priority | Category | Behavior |
|----------|----------|----------|
| 1 (Critical) | Player damage, alerts | Always audible |
| 2 (High) | Player actions, dialogue | Clear and present |
| 3 (Medium) | Enemy sounds, music | Supporting |
| 4 (Low) | Ambient details | Background |
| 5 (Background) | Environmental loops | Atmospheric |

**Voice stealing:** When max voices reached, steal from lower priorities.

---

## Ducking

Lower some sounds when others play.

### Common Relationships

| Trigger | Target | Amount | Purpose |
|---------|--------|--------|---------|
| Voice | Music | -6 to -12dB | Hear dialogue |
| SFX | Music | -3 to -6dB | Hear actions |
| Critical | All | -6dB | Emergency alerts |

**Parameters:**
- Threshold: Level that triggers ducking
- Duck amount: How much to reduce (dB)
- Attack: How fast to duck (10-50ms)
- Release: How fast to recover (200-500ms)

→ See `references/ducking-recipes.md` for implementation patterns.

---

## Spatial Audio

### Distance Attenuation

| Sound Type | Min Dist | Max Dist | Curve |
|------------|----------|----------|-------|
| Voice | 1m | 15m | Linear |
| Footsteps | 0.5m | 20m | Inverse |
| Gunshots | 5m | 200m | Logarithmic |
| Ambient point | 2m | 50m | Linear |
| UI | N/A | N/A | 2D (no falloff) |

### Occlusion

When sounds are blocked:
- Reduce volume (50% at full occlusion)
- Apply low-pass filter (20kHz → 500Hz)
- Muffled = blocked by walls

→ See `references/spatial-audio.md` for panning and occlusion code.

---

## Reverb Zones

| Space | Decay | Early Reflections | Wet Level |
|-------|-------|-------------------|-----------|
| Small room | 0.3-0.8s | High | 20-40% |
| Large hall | 1.5-3s | Medium | 30-50% |
| Cathedral | 4-8s | Low | 40-60% |
| Outdoor | 0.1-0.3s | Very low | 10-20% |
| Cave | 2-5s | High | 50-70% |

**Per-sound reverb sends:**
- Dialogue: Low (clarity)
- Footsteps: Match environment
- Music: Baked-in reverb

---

## Dynamic Range

### Compression by Context

| Context | Ratio | Attack | Release |
|---------|-------|--------|---------|
| Dialogue | 3:1 | 10ms | 200ms |
| SFX Bus | 2:1 | 1ms | 100ms |
| Music | 2:1 | 10ms | 300ms |
| Master | 4:1 | 5ms | 200ms |

### Loudness Targets

| Platform | Target | True Peak |
|----------|--------|-----------|
| PC/Console | -14 LUFS | -1 dBTP |
| Mobile | -16 LUFS | -1 dBTP |

---

## Audio States

Change audio based on game state:

| State | Music | SFX | Ambient | Notes |
|-------|-------|-----|---------|-------|
| Menu | 100% | 50% | 0% | Focus on music |
| Exploration | 80% | 100% | 100% | Full soundscape |
| Combat | 100% | 110% | 50% | SFX priority |
| Cutscene | 100% | 80% | 60% | Dialogue priority |
| Paused | 30% | 0% | 0% | Minimal |

**Transitions:** Crossfade between states (500ms-2s).

→ See `references/audio-states.md` for state machine patterns.

---

## Performance

### Voice Management
- Max voices: 32-64 typical
- Priority-based stealing
- Distance-based LOD (reduce update rate for distant sounds)

### Memory Management

| Load Type | Size | Use Case |
|-----------|------|----------|
| Resident | < 500KB | Frequent sounds |
| Streaming | > 500KB | Music, long ambient |
| On-demand | Rare | One-time sounds |

---

## Testing Checklist

- [ ] All sounds play without errors
- [ ] No clipping at master bus
- [ ] Priorities work (spawn 100 sounds)
- [ ] Ducking sounds natural
- [ ] Spatial audio pans correctly
- [ ] State transitions smooth
- [ ] Performance within budget

## Related Components

- `sonic-style-language` skill - Style consistency
- `audio-coherence-reviewer` agent - Validate integration
- `/establish-sonic-identity` - Set mix priorities
