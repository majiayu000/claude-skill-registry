---
name: spring-boot-security
description: Spring Security 7 implementation for Spring Boot 4. Use when configuring authentication, authorization, OAuth2/JWT resource servers, method security, or CORS/CSRF. Covers the mandatory Lambda DSL migration, SecurityFilterChain patterns, @PreAuthorize, and password encoding. For testing secured endpoints, see spring-boot-testing skill.
---

# Spring Security 7 for Spring Boot 4

Implements authentication and authorization with Spring Security 7's mandatory Lambda DSL.

## Critical Breaking Changes

| Removed API | Replacement | Status |
|-------------|-------------|--------|
| `and()` method | Lambda DSL closures | **Required** |
| `authorizeRequests()` | `authorizeHttpRequests()` | **Required** |
| `antMatchers()` | `requestMatchers()` | **Required** |
| `WebSecurityConfigurerAdapter` | `SecurityFilterChain` bean | **Required** |
| `@EnableGlobalMethodSecurity` | `@EnableMethodSecurity` | **Required** |

## Core Workflow

1. **Create SecurityFilterChain bean** → Configure with Lambda DSL
2. **Define authorization rules** → `authorizeHttpRequests()` with `requestMatchers()`
3. **Configure authentication** → Form login, HTTP Basic, or OAuth2
4. **Add method security** → `@EnableMethodSecurity` + `@PreAuthorize`
5. **Handle CORS/CSRF** → Configure for REST APIs

## Quick Patterns

See [EXAMPLES.md](EXAMPLES.md) for complete working examples including:
- **REST API Security** with JWT/OAuth2 (Java + Kotlin)
- **Form Login with Session Security** and CSRF
- **Method Security** with @PreAuthorize and SpEL
- **CORS Configuration** for cross-origin APIs
- **Password Encoder** (Argon2 for Security 7)

## Spring Boot 4 Specifics

- **Lambda DSL** is mandatory (no `and()` chaining)
- **Argon2** password encoder: `Argon2PasswordEncoder.defaultsForSpring7()`
- **CSRF for SPAs**: `CookieCsrfTokenRepository.withHttpOnlyFalse()`
- **@EnableMethodSecurity** replaces `@EnableGlobalMethodSecurity`

## Detailed References

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Security Configuration**: See [references/SECURITY-CONFIG.md](references/SECURITY-CONFIG.md) for complete SecurityFilterChain patterns
- **Authentication**: See [references/AUTHENTICATION.md](references/AUTHENTICATION.md) for UserDetailsService, password encoding
- **JWT/OAuth2**: See [references/JWT-OAUTH2.md](references/JWT-OAUTH2.md) for resource server, token validation

## Anti-Pattern Checklist

| Anti-Pattern | Fix |
|--------------|-----|
| Using `and()` chaining | Use Lambda DSL closures |
| `antMatchers()` | Replace with `requestMatchers()` |
| `authorizeRequests()` | Replace with `authorizeHttpRequests()` |
| CSRF disabled without JWT | Keep CSRF for session-based auth |
| Hardcoded credentials | Use environment variables or Secret Manager |
| `permitAll()` on sensitive endpoints | Audit all permit rules |
| Missing `authenticated()` default | End with `.anyRequest().authenticated()` |

## Critical Reminders

1. **Lambda DSL is mandatory** — No more `and()` chaining in Security 7
2. **Order matters** — More specific `requestMatchers` before general ones
3. **CSRF for sessions** — Only disable for stateless JWT APIs
4. **Method security needs enabling** — Add `@EnableMethodSecurity`
5. **Test security configuration** — Use `@WithMockUser` and JWT test support (see `spring-boot-testing`)
