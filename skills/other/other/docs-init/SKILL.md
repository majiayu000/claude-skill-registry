---
name: docs-init
description: "(ePost) Scan codebase and generate comprehensive documentation"
user-invokable: true
context: fork
agent: epost-documenter
metadata:
  argument-hint: "[scan entire codebase and create docs/]"
---

# Docs: Init Command

Scan the entire codebase and generate comprehensive documentation files.

## Usage
```
/docs-init
```

## Your Process

### 1. Scan the Codebase
- Use Glob to explore directory structure
- Use Grep to find key patterns (imports, exports, types)
- Read key files (package.json, tsconfig, configs)
- Identify: framework, language, database, deployment

### 2. Generate Documentation Files

Create all files in `docs/` directory (create if doesn't exist):

#### `docs/codebase-summary.md`
```markdown
# Codebase Summary

## Project Overview
[What this project does]

## Tech Stack
- [Framework]
- [Language]
- [Database]
- [Deployment]

## Directory Structure
```
[dir tree]
```

## Key Files
- `path/to/file` - Description
- `path/to/file` - Description

## Getting Started
- Installation: [commands]
- Development: [commands]
- Build: [commands]
```

#### `docs/code-standards.md`
```markdown
# Code Standards

## Naming Conventions
- Files: [pattern]
- Variables: [pattern]
- Components: [pattern]

## Code Patterns Found
- [Pattern 1 with examples]
- [Pattern 2 with examples]

## Linting/Formatting
- Tool: [name]
- Config: [location]

## Testing Approach
- Framework: [name]
- Coverage: [target]
```

#### `docs/system-architecture.md`
```markdown
# System Architecture

## High-Level Overview
[Architecture diagram description]

## Core Modules
- **Module Name** - Purpose
  - Key files: [list]
  - Dependencies: [list]

## Data Flow
[How data moves through the system]

## Key Patterns
- [Pattern used and why]
```

#### `docs/api-routes.md` (if applicable)
```markdown
# API Routes

## REST Endpoints
| Method | Path | Description | File |
|--------|------|-------------|------|
| GET | /api/... | ... | src/... |
```

#### `docs/data-models.md` (if applicable)
```markdown
# Data Models

## Database Schema
[Tables/collections and relationships]

## TypeScript Types
[Key types and interfaces]

## State Management
[How state is managed]
```

#### `docs/deployment-guide.md`
```markdown
# Deployment Guide

## Environment Variables
[Required vars and descriptions]

## Build Process
[Commands and steps]

## Deployment Platforms
- [Platform 1]: [specifics]
- [Platform 2]: [specifics]

## CI/CD
[Pipeline info if found]
```

### 3. Save Files
- Create `docs/` directory if needed
- Write each markdown file
- Use proper formatting (headings, code blocks, tables)

## Analysis Rules
- Scan EVERYTHING - don't skip directories
- Look for config files (package.json, tsconfig.json, .env.example)
- Check for Docker files, CI configs
- Find test files to understand testing approach
- Look for README files
- Examine imports/exports to understand dependencies

## Completion
Report:
- Files created: [count]
- docs/ directory location
- Summary of findings (framework, language, patterns)
- Next steps for the user
