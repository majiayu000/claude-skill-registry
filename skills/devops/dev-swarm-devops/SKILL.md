---
name: dev-swarm-devops
description: Setup development environment, MCP tools, GitHub repository, and Docker configurations. Use when user asks to setup devops, configure development environment, or start Stage 8 after tech specs.
---

# AI Builder - DevOps Setup

This skill sets up the development environment foundation, including local/cloud environment setup, MCP tools configuration, GitHub repository settings, and Docker/Dev Container configurations.

## When to Use This Skill

- User asks to setup devops or development environment
- User wants to configure GitHub repository
- User needs MCP tools setup for AI agent
- User wants Docker or Dev Container configuration
- Start Stage 8 after tech specs are defined
- When `git remote -v` shows no remote repository linked

## Your Roles in This Skill

- **DevOps Engineer**: Setup and configure development environments, CI/CD pipelines, and deployment infrastructure. Identify the best local or cloud development setup based on project requirements and ensure all tools are properly configured for AI agent usage.
- **Infrastructure Architect**: Design and implement scalable, secure infrastructure solutions. Make decisions on containerization, environment isolation, and development workflow optimization.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `07-tech-specs/` folder exists (mandatory):**
   - If NOT found: Inform user they need to define tech specs first, then STOP
   - If found: Read all files to understand:
     - Technology stack chosen
     - Development tools needed
     - Infrastructure requirements

1.5 **Verify previous stage completion (07-tech-specs):**
   - Read `07-tech-specs/README.md` and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 07, or skip it
     - If skip: create `07-tech-specs/SKIP.md` with a short reason
     - If continue: STOP and return after stage 07 is complete

2. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand all files

3. **Check if this stage should be skipped:**
   - Check if `08-devops/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 8 (devops) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (sprints)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with devops anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

4. **Check if `08-devops/` folder exists:**
   - If exists: Read all existing files to understand current state
   - If NOT exists: Will create new structure

5. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

6. **Assess Current Environment:**
   - Run `git remote -v` to check if remote repository is linked
   - Check if `.git` directory exists
   - Look for existing MCP tools configuration
   - Check for `.devcontainer/` folder
   - Check for `Dockerfile` or `docker-compose.yml`

7. **Analyze Project Requirements:**
   - Based on the tech stack (from `07-tech-specs/`), determine if project needs:
     - Local development only
     - Cloud development environment
     - Containerized development
     - Specific MCP tools (Playwright, GitHub, AWS, etc.)
   - Identify complexity level:
     - **Basic**: Simple projects with minimal setup
     - **Standard**: Projects requiring GitHub + basic MCP tools
     - **Complex**: Projects requiring full cloud setup, multiple MCP tools, advanced Docker configurations

8. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create setup plan files.**

1. **Analyze information from previous stages:**
   - Read `07-tech-specs/` to understand technology stack and tools
   - Consider cost-budget constraints for this stage
   - Assess current environment status

2. **Create or update 08-devops/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - **For L2 projects:** Create a simple README (just several lines) indicating the project level and that only `development-environment.md` (for local setup) is required.
   - **For L3+ projects:** List deliverables explicitly in README (typical: github-setup.md, mcp-setup.md, vscode-devcontainer.md, ci-pipeline.md if CI selected)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** DevOps Engineer (lead), Infrastructure Architect
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What devops setup will include:**
    - **GitHub repository setup options (with checkboxes):**
      - [ ] No Git repo (do not commit code)
      - [ ] Using dev-swarm's git repo
      - [x] Create a new GitHub repo (default when no remote exists)
      - [ ] GitHub Actions for Continuous Integration (CI)
     - MCP tools configuration (list which tools)
     - Development Environment setup (development-environment.md) - **Required for L2 projects**
     - Development container setup (if needed)
     - CI pipeline configuration (if applicable)
   - **Methodology:**
     - How environment will be configured
     - What tools will be installed
   - **Deliverables planned:**
     - List of files that will be created (github-setup.md, mcp-setup.md, development-environment.md, ci-pipeline.md if CI selected, etc.)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the devops approach and what will be configured
   - Summarize what setup files will be created
   - Explain how it aligns with previous stages and tech stack

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create Setup Plan Files

**Only after user approves the README and you re-read it:**

**IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

**These files serve dual purposes:**
1. **Initially**: Setup plans/instructions for user approval
2. **Finally**: Documentation of the actual environment (source of truth for future reset/update)

1. **Create files as specified in the approved README.md:**

   **Typical structure (example):**
   ```
   08-devops/
   ├── README.md (created in Step 1, then reviewed/approved)
   ├── github-setup.md (if specified in README)
   ├── mcp-setup.md (if specified in README)
   ├── ci-pipeline.md (if CI selected in README)
   └── vscode-devcontainer.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

2. **Create setup plan files with proposed configurations:**

**NOTE:** Use `references/deliverables.md` for file-by-file content guidance. Adapt based on the approved README and project needs.

### Step 3: Get User Confirmation

1. Present all setup plan files to the user
2. Explain what will be configured/installed
3. Ask user to review and confirm before proceeding
4. Make any adjustments based on user feedback
5. **DO NOT PROCEED** until user explicitly confirms

### Step 4: Execute Setup Tasks

**ONLY AFTER USER CONFIRMATION**, execute each setup:

1. **Execute GitHub Setup:**
   - Follow steps in `github-setup.md` or `github-repo.md`
   - **Based on user's selected option:**
     - **If "No Git repo":** Skip git setup entirely
     - **If "Using dev-swarm's git repo":** No changes needed, continue with existing repo
     - **If "Create a new GitHub repo":**
       - Ask for user approval before opening the browser or creating the repo
       - Use playwright-browser-* agent skills to automate browser interactions for creating the GitHub repo
       - Initialize git in src/ directory if not already initialized
       - Add the remote repo to src/ using `git remote add origin <repo-url>`
       - Add src/ as a git submodule to the root project using `git submodule add <repo-url> src`
       - Set the submodule branch to `main` unless the user specifies another branch
       - Record repository information in `08-devops/github-repo.md`:
         - Repository URL
         - Repository name
         - Creation date
         - Default branch (main unless specified)
         - Submodule configuration
     - **If user provides a remote repo URL:**
       - Add src/ as a git submodule to root project using `git submodule add <repo-url> src`
       - Set the submodule branch to `main` unless the user specifies another branch
       - Record information in `08-devops/github-repo.md`
   - Create branch protection rules (via GitHub CLI or web) if applicable
   - Create PR templates in `.github/PULL_REQUEST_TEMPLATE.md` if specified
   - Create issue templates if specified
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections

2. **Execute MCP Tools Setup:**
   - Follow steps in `mcp-setup.md`
   - Install/configure each MCP tool specified
   - Setup required credentials and environment variables
   - Create/update MCP configuration files
   - Test each MCP tool connectivity
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Document any manual steps user needs to complete

3. **Execute Dev Container Setup:**
   - Follow steps in `vscode-devcontainer.md`
   - Create `.devcontainer/` folder
   - Create `devcontainer.json` with specified configuration
   - Create `Dockerfile` with specified contents
   - Create `docker-compose.yml` if specified
   - Build container to test
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Fix Dockerfile or configuration issues as needed

### Step 5: Verification and Testing

For each completed setup:

1. **Verify GitHub setup:**
   - If a new repo was created or submodule was added:
     - Run `git submodule status` to verify src/ is properly configured as a submodule
     - Verify `08-devops/github-repo.md` contains accurate repository information
     - Check that src/ has its own git repository with proper remote
     - Run `git remote -v` in src/ directory to confirm remote is linked
   - If using existing dev-swarm repo:
     - Run `git remote -v` to confirm remote is linked
   - Check branch protection rules are applied (if configured)
   - Verify PR templates exist and are formatted correctly (if created)
   - Test creating a test PR (if applicable)

2. **Verify MCP tools:**
   - Test each configured MCP tool with simple commands
   - Ensure AI agent can access MCP tools
   - Verify permissions are correctly set
   - Check environment variables are loaded
   - Document any issues or limitations

3. **Verify Dev Container:**
   - Successfully build container without errors
   - Start container and verify it runs
   - Check all specified tools/extensions are available
   - Test volume mounts work correctly
   - Verify port forwarding is configured
   - Test development workflow inside container

### Step 6: Update Documentation Files

**CRITICAL**: Update all setup files to reflect actual environment:

1. **Update github-setup.md or github-repo.md:**
   - Change from "setup plan" to "current configuration"
   - Document which git repository option was selected
   - If git submodule was created:
     - Document the submodule configuration
     - Document repository URL and name
     - Document default branch (`main` unless specified)
     - Note whether the submodule is pinned to a commit/tag or tracking a branch
     - Document how to initialize/update the submodule
     - Document how to work with the submodule (commit, push, pull)
   - Document actual repository URL, settings applied
   - Document actual branch protection rules in place
   - Note any deviations from original plan
   - Add verification results
   - Add troubleshooting notes for any issues encountered

2. **Update mcp-setup.md:**
   - Change from "setup plan" to "current configuration"
   - Document actual MCP tools installed and versions
   - Document actual configuration file locations and contents
   - Document actual environment variables set
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to reset/reinstall each tool

3. **Update vscode-devcontainer.md:**
   - Change from "setup plan" to "current configuration"
   - Document actual container configuration
   - Add notes about successful build settings
   - Document any modifications made during setup
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to rebuild/reset the container

4. **Update 08-devops/README.md:**
   - Update current environment status to "Configured"
   - Add summary of what was set up
   - Add links to verification results
   - Note date of setup completion

**These updated files now serve as the source of truth for:**
- Future environment resets
- Environment updates
- Onboarding new team members
- Debugging environment issues

### Step 7: Final User Review

1. **Inform user that devops setup is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Show the updated documentation showing actual configuration
   - Show verification results for all setups
   - Confirm everything is working as expected

4. Ask if they want to proceed to `09-sprints/` (next stage)
5. Make any final adjustments based on user feedback if needed

### Step 8: Commit to Git

1. **Ask user if they want to commit the setup:**
   - Stage all changes in `08-devops/`
   - Stage `.devcontainer/` files (if created)
   - Stage `.github/` files (if created)
   - Stage any configuration files (MCP configs, etc.)
   - Commit with message: "Setup DevOps environment and configurations"

2. **Optionally push to remote** (if GitHub was set up)
