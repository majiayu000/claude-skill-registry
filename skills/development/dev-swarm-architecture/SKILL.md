---
name: dev-swarm-architecture
description: Design system architecture including components, data flow, and deployment boundaries. Use when user asks to design architecture, create architecture diagrams, or start Stage 6 after UX design.
---

# AI Builder - System Architecture

This skill creates/updates the system architecture documentation defining the system structure, major components, data flow, and deployment boundaries without specifying specific frameworks or technologies.

## When to Use This Skill

- User asks to "design architecture" or "create system design"
- User requests to start Stage 6 or the next stage after UX design
- User wants to define system components and their relationships
- User wants to understand data flow and system boundaries
- User needs to plan deployment architecture

## Prerequisites

This skill requires **05-ux** to be completed. The architecture will implement the UX design and functional requirements with a clear system structure.

## Your Roles in This Skill

- **Tech Manager (Architect)**: Lead architecture design with system overview and component definitions. Review PRD and UX design to understand requirements. Create architecture diagrams showing component relationships. Define data structures and data flow patterns. Establish architectural principles and patterns.
- **Backend Architect**: Design backend system components, API structure, and data models. Define service boundaries and responsibilities. Plan database architecture and data flow. Consider scalability and performance requirements.
- **Frontend Architect**: Design frontend architecture and component structure. Define state management approach. Plan client-side data flow and API integration patterns.
- **AI Engineer**: Design AI/ML model architecture and integration patterns. Define prompt engineering strategies and LLM integration. Plan vector database and embeddings architecture. Design model monitoring and evaluation pipelines. Consider AI costs, latency, and fallback strategies. Plan content generation and moderation systems.
- **Content Moderator**: Design content moderation architecture for AI-generated content. Define moderation workflows and automated filtering systems. Plan human-in-the-loop review processes. Design content safety and compliance systems. Consider scalability of moderation infrastructure.
- **DevOps Engineer**: Review architecture for deployment feasibility. Provide input on deployment boundaries and cloud architecture. Consider monitoring, logging, and operational aspects.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `05-ux/` folder exists (mandatory):**
   - If NOT found: Inform user they need to create UX design first, then STOP
   - If found: Read all files to understand:
     - User flows and interactions
     - Mockup structure (if UI-based app)
     - Screen navigation patterns

1.5 **Verify previous stage completion (05-ux):**
   - Read `05-ux/README.md` and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 05, or skip it
     - If skip: create `05-ux/SKIP.md` with a short reason
     - If continue: STOP and return after stage 05 is complete

2. **Check if `04-prd/` folder exists (mandatory):**
   - If NOT found: Inform user they need PRD first, then STOP
   - If found: Read to understand:
     - Functional requirements
     - Non-functional requirements (performance, security, scalability)
     - Feature list and priorities

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand all files

4. **Check if `03-mvp/` folder exists (recommended):**
   - If found: Read to understand:
     - MVP scope (what to prioritize in architecture)
     - Success metrics (inform performance targets)

5. **Check if this stage should be skipped:**
   - Check if `06-architecture/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 6 (architecture) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (tech-specs)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with architecture anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

6. **Check if `06-architecture/` folder exists:**
   - If exists: Read all existing files to understand current architecture state
   - If NOT exists: Will create new structure

7. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

8. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from previous stages:**
   - Read `05-ux/` to understand user flows and UI structure
   - Read `04-prd/` to understand functional and non-functional requirements
   - Read `03-mvp/` (if exists) to understand what to prioritize
   - Consider cost-budget constraints for this stage

2. **Create or update 06-architecture/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: system-overview.md, architecture-diagram.md, data-flow.md, deployment-boundaries.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Tech Manager (lead), Backend Architect, Frontend Architect, AI Engineer, Content Moderator, DevOps Engineer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What architecture will include:**
     - System components and their responsibilities
     - Architecture diagrams (high-level + detail)
     - Data flow for critical user journeys
     - Deployment boundaries and scaling strategy
   - **Methodology:**
     - How components will be defined (from PRD requirements)
     - Diagram approach (Mermaid for all diagrams)
   - **Deliverables planned:**
     - List of files that will be created (system-overview.md, architecture-diagram.md, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the architecture approach and what will be designed
   - Summarize what documentation files will be created
   - Explain how it aligns with previous stages

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create/Update Architecture Structure

**Only after user approves the README and you re-read it:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   06-architecture/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── system-overview.md (if specified in README)
   ├── architecture-diagram.md (if specified in README)
   ├── data-flow.md (if specified in README)
   └── deployment-boundaries.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update Architecture Documentation

**IMPORTANT: Only create architecture documentation after README is approved in Step 1 and re-read.**

**NOTE:** Use `references/deliverables.md` for file-by-file content guidance. Adapt based on the approved README and project needs.

### Step 4: Ensure Alignment

Make sure architecture aligns with:
- Non-functional requirements from 04-prd/non-functional-requirements.md
- Functional requirements from 04-prd/functional-requirements.md
- User flows from 05-ux/user-flows.md
- MVP scope from 03-mvp/ (architecture should support MVP first, then scale)

Verify that:
- All functional requirements can be implemented in this architecture
- Performance targets are achievable
- Security requirements are addressed
- Scalability needs are met
- Deployment is feasible

### Step 5: Final User Review

1. **Inform user that architecture is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Walk through the architecture diagrams
   - Explain major components and their responsibilities
   - Show data flow for critical user journeys
   - Explain deployment boundaries and security

4. **Highlight key insights:**
   - Number of major components
   - Key architectural patterns used
   - Scalability approach
   - Security boundaries
   - Cloud vs. local deployment split

5. **Ask questions:**
   - Does the architecture make sense?
   - Are there any components missing?
   - Any concerns about scalability or security?
   - Ready to proceed to next stage (tech specs)?

6. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms architecture is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `06-architecture/`
   - Commit with message: "Design system architecture and deployment (Stage 6)"
