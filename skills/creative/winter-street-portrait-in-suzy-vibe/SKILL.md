---
name: winter-street-portrait-in-suzy-vibe
description: This prompt instructs an image-generation or editing system to take an uploaded person’s photo and produce a photorealistic, cinematic winter street portrait that preserves the subject’s true identity while shifting the scene to a calm, overcast snowy setting. It specifies the desired mood, expression, composition, lens depth-of-field, and film-like color grading, and it automatically adapts wardrobe and styling based on detected gender and a chosen background context. The expected result is a high-resolution vertical portrait with gentle snowfall, subtle bokeh, and a single blue-scarf color accent, maintaining a natural, unposed, emotionally introspective look without celebrity imitation or unrealistic beautification.
skillVersionId: 019a47e6-7e48-7208-ac9b-8970b632dc5a
---

## What it does

This prompt instructs an image-generation or editing system to take an uploaded person’s photo and produce a photorealistic, cinematic winter street portrait that preserves the subject’s true identity while shifting the scene to a calm, overcast snowy setting. It specifies the desired mood, expression, composition, lens depth-of-field, and film-like color grading, and it automatically adapts wardrobe and styling based on detected gender and a chosen background context. The expected result is a high-resolution vertical portrait with gentle snowfall, subtle bokeh, and a single blue-scarf color accent, maintaining a natural, unposed, emotionally introspective look without celebrity imitation or unrealistic beautification.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `gender_detected` | Optional | Automatically identifies whether the subject presents as male or female to adjust outfit styling. | `male/female` |
| `background_context` | Optional | Description of a preferred setting | `European park` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Upload your portrait photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
    - `gender_detected` (default: `male/female`)
  - `background_context` (default: `European park`)
- Required images:
  - **Exactly 1** images: image 1 (Upload your portrait photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Upload your portrait photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019a47e6-7e48-7208-ac9b-8970b632dc5a`).

Command form:

```bash
betterprompt generate 019a47e6-7e48-7208-ac9b-8970b632dc5a \
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
betterprompt generate 019a47e6-7e48-7208-ac9b-8970b632dc5a \
  --input gender_detected=male/female \
  --input 'background_context=European park' \
  --image-input-url https://example.com/image1.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
