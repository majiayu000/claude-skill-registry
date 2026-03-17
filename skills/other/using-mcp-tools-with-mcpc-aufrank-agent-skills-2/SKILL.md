---
name: using-mcp-tools-with-mcpc
description: Use mcpc CLI to interact with MCP servers - call tools, read resources, get prompts. Use when working with Model Context Protocol servers, calling MCP tools, or accessing MCP resources programmatically; prefer key:=value bindings over raw JSON bodies.
allowed-tools: Bash(mcpc:*) Bash(node dist/cli/index.js:*) Read Grep
---

# mcpc: MCP command-line client

Use `mcpc` to interact with MCP (Model Context Protocol) servers from the command line.
This is more efficient than function calling - generate shell commands instead.

## Trust pattern
- **Always**: Read-only mcpc commands in the sandbox (e.g., `tools-list`, `tools-get`, `resources-list/read`, `prompts-list/get`, `tools-call` for read/search-only endpoints), session status checks, and commands that reuse already-created auth profiles.
- **Ask**: Anything that writes or needs network/OAuth (login/logout must be human-initiated in the foreground), connecting to new servers, commands that create/update/delete data, helper scripts that write files, or when sandbox blocks the command.
- **Never**: Destructive workspace actions (moves/deletes) without explicit user request; connecting to unknown MCP servers without instruction; backgrounding `mcpc <server> login` or trying to auto-open a browser.

## Quick reference

```text
# List sessions and auth profiles
mcpc

# Show server info
mcpc <server>
mcpc @<session>

# Tools
mcpc <target> tools-list
mcpc <target> tools-get <tool-name>
mcpc <target> tools-call <tool-name> key:=value key2:="string value"

# Resources
mcpc <target> resources-list
mcpc <target> resources-read <uri>

# Prompts
mcpc <target> prompts-list
mcpc <target> prompts-get <prompt-name> arg1:=value1

# Sessions (persistent connections)
mcpc <server> connect @<name>
mcpc @<name> <command>
mcpc @<name> close

# Authentication
mcpc <server> login
mcpc <server> logout
```

## Target types

- `mcp.example.com` - Direct HTTPS connection to remote server
- `localhost:8080` or `127.0.0.1:8080` - Local HTTP server (http:// is default for localhost)
- `@session-name` - Named persistent session (faster, maintains state)
- `config-entry` - Entry from config file (with `--config`)

## Passing arguments

Prefer `key:=value` bindings. Use inline JSON only when needed (e.g., first-arg object or complex arrays):   

```text
# String values
mcpc @s tools-call search query:="hello world"

# Numbers, booleans, null (auto-parsed as JSON)
mcpc @s tools-call search query:="hello" limit:=10 enabled:=true

# Complex JSON values
mcpc @s tools-call search config:='{"nested":"value"}' items:='[1,2,3]'

# Force string type with JSON quotes
mcpc @s tools-call search id:='"123"'

# Inline JSON object (if first arg starts with { or [)
mcpc @s tools-call search '{"query":"hello","limit":10}'

# From stdin (auto-detected when piped)
echo '{"query":"hello"}' | mcpc @s tools-call search
```

## JSON output for scripting

Always use `--json` flag for machine-readable output:

```text
# Get tools as JSON
mcpc --json @apify tools-list

# Call tool and parse result with jq
mcpc --json @apify tools-call search query:="test" | jq '.content[0].text'

# Chain commands
mcpc --json @server1 tools-call get-data | mcpc @server2 tools-call process
```

## Sessions for efficiency

Create sessions for repeated interactions:

```text
# Create session (or reconnect if exists)
mcpc mcp.apify.com connect @apify

# Use session (faster - no reconnection overhead)
mcpc @apify tools-list
mcpc @apify tools-call search query:="test"

# Restart session (useful after server updates)
mcpc @apify restart

# Close when done
mcpc @apify close
```

**Session states:**
- 🟢 **live** - Bridge running, server might or might not be responding
- 🟡 **crashed** - Bridge crashed; auto-restarts on next use
- 🔴 **expired** - Server rejected session; needs `close` and reconnect

## Authentication

**OAuth (interactive login – human-only, foreground)**:
- `mcpc <server> login` opens the browser; mcpc never opens it itself. Do not background this command or it will miss the localhost callback.
- Run login once per profile, then reuse the saved credentials in scripts.
- Re-run login to refresh/change scopes.

Python preflight to enforce “login first” in scripts (no automatic browser launches):
```python
import json, os, sys

server = os.environ.get("MCP_SERVER", "mcp.apify.com")
profile = os.environ.get("MCP_PROFILE", "default")
profiles_path = os.path.join(os.path.expanduser("~"), ".mcpc", "profiles.json")

try:
    data = json.load(open(profiles_path, "r", encoding="utf-8"))
    profiles = data.get("profiles", [])
except FileNotFoundError:
    profiles = []

has_profile = any(p.get("server") == server and p.get("name") == profile for p in profiles)
if not has_profile:
    print(f"No mcpc auth profile '{profile}' for {server}.")
    print(f"Run this yourself (foreground): mcpc {server} login --profile {profile}")
    sys.exit(1)
```

After the preflight succeeds, scripts may call `mcpc --profile <name> ...` or rely on the default profile.

**Bearer token**:
```text
mcpc -H "Authorization: Bearer $TOKEN" mcp.apify.com tools-list
mcpc -H "Authorization: Bearer $TOKEN" mcp.apify.com connect @myserver
```

## Proxy server for AI isolation

Create a proxy MCP server that hides authentication tokens:

```text
# Human creates authenticated session with proxy
mcpc mcp.apify.com connect @ai-proxy --proxy 8080

# AI agent connects to proxy (no access to original tokens)
# Note: localhost defaults to http://
mcpc localhost:8080 tools-list
mcpc 127.0.0.1:8080 connect @sandboxed
```

## Common patterns

**List and inspect tools**:
```text
mcpc @s tools-list
mcpc @s tools-get tool-name
```

**Call tool and extract text result**:
```text
mcpc --json @s tools-call my-tool | jq -r '.content[0].text'
```

**Read resource content**:
```text
mcpc @s resources-read "file:///path/to/file"
```

**Use config file for local servers**:
```text
mcpc --config .vscode/mcp.json filesystem resources-list
```

## Exit codes

- `0` - Success
- `1` - Client error (invalid arguments)
- `2` - Server error (tool failed)
- `3` - Network error
- `4` - Authentication error

## Debugging

```text
# Verbose output shows protocol details
mcpc --verbose @s tools-call my-tool
```

## Example script

See [`docs/examples/company-lookup.sh`](../examples/company-lookup.sh) for a complete example
of an AI-generated script that validates prerequisites and calls MCP tools.
