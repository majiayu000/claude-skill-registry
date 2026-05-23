---
name: dynamic-res-scaler
description: Implement dynamic resolution scaling for React Three Fiber / Three.js by adjusting DPR based on measured FPS. Use when asked to add adaptive performance scaling, automatic DPR tuning, or a DynamicResScaler-style component in a R3F scene.
---

# Dynamic Res Scaler

## Overview

Implement a small R3F component that monitors frame rate and adjusts device pixel ratio (DPR) at runtime to balance visual quality and performance.

## Workflow

1. Locate the main `Canvas` and decide where to mount the scaler (typically near the root of the scene so it always runs).
2. Create or update a `DynamicResScaler` component using `useFrame` + `useThree`.
3. Track FPS over a short interval using refs (avoid state to prevent re-renders).
4. Adjust DPR in small steps within min/max bounds and call `setDpr` only when it changes.
5. Mount the component inside the `Canvas` and verify behavior in dev builds.

## Tuning Guidelines

- **TARGET_FPS / FPS_TOLERANCE**: adjust how aggressively the scaler reacts (e.g., 60 ± 5).
- **CHECK_INTERVAL**: 300–700ms keeps changes responsive without thrashing.
- **STEP**: 0.05–0.15 is typical; smaller steps reduce visible jumps.
- **MIN_DPR / MAX_DPR**: clamp to protect performance; cap MAX_DPR to devicePixelRatio or 2.

## Resources

Use `references/dynamic-res-scaler.md` for the drop-in implementation and configuration notes based on `DynamicResScaler.tsx`.
