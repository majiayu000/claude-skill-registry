---
name: oauth2-oidc
description: >-
  Assists with implementing OAuth 2.0 and OpenID Connect for secure authentication and
  authorization. Use when configuring authorization flows, validating tokens, implementing
  PKCE for public clients, setting up social login, or building secure token handling for
  SPAs, mobile apps, and APIs. Trigger words: oauth, oidc, openid connect, authorization
  code, pkce, jwt, access token, refresh token.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["oauth2", "oidc", "authentication", "authorization", "jwt"]
---

# OAuth 2.0 / OpenID Connect

## Overview

OAuth 2.0 is the industry standard for API authorization, and OpenID Connect (OIDC) extends it for user authentication. Together they provide Authorization Code + PKCE for secure token exchange, JWT-based identity tokens, refresh token rotation, and integration with identity providers (Auth0, Okta, Keycloak, Google, Azure AD) for social login and enterprise SSO.

## Instructions

- When implementing authentication, use the Authorization Code + PKCE flow for all client types (SPAs, mobile, server) since it is the only secure flow; never use the deprecated Implicit or Resource Owner Password flows.
- When validating tokens on the API side, verify the JWT signature using the provider's JWKS endpoint, check `exp`, `iss`, and `aud` claims, and never trust client-side token validation alone.
- When storing tokens in web apps, use `httpOnly`, `secure`, `sameSite=lax` cookies; never store tokens in localStorage since it is vulnerable to XSS.
- When managing token lifecycle, use short-lived access tokens (5-15 minutes) with refresh token rotation where each refresh token is single-use and a new one is issued with each refresh.
- When integrating a provider, use the discovery endpoint (`/.well-known/openid-configuration`) for auto-configuration rather than hardcoding endpoints.
- When implementing logout, revoke the refresh token, clear the session, and redirect to the provider's logout endpoint for complete session termination.

## Examples

### Example 1: Add social login to a Next.js app with PKCE

**User request:** "Implement Google and GitHub login for my Next.js app using OAuth 2.0"

**Actions:**
1. Configure the OIDC providers with client IDs and redirect URIs
2. Implement the Authorization Code + PKCE flow with state and nonce validation
3. Exchange the code for tokens and validate the ID token JWT claims
4. Store the session in httpOnly cookies with refresh token rotation

**Output:** A Next.js app with secure social login via Google and GitHub, PKCE-protected token exchange, and httpOnly cookie sessions.

### Example 2: Secure a REST API with JWT validation

**User request:** "Add OAuth 2.0 token validation to my API endpoints"

**Actions:**
1. Fetch the provider's JWKS from the discovery endpoint
2. Create middleware that validates the access token signature, expiration, issuer, and audience
3. Extract user claims and custom scopes from the validated token
4. Return 401 for invalid tokens and 403 for insufficient scopes

**Output:** An API with JWT-based authorization that validates tokens against the provider's JWKS and enforces scope-based access control.

## Guidelines

- Always use Authorization Code + PKCE since it is the only secure flow for all client types.
- Validate tokens on the API side: verify signature, `exp`, `iss`, and `aud`; never trust client-side validation alone.
- Use `httpOnly`, `secure`, `sameSite=lax` cookies for token storage in web apps, not localStorage.
- Implement refresh token rotation where each refresh token is single-use.
- Use the provider's discovery endpoint for configuration rather than hardcoding endpoints.
- Request minimum scopes needed: `openid email` for login, not all available scopes.
- Implement proper logout: revoke refresh token, clear session, redirect to provider's logout endpoint.
