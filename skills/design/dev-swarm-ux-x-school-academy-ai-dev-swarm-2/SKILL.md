---
name: dev-swarm-ux
description: Design user experience including flows, interactions, mockups, and accessibility. Use when user asks to design UX, create mockups, or start Stage 5 after PRD.
---

# AI Builder - UX Design

This skill creates/updates the UX design documentation including user flows, interaction specifications, edge cases, accessibility requirements, and most importantly, **interactive HTML/CSS/JS mockups** for UI-based applications.

## When to Use This Skill

- User asks to "design UX" or "create mockups"
- User requests to start Stage 5 or the next stage after PRD
- User wants to visualize the product design
- User wants to create interactive prototypes
- User needs to present product design to non-technical stakeholders

## Prerequisites

This skill requires **04-prd** to be completed. The UX design will translate functional requirements into visual designs and user flows.

## Your Roles in This Skill

- **UX Designer**: Lead UX design with user flows, interaction specs, and accessibility. Create user journey maps and ensure intuitive navigation. Design information architecture and interaction patterns. Ensure WCAG 2.1 accessibility compliance.
- **UI Designer**: Create visual mockups using static HTML/CSS/JS. Define theme, color palette, typography, and spacing. Design components and layouts. Create interactive prototypes that showcase the product to non-technical stakeholders.
- **Content Moderator**: Design user input moderation workflows in UI. Define content submission and review interfaces. Plan flagging, reporting, and appeals flows. Design moderation queue interfaces. Ensure community guidelines are presented clearly in UI. Plan user communication flows for moderation actions.
- **Product Manager**: Ensure UX aligns with requirements and user stories. Review flows against acceptance criteria. Validate that design solves user problems effectively.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `04-prd/` folder exists (mandatory):**
   - If NOT found: Inform user they need to create PRD first, then STOP
   - If found: Read all files to understand:
     - Functional requirements
     - User journeys
     - Product goals
     - Non-functional requirements (especially usability and accessibility)

1.5 **Verify previous stage completion (04-prd):**
   - Read `04-prd/README.md` and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 04, or skip it
     - If skip: create `04-prd/SKIP.md` with a short reason
     - If continue: STOP and return after stage 04 is complete

2. **Check if `02-personas/` folder exists (mandatory):**
   - If NOT found: Inform user they need personas first, then STOP
   - If found: Read to understand:
     - User personas and their needs
     - User pain points
     - User preferences and behaviors

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand:
     - Cost budget (to understand constraints for this stage)

4. **Check if `03-mvp/` folder exists (recommended):**
   - If found: Read to understand:
     - MVP scope
     - Core features to prioritize in design

5. **Check if this stage should be skipped:**
   - Check if `05-ux/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 5 (ux) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (architecture)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with UX anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

6. **Check if `05-ux/` folder exists:**
   - If exists: Read all existing files to understand current UX design state
   - If NOT exists: Will create new structure

7. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

8. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `04-prd/` to understand functional requirements and user journeys
   - Read `02-personas/` to understand user needs and pain points
   - Read `03-mvp/` (if exists) to understand core features to prioritize
   - Consider cost-budget constraints for this stage

2. **Create or update 05-ux/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: user-flows.md, interaction-specs.md, edge-cases.md, accessibility.md, mockups/)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** UX Designer (lead), UI Designer, Product Manager, Content Moderator
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What UX will include:**
     - User flows for critical journeys (list key flows from PRD)
     - Interaction specifications for components
     - Edge cases and error handling
     - Accessibility compliance (WCAG 2.1 Level AA)
     - Interactive mockups (for UI-based apps)
   - **Methodology:**
     - How user flows will be created (from PRD requirements)
     - Mockup approach (HTML/CSS/JS for UI apps)
   - **Deliverables planned:**
     - List of files that will be created (user-flows.md, mockups/, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the UX approach and what will be designed
   - Summarize what documentation files and mockups will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update UX Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   05-ux/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── user-flows.md (if specified in README)
   ├── interaction-specs.md (if specified in README)
   ├── edge-cases.md (if specified in README)
   ├── accessibility.md (if specified in README)
   └── mockups/ (if specified in README - for UI-based applications)
       ├── index.html
       ├── styles.css
       ├── script.js
       └── assets/
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

   **Note**: For UI-based web/mobile/desktop apps, the `mockups/` folder with static HTML/CSS/JS files is **CRITICAL** as it showcases the product to non-technical stakeholders.

### Step 3: Create/Update UX Documentation

**IMPORTANT: Only create UX documentation after README is approved in Step 1 and re-read.**

- Use the approved README "Deliverables planned" list as the source of truth.
- Follow `references/deliverables.md` for file-by-file content guidance and mockup requirements.

### Step 4: Ensure Alignment

Make sure UX design aligns with:
- Functional requirements from 04-prd/functional-requirements.md
- User journeys from 04-prd/prd.md
- User personas from 02-personas/
- MVP scope from 03-mvp/ (prioritize core features in mockups)
- Accessibility requirements from 04-prd/non-functional-requirements.md

Verify that:
- All critical user flows are documented
- All edge cases are considered
- Accessibility checklist is complete
- Mockups showcase the product effectively (for UI-based apps)
- Interactions are clearly specified

### Step 5: Final User Review

1. **Inform user that UX design is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Show the interactive mockups (if UI-based app)
   - Walk through critical user flows
   - Demonstrate interaction patterns
   - Explain accessibility considerations

4. **Highlight key insights:**
   - Number of user flows documented
   - Key interaction patterns defined
   - Accessibility compliance level (WCAG 2.1 Level AA)
   - Mockup screens created (if applicable)
   - Theme and design system defined

5. **For mockups specifically:**
   - Open `mockups/index.html` in browser
   - Demonstrate navigation between screens
   - Show responsive behavior (resize browser)
   - Point out theme consistency (colors, fonts, spacing)
   - Explain how this represents the final product

6. **Ask questions:**
   - Does the design align with their vision?
   - Are there any flows missing?
   - Any concerns about accessibility?
   - Should any mockup screens be added/changed?
   - Ready to proceed to next stage (architecture)?

7. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms UX design is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `05-ux/`
   - Commit with message: "Design UX flows, interactions, and mockups (Stage 5)"


## Deliverables

Refer to `references/deliverables.md` for the deliverable list, content guidance, and mockup rationale.
