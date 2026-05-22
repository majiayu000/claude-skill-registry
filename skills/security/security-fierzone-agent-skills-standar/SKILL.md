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

- **Lambda DSL**: ALWAYS use Lambda DSL (`.authorizeHttpRequests(auth -> ...)`) for readability.
- **SecurityFilterChain**: Expose as `@Bean`. Do not extend `WebSecurityConfigurerAdapter`.
- **Statelessness**: Enforce `SessionCreationPolicy.STATELESS` for REST APIs.

### JWT Best Practices

- **Algorithm**: Enforce `RS256` or `HS256`. **Reject `none` algorithm** explicitly in JWT configuration.
- **Claims**: Validate `iss`, `aud`, and `exp` claims.
- **Tokens**: Short-lived access tokens (15m), secure refresh tokens.

### Hardening

- **CSRF**: Disable for stateless APIs. Enable + Cookie for Browser Apps.
- **CORS**: Explain allowed origins. NEVER use `*` with credentials.
- **Headers**: Enable default headers (HSTS, Content-Type-Options).

### Authorization

- **Method Security**: Use `@EnableMethodSecurity`.
- **Annotations**: Prefer `@PreAuthorize` over URL matching.

## Anti-Patterns

- **Adapter Extension**: `**No Adapter**: Use SecurityFilterChain bean.`
- **Chained Calls**: `**No .and()**: Use Lambda DSL.`
- **Hardcoded Secrets**: `**No Secrets**: Use Vault/Env.`
- **Legacy Matchers**: `**No antMatchers**: Use requestMatchers.`

## References

- [Implementation Examples](references/implementation.md)

## Related Topics

common/security-standards | architecture
