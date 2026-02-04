---
name: Fanvue
description: Manage content, chats, subscribers, and earnings on the Fanvue creator platform via OAuth 2.0 API.
---

# Fanvue API Skill

Integrate with the Fanvue creator platform to manage chats, posts, subscribers, earnings insights, and media content.

## Prerequisites

### 1. Create an OAuth Application

1. Go to the [Fanvue Developer Portal](https://fanvue.com/developers/apps)
2. Create a new OAuth application
3. Note your **Client ID** and **Client Secret**
4. Configure your **Redirect URI** (e.g., `https://your-app.com/callback`)

### 2. Environment Variables

Set these environment variables:

```bash
FANVUE_CLIENT_ID=your_client_id
FANVUE_CLIENT_SECRET=your_client_secret
FANVUE_REDIRECT_URI=https://your-app.com/callback
```

---

## Authentication

Fanvue uses **OAuth 2.0 with PKCE** (Proof Key for Code Exchange). All API requests require:

- **Authorization Header**: `Bearer <access_token>`
- **API Version Header**: `X-Fanvue-API-Version: 2025-06-26`

### OAuth Scopes

Request these scopes based on your needs:

| Scope | Access |
|-------|--------|
| `openid` | OpenID Connect authentication |
| `offline_access` | Refresh token support |
| `offline` | Offline access |
| `read:self` | Read authenticated user profile |
| `read:chat` | Read chat conversations |
| `write:chat` | Send messages, update chats |
| `read:post` | Read posts |
| `write:post` | Create posts |
| `read:creator` | Read subscriber/follower data |
| `read:media` | Read media vault |
| `write:tracking_links` | Manage campaign links |
| `read:insights` | Read earnings/analytics (creator accounts) |
| `read:subscribers` | Read subscriber lists (creator accounts) |

> **Note**: Some endpoints (subscribers, insights, earnings) require a **creator account** and may need additional scopes not listed in the public documentation.

### Quick Auth Flow

```typescript
import { randomBytes, createHash } from 'crypto';

// 1. Generate PKCE parameters
const codeVerifier = randomBytes(32).toString('base64url');
const codeChallenge = createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

// 2. Build authorization URL
const authUrl = new URL('https://auth.fanvue.com/oauth2/auth');
authUrl.searchParams.set('client_id', process.env.FANVUE_CLIENT_ID);
authUrl.searchParams.set('redirect_uri', process.env.FANVUE_REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'openid offline_access read:self read:chat write:chat read:post');
authUrl.searchParams.set('state', randomBytes(32).toString('hex'));
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

// Redirect user to: authUrl.toString()
```

```typescript
// 3. Exchange authorization code for tokens
const tokenResponse = await fetch('https://auth.fanvue.com/oauth2/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: process.env.FANVUE_CLIENT_ID,
    client_secret: process.env.FANVUE_CLIENT_SECRET,
    code: authorizationCode,
    redirect_uri: process.env.FANVUE_REDIRECT_URI,
    code_verifier: codeVerifier,
  }),
});

const tokens = await tokenResponse.json();
// tokens.access_token, tokens.refresh_token
```

---

## API Base URL

All API requests go to: `https://api.fanvue.com`

### Standard Request Headers

```typescript
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'X-Fanvue-API-Version': '2025-06-26',
  'Content-Type': 'application/json',
};
```

---

## Agent Automation

These workflows are designed for AI agents automating Fanvue creator accounts.

### Accessing Images (with Signed URLs)

The basic `/media` endpoint only returns metadata. To get actual viewable URLs, use the `variants` query parameter:

```typescript
// Step 1: List all media
const list = await fetch('https://api.fanvue.com/media', { headers });
const { data } = await list.json();

// Step 2: Get signed URLs for a specific media item
const media = await fetch(
  `https://api.fanvue.com/media/${uuid}?variants=main,thumbnail,blurred`, 
  { headers }
);
const { variants } = await media.json();

// variants = [
//   { variantType: 'main', url: 'https://media.fanvue.com/private/...' },
//   { variantType: 'thumbnail', url: '...' },
//   { variantType: 'blurred', url: '...' }
// ]
```

**Variant Types:**
- `main` - Full resolution original
- `thumbnail` - Optimized preview (smaller)
- `blurred` - Censored version for teasers

### Creating a Post with Media

```typescript
// Step 1: Have existing media UUIDs from vault
const mediaIds = ['media-uuid-1', 'media-uuid-2'];

// Step 2: Create post
const response = await fetch('https://api.fanvue.com/posts', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    text: 'Check out my new content! 🔥',
    mediaIds,
    audience: 'subscribers',  // or 'followers-and-subscribers'
    // Optional:
    price: null,              // Set for pay-per-view
    publishAt: null,          // Set for scheduled posts
  }),
});
```

**Audience Options:**
| Value | Who Can See |
|-------|-------------|
| `subscribers` | Paid subscribers only |
| `followers-and-subscribers` | Both free followers and subscribers |

### Sending Messages with Media

```typescript
// Get subscriber list for decision making
const subs = await fetch('https://api.fanvue.com/creators/list-subscribers', { headers });
const { data: subscribers } = await subs.json();

// Get top spenders for VIP targeting
const vips = await fetch('https://api.fanvue.com/insights/get-top-spenders', { headers });
const { data: topSpenders } = await vips.json();

// Send personalized message with media
await fetch('https://api.fanvue.com/chat-messages', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuid: subscribers[0].userUuid,
    content: 'Thanks for being a subscriber! Here\'s something special for you 💕',
    mediaIds: ['vault-media-uuid'],  // Attach media from vault
  }),
});

// Or send to multiple subscribers at once
await fetch('https://api.fanvue.com/chat-messages/mass', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuids: subscribers.map(s => s.userUuid),
    content: 'New exclusive content just dropped! 🎉',
    mediaIds: ['vault-media-uuid'],
  }),
});
```

### Agent Decision Context

For effective automation, gather this context:

```typescript
interface AutomationContext {
  // Current media in vault
  media: {
    uuid: string;
    name: string;
    type: 'image' | 'video';
    description: string;  // AI-generated caption
    signedUrl: string;    // From variants query
  }[];
  
  // Audience data
  subscribers: {
    uuid: string;
    name: string;
    subscribedAt: string;
    tier: string;
  }[];
  
  // Engagement signals
  topSpenders: {
    uuid: string;
    totalSpent: number;
  }[];
  
  // Recent earnings for trend analysis
  earnings: {
    period: string;
    total: number;
    breakdown: { type: string; amount: number }[];
  };
}
```

---

## Core Operations


### Get Current User

```typescript
const response = await fetch('https://api.fanvue.com/users/me', { headers });
const user = await response.json();
```

### List Chats

```typescript
const response = await fetch('https://api.fanvue.com/chats', { headers });
const { data, pagination } = await response.json();
```

### Send a Message

```typescript
const response = await fetch('https://api.fanvue.com/chat-messages', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuid: 'user-uuid-here',
    content: 'Hello! Thanks for subscribing!',
  }),
});
```

### Create a Post

```typescript
const response = await fetch('https://api.fanvue.com/posts', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    content: 'New content available!',
    // Add media IDs, pricing, etc.
  }),
});
```

### Get Earnings

```typescript
const response = await fetch('https://api.fanvue.com/insights/get-earnings', { headers });
const earnings = await response.json();
```

### List Subscribers

```typescript
const response = await fetch('https://api.fanvue.com/creators/list-subscribers', { headers });
const { data } = await response.json();
```

---

## API Reference

See [api-reference.md](./api-reference.md) for the complete endpoint documentation.

---

## Token Refresh

Access tokens expire. Use the refresh token to get new ones:

```typescript
const response = await fetch('https://auth.fanvue.com/oauth2/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    client_id: process.env.FANVUE_CLIENT_ID,
    client_secret: process.env.FANVUE_CLIENT_SECRET,
    refresh_token: currentRefreshToken,
  }),
});

const newTokens = await response.json();
```

---

## Error Handling

Common HTTP status codes:

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `400` | Bad request - check your parameters |
| `401` | Unauthorized - token expired or invalid |
| `403` | Forbidden - missing required scope |
| `404` | Resource not found |
| `429` | Rate limited - slow down requests |

---

## Resources

- [Fanvue API Documentation](https://api.fanvue.com/docs)
- [OAuth 2.0 Guide](https://api.fanvue.com/docs/authentication/quick-start)
- [Developer Portal](https://fanvue.com/developers/apps)
- [Fanvue App Starter Kit](https://github.com/fanvue/fanvue-app-starter)
