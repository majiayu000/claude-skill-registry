---
name: jwt-authentication
description: "Define authentication flow using JWT between frontend and backend. This skill should be used when designing the overall authentication architecture, planning token flow between frontend and backend, establishing token format and claims structure, and defining authentication state machine."
---

# JWT Authentication

## Purpose
Define authentication flow using JWT between frontend and backend. This skill establishes the end-to-end authentication architecture, coordinating token issuance on the frontend with verification on the backend to enable secure, stateless authentication.

## When to Use
- When designing the overall authentication architecture
- When planning token flow between frontend and backend
- When establishing token format and claims structure
- When defining authentication state machine
- When planning token refresh and expiration handling
- When documenting authentication requirements

## When NOT to Use
- When implementing frontend auth details (use better-auth-integration)
- When implementing backend verification (use jwt-verification)
- When working on authorization (use auth-boundary-design)
- When authentication approach hasn't been decided
- When specifications don't require authentication

## Required Clarifications
1. What are the specific authentication requirements from the specification?
2. What frontend technology is being used (Next.js, React, etc.)?
3. What backend technology is being used (FastAPI, etc.)?
4. What are the specific security requirements for the authentication system?

## Optional Clarifications
5. Are there specific user experience requirements for the authentication flow?
6. Are there existing auth patterns in the codebase to follow?
7. What are the session duration and refresh policies needed?

## Responsibilities
- Design end-to-end authentication flow
- Define JWT token structure and claims
- Plan token issuance and refresh lifecycle
- Establish token transmission patterns (headers, cookies)
- Document authentication state transitions
- Coordinate frontend and backend auth responsibilities
- Define session duration and refresh policies
- Plan logout and token invalidation

## Inputs
- Authentication requirements from specifications
- Frontend technology (Next.js, Better Auth)
- Backend technology (FastAPI)
- Security requirements
- User experience requirements

## Outputs
- Authentication flow diagram
- JWT token structure specification
- Token lifecycle documentation
- API authentication patterns
- Session management strategy
- Error handling specifications

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |

## Implementation Workflow
1. Assess authentication requirements
2. Design JWT token structure and claims
3. Plan token issuance and refresh lifecycle
4. Define authentication flow between frontend and backend
5. Document state transitions and error handling
6. Create authentication flow diagram
7. Validate against security requirements

## Output Checklist
- [ ] Authentication flow diagram created
- [ ] JWT token structure defined
- [ ] Token lifecycle documented
- [ ] API authentication patterns established
- [ ] Session management strategy defined
- [ ] Error handling specifications complete
- [ ] Security constraints followed

## Constraints
- Never design for stateful sessions (use stateless JWT)
- Never include sensitive data in JWT payload
- Never ignore token expiration requirements
- Never design without refresh token strategy
- Always use HTTPS for token transmission
- Always define clear authentication boundaries
- Always document token claims thoroughly

## Interaction With Other Skills
- **better-auth-integration:** Implements frontend portion of auth flow
- **jwt-verification:** Implements backend portion of auth flow
- **auth-boundary-design:** Defines authorization after authentication
- **rest-api-design:** Coordinates auth headers with API design
- **frontend-architecture:** Influences frontend auth state management

## Anti-Patterns
- **Stateful creep:** Introducing server-side session state
- **Token bloat:** Including unnecessary data in JWT payload
- **Expiration ignore:** Not planning for token expiration
- **Single token:** Not having refresh token strategy
- **Insecure transmission:** Allowing tokens over HTTP
- **Boundary blur:** Mixing authentication and authorization
- **Flow ambiguity:** Unclear token lifecycle documentation

## Security Best Practices
- Use strong encryption algorithms (RS256, ES256)
- Implement proper token expiration and refresh
- Never store sensitive data in JWT payloads
- Use secure transmission (HTTPS only)
- Implement CSRF protection
- Validate token signatures properly

## Documentation Resources
- [JWT Official Documentation](https://jwt.io/introduction)
- [RFC 7519 - JWT Specification](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JSON Web Algorithms (JWA)](https://tools.ietf.org/html/rfc7518)

## Phase Applicability
Phase II only. Phase I has no authentication requirements.