---
name: image-gen
description: "AI image generation: Gemini and Nano Banana backends; single/series/batch workflows with prompt-to-disk."
agent: python-general-engineer
user-invocable: false
routing:
  category: image-generation
  triggers:
    - generate image
    - create image
    - image generation
    - AI image
    - gemini image
    - make image
    - draw
    - illustrate
    - sprite generation
    - card art
    - batch generation
    - series of images
    - character art
    - pixel art
    - image post-processing
  not_for: "HTML visualization or charts (use html-artifact)"
  pairs_with:
    - python-general-engineer
    - game-sprite-pipeline
---

# image-gen

Backend-agnostic image generation workflow: single images, series with anchor-chain consistency, and batch pipelines. Two backends: Gemini (API) and Nano Banana (local scripts with post-processing).

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Every request (always load) | `references/series-consistency.md` | Anchor-chain and prompt-file-first rules apply to all generation |
| Every request (always load) | `references/backend-selection.md` | Mode decision required before every generation |
| Script output `gemini` | `references/backends/gemini.md` | Gemini API models, env vars, flags |
| Script output `nano-banana` | `references/backends/nano-banana.md` | Nano Banana subcommands, flags, aspect ratios |

## Phase 1: Detect Mode and Load References

Run the backend detection script — it reads environment variables and outputs a single word:

```bash
python3 skills/content/image-gen/scripts/detect-backend.py
```

Output values:
- `gemini` — GEMINI_API_KEY or GOOGLE_API_KEY is set
- `ask` — no key found; ask the user which backend to use

Load references based on output:

1. Load `references/series-consistency.md` (always — applies to every generation).
2. Load `references/backend-selection.md` (always — needed to pick mode and script).
3. Load `references/backends/gemini.md` when output is `gemini`.
4. Ask the user to set `GEMINI_API_KEY` or confirm they want to use local scripts when output is `ask`.

**Gate**: references loaded, backend confirmed before Phase 2.

## Phase 2: Write Prompt File

Write the complete prompt to disk before any API call. Prompt files serve as the generation record and the anchor-chain input for series — writing them first means the full intent is on disk before any quota is spent.

File naming:
- Single image: `prompts/YYYY-MM-DD-{slug}.md`
- Series: `prompts/{series-name}-01.md`, `prompts/{series-name}-02.md`, ...

Prompt file format:

```markdown
---
model: gemini-3-pro-image-preview
aspect-ratio: 1:1
flags: []
---

Full prompt text here. Be explicit about subject, style, background, and constraints.
```

Create the `prompts/` directory if absent:

```bash
mkdir -p prompts
```

For a series, write all prompt files before calling any generation script. See `references/series-consistency.md` for the anchor-chain algorithm and why this ordering prevents drift.

**Gate**: all prompt files written and reviewed before Phase 3.

## Phase 3: Select Mode and Script

Use `references/backend-selection.md` to map the request to the correct script and subcommand.

| Use case | Script | Notes |
|---|---|---|
| Single image, Gemini | `scripts/generate_image.py` | `--prompt` flag |
| Batch from prompt file, Gemini | `scripts/generate_image.py` | `--batch` flag |
| Single or batch with post-processing | `scripts/nano-banana-generate.py` | Full flag set in backend ref |
| Series with anchor chain | `scripts/nano-banana-generate.py with-reference` | Load ref images from previous outputs |
| Post-processing only | `scripts/nano-banana-process.py` | crop, remove-bg, pipeline subcommands |

**Gate**: script and subcommand identified before Phase 4.

## Phase 4: Generate

Call the selected script with absolute paths for output files — relative paths break when scripts run from different working directories.

For series generation, follow the anchor-chain sequence from `references/series-consistency.md`:
1. Generate image 1 with no reference.
2. Use output of image 1 as `--reference` for image 2.
3. Continue: each image references the previous output.

Show the full script output — the user needs status messages, warnings, and partial failure information.

**Gate**: script exits 0 before Phase 5.

## Phase 5: Verify and Report

Visual inspection is mandatory. Read the generated image file to verify:
- Subject matches the prompt
- No unwanted watermarks, logos, or artifacts
- Aspect ratio and framing are correct
- No excessive padding or dark borders that need cropping

If visual inspection fails: regenerate with an adjusted prompt. Report the issue clearly before retrying.

Report to the user:
- Output file path (absolute)
- Image dimensions
- Model used
- Post-processing applied (if any)
- Visual verification result

Report only what was requested. The user did not ask for style suggestions or additional generations.

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `GEMINI_API_KEY not set` | Missing env var | `export GEMINI_API_KEY=your_key` or `export GOOGLE_API_KEY=your_key` |
| `No image in response` | Prompt triggered safety filter or text-only response | Adjust prompt phrasing; check for policy-violating content |
| `Missing dependency: google-genai` | Package not installed | `pip install google-genai pillow` |
| `Rate limit exceeded (429)` | Too many API calls | Increase `--delay`; default 2s may be too aggressive on free tier |
| `Content policy violation (400)` | Restricted prompt content | Rephrase using neutral language; this restriction is API-side |
| `No image data in response` | API returned text only | Set `response_modalities=["IMAGE", "TEXT"]` in config |
