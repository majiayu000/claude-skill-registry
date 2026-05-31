---
name: remotion-transitions
description: This skill should be used when the user asks to create custom Remotion transitions, asks about "cool transitions", "cinematic transitions", "striped transitions", "glitch transitions", "custom TransitionPresentation", or wants to build scene-to-scene transitions in Remotion beyond the built-in library. Also triggers for "how to make transitions in Remotion", "custom transition", "high-energy transitions", "energy transitions", "branded transitions".
version: 1.0.0
---

# Remotion Custom Transitions

This skill teaches you how to build **production-grade, high-energy custom transitions** in Remotion using the `TransitionPresentation` API — the same pattern used in Fyltr's Instagram Reel campaign.

## Quick Reference

- [Custom Transition Pattern](./references/custom-transition-pattern.md) — The `TransitionPresentation` API, the exact component shape, and how timing works
- [Transition Catalog](./references/transition-catalog.md) — 6 battle-tested transitions with full source: Striped Slam, Zoom Punch, Diagonal Reveal, Emerald Burst, Vertical Shutter, Glitch Slam
- [Animation Math](./references/animation-math.md) — Easing functions, stagger formulas, spring configs, and the `clamp` extrapolation pattern used throughout

## Core Concept

Remotion's `@remotion/transitions` package exposes a `TransitionPresentation` type. You implement a **component** that receives:
- `presentationProgress` — `0` at transition start → `1` at transition end
- `presentationDirection` — `"exiting"` (old scene) or `"entering"` (new scene)
- `children` — the scene being wrapped

The same component wraps **both** scenes simultaneously. You animate different things depending on direction.

## Golden Rules

1. **Never use CSS transitions/animations** — all motion via `interpolate()` / `spring()` driven by `presentationProgress`
2. **Never use `useCurrentFrame()`** inside a transition component — use `presentationProgress` only
3. Always return `{ component, props: {} }` — the `props` object must exist even if empty
4. **Create instances outside components** at module level to keep them stable across re-renders
5. Pair with `linearTiming` (for dramatic frame-perfect transitions) or `springTiming` (for springy physics)

## When to Load References

- Building a new custom transition → load [custom-transition-pattern.md](./references/custom-transition-pattern.md) first
- Copying/adapting an existing effect → load [transition-catalog.md](./references/transition-catalog.md)
- Debugging timing or easing math → load [animation-math.md](./references/animation-math.md)
