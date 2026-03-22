---
name: extreme-wide-rapeseed-duo-one-hand-hold
description: This prompt instructs an image-generation system to produce a high-resolution, photoreal extreme-wide establishing shot of two referenced individuals centered in a vast yellow rapeseed field, front-facing, with strict one-hand-only downward handholding and all other hands relaxed, while enforcing near-perfect preservation of each person’s identity, gender expression, facial features, hair, and skin tone from the provided reference images. The intended outcome is a calm, romantic, golden-hour scene with precise composition, camera and background constraints, and automatic rejection or retry rules if similarity, gender confidence, framing, hand-contact count, or prohibited elements (e.g., text/logos or specified banned objects) deviate from the requirements.
skillVersionId: 0199513e-fe86-7b97-859b-f9d57ea7d224
---

## What it does

This prompt instructs an image-generation system to produce a high-resolution, photoreal extreme-wide establishing shot of two referenced individuals centered in a vast yellow rapeseed field, front-facing, with strict one-hand-only downward handholding and all other hands relaxed, while enforcing near-perfect preservation of each person’s identity, gender expression, facial features, hair, and skin tone from the provided reference images. The intended outcome is a calm, romantic, golden-hour scene with precise composition, camera and background constraints, and automatic rejection or retry rules if similarity, gender confidence, framing, hand-contact count, or prohibited elements (e.g., text/logos or specified banned objects) deviate from the requirements.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 2 images**. You **must pass exactly 2 image flags** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | a photo of you | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |
| 2 | Yes | a photo of your friend | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
  - **Exactly 2** images: image 1 (a photo of you) and image 2 (a photo of your friend). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (a photo of you) and image 2 (a photo of your friend)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0199513e-fe86-7b97-859b-f9d57ea7d224`).

Command form:

```bash
betterprompt generate 0199513e-fe86-7b97-859b-f9d57ea7d224 \
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
betterprompt generate 0199513e-fe86-7b97-859b-f9d57ea7d224 \
  --image-input-url https://example.com/image1.png \
  --image-input-path /path/to/image2.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
