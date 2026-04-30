---
name: canonical-markdown-authoring
description: >-
  Convert plain markdown contract drafts into OpenAgreements' canonical
  template.md authoring format — YAML frontmatter, Kind|Label|Value|Show When
  cover-term tables, oa:clause directives, [[Defined Term]] paragraphs, and
  oa:signer directives that compile to validated JSON specs and DOCX
  artifacts. Use when the user says "convert this to canonical markdown,"
  "author a new OpenAgreements template," "migrate template to template.md,"
  or "write a canonical-form contract."
license: MIT
compatibility: >-
  Requires read/write access to an OpenAgreements repo checkout (the canonical
  compiler at scripts/template_renderer/canonical-source.mjs and the
  cover-standard-signature-v1 layout must be available). Works with any agent
  that can edit local files and run `npm run` commands.
metadata:
  author: open-agreements
  version: "0.1.0"
catalog_group: Template Authoring
catalog_order: 10
---

# canonical-markdown-authoring

Convert plain markdown contract drafts into OpenAgreements' canonical `template.md`
authoring format. The canonical form is a single lawyer-editable file that compiles
to a validated JSON contract spec plus a rendered DOCX via the shared template
renderer.

## Activation

Use this skill when the user wants to:
- Convert a plain-prose contract draft into a canonical OpenAgreements `template.md`
- Migrate an existing JSON-source template to canonical authoring
- Author a new template that compiles via `npm run generate:templates`
- Add or refactor a Defined Terms clause, `oa:clause` directives, or signer metadata
- Bring a template into parity with the Wyoming / Employee IP canonical patterns

This skill assumes:
- You are working inside an OpenAgreements repo checkout. Templates live at
  `content/templates/<template-id>/template.md`.
- The shared canonical compiler (`scripts/template_renderer/canonical-source.mjs`)
  and the `cover-standard-signature-v1` layout are present.

## Canonical structure overview

A canonical `template.md` has these parts in this order:

1. **YAML frontmatter** — template ID, source paths, layout, style, document
   metadata, section labels.
2. **`# Title`** — H1 matching `document.title` in frontmatter.
3. **`## Cover Terms`** — short subtitle paragraph followed by a
   `Kind | Label | Value | Show When` table with `{snake_case}` field
   placeholders.
4. **`## Standard Terms`** — clauses, each preceded by `<!-- oa:clause id=... -->`.
   The first clause should be `Defined Terms` with `type=definitions`.
5. **`## Signatures`** — `<!-- oa:signature-mode arrangement=... -->` followed by
   exactly two `<!-- oa:signer ... -->` blocks.

## Step-by-step conversion

### Step 1 — Skeleton the frontmatter

```yaml
---
template_id: openagreements-<slug>                # kebab-case, must match the directory slug
layout_id: cover-standard-signature-v1
style_id: openagreements-default-v1
outputs:
  docx: content/templates/openagreements-<slug>/template.docx
document:
  title: <Document title>                         # MUST match the H1 below
  label: <Catalog label, e.g. "OpenAgreements XYZ">
  version: "1.0"
  license: Free to use under CC BY 4.0
  include_cloud_doc_line: true
  defined_term_highlight_mode: definition_site_only   # see "Highlight modes"
  cover_row_height: 700
sections:
  cover_terms:
    section_label: Cover Terms
    heading_title: Cover Terms
  standard_terms:
    section_label: Standard Terms
    heading_title: Standard Terms
  signature:
    section_label: Signature Page
    heading_title: Signatures
---
```

Notes:
- Canonical sources do **not** declare `source_json`. `npm run generate:templates`
  auto-discovers any `content/templates/<slug>/template.md` whose frontmatter
  declares `template_id`, `layout_id`, and `style_id`, then writes the
  generated JSON to `content/templates/<slug>/.template.generated.json`
  (a hidden, do-not-edit-by-hand artifact).
- Do **not** add `output_markdown_path` or `outputs.markdown` — the canonical
  compiler rejects them. The canonical `template.md` *is* the source.

### Step 2 — Title (H1)

```markdown
# <Document title>
```

Keep the H1 text identical to `document.title`. There is no automatic
cross-validation today, but drift between the two is a known footgun.

### Step 3 — Cover Terms section

Open with one short subtitle paragraph, then the `Kind | Label | Value | Show When`
table:

```markdown
## Cover Terms

The terms below are incorporated into and form part of this agreement.

| Kind | Label | Value | Show When |
| --- | --- | --- | --- |
| row | Company | {company_name} | always |
| row | Employee | {employee_name} | always |
| row | Effective Date | {effective_date} | always |
| group | Confidentiality |  | always |
| subrow | Trade Secrets Duration | {trade_secret_duration} | always |
| subrow | Other Confidential Information Duration | {other_confidentiality_duration} | confidentiality_other_included |
```

Rules:
- **Kind** is `row`, `group`, or `subrow`.
  - `row` — single-line cover term.
  - `group` — section header with no value (leave the `Value` column blank).
  - `subrow` — child of the most recent `group`; rendered indented.
- **Label** is the lawyer-facing label.
- **Value** is either literal text or a `{snake_case}` field placeholder. Field
  names must match `^[a-z_][a-z0-9_]*$`.
- **Show When**:
  - `always` — always rendered.
  - `<field_name>` — rendered only when the boolean field is truthy. The
    field's name must satisfy `^[a-z_][a-z0-9_]*$`.

### Step 4 — Standard Terms clauses

Every clause gets a directive, then a `### Heading`, then prose paragraphs:

```markdown
## Standard Terms

<!-- oa:clause id=assignment-of-inventions -->
### Assignment of Inventions

Employee hereby assigns and agrees to assign to Company all right, title, and
interest in Covered Inventions, to the extent permitted by law.

<!-- oa:clause id=non-competition when=noncompete_included omitted="[Intentionally Omitted.]" -->
### Non-Competition

During the Restricted Period, Employee must not engage in any Competitive Business
within the Restricted Territory.
```

Directive attributes:
- `id` — slug, kebab-case, unique within the document. Used for stable
  machine references.
- `when=<field_name>` (optional) — clause is only included when the named
  boolean field is truthy.
- `omitted="<text>"` (optional) — text rendered in place of the body when
  `when` evaluates false.

### Step 4A — Present-tense IP assignment language

If a clause transfers inventions, work product, patent rights, copyrights, or
other IP ownership, use a present-tense operative grant such as `hereby assigns`.

- Preferred baseline: `Employee hereby assigns to Company all right, title, and interest in ...`
- If future cooperation is also needed, add it after the present assignment:
  `... and will sign additional documents reasonably requested to confirm ownership.`
- Do **not** rely on `agrees to assign` or `will assign` without a present-tense
  grant. Federal Circuit contract law applied in the Stanford/Roche line of
  cases (*FilmTec*, *DDB Techs*, *Rasmussen Instruments*, the Federal Circuit
  decision in *Stanford v. Roche*, 583 F.3d 832) treats future-tense language
  as a promise to assign rather than a present transfer of rights — which
  diligence reviewers flag as a gap.
- This applies to employee invention-assignment agreements, contractor IP
  assignment clauses, work-made-for-hire fallback assignments, and standalone
  assignment instruments. It does **not** apply to NDAs or services agreements
  without IP transfer.
- "Irrevocably" (e.g. `hereby irrevocably assigns`) is optional belt-and-
  suspenders; "hereby assigns" is the doctrinal minimum.

### Step 5 — Defined Terms clause (use when it earns its keep)

Use a Defined Terms clause as the **first** clause under `## Standard Terms`
when a capitalized concept needs an explicit anchor or when a longer definition
materially shortens later operative clauses.

Before adding a definition, ask:

1. Does the definition add real substantive content, or materially reduce
   repetition by replacing a long phrase in operative clauses?
2. Is the term used enough in operative clauses that a short capitalized label
   improves readability?
3. If the substance belongs in a Cover Terms value, can that Cover Terms value
   remain the single source of truth?

Do **not** add pointer-only redefinitions for cover-page-only labels such as
`Company`, `Employee`, `Effective Date`, `Governing Law`, or `Venue`. Those
add a second lookup site without improving readability.

If a Cover Terms value contains the real substance of a defined concept, keep
all substantive content there. Use the Defined Terms clause only as a short
anchor when repeated capitalized use improves readability. Do **not** split one
definition across two sites by writing
`[[X]] has the meaning given in Cover Terms ... and includes ...`.

If you remove a formal definition, do not leave behind an unexplained
capitalized pseudo-term. Either use the exact Cover Terms label in prose
(`The Prior Inventions and Excluded Inventions identified in Cover Terms`)
or rewrite descriptively in lower-case prose.

```markdown
<!-- oa:clause id=defined-terms type=definitions -->
### Defined Terms

[[Covered Inventions]] means inventions, software, works of authorship,
discoveries, designs, data models, and related intellectual property created
during employment that arise from Company work, use Company resources, or
relate to Company actual or anticipated business.

[[Confidential Information]] means non-public information that Employee
learns, accesses, or develops during employment, including business strategies,
customer and prospect data, trade secrets, technical and product information,
financial information, personnel information, and any additional information
described in Cover Terms under Confidential Information Definition.
Confidential Information does not include information that (a) was publicly
known when Employee learned it, (b) becomes publicly known through no fault
of Employee, (c) was lawfully known to Employee before employment without
confidentiality restriction, or (d) Employee independently develops outside
the scope of employment without using Confidential Information.
```

Definition rules:
- Every paragraph inside the definitions clause must start its definition body
  with a `[[...]]` span — that span declares the canonical term.
- A leading article (`A`, `An`, `The`) before the first `[[...]]` is allowed
  and is stripped from the canonical term.
- Optional aliases follow the canonical term immediately as
  `(Aliases: [[Alias 1]], [[Alias 2]])`. Aliases never render in the legal
  output.
- Canonical terms must be unique. Aliases must be unique and may not collide
  with any canonical term.

### Step 6 — Explicit references

Anywhere outside the definitions clause, `[[Term]]` is an explicit reference and
must resolve to a canonical term, an alias, or a clause ID via
`[[clause:<id>]]`. **Plain-text mentions are valid** — you do not need to wrap
every "Confidential Information" in brackets. Use `[[...]]` only when you want
explicit linking semantics.

### Step 7 — Signatures section

```markdown
## Signatures

<!-- oa:signature-mode arrangement=entity-plus-individual -->

By signing this agreement, each party acknowledges and agrees to the obligations
above.

<!-- oa:signer id=company kind=entity capacity=through_representative label="Company" -->
**Company**

Signature: _______________
Print Name: {company_name}
Title: _______________
Date: _______________

<!-- oa:signer id=employee kind=individual capacity=personal label="Employee" -->
**Employee**

Signature: _______________
Print Name: {employee_name}
Title: _______________
Date: _______________
```

Strict rules (the `cover-standard-signature-v1` layout enforces these):
- **Exactly two signers.** Schema rejects any other count.
- **Same row IDs across signers.** Both signers should declare the same set
  of row IDs (e.g. `signature`, `print-name`, `title`, `date`) in the same
  order. The renderer unions row IDs in declaration order.
- **Matching labels and hints.** When both signers declare the same row ID,
  their `label` and `hint` must match. Mismatches are rejected with a clear
  error.
- `arrangement` is `entity-plus-individual` or `stacked`. Defaults to `stacked`.
- `kind` is `entity`, `individual`, or `acknowledging-individual`.
- `capacity` is `through_representative`, `personal`, or `acknowledging`.

### Step 8 — Generate and verify

```bash
npm run generate:templates
```

The canonical compiler:
1. Parses `template.md` → normalized model.
2. Validates definitions, references, signers, and field-name shapes.
3. Writes the regenerated JSON to `content/templates/<slug>/.template.generated.json`.
4. Renders the DOCX via the shared layout to `outputs.docx`.

After generation:
- `git diff content/templates/<slug>/.template.generated.json` — should be empty
  if your source matches the previously committed JSON.
- `npx vitest run integration-tests/canonical-source-sync.test.ts` — proves the
  canonical → JSON projection is in sync.
- `npx vitest run integration-tests/canonical-source-authoring.test.ts integration-tests/template-renderer-json-spec.test.ts packages/contract-templates-mcp/tests/tools.test.ts` — broader coverage.

## Highlight modes

`document.defined_term_highlight_mode` controls how defined terms are visually
highlighted in the rendered DOCX:

| Mode | Behavior | When to use |
| --- | --- | --- |
| `definition_site_only` | Highlights only at the definition paragraph; brackets are stripped from prose. | **Default for templates with a Defined Terms clause.** Avoids "too much blue" in body text. |
| `all_instances` | Highlights every occurrence of any term in `style.defined_terms`. | Templates without a Defined Terms clause that still want emphasis on a small fixed list (e.g. Company, Employee). |
| `none` | No highlighting. | Plain-text outputs. |

If you add a Defined Terms clause, switch to `definition_site_only`. The
template-wide `style.defined_terms` list still applies as a fallback for
`all_instances` mode.

## Reference templates

Working canonical templates already in the repo:

- `content/templates/openagreements-restrictive-covenant-wyoming/template.md` —
  feature-rich: substantive defined terms paired with narrow cover-term anchors
  for operative concepts, group/subrow cover terms, and conditional clauses.
- `content/templates/openagreements-employee-ip-inventions-assignment/template.md` —
  simpler: 2 substantive defined terms (`Covered Inventions`, `Confidential
  Information`), present-tense IP assignment language, and all-row cover terms.

When migrating a JSON-sourced template, copy the closer of these two as a
shape reference and adapt.

## Pitfalls

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| Edited `template.md` but forgot to regenerate | `canonical-source-sync.test.ts` fails | Run `npm run generate:templates` and commit the regenerated `.template.generated.json` diff. |
| H1 doesn't match `document.title` | Silent drift; renders the frontmatter title | Keep them in sync manually until cross-validation lands. |
| `output_markdown_path` left in frontmatter | Compiler throws | Remove `outputs.markdown` and any top-level `output_markdown_path`. |
| `source_json` left in frontmatter | Quietly ignored today; will become an error | Remove `source_json` — JSON paths are now derived from the slug. |
| Same-id signer rows with different labels | Layout throws "mismatched labels" error | Make both signers' row labels identical, or rename one row's ID. |
| Three signers | `cover-standard-signature-v1` rejects at render | Reduce to two signers, or add a new layout that supports N signers. |
| Field placeholder uses `camelCase` | Validation rejects | Use `snake_case` matching `^[a-z_][a-z0-9_]*$`. |
| Definitions paragraph without a `[[...]]` declaration | Compiler throws | Every paragraph in a definitions clause must declare a canonical term. |
| Alias collides with a canonical term or another alias | Compiler throws | Choose a unique alias. |
| Adding `[[...]]` everywhere in prose | "Too much blue" in DOCX | Reserve `[[...]]` for definition sites and explicit references; let plain prose stay plain. |
| Pointer-only redefinition of a cover-page-only term | Second lookup site with no readability gain | Omit the defined-term entry; use the Cover Terms label directly in prose. |
| One term split across Cover Terms and Defined Terms | Reader must combine two sources for one definition | Put all substantive content in one place — usually a substantive body definition with optional Cover Terms supplementation. |
| Capitalized pseudo-term with no exact anchor | Reader cannot tell where the term is defined | Keep an exact anchor (`identified in Cover Terms`) or rewrite in descriptive lower-case prose. |
| Bare `agrees to assign` in an IP assignment clause | Diligence flag — not a present transfer of rights | Use `hereby assigns and agrees to assign` (see Step 4A). |

## Minimal complete example

```markdown
---
template_id: openagreements-example-nda
layout_id: cover-standard-signature-v1
style_id: openagreements-default-v1
outputs:
  docx: content/templates/openagreements-example-nda/template.docx
document:
  title: Example Mutual NDA
  label: OpenAgreements Example Mutual NDA
  version: "1.0"
  license: Free to use under CC BY 4.0
  include_cloud_doc_line: true
  defined_term_highlight_mode: definition_site_only
  cover_row_height: 600
sections:
  cover_terms:
    section_label: Cover Terms
    heading_title: Cover Terms
  standard_terms:
    section_label: Standard Terms
    heading_title: Standard Terms
  signature:
    section_label: Signature Page
    heading_title: Signatures
---

# Example Mutual NDA

## Cover Terms

The terms below are incorporated into and form part of this agreement.

| Kind | Label | Value | Show When |
| --- | --- | --- | --- |
| row | Disclosing Party | {disclosing_party_name} | always |
| row | Receiving Party | {receiving_party_name} | always |
| row | Effective Date | {effective_date} | always |
| row | Confidentiality Term | {confidentiality_term} | always |

## Standard Terms

<!-- oa:clause id=defined-terms type=definitions -->
### Defined Terms

[[Confidential Information]] means non-public information disclosed by a party
that is identified as confidential at the time of disclosure or that a
reasonable person would understand to be confidential given the nature of the
information and the circumstances of disclosure.

<!-- oa:clause id=use-restrictions -->
### Use Restrictions

The Receiving Party identified in Cover Terms will use Confidential Information
solely to evaluate the business relationship contemplated between the parties
and will not disclose Confidential Information to third parties without the
Disclosing Party's written consent.

<!-- oa:clause id=term-and-survival -->
### Term and Survival

Each party's confidentiality obligations apply for the Confidentiality Term
listed in Cover Terms, beginning on the Effective Date. Trade-secret
obligations survive indefinitely.

## Signatures

<!-- oa:signature-mode arrangement=stacked -->

By signing this agreement, each party acknowledges and agrees to the obligations above.

<!-- oa:signer id=disclosing kind=entity capacity=through_representative label="Disclosing Party" -->
**Disclosing Party**

Signature: _______________
Print Name: {disclosing_party_name}
Title: _______________
Date: _______________

<!-- oa:signer id=receiving kind=entity capacity=through_representative label="Receiving Party" -->
**Receiving Party**

Signature: _______________
Print Name: {receiving_party_name}
Title: _______________
Date: _______________
```

## Notes

- Canonical authoring is the standard authoring format for OpenAgreements
  templates. New templates and migrations of existing JSON-source or
  Contract-IR-source templates should land in canonical `template.md` form
  and be picked up automatically by `npm run generate:templates`.
- This tool does not provide legal advice — consult an attorney.

## Connectors

For setup of the OpenAgreements repo / CLI, see [CONNECTORS.md](./CONNECTORS.md).
