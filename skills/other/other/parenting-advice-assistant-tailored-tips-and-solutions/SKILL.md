---
name: parenting-advice-assistant-tailored-tips-and-solutions
description: This prompt instructs the AI to act as an expert parenting coach and generate age-appropriate, tailored guidance for a specific child behavior challenge, using the provided age, context, desired outcome, and preferred parenting style. The output is a clearly organized plan that explains likely developmental reasons for the behavior, offers 3–5 practical strategies grounded in positive reinforcement and consistency, provides ready-to-use phrases for parent–child conversations, and suggests relevant follow-up resources, concluding with a brief summary and noting that approaches may need adjustment for the individual child.
skillVersionId: 0197c3c3-86c0-73d8-bef4-62636c775bb0
---

## What it does

This prompt instructs the AI to act as an expert parenting coach and generate age-appropriate, tailored guidance for a specific child behavior challenge, using the provided age, context, desired outcome, and preferred parenting style. The output is a clearly organized plan that explains likely developmental reasons for the behavior, offers 3–5 practical strategies grounded in positive reinforcement and consistency, provides ready-to-use phrases for parent–child conversations, and suggests relevant follow-up resources, concluding with a brief summary and noting that approaches may need adjustment for the individual child.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Behavior` | Required |  | (none) |
| `Child's Age` | Required |  | (none) |
| `Desired Outcome` | Required |  | (none) |
| `Parenting Style` | Required |  | (none) |
| `Additional Information` | Required |  | (none) |



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
    - `Behavior`
  - `Child's Age`
  - `Desired Outcome`
  - `Parenting Style`
  - `Additional Information`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0197c3c3-86c0-73d8-bef4-62636c775bb0`).

Command form:

```bash
betterprompt generate 0197c3c3-86c0-73d8-bef4-62636c775bb0 \
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
betterprompt generate 0197c3c3-86c0-73d8-bef4-62636c775bb0 \
  --input Behavior=<value> \
  --input Child's Age=<value> \
  --input Desired Outcome=<value> \
  --input Parenting Style=<value> \
  --input Additional Information=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
