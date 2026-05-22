---
name: agent-ops-docs
description: "Documentation management for README, CHANGELOG, API docs, and user-facing documentation. Use when creating or updating project documentation."
category: utility
invokes: [agent-ops-state, agent-ops-interview]
invoked_by: [agent-ops-implementation, agent-ops-critical-review]
state_files:
  read: [constitution.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Documentation Workflow

## Purpose

Manage user-facing documentation (README, CHANGELOG, API docs) with consistency and traceability. Ensures documentation stays synchronized with code changes.

## When to Use

- After implementing a feature that affects public API or usage
- When creating a new project (initial README)
- Before release (CHANGELOG update)
- When user requests documentation updates
- During critical review (docs consistency check)

## Documentation Types

### README.md

**Purpose**: First point of contact for new users/developers

**Required Sections**:
- Project title and description
- Installation/setup instructions
- Basic usage examples
- Configuration options (if applicable)
- Contributing guidelines (or link)
- License

**Update Triggers**:
- New feature that changes usage
- Installation process changes
- Dependencies change significantly
- Project scope/purpose evolves

### CHANGELOG.md

**Purpose**: Track notable changes between versions

**Format** (Keep a Changelog standard):
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior Y

### Fixed
- Bug fix Z

### Removed
- Deprecated feature W

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release features
```

**Update Triggers**:
- Any user-facing change
- Bug fixes
- Breaking changes (MUST document)
- Deprecations

### API Documentation

**Purpose**: Technical reference for developers

**Formats**:
- Inline docstrings (for code-level docs)
- OpenAPI/Swagger (for REST APIs)
- TypeDoc/JSDoc (for TypeScript/JavaScript)
- Sphinx/MkDocs (for Python)

**Update Triggers**:
- New public function/method/endpoint
- Parameter changes
- Return type changes
- Behavior changes

## Procedure

### Creating Documentation

1. **Identify audience**: Who will read this?
2. **Determine scope**: What must be covered?
3. **Check constitution**: Any doc-related constraints?
4. **Draft content**: Use appropriate template
5. **Review for accuracy**: Cross-check with code
6. **Update focus.md**: Note what was documented

### Updating Documentation

1. **Identify what changed**: Feature, API, behavior?
2. **Find affected docs**: README? CHANGELOG? API docs?
3. **Make minimal update**: Only what's necessary
4. **Verify examples work**: Run any code snippets
5. **Update CHANGELOG**: If user-facing change
6. **Update focus.md**: Note the update

### Documentation Review Checklist

- [ ] Accurate: Matches current code behavior
- [ ] Complete: Covers all public interfaces
- [ ] Clear: Understandable by target audience
- [ ] Examples: Working code samples included
- [ ] Up-to-date: No references to removed features
- [ ] Consistent: Terminology matches codebase

## Templates

### README Section Template

```markdown
## Feature Name

Brief description of what this feature does.

### Usage

\`\`\`language
// Example code showing basic usage
\`\`\`

### Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | string | "default" | What it does |

### Notes

Any important caveats or tips.
```

### CHANGELOG Entry Template

```markdown
## [Version] - YYYY-MM-DD

### Added
- **Feature name**: Brief description ([#issue](link))

### Changed
- **Component**: What changed and why ([#issue](link))

### Fixed
- **Bug description**: How it was fixed ([#issue](link))

### Breaking Changes
- **What broke**: Migration instructions
```

## Integration with AgentOps Workflow

### During Planning

- Identify docs that will need updates
- Add doc tasks to plan if significant

### During Implementation

- Update inline docs as code is written
- Note doc updates needed in focus.md

### During Critical Review

- Verify README accuracy
- Verify CHANGELOG is updated
- Check for stale documentation

### After Completion

- Final CHANGELOG entry
- README updates if needed
- API doc regeneration if applicable

## Location Rules

| Doc Type | Location | Notes |
|----------|----------|-------|
| README | Project root | Always `README.md` |
| CHANGELOG | Project root | Always `CHANGELOG.md` |
| API docs | `docs/` or `doc/` | Follow project convention |
| Agent docs | `.agent/docs/` | Internal agent documentation only |

## Anti-Patterns

- ❌ Documentation in code comments only (not discoverable)
- ❌ Outdated examples that don't work
- ❌ Documenting implementation details (unstable)
- ❌ Duplicating info across multiple docs
- ❌ Empty CHANGELOG entries ("various fixes")
- ❌ Version numbers without dates

```
