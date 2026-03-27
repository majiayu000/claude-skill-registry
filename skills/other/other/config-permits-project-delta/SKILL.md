---
name: config-permits-project-delta
description: "{{ 𝚫𝚫𝚫 }} Grant a permission for the current project via .claude/settings.local.json"
model: haiku
disable-model-invocation: true
allowed-tools: ["Edit(.claude/settings.local.json)"]
---

Add the permission `$ARGUMENTS` to the `permissions.allow` array in `.claude/settings.local.json` in the current project directory.

## Steps

1. Read `.claude/settings.local.json` (relative to the current project root). If the file doesn't exist, start from `{"permissions": {"allow": []}}`.
2. Check whether `$ARGUMENTS` is already present in `permissions.allow`. If it is, say so and stop.
3. Append `"$ARGUMENTS"` to the `permissions.allow` array. If the `permissions` or `allow` keys don't exist, create them.
4. Save the file using the Edit tool.
5. Confirm the permission was added and note that it applies to this project only.
