---
name: release
description: Cuts a project release. Discovers the project's release procedure (Makefile target, RELEASING.md, CI workflow, etc.) and offers to capture it durably if missing. Always invokes /review-release as preflight, proposes a version bump from CHANGELOG, then presents an exact command plan for operator confirmation before executing step-by-step. Halts on first failure rather than attempting rollback.
model: opus
---

# Release - Cut a Project Release

Executes the project's release procedure with safety guards appropriate to a high-blast-radius operation. Discovers the procedure from the project itself rather than dictating one, always runs `/review-release` as preflight, and never pushes past a BLOCKER. Plans before executing; halts on first failure rather than guessing at recovery.

**Scope of action:** local repo and configured remotes. The skill pushes commits, pushes tags, and (when the procedure includes them) publishes to package registries. It does not attempt automatic rollback of partially-executed releases.

**Reversibility note:** local steps (version bump, commit, local tag) are reversible with `git reset` / `git tag -d`. The remote push is effectively irreversible once anyone has fetched. Package-registry publication is irreversible (most registries permit yank but not delete). The skill names each step's reversibility class in the plan.

## Philosophy

**High blast radius warrants high friction.** Tagging and pushing a release is the kind of action that should never happen by accident. The skill is generous with confirmation prompts and pessimistic about partial-failure recovery. Auto-execution is never the default.

**Composition, not duplication.** Preflight checking is `/review-release`'s job. This skill always invokes it and fail-stops on red. It does not re-implement the checklist or offer to skip it.

**Discover the procedure, don't invent it.** Release procedure is project-specific — `make release`, `npm publish`, `cargo publish`, `gh release create`, a custom CI workflow, or some combination. The skill searches the conventional surfaces before falling back to asking the user. If asked, it offers durable capture so the next release is fully automated.

**Halt on first failure.** Release sequences are not atomic. A failure halfway through (e.g., tag pushed but `npm publish` failed) leaves the project in a partial state. The skill stops at the first failure and surfaces the partial state for human decision rather than pushing through or guessing at rollback.

## Workflow Overview

```
┌────────────────────────────────────────────────────────┐
│                        RELEASE                         │
├────────────────────────────────────────────────────────┤
│  1. Detect repo context                                │
│  2. Discover release procedure                         │
│  3. If procedure not found: offer durable capture      │
│  4. Determine target version (propose from CHANGELOG)  │
│  5. Idempotence check (scan for partial prior run)     │
│  6. Run /review-release as preflight (fail-stop)       │
│  7. Construct release plan (commands + reversibility)  │
│  8. Present plan + confirm                             │
│  9. Execute step-by-step (one pause at local→remote    │
│     boundary; halt on first failure)                   │
│ 10. Final summary                                      │
└────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Detect Repo Context

Run all of the following; abort cleanly on any failure:

- **Is this a git repo?** `git rev-parse --is-inside-work-tree`. Abort if not.
- **Main branch detection.** Try `git symbolic-ref refs/remotes/origin/HEAD`, then check for `main`, then `master`. Ask the user if none detected.
- **Current branch.** `git branch --show-current`.
- **Working tree clean.** `git status --porcelain`. **Abort if dirty** with the suggestion: "Commit or stash before releasing." Releases from a dirty tree are unsafe.
- **Up-to-date with origin.** `git fetch`, then check `git rev-list --count HEAD..@{u}`. If behind, abort with the suggestion to pull. If ahead, note this (it's expected if the release commit is being prepared locally, but flag it).
- **On the main branch.** If current branch is not the main branch, ask the user to confirm intent — releasing from a non-main branch is unusual but valid (e.g., backport release lines). Do not abort; defer to the user.

### 2. Discover Release Procedure

Search the following surfaces in order. Stop at the first hit, but record every hit (procedure may span multiple surfaces — e.g., Makefile target + RELEASING.md narrative):

1. **Makefile** — parse for a `release`, `publish`, or `tag` target. Read the recipe.
2. **RELEASING.md** or **RELEASE.md** at repo root.
3. **CONTRIBUTING.md** — look for a section titled "Release", "Releasing", or "Cutting a Release".
4. **CLAUDE.md** (project-level) — look for the same.
5. **package.json** — scripts named `release`, `publish`, `prepublish*`, `version*`, `postversion`.
6. **pyproject.toml** / **Cargo.toml** / equivalent — packaging metadata that implies a publish step.
7. **`.github/workflows/release.yml`** or similar CI release config.
8. **Git tag history** — `git log --tags --simplify-by-decoration --pretty="format:%d %s"` to infer pattern from prior releases (tag format like `v1.2.3` vs `1.2.3`, accompanying commit message convention like `chore: release v1.2.3`).

Record what was found and where. **Prefer executable sources over prose** — a Makefile target is the authoritative procedure if it exists.

### 3. Offer Durable Capture if Missing

If step 2 found no procedure (no executable target, no prose doc, no CI workflow, no git-tag pattern beyond bare history):

- Tell the user no procedure was discoverable.
- Ask the user to describe the release steps in order.
- Once described, offer four options for where to record them:
  - **Makefile target** (Recommended) — executable, version-controlled, callable by humans and future skill invocations. Best for sequences of shell commands.
  - **RELEASING.md** — conventional prose home. Good when steps need narrative explanation or have human-judgment branches.
  - **CLAUDE.md** — only if the project doesn't have a Makefile and doesn't warrant a top-level doc. Adds to prompt context, so prefer the above two.
  - **Skip durable capture for this release** — proceed without recording.

If the user opts to record, write the file/target now and commit it as a **separate commit** before proceeding with the release (`chore: document release procedure`). The recording commit is part of pre-release hygiene, not part of the release itself.

If the user declines to describe the procedure, abort with the suggestion that they invoke the steps manually for this release and re-run `/release` next time once a procedure is documented.

### 4. Determine Target Version

- Read `CHANGELOG.md` (or equivalent — `CHANGES`, `HISTORY.md`, etc.) and locate the unreleased section.
- Inspect commits since the last tag (`git log <last-tag>..HEAD --oneline`) for breaking-change markers (`BREAKING CHANGE:`, `feat!:`, `fix!:`, etc.) and conventional commit types (`feat:`, `fix:`, `chore:`).
- Propose a semver bump:
  - **Major** if breaking-change markers present.
  - **Minor** if `feat:` commits but no breaking changes.
  - **Patch** otherwise.
- Present: "Last tag: vX.Y.Z. Proposing vA.B.C based on [N feat: commits / breaking change in commit abc1234 / no notable commits]. Confirm or override?"
- Validate the user's chosen version against the project's tag format convention (from step 2's tag-history inspection). If the convention is `vX.Y.Z` but the user typed `1.3.0`, normalize and confirm.

If no CHANGELOG exists, skip the proposal step and ask the user directly for the target version.

### 5. Idempotence Check

Scan for evidence of a partial prior run at the target version:

- **Local tag.** `git tag --list <target-tag>` — non-empty means a local tag already exists.
- **Remote tag.** `git ls-remote --tags origin <target-tag>` — non-empty means the tag was already pushed.
- **GitHub release** (if `gh` is available). `gh release view <target-tag>` — success means a GitHub release exists.
- **Package-registry publication** (best-effort; depends on procedure). For `npm`, `npm view <pkg>@<version>`. For `cargo`, the publish step itself will fail with a clear error.

If any artifact is found, surface it and present three options:
- **Resume from the next undone step** — the plan in step 7 will skip steps whose artifact exists. This is best-effort; the skill never tries to undo existing artifacts.
- **Abort and let the user clean up manually.**
- **Choose a different target version** (return to step 4).

### 6. Run Preflight (`/review-release`)

Announce the action: "Running `/review-release` as preflight."

Invoke `/review-release` with the target version. Wait for completion.

**Fail-stop on red.** If `/review-release` reports unresolved BLOCKERs, abort the release workflow:

> "Preflight failed with N BLOCKERs. Resolve them (or run `/implement` / `/bug-fix` to address) and re-run `/release`."

Do not present a "force release" option. The no-escape-hatches rule applies.

**Carry warnings forward.** If only WARNINGs remain after preflight, surface them in the plan presentation (step 8) so the user has the full picture when deciding whether to proceed.

If `/review-release` itself made changes (e.g., auto-removed debug artifacts) and the user committed them, the working-tree state has changed since step 1. Re-verify cleanness and up-to-date status before proceeding.

### 7. Construct Release Plan

Build an ordered command list from the procedure discovered in step 2 (or recorded in step 3) and the target version from step 4. For each step, record:

- The exact command.
- A reversibility class:
  - **reversible** — local file edits before any commit; `git checkout -- <file>` undoes.
  - **reversible-locally** — local commits and local tags; `git reset` / `git tag -d` undoes.
  - **irreversible-on-publish** — pushes to remote, package-registry publishes; effectively permanent once received downstream.
  - **partially-reversible** — GitHub releases (can be deleted but the notification has gone out).

Typical plan (customized to the discovered procedure):

1. Update version in **every** manifest file that carries a version field — **reversible**. Do not assume a single canonical manifest; multiple manifests routinely co-exist and must stay in lockstep. Common combinations:
   - npm: `package.json` (plus `package-lock.json` after `npm install`).
   - Rust: `Cargo.toml` (plus `Cargo.lock` after `cargo build`).
   - Python: `pyproject.toml` (plus `setup.py` / `setup.cfg` / `__version__` constants).
   - Go: typically a source-level version constant.
   - **Claude Code plugins: both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`** — the latter is the distribution artifact; the two must agree.
   - Any project: also bump version constants embedded in source code (`VERSION = "X.Y.Z"`), badges in README, and similar.

   Scan for files containing the current version string (`git grep -F "<old-version>"`) to catch occurrences the conventional list misses. Each hit is a potential bump site; include in the plan or explicitly justify excluding.
2. Update CHANGELOG.md unreleased section with version and date — **reversible**
3. Commit version bump (`chore: release vX.Y.Z`) — **reversible-locally**
4. Create annotated tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`) — **reversible-locally**
5. Push commit to origin — **irreversible-on-publish**
6. Push tag to origin — **irreversible-on-publish**
7. Publish to package registry (`npm publish`, `cargo publish`, etc.) — **irreversible-on-publish**
8. Create GitHub release (`gh release create vX.Y.Z --generate-notes`) — **partially-reversible**

If step 5's idempotence check found existing artifacts and the user chose "resume," mark already-done steps as `[skip]` rather than removing them — visible context for the user.

### 8. Present Plan + Confirm

Present the full plan in a single block:

```
## Release Plan: vX.Y.Z

Branch:     main (clean, up-to-date with origin)
Last tag:   v1.2.3
Preflight:  /review-release passed (2 warnings — see below)

Steps:
  1. [reversible]               Update package.json version → 1.3.0
  2. [reversible]               Update CHANGELOG.md (set date to 2026-05-18)
  3. [reversible-locally]       git commit -m "chore: release v1.3.0"
  4. [reversible-locally]       git tag -a v1.3.0 -m "Release v1.3.0"
  ───── local → remote boundary (final confirmation prompt before this line) ─────
  5. [irreversible-on-publish]  git push origin main
  6. [irreversible-on-publish]  git push origin v1.3.0
  7. [irreversible-on-publish]  npm publish
  8. [partially-reversible]     gh release create v1.3.0 --generate-notes

Preflight warnings (carried over from /review-release):
  - CHANGELOG: stale entries from v1.2.0 not removed
  - DEPENDENCY: foo-lib pinned to ^2.0.0 (security advisory CVE-2026-1234)

Proceed?
```

Use `AskUserQuestion`. Options:
- **Proceed** — execute steps 1-4, then pause at the boundary for a second confirmation before steps 5+.
- **Stop here** — abort the release. No changes made.

Do not offer "edit the plan inline." If the user wants different steps, they update the procedure source (Makefile, RELEASING.md) and re-run.

### 9. Execute Step-by-Step

For each step:

1. Announce: "Step N of M: <command>".
2. Execute.
3. Check exit status.
4. **On failure:** halt. Report the error, which steps completed, and which did not. **Do not attempt rollback** — partial release state is human-judgment territory. The summary in step 10 documents the partial state.

**One mid-execution pause: the local→remote boundary.** After the last `reversible-locally` step and before the first `irreversible-on-publish` step, pause and ask:

> "Local steps complete (version bumped, committed, tagged). About to push to remote — final confirmation?"

This is the only intra-execution prompt. If the user proceeds, execute the remaining steps without further prompts. If the user aborts, report the local-only state and exit cleanly — the user can `git reset --hard HEAD~1 && git tag -d vX.Y.Z` to fully undo, or push manually later.

### 10. Final Summary

**On success:**

```
## Release Complete: vX.Y.Z

### Executed (in order)
  1. Bumped version in package.json (1.2.3 → 1.3.0)
  2. Updated CHANGELOG.md (added date 2026-05-18 to unreleased section)
  3. Committed: "chore: release v1.3.0" (sha 7a8b9c0)
  4. Tagged v1.3.0
  5. Pushed main to origin
  6. Pushed tag v1.3.0 to origin
  7. Published to npm
  8. Created GitHub release v1.3.0

### Links
  - Tag:     https://github.com/<org>/<repo>/releases/tag/v1.3.0
  - npm:     https://www.npmjs.com/package/<pkg>/v/1.3.0

### Carry-over warnings (from preflight)
  - CHANGELOG: stale entries from v1.2.0 — consider addressing post-release
  - DEPENDENCY: foo-lib security advisory — consider an immediate patch release
```

**On halt mid-execution:**

```
## Release Halted: vX.Y.Z

### Completed
  1. Bumped version in package.json
  2. Updated CHANGELOG.md
  3. Committed: "chore: release v1.3.0" (sha 7a8b9c0) — local only
  4. Tagged v1.3.0 — local only

### Failed
  Step 5: git push origin main
  Error: permission denied (publickey)

### Current state
  - Local repo has the release commit and tag.
  - Neither commit nor tag is on origin.
  - No package-registry publication.
  - No GitHub release.

### Recovery options
  - Fix push authentication and re-run /release. The idempotence check will
    detect the local tag and offer to resume from step 5.
  - Or, to fully abandon this attempt:
      git tag -d v1.3.0
      git reset --hard HEAD~1
```

## Safety Invariants

The skill must never:

- Release from a dirty working tree.
- Release from a branch behind origin without the user explicitly pulling first.
- Skip the `/review-release` preflight.
- Push past a `/review-release` BLOCKER.
- Use `git push --force` or `git push --force-with-lease` for any release operation.
- Skip the local→remote boundary confirmation.
- Attempt automatic rollback of a partially-executed release. (Partial state requires human judgment; the skill reports and exits.)
- Offer a "force release" or "skip preflight" flag.
- Bump the version, commit, or tag *and* push in a single atomic operation that can't be paused at the boundary.

These invariants are categorical. The skill does not offer flags to override them.

## Abort Conditions

**Abort the workflow:**
- Not a git repository.
- Dirty working tree.
- Branch behind origin and user declines to pull.
- No release procedure discoverable and user declines to describe one.
- `/review-release` reports unresolved BLOCKERs.
- User declines the plan at step 8.
- User declines the local→remote boundary confirmation at step 9.
- Any step fails during execution.

**Do NOT abort for:**
- `/review-release` reports WARNINGs only (carry them forward into the plan).
- Idempotence check finds prior run artifacts (offer resume / abort / new version).
- Missing CHANGELOG (ask user for the target version directly; CHANGELOG isn't strictly required).
- Current branch is not main (ask user to confirm intent; backport releases are valid).

## Composition

- **Always invokes** `/review-release` as preflight (step 6). No shortcut, no skip.
- **Suggests** `/tidy-docs` if `/review-release` flagged stale documentation as a warning. Does not invoke automatically.
- **Suggests** `/bug-fix` or `/implement` if the user wants to address `/review-release` BLOCKERs before re-running.

`/release` is a leaf skill, not an orchestrator: it composes one sub-skill linearly. It does not iterate over multiple skills or make dynamic decisions across them.

## Example Session

```
> /release

Detected: main branch = "master", current = "master", working tree clean,
up-to-date with origin.

Discovering release procedure...
  ✓ Makefile target `release` found
  ✓ Tag convention from history: vX.Y.Z
  ✓ Conventional commit pattern: "chore: pre-release cleanup for vX.Y.Z"

Determining target version...
  Last tag: v10.0.0
  Commits since last tag: 12 (1 feat:, 3 fix:, 8 chore:/docs:)
  Proposing: v10.1.0 (minor bump — 1 feat: commit)

Confirm version?
> v10.1.0

Idempotence check... no prior artifacts for v10.1.0. Clean slate.

Running /review-release as preflight...

  [/review-release output streams]

  Preflight result: PROCEED WITH CAUTION — 2 warnings, 0 blockers.

## Release Plan: v10.1.0

Branch:     master (clean, up-to-date with origin)
Last tag:   v10.0.0
Preflight:  /review-release passed (2 warnings — see below)

Steps:
  1. [reversible]               Update version in .claude-plugin/plugin.json → 10.1.0
  2. [reversible]               Update version in .claude-plugin/marketplace.json → 10.1.0
  3. [reversible]               Update CHANGELOG.md (set date to 2026-05-18)
  4. [reversible-locally]       git commit -m "chore: release v10.1.0"
  5. [reversible-locally]       git tag -a v10.1.0 -m "Release v10.1.0"
  ───── local → remote boundary ─────
  6. [irreversible-on-publish]  git push origin master
  7. [irreversible-on-publish]  git push origin v10.1.0
  8. [partially-reversible]     gh release create v10.1.0 --generate-notes

Preflight warnings:
  - CHANGELOG: minor formatting inconsistency in v10.0.0 entry (pre-existing)
  - DOCS: README.md release count may be outdated

Proceed?
> Proceed

Step 1 of 8: Updating .claude-plugin/plugin.json version → 10.1.0... done.
Step 2 of 8: Updating .claude-plugin/marketplace.json version → 10.1.0... done.
Step 3 of 8: Updating CHANGELOG.md date → 2026-05-18... done.
Step 4 of 8: Committing... done (sha 4d5e6f7).
Step 5 of 8: Tagging v10.1.0... done.

Local steps complete (version bumped in both manifests, committed, tagged).
About to push to remote — final confirmation?
> Proceed

Step 6 of 8: git push origin master... done.
Step 7 of 8: git push origin v10.1.0... done.
Step 8 of 8: gh release create v10.1.0 --generate-notes... done.

## Release Complete: v10.1.0

### Executed
  1. Bumped version to 10.1.0 in .claude-plugin/plugin.json
  2. Bumped version to 10.1.0 in .claude-plugin/marketplace.json
  3. Updated CHANGELOG.md
  4. Committed: "chore: release v10.1.0" (sha 4d5e6f7)
  5. Tagged v10.1.0
  6. Pushed master
  7. Pushed tag v10.1.0
  8. Created GitHub release v10.1.0

### Links
  - Tag: https://github.com/chrisallenlane/claude-swe-workflows/releases/tag/v10.1.0

### Carry-over warnings
  - CHANGELOG: minor formatting in v10.0.0 entry (pre-existing)
  - DOCS: README.md release count may need update — consider /tidy-docs
```
