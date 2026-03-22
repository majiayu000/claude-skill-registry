---
name: weekly-stakeholder-report-template-generator
description: This prompt instructs the AI to act as a business communications specialist and produce a reusable, executive-friendly weekly project status report email template in markdown. It uses provided project and recipient details to pre-fill the subject, greeting, and closing, and outputs a clearly structured, scannable report body with labeled sections (progress, achievements, blockers, upcoming priorities, metrics, and notes) containing bracketed placeholders so the template can be quickly completed and reused each week.
skillVersionId: 01971084-12bb-7ee2-aca3-7542e10e6a53
---

## What it does

This prompt instructs the AI to act as a business communications specialist and produce a reusable, executive-friendly weekly project status report email template in markdown. It uses provided project and recipient details to pre-fill the subject, greeting, and closing, and outputs a clearly structured, scannable report body with labeled sections (progress, achievements, blockers, upcoming priorities, metrics, and notes) containing bracketed placeholders so the template can be quickly completed and reused each week.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Sender_Name` | Required |  | (none) |
| `Project_Name` | Required |  | (none) |
| `Recipient_Names` | Required |  | (none) |
| `Week_Start_Date` | Required |  | (none) |



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
    - `Sender_Name`
  - `Project_Name`
  - `Recipient_Names`
  - `Week_Start_Date`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `01971084-12bb-7ee2-aca3-7542e10e6a53`).

Command form:

```bash
betterprompt generate 01971084-12bb-7ee2-aca3-7542e10e6a53 \
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
betterprompt generate 01971084-12bb-7ee2-aca3-7542e10e6a53 \
  --input Sender_Name=<value> \
  --input Project_Name=<value> \
  --input Recipient_Names=<value> \
  --input Week_Start_Date=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```
