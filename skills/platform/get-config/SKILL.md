---
name: get-config
description: Read engine configuration to get vault path. Called by all skills that need to access vault files.
disable-model-invocation: true
---

# Get Config

This sub-skill reads the engine configuration file to get the vault path.

## Instructions

1. Read `.claude/config.md` from the engine root directory

2. Parse the `vault_path:` line to extract the path value

3. Verify the vault path exists:
   - If it doesn't exist, report error: "Vault not found at {path}. Run `/init` to configure."

4. Return the vault path for use in file operations

## Output

Return structured JSON for the orchestrator to capture:

**Success:**
```json
{
  "success": true,
  "VAULT": "/Users/me/OneDrive/vault",
  "config_path": ".claude/config.md"
}
```

**Error:**
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-readable error message",
  "suggestion": "Run `/init` to configure."
}
```

For backwards compatibility, also output the vault path in plain text:
```
$VAULT = /Users/me/OneDrive/vault
```

## Error Cases

| Error Code | Condition | Message |
|------------|-----------|---------|
| `config_missing` | Config file not found | "No config.md found. Run `/init fresh --vault=/path` to set up." |
| `vault_path_missing` | vault_path not in config | "vault_path not configured. Run `/init` to configure." |
| `vault_not_found` | Directory doesn't exist | "Vault not found at {path}. Check path or run `/init reconnect`." |
