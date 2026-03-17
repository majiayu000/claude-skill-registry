---
name: commit
description: Create git commits following Conventional Commits format. Analyzes staged changes and generates properly formatted commit messages.
argument-hint: [optional message hint]
---

# Conventional Commit Generator

Create git commits following Conventional Commits specification.

## Usage

Run `/commit` to analyze staged changes and create a properly formatted commit.

## Workflow

1. Run `git status` and `git diff --staged` to see changes
2. Determine the commit type based on changes
3. Determine the scope (area of codebase)
4. Create commit with format: `type(scope): description`

## Commit Types

- `feat` - New feature (bumps minor version)
- `fix` - Bug fix (bumps patch version)
- `docs` - Documentation only
- `style` - Code style changes
- `refactor` - Code refactoring
- `perf` - Performance improvement (bumps patch version)
- `test` - Adding or fixing tests
- `build` - Build system or dependencies
- `ci` - CI configuration
- `chore` - Other changes

## Scopes for Fair-Forge

- `metrics` - Metric implementations
- `runners` - Test runners
- `generators` - Data generators
- `storage` - Storage backends
- `schemas` - Pydantic models
- `core` - Base classes
- `llm` - LLM integration
- `guardians` - Bias/toxicity guardians
- `deps` - Dependencies

## Commit Format

Simple: `type(scope): description`

Examples:
- `feat(metrics): add agentic evaluation metric`
- `fix(toxicity): handle empty batches`
- `docs: update installation guide`
- `refactor(core): extract base retriever logic`
- `test(runners): add integration tests`
- `build(deps): upgrade langchain-core`

For breaking changes, add exclamation mark after scope: `feat(schemas)!: rename field`

## Rules

- Use imperative mood: "add feature" not "added feature"
- Keep description under 72 characters
- Lowercase description
- No period at end
- NEVER add "Co-Authored-By" or any similar attribution line to commits
