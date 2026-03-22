---
name: productivity-coach-and-reduced-procrastination
description: This prompt instructs the AI to act as a productivity coach who analyzes the user’s listed tasks to diagnose common procrastination drivers (such as ambiguity, aversion, overload, or perfectionism) and then produces a practical, step-by-step execution plan. The output includes an immediate 10-minute starter action, task breakdowns into 15–45 minute time blocks with If–Then implementation intentions, a prioritized sequence emphasizing urgent and important items, specific environment and distraction-control rules, and a simple contingency plan for setbacks. It concludes with a daily check-in template and a small set of measurable success metrics to track progress and consistency.
skillVersionId: 019a29d2-8584-78a0-b0aa-4746bd1e461e
---

## What it does

This prompt instructs the AI to act as a productivity coach who analyzes the user’s listed tasks to diagnose common procrastination drivers (such as ambiguity, aversion, overload, or perfectionism) and then produces a practical, step-by-step execution plan. The output includes an immediate 10-minute starter action, task breakdowns into 15–45 minute time blocks with If–Then implementation intentions, a prioritized sequence emphasizing urgent and important items, specific environment and distraction-control rules, and a simple contingency plan for setbacks. It concludes with a daily check-in template and a small set of measurable success metrics to track progress and consistency.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Your_tasks` | Required |  | (none) |



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
    - `Your_tasks`
- Optional: model and options.
  - Present the human with the default model **`gpt-5`** and its available options. Look up `gpt-5` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"reasoningEffort":"low"}`.
  - If the human does not specify, defaults are used: model `gpt-5`, options `{"reasoningEffort":"low"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019a29d2-8584-78a0-b0aa-4746bd1e461e`).

Command form:

```bash
betterprompt generate 019a29d2-8584-78a0-b0aa-4746bd1e461e \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-5`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"reasoningEffort":"low"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019a29d2-8584-78a0-b0aa-4746bd1e461e \
  --input Your_tasks=<value> \
  --model gpt-5 \
  --options '{"reasoningEffort":"low"}'
```
