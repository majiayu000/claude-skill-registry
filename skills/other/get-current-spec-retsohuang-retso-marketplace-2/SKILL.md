---
name: get-current-spec
description: This skill should be used when commands need to determine which spec is active, when the user mentions "spec 001", "work on feature X", or when checking current spec context. Resolves the current working specification through user input, progress.yml, or user selection.
allowed-tools: Read, Bash, AskUserQuestion
version: 1.0.0
---

# Get Current Spec

Determine the current working specification through a three-tier priority system that checks user input first, then progress.yml, and finally prompts for user selection.

## Priority Resolution System

1. **User input** - Parse the message for spec references (highest priority)
2. **progress.yml** - Read from `.claude/spec-kit/memory/progress.yml`
3. **User selection** - Prompt user to select from available specs

## Instructions

### Step 1: Parse User Input for Spec References

Check if the user mentioned a specific spec:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/dist/cli.js list-features
```

Look for these patterns in user input:
- Full spec ID: "001-feature-name"
- Spec number: "001", "002", "spec 001"
- Feature name: "user-auth", "work on user-auth"
- Feature reference: "feature 002"

When a match is found:
1. Extract the spec ID (format: `NNN-feature-name`)
2. Call set-current-spec skill to update progress.yml
3. Proceed to output

### Step 2: Read progress.yml

When no spec found in user input, read the stored current spec:

```bash
cat .claude/spec-kit/memory/progress.yml
```

Parse the `currentSpec` field (format: `NNN-feature-name`).

When currentSpec exists and its directory exists at `.claude/spec-kit/specs/{spec-id}/`:
1. Use that spec
2. Proceed to output

### Step 3: Prompt User Selection

When no spec found in input AND no valid currentSpec in progress.yml:

1. List available specs:
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/dist/cli.js list-features
   ```

2. Use AskUserQuestion to present options and let user select

3. Call set-current-spec skill with selected spec ID

## Output Format

Provide the resolved spec context:

```
Current Spec: {NNN}-{feature-name}
Feature Number: {NNN}
Feature Name: {feature-name}
Directory: .claude/spec-kit/specs/{NNN}-{feature-name}/
Source: {user input | progress.yml | user selection}
```

## Usage Notes

- Always attempt user input parsing first before checking progress.yml
- Validate that spec directory exists before using
- Update progress.yml when user specifies a different spec
- Called by all spec-kit commands that need context (plan, tasks, implement, clarify)
