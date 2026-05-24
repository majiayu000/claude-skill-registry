---
name: 012-agile-epic
description: Guides the creation of agile epics with comprehensive definition including business value, success criteria, and breakdown into user stories. Use when the user wants to create an agile epic, define large bodies of work, break down features into user stories, or document strategic initiatives. This should trigger for requests such as Create an agile epic; Write an epic; I need to create an epic; Define an epic; Epic definition. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Create Agile Epics

Guide the agent to systematically gather information and generate a comprehensive epic definition in Markdown format. An epic represents a large body of work that can be broken down into smaller user stories, features, or tasks. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Epic core details: title/ID, owner, business value, target users
- Epic scope and context: problem statement, solution overview, success criteria, dependencies
- Epic breakdown: key features and components (3-7 high-level items)
- Risk assessment: risks, assumptions, and unknowns
- Documentation linking: related documents and epic filename
- Next steps and recommendations for epic management

## Constraints

Before generating the epic document, gather all required information through structured questions. Use exact wording from the template and wait for user responses. Always get current date before starting.

- **MANDATORY**: Get current date using terminal command before starting the epic creation process
- **MANDATORY**: Ask questions from the template one-by-one in strict order before generating any artifacts
- **MUST**: Read the reference template fresh and use exact wording—do not use cached questions
- **MUST**: Wait for user response after each question or block before proceeding
- **MUST**: Replace all date placeholders with actual current date in the generated document

## When to use this skill

- Create an agile epic
- Write an epic
- I need to create an epic
- Define an epic
- Epic definition

## Workflow

0. **Get current date**

Run `date` before starting and use it to replace all date placeholders in the generated epic document.

1. **Gather epic information**

Ask the template questions in strict order, using exact wording and waiting for user responses before continuing.

Step constraints:
- Read the question template fresh before asking
- Do not skip or reorder required questions

2. **Generate epic document**

Create the epic Markdown with all required sections (scope, value, features, dependencies, risks, and success criteria) and apply the actual current date.

3. **Provide follow-up recommendations**

Close with actionable next steps for story breakdown, planning, and epic tracking.

## Reference

For detailed guidance, examples, and constraints, see [references/012-agile-epic.md](references/012-agile-epic.md).
