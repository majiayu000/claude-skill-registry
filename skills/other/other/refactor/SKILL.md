---
name: refactor
description: >
  Orchestrator skill for the `refactor` skillset. Dispatches to member skills
  for code quality audits and structural improvements.
metadata:
  author: Jordan Godau
  version: 0.1.0

  # Strict structure (convention). Agents/tools may parse this.
  skillset:
    name: refactor
    schema_version: 1
    skills:
      - refactor-dictionaries
      - refactor-import-hygiene
      - refactor-inline-complexity
      - refactor-lexical-ontology
      - refactor-module-stutter
      - refactor-squatters
      - refactor-semantic-noise
      - refactor-structural-duplication

    # Shared resources directory for skillset assets, scripts, and references
    resources:
      root: .resources
      assets: []
      scripts: []
      references:
        - OUTPUT_FORMAT.md
        - SEVERITY_LEVELS.md

    # Chaining defaults/rules
    pipelines:
      # Recommended audit sequence: naming → structure → hygiene
      default:
        - refactor-lexical-ontology
        - refactor-module-stutter
        - refactor-squatters
        - refactor-semantic-noise
        - refactor-dictionaries
        - refactor-inline-complexity
        - refactor-import-hygiene
        - refactor-structural-duplication

      # Individual skills can run standalone
      allowed:
        - [refactor-dictionaries]
        - [refactor-import-hygiene]
        - [refactor-inline-complexity]
        - [refactor-lexical-ontology]
        - [refactor-module-stutter]
        - [refactor-semantic-noise]
        - [refactor-structural-duplication]
        - [refactor-squatters]
        # Naming cluster
        - [refactor-lexical-ontology, refactor-module-stutter, refactor-semantic-noise]
        # Post-refactor hygiene
        - [refactor-import-hygiene, refactor-inline-complexity]
        # Structure cluster
        - [refactor-squatters, refactor-structural-duplication]
        # Full audit
        - [refactor-lexical-ontology, refactor-module-stutter, refactor-squatters, refactor-semantic-noise, refactor-dictionaries, refactor-inline-complexity, refactor-import-hygiene, refactor-structural-duplication]

    # Dependencies assumed or provisioned (implementation TBD)
    requires: []

---
