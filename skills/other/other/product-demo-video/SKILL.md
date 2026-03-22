---
name: product-demo-video
description: Create polished programmatic product demo videos from software projects using a bundled Remotion template, storyboard generation, and TTS narration. Use when Codex needs to turn an app, library, CLI, or API into a demo video without screen recording, or when iterating on storyboard scenes, narration, or renders.
---

# Product Demo Video

This is the Codex-skill port of the Claude plugin. There is no slash command, so Codex should drive the workflow explicitly and use the bundled Remotion template under `assets/remotion-template/`.

## Template Setup

- If the target workspace does not already contain a Remotion project, copy `assets/remotion-template/` into a working directory such as `demo-video/`.
- Run `npm install` in that working directory.
- The template includes scene components, entrypoints, a narration script, and a starter `src/storyboard.ts`.

## Workflow

1. Scan the target project README, docs, manifests, source tree, and any existing screenshots.
2. Ask which features to highlight, preferred length, tone, brand color, and whether specific screenshots should be used.
3. Draft a storyboard using `references/scene-catalog.md`.
4. Show the storyboard for approval unless the user explicitly asks to skip that checkpoint.
5. Write or update `src/storyboard.ts`.
6. Generate narration MP3s into `public/narration/` by calling `scripts/generate-narration.sh` once per scene from a small helper script.
7. If `ffprobe` is available, measure each MP3 and set `durationInSeconds` to audio length plus roughly 0.8 seconds.
8. Preview with `npx remotion studio` and render with `npx remotion render DemoVideo output/demo.mp4`.

## Storyboard Rules

- Always start with `intro` and end with `outro`.
- Keep most scenes around 8 to 12 seconds.
- Include at least one clearly animated scene such as `workflow`, `comparison`, or a dynamic `feature`.
- Use real code and concrete product details from the target project.
- Keep narration in spoken language, roughly 120 to 150 words per minute.

## Notes

- The bundled TTS script supports macOS `say`, OpenAI TTS, and ElevenLabs.
- If the user already has a Remotion project, copy only the needed components, `src/storyboard.ts`, or the narration script instead of the entire template.
