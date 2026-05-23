---
name: project-init
description: |
  Scaffold new projects with standard structure. Use when: (1) user says
  "create project", "scaffold", "initialize", (2) starting from scratch,
  (3) need consistent project layout. Creates CLAUDE.md, README.md, PLAN.md,
  RESEARCH.md, AGENTS.md, .gitignore, and .claude/skills/ directory.
category: development
user-invocable: true
---

# Project Initialization

Scaffolds new projects with a standard structure for Claude Code workflows.

## Trigger Conditions

Invoke when user says:
- "create a new project"
- "scaffold a project"
- "initialize project"
- "start new project"
- "set up project structure"

## Procedure

### Step 1: Determine Location

Check if currently inside a git workspace:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

**If inside git workspace:**
- Navigate to parent directory
- Create new directory there
- This prevents nested git repos

**If not inside git workspace:**
- Create in current directory

### Step 2: Create Directory Structure

```bash
mkdir -p {{project_name}}
cd {{project_name}}
mkdir -p .claude/skills
mkdir -p src tests docs
```

### Step 3: Initialize Git

```bash
git init
```

### Step 4: Create Standard Files

Create these files from templates:

| File | Purpose |
|------|---------|
| CLAUDE.md | Project guidance for Claude |
| README.md | User-facing documentation |
| PLAN.md | Remaining work tracker |
| RESEARCH.md | Investigation notes |
| AGENTS.md | Agent coordination |
| .gitignore | Comprehensive patterns |

### Step 5: Create .gitignore

```gitignore
# Dependencies
node_modules/
.pnpm-store/

# Build outputs
dist/
build/
.svelte-kit/
.next/
.nuxt/

# Test artifacts
coverage/
test-results/
playwright-report/
.nyc_output/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Cache
.cache/
.turbo/
.eslintcache
.parcel-cache/

# Credentials
*.pem
*.key
credentials.json
```

### Step 6: Populate Templates

Fill templates with project-specific values:

**CLAUDE.md:**
- Project name
- Detected language (TypeScript, Python, etc.)
- Project structure
- Recommended skills based on tech stack

**README.md:**
- Project name and description
- Quick start commands
- Basic usage example

**PLAN.md:**
- Initial tasks based on user's goals
- Empty backlog section
- Empty completed section

**RESEARCH.md:**
- Topic placeholder
- Empty findings section

**AGENTS.md:**
- Empty, ready for agent coordination

### Step 7: Initial Commit

```bash
git add .
git commit -m "Initial project scaffold

Created standard structure with:
- CLAUDE.md (project guidance)
- README.md (documentation)
- PLAN.md (work tracker)
- RESEARCH.md (investigation notes)
- AGENTS.md (agent coordination)
- .gitignore (comprehensive patterns)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Output Format

After scaffolding, report:

```
Project scaffolded: {{project_name}}

Created files:
  - CLAUDE.md
  - README.md
  - PLAN.md
  - RESEARCH.md
  - AGENTS.md
  - .gitignore
  - .claude/skills/ (directory)

Next steps:
1. Review CLAUDE.md and customize for your project
2. Update README.md with project description
3. Add initial tasks to PLAN.md
4. Install skills with: skills scan --all
```

## Customization Options

User can specify:
- `--language`: Primary language (typescript, python, rust, go)
- `--framework`: Framework (react, svelte, next, sveltekit)
- `--no-git`: Skip git initialization
- `--skills`: Comma-separated list of skills to install

## Example Usage

**Basic:**
```
/project-init my-app
```

**With options:**
```
/project-init my-app --language typescript --framework sveltekit
```

## Skill Chaining

After scaffolding:
1. **dogfood-skills** runs `skills scan` to recommend skills
2. **doc-maintenance** is ready to update PLAN.md
3. **tdd** is available for test-driven development

## Notes

- Does not overwrite existing files
- Creates parent directories as needed
- Uses Handlebars-style templates ({{variable}})
- Respects user's existing git configuration
