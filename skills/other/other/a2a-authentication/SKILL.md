---
name: a2a-authentication
description: Implement A2A authentication — API keys, Bearer tokens, OAuth 2.0, OpenID Connect, and mutual TLS. Use when securing agent-to-agent communication and configuring Agent Card security schemes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Authentication

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the authentication and security section
2. Web-search `site:github.com a2aproject A2A authentication security schemes` for auth scheme details
3. Web-search `site:github.com a2aproject a2a-samples authentication` for auth implementation examples
4. Fetch SDK docs for authentication middleware and client credential handling

## Conceptual Architecture

### Why Authentication Matters

In multi-agent systems, agents must verify each other's identity and authorize access:
- **Server agents** need to know who's calling them and whether they're authorized
- **Client agents** need to present valid credentials to access server agents
- **Agent Cards** declare what authentication is required upfront

### Five Security Schemes

A2A supports the same security scheme types as OpenAPI 3.0:

#### 1. API Key (`apiKey`)
A static key sent in a header or query parameter.
- **Best for**: Internal agents, simple integrations, development
- **Agent Card declares**: Header name and location
- **Client provides**: The key value in the specified header

#### 2. HTTP Bearer (`http` with `scheme: bearer`)
A bearer token (JWT or opaque) in the `Authorization` header.
- **Best for**: Token-based auth, service-to-service with JWTs
- **Agent Card declares**: Bearer scheme, optional format hint
- **Client provides**: `Authorization: Bearer <token>`

#### 3. OAuth 2.0 (`oauth2`)
Standard OAuth 2.0 flows for token acquisition.
- **Best for**: Production systems, fine-grained scopes, delegated access
- **Agent Card declares**: OAuth flows (clientCredentials, authorizationCode), token URL, scopes
- **Client provides**: Access token obtained from the OAuth server

Common flow for agent-to-agent: **Client Credentials** (machine-to-machine, no user involvement).

#### 4. OpenID Connect (`openIdConnect`)
OIDC discovery-based authentication.
- **Best for**: Enterprise systems with identity providers, SSO environments
- **Agent Card declares**: OIDC discovery URL (`openIdConnectUrl`)
- **Client provides**: Token obtained via OIDC flow

#### 5. Mutual TLS (`mutualTLS`)
Client certificate-based authentication.
- **Best for**: High-security environments, zero-trust networks
- **Agent Card declares**: mTLS requirement
- **Client provides**: Client certificate during TLS handshake

### Agent Card Authentication Declaration

Authentication requirements are declared in the Agent Card using two top-level fields, `securitySchemes` (a map of named scheme definitions) and `security` (an array of required scheme references):
```json
{
  "securitySchemes": {
    "oauth2_auth": {
      "type": "oauth2",
      "flows": {
        "clientCredentials": {
          "tokenUrl": "https://auth.example.com/token",
          "scopes": {
            "agent:read": "Read access",
            "agent:write": "Write access"
          }
        }
      }
    }
  },
  "security": [
    { "oauth2_auth": [] }
  ]
}
```

### Extended Agent Card

The `agent/authenticatedExtendedCard` method allows agents to return a richer Agent Card to authenticated clients — exposing additional skills or capabilities that aren't visible to unauthenticated discovery.

### Auth-Required State

If a task requires authentication mid-flow:
1. Server transitions task to `auth-required` state
2. Status message includes auth instructions
3. Client authenticates and resumes the task
4. Server transitions back to `working`

### Best Practices

- Always use HTTPS for A2A communication in production
- Prefer OAuth 2.0 client credentials for production agent-to-agent auth
- Use API keys only for development or internal low-risk scenarios
- Rotate credentials regularly and support credential refresh
- Declare authentication in the Agent Card so clients know requirements before calling
- Implement rate limiting alongside authentication
- Log authentication failures for security monitoring
- Use the `auth-required` task state for dynamic auth challenges

Fetch the specification for exact authentication schema structures, security scheme field names, and the extended card method before implementing.
