---
name: release
description: |
  CONTRIBUTOR TOOL - Cut a plugin release: bump plugin.json version, finalize
  CHANGELOG, update README if needed, gate on make ci, commit, tag vX.Y.Z, and
  create the GitHub release. Use when shipping a new plugin version. NOT distributed.
argument-hint: "[patch|minor|major] | [X.Y.Z]"
effort: medium
---

# Plugin Release

Cuts a versioned release of the Elixir/Phoenix plugin. Drives the full
checklist from `CLAUDE.md` (Release + Versioning) so every release is
consistent. **Contributor tooling — not shipped in the plugin.**

## Iron Laws — Never Violate These

1. **NEVER release on a red `make ci`** — the gate runs BEFORE committing. No green, no release.
2. **NEVER `claude plugin tag`** — this is a marketplace layout (`plugins/elixir-phoenix/.claude-plugin/plugin.json`, not repo root). Tag manually: `git tag vX.Y.Z`.
3. **THREE NUMBERS MUST MATCH** — `plugin.json` version == CHANGELOG heading == git tag (`vX.Y.Z`). Verify before pushing.
4. **CONFIRM BEFORE PUBLISHING** — pushing the tag and `gh release create` are outward-facing and hard to reverse. Stop and confirm with the user; show exactly what will be pushed/published first.
5. **USERS ONLY UPDATE ON A `plugin.json` BUMP** — never ship CHANGELOG/code changes without bumping the version, or installed users get nothing (cache).
6. **ALWAYS leave a fresh empty `## [Unreleased]`** — one `[Unreleased]` becomes one version heading; re-add an empty one on top.
7. **NEVER force-push** — `git push --force` is hook-blocked here. If history needs rewriting, the user runs it via `!`.

## Step 0: Preconditions

- On `main`, working tree clean except intended release files. If feature work is uncommitted, commit it first.
- Determine version. Read current `plugins/elixir-phoenix/.claude-plugin/plugin.json`. Pick bump from `## [Unreleased]` contents:
  - **MAJOR** — breaking change (removed command, workflow redesign)
  - **MINOR** — new skill / agent / command / hook
  - **PATCH** — bug fix, doc/reference update, description tweak
- **Consolidation check** (per memory): if several phased branch bumps never released, collapse to ONE bump from the last released tag — don't stack intermediate versions.

## Step 1: Bump `plugin.json` version

Set `"version"` in `plugins/elixir-phoenix/.claude-plugin/plugin.json` to `X.Y.Z`.
(Often already bumped during the feature work — confirm it matches the target.)

## Step 2: Finalize CHANGELOG

In `CHANGELOG.md`:

1. Rename `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` (today's date).
2. Insert a fresh empty section on top (see `${CLAUDE_SKILL_DIR}/references/templates.md`).
3. Optionally add a one-line summary under the new heading (past releases do).

## Step 3: README + intro (only if needed)

- Update `README.md` ONLY if counts/version callouts changed: skill count, agent
  count (`grep -nE "[0-9]+ (skills|agents|specialist)" README.md`), or a version banner.
  A pure doc/reference PATCH usually needs **no** README change — verify, don't assume.
- Check `plugins/elixir-phoenix/skills/intro/references/tutorial-content.md` cheat sheet
  if commands/skills/agents were added, removed, or renamed.

## Step 4: Gate on `make ci`

Run `make ci` (lint + test + validate + eval-all). **Must be green.** If lint trips on
untracked non-source dirs (e.g. `social/`, `.rtk/`), that is not a code failure — exclude
them, don't ship around real failures. See `${CLAUDE_SKILL_DIR}/references/templates.md`.

## Step 5: Commit

```
git add CHANGELOG.md plugins/elixir-phoenix/.claude-plugin/plugin.json   # + README if touched
git commit   # message below
```

Commit subject (matches history): `Release vX.Y.Z — <short summary>`
End the message with the `Co-Authored-By` trailer (see `CLAUDE.md`).

## Step 6: Tag

```
git tag vX.Y.Z
```

## Step 7: CONFIRM, then publish (outward-facing)

Show the user the pending commit, tag, and release notes. **On confirmation:**

```
git push origin main
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z — <summary>" --notes-file <changelog-section>
```

Use the new CHANGELOG section as release notes (extract it to a temp file or `--notes`).

## Step 8: Verify

```
gh release view vX.Y.Z
git describe --tags --abbrev=0    # should print vX.Y.Z
```

Confirm to the user: released, tag pushed, GitHub release live.

## Reference

- `${CLAUDE_SKILL_DIR}/references/templates.md` — CHANGELOG/release-notes templates, gate snippets, gotchas
