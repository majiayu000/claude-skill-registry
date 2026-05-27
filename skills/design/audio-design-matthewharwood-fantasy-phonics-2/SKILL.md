---
name: audio-design
description: Game audio design patterns for creating sound effects and UI audio. Use when designing sounds for games, writing AI audio prompts (ElevenLabs, etc.), creating feedback sounds, or specifying audio for abilities/UI. Includes psychological principles from Kind Games, volume hierarchy, frequency masking prevention, and prompt engineering for AI audio generation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Audio Design for Games

Psychological principles and practical patterns for designing game audio that enhances player experience without causing fatigue or cognitive overload. This skill covers sound design philosophy, AI prompt engineering for audio generation, and technical specifications.

## Related Skills

- **`web-audio`**: Technical implementation patterns (AudioContext, preloading, cloneNode)
- **`ux-feedback-patterns`**: Visual + audio feedback coordination
- **`ux-animation-motion`**: Timing audio with visual animations
- **`ux-accessibility`**: Reduced motion/audio preferences

---

## Core Philosophy: Audio as Skill Atom Feedback

From Daniel Cook's Skill Atom framework, audio serves as **immediate feedback** that creates insight:

```
Action → Simulation → Feedback (AUDIO) → Insight
```

**Key Principles:**

1. **Proportional Feedback**: Sound intensity matches action significance
2. **Melodic Hierarchy**: Sounds build from simple to complex as achievements grow
3. **Error as Invitation**: Failure sounds should redirect, not punish
4. **Fantasy Cohesion**: All sounds share a unified palette creating consistent world
5. **No Cognitive Overload**: Sounds inform, never overwhelm

---

## Rule 1: Volume Hierarchy by Sound Type

Different sounds serve different psychological purposes and need balanced volumes.

| Sound Category | Volume | Frequency | Psychology |
|----------------|--------|-----------|------------|
| Micro-feedback (hover, type) | 0.2–0.3 | Very high | Subtle confirmation, shouldn't fatigue |
| UI interaction (click, toggle) | 0.25–0.35 | High | Tactile feedback, responsive feel |
| Success/feedback | 0.3–0.5 | Moderate | Clear outcome signal |
| Warning/attention | 0.4–0.5 | Low | Noticeable but not alarming |
| Phase completion | 0.5–0.6 | Low | Meaningful milestone |
| Major achievement | 0.6–0.8 | Rare | Celebration, memorable |
| Background music | 0.15–0.25 | Continuous | Atmosphere, never dominate |

**Why:** Balanced audio creates professional feel. Loud frequent sounds cause fatigue; quiet celebrations feel anticlimactic.

---

## Rule 2: Frequency Band Management (Anti-Masking)

Sounds must occupy distinct frequency bands to remain readable when played together.

### Frequency Allocation

| Sound Type | Primary Band | HPF | Notes |
|------------|--------------|-----|-------|
| Sub-bass (rumble, impact) | 30–80 Hz | None | Use sparingly, causes mud |
| Bass (weight, power) | 80–200 Hz | 80 Hz | Rock, thuds, explosions |
| Low-mid (body, warmth) | 200–500 Hz | 150–200 Hz | Most sounds need HPF here |
| Mid (clarity, presence) | 500 Hz–2 kHz | — | Core content for most sounds |
| Upper-mid (detail, attack) | 2–4 kHz | — | Transients, consonants |
| Presence (brilliance) | 4–8 kHz | — | Air, shimmer |
| High (sparkle, air) | 8–16 kHz | — | Gentle, avoid harshness |

### HPF (High-Pass Filter) Guidelines

```
HPF 100–150 Hz  → Heavy impacts, bass elements
HPF 150–200 Hz  → Standard UI, most game sounds
HPF 200–250 Hz  → Light, airy sounds (sparkles, chimes)
HPF 250+ Hz     → Ethereal, floating sounds
```

**Why:** Low frequencies mask each other and cause "mud." HPF keeps sounds clean and distinct.

---

## Rule 3: Duration by Function

Sound length must match its psychological purpose.

| Function | Duration | Rationale |
|----------|----------|-----------|
| Micro-feedback (keystroke) | 50–120 ms | Instant, doesn't interrupt |
| UI click/tap | 100–180 ms | Responsive, crisp |
| Success feedback | 200–400 ms | Satisfying but brief |
| Warning/alert | 250–500 ms | Attention-getting |
| Phase celebration | 400–800 ms | Meaningful pause |
| Major achievement | 600–1200 ms | Memorable moment |
| Ambient loop | Seamless | Background atmosphere |

### Tail Management

**Critical:** Keep tails tight to prevent audio pile-up.

```
Decay 100–250 ms  → Snappy, rapid-fire safe
Decay 250–400 ms  → Standard feedback
Decay 400–600 ms  → Celebrations, important moments
Decay 600+ ms     → Only for rare, significant events
```

---

## Rule 4: Kind Games Audio Philosophy

From Daniel Cook's Kind Games framework, audio should support prosocial design:

### Audio for Psychological Safety

| Goal | Sound Design | Anti-Pattern |
|------|--------------|--------------|
| **Error as invitation** | Gentle questioning tone, descending then rising | Harsh buzzer, punishment |
| **Encouragement** | Warm, supportive tones | Mocking or condescending |
| **Progress celebration** | Proportional joy | Over-the-top for minor achievements |
| **Failure feedback** | Curious, "try again" feel | Shame-inducing |

### Error Sound Design

```
✅ Good: "Gentle descending three-note woodwind phrase, curious not sad"
✅ Good: "Soft 'hmm' with upward questioning inflection at end"

❌ Bad: "Harsh buzzer sound"
❌ Bad: "Sad trombone descending"
❌ Bad: "Game show failure sound"
```

### Success Sound Hierarchy

Build a melodic progression that players learn to anticipate:

```
Micro:     Single tone (sparkle, chime)
Small:     Two-note ascending (success)
Medium:    Three-note phrase (phase complete)
Major:     Full flourish with resolution (achievement)
Epic:      Orchestral swell with choir (milestone)
```

---

## Rule 5: AI Audio Prompt Engineering (ElevenLabs)

When generating sounds via AI, use these prompt patterns for high clarity, low masking, non-musical UI readability.

### Prompt Structure

```
[Sound description] + [Technical specs] + [Anti-patterns]
```

### Technical Spec Template

```
"{description}, {frequency info} ({X}–{Y} kHz), HPF {Z} Hz,
{duration} ms, {decay/tail info}, no {anti-patterns}"
```

### Frequency Descriptors

| Term | Frequency Range | Use For |
|------|-----------------|---------|
| "bright transient" | 2–4 kHz | Attacks, clicks, impacts |
| "airy sheen/shimmer" | 8–12 kHz | Magic, sparkles, ethereal |
| "low-mid body" | 200–500 Hz | Warmth, weight |
| "mid presence" | 1–2 kHz | Clarity, readability |
| "sub rumble" | 30–80 Hz | Impact, power (use sparingly) |

### Essential Anti-Patterns to Include

Always specify what to **avoid** in prompts:

```
"no melody"         → Prevents musical interference with game music
"no pad/drone"      → Prevents sustained tones that cause masking
"no reverb wash"    → Keeps sound tight and readable
"no low-end buildup" → Prevents mud in mix
"no harsh highs"    → Prevents ear fatigue
"no musical tone"   → Keeps UI sounds non-distracting
"non-musical"       → Reinforces UI intent
```

---

## Rule 6: Sound Category Templates

### UI Micro-Feedback

```
"Soft {material} {action}, {duration} ms, bright transient (2–4 kHz),
HPF {180–220} Hz, short decay {80–150} ms, no musical tone, no reverb."

Examples:
- "Soft wooden tok with subtle shimmer tail, 120 ms, bright 2–4 kHz, HPF 200 Hz"
- "Gentle paper rustle with airy top, 100 ms, HPF 180 Hz, no reverb"
```

### Success/Completion

```
"Warm {instrument} {motion} with {quality} {overtone}, {duration} ms,
{frequency detail}, HPF {X} Hz, {decay} decay, non-melodic."

Examples:
- "Warm ascending harp glissando with gentle bell overtone, 350 ms"
- "Bright crystalline chime with soft shimmer tail, 300 ms, 8–12 kHz"
```

### Error/Invalid

```
"Gentle {instrument} {motion}, {quality} not {negative}, {duration} ms,
HPF {X} Hz, reads as '{intention}'."

Examples:
- "Gentle descending three-note woodwind phrase, curious not sad, 400 ms"
- "Soft questioning hum with upward inflection, 300 ms, HPF 200 Hz"
```

### Achievement/Celebration

```
"{Scale} {instrument} {action} with {detail}, {duration} ms,
{frequency}, {space} {wet%}, non-melodic."

Examples:
- "Full magical fanfare with shimmering strings, 800 ms, short room 0.3s 15% wet"
- "Grand orchestral flourish with bells and rising resolution, 1000 ms"
```

### Impact/Action

```
"{Weight} {material} {action} + {secondary}, {duration} ms,
HPF {X} Hz, {decay}, no boom, no long tail."

Examples:
- "Heavy stone thud with brief debris ticks, 400 ms, HPF 150 Hz, dry"
- "Shield deflect: tight metallic ting with micro scrape, 150 ms"
```

---

## Rule 7: Fantasy Theme Palette

For cohesive fantasy audio, maintain consistent instrument families:

### Magical/Ethereal
- Chimes (crystalline, bell-like)
- Harps (warm, flowing)
- Wind instruments (airy, breathy)
- Sparkle textures (high shimmer)

### Earthen/Natural
- Wood (soft toks, knocks)
- Stone (thuds, scrapes)
- Organic (sprouts, rustles)
- Water (drips, flows)

### Metal/Martial
- Sword (slices, clangs)
- Shield (deflects, impacts)
- Armor (clinks, rattles)
- Mechanical (clicks, locks)

### Mystical/Divine
- Choir textures (soft "ahh")
- Bells (resonant, pure)
- Shimmer (ascending)
- Glow sounds (warm hum)

---

## Rule 8: Multi-Instance Handling

When sounds may trigger simultaneously (40+ players casting), apply these modifiers:

### Layered Event Prompt Modifier

```
"40 layered one-shots, onset jitter 10–40 ms, pitch variance ±2–4 semitones,
wide stereo distribution, HPF consistent, subtle short room 0.2–0.3 s at 8–12% wet,
avoid masking and low-end buildup, preserve transient clarity."
```

### Key Techniques

| Technique | Purpose |
|-----------|---------|
| Onset jitter (10–40 ms) | Prevents phase cancellation |
| Pitch variance (±2–4 semi) | Creates natural variation |
| Stereo distribution | Spatial separation |
| Short room (0.2–0.3s, 8–12%) | Cohesion without wash |
| Consistent HPF | Prevents mud accumulation |

---

## Rule 9: Accessibility Considerations

### Reduced Audio for Motion Sensitivity

Some users prefer reduced audio stimulation with reduced motion:

```javascript
// Audio should respect prefers-reduced-motion
const reduceAudio = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (reduceAudio) {
  // Use simpler, shorter sounds
  // Reduce celebration intensity
  // Skip non-essential feedback sounds
}
```

### Non-Audio Alternatives

Every sound should have a visual equivalent:
- Micro-feedback → Visual pulse/glow
- Success → Color flash + checkmark
- Error → Shake animation + icon
- Achievement → Badge animation

---

## Rule 10: Testing Checklist

Before finalizing sounds:

- [ ] **Volume balance**: All sounds sit correctly in hierarchy
- [ ] **Frequency separation**: No masking when sounds overlap
- [ ] **Duration appropriate**: Matches function and pacing
- [ ] **HPF applied**: No unwanted low-end
- [ ] **Tail tight**: No lingering that causes pile-up
- [ ] **Non-musical**: Doesn't interfere with game music
- [ ] **Error inviting**: Failure sounds encourage retry
- [ ] **Celebration proportional**: Matches achievement significance
- [ ] **Accessible**: Works with reduced audio preference
- [ ] **40-cast safe**: Still readable when many play together

---

## Example: Fantasy Phonics Sound Design

### Complete Sound Specification

| Sound | Prompt | Vol | Duration |
|-------|--------|-----|----------|
| `sparkle` | "Soft twinkling chime like fairy dust falling, brief delicate whispered magic, 2–4 kHz transient + 8–12 kHz shimmer, HPF 220 Hz, 100 ms, no musical tone" | 0.25 | 100 ms |
| `success` | "Warm ascending harp glissando with gentle bell overtone, spell completing successfully, 2–6 kHz, HPF 200 Hz, 350 ms decay, non-melodic" | 0.4 | 350 ms |
| `phaseComplete` | "Crystalline chime cascade with soft orchestral swell, treasure chest unlock feel, triumphant but intimate, 4–12 kHz, HPF 200 Hz, 600 ms, short room 0.2s 10% wet" | 0.6 | 600 ms |
| `wordComplete` | "Full magical fanfare with shimmering strings and choir ahh, spell book illuminating, genuine mastery, 1–12 kHz, HPF 150 Hz, 800 ms, room 0.3s 15% wet" | 0.7 | 800 ms |
| `milestone` | "Grand orchestral flourish with bells rising to majestic resolution, wizard rank-up energy, proudest moment, full spectrum, HPF 100 Hz, 1200 ms, room 0.4s 20% wet" | 0.75 | 1200 ms |
| `click` | "Soft wooden tok with subtle magical shimmer tail, tapping wizard staff, tactile responsive, 2–8 kHz, HPF 200 Hz, 120 ms, no reverb" | 0.25 | 120 ms |
| `error` | "Gentle descending three-note woodwind phrase, curious not sad, sounds like 'hmm try again', invitation to explore, 500 Hz–4 kHz, HPF 180 Hz, 400 ms, no harsh" | 0.35 | 400 ms |

### Design Rationale

- **Melodic hierarchy**: sparkle (single) → success (ascending) → milestone (full flourish)
- **Fantasy cohesion**: Chimes, harps, bells, woodwinds — storybook palette
- **Error as invitation**: Questioning woodwind, not punishing buzzer
- **Proportional celebration**: 100 ms micro vs 1200 ms milestone

---

## Quick Reference: Prompt Building Blocks

### Descriptive Words by Feeling

| Feeling | Words |
|---------|-------|
| Light/Airy | soft, gentle, delicate, whispered, airy, ethereal |
| Warm/Safe | warm, cozy, friendly, inviting, supportive |
| Magical | crystalline, shimmering, sparkling, enchanted, mystical |
| Powerful | full, rich, majestic, triumphant, grand |
| Playful | bouncy, bright, cheerful, lively, sprightly |
| Serious | deep, resonant, solemn, weighty |

### Motion Words

| Motion | Use For |
|--------|---------|
| ascending | Success, progress, achievement |
| descending | Failure (gentle), settling, ending |
| cascading | Celebrations, reveals |
| pulsing | Attention, warnings |
| swelling | Building tension, major moments |
| fading | Endings, transitions |

### Material Words

| Material | Sound Character |
|----------|-----------------|
| glass/crystal | Bright, fragile, magical |
| wood | Warm, organic, grounded |
| metal | Crisp, mechanical, martial |
| stone | Heavy, ancient, solid |
| water | Flowing, soothing, natural |
| air | Light, ethereal, spacious |
