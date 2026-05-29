---
name: route-builder
description: Generates route specifications with distance and elevation constraints. Use when user asks for route suggestions, wants to explore new running paths, or needs safer surface recommendations for upcoming workouts.
metadata:
  short-description: Builds runnable routes with safety constraints and map-ready specs.
---

## When Claude should use this skill
- When the user requests a new route for a target distance/time
- During plan creation if a route is missing for an upcoming workout
- When user wants route exploration or safer surface options

## Invocation guidance
1. Provide target distance/time, surfaces, elevation preferences, and start location/constraints.
2. Return route spec with segments, elevation notes, and safety considerations.
3. Ensure output is compatible with `v0/lib/routeHelpers.ts` and `mapConfig.ts`.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- UI: Route selector modal; map layer in `v0/lib/mapConfig.ts`.
- API: `v0/app/api/route/build` (new) backed by existing mapping helpers.

## Safety & guardrails
- Exclude unsafe surfaces if flagged; avoid steep grades for beginners.
- If location data missing, request clarification and emit `SafetyFlag: missing_data`.
- No medical advice; suggest shorter routes if heat/injury risk.

## Telemetry
- Emit `ai_skill_invoked` with `distance`, `surface`, `safety_flags`.
