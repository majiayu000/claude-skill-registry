---
name: gsap-router
description: Router for GSAP animation domain. Use when implementing animations with GreenSock Animation Platform including tweens, timelines, scroll-based animations, or React integration. Routes to 4 specialized skills for fundamentals, sequencing, ScrollTrigger, and React patterns.
---

# GSAP Router

Routes to 4 specialized skills based on animation requirements.

## Routing Protocol

1. **Classify** — Identify animation type from user request
2. **Match** — Apply signal matching rules below
3. **Combine** — Production animations often need 2-3 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core (Start Here)
| Need | Skill | Signals |
|------|-------|---------|
| Basic animations, easing | `gsap-fundamentals` | tween, animate, ease, from, to, duration, delay |
| Complex sequences | `gsap-sequencing` | timeline, sequence, orchestrate, labels, callbacks |
| Scroll animations | `gsap-scrolltrigger` | scroll, pin, scrub, parallax, reveal, sticky |
| React integration | `gsap-react` | React, useGSAP, ref, hook, cleanup, context |

## Signal Matching

### Primary Signals

**gsap-fundamentals**:
- "animate", "tween", "transition"
- "ease", "easing", "timing"
- "from", "to", "fromTo"
- "duration", "delay", "repeat"
- "stagger", "properties"

**gsap-sequencing**:
- "timeline", "sequence", "orchestrate"
- "labels", "callbacks", "nested"
- "position parameter", "overlap"
- "complex animation", "choreography"
- "play", "pause", "reverse", "seek"

**gsap-scrolltrigger**:
- "scroll", "ScrollTrigger"
- "pin", "sticky", "fixed"
- "scrub", "parallax"
- "reveal on scroll", "snap"
- "progress indicator"

**gsap-react**:
- "React", "component"
- "useGSAP", "useRef", "hook"
- "cleanup", "context"
- "event handler", "state"

### Confidence Scoring

- **High (3+ signals)** — Route directly to matched skill
- **Medium (1-2 signals)** — Route with fundamentals as foundation
- **Low (0 signals)** — Start with `gsap-fundamentals`

## Common Combinations

### Basic Animation (1 skill)
```
gsap-fundamentals → Tweens, easing, basic properties
```

### React Component Animation (2 skills)
```
gsap-fundamentals → Animation principles, easing
gsap-react → Hook patterns, cleanup, refs
```

### Scroll-Based Experience (3 skills)
```
gsap-scrolltrigger → Scroll triggers, pinning
gsap-sequencing → Timeline for pinned sections
gsap-fundamentals → Individual animations
```

### Full Production (3-4 skills)
```
gsap-fundamentals → Core animations
gsap-sequencing → Complex orchestration
gsap-react → Framework integration
gsap-scrolltrigger → Scroll interactions (if needed)
```

## Decision Table

| Framework | Animation Type | Complexity | Route To |
|-----------|---------------|------------|----------|
| Vanilla JS | Simple | Low | fundamentals |
| Vanilla JS | Sequenced | Medium | fundamentals + sequencing |
| Vanilla JS | Scroll-based | Medium | fundamentals + scrolltrigger |
| React | Simple | Low | fundamentals + react |
| React | Complex | High | All four skills |
| React | Scroll | Medium | react + scrolltrigger |

## Animation Categories

### Motion Type → Skill Mapping

| Animation Type | Primary Skill | Supporting Skill |
|----------------|---------------|------------------|
| Fade in/out | `gsap-fundamentals` | - |
| Slide/move | `gsap-fundamentals` | - |
| Scale/rotate | `gsap-fundamentals` | - |
| Stagger | `gsap-fundamentals` | - |
| Page transitions | `gsap-sequencing` | fundamentals |
| Orchestrated reveals | `gsap-sequencing` | fundamentals |
| Scroll reveals | `gsap-scrolltrigger` | fundamentals |
| Parallax | `gsap-scrolltrigger` | - |
| Pinned sections | `gsap-scrolltrigger` | sequencing |
| React animations | `gsap-react` | fundamentals |
| React + scroll | `gsap-react` | scrolltrigger |

## Integration with Other Domains

### With R3F (r3f-*)
```
r3f-fundamentals → 3D scene setup
gsap-fundamentals → Object property animation
gsap-sequencing → Camera movements, scene transitions
```
GSAP animates Three.js object properties via `onUpdate`.

### With Post-Processing (postfx-*)
```
postfx-composer → Effect setup
gsap-fundamentals → Animate effect parameters
gsap-sequencing → Transition between effect states
```
GSAP drives effect intensity, colors, etc.

### With Audio (audio-*)
```
audio-playback → Music timing
gsap-sequencing → Sync animations to audio cues
gsap-fundamentals → Audio-reactive property changes
```
Timeline callbacks sync with audio events.

### With Particles (particles-*)
```
particles-systems → Particle emitters
gsap-fundamentals → Animate emitter properties
gsap-sequencing → Particle burst sequences
```

## Workflow Patterns

### Page Load Animation
```
1. gsap-fundamentals → Understand tweens, easing
2. gsap-sequencing → Build entrance timeline
3. gsap-react → Integrate with React (if applicable)
```

### Scroll Experience
```
1. gsap-scrolltrigger → Set up triggers, pins
2. gsap-sequencing → Build scrubbed timelines
3. gsap-fundamentals → Individual animation properties
```

### Interactive UI
```
1. gsap-fundamentals → Hover, click animations
2. gsap-react → Event handlers, cleanup
3. gsap-sequencing → Complex interaction sequences
```

## Temporal Collapse Stack

For the New Year countdown project:
```
gsap-fundamentals → Digit animations, pulse effects, easing
gsap-sequencing → Countdown sequence, final moment orchestration
gsap-react → Component integration, cleanup
```

Key animations:
- Digit flip on time change
- Pulse/glow intensity over time
- Final countdown dramatic sequence
- Celebration reveal at zero

## Quick Reference

### Task → Skills

| Task | Primary | Secondary |
|------|---------|-----------|
| "Animate this element" | fundamentals | - |
| "Create entrance animation" | fundamentals | react |
| "Build page transition" | sequencing | fundamentals |
| "Animate on scroll" | scrolltrigger | fundamentals |
| "React component animation" | react | fundamentals |
| "Pinned scroll section" | scrolltrigger | sequencing |
| "Complex animation sequence" | sequencing | fundamentals |
| "Staggered list animation" | fundamentals | react |

### Easing Quick Reference

| Feel | Ease |
|------|------|
| Snappy UI | `power2.out` |
| Smooth entrance | `power3.out` |
| Playful bounce | `back.out(1.7)` |
| Springy | `elastic.out` |
| Ball drop | `bounce.out` |
| Linear/mechanical | `none` |

## Fallback Behavior

- **No framework stated** → Assume vanilla JS, start with `gsap-fundamentals`
- **React mentioned** → Add `gsap-react` to combination
- **Scroll mentioned** → Add `gsap-scrolltrigger`
- **"Complex" or "sequence"** → Add `gsap-sequencing`
- **Unclear requirements** → Start with `gsap-fundamentals`

## Performance Priority

When performance is critical:
1. `gsap-fundamentals` — Use transforms, avoid layout properties
2. `gsap-react` — Proper cleanup prevents memory leaks
3. `gsap-scrolltrigger` — Use `scrub` wisely, batch updates
4. `gsap-sequencing` — Reuse timelines, don't recreate
