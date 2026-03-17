---
name: add-todo
description: Add a properly formatted TODO item to TODOS.md. Use when you need to capture a new task, bug, or feature request during development.
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# Add TODO Skill

Add a new TODO item to TODOS.md with proper formatting that integrates with `/list-todos` and `/run-todos`.

## Directory Guard

Before starting, check if `TODOS.md` exists in the current working directory.

- If it exists, read it to understand the current structure
- If it does not exist, create it with the standard template (see below)

## TODO Format Reference

TODOs in this system follow a specific format for compatibility with other skills:

### Basic Format

```markdown
- [ ] **[{Priority} / {Effort}]** {Title} — {Brief description}
```

**Components:**

| Component | Format | Examples |
|-----------|--------|----------|
| Checkbox | `- [ ]` (pending) or `- [x]` (done) | `- [ ]` |
| Priority | `P0` (critical), `P1` (high), `P2` (low) | `**[P1 / Medium]**` |
| Effort | `Low`, `Medium`, `High` | `**[P2 / Low]**` |
| Multiplier | Optional `x{N}` (0.5-2.0) | `**[P1 / Medium x1.5]**` |
| Title | Short, actionable description | `Add user authentication` |
| Description | Optional extended description | `— Support OAuth and email/password` |

### Tags

| Tag | Meaning | When to Use |
|-----|---------|-------------|
| `[ready]` | Clarified and ready to implement | After Q&A in /list-todos |
| `[priority: N]` | Personal priority multiplier | Inline override (0.5-2.0) |

### Status Markers

| Marker | Meaning |
|--------|---------|
| `— DONE` | Completed |
| `— DONE ({hash})` | Completed with commit reference |
| `— **DEFERRED** ({reason})` | Postponed with explanation |
| `— **REMOVED** ({reason})` | Canceled with explanation |

### Clarifications Section

When requirements are refined through Q&A, add a clarifications block:

```markdown
- [ ] **[P1 / Medium]** {Title}

**Clarifications (from Q&A {YYYY-MM-DD}):**
- {Question 1}: {Answer 1}
- {Question 2}: {Answer 2}
```

## Workflow

Copy this checklist and track progress:

```
Add TODO Progress:
- [ ] Step 1: Gather information (title, priority, effort, description, section)
- [ ] Step 2: Format the TODO line
- [ ] Step 3: Read current TODOS.md
- [ ] Step 4: Insert TODO into selected section
- [ ] Step 5: Confirm addition
```

### Step 1: Gather Information

Use AskUserQuestion to collect TODO details:

**Question 1: Title**
```
Question: "What is the TODO item? (brief, actionable title)"
Header: "Title"
Options:
  - Label: "Enter title"
    Description: "Type your TODO title"
```

(User will select "Other" and type their title)

**Question 2: Priority**
```
Question: "What priority level?"
Header: "Priority"
Options:
  - Label: "P1 / High (Recommended)"
    Description: "Important feature or fix, do soon"
  - Label: "P0 / Critical"
    Description: "Blocking issue, must do immediately"
  - Label: "P2 / Low"
    Description: "Nice to have, do when time permits"
```

**Question 3: Effort**
```
Question: "Estimated effort?"
Header: "Effort"
Options:
  - Label: "Medium (Recommended)"
    Description: "A few hours to a day of work"
  - Label: "Low"
    Description: "Quick task, under an hour"
  - Label: "High"
    Description: "Multiple days or significant complexity"
```

**Question 4: Description (Optional)**
```
Question: "Add a description? (optional details, context, or requirements)"
Header: "Description"
Options:
  - Label: "Skip description"
    Description: "Title is sufficient"
  - Label: "Add description"
    Description: "Include additional context"
```

If "Add description", prompt for the description text.

**Question 5: Section**
```
Question: "Which section should this go in?"
Header: "Section"
Options:
  - Label: "In Progress (Recommended)"
    Description: "Active TODO items for current work"
  - Label: "Future Concepts"
    Description: "Ideas to explore later"
```

### Step 2: Format the TODO

Construct the TODO line:

```markdown
- [ ] **[{Priority} / {Effort}]** {Title}{if description: — {Description}}
```

**Examples:**

Simple:
```markdown
- [ ] **[P1 / Medium]** Add logout button to navbar
```

With description:
```markdown
- [ ] **[P1 / Medium]** Add logout button to navbar — Should redirect to login page after logout
```

With multiplier (if user specifies):
```markdown
- [ ] **[P1 / Medium x1.5]** Add logout button to navbar — High user demand
```

### Step 3: Read Current TODOS.md

Read TODOS.md to find the appropriate section.

**Section Detection:**
- Look for `## In Progress` heading
- Look for `## Future Concepts` heading
- If neither exists, create the section

### Step 4: Insert TODO

Insert the new TODO at the **end** of the selected section, before the next section heading or end of file.

Use the Edit tool to insert the TODO.

### Step 5: Confirm

Output confirmation:

```
TODO ADDED
==========

Added to: {Section}

{The formatted TODO line}

Next steps:
- Run /list-todos to analyze and prioritize
- Use Q&A to clarify requirements
- Mark [ready] when requirements are clear
- Run /run-todos to implement
```

## TODOS.md Template

If TODOS.md doesn't exist, create it:

```markdown
# TODO

## In Progress

{new TODO here}

## Future Concepts

(Ideas to explore later)
```

## Error Handling

**If TODOS.md cannot be written:**
- Check file permissions
- Report the error and suggest: `touch TODOS.md` or check directory permissions

**If existing TODOS.md has unexpected format:**
- Preserve the original content
- Add the new TODO at the end of the file
- Warn user about non-standard format

**If user provides ambiguous priority/effort:**
- Default to P2 / Medium
- Note the default in the confirmation message

**If the file is very large (>500 lines):**
- Warn user that the file is large
- Suggest archiving completed items to TODOS-ARCHIVE.md

## Notes

- **Preserve existing format** — Match the style of existing TODOs in the file
- **Don't add [ready] automatically** — Let /list-todos Q&A determine readiness
- **Default to In Progress** — Most new TODOs are active work items
- **Keep titles actionable** — Start with a verb (Add, Fix, Update, Implement)
- **Descriptions are optional** — Only add if title alone is ambiguous
