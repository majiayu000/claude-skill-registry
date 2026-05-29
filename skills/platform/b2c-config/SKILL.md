---
name: b2c-config
description: Using the b2c CLI to view and debug current configuration for instance, SCAPI, oauth and MRT settings.
---

# B2C Config Skill

Use the `b2c setup config` command to view the resolved configuration and understand where each value comes from. This is essential for debugging configuration issues and verifying that the CLI is using the correct settings.

## When to Use

Use `b2c setup config` when you need to:

- Verify which configuration file is being used
- Check if environment variables are being read correctly
- Debug authentication failures by confirming credentials are loaded
- Understand credential source priority (dw.json vs env vars vs plugins)
- Identify hostname mismatch protection issues
- Verify MRT API key is loaded from ~/.mobify

## Examples

### View Current Configuration

```bash
# Display resolved configuration (sensitive values masked by default)
b2c setup config

# View configuration for a specific instance from dw.json
b2c setup config -i staging

# View configuration with a specific config file
b2c setup config --config /path/to/dw.json
```

### Debug Sensitive Values

```bash
# Show actual passwords, secrets, and API keys (use with caution)
b2c setup config --unmask
```

### JSON Output for Scripting

```bash
# Output as JSON for parsing in scripts
b2c setup config --json

# Pretty-print with jq
b2c setup config --json | jq '.config'

# Check which sources are loaded
b2c setup config --json | jq '.sources'
```

## Understanding the Output

The command displays configuration organized by category:

- **Instance**: hostname, webdavHostname, codeVersion
- **Authentication (Basic)**: username, password (for WebDAV)
- **Authentication (OAuth)**: clientId, clientSecret, scopes, authMethods
- **SCAPI**: shortCode
- **Managed Runtime (MRT)**: mrtProject, mrtEnvironment, mrtApiKey
- **Metadata**: instanceName (from multi-instance configs)
- **Sources**: List of all configuration sources that were loaded

Each value shows its source in brackets:
- `[DwJsonSource]` - Value from dw.json file
- `[MobifySource]` - Value from ~/.mobify file
- `[SFCC_*]` - Value from environment variable
- `[password-store]` - Value from a credential plugin

## Configuration Priority

Values are resolved with this priority (highest to lowest):

1. CLI flags and environment variables
2. Plugin sources (high priority)
3. dw.json file
4. ~/.mobify file (MRT API key only)
5. Plugin sources (low priority)
6. package.json b2c key

When troubleshooting, check the source column to understand which configuration is taking precedence.

## Common Issues

### Missing Values

If a value shows `-`, it means no source provided that configuration. Check:
- Is the field spelled correctly in dw.json?
- Is the environment variable set?
- Does the plugin provide that value?

### Wrong Source Taking Precedence

If a value comes from an unexpected source:
- Higher priority sources override lower ones
- Credential groups (username+password, clientId+clientSecret) are atomic
- Hostname mismatch protection may discard values

### Sensitive Values Masked

By default, passwords and secrets show partial values like `admi...REDACTED`. Use `--unmask` to see full values when debugging authentication issues.

## More Commands

See `b2c setup --help` for other setup commands including `b2c setup skills` for AI agent skill installation.
