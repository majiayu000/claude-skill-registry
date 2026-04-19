---
name: cloud-identity-and-auth
description: Identity, authentication, authorization, and token management for cloud platforms. Covers Keystone-style scoped tokens, OAuth 2.0 flows, OpenID Connect, JWT structure and pitfalls, federation with SAML/OIDC, service-to-service auth with mTLS and SPIFFE, principle of least privilege, IAM role design, and the service catalog pattern (public/internal/admin endpoints). Use when designing authn/authz for a multi-tenant cloud service, integrating with an identity provider, or reviewing IAM policies for over-privilege.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/cloud-identity-and-auth/SKILL.md
superseded_by: null
---
# Cloud Identity and Authentication

Identity is the bedrock of cloud security. Every API call, every internal RPC, every resource access must ultimately be attributable to a principal — a user, a service account, a workload — and must be authorized against a policy that the platform enforces uniformly. Getting this layer right is what separates a cloud platform from a collection of servers. Getting it wrong is the source of most breach post-mortems. This skill covers the core concepts and failure modes a cloud-systems practitioner has to handle.

**Agent affinity:** hamilton-cloud (IAM at AWS scale), vogels (service-to-service identity in SOA), lamport (formal reasoning about capability and delegation)

**Concept IDs:** cloud-keystone-auth, cloud-security-groups-policies, cloud-requirements-tracing

## The Three Questions

Every identity system answers three questions in order:

1. **Authentication (authn).** Who are you? Prove it.
2. **Authorization (authz).** What are you allowed to do?
3. **Accounting.** What did you do? (Audit logs.)

Separating these cleanly is the first design decision. Authentication produces an attested identity (a token, a certificate, a signed assertion). Authorization consumes that identity and a resource reference and returns allow/deny. Accounting records both.

## The Keystone Model: Scoped Tokens

OpenStack Keystone — and most cloud platforms that followed — use a scoped token model. A user authenticates and requests a token scoped to a project (or tenant, or organization). The token carries:

- The user's identity
- The project scope
- The roles granted to the user in that scope
- An expiration time
- A signature

Every downstream service (Nova, Neutron, Cinder, etc.) validates the token against Keystone and then consults its own policy file to determine whether the user's roles permit the requested action. The token is the authentication; the service's policy engine is the authorization.

### The Service Catalog Pattern

A scoped token also carries a service catalog — a list of endpoints the user can reach. Each service has three interface types:

- **public.** Internet-accessible endpoint (what external clients see).
- **internal.** Datacenter-internal endpoint, often different network path.
- **admin.** Operator-only endpoint for management and diagnostics.

Separating these by URL (not just by authz check) adds a network layer defense: even if someone acquires credentials, they need to be on the admin network to hit the admin endpoint.

## OAuth 2.0 and OpenID Connect

OAuth 2.0 is a delegation framework: a resource owner grants a client limited access to a resource without sharing credentials. It defines four main flows:

- **Authorization code flow.** Best for web applications. Client redirects user to authorization server, user authenticates there, authorization server sends a code back, client exchanges the code (using a client secret) for an access token.
- **Authorization code with PKCE.** Authorization code plus a proof-key-for-code-exchange, so public clients (mobile apps, SPAs) can use it without a client secret.
- **Client credentials.** Machine-to-machine. Client authenticates with its own credentials to get a token scoped to itself.
- **Device authorization.** For devices without a browser. Device shows a code, user enters it on another device.

**Avoid the legacy flows.** The implicit flow and resource owner password credentials grant are deprecated. They exist only to support very old clients and should not be used in new systems.

**OpenID Connect** (OIDC) sits on top of OAuth 2.0 and adds authentication. The authorization server issues both an access token (for API access) and an ID token (a JWT that attests to the user's identity). OIDC is the standard for federated single sign-on across cloud services.

## JWT: Structure and Pitfalls

A JSON Web Token is a compact, URL-safe, self-describing credential. Three base64url-encoded parts separated by dots: header, payload, signature.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSIsImV4cCI6MTcxMjM0NTY3OH0.abc...
```

The header declares the signing algorithm. The payload contains claims (standard ones like `iss`, `sub`, `aud`, `exp`, and application-specific ones). The signature is computed over header and payload with a secret (HMAC) or private key (RSA/ECDSA).

### JWT Failure Modes

- **`alg: none`.** Early JWT libraries would verify a token with `alg: none` by skipping signature check. Attackers sent tokens with forged payloads and `alg: none`. Always require a specific algorithm; never trust the header.
- **Algorithm confusion.** RSA public keys confused with HMAC secrets. Attacker takes the public key and uses it as an HMAC key. Reject tokens whose algorithm does not match what you expect.
- **Long-lived tokens.** JWTs are stateless — revocation is hard. Keep expirations short (minutes to an hour). Use refresh tokens for longer sessions, with refresh tokens held in server-side storage so they can be revoked.
- **Storing sensitive data in payload.** The payload is base64-encoded, not encrypted. Anyone with the token can read its claims.
- **Missing `aud` check.** A token issued for service A should not be accepted by service B. Always validate audience.

## Federation

Federation lets users from one identity provider (an organization's AD, Google Workspace, Okta) authenticate to another system without that system holding their credentials. Two dominant protocols:

- **SAML 2.0.** XML-based, widely used in enterprise SSO. Complex specification, lots of interoperability pitfalls, but entrenched.
- **OIDC.** JSON-based, simpler, modern. Increasingly the default for new systems.

The cloud platform (service provider) trusts the identity provider to attest to user identity and group membership, and maps those groups to local roles. Federation shifts credential management to one place, at the cost of making the identity provider a single point of failure and a high-value target.

## Service-to-Service Authentication

Inter-service calls inside a cloud platform cannot use human credentials. Several patterns:

- **mTLS.** Each service has a certificate issued by an internal CA. Services authenticate each other by presenting certificates in the TLS handshake. Strong and uniform, but certificate lifecycle management is nontrivial.
- **SPIFFE / SPIRE.** Standardized identity document format (SVID) and a workload attestation mechanism that binds identities to running workloads without a bootstrap secret.
- **Bearer tokens.** A service authenticates once (e.g., via cloud metadata service) and then presents a bearer token to downstream services. Simpler but the token is sensitive in transit.
- **Signed request headers.** AWS SigV4 is the canonical example. The client signs the request with its secret; the server verifies. Works well for request/reply.

## Authorization Models

- **Role-Based Access Control (RBAC).** Users have roles, roles have permissions. Simple, well-understood, scales to thousands of users. The model most cloud platforms start with.
- **Attribute-Based Access Control (ABAC).** Permissions are functions of attributes of the user, the resource, and the environment. More expressive, harder to audit. Used when RBAC cannot express the policy ("users from department X can access files tagged Y during hours Z").
- **Policy-as-code.** Write policies in a declarative language (AWS IAM policy language, Rego for Open Policy Agent, Cedar). Allows static analysis, diffing, and unit testing of permissions.

### Least Privilege

The baseline security principle: a principal should have the minimum permissions required to do its job. Implementation:

- Start from a deny-all default.
- Grant permissions explicitly.
- Review permissions on a schedule, removing stale grants.
- Use service accounts instead of personal accounts for automation.
- Rotate credentials, especially long-lived ones.
- Prefer short-lived tokens (STS, OIDC exchange) over long-lived keys.

## Common Failure Modes

| Failure | Example | Mitigation |
|---|---|---|
| Overprivileged default role | New service gets `admin` because "we'll tighten later" | Start with deny-all; document and track exceptions |
| Secrets in env vars committed to git | AWS keys in `.env` pushed to GitHub | Pre-commit hooks, secret scanning, rotate on detection |
| Long-lived API keys | Customer's key from 2018 still works | Mandatory rotation, expiration on all keys |
| Token scope too broad | API token with full account access for a single read op | Per-operation scopes, prefer OAuth scopes over raw keys |
| Missing audit trail | No record of who accessed what | Log every authz decision with principal, resource, action |
| Audit logs tamperable | Admin can edit logs | Append-only store, off-box shipping, hash chains |

## When to Use This Skill

- Designing the identity subsystem of a new cloud service or multi-tenant platform.
- Integrating a cloud service with an enterprise identity provider.
- Reviewing an IAM policy set for least-privilege violations.
- Implementing service-to-service authentication inside a datacenter.
- Diagnosing a production incident involving authentication or authorization failures.
- Writing a policy-as-code authorization layer.

## When NOT to Use This Skill

- Single-user, single-machine tools — OS-level permissions suffice.
- Pre-authenticated contexts where identity is handled upstream and the service only sees a principal ID.

## Decision Guidance

| Need | Recommended |
|---|---|
| Enterprise SSO | OIDC (preferred) or SAML 2.0 |
| API access for web app | OAuth 2.0 authorization code with PKCE |
| Machine-to-machine API | Client credentials flow, or SigV4-style signing |
| Inter-service auth in cluster | mTLS via SPIFFE/SPIRE, or service mesh |
| Fine-grained resource policy | ABAC with policy-as-code (Rego, Cedar) |
| Coarse organizational policy | RBAC with periodic review |
| Audit log integrity | Append-only storage, off-box shipping |

## References

- Hardt, D. (2012). "The OAuth 2.0 Authorization Framework." RFC 6749.
- Sakimura, N., et al. (2014). "OpenID Connect Core 1.0."
- Jones, M., et al. (2015). "JSON Web Token (JWT)." RFC 7519.
- NIST SP 800-63B. "Digital Identity Guidelines: Authentication and Lifecycle Management."
- Saltzer, J., Schroeder, M. (1975). "The Protection of Information in Computer Systems." IEEE.
- SPIFFE project documentation. https://spiffe.io
- Keystone documentation, OpenStack project.
