---
version: 4.1.0-fractal
name: conductor-setup
description: Initialize project with Conductor artifacts (product definition,
  tech stack, workflow, style guides)
metadata:
  argument-hint: "[--resume]"
---

# Conductor Setup

Initialize or resume Conductor project setup. This command creates foundational project documentation through interactive Q&A.

## Use this skill when

- Working on conductor setup tasks or workflows
- Needing guidance, best practices, or checklists for conductor setup

## Do not use this skill when

- The task is unrelated to conductor setup
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Pre-flight Checks

1. Check if `conductor/` directory already exists in the project root:
   - If `conductor/product.md` exists: Ask user whether to resume setup or reinitialize
   - If `conductor/setup_state.json` exists with incomplete status: Offer to resume from last step

2. Detect project type by checking for existing indicators:
   - **Greenfield (new project)**: No .git, no package.json, no requirements.txt, no go.mod, no src/ directory
   - **Brownfield (existing project)**: Any of the above exist

3. Load or create `conductor/setup_state.json`:
   ```json
   {
     "status": "in_progress",
     "project_type": "greenfield|brownfield",
     "current_section": "product|guidelines|tech_stack|workflow|styleguides",
     "current_question": 1,
     "completed_sections": [],
     "answers": {},
     "files_created": [],
     "started_at": "ISO_TIMESTAMP",
     "last_updated": "ISO_TIMESTAMP"
   }
   ```

## Interactive Q&A Protocol

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Offer 2-3 suggested answers plus "Type your own" option
- Maximum 5 questions per section
- Update `setup_state.json` after each successful step
- Validate file writes succeeded before continuing

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Section 1: Product Definition (max 5 questions)](./sub-skills/section-1-product-definition-max-5-questions.md)
### 2. [Section 2: Product Guidelines (max 3 questions)](./sub-skills/section-2-product-guidelines-max-3-questions.md)
### 3. [Section 3: Tech Stack (max 5 questions)](./sub-skills/section-3-tech-stack-max-5-questions.md)
### 4. [Section 4: Workflow Preferences (max 4 questions)](./sub-skills/section-4-workflow-preferences-max-4-questions.md)
### 5. [Section 5: Code Style Guides (max 2 questions)](./sub-skills/section-5-code-style-guides-max-2-questions.md)
### 6. [1. conductor/index.md](./sub-skills/1-conductorindexmd.md)
### 7. [2. conductor/product.md](./sub-skills/2-conductorproductmd.md)
### 8. [3. conductor/product-guidelines.md](./sub-skills/3-conductorproduct-guidelinesmd.md)
### 9. [4. conductor/tech-stack.md](./sub-skills/4-conductortech-stackmd.md)
### 10. [5. conductor/workflow.md](./sub-skills/5-conductorworkflowmd.md)
### 11. [6. conductor/tracks.md](./sub-skills/6-conductortracksmd.md)
### 12. [7. conductor/code_styleguides/](./sub-skills/7-conductorcode_styleguides.md)
