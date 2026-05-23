---
name: aria2-json-rpc
description: Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands. Use when working with aria2, download management, or torrent operations.
license: MIT
compatibility: Requires Python 3.6+. WebSocket support requires websockets package (pip install websockets) and Python version must match dependency requirements.
metadata:
  author: ISON
  version: "1.1.0"
---

## What This Skill Does

This skill enables you to control aria2 download manager through natural language commands:
- Download files (HTTP/HTTPS/FTP/Magnet/Torrent/Metalink)
- Monitor download progress and status
- Control downloads (pause, resume, remove)
- Manage batch operations (pause all, resume all)
- View statistics and configure options

## How to Use (For AI Agents)

**⚠️ CRITICAL: DO NOT manually construct JSON-RPC requests.**

**✅ ALWAYS use the Python scripts in the `scripts/` directory.**

**⚠️ IMPORTANT: Use `python3` command, NOT `python`** (especially on macOS where `python` symlink doesn't exist)

### Workflow (MUST FOLLOW)

**Step 1: Check Configuration Status**

Before executing any aria2 commands, ALWAYS check if configuration is ready:

```bash
python3 scripts/config_loader.py test
```

- If **successful**: Proceed to execute user's command
- If **failed**: Guide user to initialize configuration (see Step 2)

**Step 2: Initialize Configuration (if needed)**

If connection test fails, guide user to set up configuration:

```bash
# Recommended: User config (survives skill updates)
python3 scripts/config_loader.py init --user

# Alternative: Local config (project-specific)
python3 scripts/config_loader.py init --local
```

Then instruct user to edit the generated config file with their aria2 server details.

**Step 3: Execute User Commands**

Once configuration is ready, execute the requested aria2 operations.

### Example Workflow

**User:** "download http://example.com/file.zip"

**You execute:**
```bash
# 1. Check configuration
python3 scripts/config_loader.py test
```

If test passes:
```bash
# 2. Execute download command
python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'
```

**You respond:** "✓ Download started! GID: 2089b05ecca3d829"

If test fails:
```
Configuration not ready. Please initialize:
1. Run: python3 scripts/config_loader.py init --user
2. Edit ~/.config/aria2-skill/config.json with your aria2 server details
3. Run: python3 scripts/config_loader.py test (to verify)
```

## Documentation Structure

**For detailed execution instructions, see:**
- **[references/execution-guide.md](references/execution-guide.md)** - Complete guide for AI agents with:
  - Command mapping table (user intent → script call)
  - Parameter formatting rules
  - Step-by-step examples
  - Common mistakes to avoid
  - Response formatting guidelines

**For aria2 method reference, see:**
- **[references/aria2-methods.md](references/aria2-methods.md)** - Detailed aria2 RPC method documentation

## Common Commands Quick Reference

| User Intent | Command Example |
|-------------|----------------|
| Download a file | `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'` |
| Check status | `python3 scripts/rpc_client.py aria2.tellStatus <GID>` |
| List active downloads | `python3 scripts/rpc_client.py aria2.tellActive` |
| List stopped downloads | `python3 scripts/rpc_client.py aria2.tellStopped 0 100` |
| Pause download | `python3 scripts/rpc_client.py aria2.pause <GID>` |
| Resume download | `python3 scripts/rpc_client.py aria2.unpause <GID>` |
| Show statistics | `python3 scripts/rpc_client.py aria2.getGlobalStat` |
| Show version | `python3 scripts/rpc_client.py aria2.getVersion` |
| Purge results | `python3 scripts/rpc_client.py aria2.purgeDownloadResult` |

For detailed usage and more commands, see [execution-guide.md](references/execution-guide.md).

## Available Scripts

- `scripts/rpc_client.py` - Main interface for RPC calls
- `scripts/examples/list-downloads.py` - Formatted download list
- `scripts/examples/pause-all.py` - Pause all downloads
- `scripts/examples/add-torrent.py` - Add torrent downloads
- `scripts/examples/monitor-downloads.py` - Real-time monitoring
- `scripts/examples/set-options.py` - Modify options

## Configuration

Scripts automatically load configuration from multiple sources with the following priority (highest to lowest):

### Configuration Priority

1. **Environment Variables** (highest priority - temporary override)
   - `ARIA2_RPC_HOST`, `ARIA2_RPC_PORT`, `ARIA2_RPC_PATH`, etc.
   - Best for: CI/CD pipelines, temporary overrides, testing
   - **Note**: For reference only. Agents should use config files instead.

2. **Skill Directory Config** (project-specific configuration)
   - Location: `skills/aria2-json-rpc/config.json`
   - Best for: Project-specific settings, local testing, development
   - ⚠️ **Warning**: Lost when running `npx skills add` to update the skill

3. **User Config Directory** (global fallback, update-safe) 🆕
   - Location: `~/.config/aria2-skill/config.json`
   - Best for: Personal default settings across all projects
   - ✅ **Safe**: Survives skill updates via `npx skills add`

4. **Defaults** (localhost:6800)
   - Zero-configuration fallback for local development

### Configuration Options

- **host**: Hostname or IP address (default: `localhost`)
- **port**: Port number (default: `6800`)
- **path**: URL path (default: `null`). Set to `/jsonrpc` for standard aria2, or custom path for reverse proxy
- **secret**: RPC secret token (default: `null`)
- **secure**: Use HTTPS instead of HTTP (default: `false`)
- **timeout**: Request timeout in milliseconds (default: `30000`)

### Quick Setup (For AI Agents)

**IMPORTANT**: Always use Python scripts to manage configuration. Do NOT use shell commands directly.

**Step 1: Check current configuration status**
```bash
python3 scripts/config_loader.py show
```

**Step 2: Initialize configuration if needed**

User config (recommended - survives updates):
```bash
python3 scripts/config_loader.py init --user
```

Local config (project-specific):
```bash
python3 scripts/config_loader.py init --local
```

**Step 3: Guide user to edit the config file**

After initialization, the tool will display the config file path. Instruct user to edit it with their aria2 server details (host, port, secret, etc.).

**Step 4: Verify configuration**
```bash
python3 scripts/config_loader.py test
```

Example config file content:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "your-secret-token",
  "secure": false,
  "timeout": 30000
}
```

### Configuration Management (For AI Agents)

**Available Python scripts for configuration management:**

```bash
# Check current configuration and source
python3 scripts/config_loader.py show

# Initialize user config (recommended - update-safe)
python3 scripts/config_loader.py init --user

# Initialize local config (project-specific)
python3 scripts/config_loader.py init --local

# Test connection to aria2 server
python3 scripts/config_loader.py test
```

**Agent Workflow for Configuration Setup:**

1. **Check if config exists**: Run `python3 scripts/config_loader.py show`
2. **If config missing or invalid**: Guide user to run `python3 scripts/config_loader.py init --user`
3. **User edits config**: Tell user the file path and required fields (host, port, secret)
4. **Verify setup**: Run `python3 scripts/config_loader.py test`
5. **Proceed with operations**: Once test passes, execute user's aria2 commands

### Advanced Configuration

**Reverse Proxy Setup:**

For reverse proxy setups like `https://example.com:443/jsonrpc`, the config file should contain:

```json
{
  "host": "example.com",
  "port": 443,
  "path": "/jsonrpc",
  "secret": "your-secret-token",
  "secure": true
}
```

**Environment Variables (for reference only):**

Configuration can also be overridden via environment variables:
- `ARIA2_RPC_HOST`: Hostname
- `ARIA2_RPC_PORT`: Port number
- `ARIA2_RPC_PATH`: URL path
- `ARIA2_RPC_SECRET`: Secret token
- `ARIA2_RPC_SECURE`: "true" or "false"

Note: Use Python scripts for configuration management. Environment variables are documented here for reference only.

## Key Principles (For AI Agents)

1. **Never** construct JSON-RPC requests manually
2. **Always** call Python scripts via Bash tool using `python3` (not `python`)
3. **Always** check configuration before executing commands:
   - Run `python3 scripts/config_loader.py test` first
   - If test fails, guide user through initialization
4. **Never** run raw shell commands (mkdir, cat, export, etc.) directly
   - Use Python scripts: `config_loader.py init`, `config_loader.py show`, etc.
5. **Parse** script output and format for users
6. **Refer to** execution-guide.md when unsure

## Supported Operations

### Download Management
- Add downloads (HTTP/FTP/Magnet/Torrent/Metalink)
- Pause/resume (individual or all)
- Remove downloads
- Add with custom options

### Monitoring
- Check download status
- List active/waiting/stopped downloads
- Get global statistics
- Real-time monitoring

### Configuration
- Get/change download options
- Get/change global options
- Query aria2 version
- List available methods

### Maintenance
- Purge download results
- Remove specific results

## Need Help?

- **Execution details:** [references/execution-guide.md](references/execution-guide.md)
- **Method reference:** [references/aria2-methods.md](references/aria2-methods.md)
- **Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)
- **aria2 official docs:** https://aria2.github.io/
