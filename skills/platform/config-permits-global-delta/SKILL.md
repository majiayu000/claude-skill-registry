---
name: config-permits-global-delta
description: "{{ 𝚫𝚫𝚫 }} Grant a permission globally (all projects) via settings.local.jsonc"
model: haiku
disable-model-invocation: true
allowed-tools: ["Edit(/Users/jasonwarren/.claude/settings.local.jsonc)", "Bash(~/.claude/hooks/settings-sync.sh)"]
---

Add the permission `$ARGUMENTS` to the `permissions.allow` array in `~/.claude/settings.local.jsonc`, then run `~/.claude/hooks/settings-sync.sh` to sync it to `settings.local.json`.

## Steps

1. Read `~/.claude/settings.local.jsonc`.
2. Check whether `$ARGUMENTS` is already present in `permissions.allow`. If it is, say so and stop.
3. Append `"$ARGUMENTS"` to the `permissions.allow` array. If the key doesn't exist yet, create it at the top level alongside `hooks`.
4. Save the file using the Edit tool.
5. Run `~/.claude/hooks/settings-sync.sh` to sync the JSONC to `settings.local.json`.
6. Confirm the permission was added.
