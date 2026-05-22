---
name: ultimate-email-marketing-prompt-guide-easy-to-use-highly-effective
description: This prompt instructs the AI to generate a polished, warmly written email marketing campaign aimed at loyal customers for a customizable business, using gratitude, floral-themed emotional language, and a limited-time discount to drive urgent purchases. The result is a complete email package—including subject line, preview text, and a cleanly structured body with a clear call-to-action—featuring tasteful floral emojis, elegant design guidance, and multiple personalization placeholders (customer name, business name, discount/promotion details, and offer end date) so the message feels tailored and on-brand.
skillVersionId: 0196e7ed-a644-7005-a1e3-bccbeff2c47f
---

## What it does

This prompt instructs the AI to generate a polished, warmly written email marketing campaign aimed at loyal customers for a customizable business, using gratitude, floral-themed emotional language, and a limited-time discount to drive urgent purchases. The result is a complete email package—including subject line, preview text, and a cleanly structured body with a clear call-to-action—featuring tasteful floral emojis, elegant design guidance, and multiple personalization placeholders (customer name, business name, discount/promotion details, and offer end date) so the message feels tailored and on-brand.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `promotion` | Required |  | (none) |
| `Business_name` | Required |  | (none) |
| `Business_field` | Required |  | (none) |
| `offer_valid_until` | Required |  | (none) |



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
    - `promotion`
  - `Business_name`
  - `Business_field`
  - `offer_valid_until`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1`** and its available options. Look up `gpt-4.1` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0196e7ed-a644-7005-a1e3-bccbeff2c47f`).

Command form:

```bash
betterprompt generate 0196e7ed-a644-7005-a1e3-bccbeff2c47f \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-4.1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 0196e7ed-a644-7005-a1e3-bccbeff2c47f \
  --input promotion=<value> \
  --input Business_name=<value> \
  --input Business_field=<value> \
  --input offer_valid_until=<value> \
  --model gpt-4.1 \
  --options '{}'
```
