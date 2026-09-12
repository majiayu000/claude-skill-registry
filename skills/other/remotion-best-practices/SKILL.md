---
name: remotion-best-practices
description: |
  Programmatic React video best practices for Remotion. Use this skill whenever the user is writing, debugging, or rendering Remotion code — compositions, useCurrentFrame animations, interpolate, spring, Sequence timing, <Img>/<Video>/<Audio> from @remotion/media, staticFile, calculateMetadata, the Studio preview, `npx remotion render`, captions, subtitles, voiceover, audio visualization, ffmpeg, transitions, light leaks, transparent video, Lottie, 3D scenes, Mapbox flyovers. Triggers especially on HtmlInCanvas / "html in canvas" requests, CRT terminal effects, glitch effects, video shaders, WebGL video, and any request to scaffold a new programmatic React video. Owns `remotion render` and everything about Remotion code. Do NOT trigger for finished MP4 ad assembly from existing slides (that is `/video-content`) or for the inspiration-to-MP4 reference-video pipeline (that is `/cmo-video`).
category: creative
layer: foundation
tier: nice-to-have
source: new
version: 1.0.0
review_interval_days: 30
reads:
  - brand/creative-kit.md
  - brand/voice-profile.md
  - brand/audience.md
  - brand/positioning.md
writes:
  - marketing/video/*/
depends-on: []
triggers:
  - remotion
  - useCurrentFrame
  - interpolate
  - spring
  - Sequence
  - AbsoluteFill
  - HtmlInCanvas
  - html in canvas
  - CRT effect
  - CRT terminal
  - glitch effect
  - video shader
  - WebGL video
  - react video
  - programmatic video
  - remotion render
  - npx create-video
  - npx remotion
  - bunx remotion
  - calculateMetadata
  - staticFile
  - "@remotion/media"
allowed-tools:
  - Bash(npx remotion *)
  - Bash(npx create-video *)
  - Bash(bunx remotion *)
  - Bash(ffmpeg *)
  - Bash(node *)
  - Bash(npm *)
  - Bash(bun *)
---

# Remotion Best Practices

Domain-specific knowledge for writing, animating, and rendering Remotion videos in React. Mirrored from the upstream `remotion-dev/skills` and `remotion-dev/remotion` `.claude` snapshots — see `upstream.json` for SHAs and `scripts/check-upstream.sh` for drift detection.

This is a **knowledge skill**. Other skills (`/cmo-remotion`, `/video-content`, `/tiktok-slideshow`) chain into it for the rules. Don't invoke it directly to render a video — invoke it to ground yourself before you touch composition code.

## On Activation

Read brand files in this order. Each is a soft input — every section below works at L0 with no brand at all:

1. `brand/creative-kit.md` — colors, typography, visual brand style. Drives palette, font choice, and the look of any composition you scaffold.
2. `brand/voice-profile.md` — tone, vocabulary. Drives any visible text (titles, captions, subtitle phrasing).
3. `brand/audience.md` — who watches. Drives pacing (tight cuts for B2C scroll feeds, longer holds for B2B explainers).
4. `brand/positioning.md` — what the video is selling. Drives narrative beats and CTA copy.

If any file is missing or template, fall back to neutral defaults: 1920×1080 @ 30fps, system font stack, 6-second hold per beat. Tell the user once: "Brand files thin — using neutral defaults. Run `/cmo` foundation to ground future videos."

## When to use

- User mentions Remotion, `useCurrentFrame`, `interpolate`, `spring`, `<Sequence>`, `<Composition>`, `staticFile`.
- User wants to scaffold a programmatic React video (`npx create-video@latest`).
- User wants HtmlInCanvas, CRT terminal, glitch, video shader, or WebGL post-processing.
- User is debugging captions, subtitles, voiceover, audio visualization, or ffmpeg-piped Remotion work.
- User is rendering with `npx remotion render` and hitting WebGL / GPU / fps issues.

Do **not** use for: assembling a finished MP4 from existing slide PNGs (`/video-content`), inspiration-to-MP4 from a reference URL (`/cmo-video`), or TikTok slideshow chains (`/tiktok-slideshow`).

## Hard Rules

These are non-negotiable. Violating them produces black frames, stuttered playback, or render failures.

| Rule | Why |
|---|---|
| **CSS transitions / `@keyframes` are FORBIDDEN.** | Remotion renders frame-by-frame. CSS animations are time-based and will not advance during a still or video render. |
| **Tailwind animation classes (`animate-*`) are FORBIDDEN.** | Same reason — they compile to CSS animations. Tailwind for layout/colors is fine; Tailwind for motion is broken. |
| **Drive every motion off `useCurrentFrame()` + `interpolate()` or `spring()`.** | Frame is the only source of truth Remotion can serialize across the render worker pool. |
| **Use `<Img>`, `<Video>`, `<Audio>` from `@remotion/media`** — never native `<img>` / `<video>` / `<audio>`. | Native elements don't participate in Remotion's frame-locking, so video frames desync from the timeline and audio drifts. |
| **Reference public assets via `staticFile("path")`** — never hardcoded `/path` or `./path`. | `staticFile` resolves correctly in Studio, in the renderer, and in deployed Lambda functions. Hardcoded paths break in Lambda. |
| **Render-then-inspect.** | A composition that looks right in Studio can still ship broken frames. Render a still or short clip and look at it before declaring done. |
| **One-frame sanity check before any long render.** | `npx remotion still <id> --frame=30 --scale=0.25` is ~2 seconds. Catches missing assets, font fallbacks, layout overflow, and Tailwind misconfigs before you burn 20 minutes on a 30-second render. |

## New project setup

When in an empty folder or a workspace with no existing Remotion project:

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video
npx remotion studio
```

Flags:
- `--yes` — skip the interactive prompt.
- `--blank` — minimal scaffold, no demo composition.
- `--no-tailwind` — Tailwind ships with `animate-*` utilities that will tempt the next agent to use forbidden CSS animations. Skip it. Add Tailwind later only if you need its layout utilities and you're disciplined about animation.

For mktg projects, scaffold under `marketing/video/<name>/` so renders land alongside the rest of the marketing artifacts.

## Rule Index — load on demand

The full rule corpus lives in `rules/`. Load only what you need for the current task — don't preload everything.

### Animation core
- [rules/timing.md](rules/timing.md) — `interpolate` ranges, Bézier easing, `spring()` configuration.
- [rules/sequencing.md](rules/sequencing.md) — `<Sequence from>` / `durationInFrames`, layout="none" for inline content.
- [rules/transitions.md](rules/transitions.md) — `<TransitionSeries>` for scene-to-scene transitions.
- [rules/trimming.md](rules/trimming.md) — cutting the head or tail of an animation cleanly.
- [rules/text-animations.md](rules/text-animations.md) — typography motion patterns.

### Effects
- [rules/html-in-canvas.md](rules/html-in-canvas.md) — `<HtmlInCanvas>` for 2D/WebGL post-processing of DOM. **The user-asked feature.** See dedicated section below.
- [rules/light-leaks.md](rules/light-leaks.md) — `@remotion/light-leaks` overlays.
- [rules/transparent-videos.md](rules/transparent-videos.md) — alpha-channel render output.
- [rules/lottie.md](rules/lottie.md) — embedded Lottie JSON animations.

### Audio & narration
- [rules/audio.md](rules/audio.md) — trimming, volume curves, speed, pitch.
- [rules/voiceover.md](rules/voiceover.md) — ElevenLabs TTS into a Remotion composition.
- [rules/sfx.md](rules/sfx.md) — sound effects, layering.
- [rules/audio-visualization.md](rules/audio-visualization.md) — spectrum bars, waveforms, bass-reactive visuals.
- [rules/get-audio-duration.md](rules/get-audio-duration.md) — Mediabunny audio duration.
- [rules/silence-detection.md](rules/silence-detection.md) — auto-trim silent segments via ffmpeg.

### Captions & subtitles
- [rules/subtitles.md](rules/subtitles.md) — basic subtitle rendering.
- [rules/display-captions.md](rules/display-captions.md) — caption styling and positioning.
- [rules/import-srt-captions.md](rules/import-srt-captions.md) — load `.srt` files into a composition.
- [rules/transcribe-captions.md](rules/transcribe-captions.md) — whisper-style transcription into captions.

### Media handling
- [rules/images.md](rules/images.md) — sizing, dynamic paths, dimension queries.
- [rules/videos.md](rules/videos.md) — embedding videos with trimming, volume, speed, looping.
- [rules/gifs.md](rules/gifs.md) — GIFs synchronized to the Remotion timeline.
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) — Mediabunny dimensions.
- [rules/get-video-duration.md](rules/get-video-duration.md) — Mediabunny duration.
- [rules/ffmpeg.md](rules/ffmpeg.md) — pipeline-side video operations (encoding, format conversion, trimming).

### Composition & metadata
- [rules/compositions.md](rules/compositions.md) — stills, folders, default props, nested compositions.
- [rules/calculate-metadata.md](rules/calculate-metadata.md) — dynamic `durationInFrames` / dimensions / props from async data.
- [rules/parameters.md](rules/parameters.md) — Zod schemas for parametrizable compositions.

### Typography
- [rules/google-fonts.md](rules/google-fonts.md) — recommended font path. Use this first.
- [rules/local-fonts.md](rules/local-fonts.md) — fallback when a font isn't on Google Fonts.
- [rules/measuring-text.md](rules/measuring-text.md) — fitting text to containers, overflow detection.
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) — measure rendered DOM dimensions.

### Specialty
- [rules/3d.md](rules/3d.md) — Three.js / React Three Fiber inside Remotion.
- [rules/mapbox.md](rules/mapbox.md) — animated Mapbox flyovers (use static images for trivial maps).
- [rules/tailwind.md](rules/tailwind.md) — Tailwind setup notes if you must use it. Animation classes still forbidden.

## Composition shape

The canonical frame-driven fade-in. Memorize this shape — every other animation is a variation.

```tsx
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const FadeIn: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ opacity, fontSize: 120 }}>Hello</h1>
    </AbsoluteFill>
  );
};
```

Width / height / fps / duration belong on the `<Composition>` in `src/Root.tsx`. For dynamic durations (e.g., audio-driven length), use `calculateMetadata` — see [rules/calculate-metadata.md](rules/calculate-metadata.md).

## Render pipeline

```bash
# Preview interactively
npx remotion studio

# One-frame sanity check (always do this first)
npx remotion still MyComposition --frame=30 --scale=0.25 --output=out/check.png

# Full render
npx remotion render MyComposition out/video.mp4

# WebGL effects (HtmlInCanvas + WebGL, shaders, Three.js)
npx remotion render MyComposition out/video.mp4 --gl=angle
```

Set `--gl=angle` as the default in `remotion.config.ts` once a project uses WebGL anywhere — it avoids "blank frames in render but fine in Studio" surprises.

```ts
import { Config } from "@remotion/cli/config";
Config.setChromiumOpenGlRenderer("angle");
```

## HtmlInCanvas — the user-asked feature

`<HtmlInCanvas>` renders DOM children into a `<canvas>` so you can post-process them with the Canvas 2D API or WebGL. This is how you build CRT terminals, glitch effects, video shaders, and other "DOM but with a filter on top" looks.

**Constraints:**
- Chrome 149+ with `chrome://flags/#canvas-draw-element` enabled. Tell the user this once.
- Non-Chromium machines cannot render — flag it before starting work.
- Do NOT nest `<HtmlInCanvas>` inside another `<HtmlInCanvas>`. Remotion throws.
- Use `--gl=angle` whenever the inner effect uses WebGL.

**Working 2D blur example** (frame-driven blur radius via `onPaint`):

```tsx
import {
  AbsoluteFill,
  HtmlInCanvas,
  type HtmlInCanvasOnPaint,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useCallback } from "react";

export const Blur: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const onPaint: HtmlInCanvasOnPaint = useCallback(
    ({ canvas, element, elementImage }) => {
      const ctx = canvas.getContext("2d");
      if (!ctx) throw new Error("Failed to acquire 2D context");

      const blurPx = 4 + 18 * (0.5 + 0.5 * Math.sin((frame / fps) * Math.PI));

      ctx.reset();
      ctx.filter = `blur(${blurPx}px)`;
      const transform = ctx.drawElementImage(elementImage, 0, 0);
      element.style.transform = transform.toString();
    },
    [frame, fps],
  );

  return (
    <HtmlInCanvas width={width} height={height} onPaint={onPaint}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", fontSize: 120 }}>
        <h1>Hello</h1>
      </AbsoluteFill>
    </HtmlInCanvas>
  );
};
```

For the full WebGL pattern (texture upload via `gl.texElementImage2D`, shader programs, async multi-pass), see [rules/html-in-canvas.md](rules/html-in-canvas.md).

For a complete CRT terminal scene with scanlines, phosphor glow, and chromatic aberration, see the `/cmo-remotion` skill's `templates/CRTComposition.tsx`.

## Anti-Patterns

| Anti-pattern | Instead | Why |
|---|---|---|
| `@keyframes` or CSS `transition` | `interpolate(frame, ...)` | CSS animations are wall-clock; render workers freeze frames mid-animation and produce stutters or static stills. |
| Tailwind `animate-pulse` / `animate-bounce` / etc. | Spring or interpolate driven by frame | Same root cause — Tailwind compiles motion utilities to CSS animations. |
| `<img src="...">` / native `<video>` / native `<audio>` | `<Img>` / `<Video>` / `<Audio>` from `@remotion/media` | Native elements don't sync to Remotion's frame clock. Video desyncs and audio drifts. |
| Hardcoded `/logo.png` or `./assets/x.png` | `staticFile("logo.png")` from `public/` | Hardcoded paths break in Lambda renders and can break in Studio depending on dev-server config. |
| Skipping the one-frame `still` check | `npx remotion still <id> --frame=30 --scale=0.25` first | Catches missing fonts, broken paths, overflow in 2 seconds instead of 20-minute renders. |
| Nesting `<HtmlInCanvas>` inside `<HtmlInCanvas>` | Merge effects into one outer canvas | Chrome only honors the outermost effect; Remotion throws an explicit error. |
| WebGL effects rendered without `--gl=angle` | Add `--gl=angle` to render and `Config.setChromiumOpenGlRenderer("angle")` to config | Default GL backend silently produces blank frames in headless renders; ANGLE is required for parity with Studio. |
| Running on a non-Chromium machine for HtmlInCanvas work | Flag the constraint before starting; render on a Chrome 149+ host | Firefox / Safari engines can't enable `canvas-draw-element`; render will fail with no signal. |
| Reading the rule index for files you don't need | Load just the rule files relevant to the current task | The rule corpus is large — preloading wastes context budget that should go to brand files and the actual composition. |

## Checking for upstream updates

This skill mirrors content from `remotion-dev/skills` (primary) and `remotion-dev/remotion` `.claude` (secondary). To check for drift:

```bash
./skills/remotion-best-practices/scripts/check-upstream.sh
```

The script compares pinned SHAs in `upstream.json` against the latest commits in both upstream repos and reports added/changed rule files. Owned by ironmint — do not edit `upstream.json` or `scripts/` from this skill.

## How this composes

Three sibling skills overlap. Pick the right entry point — they are not interchangeable.

| Skill | Use when | Inputs | Output |
|---|---|---|---|
| `remotion-best-practices` | You are writing or debugging Remotion code itself. Domain knowledge only. | Composition source, rendering question | Guidance + rule pointers |
| `/cmo-remotion` | You want a polished programmatic video built end-to-end with mktg brand context. | Brief, brand files | Scaffolded composition + render |
| `/video-content` | You already have slide PNGs and want them assembled into an MP4 (ffmpeg or Remotion tier). | PNG slides, audio | Finished MP4 |
| `/tiktok-slideshow` | You want the full pipeline from positioning angle to TikTok-ready video. | Positioning angle | Script → slides → video |

`remotion-best-practices` is the **shared knowledge layer** under `/cmo-remotion` and `/video-content` (Remotion tier). Skills do not call it directly — they chain in the rules they need by file path.

## Attribution

Mirrored from:
- **Primary:** [remotion-dev/skills](https://github.com/remotion-dev/skills) — `skills/remotion/SKILL.md` and the full `skills/remotion/rules/` tree (35 files).
- **Secondary:** [remotion-dev/remotion](https://github.com/remotion-dev/remotion) — `.claude/` patterns referenced in `references/upstream-internal/MAP.md`.

Snapshot SHAs and pinned tags live in `upstream.json`. Curated and adapted via `/mktg-steal` on 2026-05-04.

Credit to **@JonnyBurger** and the Remotion contributors. Upstream is MIT-licensed; see each upstream repo for the canonical license text. The mktg adaptation only changes the entry-point SKILL.md (this file) and adds provenance scaffolding — the rule corpus is mirrored verbatim.
