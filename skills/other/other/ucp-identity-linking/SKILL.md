---
name: ucp-identity-linking
description: Implement UCP Identity Linking — OAuth 2.0 authorization code flow for linking buyer accounts between platforms and merchants, enabling personalized checkout experiences. Use when implementing account linking or SSO for UCP.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Identity Linking

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification identity-linking` and fetch the page for exact OAuth requirements, scopes, and metadata format.

Also fetch https://developers.google.com/merchant/ucp/guides/identity-linking for Google's integration guide.

## Conceptual Architecture

### What It Enables

Identity Linking lets a Platform (AI agent) authenticate a buyer with a Business (merchant) so the agent can:
- Access the buyer's existing account (loyalty points, saved addresses, order history)
- Apply account-specific discounts or pricing
- Provide personalized checkout experiences

### Protocol: OAuth 2.0 Authorization Code Flow

UCP mandates **RFC 6749 Section 4.1** (Authorization Code) as the primary mechanism:

1. Platform redirects buyer to Business's authorization endpoint
2. Buyer authenticates and consents
3. Business redirects back with authorization code
4. Platform exchanges code for access token at Business's token endpoint
5. Platform includes access token in subsequent UCP requests

### Requirements

- **HTTP Basic Authentication** (RFC 7617) for client credentials at the token endpoint
- **RFC 8414** OAuth Authorization Server Metadata at `/.well-known/oauth-authorization-server`
- **RFC 7009** token revocation support
- **RFC 9728** HTTP Resource Metadata — for discovering and linking identity provider metadata
- Optional: **OpenID RISC Profile 1.0** for async account status updates (e.g., account deleted)

### UCP Scopes

| Scope | Grants |
|-------|--------|
| `ucp:scopes:checkout_session` | All checkout operations (create, get, update, complete, cancel) |

A scope covering a capability grants access to ALL operations of that capability.

### Capability Declaration

Identity Linking is declared as a capability in the Business's discovery profile. It includes:
- Authorization endpoint URL
- Token endpoint URL
- Supported scopes
- Client registration details

### Implementation Guidance

**Business:**
- Implement standard OAuth 2.0 Authorization Code server
- Publish OAuth metadata at `/.well-known/oauth-authorization-server`
- Map UCP scopes to internal permissions
- Issue access tokens that the Platform includes in UCP requests

**Platform:**
- Discover identity linking capability from Business profile
- Initiate OAuth flow when buyer wants to link their account
- Store and refresh access tokens
- Include tokens in UCP request authorization

Fetch the exact current requirements from the live spec — OAuth details (PKCE requirements, token formats, etc.) may evolve.
