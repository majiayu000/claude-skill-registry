---
name: spring-boot-security-jwt
description: Provides JWT authentication and authorization patterns for Spring Boot 3.5.x covering token generation with JJWT, Bearer/cookie authentication, database/OAuth2 integration, and RBAC/permission-based access control using Spring Security 6.x. Use when implementing authentication or authorization in Spring Boot applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring Boot JWT Security

JWT authentication and authorization patterns for Spring Boot 3.5.x using Spring Security 6.x and JJWT. Covers token generation, validation, refresh strategies, RBAC/ABAC, and OAuth2 integration.

## Overview

This skill provides implementation patterns for stateless JWT authentication in Spring Boot applications. It covers the complete authentication flow including token generation with JJWT 0.12.6, Bearer/cookie-based authentication, refresh token rotation, and method-level authorization with `@PreAuthorize` expressions.

Key capabilities:
- Access and refresh token generation with configurable expiration
- Bearer token and HttpOnly cookie authentication strategies
- Integration with Spring Data JPA and OAuth2 providers
- RBAC with role/permission-based `@PreAuthorize` rules
- Token revocation and blacklisting for logout/rotation

## When to Use

Activate when user requests involve:
- "Implement JWT authentication", "secure REST API with tokens"
- "Spring Security 6.x configuration", "SecurityFilterChain setup"
- "Role-based access control", "RBAC", `` `@PreAuthorize` ``
- "Refresh token", "token rotation", "token revocation"
- "OAuth2 integration", "social login", "Google/GitHub auth"
- "Stateless authentication", "SPA backend security"
- "JWT filter", "OncePerRequestFilter", "Bearer token"
- "Cookie-based JWT", "HttpOnly cookie"
- "Permission-based access control", "custom PermissionEvaluator"

## Quick Reference

### Dependencies (JJWT 0.12.6)

| Artifact | Scope |
|----------|-------|
| `spring-boot-starter-security` | compile |
| `spring-boot-starter-oauth2-resource-server` | compile |
| `io.jsonwebtoken:jjwt-api:0.12.6` | compile |
| `io.jsonwebtoken:jjwt-impl:0.12.6` | runtime |
| `io.jsonwebtoken:jjwt-jackson:0.12.6` | runtime |
| `spring-security-test` | test |

See [references/jwt-quick-reference.md](references/jwt-quick-reference.md) for Maven and Gradle snippets.

### Key Configuration Properties

| Property | Example Value | Notes |
|----------|--------------|-------|
| `jwt.secret` | `${JWT_SECRET}` | Min 256 bits, never hardcode |
| `jwt.access-token-expiration` | `900000` | 15 min in milliseconds |
| `jwt.refresh-token-expiration` | `604800000` | 7 days in milliseconds |
| `jwt.issuer` | `my-app` | Validated on every token |
| `jwt.cookie-name` | `jwt-token` | For cookie-based auth |
| `jwt.cookie-http-only` | `true` | Always true in production |
| `jwt.cookie-secure` | `true` | Always true with HTTPS |

### Authorization Annotations

| Annotation | Example |
|-----------|---------|
| `@PreAuthorize("hasRole('ADMIN')")` | Role check |
| `@PreAuthorize("hasAuthority('USER_READ')")` | Permission check |
| `@PreAuthorize("hasPermission(#id, 'Doc', 'READ')")` | Domain object check |
| `@PreAuthorize("@myService.canAccess(#id)")` | Spring bean check |

## Instructions

### Step 1 — Add Dependencies

Include `spring-boot-starter-security`, `spring-boot-starter-oauth2-resource-server`, and the three JJWT artifacts in your build file. See [references/jwt-quick-reference.md](references/jwt-quick-reference.md) for exact Maven/Gradle snippets.

### Step 2 — Configure application.yml

```yaml
jwt:
  secret: ${JWT_SECRET:change-me-min-32-chars-in-production}
  access-token-expiration: 900000
  refresh-token-expiration: 604800000
  issuer: my-app
  cookie-name: jwt-token
  cookie-http-only: true
  cookie-secure: false   # true in production
```

See [references/jwt-complete-configuration.md](references/jwt-complete-configuration.md) for the full properties reference.

### Step 3 — Implement JwtService

Core operations: generate access token, generate refresh token, extract username, validate token.

```java
@Service
public class JwtService {

    public String generateAccessToken(UserDetails userDetails) {
        return Jwts.builder()
            .subject(userDetails.getUsername())
            .issuer(issuer)
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + accessTokenExpiration))
            .claim("authorities", getAuthorities(userDetails))
            .signWith(getSigningKey())
            .compact();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        try {
            String username = extractUsername(token);
            return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
        } catch (JwtException e) {
            return false;
        }
    }
}
```

See [references/jwt-complete-configuration.md](references/jwt-complete-configuration.md) for the complete JwtService including key management and claim extraction.

### Step 4 — Create JwtAuthenticationFilter

Extend `OncePerRequestFilter` to extract a JWT from the `Authorization: Bearer` header (or HttpOnly cookie), validate it, and set the `SecurityContext`.

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            chain.doFilter(request, response);
            return;
        }
        String jwt = authHeader.substring(7);
        String username = jwtService.extractUsername(jwt);
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);
            if (jwtService.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        chain.doFilter(request, response);
    }
}
```

See [references/configuration.md](references/configuration.md) for the cookie-based variant.

### Step 5 — Configure SecurityFilterChain

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/swagger-ui/**").permitAll()
                .anyRequest().authenticated()
            )
            .authenticationProvider(authenticationProvider)
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

See [references/jwt-complete-configuration.md](references/jwt-complete-configuration.md) for CORS, logout handler, and OAuth2 login integration.

### Step 6 — Create Authentication Endpoints

Expose `/register`, `/authenticate`, `/refresh`, and `/logout` via `@RestController`. Return `accessToken` + `refreshToken` in the response body (and optionally set an HttpOnly cookie).

See [references/examples.md](references/examples.md) for the complete `AuthenticationController` and `AuthenticationService`.

### Step 7 — Implement Refresh Token Strategy

Store refresh tokens in the database with `user_id`, `expiry_date`, `revoked`, and `expired` columns. On `/refresh`, verify the stored token, revoke it, and issue a new pair (token rotation).

See [references/token-management.md](references/token-management.md) for `RefreshToken` entity, rotation logic, and Redis-based blacklisting.

### Step 8 — Add Authorization Rules

Use `@EnableMethodSecurity` and `@PreAuthorize` annotations for fine-grained control:

```java
@PreAuthorize("hasRole('ADMIN')")
public Page<UserResponse> getAllUsers(Pageable pageable) { ... }

@PreAuthorize("hasPermission(#documentId, 'Document', 'READ')")
public Document getDocument(Long documentId) { ... }
```

See [references/authorization-patterns.md](references/authorization-patterns.md) for RBAC entity model, `PermissionEvaluator`, and ABAC patterns.

### Step 9 — Write Security Tests

```java
@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {

    @Test
    void shouldDenyAccessWithoutToken() throws Exception {
        mockMvc.perform(get("/api/orders"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldAllowAdminAccess() throws Exception {
        mockMvc.perform(get("/api/admin/users"))
            .andExpect(status().isOk());
    }
}
```

See [references/testing.md](references/testing.md) and [references/jwt-testing-guide.md](references/jwt-testing-guide.md) for full test suites, Testcontainers setup, and a security test checklist.

## Best Practices

### Token Security
- Use minimum 256-bit secret keys — load from environment variables, never hardcode
- Set short access token lifetimes (15 min); use refresh tokens for longer sessions
- Implement token rotation: revoke old refresh token when issuing a new one
- Use `jti` (JWT ID) claim for blacklisting on logout

### Cookie vs Bearer Header
- Prefer HttpOnly cookies for browser clients (XSS-safe)
- Use `Authorization: Bearer` header for mobile/API clients
- Set `Secure`, `SameSite=Lax` or `Strict` on cookies in production

### Spring Security 6.x
- Use `SecurityFilterChain` bean — never extend `WebSecurityConfigurerAdapter`
- Disable CSRF only for stateless APIs; keep it enabled for session-based flows
- Use `@EnableMethodSecurity` instead of deprecated `@EnableGlobalMethodSecurity`
- Validate `iss` and `aud` claims; reject tokens from untrusted issuers

### Performance
- Cache `UserDetails` with `@Cacheable` to avoid DB lookup on every request
- Cache signing key derivation (avoid re-computing HMAC key per request)
- Use Redis for refresh token storage at scale

### What NOT to Do
- Do not store sensitive data (passwords, PII) in JWT claims — claims are only signed, not encrypted
- Do not issue tokens with infinite lifetime
- Do not accept tokens without validating signature and expiration
- Do not share signing keys across environments

## Examples

### Basic Authentication Flow

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/authenticate")
    public ResponseEntity<AuthResponse> authenticate(
            @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.authenticate(request));
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refresh(@RequestBody RefreshRequest request) {
        return ResponseEntity.ok(authService.refreshToken(request.refreshToken()));
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout() {
        authService.logout();
        return ResponseEntity.ok().build();
    }
}
```

### JWT Authorization on Controller Method

```java
@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {

    @GetMapping("/users")
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        return ResponseEntity.ok(adminService.getAllUsers());
    }
}
```

See [references/examples.md](references/examples.md) for complete entity models and service implementations.

## References

| File | Content |
|------|---------|
| [references/jwt-quick-reference.md](references/jwt-quick-reference.md) | Dependencies, minimal service, common patterns |
| [references/jwt-complete-configuration.md](references/jwt-complete-configuration.md) | Full config: properties, SecurityFilterChain, JwtService, OAuth2 RS |
| [references/configuration.md](references/configuration.md) | JWT config beans, CORS, CSRF, error handling, session options |
| [references/examples.md](references/examples.md) | Complete application setup: controllers, services, entities |
| [references/authorization-patterns.md](references/authorization-patterns.md) | RBAC/ABAC entity model, PermissionEvaluator, SpEL expressions |
| [references/token-management.md](references/token-management.md) | Refresh token entity, rotation, blacklisting with Redis |
| [references/testing.md](references/testing.md) | Unit and MockMvc tests, test utilities |
| [references/jwt-testing-guide.md](references/jwt-testing-guide.md) | Testcontainers, load testing, security test checklist |
| [references/security-hardening.md](references/security-hardening.md) | Security headers, HSTS, rate limiting, audit logging |
| [references/performance-optimization.md](references/performance-optimization.md) | Caffeine cache config, async validation, connection pooling |
| [references/oauth2-integration.md](references/oauth2-integration.md) | Google/GitHub OAuth2 login, OAuth2UserService |
| [references/microservices-security.md](references/microservices-security.md) | Inter-service JWT propagation, resource server config |
| [references/migration-spring-security-6x.md](references/migration-spring-security-6x.md) | Migration from Spring Security 5.x |
| [references/troubleshooting.md](references/troubleshooting.md) | Common errors, debugging tips |

## Constraints and Warnings

### Security Constraints
- JWT tokens are signed but not encrypted — do not include sensitive data in claims
- Always validate `exp`, `iss`, and `aud` claims before trusting the token
- Signing keys must be at least 256 bits; never use weak keys in production
- Load secrets from environment variables or secure vaults, never from config files
- SameSite cookie attribute is essential for CSRF protection in cookie-based flows

### Spring Security 6.x Constraints
- `WebSecurityConfigurerAdapter` is removed — use `SecurityFilterChain` beans only
- `@EnableGlobalMethodSecurity` is deprecated — use `@EnableMethodSecurity`
- Lambda DSL is required for `HttpSecurity` configuration (no method chaining)
- `WebSecurityConfigurerAdapter.order()` replaced by `@Order` on `@Configuration` classes

### Token Constraints
- Access tokens should expire in 5-15 minutes for security
- Refresh tokens should be stored server-side (DB or Redis), never in localStorage
- Implement token blacklisting for immediate revocation on logout
- `jti` claim is required for token blacklisting to work correctly

## Related Skills

- `spring-boot-dependency-injection` — Constructor injection patterns used throughout
- `spring-boot-rest-api-standards` — REST API security patterns and error handling
- `unit-test-security-authorization` — Testing Spring Security configurations
- `spring-data-jpa` — User entity and repository patterns
- `spring-boot-actuator` — Security monitoring and health endpoints
