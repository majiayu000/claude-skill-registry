---
name: modern-editorial-top-view-portrait
description: This prompt instructs an image model to generate a hyper-realistic, magazine-style 8K editorial portrait from a top-down, slightly diagonal viewpoint, preserving the subject’s identity and natural features while placing them seated cross-legged on a bright red floor in oversized black streetwear with a left-ear earring. It specifies cinematic, dramatic overhead lighting that casts long shadows, arranges several best-selling novels neatly around the subject, and adds a small, subtle transparent text element in a bottom corner, resulting in a modern, high-detail fashion-editorial composition without logos, watermarks, or stylistic drift into non-photorealistic genres.
skillVersionId: 01999f12-7b50-7741-81b7-4ca7e1c186e8
---

## What it does

This prompt instructs an image model to generate a hyper-realistic, magazine-style 8K editorial portrait from a top-down, slightly diagonal viewpoint, preserving the subject’s identity and natural features while placing them seated cross-legged on a bright red floor in oversized black streetwear with a left-ear earring. It specifies cinematic, dramatic overhead lighting that casts long shadows, arranges several best-selling novels neatly around the subject, and adds a small, subtle transparent text element in a bottom corner, resulting in a modern, high-detail fashion-editorial composition without logos, watermarks, or stylistic drift into non-photorealistic genres.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `accessory` | Optional | Small detail items or jewelry worn by the subject | `silver earring, subtle ring, minimal necklace` |
| `outfit_style` | Optional | Defines what the subject is wearing. Choose clothing style and color that match the editorial mood. | `black T-shirt, loose black pants, sneakers` |
| `prop_details` | Optional | Objects placed around the subject to complete the editorial scene. | `best-selling novels, magazines, notebooks, art books` |
| `text_overlay` | Optional | Short text element added as a transparent caption or label. | `minimal signature, small logo text, subtle corner note` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | your portrait photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
    - `accessory` (default: `silver earring, subtle ring, minimal necklace`)
  - `outfit_style` (default: `black T-shirt, loose black pants, sneakers`)
  - `prop_details` (default: `best-selling novels, magazines, notebooks, art books`)
  - `text_overlay` (default: `minimal signature, small logo text, subtle corner note`)
- Required images:
  - **Exactly 1** images: image 1 (your portrait photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (your portrait photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01999f12-7b50-7741-81b7-4ca7e1c186e8`).

Command form:

```bash
betterprompt generate 01999f12-7b50-7741-81b7-4ca7e1c186e8 \
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
betterprompt generate 01999f12-7b50-7741-81b7-4ca7e1c186e8 \
  --input 'accessory=silver earring, subtle ring, minimal necklace' \
  --input 'outfit_style=black T-shirt, loose black pants, sneakers' \
  --input 'prop_details=best-selling novels, magazines, notebooks, art books' \
  --input 'text_overlay=minimal signature, small logo text, subtle corner note' \
  --image-input-url https://example.com/image1.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
