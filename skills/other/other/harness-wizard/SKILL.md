---
name: harness-wizard
description: Autonomous Agent Harness wizard for long-running multi-agent projects. Configures the harness pipeline (initializer, coder, tester, reviewer), sets up Archon state management, and creates session handoff protocols.
---

# Autonomous Agent Harness Wizard

Interactive wizard for setting up autonomous long-running agent harnesses. Creates fully-configured autonomous coding projects that can work across multiple sessions with proper state management, agent handoffs, and comprehensive testing strategies.

## When to Activate

Use this skill when:
- User selected Autonomous Harness in project wizard
- Setting up greenfield projects with autonomous agents
- Creating long-running development projects
- Multi-session projects requiring state persistence
- Keywords: harness wizard, setup harness, autonomous setup, multi-session, agent harness, long-running project

---

## Architecture Overview

```
MULTI-AGENT PIPELINE ARCHITECTURE

                          PROJECT WIZARD
                               │
                               ▼
              ┌────────────────────────────────┐
              │      /harness-setup            │
              │      @harness-wizard           │
              │  (This Skill - Configuration)  │
              └────────────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │      /harness-init             │
              │      @harness-initializer      │
              │  (First Session - Task Gen)    │
              └────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────┐
    │                 DEVELOPMENT LOOP                      │
    │  ┌─────────────────────────────────────────────────┐ │
    │  │           /harness-next                         │ │
    │  │           @harness-coder                        │ │
    │  │      (Feature Implementation)                   │ │
    │  └───────────────────┬─────────────────────────────┘ │
    │                      │                                │
    │           ┌──────────┴──────────┐                    │
    │           │                     │                    │
    │           ▼                     ▼                    │
    │  ┌──────────────────┐  ┌──────────────────┐         │
    │  │ @harness-tester  │  │ @harness-reviewer│         │
    │  │  (Parallel Test) │  │ (Before Complete)│         │
    │  └──────────────────┘  └──────────────────┘         │
    │           │                     │                    │
    │           └──────────┬──────────┘                    │
    │                      ▼                                │
    │              [Update Archon]                         │
    │              [Commit Changes]                        │
    │              [Repeat for each feature]               │
    └──────────────────────────────────────────────────────┘

    STATE MANAGEMENT: Archon MCP (Projects, Tasks, Documents)
```

### Agent Pipeline Summary

| Agent | Skill | Role | When Used |
|-------|-------|------|-----------|
| Setup Agent | `@harness-wizard` | Interactive configuration | Initial setup |
| Initializer | `@harness-initializer` | Generate tasks from spec | First session only |
| Coder | `@harness-coder` | Implement features | Every coding session |
| Tester | `@harness-tester` | Run tests & verify | After implementation |
| Reviewer | `@harness-reviewer` | Code quality check | Before marking complete |

---

## Wizard Entry Points

The harness wizard can be invoked through multiple paths:

```
ENTRY POINTS

1. Direct Invocation:
   User: "Set up autonomous harness"
   → Activates @harness-wizard

2. Project Wizard Delegation:
   User selects "Autonomous Harness" in project wizard
   → @project-wizard delegates to @harness-wizard

3. Resume Mode:
   User: "Resume my harness project"
   → @harness-wizard in resume mode

4. Quick Setup:
   User: "Quick harness setup for [project description]"
   → @harness-wizard with smart defaults
```

---

## Setup Modes

### Mode 1: Full Setup (Default)

Complete interactive wizard for new projects. Ask all questions systematically through phases.

**Best for:**
- New greenfield projects
- Users who want full control
- Complex applications

### Mode 2: Quick Setup

Minimal questions with smart defaults. Infers configuration from context.

**Best for:**
- Experienced users
- Existing codebases being harnessed
- Simple projects

### Mode 3: Resume Mode

Continue an existing harness project. Query Archon for project state.

**Best for:**
- Returning to paused projects
- Session recovery
- Status checks

---

## Full Setup Questionnaire

When running full setup, gather information in these phases:

### Phase 1: Project Basics

```markdown
## Harness Setup Wizard - Phase 1: Project Basics

**1. Project Name:**
   What should the project be called?
   > Use lowercase with hyphens (e.g., "saas-dashboard", "e-commerce-api")
   > Must be valid directory name (max 64 characters)

**2. Project Description:**
   Brief description of what you're building (1-3 sentences)
   > This appears in Archon and README

**3. Project Type:**
   What kind of project is this?
   - [ ] Web Application (Frontend + Backend)
   - [ ] API/Backend Only
   - [ ] CLI Application
   - [ ] Full-Stack with Database
   - [ ] Library/Package
   - [ ] Mobile App Backend
   - [ ] Other: ___

**4. Working Directory:**
   Where should the project be created?
   > Default: current directory
   > Example: E:\Repos\MyOrg\projects

**5. GitHub Repository:**
   How should we handle version control?
   - [ ] Create new repository
   - [ ] Use existing: [URL]
   - [ ] No GitHub integration (local only)
```

### Phase 2: Technical Stack

```markdown
## Phase 2: Technical Stack

**6. Primary Language:**
   What programming language?
   - [ ] TypeScript/JavaScript
   - [ ] Python
   - [ ] Go
   - [ ] Rust
   - [ ] Java/Kotlin
   - [ ] C# / .NET
   - [ ] Other: ___

**7. Framework (if applicable):**

   Frontend Framework:
   - [ ] React
   - [ ] Vue
   - [ ] Svelte
   - [ ] Next.js
   - [ ] Angular
   - [ ] None / Other

   Backend Framework:
   - [ ] Express/Fastify
   - [ ] FastAPI
   - [ ] Gin (Go)
   - [ ] Actix (Rust)
   - [ ] Spring Boot
   - [ ] ASP.NET Core
   - [ ] None / Other

**8. Database:**
   What database will you use?
   - [ ] PostgreSQL
   - [ ] MySQL/MariaDB
   - [ ] MongoDB
   - [ ] SQLite
   - [ ] Supabase
   - [ ] Firebase
   - [ ] None / TBD

**9. Package Manager:**
   Which package manager?
   - [ ] npm
   - [ ] yarn
   - [ ] pnpm
   - [ ] pip / poetry
   - [ ] go mod
   - [ ] cargo
   - [ ] nuget
```

### Phase 3: Agent Configuration

```markdown
## Phase 3: Agent Configuration

**10. Target Feature Count:**
    How many features should be generated from the spec?
    > Recommended: 20-50 for medium projects
    > Default: 30
    > Range: 10-100

**11. Session Iteration Limit:**
    Max tool calls per coding session?
    > 0 = unlimited
    > Default: 50
    > Range: 25-200

**12. Claude Model Preference:**
    Which model should the agents use?
    - [ ] claude-opus-4-5-20251101
          (Best for complex reasoning, architecture decisions)
    - [ ] claude-sonnet-4-20250514
          (Recommended - good balance of speed and capability)
    - [ ] claude-haiku-3-5-20241022
          (Fastest - good for quick iterations)

**13. Execution Mode:**
    How will you run the agents?
    - [ ] Terminal: Manual prompt execution (recommended)
    - [ ] Background: Run in background process
    - [ ] SDK: Python automation script
    - [ ] All modes supported
```

### Phase 4: MCP Server Configuration

```markdown
## Phase 4: MCP Server Configuration

**14. MCP Servers to Enable:**
    Which MCP servers should be available to agents?

    Required:
    - [x] Archon (State management - always required)

    Recommended:
    - [ ] Playwright (Browser automation for E2E testing)
    - [ ] GitHub (Repository operations, PR management)
    - [ ] Brave Search (Web research during development)

    Optional:
    - [ ] Filesystem (Enhanced file operations)
    - [ ] Memory (Persistent memory across sessions)
    - [ ] Sequential Thinking (Complex reasoning)

    Custom:
    - [ ] Other: ___ (specify MCP server name)

**15. MCP Server Configurations:**
    For each selected server, provide configuration if needed:
    > Most servers use defaults
    > Archon requires ARCHON_URL environment variable
```

### Phase 5: Testing Strategy

```markdown
## Phase 5: Testing Strategy

**16. Testing Requirements:**
    What level of testing do you want?
    - [ ] Unit tests only
          (Fast, isolated tests for functions/components)
    - [ ] Unit + Integration tests
          (Includes API and database testing)
    - [ ] Full E2E with browser automation
          (Complete user flow testing)
    - [ ] Manual testing only
          (No automated test suite)

**17. Browser Testing Tool (if E2E selected):**
    - [ ] Playwright MCP (Recommended - built-in)
    - [ ] Puppeteer MCP
    - [ ] None / Manual browser testing

**18. Test Framework:**
    Based on your language, which test framework?

    TypeScript/JavaScript:
    - [ ] Jest
    - [ ] Vitest (recommended)
    - [ ] Mocha

    Python:
    - [ ] pytest (recommended)
    - [ ] unittest

    Go:
    - [ ] go test (built-in)

    Rust:
    - [ ] cargo test (built-in)

    C# / .NET:
    - [ ] xUnit (recommended)
    - [ ] NUnit
    - [ ] MSTest

**19. Test Coverage Target:**
    Minimum code coverage percentage?
    > Default: 80%
    > Range: 50-100%
```

### Phase 6: Security Configuration

```markdown
## Phase 6: Security Configuration

**20. Allowed Bash Commands:**
    Which commands should agents be allowed to execute?

    Package Managers:
    - [ ] npm, npx, yarn, pnpm
    - [ ] pip, poetry, pipx
    - [ ] go
    - [ ] cargo
    - [ ] dotnet

    Version Control:
    - [ ] git (all operations)
    - [ ] gh (GitHub CLI)

    Build Tools:
    - [ ] tsc, webpack, vite, esbuild
    - [ ] make, cmake

    Test Runners:
    - [ ] jest, vitest, mocha
    - [ ] pytest
    - [ ] go test
    - [ ] cargo test
    - [ ] dotnet test

    Database Commands:
    - [ ] psql, mysql, mongosh
    - [ ] prisma, drizzle, typeorm

    Container Commands:
    - [ ] docker, docker-compose

**21. Denied Commands (Security):**
    Commands that should NEVER be executed:
    - [x] rm -rf (recursive delete)
    - [x] sudo (elevated privileges)
    - [x] curl/wget (arbitrary downloads)
    - [x] eval, exec (arbitrary code execution)
    - [ ] Custom: ___

**22. Filesystem Restrictions:**
    How should file access be restricted?
    - [ ] Restrict to project directory only (recommended)
    - [ ] Allow parent directory access
    - [ ] Allow home directory access
    - [ ] No restrictions

**23. Secret Handling:**
    How should secrets/credentials be managed?
    - [ ] Environment variables only (recommended)
    - [ ] .env file support
    - [ ] Secret manager integration (AWS/Azure/GCP)
    - [ ] No secrets needed
```

### Phase 7: Session Handoff Configuration

```markdown
## Phase 7: Session Handoff Configuration

**24. Handoff Document Location:**
    Where should session notes be saved?
    > In addition to Archon, a local file can be maintained
    - [ ] .harness/session-notes.md (default)
    - [ ] docs/session-notes.md
    - [ ] No local file (Archon only)

**25. Context Preservation:**
    What should be included in handoffs?
    - [x] Tasks completed this session
    - [x] Current task in progress
    - [x] Test results summary
    - [x] Blockers and issues
    - [ ] Full git diff summary
    - [ ] Files modified list
    - [ ] Decisions made
    - [ ] Questions for next session

**26. Auto-Commit Configuration:**
    Should agents automatically commit changes?
    - [ ] Yes, commit at end of each session (recommended)
    - [ ] Yes, commit after each feature completion
    - [ ] No, manual commits only

**27. Commit Message Style:**
    What commit message format?
    - [ ] Conventional Commits (feat:, fix:, etc.)
    - [ ] Simple descriptive
    - [ ] Include task ID reference
```

### Phase 8: Application Specification

```markdown
## Phase 8: Application Specification

**28. Application Specification:**
    Provide a detailed description of the application to build.

    Include:
    - Core features and functionality
    - User flows and interactions
    - Data models and relationships
    - Authentication requirements
    - Third-party integrations
    - UI/UX requirements (if applicable)
    - API endpoints needed
    - Performance requirements
    - Scalability considerations

    **Tip:** The more detailed the spec, the better the generated features.
    Aim for 500-2000 words for best results.

    You can provide:
    - [ ] Inline specification (type/paste here)
    - [ ] File path to existing spec document
    - [ ] URL to specification (will be fetched)
```

---

## Harness Configuration Generation

After gathering all questionnaire responses, generate the `.harness/` directory structure:

### Directory Structure

```
.harness/
├── config.json              # Main harness configuration
├── prompts/
│   ├── initializer.md       # Feature breakdown prompt template
│   ├── coder.md             # Implementation prompt template
│   ├── tester.md            # Testing prompt template
│   └── reviewer.md          # Review prompt template
├── templates/
│   ├── feature-task.md      # Task description template
│   ├── session-notes.md     # Handoff template
│   └── test-report.md       # Test results template
└── state/
    ├── current-session.json # Active session state
    └── history/             # Session history archive
        └── .gitkeep
```

### config.json Structure

Generate the main configuration file:

```json
{
  "harness_version": "2.0.0",
  "created_at": "[ISO_TIMESTAMP]",
  "updated_at": "[ISO_TIMESTAMP]",

  "project": {
    "name": "[PROJECT_NAME]",
    "description": "[PROJECT_DESCRIPTION]",
    "type": "[PROJECT_TYPE]",
    "path": "[FULL_PATH]",
    "archon_project_id": "[ARCHON_ID]",
    "github_repo": "[GITHUB_URL_OR_NULL]"
  },

  "tech_stack": {
    "language": "[LANGUAGE]",
    "framework": {
      "frontend": "[FRONTEND_FRAMEWORK_OR_NULL]",
      "backend": "[BACKEND_FRAMEWORK_OR_NULL]"
    },
    "database": "[DATABASE_OR_NULL]",
    "package_manager": "[PACKAGE_MANAGER]",
    "test_framework": "[TEST_FRAMEWORK]"
  },

  "agents": {
    "initializer": {
      "max_features": 30,
      "model": "claude-sonnet-4-20250514",
      "prompt_template": ".harness/prompts/initializer.md"
    },
    "coder": {
      "iteration_limit": 50,
      "model": "claude-sonnet-4-20250514",
      "prompt_template": ".harness/prompts/coder.md",
      "one_feature_per_session": true
    },
    "tester": {
      "parallel": true,
      "model": "claude-sonnet-4-20250514",
      "prompt_template": ".harness/prompts/tester.md",
      "run_after_implementation": true
    },
    "reviewer": {
      "model": "claude-sonnet-4-20250514",
      "prompt_template": ".harness/prompts/reviewer.md",
      "run_before_complete": true,
      "block_on_critical": true
    }
  },

  "mcp_servers": {
    "required": ["archon"],
    "enabled": ["archon", "playwright", "github"],
    "configurations": {
      "archon": {
        "url": "${ARCHON_URL}"
      },
      "playwright": {
        "headless": true
      }
    }
  },

  "testing": {
    "strategy": "unit_integration",
    "coverage_target": 80,
    "browser_tool": "playwright",
    "test_commands": {
      "unit": "npm test",
      "integration": "npm run test:integration",
      "e2e": "npx playwright test",
      "all": "npm run test:all"
    },
    "require_passing_before_complete": true
  },

  "security": {
    "allowed_commands": [
      "npm", "npx", "node",
      "git", "gh",
      "tsc", "vite", "esbuild",
      "jest", "vitest"
    ],
    "denied_commands": [
      "rm -rf",
      "sudo",
      "curl",
      "wget",
      "eval"
    ],
    "filesystem_restricted": true,
    "project_root_only": true,
    "env_file_support": true
  },

  "handoffs": {
    "auto_commit": true,
    "commit_style": "conventional",
    "local_notes_path": ".harness/state/session-notes.md",
    "include_in_handoff": [
      "tasks_completed",
      "current_task",
      "test_results",
      "blockers",
      "decisions"
    ],
    "archon_session_document": true
  },

  "status": "initializing"
}
```

### Prompt Templates

Generate agent-specific prompt templates:

#### .harness/prompts/initializer.md

```markdown
# Harness Initializer Prompt

You are the initializer agent for the [PROJECT_NAME] harness project.

## Your Mission

Read the application specification and generate detailed feature tasks in Archon.
This is the FIRST session - you set up everything for the coding agent.

## Project Context

- **Project**: [PROJECT_NAME]
- **Archon Project ID**: [ARCHON_PROJECT_ID]
- **Type**: [PROJECT_TYPE]
- **Stack**: [LANGUAGE] / [FRAMEWORK]
- **Database**: [DATABASE]

## Application Specification

[FULL_APP_SPEC_HERE]

## Your Tasks

1. Read and analyze the specification thoroughly
2. Break down into [MAX_FEATURES] detailed feature tasks
3. Create tasks in Archon with proper priority ordering
4. Set up project directory structure
5. Initialize development environment
6. Create clean handoff for coding agent

## Task Creation Guidelines

- Each task = 30 min to 4 hours of work
- Include acceptance criteria
- Include test steps
- Order by dependencies (high priority first)
- Group by feature tag

## Use the harness-initializer skill for full protocol.
```

#### .harness/prompts/coder.md

```markdown
# Harness Coding Prompt

You are the coding agent for the [PROJECT_NAME] harness project.

## Your Mission

Continue development from the previous session. Implement ONE feature per session
and maintain clean handoffs via Archon.

## Project Context

- **Project**: [PROJECT_NAME]
- **Archon Project ID**: [ARCHON_PROJECT_ID]
- **Stack**: [LANGUAGE] / [FRAMEWORK]

## Session Protocol

1. **Orient** - Read Archon session notes and current state
2. **Verify** - Run tests to confirm existing features work
3. **Implement** - Complete ONE task from highest priority TODO
4. **Test** - Coordinate with harness-tester skill
5. **Review** - Coordinate with harness-reviewer skill (if enabled)
6. **Handoff** - Update Archon and commit changes

## Constraints

- Max iterations: [ITERATION_LIMIT]
- Testing required: [TESTING_STRATEGY]
- Auto-commit: [AUTO_COMMIT]

## Use the harness-coder skill for full protocol.
```

#### .harness/prompts/tester.md

```markdown
# Harness Testing Prompt

You are the testing agent for the [PROJECT_NAME] harness project.

## Your Mission

Run comprehensive tests and report results to Archon.

## Testing Strategy: [TESTING_STRATEGY]

### Test Commands
- Unit: `[UNIT_TEST_COMMAND]`
- Integration: `[INTEGRATION_TEST_COMMAND]`
- E2E: `[E2E_TEST_COMMAND]`

### Coverage Target: [COVERAGE_TARGET]%

### Browser Testing
- Tool: [BROWSER_TOOL]
- Headless: true

## Protocol

1. Identify test scope (specific feature or full suite)
2. Run appropriate tests
3. Collect and analyze results
4. Report to Archon task
5. Block completion if tests fail

## Use the harness-tester skill for full protocol.
```

#### .harness/prompts/reviewer.md

```markdown
# Harness Review Prompt

You are the code review agent for the [PROJECT_NAME] harness project.

## Your Mission

Review code changes before features are marked complete.
Ensure quality, security, and architectural consistency.

## Review Checklist

### Code Quality
- [ ] Functions are focused (single responsibility)
- [ ] Variable names are meaningful
- [ ] Proper error handling
- [ ] No debug statements or TODOs

### Architecture
- [ ] Follows existing patterns
- [ ] Correct layer placement
- [ ] No circular dependencies

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] Authentication checks

### Testing
- [ ] Tests exist for new functionality
- [ ] Edge cases covered
- [ ] No tests removed

## Verdicts

- **APPROVED**: Ready to complete
- **CHANGES_REQUESTED**: Address findings
- **BLOCKED**: Critical issue, cannot complete

## Use the harness-reviewer skill for full protocol.
```

---

## Project Generation Workflow

After collecting all questionnaire responses, execute this workflow:

### Step 1: Create Archon Project

```python
# Create the project in Archon
project = manage_project("create",
    title="[PROJECT_NAME]",
    description="""[PROJECT_DESCRIPTION]

Harness Type: Autonomous Coding Agent
Project Type: [PROJECT_TYPE]
Stack: [LANGUAGE] / [FRAMEWORK]
Created: [TIMESTAMP]""",
    github_repo="[GITHUB_URL_OR_NONE]"
)
PROJECT_ID = project["project"]["id"]
```

### Step 2: Store Configuration Documents in Archon

```python
# Store harness configuration as Archon document
manage_document("create",
    project_id=PROJECT_ID,
    title="Harness Configuration",
    document_type="guide",
    content=HARNESS_CONFIG_JSON,
    tags=["harness", "config", "settings"]
)

# Store application specification
manage_document("create",
    project_id=PROJECT_ID,
    title="Application Specification",
    document_type="spec",
    content={
        "specification": "[FULL_APP_SPEC]",
        "version": "1.0",
        "created_at": "[TIMESTAMP]",
        "last_updated": "[TIMESTAMP]"
    },
    tags=["harness", "spec", "requirements"]
)

# Create session notes document
manage_document("create",
    project_id=PROJECT_ID,
    title="Session Notes",
    document_type="note",
    content={
        "sessions": [],
        "current_focus": None,
        "blockers": [],
        "next_steps": ["Run harness-initializer to begin"],
        "decisions": [],
        "last_updated": "[TIMESTAMP]"
    },
    tags=["harness", "handoff", "session", "tracking"]
)
```

### Step 3: Create META Task

```python
# Create META task for session tracking
manage_task("create",
    project_id=PROJECT_ID,
    title="META: Session Tracking & Handoffs",
    description="""This task tracks session-level progress and handoffs.

## Current Session Status
- Session: Not started
- Agent: None
- Status: Awaiting initialization

## Instructions
Update this task at the END of each session with:
1. What was completed
2. Current task being worked on
3. Any blockers or issues
4. Context for next session

## Progress
- Total Tasks: Pending initialization
- Completed: 0
- Remaining: TBD

## DO NOT mark this task as done - it's for tracking only.""",
    status="doing",
    task_order=100,
    feature="Meta",
    assignee="Session Tracker"
)
```

### Step 4: Create Initialization Task

```python
# Create initialization task
manage_task("create",
    project_id=PROJECT_ID,
    title="Initialize project and generate feature tasks",
    description="""First session initialization task.

## Tasks
1. Read Application Specification from Archon documents
2. Analyze and break down into [MAX_FEATURES] feature tasks
3. Create tasks in Archon with proper priorities
4. Create project directory structure
5. Initialize git repository
6. Set up development environment
7. Run init.sh / init.ps1
8. Verify environment works
9. Update Session Notes document
10. Commit initial structure

## Guidelines
- Each feature task: 30 min to 4 hours of work
- Include acceptance criteria
- Include test verification steps
- Order by dependencies (foundation first)
- Group related tasks by feature tag

## Output
- All tasks created in Archon
- Project structure ready
- Clean handoff for coding agent""",
    status="todo",
    task_order=99,
    feature="Setup",
    assignee="Initializer Agent"
)
```

### Step 5: Create Local Project Files

Create the following files in the project directory:

#### .harness/config.json

(Use the generated config.json structure from above)

#### init.sh (Linux/Mac)

```bash
#!/bin/bash
set -e

echo "======================================"
echo "Initializing [PROJECT_NAME] harness..."
echo "======================================"

# Create directory structure
echo "Creating directory structure..."
mkdir -p src tests docs .harness/state/history

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init

    # Create .gitignore
    cat > .gitignore << 'GITIGNORE'
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.venv/

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test coverage
coverage/
.coverage
htmlcov/

# Harness local state
.harness/state/current-session.json
.harness/state/history/*
!.harness/state/history/.gitkeep

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
GITIGNORE
fi

# Framework-specific initialization
[FRAMEWORK_INIT_COMMANDS]

# Verify setup
echo ""
echo "Verifying setup..."
[VERIFICATION_COMMANDS]

echo ""
echo "======================================"
echo "Environment ready!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Use harness-initializer skill to generate tasks"
echo "  2. Or use harness-coder skill for coding sessions"
echo ""
echo "Archon Project ID: [PROJECT_ID]"
```

#### init.ps1 (Windows)

```powershell
# Harness initialization script for Windows
$ErrorActionPreference = "Stop"

Write-Host "======================================"
Write-Host "Initializing [PROJECT_NAME] harness..."
Write-Host "======================================"

# Create directory structure
Write-Host "Creating directory structure..."
New-Item -ItemType Directory -Force -Path src, tests, docs, ".harness\state\history" | Out-Null

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..."
    git init

    # Create .gitignore
    @"
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.venv/

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test coverage
coverage/
.coverage
htmlcov/

# Harness local state
.harness/state/current-session.json
.harness/state/history/*
!.harness/state/history/.gitkeep

# Logs
*.log
npm-debug.log*
"@ | Out-File -FilePath .gitignore -Encoding utf8
}

# Framework-specific initialization
[FRAMEWORK_INIT_COMMANDS_PS1]

# Verify setup
Write-Host ""
Write-Host "Verifying setup..."
[VERIFICATION_COMMANDS_PS1]

Write-Host ""
Write-Host "======================================"
Write-Host "Environment ready!"
Write-Host "======================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Use harness-initializer skill to generate tasks"
Write-Host "  2. Or use harness-coder skill for coding sessions"
Write-Host ""
Write-Host "Archon Project ID: [PROJECT_ID]"
```

#### .harness/SKILLS.md

```markdown
# Harness Skills Reference

This project uses the autonomous agent harness system.

## Skill Pipeline

```
Setup:     @harness-wizard      (You are here - done)
           ↓
Init:      @harness-initializer (First session only)
           ↓
Loop:      @harness-coder       (Every coding session)
           ↓       ↓
           │   @harness-tester  (Parallel testing)
           │
           @harness-reviewer    (Before completion)
```

## Quick Commands

| Command | Skill | Purpose |
|---------|-------|---------|
| `/harness-init` | harness-initializer | First session setup |
| `/harness-next` | harness-coder | Continue development |
| `/harness-test` | harness-tester | Run test suite |
| `/harness-review` | harness-reviewer | Code review |
| `/harness-status` | (manual) | Check Archon status |

## Session Workflow

### First Session
```
1. Use @harness-initializer
2. It will:
   - Read the app specification
   - Generate feature tasks
   - Set up project structure
   - Create handoff for coder
```

### Coding Sessions
```
1. Use @harness-coder
2. It will:
   - Load previous session state
   - Verify existing features
   - Implement ONE feature
   - Run tests
   - Get review (if enabled)
   - Update Archon
   - Commit and handoff
```

## Archon Quick Reference

```python
# Get project status
find_tasks(filter_by="project", filter_value="[PROJECT_ID]")

# Get session notes
find_documents(project_id="[PROJECT_ID]", query="Session Notes")

# Update task status
manage_task("update", task_id="...", status="doing")
manage_task("update", task_id="...", status="done")
```

## Configuration

See `.harness/config.json` for full configuration.

Key settings:
- Max features: [MAX_FEATURES]
- Iteration limit: [ITERATION_LIMIT]
- Model: [MODEL]
- Testing: [TESTING_STRATEGY]
- Auto-commit: [AUTO_COMMIT]
```

### Step 6: Framework-Specific Setup

Based on the selected tech stack, add framework-specific files:

#### TypeScript/JavaScript + React/Next.js

```json
// package.json additions
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "vitest",
    "test:integration": "vitest run --config vitest.integration.config.ts",
    "test:e2e": "playwright test",
    "test:all": "npm run test && npm run test:integration && npm run test:e2e",
    "lint": "eslint . --ext .ts,.tsx",
    "type-check": "tsc --noEmit"
  }
}
```

#### Python + FastAPI

```toml
# pyproject.toml additions
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21",
    "httpx>=0.24",
    "ruff>=0.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
```

### Step 7: Display Setup Summary

```markdown
## Harness Setup Complete!

### Project Created
| Field | Value |
|-------|-------|
| **Name** | [PROJECT_NAME] |
| **Type** | [PROJECT_TYPE] |
| **Location** | [FULL_PATH] |
| **Archon ID** | [PROJECT_ID] |
| **GitHub** | [GITHUB_URL_OR_LOCAL] |

### Technical Stack
| Component | Selection |
|-----------|-----------|
| **Language** | [LANGUAGE] |
| **Frontend** | [FRONTEND_FRAMEWORK] |
| **Backend** | [BACKEND_FRAMEWORK] |
| **Database** | [DATABASE] |
| **Test Framework** | [TEST_FRAMEWORK] |

### Agent Configuration
| Setting | Value |
|---------|-------|
| **Max Features** | [MAX_FEATURES] |
| **Iteration Limit** | [ITERATION_LIMIT] |
| **Model** | [MODEL] |
| **Testing Strategy** | [TESTING_STRATEGY] |
| **Coverage Target** | [COVERAGE_TARGET]% |
| **Auto-Commit** | [AUTO_COMMIT] |

### MCP Servers Enabled
[LIST_OF_MCP_SERVERS]

### Files Created
```
[PROJECT_NAME]/
├── .harness/
│   ├── config.json
│   ├── prompts/
│   │   ├── initializer.md
│   │   ├── coder.md
│   │   ├── tester.md
│   │   └── reviewer.md
│   ├── templates/
│   └── state/
├── .gitignore
├── init.sh / init.ps1
└── [FRAMEWORK_FILES]
```

### Archon Resources Created
- Project record
- Harness Configuration document
- Application Specification document
- Session Notes document
- META tracking task
- Initialization task

---

## Next Steps

### Option 1: Initialize Now (Recommended)
Use the `@harness-initializer` skill to:
- Generate feature tasks from your specification
- Set up the development environment
- Create the first handoff

### Option 2: Manual Start
1. Run the init script: `./init.sh` or `.\init.ps1`
2. Then use `@harness-initializer`

### Option 3: Quick Resume Command
```
Use harness-initializer skill to begin project initialization
```

---

**Tip**: The initializer will read your app specification and create all feature
tasks. This typically takes 5-15 minutes depending on specification complexity.
```

---

## Quick Setup Mode

For quick setup, use these defaults and only ask essential questions:

### Smart Defaults

```yaml
defaults:
  feature_count: 30
  iteration_limit: 50
  model: claude-sonnet-4-20250514
  testing_strategy: unit_integration
  coverage_target: 80
  browser_tool: playwright
  execution_mode: terminal
  auto_commit: true
  commit_style: conventional
  filesystem_restricted: true
```

### Quick Setup Questions (Minimum)

Only ask for:
1. Project name
2. Project description
3. Application specification

Infer everything else from:
- Existing files in directory (package.json, requirements.txt, etc.)
- README.md content
- Git configuration
- Directory structure

### Detection Logic

```python
def detect_stack(project_path):
    """Detect tech stack from existing files."""
    stack = {}

    # Check for Node.js/TypeScript
    if exists("package.json"):
        pkg = read_json("package.json")
        stack["language"] = "typescript" if exists("tsconfig.json") else "javascript"

        # Detect framework
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "next" in deps:
            stack["framework"] = "next.js"
        elif "react" in deps:
            stack["framework"] = "react"
        elif "vue" in deps:
            stack["framework"] = "vue"

        # Detect test framework
        if "vitest" in deps:
            stack["test_framework"] = "vitest"
        elif "jest" in deps:
            stack["test_framework"] = "jest"

    # Check for Python
    elif exists("pyproject.toml") or exists("requirements.txt"):
        stack["language"] = "python"

        if exists("pyproject.toml"):
            pyproject = read_toml("pyproject.toml")
            deps = pyproject.get("project", {}).get("dependencies", [])
            if "fastapi" in str(deps):
                stack["framework"] = "fastapi"
            elif "flask" in str(deps):
                stack["framework"] = "flask"

        stack["test_framework"] = "pytest"

    # Check for other languages...

    return stack
```

---

## Resume Mode

For resume mode, follow this protocol:

### Step 1: Detect Harness Project

```bash
# Check for harness configuration
cat .harness/config.json
```

If found, extract `archon_project_id`.

### Step 2: Query Archon for Current State

```python
# Get project details
project = find_projects(project_id=archon_project_id)

# Get all tasks
tasks = find_tasks(filter_by="project", filter_value=archon_project_id)

# Get session notes
notes = find_documents(
    project_id=archon_project_id,
    query="Session Notes"
)

# Compute statistics
total_tasks = len([t for t in tasks if t["feature"] != "Meta"])
done_tasks = len([t for t in tasks if t["status"] == "done"])
doing_tasks = len([t for t in tasks if t["status"] == "doing"])
todo_tasks = len([t for t in tasks if t["status"] == "todo"])
```

### Step 3: Display Resume Summary

```markdown
## Harness Project Resume

### Project: [PROJECT_NAME]
**Archon ID**: [PROJECT_ID]
**Path**: [PROJECT_PATH]

### Progress
| Status | Count | Percentage |
|--------|-------|------------|
| Done | [DONE] | [DONE_PCT]% |
| In Progress | [DOING] | - |
| Todo | [TODO] | - |
| **Total** | **[TOTAL]** | - |

### Current State
**Last Session**: [LAST_SESSION_DATE]
**Last Agent**: [LAST_AGENT]
**Last Task Completed**: [LAST_TASK_TITLE]

### Current Task (In Progress)
[CURRENT_TASK_DETAILS_IF_ANY]

### Next Task (Highest Priority TODO)
[NEXT_TASK_DETAILS]

### Blockers
[ANY_BLOCKERS_FROM_SESSION_NOTES]

---

## Resume Options

1. **Continue Development**
   Use `@harness-coder` to continue with the next task

2. **View All Tasks**
   Query: `find_tasks(filter_by="project", filter_value="[PROJECT_ID]")`

3. **Check Session Notes**
   Query: `find_documents(project_id="[PROJECT_ID]", query="Session Notes")`

4. **Run Status Report**
   Detailed breakdown of all features and their status
```

---

## Error Handling

### If Archon is Unavailable

```markdown
## Warning: Archon MCP Server Not Accessible

The harness requires Archon for state management. Please ensure:

1. Archon MCP server is running
2. MCP configuration includes Archon
3. ARCHON_URL environment variable is set

### Check MCP Status
Run `/mcp` to see connected servers.

### Setup Instructions
See: https://github.com/archon-ai/archon-mcp

### Options
- [ ] Retry connection
- [ ] View Archon setup instructions
- [ ] Exit wizard
```

### If Project Already Exists

```markdown
## Warning: Harness Configuration Already Exists

Found existing `.harness/config.json` in this directory.

### Existing Project Details
- **Name**: [EXISTING_PROJECT_NAME]
- **Archon ID**: [EXISTING_PROJECT_ID]
- **Created**: [CREATED_DATE]

### Options

1. **Resume Existing Project** (Recommended)
   Use `@harness-coder` to continue development

2. **Create in Subdirectory**
   Create new harness in `./[NEW_PROJECT_NAME]/`

3. **Overwrite Configuration** (Destructive)
   Delete existing harness config and start fresh
   WARNING: This does NOT delete Archon project data

4. **Cancel Setup**
   Exit wizard without changes
```

### If GitHub Creation Fails

```markdown
## Warning: GitHub Repository Creation Failed

Error: [ERROR_MESSAGE]

### Possible Causes
- Not authenticated: Run `gh auth login`
- Organization access denied
- Repository name already exists
- Rate limit exceeded

### Options

1. **Retry with Different Name**
   Try a different repository name

2. **Use Existing Repository**
   Provide URL to existing repository

3. **Continue Without GitHub**
   Proceed with local-only setup
   (Can add GitHub later)
```

---

## Best Practices

### For Effective Harness Projects

1. **Detailed Specifications**
   The more detail in the app spec, the better the generated tasks.
   Aim for 500-2000 words covering all features.

2. **Start Small**
   Begin with 20-30 features. Add more later if needed.
   Overly large task lists can be overwhelming.

3. **Incremental Development**
   The harness works best with one feature per session.
   Resist the urge to do multiple features at once.

4. **Testing is Critical**
   E2E testing catches bugs that unit tests miss.
   Don't skip the tester agent.

5. **Clean Handoffs**
   Always end sessions cleanly with proper Archon updates.
   The next session depends on accurate state.

6. **Trust the Pipeline**
   Let the testing and review skills do their jobs.
   Don't bypass them to move faster.

7. **Review Decisions**
   Document architectural decisions in session notes.
   Future sessions need this context.

### Common Pitfalls to Avoid

| Pitfall | Why It's Bad | What to Do |
|---------|--------------|------------|
| Skipping initialization | Coder has no tasks | Always run initializer first |
| Vague specifications | Tasks are unclear | Write detailed specs |
| Too many features | Overwhelming, never finish | Start with 20-30 |
| Bypassing tests | Bugs accumulate | Let tester run |
| Ignoring reviews | Technical debt grows | Address findings |
| Not updating Archon | State becomes stale | Always update handoffs |
| Manual commits | Inconsistent history | Use auto-commit |

---

## Integration with Project Wizard

When activated from the project wizard (`@project-wizard`), this skill:

1. Receives pre-gathered basic project information
2. Skips Phase 1 questions (already answered)
3. Continues from Phase 2 (Technical Stack)
4. Adds harness-specific configuration to existing project

### Handoff Protocol from Project Wizard

```python
# Project wizard passes context like:
project_context = {
    "name": "...",
    "description": "...",
    "type": "...",
    "path": "...",
    "github_repo": "...",
    "language": "...",  # May be pre-selected
    "framework": "...", # May be pre-selected
}

# Harness wizard uses this and asks for remaining info
```

---

## Session State Management

### Current Session State File

`.harness/state/current-session.json`:

```json
{
  "session_number": 5,
  "started_at": "2025-01-15T09:30:00Z",
  "agent": "harness-coder",
  "task_id": "task-uuid-here",
  "task_title": "Implement user authentication",
  "iteration_count": 23,
  "status": "in_progress",
  "checkpoints": [
    {
      "time": "09:35:00",
      "action": "Started implementation"
    },
    {
      "time": "10:15:00",
      "action": "Core auth logic complete"
    }
  ]
}
```

### Session History Archive

`.harness/state/history/session-{N}.json`:

Archive completed sessions for reference. Useful for debugging or understanding project evolution.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Complete rewrite with full wizard phases |
| 1.0.0 | 2024-12 | Initial harness wizard implementation |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `@project-wizard` | Parent wizard that may delegate here |
| `@harness-initializer` | First session task generation |
| `@harness-coder` | Main development loop |
| `@harness-tester` | Test execution and reporting |
| `@harness-reviewer` | Code review before completion |
| `@autonomous-agent-harness` | Reference architecture documentation |

---

## Quick Reference Card

```
HARNESS WIZARD QUICK REFERENCE

SETUP MODES
-----------
Full Setup     Complete questionnaire (new projects)
Quick Setup    Smart defaults (existing codebases)
Resume Mode    Continue existing project

KEY CONFIGURATION
-----------------
Max Features:      20-50 recommended
Iteration Limit:   50 default (0=unlimited)
Model:             claude-sonnet-4 (default)
Testing:           unit+integration (default)
Coverage:          80% target

ARCHON RESOURCES CREATED
------------------------
- Project record
- Harness Configuration document
- Application Specification document
- Session Notes document
- META tracking task
- Initialization task

LOCAL FILES CREATED
-------------------
.harness/config.json       Main configuration
.harness/prompts/*.md      Agent prompt templates
.harness/state/            Session state tracking
init.sh / init.ps1         Environment setup

NEXT STEPS AFTER SETUP
----------------------
1. Run init script
2. Use @harness-initializer
3. Then use @harness-coder for each session
```
