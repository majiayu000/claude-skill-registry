---
name: project-wizard
version: 1.0.0
description: Interactive setup wizard for creating new projects with proper structure, security configurations, GitHub repository, and Archon project tracking. Guides users through project creation from template with pre-commit hooks, branch protection, and customized documentation. Use when starting a new project, setting up a repository, or initializing a new codebase.
---

# Project Wizard: New Project Setup

Guide users through creating properly configured new projects with security, repository integration, and task tracking. This skill ensures every project starts with consistent structure and best practices.

## Triggers

Use this skill when:
- Creating a new project
- Setting up a new repository
- Initializing a new codebase
- Starting a new workspace
- Cloning a template for new work
- Keywords: new project, create project, setup project, initialize, project wizard, scaffold, template

## What Gets Created

- Proper folder structure
- Security configurations (pre-commit hooks, secret detection)
- GitHub repository with branch protection
- Archon project for task management
- Customized documentation

---

## Interactive Setup Flow

```
PROJECT WIZARD FLOW

  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
  │ Basics  │──>│  Tech   │──>│ GitHub  │──>│ Archon  │
  │ Info    │   │ Stack   │   │ Setup   │   │ Project │
  └─────────┘   └─────────┘   └─────────┘   └─────────┘
                                                │
                                         ┌──────┴──────┐
                                         │  Generate   │
                                         │  Summary    │
                                         └─────────────┘
```

---

## Phase 1: Gather Project Information

### Basic Information

```markdown
## Project Basics

1. **Project Location**
   Where to create the project folder?
   > Enter parent directory path (e.g., E:\Repos\MyOrg)

2. **Project Name**
   What should the project be called?
   > Must be lowercase with hyphens (e.g., my-awesome-project)

3. **Project Type**
   What kind of project is this?
   - [ ] Web Frontend (React, Vue, Angular, etc.)
   - [ ] Backend API (Node.js, Python, .NET, etc.)
   - [ ] Full-Stack Application
   - [ ] CLI Tool / Library
   - [ ] Infrastructure / DevOps
   - [ ] Other

4. **Project Description**
   Brief description (under 200 characters)
   > Used for README and GitHub repo description
```

### Technical Stack

```markdown
## Technical Stack

5. **Primary Language**
   - TypeScript/JavaScript
   - Python
   - C# / .NET
   - Go
   - Rust
   - Java/Kotlin
   - Other

6. **Framework** (if applicable)
   Frontend: React, Vue, Svelte, Next.js, etc.
   Backend: Express, FastAPI, ASP.NET, Gin, etc.

7. **Package Manager**
   npm, yarn, pnpm, pip/poetry, dotnet, go mod, cargo
```

### GitHub Configuration

```markdown
## GitHub Configuration

8. **GitHub Organization**
   Where to create the repository?
   > List available with: gh org list
   > Or use personal account

9. **Repository Visibility**
   - [ ] Private (recommended)
   - [ ] Public
```

---

## Phase 2: Create Project Structure

### Directory Structure

```
<project_name>/
├── .github/
│   ├── workflows/           # CI/CD workflows
│   ├── CODEOWNERS          # Code ownership
│   └── dependabot.yml      # Dependency updates
├── .claude/
│   ├── commands/           # Custom slash commands
│   ├── context/            # Path-specific context
│   └── skills/             # Project-specific skills
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── README.md               # Project documentation
└── CLAUDE.md               # Claude Code configuration
```

### Language-Specific Additions

**TypeScript/JavaScript:**
```
├── package.json
├── tsconfig.json
├── .eslintrc.js
└── .prettierrc
```

**Python:**
```
├── pyproject.toml
├── requirements.txt
├── .python-version
└── ruff.toml
```

**C# / .NET:**
```
├── *.sln
├── src/*.csproj
├── .editorconfig
└── Directory.Build.props
```

---

## Phase 3: Initialize Git Repository

### Commands Executed

```bash
# Initialize git
git init

# Install pre-commit hooks
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg

# Create initial commit
git add .
git commit -m "feat: initial project setup"
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
      - id: check-merge-conflict

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

---

## Phase 4: Create GitHub Repository

### Repository Creation

```bash
# Create remote repository
gh repo create "<org>/<project_name>" \
  --private \
  --source=. \
  --push \
  --description "<description>"
```

### Branch Protection

```bash
# Configure branch protection for main
gh api repos/<org>/<project_name>/branches/main/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=false \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null
```

### Security Features

```bash
# Enable secret scanning
gh api repos/<org>/<project_name> \
  -X PATCH \
  -f security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'
```

---

## Phase 5: Create Archon Project

### Project Creation

```python
# Create the project in Archon
result = manage_project("create",
    title="<Project Name>",
    description="<Project Description>",
    github_repo="https://github.com/<org>/<project_name>"
)

project_id = result["project"]["id"]
```

### Initial Tasks

```python
# Setup completion task
manage_task("create",
    project_id=project_id,
    title="Complete project setup",
    description="Review and customize copied template files:\n- Update README.md\n- Configure CI/CD workflows\n- Set up development environment",
    status="todo",
    feature="Setup",
    task_order=100
)

# Architecture documentation task
manage_task("create",
    project_id=project_id,
    title="Define project architecture",
    description="Create architecture documentation:\n- System overview\n- Component diagram\n- Data flow\n- Technology decisions",
    status="todo",
    feature="Documentation",
    task_order=90
)
```

---

## Phase 6: Generate Summary

### Success Output

```markdown
# Project Created Successfully!

## Project Details
| Item | Value |
|------|-------|
| **Name** | <project_name> |
| **Location** | <full_path> |
| **Type** | <project_type> |
| **Repository** | https://github.com/<org>/<project_name> |
| **Archon Project** | <project_id> |

## What's Included
- Pre-configured .gitignore
- Pre-commit hooks with secret detection
- GitHub Actions workflows
- Claude Code configuration
- Branch protection enabled
- Secret scanning enabled

## Next Steps
1. Open the project: `code <project_path>`
2. Review and customize README.md
3. Check Archon tasks: `find_tasks(project_id="<project_id>")`
4. Start building!

## Quick Commands
| Command | Description |
|---------|-------------|
| `npm install` / `pip install -e .` | Install dependencies |
| `npm test` / `pytest` | Run tests |
| `pre-commit run --all-files` | Run all hooks |
| `gh pr create` | Create pull request |
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Path doesn't exist | Create directory or choose different path |
| Project folder exists | Overwrite or choose different name |
| gh CLI not installed | Install from https://cli.github.com |
| gh CLI not authenticated | Run `gh auth login` |
| Pre-commit install fails | `pip install pre-commit` manually |
| Archon MCP not available | Skip Archon, note in summary |

---

## Quick Mode

For experienced users, use quick setup:

```bash
# All settings in one command
/project-wizard --quick \
  --path "E:\Repos\MyOrg" \
  --name "my-api" \
  --type "backend" \
  --lang "python" \
  --org "MyOrg" \
  --private

# Or accept all smart defaults
/project-wizard --auto --name "my-project"
```

Auto mode will:
- Use current directory as parent
- Detect language from existing files or prompt
- Use first available GitHub org
- Default to private repository
- Create Archon project automatically

---

## Template Customization

### README Template by Project Type

**Web Frontend:**
```markdown
# Project Name

## Getting Started

npm install
npm run dev

## Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run tests
```

**Backend API:**
```markdown
# Project Name

## Getting Started

pip install -e ".[dev]"
uvicorn src.main:app --reload

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
```

### CLAUDE.md Template

```markdown
# CLAUDE.md - Project Configuration

## Project Overview
[Description]

## Tech Stack
- Language: [Language]
- Framework: [Framework]
- Database: [Database]

## Development Commands
- Build: [command]
- Test: [command]
- Lint: [command]

## Archon Project
- Project ID: [id]
- GitHub: [url]
```

---

## Notes

- Always verify paths exist before creating
- Pre-commit hooks are essential for security
- Archon integration enables task tracking across sessions
- Branch protection prevents accidental main branch pushes
- Secret scanning catches leaked credentials before they're exposed
