---
name: create-ksml
description: Convert project manifests into Kling Shot Markup Language (KSML) for video generation.
triggers:
  - ksml
  - kling shot markup
  - video generation manifest
provides:
  - create-ksml
composes:
  - task-monitor
---

# create-ksml

Standalone skill for generating **KSML v0.1** (Kling Shot Markup Language) from movie scripts or project manifests.

## Features

- **KSML Export**: Generates `project.ksml` YAML files compliant with v0.1 spec.
- **Prompt Compilation**: Compiles structured intent into Kling-optimized prompts.
- **Asset Linking**: Links local image assets (storyboards/keyframes) to shot definitions.

## Usage

```bash
# Convert a script to KSML
/create-ksml convert --script script.json --assets ./assets --output project.ksml
```

## Dependencies

- `pyyaml`
