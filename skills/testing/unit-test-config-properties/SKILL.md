---
name: unit-test-config-properties
description: Unit tests for @ConfigurationProperties classes with @ConfigurationPropertiesTest. Use when validating application configuration binding and validation.
category: testing
tags: [junit-5, configuration-properties, spring-profiles, property-binding]
version: 1.0.1
---

# Unit Testing Configuration Properties and Profiles

Test @ConfigurationProperties bindings, environment-specific configurations, and property validation using JUnit 5. Verify configuration loading without full Spring context startup.

## When to Use This Skill

Use this skill when:
- Testing @ConfigurationProperties property binding
- Testing property name mapping and type conversions
- Verifying configuration validation
- Testing environment-specific configurations
- Testing nested property structures
- Want fast configuration tests without Spring context

## Setup: Configuration Testing

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-configuration-processor</artifactId>
  <scope>provided</scope>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
  testImplementation("org.springframework.boot:spring-boot-starter-test")
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Testing ConfigurationProperties

### Simple Property Binding

```java
// Configuration properties class
@ConfigurationProperties(prefix = "app.security")
@Data
public class SecurityProperties {
  private String jwtSecret;
  private long jwtExpirationMs;
  private int maxLoginAttempts;
  private boolean enableTwoFactor;
}

// Unit test
import org.junit.jupiter.api.Test;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import static org.assertj.core.api.Assertions.*;

class SecurityPropertiesTest {

  @Test
  void shouldBindPropertiesFromEnvironment() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.security.jwtSecret=my-secret-key",
        "app.security.jwtExpirationMs=3600000",
        "app.security.maxLoginAttempts=5",
        "app.security.enableTwoFactor=true"
      )
      .withBean(SecurityProperties.class)
      .run(context -> {
        SecurityProperties props = context.getBean(SecurityProperties.class);

        assertThat(props.getJwtSecret()).isEqualTo("my-secret-key");
        assertThat(props.getJwtExpirationMs()).isEqualTo(3600000L);
        assertThat(props.getMaxLoginAttempts()).isEqualTo(5);
        assertThat(props.isEnableTwoFactor()).isTrue();
      });
  }

  @Test
  void shouldUseDefaultValuesWhenPropertiesNotProvided() {
    new ApplicationContextRunner()
      .withPropertyValues("app.security.jwtSecret=key")
      .withBean(SecurityProperties.class)
      .run(context -> {
        SecurityProperties props = context.getBean(SecurityProperties.class);

        assertThat(props.getJwtSecret()).isEqualTo("key");
        assertThat(props.getMaxLoginAttempts()).isZero();
      });
  }
}
```

## Testing Nested Configuration Properties

### Complex Property Structure

```java
@ConfigurationProperties(prefix = "app.database")
@Data
public class DatabaseProperties {
  private String url;
  private String username;
  private Pool pool = new Pool();
  private List<Replica> replicas = new ArrayList<>();

  @Data
  public static class Pool {
    private int maxSize = 10;
    private int minIdle = 5;
    private long connectionTimeout = 30000;
  }

  @Data
  public static class Replica {
    private String name;
    private String url;
    private int priority;
  }
}

class NestedPropertiesTest {

  @Test
  void shouldBindNestedProperties() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.database.url=jdbc:mysql://localhost/db",
        "app.database.username=admin",
        "app.database.pool.maxSize=20",
        "app.database.pool.minIdle=10",
        "app.database.pool.connectionTimeout=60000"
      )
      .withBean(DatabaseProperties.class)
      .run(context -> {
        DatabaseProperties props = context.getBean(DatabaseProperties.class);

        assertThat(props.getUrl()).isEqualTo("jdbc:mysql://localhost/db");
        assertThat(props.getPool().getMaxSize()).isEqualTo(20);
        assertThat(props.getPool().getConnectionTimeout()).isEqualTo(60000L);
      });
  }

  @Test
  void shouldBindListOfReplicas() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.database.replicas[0].name=replica-1",
        "app.database.replicas[0].url=jdbc:mysql://replica1/db",
        "app.database.replicas[0].priority=1",
        "app.database.replicas[1].name=replica-2",
        "app.database.replicas[1].url=jdbc:mysql://replica2/db",
        "app.database.replicas[1].priority=2"
      )
      .withBean(DatabaseProperties.class)
      .run(context -> {
        DatabaseProperties props = context.getBean(DatabaseProperties.class);

        assertThat(props.getReplicas()).hasSize(2);
        assertThat(props.getReplicas().get(0).getName()).isEqualTo("replica-1");
        assertThat(props.getReplicas().get(1).getPriority()).isEqualTo(2);
      });
  }
}
```

## Testing Property Validation

### Validate Configuration with Constraints

```java
@ConfigurationProperties(prefix = "app.server")
@Data
@Validated
public class ServerProperties {
  @NotBlank
  private String host;

  @Min(1)
  @Max(65535)
  private int port = 8080;

  @Positive
  private int threadPoolSize;

  @Email
  private String adminEmail;
}

class ConfigurationValidationTest {

  @Test
  void shouldFailValidationWhenHostIsBlank() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.server.host=",
        "app.server.port=8080",
        "app.server.threadPoolSize=10"
      )
      .withBean(ServerProperties.class)
      .run(context -> {
        assertThat(context).hasFailed()
          .getFailure()
          .hasMessageContaining("host");
      });
  }

  @Test
  void shouldFailValidationWhenPortOutOfRange() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.server.host=localhost",
        "app.server.port=99999",
        "app.server.threadPoolSize=10"
      )
      .withBean(ServerProperties.class)
      .run(context -> {
        assertThat(context).hasFailed();
      });
  }

  @Test
  void shouldPassValidationWithValidConfiguration() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.server.host=localhost",
        "app.server.port=8080",
        "app.server.threadPoolSize=10",
        "app.server.adminEmail=admin@example.com"
      )
      .withBean(ServerProperties.class)
      .run(context -> {
        assertThat(context).hasNotFailed();
        ServerProperties props = context.getBean(ServerProperties.class);
        assertThat(props.getHost()).isEqualTo("localhost");
      });
  }
}
```

## Testing Profile-Specific Configurations

### Environment-Specific Properties

```java
@Configuration
@Profile("prod")
class ProductionConfiguration {
  @Bean
  public SecurityProperties securityProperties() {
    SecurityProperties props = new SecurityProperties();
    props.setEnableTwoFactor(true);
    props.setMaxLoginAttempts(3);
    return props;
  }
}

@Configuration
@Profile("dev")
class DevelopmentConfiguration {
  @Bean
  public SecurityProperties securityProperties() {
    SecurityProperties props = new SecurityProperties();
    props.setEnableTwoFactor(false);
    props.setMaxLoginAttempts(999);
    return props;
  }
}

class ProfileBasedConfigurationTest {

  @Test
  void shouldLoadProductionConfiguration() {
    new ApplicationContextRunner()
      .withPropertyValues("spring.profiles.active=prod")
      .withUserConfiguration(ProductionConfiguration.class)
      .run(context -> {
        SecurityProperties props = context.getBean(SecurityProperties.class);

        assertThat(props.isEnableTwoFactor()).isTrue();
        assertThat(props.getMaxLoginAttempts()).isEqualTo(3);
      });
  }

  @Test
  void shouldLoadDevelopmentConfiguration() {
    new ApplicationContextRunner()
      .withPropertyValues("spring.profiles.active=dev")
      .withUserConfiguration(DevelopmentConfiguration.class)
      .run(context -> {
        SecurityProperties props = context.getBean(SecurityProperties.class);

        assertThat(props.isEnableTwoFactor()).isFalse();
        assertThat(props.getMaxLoginAttempts()).isEqualTo(999);
      });
  }
}
```

## Testing Type Conversion

### Property Type Binding

```java
@ConfigurationProperties(prefix = "app.features")
@Data
public class FeatureProperties {
  private Duration cacheExpiry = Duration.ofMinutes(10);
  private DataSize maxUploadSize = DataSize.ofMegabytes(100);
  private List<String> enabledFeatures;
  private Map<String, String> featureFlags;
  private Charset fileEncoding = StandardCharsets.UTF_8;
}

class TypeConversionTest {

  @Test
  void shouldConvertStringToDuration() {
    new ApplicationContextRunner()
      .withPropertyValues("app.features.cacheExpiry=30s")
      .withBean(FeatureProperties.class)
      .run(context -> {
        FeatureProperties props = context.getBean(FeatureProperties.class);

        assertThat(props.getCacheExpiry()).isEqualTo(Duration.ofSeconds(30));
      });
  }

  @Test
  void shouldConvertStringToDataSize() {
    new ApplicationContextRunner()
      .withPropertyValues("app.features.maxUploadSize=50MB")
      .withBean(FeatureProperties.class)
      .run(context -> {
        FeatureProperties props = context.getBean(FeatureProperties.class);

        assertThat(props.getMaxUploadSize()).isEqualTo(DataSize.ofMegabytes(50));
      });
  }

  @Test
  void shouldConvertCommaDelimitedListToList() {
    new ApplicationContextRunner()
      .withPropertyValues("app.features.enabledFeatures=feature1,feature2,feature3")
      .withBean(FeatureProperties.class)
      .run(context -> {
        FeatureProperties props = context.getBean(FeatureProperties.class);

        assertThat(props.getEnabledFeatures())
          .containsExactly("feature1", "feature2", "feature3");
      });
  }
}
```

## Testing Property Binding with Default Values

### Verify Default Configuration

```java
@ConfigurationProperties(prefix = "app.cache")
@Data
public class CacheProperties {
  private long ttlSeconds = 300;
  private int maxSize = 1000;
  private boolean enabled = true;
  private String cacheType = "IN_MEMORY";
}

class DefaultValuesTest {

  @Test
  void shouldUseDefaultValuesWhenNotSpecified() {
    new ApplicationContextRunner()
      .withBean(CacheProperties.class)
      .run(context -> {
        CacheProperties props = context.getBean(CacheProperties.class);

        assertThat(props.getTtlSeconds()).isEqualTo(300L);
        assertThat(props.getMaxSize()).isEqualTo(1000);
        assertThat(props.isEnabled()).isTrue();
        assertThat(props.getCacheType()).isEqualTo("IN_MEMORY");
      });
  }

  @Test
  void shouldOverrideDefaultValuesWithProvidedProperties() {
    new ApplicationContextRunner()
      .withPropertyValues(
        "app.cache.ttlSeconds=600",
        "app.cache.cacheType=REDIS"
      )
      .withBean(CacheProperties.class)
      .run(context -> {
        CacheProperties props = context.getBean(CacheProperties.class);

        assertThat(props.getTtlSeconds()).isEqualTo(600L);
        assertThat(props.getCacheType()).isEqualTo("REDIS");
        assertThat(props.getMaxSize()).isEqualTo(1000); // Default unchanged
      });
  }
}
```

## Best Practices

- **Test all property bindings** including nested structures
- **Test validation constraints** thoroughly
- **Test both default and custom values**
- **Use ApplicationContextRunner** for context-free testing
- **Test profile-specific configurations** separately
- **Verify type conversions** work correctly
- **Test edge cases** (empty strings, null values, type mismatches)

## Common Pitfalls

- Not testing validation constraints
- Forgetting to test default values
- Not testing nested property structures
- Testing with wrong property prefix
- Not handling type conversion properly

## Troubleshooting

**Properties not binding**: Verify prefix and property names match exactly (including kebab-case to camelCase conversion).

**Validation not triggered**: Ensure `@Validated` is present and validation dependencies are on classpath.

**ApplicationContextRunner not found**: Verify `spring-boot-starter-test` is in test dependencies.

## References

- [Spring Boot ConfigurationProperties](https://docs.spring.io/spring-boot/docs/current/reference/html/configuration-metadata.html)
- [ApplicationContextRunner Testing](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/context/runner/ApplicationContextRunner.html)
- [Spring Profiles](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.profiles)
