---
name: ocft
description: P2P file transfer between AI agents via message channels. Chunked, resumable, with integrity verification.
homepage: https://github.com/stormixus/ocft
---

# OCFT - OpenClaw File Transfer Protocol

P2P file transfer between AI agents via message channels.

## Links

- **GitHub**: https://github.com/stormixus/ocft
- **npm**: https://www.npmjs.com/package/ocft

## When to Use

Use this skill when:
- Transferring files between AI agents over chat channels
- Setting up peer-to-peer file sharing with trusted agents
- Sending files through Telegram, Discord, Slack, or any text-based channel
- Need chunked transfer with integrity verification

## Installation

```bash
npm install -g ocft
```

## Quick Start

```bash
# Initialize your node (generates unique ID and secret)
ocft init

# View your status
ocft status

# Set max file size (default: 100MB)
ocft set-max-size 1GB

# Export your connection info to share with peers
ocft export

# Add a trusted peer
ocft add-peer <nodeId> <secret> --name "Friend"

# Or import from URI
ocft import ocft://eyJub2RlSWQ...
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `ocft init` | Initialize node with unique ID and secret |
| `ocft status` | Show node status and configuration |
| `ocft show-secret` | Display full secret (careful!) |
| `ocft export` | Export connection info as URI |
| `ocft import <uri>` | Import peer from ocft:// URI |
| `ocft add-peer <id> <secret>` | Add a trusted peer |
| `ocft remove-peer <id>` | Remove a trusted peer |
| `ocft list-peers` | List all trusted peers |
| `ocft set-download <dir>` | Set download directory |
| `ocft set-max-size <size>` | Set max file size (e.g., 500MB, 2GB) |

## Features

- 🔗 **Message-based**: Transfer files through existing chat channels
- 📦 **Chunked transfer**: Split large files into small pieces (48KB chunks)
- ✅ **Integrity verification**: SHA-256 hash for chunks and files
- 🤝 **Request/Accept**: Explicit acceptance or auto-accept policy
- 🔒 **Security**: Trusted peer whitelist with secrets
- ⏰ **Secret TTL**: Set expiry time for trust relationships
- 🔄 **Resume**: Resume interrupted transfers from last chunk
- 📏 **Configurable size limit**: Set max file size up to any limit

## Protocol

OCFT messages use a `🔗OCFT:` prefix with Base64-encoded JSON, allowing file transfers over any text-based channel.

## Limitations

- Chunk size: 48KB (safe for Base64 in messages)
- Default max file size: 100MB (configurable via `ocft set-max-size`)
- Designed for text-based channels
