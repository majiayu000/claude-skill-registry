---
name: task
description: >
  Orchestrator skill for the `task` skillset. Standardizes task creation and lifecycle
  control with explicit validation, chronological awareness, and deterministic integrity.
metadata:
  author: Jordan Godau
  version: 0.1.0

  skillset:
    name: task
    schema_version: 1
    skills:
      - task-create
      - task-validate
      - task-review
      - task-activate
      - task-invalidate
      - task-status
      - task-list
      - task-next
      - task-prev

    resources:
      root: .resources
      assets:
        - schemas/task.frontmatter.schema.json
        - schemas/task.hash.schema.json
        - schemas/task.schema.json
        - schemas/task.00_TASK.template.md
      scripts:
        - time.py
        - timedelta.py
        - task_intent_extract.py
        - task_hash.py
        - task_status.py
        - task_list.py
        - task_nav.py
      references:
        - README.md
        - USAGE.md

    pipelines:
      default:
        - task-create
        - task-validate
        - task-activate
      allowed:
        - [task-create]
        - [task-validate]
        - [task-review]
        - [task-activate]
        - [task-invalidate]
        - [task-status]
        - [task-list]
        - [task-next]
        - [task-prev]
        - [task-create, task-validate]
        - [task-create, task-validate, task-activate]
        - [task-review, task-activate]

    requires: []

---
