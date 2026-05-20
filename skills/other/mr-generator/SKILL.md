---
name: mr-generator
description: Generate GitLab merge request descriptions from git commits with automatic categorization and Jira integration.
---

# MR Generator

Generate MR descriptions from git commits.

## Usage

```bash
# Basic (output to terminal)
python3 ~/.pi/agent/skills/mr-generator/scripts/mr_generator.py

# With Jira ticket (non-interactive)
python3 ~/.pi/agent/skills/mr-generator/scripts/mr_generator.py --jira RD-XXXX

# Create MR directly
python3 ~/.pi/agent/skills/mr-generator/scripts/mr_generator.py --create --jira RD-XXXX

# Save to file
python3 ~/.pi/agent/skills/mr-generator/scripts/mr_generator.py --output mr_description.md
```

## Best Practices

- Include project-specific testing instructions (check project's AGENTS.md for testing patterns)
- Replace template placeholders with actual working examples reviewers can copy-paste
- Keep "What's new" concise - implementation details belong in commit messages
- In monorepos, adapt testing section to the specific project's conventions

## MR Template

```
Closes #X or Relates to [link]

## What's new
- ✨ [New feature description - 1-2 bullets max]

## Testing

Run the following commands [project-specific setup]:
```bash
# Include actual working commands from AGENTS.md
```

Then test with [specific example]:
```[language]
# Real working example, not placeholders
```
```

## Commit Categorization

Automatic emoji mapping:
- 🎉 Init: `init`, `initial`
- ✨ Feature: `feat`, `add`
- 🐛 Bug: `fix`, `bug`, `patch`
- 🔥 P1: `p1`, `critical`
- 💄 Style: `style`, `ui`
- 🚀 Deploy: `deploy`, `release`
- 🔧 Refactor: `refactor`, `cleanup`
- 📚 Docs: `docs`
- 🧪 Tests: `test`

## Requirements
- Python 3.10+
- GitLab CLI (`glab auth login`)
