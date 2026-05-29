---
name: lp-do-assessment-12-promote
description: Brand dossier promotion gate (ASSESSMENT-12). Validates completeness of a Draft brand dossier and promotes to Active with operator confirmation. Lightweight gate between ASSESSMENT-11 output and lp-design-spec GATE-BD-07.
---

# lp-do-assessment-12-promote — Brand Dossier Promotion (ASSESSMENT-12)

Validates that a Draft brand dossier meets minimum completeness requirements and promotes it to Active status with operator confirmation. This is the only path from Draft to Active for brand dossiers.

## Invocation

```
/lp-do-assessment-12-promote --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

VALIDATE + PROMOTE

This skill:
- Reads the existing brand dossier and checks completeness
- Reports any gaps to the operator
- Promotes to Active only with explicit operator confirmation

Does NOT:
- Create or fill brand dossier content (that is ASSESSMENT-11)
- Make design decisions
- Skip operator confirmation

## Required Inputs (pre-flight)

| Source | Path | Required |
|--------|------|----------|
| Brand dossier | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | Yes — blocks if absent |
| Brand strategy | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-profile.user.md` | No — cross-reference if present |

If brand dossier is absent, halt and emit:
> "Brand dossier not found at `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`. Run `/lp-do-assessment-11-brand-identity --business <BIZ>` first."

If brand dossier Status is already Active, emit:
> "Brand dossier is already Active. No action needed."

---

## Steps

### Step 1: Read and validate

Read the brand dossier. Check each requirement:

| # | Requirement | Rule |
|---|-------------|------|
| 1 | Frontmatter complete | Type, Stage, Business-Unit, Business-Name, Status, Created, Updated, Last-reviewed, Owner all present |
| 2 | Audience section | Primary and Device fields are non-TBD |
| 3 | Personality section | >= 3 adjective pairs with real content |
| 4 | Light Colour Palette | >= 2 rows with HSL values (not TBD) |
| 5 | Dark Colour Palette | Dark mode table present with >= 6 token rows (bg, fg, fg-muted, border, primary, accent minimum) |
| 6 | Typography | >= 1 row with Font Family and Source (not TBD) |
| 7 | Typography font source | Font Family references Google Fonts or system stack |
| 8 | Imagery Direction | >= 2 Do items and >= 2 Don't items |
| 9 | Voice & Tone | Formality and Humour set (not TBD) |
| 10 | Token Overrides | Section present (table may be empty if no light overrides needed) |

### Step 2: Report findings

Present a checklist to the operator:

```
Brand Dossier Promotion Check — <BIZ>

[x] 1. Frontmatter complete
[x] 2. Audience section populated
[ ] 3. ...
...

Result: <N>/10 passed. <M> gaps found.
```

If all 10 pass, ask operator to confirm promotion.
If any fail, list the gaps and recommend `/lp-do-assessment-11-brand-identity --business <BIZ>` to fill them.

### Step 3: Promote (if confirmed)

1. Set `Status: Active` in frontmatter
2. Set `Updated: <today>` in frontmatter
3. Set `Last-reviewed: <today>` in frontmatter
4. Save the file

---

## Output Contract

**Path:** Same file — `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` (in-place update)

**Changes:** Only frontmatter fields (Status, Updated, Last-reviewed). No content changes.

---

## Quality Gate

Before promoting, verify:
- [ ] All 10 completeness checks pass
- [ ] Operator has explicitly confirmed promotion
- [ ] Status was Draft before promotion (never promote from an unknown state)

## Red Flags

Invalid actions — do not perform:
- Promoting without all 10 checks passing
- Promoting without operator confirmation
- Editing content sections (only frontmatter changes allowed)
- Promoting a dossier that is already Active

## Completion Message

> "Brand dossier promoted to Active: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`. All 10 completeness checks passed."
>
> "GATE-BD-07 is now satisfiable. `/lp-design-spec` can proceed for this business."

---

## Integration

**Upstream (ASSESSMENT-11):** Runs after `/lp-do-assessment-11-brand-identity` creates a Draft dossier and the operator has reviewed it.

**Downstream:** Satisfies GATE-BD-07 in `/lp-design-spec`. Also satisfies any other gate that requires `Status: Active` on the brand dossier.

**No gate:** This skill IS the gate. After promotion, the operator can proceed to S1 or S7 design-spec work.
