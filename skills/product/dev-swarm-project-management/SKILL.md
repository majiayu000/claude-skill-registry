---
name: dev-swarm-project-management
description: Plan sprints and backlogs in an AI-Driven Development workflow. Define features (backlogs), organize sprints as cumulative demo-able milestones, and manage the full development lifecycle.
---

# AI Builder - Project Management

This skill manages the complete sprint and backlog lifecycle for **AI-Driven Development**.
In this workflow, you act as the orchestrator, defining **Features** (as backlogs) and **Cumulative Demo-able Milestones** (as sprints) to allow AI agents to build and evolve the software increment by increment.

## When to Use This Skill

- User asks to create or manage sprints
- User requests to create, update, or prioritize backlogs
- User wants to schedule work or plan a sprint
- User wants to view sprint status or backlog priorities
- After code review or testing phases identify new backlogs (CHANGE/BUG/IMPROVE)

## Prerequisites

This skill works with the following folder structure:
- `02-personas/` - User personas and user stories that drive backlog scope
- `03-mvp/` - MVP scope and success criteria for initial sprint planning
- `04-prd/` - Product requirements and non-functional constraints
- `05-ux/` - UX flows, states, and mockups that shape backlog acceptance
- `06-architecture/` - System structure and dependencies that affect sequencing
- `07-tech-specs/` - Technology choices and standards (including source-code-structure.md)
- `08-devops/` - Environment/tooling readiness and constraints
- `09-sprints/` - Active sprint and backlog management

## Sprint and Backlog Guidelines (Read and Follow)

This skill **strictly follows** the rules in:
1. `dev-swarm/docs/what-is-a-feature.md` (Feature Definition)
2. `dev-swarm/docs/sprint-backlog-guidelines.md` (AI-Driven Development Sprint & Backlog Guidelines)


**Key Principles:**
*   **Backlog = Feature:** A backlog is NOT a technical task. It is a complete, user-facing Feature.
*   **Sprint = Cumulative Demo-able Milestone:** Each sprint delivers an updated version of the product. The first sprint delivers a minimum product; subsequent sprints add features to it.
*   **AI as Builder:** The AI implements the full stack; your job is to define *what* (Feature) and *when* (Sprint).

## Your Roles in This Skill

- **Project Manager**: Lead sprint planning. Define the *Value* and *Scope* of sprints. Break down the product into **Cumulative Demo-able Milestones** (Sprints). Ensure each backlog represents a complete Feature. Prioritize based on user impact and business value.
- **Tech Manager (Architect)**: Partner with the PM. Assess *Feasibility* and *Architecture*. Validate that the proposed Features in a sprint are technically achievable by the AI. Identify dependencies and structural constraints.
- **Product Manager**: Define acceptance criteria for Features. Ensure backlogs describe *user value*, not implementation details.
- **AI Engineer**: Plan AI/ML feature implementation strategies.
- **Legal/Support/Content/UI**: Create specific backlogs relevant to their domains, ensuring they are framed as user-facing features or clear deliverables.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Backlog Types

There are 4 types of backlogs:

1. **FEATURE** - A new feature request (initial development). Matches `dev-swarm/docs/what-is-a-feature.md`.
2. **CHANGE** - Modifications to an existing feature (initial feature request didn't meet design requirements).
3. **BUG** - Defects found during code review or testing to a feature.
4. **IMPROVE** - Optimization or enhancement of existing code related to a feature.

## Backlog Naming Convention (CRITICAL)

**Format:** `[BACKLOG_TYPE]-[feature-name]-<sub-feature>.md`

- **BACKLOG_TYPE**: FEATURE, CHANGE, BUG, or IMPROVE (uppercase)
- **feature-name**: Kebab-case feature identifier (e.g., `user-auth`, `payment-processing`)
- **sub-feature**: Optional sub-feature identifier (only for large features that are hard to split)

**Examples:**
- `FEATURE-user-auth-login.md`
- `CHANGE-user-auth-logout.md`
- `BUG-payment-processing-refund.md`
- `IMPROVE-user-auth-session.md`

## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Review planning inputs:**
   - `02-personas/`, `03-mvp/`, `04-prd/`, `05-ux/`, `06-architecture/`, `07-tech-specs/`, `08-devops/`.
   - Ensure you understand the "User Perspective" (what is a feature?) and "Technical Constraints".

1.5 **Verify previous stage completion (08-devops):**
   - If `08-devops/README.md` exists, read it and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 08, or skip it
     - If skip: create `08-devops/SKIP.md` with a short reason
     - If continue: STOP and return after stage 08 is complete

2. **Check for `09-sprints/` folder:**
   - If NOT found: You are initializing the project's execution phase.
   - If found: You are managing an ongoing project.

3. **Check for SKIP status:**
   - If `09-sprints/SKIP.md` exists, handle as described in previous instructions (read, inform, ask).

4. **Use Templates:** Always use templates from `templates/`.

5. **If `09-sprints/README.md` exists:** Check whether it requires diagrams.
   If it does, follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

### Step 1: Initialize Sprint Management (First Time Only)

**CRITICAL: Joint Planning by PM and TM.**

1.  **Analyze Context:** Read all stage folders.
2.  **Create `09-sprints/README.md` (The Master Plan):**
    *   Use the template in `references/README.md`.
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
    *   Populate only the template sections; do not add new headings such as Documents or Deliverables.
    *   Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting.
    *   Refer to `references/deliverables.md` for content guidance and deliverable selection.
3.  **Notify user after README is created:**
    *   Say: "I have created README.md file, please check and update or approve the content."
    *   Summarize the plan of cumulative milestones toward the MVP.
4.  **Wait for user approval:**
    *   If approved, re-read README.md (user may have updated it), then create other files.
    *   If not approved, update README based on feedback, ask again, then re-read after approval.
5.  **Create `09-sprints/sprint-feature-proposal.md`:**
    *   Follow `references/deliverables.md` for proposal content guidance.

### Step 2: Managing Backlogs (Features)

#### Creating a New Backlog

**CRITICAL:** A Backlog Item is a **FEATURE**. Refer to `dev-swarm/docs/what-is-a-feature.md`.

When creating backlogs:

1.  **File Naming:** `[BACKLOG_TYPE]-[feature-name]-<sub-feature>.md`
2.  **Scope & Definition:**
    *   **Self-Contained:** The backlog includes the *full stack* implementation for that feature.
    *   **User Value:** Describes what the user sees and does.
    *   **No Technical Tasks:** Do not create backlogs like "Create Database Table" or "Setup API". These are sub-tasks of a Feature.
3.  **Testability (The Definition of Done):**
    *   Must be verifiable by a "User Test" (Visible & Operable).
    *   Follow `dev-swarm/docs/sprint-backlog-guidelines.md`.
4.  **Metadata:** Ensure `Feature Name` matches the filename.

#### Updating Backlog Status

Track status: **Not Started** -> **In Development** -> **In Code Review** -> **In Testing** -> **Done**.
Each role adds their findings to the backlog file.

### Step 3: Sprint Planning (The Cumulative Increment)

#### Creating a Sprint

1.  **Define the Milestone:**
    *   **PM & TM Collaboration:** Select a set of Features that form a cohesive update.
    *   **Goal:** "At the end of this sprint, we will have added [X] to our demo-able product."
2.  **Draft the Plan:**
    *   **Sprint Goals:** The narrative of the milestone.
    *   **Backlog Selection:** The list of Features (Backlogs) to build.
    *   **End-User Test Plan:** How to demo the updated product. (e.g., "Log in, search for item, add to cart").
3.  **User Approval:** "Here is the plan for the [Sprint Name] milestone. We will deliver [Features]. Proceed?"
4.  **Create Structure:**
    *   Create `09-sprints/[sprint-name]/README.md` (The Sprint Spec).
    *   Create Backlog files (The Features).
    *   Update `09-sprints/README.md` index.

### Step 4: Prioritizing and Scheduling

1.  **Assess Priority:** Based on User Value and Technical Dependencies.
2.  **Update Plans:** Reflect changes in `09-sprints/README.md` and specific sprint READMEs.

## Available Templates

Use templates in `templates/`:
1. `sprints-readme.md` (Master Plan)
2. `sprint-readme.md` (Sprint Spec)
3. `backlog.md` (Feature Definition)
4. `sprint-feature-proposal.md` (Proposal)
