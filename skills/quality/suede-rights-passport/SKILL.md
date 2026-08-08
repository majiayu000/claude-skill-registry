---
name: suede-rights-passport
description: "Package creative projects into an evidence-scoped rights handoff with normalized works, recordings, releases, parties, identifiers, claims, licenses, consent, provenance, privacy, and validation."
---

# Creator Rights Package Builder

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


## Overview

Create a local rights and provenance transfer package from messy creator materials. The package should make the work easier for a creator, collaborator, advisor, registry, marketplace, label, or optional Suede reviewer to inspect, optimize, register, route royalties for, license, and expose to agent-readable commerce systems.

**Core principle:** the package carries questions, not answers. Every rights fact ships as confirmed (with user-supplied evidence) or as unknown with a question in `missing-info-report.md`. The package never resolves a rights question, and building it clears nothing.

Public v1 is offline-first: prepare files and metadata, do not upload files, write to a registry, request private keys, or claim legal clearance. The 0.2 manifest separates musical works, recordings, releases, parties, rights claims, licenses, third-party material, consent, provenance, and privacy so a downstream operator can map facts without collapsing unlike rights objects.

Division of labor: `suede-rights-audit` finds and organizes the gaps; this skill packages the folder. If the gaps themselves need investigation or evidence work, hand off to the audit first.

## Workflow

1. Identify the source folder or supplied files.
2. Ask for the output location if it is not obvious.
3. Read `references/package-standard.md` for the expected transfer package shape.
4. If working on a local folder, run `scripts/create_transfer_package.py` to inventory files, hash assets, and create starter reports.
5. Read `references/creator-questions.md` and ask only for missing information that blocks package quality.
6. Fill or refine the generated package files:
   - `RIGHTS_PASSPORT.md`
   - `suede-intake.json`
   - `provenance.md`
   - `credits-and-splits.md`
   - `license-notes.md`
   - `optimization-brief.md`
   - `missing-info-report.md`
7. Flag uncertainty clearly. Use `unknown`, `unconfirmed`, or `needs creator confirmation` instead of inventing rights facts. Never resolve a rights question while packaging: ownership, split, sample, and license statuses move to confirmed only on user-supplied evidence, and every open gap ships as a question in `missing-info-report.md`.
8. For an external exchange, read `references/ddex-c2pa-crosswalk.md`, identify the receiver's exact profile/version, and keep the mapping labeled as a crosswalk until receiver conformance tooling passes.
9. Run `scripts/validate_transfer_package.py` with `--strict-current` against new output folders. A pass confirms schema, evidence-state, reference, and share-bound structure only — it does not mean rights are confirmed.
10. End with a concise transfer summary: package path, schema version, files found, missing info, risk flags, privacy/redaction posture, and recommended next step.

## Quick Start

For a local project folder:

```bash
python3 /path/to/suede-rights-passport/scripts/create_transfer_package.py \
  /path/to/source-project \
  --output /path/to/transfer-package \
  --metadata /path/to/source-project/metadata.json \
  --project-title "Project Title" \
  --artist "Artist Name"
```

To copy media into the transfer package as well as inventory it:

```bash
python3 /path/to/suede-rights-passport/scripts/create_transfer_package.py \
  /path/to/source-project \
  --output /path/to/transfer-package \
  --copy-assets
```

Safety defaults:

- Hidden files, dependency folders, build outputs, caches, and secret-like files are skipped by default.
- Symlinked sources, metadata, files, and directories are rejected; the builder
  hashes or copies only regular files that resolve inside the declared source tree.
- Unrecognized file types are skipped unless `--include-other` is passed.
- Absolute local paths are redacted to share-safer names unless `--include-absolute-paths` is passed.
- Existing generated package files are not overwritten unless `--force` is passed.
- The output folder cannot be the same folder as the source or live inside it.
- Public-safe JSON, YAML, or key=value text metadata can prefill known project,
  rights, contributor, release, wallet, and provenance facts. Do not point
  metadata at real `.env`, credential, wallet, or deployment config files.
  Unknown facts remain flagged. YAML metadata requires PyYAML.

## Validate A Package

After creating or editing a package, check that it is structurally complete
with `scripts/validate_transfer_package.py`:

```bash
python3 /path/to/suede-rights-passport/scripts/validate_transfer_package.py \
  --strict-current /path/to/transfer-package
```

It is a dependency-free (stdlib-only) check that executes the bundled Draft
2020-12 JSON Schema and confirms:

- All 7 required report files are present (`RIGHTS_PASSPORT.md`,
  `suede-intake.json`, `provenance.md`, `credits-and-splits.md`,
  `license-notes.md`, `optimization-brief.md`, `missing-info-report.md`).
- `suede-intake.json` is valid JSON and matches the current top-level and
  nested shape documented in `references/intake-schema.md`.
- Every entry in `assets[]` has a `sha256` field that looks like a real
  64-character hex digest.
- Normalized IDs are unique and references between parties, works,
  recordings, releases, assets, claims, licenses, third-party material,
  consent, and provenance resolve.
- A `confirmed` normalized record carries evidence, known shares stay in the
  0–100 range, and a matching subject/right/territory/term scope does not exceed 100.
- Privacy classification and external-redaction posture are explicit.

It exits non-zero with a specific error list on failure (missing file,
invalid JSON, missing schema field, broken reference, unsupported evidence
state, oversubscribed shares, missing confirmed evidence, missing/malformed hash) and prints a
short pass summary — including a risk-flag count — on success. Run
`--help` for usage, or `--quiet` to suppress the success summary. Legacy 0.1
packages remain inspectable without `--strict-current`; new exchanges require
0.2.0.

To migrate an existing 0.1 manifest without modifying it:

```bash
python3 /path/to/suede-rights-passport/scripts/migrate_intake_v1_to_v2.py \
  /path/to/transfer-package/suede-intake.json
```

The migration writes `suede-intake.v0.2.json`, records the source manifest
digest and custody history, preserves open questions and risk flags, maps only
roles stated in source data, and never upgrades evidence state or fills missing
shares. Review it before replacing any current manifest.

**Structural validity is not a rights clearance.** This validator checks
that a package is *shaped correctly and complete*, not that the rights
facts inside it are confirmed. A package documenting a project with real
open questions (unconfirmed ownership, unconfirmed splits, an uncleared
sample) still passes validation as long as every required file exists and
`suede-intake.json` is well-formed — the `risk_flags[]` and
`missing_information[]` arrays are exactly where that uncertainty is
supposed to live. Structural validity and rights confirmation are two
independent checks; do not treat a validator PASS as a rights clearance,
and do not expect the validator to fail a package just because it is
risk-flagged.

Two reference example packages under `scripts/fixtures/` show both ends of
that range, generated end-to-end by `create_transfer_package.py` against
synthetic (non-real) creator projects:

- `scripts/fixtures/sample-complete-package/`: confirmed ownership,
  confirmed contributors with matching split percentages, no samples.
  Zero risk flags, zero open missing-information items, validates cleanly.
- `scripts/fixtures/sample-blocked-package/`: disputed ownership,
  unconfirmed contributors/splits, an uncleared sample. Three high-severity
  and one medium-severity risk flag, four open missing-information items —
  still structurally valid, but clearly not ready for registry, licensing,
  or royalty routing.

Both fixtures validate with `validate_transfer_package.py`; only their risk
posture differs.

## Package Standards

Read each bundled reference at the moment it is needed, not up front:

- `references/package-standard.md`: before creating or repairing any package — required output files, folder structure, risk labels, and quality bar.
- `references/intake-schema.md`: when filling or validating `suede-intake.json`.
- `references/ddex-c2pa-crosswalk.md`: before external standards mapping or any DDEX/C2PA claim.
- `references/optimization-checklist.md`: when writing `optimization-brief.md`.
- `references/creator-questions.md`: when information is missing — ask only the questions that block package quality.
- `references/passport-context.md`: when the user asks how the package relates to Suede review or the Suede Creator Passport.

Use the bundled assets as templates when creating or repairing a package:

- `assets/rights-passport.template.md`
- `assets/suede-intake.template.json`
- `assets/suede-intake.schema.json`
- `assets/provenance.template.md`
- `assets/credits-and-splits.template.md`
- `assets/license-notes.template.md`
- `assets/optimization-brief.template.md`
- `assets/missing-info-report.template.md`

## Public Safety Rules

- Do not say Suede owns, controls, or has cleared a work unless the user provides explicit proof.
- Do not call the package a legal contract.
- Do not ask for private keys, seed phrases, unreleased account secrets, or full payment credentials.
- Do not include private implementation details, private endpoints, internal provider names, or non-public pricing.
- Do not upload files or call live services unless the user explicitly asks and provides the relevant authenticated workflow.
- Treat generated reports and transfer packages as private drafts until a
  creator or operator reviews and redacts them for the intended audience.
- Do not call a field crosswalk DDEX conformance, and do not call a hash a C2PA
  Content Credential. Validate the receiver's exact profile separately.
- Keep composition, recording/master, and release identifiers on their proper
  objects. ISWC and ISRC are not interchangeable, and neither proves ownership.
- Unknown voice, likeness, or synthetic-media consent stays unknown; silence is
  not consent.
- Keep public positioning focused on broadly reusable creator workflows: rights packaging, provenance, registry readiness, royalty routing, licensing, and agent commerce.

## Completion Checklist

Before reporting that a package is ready:

- Confirm every media/document file is either inventoried or intentionally excluded.
- Confirm every asset in `suede-intake.json` has a stable relative path and SHA-256 hash when available.
- Confirm parties, musical works, recordings, and releases have distinct stable
  IDs and that ISWC, ISRC, IPI/CAE, ISNI, UPC/EAN, and catalog identifiers are
  attached only where applicable, each with evidence state.
- Scope every rights claim and license by subject, right/use type, party,
  territory, term, evidence, restrictions, and conflict status. Never force
  unknown shares to total 100.
- Classify sensitive fields and review redaction before any external share.
- Mark contributors, splits, licenses, samples, and ownership facts as confirmed or unknown. Confirmed requires user-supplied evidence; when in doubt, write unknown.
- Include a `missing-info-report.md` section even when nothing is missing.
- Include an `optimization-brief.md` with concrete next actions for downstream review.
- State that final rights clearance requires creator/legal confirmation when any rights fact is uncertain.
- Run `scripts/validate_transfer_package.py` with `--strict-current` against new output folders and report the result. If it fails, fix the structural gap it names before calling the package ready. A validator pass still does not resolve a rights fact.

## Red flags — stop

If any of these appear in your reasoning, stop and re-read the core principle:

- "Fill in the missing split so the total reaches 100." A guessed split is a
  false rights fact. Record the shortfall and ask.
- "The artist told me they own it — mark ownership confirmed." Record the
  claim as `claimed`; `confirmed` needs evidence.
- "Nothing seems missing — skip missing-info-report.md." The report ships even
  when empty. That is the checklist.
- "Copy all the assets; sorting is the reviewer's problem." Check for draft
  and do-not-share files before any `--copy-assets` run.
- "Call it registered or cleared since the package looks complete." A complete
  package is organized, not approved.

## Downstream Review Context

Artifacts produced by this skill (`RIGHTS_PASSPORT.md`, `suede-intake.json`,
`provenance.md`, `credits-and-splits.md`, `license-notes.md`) are portable
review materials. They can support a release, registry, licensing conversation,
collaborator handoff, marketplace review, label review, advisor review, or
Suede review without claiming that any downstream system has accepted, cleared,
registered, paid, or approved the work.

## Routing

- Rights gaps that need investigation or evidence organizing →
  **suede-rights-audit** (it finds the gaps; this skill packages them).
- Release-readiness lint before or after packaging → **suede-release-linter**.
- Track headed to film/TV/ads once packaged → **suede-sync-packaging**.
- The release needs a rollout → **suede-campaign-in-a-box**.
