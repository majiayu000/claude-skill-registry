---
name: hl7v2-info
description: Look up segment fields, datatypes, components, tables, and message structures. MUST use this skill for writing HL7v2↔FHIR converters, mapping HL7v2 fields, checking field positions/optionality, verifying HL7v2 compliance or answering questions about hl7v2.
---

# HL7v2 Reference Lookup

Look up HL7v2 definitions using the reference script:

```bash
bun scripts/hl7v2-ref-lookup.ts <code> [--version <version>]
```

- `<code>`: the HL7v2 identifier to look up. Must be one of:
  - Message: `ORU_R01`, `ADT_A01`
  - Segment: `PID`, `OBX`
  - Field: `PID.3`, `OBX.2`
  - Component: `PID.3.1`, `CWE.1`
  - Table: `0001`, `0203`
  - Datatype: `CWE`, `ST`, `ID`
- `--version`: HL7v2 version (default `2.8.2`). Supported: `2.5`, `2.8.2`

## Version rules

This project has reference data for **two HL7v2 versions**: v2.5 and v2.8.2.

- **When answering user questions** (no version specified): look up **both versions in parallel** and present results. Highlight differences (optionality, cardinality, field presence, data types, table values). If identical, say so briefly.
- **When coding** (writing/modifying converters, parsers, builders): use **v2.8.2** as the primary reference — this is the project's target version. Check v2.5 if dealing with backward-compatibility concerns or if the code explicitly references v2.5.
- **When user specifies a version**: use only that version.

## When to use

- **Answering questions**: User asks about HL7v2 fields, datatypes, or message structures
- **Design/architecture**: Need to understand what fields a segment contains, what values a table allows, or how a message is structured
- **Coding**: Building or parsing HL7v2 segments — look up field positions, datatypes, optionality, cardinality, and valid table values
- **Code review**: Verify that field mappings, datatypes, and table values are correct

Do NOT skip this skill and rely on codebase exploration or memory for HL7v2 specifications. The reference data is the authoritative source.

When looking up multiple codes, make **separate Bash tool calls** in the same response — do NOT use shell `&` or `&&` to chain commands. The script is allowlisted individually (`bun scripts/hl7v2-ref-lookup.ts:*`), and chained shell commands bypass the allowlist and trigger permission prompts. Show the full script output to the user without modification.
