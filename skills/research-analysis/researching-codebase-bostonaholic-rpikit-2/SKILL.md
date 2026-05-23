---
name: researching-codebase
description: >-
  This skill should be used when the user asks to "research the codebase",
  "understand how X works", "explore the code", "gather context",
  "investigate the implementation", "analyze the architecture", or invokes
  the rpikit:research command. Provides methodology for thorough interrogation
  and codebase exploration before planning or implementation.
---

# Research Methodology

Research topic: **$ARGUMENTS**

## Overview

Help turn research requests into thorough codebase understanding through
natural collaborative dialogue.

Start by understanding what the user needs to learn, then ask questions one
at a time to refine the scope. Once you understand what you're researching,
explore the codebase systematically, presenting findings in digestible
sections and validating as you go.

## The Iron Law

**Ask questions BEFORE exploring code.**

Do not touch the codebase until the problem is understood. Resist the urge
to immediately search for files or read code.

## Phase 1: Understanding the Request

**Your first action must be asking a clarifying question.**

Do NOT:

- Read any files
- Search the codebase
- Use Glob or Grep
- Explore anything
- Make assumptions about what the user wants

**Ask questions one at a time using AskUserQuestion:**

- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message
- If a topic needs more exploration, break it into multiple questions

**Focus on understanding:**

- **Purpose**: What are they trying to accomplish? (build, change, fix, learn)
- **Specifics**: What exactly should happen or change?
- **Scope**: How big is this? (one file, multiple files, architectural)
- **Constraints**: Any requirements around performance, compatibility, security?
- **Context**: Have they already looked at anything or have hunches?

**When you believe you understand, confirm:**

Summarize your understanding and ask if it's accurate before proceeding.
If anything needs clarification, ask follow-up questions.

## Phase 2: Exploration

**Only proceed after confirming understanding with the user.**

### Locate Relevant Files

Use the **file-finder** agent to locate files relevant to the research objective:

```text
Task tool with subagent_type: "file-finder"
Prompt: "Find files related to [topic from interrogation]. Goal: [user's stated purpose]"
```

The file-finder will return a structured report with:

- Core files to examine first
- Supporting files and utilities
- Test files
- Configuration files
- Suggested reading order

### Explore the Discovered Files

Use TodoWrite to track exploration based on the file-finder report.

**Examine core files first:**

- Read files in the suggested order
- Understand the main flow and architecture
- Note patterns and conventions

**Trace relevant data flow:**

- Follow data through the identified files
- Identify inputs, transformations, outputs
- Document state changes and side effects

**Review supporting files:**

- Examine utilities and helpers
- Note reusable patterns
- Document conventions for testing and error handling

**Identify technical constraints:**

- External dependencies
- Performance considerations
- Security implications

### Research External Context (When Needed)

If codebase exploration reveals external factors that need investigation, use
the **web-researcher** agent:

```text
Task tool with subagent_type: "web-researcher"
Prompt: "[specific research question about external topic]"
```

Use web research for:

- Understanding external libraries or APIs the code depends on
- Comparing implementation approaches or best practices
- Investigating third-party service documentation
- Researching security implications or known issues

The web-researcher returns findings with source citations and confidence
assessments.

**Present findings incrementally:**

- Share what you find in digestible sections
- Ask if findings align with expectations or if you should look elsewhere
- Be ready to redirect based on feedback

## Phase 3: Document Findings

Create research document at: `docs/plans/YYYY-MM-DD-<topic>-research.md`

(Use today's date in YYYY-MM-DD format)

```markdown
# Research: <Topic> (YYYY-MM-DD)

## Problem Statement

[What the user wants to accomplish]

## Requirements

[Key requirements gathered during interrogation]

## Findings

### Relevant Files

| File            | Purpose     | Key Lines |
| --------------- | ----------- | --------- |
| path/to/file.ts | Description | 42-87     |

### Existing Patterns

[Patterns discovered that inform implementation]

### Dependencies

[External and internal dependencies]

### External Research

[Findings from web research, if conducted - include sources]

### Technical Constraints

[Limitations discovered during exploration]

## Open Questions

[Questions that remain unanswered]

## Recommendations

[Initial thoughts on approach]
```

## Phase 4: Transition

Ask what the user wants to do next:

- Create an implementation plan
- Continue researching
- End for now

## Questioning Techniques

**Funnel questions** - Start broad, narrow based on answers:

1. "What are you trying to accomplish?" (broad)
2. "Which part is most important?" (narrowing)
3. "What would success look like?" (specific)

**Assumption surfacing** - Make assumptions explicit:

> I'm assuming this needs to work with the existing auth system. Is that
> correct?

**Trade-off questions** - When multiple approaches exist:

> There's a trade-off: Option A is faster to build but less flexible.
> Option B is more flexible but more complex. Which matters more here?

**Clarification through examples** - When requirements are vague:

> Can you give me an example of what you'd expect to happen?

## Anti-Patterns

| Wrong                                          | Right                                                 |
| ---------------------------------------------- | ----------------------------------------------------- |
| Reading files immediately                      | Ask questions first                                   |
| Multiple questions in one message              | One question, wait, then next                         |
| "I understand, let me look"                    | "Let me confirm: [summary]. Accurate?"                |
| "How should we handle this?"                   | "Should we A) do X, B) do Y, or C) something else?"   |
| "I'll add a new AuthService"                   | "The codebase uses repository pattern. Auth is here." |

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended
- **Confirm before exploring** - Validate understanding first
- **Incremental findings** - Present discoveries in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't fit

## Markdown Validation

After writing the research document, validate markdown formatting:

Invoke Skill tool with skill: "rpikit:markdown-validation"

Fix all errors before presenting findings. Research documents with linting
errors undermine credibility.
