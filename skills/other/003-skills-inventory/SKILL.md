---
name: 003-skills-inventory
description: Use when you need to generate a checklist document with Java system prompts from skills.xml, following the embedded section template and producing INVENTORY-SKILLS-JAVA.md. This should trigger for requests such as Create Java system prompts checklist; Generate INVENTORY-SKILLS-JAVA.md; Use @003-skills-inventory. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create a Checklist with all Java steps to use with system prompts for Java

Create a comprehensive step-by-step checklist document for Java system prompts by following the embedded section template and deriving rows from `skills-generator/src/main/resources/skills.xml`.

**What is covered in this Skill?**

- Inventory-driven checklist generation
- Output file creation as `INVENTORY-SKILLS-JAVA.md`
- Strict coverage of every effective skill id declared in `skills.xml`

## Constraints

Follow the template sections exactly and use `skills.xml` as the single source of truth for skill rows.

- **DO NOT** create additional sections beyond what the template defines
- **DO NOT** add skill rows absent from `skills.xml`
- **DO NOT** omit any skill declared in `skills.xml`
- **ONLY** use the `skillId` attribute as the generated skill id when it exists
- **ONLY** use the single `reference-list/reference` value as the generated skill id when `skillId` is absent
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Create Java system prompts checklist
- Generate INVENTORY-SKILLS-JAVA.md
- Use @003-skills-inventory

## Workflow

1. **Read the template and inventory source**

Read `references/003-skills-inventory.md` and `skills-generator/src/main/resources/skills.xml` before generating output.

Step constraints:
- Do not use cached or remembered template content
- Preserve exact section structure from the reference
- Use `skillId` when present; otherwise use the single reference name

2. **Generate inventory document**

Create `INVENTORY-SKILLS-JAVA.md` at the requested output path, or in the project root when no explicit path is requested, with one row for every effective skill id declared in `skills.xml`.

3. **Validate inventory coverage**

Verify that the generated file contains every effective skill id from `skills.xml`, contains no extra skill rows, and preserves all expected sections from the reference.

## Reference

For detailed guidance, examples, and constraints, see [references/003-skills-inventory.md](references/003-skills-inventory.md).
