---
name: prompt-forge
license: MIT
description: >
  Shape, refine, and stabilize human intent into a canonical prompt artifact.
  Iteratively clarifies ambiguity until user confirms readiness.
metadata:
  author: Jordan Godau
  version: 0.1.0
  references:
    - 00_ROUTER.md
    - 01_SUMMARY.md
    - 02_CONTRACTS.md
    - 03_TRIGGERS.md
    - 04_NEVER.md
    - 05_ALWAYS.md
    - 06_PROCEDURE.md
    - 07_FAILURES.md
  scripts:
    - forge.sh
    - forge.ps1
    - validate.sh
    - help.sh
  assets:
    - assets/prompt-artifact-schema.md
    - assets/prompt-artifact-schema.json
    - assets/receipt-schema.json
    - assets/observability-template.md
  artifacts:
    - .prompt/active.yaml
  keywords:
    - prompt
    - forge
    - refine
    - clarify
    - intent
    - draft
---

# INSTRUCTIONS

1. Refer to `metadata.references` for the complete skill definition.
2. Use individual scripts: `forge.sh`, `validate.sh`, `help.sh`
