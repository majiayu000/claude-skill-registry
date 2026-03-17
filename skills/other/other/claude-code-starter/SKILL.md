---
name: claude-code-starter
description: Analyze a project's tech stack and generate comprehensive Claude Code configuration files (.claude/ directory with CLAUDE.md, skills, agents, rules, and commands). Use when setting up Claude Code for a new or existing repository.
---

# Claude Code Starter

You are setting up Claude Code configuration for a project. Follow the flow below to analyze the project and generate all `.claude/` configuration files.

## Step 1: Detect Project Type

Check if this is a **new project** (empty or <3 source files) or an **existing project**.

**For new projects**, ask the user these questions:
1. What are you building? (project description)
2. Primary language? (TypeScript, JavaScript, Python, Go, Rust, Swift, Kotlin, Java, Ruby, C#, PHP, C++)
3. Framework? (filtered by language — e.g. Next.js/React/Vue for TS/JS, FastAPI/Django/Flask for Python)
4. Package manager? (filtered by language)
5. Testing framework? (filtered by language, or "None")
6. Linter/Formatter? (filtered by language, or "None")
7. Project type? (Web App, API/Backend, CLI Tool, Library/Package, Mobile App, Desktop App, Monorepo, Other)

**For existing projects**, analyze the codebase:
- Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, or equivalent
- Detect languages, frameworks, package manager, testing, linting, formatting, bundler
- Identify architecture patterns, directory structure, code conventions

## Step 2: Create `.claude/settings.json`

Generate `settings.json` with permissions based on detected stack. Example:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read(**)", "Edit(**)", "Write(.claude/**)", "Bash(git:*)",
      "Bash(npm:*)", "Bash(node:*)"
    ]
  }
}
```

Add language/framework-specific permissions (e.g. `Bash(cargo:*)` for Rust, `Bash(pytest:*)` for Python).

## Step 3: Generate CLAUDE.md

Perform deep codebase analysis and generate `.claude/CLAUDE.md` following this structure:

### Phase 1: Discovery

Read actual project files to discover:
- Project identity (name, version, description, purpose)
- Directory structure map (depth 3)
- Tech stack deep scan (languages, frameworks, database, auth, API layer, styling, build tools, CI/CD)
- Architecture pattern recognition (MVC, Clean, Hexagonal, etc.)
- Entry points and key files
- Code conventions (naming, imports, exports, function style, error handling)
- Development workflow (scripts, env vars, pre-commit hooks, testing setup)
- Domain knowledge (entities, workflows, integrations)

### Phase 2: Write CLAUDE.md

Using ONLY discovered information, write `.claude/CLAUDE.md` with:
- Project name + one-line description
- Overview (purpose, audience, value proposition)
- Architecture (pattern, directory structure, data flow, key files)
- Tech stack table
- Development setup (prerequisites, getting started, env variables)
- Common commands
- Code conventions (naming patterns, patterns to follow, anti-patterns)
- Testing (commands, writing patterns)
- Domain knowledge (entities, workflows)
- Gotchas & important notes
- Rules

### Phase 3: Quality Check

Verify every section contains project-specific content, not generic boilerplate. Skip sections without real content.

## Step 4: Generate Skills

Write each skill file to `.claude/skills/` with YAML frontmatter (`name`, `description`, `globs`).

### Core Skills (ALWAYS generate all 8):

1. **`.claude/skills/pattern-discovery.md`** — Analyze codebase to discover and document patterns. Include project-specific search strategies based on the actual directory structure and file patterns found.

2. **`.claude/skills/systematic-debugging.md`** — 4-phase methodology: Reproduce, Locate, Diagnose, Fix. Tailor reproduction steps to the project's actual test runner and dev server commands.

3. **`.claude/skills/testing-methodology.md`** — AAA pattern (Arrange, Act, Assert). Use the project's actual testing framework syntax (e.g., `describe`/`it` for Jest/Vitest, `def test_` for pytest). Include mocking patterns specific to the stack.

4. **`.claude/skills/iterative-development.md`** — TDD workflow loop: write failing test → implement → verify → refactor. Use the project's actual test command and lint command.

5. **`.claude/skills/commit-hygiene.md`** — Atomic commits, conventional commit format, size thresholds (±300 lines), when-to-commit triggers.

6. **`.claude/skills/code-deduplication.md`** — Check-before-write principle. Search existing code before writing new code. Include project-specific glob patterns for common file types.

7. **`.claude/skills/simplicity-rules.md`** — Function length limits (≤40 lines), file limits (≤300 lines), cyclomatic complexity constraints. Decomposition patterns.

8. **`.claude/skills/security.md`** — .gitignore entries for the stack, environment variable handling patterns, OWASP checklist items relevant to the detected framework.

### Framework-Specific Skills (ONLY if detected):

Generate the appropriate skill based on detected frameworks:

| Framework | Skill File | Key Content |
|-----------|-----------|-------------|
| Next.js | `nextjs-patterns.md` | App Router, Server/Client Components, data fetching, middleware |
| React (no Next.js) | `react-components.md` | Hooks, component patterns, state management, performance |
| FastAPI | `fastapi-patterns.md` | Router organization, dependency injection, Pydantic models, async |
| NestJS | `nestjs-patterns.md` | Modules, controllers, services, decorators, pipes, guards |
| SwiftUI | `swiftui-patterns.md` | Property wrappers, MVVM, navigation, previews |
| UIKit | `uikit-patterns.md` | View controllers, Auto Layout, delegates, MVC |
| Vapor | `vapor-patterns.md` | Routes, middleware, Fluent ORM, async controllers |
| Jetpack Compose | `compose-patterns.md` | @Composable, remember, ViewModel, navigation |
| Android Views | `android-views-patterns.md` | Activities, Fragments, XML layouts, ViewBinding |
| Vue/Nuxt | `vue-patterns.md` | Composition API, composables, Pinia, routing |
| Django | `django-patterns.md` | Models, views, serializers, middleware, admin |
| Rails | `rails-patterns.md` | MVC, ActiveRecord, concerns, service objects |
| Spring | `spring-patterns.md` | Beans, controllers, services, repositories, AOP |

Tailor ALL skill content to the specific project's patterns, file structure, and conventions discovered during analysis.

## Step 5: Generate Agents

Write 2 agent files to `.claude/agents/`:

### `.claude/agents/code-reviewer.md`
```yaml
---
name: code-reviewer
description: Reviews code for quality, security issues, and best practices
tools:
  - Read
  - Grep
  - Glob
  - "Bash(biome check .)"  # Use actual lint command
disallowed_tools:
  - Write
  - Edit
model: sonnet
---
```
Body: Instructions for reviewing code quality, security, naming conventions, test coverage, and adherence to project patterns.

### `.claude/agents/test-writer.md`
```yaml
---
name: test-writer
description: Generates comprehensive tests for code
tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - "Bash(bun test)"  # Use actual test command
model: sonnet
---
```
Body: Instructions for writing tests using the project's actual testing framework, following existing test patterns.

## Step 6: Generate Rules

Write rule files to `.claude/rules/`:

### Always Generate:
- **`.claude/rules/code-style.md`** — Formatting tool, comment style, error handling, git commit conventions.

### Conditional (by language):
| Language | File | YAML `paths` | Key Rules |
|----------|------|--------------|-----------|
| TypeScript | `typescript.md` | `["**/*.ts", "**/*.tsx"]` | Strict mode, type annotations, import style |
| Python | `python.md` | `["**/*.py"]` | Type hints, docstrings, import ordering |
| Swift | `swift.md` | `["**/*.swift"]` | Access control, optionals, protocol-oriented |
| Go | `go.md` | `["**/*.go"]` | Error handling, interfaces, package naming |
| Rust | `rust.md` | `["**/*.rs"]` | Ownership, error handling, trait patterns |

Each rule file needs YAML frontmatter with `paths` for file matching.

## Step 7: Generate Commands

Write 5 command files to `.claude/commands/`:

### `.claude/commands/task.md`
```yaml
---
allowed-tools: ["Read", "Write", "Edit", "Glob"]
description: "Start or switch to a new task"
argument-hint: "<task description>"
---
```
Instructions to update `.claude/state/task.md` with new task, set status to "In Progress".

### `.claude/commands/status.md`
```yaml
---
allowed-tools: ["Read", "Glob", "Bash(git status)"]
description: "Show current task and session state"
---
```
Instructions to read task.md, show git status, summarize current state.

### `.claude/commands/done.md`
```yaml
---
allowed-tools: ["Read", "Write", "Edit", "Glob", "Bash(git:*)", "Bash(bun test)"]
description: "Mark current task complete"
---
```
Instructions to run tests, lint, verify, update task.md status to "Done".

### `.claude/commands/analyze.md`
```yaml
---
allowed-tools: ["Read", "Glob", "Grep"]
description: "Deep analysis of a specific area"
argument-hint: "<area or file path>"
---
```
Instructions to perform thorough analysis of specified area.

### `.claude/commands/code-review.md`
```yaml
---
allowed-tools: ["Read", "Glob", "Grep", "Bash(git diff)"]
description: "Review code changes for quality and security"
---
```
Instructions to review staged/unstaged changes.

## Output Summary

After generating all files, output a brief summary:
- List of files created
- Any gaps found (missing config files, unclear patterns)
- Suggested next steps

## Important Guidelines

1. **Be specific, not generic.** Every file must contain project-specific content.
2. **Reference real files.** Use `path/to/file.ts:lineNumber` format.
3. **Use actual commands.** Reference the project's real test/lint/build commands.
4. **Skip what doesn't apply.** Don't generate framework skills for frameworks not in use.
5. **Respect existing files.** If `.claude/` files exist, read and preserve manually-added content.
