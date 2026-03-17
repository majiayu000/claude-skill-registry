---
name: config-file-explainer
description: Explain a configuration file and its key options. Use when a junior developer is confused by a config file.
---

# Config File Explainer

## Purpose
Explain a configuration file and its key options.

## Inputs to request
- The config file content and file path.
- Target environment or runtime.
- Which behavior needs changing.

## Workflow
1. Summarize the file purpose and major sections.
2. Explain the top options and default values.
3. Point out which options are safe to change.

## Output
- Annotated config summary.

## Quality bar
- Call out risky settings explicitly.
- Keep explanations tied to real outcomes.
