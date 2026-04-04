---
name: update-turbo
description: "Update installed Turbo skills from the local repo with a dynamic changelog, conflict resolution for customized skills, and guided user experience. Use when the user asks to \"update turbo\", \"update turbo skills\", \"reinstall turbo\", or \"upgrade turbo\"."
---

# Update Turbo

Read the latest update instructions from the local repo and follow them.

## Step 1: Read Instructions

Read `~/.turbo/config.json` to determine `repoMode`. Determine the upstream remote:

- Clone or source: `origin`
- Fork: `upstream`

Fetch the remote, then read the latest UPDATE.md:

```bash
git -C ~/.turbo/repo fetch <remote>
git -C ~/.turbo/repo show <remote>/main:UPDATE.md
```

## Step 2: Follow Instructions

Follow the fetched UPDATE.md instructions from start to finish. The fetch from Step 1 satisfies Phase 1 Step 1's fetch requirement.
