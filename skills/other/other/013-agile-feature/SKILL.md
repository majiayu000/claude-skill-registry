---
name: 013-agile-feature
description: Guides the creation of detailed agile feature documentation from an existing epic. Use when the user wants to split an epic into feature files, derive features with scope and acceptance criteria, or plan feature documentation for stakeholders or engineering. This should trigger for requests such as Create features from an epic; Split epic into features; Feature files from epic; Derive features from epic. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Create Agile Features from an Epic

Guide the agent to analyze an epic (from file path or pasted content), hold a structured conversation, and generate one Markdown feature document per agreed feature. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Epic intake: path or pasted content, confirmation of epic summary
- Feature scope: which features to document, technical vs high-level depth
- Audience and content mix: stakeholders vs engineering, functional vs technical emphasis
- File organization: naming convention and output location
- Per-feature refinement: user story links or suggestions, dependencies, success metrics
- Optional timeline, release constraints, risks, and technical challenges
- Date handling via `date` for Created/Last Updated fields

## Constraints

Read the epic before summarizing. Ask questions in order; repeat questions 9–11 for each identified feature. Use the feature template and user-provided naming and paths.

- **MANDATORY**: Get current date using terminal command before generating feature files
- **MUST**: Read epic content from path or use pasted content—do not invent epic details
- **MUST**: Use exact wording from the questions template for numbered questions
- **MUST**: Repeat per-feature questions (9–11) for every feature in scope
- **MUST**: Wait for user responses before proceeding through the flow

## When to use this skill

- Create features from an epic
- Split epic into features
- Feature files from epic
- Derive features from epic

## Workflow

0. **Get current date**

Run `date` before generation and use that value for all date placeholders in feature documents.

1. **Analyze epic and gather feature details**

Read epic content from file path or pasted input, summarize it for confirmation, then ask the template questions in order.

Step constraints:
- Use exact wording from the numbered template questions
- Repeat per-feature questions (9-11) for every identified feature

2. **Generate one document per feature**

Create one Markdown feature file per agreed feature, honoring user-defined naming, output path, audience/depth preferences, and per-feature inputs.

3. **Close with integration guidance**

Provide next steps for prioritization, breakdown into user stories, and alignment with epic goals and dependencies.

## Reference

For detailed guidance, examples, and constraints, see [references/013-agile-feature.md](references/013-agile-feature.md).
