---
name: b2c-code
description: Deploy and manage code versions on B2C Commerce instances. Use when uploading cartridges, activating code versions, watching for file changes during development, or syncing local code to sandbox.
---

# B2C Code Skill

Use the `b2c` CLI plugin to deploy and manage code versions on Salesforce B2C Commerce instances.

## Examples

### Deploy Cartridges

```bash
# deploy all cartridges from current directory
b2c code deploy

# deploy cartridges from a specific directory
b2c code deploy ./my-cartridges

# deploy to a specific server and code version
b2c code deploy --server my-sandbox.demandware.net --code-version v1

# deploy and reload (re-activate) the code version
b2c code deploy --reload

# delete existing cartridges before upload and reload
b2c code deploy --delete --reload

# deploy only specific cartridges
b2c code deploy -c app_storefront_base -c plugin_applepay

# exclude specific cartridges from deployment
b2c code deploy -x test_cartridge
```

### Watch for Changes

```bash
# watch cartridges and upload changes automatically
b2c code watch

# watch a specific directory
b2c code watch ./my-cartridges

# watch with specific server and code version
b2c code watch --server my-sandbox.demandware.net --code-version v1

# watch only specific cartridges
b2c code watch -c app_storefront_base

# watch excluding specific cartridges
b2c code watch -x test_cartridge
```

### List Code Versions

```bash
# list code versions on the instance
b2c code list

# list with JSON output
b2c code list --json
```

### Activate Code Version

```bash
# activate a code version
b2c code activate <version-name>

# reload (re-activate) the current code version
b2c code activate --reload
```

**Note:** Activating a code version triggers Custom API endpoint registration. If you've added or modified Custom APIs, use `--reload` with deploy or activate to register them. Check registration status with the `b2c-cli:b2c-scapi-custom` skill.

### Delete Code Version

```bash
# delete a code version
b2c code delete <version-name>
```

### More Commands

See `b2c code --help` for a full list of available commands and options in the `code` topic.

## Related Skills

- `b2c-cli:b2c-scapi-custom` - Check Custom API registration status after deployment
- `b2c-cli:b2c-webdav` - Low-level file operations (delete cartridges, list files)
- `b2c:b2c-custom-api-development` - Creating Custom API endpoints
