---
name: le-calice
description: Ce prompt demande de générer une image ultra‑réaliste en 4K (16:9) d’un homme dont le visage doit rester parfaitement identique à celui de l’image fournie, intégré dans une scène de temple au trésor façon aventurier‑archéologue. Il précise sa tenue complète, sa pose (remplacer un calice doré par une pierre), l’environnement (portes monumentales, trésors poussiéreux, plantes, racines, stalactites et petits animaux), ainsi que le cadrage, la mise au point, la palette, l’éclairage en clair‑obscur et des contraintes négatives. Le résultat attendu est un plan moyen cinématographique, fortement texturé et contrasté, centré sur son visage concentré et le calice éclairé par un rayon de lumière, sans altérer le visage ni ajouter de nouvelles personnes.
skillVersionId: 019a54bd-9d11-763c-a50e-7eefba9cf37d
---

## What it does

Ce prompt demande de générer une image ultra‑réaliste en 4K (16:9) d’un homme dont le visage doit rester parfaitement identique à celui de l’image fournie, intégré dans une scène de temple au trésor façon aventurier‑archéologue. Il précise sa tenue complète, sa pose (remplacer un calice doré par une pierre), l’environnement (portes monumentales, trésors poussiéreux, plantes, racines, stalactites et petits animaux), ainsi que le cadrage, la mise au point, la palette, l’éclairage en clair‑obscur et des contraintes négatives. Le résultat attendu est un plan moyen cinématographique, fortement texturé et contrasté, centré sur son visage concentré et le calice éclairé par un rayon de lumière, sans altérer le visage ni ajouter de nouvelles personnes.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs



### Models and options

This skill's modality is: **`image`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"image"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "image"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:

- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `019a54bd-9d11-763c-a50e-7eefba9cf37d`).

Command form:

```bash
betterprompt generate 019a54bd-9d11-763c-a50e-7eefba9cf37d \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gemini-2.5-flash-image-preview`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 019a54bd-9d11-763c-a50e-7eefba9cf37d \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```
