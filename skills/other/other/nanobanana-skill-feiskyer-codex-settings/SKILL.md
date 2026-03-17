---
name: nanobanana-skill
description: Generate, remix, or edit images with Nanobanana / Nano Banana 2 through the bundled Gemini CLI wrapper. Use this whenever the user wants AI image generation or editing, especially for reference-image composition, character consistency, grounded visuals that may need live web search, style transfer, marketing graphics, product mockups, social assets, or when they explicitly mention Nanobanana, Gemini image models, Google image generation, AI drawing, 图片生成, AI绘图, 图片编辑, or 生成图片.
---

# Nanobanana Image Skill

Use the bundled `nanobanana.py` tool to generate or edit images with Gemini image models. The default path now targets **Nano Banana 2** (`gemini-3.1-flash-image-preview`) and turns on **thinking summaries** plus **Google Search grounding** by default, because those defaults are the main reason to use this skill instead of a generic image prompt.

## When to use this skill

Use it for:

1. Creating a new image from text
2. Editing or remixing one or more existing images
3. Combining several reference images into one composition
4. Requests where factual freshness matters and image grounding should use live web data
5. Requests that need strong text rendering, layout reasoning, or more deliberate composition

Do not use it for:

1. Non-image tasks
2. Image work that explicitly must use another provider or another installed image skill

## Requirements

1. `GEMINI_API_KEY` must exist in `~/.nanobanana.env` or the shell environment.
2. Python dependencies from `requirements.txt` must be installed.
3. The executable is the `nanobanana.py` file in this same skill directory. Resolve its absolute path once before running it.

Example env file:

```bash
GEMINI_API_KEY=sk-dummy
```

## Default behavior

Unless the user explicitly asks otherwise, prefer these defaults:

1. Model: `gemini-3.1-flash-image-preview`
2. Search grounding: enabled
3. Thinking summaries: enabled
4. Thinking level: `high`
5. Resolution: `1K`
6. Aspect ratio: leave unspecified unless the user clearly wants a shape

Leaving aspect ratio unspecified is usually better for edits because Gemini can match the input image shape. For text-only generation, pick an aspect ratio only when the user implies a format such as poster, square post, banner, phone wallpaper, or ultrawide hero image.

## Workflow

### 1. Clarify only the missing constraints

Ask only for details that materially affect the result:

1. The image brief or editing instruction
2. Any input/reference images to use
3. Target format or aspect ratio if implied by the use case
4. Output filename if the user cares where it lands

Do not force the user to choose a model, search mode, or thinking mode unless they asked for that level of control. The latest Nanobanana 2 path is already the default.

### 2. Choose the right mode

Use **generate** when there are no input images.

Use **edit/composite** when there are one or more input images. Nanobanana 2 can mix multiple references, so do not artificially limit the task to a single image if the user is clearly asking for a blend, lineup, storyboard, or consistency pass.

### 3. Run the bundled tool

Use the script beside this skill file.

Basic generation:

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Create a high-end coffee bag package design with tactile paper texture and clear typography" \
  --output /absolute/path/to/output/package.png
```

Editing or compositing:

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Turn these product photos into a clean 4:5 ecommerce hero image with a soft studio shadow and subtle headline area" \
  --input /absolute/path/to/ref1.png /absolute/path/to/ref2.png \
  --aspect-ratio 4:5 \
  --output /absolute/path/to/output/hero.png
```

Grounded generation with saved text metadata:

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Use Google Search to ground an editorial illustration about the most recent lunar mission and create a clean magazine cover concept" \
  --aspect-ratio 2:3 \
  --text-output /absolute/path/to/output/cover.txt \
  --metadata-output /absolute/path/to/output/cover.json \
  --output /absolute/path/to/output/cover.png
```

### 4. Return the result clearly

Always tell the user:

1. The saved image path or paths
2. Whether search grounding stayed enabled
3. Whether text/thought summaries were saved anywhere
4. Any relevant limitation or warning from the run

If the model returns text but no image, report that plainly and suggest a more explicit image-focused prompt instead of pretending the run succeeded.

## Recommended options

### Models

1. `gemini-3.1-flash-image-preview`: default. Best default for fast, high-volume image generation and editing with Nanobanana 2 features.
2. `gemini-3-pro-image-preview`: slower, but a good override for very detail-heavy or typography-sensitive work.
3. `gemini-2.5-flash-image`: legacy fallback if the user specifically wants the older Nanobanana model.

### Aspect ratios

Supported ratios:

1. `1:1`
2. `1:4`
3. `1:8`
4. `2:3`
5. `3:2`
6. `3:4`
7. `4:1`
8. `4:3`
9. `4:5`
10. `5:4`
11. `8:1`
12. `9:16`
13. `16:9`
14. `21:9`

Quick picks:

1. `1:1` for logos, icons, thumbnails, and general social posts
2. `4:5` for feed posts and product cards
3. `2:3` for posters and book-cover style work
4. `9:16` for stories, shorts, and phone wallpaper
5. `16:9` or `21:9` for slides, banners, and desktop hero art
6. `1:4`, `4:1`, `1:8`, `8:1` for very tall or very wide experimental layouts now supported by Nanobanana 2

### Resolution

1. `512px`: Nanobanana 2 only. Best for quick ideation.
2. `1K`: default. Good tradeoff for most requests.
3. `2K`: use for polished deliverables.
4. `4K`: use when the user explicitly needs a high-resolution final.

### Thinking and search

1. Keep search grounding on by default when the request could benefit from live facts, current events, or real product references.
2. Keep thinking summaries on by default because Nanobanana 2 often composes better on multi-constraint tasks.
3. Lower `--thinking-level` to `low` or `minimal` when the user prioritizes latency over refinement.
4. Disable search only when the user wants a purely imaginative result or explicitly requests no web grounding.

## Prompting guidance

Good Nanobanana prompts are direct production briefs, not vague art wishes. Include:

1. Subject
2. Visual style
3. Composition or camera framing
4. Required text if any
5. Output use case
6. Constraints such as brand colors, empty space, or realism level

Prefer prompts like:

```text
Create a premium sparkling water can advertisement. Use a cold studio product-photo look, silver highlights, condensation droplets, and a clean dark-teal background. Leave negative space in the upper-right for headline copy.
```

Instead of:

```text
make a cool drink ad
```

For edits, tell the model what to preserve and what to change:

```text
Keep the shoe silhouette and logo placement intact. Replace the background with a bright outdoor basketball court, add dynamic afternoon shadows, and keep the image looking like a real sports campaign photo.
```

## Nanobanana 2 capabilities to lean on

1. Multi-reference composition with many input images
2. Better grounded visuals with Google Search and Google Image Search support behind the built-in search tool
3. Wider aspect-ratio support, including very tall and very wide outputs
4. `512px` fast ideation output in addition to `1K`, `2K`, and `4K`
5. Stronger iterative reasoning via Gemini 3 thinking controls

## Error handling

If the run fails:

1. Check `~/.nanobanana.env` and confirm `GEMINI_API_KEY` is present.
2. Confirm each input image path exists and is readable.
3. Confirm the output directory is writable.
4. If a feature looks unsupported, retry with `gemini-3.1-flash-image-preview` first.
5. If the response contains only text, rewrite the prompt so the image deliverable is explicit.

## Examples

### Fast ideation

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Create three-dimensional sticker-style fruit mascots on white" \
  --resolution 512px \
  --output /absolute/path/to/output/stickers.png
```

### Grounded current-events visual

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Use Google Search to ground a newspaper-style illustration about the latest Mars mission and create a restrained front-page visual" \
  --aspect-ratio 3:2 \
  --output /absolute/path/to/output/mars.png
```

### Multi-reference composite

```bash
python3 /absolute/path/to/nanobanana.py \
  --prompt "Create a single brand moodboard from these references. Keep the ceramic texture from the first image, the palette from the second, and the lighting mood from the third." \
  --input /absolute/path/to/a.png /absolute/path/to/b.png /absolute/path/to/c.png \
  --aspect-ratio 16:9 \
  --output /absolute/path/to/output/moodboard.png
```
