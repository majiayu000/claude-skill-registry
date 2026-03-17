---
name: prompt-compile
license: MIT
description: >
  Compile the YAML artifact into PROMPT.md with deterministic structure.
  A final agent pass polishes for fluidity, conciseness, and correctness.
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
    - compile.sh
    - compile.ps1
    - validate.sh
    - help.sh
  assets:
    - assets/prompt-artifact-schema.md
    - assets/prompt-artifact-schema.json
    - assets/receipt-schema.json
    - assets/observability-template.md
  artifacts:
    - .prompt/PROMPT.md
  keywords:
    - prompt
    - compile
    - render
    - markdown
    - output
---

# INSTRUCTIONS

1. Refer to `metadata.references` for the complete skill definition.
2. Use individual scripts: `compile.sh`, `validate.sh`, `help.sh`
