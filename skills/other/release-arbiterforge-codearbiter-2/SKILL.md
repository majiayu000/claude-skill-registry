---
name: release
description: The single permitted path to a version tag. Routed to when the user invokes /release on a non-default branch with a green suite. Derives the SemVer bump from Conventional-Commits history since the last tag, rolls the commits into CHANGELOG.md, writes an annotated tag, and on authorization publishes it as a GitHub Release with the changelog section as its notes. A release commit, if needed, routes through commit-gate; the tag and Release are never published without explicit authorization.
---

# release

The single permitted path to a version tag. Routed to when the user invokes `/release`. Derive the bump from the commit log, update the changelog, tag — nothing more.

## Pre-flight

**This repo ships two independently-versioned plugins** (`ca` and `ca-sandbox`, per ADR-0007), each with its own tag series (`v*` vs `ca-sandbox-v*`), its own payload path, and its own built artifact. `/release` targets the **`ca`** plugin: tags `vMAJOR.MINOR.PATCH`, payload `plugins/ca/`, manifest `plugins/ca/.claude-plugin/plugin.json`. Every step below is scoped to `ca` — a `ca-sandbox` tag or commit MUST NOT influence ca's version, window, or changelog.

Read these, or STOP and surface the gap — never guess:

- `<project-root>/.codearbiter/CONTEXT.md` — the default-branch name and project context.
- `git status` must be clean. A dirty tree STOPs — commit or stash via `commit-gate` first.
- The current branch MUST NOT be `main`, `master`, or the default branch. Release lands through the normal branch/PR path; if HEAD is the default branch, STOP.
- **Resolve `LAST_TAG` from ca's SemVer tags only** — never bare `git describe --tags --abbrev=0`, which returns the nearest tag by commit-graph ancestry and in this two-plugin repo resolves to a `ca-sandbox-v*` tag, silently basing the entire release on the wrong baseline. Resolve it through the tested helper — the single source of truth, do not hand-roll a grep: `LAST_TAG=$(git tag -l | python3 .github/scripts/_releaselib.py last-tag)`. `_releaselib.last_tag_select` returns the highest `vMAJOR.MINOR.PATCH`, excluding pre-releases (`-beta`/`-rc`/`-alpha`) and the `ca-sandbox-v*` series, or `<none>` (its logic is pinned by `.github/scripts/test_release_lib.py`). No matching tag → `LAST_TAG=<none>`, treat the full history as the window, base version `0.0.0`.
- **Scope the release window to the `ca` payload:** the commit set is `git log LAST_TAG..HEAD -- plugins/ca/`, NOT the whole repo — a `feat(ca-sandbox)` commit must not bump `ca` or land in ca's changelog. This payload-scoped set must be non-empty; if empty, STOP — nothing to release for `ca`.
- **Manifest read:** read the `version` field of `plugins/ca/.claude-plugin/plugin.json`. Phase 1 asserts the derived bump equals it and updates it (and the README badges/counts) — a tag whose version runs ahead of `plugin.json` ships nothing, because `claude plugin update` no-ops on an unchanged version string.
- **farm.js freshness — rebuild unconditionally:** every release, regardless of whether `farm.ts` changed in the window, rebuild and assert the committed bundle is in sync: `(cd plugins/ca/tools && npm run build) && git diff --quiet -- plugins/ca/tools/farm.js`. A non-empty diff means `farm.js` is stale — a release blocker (the plugin ships `farm.js`, not `farm.ts`); commit the rebuild through `commit-gate` before tagging. Scope is `ca` only — `sandbox.js` belongs to the ca-sandbox release path, not here. The mechanical backstop is the CI `tools` job, which rebuilds and `git diff --quiet`s `farm.js` on every `plugins/ca/**`-touching PR; this local check is the belt to that suspenders, not a standalone gate. (The old form gated the rebuild on an in-window `farm.ts` change and so missed a `farm.js` that went stale before the window.)

## Phase 1 — Version & changelog · gate: BLOCK

Derive the bump mechanically from the commit log; do not guess it.

1. Read every commit in the ca-scoped window: `git log LAST_TAG..HEAD --pretty=format:%H%n%s%n%b%n---- -- plugins/ca/` (the `-- plugins/ca/` path scope is load-bearing — it excludes `ca-sandbox` commits from the bump and changelog).
2. Classify each subject by its Conventional-Commits prefix and apply the highest-precedence bump:
   - `BREAKING CHANGE:` footer or `!` after the type/scope → **major**.
   - else any `feat` → **minor**.
   - else any `fix`, `perf`, `refactor` → **patch**.
   - `test` / `docs` / `chore` / `ci` only → no bump. If the whole window is non-bumping, STOP — there is nothing to release.
3. Compute the next version, confirm it is strictly greater than `LAST_TAG`, and assert it **equals** the `version` in `plugins/ca/.claude-plugin/plugin.json`. If the manifest lags the derived bump, bump it now — that is a precondition of tagging (Pre-flight), not an afterthought; a tag ahead of `plugin.json` ships nothing. Present the version and the per-commit classification to the user for confirmation.
4. Derive the release date **once** — `RELEASE_DATE=$(date +%F)` — and reuse that single value for the changelog header, the Phase-2 `Released-at:` footer, and the Phase-3 Release; never hand-type the date a second time (`_releaselib.release_dates_consistent` verifies the changelog-header date equals the `Released-at:` date). Roll the `CHANGELOG:` footers from each `feat` / `fix` / `perf` commit into a new `## [MAJOR.MINOR.PATCH] — $RELEASE_DATE` section in the repo's `CHANGELOG.md` (the Keep-a-Changelog bracket heading the repo ships and the `_releaselib` guards match, not the bare `v`-prefixed form), grouped Added / Fixed / Performance. Prior sections stay intact. Create the file with a `# Changelog` heading if absent. **A `feat`/`fix` commit missing its `CHANGELOG:` footer is a BLOCK**, not a soft finding: surface the `[NEEDS-TRIAGE]` and STOP — never auto-fill, and never tag a changelog that silently drops a user-visible change. The changelog is a user-facing deliverable: apply `${CLAUDE_PLUGIN_ROOT}/includes/anti-slop-design/core.md` §3.A (no prose-separator em-dashes in the entry prose) and §3.B (copy self-audit), and the `medium-documents` §7.A.1 changelog guidance, to each rolled entry.
5. **Sync the release surfaces to the repo — mechanically derived, never typed.** Update, all to the derived version / live counts: `plugins/ca/.claude-plugin/plugin.json` `version`; the README version badge (`version-X.Y.Z`); the command / skill / agent **count** badges and every prose echo of those counts (e.g. "N commands", the `commands/ (N)` tree line). Derive each count from the repo, never increment by hand: `commands = ls plugins/ca/commands/*.md | grep -v INDEX | wc -l`, `skills = ls -d plugins/ca/skills/*/ | wc -l`, `agents = ls plugins/ca/agents/*.md | grep -v INDEX | wc -l`. Then assert the canonical catalog `plugins/ca/COMMANDS.md` enumerates exactly those command files, and that the README full-catalog table lists every one of them (the `$ca-commands` body at `plugins/ca/commands/COMMANDS.md` renders from the canonical catalog and holds no rows of its own — do not treat it as a second catalog). A badge, prose-count, README-table, or catalog drift is a **BLOCK** — reconcile it before tagging. The CI badge-consistency guard (`.github/scripts/check_badge_consistency.py`) is the mechanical backstop for this step; if it is red, this step is not done.
6. If the changelog edit or the surface sync needs to land as a commit before tagging, route it through `commit-gate`. Do not reimplement the commit path here.

Gate: version confirmed, strictly monotonic, matching the commit log, and equal to `plugin.json`; `CHANGELOG.md` updated; README badges/prose-counts and the `COMMANDS.md` catalog reconciled to the repo. BLOCK if the classification disagrees with the log, the window is non-bumping, a bumping commit's `CHANGELOG:` footer is missing, or any surface count/catalog drifts.

## Phase 2 — Tag & report · gate: BLOCK

1. Compose the annotated tag from the Phase 1 section plus a `Released-at: $RELEASE_DATE` footer (the same date derived once in Phase 1; `_releaselib.release_dates_consistent` must pass against the changelog section). Tag with `git tag -a vMAJOR.MINOR.PATCH -F <message-file>` — never `-m` for multi-line content, never an interactive editor. **If the tag already exists, do not flatly abort — classify the state** with `_releaselib.classify_publish_state` via `python3 .github/scripts/_releaselib.py classify <tag_exists> <tag_sha> <head_sha> <tag_version> <manifest_version> <release_nondraft>`: `abort_mismatch` (tag points at a non-HEAD commit, or its version disagrees with the manifest) → STOP; `already_published` (a non-draft Release already exists on the tag) → nothing to do; `resume_publish` (tag already at HEAD with the matching version but no Release) → skip re-tagging and resume at Phase 3 to create the missing Release.
2. Report: version, bump rationale, the per-commit classification, the changelog section, and the tag SHA.
3. MUST NOT push the tag or create the GitHub Release here. Publication is Phase 3, a separate step the user authorizes after reading the report.

Gate: the annotated tag exists locally and the report is delivered. Nothing is published.

## Phase 3 — Publish · gate: STOP

The tag and the GitHub Release publish together, and only after the user explicitly authorizes publication. This phase does not run until then; absent authorization, nothing leaves the local repo.

On authorization:

1. Push the tag: `git push origin vMAJOR.MINOR.PATCH`.
2. **Guard the notes-file first:** assert its first heading matches the tag — `python3 .github/scripts/_releaselib.py notes-match vMAJOR.MINOR.PATCH <Phase-1 section file>` (exit 0). A stale notes-file (`_releaselib.notes_heading_matches` False) would publish the wrong changelog section under the right tag — STOP on mismatch. Then create the GitHub Release from the **same changelog section composed in Phase 1** — reuse it as the notes, never re-derive or hand-write them. **Set `--latest` conditionally:** the repo ships two release series but GitHub has one repo-wide "Latest" — assert `--latest` only when this tag is the newest release across *both* plugins (compare against `gh release list`); otherwise pass `--latest=false` so a `ca` release doesn't steal the badge from a newer `ca-sandbox` release, or vice-versa. `gh release create vMAJOR.MINOR.PATCH --title "<title>" --notes-file <Phase-1 section file> --latest[=false] --verify-tag`. The title follows the existing convention `codeArbiter MAJOR.MINOR.PATCH: <summary>`, with no em-dash separator.
3. Handle edge cases explicitly, never silently: if a Release for the tag already exists, report it and skip creation (the tag push may already have landed); if `gh` is missing, unauthenticated, or the call fails, STOP and print the exact `gh release create` command so publication can be finished by hand rather than left half-done.
4. **Verify publication — never assume it.** Read the Release back: `gh release view vMAJOR.MINOR.PATCH --json url,isDraft,tagName`. STOP unless it returns a **non-draft** Release on the correct tag; `gh release create` can partially succeed (tag pushed, Release rejected for an empty notes-file or a permissions/`--verify-tag` race), and an unverified publish is not a published release. Report the Release URL only once the read-back confirms it.

Gate: with authorization, the tag is pushed AND a non-draft GitHub Release on that tag is confirmed by read-back (or, on failure, the exact manual command was surfaced and the half-finished state named). A failed or unverified publish is NOT a passing gate. Without authorization, nothing is published.

## Hard rules

- MUST NOT tag on a red suite — `commit-gate` enforces green on every commit reaching HEAD; do not re-run it, but do not tag if the last suite was red.
- MUST NOT write to `main`, `master`, or the default branch, and MUST NOT force-push. Releases land through the normal branch/PR path.
- MUST NOT push the tag or create the GitHub Release without explicit user authorization; they publish together in Phase 3, even after the local tag composes.
- MUST scope tag resolution, the commit window, and the bump derivation to the `ca` payload (`plugins/ca/`); a `ca-sandbox` tag or commit MUST NOT influence ca's version, window, or changelog. MUST NOT resolve `LAST_TAG` with bare `git describe --tags`.
- MUST assert the derived version equals `plugins/ca/.claude-plugin/plugin.json`, and MUST sync the README version/count badges, their prose echoes, the README full-catalog table, and the canonical `plugins/ca/COMMANDS.md` catalog to the repo before tagging — counts derived mechanically, never typed.
- MUST verify the published Release by read-back (`gh release view` → non-draft, correct tag); a failed or unverified publish is not a passing gate. MUST NOT assert `--latest` unless the tag is the newest release across both plugins.
- MUST use the Phase-1 changelog section verbatim as the GitHub Release notes — never re-derive or hand-write them.
- MUST NOT guess the version — derive it from the commit log. A `feat` in the window cannot ship as a `patch`.
- MUST NOT auto-fill a missing `CHANGELOG:` footer, and MUST NOT tag past one — a missing footer on a bumping commit is a Phase-1 BLOCK, surfaced as `[NEEDS-TRIAGE]` and stopped.
- MUST NOT tag a non-bumping window — `test`/`docs`/`chore`/`ci`-only sets do not release.
