---
name: create-handoff
description: Create handoff documentation for work-in-progress sessions. Use when handing off work to another agent to supplement history compaction and and progress summarization.
user-invocable: true
---

# Create Handoff

You are tasked with writing a handoff document to hand off your work to another agent in a new session. You will create a handoff document that is thorough, but also **concise**. The goal is to compact and summarize your context without losing any of the key details of what you're working on.

## Process

### 1. Filepath & Metadata

Use the following information to understand how to create your document: - create your file under `.claude/scratchpad/handoffs/[feature]_description.md`, where: feature is a brief kebab-case description

### 2. Handoff writing.

use the defined filepath, and the following YAML frontmatter pattern. Structure the document with YAML frontmatter followed by content:

Use the following template structure:

```markdown
---
date: [Current date and time with timezone in ISO format]
git_commit: [Current commit hash]
branch: [Current branch name]
repository: [Repository name]
topic: '[Feature/Task Name] Implementation Strategy'
last_updated: [Current date in YYYY-MM-DD format]
type: implementation_strategy
---

# Handoff: {ticket-id} {very concise description}

## Task(s)

{description of the task(s) that you were working on, along with the status of each (completed, work in progress, planned/discussed). If you are working on an implementation plan, make sure to call out which phase you are on. Make sure to reference the plan document and/or research document(s) you are working from that were provided to you at the beginning of the session, if applicable.}

## Critical References

{List any critical specification documents, architectural decisions, or design docs that must be followed. Include only 2-3 most important file paths. Leave blank if none.}

## Recent changes

{describe recent changes made to the codebase that you made in line:file syntax}

## Learnings

{describe important things that you learned - e.g. patterns, root causes of bugs, or other important pieces of information someone that is picking up your work after you should know. consider listing explicit file paths.}

## Artifacts

{ an exhaustive list of artifacts you produced or updated as filepaths and/or file:line references - e.g. paths to feature documents, implementation plans, etc that should be read in order to resume your work.}

## Action Items & Next Steps

{ a list of action items and next steps for the next agent to accomplish based on your tasks and their statuses}

## Other Notes

{ other notes, references, or useful information - e.g. where relevant sections of the codebase are, where relevant documents are, or other important things you leanrned that you want to pass on but that don't fall into the above categories}
```

---

##. Additional Notes & Instructions

- **more information, not less**. This is a guideline that defines the minimum of what a handoff should be. Always feel free to include more information if necessary.
- **be thorough and precise**. include both top-level objectives, and lower-level details as necessary.
- **avoid excessive code snippets**. While a brief snippet to describe some key change is important, avoid large code blocks or diffs; do not include one unless it's necessary (e.g. pertains to an error you're debugging). Prefer using `/path/to/file.ext:line` references that an agent can follow later when it's ready, e.g. `packages/dashboard/src/app/dashboard/page.tsx:12-24`
