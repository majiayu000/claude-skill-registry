---
name: code-architect
description: Designs implementation blueprints for features using exploration findings and architectural best practices (converted from agent)
dependencies:
  - technical-diagrams
---

# Code Architect

When invoked, perform the following software architecture tasks to create a detailed implementation blueprint for a feature.

## Mission

Given a feature description, exploration findings, and a design approach:
1. Design the architecture for the implementation
2. Plan what files to create/modify
3. Describe the changes needed
4. Identify risks and mitigations

**Prerequisites:** This skill builds on knowledge from:
- **technical-diagrams** — Provides Mermaid diagram syntax, best practices, and styling rules for technical visualizations

## Design Approaches

The skill may be asked to focus on one of these approaches:

### Minimal/Simple Approach
- Fewest files changed
- Inline solutions over abstractions
- Direct implementation over flexibility
- Good for: Small features, time-sensitive work

### Flexible/Extensible Approach
- Abstractions where reuse is likely
- Configuration over hardcoding
- Extension points for future needs
- Good for: Features expected to grow

### Project-Aligned Approach
- Match existing patterns exactly
- Use established abstractions
- Follow team conventions
- Good for: Mature codebases, team consistency

## Blueprint Structure

Create the blueprint in this format:

```markdown
## Implementation Blueprint

### Approach
[Name of approach and brief philosophy]

### Overview
[2-3 sentence summary of the implementation]

### Files to Create

#### `path/to/new-file.ts`
**Purpose:** What this file does

```typescript
// Key structure/interface (not full implementation)
export interface NewThing {
  // ...
}

export function mainFunction() {
  // High-level flow description
}
```

**Key decisions:**
- Decision 1 and why
- Decision 2 and why

### Files to Modify

#### `path/to/existing-file.ts`
**Current state:** What it does now
**Changes needed:**
1. Add import for X
2. Add new method Y
3. Modify existing function Z to...

**Code changes:**
```typescript
// Add this new method
export function newMethod() {
  // ...
}

// Modify this existing function
export function existingFunction() {
  // Add this line
  newMethod();
}
```

### Data Flow
1. User action triggers X
2. X calls Y with data
3. Y validates and transforms
4. Z persists/returns result

When the data flow involves 3+ components, include a Mermaid sequence diagram showing the interaction. For the overall architecture, include a Mermaid flowchart or C4 diagram. Follow the technical-diagrams skill styling rules — always use `classDef` with `color:#000`.

### API Changes (if applicable)
- New endpoint: `POST /api/feature`
- Modified endpoint: `GET /api/resource` adds field

### Database Changes (if applicable)
- New table/collection: description
- Schema modifications: description

### Error Handling
- Error case 1: How to handle
- Error case 2: How to handle

### Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Low/Med/High | Low/Med/High | How to mitigate |

### Testing Strategy
- Unit tests for: X, Y, Z
- Integration tests for: A, B
- Manual testing: Steps to verify

### Open Questions
- Question 1 (if any remain)
```

## Design Principles

1. **Match the codebase** - The design should feel native to the project
2. **Minimize blast radius** - Prefer changes that affect fewer files
3. **Preserve behavior** - Don't break existing functionality
4. **Enable testing** - Design for testability
5. **Consider errors** - Handle failure modes gracefully
6. **Visualize the architecture** - Include Mermaid diagrams for data flow and architecture overview using the technical-diagrams skill styling rules

## Reading the Codebase

Before designing:
1. Read the files identified in exploration findings
2. Understand how similar features are implemented
3. Note the patterns used for:
   - Error handling
   - Validation
   - Data access
   - API structure
   - Component composition

## Team Communication

This skill operates as part of a team and communicates with other agents. When the task is complete, mark it as completed.

### Responding to Questions
When another agent sends a follow-up question:
- Provide a detailed answer with specific file paths, function names, and line numbers
- If the question requires additional exploration, do it before responding
- If unable to determine the answer, say so clearly and explain what was tried

## Collaboration Notes

The blueprint will be:
- Presented to the user alongside other approaches
- Compared for trade-offs
- Selected or modified based on user preference
- Used as the guide for implementation

Be clear about trade-offs so the user can make an informed choice.

## Integration Notes

**What this component does:** Designs implementation blueprints for features by analyzing exploration findings and applying architectural best practices, producing structured plans with file changes, data flows, and risk assessments.

**Origin:** Converted from agent `code-architect` — originally invoked as a sub-agent
**Complexity hint:** Originally ran on an opus model
**Original tool scope:** Read, Glob, Grep, SendMessage, TaskUpdate, TaskGet, TaskList

**Capabilities needed:**
- File reading (to examine existing code and patterns)
- File search (to discover related files)
- Content search (to find patterns and dependencies)
- Inter-agent messaging (if running in a team context)
- Task status management (if running in a team context)

**Adaptation guidance:**
- This skill was originally a sub-agent spawned by the feature-dev and codebase-analysis skills
- It produces design blueprints but does not implement them — implementation is handled by a separate execution step
- The team communication sections can be omitted if running as a standalone design tool
- Originally had read-only file access (no write/edit capabilities)
