---
name: 304-frameworks-spring-boot-security
description: Use when you need to design, review, or improve security in Spring Boot applications — including SecurityFilterChain, OAuth2/JWT resource server patterns, form login basics, method security (@PreAuthorize), CSRF and CORS for APIs, session fixation, security headers, exception handling, password encoding, and sensitive-data-safe logging. This should trigger for requests such as Add Spring Boot security support; Review Spring Boot security configuration; Improve API authorization in Spring Boot; Add JWT resource server security in Spring Boot; Harden Spring Boot security headers and CSRF settings. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot Security Guidelines

Apply Spring Boot security best practices with secure-by-default API boundaries.

**What is covered in this Skill?**

- Spring Security configuration and SecurityFilterChain setup
- Authentication and authorization policies for endpoints
- Method-level security (@PreAuthorize / @Secured)
- Principle of least privilege for roles and scopes
- Secure error handling and denial responses
- Sensitive data handling in logs and responses

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying security changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Spring Boot security support
- Review Spring Boot security configuration
- Improve API authorization in Spring Boot
- Add JWT resource server security in Spring Boot
- Harden Spring Boot security headers and CSRF settings
- Implement method security with @PreAuthorize in Spring Boot

## Workflow

1. **Read reference and assess project context**

Read `references/304-frameworks-spring-boot-security.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor security-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/304-frameworks-spring-boot-security.md](references/304-frameworks-spring-boot-security.md).
