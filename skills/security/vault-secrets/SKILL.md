---
name: vault-secrets
description: HashiCorp Vault secrets management
allowed-tools: [Bash, Read]
---

# Vault Secrets Skill

## Overview

HashiCorp Vault secrets management with critical safety controls. 90%+ context savings via progressive disclosure.

## Requirements

- Vault CLI installed
- VAULT_ADDR environment variable
- VAULT_TOKEN or authentication method configured

## Tools (Progressive Disclosure)

### Secret Operations

| Tool      | Description          | Confirmation |
| --------- | -------------------- | ------------ |
| kv-get    | Read secret          | Yes          |
| kv-put    | Write secret         | **REQUIRED** |
| kv-delete | Delete secret        | **REQUIRED** |
| kv-list   | List secrets at path | No           |

### Authentication

| Tool         | Description           |
| ------------ | --------------------- |
| token-lookup | Look up current token |
| auth-list    | List auth methods     |
| login        | Authenticate to Vault |

### Policies

| Tool        | Description   |
| ----------- | ------------- |
| policy-list | List policies |
| policy-read | Read policy   |

### PKI

| Tool       | Description        | Confirmation |
| ---------- | ------------------ | ------------ |
| pki-issue  | Issue certificate  | Yes          |
| pki-revoke | Revoke certificate | **REQUIRED** |

### BLOCKED Operations

| Tool               | Status      |
| ------------------ | ----------- |
| operator seal      | **BLOCKED** |
| operator step-down | **BLOCKED** |
| secrets disable    | **BLOCKED** |

## Security

⚠️ **NEVER log or display secret values**
⚠️ **All write/delete operations require confirmation**
⚠️ **Operator commands are BLOCKED**

## Agent Integration

- **security-architect** (primary): Secrets management, policy design
- **devops** (primary): Secret rotation, deployment credentials
- **developer** (secondary): Application secrets access

## Troubleshooting

| Issue              | Solution                         |
| ------------------ | -------------------------------- |
| Permission denied  | Check Vault token and policies   |
| Connection refused | Verify VAULT_ADDR is correct     |
| Token expired      | Re-authenticate with vault login |
