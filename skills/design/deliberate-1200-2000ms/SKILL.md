---
name: deliberate-1200-2000ms
description: Use when building slow intentional animations between 1200-2000ms - app intros, loading sequences, storytelling moments that create emotional resonance
---

# Deliberate Animations (1200-2000ms)

At 1200-2000ms, you're creating **experiences, not interfaces**. This duration is for moments of genuine storytelling where animation itself is the content.

## Disney Principles at Deliberate Speed

### Full Narrative Expression

**Squash & Stretch**: Character-defining - 30-40% deformation creates personality. Objects become characters.

**Anticipation**: Full dramatic preparation - 300-400ms wind-up creates tension and expectation.

**Staging**: Scene direction - think cinematography. Establish shot, then detail. Clear narrative flow.

**Straight Ahead/Pose to Pose**: Pose to pose mandatory - 6-10 key poses define the narrative arc.

**Follow Through**: Extended settling - 300-500ms of secondary motion after primary completes.

**Slow In/Slow Out**: Narrative pacing - ease curves tell emotional stories. Sharp starts mean urgency, soft ends mean resolution.

**Arcs**: Orchestrated paths - motion paths are designed, not default. Each element's trajectory contributes to composition.

**Secondary Action**: Full ecosystem - primary, secondary, tertiary, ambient all working together.

**Timing**: 72-120 frames at 60fps. Animation-quality frame counts.

**Exaggeration**: Emotional amplification - push for feeling, not just movement.

**Solid Drawing**: Dimensional storytelling - parallax, depth, perspective shifts create space.

**Appeal**: Deep emotional engagement - users feel something during these animations.

## Easing Recommendations

```css
/* Narrative arc - beginning, middle, end */
animation-timing-function: cubic-bezier(0.34, 0, 0.14, 1);

/* Graceful, considered motion */
transition: all 1500ms cubic-bezier(0.16, 1, 0.3, 1);

/* Building momentum */
transition: all 1800ms cubic-bezier(0.65, 0, 0.35, 1);

/* Elastic storytelling */
transition: transform 1600ms cubic-bezier(0.68, -0.6, 0.32, 1.6);
```

## Best Use Cases

- App splash/launch sequences
- Brand moments
- Tutorial narratives
- Achievement celebrations
- Milestone animations
- Emotional state changes (error to success)
- Story-driven onboarding
- Feature announcements

## Implementation Pattern

```css
@keyframes appLaunch {
  0% {
    opacity: 0;
    transform: scale(0.6) translateY(50px);
    filter: blur(10px);
  }
  30% {
    opacity: 1;
    filter: blur(5px);
  }
  60% {
    transform: scale(1.02) translateY(-10px);
    filter: blur(0);
  }
  80% {
    transform: scale(0.99) translateY(5px);
  }
  100% {
    transform: scale(1) translateY(0);
  }
}

.app-launch {
  animation: appLaunch 1800ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

## Critical Considerations

- Users MUST be able to skip/dismiss
- Never block critical paths
- Avoid on repeat visits (detect returning users)
- Must add genuine value, not decoration
- Test for motion sensitivity (prefer reduced motion)

## Key Insight

Deliberate animations are **brand investments**. They don't just show what's happening - they make users feel something. Budget for design, iteration, and testing. These moments define perceived quality.
