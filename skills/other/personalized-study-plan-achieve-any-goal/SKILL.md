---
name: personalized-study-plan-achieve-any-goal
description: This prompt asks the AI to generate a structured, stage-by-stage study plan tailored to your career, current proficiency, desired goal, and target timeframe, aligned with your academic major and interests. The result is a detailed roadmap with clear objectives per stage, specific daily activities for each relevant skill/aspect (with an estimated hourly schedule), and curated learning resources (books/apps/videos), plus practice tasks and exercises that incorporate topics from your major to keep the learning applied and goal-focused.
skillVersionId: 0196ecfe-4d40-73e0-80fb-68ba03361248
---

## What it does

This prompt asks the AI to generate a structured, stage-by-stage study plan tailored to your career, current proficiency, desired goal, and target timeframe, aligned with your academic major and interests. The result is a detailed roadmap with clear objectives per stage, specific daily activities for each relevant skill/aspect (with an estimated hourly schedule), and curated learning resources (books/apps/videos), plus practice tasks and exercises that incorporate topics from your major to keep the learning applied and goal-focused.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `career` | Required |  | (none) |
| `Desired_goal` | Required |  | (none) |
| `Target_timeframe` | Required |  | (none) |
| `Current_proficiency_level` | Required |  | (none) |



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
    - `career`
  - `Desired_goal`
  - `Target_timeframe`
  - `Current_proficiency_level`
- Optional: model and options.
  - Present the human with the default model **`gpt-4o`** and its available options. Look up `gpt-4o` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4o`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0196ecfe-4d40-73e0-80fb-68ba03361248`).

Command form:

```bash
betterprompt generate 0196ecfe-4d40-73e0-80fb-68ba03361248 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-4o`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 0196ecfe-4d40-73e0-80fb-68ba03361248 \
  --input career=<value> \
  --input Desired_goal=<value> \
  --input Target_timeframe=<value> \
  --input Current_proficiency_level=<value> \
  --model gpt-4o \
  --options '{}'
```
