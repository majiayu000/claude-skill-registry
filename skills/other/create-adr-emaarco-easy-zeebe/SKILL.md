---
name: create-adr
argument-hint: "\"<short description of the decision>\""
allowed-tools: Read, Write, Glob
description: Write a new Architectural Decision Record (ADR) for this project in MADR format with interactive content gathering and user confirmation before writing. Use when the user asks to "write an ADR", "create an architectural decision record", or "document a design decision". Auto-numbers from the existing ADR index, derives the filename slug from the title, and shows a full draft for review before writing the file.
---

# Skill: create-adr

Write a new Architectural Decision Record following the MADR format used in `docs/adr/`.

## Instructions

### Step 1 – Verify prerequisites

Check that `docs/adr/` exists by running Glob for `docs/adr/*.md`.

- If the directory does not exist or Glob returns no results at all (not even the template), **stop immediately**
  and tell the user: "The `docs/adr/` directory is missing. Please create it and add an ADR template at
  `docs/adr/0000-adr-template.md` before running this skill again."

Check that `docs/adr/0000-adr-template.md` exists.

- If the template file is missing, **stop immediately** and tell the user: "No ADR template found at
  `docs/adr/0000-adr-template.md`. Please add a template before running this skill again."

Do not proceed until both checks pass.

### Step 1b – Determine the next ADR number

From the Glob results, extract the four-digit numeric prefix from each filename
(e.g. `0001` from `0001-hexagonal-architecture.md`). The next number is the highest existing prefix plus one,
zero-padded to four digits. If no non-template files exist (only `0000-adr-template.md`), start at `0001`.

### Step 2 – Derive the filename slug

Convert `$ARGUMENTS` to a kebab-case slug:
- Lowercase all characters
- Replace spaces and underscores with hyphens
- Remove characters that are not alphanumeric or hyphens
- Collapse consecutive hyphens into one

Target file path: `docs/adr/{XXXX}-{slug}.md`

Example: `"use bpmn-to-code for process constant generation"` →
`docs/adr/0002-use-bpmn-to-code-for-process-constant-generation.md`

### Step 3 – Read the template

Read `docs/adr/0000-adr-template.md` (already confirmed to exist in Step 1) as the structural reference.

### Step 4 – Gather content from the user

Ask the user the following (you may ask all at once). Skip any question that `$ARGUMENTS` already answers.

1. **Context**: What is the problem or situation that motivated this decision? What forces or constraints apply?
2. **Decision**: What was decided? State it in one or two clear sentences using active voice.
3. **Positive consequences**: What becomes better or easier as a result?
4. **Negative consequences**: What becomes harder or is accepted as a trade-off?
5. **Neutral consequences** (optional): What simply changes, with no clear positive or negative value?

### Step 5 – Draft the ADR

Compose the ADR using the template structure:
- Title: short imperative phrase derived from `$ARGUMENTS`
- Date: today's date in `YYYY-MM-DD` format
- Status: `Accepted` by default — ask the user only if they indicate a different status is appropriate
- Context, Decision, Consequences: from Step 4

Show the complete draft to the user before writing.

### Step 6 – Confirm and write

Ask: "Write this ADR to `{target-path}`? (yes / edit / cancel)"

- **yes** → write the file and report the path
- **edit** → apply the user's changes, show the updated draft, and ask again
- **cancel** → stop without writing

### Step 7 – Report

After writing, output:
- The path of the created file
- A reminder to commit the ADR in the same commit as the code change it documents, so the decision and its
  implementation are traceable together in git history
