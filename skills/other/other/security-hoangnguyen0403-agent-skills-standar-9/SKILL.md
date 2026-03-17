---
name: Spring Boot Security
description: Spring Security 6+ standards, Lambda DSL, and Hardening
metadata:
  labels: [spring-boot, security, oauth2, jwt]
  triggers:
    files: ['**/*SecurityConfig.java', '**/*Filter.java']
    keywords: [security-filter-chain, lambda-dsl, csrf, cors]
---

# Spring Boot Security Standards

## **Priority: P0 (CRITICAL)**

## Implementation Guidelines

### Configuration (Spring Security 6+)

- **Lambda DSL**: ALWAYS use Lambda DSL.
- **SecurityFilterChain**: Expose as `@Bean`. Do not extend `WebSecurityConfigurerAdapter`.
- **Statelessness**: Enforce `SessionCreationPolicy.STATELESS` for REST APIs.

#### Golden Snippet

See [Security Configuration](references/implementation.md) for full `SecurityFilterChain` example.

### Authentication vs Authorization

- **Authentication**: Validation of credentials (Who are you?). Use `AuthenticationManager` or `JwtDecoder`.
- **Authorization**: Verification of access rights (Can you do this?). Use `@PreAuthorize`.

### JWT Best Practices

- **Algorithm**: Enforce `RS256` or `HS256`. **Reject `none` algorithm**.
- **Claims**: Validate `iss`, `aud`, and `exp`.
- **Tokens**: Short-lived access tokens (15m), secure refresh tokens (httpOnly cookie).

### Hardening Checklist

- [ ] **CSRF**: Disabled for pure APIs? Enabled + Cookie for Browser Apps?
- [ ] **CORS**: Specific origins permitted? No `*` with credentials?
- [ ] **Headers**: HSTS, Content-Type-Options, X-Frame-Options enabled?
- [ ] **Secrets**: No hardcoded keys? Loaded from Vault/Env?
- [ ] **Rate Limiting**: Applied on login/expensive endpoints?
- [ ] **Dependencies**: Scanned for CVEs?

## Anti-Patterns

- **Adapter Extension**: `**No Adapter**: Use SecurityFilterChain bean.`
- **Chained Calls**: `**No .and()**: Use Lambda DSL.`
- **Hardcoded Secrets**: `**No Secrets**: Use Vault/Env.`
- **Legacy Matchers**: `**No antMatchers**: Use requestMatchers.`

## References

- [Implementation Examples](references/implementation.md)

## Related Topics

common/security-standards | architecture
