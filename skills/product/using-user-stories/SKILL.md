---
name: using-user-stories
description: Document and track feature implementation with user stories. Workflow for authoring stories, building features, and marking acceptance criteria as passing.
---

# Working with User Stories

Document and track feature implementation with user stories. Workflow for authoring stories, building features, and marking acceptance criteria as passing.

User stories document what features should do and track implementation status. When AI agents work through user stories systematically, they produce better results and leave a clear trail of what was done.

---

## Workflow

When working on features:

1. **Author/Update**: Create or modify user story features before building
2. **Build & Test**: Implement until tests pass
3. **Mark Passing**: Set `passes: true` when verified

---

## When to Create User Stories

Create user stories when:

- Starting a new feature or flow
- Fixing a bug that should have test coverage
- Implementing requirements from a design or spec
- Breaking down a large feature into testable increments

---

## Writing Effective Steps

Steps should be:

- **Verifiable**: Each step can be checked by running the app or tests
- **Imperative**: Written as commands ("Navigate to", "Click", "Verify")
- **Specific**: Include URLs, button names, expected values

Good:

```json
{
  "description": "User deletes a chat",
  "steps": [
    "Navigate to /chats",
    "Click the menu button on a chat",
    "Click 'Delete' option",
    "Confirm deletion in dialog",
    "Verify chat is removed from list"
  ],
  "passes": false
}
```

Avoid vague steps:

```json
{
  "description": "User deletes a chat",
  "steps": ["Delete a chat", "Check it worked"],
  "passes": false
}
```

---

## Documenting Work Done

When completing a feature:

1. Verify all steps work manually or via tests
2. Update `passes: true` in the user story
3. Commit both the implementation and the updated story

This creates a log of completed work that future agents can reference.

---

## Using with AI Agents

AI agents can read user stories to:

- Understand what features need to be built
- Know the exact acceptance criteria
- Find features that still need work (`passes: false`)
- Log their progress by marking features as passing

For automated agent loops, see the **Ralph Agent Loop** recipe.

---

## Verifying Stories

Run the verification script to check all stories have valid format:

```bash
bun run user-stories:verify
```

This validates:

- All files are valid JSON
- Each feature has required fields
- Steps are non-empty strings
- Shows pass/fail counts per file
