---
name: generate-50-personalized-english-vocabulary-words
description: This prompt asks the AI to act as an English instructor and generate 50 two-sided flashcards tailored to the learner’s level, goal, and chosen topic focus. The flashcards’ fronts present key English concepts or terms, and the backs provide brief explanations plus a memorable image idea or example to aid recall. The outcome is a curated set of basic-to-intermediate English learning cards designed for efficient study and preparation for the specified purpose.
skillVersionId: 01975428-bf51-739a-bf18-38cd18fed90b
---

## What it does

This prompt asks the AI to act as an English instructor and generate 50 two-sided flashcards tailored to the learner’s level, goal, and chosen topic focus. The flashcards’ fronts present key English concepts or terms, and the backs provide brief explanations plus a memorable image idea or example to aid recall. The outcome is a curated set of basic-to-intermediate English learning cards designed for efficient study and preparation for the specified purpose.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `level` | Required |  | (none) |
| `topic` | Required |  | (none) |
| `purpose` | Required |  | (none) |



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
    - `level`
  - `topic`
  - `purpose`
- Optional: model and options.
  - Present the human with the default model **`gpt-4o`** and its available options. Look up `gpt-4o` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4o`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01975428-bf51-739a-bf18-38cd18fed90b`).

Command form:

```bash
betterprompt generate 01975428-bf51-739a-bf18-38cd18fed90b \
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
betterprompt generate 01975428-bf51-739a-bf18-38cd18fed90b \
  --input level=<value> \
  --input topic=<value> \
  --input purpose=<value> \
  --model gpt-4o \
  --options '{}'
```
