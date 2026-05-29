---
name: software-project-specification-generator
description: This prompt instructs the AI to produce a structured, developer-ready software feature specification for a given project by summarizing the project’s purpose and audience, enumerating and detailing core features, defining the intended technology stack, and capturing performance and security requirements. The expected outcome is a clear, technical document that stakeholders and engineers can use to align on scope, implementation expectations, and non-functional requirements.
skillVersionId: 0197c4d0-d645-7f24-81c9-864a98b753f6
---

## What it does

This prompt instructs the AI to produce a structured, developer-ready software feature specification for a given project by summarizing the project’s purpose and audience, enumerating and detailing core features, defining the intended technology stack, and capturing performance and security requirements. The expected outcome is a clear, technical document that stakeholders and engineers can use to align on scope, implementation expectations, and non-functional requirements.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Tech_stack` | Required |  | (none) |
| `Key_features` | Required |  | (none) |
| `Project_name` | Required |  | (none) |
| `Target_audience` | Required |  | (none) |
| `Security_considerations` | Required |  | (none) |
| `Performance_requirements` | Required |  | (none) |



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
    - `Tech_stack`
  - `Key_features`
  - `Project_name`
  - `Target_audience`
  - `Security_considerations`
  - `Performance_requirements`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0197c4d0-d645-7f24-81c9-864a98b753f6`).

Command form:

```bash
betterprompt generate 0197c4d0-d645-7f24-81c9-864a98b753f6 \
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
betterprompt generate 0197c4d0-d645-7f24-81c9-864a98b753f6 \
  --input Tech_stack=<value> \
  --input Key_features=<value> \
  --input Project_name=<value> \
  --input Target_audience=<value> \
  --input Security_considerations=<value> \
  --input Performance_requirements=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
