---
name: cinematic-overhead-streetwear-portrait
description: This prompt instructs an AI to generate a photorealistic, cinematic overhead streetwear campaign image of a model standing on a zebra crossing, using provided wardrobe and accessory variables to keep styling consistent. It defines a clean, balanced editorial composition with minimal background clutter, tailored for urban fashion lookbooks and brand/magazine use, while enforcing safety rules that avoid nudity, sexualization, and depicting minors in adult styling.
skillVersionId: 01994b44-236f-76bc-8d1a-4bb902d9d4ab
---

## What it does

This prompt instructs an AI to generate a photorealistic, cinematic overhead streetwear campaign image of a model standing on a zebra crossing, using provided wardrobe and accessory variables to keep styling consistent. It defines a clean, balanced editorial composition with minimal background clutter, tailored for urban fashion lookbooks and brand/magazine use, while enforcing safety rules that avoid nudity, sexualization, and depicting minors in adult styling.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `top_style` | Optional | Crop top or shirt style. | `White fitted crop top` |
| `accessories` | Optional | Extra fashion elements like sunglasses, jewelry, bags. | `Black aviator shades, silver chain` |
| `pants_style` | Optional | Style of jeans or bottomwear. | `Loose baggy ripped denim` |
| `sneakers_style` | Optional | Sneaker design or brand vibe. | `Chunky white sneakers` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Upload a clear photo of your face so the AI can keep your identity in the final image. | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
    - `top_style` (default: `White fitted crop top`)
  - `accessories` (default: `Black aviator shades, silver chain`)
  - `pants_style` (default: `Loose baggy ripped denim`)
  - `sneakers_style` (default: `Chunky white sneakers`)
- Required images:
  - **Exactly 1** images: image 1 (Upload a clear photo of your face so the AI can keep your identity in the final image.). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Upload a clear photo of your face so the AI can keep your identity in the final image.)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01994b44-236f-76bc-8d1a-4bb902d9d4ab`).

Command form:

```bash
betterprompt generate 01994b44-236f-76bc-8d1a-4bb902d9d4ab \
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
betterprompt generate 01994b44-236f-76bc-8d1a-4bb902d9d4ab \
  --input 'top_style=White fitted crop top' \
  --input 'accessories=Black aviator shades, silver chain' \
  --input 'pants_style=Loose baggy ripped denim' \
  --input 'sneakers_style=Chunky white sneakers' \
  --image-input-url https://example.com/image1.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
