---
name: automates
description: Open the AutoMates root folder in Finder
allowed-tools:
  - Bash
---

# /automates - Open AutoMates Folder

Opens the AutoMates root folder in your system file browser so you can browse agent identities, the library, dashboard, and everything under the hood.

## Usage

```
/automates
```

## Instructions

Run this command to open the root folder:

```bash
open "$(pwd)"
```

Then tell the user:

```
Opened AutoMates root folder. Here's what's inside:

AgenTeam/    — Agent identities and memory (one folder per agent)
Library/     — Knowledge base, research sources, Fetcher agent, Rules.md
Dashboard/   — Brief.md, Project_Description.md, Work_Space (active projects)
CLAUDE.md    — Shared config (auto-loaded every session)
.claude/     — Skills (slash commands)
```
