---
name: lead-gen-campaign-timeline-planner-with-roles-and-dates
description: It instructs the AI to act as a project manager and produce a date-specific, step-by-step implementation timeline for a lead generation campaign for a specified business type running between given start and end dates. The output should map each phase—planning/content creation, platform setup/testing, launch milestones, optimization checkpoints, and final evaluation—to concrete dates and assign accountable roles such as content, ads, and design, presented immediately without any introductory text.
skillVersionId: 01981c88-7dc4-791b-a2e8-efa749e62165
---

## What it does

It instructs the AI to act as a project manager and produce a date-specific, step-by-step implementation timeline for a lead generation campaign for a specified business type running between given start and end dates. The output should map each phase—planning/content creation, platform setup/testing, launch milestones, optimization checkpoints, and final evaluation—to concrete dates and assign accountable roles such as content, ads, and design, presented immediately without any introductory text.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `End_Date` | Required |  | (none) |
| `Start_Date` | Required |  | (none) |
| `Type_of_business` | Required |  | (none) |



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
    - `End_Date`
  - `Start_Date`
  - `Type_of_business`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01981c88-7dc4-791b-a2e8-efa749e62165`).

Command form:

```bash
betterprompt generate 01981c88-7dc4-791b-a2e8-efa749e62165 \
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
betterprompt generate 01981c88-7dc4-791b-a2e8-efa749e62165 \
  --input End_Date=<value> \
  --input Start_Date=<value> \
  --input Type_of_business=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
