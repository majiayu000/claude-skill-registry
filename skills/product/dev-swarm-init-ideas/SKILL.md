---
name: dev-swarm-init-ideas
description: Transform non-technical ideas into professional project kickoff documentation. Use when user asks to init, kickoff, or start a new project, or when ideas.md needs to be formalized into structured documentation.
---

# AI Builder - Initialize Ideas

This skill transforms non-technical or non-professional ideas into professional project kickoff documentation with proper structure and business analysis. It intelligently determines project complexity and scale, then creates only the necessary stages and documentation appropriate for the project size.

## When to Use This Skill

- User asks to "init" or "kickoff" the project
- User wants to start a new project from ideas
- User has an ideas.md file that needs to be formalized
- User wants to create initial project documentation

## Your Roles in This Skill

- **Business Owner**: Ensure commercial success and financial viability. Define business goals, identify the problem statement, and articulate value propositions that balance user value with business profitability.
- **Product Manager**: Create compelling products that meet user needs. Conduct research to identify target users, extract requirements, and ensure the product aligns with both user expectations and business goals.
- **Role Reference**: Consult `dev-swarm/docs/dev-swarm-roles.md` to assign the correct owner/attendances for the 00-init-ideas README. Do not write requirements outside the owning role.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Ensure MCP Server is Configured and Running

1. Check whether the current AI code agent has the `dev-swarm` MCP server configured and running.
2. If it is not configured or not running, refer to reference file `references/mcp-server-check.md` to fix it.

### Step 1: Check for Existing Project and ideas.md

1. **Check if `src/` folder exists and contains files:**
   - Check if `src/` directory exists
   - Check if `src/` contains any files (other than just `.gitkeep`)
   - **If src/ contains an existing project:**
     - Inform the user: "An existing project was found in src/. Before starting a new project, the current project should be archived."
     - Ask the user: "Would you like me to archive the existing project using the project-archive skill?"
     - **If user says yes:**
       - Use the Skill tool to invoke `dev-swarm-project-archive`
       - Wait for archiving to complete
       - Then proceed with this skill
     - **If user says no:**
       - Stop execution and inform the user they need to handle the existing project first
       - Exit the skill

2. **Check if `00-init-ideas/` folder exists and has content:**
   - If exists with content: Read all existing files to understand current state
   - If exists but empty (only .gitkeep): Will create new structure
   - If NOT exists: Will create new structure

3. **Check if `ideas.md` exists in the project root:**
   - If exists: Read and analyze the content as input
   - If NOT exists: Ask the user to provide basic ideas for the project, then create `ideas.md`

4. Proceed to Step 2 with gathered context

### Step 2: Classify Project Complexity and Scale

1. **Read the classification standard and scaling rules:**
   - Read `dev-swarm/docs/software-dev-classification.md`
   - Read `dev-swarm/docs/research-specs-rules.md`
   - Read `dev-swarm/docs/mermaid-diagram-guide.md`

2. **Analyze ideas.md to determine:**
   - **Project Purpose (P1-P4):**
     - P1: Personal Tool (individual use, disposable)
     - P2: Internal Tool (team/company use)
     - P3: Open Source Project (public collaboration)
     - P4: Commercial/Profit-Oriented Product

   - **Development Scale (L0-L7):**
     - L0: One-Off Execution (run once, single file)
     - L1: Reusable Script (used repeatedly, basic args)
     - L2: Tool with Environment Setup (dependencies, packaging)
     - L3: Single-Service Application (real app with users)
     - L4: Product MVP (minimal viable product)
     - L5: Multi-Platform MVP (web + mobile)
     - L6: Growth-Stage Product (scaling users/team)
     - L7: Platform/Ecosystem (others build on it)

3. **Document the classification:**
   - Record the classification using the README template checkboxes
   - Do not add separate classification statements or exclusion sections outside the template

### Step 3: Extract Project Information

From the ideas.md file and any existing documentation:
1. Identify and pick the best project name
2. Extract key requirements and goals
3. Identify problem statements
4. Identify target users
5. Extract value propositions

### Step 4: Determine Required Stages Based on Project Scale

Based on the determined scale level, decide which stages are needed:

**For L0-L1 (Very Small Projects - Scripts):**
- 00-init-ideas/README.md (how to implement the script or refined requirements)
- src/script_name.sh (or appropriate extension)
- NO other stages needed

**For L2 (Tool with Environment):**
- 00-init-ideas/ (required)
- 07-tech-specs/ (minimal)
- 08-devops/ (basic setup with development-environment.md)
- 10-deployment/ (required for tools/agent skills)
- SKIP: 01-market-research, 02-personas, 03-mvp, 04-prd, 05-ux, 06-architecture, 09-sprints

**For L3-L4 (Single Service / MVP):**
- All stages except possibly 10-deployment (if not deploying to cloud yet)

**For L5-L7 (Multi-Platform / Growth / Platform):**
- ALL stages required (00 through 10)

Stage READMEs are created only when each stage starts. See
`dev-swarm/docs/stage-readme-guidelines.md` for the shared README prep steps.

### Step 5: Project Root README.md
   - **IMPORTANT: DO NOT create or modify the root README.md file**
   - The project readme file we are developing should be maintained in `src/README.md` by developers

### Step 6: Create Stage Folder Structure

Create folders from `00-init-ideas` through `10-deployment` without creating
stage README or SKIP files for stages 01-10. Each stage README is created only
when that stage starts.

1. **00-init-ideas (ALWAYS REQUIRED):**
   - Create the folder only here. The README.md is created in Step 8.

2. **For stages 01-10:**
   - Create empty folders only.
   - Do not create README.md or SKIP.md in this step.
   - Record which stages are expected to be skipped in
     `00-init-ideas/README.md` for user to review or update.

3. **Create basic folder structure if needed:**
   - Also create: `features/`, `src/`, `99-archive/`
   - Add `.gitkeep` files to empty folders if necessary

### Step 7: User Confirmation on Structure

1. **Present the proposed structure to the user:**
   - Show which stages will be created
   - Show which stages will be skipped (with reasons)
   - Show the classification selections (checkboxes)

2. **Ask user to confirm:**
   - "Does this project structure match your expectations?"
   - "Should any stages be added or removed?"

3. **Make adjustments based on user feedback**

### Step 8: Create 00-init-ideas Documentation

**Once user confirms the structure:**

1. **For L0-L1 projects:**
   - Create detailed 00-init-ideas/README.md with:
     - How to implement the script/tool
     - Requirements and specifications
     - Usage instructions
   - Say: "I have created README.md file, please check and update or approve the content."
   - If approved, re-read README.md (user may have updated it), then ask if user wants to proceed with implementation in src/

2. **For L2+ projects:**
   - Create 00-init-ideas/README.md first without pre-approval
   - Use the README template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Do not add extra headings beyond the template; use the Stage files checklist to list docs and avoid a separate Documents section
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Any options or solutions in the README must be presented as checkboxes with
     a default selection
   - Say: "I have created README.md file, please check and update or approve the content."
   - After approval, re-read README.md (user may have updated it). README.md is already created (owner: Business Owner, attendances: Product Manager). Then create all remaining documentation files in 00-init-ideas/
   - Create `SKIP.md` in each skipped stage folder based on the selections in
     the "Skipped stages" section of `00-init-ideas/README.md`
   - After creating skip files, remove the "## Skipped stages" section from
     `00-init-ideas/README.md` and tell the user this section is no longer needed

**File Content Guidance:**

Refer to `references/deliverables.md` for file-by-file content guidance, including cost-budget expectations.

### Step 9: User Confirmation on 00-init-ideas Content

1. **Ask the user to review:**
   - All generated documentation in `00-init-ideas/`
   - The classification and project structure
   - Content accuracy and completeness

2. **Make any adjustments based on user feedback**
   - If user wants to reduce budget: Adjust stage scope, research depth, or testing coverage
   - If user wants to increase budget: Expand scope, add more thorough research/testing

3. **Ask if they want to proceed to the next stage:**
   - For L0-L1: "Would you like me to implement the script in src/?"
   - For L2+: "Do you approve the estimated budget? Would you like me to proceed to the next stage (market-research or personas)?"

### Step 10: Initialize Git Repository (if needed)

1. Check if git repository is initialized
2. If not, run `git init`

### Step 11: Commit to Git (if user confirms)

1. **If user confirms the contents are good:**
   - Ask if they want to commit to git

2. **If user wants to commit:**
   - Stage all created/modified files
   - Use the dev-swarm-draft-commit-message skill to draft the commit message
   - Commit with the drafted message (should follow conventional commit format)
   - Example: "feat: initialize project with ideas documentation and stage structure"
