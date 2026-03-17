---
name: skill-deploy-update
description: Use when creating, updating, or syncing Codex skills for this repo, including installing skills into CODEX_HOME and using scripts/sync_skills.ps1 to symlink repo skills; also use when drafting a new SKILL.md or adjusting skill folder structure.
---
# Skill Deploy and Update

Use this skill to keep project skills stored in-repo and linked into CODEX_HOME via the sync script. Prefer symlinks so the repo is the source of truth.

## When to Use

- Add, rename, or restructure a skill folder in docs/skills.
- Update SKILL.md contents or bundled resources.
- Sync repo skills into CODEX_HOME for Codex discovery.

## Repo Layout

Each skill must live in its own folder:

```
docs/skills/<skill-name>/
  SKILL.md
  scripts/
  references/
  assets/
```

The SKILL.md frontmatter name must match the folder name.

## Sync Script

Use the repo sync script to link all repo skills into CODEX_HOME:

```powershell
.\\scripts\\sync_skills.ps1
```

Optional: pass a custom repo skills path:

```powershell
.\\scripts\\sync_skills.ps1 -RepoSkillsPath "C:\\path\\to\\repo\\docs\\skills"
```

## How to Update a Skill

1. Edit the skill folder under docs/skills.
2. Keep instructions concise and imperative.
3. Re-run the sync script.
4. If a skill was renamed, delete the old link in CODEX_HOME if it is not a symlink.

## Skill Template

Use the bundled template at assets/skill-template/SKILL.md as a starting point.
