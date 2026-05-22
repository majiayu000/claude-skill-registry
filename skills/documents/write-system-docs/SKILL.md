---
name: write-system-docs
description: Write system design documentation for the Investor Prospecting System. Triggers on "write docs", "document flow", "document system", "add documentation", "transcribe flow". Creates consistent markdown documentation from Whimsical extractions or verbal descriptions.
---

# Write System Docs

## When to Use

- Adding flow documentation to investor-prospecting-docs
- Transcribing Gemini-extracted Whimsical content
- Documenting system designs from verbal descriptions
- Creating router READMEs for new systems

## Invocation

| Command | Action |
|---------|--------|
| `/write-system-docs` | Interactive mode |
| `/write-system-docs flow` | Create flow document |
| `/write-system-docs router` | Create router README |
| `/write-system-docs reference` | Create reference document |
| `/write-system-docs reference sheet` | Extract Google Sheet |
| `/write-system-docs reference doc` | Extract Google Doc |
| `/write-system-docs reference pdf` | Create PDF entry |

## Standards

**Always read first:** `docs/system-design/CLAUDE.md`

## Workflow

1. Read documentation standards
2. Determine document type
3. Gather input content
4. Create document using template
5. Run quality checklist
6. Update router READMEs
7. Log to Linear (DIS-266)

**Use TodoWrite to track all steps.**

## References

| Topic | Link |
|-------|------|
| Flow template | [references/templates/flow-document.md](references/templates/flow-document.md) |
| Router template | [references/templates/router-document.md](references/templates/router-document.md) |
| Reference template | [references/templates/reference-document.md](references/templates/reference-document.md) |
| Extraction workflow | [references/workflows/extraction-workflow.md](references/workflows/extraction-workflow.md) |
| Quality checklist | [references/workflows/quality-checklist.md](references/workflows/quality-checklist.md) |
| Conventions | [references/conventions.md](references/conventions.md) |
