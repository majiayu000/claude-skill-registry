---
name: stranger-things-final-season-poster
description: This prompt instructs an image-generation system to take a user-supplied portrait and convert it into an ultra-realistic, Netflix-style character poster that matches the look and layout of a Stranger Things Season 5 promo, preserving the person’s identity while adding cinematic red-and-black lighting, a single clearly readable neon “5” in the background, specified wardrobe styling based on gender presentation, and fixed branding text/logos placed in exact positions for a print-ready, high-resolution poster result.
skillVersionId: 019ad80e-b6d6-7089-ac4d-a56ee5fed2db
---

## What it does

This prompt instructs an image-generation system to take a user-supplied portrait and convert it into an ultra-realistic, Netflix-style character poster that matches the look and layout of a Stranger Things Season 5 promo, preserving the person’s identity while adding cinematic red-and-black lighting, a single clearly readable neon “5” in the background, specified wardrobe styling based on gender presentation, and fixed branding text/logos placed in exact positions for a print-ready, high-resolution poster result.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Upload your photo to generate | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
  - **Exactly 1** images: image 1 (Upload your photo to generate). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-3-pro-image-preview`** and its available options. Look up `gemini-3-pro-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"aspectRatio":"2:3","resolution":"1K"}`.
  - If the human does not specify, defaults are used: model `gemini-3-pro-image-preview`, options `{"aspectRatio":"2:3","resolution":"1K"}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Upload your photo to generate)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019ad80e-b6d6-7089-ac4d-a56ee5fed2db`).

Command form:

```bash
betterprompt generate 019ad80e-b6d6-7089-ac4d-a56ee5fed2db \
  [--image-input-url <url>] \
  [--image-input-base64 <base64>] \
  [--image-input-path <absolute path to image>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each image using one of `--image-input-url`, `--image-input-base64`, or `--image-input-path`, in the order matching the imageInputs descriptions (image 1 first, then image 2, etc.).
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gemini-3-pro-image-preview`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"aspectRatio":"2:3","resolution":"1K"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019ad80e-b6d6-7089-ac4d-a56ee5fed2db \
  --image-input-url https://example.com/image1.png \
  --model gemini-3-pro-image-preview \
  --options '{"aspectRatio":"2:3","resolution":"1K"}'
```
