---
name: ln-61-repository-publisher
description: "Commits, pushes and remotely verifies authorized repository changes; does not create releases."
---

# Repository Publisher

**Goal:** Publish only changes the user has authorized, then verify the result from the remote source.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Scope, staging, history, and synchronization | Native Git CLI | Stop if equivalent Git evidence is unavailable |
| Repository validation | Project-native commands and installed validators | Documented manual checks |
| Remote branch and CI state | Authenticated hosting CLI or connector | Git remote evidence plus direct workflow URLs |
| Clean-source verification | Temporary clone and isolated host configuration when distribution surfaces changed | Remote raw files plus `BLOCKED` for required install evidence |
| Static-site verification | Deployment workflow plus direct HTTP request | Hosting API deployment state |
| Current marketplace behavior | Official host documentation | Mark assumptions and avoid destructive retries |

Prefer compact Git output first, then open the full diff for files that will be staged. Never pipe commands in a way that hides the failing exit code.

Use hosting APIs for remote facts and Git for repository facts. Local distribution or deployment state cannot prove that a remote consumer update works.

## Checklist

### Establish scope and evidence

- [ ] Confirm the user explicitly requested a commit and push and identify the intended branch.
- [ ] Read repository instructions, release rules, and the current branch policy before mutation.
- [ ] Check `git status -sb`, staged and unstaged diffs, untracked files, remotes, and recent commit style.
- [ ] Identify unrelated user changes; do not stage them without explicit whole-worktree authorization.
- [ ] Inspect deletions and generated files as carefully as edited text.
- [ ] Check whether behavior, installation commands, catalogs, layout, or the public site require matching documentation updates.
- [ ] Do not change versions, tags, or release metadata during an ordinary publication unless the request or repository policy explicitly includes them.
- [ ] For marketplace edits, confirm every stable identifier is unchanged unless an intentional migration was approved.
- [ ] When multiple host catalogs exist and repository policy requires parity, confirm they contain the same distribution units in the required order.
- [ ] When metadata is duplicated across manifests or catalogs, confirm descriptions and source paths agree with the canonical source.

### Validation Routing

- [ ] Discover and run repository-native validation commands before generic checks.
- [ ] For changed skills, run repository-required or host-native skill validators, or perform their documented manual fallback.
- [ ] For changed plugins or packages, run repository-required validators, or perform their documented manual fallback.
- [ ] Run every host-native strict validator whose distribution surface exists and changed or is required by repository policy.
- [ ] Run only the catalog parity, manifest parsing, stale-reference, local-link, and whitespace checks required by the repository and affected surfaces.
- [ ] Run only relevant product tests; do not invent a heavyweight release gate absent from repository policy.
- [ ] Stop before commit on a confirmed failing required check unless the user explicitly accepts the failure.
- [ ] Record skipped checks with the exact missing dependency or environment.

### Synchronization and Commit

- [ ] Fetch the target remote and compare local HEAD with the remote branch before committing.
- [ ] If behind or diverged, inspect both sides and reconcile within the authorized branch workflow while preserving user changes; stop for unresolved semantic conflicts or a required history rewrite. Never force-push implicitly.
- [ ] Stage explicit paths when the worktree is mixed; use whole-worktree staging only when the user approved all changes.
- [ ] Review the cached diff and diffstat after staging.
- [ ] Exclude secrets, local caches, temporary artifacts, and unintended credentials from the staged set without deleting user-owned files; if an intended change contains a secret, block that publication and report redacted evidence.
- [ ] Match the repository's commit-message convention and summarize the entire staged change.
- [ ] Preserve configured commit signing and attribution policy; do not invent contributor identities or disable required signing.
- [ ] Create the commit and capture its full SHA.
- [ ] Push to the authorized branch without changing branch protections or using force.

### Remote Verification

- [ ] Verify the published commit on the authorized remote through Git or the hosting API; use a second source only if identity or synchronization is uncertain.
- [ ] Track required CI for the pushed commit with bounded waits and direct run URLs. If execution cannot continue waiting, report pending state as `PARTIAL`; do not equate pending with success.
- [ ] If the static site changed, wait for deployment and verify live content with a cache-busting request.
- [ ] If installation or marketplace content changed, clone an authorized consumer-accessible remote into a clean temporary directory and validate the affected distribution surface.
- [ ] When install or update behavior changed, test at least one affected package or plugin from its documented distribution source in isolated host configuration.
- [ ] When stable distribution identifiers or versions exist, verify the installed artifact resolves under the expected identifier and version.
- [ ] Keep temporary host configuration isolated from the user's active settings and remove it safely afterward.
- [ ] Recheck local worktree and HEAD against the published commit. If the remote advanced concurrently, verify that it still contains the published commit and report both SHAs; do not overwrite newer work to restore equality.

### Safety Gates

- [ ] Never expose authentication tokens or credential values in output.
- [ ] Never create a release, tag, package publication, discussion, or pull request unless explicitly requested.
- [ ] Never delete remote branches or alter the default branch as a side effect.
- [ ] Return `BLOCKED` rather than bypassing branch protection, authentication, or required checks.

## Verdict

- `PUBLISHED` — commit, push, required CI, and applicable remote verification succeeded.
- `PARTIAL` — the push succeeded but a non-destructive remote check is pending or failed.
- `BLOCKED` — publication did not complete because authorization, synchronization, validation, or remote access failed.

- [ ] Verify remote publication refers to the exact checked source state and exclude unverified later changes; repository publication alone does not prove a release or deployment.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Published/excluded paths, branch, full commit SHA, remote URL, validation results, CI/deployment URLs, and applicable clean-source install/update proof. For `PARTIAL`, state whether the pushed commit is safe to leave and the observable event that closes verification. Use `PUBLISHED` only when the remote commit and every applicable required workflow are observed.
