---
name: ralph-plan
description: Generate a structured PRD with user stories from requirements. Creates prd.json and initializes progress tracking for autonomous development with /ralph-execute.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, AskUserQuestion
user_invocable: true
argument-hint: <requirements> [--branch NAME] [--max-stories N]
---

# Ralph Planning Skill

Generate a Product Requirements Document (PRD) with prioritized user stories from requirements. This prepares a project for autonomous iterative development with `/ralph-execute`.

## Invocation

```
/ralph-plan <requirements> [options]
```

**Arguments:**
- `<requirements>` - Feature description (inline text, file path, or URL)
- `--branch NAME` - Branch name (default: auto-generated with `ralph/` prefix)
- `--max-stories N` - Maximum stories to generate (default: 10)

**Examples:**
```bash
/ralph-plan "Build a user authentication system with login and registration"
/ralph-plan ./requirements.md --branch ralph/auth-system
/ralph-plan --max-stories 15
```

## Execution Flow

### Phase 1: Gather Requirements

#### Step 1.1: Parse Input

If `<requirements>` is:
- **File path**: Read the file contents
- **URL**: Fetch and extract requirements
- **Inline text**: Use directly
- **Not provided**: Ask the user what feature they want to build

#### Step 1.2: Analyze Codebase Context

Before generating stories, understand the existing codebase:

```bash
# Identify project type and structure
ls -la
cat package.json 2>/dev/null
```

Look for:
- Existing patterns in the codebase
- UI component library in use
- State management approach
- Testing patterns
- Routing solution

#### Step 1.3: Identify Quality Gate Commands

Read `package.json` scripts section and determine available commands:

| Check | Preferred Command | Fallback |
|-------|-------------------|----------|
| TypeScript | `npm run check` or `npm run typecheck` | `npx tsc --noEmit` |
| Lint | `npm run lint` | `npx eslint .` |
| Test | `npm run test` | Skip if not configured |
| Build | `npm run build` | Skip (optional gate) |

### Phase 2: Ask Clarifying Questions

**CRITICAL**: Before generating stories, ask 3-5 clarifying questions with lettered options.

Use the AskUserQuestion tool to get clarity on:
1. Scope and approach decisions
2. UI/UX preferences
3. Technical constraints
4. Priority trade-offs

**Example Questions:**
```
Before I generate stories, I need to clarify a few things:

1. Authentication approach:
   A) Email/password only
   B) OAuth (Google, GitHub)
   C) Magic links
   D) All of the above

2. UI framework preference:
   A) Use existing component library
   B) Build from scratch
   C) Mix of both

3. Error handling:
   A) Toast notifications
   B) Inline error messages
   C) Both

Please respond like "1A, 2A, 3C" with your choices.
```

### Phase 3: Generate PRD

#### Step 3.1: Create User Stories

Transform requirements into atomic, testable user stories following these rules:

**Story Sizing Rules:**
- ✅ Add database column with default value
- ✅ Create single UI component
- ✅ Add one API endpoint
- ✅ Add form validation
- ❌ Build entire dashboard (too big - split into schema, queries, components, filters)
- ❌ Complete authentication system (too big - split into login, register, reset, session)

**Each story MUST fit in one context window (~5-15 minutes implementation)**

**Story Template:**
```json
{
  "id": "US-001",
  "title": "Brief action-oriented title (max 80 chars)",
  "description": "As a [user], I want [capability] so that [benefit]. Implementation should [specific guidance].",
  "acceptanceCriteria": [
    "Component renders without errors",
    "TypeScript compiles with no errors",
    "Follows existing patterns in src/components/",
    "Verify in browser using visual-polish-inspector"  // For UI stories
  ],
  "priority": 1,
  "status": "pending",
  "failureCount": 0,
  "requiresBrowserVerification": true  // true for UI stories
}
```

#### Step 3.2: Order Stories by Dependency

Stories MUST be ordered so earlier ones don't depend on later ones:

1. **Foundation** - Types, schemas, context providers, utilities
2. **Backend** - API routes, server actions, database changes
3. **Components** - UI components that depend on backend
4. **Pages/Views** - Pages that compose components
5. **Integration** - Final wiring, polish, edge cases

#### Step 3.3: Write prd.json

Create `.ralph/` directory and write the PRD:

```bash
mkdir -p .ralph
```

Write to `.ralph/prd.json`:

```json
{
  "projectName": "[Extracted from requirements]",
  "branchName": "ralph/[feature-slug]",
  "createdAt": "[ISO timestamp]",
  "updatedAt": "[ISO timestamp]",
  "qualityGates": {
    "typecheck": "npm run check",
    "lint": "npm run lint",
    "test": null,
    "build": null
  },
  "config": {
    "maxIterations": 10,
    "maxFailuresPerStory": 3,
    "autoCommit": true
  },
  "userStories": [...],
  "summary": {
    "totalStories": N,
    "passed": 0,
    "blocked": 0,
    "pending": N,
    "iterationsRun": 0
  }
}
```

### Phase 4: Initialize Tracking

#### Step 4.1: Initialize progress.txt

Write header to `.ralph/progress.txt`:

```
================================================================================
RALPH PROGRESS LOG - [Project Name]
Branch: [branch-name]
Started: [ISO timestamp]
================================================================================

--- CODEBASE PATTERNS (Consolidated) ---
// This section is updated after each iteration
// Reusable patterns also go to AGENTS.md

[Initial patterns discovered during analysis]

================================================================================
```

#### Step 4.2: Create/Switch to Feature Branch

```bash
git checkout -b [branch-name] 2>/dev/null || git checkout [branch-name]
```

### Phase 5: Present Summary

Display the generated PRD summary:

```
RALPH PRD GENERATED
━━━━━━━━━━━━━━━━━━━

Project: [Name]
Branch: [branch-name]
Stories: [N] user stories

Priority Order:
1. US-001: [Title]
2. US-002: [Title]
...

Quality Gates:
✓ TypeScript: npm run check
✓ Lint: npm run lint
○ Test: not configured
○ Build: disabled

Files Created:
- .ralph/prd.json
- .ralph/progress.txt

Next Step:
Run `/ralph-execute` to begin autonomous development.
Run `/ralph-execute --dry-run` to preview the first story.
```

## Error Handling

| Error | Action |
|-------|--------|
| Cannot parse requirements | Ask user to clarify or provide structured input |
| No package.json found | Ask about project type, suggest manual quality gate config |
| Branch already exists | Ask to reuse or create new name |
| .ralph/ already exists | Ask to overwrite, append stories, or abort |

## Quality Checklist

Before completing, verify:
- [ ] Asked 3-5 clarifying questions
- [ ] Stories are small enough (1-3 files each)
- [ ] Stories are ordered by dependency
- [ ] Each story has testable acceptance criteria
- [ ] UI stories include browser verification requirement
- [ ] Quality gates are configured correctly
- [ ] Feature branch created/checked out

## Anti-Patterns to Avoid

1. **Vague acceptance criteria** - "Works correctly" is NOT acceptable
2. **Oversized stories** - If it touches >3 files, split it
3. **Missing dependencies** - Story 5 can't depend on Story 10
4. **Skipping questions** - Always ask clarifying questions
5. **Generic descriptions** - Be specific about implementation approach

## Output Files

After successful execution:
1. `.ralph/prd.json` - Complete PRD with stories
2. `.ralph/progress.txt` - Initialized log with codebase analysis
3. Git branch created/checked out
