---
name: junit-integration
description: Maven integration testing with Failsafe plugin, IT naming conventions, and profile configuration
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# JUnit Integration Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

Integration testing standards for Maven projects using the Failsafe plugin. This skill covers test separation, naming conventions, and profile configuration.

## Prerequisites

This skill applies to Maven projects:
- `maven-surefire-plugin` (unit tests)
- `maven-failsafe-plugin` (integration tests)

## Key Principles

### Test Separation

Integration tests should be completely separated from unit tests to ensure:

* Fast unit test execution during regular development builds
* Isolated integration test execution that can be run independently
* Clear distinction between test types for CI/CD pipelines
* Proper resource management for integration tests requiring external dependencies

### Maven Plugin Usage

* **Maven Surefire Plugin**: Handles unit tests during the `test` phase
* **Maven Failsafe Plugin**: Handles integration tests during the `integration-test` and `verify` phases

## Naming Conventions

Integration tests must follow Maven's standard naming conventions:

* `**/*IT.java` - Integration Test classes
* `**/*ITCase.java` - Alternative integration test naming

```java
// ✅ Correct naming
public class TokenKeycloakIT extends KeycloakITBase {
    // Integration test implementation
}

// ❌ Incorrect naming (would be treated as unit test)
public class TokenKeycloakITTest extends KeycloakITBase {
    // This follows unit test naming convention
}
```

## Maven Configuration

### Base Configuration

Configure surefire plugin to exclude integration tests from normal builds:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <excludes>
            <exclude>**/*IT.java</exclude>
            <exclude>**/*ITCase.java</exclude>
        </excludes>
    </configuration>
</plugin>
```

### Integration Test Profile

Create a dedicated profile for integration tests:

```xml
<profile>
    <id>integration-tests</id>
    <build>
        <plugins>
            <!-- Skip Surefire Plugin (unit tests) when running integration tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <skipTests>true</skipTests>
                </configuration>
            </plugin>
            <!-- Maven Failsafe Plugin for Integration Tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-failsafe-plugin</artifactId>
                <configuration>
                    <includes>
                        <include>**/*IT.java</include>
                        <include>**/*ITCase.java</include>
                    </includes>
                </configuration>
                <executions>
                    <execution>
                        <id>integration-test</id>
                        <goals>
                            <goal>integration-test</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>verify</id>
                        <goals>
                            <goal>verify</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</profile>
```

## Critical Configuration Details

### Why Skip Unit Tests in Integration Profile

**Problem**: Without explicit unit test skipping, the integration-tests profile would run:
1. All unit tests (via surefire)
2. All integration tests (via failsafe)

**Solution**: Configure surefire to skip tests when the integration-tests profile is active.

### Failsafe Goals

Both goals are required for proper integration test execution:

* `integration-test`: Runs the integration tests
* `verify`: Checks the results and fails the build if tests failed

## Maven Commands

### Normal Development Build

```bash
# Runs only unit tests, excludes integration tests
./mvnw clean test

# Full build without integration tests
./mvnw clean verify
```

### Integration Test Execution

```bash
# Run only integration tests (skips unit tests)
./mvnw clean verify -Pintegration-tests

# Run integration tests for specific modules
./mvnw clean verify -Pintegration-tests -pl module1
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Integration Tests
  run: ./mvnw --no-transfer-progress clean verify -Pintegration-tests -pl module1,module2
```

### Build Verification

Ensure both scenarios work correctly:

1. **Normal Build**: Should only run unit tests
2. **Integration Profile**: Should skip unit tests and only run integration tests

## JUnit 5 Nested Tests

Integration tests can use JUnit 5 nested test classes. The naming convention applies to the outer class:

```java
public class TokenKeycloakIT {

    @Nested
    class AccessTokenTests {
        @Test
        void shouldValidateAccessToken() {
            // Test implementation
        }
    }

    @Nested
    class IdTokenTests {
        @Test
        void shouldValidateIdToken() {
            // Test implementation
        }
    }
}
```

## Common Pitfalls

### ❌ Incorrect Naming Convention

```java
// Wrong - will be treated as unit test
public class TokenKeycloakITTest { }
```

### ❌ Missing Surefire Skip Configuration

Without `<skipTests>true</skipTests>` in the integration-tests profile, both unit and integration tests will run.

### ❌ Wrong Maven Goal

```bash
# Wrong - only compiles and runs surefire (unit tests)
mvn clean test -Pintegration-tests

# Correct - runs full lifecycle including failsafe (integration tests)
mvn clean verify -Pintegration-tests
```

### ❌ Missing Failsafe Executions

Without proper `<executions>` configuration, failsafe tests might not run or results might not be verified.

## Verification Checklist

- [ ] Normal build (`mvnw clean test`) excludes integration tests
- [ ] Integration profile (`mvnw clean verify -Pintegration-tests`) skips unit tests
- [ ] Integration profile successfully runs integration tests
- [ ] CI/CD workflow includes integration test execution
- [ ] Integration test naming follows Maven conventions
- [ ] Both surefire exclusions and failsafe inclusions are properly configured

## Related Skills

- `pm-dev-java:junit-core` - JUnit 5 core patterns
- `pm-dev-java:java-cdi-quarkus` - Quarkus-specific testing
- `pm-dev-builder:builder-maven-rules` - Maven build standards

## Additional Resources

* [Maven Surefire Plugin Documentation](https://maven.apache.org/surefire/maven-surefire-plugin/)
* [Maven Failsafe Plugin Documentation](https://maven.apache.org/surefire/maven-failsafe-plugin/)
* [Maven Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)
