---
name: device-authorization
description: This skill should be used when the user asks to "implement device auth", "add device authorization", "authenticate desktop app", "authenticate CLI tool", "device code flow", "RFC 8628", "poll for token", "get user info after device auth", or mentions authenticating apps that can't handle browser redirects. Provides step-by-step guidance for device authorization with Sigma Identity.
version: 0.1.0
---

# Device Authorization Flow (RFC 8628)

Authenticate desktop apps, CLI tools, and devices without browser redirect capability using Sigma Identity.

## When to Use

- **Desktop apps** (Electron, Tauri) that need cross-origin auth
- **CLI tools** that can't open browser windows reliably
- **TV/IoT apps** with limited input capability
- Any app where OAuth redirect flow is impractical

## Flow Overview

```
1. App requests device code from Sigma
2. User visits verification URL in browser
3. User enters code and approves
4. App polls for token (receives access_token when approved)
5. App fetches user info with Bearer token
```

## Endpoints

All endpoints are on `https://auth.sigmaidentity.com`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/device/code` | POST | Get device_code and user_code |
| `/api/auth/device/token` | POST | Poll for access_token |
| `/api/auth/oauth2/userinfo` | GET | Fetch user info with Bearer token |

## Implementation

### Step 1: Request Device Code

```typescript
const authUrl = "https://auth.sigmaidentity.com";

const response = await fetch(`${authUrl}/api/auth/device/code`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    client_id: "your-app-name",
    scope: "openid profile",
  }),
});

const deviceAuth = await response.json();
// {
//   device_code: "abc123...",
//   user_code: "ABCD-1234",
//   verification_uri: "https://auth.sigmaidentity.com/device",
//   verification_uri_complete: "https://auth.sigmaidentity.com/device?code=ABCD-1234",
//   expires_in: 900,
//   interval: 5
// }
```

### Step 2: Show User Code & Open Browser

Display the user code prominently and open the verification URL:

```typescript
// Display to user
console.log(`Enter code: ${deviceAuth.user_code}`);
console.log(`Visit: ${deviceAuth.verification_uri}`);

// Or open browser directly with pre-filled code
openBrowser(deviceAuth.verification_uri_complete);
```

### Step 3: Poll for Token

Poll at the specified interval until user approves:

```typescript
async function pollForToken(deviceCode: string, interval: number): Promise<string> {
  const pollInterval = interval * 1000;

  while (true) {
    await new Promise(r => setTimeout(r, pollInterval));

    const response = await fetch(`${authUrl}/api/auth/device/token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        grant_type: "urn:ietf:params:oauth:grant-type:device_code",
        device_code: deviceCode,
        client_id: "your-app-name",
      }),
    });

    const data = await response.json();

    if (data.access_token) {
      return data.access_token;
    }

    // Handle error cases per RFC 8628
    switch (data.error) {
      case "authorization_pending":
        continue; // Keep polling
      case "slow_down":
        pollInterval += 5000; // Increase interval
        continue;
      case "expired_token":
        throw new Error("Code expired - please restart");
      case "access_denied":
        throw new Error("User denied authorization");
      default:
        throw new Error(data.error || "Unknown error");
    }
  }
}
```

### Step 4: Fetch User Info

Use the access token to get user details:

```typescript
const userInfoRes = await fetch(`${authUrl}/api/auth/oauth2/userinfo`, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

const userInfo = await userInfoRes.json();
// {
//   sub: "user-id-123",
//   name: "satoshi",
//   email: "user@example.com",
//   picture: "https://...",
//   bap_id: "bap-identity-key",  // Sigma-specific
//   pubkey: "03abc..."           // Sigma-specific
// }
```

## User Info Response Fields

Standard OIDC claims:
- `sub` - User ID (use as userId)
- `name` - Display name
- `email` - Email address
- `picture` - Avatar URL

Sigma-specific claims:
- `bap_id` - BAP identity key (use as bapId)
- `pubkey` - User's public key
- `bap` - Full BAP profile (JSON string)

## CORS Configuration

For cross-origin requests from localhost or desktop apps, these endpoints allow any origin:
- `/api/auth/device/code`
- `/api/auth/device/token`
- `/api/auth/oauth2/userinfo`

Security is enforced via the access token, not origin validation.

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `authorization_pending` | User hasn't approved yet | Continue polling |
| `slow_down` | Polling too fast | Increase interval by 5s |
| `expired_token` | Code expired (15 min default) | Restart flow |
| `access_denied` | User denied request | Show error to user |

## Complete Example

```typescript
async function deviceAuth() {
  const authUrl = "https://auth.sigmaidentity.com";

  // 1. Get device code
  const codeRes = await fetch(`${authUrl}/api/auth/device/code`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ client_id: "my-app", scope: "openid profile" }),
  });
  const deviceAuth = await codeRes.json();

  // 2. Show code to user
  console.log(`Code: ${deviceAuth.user_code}`);
  openBrowser(deviceAuth.verification_uri_complete);

  // 3. Poll for token
  const accessToken = await pollForToken(
    deviceAuth.device_code,
    deviceAuth.interval
  );

  // 4. Fetch user info
  const userRes = await fetch(`${authUrl}/api/auth/oauth2/userinfo`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  const user = await userRes.json();

  return {
    userId: user.sub,
    bapId: user.bap_id,
    name: user.name,
    image: user.picture,
  };
}
```

## Security Considerations

- Device codes expire after 15 minutes (configurable)
- Polling is rate-limited (5s default interval)
- Access tokens are short-lived (1 hour default)
- No client_secret required - security comes from user approval
- User must explicitly approve on auth.sigmaidentity.com

## Agent Identity Use Case

The device authorization flow is the primary mechanism for **AI agent authentication**. Agents (Claude Code bots, autonomous services, CLI tools) cannot handle browser redirects but need verifiable BAP identities.

### How It Works for Agents

1. **Agent requests device code** — the agent process calls the device endpoint programmatically
2. **Human owner approves** — the owner authenticates at `/device` with their BAP identity and approves the agent
3. **Agent receives OAuth token** — the token contains BAP claims (`bap_id`, `pubkey`) linking the agent to the owner's identity
4. **Member key delegation** — the agent operates with a derived member key, not the owner's master key
5. **Agent authenticates to services** — standard OAuth token accepted by any app that trusts Sigma

### ClawNet Trust Scoring

ClawNet queries the agent's BAP identity to compute a trust score (0-100) based on:
- **Attestation history** — how long the identity has been active on-chain
- **Skill signatures** — AIP-signed skill attestations from verified authors
- **Cross-attestation** — endorsements from other trusted identities
- **Version continuity** — consistent identity across updates

Higher trust scores enable greater agent autonomy: more skills, higher spending limits, less human-in-the-loop approval required.

## Tauri/Desktop Integration

For Tauri apps, use the shell plugin to open the browser:

```rust
// In Tauri command
use tauri_plugin_shell::ShellExt;

app.shell().open(verification_url, None)?;
```

Or from JavaScript:
```typescript
import { open } from "@tauri-apps/plugin-shell";
await open(deviceAuth.verification_uri_complete);
```

## Reference

- [RFC 8628 - Device Authorization Grant](https://datatracker.ietf.org/doc/html/rfc8628)
- [Better Auth Device Authorization](https://www.better-auth.com/docs/plugins/device-authorization)
