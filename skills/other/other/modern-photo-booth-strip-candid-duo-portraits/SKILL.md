---
name: modern-photo-booth-strip-candid-duo-portraits
description: This prompt instructs the AI to generate a photorealistic, modern photo booth-style film strip composed of four vertically stacked, evenly spaced frames, each showing the same young man and young woman waist-up against a plain neutral studio background under soft, diffused lighting. Across the sequence, their poses and expressions shift subtly (e.g., laughing, leaning in, pointing, and smiling) to convey natural chemistry and candid interaction while maintaining consistent framing, color balance, and minimal white borders, with no text, logos, props, or decorative elements.
skillVersionId: 019a0a93-5979-720c-ad97-5c944c1362f3
---

## What it does

This prompt instructs the AI to generate a photorealistic, modern photo booth-style film strip composed of four vertically stacked, evenly spaced frames, each showing the same young man and young woman waist-up against a plain neutral studio background under soft, diffused lighting. Across the sequence, their poses and expressions shift subtly (e.g., laughing, leaning in, pointing, and smiling) to convey natural chemistry and candid interaction while maintaining consistent framing, color balance, and minimal white borders, with no text, logos, props, or decorative elements.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 2 images**. You **must pass exactly 2 image flags** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Your photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |
| 2 | Yes | Your photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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

- Required images:
  - **Exactly 2** images: image 1 (Your photo) and image 2 (Your photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Your photo) and image 2 (Your photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019a0a93-5979-720c-ad97-5c944c1362f3`).

Command form:

```bash
betterprompt generate 019a0a93-5979-720c-ad97-5c944c1362f3 \
  [--image-input-url <url>] \
  [--image-input-base64 <base64>] \
  [--image-input-path <absolute path to image>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each image using one of `--image-input-url`, `--image-input-base64`, or `--image-input-path`, in the order matching the imageInputs descriptions (image 1 first, then image 2, etc.).
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gemini-2.5-flash-image-preview`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019a0a93-5979-720c-ad97-5c944c1362f3 \
  --image-input-url https://example.com/image1.png \
  --image-input-path /path/to/image2.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
