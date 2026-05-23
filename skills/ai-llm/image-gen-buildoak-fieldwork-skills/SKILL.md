---
name: image-gen
version: 2.1.0
description: |
  Image generation, editing, and review via OpenRouter API. Five models from budget to premium.
  Style presets for series consistency, JSON structured prompts, reference image anchoring,
  system message support, prompt upsampling. Vision-based quality review loop. Zero dependencies
  beyond Python stdlib. Use when: generate, create, draw, design, illustrate, edit,
  or modify images.
tools_required:
  - python3 (stdlib only, no pip deps)
triggers:
  - generate image, create image, draw, design, illustrate, sketch, render
  - make me a picture, create a logo, design a poster, generate artwork
  - edit image, modify image, change the background, add text to image
  - style transfer, make it look like, convert to watercolor
  - inpainting, remove object, replace background
  - user sends image + modification request
---

# image-gen

Image generation and editing via OpenRouter. Five models, three scripts, style presets, one JSON contract.

**Scripts:** `./scripts/generate.py`, `./scripts/edit.py`, `./scripts/review.py`
**Presets:** `./presets/*.json`
**Output dir:** `./data/`

## Setup

```bash
export OPENROUTER_API_KEY_IMAGES='your-api-key-here'
```

- **Claude Code:** copy this skill folder into `.claude/skills/image-gen/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, API keys, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

### Credential management

Three tiers for managing the `OPENROUTER_API_KEY_IMAGES` environment variable:

1. **Vault skill (recommended):** If you have a vault or secret-management skill, store the key there and export it before running scripts. Example: `export OPENROUTER_API_KEY_IMAGES=$(vault get OPENROUTER_API_KEY_IMAGES)`
2. **Custom secret manager:** Use your team's preferred secret manager (1Password CLI, AWS Secrets Manager, etc.)
3. **Plain export:** `export OPENROUTER_API_KEY_IMAGES='your-api-key-here'` in your shell profile

Optional keys for additional features:
- `OPENAI_API_KEY` -- for mask-based inpainting via `edit.py --mode openai`
- `ANTHROPIC_API_KEY` -- for auto-review via `review.py --auto`

---

## Model Selection

```text
What do you need?
  |
  +-- Fast + cheap + good enough?
  |     --> nanobanana (~$0.0004/image)
  |
  +-- High quality, no text?
  |     --> flux.2-pro (best visual quality)
  |
  +-- Text in the image?
  |     --> gpt-5-image (best text rendering)
  |
  +-- Image editing?
  |     +-- Describe changes in words --> gpt-5-image or nanobanana-pro
  |     +-- Paint mask area to change --> edit.py --mode openai
  |
  +-- Budget generation at scale?
  |     --> flux.2-klein (fastest, cheapest Flux)
  |
  +-- Quality + editing + reasoning?
        --> nanobanana-pro (best balance)
```

| Alias | Type | Cost | Best For |
|---|---|---|---|
| `flux.2-pro` | Image-only | ~$0.03/MP | Default high-quality generation |
| `flux.2-klein` | Image-only | ~$0.014/MP | Fast, budget generation |
| `gpt-5-image` | Text+Image | ~$0.04/image | Text rendering, complex edits |
| `nanobanana-pro` | Text+Image | ~$0.012/image | Balanced quality + editing |
| `nanobanana` | Text+Image | ~$0.0004/image | Lowest-cost generation |

Full comparison: `./references/model-card.md`

---

## Quick Reference

```bash
# Generate with default model (flux.2-pro)
python ./scripts/generate.py \
  --prompt "A red fox in snow" \
  --output-dir ./data/

# Generate with style preset
python ./scripts/generate.py \
  --prompt "A scene description for consistent series" \
  --preset default \
  --output-dir ./data/

# Generate with style reference image
python ./scripts/generate.py \
  --prompt "A new scene" \
  --style-ref /path/to/golden-image.png \
  --output-dir ./data/

# Generate with multiple style refs
python ./scripts/generate.py \
  --prompt "Scene desc" \
  --style-ref /path/to/ref1.png \
  --style-ref /path/to/ref2.png

# Generate with system message (GPT-5 / NanoBanana only)
python ./scripts/generate.py \
  --prompt "Scene desc" \
  --model gpt-5-image \
  --system-prompt "You generate muted watercolor illustrations..."

# Generate with prompt upsampling disabled
python ./scripts/generate.py \
  --prompt "Exact scene" \
  --model flux.2-pro \
  --no-prompt-upsampling

# Generate with options (model, aspect ratio, size)
python ./scripts/generate.py \
  --prompt "Tokyo skyline at sunset" \
  --model nanobanana-pro \
  --aspect-ratio 16:9 \
  --size 2K \
  --output-dir ./data/

# Generate with text (GPT-5 Image)
python ./scripts/generate.py \
  --prompt 'Poster with text "HELLO WORLD" in bold sans-serif typography' \
  --model gpt-5-image \
  --output-dir ./data/

# Edit image (chat-based)
python ./scripts/edit.py \
  --mode openrouter \
  --input-image ./data/input.png \
  --prompt "Change the background to a sunset beach" \
  --model gpt-5-image \
  --output-dir ./data/

# Edit image (mask-based)
python ./scripts/edit.py \
  --mode openai \
  --input-image ./data/input.png \
  --mask ./data/mask.png \
  --prompt "Replace masked area with a small bonsai tree" \
  --openai-size 1024x1024 \
  --output-dir ./data/

# Review quality (auto mode)
python ./scripts/review.py \
  --image ./data/output.png \
  --original-prompt "A red fox in snow" \
  --auto
```

---

## Style Presets

Presets encode visual identity into reusable JSON files. A preset defines palette, composition, rendering style, model defaults, and system messages.

### How Presets Work

1. Pick a preset based on the project context
2. `generate.py --preset <name>` loads the preset JSON
3. The script applies the preset: enhances the prompt with style data, selects model defaults, injects system messages
4. For Flux models: prompt is constructed as JSON (structured prompt, prevents concept bleeding)
5. For GPT-5/NanoBanana: style block is prepended as natural language, system message is injected

### Available Presets

| Preset | File | Description |
|--------|------|-------------|
| `default` | `presets/default.json` | No style constraints. Quality-focused defaults. |

### Preset Schema

```json
{
  "name": "preset-name",
  "description": "What this preset is for",
  "defaults": {
    "model": "flux.2-pro",
    "aspect_ratio": "3:2",
    "size": "2K"
  },
  "style": {
    "description": "Overall style description",
    "color_palette": ["#hex1", "#hex2", "#hex3"],
    "mood": "Emotional tone",
    "lighting": "Lighting description",
    "composition": "Composition rules",
    "rendering": "Rendering constraints",
    "camera": {"angle": "...", "framing": "..."},
    "anti_patterns": ["thing to avoid", "another thing"],
    "reference_images": ["/absolute/path/to/golden.png"]
  },
  "system_message": "System prompt for GPT-5/NanoBanana models"
}
```

### Priority Order (CLI > Preset > Hardcoded)

- `--model` flag overrides `preset.defaults.model`
- `--aspect-ratio` flag overrides `preset.defaults.aspect_ratio`
- `--size` flag overrides `preset.defaults.size`
- `--system-prompt` flag overrides `preset.system_message`
- If no preset and no flag: hardcoded defaults (flux.2-pro, 1:1, 2K)

### Creating a New Preset

1. Copy `presets/default.json` as a template
2. Set `name` and `description`
3. Fill `defaults` with preferred model, aspect ratio, size
4. Fill `style` with palette (HEX values), composition rules, rendering constraints
5. Write `system_message` for GPT-5/NanoBanana (ignored by Flux)
6. Optionally add `reference_images` paths for visual anchoring
7. Test: `python generate.py --prompt "test scene" --preset your-preset`

---

## Style References

Use `--style-ref` to pass reference images for visual anchoring. The script prepends a style transfer instruction automatically.

```bash
# Single reference (anchor to a "golden" image)
python ./scripts/generate.py --prompt "New scene" \
  --style-ref /path/to/golden.png

# Multiple references (combine style + content refs, up to 8)
python ./scripts/generate.py --prompt "New scene" \
  --style-ref /path/to/style-ref.png \
  --style-ref /path/to/character-ref.png
```

Reference images from presets (`style.reference_images`) are automatically loaded alongside CLI refs.

Full workflow and per-model consistency techniques: `./references/style-consistency.md`

---

## System Messages

Use `--system-prompt` to set persistent style context for GPT-5 Image and NanoBanana models. System messages are injected as the system role, keeping the user prompt focused on scene content only.

```bash
python ./scripts/generate.py \
  --prompt "A quiet village at dawn" \
  --model gpt-5-image \
  --system-prompt "You generate muted watercolor illustrations with earth-tone palettes..."
```

System messages can also be set in presets via the `system_message` field. CLI `--system-prompt` overrides preset system messages.

Flux models do not support system messages (the flag is silently ignored).

---

## Prompt Upsampling

Flux models support `prompt_upsampling` -- an API feature that auto-enhances basic prompts into richer descriptions before generation.

- **Default:** ON for Flux models (flux.2-pro, flux.2-klein)
- **Disable:** `--no-prompt-upsampling` when you want exact prompt control
- **Enable:** `--prompt-upsampling` (explicit, same as default)
- **Non-Flux models:** Flag is silently ignored

```bash
# Default: upsampling ON (good for short/simple prompts)
python ./scripts/generate.py --prompt "A cat" --model flux.2-pro

# Disable: exact prompt control (good for precise/pre-enhanced prompts)
python ./scripts/generate.py --prompt "Detailed exact scene..." \
  --model flux.2-pro --no-prompt-upsampling
```

---

## Prompt Engineering

### Enhance-before-generate protocol

1. Identify intent: photo, illustration, logo, diagram, etc.
2. Select preset if this is series work.
3. Fill missing details: subject, style, lighting, composition, camera/look.
4. Tune prompt shape to model: concise for Flux, more explicit for GPT-5/NanoBanana family.
5. Add quality boosters that match requested style.

### Example: raw prompt -> enhanced prompt

- Raw prompt: `a cat in space`
- Enhanced prompt: `Orange tabby cat in a custom spacesuit floating in zero gravity, Earth visible in helmet reflection, dramatic rim lighting, cinematic framing, ultra-detailed, high contrast, clean background`

Templates, per-model formats, JSON structured prompts, and examples: `./references/prompt-templates.md`

---

## Generation Workflow

### 1. Select Preset (if applicable)

If the image is part of a series or project with established visual identity, select the appropriate preset.

### 2. Enhance Prompt

Transform the raw prompt into a model-optimized prompt. Each model interprets prompts differently:

- **Flux:** Concise, front-loaded, under 80 words. JSON for complex multi-element scenes. HEX colors for precision.
- **GPT-5 Image:** Detailed natural language. System messages for series work. Text in quotes for rendering.
- **NanoBanana:** Structured narrative. Constrain palette explicitly for muted styles ("no neon, desaturated").

### 3. Generate

```bash
python ./scripts/generate.py \
  --prompt "[enhanced prompt]" \
  --model [chosen model] \
  --preset [preset if applicable] \
  --aspect-ratio [ratio] \
  --size [1K|2K|4K]
```

Output: JSON to stdout with `path`, `model`, `cost_estimate`, `generation_time_ms`.

When a preset is used, the script handles prompt enhancement internally. Enhance the scene description but do NOT manually add style parameters -- the preset handles that.

### 4. Review (Optional)

For quality-critical work:

```bash
python ./scripts/review.py \
  --image /path/to/output.png \
  --original-prompt "[the enhanced prompt]" \
  --auto
```

Output: JSON with `score`, `verdict` (accept/refine/reject), `critique`, `suggested_refinement`.

- `accept` (score >= 7): Deliver to user
- `refine` (score 4-6): Re-generate with `suggested_refinement` applied
- `reject` (score < 4): Re-generate with different model or reworked prompt

### 5. Deliver

Return the file path and a brief description.

---

## Editing Workflow

### Chat-Based Editing (OpenRouter)

For natural language edits: "make it darker", "change background to beach", "add a hat".

```bash
python ./scripts/edit.py --mode openrouter \
  --input-image /path/to/original.png \
  --prompt "Change the background to a sunset beach" \
  --model nanobanana-pro
```

Best models for chat editing: `gpt-5-image`, `nanobanana-pro`.

### Mask-Based Inpainting (OpenAI Direct)

For precise area editing with a mask image.

```bash
python ./scripts/edit.py --mode openai \
  --input-image /path/to/original.png \
  --mask /path/to/mask.png \
  --prompt "A fluffy orange cat" \
  --openai-size 1024x1024
```

Requires `OPENAI_API_KEY`. Mask: PNG with transparent areas where edits should happen.

---

## Script Output Contract

All scripts output JSON to stdout. Parse JSON, never text.

### generate.py success

```json
{
  "success": true,
  "path": "/abs/path/to/20260217-143052-flux-2-pro.png",
  "all_paths": ["/abs/path/to/20260217-143052-flux-2-pro.png"],
  "model": "black-forest-labs/flux.2-pro",
  "prompt": "the user prompt",
  "enhanced_prompt": "the preset-enhanced prompt (if different)",
  "preset": "my-preset",
  "aspect_ratio": "16:9",
  "size": "2K",
  "cost_estimate": "~$0.120",
  "generation_time_ms": 8500,
  "image_count": 1,
  "style_refs": ["/path/to/ref.png"],
  "system_message_used": true
}
```

### generate.py / edit.py error

```json
{
  "success": false,
  "error": "HTTP 429: Too Many Requests",
  "details": "Rate limit exceeded...",
  "model": "black-forest-labs/flux.2-pro",
  "generation_time_ms": 150
}
```

### review.py output (auto mode)

```json
{
  "success": true,
  "mode": "auto",
  "score": 8,
  "prompt_adherence": 9,
  "technical_quality": 8,
  "composition": 7,
  "verdict": "accept",
  "critique": "Strong prompt adherence with vivid colors. Minor composition issue with empty right third.",
  "suggested_refinement": ""
}
```

---

## CLI Flags Reference

### generate.py

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Generation prompt |
| `--model` | preset or `flux.2-pro` | Model alias or full OpenRouter ID |
| `--aspect-ratio` | preset or `1:1` | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `--size` | preset or `2K` | 1K, 2K, 4K |
| `--output-dir` | `./data/` | Output directory |
| `--output-file` | auto-named | Explicit output path |
| `--seed` | none | Random seed (model-dependent) |
| `--input-image` | none | Input image for editing |
| `--preset` | none | Style preset name or path to JSON file |
| `--style-ref` | none | Style reference image path (repeatable, up to 8) |
| `--prompt-upsampling` | on for Flux | Enable Flux prompt_upsampling |
| `--no-prompt-upsampling` | | Disable prompt_upsampling |
| `--system-prompt` | preset or none | System message for GPT-5/NanoBanana |

### edit.py

| Flag | Default | Description |
|---|---|---|
| `--mode` | required | `openrouter` or `openai` |
| `--input-image` | required | Image to edit |
| `--prompt` | required | Edit instruction |
| `--mask` | none | Mask PNG (openai mode) |
| `--model` | `gpt-5-image` | Model for openrouter mode |
| `--openai-model` | `gpt-image-1` | Model for openai mode |
| `--openai-size` | none | Size for openai mode |
| `--openai-quality` | none | Quality for openai mode |
| `--output-dir` | `./data/` | Output directory |
| `--output-file` | auto-named | Explicit output path |

### review.py

| Flag | Default | Description |
|---|---|---|
| `--image` | required | Image to review |
| `--original-prompt` | required | Prompt used for generation |
| `--auto` | false | Auto-review via Anthropic API |

---

## Cost Tracking

Report cost after every generation. Use the `cost_estimate` field from script output.

| Model | Typical Cost |
|---|---|
| NanoBanana | $0.0004 |
| Flux 2 Klein | $0.01-0.03 |
| NanoBanana Pro | $0.01-0.03 |
| Flux 2 Pro | $0.03-0.12 |
| GPT-5 Image | $0.03-0.10 |

Tip: for batch generation (5+ images), prefer NanoBanana or Flux 2 Klein to control spend.

---

## Error Handling

| Error | Action |
|---|---|
| No API key | Script exits with JSON error. Check env vars. |
| HTTP 429 (rate limit) | Wait 10s, retry. If persistent, switch model. |
| HTTP 402 (no credits) | Top up OpenRouter account. |
| No images in response | Check model supports image output. Try different model. |
| Timeout (>180s) | Model may be overloaded. Try Klein or NanoBanana for speed. |
| Image quality too low | Run review loop. Refine prompt or switch to higher-quality model. |
| Preset not found | Check presets/ directory. Use preset name without .json extension. |

---

## Anti-Patterns

| Do NOT | Do Instead |
|---|---|
| Send raw user prompts to models | Always enhance prompts first |
| Use Flux for text in images | Use GPT-5 Image or NanoBanana Pro |
| Use GPT-5 for bulk generation | Use NanoBanana or Flux Klein (10-100x cheaper) |
| Skip cost reporting | Always report estimated cost |
| Retry same prompt on failure | Rework prompt or switch model |
| Use review loop for casual requests | Reserve for quality-critical work |
| Forget to set API key before running | Export required keys before running scripts |
| Use JSON prompts for GPT-5 Image | GPT-5 prefers natural language; JSON adds no benefit |
| Use verbal color descriptions with Flux | Use HEX values in palette for precise control |
| Generate series images without a preset | Create a preset for any 3+ image series |
| Forget --style-ref for consistency | Use golden image as reference for series work |

---

## Bundled Resources Index

| Path | What | When to Load |
|---|---|---|
| `./scripts/generate.py` | Core image generation script | Every generation task |
| `./scripts/edit.py` | Chat-based and mask-based editing | Image modification requests |
| `./scripts/review.py` | Vision-based quality review | Quality-critical workflows |
| `./presets/default.json` | Default preset (no style constraints) | Reference for preset schema |
| `./references/prompt-templates.md` | SOTA prompt engineering: per-model formats, JSON templates, style modifiers, enhancement protocol | Prompt engineering step |
| `./references/style-consistency.md` | Reference image workflow, seed workflow, consistency technique stack | Generating image series requiring visual consistency |
| `./references/model-card.md` | Model capabilities, tradeoffs, pricing context | Model selection and optimization |
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./references/api-reference.md` | API payload and integration details | Debugging and advanced usage |
| `./references/book-to-prompts-playbook.md` | Method for extracting visual prompts from literature | Book illustration projects |
| `./examples/` | Example outputs by model | Visual quality and style calibration |
| `./UPDATES.md` | Changelog for this skill | Checking new features/fixes |
| `./UPDATE-GUIDE.md` | Agent-oriented update instructions | Applying updates safely |

---

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the image-gen skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

To check upstream updates directly from GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/buildoak/fieldwork-skills/main/skills/image-gen/UPDATES.md | head -40
```
