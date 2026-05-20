---
name: three-generation-family-studio-portrait-prompt
description: This prompt instructs an AI to act as a professional studio family portrait director and produce a single polished, photorealistic multi‑generation group portrait by seamlessly merging the provided individual reference photos into one cohesive studio scene. It specifies the desired studio backdrop color, lighting style, and coordinated wardrobe, and requires consistent shadows and color grading, authentic expressions, and preserved facial likeness and proportions for every person. The intended outcome is an elegant, timeless, print‑ready family portrait that includes exactly all original family members with no additions or omissions, avoids unrealistic edits or props, and follows privacy, workflow, and quality constraints to ensure a natural, high‑end result delivered reliably.
skillVersionId: 01992c73-9d55-79a3-a972-240526e36663
---

## What it does

This prompt instructs an AI to act as a professional studio family portrait director and produce a single polished, photorealistic multi‑generation group portrait by seamlessly merging the provided individual reference photos into one cohesive studio scene. It specifies the desired studio backdrop color, lighting style, and coordinated wardrobe, and requires consistent shadows and color grading, authentic expressions, and preserved facial likeness and proportions for every person. The intended outcome is an elegant, timeless, print‑ready family portrait that includes exactly all original family members with no additions or omissions, avoids unrealistic edits or props, and follows privacy, workflow, and quality constraints to ensure a natural, high‑end result delivered reliably.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `clothing_style` | Optional |  | `coordinated white shirts with light denim jeans` |
| `lighting_style` | Optional |  | `soft diffused lighting with gentle highlights` |
| `background_color` | Optional |  | `soft pastel blue` |



### imageInputs

This prompt requires **exactly 3 images**. You **must pass exactly 3 image flags** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Grandparents image | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |
| 2 | Yes | Parents Image | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |
| 3 | Yes | Children image | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


### Models and options

This skill's modality is: **`image`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"image"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "image"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:

- Optional text inputs (use defaults if not provided by the human):
    - `clothing_style` (default: `coordinated white shirts with light denim jeans`)
  - `lighting_style` (default: `soft diffused lighting with gentle highlights`)
  - `background_color` (default: `soft pastel blue`)
- Required images:
  - **Exactly 3** images: image 1 (Grandparents image), image 2 (Parents Image), and image 3 (Children image). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Grandparents image), image 2 (Parents Image), and image 3 (Children image)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01992c73-9d55-79a3-a972-240526e36663`).

Command form:

```bash
betterprompt generate 01992c73-9d55-79a3-a972-240526e36663 \
  [--input <key>=<value>] \
  [--image-input-url <url>] \
  [--image-input-base64 <base64>] \
  [--image-input-path <absolute path to image>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- Pass each image using one of `--image-input-url`, `--image-input-base64`, or `--image-input-path`, in the order matching the imageInputs descriptions (image 1 first, then image 2, etc.).
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gemini-2.5-flash-image-preview`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 01992c73-9d55-79a3-a972-240526e36663 \
  --input 'clothing_style=coordinated white shirts with light denim jeans' \
  --input 'lighting_style=soft diffused lighting with gentle highlights' \
  --input 'background_color=soft pastel blue' \
  --image-input-url https://example.com/image1.png \
  --image-input-path /path/to/image2.png \
  --image-input-url https://example.com/image3.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
