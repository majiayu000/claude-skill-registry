---
name: embry-config
description: Read and explain Embry OS configuration from embry.yaml
triggers:
  - "embry config"
  - "show config"
  - "what are the settings"
allowed-tools:
  - Read

provides:
  - embry-config
composes: [, task-monitor]
---

# Embry Config

Read and explain the Embry OS configuration from `embry.yaml`.

## Steps

1. Read `embry.yaml` from the project root
2. Parse and explain each section:
   - **version** — Config schema version
   - **environment** — Theme setting (office/industrial/home)
   - **services** — Socket paths and connection details for all 6 daemons
   - **airgap** — Whether air-gap mode is enabled (all inference local)
   - **skills** — Skill discovery paths and Memory First enforcement
   - **persona** — Default persona, voice, humor, and register settings
   - **modes** — Distance mode timeouts (idle, launcher dismiss)
3. Highlight any non-default or notable settings
4. If the user asks about a specific setting, focus on that section
