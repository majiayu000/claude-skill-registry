---
name: create-ops-spreadsheet
description: Define an operations spreadsheet deliverable with schema, formula logic, ownership, and a starter CSV template.
---

# Create Ops Spreadsheet

Design spreadsheet-based operational deliverables with explicit structure and validation logic.

## When to Use

Use this skill when a task deliverable is a spreadsheet model, tracker, planner, or reconciliation sheet.

## Operating Mode

**SPREADSHEET SPEC + TEMPLATE AUTHORING**

**Allowed:** define schema, formulas, validation rules, and template files.

**Not allowed:** vague column definitions, implicit formulas, undocumented data sources.

## Inputs

- Spreadsheet purpose and users
- Required tabs/views
- Data sources and refresh cadence
- Required calculations/formulas
- Quality controls (validation rules, reconciliation checks)

## Outputs

Create/update:

- Spec: `docs/ops/spreadsheets/<slug>-spec.md`
- Template: `docs/ops/spreadsheets/<slug>-template.csv` (starter tab format)

Spec sections:

```markdown
# <Spreadsheet Name> Spec

## Purpose
## Users / Owners
## Sheet Structure
## Column Dictionary
## Formula Rules
## Data Validation Rules
## Source Inputs & Refresh Cadence
## QA / Reconciliation Checklist
```

## Workflow

1. Define purpose and user decisions this sheet supports.
2. Specify columns with type/constraints/defaults.
3. Define formulas and validation rules explicitly.
4. Produce starter CSV template with headers.
5. Add QA/reconciliation checklist and owner responsibilities.

## Quality Gate

- [ ] Every column has type and meaning.
- [ ] Formula logic is explicit and reproducible.
- [ ] Validation/reconciliation checks are actionable.
- [ ] Ownership and refresh cadence are clear.

## Completion Message

> "Spreadsheet deliverable ready: `docs/ops/spreadsheets/<slug>-spec.md` + `docs/ops/spreadsheets/<slug>-template.csv`."
