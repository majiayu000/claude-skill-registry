---
name: updating-op-secrets
description: Updates existing secrets in 1Password using the op CLI. Use when the user needs to modify passwords, edit field values, add or remove fields, rename items, move items between vaults, or manage tags on existing 1Password items. Supports all item types including Login, Password, API Credential, and Secure Note.
---

# Overview

This skill enables agents to update existing secrets in 1Password using the `op` CLI. It supports comprehensive update operations including editing field values, adding and removing fields, renaming items, moving items between vaults, and managing tags.

The skill assumes the `op` CLI is installed and the user is already authenticated.

# Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Supported Operations](#supported-operations)
- [Workflow](#workflow)
  - [Phase 1: Context Assessment](#phase-1-context-assessment)
  - [Phase 2: Update Execution](#phase-2-update-execution)
- [Reference Documentation](#reference-documentation)

# Supported Operations

| Operation | Use Case |
|-----------|----------|
| Edit Field | Update password, username, credential, or other field values |
| Add Field | Add new custom fields to an existing item |
| Remove Field | Delete custom fields from an item |
| Rename Item | Change an item's title |
| Move Item | Transfer an item to a different vault |
| Manage Tags | Add, replace, or remove tags |

# Workflow

## Phase 1: Context Assessment

### Step 1: Understand the Request

Determine what the user wants to update:

1. **Identify the target item**:
   - Item name or ID
   - Vault location (if known or ambiguous)

2. **Identify the update operation**:
   - Edit field value(s)
   - Add new field(s)
   - Remove field(s)
   - Rename item
   - Move to different vault
   - Modify tags

3. **Gather required information**:
   - For field edits: field name(s) and new value(s)
   - For new fields: section name, field name, field type, value
   - For removal: field name to delete
   - For rename: new title
   - For move: destination vault
   - For tags: tag list to set

4. **Clarify if needed**:
   - If item name is ambiguous, ask for vault or use item ID
   - If field name is ambiguous, ask for section
   - For moves, confirm destination vault exists

## Phase 2: Update Execution

### Step 2: Execute Update Command

Based on the context assessment, execute the appropriate `op` command.

See [op CLI Update Command Reference](references/op-update-commands.md) for complete command syntax.

**Edit field value**:
```bash
op item edit "<item-name>" <field>=<newvalue> --format json
```

**Edit field in section**:
```bash
op item edit "<item-name>" "Section.field"=<newvalue> --format json
```

**Add custom field**:
```bash
op item edit "<item-name>" "Section.newfield[type]"=<value> --format json
```

**Remove custom field**:
```bash
op item edit "<item-name>" "Section.field[delete]" --format json
```

**Rename item**:
```bash
op item edit "<item-name>" --title "<new-title>" --format json
```

**Move to vault**:
```bash
op item move "<item-name>" --destination-vault "<vault>"
```

**Set tags**:
```bash
op item edit "<item-name>" --tags "<tag1>,<tag2>" --format json
```

**Generate new password**:
```bash
op item edit "<item-name>" --generate-password --format json
```

### Step 3: Confirm Update

1. **Parse JSON response** to extract updated item details
2. **Verify update** by checking the response shows expected changes
3. **Present confirmation** to user:
   - Item title and ID
   - Fields that were modified
   - New vault location (if moved)
   - Generated password (if applicable)

**Note**: When moving items, inform the user that the item receives a new ID.

### Step 4: Handle Errors

Common errors and resolutions:

| Error | Resolution |
|-------|------------|
| `item not found` | Verify item name, try listing items in vault |
| `vault not found` | List available vaults with `op vault list` |
| `more than one item matches` | Use item ID instead of name, or specify vault with `--vault` |
| `field not found` | List item fields with `op item get` to verify field name |
| `cannot delete built-in field` | Use empty string to clear: `field=""` |
| `permission denied` | Verify vault access permissions |

# Reference Documentation

- [op CLI Update Command Reference](references/op-update-commands.md) - Complete command syntax for all update operations
