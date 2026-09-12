---
name: cmo-remotion
description: |
  Brand-grounded Remotion video pipeline. Take a brief, ground it in `brand/` (voice, audience, positioning, creative-kit), write a beat sheet, scaffold a fresh Remotion project, generate any required assets, compose with frame-driven animations, and bake a final MP4. Use this skill whenever the user wants to build a NEW Remotion video from scratch — product films, motion graphics, code-driven shaders, CRT/glitch effects, HTML-in-canvas demos, React video. Triggers on requests like "make a remotion video", CRT/glitch/scanline effects, html-in-canvas demos, video shaders, WebGL video, and frame-driven React video. This is the mktg-native sibling of the personal `/cmo-video` skill: `/cmo-video` recreates the *style* of an existing reference video; `/cmo-remotion` builds something new from a brief. Always load `remotion-best-practices` before stage 5 (compose).
category: creative
layer: orchestrator
tier: nice-to-have
reads:
  - brand/creative-kit.md
  - brand/voice-profile.md
  - brand/audience.md
  - brand/positioning.md
writes:
  - marketing/video/*/
  - marketing/handoffs/*-handoff.yaml
depends-on: []
triggers:
  - remotion video
  - make a remotion video
  - /cmo-remotion
  - build a remotion composition
  - video shader
  - react video
  - html in canvas video
  - CRT effect
  - glitch video
  - scanline effect
  - shader video
  - code-driven video
  - WebGL video
  - frame-driven animation
  - render an mp4 with react
  - remotion composition
  - new remotion project
review_interval_days: 30
version: 1.0.0
allowed-tools:
  - Bash(npx remotion *)
  - Bash(npx create-video *)
  - Bash(bunx remotion *)
  - Bash(ffmpeg *)
  - Bash(node *)
  - Bash(npm *)
  - Bash(bun *)
  - Bash(mktg status *)
---

# /cmo-remotion — Brand-Grounded Remotion Video Pipeline

The mktg-native end-to-end pipeline for **building a new Remotion video from a brief**. Brief in, MP4 out. Brand memory grounds it; `remotion-best-practices` powers the compose stage.

## North Star

The user wants a Remotion video that is *theirs* — voiced like their brand, aimed at their audience, hitting their positioning. They do not want a generic motion-graphics template, and they do not want to recreate someone else's video literally.

This skill is the Remotion equivalent of `/cmo-video`, with one key difference: `/cmo-video` is a *style transfer pipeline* — point it at a reference URL and it deconstructs the reference, generates fresh assets in that idiom, and ships a recreation. `/cmo-remotion` is a *brief-to-render pipeline* — start from a goal ("explain our product in 30s", "demo the CRT shader", "ad for our launch"), ground it in `brand/`, and ship.

You collaborate with the user across six stages, the same way `/cmo` collaborates across the marketing skill stack: suggest, ask one question at a time, push back when the brief is too big, and never silently advance. Show the beat sheet, get a yes, then scaffold. Show the asset list, get a yes, then generate. Show a single frame at composition midpoint, get a yes, then bake the full render.

## When to use (vs other video skills)

| User says | Route to | Why |
|---|---|---|
| "make a video like this <URL>" | personal `/cmo-video` | That pipeline is style-transfer from a reference. Stop after stage 2 if they only want the deconstruction. |
| "I have these PNG slides, make a video" | `/video-content` | Three-tier ffmpeg/Remotion pipeline that takes existing slides → video. No scaffold, no compose-from-scratch. |
| "make me a TikTok slideshow" | `/tiktok-slideshow` | Format-specific orchestrator that chains `/slideshow-script → /paper-marketing → /video-content`. |
| "build me a Remotion video about X" | **this skill** | New composition from a brief. Code-driven, frame-driven, brand-grounded. |
| "make a CRT shader / glitch / scanline video" | **this skill** | Stage 5 loads `remotion-best-practices/rules/html-in-canvas.md` and points you at the CRT template. |
| "edit my finished video" | Not this skill | Remotion is a video *generator*, not an editor. Use a real NLE for cuts on existing footage. |
| "transcribe / summarize this video" | `mktg transcribe` then `/summarize` | Different intent. |

## Workflow — the six stages

```
1. BRIEF       capture goal + audience + runtime + aspect + one-line takeaway
2. SCRIPT      beat sheet (scene · duration · voiceover · onscreen · visual · motion)
3. SCAFFOLD    npx create-video@latest --yes --blank --no-tailwind <slug>
4. ASSETS      generate PNGs via /codex:image or /image-gen → rembg → public/
5. COMPOSE     load remotion-best-practices, pick rule files by intent, build frame-driven
6. BAKE        single-frame midpoint check → npx remotion render → MP4
```

Each stage produces a checkpoint artifact under `marketing/video/<slug>/<n>-<stage>/`. The pipeline is **resumable** — read `pipeline.json`, pick a stage, continue. Never re-run a completed stage unless the user explicitly asks for "redo stage X".

### Stage 1 — BRIEF

Capture in one short conversation:

- **Goal.** "What's this video supposed to do?" (Drive signups, explain product, demo a feature, build authority, hype a launch.)
- **Audience.** "Who's watching?" If `brand/audience.md` is populated, propose the most relevant persona; ask if it's right.
- **Runtime.** Default to 8–15s for social, 30–90s for product film, ≤10s for shaders/loops. Push back on anything over 60s without a real reason.
- **Aspect ratio.** 1080×1920 vertical (TikTok/Reels), 1920×1080 horizontal (YouTube/landing page), 1080×1080 square. Default by goal.
- **One-sentence takeaway.** "If they only remember one thing, what is it?" If they can't say it in a sentence, the script is going to fail — slow down here.

If `brand/voice-profile.md`, `brand/positioning.md`, or `brand/creative-kit.md` are present, ground every brief decision in them. Quote the relevant line back: "Your voice profile says you avoid hype words — so the takeaway shouldn't lead with 'revolutionary'. How about 'the part of {X} no one shows you'?"

### Stage 2 — SCRIPT

A beat sheet is a table — one row per scene — with these columns:

| Scene | Duration | Voiceover (if any) | Onscreen text | Visual | Motion |
|-------|----------|---------------------|---------------|--------|--------|

The script is the **load-bearing stage**. A bad script makes a beautiful render boring. Co-write it: propose 2–3 beats, get a reaction, revise. Don't dump 8 beats in one shot.

Before approving, run the one-line gut check: *"If I read just the voiceover column out loud, does it tell the story?"* If not, rewrite.

### Stage 3 — SCAFFOLD

```bash
npx create-video@latest --yes --blank --no-tailwind <project-slug>
cd <project-slug>
npm install
```

Use `--blank` so we don't inherit the demo composition. Use `--no-tailwind` so the project stays minimal — Remotion has no inherent need for Tailwind, and the styles we author live alongside the components.

Project lives at `marketing/video/<slug>/project/`. Add `out/`, `node_modules/`, and any large generated assets to `.gitignore` if not already there.

### Stage 4 — ASSETS

If the video is **code-driven** (CRT shader, type-only, geometric) — skip this stage. The composition needs no PNGs.

Otherwise:
- Use `/codex:image` (preferred for craft-grade prompting) or `/image-gen` (Gemini Nano Banana 2 — model `gemini-3.1-flash-image-preview`, never older).
- Cap the asset count: ≤ 12 generated images for a single-scene 8s video, ≤ 8 per scene for multi-scene work. More than that and you're bloating cost and inviting style drift.
- Cut every transparent-background asset through `rembg`. Image models lie about transparency.
- Drop final assets into `<project>/public/`.

### Stage 5 — COMPOSE

**This stage is a prerequisite gate, not a reference.** Before you write the composition, load:

1. `marketing-cli/skills/remotion-best-practices/SKILL.md` — top-level entry to the rules.
2. The **specific** rule files that match your intent (pick what applies, don't load everything):

| Intent | Rule file |
|---|---|
| Code-driven shader / CRT / glitch | `rules/html-in-canvas.md` |
| Typewriter / animated text | `rules/text-animations.md` + `rules/assets/text-animations-typewriter.tsx` |
| Scene-to-scene cuts and crossfades | `rules/transitions.md` |
| Voiceover narration | `rules/voiceover.md` + `rules/audio.md` |
| Captions / subtitles | `rules/subtitles.md` + `rules/import-srt-captions.md` |
| Light leaks / film texture | `rules/light-leaks.md` |
| 3D / Three.js | `rules/3d.md` |
| Lottie | `rules/lottie.md` |
| Map embeds | `rules/mapbox.md` |
| Local fonts | `rules/local-fonts.md` |
| Google fonts | `rules/google-fonts.md` |

For the **CRT shader** intent specifically, copy the canonical drop-in: see [./templates/CRTComposition.tsx](./templates/CRTComposition.tsx).

Compose against the brand. Pull primary/secondary colors from `brand/creative-kit.md`. Match typography to the visual identity. The Remotion `<Composition>` is just the renderer — the grammar comes from the brand.

### Stage 6 — BAKE

Always render-then-inspect. Never trust the first render.

```bash
# Sanity check at composition midpoint (catches static layout bugs cheap)
npx remotion still <CompositionId> out/check.png --frame=<half-of-durationInFrames>

# Full render
npx remotion render <CompositionId> out/<name>.mp4

# WebGL effects (HtmlInCanvas, three.js, shader compositions) need ANGLE
npx remotion render --gl=angle <CompositionId> out/<name>.mp4
```

After the first render, sample frames at `0%, 12.5%, 37.5%, 62.5%, 90%` of duration with `npx remotion still`. Eyeball each. Fix what bugs the user. Re-render.

## Required Reading Before Stage 3

You must load these *before* you scaffold a Remotion project — they catch the framework-fighting mistakes early:

1. `/Users/moizibnyousaf/projects/mktgmono/marketing-cli/skills/remotion-best-practices/SKILL.md` — top-level entry.
2. The specific `rules/<topic>.md` file(s) matching your intent (the table in Stage 5 lists them).

If you skip this and "just start coding," you will end up writing CSS keyframes, you will hit "WebGL not enabled in render," and you will need to redo it. Loading the rules first costs ~30 seconds. Skipping costs ~30 minutes.

## Hard Principles (non-negotiable)

These are not preferences. Skipping them produces broken or low-quality videos.

1. **Frame-driven only.** `useCurrentFrame()` + `interpolate()` + `spring()`. Never CSS `@keyframes`, never Tailwind `animate-*` classes. CSS animations run on wall-clock time and render with all elements stuck at their starting opacity in the produced MP4.
2. **Render-then-inspect.** First render is never the final. Always sample at least 5 frames, eyeball each, fix the things that bug you, re-render.
3. **One-frame sanity check.** Before kicking off a full render of a long composition, render the midpoint frame as a still. If layout is broken there, full render is wasted.
4. **Brand-ground before composition.** Read `brand/creative-kit.md` and `brand/voice-profile.md` *before* you write the composition's TSX. Colors and tone are not afterthoughts.
5. **Load `remotion-best-practices` before stage 5.** Compose without the rules and you will fight the framework.
6. **Cap asset counts.** ≤ 12 PNGs per single-scene 8s video, ≤ 8 per scene multi-scene. More than that and you're inviting style drift across assets.
7. **WebGL needs `--gl=angle` on render.** HtmlInCanvas with WebGL2 in Studio works without it; CLI render does not.
8. **Never copy copyrighted footage.** This pipeline generates fresh assets — never extract video frames as final assets.

## Templates

The `templates/` directory ships drop-in components you can copy into a freshly scaffolded project.

| Template | What it is | When to use |
|---|---|---|
| [./templates/CRTComposition.tsx](./templates/CRTComposition.tsx) | Full HtmlInCanvas + WebGL2 fragment shader CRT effect over a typewriter terminal scene. ~10s, 1920×1080, 60fps. | The canonical example for code-driven shader videos. Demonstrates barrel distortion, scanlines, vignette, chromatic aberration, and frame-modulated intensity. |
| [./templates/Root.tsx](./templates/Root.tsx) | Remotion `<Composition>` registration for the CRT example. | Drop-in alongside `CRTComposition.tsx`. |
| [./templates/index.ts](./templates/index.ts) | `registerRoot(Root)` entry. | Replace the scaffolded `src/index.ts`. |
| [./templates/README.md](./templates/README.md) | How to copy these into a freshly scaffolded project, preview in Studio, and render. | Read once before using the templates. |

## Disambiguation

| User says | Route to | Why |
|---|---|---|
| "recreate this video" + URL | personal `/cmo-video` | Reference-driven style transfer pipeline. |
| "I have PNG slides, make a video" | `/video-content` | Three-tier slides-to-video pipeline. |
| "make me a TikTok slideshow" | `/tiktok-slideshow` | Format-specific orchestrator. |
| "ANY new Remotion video from a brief" | **this skill** | Brief-to-render. |
| "make a shader video" / "CRT effect" / "glitch" | **this skill** + load `html-in-canvas.md` + use the CRT template | Code-driven, no asset gen. |
| "render the existing project I already have" | **this skill, stage 6 only** | Skip stages 1–5; just the bake protocol. |
| "edit a finished MP4" | Not this skill | Remotion generates; doesn't edit. |

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Skipping stage 1 (BRIEF) and going straight to scaffold | The composition will lack a runtime/aspect/takeaway and you'll thrash on basic decisions inside Stage 5. The brief is 5 minutes of conversation, not bureaucracy. | Always capture goal · audience · runtime · aspect · one-sentence takeaway before scaffolding. |
| Skipping stage 2 (SCRIPT) | Without a beat sheet, the composition becomes a pretty slideshow in arbitrary order. Pacing collapses. The script also tells you what assets you actually need in stage 4. | Always produce the beat sheet *before* generating any asset or writing TSX. |
| Generating assets before the script is approved | You'll generate assets that don't match the final beat sheet and burn the budget. Cost discipline starts here. | Stage 4 reads from stage 3's beat sheet. Order matters. |
| Using CSS `@keyframes` or Tailwind `animate-*` classes inside Remotion | They run on wall-clock time, not composition frames. The video renders with elements stuck at `opacity: 0`. | Frame-driven only. `useCurrentFrame()` + `interpolate()` + `spring()`. See `remotion-best-practices/rules/`. |
| Trusting `/codex:image` / `/image-gen` PNGs to have transparent backgrounds | Image models lie about transparency. Even with explicit prompts, they bake in white or off-white backgrounds intermittently. | Always batch-cut every transparent asset through `rembg` before composition. |
| Rendering WebGL compositions without `--gl=angle` | The render runs but every WebGL effect renders as a blank canvas. You'll only notice after the full render finishes and you watch the MP4. | Always pass `--gl=angle` for any composition that uses HtmlInCanvas with WebGL, three.js, or any GPU shader. |
| Rendering the full composition before sampling stills | First render is almost never right. Layout bugs at the midpoint waste an entire render cycle. | Run a single-frame still at composition midpoint first. Then `npx remotion still` at 5 evenly-spaced frames. Then full render. |
| Loading every rule file in `remotion-best-practices/rules/` "just in case" | Context bloat. The 30+ rule files are an index, not a manifest. | Pick by intent. Shader → `html-in-canvas.md`. Type → `text-animations.md`. Voice → `voiceover.md`. The table in Stage 5 lists the mapping. |
| Composing without reading `brand/voice-profile.md` (when present) | The voiceover and onscreen text drift off-voice. Then the user has to ask you to "make it sound more like us" in stage 6. | Read the voice profile *before* writing the script. Quote it back to anchor the writing. |

## On Activation

1. **Run `mktg status --json`.** If `health: "needs-setup"`, route to `/mktg-setup` first — same as `/cmo`.
2. **Read brand/.** Detect which of `voice-profile.md`, `audience.md`, `positioning.md`, `creative-kit.md` exist and are non-template. Surface what's populated and what's missing.
3. **Verify prerequisites.** `node --version` ≥ 22, `npx --version` reachable. If the user's video uses voiceover, also confirm `mktg doctor` shows the voice provider (ElevenLabs).
4. **Walk the six stages.** Default to **interactive** — produce each stage's artifact, share it, ask "good?" before moving on. Pass `--auto` to run stages 1, 3, 4 unattended (script and compose always require approval — they're not cheap to redo).
5. **Tell the user where you are.** Every stage transition: one sentence describing what you produced, what's next, and where the artifact lives.

## Origin

This skill is the mktg-native counterpart to the personal-library `/cmo-video` skill. `/cmo-video` predates this one and is purpose-built for *recreating* a reference video. `/cmo-remotion` covers the larger case: building a new Remotion video from a brief, grounded in `brand/`. The two skills share philosophy (frame-driven only, render-then-inspect, conversation-not-pipeline) but split on the inception path.

The CRT template ships in v1 because it's the load-bearing demo for the HtmlInCanvas API — a code-driven, asset-free composition that proves out the WebGL render path end-to-end.
