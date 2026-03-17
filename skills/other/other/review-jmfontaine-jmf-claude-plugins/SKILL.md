---
name: review
description: Review project files for consistency, completeness, and correctness. Use when asked to review, audit, check, or validate project configuration files (justfile, Makefile, CI workflows, pre-commit config, pyproject.toml, Dockerfile, docker-compose, etc.) or documentation files (README, CLAUDE.md, CONTRIBUTING, etc.). Supports both single-file review and cross-file consistency checks.
---

# Project File Review

Review project files across three dimensions, then suggest fixes and improvements.

## Dimensions

- **Consistency**: Naming conventions, formatting, patterns, and style are uniform within and across files.
- **Completeness**: Nothing is missing. All referenced targets, commands, variables, and dependencies exist. All expected sections are present.
- **Correctness**: Syntax is valid. Commands work. Paths exist. Versions are compatible. Logic is sound.

## Workflow

### Phase 1: Individual File Review

Review each file separately. For each file:

1. Read the file fully.
2. Evaluate against all three dimensions.
3. Report findings grouped by dimension.
4. Suggest specific fixes with code snippets.

### Phase 2: Cross-File Consistency

When multiple files are provided, or after individual reviews, check alignment across files:

1. Verify shared references match (e.g., target names in justfile match CI workflow steps, Python version in pyproject.toml matches CI matrix and Dockerfile).
2. Check that documented commands in README match actual targets/scripts.
3. Confirm dependency lists are synchronized (e.g., pyproject.toml vs requirements files vs CI install steps).
4. Ensure CLAUDE.md reflects the actual project structure and tooling.

### Discovery Mode

When reviewing a file, suggest other project files that should be cross-checked. Common relationships:

- **justfile / Makefile** <-> CI workflows, README, pre-commit config
- **pyproject.toml** <-> Dockerfile, CI workflows, pre-commit config
- **README** <-> CLAUDE.md, justfile, CI workflows
- **Dockerfile** <-> docker-compose, CI workflows, pyproject.toml
- **pre-commit config** <-> CI workflows, pyproject.toml

Offer to review related files the user hasn't mentioned yet.

## Output Format

For each file, report:

```
### <filename>

#### Consistency
- [finding + suggested fix]

#### Completeness
- [finding + suggested fix]

#### Correctness
- [finding + suggested fix]
```

After all individual reviews, add a cross-file section:

```
### Cross-File Alignment
- [inconsistency + which files + suggested fix]
```

Omit empty sections. Prioritize actionable findings over nitpicks.
