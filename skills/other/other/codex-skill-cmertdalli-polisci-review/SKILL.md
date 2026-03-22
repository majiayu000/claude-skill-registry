---
name: polisci-review
description: Run a political science pre-submission audit with journal-aware personas, stage-aware standards, and evidence-grounded issue reporting.
metadata:
  short-description: Political science pre-submission audit
---

# PoliSci Review

This installed skill is self-contained.

Read the canonical files in this order:

1. `./core/invocation-spec.md`
2. `./core/journal-manifest.json`
3. `./core/paper-discovery.md`
4. `./core/track-stage-rules.md`
5. `./core/issue-taxonomy.md`
6. `./core/references/guardrails.md`
7. `./core/references/journal-signals.md`
8. `./core/references/journal-personas.md`
9. all relevant files in `./core/modules/`
10. `./core/report-template.md`

Workflow:

1. Parse user arguments using the canonical invocation contract.
2. Discover the manuscript and linked component files. Prefer `.tex` whenever available; support `.docx`, `.md`, `.txt`, and text-readable `.pdf` on a best-effort basis.
3. Detect stage and track when omitted.
4. Apply the selected journal persona and the 9-module audit structure.
5. Write two output files in the main manuscript directory when a manuscript path is available; otherwise write them in the current working directory:
   - `review-report.md` following `./core/report-template.md`
   - `review-report.json` conforming to `./core/issue-schema.json`
6. Before finishing, make sure `review-report.json` is valid JSON and briefly confirm the paths you wrote.

Guardrails:

- Do not merely describe the outputs. Write the files unless the environment prevents file output.
- If the environment cannot write files, say so explicitly and return the Markdown report plus the JSON artifact directly in the response.
- Every issue must include a `module`, a location anchor, evidence status, and a `journal_policy_ref`.
- Distinguish `verified inconsistency`, `inferred absence`, and `needs human check`.
- Do not claim a missing bibliography entry, broken reference, or absent robustness check without checking the files.
- If `.docx` or `.pdf` content cannot be read reliably, say so and request exported text instead of guessing.
- Do not review proposals as if they were completed articles.
- Use `PA` for `Political Analysis`.
