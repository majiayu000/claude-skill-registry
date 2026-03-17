---
name: better-auth-integration
description: "Configure Better Auth on the frontend and coordinate JWT issuance. This skill should be used when setting up Better Auth in Next.js frontend, configuring authentication providers, handling user sessions, and coordinating token issuance for backend API authentication."
---

# Better Auth Integration

## Purpose
Configure Better Auth on the frontend and coordinate JWT issuance. This skill establishes patterns for integrating Better Auth as the authentication provider, handling user sessions, and coordinating token issuance for backend API authentication.

## When to Use
- When setting up Better Auth in Next.js frontend
- When configuring authentication providers (email, OAuth)
- When handling user session management
- When coordinating JWT token issuance
- When implementing login/logout flows
- When troubleshooting authentication issues

## When NOT to Use
- When working on backend JWT verification (use jwt-verification)
- When designing overall auth flow (use jwt-authentication)
- When Better Auth isn't the chosen auth provider
- When working on unauthenticated features
- When the auth provider hasn't been confirmed

## Required Clarifications
1. What authentication providers are needed (email, Google, GitHub, etc.)?
2. What is the Next.js project structure and app router setup?
3. What are the backend API endpoints that require JWT authentication?
4. Are there specific session duration requirements?

## Optional Clarifications
5. Are there specific UI/UX requirements for the authentication flow?
6. Are there existing auth patterns in the codebase to follow?

## Responsibilities
- Configure Better Auth client in Next.js
- Set up authentication providers
- Handle user session state
- Coordinate JWT token issuance and refresh
- Implement secure token storage (httpOnly cookies)
- Configure auth callbacks and redirects
- Handle authentication errors gracefully
- Document auth configuration requirements

## Inputs
- Better Auth documentation and requirements
- Authentication provider configurations
- Next.js App Router structure
- Session management requirements
- JWT token requirements for backend

## Outputs
- Better Auth client configuration
- Auth provider setup
- Session management patterns
- Token issuance configuration
- Login/logout flow documentation
- Error handling patterns

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |

## Implementation Workflow
1. Assess existing auth infrastructure
2. Configure Better Auth client with required providers
3. Set up session management
4. Integrate with backend JWT requirements
5. Test authentication flows
6. Document implementation

## Output Checklist
- [ ] Better Auth client configured correctly
- [ ] Authentication providers set up
- [ ] Secure session management implemented
- [ ] JWT token coordination established
- [ ] Error handling patterns in place
- [ ] Security constraints followed

## Constraints
- Never store tokens in localStorage (use httpOnly cookies)
- Never expose auth secrets in client-side code
- Never skip CSRF protection
- Never ignore token expiration handling
- Always use HTTPS for auth operations
- Always validate redirect URLs
- Always handle auth errors with user-friendly messages

## Interaction With Other Skills
- **jwt-authentication:** Operates within broader auth flow design
- **jwt-verification:** Provides tokens for backend verification
- **nextjs-app-router:** Integrates with App Router patterns
- **auth-aware-ui:** Provides auth state for UI components
- **auth-boundary-design:** Coordinates with frontend auth boundary

## Anti-Patterns
- **Token exposure:** Storing tokens in localStorage or exposing in URLs
- **Secret leakage:** Including auth secrets in client bundles
- **Session confusion:** Inconsistent session state across components
- **Redirect vulnerability:** Not validating redirect URLs
- **Error swallowing:** Hiding auth errors from users
- **CSRF ignorance:** Not implementing CSRF protection
- **Refresh neglect:** Not handling token refresh properly

## Security Best Practices
- Use httpOnly cookies for token storage
- Implement proper CSRF protection
- Validate all redirect URLs
- Handle token refresh securely
- Use HTTPS for all auth operations

## Documentation Resources
- [Better Auth Official Documentation](https://better-auth.com/docs)
- [Next.js Authentication Patterns](https://nextjs.org/docs/app/building-your-application/authentication)
- [JWT Best Practices](https://jwt.io/introduction)

## Phase Applicability
Phase II only. Phase I has no authentication requirements.