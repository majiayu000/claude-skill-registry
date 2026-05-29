---
name: 014-agile-user-story
description: Guides the creation of agile user stories and Gherkin feature files. Use when the user wants to create a user story, write acceptance criteria, define Gherkin scenarios, or author BDD feature files. This should trigger for requests such as Create a user story; Write a user story; I need to write a user story. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Create Agile User Stories and Gherkin Feature Files

Guide the agent to ask targeted questions to gather details for a user story and its Gherkin acceptance criteria, then generate a Markdown user story and a separate Gherkin `.feature` file. **This is an interactive SKILL**.

**What is covered in this Skill?**

- User story core details: title, persona, goal, benefit
- Gherkin feature file: Feature name, background steps, scenarios
- Acceptance criteria: Given / When / Then with data examples
- File naming and linking between user story and feature file
- INVEST quality validation before finalization (Independent, Negotiable, Valuable, Estimable, Small, Testable)

## Constraints

Before generating artifacts, gather all required information through structured questions. Use exact wording from the template and wait for user responses.

- **MANDATORY**: Ask questions from the template one-by-one in strict order before generating any artifacts
- **MUST**: Read the reference template fresh and use exact wording—do not use cached questions
- **MUST**: Wait for user response after each question or block before proceeding
- **MUST**: Repeat scenario questions for each additional scenario when user indicates more scenarios
- **MUST**: Validate the final user story against INVEST and present a pass/fail checkpoint for each criterion before finalizing

## When to use this skill

- Create a user story
- Write a user story
- I need to write a user story

## Workflow

1. **Gather story and scenario details**

Run the interactive questionnaire in strict order and wait for user responses before moving to the next question block.

Step constraints:
- Use the exact wording from the referenced template
- Repeat scenario questions for each additional scenario requested by the user

2. **Generate the two artifacts**

Create the user story Markdown and Gherkin `.feature` content using only gathered inputs, including links between files and scenario tags.

3. **Validate quality before finalizing**

Check output completeness and provide an INVEST pass/fail checkpoint with concrete evidence for each criterion.

## Reference

For detailed guidance, examples, and constraints, see [references/014-agile-user-story.md](references/014-agile-user-story.md).
