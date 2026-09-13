---
name: ln-62-release-publisher
description: "Prepares and publishes an explicitly requested tagged GitHub release; does not deploy applications."
---

# Release Publisher

**Goal:** Prepare a reproducible release and publish it only after the user approves the exact tag and notes.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Release boundary and commit evidence | Git history, tags, and diffs | Hosting API commit comparison |
| Existing release style and state | Authenticated GitHub CLI or connector | Public GitHub API for read-only evidence |
| Release identity and version scope | Repository policy, prior tags, and canonical version files when present | Stop only when the release identity remains ambiguous |
| Release validation | Repository-native gates and clean checkout | Manual structural checks with reduced confidence |
| Tag and GitHub Release creation | Git plus an authenticated GitHub release capability | `BLOCKED`; do not emulate release state in files |
| Installation verification | Isolated environment against the documented distribution source | Clean source validation without install proof |

When publishing through a shell, use a temporary notes file so Markdown, quotes, and code blocks are not reinterpreted. Keep credentials in the host credential store and never echo them.

Do not browse for generic release advice when repository policy and previous comparable releases answer the question. Use official host documentation only for current API or CLI behavior.

## Checklist

### Establish scope and evidence

- [ ] Confirm the user explicitly requested a release and identify the repository, release target, and intended audience.
- [ ] Read repository release rules before selecting a version, tag shape, files, or publication sequence.
- [ ] Verify an authenticated GitHub release capability, repository access, and permission to create releases.
- [ ] Require a clean worktree or explicitly exclude unrelated changes before release preparation.
- [ ] Fetch tags and the target branch; confirm local HEAD is synchronized with the remote release branch.
- [ ] Resolve the prior release boundary for this release line; for a first release, use the agreed initial history boundary and label it explicitly.
- [ ] Inspect commits and full commit bodies from the previous release boundary to the proposed release commit.
- [ ] Read the affected manifests, authoritative documentation, installation instructions, configured catalogs, and user-facing migration notes when present.
- [ ] Treat commits and source diffs as evidence; use existing release notes only as secondary context.

### Version and Scope

- [ ] Use the repository's declared versioning policy; do not impose CalVer, SemVer, or a shared catalog version when none is specified.
- [ ] If the release target or tag is ambiguous, stop and ask instead of inventing a convention.
- [ ] Check the proposed tag locally and remotely. For a resumed approved release, verify its exact target and existing release state before continuing; otherwise treat a collision as a blocker, never overwrite it.
- [ ] Prepare version changes only in canonical fields identified by repository instructions; keep them local and reviewable until proposal approval.
- [ ] Update only packages, plugins, or components included in the release; do not bump unrelated manifests for visual consistency.
- [ ] Keep a new distribution unit at its approved initial version unless this release explicitly advances it.
- [ ] Ensure the tag, release title, and notes describe the same release unit; require manifest-version alignment only for versioned manifests included in that unit.
- [ ] Document breaking installation or behavior changes in the repository's required migration surface.

### Release Notes

- [ ] Read the most recent comparable releases and preserve useful house style without copying stale structure.
- [ ] Group changes by user outcome, not by file list or internal implementation chronology.
- [ ] Lead with why the release matters, then state the concrete behavior users receive.
- [ ] Include exact install or update commands only after verifying them against the current authoritative documentation and applicable distribution metadata.
- [ ] Include migration steps for every confirmed breaking change, with old and new behavior clearly separated.
- [ ] Mention removed behavior plainly; do not disguise removal as simplification.
- [ ] Credit external contributors by verified handle and omit a contributors section for solo work.
- [ ] Link to canonical documentation and repository paths that exist at the release commit.
- [ ] Exclude claims about adoption, performance, compatibility, or counts that cannot be reproduced.
- [ ] Distinguish measured facts from interpretation and future intent.

### Validation and Approval

- [ ] Run every repository release gate and the relevant product, package, plugin, skill, or marketplace checks for surfaces that exist.
- [ ] When multiple host catalogs exist and repository policy requires parity, confirm they remain aligned; preserve every stable distribution identifier unless migration was approved.
- [ ] When installation surfaces change, validate an isolated snapshot of the exact proposed tree before approval and identify its baseline and patch; after committing, verify that the release commit contains that validated tree.
- [ ] Record commands, versions, exit codes, and skipped checks without exposing secrets.
- [ ] Present the exact version changes, tag, title, full notes, validation evidence, and planned commands.
- [ ] Wait for explicit user approval of that exact proposal before committing version changes, tagging, or publishing.
- [ ] Reuse approval while version changes, target, tag, title, and notes remain exactly as approved; present changed publication content for renewed approval before publishing.

### Publication

- [ ] Reconcile prepared metadata and documentation with the approved proposal; apply any outstanding approved edits and exclude unrelated changes.
- [ ] Confirm required release gates cover the final approved tree; rerun only checks invalidated by final edits or unresolved failures.
- [ ] Commit and push the release commit using the authorized branch workflow.
- [ ] Confirm required CI succeeds on the release commit before creating the tag.
- [ ] Create an annotated or repository-standard tag pointing at the verified commit and push it without force.
- [ ] Create the GitHub Release from a file containing the approved notes to preserve Markdown and shell safety.
- [ ] Verify the published tag, target commit, title, body, and release URL through the hosting API.
- [ ] Test documented installation or update from the repository's documented release or distribution source when the release changes an installation surface.
- [ ] Do not publish npm, PyPI, NuGet, container, or other packages unless separately authorized.
- [ ] Do not create a community announcement as an implicit side effect.

### Failure Handling

- [ ] Before public tagging, diagnose failures and correct bounded preparation defects within scope; reuse approval only if the proposal is unchanged. Stop on unresolved prerequisites and preserve the exact state.
- [ ] If tag publication or release creation returns an uncertain result, inspect remote tag and release identity before retrying. Report partial state and resume only the missing approved operation; never create a duplicate or overwrite conflicting content.
- [ ] Never delete or move a published tag without explicit approval.
- [ ] Never overwrite an existing release or use force to conceal a bad release commit.

## Verdict

- `RELEASED` — tag and GitHub Release point to the verified commit and remote checks pass.
- `READY` — proposal and evidence are complete but publication awaits approval.
- `PARTIAL` — externally visible release state exists but verification or a later step failed.
- `BLOCKED` — release cannot proceed safely.

- [ ] Bind the published release to the checked commit, exact tag, and approved notes; do not infer application deployment or operational health from a GitHub Release.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Release scope, canonical version changes, tag/commit, title, full proposed notes before approval or release URL afterward, validation evidence, and publication state. For `PARTIAL`, enumerate every externally visible object and the approval needed before deleting, moving, or replacing it.
