---
name: oidc-integration
description: Plan and implement OIDC and OAuth 2.0 integration for React or TypeScript frontends and Java or Spring Boot backends. Use whenever the user mentions OIDC, OpenID Connect, OAuth login, SSO, PKCE, authorization code flow, refresh tokens, JWT or JWKS validation, login callback pages, protected routes, Keycloak, Auth0, IdentityServer, Authing, multi-provider auth, or "add login" and "integrate IdP" style requests even if they do not explicitly say OIDC.
---

# OIDC Integration

Use this skill to design or implement authentication flows that rely on an OpenID Connect provider.

## Objective

Help the user integrate OIDC in a way that matches their architecture, avoids unsafe defaults, and produces code that fits the current stack instead of dumping generic samples.

## Working Style

Start by identifying the actual integration shape before writing code.

Check these points first:

- Which side owns auth state: SPA only, backend session, or BFF.
- Which provider is involved: Keycloak, Auth0, IdentityServer, Authing, Azure AD, or another OIDC-compliant IdP.
- Whether there is one provider or multiple providers.
- Whether the client is public or confidential.
- Whether refresh tokens are required.
- Whether the user needs login only, login plus logout, route protection, token validation, or full end-to-end flow.
- Whether the codebase already uses auth libraries that should be extended rather than replaced.

If the user only needs one layer, stay scoped to that layer. Do not generate both frontend and backend integration unless the task actually spans both.

## Security Defaults

Apply these defaults unless the user explicitly needs something different:

- Prefer Authorization Code Flow.
- For browser-based public clients, use PKCE.
- Prefer provider metadata discovery from `/.well-known/openid-configuration` over hardcoding endpoints.
- Prefer server-managed sessions or httpOnly cookies over storing long-lived tokens in `localStorage`.
- If a pure SPA must hold tokens in browser storage, call out the tradeoff and keep token lifetime short.
- Request `offline_access` only when refresh tokens are actually needed.
- Validate `iss`, `aud`, signature, expiry, and key rotation behavior.
- Treat logout as two separate concerns: local app logout and provider logout.

Do not normalize insecure shortcuts as the default recommendation.

## Preferred Implementation Path

Prefer framework-native or well-supported libraries before hand-rolled auth code.

If the user asks for concrete implementation examples, read only the relevant reference file instead of expanding the main skill body:

- `references/react-spa.md` for React or TypeScript SPA login, callback, guards, and API calls.
- `references/spring-resource-server.md` for Spring Boot bearer-token validation and route protection.
- `references/multi-provider.md` for dual-provider or multi-issuer setups.

### Frontend

Prefer these options when they fit the existing stack:

- `oidc-client-ts`
- `react-oidc-context`
- Existing auth wrapper already present in the repo

Generate custom PKCE and token exchange code only when the project constraints require it.

### Spring Boot Backend

Prefer these options before writing custom JWT validation services:

- `spring-boot-starter-oauth2-client` for login flows
- `spring-boot-starter-oauth2-resource-server` for bearer token validation
- Spring Security configuration over manual interceptors when standard resource server behavior is enough

Only fall back to manual JWKS lookup and custom validation logic when the provider or architecture requires non-standard behavior.

## Implementation Checklist

When producing code or a plan, cover the relevant items below.

### Frontend Deliverables

- OIDC provider configuration
- Login entry point
- Callback handling
- Auth state restoration on app startup
- Route protection or guard logic
- API client auth header strategy
- Token refresh behavior if required
- Logout flow
- Return-to-original-page behavior after login
- Multi-provider selection if applicable

### Backend Deliverables

- Provider configuration and environment variables
- Metadata or JWKS discovery
- Token validation strategy
- User principal or claims mapping
- Protected and public route rules
- CORS and cookie strategy when frontend and backend are split
- Multi-issuer handling if applicable

## Architecture Guidance

Use the architecture that matches the product, not the most code-heavy option.

### SPA Talking Directly to APIs

Use Authorization Code Flow with PKCE.

Include:

- provider config
- callback page
- auth state provider
- refresh strategy if needed
- 401 retry or re-login behavior

Be explicit about token storage tradeoffs.

### Backend or BFF Owns the Session

Prefer backend-managed sessions and httpOnly cookies.

This is usually the safer default when:

- the backend already exists
- the frontend is same-origin with the backend
- the app does not need browser-side access tokens
- the team wants to reduce token exposure in JavaScript

### Multi-Provider Authentication

Keep provider-specific configuration explicit.

- Separate provider configs.
- Persist which provider initiated the login flow.
- Keep callback handling able to resolve the active provider.
- On the backend, support issuer-based selection rather than guessing.

## Output Expectations

When responding to a user task, produce only what is needed for that repository and request.

Prefer this order:

1. State the chosen flow and why it fits.
2. List the files or components that need to exist.
3. Implement the minimal complete path.
4. Call out required environment variables and provider settings.
5. Mention important follow-up checks such as logout, refresh, and expired-token handling.

Avoid pasting large tutorial blocks if the task only needs a narrow change.

## Common Pitfalls

Watch for these failure modes:

- Hardcoding token or JWKS endpoints instead of using discovery metadata.
- Recommending implicit flow.
- Storing refresh tokens in browser storage without acknowledging the risk.
- Forgetting to persist and restore the original return URL.
- Implementing refresh but not handling refresh failure.
- Validating signature only, while skipping issuer or audience checks.
- Assuming a single issuer when the app supports multiple providers.
- Mixing frontend login concerns with backend bearer-token validation concerns.

## Minimal Patterns

Use compact patterns instead of oversized examples.

### Frontend Config Shape

```typescript
export const oidcConfig = {
  authority: import.meta.env.VITE_OIDC_AUTHORITY,
  clientId: import.meta.env.VITE_OIDC_CLIENT_ID,
  redirectUri: `${window.location.origin}/auth/callback`,
  scope: 'openid profile email',
  responseType: 'code',
};
```

If the app is a public client, add PKCE support.

### Spring Resource Server Direction

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com
```

Prefer this direction over handwritten JWT parsing when standard Spring Security support is sufficient.

For fuller examples, read the relevant file from `references/` rather than pasting every variant by default.

## Verification

Before considering the integration complete, verify the relevant flows:

- Login succeeds from a clean session.
- Callback handles success and provider error responses.
- Protected routes redirect or reject correctly.
- Expired access tokens are handled correctly.
- Refresh behavior works or fails cleanly.
- Backend rejects tokens with wrong issuer or audience.
- Logout clears local state and, when needed, signs out from the provider.

## Final Reminder

This skill should help the model make a correct architectural choice first, then implement the smallest sound solution for that stack. Favor safe defaults, existing framework support, and repository-specific adaptation over generic auth boilerplate.
