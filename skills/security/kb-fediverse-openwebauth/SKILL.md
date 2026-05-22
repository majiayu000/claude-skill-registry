---
name: kb-fediverse-openwebauth
description: >
  Background knowledge about the OpenWebAuth (OWA) federated remote
  authentication protocol, based on FEP-61cf (DRAFT status). Covers the
  5-step authentication handshake between home instance, target instance,
  and user browser; WebFinger discovery of redirect and token endpoints
  (rel="http://purl.org/openwebauth/v1" and v1#redirect); HTTP Signature
  signed token requests; RSA PKCS#1 v1.5 encrypted single-use tokens;
  the owt query parameter; the zid login trigger; the /magic fallback
  endpoint; authentication vs authorization distinction; security
  considerations (open redirects, CSRF, information leakage, token
  expiry); the history from Magic Auth in Mistpark (2010) through Zot
  and Hubzilla to standalone OpenWebAuth (2017); comparison with OAuth
  2.0 and OIDC (FEP-d8c2); use cases for private content access,
  cross-server permissions, and wall-to-wall posting; and implementations
  across Hubzilla, Streams, Forte, Friendica, and FedIAM. Load when the
  user asks about federated single sign-on in the Fediverse; OpenWebAuth
  or OWA; Magic Auth; FEP-61cf; how to authenticate remote users without
  local accounts; cross-server identity verification; how to let users
  from other instances access private content; the zid parameter; the
  owt token flow; how Hubzilla's remote authentication works; or how to
  implement browser-based SSO for ActivityPub servers.
user-invocable: false
---

# Fediverse OpenWebAuth (FEP-61cf) — Complete Reference

## Overview

OpenWebAuth (OWA) is a federated remote authentication protocol that
enables browser-based single sign-on across Fediverse services. A user
logged in at their home instance can be automatically recognized by other
compatible servers without creating local accounts, without third-party
cookies, and often without any explicit user interaction.

FEP-61cf (authored by FenTiger, received 2024-02-06, **status DRAFT**)
formally documents the protocol, which was written based on
reverse-engineering existing implementations in Hubzilla and (streams).

OpenWebAuth is also known as Magic Auth, Magic Sign On, Remote
Authentication, or rMagic. The name "Magic Auth" persists informally
because "of how seamless the experience is."

## The Problem: No Identity Across Servers

In the current Fediverse, when you browse to a different server, that
server has no idea who you are. This causes several painful problems:

1. **Private content is inaccessible** — if someone on `podunk.edu` shares
   a private video only with `bob@example.com`, Bob cannot view it by
   visiting `podunk.edu`. The server doesn't know he's Bob.

2. **Remote profiles are limited** — when jumping from instance to instance,
   users lose their identity. They can't interact natively with content.

3. **No cross-server permissions** — fine-grained access controls (e.g.,
   "only Alice and Bob can see this photo") only work when the server can
   identify the viewer.

4. **No wall-to-wall posting** — users can't post directly on someone
   else's wall or profile on a remote server.

OpenWebAuth solves this: "You can jump from one part of the Fediverse to
another, and your permissions will be granted automatically. Anything you
were given permission to access unlocks and becomes visible on the page."

## Authentication vs Authorization

OpenWebAuth is strictly an **authentication** protocol — it proves who you
are. It is NOT an authorization protocol.

> "OpenWebAuth allows `someone@example.social` to log into `example.com`
> as `someone@example.social`, and `example.com` determines what
> `someone@example.social` can do on `example.com`. But `example.com`
> cannot impersonate `someone@example.social`."

The target instance decides locally what an authenticated remote user can
do. OpenWebAuth provides the identity; the target provides the permissions.

This is the fundamental distinction from OAuth 2.0, which is an
**authorization** framework — it grants permissions for a client to act on
behalf of a user.

## Architecture

The protocol has two participants:

- **Home instance** — hosts the user's identity. Equivalent to the Identity
  Provider (IdP) in SAML and OpenID Connect. Only the home instance has
  access to the user's private key.
- **Target instance** — allows remote users to log in. Equivalent to the
  Relying Party (RP) in SAML and OpenID Connect. Only uses public keys.

Each user is identified by a public/private key pair. The protocol relies
on ActivityPub actor documents for public key discovery.

## Login Flow Initiation

Two mechanisms trigger the authentication:

1. **Login form** — user visits the target instance and submits their
   Fediverse ID (e.g., `alice@example.social`) via a login form
2. **`zid=` parameter** — user follows a link containing
   `?zid=alice@example.social`, which auto-triggers authentication

The `zid=` mechanism can be used in links embedded in content, enabling
seamless authentication when clicking through from a home timeline to
remote content.

**Security note**: the `zid=` parameter can facilitate attacks if
adversaries craft malicious links with manipulated identity values.

## The 5-Step Protocol Handshake

### Step 1: Target Redirects to Home Instance

The target instance discovers the home instance's redirect endpoint via
WebFinger:

```
GET /.well-known/webfinger?resource=acct:alice@home.example
```

Look for a link with `rel="http://purl.org/openwebauth/v1#redirect"`.
If not found, fall back to the hardcoded `/magic` endpoint on the home
instance.

Construct the redirect URL:

```
https://home.example/magic?owa=1&bdest=<hex-encoded-destination-URL>
```

The `bdest` parameter contains the target URL (where the user wants to end
up) converted from UTF-8 to hexadecimal encoding.

**Origin validation**: the target MUST validate that the redirect hostname
matches the claimed identity's domain to prevent open redirector abuse.

### Step 2: Home Instance Requests a Token

The home instance's `/magic` endpoint:

1. Verifies the user has a valid session cookie (i.e., is logged in)
2. Decodes the `bdest` URL from hex
3. Performs a WebFinger lookup for the target's token endpoint, seeking
   `rel="http://purl.org/openwebauth/v1"`
4. Sends an HTTP-Signature-signed request to the token endpoint
5. Includes an `X-Open-Web-Auth` header with a random string for
   additional entropy
6. If WebFinger discovery fails, returns an HTTP error (preventing open
   redirection — never redirects on failure)

The signed request uses an `Authorization` header starting with the word
`Signature` followed by the encoded HTTP signature, per ActivityPub
conventions.

### Step 3: Target Instance Provides Encrypted Token

The target instance's token endpoint:

1. Extracts the `keyId` from the signed request's `Authorization` header
2. Fetches the actor record and public key via the `keyId` URL
3. Verifies the HTTP signature
4. Generates a URL-safe random token string
5. Stores the token locally (with a short expiry, typically minutes)
6. Encrypts the token using the actor's **public key** with RSA PKCS #1
   v1.5
7. Encodes the encrypted result as URL-safe Base64 without padding
8. Returns JSON:

```json
{
  "success": true,
  "encrypted_token": "<base64-encoded-encrypted-token>"
}
```

The token endpoint accepts both GET and POST requests. Some implementations
send POST with random bodies.

### Step 4: Home Instance Decrypts and Redirects

The home instance:

1. Decodes the JSON response
2. Verifies `"success": true`
3. Decrypts the Base64-encoded token using the actor's **private key**
4. Redirects the user's browser to:

```
<bdest>?owt=<decrypted-token>
```

### Step 5: Target Instance Validates Token and Logs In

The target instance:

1. Extracts the `owt` query parameter
2. Matches it against the token stored in Step 3
3. If valid, logs the user in as the remote identity
4. **Immediately deletes the token** — single-use enforcement

After this step, the target instance sets a session cookie for the
authenticated remote user. Subsequent page loads on the target don't
require repeating the handshake.

## WebFinger Link Relations

The protocol defines two custom WebFinger link relations:

| Relation | Purpose | Published by |
|----------|---------|-------------|
| `http://purl.org/openwebauth/v1#redirect` | Redirect endpoint (Step 1) | Home instance |
| `http://purl.org/openwebauth/v1` | Token endpoint (Step 2-3) | Target instance |

If the redirect endpoint is not discoverable via WebFinger, implementations
fall back to the hardcoded `/magic` path on the home instance.

## Key Usage Summary

| Operation | Key used | By whom |
|-----------|----------|---------|
| Sign token request (Step 2) | Private key | Home instance |
| Verify signature (Step 3) | Public key | Target instance |
| Encrypt token (Step 3) | Public key | Target instance |
| Decrypt token (Step 4) | Private key | Home instance |

Only the home instance ever touches the private key. The target instance
operates exclusively with public keys.

## Security Considerations

### Information Leakage

The home instance learns which target instances the user visits (because it
performs the redirect and token exchange on the user's behalf).
Implementations should consider consent screens or privacy policies
restricting automatic authentication.

### Token Security

- Tokens are **single-use** — deleted immediately after validation
- Tokens **expire within minutes** — prevents storage exhaustion (DoS) from
  unused tokens
- Tokens are **encrypted with the actor's public key** — only the home
  instance (with the private key) can decrypt them

### Impersonation Prevention

The target instance MUST trust the `owt=` token over the original `zid=`
parameter. The identity proven by the cryptographic handshake takes
precedence over the unverified `zid` claim.

Additionally, the target validates that the token endpoint's origin matches
the `bdest` origin, preventing attackers from redirecting users to malicious
token endpoints.

### Open Redirection Mitigations

Three layers of defense:

1. **First redirect** (target → home): validates that the hostname matches
   the claimed identity
2. **Second redirect** (home → target): validates that the token endpoint
   origin matches the `bdest` origin
3. **Failed discovery**: returns HTTP errors rather than redirecting —
   never silently redirects on failure

### The `zid=` Attack Surface

Links containing `zid=` parameters can be crafted by adversaries. When
generalized beyond OpenWebAuth, this parameter could enable mix-up attacks.
OpenWebAuth mitigates this through strict origin validation at each step.

## History: From Magic Auth to OpenWebAuth

### Magic Auth in Mistpark (2010)

Mike Macgirvin created Magic Auth as part of **Mistpark** in 2010 — the
project that would later become Friendica. Magic Auth enabled federated
single sign-on across decentralized nodes but was tightly coupled to the
Zot protocol and "somewhat limited" in Friendica.

### Integration into Hubzilla via Zot

As Mistpark evolved through Friendika → Friendica → Red Matrix →
**Hubzilla**, Magic Auth remained embedded in the Zot protocol. In Hubzilla,
it became central to features like fine-grained access control, private
content sharing, and wall-to-wall posting — all of which depend on knowing
who is visiting the server.

### Standalone OpenWebAuth (October 2017)

Magic Auth was "separated from Zot and made into its own protocol called
OpenWebAuth to facilitate adoption by other platforms." Released in Hubzilla
2.8. The key insight: authentication and communication are **orthogonal
problems**. By extracting auth into a standalone spec, non-Zot projects
could adopt it without the full Zot stack.

### Zotlabs Era (2018-2022)

Mike Macgirvin launched Zotlabs to advance Zot6 and integrate OpenWebAuth.
Multiple experimental projects (Osada, Zap, Roadhouse) eventually converged
into the **(streams) repository** (October 2021).

### Broader Adoption (2023+)

- **Friendica** became the first non-Zot-family project to implement
  OpenWebAuth (~2023)
- **Forte** (by benpate) implemented OWA as an alternative to Activity
  Intents for wall-to-wall posting
- **FedIAM** implemented the protocol
- **FEP-61cf** submitted February 2024, formally documenting the protocol

## OpenWebAuth vs OAuth 2.0 / OIDC

| Aspect | OpenWebAuth (FEP-61cf) | OAuth 2.0 / OIDC (FEP-d8c2) |
|--------|----------------------|----------------------------|
| Purpose | Authentication (identity) | Authorization (permissions) |
| Scope | Browser-based SSO only | Multi-platform (browser, mobile, API) |
| Complexity | Simple — WebFinger + HTTP Sig + token | Complex — client registration, scopes, refresh tokens |
| Client registration | None required | Required (RFC 7591) |
| Fediverse implementations | 5+ servers | Mastodon's partial OAuth (non-compliant RFC 7591) |
| Private key usage | Home instance only | Client + server |
| Target can act as user? | No — authentication only | Yes — authorized actions via access tokens |

The "not invented here" criticism (erlend_sh on SocialHub) argued existing
OAuth/OIDC standards should be used instead. FenTiger's response: OWA and
OAuth solve different problems; OWA is simpler, already deployed, and OIDC
Discovery + Dynamic Client Registration have no existing Fediverse
implementations.

## Implementation Status

### Identity Providers (Publishing OWA)

| Implementation | Status | Since |
|---------------|--------|-------|
| Hubzilla | Implemented | 2017 (v2.8) |
| (streams) | Implemented | 2021 |
| Forte | Implemented | 2024 |
| Friendica | Partial | ~2023 |
| FedIAM | Implemented | 2024 |
| Mastodon | Proposed (issue #7643) | — |
| Pixelfed | Proof-of-concept | — |

### Relying Parties (Accepting OWA)

| Implementation | Status |
|---------------|--------|
| Hubzilla | Implemented |
| (streams) | Implemented |
| Forte | Implemented |
| FedIAM | Implemented |
| Bridgy Fed | Proposed |
| Great Ape | Proposed |

### The Mastodon Barrier

Mastodon issue #7643 (opened May 2018, still open) requests OpenWebAuth
support. The fundamental barrier: implementing server-side OWA requires
"the Mastodon service to have the concept of authorization of users without
an account on the Mastodon server." This is an architectural change, not
just a protocol implementation. A partial PR (#25012) was created for
client-side functionality only.

## Implementation Guidance

### Publishing as an Identity Provider (Home Instance)

1. Advertise your redirect endpoint via WebFinger with
   `rel="http://purl.org/openwebauth/v1#redirect"`
2. Implement the redirect endpoint (traditionally `/magic`):
   - Check the user's session cookie
   - Decode the `bdest` parameter from hex
   - Discover the target's token endpoint via WebFinger
   - Send an HTTP-Signature-signed request with `X-Open-Web-Auth` header
   - Decrypt the returned token with the actor's private key
   - Redirect the browser to `bdest?owt=<token>`
3. On failure at any step, return an HTTP error — never redirect

### Accepting as a Relying Party (Target Instance)

1. Advertise your token endpoint via WebFinger with
   `rel="http://purl.org/openwebauth/v1"`
2. Implement the token endpoint:
   - Extract `keyId` from the `Authorization: Signature ...` header
   - Fetch the actor's public key
   - Verify the HTTP signature
   - Generate a random token, store it locally with a short TTL
   - Encrypt with the actor's public key (RSA PKCS #1 v1.5)
   - Return `{"success": true, "encrypted_token": "<base64>"}`
3. On pages that accept `owt=` parameter:
   - Match the token against stored tokens
   - Log the user in as the remote identity
   - Delete the token immediately
4. Implement a login form or `zid=` parameter handling to trigger the flow
5. Decide what permissions authenticated remote users receive

### Handling the `zid=` Parameter

Check for `zid=` on page loads. If present and the user is not already
authenticated, initiate the OpenWebAuth flow. The `zid` value is the user's
Fediverse address (e.g., `alice@home.example`).

### Hardcoded Path Concerns

The `/magic` fallback path may conflict with CMS content. Best practice:

1. Always check WebFinger first for the redirect/token endpoints
2. Only fall back to `/magic` for backward compatibility with older
   Hubzilla/Streams instances
3. Consider using `/.well-known/open-web-auth` for new implementations
   (proposed by benpate but not yet standardized)

## Known Issues and Open Questions

1. **DRAFT status** — FEP-61cf has not reached FINAL; the spec may change
2. **Browser-only** — no support for mobile apps, API clients, or desktop
   applications (unlike OAuth/OIDC)
3. **Privacy concern** — home instance learns every target the user visits;
   most implementations don't show consent screens
4. **Mastodon architectural gap** — supporting accountless remote users
   requires fundamental changes to Mastodon's data model
5. **Hardcoded `/magic` path** — conflicts with CMS installations;
   WebFinger-first discovery should become primary
6. **Missing spec details** — cookie-based login verification and activity
   attribution to home instance actors are implementation requirements not
   fully documented in the FEP
7. **RSA-only encryption** — the token encryption uses RSA PKCS #1 v1.5;
   no support for Ed25519 or other key types commonly used in newer
   ActivityPub implementations
8. **Redundancy debate** — silverpill argued that self-controlled keys
   (FEP-ae97) could make OWA redundant; the community has not resolved this
