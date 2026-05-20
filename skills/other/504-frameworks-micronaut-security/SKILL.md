---
name: 504-frameworks-micronaut-security
description: Use when you need to design, review, or improve security in Micronaut applications — including micronaut-security authentication, @Secured and intercept-url-map rules, JWT/session strategies, SecurityService checks, CORS, CSRF awareness for browser apps, rejection handlers, and sensitive-data-safe logging. This should trigger for requests such as Add Micronaut security support; Review Micronaut security configuration; Improve API authorization in Micronaut; Add JWT security in Micronaut; Harden Micronaut route authorization rules. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut Security Guidelines

Apply Micronaut security best practices with secure-by-default API boundaries.

**What is covered in this Skill?**

- Micronaut security configuration and authentication setup
- Authorization with @Secured and role-based policies
- Endpoint and route protection strategy
- Least-privilege design and policy boundaries
- Secure error/denial behavior
- Sensitive data handling in logs and responses

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying security changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Micronaut security support
- Review Micronaut security configuration
- Improve API authorization in Micronaut
- Add JWT security in Micronaut
- Harden Micronaut route authorization rules
- Implement @Secured policies in Micronaut controllers

## Workflow

1. **Read reference and assess project context**

Read `references/504-frameworks-micronaut-security.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor security-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/504-frameworks-micronaut-security.md](references/504-frameworks-micronaut-security.md).
