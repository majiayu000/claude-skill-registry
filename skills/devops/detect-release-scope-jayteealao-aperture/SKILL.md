---
name: detect-release-scope
description: Analyze git changes to determine release scope (marketplace/plugin/variants)
user-invocable: false
---

# Detect Release Scope

## Purpose

Analyzes git changes (modified, staged, and untracked files) to intelligently determine which release scope should be targeted: marketplace-level, per-plugin, or variants. This skill is the foundation for the release workflow, ensuring the correct versioning context is used.

## Input Context

The skill expects to be invoked in a git repository with changes to analyze. It will examine:

- Modified files (staged and unstaged)
- Newly created files
- Deleted files
- Current git branch

## Workflow

### 1. Gather Git Status

Use `git status --porcelain` to get a machine-readable list of all changed files:

```bash
git status --porcelain
```

Parse the output to categorize files by path patterns.

### 2. Categorize Files by Scope

Analyze each changed file path and increment counters for each scope:

**Marketplace Scope Indicators:**
- `.claude-plugin/marketplace.json`
- Root `README.md` (when marketplace.json also changed)
- Root `CHANGELOG.md`

**Plugin Scope Indicators:**
- `plugins/{plugin-name}/.claude-plugin/plugin.json`
- `plugins/{plugin-name}/skills/**/*`
- `plugins/{plugin-name}/commands/**/*`
- `plugins/{plugin-name}/README.md`
- `plugins/{plugin-name}/CHANGELOG.md`

**Variants Scope Indicators:**
- `variants/variants.json`
- `variants/*/CLAUDE.md`
- `variants/CHANGELOG.md`
- `variants/README.md`

### 3. Determine Primary Scope

Apply the following logic:

**Single Plugin Dominance:**
- If 70%+ of changes are within a single plugin directory → `plugin:<name>`

**Variants Dominance:**
- If 70%+ of changes are within `variants/` → `variants`

**Marketplace Changes:**
- If marketplace.json is modified AND no plugin dominance → `marketplace`

**Ambiguous Cases:**
- If changes are split across multiple scopes with no clear majority:
  - Return all detected scopes with file counts
  - Set confidence level to "ambiguous"
  - Command will prompt user to choose

### 4. Validate Current Branch

Check if the current branch is `master` or `main`:

```bash
git branch --show-current
```

If on a different branch, include a warning in the output.

## Output Format

Return a structured response with:

```
{
  "primary_scope": "plugin:daily-carry" | "marketplace" | "variants" | "ambiguous",
  "confidence": "high" | "medium" | "low" | "ambiguous",
  "evidence": {
    "marketplace_changes": <count>,
    "plugin_changes": {
      "daily-carry": <count>,
      "agent-behavior-patterns": <count>
    },
    "variants_changes": <count>
  },
  "current_branch": "master",
  "warnings": [
    "Not on master branch",
    "Multiple scopes detected"
  ]
}
```

## Examples

### Example 1: Clear Plugin Scope

**Git Status:**
```
M plugins/daily-carry/skills/deploy-site/SKILL.md
M plugins/daily-carry/README.md
A plugins/daily-carry/skills/new-skill/SKILL.md
```

**Output:**
```
{
  "primary_scope": "plugin:daily-carry",
  "confidence": "high",
  "evidence": {
    "marketplace_changes": 0,
    "plugin_changes": {
      "daily-carry": 3
    },
    "variants_changes": 0
  },
  "current_branch": "master",
  "warnings": []
}
```

### Example 2: Ambiguous Multi-Scope

**Git Status:**
```
M .claude-plugin/marketplace.json
M plugins/daily-carry/skills/deploy-site/SKILL.md
M variants/Android/CLAUDE.md
```

**Output:**
```
{
  "primary_scope": "ambiguous",
  "confidence": "ambiguous",
  "evidence": {
    "marketplace_changes": 1,
    "plugin_changes": {
      "daily-carry": 1
    },
    "variants_changes": 1
  },
  "current_branch": "master",
  "warnings": [
    "Multiple scopes detected - please specify scope explicitly"
  ]
}
```

### Example 3: Variants Release

**Git Status:**
```
M variants/Typescript/CLAUDE.md
M variants/Python/CLAUDE.md
M variants/Generic/CLAUDE.md
M variants/CHANGELOG.md
```

**Output:**
```
{
  "primary_scope": "variants",
  "confidence": "high",
  "evidence": {
    "marketplace_changes": 0,
    "plugin_changes": {},
    "variants_changes": 4
  },
  "current_branch": "master",
  "warnings": []
}
```

## Error Handling

- **No git repository**: Return error with message "Not a git repository"
- **No changes detected**: Return error with message "No changes to release"
- **Invalid git state**: Return error with details about unresolved conflicts or detached HEAD

## Integration Notes

This skill is invoked by the `/release` command in Phase 1. The command will:
1. Use the `primary_scope` if confidence is "high" or "medium"
2. Prompt user to choose if confidence is "ambiguous"
3. Respect explicit scope argument if provided (bypasses detection)
