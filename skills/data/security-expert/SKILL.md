---
name: security-expert
description: "This skill should be used when the user asks to 'secure my API', 'implement authentication', 'configure Keycloak', 'add authorization', 'fix JWT issues', 'set up OAuth', 'review security', 'security audit', 'pen test prep', 'prevent SQL injection', 'fix XSS', 'CSRF protection', or works with JWT tokens, OAuth 2.0/OIDC flows, Spring Security, ABAC/RBAC policies, CORS, CSRF, XSS prevention, SQL injection, OWASP guidelines, or debugging auth failures in Spring/Keycloak environments."
---

# Security Expert Skill

Expert guidance for API security, authentication, authorization, and identity management.

## Core Competencies

- **Authentication**: JWT, OAuth 2.0, OpenID Connect, SAML, session management
- **Authorization**: RBAC, ABAC, ReBAC, policy engines
- **Identity Providers**: Keycloak, Okta, Auth0, Azure AD
- **Frameworks**: Spring Security, Spring Boot, Jakarta EE Security
- **Web Security**: OWASP Top 10, CSP, CORS, CSRF, XSS prevention
- **Injection Prevention**: SQL injection, parameterized queries, input validation
- **Frontend Security**: React XSS protection, DOMPurify, URL sanitization, CSP for SPAs

## Quick Reference

### JWT Best Practices
- Always validate: signature, expiration (`exp`), issuer (`iss`), audience (`aud`)
- Use RS256/ES256 for distributed systems (asymmetric), HS256 only for single-service
- Keep tokens short-lived (5-15 min access, hours-days refresh)
- Never store sensitive data in JWT payload (it's base64, not encrypted)
- Implement token revocation via blacklist or short expiry + refresh rotation

### Spring Security + Keycloak Integration Pattern
```java
// Minimal resource server config
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated());
        return http.build();
    }
}
```

### ABAC vs RBAC Decision Matrix
| Use RBAC when | Use ABAC when |
|---------------|---------------|
| Simple role hierarchy | Context-dependent access (time, location) |
| Static permissions | Resource-level attributes matter |
| Small number of roles | Complex business rules |
| Audit simplicity needed | Fine-grained, dynamic policies |

## Reference Files

For detailed guidance, consult these references:

- **[references/jwt-security.md](references/jwt-security.md)**: JWT vulnerabilities, attack vectors, secure implementation
- **[references/keycloak.md](references/keycloak.md)**: Keycloak realm setup, client types, mappers, flows
- **[references/spring-security.md](references/spring-security.md)**: Filter chain, method security, OAuth2 client/resource server
- **[references/authorization-patterns.md](references/authorization-patterns.md)**: RBAC, ABAC, ReBAC patterns and policy engines
- **[references/owasp-api-security.md](references/owasp-api-security.md)**: OWASP API Security Top 10 with mitigations
- **[references/security-headers.md](references/security-headers.md)**: HTTP security headers, CSP, CORS configuration
- **[references/injection-prevention.md](references/injection-prevention.md)**: SQL injection prevention, parameterized queries, JPA patterns
- **[references/xss-prevention.md](references/xss-prevention.md)**: React XSS protection, DOMPurify, URL validation, CSP for SPAs
- **[references/csrf-prevention.md](references/csrf-prevention.md)**: CSRF tokens, double submit, SameSite cookies, Spring CSRF

## Workflow: Security Review

1. **Identify attack surface**: Public endpoints, auth flows, data exposure
2. **Check authentication**: Token validation, session handling, credential storage
3. **Check authorization**: Access control at endpoint and resource level
4. **Review data handling**: Input validation, output encoding, sensitive data exposure
5. **Examine configuration**: Security headers, CORS, error handling, logging
6. **Test edge cases**: Token expiry, concurrent sessions, privilege escalation

## Common Security Pitfalls

```
❌ Trusting JWT without signature validation
❌ Storing tokens in localStorage (XSS vulnerable)
❌ Using symmetric keys across services
❌ Missing audience validation
❌ Exposing stack traces in errors
❌ Permissive CORS (Access-Control-Allow-Origin: *)
❌ Missing rate limiting on auth endpoints
❌ Logging sensitive data (tokens, passwords)
❌ String concatenation in SQL queries (injection)
❌ Using innerHTML without sanitization
❌ Allowing javascript: URLs in user-controlled hrefs
❌ Disabling CSRF for cookie-authenticated APIs
❌ GET requests with side effects (CSRF vulnerable)
```

## Debugging Security Issues

For auth failures, check in order:
1. Token format and encoding (is it valid JWT structure?)
2. Signature verification (correct algorithm and key?)
3. Claims validation (exp, iss, aud correct?)
4. Role/scope mapping (Keycloak mappers configured?)
5. Spring Security filter chain (debug with `logging.level.org.springframework.security=DEBUG`)
