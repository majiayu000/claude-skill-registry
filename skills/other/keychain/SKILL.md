---
name: keychain
description: This prompt instructs an image generation/editing system to produce a high-resolution vertical portrait that preserves the subject’s exact real-world likeness while adding a physically plausible keychain in their hand featuring a small, stylized 3D cartoon version of the same person. The result should look like professional photography—natural skin texture, cinematic lighting, shallow depth of field, warm indoor background—while the mini figure reads as a toy-like 3D character with matching outfit and clear resemblance, integrated with consistent lighting, realistic metallic materials, and correct shadows, avoiding artifacts like distorted hands, mismatched identity, or watermarks.
skillVersionId: 019c418f-13c2-7063-a866-0f22b5b16ce9
---

## What it does

This prompt instructs an image generation/editing system to produce a high-resolution vertical portrait that preserves the subject’s exact real-world likeness while adding a physically plausible keychain in their hand featuring a small, stylized 3D cartoon version of the same person. The result should look like professional photography—natural skin texture, cinematic lighting, shallow depth of field, warm indoor background—while the mini figure reads as a toy-like 3D character with matching outfit and clear resemblance, integrated with consistent lighting, realistic metallic materials, and correct shadows, avoiding artifacts like distorted hands, mismatched identity, or watermarks.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Upload your photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
  - **Exactly 1** images: image 1 (Upload your photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-3-pro-image-preview`** and its available options. Look up `gemini-3-pro-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"aspectRatio":"3:4","resolution":"1K"}`.
  - If the human does not specify, defaults are used: model `gemini-3-pro-image-preview`, options `{"aspectRatio":"3:4","resolution":"1K"}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Upload your photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019c418f-13c2-7063-a866-0f22b5b16ce9`).

Command form:

```bash
betterprompt generate 019c418f-13c2-7063-a866-0f22b5b16ce9 \
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
betterprompt generate 019c418f-13c2-7063-a866-0f22b5b16ce9 \
  --image-input-url https://example.com/image1.png \
  --model gemini-3-pro-image-preview \
  --options '{"aspectRatio":"3:4","resolution":"1K"}'
```
