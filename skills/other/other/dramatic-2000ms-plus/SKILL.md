---
name: dramatic-2000ms-plus
description: Use when building extended animation sequences over 2000ms - cinematic intros, story sequences, premium experiences where animation IS the product
---

# Dramatic Animations (2000ms+)

Beyond 2000ms, animation becomes **cinema**. These aren't UI transitions - they're short films embedded in your product. Reserve for moments that define your brand.

## Disney Principles at Dramatic Scale

### Full Cinematic Treatment

**Squash & Stretch**: Fully animated character - 40%+ deformation for organic, living motion. Physics-defying when needed.

**Anticipation**: Dramatic tension - 400-600ms build-up. The audience waits with expectation.

**Staging**: Cinematography - establishing shots, close-ups, reveals. Think in scenes, not states.

**Straight Ahead/Pose to Pose**: Hybrid approach - pose-to-pose structure with straight-ahead detail passes.

**Follow Through**: Extended ecosystem - everything continues moving after primary action. World feels alive.

**Slow In/Slow Out**: Emotional timing - curves match narrative beats. Pause for emphasis.

**Arcs**: Choreographed paths - every element's path is intentionally designed.

**Secondary Action**: Full orchestration - layers of motion at different scales and speeds.

**Timing**: 120+ frames at 60fps. Full animation production values.

**Exaggeration**: Artistic license - break physics for emotional truth.

**Solid Drawing**: 3D environments - parallax, depth of field, camera movement.

**Appeal**: Memorable experiences - users tell others about these moments.

## Easing Recommendations

```css
/* Multi-phase narrative */
animation-timing-function: cubic-bezier(0.22, 0.61, 0.36, 1);

/* Building drama */
animation-timing-function: cubic-bezier(0.55, 0.06, 0.68, 0.19);

/* Resolution/satisfaction */
animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1);

/* Complex sequences - use multiple keyframes with varying easings */
```

## Best Use Cases

- Product launch reveals
- Brand hero moments
- Premium onboarding (once per user)
- Achievement/milestone celebrations
- Game-like interactions
- Data story visualizations
- Annual report animations
- Marketing microsites

## Implementation Pattern

```css
@keyframes epicReveal {
  0% {
    opacity: 0;
    transform: perspective(1000px) rotateX(30deg) translateY(100px) scale(0.7);
    filter: blur(20px);
  }
  25% {
    opacity: 0.8;
    filter: blur(10px);
  }
  50% {
    transform: perspective(1000px) rotateX(-5deg) translateY(-20px) scale(1.05);
    filter: blur(0);
  }
  75% {
    transform: perspective(1000px) rotateX(2deg) translateY(10px) scale(0.98);
  }
  90% {
    transform: perspective(1000px) rotateX(-1deg) translateY(-5px) scale(1.01);
  }
  100% {
    opacity: 1;
    transform: perspective(1000px) rotateX(0) translateY(0) scale(1);
  }
}

.epic-reveal {
  animation: epicReveal 3000ms cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
}
```

## Requirements

- **Skippable**: Always allow skip (tap/click/keypress)
- **Once per user**: Store preference, don't repeat
- **Reduced motion**: Provide instant alternative
- **Loading strategy**: Preload or progressive enhancement
- **Performance budget**: Dedicated optimization pass
- **Sound design**: Consider audio (with mute option)

## Production Considerations

- Storyboard before building
- Get stakeholder buy-in on duration
- Test on low-end devices
- Consider video fallback for complex sequences
- Budget 3-5x normal development time

## Key Insight

Dramatic animations are **mini-productions**. They require storyboarding, iteration, and polish. The payoff is brand differentiation and memorable experiences. Invest accordingly.
