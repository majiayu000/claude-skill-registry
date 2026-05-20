---
name: elnora-admin
description: >
  Use this skill when the user asks about "Elnora account", "API keys",
  "audit log", "feature flags", "health check", "terms of service",
  "platform status", "feedback", "invitation", or any Elnora platform
  administration task.
---

# Elnora Admin

Platform administration tools for account management, API keys, audit logs,
feature flags, agreements, invitations, and system health.

## Auth

The Elnora MCP server handles authentication automatically via OAuth 2.1
(browser popup) or API key bearer tokens in the MCP connection headers.
There is no manual login/logout step — auth "just works" when the MCP
server is configured.

## Core Concepts

- **Health check** requires no authentication — use it to verify the platform is up.
- **API keys** are shown in full **only once** at creation time. Store them securely immediately.
- **Audit logs** track actions across the org. Filterable by org, action type, and user.
- **Feature flags** are read-only. Use them to check what capabilities are enabled.
- **Agreements** (terms of service) must be accepted before using certain features.
- **Invitations** can be inspected and accepted to join an org.

## Tools Reference

### System Health

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_health_check` | Check platform status | — (no auth required) |

### Account

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_get_account` | Get current user's account info | — |
| `elnora_update_account` | Update account details | fields to update |

### API Keys

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_api_keys` | List existing API keys | — |
| `elnora_create_api_key` | Create a new API key | `name` |
| `elnora_revoke_api_key` | Revoke an API key | `key_id` |

**Critical**: `elnora_create_api_key` returns the full key **only once**. The key is never
shown again. Always present it to the user immediately and remind them to store it securely.

### Agreements

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_agreements` | List terms/agreements | — |
| `elnora_accept_terms` | Accept terms of service | `agreement_id` |

### Feedback

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_submit_feedback` | Submit platform feedback | `message`, optional `type` |

### Audit Log

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_audit_log` | Query audit events | `org_id`, optional filters |

Filters may include action type, user, and date range. Always scope to a specific
`org_id` to get relevant results.

### Feature Flags

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_flags` | List all feature flags | — |
| `elnora_get_flag` | Get a specific flag's value | `flag_name` |

Feature flags are **read-only**. Use them to check whether a feature is enabled
before attempting to use it.

### Invitations

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_get_invitation_info` | Inspect an invitation | `invitation_id` |
| `elnora_accept_invitation` | Accept an org invitation | `invitation_id` |

## Common Workflows

### Check platform health

1. `elnora_health_check` — no auth needed, confirms the API is reachable

### Create and store an API key

1. `elnora_create_api_key` with a descriptive `name`
2. **Immediately** present the returned key to the user
3. Remind them this is the only time the full key is shown

### Review audit activity

1. `elnora_list_audit_log` with `org_id` and any desired filters
2. Paginate if needed — check response for pagination fields

### Check feature availability

1. `elnora_list_flags` to see all flags, or `elnora_get_flag` for a specific one
2. Use the flag value to decide whether to proceed with a feature

### Accept an invitation

1. `elnora_get_invitation_info` with `invitation_id` to review details
2. `elnora_accept_invitation` to join the org

### View and accept terms

1. `elnora_list_agreements` to see pending agreements
2. `elnora_accept_terms` with the `agreement_id` to accept

## ID Format

All IDs are UUIDs (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).
