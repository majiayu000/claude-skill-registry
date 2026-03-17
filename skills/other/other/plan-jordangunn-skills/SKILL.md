---
name: plan
description: >
  Orchestrator skill for the `plan` skillset. Dispatches to member skills in a safe, predictable order.
metadata:
  author: Jordan Godau
  version: 0.1.0

  # Strict structure (convention). Agents/tools may parse this.
  skillset:
    name: plan
    schema_version: 1
    skills:
      - plan-create
      - plan-exec
      - plan-status

    # Shared resources directory for skillset assets, scripts, and references
    resources:
      root: .resources
      assets: []
      scripts: []
      references: 
        - DEFINITIONS.md
        - FRONTMATTER.md

    # Chaining defaults/rules
    pipelines:
      default:
        - plan-create
        - plan-exec
      allowed:
        - [plan-exec]
        - [plan-create]
        - [plan-status]
        - [plan-create, plan-exec]

    # Dependencies assumed or provisioned (implementation TBD)
    requires: []

---
