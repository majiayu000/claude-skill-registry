---
name: check-workspace-status
description: Use when asking what targets/sources are configured, or wanting to see current Speakeasy setup
---

# check-workspace-status

## Command

```bash
# For LLMs/automation (recommended)
speakeasy status --output json

# For human-readable output
speakeasy status --output console
```

Requires `SPEAKEASY_API_KEY` env var (see `configure-authentication` skill).

## Output Includes

- Workspace name and account type
- Published targets (version, URLs, last publish/generate)
- Configured targets (unpublished, with repo URLs)
- Unconfigured targets and generation failures
