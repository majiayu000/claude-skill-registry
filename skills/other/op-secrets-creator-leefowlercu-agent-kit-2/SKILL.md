---
name: creating-op-secrets
description: Creates secrets in 1Password using the op CLI. Use when the user needs to store new passwords, API keys, login credentials, or secure notes in 1Password. Supports Login, Password, API Credential, and Secure Note item types with optional vault selection and password generation.
---

# Overview

This skill enables agents to create secrets in 1Password using the `op` CLI. It supports creating Login, Password, API Credential, and Secure Note items with template support and vault selection.

The skill assumes the `op` CLI is installed and the user is already authenticated.

# Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Supported Item Types](#supported-item-types)
- [Workflow](#workflow)
  - [Phase 1: Context Assessment](#phase-1-context-assessment)
  - [Phase 2: Secret Creation](#phase-2-secret-creation)
- [Reference Documentation](#reference-documentation)

# Supported Item Types

| Type | Category | Use Case |
|------|----------|----------|
| Login | LOGIN | Website accounts, application logins |
| Password | PASSWORD | Standalone passwords, WiFi, PINs |
| API Credential | API_CREDENTIAL | API keys, access tokens, service credentials |
| Secure Note | SECURE_NOTE | Text notes, recovery codes, configurations |

# Workflow

## Phase 1: Context Assessment

### Step 1: Understand the Request

Determine what the user wants to create:

1. **Identify the item type**:
   - Login: Has username/password for a website or service
   - Password: Standalone password without login context
   - API Credential: API key, token, or service credential
   - Secure Note: Text information to store securely

2. **Gather required information**:
   - Title for the item (required)
   - Target vault (optional, uses default if not specified)
   - Field values based on item type

3. **Check for special requirements**:
   - Should password be auto-generated?
   - Are there tags to apply?
   - Any custom sections needed?

See [Item Templates Reference](references/item-templates.md) for field requirements per type.

## Phase 2: Secret Creation

### Step 2: Gather Field Values

Based on the item type, collect the necessary field values:

**Login**:
- `username`: Account username or email
- `password`: Account password (or use `--generate-password`)
- `url`: Website URL (via `--url` flag)

**Password**:
- `password`: The password value (or use `--generate-password`)

**API Credential**:
- `credential`: The API key or secret
- `username`: Optional key identifier

**Secure Note**:
- `notesPlain`: The note content

### Step 3: Execute Create Command

Build and execute the appropriate `op item create` command.

See [op CLI Create Command Reference](references/op-create-commands.md) for complete syntax.

**Basic pattern**:
```bash
op item create --category <CATEGORY> \
  --title "<title>" \
  [--vault "<vault>"] \
  [field assignments...] \
  --format json
```

**With generated password**:
```bash
op item create --category Login \
  --title "<title>" \
  --generate-password=24 \
  username=<user> \
  --format json
```

### Step 4: Confirm Creation

1. **Parse JSON response** to extract item details
2. **Verify creation** by checking for item ID in response
3. **Present confirmation** to user:
   - Item title and ID
   - Vault location
   - Generated password (if applicable)

### Step 5: Handle Errors

Common errors and resolutions:

| Error | Resolution |
|-------|------------|
| `vault not found` | List vaults with `op vault list`, verify name |
| `already exists` | Use different title or update existing item |
| `invalid category` | Use valid category: Login, Password, "API Credential", "Secure Note" |
| `missing required field` | Provide required fields for the category |

# Reference Documentation

- [op CLI Create Command Reference](references/op-create-commands.md) - Complete command syntax and options
- [Item Templates Reference](references/item-templates.md) - Field structures for each item type
