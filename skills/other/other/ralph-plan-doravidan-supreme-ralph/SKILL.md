---
name: ralph-plan
description: Decompose PRD stories into implementation subtasks using the Planner agent
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, TodoWrite
---

# RALPH-PLAN - Strategic Implementation Planning

Decompose PRD user stories into detailed, ordered implementation subtasks.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-plan` | Generate implementation plan from prd.json |
| `/ralph-plan US-001` | Plan specific story only |
| `/ralph-plan --refresh` | Regenerate plan for incomplete stories |

## Triggers

- `/ralph-plan`
- "plan the implementation"
- "create subtasks"
- "break down the PRD"

## Prerequisites

Before planning, verify:

```bash
# Check for PRD
if [ -f prd.json ]; then
  echo "✓ Found prd.json"
  TOTAL=$(cat prd.json | jq '.userStories | length')
  REMAINING=$(cat prd.json | jq '[.userStories[] | select(.passes == false)] | length')
  echo "  $REMAINING/$TOTAL stories need planning"
else
  echo "❌ No prd.json found"
  echo "Run /prd [feature] first to create a PRD"
  exit 1
fi

# Check for project context
[ -f PROJECT_SPEC.md ] && echo "✓ Found PROJECT_SPEC.md"
[ -f CLAUDE.md ] && echo "✓ Found CLAUDE.md"
[ -d .ralph/memory ] && echo "✓ Found memory layer"
```

## Planning Process

### Step 1: Load Context

Read all relevant context:

1. **PRD** - User stories and acceptance criteria
2. **PROJECT_SPEC.md** - Tech stack, patterns, conventions
3. **CLAUDE.md** - Project-specific rules
4. **Memory** - Past implementations and learnings

```bash
# Read PRD
cat prd.json

# Read project patterns
cat PROJECT_SPEC.md 2>/dev/null || echo "No PROJECT_SPEC.md"

# Read memory insights
cat .ralph/memory/insights.json 2>/dev/null || echo "No prior insights"
```

### Step 2: Analyze Each Story

For each incomplete story, determine:

1. **Scope** - What files need to change?
2. **Dependencies** - What must exist first?
3. **Complexity** - How many subtasks needed?
4. **Risks** - What could go wrong?

### Step 3: Decompose Into Subtasks

Break each story into atomic subtasks:

**Subtask Guidelines:**
- ONE clear outcome per subtask
- 15-30 minutes of work each
- Clear file scope (which files to modify/create)
- Testable acceptance criteria
- Explicit dependencies

**Subtask Schema:**
```json
{
  "id": "ST-001-1",
  "storyId": "US-001",
  "title": "Create User type definitions",
  "description": "Define TypeScript interfaces for User entity",
  "files_to_create": ["src/types/user.ts"],
  "files_to_modify": ["src/types/index.ts"],
  "dependencies": [],
  "acceptance_criteria": [
    "User interface with id, email, createdAt",
    "Type exported from index.ts",
    "Typecheck passes"
  ],
  "estimated_complexity": "low",
  "parallelizable": true
}
```

### Step 4: Build Dependency Graph

Map which subtasks can run in parallel vs sequentially:

```
US-001 Subtasks:
  ST-001-1 (types) ──┬── ST-001-3 (service) ── ST-001-5 (API)
  ST-001-2 (schema) ─┘        │
                              └── ST-001-4 (tests)
```

**Parallel:** ST-001-1 and ST-001-2 (no dependencies)
**Sequential:** ST-001-3 depends on both 1 and 2

### Step 5: Identify Risks

For each story, note:

```json
{
  "storyId": "US-001",
  "risks": [
    {
      "type": "integration",
      "description": "Database schema may conflict with existing tables",
      "mitigation": "Check existing migrations first"
    }
  ]
}
```

### Step 6: Clarify Ambiguities

**CRITICAL:** If anything is unclear, use AskUserQuestion:

```
? The PRD mentions "secure password storage" but doesn't specify the algorithm.
  ○ bcrypt (Recommended)
  ○ argon2
  ○ scrypt
  ○ Let me specify
```

### Step 7: Output Implementation Plan

Write to `implementation_plan.json`:

```json
{
  "prdVersion": "1.0.0",
  "planVersion": "1.0.0",
  "generatedAt": "2026-01-25T10:00:00Z",
  "complexity": "STANDARD",
  "summary": {
    "totalStories": 6,
    "totalSubtasks": 24,
    "parallelizable": 8,
    "sequential": 16,
    "estimatedIterations": 16
  },
  "stories": [
    {
      "storyId": "US-001",
      "title": "Create User model and types",
      "subtasks": [
        {
          "id": "ST-001-1",
          "title": "Create User type definitions",
          "description": "Define TypeScript interfaces",
          "files_to_create": ["src/types/user.ts"],
          "files_to_modify": ["src/types/index.ts"],
          "dependencies": [],
          "acceptance_criteria": ["..."],
          "estimated_complexity": "low",
          "parallelizable": true
        }
      ],
      "execution_order": {
        "parallel_batch_1": ["ST-001-1", "ST-001-2"],
        "sequential": ["ST-001-3", "ST-001-4", "ST-001-5"]
      },
      "risks": []
    }
  ],
  "global_risks": [],
  "clarifications": []
}
```

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                 Implementation Plan Generated                   ║
╚════════════════════════════════════════════════════════════════╝

PRD: User Authentication System
Complexity: STANDARD

Stories: 6
Subtasks: 24 total
  - Parallelizable: 8 (can run concurrently)
  - Sequential: 16 (have dependencies)

Estimated iterations: 16

Story Breakdown:
  US-001: Create User model (4 subtasks)
  US-002: Password hashing (3 subtasks)
  US-003: JWT utilities (5 subtasks)
  US-004: Auth routes (4 subtasks)
  US-005: Auth middleware (4 subtasks)
  US-006: Session management (4 subtasks)

Risks Identified: 2
  [MEDIUM] Database migration conflicts
  [LOW] JWT secret rotation

Plan saved to: implementation_plan.json

Next: Run /ralph-run to start implementation
```

## Guidelines

1. **NEVER implement** - Only plan, let Coder agent implement
2. **ASK when unclear** - Use AskUserQuestion for ambiguities
3. **RESPECT patterns** - Plans must follow PROJECT_SPEC.md
4. **THINK dependencies** - Order subtasks correctly
5. **KEEP atomic** - One clear outcome per subtask
6. **LOG insights** - Save planning learnings to memory

## Error Handling

| Error | Action |
|-------|--------|
| No PRD found | Direct to `/prd [feature]` |
| Unclear requirements | Use AskUserQuestion |
| Missing PROJECT_SPEC | Warn but continue with defaults |
| Conflicting dependencies | Flag for user review |
