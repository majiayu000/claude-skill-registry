---
name: claude-config
description: Use when the user wants to add allowed commands, plugins, env vars, or other fields to their shared Claude Code settings managed by shizuku. Use when they say things like "add X to my allowed commands", "add plugin Y", or "set env var Z".
---

# Claude Config Manager

Manages shared Claude Code settings (`~/.claude/settings.json`) via the shizuku claude app. All changes go through `apps/claude/claude.go`.

For the full settings.json schema and all available fields, see: https://code.claude.com/docs/en/settings

## How It Works

The claude app reads the existing `~/.claude/settings.json`, additively merges managed fields, and writes the result. Existing user-set fields are never removed.

**Managed fields and their merge strategies:**

| Field | Type | Strategy | Variable |
|-------|------|----------|----------|
| `enabledPlugins` | `map[string]any` | Set key to `true` | `desiredPlugins` |
| `permissions.allow` | `[]any` | Append if not present | `desiredAllowedCommands` |
| `env` | `map[string]any` | Set key to value | `desiredEnv` |

Unmanaged fields (e.g. `plansDirectory`, `promptSuggestionEnabled`) pass through untouched.

## Adding an Allowed Command

1. Open `apps/claude/claude.go`
2. Add the command string to the `desiredAllowedCommands` slice
3. Build and verify with diff

**Command format examples:**
- `Bash(command:*)` - Allow a bash command with any args
- `Bash(git add:*)` - Allow a specific git subcommand
- `Skill(name)` - Allow a skill invocation
- `Edit(path/*)` - Allow edits to a path pattern
- `WebFetch(domain.com:*)` - Allow fetching from a domain

**Example: adding `Bash(docker:*)` to allowed commands:**

```go
var desiredAllowedCommands = []string{
    "Bash(grep:*)",
    // ... existing entries ...
    "Bash(docker:*)",  // add here
}
```

## Adding a Plugin

1. Open `apps/claude/claude.go`
2. Add the plugin identifier to the `desiredPlugins` slice
3. Build and verify with diff

```go
var desiredPlugins = []string{
    // ... existing entries ...
    "new-plugin@marketplace-name",  // add here
}
```

## Adding an Environment Variable

1. Open `apps/claude/claude.go`
2. Add the key-value pair to the `desiredEnv` map
3. Build and verify with diff

```go
var desiredEnv = map[string]string{
    // ... existing entries ...
    "VARIABLE_NAME": "value",  // add here
}
```

Env vars set here are injected into every Claude Code session. Common uses: telemetry config, default model settings, proxy URLs.

## Adding a New Managed Field

To manage a new top-level or nested field from `settings.json`, add merge logic in `mergeSettings()` after the existing blocks. Follow the established patterns:

**For map fields** (like `enabledPlugins`, `env`):
```go
fieldMap, _ := settings["fieldName"].(map[string]any)
if fieldMap == nil {
    fieldMap = map[string]any{}
}
for k, v := range desiredItems {
    fieldMap[k] = v
}
settings["fieldName"] = fieldMap
```

**For array fields** (like `permissions.allow`):
```go
parent, _ := settings["parent"].(map[string]any)
if parent == nil {
    parent = map[string]any{}
}
items, _ := parent["field"].([]any)
existing := map[string]bool{}
for _, entry := range items {
    if s, ok := entry.(string); ok {
        existing[s] = true
    }
}
for _, item := range desiredItems {
    if !existing[item] {
        items = append(items, item)
    }
}
parent["field"] = items
settings["parent"] = parent
```

**For scalar fields** (e.g. setting a boolean):
```go
settings["fieldName"] = desiredValue
```

## Verification

After any change, always:

1. `/task build`
2. `/task run diff -p` - Confirm the field appears correctly in the diff
3. `/task run sync --verbose` - Apply if satisfied

## Key File

All changes happen in one file: `apps/claude/claude.go`
