---
name: 001-skills-inventory
description: Use when you need to generate a checklist document with Java system prompts, following the embedded template exactly and producing INVENTORY-SKILLS-JAVA.md in the project root. This should trigger for requests such as Create Java system prompts checklist; Generate INVENTORY-SKILLS-JAVA.md; Use @001-skills-inventory. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Create a Checklist with all Java steps to use with system prompts for Java

Create a comprehensive step-by-step checklist document for Java system prompts by following the embedded template exactly.

**What is covered in this Skill?**

- Exact-template checklist generation
- Output file creation as `INVENTORY-SKILLS-JAVA.md`
- Strict adherence to listed steps and cursor rules

## Constraints

Follow the template exactly without adding or removing steps, sections, or rules.

- **DO NOT** create additional steps beyond what the template defines
- **DO NOT** add cursor rules not explicitly listed in the template
- **ONLY** use exact wording and structure from the embedded template
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Create Java system prompts checklist
- Generate INVENTORY-SKILLS-JAVA.md
- Use @001-skills-inventory

## Workflow

1. **Read the embedded template**

Read `references/001-skills-inventory.md` before generating output and use it as the single source of truth.

Step constraints:
- Do not use cached or remembered template content
- Preserve exact section and checklist structure from the reference

2. **Generate inventory document**

Create `INVENTORY-SKILLS-JAVA.md` in the project root using the exact wording and order from the reference template.

3. **Validate template fidelity**

Verify that no extra steps or rules were added, and that all expected sections from the reference are present in the generated file.

## Reference

For detailed guidance, examples, and constraints, see [references/001-skills-inventory.md](references/001-skills-inventory.md).
