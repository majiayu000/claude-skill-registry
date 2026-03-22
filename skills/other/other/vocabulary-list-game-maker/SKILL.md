---
name: vocabulary-list-game-maker
description: 
skillVersionId: 019918cd-120c-77da-b16e-52a1db3086c7
---

## What it does

This prompt instructs the AI to act as a language-teaching assistant and, using the specified language, topic, learner level, age group, and preferred game type, produce a themed set of 10–20 level-appropriate vocabulary items with brief explanations or translations, plus a ready-to-print classroom word game based on that vocabulary and clear steps for teachers to run the activity in class.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `topic` | Optional |  | `auto` |
| `language` | Required | Allowed options: Chinese, English | (none) |
| `age_range` | Optional |  | `14-16` |
| `game_type` | Required | Allowed options: Crossword, Word Search, Memory Cards, Matching Game | (none) |
| `CEFR_level` | Optional |  | `A1` |



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
    - `language`
  - `game_type`
- Optional text inputs (use defaults if not provided by the human):
    - `topic` (default: `auto`)
  - `age_range` (default: `14-16`)
  - `CEFR_level` (default: `A1`)
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019918cd-120c-77da-b16e-52a1db3086c7`).

Command form:

```bash
betterprompt generate 019918cd-120c-77da-b16e-52a1db3086c7 \
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
betterprompt generate 019918cd-120c-77da-b16e-52a1db3086c7 \
  --input topic=auto \
  --input language=Chinese \
  --input age_range=14-16 \
  --input game_type=Crossword \
  --input CEFR_level=A1 \
  --model gpt-4.1-mini \
  --options '{}'
```
