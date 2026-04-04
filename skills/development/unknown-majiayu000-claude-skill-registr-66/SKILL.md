---
name: deleting-op-secrets
description: Deletes or archives secrets in 1Password using the op CLI. Use when the user needs to permanently remove items, archive deprecated credentials, or clean up unused secrets from 1Password vaults. Supports both permanent deletion and archiving for later recovery.
---

# Overview

This skill enables agents to delete or archive secrets in 1Password using the `op` CLI. It supports permanent deletion for items no longer needed and archiving for items that might need to be recovered later.

The skill assumes the `op` CLI is installed and the user is already authenticated.

# Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Supported Operations](#supported-operations)
- [Workflow](#workflow)
  - [Phase 1: Context Assessment](#phase-1-context-assessment)
  - [Phase 2: Delete Execution](#phase-2-delete-execution)
- [Reference Documentation](#reference-documentation)

# Supported Operations

| Operation | Use Case |
|-----------|----------|
| Delete Item | Permanently remove an item from 1Password |
| Archive Item | Move an item to Archive for potential recovery |

# Workflow

## Phase 1: Context Assessment

### Step 1: Understand the Request

Determine what the user wants to delete or archive:

1. **Identify the target item**:
   - Item name or ID
   - Vault location (if known or ambiguous)

2. **Identify the operation type**:
   - Permanent deletion (item removed completely)
   - Archive (item moved to Archive, recoverable)

3. **Assess the situation**:
   - Is the credential compromised? (permanent delete recommended)
   - Might the item be needed later? (archive recommended)
   - Is this a cleanup of test/duplicate items? (permanent delete)

4. **Clarify if needed**:
   - If item name is ambiguous, ask for vault or use item ID
   - If operation type is unclear, recommend archive as safer option

## Phase 2: Delete Execution

### Step 2: Confirm Deletion

Before executing a destructive operation, confirm with the user:

1. **For permanent deletion**:
   - Warn that this action cannot be undone
   - Confirm the correct item is targeted
   - Suggest archive as alternative if appropriate

2. **For archiving**:
   - Confirm the item will be moved to Archive
   - Explain that archived items can be restored via 1Password app

### Step 3: Execute Delete Command

Based on the context assessment, execute the appropriate `op` command.

See [op CLI Delete Command Reference](references/op-delete-commands.md) for complete command syntax.

**Permanent deletion**:
```bash
op item delete "<item-name>"
```

**Permanent deletion from specific vault**:
```bash
op item delete "<item-name>" --vault "<vault>"
```

**Archive item**:
```bash
op item delete "<item-name>" --archive
```

**Archive from specific vault**:
```bash
op item delete "<item-name>" --vault "<vault>" --archive
```

### Step 4: Handle Errors

Common errors and resolutions:

| Error | Resolution |
|-------|------------|
| `item not found` | Verify item name, try listing items in vault |
| `vault not found` | List available vaults with `op vault list` |
| `more than one item matches` | Use item ID instead of name, or specify vault with `--vault` |
| `permission denied` | Verify vault access permissions |

# Reference Documentation

- [op CLI Delete Command Reference](references/op-delete-commands.md) - Complete command syntax for delete and archive operations
