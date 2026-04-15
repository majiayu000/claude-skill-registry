---
name: find-skills
description: Use when the user asks how to do something, wants a skill for a task, or wants to discover and install new agent capabilities.
argument-hint: [search query]
---

query = $ARGUMENTS

Discover and install skills from the open agent skills ecosystem using the Skills CLI (`npx skills`).

Browse available skills at https://skills.sh/

## CLI

```bash
npx skills find [query]              # search by keyword
npx skills add <owner/repo@skill>    # install a skill
npx skills check                     # check for updates
npx skills update                    # update all installed
```

## Install Protocol

Always pass `-a claude-code -y` when installing. `-a` targets `.claude/skills/` only — without it, the CLI scatters files into `.agents/`, `.junie/`, `.kilocode/`, `.kiro/`. `-y` skips confirmation. Add `-g` only if the user explicitly asks for a global install.

```bash
npx skills add <owner/repo@skill> -a claude-code -y
```

## Post-Install Cleanup (mandatory)

The CLI always creates `.agents/skills/<name>/` as internal storage and symlinks from `.claude/skills/`. No flag prevents this. Every install requires cleanup:

```bash
# Replace symlink with real copy
rm .claude/skills/<skill-name>
cp -R .agents/skills/<skill-name> .claude/skills/<skill-name>

# Remove all CLI artifacts
rm -rf .agents .junie .kilocode .kiro
rm -f skills-lock.json
```
