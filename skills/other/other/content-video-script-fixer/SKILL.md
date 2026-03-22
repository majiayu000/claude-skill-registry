---
name: content-video-script-fixer
description: This prompt instructs the AI to act as a strict, detail-focused marketing manager who reviews a provided video script against a specified topic and explicit video requirements, then delivers a structured, evidence-based critique. The outcome is a blunt but constructive assessment that pinpoints what meets the requirements, what fails or weakens conversion impact, why those issues matter, and exactly how to improve clarity, engagement, and marketing effectiveness—without rewriting the full script unless requested.
skillVersionId: 019afec5-d5f2-706b-a0f2-12a8df09d797
---

## What it does

This prompt instructs the AI to act as a strict, detail-focused marketing manager who reviews a provided video script against a specified topic and explicit video requirements, then delivers a structured, evidence-based critique. The outcome is a blunt but constructive assessment that pinpoints what meets the requirements, what fails or weakens conversion impact, why those issues matter, and exactly how to improve clarity, engagement, and marketing effectiveness—without rewriting the full script unless requested.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Your_topic` | Required |  | (none) |
| `Video_requirements` | Required |  | (none) |
| `Your_content_script` | Required | Put your raw/demo video script here | (none) |



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
    - `Your_topic`
  - `Video_requirements`
  - `Your_content_script`
- Optional: model and options.
  - Present the human with the default model **`grok-4-fast`** and its available options. Look up `grok-4-fast` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"reasoningEffort":"medium"}`.
  - If the human does not specify, defaults are used: model `grok-4-fast`, options `{"reasoningEffort":"medium"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019afec5-d5f2-706b-a0f2-12a8df09d797`).

Command form:

```bash
betterprompt generate 019afec5-d5f2-706b-a0f2-12a8df09d797 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`grok-4-fast`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"reasoningEffort":"medium"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019afec5-d5f2-706b-a0f2-12a8df09d797 \
  --input Your_topic=<value> \
  --input Video_requirements=<value> \
  --input Your_content_script=<value> \
  --model grok-4-fast \
  --options '{"reasoningEffort":"medium"}'
```
