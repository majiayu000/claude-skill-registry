---
name: reading-op-secrets
description: Reads secrets from 1Password using the op CLI. Use when the user needs to retrieve passwords, API keys, credentials, documents, or one-time passwords stored in 1Password. Supports reading items by name or ID, extracting specific fields, listing vault contents, and reading secret references.
---

# Overview

This skill enables agents to read secrets from 1Password using the `op` CLI. It supports comprehensive read operations including full items, specific fields, documents, attachments, and one-time passwords.

The skill assumes the `op` CLI is installed and the user is already authenticated.

# Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Supported Operations](#supported-operations)
- [Workflow](#workflow)
  - [Phase 1: Context Assessment](#phase-1-context-assessment)
  - [Phase 2: Secret Retrieval](#phase-2-secret-retrieval)
- [Reference Documentation](#reference-documentation)

# Supported Operations

| Operation | Use Case |
|-----------|----------|
| Get Item | Retrieve complete item with all fields |
| Get Field | Extract specific field value(s) |
| List Items | Browse items in vault(s) |
| Get Document | Retrieve document content |
| Get OTP | Get current one-time password |
| Read Reference | Read using `op://` secret reference |

# Workflow

## Phase 1: Context Assessment

### Step 1: Understand the Request

Determine what the user needs:

1. **Identify the secret type**:
   - Specific item (name or ID known)
   - Specific field from an item
   - List of items (browsing/searching)
   - Document content
   - One-time password
   - Secret reference (`op://` URI)

2. **Identify scope**:
   - Specific vault or search all vaults
   - Any filtering criteria (tags, categories)

3. **Clarify if needed**:
   - If item name is ambiguous, ask for vault or use item ID
   - If multiple fields could match, ask which specific field

## Phase 2: Secret Retrieval

### Step 2: Execute the Appropriate Command

Based on the context assessment, execute the appropriate `op` command.

See [op CLI Read Command Reference](references/op-read-commands.md) for complete command syntax.

**Get Complete Item**:
```bash
op item get "<item-name>" --format json
```

**Get Specific Field**:
```bash
op item get "<item-name>" --fields "<field-name>" --format json
```

**List Items**:
```bash
op item list [--vault "<vault>"] [--categories <category>] --format json
```

**Get Document**:
```bash
op document get "<document-name>"
```

**Get OTP**:
```bash
op item get "<item-name>" --otp
```

**Read Secret Reference**:
```bash
op read "op://<vault>/<item>/<field>"
```

### Step 3: Parse and Present Results

1. **Parse JSON output** (when using `--format json`)
2. **Extract relevant information** based on user's request
3. **Present clearly**:
   - For single values: provide the value directly
   - For items: summarize fields, highlight requested data
   - For lists: present in table format with key metadata

See [Output Schemas Reference](references/output-schemas.md) for JSON structure details.

### Step 4: Handle Errors

Common errors and resolutions:

| Error | Resolution |
|-------|------------|
| `item not found` | Verify item name, try listing items in vault |
| `vault not found` | List available vaults with `op vault list` |
| `more than one item matches` | Use item ID instead of name, or specify vault |
| `field not found` | List item fields with full `op item get` |

# Reference Documentation

- [op CLI Read Command Reference](references/op-read-commands.md) - Complete command syntax for all read operations
- [Output Schemas Reference](references/output-schemas.md) - JSON output structure examples
