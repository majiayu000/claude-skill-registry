---
name: tracedocs
description: "Turn any codebase into evidence-grounded Markdown docs plus a machine-readable index.json. Every claim cites its source; never invents deployment steps."
category: development-code
---

# tracedocs

Turn any codebase into an evidence-grounded documentation package (overview,
operation, deployment, learning, architecture, API/data, troubleshooting,
maintenance) plus a machine-readable `index.json` for AI agents. Every
operational/deployment claim cites a source file and a confidence label
(Verified / Inferred / Unknown / Needs confirmation); it never invents
deployment steps and records gaps instead.

Full skill, references, templates, and a validated sample output:
https://github.com/wxggzz/tracedocs (MIT).

## When to Use This Skill

- Onboarding to, or documenting, an unfamiliar codebase
- Producing durable, in-repo docs for operation, deployment, and maintenance
- Preparing an AI-agent-ready knowledge handoff (with `index.json`)
- Turning a repo into a study guide whose claims are traceable to source

## What This Skill Does

1. Analyzes the codebase (stack, scripts, entry points, env-var names, deploy
   signals, tests).
2. Builds an evidence map (source map, assumptions, generation log) with
   confidence labels.
3. Writes the Markdown manuals and an `index.json` manifest; never invents
   deployment steps.
4. Runs a quality check (paths exist, commands sourced, no secret values, gaps
   documented).

## How to Use

### Basic Usage

```
Use tracedocs to generate evidence-grounded study docs for this repository. Write the output to study-docs/.
```

## Example

**User**: "Document ./my-app with tracedocs"

The skill scans the repo and writes a `study-docs/` package (00-10 manuals +
`index.json` + `_evidence/`), citing each operational claim's source and
labelling its confidence - and explicitly noting anything it cannot verify
(for example, "no deployment configuration found in the repo").
