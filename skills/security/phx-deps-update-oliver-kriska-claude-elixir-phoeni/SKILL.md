---
name: phx-deps-update
description: Bump outdated Hex deps — inventory, snapshot changelogs, update, fix
  breaks, split reviewable PRs (patches bundled, majors solo). Use to upgrade/bump
  Elixir dependencies or when versions fall behind. NOT for deps.get failures (/skill:phx-investigate).
---

# Dependency Update (Freshness)

Inventory → update → fix breaks → grouped PRs. This is the only MUTATING
deps skill: it edits `mix.exs`, `mix.lock`, and source. Security scanning
stays in `/skill:phx-deps-audit`; the vet ledger stays in `/skill:phx-deps-vet`.

## Usage

```
/skill:phx-deps-update                       # inventory + interactive scope pick
/skill:phx-deps-update --scope patch         # bundle all patch bumps, one PR
/skill:phx-deps-update --pkg phoenix_live_view   # one package (+ coupled group)
/skill:phx-deps-update --dry-run             # inventory only, no changes
```

## Iron Laws

1. **NEVER cross a major version without an explicit `mix.exs` edit** —
   `mix deps.update` stays within requirements. Edit the constraint first;
   add `override: true` only when `mix hex.outdated <pkg>` shows a
   transitive consumer blocking. One major per PR
2. **ALWAYS snapshot the changelog delta BEFORE updating** — capture
   `deps/<pkg>/CHANGELOG.md`, then delta via `mix hex.package diff`. Never
   update blind
3. **NEVER claim an update is safe without verification** — run
   `/skill:phx-verify` (compile --warnings-as-errors + test). "Compiles" ≠ "works"
4. **ALWAYS move coupled packages together** — Phoenix core, Ecto, Ash,
   Oban, telemetry families update in the SAME step/commit (see
   `references/coupled-groups.md`)
5. **NEVER commit a partial bump** — `mix.lock` + `mix.exs` edits + (for
   Phoenix-family) `assets/package-lock.json` in ONE commit
6. **HAND OFF security to `/skill:phx-deps-audit`** — run it on the lock diff
   before any PR; don't reimplement audit rules
7. **`hex.outdated` exit 1 is normal** — it means "deps are outdated", not
   failure. Capture with `|| true`

## Workflow

### Phase 0: Discover

Read `mix.exs`: deps list, umbrella (`apps_path:`), git/path deps, private
orgs (`organization:`/`repo:` in tuples), Phoenix/Ash presence. Create
scratch dir `.claude/deps-update/{YYYY-MM-DD}/`.

### Phase 1: Inventory

`mix hex.outdated --all || true` — parse the text table (no JSON exists;
see `references/update-mechanics.md`). Classify each
row patch/minor/major by semver delta; `Update not possible` = blocked
major (mix.exs constraint). Write `inventory.md` to scratch. Render
grouped table: Patch / Minor / Major / Blocked / Git-deps (manual).
`--dry-run` stops here.

### Phase 2: Scope (AskUserQuestion)

Present groups with counts and risk. Default recommendation: "Patches (N)
— low risk, bundle into one PR". `--scope`/`--pkg` flags skip the prompt.
When ≥2 members of a coupled group are outdated, force them into one step
even under a narrower scope.

### Phase 3: Per-Package Update Loop

For each selected package, in coupled-group order:

1. Snapshot `deps/<pkg>/CHANGELOG.md` → `scratch/before/`
2. Update — patch/minor: `mix deps.update <pkg> [coupled...]`;
   major: edit `mix.exs` constraint (+ `override: true` if needed), then
   `mix deps.update <pkg>`
3. `git diff mix.lock` → the REAL `{pkg, old, new}` set (hex.outdated says
   what could change; the lock diff says what did)
4. Changelog delta: `mix hex.package diff <pkg> <old>..<new>` — keep the
   CHANGELOG hunk. Empty → `gh api repos/{o}/{r}/releases` fallback →
   compare-URL note (see `references/changelog-sources.md`)
5. Write `scratch/{pkg}-{old}-{new}.md`
6. Phoenix-family in the diff + `assets/package.json` exists →
   `npm install --prefix assets`, stage `assets/package-lock.json` with
   the same commit

### Phase 4: Verify

Run `/skill:phx-verify`. On failure → Phase 5; else Phase 6.

### Phase 5: Breaking-Change Fixes

Read the changelog deltas for "breaking"/"removed"/"deprecated" + the
compile/test errors. Fix source (apply the sibling-file check). Re-verify.

### Phase 6: Security Handoff

Run `/skill:phx-deps-audit` on the working `mix.lock` diff (its Mode B default).
BLOCK findings → surface and offer `/skill:phx-deps-vet <pkg> <ver>` for
accepted risks. Never skip this before a PR.

### Phase 7: Group, Commit, PR

Apply the splitting strategy (`references/pr-strategy.md`):
patches bundled, minors by area, majors solo, coupled groups always
together. PR bodies cite the changelog excerpt, the
`https://diff.hex.pm/diff/<pkg>/<old>..<new>` link, verification result,
and the deps-audit risk band. Stage lock + mix.exs + package-lock together.

## Integration

```text
/skill:phx-deps-update (mutating) → /skill:phx-deps-audit (security, Mode B)
        │                              │ BLOCK → /skill:phx-deps-vet (ledger)
        └→ /skill:phx-verify (gate) → grouped commits / PRs
```

## References

- `references/update-mechanics.md` — hex.outdated parsing, update vs unlock+get, majors, lock-diff
- `references/changelog-sources.md` — hex.package diff, gh fallbacks, private orgs
- `references/coupled-groups.md` — must-move-together groups + edge cases
- `references/pr-strategy.md` — grouping rules, area buckets, PR template, scratch layout
