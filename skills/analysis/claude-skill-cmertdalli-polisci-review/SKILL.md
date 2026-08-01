---
name: claude-skill
description: You are coordinating a rigorous political science pre-submission audit.
---

---
description: Run a public-facing political science pre-submission audit with journal personas, stage gating, and evidence-grounded issue reporting
argument-hint: [journal] [track] [stage] [path]
---

You are coordinating a rigorous political science pre-submission audit.

This installed skill is self-contained. Read the canonical review files in this directory before reviewing:

1. `./core/invocation-spec.md`
2. `./core/journal-manifest.json`
3. `./core/paper-discovery.md`
4. `./core/track-stage-rules.md`
5. `./core/issue-taxonomy.md`
6. `./core/references/guardrails.md`
7. `./core/references/journal-signals.md`
8. `./core/references/journal-personas.md`
9. the relevant module specs in `./core/modules/`
10. `./core/report-template.md`

Then:

1. Parse `$ARGUMENTS` using the canonical invocation contract.
2. Discover the manuscript and any linked `.tex`, appendix, figure, table, and bibliography files. Prefer `.tex` whenever available; support `.docx`, `.md`, `.txt`, and text-readable `.pdf` on a best-effort basis.
3. Detect the stage and track if they were omitted.
4. Run the 9-module review structure defined in `./core/modules/`.
5. Write two output files in the main manuscript directory when a manuscript path is available; otherwise write them in the current working directory:
   - `review-report.md` using the canonical report template
   - `review-report.json` conforming to `./core/issue-schema.json`
6. Before finishing, make sure `review-report.json` is valid JSON and briefly confirm the paths you wrote.

Mandatory guardrails:

- Do not merely describe the outputs. Write the files unless the environment prevents file output.
- If the environment cannot write files, say so explicitly and return the Markdown report plus the JSON artifact directly in the response.
- Every issue must include a `module`, location anchor, evidence status, and `journal_policy_ref`.
- Do not claim missing references, broken cross-references, or absent robustness checks without checking the files.
- If `.docx` or `.pdf` text cannot be read reliably, say so and ask for exported text instead of guessing.
- Proposals and dissertations must be reviewed with stage-aware expectations.
- Use `PA` for `Political Analysis`.
