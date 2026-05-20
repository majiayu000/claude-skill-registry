---
name: skill-promotion-and-dedup
description: Promote imported skills into first-class categories while preventing duplicate-name discovery conflicts. Includes backup, verification, and rollback.
---

# Skill Promotion and Dedup (Hermes)

Use this when users import many custom skills (e.g. under `~/.hermes/skills/imported-codex`) and want better discoverability/reliability.

## When to use
- User says imported skills are hard to trigger/find.
- Same skill names exist in multiple categories (imported + official), causing inconsistent selection.
- User wants to keep imported originals, but use promoted copies as active skills.

## Core idea
1. Promote imported skills to first-class categories (social-media, research, media, etc.).
2. Keep imported originals as archive.
3. Disable duplicate active entries in archive (avoid two `SKILL.md` files with same `name:`).

## Procedure

1) Inventory and mapping
- Enumerate source skills under `~/.hermes/skills/imported-codex/*/SKILL.md`.
- Create an explicit mapping: `skill_name -> target_category`.
- Do not proceed with unmapped skills.

2) Backup and promote
- Create backup root: `~/.hermes/skill-promotions/<timestamp>/`.
- For each skill:
  - If target exists, backup existing target first.
  - Copy imported skill folder to target category path.
- Save a manifest: `promotion-manifest.json` with source/target/backups.

3) Configure defaults where needed
- If there are competing skills for same domain, clarify routing in descriptions.
- Example used successfully:
  - `bird-twitter`: default for read-only Twitter via browser login.
  - `xitter`: official API / write actions.

4) Deduplicate active discovery
- In archive category (`imported-codex`), rename `SKILL.md` -> `SKILL.imported.md`.
- Keep scripts/assets/references intact.
- Optionally add `imported-codex/DESCRIPTION.md` stating this is archive-only.
- Important: if duplicate active definitions remain, `skills_list` may surface unstable/partial results (some promoted skills appear missing by category). Disable archive `SKILL.md` first, then re-check.

4b) Optional deletion mode (when user wants no archive)
- Create a one-file archive first (safety):
  - `tar -czf ~/.hermes/skill-promotions/archive-before-delete/imported-codex-<ts>.tgz -C ~/.hermes/skills imported-codex`
- Delete archive directory:
  - `rm -rf ~/.hermes/skills/imported-codex`
- Verify:
  - `skills_list(category='imported-codex')` returns empty
- If user asks for zero backup retention, delete the tarball too.

5) Verify
- `skills_list(category=...)` for all target categories.
- `skills_list(category='imported-codex')` should be empty or non-active.
- `skill_view(<key_skill>)` resolves to promoted category path.
- Smoke-check critical runtime tools (e.g. `bird check --plain`).

6) Rollback support
- Generate rollback script from manifest:
  - Restore archive `SKILL.md` from `SKILL.imported.md`.
  - Remove promoted target copies.
- Store script under `~/.hermes/skill-promotions/rollback-*.sh`.

## Pitfalls
- Duplicate skill names across categories cause non-deterministic discoverability.
- Moving without backups risks losing custom local edits in existing targets.
- Forgetting to disable archive copies keeps the conflict alive.

## Success criteria
- User’s common skills appear in expected first-class categories.
- Archive remains preserved and recoverable.
- No duplicate active definitions for same skill name.
- A documented rollback path exists.
