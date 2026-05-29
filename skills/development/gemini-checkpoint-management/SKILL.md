---
name: gemini-checkpoint-management
description: Central authority for Gemini CLI Checkpointing. Covers git-based file snapshots, automatic state saving, /restore command, and rollback. Use when enabling checkpointing, restoring previous states, undoing changes, or planning experimental workflows with Gemini. Delegates 100% to gemini-cli-docs for official documentation.
allowed-tools: Read, Glob, Grep, Skill
---

# Gemini Checkpoint Management

## MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini checkpointing:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific checkpointing topic
> 3. **BASE** responses EXCLUSIVELY on official documentation loaded

## Overview

Meta-skill for managing Gemini CLI's checkpointing system. Checkpointing creates automatic snapshots before file modifications, enabling instant rollback.

## When to Use This Skill

**Keywords:** checkpoint, rollback, restore, undo, snapshot, revert, experiment, checkpointing, /restore

**Use this skill when:**

- Enabling or configuring checkpointing
- Listing available checkpoints
- Restoring to a previous state
- Understanding checkpoint storage
- Planning experimental workflows

## How Checkpointing Works

When enabled, before any file modification Gemini creates:

1. **Git Snapshot**: Shadow repo at `~/.gemini/history/<project_hash>`
2. **Conversation History**: Complete session state
3. **Pending Tool Call**: The operation about to execute

Checkpoints are stored locally and don't interfere with your project's Git repository.

## Configuration

### Enable Checkpointing

Add to `settings.json`:

```json
{
  "general": {
    "checkpointing": {
      "enabled": true
    }
  }
}
```

### Verify Configuration

```bash
cat ~/.gemini/settings.json | jq '.general.checkpointing'
```

## Commands

### List Checkpoints

```text
/restore
```

Shows available checkpoint files for the current project.

### Restore Checkpoint

```text
/restore <checkpoint_file>
```

Restores files and conversation to the checkpoint state.

### Checkpoint Naming

Format: `{timestamp}-{filename}-{tool_name}`

Example: `2025-06-22T10-00-00_000Z-my-file.txt-write_file`

## Storage Locations

| Data | Location |
| --- | --- |
| Git snapshots | `~/.gemini/history/<project_hash>` |
| Checkpoint metadata | `~/.gemini/tmp/<project_hash>/checkpoints` |

## Keyword Registry (Delegates to gemini-cli-docs)

| Topic | Query Keywords |
| --- | --- |
| Enable | `checkpointing enabled`, `enable checkpointing settings` |
| Commands | `/restore command`, `list checkpoints`, `restore checkpoint` |
| Storage | `checkpoint storage`, `~/.gemini/history`, `snapshot location` |
| Workflow | `checkpointing workflow`, `automatic snapshots` |

## Quick Decision Tree

**What do you want to do?**

1. **Enable checkpointing** -> Query gemini-cli-docs: "checkpointing enabled settings"
2. **List checkpoints** -> Use `/restore` command
3. **Restore state** -> Use `/restore <checkpoint_name>`
4. **Find storage** -> Query gemini-cli-docs: "checkpoint storage ~/.gemini/history"
5. **Understand workflow** -> Query gemini-cli-docs: "checkpointing workflow"

## Best Practices

1. **Enable for experiments**: Always enable when doing risky refactors
2. **Note checkpoint names**: Before major changes, list existing checkpoints
3. **Test after restore**: Verify state after restoring
4. **Clean up periodically**: Old checkpoints consume disk space

## Verification Checkpoint

- [ ] Did I invoke gemini-cli-docs skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

## Test Scenarios

### Scenario 1: Direct Activation

**Query**: "Use the gemini-checkpoint-management skill to enable checkpointing"
**Expected Behavior**:

- Skill activates on keyword "checkpoint"
- Delegates to gemini-cli-docs for official documentation
**Success Criteria**: User receives accurate checkpointing configuration steps

### Scenario 2: Keyword Activation

**Query**: "How do I rollback changes in Gemini CLI?"
**Expected Behavior**:

- Skill activates on keywords "rollback", "restore"
- Provides /restore command usage
**Success Criteria**: Response includes command syntax and checkpoint listing

### Scenario 3: Troubleshooting

**Query**: "Where are Gemini checkpoints stored?"
**Expected Behavior**:

- Skill activates on "checkpoint storage"
- Provides ~/.gemini/history path information
**Success Criteria**: User understands checkpoint storage structure

## References

Query `gemini-cli-docs` for official documentation on:

- "checkpointing"
- "/restore command"
- "checkpoint storage"

## Version History

- v1.1.0 (2025-11-30): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
