---
name: prompt-exec
license: MIT
description: >
  Execute the forged prompt exactly as written. Requires explicit consent
  and a ready artifact. Deletes artifact after successful execution.
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
    - exec.sh
    - exec.ps1
    - validate.sh
    - help.sh
  assets:
    - assets/prompt-artifact-schema.md
    - assets/prompt-artifact-schema.json
    - assets/receipt-schema.json
    - assets/observability-template.md
  artifacts:
    - .prompt/receipts/
  keywords:
    - prompt
    - execute
    - run
    - proceed
    - go
---

# INSTRUCTIONS

1. Refer to `metadata.references` for the complete skill definition.
2. Use individual scripts: `exec.sh`, `validate.sh`, `help.sh`
