---
name: ralph
description: Run RALPH autonomous development loop. Converts PRD markdown to prd.json and runs autonomous implementation.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Ralph Skill

Convert PRD Markdown files to prd.json format for RALPH automation.

## Trigger

This skill activates when the user asks to:
- Convert a PRD to JSON
- Prepare a PRD for RALPH
- Create prd.json from a PRD file

## Process

### Step 1: Read the PRD

Read the specified PRD Markdown file:

```bash
cat tasks/prd-[feature-name].md
```

### Step 2: Extract Information

Parse the PRD to extract:
- Project name (from title)
- Description (from overview)
- User stories with:
  - ID (US-001, US-002, etc.)
  - Title
  - Description (As a... I want... So that...)
  - Acceptance criteria
  - Priority

### Step 3: Generate prd.json

Create the JSON structure:

```json
{
  "project": "[Feature Name]",
  "branchName": "ralph/[feature-slug]",
  "description": "[Overview text]",
  "createdAt": "[Today's date]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "[Full story description]",
      "acceptanceCriteria": [
        "[Criterion 1]",
        "[Criterion 2]",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Step 4: Validate and Save

Before saving, validate:
1. Every story has "Typecheck passes" in criteria
2. Stories are ordered by priority (dependencies first)
3. Each story is small enough for one iteration
4. Branch name follows `ralph/[feature-slug]` format

Archive previous prd.json if it exists:

```bash
if [ -f prd.json ]; then
  mkdir -p archive/$(date +%Y-%m-%d)
  cp prd.json archive/$(date +%Y-%m-%d)/
  cp progress.txt archive/$(date +%Y-%m-%d)/ 2>/dev/null || true
fi
```

Save the new prd.json:

```bash
cat > prd.json << 'EOF'
[JSON content]
EOF
```

Reset progress.txt for new feature:

```bash
cat > progress.txt << 'EOF'
# Progress Log - ralph/[feature-slug]

## Codebase Patterns
(Patterns will be added as they are discovered)

---

EOF
```

## Rules for Story Conversion

### 1. Story Sizing
If a PRD story is too large, split it:
- Data model → separate story
- Backend logic → separate story
- API endpoint → separate story
- UI component → separate story
- Tests → integrated into each story

### 2. Priority Assignment
Assign priorities based on dependencies:
- Priority 1: Schema/data models (foundation)
- Priority 2: Core business logic
- Priority 3: API/backend endpoints
- Priority 4: UI components
- Priority 5: Polish/optimization

### 3. Required Criteria
Always ensure these criteria exist:
- All stories: "Typecheck passes"
- Backend stories: "Tests pass"
- UI stories: "Verify in browser"
- API stories: "Response format is correct"

### 4. Branch Naming
Convert feature name to slug:
- "User Authentication" → `ralph/user-authentication`
- "Dark Mode Toggle" → `ralph/dark-mode-toggle`
- Use lowercase, replace spaces with hyphens

## Output

After conversion:

```
Converted PRD to prd.json

Summary:
- Project: [Feature Name]
- Branch: ralph/[feature-slug]
- Stories: [N] total

Stories:
1. US-001: [Title] (Priority 1)
2. US-002: [Title] (Priority 2)
...

Next steps:
1. Review prd.json for accuracy
2. Start RALPH: ./scripts/ralph/ralph.sh 20
3. Monitor progress in progress.txt
```

## Example Conversion

Input (`tasks/prd-dark-mode.md`):
```markdown
# PRD: Dark Mode Toggle

## Overview
Add a dark mode toggle to the application settings.

## User Stories

### US-001: Create theme context
**As a** developer
**I want** a theme context provider
**So that** components can access the current theme

**Acceptance Criteria:**
- [ ] ThemeContext created with light/dark values
- [ ] ThemeProvider wraps the app
- [ ] useTheme hook exported
- [ ] Typecheck passes
```

Output (`prd.json`):
```json
{
  "project": "Dark Mode Toggle",
  "branchName": "ralph/dark-mode-toggle",
  "description": "Add a dark mode toggle to the application settings.",
  "createdAt": "2026-01-19",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create theme context",
      "description": "As a developer, I want a theme context provider so that components can access the current theme",
      "acceptanceCriteria": [
        "ThemeContext created with light/dark values",
        "ThemeProvider wraps the app",
        "useTheme hook exported",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```
