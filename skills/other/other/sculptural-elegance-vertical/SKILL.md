---
name: sculptural-elegance-vertical
description: This prompt instructs an AI image generator to create a vertical 1080×1920 cinematic portrait that preserves the subject’s facial identity while styling them in a black blazer under stark, high-contrast lighting. It guides the composition by specifying a camera angle, a focal emphasis, an intended mood or theme, and a bold background color to heighten contrast with luminous skin and dark clothing. It also defines the subject’s facial expression, resulting in a dramatic, tightly art-directed portrait with consistent features and a clear visual tone.
skillVersionId: 01997ea1-e3a8-7b77-a8f7-7f4174a4b7ef
---

## What it does

This prompt instructs an AI image generator to create a vertical 1080×1920 cinematic portrait that preserves the subject’s facial identity while styling them in a black blazer under stark, high-contrast lighting. It guides the composition by specifying a camera angle, a focal emphasis, an intended mood or theme, and a bold background color to heighten contrast with luminous skin and dark clothing. It also defines the subject’s facial expression, resulting in a dramatic, tightly art-directed portrait with consistent features and a clear visual tone.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `insert_angle` | Optional |  | `slightly low, upward angle` |
| `insert_emphasis` | Optional |  | `jawline and neck` |
| `insert_mood_or_theme` | Optional |  | `quiet dominance and sculptural elegance` |
| `Insert_background_color` | Optional |  | `Deep, saturated crimson red` |
| `insert_facial_expression` | Optional |  | `cackling` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | A portrail photo | `--image-input-url <url>` or `--image-input-base64 <base64>` or `--image-input-path <absolute path to image>` |


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
    - `insert_angle` (default: `slightly low, upward angle`)
  - `insert_emphasis` (default: `jawline and neck`)
  - `insert_mood_or_theme` (default: `quiet dominance and sculptural elegance`)
  - `Insert_background_color` (default: `Deep, saturated crimson red`)
  - `insert_facial_expression` (default: `cackling`)
- Required images:
  - **Exactly 1** images: image 1 (A portrail photo). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (A portrail photo)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01997ea1-e3a8-7b77-a8f7-7f4174a4b7ef`).

Command form:

```bash
betterprompt generate 01997ea1-e3a8-7b77-a8f7-7f4174a4b7ef \
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
betterprompt generate 01997ea1-e3a8-7b77-a8f7-7f4174a4b7ef \
  --input 'insert_angle=slightly low, upward angle' \
  --input 'insert_emphasis=jawline and neck' \
  --input 'insert_mood_or_theme=quiet dominance and sculptural elegance' \
  --input 'Insert_background_color=Deep, saturated crimson red' \
  --input insert_facial_expression=cackling \
  --image-input-url https://example.com/image1.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
