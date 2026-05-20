---
name: design-interaction-motion-craft
description: Use when designing or reviewing transitions, gestures, and state-change motion across web, mobile, and desktop interfaces.
---

# Interaction Motion Craft

## Overview

Apply interaction and animation craft as a behavior system, not decoration. Motion must communicate causality, preserve context, and stay interruptible under real usage frequency.

## Mandatory Use Cases

- Navigation transitions, modal/sheet presentations, list reordering, drag/gesture UI.
- Loading/skeleton/progress states, success/error confirmation, hover/focus feedback.
- Any request containing animation polish, interaction feel, delight, fluidity, snappiness.

## Workflow (Required)

1. Define event chain: `trigger -> transition -> resulting state`.
2. Declare intent per motion segment: orient, emphasize, confirm, warn, or defer.
3. Decide coupling: real-time (`during gesture`) vs commit-time (`on release`).
4. Select principle set (below) and reject non-functional animation.
5. Validate interruptibility, reduced-motion behavior, and performance budget.

## Core Interaction Rules

- Motion must explain what changed and why.
- Gesture-linked feedback should start immediately and follow input direction/velocity.
- Prefer reversible transitions; avoid locking users into long non-interruptible sequences.
- Maintain object constancy: source and destination should be visually traceable.
- Repetition penalty: high-frequency interactions require subtle motion; novelty decays fast.
- System coherence: one motion language across product (easing, duration, spatial direction).
- Keep gesture semantics stable across surfaces (same gesture family, same intent class).
- Avoid threshold-only dead zones: show coupled response from first movement, then apply thresholded commit logic.

## Timing + Frequency Budget

- Interaction response onset: immediate perceptual feedback (target <=100ms).
- Micro interactions: typically 120-220ms.
- Structural transitions (screen/sheet/context shifts): typically 220-450ms.
- Repeated interactions (tab change, like, toggle): stay on the lower end.
- One-time onboarding/celebratory moments: may run longer if skippable and rare.

## Frequency x Novelty Matrix (Required)
→ *Consult [full interaction article reference](references/rauno-interaction-design.md) for rationale and boundary cases.*

- High frequency + low novelty: optimize for speed, predictability, and low cognitive load.
- High frequency + high novelty: reject by default; allow only with measured task benefit.
- Low frequency + low novelty: acceptable utility baseline.
- Low frequency + high novelty: reserve for signature moments, onboarding, or milestone feedback.

## Risk-Based Trigger Timing

- Reversible/continuous interactions: allow `during gesture` updates.
- Irreversible/high-impact actions: prefer commit-time transitions plus explicit confirmation states.
- If accidental activation cost is high, bias toward staging and clarity over expressiveness.

## Touch Ergonomics + Occlusion

- Ensure finger/pointer does not hide critical feedback during manipulation.
- For precision handles/sliders, preserve control continuity when touch exits narrow hit areas.
- Use temporary reveal/magnification patterns if direct-touch obscures target detail.

## 12 Animation Principles -> UI Translation

- `Squash/Stretch`: communicate state elasticity (press, drag resistance) without breaking readability.
- `Anticipation`: pre-cue significant movement (small pre-motion before large change).
- `Staging`: isolate primary action; suppress competing motion.
- `Straight Ahead/Pose-to-Pose`: key-state-first for UI transitions; avoid uncontrolled frame drift.
- `Follow-through/Overlap`: secondary elements settle after primary object for realism.
- `Slow In/Out`: ease-in/ease-out for natural acceleration curves.
- `Arcs`: prefer curved trajectories for floating objects and gesture-driven movement.
- `Secondary Action`: add supportive detail only if primary action remains clear.
- `Timing`: duration communicates weight/importance.
- `Exaggeration`: use sparingly for feedback clarity, not spectacle.
- `Solid Drawing`: preserve believable volume/depth cues in 2D/3D transforms.
- `Appeal`: motion style aligned with brand/product character.

## Failure Modes (Blockers)

- Delayed response after input (UI feels disconnected).
- Decorative motion with no semantic payload.
- Mismatched easing/duration across components.
- Uninterruptible long transitions.
- Motion that obscures hierarchy or causes tracking loss.
- No reduced-motion fallback.
- High-frequency workflows depend on novelty-heavy motion for baseline usability.
- Gesture commits without clear intent confidence in high-risk actions.

## Output Contract

- For implementation tasks: include `intent map`, selected principles, and timing rationale.
- For reviews: list failures by severity and provide direct remediation.
- Always state reduced-motion handling.

## Related Skills

- `design-audit` - objective sign-off gates for complete design quality.
- `design` - high-fidelity frontend implementation once motion rules are set.

## Source Basis

- https://rauno.me/craft/interaction-design
- https://www.userinterface.wiki/12-principles-of-animation
- references/rauno-interaction-design.md
