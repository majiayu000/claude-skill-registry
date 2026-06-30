---
name: 001-commands-inventory
description: Use when you need to generate a checklist document with embedded commands inventory, following the embedded template exactly and producing INVENTORY-COMMANDS-JAVA.md in the project root. This should trigger for requests such as Create embedded commands inventory checklist; Generate INVENTORY-COMMANDS-JAVA.md; Use @001-commands-inventory. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create a Checklist with embedded commands inventory for Java

Create a comprehensive checklist document for embedded commands inventory by following the embedded template exactly.

**What is covered in this Skill?**

- Exact-template checklist generation
- Output file creation as `INVENTORY-COMMANDS-JAVA.md`
- Strict adherence to listed sections and content

## Constraints

Follow the template exactly without adding or removing sections, rows, or command entries.

- **DO NOT** create additional rows beyond what the template defines
- **DO NOT** add command entries not explicitly listed in the template
- **ONLY** use exact wording and structure from the embedded template
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Create embedded commands inventory checklist
- Generate INVENTORY-COMMANDS-JAVA.md
- Use @001-commands-inventory

## Workflow

1. **Read the embedded template**

Read `references/001-commands-inventory.md` before generating output and use it as the authoritative template.

Step constraints:
- Do not use cached or partial template content
- Preserve exact table rows, headings, and structure from the reference

2. **Generate inventory document**

Create `INVENTORY-COMMANDS-JAVA.md` in the project root using the exact wording and ordering from the reference template.

3. **Validate template fidelity**

Confirm no extra command rows were introduced and all required reference sections are present in the generated file.

## Reference

For detailed guidance, examples, and constraints, see [references/001-commands-inventory.md](references/001-commands-inventory.md).
