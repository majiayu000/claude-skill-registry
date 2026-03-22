---
name: surrealfs
description: "SurrealFS virtual filesystem for AI agents. Rust core + Python agent (Pydantic AI). Persistent file operations backed by SurrealDB. Part of the surreal-skills collection."
license: MIT
metadata:
  version: "1.0.4"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-22"
  upstream:
    repo: "surrealdb/surrealfs"
    sha: "0008a3a94dbe"
requires:
  env_vars:
    - name: SURREAL_ENDPOINT
      purpose: "SurrealDB server URL (for remote backend)"
      sensitive: false
    - name: SURREAL_USER
      purpose: "SurrealDB authentication username"
      sensitive: true
    - name: SURREAL_PASS
      purpose: "SurrealDB authentication password"
      sensitive: true
security:
  no_network: false
  no_network_note: "Connects to user-specified SurrealDB endpoint. Python agent hosts HTTP on localhost by default."
  no_credentials: false
  no_credentials_note: "Requires SurrealDB credentials for remote backend connections."
  scripts_auditable: true
  no_obfuscated_code: true
  no_binary_blobs: true
---

# SurrealFS -- Virtual Filesystem for AI Agents

SurrealFS provides a persistent, queryable virtual filesystem backed by SurrealDB.
Designed for AI agents that need durable file operations, hierarchical storage,
and content search across sessions.

## Components

| Component | Crate/Package | Language | Purpose |
|-----------|---------------|----------|---------|
| Core Library | `surrealfs` | Rust | Filesystem operations, CLI REPL, SurrealDB storage layer |
| AI Agent | `surrealfs-ai` | Python (Pydantic AI) | Agent interface with tool integration, HTTP hosting |

## Rust Core -- Commands

The `surrealfs` crate provides a REPL with POSIX-like commands:

| Command | Description |
|---------|-------------|
| `ls` | List directory contents |
| `cat` | Display file contents |
| `tail` | Show last lines of a file |
| `nl` | Number lines of a file |
| `grep` | Search file contents |
| `touch` | Create empty file |
| `mkdir` | Create directory |
| `write_file` | Write content to file |
| `edit` | Edit file contents |
| `cp` | Copy file |
| `cd` | Change directory |
| `pwd` | Print working directory |

Supports piping from external commands: `curl https://example.com > /pages/example.html`

Storage backends:
- Embedded RocksDB (local)
- Remote SurrealDB via WebSocket

## Python AI Agent

Built on Pydantic AI with tools that mirror the filesystem commands.

```python
from surrealfs_ai import build_chat_agent

# Create the agent (default LLM: Claude Haiku)
agent = build_chat_agent()

# Expose over HTTP
import uvicorn
app = agent.to_web()
uvicorn.run(app, host="127.0.0.1", port=7932)
```

Features:
- Default LLM: Claude Haiku
- Telemetry via Pydantic Logfire (OpenTelemetry) -- see Security section for opt-out
- All filesystem operations available as agent tools
- HTTP hosting (default port 7932, bound to 127.0.0.1)
- Path normalization: virtual FS root `/` is isolated; paths cannot escape to host filesystem

## Quick Start

```bash
# Install the Rust core
cargo install surrealfs

# Start the REPL with embedded storage
surrealfs

# Or connect to a remote SurrealDB instance
surrealfs --endpoint ws://localhost:8000 --user root --pass root --ns agent --db workspace

# Install the Python agent
pip install surrealfs-ai

# Run the agent HTTP server
python -m surrealfs_ai --host 127.0.0.1 --port 7932
```

## Use Cases

- Persistent workspace for AI agent sessions
- Hierarchical document storage with metadata queries
- Multi-agent shared file access with SurrealDB permissions
- Content strategy and knowledge management
- Project scaffolding and template management

## Security Considerations

**Credentials**: Remote SurrealDB connections require `--user`/`--pass`. Use
dedicated, least-privilege credentials scoped to a specific namespace/database.
Never use `root` credentials in shared or production environments.

**Telemetry**: The Python agent uses Pydantic Logfire (OpenTelemetry). To
disable telemetry, set: `export LOGFIRE_SEND_TO_LOGFIRE=false` or configure
Logfire with `send_to_logfire=False` in code. Audit telemetry endpoints before
enabling in environments with sensitive data.

**HTTP binding**: The agent binds to `127.0.0.1` by default. Do not expose to
`0.0.0.0` or public networks without authentication and TLS. If running in a
container, use network isolation.

**Pipe commands**: The Rust core supports `curl URL > /path` syntax for content
ingress. This executes the pipe source command on the host. Use only with
trusted URLs in controlled environments. Do not allow untrusted input to
construct pipe commands.

**Sandboxing**: The virtual FS root (`/`) is a SurrealDB-backed abstraction,
not the host filesystem. Path traversal (e.g., `../../etc/passwd`) is
normalized and rejected. However, pipe commands execute on the host -- run
in a container or sandbox if accepting untrusted agent input.

## Full Documentation

See the main skill's rule file for complete guidance:
- **[rules/surrealfs.md](../../rules/surrealfs.md)** -- architecture, Rust core API, Python agent setup, SurrealDB schema, multi-agent patterns, and deployment
- **[surrealdb/surrealfs](https://github.com/surrealdb/surrealfs)** -- upstream repository
