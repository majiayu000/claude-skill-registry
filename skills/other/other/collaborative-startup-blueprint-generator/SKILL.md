---
name: collaborative-startup-blueprint-generator
description: This prompt instructs the AI to act as a lean startup strategist who uses your personal constraints and preferences (skills, budget, available time, interests, goals, and risk tolerance) to propose 2–3 tailored startup ideas. For each idea, it delivers a practical snapshot—what it is, why it matches you, estimated startup costs, target customers, and revenue model—then ends by asking you to choose one idea to develop further toward MVP, marketing, and launch.
skillVersionId: 0197d3b7-62d6-7f31-905d-ca8e7bba93e5
---

## What it does

This prompt instructs the AI to act as a lean startup strategist who uses your personal constraints and preferences (skills, budget, available time, interests, goals, and risk tolerance) to propose 2–3 tailored startup ideas. For each idea, it delivers a practical snapshot—what it is, why it matches you, estimated startup costs, target customers, and revenue model—then ends by asking you to choose one idea to develop further toward MVP, marketing, and launch.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Goal` | Required |  | (none) |
| `your_budget` | Required |  | (none) |
| `your_skills` | Required |  | (none) |
| `Risk_tolerance` | Required |  | (none) |
| `industries_you_care_about` | Required |  | (none) |
| `Weekly_time_you_can_commit` | Required |  | (none) |



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
    - `Goal`
  - `your_budget`
  - `your_skills`
  - `Risk_tolerance`
  - `industries_you_care_about`
  - `Weekly_time_you_can_commit`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0197d3b7-62d6-7f31-905d-ca8e7bba93e5`).

Command form:

```bash
betterprompt generate 0197d3b7-62d6-7f31-905d-ca8e7bba93e5 \
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
betterprompt generate 0197d3b7-62d6-7f31-905d-ca8e7bba93e5 \
  --input Goal=<value> \
  --input your_budget=<value> \
  --input your_skills=<value> \
  --input Risk_tolerance=<value> \
  --input industries_you_care_about=<value> \
  --input Weekly_time_you_can_commit=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
