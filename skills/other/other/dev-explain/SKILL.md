---
name: dev-explain
description: "Explain something in detail with investigation. No changes, no suggestions, no opinions. Facts and technical depth only. Usage: /dev-explain <topic>"
---

The user's topic is in the argument string passed to this skill. Investigate
and explain it.

If no argument was provided, ask the user what they want explained.

## Rules

1. **Explain with depth.** The user wants to understand how something works.
   Trace the full path: which functions are called, what data flows where,
   what the format looks like on disk, what the GPU receives. Include line
   numbers, struct layouts, byte offsets — the level of detail a programmer
   needs to modify the code confidently.

2. **Investigate.** Unlike `/dev-ask`, you should read files, follow call
   chains, check implementations, and verify claims against the actual code.
   The user expects you to do the legwork and report what you found.

3. **Do not make changes.** Do not edit files. Do not propose edits. Do not
   create branches. Do not commit. Read-only.

4. **Do not suggest.** No "you might want to," no "consider," no "it would
   be better to." The user asked how something works, not what to do about it.

5. **Do not apologize.** There is nothing to apologize for.

6. **Do not be defensive.** If something is broken, poorly designed, or
   missing, say so plainly. The user needs accurate information, not
   reassurance.

7. **Report what is, not what should be.** Describe the current state of the
   code. Do not editorialize about whether it is good or bad. Do not propose
   alternatives unless the user explicitly asks "what are the alternatives."

8. **No personality.** No greetings, no sign-offs, no emojis, no enthusiasm.
   Write like a technical reference document.

## Format

Start with a one-sentence summary of the answer. Then provide the detailed
explanation with code references, data flow, and supporting evidence. Use
headers to organize sections if the explanation covers multiple components.
Include file paths and line numbers for every claim about the code.

## Example invocation

```text
/dev-explain how the scene renderer handles transparent submeshes
```

Response:

`forge_scene_draw_model()` in `common/scene/forge_scene.h` splits submeshes
into two passes by alpha mode.

### Pass 1 — Opaque and MASK

Iterates all nodes. For each node with a mesh, iterates submeshes. If
`material.alpha_mode` is `OPAQUE` or `MASK`, draws immediately with
`SDL_DrawGPUIndexedPrimitives`. MASK materials bind the `shadow_mask`
pipeline which samples the base color texture and calls `clip(alpha -
cutoff)` in the fragment shader (`common/scene/shaders/shadow_mask.frag.hlsl:18`).
Depth writes are enabled.

### Pass 2 — BLEND

Submeshes with `alpha_mode == BLEND` are collected into a
`ForgeSceneTransparentDraw` array (max 256 entries). Each entry stores the
node index, submesh index, and a sort distance computed from the submesh's
precomputed object-space centroid transformed to world space via
`mat4_multiply_vec4(placement * node->world_transform, centroid)`. The
distance is `vec3_length(world_centroid - cam_position)`.

The array is sorted back-to-front with `SDL_qsort` using a float comparison.
Then each entry is drawn with the blend pipeline: `SRC_ALPHA /
ONE_MINUS_SRC_ALPHA`, depth test enabled, depth writes disabled.

Centroids are precomputed at model load time in
`forge_scene_load_model()` by averaging vertex positions per submesh.
