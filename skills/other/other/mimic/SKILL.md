---
name: mimic
license: MIT
description: |
  Persona overlay skill. Applies stylistic transforms to prose output.
  Slot: assets/persona/spec.yaml | Library: assets/library/ | Schema: assets/schema.yaml
metadata:
  author: Jordan Godau
  version: 3.0.0
  scripts:
    validate: scripts/validate.sh
    load: scripts/load.sh
    eject: scripts/eject.sh
    list: scripts/list.sh
  references:
    - references/00_PROTOCOL.md
    - references/01_GUARDRAILS.md
    - references/02_ORCHESTRATION.md
    - references/03_TRUE_FORM.md
    - references/04_ACTIVATION.md
  keywords:
    - mimic
    - persona
    - overlay
---
