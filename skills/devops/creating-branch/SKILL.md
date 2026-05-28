---
name: creating-branch
description: Creates feature branches with optimized short naming, auto-incrementing, and commit type detection (feat/fix/refactor). Supports manual descriptions and auto-generation from uncommitted git changes. Use when user requests to create branch, start new branch, make branch, checkout new branch, switch branch, new task, start working on, begin work on feature, begin feature, create feature branch, run /create-branch command, or mentions "branch", "feature", "new feature", "feat", "fix", or "checkout".
model: haiku
---

# Git Branch Creation Workflow

Execute feature branch creation with intelligent naming, automatic type detection, and sequential numbering.

## Usage

This skill is invoked when:
- User runs `/create-branch` or `/git:create-branch` command
- User requests to create a new feature branch
- User asks to start a new branch for a task

## Two Operation Modes

### Mode 1: With Description (Manual)

The command takes a description and automatically detects the commit type.

**Format**: `/create-branch <description>`

**Examples**:
```bash
/create-branch add user authentication
→ Creates: feat/001-user-authentication

/create-branch fix login bug
→ Creates: fix/002-login-bug

/create-branch refactor auth service
→ Creates: refactor/003-auth-service

/create-branch remove deprecated code
→ Creates: chore/004-remove-deprecated

/create-branch document api endpoints
→ Creates: docs/005-document-api
```

### Mode 2: Auto-Generate from Changes (No Arguments)

When no arguments provided and no sdlc-develop specs exist, analyze uncommitted changes to generate branch name automatically.

**Format**: `/create-branch` (no arguments)

**Process**:
1. Check for sdlc-develop specs (see Mode 3)
2. If no specs, check for uncommitted changes (both staged and unstaged)
3. If no changes exist, display error and require description
4. If changes exist, analyze to generate description
5. Create branch with auto-generated name

**Examples**:
```bash
# After modifying authentication files
/create-branch
→ Auto-detected from changes: feat/006-authentication-system
→ (based on: login.py, auth_service.ts, user_model.py)

# After fixing payment bug
/create-branch
→ Auto-detected from changes: fix/007-payment-processing
→ (based on: payment.js, checkout.py)
```

### Mode 3: From SDLC-Develop Spec (Arkhe Integration)

When no arguments provided and sdlc-develop specs exist, the skill can create branches linked to existing feature specs.

**Detection Flow:**
1. Check if `.arkhe.yaml` exists → read `develop.specs_dir` (default: `arkhe/specs`)
2. Scan `{specs_dir}/` for existing spec directories
3. If specs found → present selection via `AskUserQuestion`
4. Use spec directory name for branch name

**Example:**
```bash
# Specs exist: arkhe/specs/01-user-auth/, arkhe/specs/02-dashboard/
/create-branch

# Prompt: "Select a feature spec for this branch"
# Options: 01-user-auth, 02-dashboard, None (auto-generate from changes)

# User selects 01-user-auth
→ Creates: feat/01-user-auth
```

## Commit Type Detection

The workflow automatically detects commit types from keywords in the description:

| Type | Keywords |
|------|----------|
| **feat** | add, create, implement, new, update, improve |
| **fix** | fix, bug, resolve, correct, repair |
| **refactor** | refactor, rename, reorganize |
| **chore** | remove, delete, clean, cleanup |
| **docs** | docs, document, documentation |

If no keyword is detected, defaults to `feat`.

## Branch Naming Format

**Pattern**: `{type}/{number}-{keyword1}-{keyword2}`

**Components**:
- **type**: Auto-detected commit type (feat, fix, refactor, chore, docs)
- **number**: Auto-incremented 3-digit number (001, 002, 003...)
- **keywords**: First 2-3 meaningful words from description (lowercase, hyphenated)

**Examples**:
- Input: "add user authentication system"
- Output: `feat/001-user-authentication`

- Input: "fix null pointer in login"
- Output: `fix/002-null-pointer`

## Important Notes

- **Sequential Numbering**: Finds next available number by scanning existing branches
- **Keyword Extraction**: Filters common words, keeps 2-3 meaningful terms
- **Lowercase Convention**: All branch names are lowercase with hyphens
- **Conventional Commits**: Aligns with conventional commit types
- **SDLC-Develop Integration**: Detects feature specs from `.arkhe.yaml`

## Supporting Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Detailed step-by-step process with bash scripts
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world examples for all branch types
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
