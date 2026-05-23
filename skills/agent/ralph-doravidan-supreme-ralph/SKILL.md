---
name: ralph
description: Run RALPH autonomous development loop. Converts PRD markdown to prd.json and runs autonomous implementation.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# RALPH Skill - PRD Conversion & Management

Convert PRD Markdown files to prd.json format and manage RALPH autonomous development.

## Triggers

This skill activates when:
- `/ralph` - Show status and help
- `/ralph --status` - Show detailed PRD status
- `/ralph --validate` - Validate prd.json
- `/ralph --reset` - Reset progress.txt for fresh start
- `/ralph --analyze` - Re-analyze project and update specs
- `/ralph-convert <file>` - Convert PRD markdown to prd.json

## Commands

### `/ralph` - Status & Help

Show current PRD status and available commands:

```bash
# Check if prd.json exists
if [ -f prd.json ]; then
  echo "=== RALPH Status ==="
  cat prd.json | jq '{
    project: .project,
    branch: .branchName,
    total: (.userStories | length),
    complete: ([.userStories[] | select(.passes == true)] | length),
    remaining: ([.userStories[] | select(.passes == false)] | length)
  }'

  echo ""
  echo "=== Stories ==="
  cat prd.json | jq -r '.userStories[] | "\(.id): \(.title) [\(if .passes then "✓" else "○" end)]"'
else
  echo "No prd.json found."
  echo ""
  echo "Create one with:"
  echo "  /prd [feature description]"
fi
```

### `/ralph --status` - Detailed Status

```bash
echo "=== PRD Status ==="
cat prd.json | jq '.'

echo ""
echo "=== Progress Log (last 50 lines) ==="
tail -50 progress.txt 2>/dev/null || echo "No progress.txt found"

echo ""
echo "=== Git Status ==="
git status --short
git log --oneline -5
```

### `/ralph --validate` - Validate PRD

Check prd.json for issues:

```bash
# Validation checks:
# 1. JSON is valid
# 2. Required fields exist
# 3. All stories have acceptance criteria
# 4. Stories have quality gate criteria
# 5. Priorities are sequential
# 6. Branch name follows convention
```

**Validation Rules:**
- `project` - Required, non-empty string
- `branchName` - Required, format: `ralph/[slug]`
- `userStories` - Required, non-empty array
- Each story must have:
  - `id` - Format: `US-XXX`
  - `title` - Non-empty string
  - `acceptanceCriteria` - Array with at least 2 items
  - `priority` - Number 1-10
  - `passes` - Boolean

**Output:**
```
Validating prd.json...

✓ JSON is valid
✓ Project name: [name]
✓ Branch: ralph/[slug]
✓ Stories: [N] total

Story Validation:
  US-001: [Title] ✓
  US-002: [Title] ✓
  ...

⚠ Warnings:
  - US-003: Missing "Tests pass" in acceptance criteria
  - US-005: Large story (6+ criteria), consider splitting

✓ PRD is valid and ready for RALPH
```

### `/ralph --reset` - Reset Progress

Reset progress.txt while preserving patterns:

```bash
# Archive current progress
if [ -f progress.txt ]; then
  mkdir -p archive/$(date +%Y-%m-%d)
  cp progress.txt archive/$(date +%Y-%m-%d)/progress-backup.txt
fi

# Extract patterns section from current progress
PATTERNS=$(sed -n '/## Codebase Patterns/,/^---$/p' progress.txt 2>/dev/null)

# Get branch name from prd.json
BRANCH=$(cat prd.json | jq -r '.branchName')

# Create fresh progress.txt
cat > progress.txt << EOF
# Progress Log - $BRANCH

Reset: $(date +%Y-%m-%d)

$PATTERNS

---

EOF

echo "Progress reset. Previous progress archived."
```

### `/ralph --analyze` - Re-analyze Project

Re-run project analysis and update specs:

```bash
# This triggers the project analyzer to refresh:
# - PROJECT_SPEC.md
# - scripts/ralph/CLAUDE.md context
# - progress.txt patterns

node scripts/run-ralph.js --analyze
```

### `/ralph-convert <file>` - Convert PRD to JSON

Convert a PRD markdown file to prd.json:

```
Converting: tasks/prd-[feature].md

Reading PRD...
Extracting project info...
Parsing user stories...
Validating structure...

Generated prd.json:
- Project: [Feature Name]
- Branch: ralph/[feature-slug]
- Stories: [N] total

Initializing progress.txt...
Done!

Next: ./scripts/ralph/ralph.sh 20
```

## PRD Conversion Process

### Step 1: Read the PRD

```bash
cat tasks/prd-[feature-name].md
```

### Step 2: Extract Information

Parse the PRD to extract:
- **Project name** - From `# PRD: [Name]` title
- **Description** - From `## Overview` section
- **Project Context** - From `## Project Context` if present
- **User stories** with:
  - ID (US-001, US-002, etc.)
  - Title
  - Description (As a... I want... So that...)
  - Acceptance criteria (bullet points)
  - Priority

### Step 3: Generate prd.json

```json
{
  "project": "[Feature Name]",
  "branchName": "ralph/[feature-slug]",
  "description": "[Overview text]",
  "createdAt": "[Today's date]",
  "projectContext": {
    "name": "[Project name from PROJECT_SPEC.md]",
    "language": "[typescript/python/go]",
    "framework": "[react/express/fastapi]",
    "hasTypes": true,
    "testFramework": "[vitest/pytest]"
  },
  "existingPatterns": {
    "moduleSystem": "[ES modules/CommonJS]",
    "testFramework": "[vitest/jest/pytest]",
    "linter": "[eslint/biome/ruff]"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "[Full story description]",
      "acceptanceCriteria": [
        "[Criterion 1]",
        "[Criterion 2]"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Step 4: Archive Previous PRD

If prd.json already exists:

```bash
mkdir -p archive/$(date +%Y-%m-%d)
cp prd.json archive/$(date +%Y-%m-%d)/prd-backup.json
cp progress.txt archive/$(date +%Y-%m-%d)/progress-backup.txt 2>/dev/null
```

### Step 5: Initialize Progress

Create fresh progress.txt:

```markdown
# Progress Log - ralph/[feature-slug]

Started: [Date]
Feature: [Feature description]

## Project Context
[From PROJECT_SPEC.md if available]

## Codebase Patterns
[Patterns from analysis or PROJECT_SPEC.md]

## Quality Commands
```bash
[typecheck command]
[lint command]
[test command]
```

---

```

## Story Conversion Rules

### 1. Story Sizing

If a PRD story is too large, split it:
- Data model → separate story
- Backend logic → separate story
- API endpoint → separate story
- UI component → separate story
- Tests → integrated into each story

### 2. Priority Assignment

Assign priorities based on dependencies:

| Priority | Category | Examples |
|----------|----------|----------|
| 1 | Foundation | Schema, types, interfaces |
| 2 | Core Logic | Services, business logic |
| 3 | API/Backend | Routes, controllers, middleware |
| 4 | UI Components | Forms, displays, interactions |
| 5 | Polish | Optimization, edge cases, docs |

### 3. Required Acceptance Criteria

Always ensure these criteria exist based on tech stack:

**TypeScript/JavaScript:**
- "TypeScript compiles without errors" or "No type errors"
- "ESLint/Biome passes"
- "Tests pass"

**Python:**
- "Type hints complete"
- "Ruff/Pylint passes"
- "Pytest passes"

**Go:**
- "`go build` succeeds"
- "`golangci-lint` passes"
- "`go test ./...` passes"

**For specific story types:**
- UI stories: "Verify in browser", "Accessible"
- API stories: "Response format correct", "Error handling complete"
- Auth stories: "Security best practices followed"

### 4. Branch Naming

Convert feature name to slug:
- "User Authentication" → `ralph/user-authentication`
- "Dark Mode Toggle" → `ralph/dark-mode-toggle`
- Use lowercase, replace spaces with hyphens
- Max 30 characters

## Output Format

After conversion:

```
=== PRD Converted ===

Project: [Feature Name]
Branch: ralph/[feature-slug]
Stories: [N] total

Story Summary:
  1. US-001: [Title] (Priority 1) - Foundation
  2. US-002: [Title] (Priority 2) - Core logic
  3. US-003: [Title] (Priority 3) - API
  ...

Files Created/Updated:
  - prd.json
  - progress.txt

Next Steps:
  1. Review prd.json for accuracy
  2. Create branch: git checkout -b ralph/[feature-slug]
  3. Start RALPH: ./scripts/ralph/ralph.sh 20
```

## Example Conversion

**Input** (`tasks/prd-user-auth.md`):
```markdown
# PRD: User Authentication

## Overview
Add user authentication with email/password login.

## User Stories

### US-001: Create user model
**As a** developer
**I want** a User model with proper types
**So that** I can store user data securely

**Acceptance Criteria:**
- [ ] User interface with id, email, passwordHash
- [ ] Validation for email format
- [ ] TypeScript compiles

**Priority:** 1
```

**Output** (`prd.json`):
```json
{
  "project": "User Authentication",
  "branchName": "ralph/user-auth",
  "description": "Add user authentication with email/password login.",
  "createdAt": "2026-01-22",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create user model",
      "description": "As a developer, I want a User model with proper types so that I can store user data securely",
      "acceptanceCriteria": [
        "User interface with id, email, passwordHash",
        "Validation for email format",
        "TypeScript compiles"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Integration with RALPH

After prd.json is created:

1. **Create feature branch:**
   ```bash
   git checkout -b ralph/[feature-slug]
   ```

2. **Start RALPH:**
   ```bash
   ./scripts/ralph/ralph.sh 20
   ```

3. **Monitor progress:**
   ```bash
   tail -f progress.txt
   cat prd.json | jq '.userStories[] | {id, title, passes}'
   ```

4. **When complete:**
   ```bash
   git log --oneline
   # Review changes, create PR
   ```
