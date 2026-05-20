---
name: create-cartoon-image
description: Design a charming, hand-drawn cartoon illustration of an office scene that incorporates Chinese cultural elements and symbolism.
skillVersionId: 01971b93-89bf-760f-aaab-8d9415d2b709
---

## What it does

This prompt directs an image model to generate a playful, hand-drawn cartoon infographic of a specific office, depicting two employees at desks and an adjacent break room while visually incorporating five color-coded objects that symbolize the traditional Chinese elements. The result is a soft pastel, clean-line illustration with a Chinese-inspired atmosphere, practical office details (like a calendar and file organizer), and clear English callouts that annotate the office’s benefits.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `office_name` | Optional | test | `Feng Shui-inspired` |



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
    - `office_name` (default: `Feng Shui-inspired`)
- Optional: model and options.
  - Present the human with the default model **`imagen-3.0-generate-002`** and its available options. Look up `imagen-3.0-generate-002` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"aspectRatio":"9:16"}`.
  - If the human does not specify, defaults are used: model `imagen-3.0-generate-002`, options `{"aspectRatio":"9:16"}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01971b93-89bf-760f-aaab-8d9415d2b709`).

Command form:

```bash
betterprompt generate 01971b93-89bf-760f-aaab-8d9415d2b709 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`imagen-3.0-generate-002`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"aspectRatio":"9:16"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 01971b93-89bf-760f-aaab-8d9415d2b709 \
  --input 'office_name=Feng Shui-inspired' \
  --model imagen-3.0-generate-002 \
  --options '{"aspectRatio":"9:16"}'
```
