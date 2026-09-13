---
name: ln-64-community-announcer
description: "Drafts or publishes authorized, fact-checked GitHub Discussions announcements; does not create releases."
---

# Community Announcer

**Goal:** Create a source-backed announcement and publish it only after the user approves the full draft.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Repository identity and permissions | Authenticated GitHub CLI or connector | Public GitHub API for read-only discovery |
| Discussion categories and publication | GitHub GraphQL API | Continue a draft with destination limitations; publication is `BLOCKED` without this capability |
| Shipped-change evidence | Remote Git history, releases, and canonical files | Clean remote clone |
| Commands, paths, names, and counts | Focused repository search and direct reads | Hosting API content reads |
| Current external claims | Primary dated sources | Omit the claim when it cannot be verified |
| Draft publication | Temporary Markdown file passed to the API | Safely escaped API input with read-back verification |

Prefer the hosting API over scraping rendered pages. Use the browser only to inspect presentation or a page the API cannot expose.

Do not expose repository tokens, category node IDs, or other credentials in the announcement. IDs may be used for the mutation but are not audience content.

## Checklist

### Establish scope and evidence

- [ ] Resolve the target repository from the request or hosting client and determine whether the task is draft-only or includes publication.
- [ ] Read the default branch and source evidence. Discover Discussions availability and a suitable category when accessible; missing publication access does not prevent a fact-checked draft.
- [ ] For draft-only work, report destination limitations and continue. Before publication, require write access, repository/category IDs, and a suitable enabled Discussions category; do not silently publish elsewhere.
- [ ] Identify the announcement subject from the user's request, a release, or a bounded commit range.
- [ ] Read repository communication guidance when present, but do not require a community strategy file.
- [ ] Read the current authoritative documentation, installation instructions, affected manifests, release notes, and relevant source diffs when present.
- [ ] Inspect recent commits and up to three available comparable announcements for cadence, repeated claims, and house style; do not require prior announcements in a new or low-volume repository.
- [ ] Pin shipped claims to the target remote commit or release, including release lines behind the default branch; never present an unpushed local diff as available.
- [ ] Separate what shipped, what changed for users, migration needs, and future intent.

### Classification and Style

- [ ] Classify the announcement as release, breaking change, feature update, architecture change, or community news.
- [ ] Choose the shortest style that explains the user outcome and its significance.
- [ ] Match the project's voice while keeping claims understandable without internal repository context.

### Draft

- [ ] Write a specific title that names the outcome rather than saying only "update" or "announcement".
- [ ] Open with the user problem or the most important shipped outcome.
- [ ] Explain why the change was made using evidence from commits, docs, or release notes.
- [ ] Summarize highlights in outcome language and name exact products, packages, plugins, skills, or components where useful.
- [ ] Include verified installation or update commands when the reader must act.
- [ ] Make breaking changes prominent and provide clear before-and-after migration steps; follow repository format rather than requiring a particular callout label.
- [ ] Link to canonical documentation at the default branch or immutable release tag as appropriate.
- [ ] Include a short "What's next" section only for committed or clearly labelled tentative work.
- [ ] Thank verified external contributors by handle; omit the section for solo work.
- [ ] End with one genuine, answerable feedback question when community input would be useful.

### Fact Check

- [ ] Verify every command against current authoritative documentation and any stable package, plugin, or marketplace identifier it uses.
- [ ] Verify every named product, package, plugin, skill, component, file path, category, version, tag, and link against the remote repository.
- [ ] Recompute every count from the target commit; avoid counts when they add no user value.
- [ ] Confirm feature descriptions against the actual changed source, documentation, or manifest, not commit-title shorthand.
- [ ] Confirm removed capabilities and compatibility limits are stated explicitly.
- [ ] Do not invent adoption, download, search-volume, performance, compatibility, or roadmap claims.
- [ ] Label estimates, interpretations, and future intent instead of presenting them as shipped facts.
- [ ] Remove generic hype, repeated conclusions, excessive headings, canned transitions, and symmetrical filler lists.
- [ ] Re-read the draft as a new user and ensure it explains both the value and any required action.

### Approval and Publication

- [ ] Present the exact title and full Markdown body to the user before creating external state.
- [ ] Include the evidence range and selected category, or the unresolved destination limitation, with the draft.
- [ ] For draft-only work, complete the self-check and report `DRAFT READY` without waiting; clear publication-only items with this scope reason. For publication, require explicit approval of the exact copy and destination; reuse unchanged approval already given in the session. A request to announce does not approve unseen final copy.
- [ ] If the user changes any substantive claim or instruction, fact-check the revised draft again.
- [ ] Write the approved body to a temporary file to preserve formatting and avoid shell interpolation errors.
- [ ] Only for authorized publication, verify write access and destination, then publish through the GitHub Discussions GraphQL mutation using discovered repository and category IDs. Clear publication-only criteria when the request ends at a draft.
- [ ] Read the discussion back and verify title, body, category, and URL. After an uncertain response, inspect the returned ID or matching destination/content before retrying; stop if identity remains ambiguous rather than risk a duplicate.
- [ ] Remove the temporary draft safely after verification.
- [ ] Report the discussion URL and any manual action, such as pinning, that the API cannot perform.
- [ ] Do not create tags, releases, issues, comments, or cross-posts unless explicitly requested.

## Verdict

- `DRAFT READY` — fact-checked copy is complete; publication is either outside scope or awaiting exact-copy approval.
- `PUBLISHED` — the approved discussion exists and was read back successfully.
- `BLOCKED` — source evidence prevents a trustworthy draft, or a requested publication cannot proceed because its permissions, category, or verification is unavailable. Distinguish a completed draft from blocked publication.

- [ ] Verify claims about availability and measured effects against the actual release, deployment, or outcome evidence; distinguish announced plans from available capabilities.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Announcement classification, evidence range, destination/category or limitation, exact title, full fact-checked Markdown draft before approval, and fact-check summary. After publication, give the discussion URL and read-back verification while retaining approved copy in the response history. Report manual actions such as pinning; a mismatch with approved copy is `BLOCKED` and requires approval before editing/deleting external content.
