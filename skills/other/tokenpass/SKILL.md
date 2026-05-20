---
name: tokenpass
description: This skill should be used when the user asks about "TokenPass", "install TokenPass", "run TokenPass server", "TokenPass desktop app", "TokenPass API", "personal identity server", "be your own OAuth provider", or needs help setting up, configuring, or integrating TokenPass Server or Desktop applications. Provides installation, configuration, and API integration guidance.
version: 1.0.0
---

# TokenPass

TokenPass is a personal identity server that enables Bitcoin-backed authentication. Run your own OAuth provider with cryptographic signing, encryption, and BAP (Bitcoin Attestation Protocol) identity management.

## Overview

TokenPass consists of two components:

| Component | Description | Port |
|-----------|-------------|------|
| **TokenPass Server** | REST API for wallet management, signing, encryption | 21000 |
| **TokenPass Desktop** | Electron app with system tray, auto-start | - |

## Installation

### TokenPass Server

```bash
# Clone and install
git clone https://github.com/b-open-io/tokenpass-server
cd tokenpass-server
bun install

# Start the server
bun dev
```

Server runs at `http://localhost:21000` with API prefix `/api/`.

### TokenPass Desktop

Download from [GitHub Releases](https://github.com/b-open-io/tokenpass-desktop/releases):

| Platform | File |
|----------|------|
| macOS (Apple Silicon) | `TokenPass-X.X.X-arm64.dmg` |
| macOS (Intel) | `TokenPass-X.X.X-x64.dmg` |
| Windows | `TokenPass-X.X.X-setup.exe` |
| Linux | `TokenPass-X.X.X.AppImage` |

The desktop app wraps the server with a system tray icon and auto-start capability.

## Authentication Flow

TokenPass uses a two-step authentication model:

1. **Wallet Setup** (one-time): Create wallet with `POST /api/register`
2. **Unlock Wallet**: Call `POST /api/login` with password
3. **Get Access Token**: Call `POST /api/auth` with host and scopes
4. **Make API Calls**: Use token in `Authorization` header

```typescript
// 1. Register (first time only)
await fetch('http://localhost:21000/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    password: 'secure-password',
    displayName: 'Alice'
  })
});

// 2. Login (unlocks wallet)
await fetch('http://localhost:21000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ password: 'secure-password' })
});

// 3. Get access token for a host
const { accessToken } = await fetch('http://localhost:21000/api/auth', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    password: 'secure-password',
    host: 'example.com',
    expire: '1h',
    scopes: 'sign,encrypt'
  })
}).then(r => r.json());

// 4. Sign a message
const signature = await fetch('http://localhost:21000/api/sign', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': accessToken  // No "Bearer" prefix
  },
  body: JSON.stringify({ message: 'Hello World' })
}).then(r => r.json());
```

## API Endpoints

### Wallet Management

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/register` | POST | - | Create new wallet |
| `/api/login` | POST | - | Unlock wallet |
| `/api/logout` | POST | - | Lock wallet |
| `/api/status` | GET | - | Check wallet status |
| `/api/export` | POST | Password | Export seed/mnemonic |

### Access Tokens

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth` | POST | Password | Generate access token |

**Token Expiry Options:** `once` (10s), `1h`, `1d`, `1w`, `1m`, `forever`

**Scopes:** `sign`, `encrypt`, `decrypt`, `read_profile`, `write_profile`, `read_state`, `write_state`, `fund`, `transfer`

### Cryptographic Operations

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/sign` | POST | Token | Sign message (BSM format) |
| `/api/encrypt` | POST | Token | Encrypt with ECIES |

### Identity Management

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/profile` | GET | - | Get BAP profile |
| `/api/profile` | POST | - | Update BAP profile |

## Configuration

### Environment Variables

```bash
# CORS whitelist (comma-separated)
TOKENPASS_ORIGIN_WHITELIST=https://app1.com,https://app2.com
```

### Data Storage

All data stored in `~/.tokenpass/`:

| File | Description |
|------|-------------|
| `seed.db` | Encrypted master seed (AES-256-CBC) |
| `keys.db` | Derived Bitcoin keys per host |
| `state.db` | Access tokens and per-host state |

## React Integration

The `@sigma-auth/better-auth-plugin` provides a full React client with automatic TokenPass detection:

```typescript
import { createAuthClient } from "better-auth/client";
import { sigmaClient } from "@sigma-auth/better-auth-plugin/client";

export const authClient = createAuthClient({
  baseURL: "https://auth.sigmaidentity.com",
  plugins: [
    sigmaClient({
      preferLocal: true,  // Auto-detect local TokenPass
      localServerUrl: "http://localhost:21000",
      onServerDetected: (url, isLocal) => {
        console.log(`Using ${isLocal ? 'local' : 'cloud'} signer: ${url}`);
      }
    })
  ],
});

// Sign requests (uses TokenPass if available)
const authToken = await authClient.sigma.sign("/api/endpoint", { data: "value" });

// Encrypt/decrypt with Type42 key derivation
const encrypted = await authClient.sigma.encrypt("secret", friendBapId);
const decrypted = await authClient.sigma.decrypt(encrypted, friendBapId);
```

The client automatically:
- Probes for local TokenPass server on `localhost:21000`
- Falls back to cloud iframe signer if unavailable
- Handles OAuth flow with PKCE
- Manages identity state and token storage

## Related Skills

- **setup-nextjs**: Full Next.js integration guide with OAuth flow
- **bitcoin-auth-diagnostics**: Troubleshoot auth token issues
- **bsv-skills:message-signing**: BSM signature verification
- **bsv-skills:key-derivation**: Type42/BIP32 key derivation

## Additional Resources

### Reference Files

For detailed API documentation and examples:
- **`references/api-reference.md`** - Complete REST API documentation
- **`references/integration-examples.md`** - Code examples for common integrations

### Documentation

- Server README: https://github.com/b-open-io/tokenpass-server
- Desktop Releases: https://github.com/b-open-io/tokenpass-desktop/releases
- Web Documentation: https://tokenpass.app/docs
