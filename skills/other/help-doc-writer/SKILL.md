---
name: help-doc-writer
description: Produce a concise Markdown outline for a help-center article based on a given topic and context, adhering to strict style, content, and structure rules without inventing details.
skillVersionId: 019a4f2e-f796-755e-8d3c-0bb6efef7f81
---

## What it does

This prompt instructs the AI to produce a concise, skimmable Help Center article outline in Markdown for a provided topic, using only details explicitly supplied in the accompanying context. The result is a structured set of headings and short procedural steps written in second-person voice, with bolded UI labels, per-step outcome checks, optional screenshot placeholders only when referenced, and practical Troubleshooting and FAQ sections that avoid inventing product-specific information.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `topic` | Required |  | (none) |
| `additional_context` | Required |  | (none) |



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
    - `topic`
  - `additional_context`
- Optional: model and options.
  - Present the human with the default model **`grok-4-fast`** and its available options. Look up `grok-4-fast` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"reasoningEffort":"low"}`.
  - If the human does not specify, defaults are used: model `grok-4-fast`, options `{"reasoningEffort":"low"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019a4f2e-f796-755e-8d3c-0bb6efef7f81`).

Command form:

```bash
betterprompt generate 019a4f2e-f796-755e-8d3c-0bb6efef7f81 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`grok-4-fast`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"reasoningEffort":"low"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019a4f2e-f796-755e-8d3c-0bb6efef7f81 \
  --input topic=<value> \
  --input additional_context=<value> \
  --model grok-4-fast \
  --options '{"reasoningEffort":"low"}'
```
