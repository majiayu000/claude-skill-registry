---
name: claude-md-manager
description: Create, audit, and maintain CLAUDE.md documentation files that configure Claude Code for projects. Use this skill when (1) initializing a new project with Claude Code configuration, (2) reviewing or improving existing CLAUDE.md files, (3) organizing project instructions using progressive disclosure patterns, (4) converting repeated instructions into permanent documentation, or (5) setting up agent_docs/ structures for larger codebases. Handles the WHAT/WHY/HOW framework, conciseness optimization, and file import patterns.
---

# CLAUDE.md Manager

Create and maintain effective CLAUDE.md files that configure Claude Code's project behavior.

## Core Workflow

### 1. Determine the Mode

**Creating new CLAUDE.md:**
- Analyze project structure, tech stack, and conventions
- Generate focused documentation using WHAT/WHY/HOW framework
- Target under 100 lines (max 300)

**Refreshing existing CLAUDE.md:**
- Audit current content for bloat, staleness, and anti-patterns
- Identify instructions that should be externalized
- Optimize for conciseness and relevance

### 2. Project Analysis (for new files)

Examine:
- `package.json`, `Cargo.toml`, `pyproject.toml`, etc. for stack
- Directory structure for architecture patterns
- Existing README.md for project context
- `.github/`, `Makefile`, scripts for workflows
- Test directories for testing conventions

### 3. Apply the WHAT/WHY/HOW Framework

**WHAT** - Technical reality:
- Tech stack and key dependencies
- Directory structure and architecture
- Key files and entry points

**WHY** - Context and purpose:
- What the project does
- Why certain patterns exist
- Functional purpose of directories

**HOW** - Practical workflows:
- Build commands (package manager specifics)
- Test execution
- Development workflow
- Deployment process

### 4. Validation Review Pass

After creating or refreshing CLAUDE.md, validate claims against the actual codebase using OSGrep. This catches stale commands, incorrect paths, and drifted conventions.

#### Validation Steps

**1. Validate Commands**
```bash
# For each command documented, verify it exists
osgrep "dev server startup configuration" -p $REPO -m 3
osgrep "test runner setup" -p $REPO -m 3
osgrep "build script configuration" -p $REPO -m 3
```

**2. Validate Directory Structure**
```bash
# Verify directories contain what's documented
osgrep "component definitions" -p $REPO/src/components -m 3
osgrep "API route handlers" -p $REPO/src/routes -m 3
```

**3. Validate @import References**
```bash
# Check each @path/to/file reference exists
test -f $REPO/docs/architecture.md && echo "EXISTS" || echo "MISSING"
```

**4. Validate Conventions**
```bash
# Verify conventions match actual code patterns
osgrep "error handling patterns" -p $REPO -m 5
osgrep "state management approach" -p $REPO -m 5
```

#### Validation Report Format

```markdown
## Validation Report
- [x] `pnpm dev` - Verified in package.json scripts
- [x] `/src/components` - Contains 23 .tsx files
- [ ] `/src/services` - **EMPTY** - No files found
- [ ] `@agent_docs/testing.md` - **MISSING**
- [ ] "No class components" - **VIOLATION**: Found 2 in /src/legacy/
```

#### Deep Validation with /review (Optional)

For large codebases or quarterly audits, run multi-agent review:

```
/compounding-engineering:workflows:review CLAUDE.md
```

This invokes architecture-strategist and pattern-recognition-specialist agents to thoroughly verify structure claims and convention accuracy.

## Conciseness Rules

**Context budget:** Claude's context window is shared. Every line in CLAUDE.md competes with conversation history and system prompts. LLMs can follow ~150-200 instructions consistently; the system prompt already uses ~50.

**Targets:**
- Ideal: Under 60 lines (like HumanLayer's production file)
- Good: Under 100 lines
- Maximum: 300 lines (refactor if exceeded)

**Techniques:**
- Use `file:line` references instead of copying code
- Externalize task-specific docs to `agent_docs/`
- Remove anything Claude can infer from code
- Delete obvious instructions (Claude reads code patterns)

## Progressive Disclosure Pattern

When CLAUDE.md grows beyond 100 lines, split into focused files:

```
agent_docs/
├── building.md          # Build process details
├── testing.md           # Test conventions and execution
├── code-conventions.md  # Style and patterns
├── architecture.md      # System design decisions
└── deployment.md        # Release process
```

Reference in CLAUDE.md:
```markdown
# Detailed Guides
- Building: @agent_docs/building.md
- Testing: @agent_docs/testing.md
- Architecture: @agent_docs/architecture.md
```

Claude loads these only when relevant.

### Beyond agent_docs/

Three additional progressive disclosure mechanisms complement `agent_docs/`:

- **`.claude/rules/*.md`** — Path-scoped modular instructions with YAML frontmatter `paths:` globs. Load conditionally when matching files are in context. Use for instructions that apply only to specific file paths. See `references/memory-hierarchy.md` for the full rules reference.
- **Skills** (`.claude/skills/`) — Domain knowledge that is only sometimes relevant. CLAUDE.md loads every session; skills load on demand with zero context cost when inactive.
- **Custom subagents** (`.claude/agents/*.md`) — Agent-specific instructions belong in agent definitions, not in CLAUDE.md. Agent files support tool restrictions and model selection.

## File Import Syntax

CLAUDE.md supports `@path/to/file` imports:
- `@README.md` - Import from project root
- `@docs/guide.md` - Import from subdirectory
- `@~/.claude/personal.md` - Personal preferences (not committed)
- Works recursively up to 5 levels
- Not evaluated inside code blocks
- Start imported files at `##` heading level to avoid hierarchy conflicts with the main CLAUDE.md

## Anti-Patterns to Avoid

**Avoid these patterns:**

1. **Linting via LLM** - CLAUDE.md instructions are advisory (the agent may ignore under context pressure). Use hooks for guaranteed execution:
   ```markdown
   # WRONG - Don't add to CLAUDE.md:
   "Always run eslint before committing"

   # RIGHT - Use a hook instead (deterministic, runs every time)
   ```

2. **Auto-generated CLAUDE.md** - `/init` produces suboptimal results. Craft manually.

3. **Exhaustive style guides** - Claude learns from existing code patterns.

4. **Task-specific instructions in root file** - Use agent_docs/ instead.

5. **Inline code snippets** - Use `file:line` references that stay current.

6. **Secrets or credentials** - CLAUDE.md should be treated as public.

7. **Negative-only constraints** - Bare prohibitions ("never do X") with no alternative cause stuck agents. Every "never X" should end with "— do Y instead."

8. **Bare file references** - Naked `@path` imports without context get ignored. Pitch each import: explain when and why to read it (e.g., `@agent_docs/testing.md — test conventions and coverage thresholds. Read when writing or modifying tests.`).

## Template Structure

```markdown
# Project Name

Brief description of what this project does.

## Stack
- [Framework] with [Key libraries]
- [Database/Storage]
- [Key tooling]

## Structure
- `/src` - Application code
- `/tests` - Test suites
- `/docs` - Documentation

## Commands
- Dev: `npm run dev`
- Test: `npm test`
- Build: `npm run build`

## Conventions
- [Critical convention 1]
- [Critical convention 2]

## Workflow
- Branch naming: `feature/description`
- Commits: Conventional Commits format
- PR: Rebase before merge

## Architecture Notes
@docs/architecture.md (if complex)
```

## Audit Checklist (for refresh)

When reviewing existing CLAUDE.md:

- [ ] Under 100 lines? If not, identify extraction candidates
- [ ] Using `file:line` refs instead of inline code?
- [ ] Task-specific docs in agent_docs/?
- [ ] No linting/style enforcement (use hooks)?
- [ ] No credentials or secrets?
- [ ] No obvious/inferable instructions?
- [ ] All commands actually work?
- [ ] Architecture info still accurate?
- [ ] OSGrep validation run? (commands, directories, conventions)
- [ ] File references still valid?
- [ ] Negative instructions paired with alternatives?
- [ ] File imports pitched (explain when/why to read)?
- [ ] Path-specific instructions in `.claude/rules/` instead of root CLAUDE.md?

## Global Registration

When creating or refreshing a project CLAUDE.md, ensure the project has an entry in `~/.claude/agent_docs/active-projects.md` with its directory and active plan.

## Hierarchical Files

For monorepos, use CLAUDE.md at multiple levels:

```
/CLAUDE.md              # Repo-wide conventions
/frontend/CLAUDE.md     # Frontend-specific
/backend/CLAUDE.md      # Backend-specific
/services/auth/CLAUDE.md # Service-specific
```

Each file is concise and scope-appropriate.

## Resources

- `references/best-practices.md` - Deep dive on effectiveness patterns
- `references/memory-hierarchy.md` - Instruction placement, `.claude/rules/`, `CLAUDE.local.md`
- `references/templates.md` - Project-type-specific templates (9 variants)
- `scripts/analyze_project.py` - Automated project structure analysis
