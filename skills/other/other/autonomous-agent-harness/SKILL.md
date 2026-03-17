---
name: autonomous-agent-harness
version: 2.0.0
description: Set up autonomous coding agent projects with long-running harnesses using Archon MCP for state management. Creates complete project scaffolds with initializer/coding agent prompts, feature tracking, session handoffs, security configuration, and browser testing integration. Based on Anthropic's effective harnesses guide. Use when building autonomous coding agents, long-running AI workflows, or multi-session development projects.
---

# Autonomous Coding Agent Harness Setup

Create fully-configured autonomous coding agent projects that can work across multiple sessions with proper state management, handoffs, and testing. Uses **Archon MCP** for project/task tracking, enabling persistent state management and context preservation.

## 🚀 Quick Start

Use these prompts to interact with the harness system:

| Command | Description |
|---------|-------------|
| `/harness-setup` | Launch full setup wizard |
| `/harness-quick` | Quick setup with smart defaults |
| `/harness-init` | Initialize project (first session) |
| `/harness-next` | Start next coding session |
| `/harness-status` | Check project status |
| `/harness-resume` | Resume existing project |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT PIPELINE                              │
│                                                                      │
│   /harness-setup → @harness-wizard                                  │
│         │                                                            │
│         ▼                                                            │
│   /harness-init → @harness-initializer                              │
│         │                                                            │
│         ▼                                                            │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  /harness-next → @harness-coder                             │   │
│   │         │                                                    │   │
│   │         ├──► @harness-tester (parallel)                     │   │
│   │         │                                                    │   │
│   │         ├──► @harness-reviewer (before completion)          │   │
│   │         │                                                    │   │
│   │         ▼                                                    │   │
│   │   [Repeat for each feature]                                  │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│   State Management: Archon MCP (Projects, Tasks, Documents)         │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Pipeline

| Agent | Role | When Used |
|-------|------|-----------|
| `@harness-wizard` | Interactive setup | Initial configuration |
| `@harness-initializer` | Generate tasks from spec | First session only |
| `@harness-coder` | Implement features | Every coding session |
| `@harness-tester` | Run tests & verify | After implementation (parallel) |
| `@harness-reviewer` | Code review | Before marking complete |

## Features

- **Multi-Agent System**: Four specialized agents working together
- **Archon State Management**: Projects, tasks, and documents via MCP
- **Clean Handoffs**: Session notes and context for seamless continuation
- **Parallel Testing**: Testing agent can run in background
- **Code Review**: Optional review before feature completion
- **Multiple Execution Modes**: Terminal, background, or SDK

---

---

## Project Setup Questionnaire

When the user requests to set up an autonomous coding agent project, gather the following information systematically:

### Phase 1: Project Basics

```
I'll help you set up an autonomous coding agent project. Let's gather the required information:

## PROJECT BASICS

**1. Project Name:**
   What should the project be called? (e.g., "saas-dashboard", "e-commerce-api")
   →

**2. Project Description:**
   Brief description of what you're building (1-3 sentences)
   →

**3. Project Type:**
   - [ ] Web Application (Frontend + Backend)
   - [ ] API/Backend Only
   - [ ] CLI Application
   - [ ] Full-Stack with Database
   - [ ] Mobile App Backend
   - [ ] Other: _____________

**4. GitHub Repository:**
   Will this use a GitHub repo? If yes, provide URL (or "create new")
   →
```

### Phase 2: Technical Stack

```
## TECHNICAL STACK

**5. Primary Language:**
   - [ ] TypeScript/JavaScript
   - [ ] Python
   - [ ] Go
   - [ ] Rust
   - [ ] Java
   - [ ] Other: _____________

**6. Framework (if applicable):**
   - Frontend: (React, Vue, Svelte, Next.js, etc.)
   - Backend: (Express, FastAPI, Gin, Actix, Spring, etc.)
   →

**7. Database:**
   - [ ] PostgreSQL
   - [ ] MySQL/MariaDB
   - [ ] MongoDB
   - [ ] SQLite
   - [ ] Supabase
   - [ ] Firebase
   - [ ] None/TBD
   - [ ] Other: _____________

**8. Package Manager:**
   - [ ] npm
   - [ ] yarn
   - [ ] pnpm
   - [ ] pip/poetry
   - [ ] go mod
   - [ ] cargo
```

### Phase 3: Agent Configuration

```
## AGENT CONFIGURATION

**9. Max Features/Tasks:**
   How many features should the initializer create? (recommended: 20-50)
   → Default: 30

**10. Session Iteration Limit:**
   Max iterations per coding session? (0 = unlimited)
   → Default: 50

**11. Claude Model:**
   - [ ] claude-opus-4-5-20251101 (Recommended for complex projects)
   - [ ] claude-sonnet-4-20250514 (Faster, good balance)
   - [ ] claude-haiku-3-5-20241022 (Quick iterations)

**12. MCP Servers to Enable:**
   - [ ] Archon (Required - state management)
   - [ ] Playwright (Browser automation testing)
   - [ ] GitHub (Repository operations)
   - [ ] Brave Search (Web research)
   - [ ] Custom: _____________
```

### Phase 4: Testing & Security

```
## TESTING & SECURITY

**13. Testing Strategy:**
   - [ ] Unit tests only
   - [ ] Unit + Integration tests
   - [ ] Full E2E with browser automation
   - [ ] No automated tests (manual verification)

**14. Browser Testing Tool:**
   - [ ] Playwright MCP (Recommended)
   - [ ] Puppeteer MCP
   - [ ] None

**15. Allowed Bash Commands:**
   Select commands the coding agent can execute:
   - [ ] Package managers (npm, pip, etc.)
   - [ ] Git operations
   - [ ] Build tools
   - [ ] Test runners
   - [ ] Database commands
   - [ ] Docker commands
   - [ ] Custom: _____________

**16. Filesystem Restrictions:**
   Should the agent be restricted to project directory only?
   - [ ] Yes (Recommended)
   - [ ] No (Allow broader access)
```

### Phase 5: Archon Integration

```
## ARCHON INTEGRATION

**17. Archon MCP Server:**
   Is Archon MCP server configured and accessible?
   - [ ] Yes, already configured
   - [ ] No, need setup instructions

**18. Existing Archon Project:**
   - [ ] Create new Archon project
   - [ ] Use existing project ID: _____________

**19. Task Assignment:**
   Who should tasks be assigned to by default?
   - [ ] "Coding Agent"
   - [ ] "User"
   - [ ] Custom: _____________
```

### Phase 6: Application Specification

```
## APPLICATION SPECIFICATION

**20. App Specification:**
   Provide a detailed description of the application to build. Include:
   - Core features and functionality
   - User flows and interactions
   - Data models and relationships
   - Authentication requirements
   - Third-party integrations
   - UI/UX requirements

   (This will be saved as app_spec.txt and used to generate feature tasks)

   →
```

---

## Project Generation Workflow

After collecting all questionnaire responses, execute this workflow:

### Step 1: Create Archon Project

```python
# Create project in Archon
manage_project("create",
    title="<PROJECT_NAME>",
    description="<PROJECT_DESCRIPTION>",
    github_repo="<GITHUB_URL>"
)
# Save returned project_id for all subsequent operations
```

### Step 2: Generate Directory Structure

Create the following project scaffold:

```
<project_name>/
├── .archon_project.json        # Project marker with Archon project_id
├── .claude_settings.json       # Security settings and allowed commands
├── app_spec.txt                # Application specification
├── init.sh                     # Environment setup script
├── claude-progress.txt         # Session progress tracking
├── features.json               # Feature registry (pass/fail tracking)
├── prompts/
│   ├── initializer_prompt.md   # First session prompt
│   └── coding_prompt.md        # Continuation session prompt
├── src/                        # Application source code
├── tests/                      # Test files
└── docs/                       # Documentation
```

### Step 3: Generate Configuration Files

**`.archon_project.json`**:
```json
{
  "project_id": "<ARCHON_PROJECT_ID>",
  "project_name": "<PROJECT_NAME>",
  "created_at": "<TIMESTAMP>",
  "status": "initializing"
}
```

**`.claude_settings.json`**:
```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(node:*)",
      "Bash(git:*)",
      "Bash(python:*)",
      "Bash(pip:*)",
      "Bash(pytest:*)",
      "Read", "Write", "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(curl:*)",
      "Bash(wget:*)"
    ]
  },
  "mcp_servers": ["archon", "playwright-mcp"],
  "model": "<SELECTED_MODEL>",
  "max_iterations": <ITERATION_LIMIT>
}
```

**`features.json`**:
```json
{
  "total_features": 0,
  "completed": 0,
  "features": []
}
```

### Step 4: Generate Agent Prompts

**`prompts/initializer_prompt.md`** (First Session):
```markdown
# Initializer Agent Prompt

You are initializing a new autonomous coding project: {PROJECT_NAME}

## Your Tasks:
1. Read the app_spec.txt file thoroughly
2. Connect to Archon MCP and verify project: {PROJECT_ID}
3. Create {MAX_FEATURES} detailed task issues in Archon with:
   - Clear, testable acceptance criteria
   - Specific test steps
   - Priority ordering (task_order field)
   - Feature grouping
4. Create META task for session tracking/handoffs
5. Initialize the project structure (src/, tests/, docs/)
6. Run init.sh to set up the environment
7. Update claude-progress.txt with session summary
8. Commit all changes with descriptive message

## Archon Integration:
- Project ID: {PROJECT_ID}
- Use manage_task("create", ...) for each feature
- Use manage_task("update", task_id, status="doing") when starting work
- Add detailed notes to task descriptions for handoffs

## Feature Task Template:
Each task should include:
- Clear title describing the feature
- Description with:
  - What needs to be built
  - Acceptance criteria (testable)
  - Test steps for verification
  - Dependencies on other tasks
- Feature tag for grouping
- Priority via task_order (higher = more important)

## Session Handoff:
Before ending, update:
1. claude-progress.txt with what was completed
2. features.json with created features
3. META task in Archon with session summary
4. Git commit with all changes
```

**`prompts/coding_prompt.md`** (Continuation Sessions):
```markdown
# Coding Agent Prompt

You are continuing work on: {PROJECT_NAME}

## Session Startup Protocol:
1. Verify working directory is correct
2. Read claude-progress.txt for previous session context
3. Review git log for recent changes
4. Query Archon for current task status:
   ```
   find_tasks(filter_by="project", filter_value="{PROJECT_ID}")
   ```
5. Run health check on previously completed features
6. Select highest-priority TODO task

## Work Loop:
For each task:
1. Mark task as "doing" in Archon:
   ```
   manage_task("update", task_id="...", status="doing")
   ```
2. Implement the feature following acceptance criteria
3. Write/run tests for the feature
4. Use Playwright MCP for browser testing if UI involved
5. Update task with implementation notes
6. Mark task as "review":
   ```
   manage_task("update", task_id="...", status="review")
   ```
7. Commit changes with descriptive message
8. Update features.json with pass/fail status

## Testing Requirements:
- Run existing tests before starting new work
- If any test fails, fix it before proceeding
- NEVER remove or modify tests to make them pass
- Use Playwright for E2E testing:
  ```
  mcp__playwright__browser_navigate(url="http://localhost:3000")
  mcp__playwright__browser_snapshot()
  ```

## Session Handoff:
Before ending:
1. Update claude-progress.txt with:
   - Tasks completed this session
   - Current task status
   - Any blockers or issues
   - Next steps
2. Update META task in Archon
3. Commit all changes
4. Leave codebase in clean, working state

## CRITICAL RULES:
- Never declare project complete without full E2E verification
- Never skip tests or mark features done without testing
- Always update Archon task status accurately
- Always commit incrementally with meaningful messages
```

### Step 5: Create Init Script

**`init.sh`**:
```bash
#!/bin/bash
set -e

echo "Initializing {PROJECT_NAME}..."

# Create directories
mkdir -p src tests docs

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
    echo "node_modules/" >> .gitignore
    echo ".env" >> .gitignore
    echo "__pycache__/" >> .gitignore
fi

# Project-specific initialization
{INIT_COMMANDS}

echo "Environment setup complete!"
echo "Run 'npm start' or appropriate command to start development"
```

### Step 6: Create Archon Tasks

Use Archon MCP to create the initial task structure:

```python
# Create META task for session tracking
manage_task("create",
    project_id="<PROJECT_ID>",
    title="META: Session Tracking & Handoffs",
    description="Track session summaries, blockers, and handoff notes. Update after each session.",
    task_order=100,
    feature="Meta",
    assignee="Coding Agent"
)

# Create initial setup task
manage_task("create",
    project_id="<PROJECT_ID>",
    title="Initial project setup and environment configuration",
    description="Set up development environment, install dependencies, configure build tools",
    task_order=99,
    feature="Setup",
    assignee="Coding Agent"
)
```

---

## Handoff Workflow

### Between Sessions

The coding agent should follow this handoff protocol:

1. **Update Progress File**:
   ```
   ## Session: <DATE>

   ### Completed:
   - Task #1: Feature description (DONE)
   - Task #2: Feature description (IN PROGRESS)

   ### Blockers:
   - None / List any blockers

   ### Next Steps:
   - Continue Task #2
   - Start Task #3

   ### Notes for Next Session:
   - Important context or decisions made
   ```

2. **Update Archon META Task**:
   ```python
   manage_task("update",
       task_id="<META_TASK_ID>",
       description="Updated session summary:\n\n<PROGRESS_SUMMARY>"
   )
   ```

3. **Git Commit**:
   ```bash
   git add .
   git commit -m "Session end: <SUMMARY>

   Completed: <TASK_LIST>
   Next: <NEXT_TASK>"
   ```

---

## Feature Registry Management

The `features.json` file tracks all features and their status:

```json
{
  "total_features": 30,
  "completed": 12,
  "passing": 11,
  "failing": 1,
  "features": [
    {
      "id": 1,
      "archon_task_id": "uuid-here",
      "name": "User Authentication",
      "status": "passing",
      "implemented_at": "2024-01-15",
      "tested": true,
      "test_results": {
        "unit": "pass",
        "e2e": "pass"
      }
    },
    {
      "id": 2,
      "archon_task_id": "uuid-here",
      "name": "Dashboard Layout",
      "status": "failing",
      "implemented_at": "2024-01-16",
      "tested": true,
      "test_results": {
        "unit": "pass",
        "e2e": "fail",
        "failure_reason": "Chart component not rendering"
      }
    }
  ]
}
```

---

## Running the Agent Harness

### Using Claude Agent SDK (Python)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_initializer():
    """Run the initializer agent for first session"""
    with open("prompts/initializer_prompt.md") as f:
        prompt = f.read()

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            mcp_servers=["archon", "github"],
            model="claude-opus-4-5-20251101"
        )
    ):
        print(message)

async def run_coding_agent():
    """Run the coding agent for subsequent sessions"""
    with open("prompts/coding_prompt.md") as f:
        prompt = f.read()

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            mcp_servers=["archon", "playwright-mcp"],
            model="claude-opus-4-5-20251101",
            max_iterations=50
        )
    ):
        print(message)

# Run initializer first time
asyncio.run(run_initializer())

# Run coding agent for subsequent sessions
asyncio.run(run_coding_agent())
```

### Using Claude Code CLI

```bash
# First session - Initializer
claude --prompt "$(cat prompts/initializer_prompt.md)" \
       --model claude-opus-4-5-20251101 \
       --mcp archon,github

# Subsequent sessions - Coding Agent
claude --prompt "$(cat prompts/coding_prompt.md)" \
       --model claude-opus-4-5-20251101 \
       --mcp archon,playwright-mcp \
       --max-iterations 50
```

---

## Archon MCP Quick Reference

### Project Management
```python
# Create project
manage_project("create", title="My App", description="...", github_repo="...")

# Get project
find_projects(project_id="uuid")

# List all projects
find_projects()
```

### Task Management
```python
# Create task
manage_task("create",
    project_id="...",
    title="Feature name",
    description="Details...",
    status="todo",
    assignee="Coding Agent",
    task_order=50,
    feature="Auth"
)

# Update task status
manage_task("update", task_id="...", status="doing")
manage_task("update", task_id="...", status="review")
manage_task("update", task_id="...", status="done")

# Get tasks
find_tasks(filter_by="project", filter_value="<project_id>")
find_tasks(filter_by="status", filter_value="todo")
find_tasks(task_id="<specific_task_id>")
```

### Task Status Flow
```
todo → doing → review → done
```

---

## Best Practices

1. **Incremental Progress**: Work on single features per session
2. **Test Everything**: Verify E2E functionality, not just code changes
3. **Clean Handoffs**: Leave environment ready for next session
4. **Explicit State**: Never assume - always check Archon for current state
5. **Atomic Commits**: Commit after each feature completion
6. **No Test Shortcuts**: Never modify tests to pass artificially
7. **Document Decisions**: Add context to Archon tasks and progress file
8. **Verify Before Claiming**: Test features before marking complete

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Agent skips testing | Add explicit testing requirements in prompt |
| Lost context between sessions | Check claude-progress.txt and Archon META task |
| Feature marked done but broken | Run E2E tests, update features.json status |
| Archon connection failed | Verify MCP server configuration |
| Agent declares premature completion | Require explicit feature count verification |

### Recovery Commands

```bash
# Check project status
find_tasks(filter_by="project", filter_value="<PROJECT_ID>")

# View recent progress
cat claude-progress.txt
git log --oneline -10

# Verify features
cat features.json | jq '.features[] | select(.status=="failing")'

# Reset stuck task
manage_task("update", task_id="...", status="todo")
```

---

## Notes

- This skill requires **Archon MCP server** to be configured and running
- Playwright MCP is recommended for E2E testing but optional
- The agent harness works best with detailed, specific app specifications
- For complex projects, consider breaking into phases (MVP, v1, v2)
- Review and adjust generated prompts based on project-specific needs
