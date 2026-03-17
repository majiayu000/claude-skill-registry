---
name: aws-sdk-java-v2-secrets-manager
description: Provides AWS Secrets Manager patterns using AWS SDK for Java 2.x. Use when storing/retrieving secrets (passwords, API keys, tokens), rotating secrets automatically, managing database credentials, or integrating secret management into Spring Boot applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - AWS Secrets Manager

## Overview

AWS Secrets Manager helps you protect secrets needed to access your applications, services, and IT resources. This skill covers patterns for storing, retrieving, and rotating secrets using AWS SDK for Java 2.x, including Spring Boot integration and caching strategies.

## When to Use

Use this skill when:
- Storing and retrieving application secrets programmatically
- Managing database credentials securely without hardcoding
- Implementing automatic secret rotation with Lambda functions
- Integrating AWS Secrets Manager with Spring Boot applications
- Setting up secret caching for improved performance
- Creating secure configuration management systems
- Working with multi-region secret deployments
- Implementing audit logging for secret access

## Instructions

Follow these steps to work with AWS Secrets Manager:

1. **Add Dependencies** - Include secretsmanager dependency and caching library
2. **Create Client** - Instantiate SecretsManagerClient with proper configuration
3. **Store Secrets** - Use createSecret() to store new secrets
4. **Retrieve Secrets** - Use getSecretValue() to fetch secrets
5. **Implement Caching** - Use SecretCache for improved performance
6. **Configure Rotation** - Set up automatic rotation schedules
7. **Integrate with Spring** - Configure beans and property sources
8. **Monitor Access** - Enable CloudTrail logging for audit trails

## Dependencies

### Maven
```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>secretsmanager</artifactId>
</dependency>

<!-- For secret caching (recommended for production) -->
<dependency>
    <groupId>com.amazonaws.secretsmanager</groupId>
    <artifactId>aws-secretsmanager-caching-java</artifactId>
    <version>2.0.0</version> // Use the sdk v2 compatible version
</dependency>
```

### Gradle
```gradle
implementation 'software.amazon.awssdk:secretsmanager'
implementation 'com.amazonaws.secretsmanager:aws-secretsmanager-caching-java:2.0.0
```

## Quick Start

### Basic Client Setup
```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.secretsmanager.SecretsManagerClient;

SecretsManagerClient secretsClient = SecretsManagerClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Store a Secret
```java
import software.amazon.awssdk.services.secretsmanager.model.*;

public String createSecret(String secretName, String secretValue) {
    CreateSecretRequest request = CreateSecretRequest.builder()
        .name(secretName)
        .secretString(secretValue)
        .build();

    CreateSecretResponse response = secretsClient.createSecret(request);
    return response.arn();
}
```

### Retrieve a Secret
```java
public String getSecretValue(String secretName) {
    GetSecretValueRequest request = GetSecretValueRequest.builder()
        .secretId(secretName)
        .build();

    GetSecretValueResponse response = secretsClient.getSecretValue(request);
    return response.secretString();
}
```

## Core Operations

### Secret Management
- Create secrets with `createSecret()`
- Retrieve secrets with `getSecretValue()`
- Update secrets with `updateSecret()`
- Delete secrets with `deleteSecret()`
- List secrets with `listSecrets()`
- Restore deleted secrets with `restoreSecret()`

### Secret Versioning
- Access specific versions by `versionId`
- Access versions by stage (e.g., "AWSCURRENT", "AWSPENDING")
- Automatically manage version history

### Secret Rotation
- Configure automatic rotation schedules
- Lambda-based rotation functions
- Immediate rotation with `rotateSecret()`

## Caching for Performance

### Setup Cache
```java
import com.amazonaws.secretsmanager.caching.SecretCache;

public class CachedSecrets {
    private final SecretCache cache;

    public CachedSecrets(SecretsManagerClient secretsClient) {
        this.cache = new SecretCache(secretsClient);
    }

    public String getCachedSecret(String secretName) {
        return cache.getSecretString(secretName);
    }
}
```

### Cache Configuration
```java
import com.amazonaws.secretsmanager.caching.SecretCacheConfiguration;

SecretCacheConfiguration config = SecretCacheConfiguration.builder()
    .maxCacheSize(1000)
    .cacheItemTTL(3600000) // 1 hour
    .build();
```

## Spring Boot Integration

### Configuration
```java
@Configuration
public class SecretsManagerConfiguration {

    @Bean
    public SecretsManagerClient secretsManagerClient() {
        return SecretsManagerClient.builder()
            .region(Region.of(region))
            .build();
    }

    @Bean
    public SecretCache secretCache(SecretsManagerClient secretsClient) {
        return new SecretCache(secretsClient);
    }
}
```

### Service Layer
```java
@Service
public class SecretsService {

    private final SecretCache cache;

    public SecretsService(SecretCache cache) {
        this.cache = cache;
    }

    public <T> T getSecretAsObject(String secretName, Class<T> type) {
        String secretJson = cache.getSecretString(secretName);
        return objectMapper.readValue(secretJson, type);
    }
}
```

### Database Configuration
```java
@Configuration
public class DatabaseConfiguration {

    @Bean
    public DataSource dataSource(SecretsService secretsService) {
        Map<String, String> credentials = secretsService.getSecretAsMap(
            "prod/database/credentials");

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(credentials.get("url"));
        config.setUsername(credentials.get("username"));
        config.setPassword(credentials.get("password"));

        return new HikariDataSource(config);
    }
}
```

## Examples

### Database Credentials Structure
```json
{
  "engine": "postgres",
  "host": "mydb.us-east-1.rds.amazonaws.com",
  "port": 5432,
  "username": "admin",
  "password": "MySecurePassword123!",
  "dbname": "mydatabase",
  "url": "jdbc:postgresql://mydb.us-east-1.rds.amazonaws.com:5432/mydatabase"
}
```

### API Keys Structure
```json
{
  "api_key": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
  "api_secret": "MySecretKey123!",
  "api_token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Common Patterns

### Error Handling
```java
try {
    String secret = secretsClient.getSecretValue(request).secretString();
} catch (SecretsManagerException e) {
    if (e.awsErrorDetails().errorCode().equals("ResourceNotFoundException")) {
        // Handle missing secret
    }
    throw e;
}
```

### Batch Operations
```java
List<String> secretNames = List.of("secret1", "secret2", "secret3");
Map<String, String> secrets = secretNames.stream()
    .collect(Collectors.toMap(
        Function.identity(),
        name -> cache.getSecretString(name)
    ));
```

## Best Practices

1. **Secret Management**:
   - Use descriptive secret names with hierarchical structure
   - Implement versioning and rotation
   - Add tags for organization and billing

2. **Caching**:
   - Always use caching in production environments
   - Configure appropriate TTL values based on secret sensitivity
   - Monitor cache hit rates

3. **Security**:
   - Never log secret values
   - Use KMS encryption for sensitive secrets
   - Implement least privilege IAM policies
   - Enable CloudTrail logging

4. **Performance**:
   - Reuse SecretsManagerClient instances
   - Use async operations when appropriate
   - Monitor API throttling limits

5. **Spring Boot Integration**:
   - Use `@Value` annotations for secret names
   - Implement proper exception handling
   - Use configuration properties for secret names

## Testing Strategies

### Unit Testing
```java
@ExtendWith(MockitoExtension.class)
class SecretsServiceTest {

    @Mock
    private SecretCache cache;

    @InjectMocks
    private SecretsService secretsService;

    @Test
    void shouldGetSecret() {
        when(cache.getSecretString("test-secret")).thenReturn("secret-value");

        String result = secretsService.getSecret("test-secret");

        assertEquals("secret-value", result);
    }
}
```

### Integration Testing
```java
@SpringBootTest(classes = TestSecretsConfiguration.class)
class SecretsManagerIntegrationTest {

    @Autowired
    private SecretsService secretsService;

    @Test
    void shouldRetrieveSecret() {
        String secret = secretsService.getSecret("test-secret");
        assertNotNull(secret);
    }
}
```

## Troubleshooting

### Common Issues
- **Access Denied**: Check IAM permissions
- **Resource Not Found**: Verify secret name and region
- **Decryption Failure**: Ensure KMS key permissions
- **Throttling**: Implement retry logic and backoff

### Debug Commands
```bash
# Check secret exists
aws secretsmanager describe-secret --secret-id my-secret

# List all secrets
aws secretsmanager list-secrets

# Get secret value (CLI)
aws secretsmanager get-secret-value --secret-id my-secret
```

## References

For detailed information and advanced patterns, see:

- [API Reference](./references/api-reference.md) - Complete API documentation
- [Caching Guide](./references/caching-guide.md) - Performance optimization strategies
- [Spring Boot Integration](./references/spring-boot-integration.md) - Complete Spring integration patterns

## Related Skills

- `aws-sdk-java-v2-core` - Core AWS SDK patterns and best practices
- `aws-sdk-java-v2-kms` - KMS encryption and key management
- `spring-boot-dependency-injection` - Spring dependency injection patterns

## Constraints and Warnings

- **Secret Size**: Maximum secret size is 10KB
- **API Costs**: Each API call incurs a cost; use caching to reduce calls
- **Rotation Limits**: Some secret types cannot be rotated automatically
- **Replication Limits**: Multi-region secrets have replication limits
- **Version Limits**: Secrets retain up to 100 versions including pending versions
- **Deletion Delay**: Secret deletion requires 7-30 day recovery window
- **KMS Encryption**: Secrets are encrypted using AWS KMS; key management is important
- **Cache Consistency**: Cached secrets may be stale during rotation
- **IAM Permissions**: Secrets require specific IAM actions for access
- **Logging**: Avoid logging secret values; use CloudTrail for audit trails