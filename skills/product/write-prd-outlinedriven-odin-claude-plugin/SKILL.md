---
name: write-prd
description: 'Use when a user asks to write a PRD or draft feature requirements. Produces a structured PRD with evidence-driven citations and opens a PR. Not for product specs with behavioral invariants; use write-product-spec. Not for tech specs; use write-tech-spec.'
disable-model-invocation: true
---

# Write PRD

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to write a PRD, create a product spec, or draft requirements for a feature. |
| Authority | Human-only: must be explicitly invoked. Credentials, paid actions, and remote publishing are previewed and confirmed before execution. |
| Side effect | Saves a PRD to reports/prds/; creates a GitHub PR; optionally exports to Google Docs, Notion, or Slack as separate user-initiated steps. |
| Done | A PRD file exists at reports/prds/prd_<feature_slug>_YYYY-MM-DD.md containing all ten required sections in the order specified in the procedure. |

## Inputs

| Input | Required |
|---|---|
| Feature name or description | Required |
| Target users | Optional |
| Constraints | Optional |
| Related URLs or docs | Optional |
| Priority level (P0/P1/P2) | Optional |

## Procedure

1. **Confirm scope.** Stop if no feature name or description is supplied. Ask only what is strictly necessary; do not widen scope. Done when: the feature name or description is confirmed.
2. **Gather context.** Read the following local sources when present and non-stale (≤7 days):
   - `reports/customer_feedback_summaries/`: user pain points and NPS data
   - `reports/competitor_changelog_reports/` or `reports/feature_research/`: competitive positioning
   - `reports/git_history_analysis/`: engineering work and priorities
   - `reports/weekly_product_briefings/`: recent briefings for the feature area

   If a source directory is absent or its content is stale (>7 days), note the absence and continue. Skip any source that returns an error. Done when: all available non-stale sources are read and stale/missing ones are noted.
3. **Cite every claim.** Every claim in the Problem Statement and Technical Considerations sections must carry a citation to a source: report filename, URL, or issue number. Unattributed claims must be tagged `[UNCITED]` and resolved or flagged in Open Questions. Done when: every claim carries a citation or is tagged `[UNCITED]`.
4. **Draft the PRD.** Produce a document with these sections in order: TL;DR, Problem Statement, Goals & Success Metrics (with non-goals), Target Users, Scope (in scope / out of scope), Proposed Solution (overview and key user flows), Technical Considerations, Competitive Context, Open Questions, References. Include the header block: title, author, date, status (Draft), priority. Done when: all sections are drafted with content and the section order is correct.
5. **Save the PRD.** Derive the feature slug from the feature name (lowercase, hyphenated). Write the file to `reports/prds/prd_<feature_slug>_YYYY-MM-DD.md`. Create the directory if absent. Done when: the PRD file is written to the correct path.
6. **Create a PR.** Before staging, present the saved PRD path and a content summary to the user and obtain explicit confirmation. Then stage and commit the PRD file; open a pull request against the tracked default branch. If VCS commands fail, report the error with the full path. Done when: the user confirms, the PRD is committed, and the PR is open against the default branch.
7. **Optional exports.** Google Docs, Notion, and Slack are separate user-initiated steps outside this skill's required path. Do not invoke them as part of the core workflow. Done when: the user is informed that exports are separate steps.

## Failure and recovery
| Failure class | Partial-result rule | Recovery |
|---|---|---|
| Feature name absent | No file written | Stop; ask for the feature name. |
| File write fails | No PRD on disk | Report the error with the path and root cause; PRD is lost. |
| PR creation fails | PRD file exists | Report the error; do not delete the PRD file. |
| Source read fails | Continue without that source | Note the absence; do not halt. |
| Stale data (>7 days) | Note staleness | Proceed; do not block. |
| Uncited claim | Flag with `[UNCITED]` | Resolve or move to Open Questions. |
| Missing required section | PRD is incomplete | Do not claim Done; report which section is absent. |

## Output
`reports/prds/prd_<feature_slug>_YYYY-MM-DD.md` with sections in order: TL;DR, Problem Statement, Goals & Success Metrics, Target Users, Scope, Proposed Solution, Technical Considerations, Competitive Context, Open Questions, References; plus an open PR against the default branch.
