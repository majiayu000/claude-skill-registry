---
name: authkit
description: Add OAuth connections for 200+ platforms (Gmail, Slack, HubSpot, etc.) with Pica's drop-in AuthKit widget
---

# Pica AuthKit Integration Guide

Complete guide for integrating Pica AuthKit to enable users to connect third-party tools (Gmail, Slack, HubSpot, etc.) in your application.

## What is AuthKit?

AuthKit is a drop-in OAuth component that:
- Provides pre-built UI for 200+ integration OAuth flows
- Handles token management and refresh automatically
- Works with any frontend framework (React, Vue, vanilla JS)
- Requires a backend token endpoint

## Prerequisites

- Pica API key from https://app.picaos.com/settings/api-keys
- Backend capable of making authenticated API calls
- Frontend capable of running JavaScript

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Your Backend   │────▶│  Pica API   │
│  (AuthKit)  │     │ (Token Endpoint)│     │             │
└─────────────┘     └─────────────────┘     └─────────────┘
       │                                           │
       └───────────── OAuth Flow ──────────────────┘
```

1. Frontend calls your token endpoint
2. Your backend generates a Pica session token
3. AuthKit uses token to manage OAuth flow
4. On success, you receive connection details to store

---

## Step 1: Install Packages

**Frontend:**
```bash
npm install @picahq/authkit
```

**Backend:**
```bash
npm install @picahq/authkit-token
```

---

## Step 2: Backend Token Endpoint

Create an endpoint that generates AuthKit session tokens.

### Requirements
- Must accept POST requests
- Must return token object directly (not wrapped)
- Must include CORS headers (AuthKit iframe calls this endpoint)
- Should identify the user via header or body parameter

### Token Generation

```typescript
import { AuthKitToken } from "@picahq/authkit-token";

const authKitToken = new AuthKitToken(PICA_SECRET_KEY);

const token = await authKitToken.create({
  identity: userId,      // Your user's unique identifier
  identityType: "user",  // "user" | "team" | "organization" | "project"
});

// Return token directly
return token;
```

### Identity Types

| Type | Use Case |
|------|----------|
| `user` | Personal connections per user |
| `team` | Shared connections within a team |
| `organization` | Company-wide shared connections |
| `project` | Project-scoped isolated connections |

### Required CORS Headers

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, x-user-id
```

**Important:** Include any custom headers you use (like `x-user-id`) in the allowed headers.

### Example Response

The token endpoint should return the token object directly:

```json
{
  "token": "akt_xxxxx...",
  "expiresAt": "2024-01-01T00:00:00Z"
}
```

---

## Step 3: Frontend Integration

### Using the React Hook

```typescript
import { useAuthKit } from "@picahq/authkit";

function ConnectButton() {
  const { open, isLoading } = useAuthKit({
    token: {
      url: "https://your-domain.com/api/authkit/token", // MUST be full URL
      headers: {
        "x-user-id": currentUserId,
      },
    },
    selectedConnection: "Gmail",  // Optional: skip list, go directly to this integration
    onSuccess: (connection) => {
      // connection.key - unique identifier for this connection
      // connection.platform - e.g., "gmail"
      // connection.environment - "live" or "test"
      // connection.state - "operational", "degraded", "failed", "unknown"

      saveConnectionToDatabase(connection);
    },
    onError: (error) => {
      console.error("Connection failed:", error);
    },
    onClose: () => {
      console.log("Modal closed");
    },
  });

  return (
    <button onClick={() => open()} disabled={isLoading}>
      Connect Integration
    </button>
  );
}
```

### Critical: Token URL Must Be Full URL

```typescript
// CORRECT - Full URL
url: "https://your-domain.com/api/authkit/token"
url: `${window.location.origin}/api/authkit/token`

// INCORRECT - Will fail
url: "/api/authkit/token"
```

### selectedConnection Parameter

Pass the integration's **display name** to skip the integration list:

```typescript
// Opens directly to Gmail auth flow
selectedConnection: "Gmail"

// Opens directly to Slack auth flow
selectedConnection: "Slack"

// Opens to integration list (user picks)
selectedConnection: undefined
```

**Note:** Use the display name (e.g., "Gmail", "Google Calendar", "HubSpot"), not the platform ID.

---

## Step 4: Store Connections

When `onSuccess` fires, save the connection to your database.

### Connection Object Structure

```typescript
interface Connection {
  key: string;          // "live::gmail::default::abc123" - use this for API calls
  platform: string;     // "gmail"
  environment: string;  // "live" or "test"
  state: string;        // "operational", "degraded", "failed", "unknown"
}
```

### Recommended Database Schema

```sql
CREATE TABLE user_connections (
    id UUID PRIMARY KEY,
    user_id TEXT NOT NULL,           -- Your user identifier
    platform TEXT NOT NULL,          -- "gmail", "slack", etc.
    connection_key TEXT UNIQUE,      -- Pica connection key
    environment TEXT DEFAULT 'live', -- "live" or "test"
    state TEXT DEFAULT 'operational',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Save on Success

```typescript
onSuccess: async (connection) => {
  await fetch("/api/connections", {
    method: "POST",
    body: JSON.stringify({
      user_id: currentUserId,
      platform: connection.platform,
      connection_key: connection.key,
      environment: connection.environment,
      state: connection.state,
    }),
  });

  refreshConnectionsList();
}
```

---

## Step 5: List Available Integrations

Fetch available integrations from Pica API.

### API Request

```
GET https://api.picaos.com/v1/available-connectors?authkit=true&limit=300
Headers:
  x-pica-secret: YOUR_PICA_SECRET_KEY
```

### Response Structure

```json
{
  "rows": [
    {
      "platform": "gmail",
      "name": "Gmail",
      "category": "Communication",
      "image": "https://...",
      "description": "..."
    }
  ],
  "total": 200,
  "pages": 1,
  "page": 1
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `platform` | Platform identifier (use for API calls) |
| `name` | Display name (use for `selectedConnection`) |
| `category` | Category for grouping |
| `image` | Logo URL |

---

## Step 6: Using Connections

Once stored, use the `connection_key` to make API calls via Pica.

### Passthrough API

```
POST https://api.picaos.com/v1/passthrough/{platform}/{action}
Headers:
  x-pica-secret: YOUR_PICA_SECRET_KEY
  x-pica-connection-key: CONNECTION_KEY_FROM_DATABASE
  Content-Type: application/json
```

### Example: Send Gmail

```typescript
const response = await fetch(
  "https://api.picaos.com/v1/passthrough/gmail/messages/send",
  {
    method: "POST",
    headers: {
      "x-pica-secret": PICA_SECRET_KEY,
      "x-pica-connection-key": user.gmailConnectionKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      to: "recipient@example.com",
      subject: "Hello",
      body: "Message content",
    }),
  }
);
```

---

## Local Development

### Chrome Security Flag

Chrome may block the AuthKit iframe from calling localhost. To fix:

1. Go to `chrome://flags`
2. Search for "Block insecure private network requests"
3. Set to **Disabled**
4. Restart Chrome

### Alternative: Use ngrok

Expose your local server via ngrok and use that URL for the token endpoint.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 405 Method Not Allowed | Missing OPTIONS handler | Add OPTIONS endpoint with CORS headers |
| CORS error | Missing or wrong CORS headers | Include all custom headers in Access-Control-Allow-Headers |
| Token fetch fails | Invalid PICA_SECRET_KEY | Verify key at app.picaos.com/settings/api-keys |
| Opens list instead of integration | Wrong selectedConnection value | Use display name ("Gmail") not platform ID ("gmail") |
| Connection not saving | onSuccess not storing data | Save connection in onSuccess callback |
| Foreign key error | user_id references non-existent user | Remove foreign key constraint or ensure user exists |

---

## API Reference

### Token Generation
```typescript
import { AuthKitToken } from "@picahq/authkit-token";
const token = new AuthKitToken(secretKey);
await token.create({ identity, identityType });
```

### Frontend Hook
```typescript
import { useAuthKit } from "@picahq/authkit";
const { open, isLoading } = useAuthKit({ token, onSuccess, onError, onClose, selectedConnection });
```

### Pica API Endpoints
- **Available Connectors:** `GET /v1/available-connectors?authkit=true`
- **List Connections:** `GET /v1/vault/connections?identity={id}&identityType=user`
- **Passthrough:** `POST /v1/passthrough/{platform}/{action}`

### Documentation
- Pica Docs: https://docs.picaos.com
- AuthKit Setup: https://docs.picaos.com/authkit/setup
- Available Connectors: https://docs.picaos.com/available-connectors
