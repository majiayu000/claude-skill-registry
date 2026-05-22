---
name: dev-swarm-tech-specs
description: Define technical specifications including tech stack, security, theme standards (from UX mockup), coding standards, and testing standards. Use when user asks to define tech specs, choose tech stack, or start Stage 7 after architecture.
---

# AI Builder - Technical Specifications

This skill creates/updates the technical specifications documentation defining the technology stack, security posture, theme standards (extracted from UX mockup), coding standards, testing standards, and security standards.

## When to Use This Skill

- User asks to "define tech specs" or "choose tech stack"
- User requests to start Stage 7 or the next stage after architecture
- User wants to select technologies and frameworks
- User wants to establish coding and testing standards
- User needs to define security standards

## Prerequisites

This skill requires **06-architecture** to be completed for L3+ projects. For L2 projects, this stage can proceed without architecture documentation.

## Your Roles in This Skill

- **Tech Manager (Architect)**: Lead tech stack selection and standards definition. Review architecture to choose appropriate technologies. Define coding and testing standards. Ensure technical choices align with requirements and constraints.
- **Security Engineer**: Define security posture, authentication approach, and secure coding standards. Identify security threats and mitigation strategies. Establish security testing and compliance requirements.
- **UI Designer**: Extract theme standards from approved UX mockup. Document colors, fonts, spacing, and design tokens. Ensure design consistency rules are clear for implementation.
- **DevOps Engineer**: Review tech stack for deployment and operational feasibility. Provide input on infrastructure compatibility. Consider monitoring and logging requirements.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

First read and understand rules: `dev-swarm/docs/research-specs-rules.md` then:

1. **Check for Project Scale (L2 vs L3+):**
   - Check `00-init-ideas/README.md` or classification to determine project scale.

2. **Check if `06-architecture/` folder exists:**
   - **For L3+ projects (Mandatory):**
     - If NOT found: Inform user they need to create architecture first, then STOP.
     - If found: Read all files.
   - **For L2 projects (Optional):**
     - If found: Read files.
     - If NOT found: Proceed without it.

2.5 **Verify previous stage completion (06-architecture when required):**
   - If `06-architecture/README.md` exists, read it and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 06, or skip it if allowed
     - If skip: create `06-architecture/SKIP.md` with a short reason
     - If continue: STOP and return after stage 06 is complete

3. **Check if `05-ux/` folder exists (Mandatory for L3+):**
   - If NOT found and project is L3+: Warn user.
   - For L2: Skip if not relevant.
     - **CSS variables and design tokens**
     - **Color palette**
     - **Typography (fonts, sizes)**
     - **Spacing system**
     - **Border radius and shadows**
     - **Component styles**

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read all files to understand it

4. **Check if `04-prd/` folder exists (recommended):**
   - If found: Read to understand:
     - Non-functional requirements (performance, security, compliance)
     - Technical constraints

5. **Check if `03-mvp/` folder exists (recommended):**
   - If found: Read to understand:
     - MVP scope (prioritize tech choices for MVP)
     - Timeline constraints

6. **Check if this stage should be skipped:**
   - Check if `07-tech-specs/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 7 (tech-specs) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (devops)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with tech specs anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

7. **Check if `07-tech-specs/` folder exists:**
   - If exists: Read all existing files to understand current tech specs state
   - If NOT exists: Will create new structure

8. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

9. **Read source code structure guidance (mandatory):**
   - Read `dev-swarm/docs/source-code-structure.md`
   - Use it as the baseline when creating `07-tech-specs/source-code-structure.md`

10. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `06-architecture/` to understand system components and deployment
   - Read `05-ux/mockups/styles.css` to extract theme (CRITICAL for theme-standards.md)
   - Read `04-prd/` to understand non-functional requirements
   - Read `03-mvp/` (if exists) to understand what to prioritize
   - Consider cost-budget constraints for this stage

2. **Create or update 07-tech-specs/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - **For L2 projects:** Create a simple README (just several lines) indicating the project level and that only `tech-stack.md` is required.
   - **For L3+ projects:** List deliverables explicitly in README (typical: tech-stack.md, security.md, theme-standards.md, coding-standards.md, source-code-structure.md, testing-standards.md, security-standards.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Tech Manager (lead), Security Engineer, UI Designer, DevOps Engineer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What tech specs will include:**
     - Technology stack selection with rationale
     - Security posture and authentication approach
     - Theme standards extracted from UX mockup (CRITICAL)
     - Coding standards and best practices
     - Testing standards and coverage requirements
     - Security standards for secure coding
   - **Methodology:**
     - How tech stack will be selected (based on architecture + requirements)
     - How theme will be extracted from mockup CSS (DO NOT invent values)
   - **Deliverables planned:**
     - List of files that will be created (tech-stack.md, theme-standards.md, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the tech specs approach and what will be defined
   - Summarize what documentation files will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update Tech Specs Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   07-tech-specs/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── tech-stack.md (if specified in README)
   ├── security.md (if specified in README)
   ├── theme-standards.md (if specified in README - MUST extract from UX mockup)
   ├── coding-standards.md (if specified in README)
   ├── source-code-structure.md (if specified in README)
   ├── testing-standards.md (if specified in README)
   └── security-standards.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update Technical Specifications Documentation

**IMPORTANT: Only create tech specs documentation after README is approved in Step 1 and re-read.**

**NOTE:** Use `references/deliverables.md` for file-by-file content guidance. Adapt based on the approved README and project needs.

### Step 4: Ensure Alignment

Make sure tech specs align with:
- Architecture from 06-architecture/
- Non-functional requirements from 04-prd/non-functional-requirements.md
- **UX mockup theme** from 05-ux/mockups/styles.css (CRITICAL for theme-standards.md)
- MVP scope from 03-mvp/ (prioritize tech choices for MVP)

Verify that:
- Tech stack can implement the architecture
- Theme standards match the UX mockup exactly
- Security standards address requirements
- Testing standards ensure quality
- Coding standards are clear and enforceable

### Step 5: Final User Review

1. **Inform user that tech specs are complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Review chosen tech stack and rationale
   - Show theme standards extracted from UX mockup
   - Explain security approach
   - Walk through coding and testing standards

4. **Highlight key insights:**
   - Frontend framework choice and why
   - Backend framework choice and why
   - Database choice and why
   - **Theme values extracted from mockup** (show side-by-side)
   - Security compliance level
   - Test coverage requirements

5. **Ask questions:**
   - Comfortable with tech stack choices?
   - Theme standards match their vision?
   - Any security concerns?
   - Testing requirements achievable?
   - Ready to proceed to next stage (DevOps)?

6. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms tech specs are complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `07-tech-specs/`
   - Commit with message: "Define tech stack and engineering standards (Stage 7)"
