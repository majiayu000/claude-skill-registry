---
name: yes-or-no
description: This prompt sets up an AI feng shui advisor that, given a specific planned activity plus the user’s date and birth details and city, calculates a weighted confidence score and outputs a locale-appropriate recommendation as “should do” vs “should not do” percentages first, followed by a brief rationale and practical tips such as favorable time windows, directions, colors, and alternative better dates, while explicitly noting assumptions when data is missing and keeping the guidance non-harmful and for reference only.
skillVersionId: 01996181-4975-729e-b6db-3c5e513b7715
---

## What it does

This prompt sets up an AI feng shui advisor that, given a specific planned activity plus the user’s date and birth details and city, calculates a weighted confidence score and outputs a locale-appropriate recommendation as “should do” vs “should not do” percentages first, followed by a brief rationale and practical tips such as favorable time windows, directions, colors, and alternative better dates, while explicitly noting assumptions when data is missing and keeping the guidance non-harmful and for reference only.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `City` | Optional | City Location | `Ho Chi Minh` |
| `gender` | Optional | male/female/unknown | `male` |
| `Current_day` | Optional | YYYY-MM-DD | `2025-09-19` |
| `birthday_day` | Optional | YYYY-MM-DD | `2004-01-06` |
| `birthday_time` | Optional | HH:mm hoặc unknown | `unknown` |
| `describe_the_intended_work` | Optional | The job you are hesitant about | `eat chicken in mcdonald` |



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

- Optional text inputs (use defaults if not provided by the human):
    - `City` (default: `Ho Chi Minh`)
  - `gender` (default: `male`)
  - `Current_day` (default: `2025-09-19`)
  - `birthday_day` (default: `2004-01-06`)
  - `birthday_time` (default: `unknown`)
  - `describe_the_intended_work` (default: `eat chicken in mcdonald`)
- Optional: model and options.
  - Present the human with the default model **`gpt-5`** and its available options. Look up `gpt-5` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-5`, options `{}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01996181-4975-729e-b6db-3c5e513b7715`).

Command form:

```bash
betterprompt generate 01996181-4975-729e-b6db-3c5e513b7715 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-5`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 01996181-4975-729e-b6db-3c5e513b7715 \
  --input 'City=Ho Chi Minh' \
  --input gender=male \
  --input Current_day=2025-09-19 \
  --input birthday_day=2004-01-06 \
  --input birthday_time=unknown \
  --input 'describe_the_intended_work=eat chicken in mcdonald' \
  --model gpt-5 \
  --options '{}'
```
