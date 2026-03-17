---
name: api-jwt-authenticator
category: Security
author: Claude
version: 1.0.0
tags: [fastapi, jwt, authentication, security, api]
description: A conceptual skill for securing FastAPI REST APIs with JWT authentication
---

# API JWT Authenticator Skill

## When to Use This Skill

Use this conceptual skill when you need to implement secure JWT-based authentication for FastAPI REST APIs. This skill is appropriate for:

- Protecting API endpoints that require user authentication
- Enforcing user-specific access control (ensuring users can only access their own resources)
- Implementing stateless authentication in microservices
- Securing REST APIs with standard JWT token validation
- Adding role-based access control (RBAC) to API endpoints

This skill should NOT be used for:
- Public APIs that don't require authentication
- APIs that use alternative authentication methods (OAuth, API keys, etc.)
- Simple applications where basic auth is sufficient

## Prerequisites

- Understanding of JWT (JSON Web Token) concepts
- FastAPI application framework knowledge
- Basic security principles and authentication patterns
- Environment for managing secret keys securely

## Conceptual Implementation Framework

### JWT Token Extraction Capability
- Extract JWT tokens from the Authorization header in the format "Bearer <token>"
- Handle malformed or missing authorization headers appropriately
- Validate the presence of the "Bearer" prefix in the header

### Token Validation Capability
- Validate JWT tokens using a shared secret key
- Verify token signature to ensure integrity
- Check token expiration (exp) claim to prevent usage of expired tokens
- Validate token issuer (iss) and audience (aud) claims when applicable

### User Identity Verification Capability
- Extract user identity information from the token payload
- Compare the user ID in the token with the requested resource
- Enforce access control rules based on user identity
- Ensure users can only access resources belonging to them

### Error Handling Capability
- Generate appropriate HTTP 401 Unauthorized responses for invalid tokens
- Generate HTTP 403 Forbidden responses for insufficient permissions
- Provide clear error messages without exposing sensitive information
- Log authentication failures for security monitoring

## Expected Input/Output

### Input Requirements:

1. **JWT Token Format**:
   - Token must be in the `Authorization` header as `Bearer <token>`
   - Token must contain valid JWT structure with required claims
   - Token must not be expired

2. **Token Claims**:
   - `sub` (subject): User identifier
   - `exp` (expiration): Token expiration timestamp
   - `user_id` (optional): Unique user identifier for access control
   - `role` (optional): User role for role-based access control

### Output Formats:

1. **Successful Authentication Response**:
   - HTTP 200 OK for protected endpoints
   - Response body with authenticated user information
   - Properly authenticated user context for downstream processing

2. **401 Unauthorized Response** (Invalid/Expired Token):
   - HTTP 401 status code
   - Error message: "Could not validate credentials"
   - Appropriate WWW-Authenticate header

3. **403 Forbidden Response** (Insufficient Permissions):
   - HTTP 403 status code
   - Error message: "Access forbidden: Insufficient permissions"
   - Clear indication of permission issue

4. **Token Generation Response** (when applicable):
   - HTTP 200 OK
   - Response body containing access token and token type
   - Secure token delivery mechanism

## Security Considerations

1. **Token Transmission**: Always use HTTPS in production to prevent token interception
2. **Token Storage**: Store secret keys securely in environment variables or secure vaults
3. **Token Expiration**: Set appropriate expiration times to limit exposure windows
4. **Token Validation**: Always validate token signature and claims before trusting
5. **Information Disclosure**: Avoid exposing sensitive information in error messages
6. **Rate Limiting**: Implement rate limiting to prevent brute force attacks
7. **Logging**: Log authentication events for security monitoring without storing tokens

## Integration Patterns

### Dependency Injection Pattern
- Use FastAPI's dependency system to inject authentication requirements
- Apply authentication dependencies to specific routes or entire routers
- Combine multiple authentication requirements as needed

### Middleware Integration
- Implement authentication as middleware for global application
- Handle authentication at the application level
- Centralize authentication logic for consistent enforcement

### Role-Based Access Control (RBAC)
- Define roles and permissions in token claims
- Implement role verification in authentication dependencies
- Enforce role-based access to specific endpoints

## Testing Considerations

- Test authentication failure scenarios (invalid tokens, expired tokens)
- Verify user-specific access control rules
- Test role-based access restrictions
- Validate error response formats and status codes
- Test token refresh mechanisms (if implemented)

## Performance Implications

- JWT validation has minimal computational overhead
- Consider token caching strategies for high-traffic applications
- Balance token expiration time with performance requirements
- Monitor authentication-related latency in production