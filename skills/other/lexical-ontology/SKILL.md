---
name: refactor-lexical-ontology
license: MIT
description: |
  Audit identifiers and namespaces for lexical-semantic and ontological correctness.
  Detect semantic role misalignment (agent/tool/process/artifact), derivational misuse
  (e.g., -er agent nouns), and category errors between modules, packages, classes,
  functions, and data artifacts. Output a single Markdown report with actionable fixes.
metadata:
  author: Jordan Godau
  references:
    - 01_INTENT.md
    - 02_PRECONDITONS.md
    - 03_RULES.md
    - 04_PROCEDURE.md
    - 05_OUTPUT.md
  keywords:
    - naming
    - ontology
    - lexical
    - semantic
    - agent
    - process
    - artifact
    - suffix
    - convention
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- The user says: "naming feels off", "planner vs planning", "module naming convention",
  "agentive suffix misuse", "semantic role mismatch", "ontology drift", "lexical audit"
- A naming refactor is planned or ongoing
- Confusion exists between *thing* vs *doer* vs *process* vs *tool* in identifiers
- The codebase has inconsistent conventions between directories/modules/classes/functions

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PRECONDITIONS.md`
- `03_RULES.md`
- `04_PROCEDURE.md`
- `05_OUTPUT.md`

## Scripts

If scripts are present, also read `scripts/INDEX.md` and follow any automated steps first.
