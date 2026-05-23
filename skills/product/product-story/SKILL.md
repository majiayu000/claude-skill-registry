---
name: product-story
description: Generates user stories, spikes, and bugs from a PRD or questions. Plans the stories, refines them one by one with the user, and creates them directly in Linear. Use when you need to break down requirements into stories, create backlog items, or when the user mentions "user story", "spike", "bug", "story", "backlog".
---

# Story Writer - Linear Story Generator

This skill generates user stories, spikes, and bugs from a PRD (or questions), validates the plan with the user, and then refines and creates each story directly in Linear.

## Core Principles

1. **INVEST** - Stories must be Independent, Negotiable, Valuable, Estimable, Small, Testable.
2. **Rule-oriented criteria** - Checklist format, not Given/When/Then.
3. **One story at a time** - Refine and validate before creating.
4. **Search before creating** - Avoid duplicates in Linear.
5. **Spike for uncertainty** - When there is high technical risk, spike first.

---

## Conversation Flow (4 Phases)

### Phase 1: Data Input

**1.1 Ask for the source:**

> "Do you have a PRD for this feature?"

- **If yes**: Read the PRD file, extract requirements from sections P0/P1/P2.
- **If no**: Ask discovery questions:
- What problem are we solving?
- Who is the user?
- What functionalities are required?

**1.2 Identify the squad:**

> "Which squad? (app-mobile / gabriel-os / integrations)"

**1.3 Identify the Linear project:**

> "Is there a project in Linear to link these stories to?"

- If mentioned, use that project.
- If not mentioned, search for related projects in Linear:
- Use `mcp__linear__list_projects` with a query for the feature name.
- **Exclude projects with state Completed or Cancelled.**
- Show options found to the user.

- **If no project is found**, proceed without a project but warn the user:
  > "I couldn't find a related project. I can create the stories without a project, but I recommend creating one in Linear to better organize the work. Do you want to continue anyway?"

---

### Phase 2: Story Planning

**2.1 Analyze requirements and generate a story map:**

- List all proposed stories with type (User Story / Spike / Bug).
- Apply the INVEST principle—break large requirements into smaller stories.
- Identify dependencies between stories.
- Suggest spikes for areas of technical uncertainty.

**2.2 Present the plan to the user:**

```
📋 Story Plan for [Feature]:

1. [Spike] Investigate technical feasibility - evaluate API/integration
2. [US] Main functionality - brief description
3. [US] User visual feedback - brief description
4. [US] Error handling - brief description
5. [Bug] Fix known issue - brief description

Does this make sense? Would you like to add, remove, or adjust anything?

```

**2.3 Wait for user validation before proceeding.**

---

### Phase 3: Story Refinement (One by One)

For each story in the plan:

**3.1 Search Linear for similar stories:**

- Use `mcp__linear__list_issues` with a query.
- **Exclude issues with status type Completed or Cancelled.**
- If a similar one is found, ask:
  > "I found a similar issue: '[title]'. Do you want to use the existing one or create a new one?"

**3.2 Search Slack for context:**

- Search for messages related to the story topic.
- Find discussions, decisions, and feedback that enrich the understanding.
- Show relevant findings to the user before generating.

**3.3 Ask the user for more context:**

> "Let's refine the story '[title]'. The more context you can provide, the better the story will be."

Ask according to the type:

- **For User Story**: specific scenarios, edge cases, integrations, expected behaviors.
- **For Spike**: hypotheses to validate, known risks, considered approaches.
- **For Bug**: logs, screenshots, frequency of occurrence, impact on the user.

**3.4 Generate content using the appropriate template:**

> **IMPORTANT**: Templates are the source of truth. Always read them dynamically to get the most current structure.

- **For User Story**: Read and follow `templates/user-story.md`.
- **For Spike**: Read and follow `templates/spike.md`.
- **For Bug**: Read and follow `templates/bug.md`.

**3.5 Show to user for refinement:**

- Present the generated content.
- Ask:
  > "Anything to adjust before creating in Linear?"

**3.6 Create in Linear after approval:**

- Use `mcp__linear__create_issue`.
- Configure:
- **title**: story title.
- **description**: full content in markdown.
- **team**: squad identified in Phase 1.
- **project**: project ID (if available).
- **state**: "Refinamento Geral" (this is the status name).
- **labels**: add if any existing label makes sense.

- To check available labels, use `mcp__linear__list_issue_labels`.
- Show the link to the created issue to the user.

**3.7 Move to the next story in the plan.**

---

### Phase 4: Final Summary

After creating all stories:

**4.1 Show a summary of all created issues with Linear links:**

```
✅ Stories created successfully!

| # | Type  | Title           | Link            |
|---|-------|-----------------|-----------------|
| 1 | Spike | Investigate API | [INT-123](link) |
| 2 | US    | Video upload    | [INT-124](link) |
| 3 | US    | Video preview   | [INT-125](link) |

```

**4.2 Suggest next steps:**

- Schedule refinement with the squad.
- Prioritize in the backlog.
- Assign owners.

---

## Linear Integration

### Search for similar issues

```
mcp__linear__list_issues with:
- query: title keywords
- team: squad team
- includeArchived: false
- Filter: exclude status type "Completed" or "Cancelled"

```

### Search for related projects

```
mcp__linear__list_projects with:
- query: feature name
- team: squad team
- Filter: exclude state "Completed" or "Cancelled"

```

### Create issue

```
mcp__linear__create_issue with:
- title: story title
- description: full content (markdown)
- team: squad team
- project: project ID (if available)
- state: "Refinamento Geral"
- labels: [if applicable]

```

### Get available labels

```
mcp__linear__list_issue_labels with:
- team: squad team

```

---

## Slack Integration

### Search context

- Search for messages related to the story topic.
- Find discussions, decisions, and user feedback.
- Enrich problem understanding with real conversations.

---

## Activation Examples

The user can start with:

- "I want to create the stories for the [feature] PRD."
- "Help me break this PRD down into user stories."
- "I need to create stories for [functionality]."
- "Let's create the stories for [feature]."
- "I have a bug to report about [problem]."
- "I need to create a spike to investigate [uncertainty]."

---

## Tips for the PM

- **More context is better** - Provide details about scenarios, edge cases, and integrations.
- **Don't skip planning** - Validate the story map before refining.
- **Spikes first** - If there is technical uncertainty, create a spike before user stories.
- **One story at a time** - Refine and approve each story before moving forward.
- **Review templates** - The templates in `templates/` are the source of truth.

---

**Story Writer skill is ready. Would you like to translate another one or start a story planning session?**
