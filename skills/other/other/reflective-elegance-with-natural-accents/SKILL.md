---
name: reflective-elegance-with-natural-accents
description: This prompt directs an image model to generate a high-resolution, hyperrealistic luxury campaign-style product shot by placing a specified product on a glossy reflective surface, enriching it with defined details, and surrounding it with curated ingredients or decorative elements plus a harmonized dynamic splash effect. It specifies soft directional studio lighting, a minimalist gradient background, and a balanced editorial composition to produce a premium, art-directed visual suitable for showcasing high-end products in the chosen category.
skillVersionId: 0197674d-f10c-76ff-80c7-30f59281517f
---

## What it does

This prompt directs an image model to generate a high-resolution, hyperrealistic luxury campaign-style product shot by placing a specified product on a glossy reflective surface, enriching it with defined details, and surrounding it with curated ingredients or decorative elements plus a harmonized dynamic splash effect. It specifies soft directional studio lighting, a minimalist gradient background, and a balanced editorial composition to produce a premium, art-directed visual suitable for showcasing high-end products in the chosen category.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `category` | Required |  | (none) |
| `product_name` | Required |  | (none) |
| `surface_color` | Required |  | (none) |
| `background_color_range` | Required |  | (none) |
| `product_specific_details` | Required |  | (none) |
| `liquid_type_or_abstract_shape` | Required |  | (none) |
| `ingredient_or_decorative_element` | Required |  | (none) |



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
    - `category`
  - `product_name`
  - `surface_color`
  - `background_color_range`
  - `product_specific_details`
  - `liquid_type_or_abstract_shape`
  - `ingredient_or_decorative_element`
- Optional: model and options.
  - Present the human with the default model **`gpt-image-1`** and its available options. Look up `gpt-image-1` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"image":{"quality":1},"quality":"medium"}`.
  - If the human does not specify, defaults are used: model `gpt-image-1`, options `{"image":{"quality":1},"quality":"medium"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0197674d-f10c-76ff-80c7-30f59281517f`).

Command form:

```bash
betterprompt generate 0197674d-f10c-76ff-80c7-30f59281517f \
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
betterprompt generate 0197674d-f10c-76ff-80c7-30f59281517f \
  --input category=<value> \
  --input product_name=<value> \
  --input surface_color=<value> \
  --input background_color_range=<value> \
  --input product_specific_details=<value> \
  --input liquid_type_or_abstract_shape=<value> \
  --input ingredient_or_decorative_element=<value> \
  --model gpt-image-1 \
  --options '{"image":{"quality":1},"quality":"medium"}'
```
