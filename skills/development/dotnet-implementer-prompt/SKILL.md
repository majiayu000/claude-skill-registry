---
name: dotnet-implementer-prompt
description: Use when dispatching subagents for .NET backend implementation tasks, whether from a plan or ad-hoc work requiring TDD and self-review
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# .NET Implementer Subagent Prompt Guide

## Overview

A pattern and concrete example for dispatching .NET implementer subagents. Ensures every subagent gets complete context, follows TDD, self-reviews, and reports consistently.

**Core principle:** The subagent should never need to read the plan file or guess context -- everything it needs is in the prompt.

## When to Use

- Dispatching a subagent for a .NET backend implementation task from a plan
- Breaking an implementation plan into parallelizable units of work
- Ad-hoc implementation work requiring TDD, self-review, and structured reporting

## When NOT to Use

- Frontend-only tasks (use a frontend implementer template)
- One-off questions or investigations (just ask directly)
- Tasks with no implementation (e.g., pure documentation, plan writing)

## Quick Reference: Required Prompt Sections

| Section | Purpose | Required? |
|---------|---------|-----------|
| Task Description | Full spec text, not references -- subagent cannot read plan files | Yes |
| Context | Architectural layer, dependencies, existing patterns to follow | Yes |
| Working Directory | Absolute path so subagent starts in the right place | Yes |
| TDD Requirement | Link to `saurun:dotnet-tdd` for Red-Green-Refactor cycle | Yes |
| Self-Review | Checklist the subagent runs before reporting back | Yes |
| Report Format | Structured output so the orchestrator can parse results | Yes |

## Common Mistakes

- **Not pasting full task text** -- writing "see task 3 in plan" instead of pasting the actual spec. The subagent cannot read plan files.
- **Vague context** -- saying "you know the project" instead of specifying entity names, existing patterns, and architectural layer.
- **Forgetting working directory** -- subagent starts in wrong directory, wastes cycles figuring out project structure.
- **Not specifying expected test failures** -- if you know what the RED step should look like, tell the subagent so it can verify.
- **Omitting dependencies between tasks** -- not mentioning that Task 2 depends on types introduced in Task 1.

## Prompt Structure

Every dispatch prompt follows this structure. See the concrete example below for how to fill each section.

### 1. Task Description

Paste the full task specification. Never reference a file or task number without the actual text.

### 2. Context

Set the scene: which project, which layer (Domain, Application, Infrastructure, API), what entities and patterns already exist, and any inter-task dependencies.

### 3. Before You Begin

If the task description above is ambiguous or missing acceptance criteria, ask for clarification before starting. Otherwise, proceed immediately.

### 4. Your Job

1. Implement exactly what the task specifies
2. **REQUIRED SUB-SKILL:** Follow `saurun:dotnet-tdd` strictly. No exceptions.
3. Verify implementation works: `dotnet test`
4. Commit your work
5. Self-review (see below)
6. Report back

### 5. Self-Review Checklist

**Completeness:**
- Did I fully implement everything in the spec?
- Did I miss any requirements?
- Are there edge cases I didn't handle?

**Quality:**
- Is this my best work?
- Are names clear and accurate (match what things do, not how they work)?
- Is the code clean and maintainable?

**Discipline:**
- Did I avoid overbuilding (YAGNI)?
- Did I only build what was requested?
- Did I follow existing patterns in the codebase?

**Testing:**
- Did I follow TDD? (test first, watch fail, minimal code, watch pass, refactor)
- Would each test catch a real bug? If not, delete it.
- **REFERENCE:** See `saurun:dotnet-tdd` verification checklist for complete test quality criteria.

If you find issues during self-review, fix them now before reporting.

### 6. Report Format

- What you implemented
- What you tested and test results
- Files changed
- Self-review findings (if any)
- Any issues or concerns

## Template (Quick Copy)

The following shows the prompt structure to pass to the Task tool when dispatching a subagent. This is conceptual prompt structure, not literal tool syntax.

```
Task tool (saurun:backend-implementer):
  description: "Implement [task name]"
  prompt: |
    You are implementing [task name].

    ## Task Description
    [PASTE FULL TASK TEXT HERE - subagent cannot read plan files]

    ## Context
    [Project, bounded context, layer (Domain/Application/Infrastructure/API)]
    [Existing entities, patterns, handlers to follow]
    [Inter-task dependencies if any]

    ## Before You Begin
    If the task description above is ambiguous or missing acceptance criteria,
    ask for clarification before starting. Otherwise, proceed immediately.

    ## Your Job
    1. Implement exactly what the task specifies
    2. **REQUIRED SUB-SKILL:** Follow saurun:dotnet-tdd strictly. No exceptions.
    3. Verify implementation works: `dotnet test`
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: [absolute path to backend root]

    While you work: if you encounter something unexpected or unclear, ask
    questions. Don't guess or make assumptions.

    ## Before Reporting Back: Self-Review
    [Include full self-review checklist from guide]

    ## Report Format
    - What you implemented
    - What you tested and test results
    - Files changed
    - Self-review findings (if any)
    - Any issues or concerns
```

## Concrete Example

Below is a fully filled-in dispatch prompt for a realistic .NET task. Use this as your model.

The following shows the prompt structure to pass to the Task tool when dispatching a subagent. This is conceptual prompt structure, not literal tool syntax.

```
Task tool (saurun:backend-implementer):
  description: "Implement AddItem endpoint for ShoppingList API"
  prompt: |
    You are implementing the AddItem endpoint for the ShoppingList API.

    ## Task Description

    Add a POST endpoint `POST /api/shopping-lists/{listId}/items` that adds an item to
    an existing shopping list. The request body contains `name` (string, required,
    max 200 chars) and `quantity` (int, required, min 1). The endpoint should:
    - Return 201 with the created item (id, name, quantity, addedAt)
    - Return 404 if the shopping list does not exist
    - Return 400 if validation fails (missing name, name too long, quantity < 1)
    - Use the ShoppingList aggregate to enforce invariants (max 50 items per list)
    - Return 409 if adding the item would exceed the 50-item limit

    ## Context

    This is in the ShoppingList bounded context. The domain layer already has a
    `ShoppingList` aggregate with an `Items` collection and a `ShoppingListItem`
    entity. The Application layer has a `IShoppingListRepository` interface.
    Follow the existing pattern from `CreateShoppingListCommandHandler` for the
    command/handler structure. The API layer uses Carter for minimal API endpoints --
    see `CreateShoppingListEndpoint.cs` for the pattern.

    No other tasks depend on this, but this task depends on the ShoppingList
    aggregate already existing (it does).

    ## Before You Begin

    If the task description above is ambiguous or missing acceptance criteria,
    ask for clarification before starting. Otherwise, proceed immediately.

    ## Your Job

    1. Implement exactly what the task specifies
    2. **REQUIRED SUB-SKILL:** Follow saurun:dotnet-tdd strictly. No exceptions.
    3. Verify implementation works: `dotnet test`
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: /Users/dev/repos/shopping-app/backend

    While you work: if you encounter something unexpected or unclear, ask
    questions. Don't guess or make assumptions.

    ## Before Reporting Back: Self-Review

    Review your work with fresh eyes. Ask yourself:

    **Completeness:**
    - Did I fully implement everything in the spec?
    - Did I miss any requirements (404, 400, 409 cases)?
    - Are there edge cases I didn't handle?

    **Quality:**
    - Is this my best work?
    - Are names clear and accurate?
    - Is the code clean and maintainable?

    **Discipline:**
    - Did I avoid overbuilding (YAGNI)?
    - Did I only build what was requested?
    - Did I follow existing patterns (Carter endpoints, CQRS handlers)?

    **Testing:**
    - Did I follow TDD? (test first, watch fail, minimal code, watch pass, refactor)
    - Would each test catch a real bug? If not, delete it.
    - REFERENCE: See saurun:dotnet-tdd verification checklist.

    If you find issues during self-review, fix them now before reporting.

    ## Report Format

    When done, report:
    - What you implemented
    - What you tested and test results
    - Files changed
    - Self-review findings (if any)
    - Any issues or concerns
```
