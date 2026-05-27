---
name: convert-other-to-antigravity-skills
description: Converts existing skills to the Antigravity standard (Project-root relative paths, uv dependency management). Use this when adding new skills or fixing existing ones to run properly in the Antigravity environment.
---

# Convert Skills to Antigravity Standard

This skill automatically updates a skill's `SKILL.md` file to follow the Antigravity project standards.

## Prerequisites

This skill uses `uv` for dependency management.

1. Initialize `uv` project (if not already done):
```bash
uv init .
```

2. Add dependencies (No external packages required for this skill):
```bash
# uv add [package]
```

3. Run the skill using `uv run`:
```bash
uv run [script_path] ...
```

## Features

- **Path Correction**: Updates `.claude/skills` or relative `scripts/` paths to `.agent/skills/<skill-name>/...`.
- **UV Integration**: Replaces `python3` commands with `uv run`.
- **Prerequisites**: Adds the standard `uv` setup guide to the top of the skill documentation.

## Usage

To convert a target skill, run the conversion script from the project root:

```bash
uv run .agent/skills/convert-other-to-antigravity-skills/scripts/convert.py <target-skill-name>
```

### Examples

Convert a newly added skill named `my-new-skill`:
```bash
uv run .agent/skills/convert-other-to-antigravity-skills/scripts/convert.py my-new-skill
```

Convert a skill by path:
```bash
uv run .agent/skills/convert-other-to-antigravity-skills/scripts/convert.py .agent/skills/legacy-skill
```
