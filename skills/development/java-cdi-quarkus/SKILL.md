---
name: java-cdi-quarkus
description: Quarkus-specific CDI patterns including @QuarkusTest, native image support, and reflection registration
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# Java CDI Quarkus Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

Quarkus-specific CDI standards extending core CDI patterns with Quarkus testing, native image support, and GraalVM reflection configuration.

## Prerequisites

This skill applies to Quarkus projects:
- `io.quarkus:quarkus-junit5` (Quarkus testing)
- `io.quarkus:quarkus-jacoco` (coverage)

## Workflow

### Step 1: Load Quarkus Testing Standards

**CRITICAL**: Load this standard for any Quarkus testing work.

```
Read: standards/quarkus-testing.md
```

This provides foundational rules for:
- @QuarkusTest and @QuarkusIntegrationTest
- JaCoCo configuration for Quarkus
- REST Assured patterns

### Step 2: Load Additional Standards (As Needed)

**External Integration Testing** (load for Docker-based IT):
```
Read: standards/integration-testing.md
```

Use when: Configuring external API integration tests with Docker containers. For basic Maven Failsafe setup, see `pm-dev-java:junit-integration`.

**Native Image** (load for GraalVM work):
```
Read: standards/quarkus-native.md
```

Use when: Building native images or troubleshooting native compilation.

**Reflection Registration** (load for native issues):
```
Read: standards/quarkus-reflection.md
```

Use when: Resolving reflection issues in native builds.

**Container Standards** (load for Docker deployment):
```
Read: standards/container.md
```

Use when: Configuring container images, Docker Compose, health checks, or certificate management.

**Security Standards** (load for security work):
```
Read: standards/security.md
```

Use when: Implementing OWASP-compliant security, secure logging, or runtime security configuration.

## Key Rules Summary

### @QuarkusTest Setup
```java
@QuarkusTest
class TokenValidatorTest {

    @Inject
    TokenValidator validator;

    @Test
    @DisplayName("Should validate valid token")
    void shouldValidateValidToken() {
        ValidationResult result = validator.validate(validToken);
        assertTrue(result.isValid());
    }
}
```

### REST Assured Testing
```java
@QuarkusTest
class UserResourceTest {

    @Test
    void shouldReturnUsers() {
        given()
            .when().get("/api/users")
            .then()
            .statusCode(200)
            .body("$.size()", greaterThan(0));
    }
}
```

### JaCoCo Dependencies
```xml
<!-- Required for Quarkus test coverage -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-jacoco</artifactId>
    <scope>test</scope>
</dependency>
```

### Native Image Build
```bash
# Build native image
mvn package -Pnative

# Run native integration tests
mvn verify -Pnative -Dquarkus.test.native-image-profile=native
```

## Related Skills

- `pm-dev-java:java-cdi` - Core CDI patterns
- `pm-dev-java:junit-integration` - Maven integration testing
- `pm-dev-java:junit-core` - JUnit 5 core patterns

## Standards Reference

| Standard | Purpose |
|----------|---------|
| quarkus-testing.md | @QuarkusTest, JaCoCo, REST Assured |
| integration-testing.md | External API testing with Docker (extends junit-integration) |
| quarkus-native.md | GraalVM native image builds |
| quarkus-reflection.md | Reflection registration for native |
| container.md | Docker deployment, health checks, certificate management |
| security.md | OWASP security, secure logging, runtime security |
