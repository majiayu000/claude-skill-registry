---
name: 404-frameworks-quarkus-security
description: Use when you need to design, review, or improve security in Quarkus applications — including Quarkus Security with JWT/OIDC, basic auth, @RolesAllowed / @Authenticated / @PermitAll, SecurityIdentity, permission checks, path-based authorization in configuration, exception mapping for auth failures, and sensitive-data-safe logging. This should trigger for requests such as Add Quarkus security support; Review Quarkus security configuration; Improve API authorization in Quarkus; Add JWT/OIDC security in Quarkus; Harden Quarkus authorization rules. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus Security Guidelines

Apply Quarkus security best practices with secure-by-default API and service boundaries.

**What is covered in this Skill?**

- Quarkus security configuration for authentication mechanisms
- Authorization with @RolesAllowed / @Authenticated / @PermitAll
- Endpoint and resource protection strategy
- Least-privilege role design
- Secure denial/error handling behavior
- Sensitive data protection in logs and responses

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying security changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Quarkus security support
- Review Quarkus security configuration
- Improve API authorization in Quarkus
- Add JWT/OIDC security in Quarkus
- Harden Quarkus authorization rules
- Implement SecurityIdentity checks in Quarkus services

## Workflow

1. **Read reference and assess project context**

Read `references/404-frameworks-quarkus-security.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor security-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/404-frameworks-quarkus-security.md](references/404-frameworks-quarkus-security.md).
