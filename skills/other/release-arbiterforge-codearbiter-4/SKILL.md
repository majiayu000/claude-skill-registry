---
name: release
description: The single permitted path to a version tag, for any of the four independently-versioned plugins. Routed to when the user invokes /release on a non-default branch with a green suite. Takes the target plugin as its one argument (default ca), derives the SemVer bump from Conventional-Commits history since that plugin's last tag, rolls the commits into that plugin's CHANGELOG, writes an annotated tag in that plugin's namespace, and on authorization publishes it as a GitHub Release with the changelog section as its notes. A release commit, if needed, routes through commit-gate; the tag and Release are never published without explicit authorization.
---

# release

The single permitted path to a version tag. Routed to when the user invokes `/release [target]`. Derive the bump from the commit log, update the changelog, tag — nothing more.

**One command, four plugins.** `/release` takes the target plugin as its only argument and defaults to **`ca`**, so a bare `/release` behaves exactly as it always has. `/release ca-pi` releases ca-pi. There is deliberately no second command per plugin: four commands would be four public surfaces to govern, catalog, and carry, for one operation whose only difference is which row of the table below it reads.

Every phase below is written once, against that row. Nothing in this skill is per-plugin prose.

## Targets

Resolve the row for `$TARGET` FIRST and use it throughout. `$TAG_PREFIX` comes from the shared register, never typed from memory: `TAG_PREFIX=$(python3 .github/scripts/_releaselib.py tag-prefix $TARGET)` — the same `_releaselib.RELEASE_TAG_PREFIXES` the hosted `release` workflow's lanes are asserted against, so the command and the workflow cannot disagree about a namespace.

| `$TARGET` | `$TAG_PREFIX` | `$MANIFEST` | `$CHANGELOG` | `$PAYLOAD` (window scope) | `$ARTIFACTS` (rebuild + assert clean) | `--latest` |
|---|---|---|---|---|---|---|
| `ca` | `v` | `plugins/ca/.claude-plugin/plugin.json` | `CHANGELOG.md` | `plugins/ca/` | `plugins/ca/tools/farm.js` | **yes** |
| `ca-codex` | `ca-codex-v` | `plugins/ca-codex/.codex-plugin/plugin.json` | `plugins/ca-codex/CHANGELOG.md` | `plugins/ca-codex/` | none | no |
| `ca-sandbox` | `ca-sandbox-v` | `plugins/ca-sandbox/.claude-plugin/plugin.json` | `plugins/ca-sandbox/CHANGELOG.md` | `plugins/ca-sandbox/` | `plugins/ca-sandbox/tools/sandbox.js`, `plugins/ca-sandbox/tools/claude-inside.js` | no |
| `ca-pi` | `ca-pi-v` | `plugins/ca-pi/package.json` **and** the repo-root `package.json` | `plugins/ca-pi/CHANGELOG.md` | `plugins/ca-pi/` (excluding `tools/`) | `plugins/ca-pi/extensions/codearbiter.js`, `plugins/ca-pi/extensions/codearbiter-child.js` | no |

Three of these rows carry a trap worth stating rather than discovering:

- **`ca-pi` has TWO manifests.** Pi installs the repository ROOT as the package (`pi install git:github.com/arbiterForge/codeArbiter@ca-pi-v<version>`), so the root `package.json` is what a consumer's install actually reads. It is GENERATED — regenerate it with `python3 tools/build-host-packages.py`, never hand-edit it — and it must equal `plugins/ca-pi/package.json` before tagging, or the tag installs a package claiming a version the tag does not name.
- **`ca-pi`'s payload excludes `tools/`.** `plugins/ca-pi/tools/` holds TypeScript sources, a vitest config, and a lockfile, none of which run on an installed machine (`.github/scripts/payload_scope.py` owns this rule). Its *built* bundles under `extensions/` do ship and are in scope.
- **Only `ca` takes `--latest`, and every sibling must pass `--latest=false` EXPLICITLY.** Omitting the flag is not declining it: GitHub defaults `make_latest` to true for any non-prerelease, so a sibling that simply does not ask for the badge still takes it. That is not hypothetical — the first `ca-pi` release displaced `ca`'s from the position every visitor sees, because the hosted lane omitted the flag rather than refusing it. GitHub has one repo-wide "Latest" and this repo ships four series.

## Pre-flight

**This repo ships four independently-versioned plugins** (ADR-0007 for the sibling split, ADR-0011 for the Codex host), each with its own tag series, payload path, manifest, and changelog. A sibling's tag or commit MUST NOT influence `$TARGET`'s version, window, or changelog — that isolation is what the table's per-row scoping buys, and it is the single most common way a release goes wrong.

Read these, or STOP and surface the gap — never guess:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — the default-branch name and project context.
- `$TARGET` must be one of the four rows above. An unrecognised target STOPs; do not guess which plugin was meant.
- `git status` must be clean. A dirty tree STOPs — commit or stash via `commit-gate` first.
- The current branch MUST NOT be `main`, `master`, or the default branch. Release lands through the normal branch/PR path; if HEAD is the default branch, STOP.
- **Resolve `LAST_TAG` from `$TARGET`'s series only** — never bare `git describe --tags --abbrev=0`, which returns the nearest tag by commit-graph *ancestry* and in this multi-plugin repo routinely resolves to another plugin's tag, silently basing the entire release on the wrong baseline. Resolve it through the tested helper, never a hand-rolled grep: `LAST_TAG=$(git tag -l | python3 .github/scripts/_releaselib.py last-tag $TAG_PREFIX)`. `_releaselib.last_tag_select` returns the highest `$TAG_PREFIX`-prefixed `MAJOR.MINOR.PATCH`, excluding pre-releases (`-beta`/`-rc`/`-alpha`), or `<none>`; its series isolation is a property of an ANCHORED match, so no series can resolve another's tag (pinned by `.github/scripts/test_release_lib.py`). No matching tag → `LAST_TAG=<none>`, treat the full history as the window, base version `0.0.0`. A series with no tag yet is normal, not an error.
- **Scope the release window to `$PAYLOAD`:** the commit set is `git log LAST_TAG..HEAD -- $PAYLOAD`, NOT the whole repo — a `feat(ca-sandbox)` commit must not bump `ca` or land in ca's changelog, and vice versa. This payload-scoped set must be non-empty; if empty, STOP — nothing to release for `$TARGET`.
- **Manifest read:** read the `version` field of `$MANIFEST`. Phase 1 asserts the derived bump equals it and updates it — a tag whose version runs ahead of the manifest ships nothing, because `claude plugin update` no-ops on an unchanged version string. For `ca-pi`, both manifests count.
- **`$ARTIFACTS` freshness — rebuild unconditionally:** every release, regardless of whether the sources changed in the window, rebuild and assert every committed bundle in `$ARTIFACTS` is in sync (`cd` into that plugin's `tools/` and `npm run build`, or `node build.mjs` for ca-pi, then `git diff --quiet -- <each artifact>`). A non-empty diff means a shipped bundle is stale — a release blocker, because the plugin ships the built file, not its source; commit the rebuild through `commit-gate` before tagging. Scope is `$TARGET` only: another plugin's stale bundle is that plugin's release problem, not this one's. The mechanical backstop is CI's per-plugin `tools` job; this local check is the belt to that suspenders. (The old form gated the rebuild on an in-window source change and so missed a bundle that went stale *before* the window.)

## Phase 1 — Version & changelog · gate: BLOCK

Derive the bump mechanically from the commit log; do not guess it.

1. Read every commit in the `$PAYLOAD`-scoped window: `git log LAST_TAG..HEAD --pretty=format:%H%n%s%n%b%n---- -- $PAYLOAD` (the path scope is load-bearing — it excludes every sibling's commits from the bump and changelog).
2. Classify each subject by its Conventional-Commits prefix and apply the highest-precedence bump:
   - `BREAKING CHANGE:` footer or `!` after the type/scope → **major**.
   - else any `feat` → **minor**.
   - else any `fix`, `perf`, `refactor` → **patch**.
   - `test` / `docs` / `chore` / `ci` only → no bump. If the whole window is non-bumping, STOP — there is nothing to release.
3. Compute the next version, confirm it is strictly greater than `LAST_TAG`, and assert it **equals** the `version` in `$MANIFEST` (for `ca-pi`, in BOTH manifests). If the manifest lags the derived bump, bump it now — that is a precondition of tagging (Pre-flight), not an afterthought; a tag ahead of the manifest ships nothing. Present the version and the per-commit classification to the user for confirmation.
4. Derive the release date **once** — `RELEASE_DATE=$(date +%F)` — and reuse that single value for the changelog header, the Phase-2 `Released-at:` footer, and the Phase-3 Release; never hand-type the date a second time (`_releaselib.release_dates_consistent` verifies the changelog-header date equals the `Released-at:` date). Roll the `CHANGELOG:` footers from each `feat` / `fix` / `perf` commit into a new `## [MAJOR.MINOR.PATCH] — $RELEASE_DATE` section in `$CHANGELOG` (the Keep-a-Changelog bracket heading the repo ships and the `_releaselib` guards match, not the bare `v`-prefixed form), grouped Added / Fixed / Performance. Prior sections stay intact. Create the file with a `# Changelog` heading if absent. **A `feat`/`fix` commit missing its `CHANGELOG:` footer is a BLOCK**, not a soft finding: surface the `[NEEDS-TRIAGE]` and STOP — never auto-fill, and never tag a changelog that silently drops a user-visible change. The changelog is a user-facing deliverable: apply `${CLAUDE_PLUGIN_ROOT}/includes/anti-slop-design/core.md` §3.A (no prose-separator em-dashes in the entry prose) and §3.B (copy self-audit), and the `medium-documents` §7.A.1 changelog guidance, to each rolled entry.
5. **Sync `$TARGET`'s release surfaces to the repo — mechanically derived, never typed.** Update `$MANIFEST`'s `version` in every case. Then, additionally:
   - **`ca`** — the README version badge (`version-X.Y.Z`); the command / skill / agent **count** badges and every prose echo of those counts (e.g. "N commands", the `commands/ (N)` tree line). Derive each count from the repo, never increment by hand: `commands = ls plugins/ca/commands/*.md | grep -v INDEX | wc -l`, `skills = ls -d plugins/ca/skills/*/ | wc -l`, `agents = ls plugins/ca/agents/*.md | grep -v INDEX | wc -l`. Then assert the canonical catalog `plugins/ca/COMMANDS.md` enumerates exactly those command files, and that the README full-catalog table lists every one of them (the `/ca:commands` body at `plugins/ca/commands/COMMANDS.md` renders from the canonical catalog and holds no rows of its own — do not treat it as a second catalog).
   - **`ca-pi`** — regenerate the root `package.json` with `python3 tools/build-host-packages.py` and assert it now equals `plugins/ca-pi/package.json`. Never hand-edit it: it is generated metadata, and the release guard checks that it moved together with the plugin manifest.
   - **`ca-codex`, `ca-sandbox`** — the manifest only; neither owns a README badge or count surface.

   A badge, prose-count, README-table, catalog, or root-manifest drift is a **BLOCK** — reconcile it before tagging. CI's badge-consistency guard (`.github/scripts/check_badge_consistency.py`) and the per-plugin version-bump gates are the mechanical backstop; if either is red, this step is not done.
6. If the changelog edit or the surface sync needs to land as a commit before tagging, route it through `commit-gate`. Do not reimplement the commit path here.

Gate: version confirmed, strictly monotonic within `$TARGET`'s series, matching the commit log, and equal to `$MANIFEST` (both, for ca-pi); `$CHANGELOG` updated; `$TARGET`'s surfaces reconciled to the repo. BLOCK if the classification disagrees with the log, the window is non-bumping, a bumping commit's `CHANGELOG:` footer is missing, or any surface drifts.

## Phase 2 — Tag & report · gate: BLOCK

1. Compose the annotated tag from the Phase 1 section plus a `Released-at: $RELEASE_DATE` footer (the same date derived once in Phase 1; `_releaselib.release_dates_consistent` must pass against the changelog section). Tag with `git tag -a ${TAG_PREFIX}MAJOR.MINOR.PATCH -F <message-file>` — never `-m` for multi-line content, never an interactive editor. **If the tag already exists, do not flatly abort — classify the state** with `_releaselib.classify_publish_state` via `python3 .github/scripts/_releaselib.py classify <tag_exists> <tag_sha> <head_sha> <tag_version> <manifest_version> <release_nondraft>`: `abort_mismatch` (tag points at a non-HEAD commit, or its version disagrees with the manifest) → STOP; `already_published` (a non-draft Release already exists on the tag) → nothing to do; `resume_publish` (tag already at HEAD with the matching version but no Release) → skip re-tagging and resume at Phase 3 to create the missing Release.
2. Report: `$TARGET`, version, bump rationale, the per-commit classification, the changelog section, and the tag SHA.
3. MUST NOT push the tag or create the GitHub Release here. Publication is Phase 3, a separate step the user authorizes after reading the report.

Gate: the annotated tag exists locally and the report is delivered. Nothing is published.

## Phase 3 — Publish · gate: STOP

The tag and the GitHub Release publish together, and only after the user explicitly authorizes publication. This phase does not run until then; absent authorization, nothing leaves the local repo.

**Prefer the hosted lane when it is available.** The `release` workflow carries the same four targets and enforces structurally what the steps below can only ask you to do: a read-only preflight that holds no write token resolves exactly one target, merge readiness must be green for the exact commit being tagged, and the publish is idempotent by construction. Dispatch it from the default branch with `$TARGET`'s version in that target's confirmation input and every other input blank. The steps below are the local equivalent for when a dispatch is not available — same guards, weaker enforcement, so follow them exactly.

On authorization:

1. Push the tag: `git push origin ${TAG_PREFIX}MAJOR.MINOR.PATCH`.
2. **Guard the notes-file first:** assert its first heading matches the tag — `python3 .github/scripts/_releaselib.py notes-match ${TAG_PREFIX}MAJOR.MINOR.PATCH <Phase-1 section file>` (exit 0). A stale notes-file (`_releaselib.notes_heading_matches` False) would publish the wrong changelog section under the right tag — STOP on mismatch. Then create the GitHub Release from the **same changelog section composed in Phase 1** — reuse it as the notes, never re-derive or hand-write them. **`--latest` follows the table:** assert it only for `ca`, and only when this tag is also the newest release across all four series (compare against `gh release list`); for every sibling pass `--latest=false`. GitHub has one repo-wide "Latest" and this repo ships four series, so a sibling claiming it hides ca's current release from every visitor. `gh release create ${TAG_PREFIX}MAJOR.MINOR.PATCH --title "<title>" --notes-file <Phase-1 section file> --latest[=false] --verify-tag`. The title convention is `<$TARGET display name> MAJOR.MINOR.PATCH: <summary>` — `codeArbiter X.Y.Z: …` for ca, `ca-pi X.Y.Z: …` for ca-pi — with no em-dash separator.
3. Handle edge cases explicitly, never silently: if a Release for the tag already exists, report it and skip creation (the tag push may already have landed); if `gh` is missing, unauthenticated, or the call fails, STOP and print the exact `gh release create` command so publication can be finished by hand rather than left half-done.
4. **Verify publication — never assume it.** Read the Release back: `gh release view ${TAG_PREFIX}MAJOR.MINOR.PATCH --json url,isDraft,tagName`. STOP unless it returns a **non-draft** Release on the correct tag; `gh release create` can partially succeed (tag pushed, Release rejected for an empty notes-file or a permissions/`--verify-tag` race), and an unverified publish is not a published release. Report the Release URL only once the read-back confirms it.
5. **Record the tag's provenance (issue #386).** A git tag is a mutable ref, and the commit a tag was *originally* published at is not recoverable from the API once it moves — a moved tag looks exactly like a tag that was always there. So write it down: add the new tag to `.github/published-tags.json` under `tags`, as `{"object_sha": <the ref's sha>, "object_type": "tag", "commit_sha": <the commit it dereferences to>}`. Read both mechanically from the remote you just pushed to, never from local state: `git ls-remote --tags origin ${TAG_PREFIX}MAJOR.MINOR.PATCH` for the ref sha and `git rev-parse ${TAG_PREFIX}MAJOR.MINOR.PATCH^{commit}` for the commit. That entry is what `.github/scripts/check_tag_immutability.py` compares the live ref against on every CI run; an unrecorded tag is an unguarded tag, and CI says so as a warning until this lands. The entry rides in a normal commit through `commit-gate` on the release branch.

Gate: with authorization, the tag is pushed AND a non-draft GitHub Release on that tag is confirmed by read-back (or, on failure, the exact manual command was surfaced and the half-finished state named), AND the tag's provenance is recorded in `.github/published-tags.json`. A failed or unverified publish is NOT a passing gate. Without authorization, nothing is published.

## Recovering from a bad release

**A published tag is immutable. Correction means publishing a NEW version — never moving, re-pointing, or deleting the old one** (issue #386, maintainer ruling 2026-07-25: repository rulesets, and deliberately **no break-glass role**).

This is not a style preference. The README instructs consumers to pin an exact tag (`ca-pi-v<version>` for Pi), so the tag *is* the identity of a payload that review, CI, and a published changelog have all vouched for. Retargeting `v2.8.13` does not fix `v2.8.13` for anyone who already installed it; it silently changes what everyone who installs it *next* gets, under a version whose verification history now describes different code. Deleting it is worse — every pinned install breaks at once, with no version left to roll back to.

When a release is wrong:

1. **Leave the bad tag and its Release exactly where they are.** Do not `git push --force` the tag, do not `git push --delete`, do not `gh release delete`. The bad version staying visible is what lets a consumer tell which payload they got.
2. Fix the defect on a branch and land it through the normal PR path.
3. Run `/release $TARGET` again. The bump is derived from that plugin's commit log as usual, so the fix ships as the next patch (or higher) version in the same series.
4. Mark the bad release so nobody installs it on purpose: `gh release edit <bad-tag> --prerelease` demotes it out of the Latest position, and a note at the top of its body should name the superseding version. Editing release *notes* is fine — it changes no code and moves no ref.
5. If the bad release is actively harmful (a leaked secret, a destructive bug), say so in the new release's notes and in the old release's body. An advisory is the sanctioned way to un-recommend a version; a moved tag is not.

The one case that is **not** a correction: a tag pushed by mistake with **no** GitHub Release and no possibility of a consumer having fetched it. Even then, prefer superseding it. If it must be removed, that is a maintainer action taken deliberately and announced, and `.github/published-tags.json` must be updated in the same PR so the drift audit does not report a deletion it was told to expect.

**If CI reports tag drift, the manifest is the witness, not the suspect.** `[CHECK] | [REPO] | Published tag immutability` going red means a published ref moved. The fix is to restore the ref to its recorded sha and find out who moved it. Editing `.github/published-tags.json` to match the new sha would "fix" the check by deleting the evidence — never do that to silence a red run. The only legitimate manifest edits are recording a newly published tag (Phase 3 step 5) and a deliberate, announced removal.

## Hard rules

- MUST resolve `$TARGET` to exactly one row of the Targets table before anything else, and MUST STOP on an unrecognised target rather than guessing which plugin was meant.
- MUST NOT tag on a red suite — `commit-gate` enforces green on every commit reaching HEAD; do not re-run it, but do not tag if the last suite was red.
- MUST NOT write to `main`, `master`, or the default branch, and MUST NOT force-push. Releases land through the normal branch/PR path.
- MUST NOT push the tag or create the GitHub Release without explicit user authorization; they publish together in Phase 3, even after the local tag composes.
- MUST scope tag resolution, the commit window, and the bump derivation to `$TARGET`'s series and `$PAYLOAD`; another plugin's tag or commit MUST NOT influence this release's version, window, or changelog. MUST NOT resolve `LAST_TAG` with bare `git describe --tags`, and MUST take `$TAG_PREFIX` from `_releaselib` rather than typing it.
- MUST assert the derived version equals `$MANIFEST` — and for `ca-pi`, that the GENERATED root `package.json` equals the plugin manifest, regenerated via `tools/build-host-packages.py` and never hand-edited.
- MUST rebuild `$ARTIFACTS` and assert every committed bundle is clean before tagging; the plugin ships the built file, not its source.
- MUST sync `ca`'s README version/count badges, their prose echoes, the README full-catalog table, and the canonical `plugins/ca/COMMANDS.md` catalog when `$TARGET` is `ca` — counts derived mechanically, never typed.
- MUST verify the published Release by read-back (`gh release view` → non-draft, correct tag); a failed or unverified publish is not a passing gate.
- MUST NOT assert `--latest` for any target except `ca`, and not even for `ca` unless the tag is the newest release across all four series.
- MUST use the Phase-1 changelog section verbatim as the GitHub Release notes — never re-derive or hand-write them.
- MUST NOT guess the version — derive it from the commit log. A `feat` in the window cannot ship as a `patch`.
- MUST NOT auto-fill a missing `CHANGELOG:` footer, and MUST NOT tag past one — a missing footer on a bumping commit is a Phase-1 BLOCK, surfaced as `[NEEDS-TRIAGE]` and stopped.
- MUST NOT tag a non-bumping window — `test`/`docs`/`chore`/`ci`-only sets do not release.
- **MUST NOT move, retarget, delete, or re-point a published tag**, in any namespace (`v*`, `ca-codex-v*`, `ca-sandbox-v*`, `ca-pi-v*`), for any reason — no `git push --force` on a tag, no `git push --delete`, no `gh release delete`. A bad release is corrected by publishing a NEW version; see "Recovering from a bad release". There is no break-glass path (issue #386).
- MUST record every newly published tag in `.github/published-tags.json`, and MUST NOT edit an existing entry to silence a red `[CHECK] | [REPO] | Published tag immutability` run — a red run means a ref moved, and the manifest is the evidence of where it belonged.
