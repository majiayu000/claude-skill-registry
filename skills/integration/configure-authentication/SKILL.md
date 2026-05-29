---
name: configure-authentication
description: Use when setting up Speakeasy authentication, configuring API keys, or troubleshooting auth errors in non-interactive/CI environments
---

# configure-authentication

## Quick Setup

Set `SPEAKEASY_API_KEY` environment variable (takes precedence over config files):

```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```

Get your API key: [Speakeasy Dashboard](https://app.speakeasy.com) → Settings → API Keys

## Verifying Authentication

```bash
speakeasy status --output json
```

Returns workspace info if authenticated; `unauthorized` error if not.

## Common Errors

| Error | Solution |
|-------|----------|
| `unauthorized` | Set valid `SPEAKEASY_API_KEY` env var |
| `workspace not found` | Check workspace ID in `~/.speakeasy/config.yaml` |

## Alternative: Config File

Create `~/.speakeasy/config.yaml`:

```yaml
speakeasy_api_key: "<your-api-key>"
speakeasy_workspace_id: "<workspace-id>"  # optional
# For multiple workspaces:
workspace_api_keys:
  org@workspace: "<api-key>"
```
