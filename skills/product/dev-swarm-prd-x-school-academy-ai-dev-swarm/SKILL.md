---
name: dev-swarm-prd
description: Create comprehensive Product Requirements Document (PRD) defining product behavior, functional and non-functional requirements. Use when user asks to create PRD, write requirements, or start Stage 4 after MVP definition.
---

# AI Builder - Product Requirements Document (PRD)

This skill creates/updates the Product Requirements Document (PRD) that locks down product behavior and requirements without specifying the technical implementation or tech stack.

## When to Use This Skill

- User asks to "create PRD" or "write PRD"
- User requests to start Stage 4 or the next stage after MVP definition
- User wants to define detailed product requirements
- User wants to document functional and non-functional requirements
- User needs to expand MVP scope into full product specification

## Prerequisites

This skill requires **03-mvp** to be completed. The PRD will expand the MVP scope into a comprehensive product specification with detailed requirements.

## Your Roles in This Skill

- **Product Manager**: Lead PRD creation with detailed feature specifications. Refine and expand user stories from MVP into complete requirements. Define acceptance criteria for each feature. Ensure alignment with business goals and user needs. Create product overview, goals, and user journeys.
- **UX Designer**: Provide user experience perspective on requirements. Define user journeys and interaction expectations. Ensure requirements support good user experience. Contribute to functional requirements from UX perspective.
- **Tech Manager (Architect)**: Review requirements for technical feasibility. Define non-functional requirements (performance, security, scalability). Identify technical constraints and dependencies. Ensure requirements are implementable without over-specifying technology.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `03-mvp/` folder exists (mandatory):**
   - If NOT found: Inform user they need to define MVP first, then STOP
   - If found: Read all files to understand:
     - MVP scope and P0 features
     - Out-of-scope items (P1/P2 features)
     - Success metrics
     - Target users

1.5 **Verify previous stage completion (03-mvp):**
   - Read `03-mvp/README.md` and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 03, or skip it
     - If skip: create `03-mvp/SKIP.md` with a short reason
     - If continue: STOP and return after stage 03 is complete

2. **Check if `02-personas/` folder exists (mandatory):**
   - If NOT found: Inform user they need personas first, then STOP
   - If found: Read to understand:
     - User personas
     - All user stories (P0/P1/P2)
     - User needs and pain points

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand:
     - Problem statement
     - Value proposition
     - Owner requirements
     - Cost budget (to understand constraints for this stage)

4. **Check if `01-market-research/` folder exists (optional):**
   - If found: Read to understand:
     - Market context
     - Competitive landscape
     - Validation findings

5. **Check if this stage should be skipped:**
   - Check if `04-prd/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 4 (prd) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (ux)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with PRD anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

6. **Check if `04-prd/` folder exists:**
   - If exists: Read all existing files to understand current PRD state
   - If NOT exists: Will create new structure

7. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

8. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `03-mvp/` to understand MVP scope and features
   - Read `02-personas/` to understand user stories (P0/P1/P2)
   - Read `00-init-ideas/` to understand problem statement and value proposition
   - Read `01-market-research/` (if exists) to understand market context
   - Consider cost-budget constraints for this stage

2. **Create or update 04-prd/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: prd.md, functional-requirements.md, non-functional-requirements.md, out-of-scope.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Product Manager (lead), UX Designer, Tech Manager
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What PRD will include:**
     - Product overview, goals, and user journeys
     - Functional requirements (based on user stories)
     - Non-functional requirements (performance, security, scalability)
     - Out-of-scope items
   - **Methodology:**
     - How requirements will be defined (from MVP + all user stories)
     - How functional requirements will be structured
   - **Deliverables planned:**
     - List of files that will be created (prd.md, functional-requirements.md, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the PRD approach and what will be documented
   - Summarize what documentation files will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update PRD Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   04-prd/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── prd.md (if specified in README)
   ├── functional-requirements.md (if specified in README)
   ├── non-functional-requirements.md (if specified in README)
   └── out-of-scope.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update PRD Documentation

**IMPORTANT: Only create PRD documentation after README is approved in Step 1 and re-read.**

**NOTE:** Use `references/deliverables.md` for file-by-file content guidance. Adapt based on the approved README and project needs.

### Step 4: Ensure Traceability

Make sure all requirements map back to:
- User stories from 02-personas/user-stories.md
- MVP scope from 03-mvp/mvp-scope.md
- Problem statement from 00-init-ideas (if available)
- Value proposition from 00-init-ideas (if available)

Verify that:
- All P0 features from MVP are fully specified as functional requirements
- P1/P2 features are included or explicitly deferred to out-of-scope
- Each requirement has clear acceptance criteria
- Requirements are testable and implementable

### Step 5: Final User Review

1. **Inform user that PRD is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Number of functional requirements (organized by category)
   - Key non-functional requirements (performance, security, compliance)
   - What's explicitly out of scope
   - How this builds on MVP definition
   - Phasing plan (MVP → v1.0 → future)
   - Explain the completeness: "This PRD locks down WHAT the product does, not HOW it's built"

4. Ask if they want to proceed to the next stage (UX design)
5. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms PRD is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `04-prd/`
   - Commit with message: "Create Product Requirements Document (Stage 4)"
