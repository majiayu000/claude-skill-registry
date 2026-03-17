---
name: md-split
description: >
  Splits a Markdown file by H2 headings into numbered documents, generates
  .INDEX.md, and scaffolds .SUMMARY.md workflow.
metadata:
  author: Jordan Godau
  version: 0.1.0
  references:
    - 00_INSTRUCTIONS.md
    - 01_INTENT.md
    - 02_PRECONDITIONS.md
    - 03_SCRIPTS.md
    - 04_PROCEDURE.md
    - 05_EDGE_CASES.md
    - 06_TEMPLATES.md
  scripts:
    - scripts/split.sh
    - scripts/split.ps1
    - scripts/index/index.sh
    - scripts/index/index.ps1
  assets:
    - assets/EXAMPLE.md
  keywords:
    - markdown
    - split
    - chunking
    - docs
---
