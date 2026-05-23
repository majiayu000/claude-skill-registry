---
description: Initialize BMAD config and directory structure for a project
user-invocable: true
---

# BMAD Initialization

**Goal:** Set up BMAD Method structure in the current project.

## Initialization Steps

1. **Create directory structure:**

   ```text
   bmad/
   ├── config.yaml          # Project configuration
   └── agent-overrides/     # Optional agent customizations

   planning-artifacts/
   ├── workflow-status.yaml # Workflow progress tracking
   └── (generated docs)

   implementation-artifacts/
   └── stories/             # Story files during implementation
   ```

2. **Collect project information:**
   - Project name
   - Project type (web-app, mobile-app, api, library, game, other)
   - Project level:
     - Level 0: Single atomic change (1 story)
     - Level 1: Small feature (1-10 stories)
     - Level 2: Medium feature set (5-15 stories)
     - Level 3: Complex integration (12-40 stories)
     - Level 4: Enterprise expansion (40+ stories)

3. **Create project config** (`bmad/config.yaml`):

   ```yaml
   project_name: { collected }
   project_type: { collected }
   project_level: { collected }
   user_name: { from system or ask }
   user_skill_level: intermediate
   communication_language: English
   document_output_language: English
   planning_artifacts: ./planning-artifacts
   implementation_artifacts: ./implementation-artifacts
   project_knowledge: ./docs
   ```

4. **Create workflow status** (`planning-artifacts/workflow-status.yaml`):

   ```yaml
   project: { project_name }
   level: { project_level }
   last_updated: { timestamp }

   phases:
     analysis:
       product-brief: not-started
       research: not-started
     planning:
       prd: { required if level >= 2, else optional }
       tech-spec: { required if level <= 1, else optional }
       ux-design: optional
     solutioning:
       architecture: { required if level >= 2, else optional }
       epics-stories: not-started
     implementation:
       sprint-planning: not-started
       current-sprint: null
   ```

5. **Confirm initialization:**

   ```text
   ✓ BMAD Method initialized!

   Project: {project_name}
   Type: {project_type}
   Level: {project_level}

   Configuration: bmad/config.yaml
   Status tracking: planning-artifacts/workflow-status.yaml

   Recommended next step: {based on level}
   ```

6. **Recommend next workflow** based on project level:
   - Level 0-1: `/bmad:product-brief` or `/bmad:quick-spec`
   - Level 2+: `/bmad:product-brief` → `/bmad:create-prd`

## Usage

```bash
/bmad:init
```

The command will interactively guide you through project setup.
