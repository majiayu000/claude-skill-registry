---
name: prd-task-creation
description: |
  Provides PRD format rules, story sizing guidance, quality gates, and templates for generating ralph-tui compatible prd.json files. Load this skill when creating user stories from deltas.
---

# PRD Task Creation Reference

This skill provides the shared knowledge needed to create user stories from deltas for ralph-tui execution.

---

## PRD JSON Schema

The output MUST be a FLAT JSON object with fields at the ROOT level.

### Required Fields

```json
{
  "name": "Project Name",
  "branchName": "ralph/feature-name",
  "description": "Brief summary of what the PRD covers",
  "userStories": [...]
}
```

### User Story Fields

```json
{
  "id": "US-001",
  "title": "DLT-XXX: [Brief description]",
  "description": "As a [role], I want [action] so that [benefit]",
  "acceptanceCriteria": [
    "Specific, verifiable criterion",
    "cd backend && just test passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": "Delta docs, feature refs, ADRs, patterns, complexity",
  "dependsOn": []
}
```

### Schema Anti-Patterns (DO NOT USE)

**WRONG: Wrapper object**
```json
{
  "prd": {
    "name": "...",
    "userStories": [...]
  }
}
```
The "name" and "userStories" fields must be at the ROOT level.

**WRONG: Using "tasks" instead of "userStories"**
```json
{
  "name": "...",
  "tasks": [...]
}
```
The array is called **"userStories"**, not "tasks".

**WRONG: Using "status" instead of "passes"**
```json
{
  "userStories": [{
    "id": "US-001",
    "status": "open"
  }]
}
```
Use `"passes": false` for incomplete stories, `"passes": true` for completed.

**WRONG: Complex nested structures**
```json
{
  "metadata": {...},
  "overview": {...},
  "migration_strategy": {
    "phases": [...]
  }
}
```
Even if deltas describe phases, you MUST flatten into a single "userStories" array.

**CORRECT: Flat structure at root**
```json
{
  "name": "Project Name",
  "branchName": "ralph/feature-name",
  "userStories": [
    {"id": "US-001", "title": "...", "passes": false, "dependsOn": []},
    {"id": "US-002", "title": "...", "passes": false, "dependsOn": ["US-001"]}
  ]
}
```

---

## Story Size Guidelines

**Each story must be completable in ONE ralph-tui iteration (~one agent context window) and deliver ONE atomic unit of value.**

Ralph-tui spawns a fresh agent instance per iteration with no memory of previous work. Stories should be large enough to add value but small enough to maintain context between tasks.

### Just Right (atomic value increments)

- Create a new frontend component with props interface (without parent integration)
- Integrate component into parent component and wire up events
- Implement database migration for new table
- Update ORM model to match new schema
- Implement service function for main use case (defer edge cases)
- Create API endpoint with basic validation
- Update routing configuration for new pages

**Tests are separate stories** that depend on their corresponding implementation stories. This allows implementing all code first, then testing in batch.

### Too Big (split these further)

- "Create component and integrate it" -> Split: Create component, then integrate
- "Backend endpoint + service + tests" -> Split: Service, endpoint, tests (3 separate stories)
- "Migration + model + tests" -> Split: Migration, model, tests (3 separate stories)
- "Full feature implementation" -> Split by layers (DB, backend, UI)

### Too Small (combine these)

- "Add import statement" as separate story
- "Fix typo in variable name" as separate story
- "Add single CSS class" as separate story

### Story Splitting Criteria

Group implementation steps from the delta plan based on:

1. **Single value delivery:** Each story should deliver ONE atomic unit of value
2. **File/Component proximity:** Steps affecting the same file or related components stay together
3. **Layer proximity:** Database changes, backend logic, UI components should be separate stories
4. **Test separation:** Tests are separate stories that depend on implementation stories

### Typical Groupings

- 1-2 implementation steps per story (not 2-4)
- Creating a component (1 story) vs integrating it (another story)
- Service function (1 story) vs endpoint (1 story) vs tests (separate story)
- Migration (1 story) vs model update (1 story) vs tests (separate story)

### Review Story

After all implementation stories for a delta, add a **review story**.

---

## Quality Gates

Commands that must pass for each user story, extracted from CLAUDE.md or project conventions.

### Backend Deltas

- `cd backend && just test` - Run all tests
- `cd backend && just lint` - Run linting (ruff check)
- `cd backend && just typecheck` - Run type checking (ty)

### Frontend Deltas

- `cd frontend && npm test` - Run all tests
- `cd frontend && npm run lint` - Run ESLint
- `cd frontend && npm run typecheck` - Run TypeScript type checking

### Fullstack Deltas

Include both backend and frontend gates as appropriate for each story.

---

## Story Description Format

Stories should have clear descriptions that describe what needs to be done:

### Implementation Stories

Write a clear user story: "As a [role], I want [action] so that [benefit]". The context describes which steps or parts of the delta to implement.

### Review Stories

Write a clear review instruction describing what to review (specs, designs, decisions).

---

## Acceptance Criteria Formatting

### Implementation Stories

Include in order:

1. **Story-specific criteria** from the delta spec and plan (what this story accomplishes)
2. **Quality gates** appended at the end (backend/frontend commands)

The description field should contain the user story.

Example:
```json
{
  "description": "As a user, I want to see a placeholder message when no session exists so that I understand the current state.",
  "acceptanceCriteria": [
    "PlaceholderMessage component created at frontend/src/components/sessions/placeholder-message.tsx",
    "ARIA attributes properly configured (role=\"status\", aria-live=\"polite\")",
    "cd frontend && npm test passes",
    "cd frontend && npm run lint passes",
    "cd frontend && npm run typecheck passes"
  ]
}
```

### Review Stories

Include:

1. **Verification against spec, design, and referenced ADRs/patterns**

The description field should contain clear review instructions.

Example:
```json
{
  "description": "Review the completed DLT-009 implementation against spec, design, and relevant decisions.",
  "acceptanceCriteria": [
    "All acceptance criteria from docs/delta-specs/DLT-009.md verified",
    "Implementation follows docs/delta-designs/DLT-009.md decisions",
    "Code complies with ADR-009 (TanStack Query), ADR-011 (shadcn/ui + Tailwind)"
  ]
}
```

### Good Criteria (verifiable)

- "Add `status` column to tasks table with default 'open'"
- "PlaceholderMessage component created at frontend/src/components/sessions/placeholder-message.tsx"
- "Filter dropdown has options: All, Open, Closed"

### Bad Criteria (vague)

- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

---

## Output Format Template

### Complete Story Object

```json
{
  "id": "US-001",
  "title": "DLT-XXX: [Step description from plan]",
  "description": "As a [role], I want [action] so that [benefit from spec]",
  "acceptanceCriteria": [
    "[Implementation step criteria from plan]",
    "[Acceptance criterion from spec]",
    "cd [backend|frontend] && [test command] passes",
    "cd [backend|frontend] && [lint command] passes",
    "cd [backend|frontend] && [typecheck command] passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": "Delta: DLT-XXX ([complexity]). Steps X-Y from plan. Feature: [path]. ADRs: [list]. Patterns: [list].",
  "dependsOn": []
}
```

### Notes Field Content

Include:
- Delta ID and complexity level
- Which implementation steps from the plan are covered
- Affected feature spec/design paths (from "Detected Impacts")
- Referenced ADRs (from plan's Pre-Implementation Checklist)
- Referenced design patterns (from plan's Pre-Implementation Checklist)

---

## Dependency Ordering

### Correct Order

1. Schema/database changes (no dependencies)
2. Backend logic (depends on schema)
3. UI components (depends on backend)
4. Integration/polish (depends on UI)
5. Review story (depends on all implementation stories)

### dependsOn Array

Use the `dependsOn` array to specify which stories must complete first:

```json
{
  "id": "US-002",
  "title": "Create API endpoints",
  "dependsOn": ["US-001"]
}
```

Ralph-tui will:
- Show US-002 as "blocked" until US-001 completes
- Never select US-002 for execution while US-001 is open
- Include "Prerequisites: US-001" in the prompt when working on US-002

---

## Writing for AI Agents

The JSON will be executed by AI coding agents via ralph-tui. Therefore:

- The description field should contain a clear user story for implementation stories
- The description field should contain clear review instructions for review stories
- Be explicit about file paths in notes (use docs/delta-specs/DLT-XXX.md format)
- Include affected feature specs/designs in notes
- Include referenced ADRs and design patterns in notes
- Reference specific implementation steps in acceptance criteria
- Include acceptance criteria that are verifiable (not vague)
- Set dependsOn correctly based on dependencies, spec requirements, and story ordering
