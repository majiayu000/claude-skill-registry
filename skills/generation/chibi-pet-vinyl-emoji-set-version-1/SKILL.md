---
name: chibi-pet-vinyl-emoji-set-version-1
description: This prompt instructs an image-generation workflow to create a cohesive pack of nine polished, 3D-rendered digital stickers depicting a chibi-style vinyl capsule toy version of a specific real pet based on an uploaded reference photo, preserving the pet’s exact identifying traits while translating them into a smooth collectible-toy aesthetic. The result is a modern, consistent 2025-style “pet emoji” sticker set on a clean background, with each sticker showing a different specified facial expression and maintaining uniform lighting, materials, and toy proportions for easy cropping and pack-wide visual cohesion.
skillVersionId: 0197ed83-ab84-7fcf-82fa-679bbdae737a
---

## What it does

This prompt instructs an image-generation workflow to create a cohesive pack of nine polished, 3D-rendered digital stickers depicting a chibi-style vinyl capsule toy version of a specific real pet based on an uploaded reference photo, preserving the pet’s exact identifying traits while translating them into a smooth collectible-toy aesthetic. The result is a modern, consistent 2025-style “pet emoji” sticker set on a clean background, with each sticker showing a different specified facial expression and maintaining uniform lighting, materials, and toy proportions for easy cropping and pack-wide visual cohesion.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Your Pet | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
  - **Exactly 1** images: image 1 (Your Pet). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gpt-image-1`** and its available options. Look up `gpt-image-1` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"image":{"quality":1},"quality":"medium"}`.
  - If the human does not specify, defaults are used: model `gpt-image-1`, options `{"image":{"quality":1},"quality":"medium"}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Your Pet)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0197ed83-ab84-7fcf-82fa-679bbdae737a`).

Command form:

```bash
betterprompt generate 0197ed83-ab84-7fcf-82fa-679bbdae737a \
  [--image-input-url <url>] \
  [--image-input-base64 <base64>] \
  [--image-input-path <absolute path to image>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each image using one of `--image-input-url`, `--image-input-base64`, or `--image-input-path`, in the order matching the imageInputs descriptions (image 1 first, then image 2, etc.).
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-image-1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"image":{"quality":1},"quality":"medium"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 0197ed83-ab84-7fcf-82fa-679bbdae737a \
  --image-input-url https://example.com/image1.png \
  --model gpt-image-1 \
  --options '{"image":{"quality":1},"quality":"medium"}'
```
