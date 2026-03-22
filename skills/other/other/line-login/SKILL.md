---
name: line-login
description: Comprehensive reference for LINE Login (OAuth 2.1) — authorization code flow, PKCE, token management, ID token JWT verification, user profiles, bot linking, and login button design. This skill should be used when the user asks to "implement LINE Login", "add Log in with LINE", "set up OAuth authorization flow", "verify an ID token", "refresh an access token", "link a bot to login", "design a login button", or mentions LINE Login, OAuth 2.1, PKCE, authorization code flow, ID token JWT verification, token refresh/revocation, user profile retrieval, bot linking, SSO login, LIFF authentication, or LINE MINI App authentication. Always use this skill whenever the user mentions LINE authentication, social login with LINE, or OAuth flows involving LINE, even if they don't explicitly say "LINE Login".
---

# LINE Login

**Do not answer LINE Login questions from memory — LINE updates APIs frequently and training data is unreliable. Always consult the references below.**

LINE Login v2.1 is built on OAuth 2.0 and OpenID Connect. It provides user authentication, profile access, and bot linking for web apps, native apps (iOS/Android), Unity, and Flutter.

## Workflow

### Build
1. Read [references/api-common.md](references/api-common.md) (forward compatibility, rate limits, client_secret rules)
2. Read [references/security.md](references/security.md) (security checklist, development guidelines)
3. Load the relevant reference for the feature being implemented
4. Write code following specs and constraints from references

### Review / Debug
1. Read [references/api-common.md](references/api-common.md) (status codes, error responses, forward compatibility)
2. Read [references/security.md](references/security.md) (security checklist, common pitfalls)
3. Load relevant references for the code being reviewed
4. Cross-check code against specs (parameter requirements, token expiry, signing algorithms, required validations)
5. Report violations with reference to specific constraints

## Environment Variables

```
LINE_LOGIN_CHANNEL_ID=LINE Login Channel ID
LINE_LOGIN_CHANNEL_SECRET=Channel secret (ID token verification, token exchange)
LINE_LOGIN_REDIRECT_URI=Registered callback URL
```

## Common Specifications

**Read [references/api-common.md](references/api-common.md) before writing any LINE Login code.** Contains rules that affect all API interactions: forward compatibility (don't use strict schemas — LINE adds fields without notice), rate limits, `client_secret` conditional requirement by App types, error responses, and logging recommendations.

## OAuth 2.1 Authorization Code Flow

```
User → authorize endpoint → LINE Login screen → callback with code → token exchange → access_token + id_token
```

### Minimal Flow (pseudocode)

```
# 1. Redirect user to authorize
state = random_token()
session.save(state)
redirect to:
  https://access.line.me/oauth2/v2.1/authorize?
    response_type=code
    &client_id={channel_id}
    &redirect_uri={callback_url}
    &state={state}
    &scope=profile%20openid%20email

# 2. Callback — exchange code for token
if params.state != session.state:
    return 403  # CSRF check failed

POST https://api.line.me/oauth2/v2.1/token
  grant_type=authorization_code
  &code={params.code}
  &redirect_uri={callback_url}
  &client_id={channel_id}
  &client_secret={channel_secret}

# 3. Response
{ access_token, token_type, refresh_token, expires_in, id_token, scope }
```

| Step | Endpoint |
|------|----------|
| Authorize | `GET https://access.line.me/oauth2/v2.1/authorize` |
| Token Exchange | `POST https://api.line.me/oauth2/v2.1/token` |

- Scopes: `profile`, `openid`, `email` (space-separated)
- Authorization code: valid **10 minutes**, one-time use
- PKCE: recommended for public clients (SPA/Mobile), only `S256` supported

Full authorize parameters, PKCE, scope combinations, error codes → **[references/oauth-flow.md](references/oauth-flow.md)**

## Token Management

| Operation | Endpoint |
|-----------|----------|
| Verify Access Token | `GET https://api.line.me/oauth2/v2.1/verify?access_token={token}` |
| Refresh Token | `POST https://api.line.me/oauth2/v2.1/token` (grant_type=refresh_token) |
| Revoke Token | `POST https://api.line.me/oauth2/v2.1/revoke` |
| Verify ID Token | `POST https://api.line.me/oauth2/v2.1/verify` (id_token + client_id) |

| Token | Validity |
|-------|----------|
| Access Token | 30 days |
| Refresh Token | 90 days |

ID Token signing: **HS256** (web login) / **ES256** (native app, SDK, LIFF)

Full token APIs, ID Token claims, signing verification → **[references/token-management.md](references/token-management.md)**

## User & Bot Linking

| Operation | Endpoint |
|-----------|----------|
| Get User Profile | `GET https://api.line.me/v2/profile` |
| Check Friendship | `GET https://api.line.me/friendship/v1/status` |
| Deauthorize | `POST https://api.line.me/user/v1/deauthorize` |

- `bot_prompt` parameter: `normal` (on consent screen) / `aggressive` (separate screen after consent)
- `friendship_status_changed`: included in token response when bot linking is configured

Full user profile, bot linking logic → **[references/user-profile.md](references/user-profile.md)**

## Security

- **state**: must be cryptographically random, always validate on callback
- **PKCE**: use for public clients (SPA, mobile apps)
- **Channel Secret**: server-side only, never expose to client
- **redirect_uri**: must be HTTPS
- **ID Token**: always verify signature before trusting claims

Full security checklist, development guidelines, auto login failure handling → **[references/security.md](references/security.md)**

## Reference Index

| File | Topic |
|------|-------|
| [references/api-common.md](references/api-common.md) | **Read first.** Rate limits, status codes, forward compatibility, client_secret rules, logging |
| [references/oauth-flow.md](references/oauth-flow.md) | Authorization flow, PKCE, scopes, auth methods, error codes |
| [references/token-management.md](references/token-management.md) | Token exchange/refresh/revoke/verify, ID Token claims and signing |
| [references/security.md](references/security.md) | Security checklist, development guidelines, auto login failure, login button design |
| [references/user-profile.md](references/user-profile.md) | User profile API, Link a Bot, friendship status |
| [references/experts.md](references/experts.md) | LINE Login domain experts for architecture guidance |

## SDK

Native SDKs: [iOS (Swift)](https://developers.line.biz/en/docs/line-login-sdks/ios-sdk/) | [Android](https://developers.line.biz/en/docs/line-login-sdks/android-sdk/) | [Unity](https://developers.line.biz/en/docs/line-login-sdks/unity-sdk/) | [Flutter](https://pub.dev/packages/flutter_line_sdk)

For web apps, use the OAuth 2.1 flow directly (no SDK required).
