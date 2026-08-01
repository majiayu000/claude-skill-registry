---
name: jwt-verification
description: Verify JWT tokens in backend services and enforce authenticated user
  context. This skill establishes patterns for token validation, claim extraction,
  and user context propagation throughout the backend request lifecycle.
---

# Skill: jwt-verification

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

## Phase Applicability
Phase II only. Phase I has no authentication requirements.
