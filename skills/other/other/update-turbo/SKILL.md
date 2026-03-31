---
name: update-turbo
description: "Update installed Turbo skills from the local repo with a dynamic changelog, conflict resolution for customized skills, and guided user experience. Use when the user asks to \"update turbo\", \"update turbo skills\", \"reinstall turbo\", or \"upgrade turbo\"."
---

# Update Turbo

Fetch the latest update instructions from the Turbo repo and follow them.

## Step 1: Fetch Instructions

Use `WebFetch` to retrieve the update instructions:

```
https://raw.githubusercontent.com/tobihagemann/turbo/main/UPDATE.md
```

## Step 2: Follow Instructions

Follow the fetched UPDATE.md instructions from start to finish.
