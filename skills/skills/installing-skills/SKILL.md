---
name: installing-skills
description: Install skills from github.com/oaustegard/claude-skills into /mnt/skills/user. Use when user mentions "install skills", "load skills", "add skills", "update skills", "refresh skills", or references a skill not currently installed.
---

# Installing Skills

Install skills from github.com/oaustegard/claude-skills to `/mnt/skills/user`, making them available in the current and future conversations.

## Execution

Run the installation script:

```bash
bash /mnt/skills/user/installing-skills/scripts/install.sh
```

The script:
- Fetches repository contents via GitHub API
- Downloads SKILL.md for each skill directory
- Reports installed/updated/skipped counts
- Excludes: templates, .github, .claude, uploads directories

## Network Requirements

Requires access to:
- `api.github.com` - Repository structure listing
- `raw.githubusercontent.com` - File downloads

If blocked, report the specific endpoint and suggest checking network settings.

## Triggers

Execute installation automatically when:
- User explicitly requests skill installation/update
- User references a skill not present in `/mnt/skills/user`
- User mentions missing capabilities that match known skill patterns

After installation, proceed with user's original request.

## Verification

Installed skills appear in system's `<available_skills>` automatically. Manual verification:

```bash
ls /mnt/skills/user
```

## Manual Installation

For single skills or testing:

```bash
mkdir -p /mnt/skills/user/{skill-name}
curl -s "https://raw.githubusercontent.com/oaustegard/claude-skills/main/{skill-name}/SKILL.md" \
  -o "/mnt/skills/user/{skill-name}/SKILL.md"
```
