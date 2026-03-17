---
name: jwt-verification
description: "Verify JWT tokens in backend services and enforce authenticated user context. This skill should be used when implementing JWT token validation in FastAPI, extracting user identity from JWT claims, designing authenticated endpoint middleware, establishing user context for request processing, handling token expiration and refresh scenarios, and debugging authentication failures."
---

# JWT Verification

## Purpose
Verify JWT tokens in backend services and enforce authenticated user context. This skill establishes patterns for token validation, claim extraction, and user context propagation throughout the backend request lifecycle.

## When to Use
- When implementing JWT token validation in FastAPI
- When extracting user identity from JWT claims
- When designing authenticated endpoint middleware
- When establishing user context for request processing
- When handling token expiration and refresh scenarios
- When debugging authentication failures

## When NOT to Use
- When working on frontend authentication (use better-auth-integration)
- When designing the overall auth flow (use jwt-authentication)
- When tokens haven't been issued yet
- When working on public/unauthenticated endpoints
- When designing authorization rules (use auth-boundary-design)

## Required Clarifications
1. What is the JWT token format and structure expected by the system?
2. What authentication provider is issuing the tokens (Better Auth, Auth0, etc.)?
3. What are the specific claims that need to be extracted and validated?
4. What is the expected token signature algorithm (RS256, HS256, etc.)?

## Optional Clarifications
5. Are there specific error handling requirements for invalid tokens?
6. Are there existing auth patterns in the codebase to follow?
7. What are the performance requirements for token verification?

## Responsibilities
- Validate JWT signature using appropriate secret/public key
- Verify token expiration (exp claim)
- Extract user identity from token claims (sub, email, etc.)
- Propagate user context through request lifecycle
- Handle invalid/expired token errors appropriately
- Configure JWT validation middleware for FastAPI
- Support token refresh when needed
- Log authentication events for security auditing

## Inputs
- JWT tokens from Authorization header
- JWT secret or public key configuration
- Expected token claims and structure
- Token issuer configuration (Better Auth)
- Authentication requirements from specifications

## Outputs
- Validated user context object
- Authentication middleware for FastAPI
- Error responses for invalid tokens (401 Unauthorized)
- User identity extraction patterns
- Token validation configuration

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |

## Implementation Workflow
1. Assess JWT verification requirements
2. Configure JWT validation with appropriate keys
3. Implement token signature verification
4. Extract and validate required claims
5. Create authentication middleware
6. Handle error cases appropriately
7. Test token validation with various scenarios
8. Document verification patterns

## Output Checklist
- [ ] JWT signature validation implemented
- [ ] Token expiration verification configured
- [ ] User identity extraction working
- [ ] Authentication middleware created
- [ ] Error handling for invalid tokens implemented
- [ ] Security logging configured
- [ ] Performance requirements met

## Constraints
- Never trust token claims without signature verification
- Never log full token contents (security risk)
- Never store tokens in backend (stateless verification)
- Never bypass verification for any authenticated endpoint
- Always verify token expiration
- Always use secure key management (environment variables)
- Always return 401 for invalid/expired tokens

## Interaction With Other Skills
- **jwt-authentication:** Operates within broader authentication flow design
- **better-auth-integration:** Validates tokens issued by Better Auth
- **fastapi-architecture:** Integrates as middleware in FastAPI application
- **auth-boundary-design:** Provides verified user context for authorization
- **python-backend-structure:** Fits within backend code organization

## Anti-Patterns
- **Signature skip:** Accepting tokens without signature verification
- **Expiration ignore:** Not checking token expiration claims
- **Claim trust:** Blindly trusting token claims without verification
- **Token logging:** Logging full tokens which exposes credentials
- **Inconsistent handling:** Different verification logic across endpoints
- **Secret exposure:** Hardcoding JWT secrets in source code
- **Error leakage:** Exposing verification failure details to attackers

## Security Best Practices
- Use asymmetric algorithms (RS256) for better security
- Implement proper key rotation mechanisms
- Use constant-time comparison for token validation
- Log authentication attempts without revealing sensitive details
- Implement rate limiting for authentication endpoints
- Validate all token claims, not just the signature

## Documentation Resources
- [JWT Verification Best Practices](https://jwt.io/introduction)
- [RFC 7519 - JWT Specification](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)

## Phase Applicability
Phase II only. Phase I has no authentication requirements.