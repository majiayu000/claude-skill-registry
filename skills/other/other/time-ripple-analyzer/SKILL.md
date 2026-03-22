---
name: time-ripple-analyzer
description: This prompt instructs the AI to act as a time travel consultant who evaluates a user-defined historical era and a specific past alteration affecting a key figure or invention, then outlines multiple plausible ripple effects across history, technology, society, and the traveler’s origin timeline. The result is a structured, accessible analysis that connects causal chains, paradoxes, and ethical considerations using both scientific reasoning and speculative imagination, concluding with open-ended questions to encourage further exploration of alternate timelines.
skillVersionId: 019be4cb-a629-733b-b80a-0731bf11cb2e
---

## What it does

This prompt instructs the AI to act as a time travel consultant who evaluates a user-defined historical era and a specific past alteration affecting a key figure or invention, then outlines multiple plausible ripple effects across history, technology, society, and the traveler’s origin timeline. The result is a structured, accessible analysis that connects causal chains, paradoxes, and ethical considerations using both scientific reasoning and speculative imagination, concluding with open-ended questions to encourage further exploration of alternate timelines.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Key_Figure` | Required | The person, group, or invention affected | (none) |
| `Intentional` | Required | Whether the change was intentional or accidental | (none) |
| `Time_Period` | Required | The historical year or era the user travels to | (none) |
| `Altered_Event` | Required | The action or change caused by the user in the past | (none) |



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
    - `Key_Figure`
  - `Intentional`
  - `Time_Period`
  - `Altered_Event`
- Optional: model and options.
  - Present the human with the default model **`grok-4.1-fast`** and its available options. Look up `grok-4.1-fast` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"reasoningEffort":"none"}`.
  - If the human does not specify, defaults are used: model `grok-4.1-fast`, options `{"reasoningEffort":"none"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019be4cb-a629-733b-b80a-0731bf11cb2e`).

Command form:

```bash
betterprompt generate 019be4cb-a629-733b-b80a-0731bf11cb2e \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`grok-4.1-fast`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"reasoningEffort":"none"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019be4cb-a629-733b-b80a-0731bf11cb2e \
  --input Key_Figure=<value> \
  --input Intentional=<value> \
  --input Time_Period=<value> \
  --input Altered_Event=<value> \
  --model grok-4.1-fast \
  --options '{"reasoningEffort":"none"}'
```
