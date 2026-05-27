---
name: brand-x-celebration-minimalist-poster-design-prompt
description: This prompt instructs the AI to act as a creative visual strategist and produce an original minimalist poster concept that leverages negative space to express emotion, symbolism, and brand identity. Using provided inputs for the business name, product or service, occasion or holiday, and message or tagline, it outputs a structured concept detailing the occasion, a negative-space-driven visual idea, a two-color palette with strong contrast, a fitting tagline, and concise style notes to ensure the result is clever, resonant, and non-cliché.
skillVersionId: 01982c71-1356-75cd-802f-f0f4f6343ff1
---

## What it does

This prompt instructs the AI to act as a creative visual strategist and produce an original minimalist poster concept that leverages negative space to express emotion, symbolism, and brand identity. Using provided inputs for the business name, product or service, occasion or holiday, and message or tagline, it outputs a structured concept detailing the occasion, a negative-space-driven visual idea, a two-color palette with strong contrast, a fitting tagline, and concise style notes to ensure the result is clever, resonant, and non-cliché.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Main_Product` | Required |  | (none) |
| `Business_Name` | Required |  | (none) |
| `Message_or_Tagline` | Required |  | (none) |
| `Occasion_or_Holiday` | Required |  | (none) |



### Models and options

This skill's modality is: **`text`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"text"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "text"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:


- Required text inputs:
    - `Main_Product`
  - `Business_Name`
  - `Message_or_Tagline`
  - `Occasion_or_Holiday`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01982c71-1356-75cd-802f-f0f4f6343ff1`).

Command form:

```bash
betterprompt generate 01982c71-1356-75cd-802f-f0f4f6343ff1 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-4.1-mini`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 01982c71-1356-75cd-802f-f0f4f6343ff1 \
  --input Main_Product=<value> \
  --input Business_Name=<value> \
  --input Message_or_Tagline=<value> \
  --input Occasion_or_Holiday=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
