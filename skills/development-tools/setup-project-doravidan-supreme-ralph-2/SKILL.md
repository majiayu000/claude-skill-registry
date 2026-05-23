---
name: setup-project
description: Setup Claude Code Configuration with full RALPH autonomous development integration
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Setup Claude Code Configuration

Analyze the current project and create comprehensive Claude Code configuration including CLAUDE.md, rules, slash commands, agents, skills, hooks, and RALPH autonomous development setup.

## Overview

This skill performs intelligent project setup by:
1. **Deep Project Analysis** - Scans codebase for language, framework, patterns, conventions
2. **Claude Code Configuration** - Creates CLAUDE.md, rules, commands, agents, skills, hooks
3. **RALPH Integration** - Sets up autonomous development with intelligent PRD generation
4. **PROJECT_SPEC.md** - Generates comprehensive project documentation for RALPH context

## Execution Flow

### Phase 1: Project Analysis

First, thoroughly explore the codebase to understand:

```bash
# Check for manifest files to determine tech stack
ls -la package.json tsconfig.json pyproject.toml go.mod Cargo.toml *.csproj 2>/dev/null

# Check for existing Claude configuration
ls -la .claude/ CLAUDE.md 2>/dev/null

# Get project structure overview
find . -maxdepth 2 -type d ! -path './node_modules*' ! -path './.git*' 2>/dev/null | head -30
```

**Analyze:**
- **Language**: TypeScript, JavaScript, Python, Go, Rust, C#
- **Framework**: React, Next.js, Vue, Express, FastAPI, Django, NestJS, etc.
- **Package Manager**: npm, yarn, pnpm, bun, pip, cargo, go mod
- **Test Framework**: Vitest, Jest, Mocha, Pytest, Go test
- **Linting**: ESLint, Biome, Prettier, Ruff
- **Type System**: TypeScript strict mode, Python type hints
- **Build System**: Vite, Webpack, esbuild, Turbopack

### Phase 2: Create Directory Structure

```bash
mkdir -p .claude/rules .claude/commands .claude/agents .claude/skills .claude/hooks
mkdir -p scripts/ralph tasks
```

### Phase 3: Generate CLAUDE.md

Create a comprehensive CLAUDE.md based on analysis:

```markdown
# Project: [Name]

[One-line description from package.json/README]

## Architecture Overview

```
[Directory tree - 3 levels deep]
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | [Detected language] |
| Framework | [Detected framework] |
| Runtime | [Node.js version / Python version] |
| Package Manager | [npm/yarn/pnpm/pip/cargo] |
| Test Framework | [Vitest/Jest/Pytest] |
| Linting | [ESLint/Biome/Ruff] |

## Development Commands

| Command | Description |
|---------|-------------|
| `[dev command]` | Start development server |
| `[build command]` | Build for production |
| `[test command]` | Run tests |
| `[lint command]` | Run linter |
| `[typecheck command]` | Type checking |

## Key Patterns

[Document discovered patterns:]
- Module system (ES modules / CommonJS)
- Naming conventions (camelCase / kebab-case / PascalCase)
- Import order (Node builtins → External → Local)
- Testing patterns (test location, naming)
- Type usage (strict TypeScript, Python type hints)

## Code Style Quick Reference

[Language-specific conventions discovered]

## Important Files

| File | Purpose |
|------|---------|
| [entry point] | Application entry |
| [main config] | Configuration |
| [key modules] | Core functionality |

## Environment Variables

[List from .env.example or detected - NEVER values, only names]

## Files to Avoid Reading

```
node_modules/
dist/
build/
.next/
coverage/
__pycache__/
*.log
.env
.env.*
```

## Summary Instructions

When compacting context, prioritize:
1. Current task progress and remaining steps
2. Recent code changes and their purpose
3. Error messages and their solutions
4. API contracts and data models

Deprioritize:
1. Full file contents after initial read
2. Build output and compiler messages
3. Large dependency listings
```

### Phase 4: Create Style Rules (.claude/rules/)

Based on detected tech stack, create appropriate rule files:

#### For TypeScript/JavaScript:
**typescript-style.md** or **javascript-style.md**:
- Import/export conventions
- Async/await patterns
- Error handling approach
- File operation libraries (fs-extra vs native fs)
- Path handling (path.join vs string concatenation)

#### For Python:
**python-style.md**:
- Type hints requirements
- Async patterns (asyncio)
- Virtual environment expectations
- Import organization

#### For Go:
**go-style.md**:
- Error handling (explicit returns)
- Package organization
- Interface usage
- Concurrency patterns

#### Always create:
**security.md**:
- Sensitive file patterns to avoid
- Environment variable handling
- Input validation requirements
- Authentication patterns

**code-style.md**:
- Naming conventions
- Indentation (2 spaces / 4 spaces / tabs)
- Line length limits
- Comment expectations

### Phase 5: Create Slash Commands (.claude/commands/)

Create commands based on project needs:

**commit.md** - Git commit helper
**review.md** - Code review checklist
**test.md** - Run tests with coverage
**deploy.md** - Deployment automation (if applicable)
**ralph.md** - RALPH status and control
**ralph-run.md** - Run RALPH autonomous agent

### Phase 6: Create Custom Agents (.claude/agents/)

**code-reviewer.md** - Expert code review
**debugger.md** - Debugging specialist
**researcher.md** - Codebase exploration

### Phase 7: Create Skills (.claude/skills/)

**code-review/SKILL.md** - Code review skill
**prd/SKILL.md** - PRD generation skill
**ralph/SKILL.md** - PRD to JSON conversion
**ralph-run/SKILL.md** - RALPH execution

### Phase 8: Configure Hooks (.claude/hooks/)

**hooks.json**:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "[lint command]",
        "timeout": 30000
      }]
    }],
    "Stop": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/auto-compact.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

**auto-compact.sh** - Context usage monitoring (warns at 70%)

### Phase 9: Configure Settings (.claude/settings.json)

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(git:*)",
      "Bash([test runner]:*)",
      "Bash(mkdir:*)",
      "Bash(chmod:*)",
      "Bash(ls:*)",
      "Bash(rm:*)",
      "Bash(cp:*)",
      "Bash(mv:*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(./secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Read(**/credentials*)",
      "Read(node_modules/**)",
      "Read(coverage/**)"
    ]
  }
}
```

### Phase 10: RALPH Autonomous Development Setup

#### 10a: Generate PROJECT_SPEC.md

Create comprehensive project specification:

```markdown
# Project Specification: [Name]

> Generated: [Date]
> Analyzed by: claude-init

## Overview
[From README/package.json]

## Tech Stack
[Full technology breakdown]

## Directory Structure
[3-level tree]

## Dependencies
### Production
[Top 15 with purposes]

### Development
[Top 10 with purposes]

## Available Scripts
[All npm scripts / Makefile targets]

## Code Patterns & Conventions
### Testing
- Framework, location, coverage config

### Type System
- Language, strict mode

### Code Style
- Naming, module system, linting, formatting, import order

## Codebase Patterns for RALPH
[Discovered patterns as bullet list]

## Quality Gates
```bash
# Commands RALPH must run before marking stories complete
[typecheck command]
[lint command]
[test command]
```
```

#### 10b: Create scripts/ralph/

**ralph.sh** - Bash loop that runs Claude iterations:
```bash
#!/bin/bash
MAX_ITERATIONS="${1:-10}"
ITERATION=0
while [ $ITERATION -lt $MAX_ITERATIONS ]; do
  ITERATION=$((ITERATION + 1))
  echo "=== RALPH Iteration $ITERATION/$MAX_ITERATIONS ==="

  # Run Claude with RALPH prompt
  claude --dangerously-skip-permissions \
    -p "$(cat scripts/ralph/CLAUDE.md)" \
    --allowedTools 'Bash(git:*),Bash(npm:*),Read,Write,Edit,Grep,Glob'

  # Check for completion signal
  if grep -q "COMPLETE" progress.txt 2>/dev/null; then
    echo "✓ All stories complete!"
    break
  fi
done
```

**CLAUDE.md** - RALPH system prompt with:
- Mission: One story per iteration
- Context sources: prd.json, PROJECT_SPEC.md, progress.txt, git history
- Quality gates: typecheck, lint, test
- Commit format: `feat: [Story-ID] - [Story Title]`
- Exit signal: `<promise>COMPLETE</promise>`
- Project-specific context from analysis

#### 10c: Create Initial PRD (if feature provided)

If user provides `--feature "description"`:

1. Generate intelligent prd.json based on:
   - Feature description
   - Tech stack (React UI, Backend API, etc.)
   - Existing patterns (TypeScript, test framework, linting)

2. Create appropriately-sized user stories:
   - Priority 1: Data models/types
   - Priority 2: Core logic/services
   - Priority 3: API/routes
   - Priority 4: UI components
   - Priority 5: Polish/tests

3. Initialize progress.txt with discovered patterns

4. Create tasks/prd-[feature].md markdown version

### Phase 11: Output Summary

After completion, display:

```
## Claude Code Configuration Complete

### Created Files:
- CLAUDE.md (comprehensive project documentation)
- PROJECT_SPEC.md (RALPH context document)
- .claude/settings.json
- .claude/rules/*.md ([count] rules)
- .claude/commands/*.md ([count] commands)
- .claude/agents/*.md ([count] agents)
- .claude/skills/*/SKILL.md ([count] skills)
- .claude/hooks/hooks.json
- .claude/hooks/auto-compact.sh
- scripts/ralph/ralph.sh
- scripts/ralph/CLAUDE.md

[If PRD created:]
- prd.json ([count] user stories)
- progress.txt (initialized with patterns)
- tasks/prd-[feature].md

### Available Commands:
- /commit - Git commit with formatted message
- /review - Code review checklist
- /test - Run tests
- /ralph - RALPH status
- /ralph-run - Start RALPH

### RALPH Status:
[If PRD created:]
- Feature: "[feature description]"
- Stories: [count] total
- Branch: ralph/[feature-slug]
- Ready to run: ./scripts/ralph/ralph.sh 20

[If no PRD:]
- No PRD configured
- Create one: /prd [feature description]

### Next Steps:
1. Review CLAUDE.md for accuracy
2. Customize rules for team conventions
3. [If PRD] Run: ./scripts/ralph/ralph.sh 20
4. [If no PRD] Create PRD: /prd [feature]
```

---

## Tech Stack Detection Reference

| File | Stack |
|------|-------|
| `package.json` | Node.js ecosystem |
| `tsconfig.json` | TypeScript |
| `vite.config.*` | Vite bundler |
| `next.config.*` | Next.js framework |
| `nuxt.config.*` | Nuxt framework |
| `svelte.config.*` | SvelteKit |
| `angular.json` | Angular |
| `*.xcodeproj` | iOS/macOS |
| `build.gradle*` | Android/JVM |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pyproject.toml` | Python (modern) |
| `requirements.txt` | Python (legacy) |

## Files to Always Exclude

```
node_modules/
dist/
build/
.next/
.nuxt/
target/          # Rust
bin/             # Go compiled
__pycache__/
*.pyc
.venv/
venv/
.git/objects/
coverage/
*.log
```

---

## RALPH Workflow After Setup

```bash
# 1. Run setup (with optional feature)
/setup-project
# or
/setup-project --feature "User authentication system"

# 2. If PRD created, review it
cat prd.json
cat PROJECT_SPEC.md

# 3. Start RALPH autonomous development
./scripts/ralph/ralph.sh 20

# 4. Monitor progress
tail -f progress.txt
cat prd.json | jq '.userStories[] | {id, title, passes}'

# 5. When complete, review and merge
git log --oneline -20
git diff main...HEAD
```

## Interactive Mode

When run without `--yes`, prompt for:
1. Project name confirmation
2. Language/framework verification
3. Commands to enable (hooks, agents, commands, rules, skills)
4. RALPH setup preference
5. Initial feature description (optional)

## Command Line Options

```bash
/setup-project [options]
  -t, --target <path>     Target directory (default: current)
  -y, --yes               Skip prompts, use defaults
  -m, --merge             Merge with existing config
  -f, --feature <desc>    Create initial PRD for feature
  --no-hooks              Skip hooks setup
  --no-agents             Skip agents setup
  --no-commands           Skip commands setup
  --no-rules              Skip rules setup
  --no-skills             Skip skills setup
  --no-ralph              Skip RALPH setup
```

## Quality Assurance

Before completing setup, verify:
- [ ] CLAUDE.md accurately describes the project
- [ ] PROJECT_SPEC.md has correct tech stack
- [ ] Rules match detected language/framework
- [ ] Commands use correct package manager
- [ ] Hooks reference correct lint/test commands
- [ ] Settings.json has appropriate permissions
- [ ] RALPH scripts are executable (chmod +x)
- [ ] PRD stories (if created) are appropriately sized
