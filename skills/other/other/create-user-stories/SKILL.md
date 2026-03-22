---
name: create-user-stories
description: Generate user story map with BDD acceptance criteria when the user asks to create user stories, write stories, or break down a feature into stories
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature name or path to PRD]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: product, user-stories, requirements
---

# Create User Stories

## Overview

Generate a user story map following Jeff Patton's story mapping approach, with BDD-style Given/When/Then acceptance criteria for every story. Stories are grouped by user activity, tagged with priority and complexity, and include dedicated edge-case stories.

## Workflow

1. **Read product context** — Load `.chalk/docs/product/0_product_profile.md` and any JTBD docs to understand personas, goals, and existing terminology. If no product context exists, work from what the user provides.

2. **Locate the PRD** — If `$ARGUMENTS` references a PRD (by path or name), read it. Search `.chalk/docs/product/` for PRD files matching the feature. If a PRD exists, it is the primary input. If no PRD exists, accept the feature description from `$ARGUMENTS` directly and note that stories are being written without a PRD.

3. **Identify user activities** — Break the feature into 3-7 high-level user activities (the "backbone" in story mapping). Each activity represents a distinct thing the user does to accomplish their goal. Activities are ordered left-to-right by the sequence the user would perform them.

4. **Write stories for each activity** — Under each activity, write stories from highest to lowest priority. Each story gets:
   - The story statement: "As a [persona], I want [action], so that [outcome]"
   - 2-4 acceptance criteria in Given/When/Then format
   - A priority tag: must (MVP), should (important but not blocking), could (nice-to-have)
   - A complexity tag: S (< 1 day), M (1-3 days), L (3-5 days)

5. **Generate edge-case stories** — For every activity, add at least one story covering:
   - Error states (what happens when things go wrong)
   - Empty states (first-time use, no data available)
   - Boundary conditions (max limits, large inputs, concurrent access)
   - Permission boundaries (unauthorized user, expired session, role restrictions)

6. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

7. **Write the file** — Save to `.chalk/docs/product/<n>_user_stories_<feature_slug>.md`.

8. **Confirm** — Tell the user the stories were created, share the file path, total story count, and the must/should/could breakdown.

## Story Map Structure

```markdown
# User Stories: <Feature Name>

Last updated: <YYYY-MM-DD> (Initial draft)

Source PRD: [<PRD title>](./<prd_filename>.md) (or "None — stories written from feature description")

## Story Map Overview

| Activity | Must | Should | Could | Total |
|----------|------|--------|-------|-------|
| <activity 1> | X | Y | Z | N |
| <activity 2> | X | Y | Z | N |
| **Total** | **X** | **Y** | **Z** | **N** |

---

## Activity 1: <Activity Name>

<1-sentence description of what the user is doing and why>

### Story 1.1: <Short story title>

**Priority**: must | **Complexity**: S/M/L

As a [persona], I want [action], so that [outcome].

**Acceptance Criteria**:
- Given [context], when [action], then [expected result]
- Given [context], when [action], then [expected result]
- Given [context], when [action], then [expected result]

### Story 1.2: <Short story title>

...

### Story 1.E1: <Edge case title>

**Priority**: must | **Complexity**: S/M/L
**Edge case type**: error state | empty state | boundary | permission

As a [persona], I want [behavior when X goes wrong], so that [I can recover / understand what happened].

**Acceptance Criteria**:
- Given [error/edge context], when [action], then [graceful handling]
- Given [error/edge context], when [action], then [user feedback]

---

## Activity 2: <Activity Name>

...
```

## Writing Stories

### The Story Statement

Each story has three parts that must all be present:

- **As a [persona]**: Use a specific persona from the product profile, not "a user." If no personas exist, define them inline (e.g., "As a first-time customer who has never used the product").
- **I want [action]**: Describe the action from the user's perspective. "I want to filter search results" not "I want the system to implement filtering."
- **So that [outcome]**: State the user value, not the system behavior. "So that I can find the right item without scrolling through hundreds of results" not "so that the filter query runs on the backend."

### Acceptance Criteria

Every criterion follows Given/When/Then strictly:

- **Given** [a specific, reproducible starting state]
- **When** [a single user action]
- **Then** [an observable, verifiable outcome]

Good: "Given a user with 50+ saved items, when they type 3 characters in the search field, then matching items appear within 500ms and non-matching items are hidden."

Bad: "Given the user is on the page, when they search, then it works correctly."

### Priority Tags

| Tag | Meaning | Guidance |
|-----|---------|----------|
| must | MVP — feature does not ship without this | Core happy path, critical error handling |
| should | Important but not launch-blocking | Secondary workflows, polish, non-critical edge cases |
| could | Nice-to-have, do if time permits | Convenience features, optimizations, advanced scenarios |

### Complexity Tags

| Tag | Meaning | Guidance |
|-----|---------|----------|
| S | Less than 1 day of engineering work | Single component, no new APIs, no data model changes |
| M | 1-3 days of engineering work | Multiple components, may need a new API endpoint or schema change |
| L | 3-5 days of engineering work | Cross-cutting, new infrastructure, significant data model changes |

If a story is larger than L, it should be split into smaller stories.

## Output

- **File**: `.chalk/docs/product/<n>_user_stories_<feature_slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# User Stories: <Feature Name>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Stories without acceptance criteria** — A story with no Given/When/Then is just a sentence. It cannot be estimated, tested, or verified. Every story gets 2-4 criteria, no exceptions.
- **Missing edge-case stories** — Happy-path-only story maps lead to brittle products. Every activity must have at least one edge-case story covering error states, empty states, boundaries, or permissions.
- **Acceptance criteria that are not testable** — "The experience should be smooth" cannot be verified. Every criterion must be specific enough that a QA engineer can write a test case from it without asking questions.
- **Stories that are really tasks** — "As a developer, I want to set up the database schema" is a task, not a user story. Stories describe user-visible value. Implementation tasks belong in engineering plans, not story maps.
- **"As a user" without specificity** — Always use a named persona or a descriptive phrase. "As a user" tells the engineer nothing about who they are building for. "As a warehouse manager checking inventory at end-of-shift" tells them everything.
- **Skipping the story map overview** — The summary table is the first thing a PM or stakeholder reads. It shows scope at a glance: how many stories, how they break down by priority. Never omit it.
- **One giant activity** — If an activity has more than 8 stories, it is too broad. Split it into two activities. Story maps should be scannable.
- **Duplicating the PRD** — Stories operationalize the PRD, they do not restate it. Do not copy-paste problem statements or metrics into the stories doc. Reference the PRD by filename instead.
