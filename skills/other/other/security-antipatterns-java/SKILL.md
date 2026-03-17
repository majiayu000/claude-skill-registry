---
name: security-antipatterns-java
description: Use when generating Java code for web applications, APIs, or enterprise systems - prevents OWASP Top 10 vulnerabilities in Spring Boot, Jakarta EE, and core Java
version: "1.0.0"
allowed-tools: "Read"
metadata:
  short-description: Prevents OWASP Top 10 vulnerabilities in Java/Spring applications
---

# Security Anti-Patterns Guard for Java

## Overview

Code generation guard that prevents security vulnerabilities while writing Java web application code. Covers OWASP Top 10 Web (2025), OWASP API Security Top 10 (2023), with CWE references throughout.

**Stack:** Java 11/17/21, Spring Boot, Spring Security, Jakarta EE, Hibernate, JPA

**Java Version Focus:**
- Java 17 (primary target - ~35% usage)
- Java 11 (secondary - ~33% usage)
- Java 21 (latest LTS - growing adoption)

## When to Activate

Activate when generating code that:
- Handles user input (forms, API requests, file uploads)
- Queries databases (JDBC, JPA, Hibernate)
- Performs authentication or authorization
- Manages sessions or JWT tokens
- Processes files or paths
- Serializes/deserializes data (ObjectInputStream, XML, JSON)
- Uses cryptographic operations
- Executes system commands or processes
- Configures Spring Security or Jakarta EE security

## Critical Rules (Top 10)

1. **NEVER** concatenate strings into SQL queries - use `PreparedStatement` or JPA named parameters
2. **NEVER** use `ObjectInputStream.readObject()` on untrusted data - use JSON with validation
3. **NEVER** use `Runtime.exec()` with user input - use `ProcessBuilder` with argument list
4. **NEVER** use `java.util.Random` for security - use `SecureRandom`
5. **NEVER** use MD5/SHA1 for passwords - use BCrypt or Argon2
6. **NEVER** hardcode secrets - use environment variables or secret managers
7. **NEVER** disable CSRF without understanding the risk - keep enabled for browser clients
8. **NEVER** trust user-supplied file paths - normalize and validate with `Path.resolve()` + `startsWith()`
9. **ALWAYS** verify resource ownership (BOLA) - check `userId` before returning data
10. **ALWAYS** validate input at API boundaries - use Bean Validation annotations

## Module Index

| Module | Focus | Key Vulnerabilities |
|--------|-------|---------------------|
| [references/injection.md](references/injection.md) | SQL, Command, LDAP, XPath, JPQL | CWE-89, CWE-78, CWE-90, CWE-643 |
| [references/deserialization.md](references/deserialization.md) | ObjectInputStream, XXE, JSON/YAML | CWE-502, CWE-611 |
| [references/xss-output.md](references/xss-output.md) | XSS, template escaping, JSP/Thymeleaf | CWE-79 |
| [references/auth-access.md](references/auth-access.md) | BOLA, BFLA, sessions, JWT | CWE-862, CWE-863, CWE-287 |
| [references/crypto-secrets.md](references/crypto-secrets.md) | Secrets, hashing, encryption | CWE-798, CWE-327, CWE-916 |
| [references/input-validation.md](references/input-validation.md) | Bean Validation, forms, uploads | CWE-20, CWE-434, CWE-915 |
| [references/file-operations.md](references/file-operations.md) | Path traversal, temp files, NIO | CWE-22, CWE-377 |
| [references/spring-security.md](references/spring-security.md) | CSRF, CORS, method security, actuators | Spring-specific |
| [references/jakarta-ee.md](references/jakarta-ee.md) | Servlet security, EJB, JAX-RS | Jakarta EE-specific |
| [references/dependencies.md](references/dependencies.md) | Maven/Gradle audit, supply chain | CWE-1104, CWE-1357 |
| [references/java-runtime.md](references/java-runtime.md) | Reflection, ReDoS, ScriptEngine | CWE-94, CWE-1333 |

## Quick Decision Tree

```
User input involved?
├─ Database query → See references/injection.md (use PreparedStatement/JPA named params)
├─ File path → See references/file-operations.md (use Path.resolve() + startsWith check)
├─ Command execution → See references/injection.md (ProcessBuilder with list args)
├─ Deserialization → See references/deserialization.md (NEVER ObjectInputStream on untrusted)
├─ Template rendering → See references/xss-output.md (use th:text not th:utext)
└─ API endpoint → See references/auth-access.md + references/input-validation.md

Storing/generating secrets?
├─ API keys → See references/crypto-secrets.md (env vars or Vault)
├─ Passwords → See references/crypto-secrets.md (BCrypt/Argon2)
└─ Tokens → See references/crypto-secrets.md (SecureRandom)

Framework-specific?
├─ Spring Boot → See references/spring-security.md
├─ Jakarta EE → See references/jakarta-ee.md
└─ Core Java → See references/java-runtime.md
```

## How to Use This Skill

1. **During code generation:** Reference relevant module for specific vulnerability patterns
2. **Code review:** Check generated code against patterns in each module
3. **When uncertain:** Default to the more secure option; add explicit comments explaining security decisions

## Sources

- [OWASP Java Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html)
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)
- [SEI CERT Oracle Coding Standard for Java](https://wiki.sei.cmu.edu/confluence/display/java/)
- [Baeldung Security Guides](https://www.baeldung.com/security-spring)
