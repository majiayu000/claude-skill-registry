---
name: 200-agents-md
description: Use when you need to generate an AGENTS.md file for a Java repository — covering project conventions, tech stack, file structure, commands, Git workflow, and contributor boundaries — through a modular, step-based interactive process that adapts to your specific project needs. This should trigger for requests such as Create AGENTS.md; Update AGENTS.md file; Add agent instructions. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# AGENTS.md Generator for Java repositories

Generate a comprehensive AGENTS.md file for Java repositories through a modular, step-based interactive process that covers role definition, tech stack, file structure, commands, Git workflow, and contributor boundaries. **This is an interactive SKILL**.

**What is covered in this Skill?**

- AGENTS.md generation for Java repositories of any complexity
- Role and expertise definition for AI agents and contributors
- Tech stack documentation: language, build tool, frameworks, pipelines
- File structure mapping with read/write boundaries
- Command catalogue for build/test/deploy/run workflows
- Git workflow conventions: branching strategy, commit message format
- Contributor boundaries using ✅ Always do / ⚠️ Ask first / 🚫 Never do formatting

## Constraints

No Maven validation is required before generating AGENTS.md. Review the project structure and existing documentation before starting to provide accurate answers during Step 1.

- **BEFORE STARTING**: Review the project structure and existing documentation to provide accurate answers during Step 1
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each AGENTS.md generation pattern
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Create AGENTS.md
- Update AGENTS.md file
- Add agent instructions

## Workflow

1. **Review repository context before drafting**

Inspect project structure and existing documentation to prepare accurate responses for the AGENTS.md discovery phase.

2. **Read AGENTS generation reference**

Read `references/200-agents-md.md` and follow its generation patterns and safeguards.

3. **Run interactive requirements capture**

Gather role, tech stack, commands, workflow, and boundaries in a modular step-based conversation.

4. **Generate AGENTS.md artifact**

Create AGENTS.md with ✅ Always do / ⚠️ Ask first / 🚫 Never do boundaries and repository-specific conventions.

## Reference

For detailed guidance, examples, and constraints, see [references/200-agents-md.md](references/200-agents-md.md).
