---
name: ce-adr-author
description: >
  Author or revise ADR files and release-plan ADR entries; use for new ADR drafts,
  status transitions, and ADR governance updates.
---

# CE ADR Author

Use this skill for any architectural record work in
`docs/improvement/adrs/`.

## Core assets

- `assets/adr_template.md` - canonical ADR template (copy this first).
- `docs/improvement/adrs/` - authoritative ADR directory.
- `docs/improvement/RELEASE_PLAN_v1.md` - roadmap entry that must stay aligned.

## Workflow

1. Determine whether this is a new ADR or an update to an existing ADR.
2. For new ADRs, calculate the next ADR number:

```bash
Get-ChildItem docs/improvement/adrs/ADR-*.md |
  ForEach-Object { [int]($_.Name -replace 'ADR-(\d+).*','$1') } |
  Measure-Object -Maximum | Select-Object -ExpandProperty Maximum
```

3. Copy the template asset to the target file:

```bash
Copy-Item .claude/skills/ce-adr-author/assets/adr_template.md `
  docs/improvement/adrs/ADR-<NNN>-<kebab-slug>.md
```

4. Fill every required field and section in the template. Keep language
   normative when needed (`MUST`, `MUST NOT`, `SHOULD`).
5. Add/validate `Related:` ADR links and update references to superseded ADRs.
6. If the decision changes implementation sequencing, add a one-line summary in
   `docs/improvement/RELEASE_PLAN_v1.md` under ADR roadmap summary.
7. If status changes to `Superseded`, rename the replaced ADR with
   `superseded ` prefix and set `Superseded-by`.

## Status lifecycle

| Status | Meaning |
|---|---|
| `Draft` | Under review; not yet binding |
| `Accepted` | Binding and enforceable |
| `Accepted (scoped)` | Binding only for explicit scope |
| `Deprecated` | Visible but replaced guidance exists |
| `Superseded` | Replaced by newer ADR |

## Required quality checks

- Filename uses `ADR-<NNN>-<kebab-slug>.md`.
- Template sections are complete (Context, Decision, Alternatives, Consequences,
  Adoption, Open Questions).
- At least two alternatives are documented with rejection rationale.
- Decision text states enforceable constraints clearly.
- `Related:` entries point to real ADR files.
- Release-plan linkage is updated when applicable.

## Output contract

Return:

1. ADR file path and status.
2. Summary of decision and alternatives.
3. Any companion updates made to `RELEASE_PLAN_v1.md`.
