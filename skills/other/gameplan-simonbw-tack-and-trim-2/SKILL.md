---
name: gameplan
description: Guides creating detailed execution plans for features, refactors, and code changes. Use when user requests a gameplan, or when user invokes /gameplan.
---

# Gameplan Skill

Create a comprehensive execution plan before implementing significant code changes.

## When to Use

- User explicitly requests a gameplan or invokes `/gameplan`
- Planning a new feature, refactor, or significant code change
- Changes span multiple files or have complex dependencies

## Process

### 1. Understand the Request

Before writing anything, gather context:
- Read the relevant existing code to understand current state
- Identify all files that might be affected
- Ask clarifying questions to eliminate ambiguity

**Ask questions NOW, not later.** The plan must be executable without further clarification.

### 2. Create the Plan File

Create a markdown file in the `plans/` directory named after the feature:
- Use kebab-case: `feature-name.md`
- Examples: `physics-refactor.md`, `auth-system.md`, `performance-optimization.md`

### 3. Required Sections

Every gameplan must include these four sections:

#### Current State
Describe what the codebase looks like now:
- List relevant files with their paths
- Describe the current architecture/approach
- Note any pain points or limitations being addressed

#### Desired Changes
Describe what we want to achieve:
- Clear description of the end goal
- Why this change is being made
- Any constraints or requirements

#### Files to Modify
List every file that needs changes:
```
- `src/path/to/file.ts` - Brief description of changes needed
- `src/another/file.ts` - What will be added/modified/removed
```

Be specific about function names, classes, and line-level changes where possible.

#### Execution Order
Specify what can be done in parallel vs sequentially:

```
## Parallel Work (no dependencies)
- File A and File B can be modified independently

## Sequential Work (has dependencies)
1. First: Create new interfaces in types.ts
2. Then: Update implementations that depend on those interfaces
3. Finally: Update tests
```

## Quality Checklist

Before finalizing the plan, verify:
- [ ] No open questions remain
- [ ] All affected files are listed
- [ ] Current state accurately reflects the code (you read it, not guessed)
- [ ] Execution order accounts for all dependencies
- [ ] Another developer could execute this plan without asking questions
