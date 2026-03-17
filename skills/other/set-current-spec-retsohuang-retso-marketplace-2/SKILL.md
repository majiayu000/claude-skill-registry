---
name: set-current-spec
description: This skill should be used when switching between specs, after creating a new spec with "/spec-kit:specify", when the user says "switch to spec 002" or "work on feature X", or when resuming work on a different feature. Updates progress.yml with the current working specification.
allowed-tools: Bash
version: 1.0.0
---

# Set Current Spec

Update the current working specification in `.claude/spec-kit/memory/progress.yml` to track which spec is active.

## Purpose

This skill persists the active spec selection so that subsequent spec-kit commands know which feature to operate on without requiring explicit specification each time.

## Instructions

### Step 1: Validate Spec Exists

Verify the spec directory exists before setting:

```bash
# Check directory exists
test -d .claude/spec-kit/specs/{spec-id}
```

Spec ID format: `NNN-feature-name` (e.g., `001-user-auth`, `002-payment-flow`)

If directory does not exist, report error and list available specs.

### Step 2: Update progress.yml

Set the current spec using the CLI:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/dist/cli.js set-current-spec "{spec-id}"
```

This command:
- Creates `.claude/spec-kit/memory/` directory if needed
- Writes `currentSpec: "{spec-id}"` to progress.yml
- Returns success confirmation with spec details

### Step 3: Confirm Update

Display confirmation to user:

```
✅ Current spec set to: {NNN}-{feature-name}
Location: .claude/spec-kit/specs/{NNN}-{feature-name}/

All spec-kit commands will now operate on this feature.
```

## When This Skill Is Called

**Directly by user:**
- User says "switch to spec 002"
- User says "work on the user-auth feature"
- User wants to change active spec

**Called by other skills:**
- get-current-spec skill when user selects a spec from prompt
- After spec creation by /spec-kit:specify command

**Called by commands:**
- /spec-kit:specify automatically sets new spec as current

## Related Skills

- **get-current-spec** - Determines which spec is active (calls this skill when needed)

## Error Handling

When spec directory not found:
1. List available specs with `list-features` CLI command
2. Suggest correct spec ID format
3. Do not update progress.yml with invalid spec
