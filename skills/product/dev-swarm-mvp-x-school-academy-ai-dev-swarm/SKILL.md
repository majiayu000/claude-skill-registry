---
name: dev-swarm-mvp
description: Define MVP scope, success metrics, and explicit out-of-scope items to focus on the smallest testable product. Use when user asks to define MVP, scope MVP, or start Stage 3 after personas.
---

# AI Builder - MVP Definition

This skill creates/updates the MVP (Minimum Viable Product) definition by identifying the smallest testable product that delivers core value, explicitly defining what NOT to build, and establishing success metrics for validation.

## When to Use This Skill

- User asks to "define MVP" or "scope MVP"
- User requests to start Stage 3 or the next stage after personas
- User wants to identify core features for MVP
- User wants to define success metrics
- User needs to clarify what should be excluded from MVP

## Prerequisites

This skill requires **02-personas** to be completed. The MVP scope will build upon user personas and prioritized user stories (P0/P1/P2) defined in that stage.

## Your Roles in This Skill

- **Product Manager**: Define MVP scope by selecting only P0 (must-have) features. Create success criteria and key metrics for MVP validation. Identify what "viable" means for the specific product. Define learning objectives and what needs to be validated.
- **Tech Manager (Architect)**: Design MVP architecture with future scalability in mind. Identify technical shortcuts acceptable for MVP and document technical debt. Plan for instrumentation and analytics from day one. Define what can be manual vs. automated in MVP.
- **UX Designer**: Simplify designs to MVP essentials. Create streamlined user flows for core features only. Focus on usability over polish. Ensure core user journey is intuitive.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `02-personas/` folder exists (mandatory):**
   - If NOT found: Inform user they need to create personas first, then STOP
   - If found: Read all files to understand:
     - User personas and their needs
     - User stories (especially P0 stories)
     - Acceptance criteria
     - Problem statement reference

1.5 **Verify previous stage completion (02-personas):**
   - Read `02-personas/README.md` and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 02, or skip it
     - If skip: create `02-personas/SKIP.md` with a short reason
     - If continue: STOP and return after stage 02 is complete

2. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand:
     - Problem statement
     - Value proposition
     - Owner requirements
     - Cost budget (to understand constraints for this stage)

3. **Check if `01-market-research/` folder exists (optional):**
   - If found: Read to understand:
     - Market gaps
     - Competitor features
     - Validation findings

4. **Check if this stage should be skipped:**
   - Check if `03-mvp/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 3 (mvp) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (prd)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with MVP anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

5. **Check if `03-mvp/` folder exists:**
   - If exists: Read all existing files to understand current MVP definition
   - If NOT exists: Will create new structure

6. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

7. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `02-personas/` to understand user personas and P0 user stories
   - Read `00-init-ideas/` to understand problem statement and value proposition
   - Read `01-market-research/` (if exists) to understand market context
   - Consider cost-budget constraints for this stage

2. **Create or update 03-mvp/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: mvp-scope.md, out-of-scope.md, success-metrics.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Product Manager, Tech Manager, UX Designer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What MVP will be defined:**
     - How P0 features from personas will be scoped into MVP
     - What success metrics will be defined
     - What will be explicitly excluded (out-of-scope)
   - **Methodology:**
     - How MVP scope will be determined (P0 features only)
     - Success metrics approach
   - **Deliverables planned:**
     - List of files that will be created (mvp-scope.md, out-of-scope.md, success-metrics.md, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the MVP approach and what will be defined
   - Summarize what documentation files will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update MVP Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   03-mvp/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── mvp-scope.md (if specified in README)
   ├── out-of-scope.md (if specified in README)
   └── success-metrics.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update MVP Scope Documentation

**IMPORTANT: Only create MVP documentation after README is approved in Step 1 and re-read.**

**NOTE:** Use `references/deliverables.md` for file-by-file content guidance. Adapt based on the approved README and project needs.

### Step 4: Ensure Traceability

Make sure MVP scope maps back to:
- P0 user stories from 02-personas/user-stories.md
- Primary persona needs from 02-personas/persona-primary.md
- Problem statement from 00-init-ideas (if available)
- Value proposition from 00-init-ideas (if available)

Ensure out-of-scope clearly excludes P1 and P2 features.

### Step 5: Final User Review

1. **Inform user that MVP definition is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Number of P0 features in MVP scope
   - What's explicitly excluded (P1/P2 features deferred)
   - Success metrics and validation approach
   - Estimated timeline (sprints)
   - Explain the rationale: why this is the smallest testable product

4. Ask if they want to proceed to the next stage (PRD creation)
5. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms MVP definition is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `03-mvp/`
   - Commit with message: "Define MVP scope and success metrics (Stage 3)"
