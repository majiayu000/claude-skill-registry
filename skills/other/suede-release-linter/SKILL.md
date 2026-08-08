---
name: suede-release-linter
description: "Audit creative release folders before handoff: metadata, file structure, artwork, lyrics, stems, rights blockers, and platform readiness."
---

# Release Metadata Linter

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

Audit a music or media project folder and produce a practical release-readiness report. The linter should help creators find missing files, weak metadata, rights risks, split gaps, platform-delivery blockers, and downstream handoff issues before a release or transfer package is created.

**Core principle:** report what is present, missing, or unknown. Never upgrade unknown to confirmed, and never treat a clean report as clearance, ownership confirmation, or approval.

Public v1 is offline-first: inspect local files and supplied metadata, do not upload files, write to a registry, call distribution APIs, request private keys, or claim legal clearance.

## Workflow

1. Identify the source folder or supplied files.
2. Ask for the output location if it is not obvious.
3. Read `references/lint-rules.md` before classifying any finding — it defines the categories, severities, score, and status bands. Do not assign severities from memory.
4. If working on a local folder, run `scripts/lint_release.py` to generate `release-lint-report.md` and `release-lint-report.json`.
5. Read `references/fix-guidance.md` when turning findings into specific next actions.
6. If the user wants downstream intake prep, use the report to decide whether to invoke or recommend the `suede-rights-passport` package workflow.
7. Do not invent release metadata. Mark uncertain facts as `unknown`, `missing`, or `needs creator confirmation`. Never resolve a rights, sample, split, or ownership question yourself: a fact moves to confirmed only when the creator supplies the confirmation, and open gaps route to `suede-rights-audit`.
8. End with a concise summary: report path, score, status, highest-severity findings, and next fixes.

## Quick Start

```bash
python3 /path/to/suede-release-linter/scripts/lint_release.py \
  /path/to/music-project \
  --output /path/to/release-lint-output
```

If the source folder contains a metadata file, pass it explicitly:

```bash
python3 /path/to/suede-release-linter/scripts/lint_release.py \
  /path/to/music-project \
  --metadata /path/to/music-project/metadata.json \
  --output /path/to/release-lint-output
```

Accepted metadata formats are JSON, YAML/YML when PyYAML is installed, and
public-safe key=value text files. Do not point metadata at real `.env`,
credential, wallet, or deployment config files.

Safety defaults:

- Hidden files, dependency folders, build outputs, caches, and secret-like files are skipped by default.
- Unrecognized file types are skipped unless `--include-other` is passed.
- Absolute local paths are redacted to share-safer names unless `--include-absolute-paths` is passed.
- Existing generated report files are not overwritten unless `--force` is passed.
- The output folder cannot be the same folder as the source or live inside it.
- YAML metadata requires PyYAML: `python3 -m pip install PyYAML`.

## What To Check

Read each bundled reference at the moment it is needed, not up front:

- `references/lint-rules.md`: before classifying findings, or when hand-linting without the script — categories, severity levels, score, and status bands.
- `references/metadata-fields.md`: when metadata is missing, malformed, or being authored — recommended fields, accepted aliases, and confirmation values.
- `references/fix-guidance.md`: when turning findings into next actions or a fix plan.
- `references/passport-context.md`: when the user asks how the lint report relates to Suede review or the Suede Creator Passport.

The script writes:

- `release-lint-report.md`: human-readable report.
- `release-lint-report.json`: machine-readable findings.

Use the bundled assets when repairing or hand-writing reports:

- `assets/release-lint-report.template.md`
- `assets/release-lint-report.template.json`
- `assets/metadata.example.json`

## Fixtures

Two synthetic release folders under `scripts/fixtures/` exist to sanity-check
that the linter still categorizes correctly after any change to
`scripts/lint_release.py`. All names, contributors, and metadata in both
fixtures are fake — no real personal data.

- `scripts/fixtures/sample-clean-project/`: a small release folder (metadata,
  a WAV master, square 1600x1600 artwork, a lyrics file, three stems) shaped
  to score cleanly against `references/lint-rules.md`.
- `scripts/fixtures/sample-blocked-project/`: a release folder deliberately
  missing title, artist, primary media, artwork, ownership confirmation, and
  valid split totals, with samples indicated but clearance unconfirmed — it
  triggers real `error`-severity findings.
- `scripts/fixtures/sample-clean-project.expected.md` /
  `.expected.json` and `scripts/fixtures/sample-blocked-project.expected.md` /
  `.expected.json`: the actual `release-lint-report.md` / `.json` output
  produced by running the script against each fixture, committed as a
  regression baseline.

To re-check the linter's behavior, run it from this skill folder and diff
the result against the committed expected output:

```bash
python3 scripts/lint_release.py scripts/fixtures/sample-clean-project \
  --output /tmp/suede-lint-check-clean
diff scripts/fixtures/sample-clean-project.expected.md \
  /tmp/suede-lint-check-clean/release-lint-report.md

python3 scripts/lint_release.py scripts/fixtures/sample-blocked-project \
  --output /tmp/suede-lint-check-blocked
diff scripts/fixtures/sample-blocked-project.expected.md \
  /tmp/suede-lint-check-blocked/release-lint-report.md
```

The clean fixture should score `99` with `0` errors, `0` warnings, and the
status `strong` (the single unavoidable `info` finding is the
`rights-passport-candidate` note the script always appends). The blocked
fixture should score `0` with `7` errors, `11` warnings, `2` info findings,
and the status `blocked`, and the script should exit `1`. The `.md` reports
diff byte-for-byte on a clean re-run; the `.json` reports will differ only in
the `generated_at` timestamp line, since that field is set to the current
time on every run.

## Public Safety Rules

- Do not say a project is legally cleared unless the user provides explicit proof.
- Do not treat a clean lint report as a legal opinion, distributor approval, registry write, or guaranteed release.
- Do not ask for private keys, seed phrases, unreleased account secrets, or full payment credentials.
- Do not include private implementation details, private endpoints, internal provider names, or non-public pricing.
- Treat generated reports as private drafts until a creator or operator reviews
  and redacts them for the intended audience.
- Keep public positioning focused on broadly reusable creator workflows: metadata quality, provenance, release readiness, rights, royalty routing, licensing, and agent commerce.

## Completion Checklist

Before reporting a lint result:

- Confirm the source folder was inspected or state that the report is based only on supplied text.
- Confirm whether metadata was discovered, supplied, or missing.
- Report the score and severity counts.
- List all `error` findings and the most important `warning` findings.
- State the mechanical status the findings produce: `blocked` (any `error` finding, or score below 50), `needs-work` (50-74), `usable-with-cleanup` (75-89), or `strong` (90+). Never soften a `blocked` status in prose.
- Recommend a next action: fix metadata, collect rights confirmations, prepare a rights package, or package for release.

## Red flags — stop

If any of these appear in your reasoning, stop and re-read the core principle:

- "The folder looks complete — skip the script." Run it. Eyeballing is not
  linting.
- "The artist obviously owns it." Ownership status comes from the creator, not
  from the folder.
- "One unconfirmed split won't block anything." Split errors block royalty
  routing and licensing by rule.
- "Round the score up; it's close." The score is arithmetic, not judgment.
- "A clean report means it's cleared." A clean report means fewer prep
  blockers. Nothing more.

## Downstream Review Context

A clean release-lint report is a portable review artifact. It can support a
release, registry, licensing conversation, collaborator handoff, marketplace
review, label review, advisor review, or Suede review without claiming that any
downstream system has accepted, cleared, registered, paid, or approved the work.

## Routing

- Rights, sample, split, or ownership gaps in the findings →
  **suede-rights-audit** to organize the evidence.
- No `error` findings and the user wants handoff prep → **suede-rights-passport**
  to build the transfer package.
- Track headed for film/TV/ads → **suede-sync-packaging**.
- The release needs a rollout → **suede-campaign-in-a-box**.
