---
name: agent-identity
description: Authenticate AI agents with auth servers using the Agent Identity (AID) protocol. Supports Ed25519 identity documents, proof of possession, OAuth 2.0 token exchange, and scoped JWT tokens. Self-contained — works independently without other protocols.
license: MIT
compatibility: Requires curl, jq, openssl (3.x for Ed25519), and base64 CLI tools. macOS and Linux supported.
metadata:
  version: "0.2.0"
  homepage: "https://agentids.org"
  repository: "https://github.com/agentmessaging/agent-identity"
---

# Agent Identity (AID) Protocol

Authenticate AI agents with auth servers using cryptographic identity documents and proof of possession. AID is self-contained — no other protocols required.

## When to use this skill

Use this skill when the user or task requires:
- Initializing an agent's Ed25519 identity
- Registering an agent's identity with an auth server
- Obtaining JWT tokens for API access via token exchange
- Checking an agent's AID registration status
- Setting up agent-to-server authentication
- Configuring scoped permissions for agent API access

## Quick Start

```bash
# 1. Initialize agent identity (one-time)
aid-init.sh --auto

# 2. Register with an auth server (one-time, requires admin token)
aid-register.sh --auth https://auth.23blocks.com/acme \
  --token <ADMIN_JWT> --role-id 2

# 3. Get a JWT token
TOKEN=$(aid-token.sh --auth https://auth.23blocks.com/acme --quiet)

# 4. Use it for API calls
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/resource
```

## Installation

### For Claude Code (skill)

```bash
npx skills add agentmessaging/agent-identity
```

### Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/agentmessaging/agent-identity/main/install.sh | bash
```

### Manual

```bash
git clone https://github.com/agentmessaging/agent-identity.git ~/agent-identity
export PATH="$HOME/agent-identity/scripts:$PATH"
```

## Commands Reference

### aid-init.sh — Initialize Agent Identity

Create an Ed25519 keypair and identity for this agent.

```bash
aid-init.sh --auto              # Auto-detect name from environment
aid-init.sh --name my-agent     # Specify agent name
aid-init.sh --name my-agent --force  # Overwrite existing
```

**Parameters:**
- `--auto` — Auto-detect agent name from environment
- `--name, -n` — Specify agent name
- `--force, -f` — Overwrite existing identity

### aid-register.sh — Register with Auth Server

One-time registration linking the agent's Ed25519 identity to a tenant with a specific role.

```bash
aid-register.sh --auth https://auth.23blocks.com/acme \
  --token <ADMIN_JWT> --role-id 2
```

**Parameters:**
- `--auth, -a` — Auth server URL (required)
- `--token, -t` — Admin JWT for authorization (required)
- `--role-id, -r` — Role ID to assign (required)
- `--api-key, -k` — API key (X-Api-Key header)
- `--name, -n` — Display name (default: agent name)
- `--description, -d` — Agent description
- `--lifetime, -l` — Token lifetime in seconds (default: 3600)

**What it does:**
1. Reads the agent's Ed25519 public key and identity
2. POSTs the registration to the server's agent registration endpoint
3. Stores the registration locally for future token exchanges

### aid-token.sh — Exchange Identity for JWT Token

Performs the OAuth 2.0 token exchange using `grant_type=urn:aid:agent-identity`.

```bash
# Get a token (uses cache if valid)
aid-token.sh --auth https://auth.23blocks.com/acme

# Get just the token string (for scripting)
TOKEN=$(aid-token.sh --auth https://auth.23blocks.com/acme --quiet)

# Get a token with specific scopes
aid-token.sh --auth https://auth.23blocks.com/acme --scope "files:read files:write"
```

**Parameters:**
- `--auth, -a` — Auth server URL (required)
- `--scope, -s` — Space-separated scopes (optional)
- `--json, -j` — Output as JSON
- `--quiet, -q` — Output only the token string
- `--no-cache` — Skip token cache

**What it does:**
1. Builds a fresh Agent Identity Document with current timestamp
2. Creates a Proof of Possession (`aid-token-exchange\n{timestamp}\n{auth_issuer}`)
3. Signs the proof with the agent's Ed25519 private key
4. POSTs to the OAuth token endpoint with `grant_type=urn:aid:agent-identity`
5. Returns the JWT access token (cached for reuse)

### aid-status.sh — Check Identity & Registration Status

```bash
aid-status.sh          # Human-readable output
aid-status.sh --json   # JSON output
```

## How AID Authentication Works

### Step 1: Agent Identity Document

A signed JSON document proving the agent's identity:

```json
{
  "aid_version": "1.0",
  "address": "support-agent@default.local",
  "alias": "support-agent",
  "public_key": "-----BEGIN PUBLIC KEY-----\n...",
  "key_algorithm": "Ed25519",
  "fingerprint": "SHA256:abc123...",
  "issued_at": "2026-03-23T00:00:00Z",
  "expires_at": "2026-09-23T00:00:00Z",
  "signature": "base64-ed25519-signature"
}
```

### Step 2: Proof of Possession

The agent signs a challenge proving it holds the private key:

```
aid-token-exchange\n{timestamp}\n{auth_server_url}
```

### Step 3: Token Exchange

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn%3Aaid%3Aagent-identity
&agent_identity={base64url-identity-document}
&proof={base64url-signed-proof}
```

### Step 4: Use the JWT

The server returns a standard OAuth 2.0 response with an RS256 JWT access token. Use it with any API that validates JWTs via the auth server's JWKS endpoint.

## Natural Language Examples

Agents should map these user intents to the appropriate commands:

- "Initialize my identity" -> `aid-init.sh --auto`
- "Register with the API" -> `aid-register.sh --auth <url> --token <jwt> --role-id <id>`
- "Get me an API token" -> `aid-token.sh --auth <url>`
- "Check my registrations" -> `aid-status.sh`
- "Authenticate with the auth server" -> `aid-token.sh --auth <url>`

## Security

- **Self-contained** — no external protocol dependencies
- **Ed25519 signatures** — identity documents are cryptographically signed
- **Proof of possession** — agents prove key ownership at every token exchange
- **Human-controlled access** — admin creates roles and registers agents
- **Short-lived tokens** — JWTs expire quickly, limiting blast radius
- **No shared secrets** — private keys never leave the agent
- **Scoped access** — tokens carry only the permissions the agent's role allows

## Interoperability

AID shares the `~/.agent-messaging/agents/` directory with [AMP](https://agentmessaging.org) if both are installed. One identity serves both protocols. Neither requires the other.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Agent identity not initialized" | Run `aid-init.sh --auto` |
| "Not registered" | Run `aid-register.sh` with auth server details |
| "Proof expired" | Clock skew >5 minutes; sync system clock |
| "Invalid signature" | Agent identity may be corrupted; re-init and re-register |
| "Fingerprint mismatch" | Agent key changed since registration; re-register |
| "Scope not allowed" | Request only scopes granted during registration |

## Protocol Reference

Full specification: https://agentids.org
GitHub: https://github.com/agentmessaging/agent-identity
