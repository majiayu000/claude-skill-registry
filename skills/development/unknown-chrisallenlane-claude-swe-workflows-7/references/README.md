# /release — Cut a Project Release

## Overview

The `/release` skill executes the project's release procedure with safety guards appropriate to a high-blast-radius operation. It discovers the procedure from the project (Makefile, RELEASING.md, CI workflow, git tag history) rather than dictating one, always invokes `/review-release` as preflight, and never pushes past a BLOCKER. It plans before executing and halts on first failure rather than guessing at recovery.

The skill sits in the same conceptual lane as `/review-release` but on the opposite side of the act/check seam: `/review-release` is advisory (it tells you whether the release is ready), `/release` is the mutator (it actually cuts the release). The two are designed to compose — `/release` always runs `/review-release` internally as preflight, so the user does not need to run them in sequence manually.

**Scope:** local repo and configured remotes. The skill pushes commits, pushes tags, and (when the procedure includes them) publishes to package registries and creates GitHub releases. It does not attempt automatic rollback of partially-executed releases.

**Key benefits:**
- One pass replaces the manual sequence of version-bump, commit, tag, push, publish, release-create.
- Discovers the project's release procedure rather than imposing a one-size-fits-all flow.
- Always preflight-checked via `/review-release`; no shortcut, no skip flag.
- Reversibility-annotated plan: every step labeled with its rollback class so the user knows what's at stake at each line of the plan.
- Halts on first failure with an honest report of partial state, rather than improvising recovery.

## When to Use

**Use `/release` for:**
- Cutting a new project release after the work for that version is merged to the main branch.
- Re-attempting a release that previously halted mid-execution (the idempotence check will detect prior artifacts and offer to resume).
- Releases of any kind — patch, minor, major, pre-release. The skill is version-agnostic.

**Don't use `/release` for:**
- Investigating whether a release is ready. Use `/review-release` directly — it's advisory.
- Rolling back a published release. Once a tag is on origin and a package is on the registry, recovery is human-judgment territory; the skill does not attempt it.
- Hotfix releases that need to bypass `/review-release`. There is no bypass — if `/review-release` reports a BLOCKER, fix it or abort. "We need to ship this broken thing right now" is not the skill's contract.

**Rule of thumb:** if the operation cuts a versioned, tagged, publicly-published artifact from a clean, preflight-passing state, `/release` handles it. If the operation does anything else — investigating, rolling back, bypassing checks — use the underlying tools directly.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /release Workflow                                               │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. DETECT REPO CONTEXT                      │
 │  ────────────────────────────────────────    │
 │  • Git repo present                          │
 │  • Main branch detected                      │
 │  • Working tree clean (abort if dirty)       │
 │  • Up-to-date with origin                    │
 │  • On main branch (confirm if not)           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. DISCOVER RELEASE PROCEDURE               │
 │  ────────────────────────────────────────    │
 │  Search in order: Makefile → RELEASING.md →  │
 │  CONTRIBUTING.md → CLAUDE.md → package.json  │
 │  → pyproject.toml / Cargo.toml → CI workflow │
 │  → git tag history                           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. OFFER DURABLE CAPTURE (if not found)     │
 │  ────────────────────────────────────────    │
 │  Makefile target (Recommended) → RELEASING.md│
 │  → CLAUDE.md → Skip for this release         │
 │  Recording lands as a separate commit.       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. DETERMINE TARGET VERSION                 │
 │  ────────────────────────────────────────    │
 │  Read CHANGELOG + conventional-commit scan;  │
 │  propose semver bump; user confirms.         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. IDEMPOTENCE CHECK                        │
 │  ────────────────────────────────────────    │
 │  Local tag? Remote tag? GitHub release?      │
 │  Registry publication? Offer resume/abort/   │
 │  new-version if any artifact exists.         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. PREFLIGHT (/review-release)              │
 │  ────────────────────────────────────────    │
 │  ALWAYS invoked. Fail-stop on BLOCKERs.      │
 │  Carry WARNINGs forward into the plan.       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. CONSTRUCT RELEASE PLAN                   │
 │  ────────────────────────────────────────    │
 │  Ordered command list with reversibility     │
 │  annotation per step.                        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  8. PRESENT PLAN + CONFIRM                   │
 │  ────────────────────────────────────────    │
 │  Show all steps in a single block; user      │
 │  proceeds or aborts. No inline-edit option.  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  9. EXECUTE STEP-BY-STEP                     │
 │  ────────────────────────────────────────    │
 │  One pause: at the local → remote boundary.  │
 │  Halt on first failure; no rollback attempt. │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │ 10. FINAL SUMMARY                            │
 │  ────────────────────────────────────────    │
 │  On success: executed steps + links + carry- │
 │  over warnings.                              │
 │  On halt: completed + failed + current state │
 │  + recovery options.                         │
 └──────────────────────────────────────────────┘
```

## The Reversibility Tiers

Every step in the plan is annotated with one of four reversibility classes. The classes are not arbitrary — they correspond to materially different recovery profiles:

 | Tier                         | Examples                                                  | How to undo                                                                                                            |
 | ---------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
 | `reversible`                 | File edits to `package.json`, CHANGELOG.md before commit  | `git checkout -- <file>`                                                                                               |
 | `reversible-locally`         | Local commit, local tag (`git commit`, `git tag`)         | `git reset --hard HEAD~1`, `git tag -d <name>`                                                                         |
 | `irreversible-on-publish`    | `git push`, `npm publish`, `cargo publish`                | Cannot be undone once anyone has fetched / installed. Some registries permit yank-but-not-delete.                      |
 | `partially-reversible`       | `gh release create`                                       | The GitHub release can be deleted, but notifications have already gone out and consumers may have started downloading. |

The plan's presentation places a visible boundary line between the last `reversible-locally` step and the first `irreversible-on-publish` step. That boundary is the **one** mid-execution confirmation pause the skill performs — see [The Local → Remote Boundary](#the-local--remote-boundary) below.

## Why Discover, Don't Dictate

Different projects have different release procedures. Examples from real codebases:

- **Pure-Go binary distributed via GitHub releases:** version constant in source → commit → tag → push → `goreleaser` builds and uploads.
- **npm library:** bump `package.json` → CHANGELOG → commit → tag → push → `npm publish` → `gh release create`.
- **Rust crate:** bump `Cargo.toml` → commit → tag → push → `cargo publish`.
- **Python package on PyPI:** bump `pyproject.toml` → CHANGELOG → commit → tag → push → `python -m build` → `twine upload`.
- **Claude Code plugin (this repo):** bump **both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` → CHANGELOG → commit → tag → push. The two manifests both carry a `version` field and must agree — `marketplace.json` is the distribution artifact for `claude plugin marketplace add` and is easy to forget if `plugin.json` is treated as canonical.
- **Internal monorepo with custom release scripts:** `make release` or `./scripts/release.sh` orchestrates everything.

A skill that hard-codes any one of these flows will be wrong for the other five. So `/release` searches the project's own artifacts in priority order — preferring executable sources (Makefile targets, npm scripts, CI workflows) over prose (RELEASING.md) over inference (git tag history).

The search order is **executable > prose > inferred**:

1. **Executable** sources (Makefile target, package.json script, CI workflow) are authoritative because they're what would actually run if invoked manually.
2. **Prose** sources (RELEASING.md, CONTRIBUTING.md release section, CLAUDE.md) are next because they're human-curated but require interpretation.
3. **Inferred** patterns (git tag history) are the fallback — they tell you the tag format and commit-message conventions but not the publication steps.

If none of those exist, the skill asks the user and then offers durable capture, again preferring the executable home (a Makefile target) over the prose home (RELEASING.md) over the prompt-context home (CLAUDE.md). The principle: **next time, the procedure should be discoverable without the user describing it again.**

## /review-release is a Hard Gate

`/release` always invokes `/review-release` as preflight (workflow step 6). This is a categorical design choice — there is no skip flag, no recently-run-cache, no "force release" override.

The rationale:

- **Skill invocation history is a fragile signal.** Whether `/review-release` ran earlier in the session does not tell us whether the working tree is still in the state that passed.
- **The cost of always running is small.** `/review-release` is fast on a clean tree. If it isn't, that's a `/review-release` problem to solve in that skill.
- **The cost of skipping wrongly is large.** A release that should have caught a debug artifact, a version mismatch, or a CHANGELOG gap, but didn't, ships the defect to users.
- **An escape hatch invites misuse.** A `--force` flag exists to be used. Once it exists, people use it in situations where they shouldn't. Better to have no flag and require the user to explicitly fix or abort.

The asymmetry here is intentional: the preflight imposes friction proportional to the irreversibility of the action it gates.

## The Local → Remote Boundary

The release plan is laid out so all `reversible` and `reversible-locally` steps happen first, then a visible boundary, then all `irreversible-on-publish` and `partially-reversible` steps. After the user confirms the plan (workflow step 8), the skill executes the local steps without intra-step prompts. At the boundary, it pauses:

> "Local steps complete (version bumped, committed, tagged). About to push to remote — final confirmation?"

This is the **one** mid-execution confirmation. It exists because:

- The boundary corresponds to a real semantic transition. Before it: everything can be `git reset`'d away. After it: anything pushed is in the wild.
- A single pause at the meaningful boundary is less friction than per-step prompts, and more useful than no pause at all.
- It gives the user a final chance to inspect local state (`git log`, `git show vX.Y.Z`) before publishing.

If the user aborts at the boundary, the release is **partial** — the local commit and tag exist but were never published. The skill reports this honestly and exits. The user can either:
- Push later manually with `git push origin <main>` and `git push origin <tag>`, or
- Abandon with `git tag -d <tag>` and `git reset --hard HEAD~1`.

## No Rollback Attempt on Failure

If any step fails during execution, the skill halts and reports the partial state. It does **not** attempt automatic rollback. The reasons:

- **Recovery is judgment-laden.** If `npm publish` succeeds but `gh release create` fails, the right next step depends on what the team values — re-attempting the GitHub release, manually creating it, or accepting the gap.
- **Wrong rollback is worse than no rollback.** A failed push might be a transient network error; rolling back the local tag would force a re-tag with a potentially different SHA on retry.
- **Partial state is informative.** The user benefits from seeing exactly which steps completed and which didn't, with the project in a state they can inspect with familiar tools (`git log`, `git tag`, `gh release list`).

The skill's job at failure is to **stop, surface, and step away**. The user's job is to decide what to do next.

The final summary on a halted release lists:

1. **Completed steps**, with the SHA / artifact / state each created.
2. **The failed step**, with the exact error.
3. **Current state**, broken down by location (local repo, remote, registry, GitHub).
4. **Recovery options**, both "resume the release" and "abandon" — concrete commands.

## Safety Invariants (Categorical)

These are categorical, not configurable. The skill does not offer flags to override them:

- Never release from a dirty working tree.
- Never release from a branch behind origin without an explicit pull first.
- Never skip the `/review-release` preflight.
- Never push past a `/review-release` BLOCKER.
- Never use `git push --force` or `git push --force-with-lease` for a release operation.
- Never skip the local → remote boundary confirmation.
- Never attempt automatic rollback of a partially-executed release.
- Never offer a "force release", "skip preflight", or "ignore blockers" flag.

The principle: a high-blast-radius skill must be safer than the underlying commands it composes. If the user wants to bypass any of these, they invoke the underlying commands directly — the friction of typing them out is the safety mechanism.

## Tips for Effective Use

1. **Run `/release` instead of `/review-release; /release`.** The latter is the obvious sequence, but `/release` already invokes `/review-release` internally. Running it twice is redundant and forces you through the interactive parts of `/review-release` twice.

2. **Capture the procedure on the first run.** When the skill asks where to record the release procedure, choose **Makefile target** unless the procedure has substantive narrative (branching decisions, judgment calls, post-release checklist). A `make release` target is the most ergonomic durable home — humans run it directly, future `/release` invocations discover it automatically.

3. **Pause and read the plan.** The plan presentation is the high-leverage decision point. Reading it carefully — especially the reversibility annotations — is much more valuable than reading the per-step output during execution.

4. **Treat the boundary confirmation as the last off-ramp.** Once the boundary is past, recovery is hard. If anything about the plan, the tag, or the local state looks wrong, abort there. The local commit and tag are easy to discard.

5. **On a halted release, prefer resume over abandon.** The idempotence check exists to make re-running `/release` after a halt safe. If you just fix the underlying error (auth, network, registry credentials) and re-run, the skill will pick up from where it stopped. Abandoning and re-attempting from scratch is rarely necessary.

6. **Don't use `/release` to ship something `/review-release` says is broken.** That's not what the skill is for. If the BLOCKER is wrong (false positive in `/review-release`), fix `/review-release`. If the BLOCKER is right, fix the underlying issue. There's no third option.

## Example Session

See the [SKILL.md](../SKILL.md#example-session) for a full worked example.

## Edge Cases and Failure Modes

**No release procedure discoverable and user declines to describe one.** The skill aborts cleanly with the suggestion that the user invoke the steps manually for this release and re-run `/release` next time once a procedure is documented.

**Branch is not main.** The skill confirms intent rather than aborting — backport release lines (e.g., releasing v1.x.x from `release/1.x` while main is on 2.x) are a valid case. The user confirms; the skill proceeds.

**No CHANGELOG.** The version-bump proposal step skips the CHANGELOG-driven semver inference and asks the user directly. No CHANGELOG is a missing-information signal, not a blocker.

**`/review-release` itself made changes (auto-fixes) and the user committed them.** The working-tree state has shifted since step 1's context detection. The skill re-verifies cleanness and up-to-date status before proceeding to plan construction.

**Local tag exists but was not pushed.** Idempotence check detects this. The user can resume from the push step. The skill does not delete the local tag.

**Remote tag exists but no GitHub release.** Same — resume from `gh release create`. The skill does not delete the remote tag.

**Package-registry publish step fails mid-way (e.g., `npm publish` rejected for a name conflict).** The skill halts. The current state is: commit + tag pushed, registry rejected. The user must decide whether to choose a different package name (requires version bump and re-tag), contact the registry, or abandon. The skill does not guess.

**User aborts at the local → remote boundary.** Reported as a clean halt: local commit and tag exist, nothing pushed. Recovery options listed.

**`gh` command not available.** GitHub release creation step is dropped from the plan with a note. The user can create the release manually via the web UI.

**Working tree was clean at step 1 but is now dirty at execution time.** This is unusual (the user would have had to make changes during the planning phase). The skill detects this on step 1 of execution and halts — the plan was built against a different tree state.

**`/review-release` reports BLOCKERs.** The skill aborts with the suggestion to address them and re-run. No force-through option exists.
