---
name: imagegen
description: >-
  Use when the user asks to generate or edit images via the OpenAI Image API
  (for example: generate image, edit/inpaint/mask, background removal or
  replacement, transparent background, product shots, concept art, covers, or
  batch variants); run the bundled CLI (scripts/image_gen.py) and require
  OPENAI_API_KEY for live calls.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - builder
    - image-generation
    - openai
    - ai
  provenance:
    upstream_source: "imagegen"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T12:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.88
---

# Image Generation Skill

Generate or edit images using the OpenAI Image API via a bundled CLI.

## Overview

This skill creates image artifacts — new images from text prompts, edits of existing images (inpainting, background replacement, object removal), and batch generation of multiple variants. It wraps the OpenAI Image API through a bundled Python CLI (`scripts/image_gen.py`) that handles prompt augmentation, parameter validation, retries, and output management.

**What it creates:**
- Generated images from text prompts (product shots, concept art, heroes, logos, wireframes)
- Edited images from input images with optional masks (background removal, inpainting, style transfer)
- Batch image sets from JSONL manifests (multiple prompts run concurrently)

**Prerequisites:**
- `OPENAI_API_KEY` environment variable must be set
- Python 3 with `openai` package (`uv pip install openai`)
- Optional: `pillow` for downscaling (`uv pip install pillow`)

## Decision Tree

Classify each request into one mode:

```
User request
 |- Provides input image OR says "edit/retouch/inpaint/mask/change only X"
 |   -> MODE: edit
 |- Needs many different prompts/assets
 |   -> MODE: generate-batch
 |- Otherwise
     -> MODE: generate
```

Special cases:
- "transparent background" on existing image -> **edit** (background extraction)
- "transparent background" on new image -> **generate** with `--background transparent`
- "remove background" -> **edit**
- Multiple variants of same prompt -> **generate** with `--n` (not batch)
- Multiple different prompts -> **generate-batch**

## Workflow

### Step 1: Check Environment

Verify `OPENAI_API_KEY` is set. If missing, guide the user:
1. Create a key at https://platform.openai.com/api-keys
2. Export it: `export OPENAI_API_KEY="sk-..."`
3. Never ask the user to paste the key in chat

Check dependencies:
```bash
python3 -c "import openai" 2>/dev/null || uv pip install openai
```

### Step 2: Classify Intent

Use the decision tree above. If ambiguous, ask the user.

### Step 3: Collect Inputs

Gather from the user:
- **Prompt**: The primary text description
- **Constraints**: What to include/exclude
- **Size**: `1024x1024` (default), `1536x1024`, `1024x1536`, or `auto`
- **Quality**: `auto` (default), `low`, `medium`, `high`

For edits, also collect:
- **Input image(s)**: File path(s)
- **Mask** (optional): PNG with alpha channel, matching input dimensions
- **Invariants**: What must NOT change

### Step 4: Augment Prompt

Reformat the user's prompt into a structured spec. Only make implicit details explicit; do not invent new creative requirements.

**Generate template** (include only relevant lines):
```
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Scene/background: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

**Edit template:**
```
Use case: <taxonomy slug>
Primary request: <edit instruction>
Constraints: change only <X>; keep <Y> unchanged
```

See `references/prompting-guide.md` for best practices.

### Step 5: Run CLI

Set the CLI path:
```bash
IMAGE_GEN="<skill-directory>/scripts/image_gen.py"
```

**Generate:**
```bash
python3 "$IMAGE_GEN" generate --prompt "<augmented prompt>" --size 1024x1024
```

**Edit:**
```bash
python3 "$IMAGE_GEN" edit --image input.png --prompt "<augmented prompt>"
```

**Batch** (write temp JSONL, run, clean up):
```bash
mkdir -p tmp/imagegen
cat > tmp/imagegen/jobs.jsonl << 'EOF'
{"prompt": "First prompt", "size": "1024x1024"}
{"prompt": "Second prompt", "size": "1536x1024"}
EOF
python3 "$IMAGE_GEN" generate-batch --input tmp/imagegen/jobs.jsonl --out-dir output/
rm -f tmp/imagegen/jobs.jsonl
```

Full CLI reference: `references/cli-reference.md`

### Step 6: Inspect and Validate

1. Report output file paths to the user
2. Open/view the image to check quality
3. Validate: subject accuracy, style match, text rendering, constraint compliance

### Step 7: Iterate

If output doesn't meet requirements:
1. Make a **single targeted change** (prompt wording or parameter)
2. Re-run the CLI
3. Re-inspect

For edits, re-state invariants every iteration to reduce drift.

### Step 8: Deliver

Save final outputs and report file path(s), final prompt used, and key parameters.

## Use-Case Taxonomy

**Generate slugs:**

| Slug | Use For |
|------|---------|
| `photorealistic-natural` | Candid/editorial scenes with real texture |
| `product-mockup` | Product/packaging shots, catalog imagery |
| `ui-mockup` | App/web interface mockups |
| `infographic-diagram` | Diagrams with structured layout and text |
| `logo-brand` | Logo/mark exploration |
| `illustration-story` | Comics, children's book art |
| `stylized-concept` | Style-driven concept art, 3D renders |
| `historical-scene` | Period-accurate scenes |

**Edit slugs:**

| Slug | Use For |
|------|---------|
| `text-localization` | Translate/replace in-image text |
| `identity-preserve` | Try-on, person-in-scene with locked identity |
| `precise-object-edit` | Remove/replace a specific element |
| `lighting-weather` | Time-of-day/atmosphere changes |
| `background-extraction` | Transparent background / clean cutout |
| `style-transfer` | Apply reference style to new content |
| `compositing` | Multi-image merge |
| `sketch-to-render` | Line art to photorealistic render |

## Defaults and Rules

- Model: `gpt-image-1.5` unless user requests `gpt-image-1-mini`
- Size: `1024x1024` | Quality: `auto` | Format: `png`
- Transparent backgrounds require `png` or `webp` format
- Prefer the bundled CLI over one-off scripts
- Never modify `scripts/image_gen.py`
- Use `uv run --with openai` if the package isn't in the active environment

## Prompt Augmentation Rules

- Keep augmentation short; add only details the user implied
- Classify into a taxonomy slug and tailor constraints to that bucket
- For edits, explicitly list invariants ("change only X; keep Y unchanged")
- Do not add creative elements the user didn't ask for
- For "tacky" results, add: `Avoid: stock-photo vibe; cheesy lens flare; oversaturated neon`
- Quote exact text verbatim; spell uncommon words letter-by-letter

## Examples

### Example 1: Generate a product hero

```
User: Generate a hero image for my coffee shop landing page

Assistant: I'll create a hero image for your coffee shop.

Augmented prompt:
  Use case: product-mockup
  Asset type: landing page hero
  Primary request: warm coffee shop scene with a ceramic mug
  Style/medium: clean product photography
  Composition/framing: centered, negative space on the right for headline
  Lighting/mood: soft warm studio lighting
  Constraints: no logos, no text, no watermark

Running: python3 scripts/image_gen.py generate \
  --prompt "..." --size 1536x1024

Output: output.png (1536x1024)
```

### Example 2: Edit (background removal)

```
User: Remove the background from product.png and make it transparent

Assistant: I'll extract the product on a transparent background.

Augmented prompt:
  Use case: background-extraction
  Primary request: extract product on transparent background
  Constraints: crisp silhouette, no halos; preserve label text

Running: python3 scripts/image_gen.py edit --image product.png \
  --prompt "..." --background transparent --output-format png

Output: output.png (transparent PNG)
```

### Example 3: Batch generation

```
User: Generate 4 seasonal hero images for our website

Assistant: I'll create a JSONL batch with 4 seasonal prompts.

Steps:
  1. Write tmp/imagegen/seasonal.jsonl with 4 jobs
  2. python3 scripts/image_gen.py generate-batch \
       --input tmp/imagegen/seasonal.jsonl --out-dir output/seasonal/
  3. rm tmp/imagegen/seasonal.jsonl

Output: output/seasonal/ (4 images)
```

## Output Checklist

After each generation, verify:

- [ ] Output file exists at the expected path
- [ ] Image format matches request (png/jpeg/webp)
- [ ] Image dimensions match `--size` parameter
- [ ] Subject matches the user's description
- [ ] Style/mood matches the augmented prompt
- [ ] Text (if any) renders correctly and verbatim
- [ ] Constraints are satisfied (no logos, no watermarks, etc.)
- [ ] For edits: invariants are preserved (unchanged regions)
- [ ] For batch: all jobs produced output
- [ ] Temporary files (JSONL) cleaned up

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `OPENAI_API_KEY is not set` | Export the key: `export OPENAI_API_KEY="sk-..."` |
| `openai SDK not installed` | Run `uv pip install openai` or `pip install openai` |
| Network blocked in sandbox | See `references/codex-network.md` for sandbox config |
| Rate limit (429) | CLI retries automatically; reduce `--concurrency` for batch |
| Transparent bg but got opaque | Set `--output-format png` or `webp` with `--background transparent` |
| Mask dimension mismatch | Ensure mask PNG matches input image dimensions |
| Tacky/stock-photo results | Add `Avoid:` line in prompt; specify restraint (editorial, minimal) |
| Text renders incorrectly | Spell letter-by-letter; use `quality=high`; require verbatim |

## Reference Map

- **`references/cli-reference.md`**: CLI commands, flags, defaults, and recipes
- **`references/image-api-reference.md`**: API endpoints, parameters, sizes, quality levels
- **`references/prompting-guide.md`**: Prompt structure, specificity, composition, constraints
- **`references/sample-prompts.md`**: Copy-paste prompt recipes for generate and edit workflows
