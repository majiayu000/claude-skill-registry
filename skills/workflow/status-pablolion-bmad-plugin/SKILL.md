---
description: Check BMAD project progress and get next-step recommendations
user-invocable: true
---

# BMAD Workflow Status

**Goal:** Display current project status and recommend next workflow.

## Execution Steps

1. **Check for BMAD initialization:**
   - Look for `bmad/config.yaml`
   - If not found: suggest running `/bmad:init`

2. **Load configuration:**
   - Read `bmad/config.yaml` for project info
   - Read `planning-artifacts/workflow-status.yaml` for progress

3. **Display status:**

   ```text
   Project: {project_name} ({project_type}, Level {project_level})

   ✓ Phase 1: Analysis
     ✓ product-brief (planning-artifacts/product-brief-{date}.md)
     - research (optional)

   → Phase 2: Planning [CURRENT]
     ⚠ prd (required - NOT STARTED)
     - ux-design (optional)

   Phase 3: Solutioning
     - architecture (required)
     - epics-stories (not started)

   Phase 4: Implementation
     - sprint-planning (not started)
   ```

4. **Determine recommendations** based on:
   - Project level
   - Completed workflows
   - Required vs optional workflows
   - Workflow dependencies

5. **Recommend next step:**

   ```text
   Recommended: Create PRD with /bmad:create-prd

   Why? For Level 2+ projects, PRD ensures all requirements are
   captured before architecture and implementation.
   ```

6. **Offer to execute:**

   ```text
   Would you like to start /bmad:create-prd now?
   ```

## Status Icons

- ✓ Complete (with file path)
- → Current phase
- ⚠ Required but not started
- - Optional or not started

## Usage

```bash
/bmad:status
```

Run anytime to check progress and get recommendations.
