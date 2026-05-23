---
name: remotion-video
description: Build and render Remotion videos using React compositions. Use when defining `<Composition>` entries (often in `src/Root.tsx`), implementing deterministic frame-based animations with `useCurrentFrame()`, sequencing (`Sequence`/`Series`/`TransitionSeries`), and adding media via `OffthreadVideo`, `Img`, `Audio`, and `staticFile()`.
---

# Remotion Video (React)

## Instructions

1. Define one or more compositions (commonly in `src/Root.tsx`).
   - Use defaults unless specified otherwise: `fps={30}`, `width={1920}`, `height={1080}`, and composition `id="MyComp"`.
   - Ensure `defaultProps` matches the React component props shape and is JSON-serializable.

2. Implement video components as deterministic, frame-driven React.
   - Drive animations from `useCurrentFrame()` and `useVideoConfig()`.
   - Avoid `Math.random()`; use Remotion’s `random(seed)`.
   - Avoid interactive UI patterns (no click handlers / hover state). Prefer pure functions of `frame` + props.

3. Use the right primitives for timing, layering, and animation.
   - Layer elements with `AbsoluteFill`.
   - Time-shift mounts with `Sequence` and play back-to-back with `Series`.
   - For transitions between clips, use `TransitionSeries` from `@remotion/transitions`.
   - Use `interpolate()` (usually with `{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}`) and/or `spring()` for motion.

4. Use the correct media tags.
   - Video: prefer `<OffthreadVideo>`.
   - Images: use `<Img>`.
   - GIFs: use `<Gif>` from `@remotion/gif`.
   - Audio: use `<Audio>`.
   - For local assets in `public/`, use `staticFile('...')`.

5. Preview and render.
   - Start Studio: `npx remotion studio` (alias: `npx remotion preview`).
   - Render: `npx remotion render <composition-id> <output-path>` (if you omit the ID, Remotion will prompt).

6. When unsure, read the bundled references.
   - Detailed patterns/snippets: `references/remotion-notes.md`
   - CLI notes: `references/remotion-cli.md`
   - Media notes: `references/remotion-media.md`

## Examples

### Minimal composition + frame-based component

See `references/remotion-notes.md` for the canonical `src/Root.tsx` + `MyComp` snippets.
