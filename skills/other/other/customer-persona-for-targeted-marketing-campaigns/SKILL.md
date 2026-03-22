---
name: customer-persona-for-targeted-marketing-campaigns
description: This prompt takes a set of persona attributes (demographics, lifestyle, motivations, behaviors, influences, and pain points) and uses them to construct a coherent marketing customer profile that can guide campaign targeting and messaging, with the intended outcome of producing a visual illustration that depicts only the persona as an image without any accompanying text.
skillVersionId: 0198d0d2-355f-7448-8311-f34e49e280fb
---

## What it does

This prompt takes a set of persona attributes (demographics, lifestyle, motivations, behaviors, influences, and pain points) and uses them to construct a coherent marketing customer profile that can guide campaign targeting and messaging, with the intended outcome of producing a visual illustration that depicts only the persona as an image without any accompanying text.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `age` | Required |  | (none) |
| `name` | Required |  | (none) |
| `gender` | Required |  | (none) |
| `income` | Required |  | (none) |
| `location` | Required |  | (none) |
| `lifestyle` | Required |  | (none) |
| `occupation` | Required |  | (none) |
| `pain_points` | Required |  | (none) |
| `main_motivation` | Required |  | (none) |
| `shopping_behavior` | Required |  | (none) |
| `consumption_habits` | Required |  | (none) |
| `influencing_factors` | Required |  | (none) |
| `relationship_status` | Required |  | (none) |



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


- Required text inputs:
    - `age`
  - `name`
  - `gender`
  - `income`
  - `location`
  - `lifestyle`
  - `occupation`
  - `pain_points`
  - `main_motivation`
  - `shopping_behavior`
  - `consumption_habits`
  - `influencing_factors`
  - `relationship_status`
- Optional: model and options.
  - Present the human with the default model **`gpt-image-1`** and its available options. Look up `gpt-image-1` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"image":{"quality":1},"quality":"medium"}`.
  - If the human does not specify, defaults are used: model `gpt-image-1`, options `{"image":{"quality":1},"quality":"medium"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0198d0d2-355f-7448-8311-f34e49e280fb`).

Command form:

```bash
betterprompt generate 0198d0d2-355f-7448-8311-f34e49e280fb \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-image-1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"image":{"quality":1},"quality":"medium"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 0198d0d2-355f-7448-8311-f34e49e280fb \
  --input age=<value> \
  --input name=<value> \
  --input gender=<value> \
  --input income=<value> \
  --input location=<value> \
  --input lifestyle=<value> \
  --input occupation=<value> \
  --input pain_points=<value> \
  --input main_motivation=<value> \
  --input shopping_behavior=<value> \
  --input consumption_habits=<value> \
  --input influencing_factors=<value> \
  --input relationship_status=<value> \
  --model gpt-image-1 \
  --options '{"image":{"quality":1},"quality":"medium"}'
```
