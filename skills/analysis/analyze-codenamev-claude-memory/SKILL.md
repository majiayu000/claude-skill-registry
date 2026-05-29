---
name: project-analysis
description: Knowledge about analyzing projects for tech stack, frameworks, tools, and conventions. Use when asked to understand or learn about a project's structure.
user-invocable: false
---

# Analyze Project Skill

Analyze the current project and store facts about it in long-term memory.

## Workflow

1. **Read key project files** to understand the tech stack
2. **Extract facts** about languages, frameworks, tools, conventions
3. **Store facts** using `memory.store_extraction`

## Files to Read

Read these files (if they exist) to understand the project:

### Package/Dependency Files
- `Gemfile` - Ruby dependencies (Rails, RSpec, etc.)
- `package.json` - JavaScript/TypeScript dependencies
- `pyproject.toml` or `requirements.txt` - Python dependencies
- `Cargo.toml` - Rust dependencies
- `go.mod` - Go dependencies
- `pom.xml` or `build.gradle` - Java dependencies

### Configuration Files
- `README.md` - Project overview and setup instructions
- `tsconfig.json` - TypeScript configuration
- `.eslintrc*` or `eslint.config.*` - ESLint configuration
- `.prettierrc*` - Prettier configuration
- `.rubocop.yml` or `.standard.yml` - Ruby linting
- `Dockerfile` - Container configuration
- `.github/workflows/*.yml` - CI/CD configuration

### Convention Files
- `.editorconfig` - Editor configuration
- `CLAUDE.md` or `AGENTS.md` - AI assistant instructions

## What to Extract

Look for and store facts about:

| Category | Predicate | Examples |
|----------|-----------|----------|
| Languages | `uses_language` | Ruby, TypeScript, Python, Go, Rust |
| Frameworks | `uses_framework` | Rails, React, Next.js, Django, FastAPI |
| Tools | `uses_tool` | RSpec, Jest, ESLint, Prettier, Docker |
| Databases | `uses_database` | PostgreSQL, MySQL, Redis, MongoDB |
| Package Manager | `uses_package_manager` | Bundler, npm, pnpm, Poetry, Cargo |
| CI/CD | `uses_ci` | GitHub Actions, CircleCI, GitLab CI |
| Conventions | `has_convention` | EditorConfig, 2-space indentation |

## Example Analysis

After reading `Gemfile`:
```ruby
source 'https://rubygems.org'
gem 'rails', '~> 7.0'
gem 'pg'
gem 'rspec-rails', group: :test
```

Store these facts:
```json
{
  "entities": [
    {"type": "language", "name": "Ruby"},
    {"type": "framework", "name": "Rails"},
    {"type": "database", "name": "PostgreSQL"},
    {"type": "tool", "name": "RSpec"}
  ],
  "facts": [
    {
      "subject": "repo",
      "predicate": "uses_language",
      "object": "Ruby",
      "quote": "Gemfile present",
      "strength": "stated"
    },
    {
      "subject": "repo",
      "predicate": "uses_framework",
      "object": "Rails",
      "quote": "gem 'rails', '~> 7.0'",
      "strength": "stated"
    },
    {
      "subject": "repo",
      "predicate": "uses_database",
      "object": "PostgreSQL",
      "quote": "gem 'pg'",
      "strength": "stated"
    },
    {
      "subject": "repo",
      "predicate": "uses_tool",
      "object": "RSpec",
      "quote": "gem 'rspec-rails'",
      "strength": "stated"
    },
    {
      "subject": "repo",
      "predicate": "uses_package_manager",
      "object": "Bundler",
      "quote": "Gemfile present",
      "strength": "stated"
    }
  ]
}
```

## Best Practices

1. **Check what exists first**: Use `memory.recall` with broad query like "uses" to see existing facts
2. **Don't duplicate**: Skip facts that are already stored
3. **Include quotes**: Reference the specific line or file where you found the information
4. **Use `stated` strength**: For explicit declarations in config files
5. **Be selective**: Only store durable, useful facts—not every dependency

## Scope

- Use `scope_hint: "project"` for project-specific facts (default)
- Use `scope_hint: "global"` for user preferences found in global config files
