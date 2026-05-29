---
name: sync-plugin-cache
description: Synchronize all marketplace bundles to the Claude plugin cache
user-invocable: true
allowed-tools: Bash
---

# Sync Plugin Cache Skill

Synchronizes all bundles from `marketplace/bundles/` to the Claude plugin cache at `~/.claude/plugins/cache/plan-marshall/`.

## Parameters

None - Synchronizes all bundles automatically.

## Usage Examples

```bash
/sync-plugin-cache
```

Syncs all bundles after making changes to marketplace components.

## Workflow

### Step 1: Identify Bundles and Versions

Find all bundles and extract their versions from plugin.json:
```bash
for bundle in marketplace/bundles/*/; do
  name=$(basename "$bundle")
  version=$(python3 -c "import json; print(json.load(open('${bundle}.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "unknown")
  echo "$name:$version"
done
```

This outputs bundle:version pairs like `{bundle}:{version}`.

### Step 2: Determine Cache Location

The plugin cache location is: `~/.claude/plugins/cache/plan-marshall/`

Each bundle is cached at: `~/.claude/plugins/cache/plan-marshall/{bundle}/{version}/`

**IMPORTANT**: The version folder is required to match Claude Code's installation structure.

### Step 3: Sync Each Bundle

**CRITICAL**: Execute ALL rsync commands in PARALLEL using separate Bash tool calls in a single message. Do NOT use a for loop or sequential execution.

For each bundle found, invoke a separate Bash tool call using the version from Step 1:
```bash
rsync -av --delete marketplace/bundles/{bundle}/ ~/.claude/plugins/cache/plan-marshall/{bundle}/{version}/
```

The `--delete` flag ensures removed files are also removed from cache.

**NOTE**: Always use the version from each bundle's `plugin.json`, not a hardcoded value.

### Step 4: Display Summary

Show sync results listing each bundle synchronized and the cache location.

## Critical Rules

- Always use rsync with `--delete` to ensure cache matches source exactly
- Do NOT modify source files, only copy to cache
- If rsync fails, show error and continue with remaining bundles

## Related

- `/marshall-steward` - Project configuration including cache regeneration
- CLAUDE.md - Documents the plugin cache sync pattern
