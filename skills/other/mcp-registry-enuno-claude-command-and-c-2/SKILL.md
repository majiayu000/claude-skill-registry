---
name: mcp-registry
description: Official MCP Registry for discovering and publishing Model Context Protocol servers - the app store for MCP servers
version: 1.0.0
tags: [mcp, model-context-protocol, registry, server-discovery, mcp-publisher, npm, pypi, docker]
---

# MCP Registry

The MCP Registry provides MCP clients with a list of MCP servers, functioning like an app store for MCP servers. It enables discoverability and integration of Model Context Protocol servers across the ecosystem.

## Key Features

- **Server Discovery** - Find and integrate MCP servers
- **Multi-Platform Publishing** - npm, PyPI, NuGet, Docker, MCPB support
- **Authentication Options** - GitHub OAuth, OIDC, DNS, HTTP verification
- **Remote Servers** - Streamable HTTP and SSE transport
- **Version Management** - Semantic versioning with immutable publications
- **GitHub Actions** - Automated CI/CD publishing workflows
- **Namespace Validation** - Verified ownership of server identities

## API Status

The Registry API is at **v0.1 (API Freeze)** - no breaking changes while validating real-world implementations. General availability planned after feedback period.

**Live API Documentation**: https://registry.modelcontextprotocol.io/docs

## Quick Start

### 1. Install Publisher CLI

```bash
# macOS (Homebrew)
brew install modelcontextprotocol/tap/mcp-publisher

# Or download pre-built binaries from GitHub releases
# https://github.com/modelcontextprotocol/registry/releases
```

### 2. Initialize Server Configuration

```bash
# Generate server.json template
mcp-publisher init

# Validate without publishing
mcp-publisher validate
```

### 3. Authenticate

```bash
# GitHub OAuth (interactive)
mcp-publisher login github

# GitHub Actions OIDC (automated)
mcp-publisher login github-oidc

# DNS verification
mcp-publisher login dns --domain example.com --private-key-file key.pem

# HTTP verification
mcp-publisher login http --domain example.com --private-key-file key.pem
```

### 4. Publish

```bash
mcp-publisher publish
```

## Publisher CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Create server.json template (auto-detects project metadata) |
| `login` | Authenticate with the registry |
| `logout` | Clear saved authentication |
| `publish` | Publish server.json to the registry |
| `validate` | Validate server.json without publishing |
| `--version` | Display version, commit hash, and build timestamp |

## Server Configuration (server.json)

### Basic Structure

```json
{
  "$schema": "https://registry.modelcontextprotocol.io/schemas/server.json",
  "name": "io.github.username/server-name",
  "title": "My MCP Server",
  "description": "A useful MCP server for...",
  "version": "1.0.0",
  "repository": "https://github.com/username/server-name",
  "website": "https://example.com",
  "icon": "https://example.com/icon.png",
  "packages": [...],
  "remotes": [...]
}
```

### Name Format Requirements

| Auth Method | Name Pattern | Example |
|-------------|--------------|---------|
| GitHub | `io.github.username/*` | `io.github.alice/weather-server` |
| GitHub Org | `io.github.orgname/*` | `io.github.anthropic/everything` |
| Domain | `com.example.*/*` | `io.modelcontextprotocol/everything` |

**Constraints**:
- Pattern: `^[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+$`
- Length: 3-200 characters
- Must contain exactly one forward slash

### Description Limits

- Length: 1-100 characters
- Keep concise and descriptive

## Package Types

### npm Packages

```json
{
  "packages": [{
    "registryType": "npm",
    "name": "@username/my-server",
    "version": "1.0.0",
    "runtime": "node",
    "runtimeArgs": ["--experimental-fetch"]
  }]
}
```

**Verification**: Add `mcpName` to package.json matching server name.

```json
{
  "name": "@username/my-server",
  "mcpName": "io.github.username/my-server"
}
```

### PyPI Packages

```json
{
  "packages": [{
    "registryType": "pypi",
    "name": "my-mcp-server",
    "version": "1.0.0",
    "runtime": "python"
  }]
}
```

**Verification**: Add to README (can be hidden in comment):
```
mcp-name: io.github.username/my-server
```

### NuGet Packages

```json
{
  "packages": [{
    "registryType": "nuget",
    "name": "MyMcpServer",
    "version": "1.0.0",
    "runtime": "dotnet"
  }]
}
```

**Verification**: Same as PyPI - `mcp-name` in README.

### Docker/OCI Images

```json
{
  "packages": [{
    "registryType": "oci",
    "identifier": "ghcr.io/username/my-server:1.0.0"
  }]
}
```

**Supported Registries**:
- Docker Hub
- GitHub Container Registry (ghcr.io)
- Google Artifact Registry
- Azure Container Registry
- Microsoft Container Registry

**Verification**: Add Dockerfile label:
```dockerfile
LABEL io.modelcontextprotocol.server.name="io.github.username/my-server"
```

### MCPB Packages (Binary Releases)

```json
{
  "packages": [{
    "registryType": "mcpb",
    "identifier": "https://github.com/username/server/releases/download/v1.0.0/server-mcp-linux-amd64",
    "fileSha256": "abc123..."
  }]
}
```

**Requirements**:
- URL must contain the string "mcp"
- SHA256 checksum required for integrity

## Remote Servers

### Streamable HTTP (Recommended)

```json
{
  "remotes": [{
    "type": "streamable-http",
    "url": "https://api.example.com/mcp"
  }]
}
```

### Server-Sent Events (SSE)

```json
{
  "remotes": [{
    "type": "sse",
    "url": "https://api.example.com/mcp/sse"
  }]
}
```

### URL Template Variables

Support dynamic configuration for multi-tenant deployments:

```json
{
  "remotes": [{
    "type": "streamable-http",
    "url": "https://api.example.com/{tenant_id}/mcp",
    "variables": {
      "tenant_id": {
        "description": "Your organization's tenant identifier",
        "isRequired": true
      }
    }
  }]
}
```

**Variable Properties**:
- `description` - Explains the variable's purpose
- `isRequired` - Marks mandatory fields
- `default` - Provides fallback values
- `choices` - Offers predefined options
- `isSecret` - Indicates sensitive data

### HTTP Headers

Configure authentication headers for clients:

```json
{
  "remotes": [{
    "type": "streamable-http",
    "url": "https://api.example.com/mcp",
    "headers": [{
      "name": "Authorization",
      "description": "Bearer token for API access",
      "isRequired": true,
      "isSecret": true
    }]
  }]
}
```

### Hybrid Deployment

Combine remote and local packages in same server.json:

```json
{
  "packages": [{
    "registryType": "npm",
    "name": "@example/server"
  }],
  "remotes": [{
    "type": "streamable-http",
    "url": "https://api.example.com/mcp"
  }]
}
```

## Authentication Methods

### GitHub OAuth

Interactive browser-based authentication:

```bash
mcp-publisher login github
# Opens browser for GitHub authorization
# Enter device code when prompted
```

### GitHub OIDC (CI/CD)

For automated publishing from GitHub Actions:

```bash
mcp-publisher login github-oidc
```

Requires `id-token: write` permission in workflow.

### DNS Verification

Domain ownership via TXT record:

1. Generate Ed25519, ECDSA P-384, or cloud KMS key pair
2. Create TXT record:
   ```
   _mcp-registry.example.com TXT "v=MCPv1; k=ed25519; p=${PUBLIC_KEY}"
   ```
3. Login:
   ```bash
   mcp-publisher login dns --domain example.com --private-key-file key.pem
   ```

### HTTP Verification

Domain ownership via well-known file:

1. Generate key pair
2. Host file at `https://example.com/.well-known/mcp-registry-auth`:
   ```
   v=MCPv1; k=ed25519; p=${PUBLIC_KEY}
   ```
3. Login:
   ```bash
   mcp-publisher login http --domain example.com --private-key-file key.pem
   ```

## Versioning

### Requirements

- Version must be unique for each publication
- Once published, version and metadata are immutable
- Version range indicators are prohibited (`^`, `~`, `>=`, `*`)

### Recommended Formats

| Format | Example |
|--------|---------|
| Semantic | `1.0.0` |
| Prerelease | `2.1.3-alpha`, `1.0.0-beta.1` |
| Date-based | `2025.11.25` |
| Prefixed | `v1.0` |

### Best Practices

- Align server version with underlying package versions
- For remote APIs, match server version to API version
- Use prerelease notation (`1.2.3-1`) for metadata-only updates

## GitHub Actions Integration

### OIDC Authentication (Recommended)

```yaml
name: Publish MCP Server
on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build and test
        run: |
          npm run build
          npm test

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Install mcp-publisher
        run: |
          curl -L https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher-linux-amd64 -o mcp-publisher
          chmod +x mcp-publisher

      - name: Publish to MCP Registry
        run: |
          ./mcp-publisher login github-oidc
          ./mcp-publisher publish
```

### GitHub PAT Authentication

```yaml
- name: Publish to MCP Registry
  run: |
    ./mcp-publisher login github --token ${{ secrets.MCP_GITHUB_TOKEN }}
    ./mcp-publisher publish
```

**Required scopes**: `read:org`, `read:user`

### DNS Authentication

```yaml
- name: Publish to MCP Registry
  run: |
    echo "${{ secrets.MCP_PRIVATE_KEY }}" > key.pem
    ./mcp-publisher login dns --domain example.com --private-key-file key.pem
    ./mcp-publisher publish
    rm key.pem
```

### Triggering Deployment

```bash
git tag v1.0.0
git push origin v1.0.0
```

## API Reference

### List Servers

```bash
GET https://registry.modelcontextprotocol.io/api/v0/servers
```

### Get Server

```bash
GET https://registry.modelcontextprotocol.io/api/v0/servers/{name}
```

### Search Servers

```bash
GET https://registry.modelcontextprotocol.io/api/v0/servers?q=weather
```

### Response Structure

```json
{
  "servers": [{
    "name": "io.github.username/weather-server",
    "title": "Weather Server",
    "description": "Get weather data from any location",
    "version": "1.0.0",
    "packages": [...],
    "remotes": [...],
    "meta": {
      "io.modelcontextprotocol.registry": {
        "status": "published",
        "publishedAt": "2025-01-15T12:00:00Z",
        "updatedAt": "2025-01-15T12:00:00Z",
        "isLatest": true
      }
    }
  }],
  "meta": {
    "cursor": "abc123",
    "count": 100
  }
}
```

## Development Setup

### Prerequisites

- Docker
- Go 1.24.x
- ko (container image builder)
- golangci-lint v2.4.0

### Running Locally

```bash
# Clone repository
git clone https://github.com/modelcontextprotocol/registry.git
cd registry

# Start development environment
make dev-compose
# Registry available at localhost:8080
# Database resets on restart

# Build publisher CLI
make publisher
./bin/mcp-publisher --help
```

### Pre-built Container Images

Available at GitHub Container Registry:
- Release tags
- Continuous builds from main
- Development builds

## Publishing Workflow (npm Example)

### Step 1: Add Verification Metadata

```json
// package.json
{
  "name": "@username/my-mcp-server",
  "version": "1.0.0",
  "mcpName": "io.github.username/my-server"
}
```

### Step 2: Publish to npm

```bash
npm run build
npm publish
```

### Step 3: Create server.json

```bash
mcp-publisher init
```

Edit generated file:
```json
{
  "$schema": "https://registry.modelcontextprotocol.io/schemas/server.json",
  "name": "io.github.username/my-server",
  "title": "My Server",
  "description": "Useful MCP server",
  "version": "1.0.0",
  "repository": "https://github.com/username/my-server",
  "packages": [{
    "registryType": "npm",
    "name": "@username/my-mcp-server",
    "version": "1.0.0",
    "runtime": "node"
  }]
}
```

### Step 4: Authenticate and Publish

```bash
mcp-publisher login github
mcp-publisher publish
```

### Step 5: Verify

```bash
curl "https://registry.modelcontextprotocol.io/api/v0/servers/io.github.username/my-server"
```

## Troubleshooting

### Authentication Errors

| Issue | Solution |
|-------|----------|
| Token expired | Re-run `mcp-publisher login` |
| Namespace mismatch | Ensure server name matches your GitHub username/org |
| OIDC permission denied | Add `id-token: write` to workflow |

### Validation Failures

| Issue | Solution |
|-------|----------|
| Missing mcpName | Add `mcpName` to package.json matching server name |
| Invalid version | Use semantic versioning without range indicators |
| Name format error | Use reverse-DNS format with single slash |

### Publishing Failures

| Issue | Solution |
|-------|----------|
| Package not found | Ensure npm/PyPI package is published first |
| Verification failed | Check mcpName/mcp-name matches exactly |
| Already published | Increment version number |

## Community & Resources

- **Discord** - Real-time discussion
- **GitHub Discussions** - Product/technical requirements
- **GitHub Issues** - Technical work tracking
- **API Docs** - https://registry.modelcontextprotocol.io/docs

## Maintainers

- Adam Jones (Anthropic)
- Tadas Antanavicius (PulseMCP)
- Toby Padilla (GitHub)
- Radoslav Dimitrov (Stacklok)

## Resources

- **Registry**: https://registry.modelcontextprotocol.io
- **GitHub**: https://github.com/modelcontextprotocol/registry
- **MCP Specification**: https://modelcontextprotocol.io
- **API Documentation**: https://registry.modelcontextprotocol.io/docs
