---
name: bmad-revendor
description: Maintainer-only. Use when re-vendoring skills/BMAD/ against a newer BMAD-METHOD commit — "update BMAD", "re-vendor BMAD", "bump the BMAD pin". Not part of the Hedgehog discipline a consuming project copies; this only applies to the Hedgehog repo itself.
---

# Re-vendoring BMAD-METHOD

`skills/BMAD/` is a pinned, manually-updated vendor copy of seven skills
from `bmad-code-org/BMAD-METHOD`'s `bmm` module (see
`skills/BMAD/ATTRIBUTION.md` for the current pin). It is never
auto-updated — re-vendoring is a deliberate act, run only when this
skill is invoked by name or the user explicitly asks to update BMAD.

## What's vendored, and why these specific paths

Seven skill directories plus two shared scripts they all depend on:

- `src/core-skills/bmad-brainstorming`
- `src/core-skills/bmad-advanced-elicitation`
- `src/core-skills/bmad-deep-recon`
- `src/bmm-skills/1-analysis/bmad-product-brief`
- `src/bmm-skills/1-analysis/bmad-prfaq`
- `src/bmm-skills/2-plan-workflows/bmad-prd`
- `src/bmm-skills/2-plan-workflows/bmad-ux`
- `src/scripts/memlog.py`, `src/scripts/resolve_customization.py` — shared
  utilities every one of the seven skills calls. Not inside any single
  skill directory upstream; vendored separately into `skills/BMAD/scripts/`.

`bmad-deep-recon` is the one skill in this set that, as of the last vendor
pass, existed only on BMAD-METHOD's `main` branch — not in any tagged
release. If that's still true, pin to `main` at a specific commit SHA
rather than a release tag (see "Pinning," below); if BMAD-METHOD has since
tagged a release containing it, prefer that tag instead.

## Procedure

1. **Find the ref to vendor against.** Check `gh repo view
   bmad-code-org/BMAD-METHOD --json defaultBranchRef` and `gh api
   repos/bmad-code-org/BMAD-METHOD/tags` for available release tags. If
   every one of the seven skills above exists in the newest tag, pin to
   that tag. If `bmad-deep-recon` (or any other of the seven) is
   unreleased, pin to `main` at its current commit SHA instead — get it
   via `gh api repos/bmad-code-org/BMAD-METHOD/commits/main --jq '.sha'`.
   Don't silently drop a skill just because it's unreleased; ask the user
   how to resolve the conflict if it's not obvious (this came up during
   the original vendor pass — see git history on `skills/BMAD/`).

2. **List the file tree at that ref**, scoped to the seven skill
   directories plus `src/scripts/`:
   ```bash
   gh api "repos/bmad-code-org/BMAD-METHOD/git/trees/<ref>?recursive=true" \
     --jq '.tree[] | select(.type=="blob") | .path' \
     | grep -E "^src/(core-skills/(bmad-brainstorming|bmad-advanced-elicitation|bmad-deep-recon)|bmm-skills/1-analysis/(bmad-product-brief|bmad-prfaq)|bmm-skills/2-plan-workflows/(bmad-prd|bmad-ux)|scripts)/"
   ```
   Diff this against the current file list in `skills/BMAD/` (excluding
   `LICENSE`, `ATTRIBUTION.md`, and any files this skill's step 4 strips)
   to see what's new, removed, or moved upstream before blindly
   overwriting — a file that moved to a new path upstream needs its
   path updated here too, not a stale copy left behind.

3. **Fetch every file** at that ref via `gh api
   repos/bmad-code-org/BMAD-METHOD/contents/<path>?ref=<sha>` (the
   `.content` field is base64), decoding with `base64 --decode` (BSD
   `base64` on macOS needs `-i`/`-o` flags, not `-d <file>`) into
   `skills/BMAD/<path-with-src/-stripped>`. Also re-fetch `LICENSE` from
   the repo root the same way.

4. **Re-apply the strip pass.** Every vendored `SKILL.md` and its
   `references/*.md` files have BMAD's own orchestration layer removed —
   this doesn't survive a raw re-fetch and must be redone by hand each
   time:
   - Central config resolution (`_bmad/scripts/resolve_config.py`,
     `_bmad/config.toml`, `_bmad/bmm/config.yaml`) — not vendored;
     replace with trivial inline defaults for `{user_name}`,
     `{communication_language}` (English), `{date}` (today),
     `{project_name}`.
   - `_bmad/scripts/resolve_customization.py` and
     `_bmad/scripts/memlog.py` calls — these ARE vendored (in
     `skills/BMAD/scripts/`); rewrite their paths to
     `{bmad-root}/scripts/<name>.py`, where `{bmad-root}` is defined once
     per file (in a "Conventions" section) as the vendored `skills/BMAD/`
     root.
   - `bmad-party-mode` mentions/invocations — remove (not vendored).
   - Chain-forward "common next skill" suggestions, `bmad-help`
     references, and misroute-detection pointing at non-vendored BMAD
     skills — remove. Control returns to Hedgehog's `planner` after each
     skill, not to BMAD's own routing.
   - Keep `bmad-advanced-elicitation` invocations — it IS vendored.
   - Verify when done:
     ```bash
     cd skills/BMAD && grep -rn "_bmad/\|resolve_config\.py\|party-mode\|party_mode\|bmad-help\|common next\|scan for misroute" --include="*.md" .
     ```
     Zero matches is the bar. Read each match before deciding it's really
     orchestration — don't blind-strip a line that happens to contain one
     of these words for an unrelated reason.

5. **Verify self-containment.** Every vendored Python script must compile
   and its own test suite must pass, standalone, from inside
   `skills/BMAD/`:
   ```bash
   cd skills/BMAD
   for f in $(find . -name "*.py" -not -path "*/tests/*"); do python3 -c "import py_compile; py_compile.compile('$f', doraise=True)"; done
   uv run --with pytest python3 -m pytest scripts/tests/ core-skills/*/scripts/tests/ -q
   ```
   Also confirm no vendored file references an absolute path outside
   `skills/BMAD/` or a project path from the machine that did the
   vendoring.

6. **Update `skills/BMAD/ATTRIBUTION.md`**: new pinned ref (tag or commit
   SHA), new date, and a note if the vendored file set itself changed
   (a skill added/removed upstream, a shared script renamed, etc.).

7. **One commit**, `chore(bmad): re-vendor to <ref>` — the whole
   re-vendor pass is one unit of work, not split across the fetch and the
   strip pass.

## Constraints

- Never auto-run this on a schedule or "while you're in the area" — only
  on explicit request, same posture as `src/golden-cores/full-stack-app` regeneration.
- Never hand-patch a single vendored file to fix an upstream bug without
  also updating `ATTRIBUTION.md` — a silent local fork is worse than a
  stale pin, since nothing records that `skills/BMAD/` has diverged from
  what its own attribution claims.
- If BMAD-METHOD has restructured upstream (skill renamed, moved to a
  different module, split into multiple skills) since the last vendor
  pass, don't force a mechanical file-for-file replace — read the new
  shape and decide whether Hedgehog's list of seven skills still makes
  sense, or whether `src/agents/planner.md`'s shelf-invocation list
  (Section "Planning intake" in that file) itself needs updating to
  match. Surface this to the user rather than silently adapting.
