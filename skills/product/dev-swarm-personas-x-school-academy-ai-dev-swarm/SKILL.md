---
name: dev-swarm-personas
description: Create/Updates detailed user personas and prioritized user stories based on target users and market research. Use when user asks to create personas, define user stories, or start Stage 2 after market research or init-ideas.
---

# AI Builder - Personas & User Stories

This skill creates/updates detailed user personas and prioritized user stories to define who will use the product and what they need to accomplish.

## When to Use This Skill

- User asks to "create personas" or "define user stories"
- User requests to start Stage 2 or the next stage after market-research
- User wants to define target users in detail
- User wants to create/update user stories

## Prerequisites

This skill requires **00-init-ideas** to be completed. Market research (01-market-research) is optional.

## Your Roles in This Skill

- **Product Manager**: Create user stories in "As a [role], I want [feature] so that [benefit]" format. Prioritize features based on user needs and business goals (P0/P1/P2). Define acceptance criteria for each feature.
- **UX Designer**: Create user personas based on target user research. Map user journeys and identify user needs and pain points. Ensure personas reflect real user behaviors and goals.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `00-init-ideas/` exists (mandatory):**
   - If NOT found: Inform user they need to init ideas first, then STOP
   - If found: Read all files to understand:
     - Problem statement
     - Target users
     - Value proposition
     - Owner requirements
     - Cost budget (to understand constraints for this stage)

2. **Check if `01-market-research/` exists (optional):**
   - If found: Read files to understand:
     - Target audience segments
     - Competitor user bases
     - Market validation findings
     - Gap analysis
   - If NOT found: Continue with just init-ideas data (acceptable for L2 projects)

2.5 **Verify previous stage completion (01-market-research):**
   - If `01-market-research/README.md` exists, read it and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 01, or skip it
     - If skip: create `01-market-research/SKIP.md` with a short reason
     - If continue: STOP and return after stage 01 is complete

3. **Check if this stage should be skipped:**
   - Check if `02-personas/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 2 (personas) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (mvp)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with personas anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

4. **Check if `02-personas/` folder exists:**
   - If exists: Read all existing files to understand current state
   - If NOT exists: Will create new structure

5. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

6. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `00-init-ideas/` to understand problem, target users, value proposition
   - Read `01-market-research/` (if exists) to understand market segments and user validation
   - Consider cost-budget constraints for this stage

2. **Create or update 02-personas/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: persona-primary.md, persona-secondary.md, user-stories.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Product Manager, UX Designer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What personas will be created:**
     - How many personas (1-2 typically)
     - What market research insights will inform personas
     - What user stories will be created (P0/P1/P2)
   - **Methodology:**
     - How personas will be created (based on init-ideas + market research)
     - User story format and prioritization approach
   - **Deliverables planned:**
     - List of files that will be created (persona-primary.md, user-stories.md, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the personas approach and what will be created
   - Summarize what documentation files will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update Personas Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   02-personas/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── persona-primary.md (if specified in README)
   ├── persona-secondary.md (if specified in README)
   └── user-stories.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update User Personas

**IMPORTANT: Only create personas after README is approved in Step 1 and re-read.**

- Use `references/deliverables.md` for persona file content guidance.

### Step 4: Create/Update User Stories

- Use `references/deliverables.md` for user story content guidance.

### Step 5: Ensure Traceability

Make sure user stories map back to:
- Problem statement from 00-init-ideas
- Value proposition from 00-init-ideas
- Gap analysis from 01-market-research (if available)
- Owner requirements from 00-init-ideas

### Step 6: Final User Review

1. **Inform user that personas and user stories are complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Number of personas created
   - P0/P1/P2 story distribution
   - How stories address the core problem

4. Ask if they want to proceed to the next stage (MVP definition)
5. Make adjustments based on user feedback if needed

### Step 7: Commit to Git (if user confirms)

1. **If user confirms personas and user stories are complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `02-personas/`
   - Commit with message: "Define user personas and prioritized user stories (Stage 2)"
