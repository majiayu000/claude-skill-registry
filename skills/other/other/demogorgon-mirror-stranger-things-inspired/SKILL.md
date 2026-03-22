---
name: demogorgon-mirror-stranger-things-inspired
description: This prompt instructs an image model to generate two photorealistic horror bathroom scenes—one with a woman in a white lace dress and one with a man in a white garment—each using an exact, undistorted reference face, posed front-facing at a sink with a fearful expression. In both versions, the mirror behind them shows a Demogorgon-like creature only in the reflection, aligned correctly with the subject and rendered in a cold, desaturated, cinematic style with grime/fog for tension. The intended result is a consistent, Stranger Things–inspired composition where the human remains clearly visible in the foreground while the monster dominates the mirror, with strict negatives preventing pose changes, face obstruction, stylization, or creature substitution.
skillVersionId: 019ac429-e055-769f-8588-bb34946c9243
---

## What it does

This prompt instructs an image model to generate two photorealistic horror bathroom scenes—one with a woman in a white lace dress and one with a man in a white garment—each using an exact, undistorted reference face, posed front-facing at a sink with a fearful expression. In both versions, the mirror behind them shows a Demogorgon-like creature only in the reflection, aligned correctly with the subject and rendered in a cold, desaturated, cinematic style with grime/fog for tension. The intended result is a consistent, Stranger Things–inspired composition where the human remains clearly visible in the foreground while the monster dominates the mirror, with strict negatives preventing pose changes, face obstruction, stylization, or creature substitution.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Your photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
  - **Exactly 1** images: image 1 (Your photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-3-pro-image-preview`** and its available options. Look up `gemini-3-pro-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"aspectRatio":"3:4","resolution":"1K"}`.
  - If the human does not specify, defaults are used: model `gemini-3-pro-image-preview`, options `{"aspectRatio":"3:4","resolution":"1K"}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Your photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019ac429-e055-769f-8588-bb34946c9243`).

Command form:

```bash
betterprompt generate 019ac429-e055-769f-8588-bb34946c9243 \
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
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"aspectRatio":"3:4","resolution":"1K"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019ac429-e055-769f-8588-bb34946c9243 \
  --image-input-url https://example.com/image1.png \
  --model gemini-3-pro-image-preview \
  --options '{"aspectRatio":"3:4","resolution":"1K"}'
```
