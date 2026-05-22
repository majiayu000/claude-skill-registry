---
name: aws-sdk-java-v2-secrets-manager
description: Provides AWS Secrets Manager patterns for AWS SDK for Java 2.x, including secret retrieval, caching, rotation-aware access, and Spring Boot integration. Use when storing or reading secrets in Java services, replacing hardcoded credentials, or wiring secret-backed configuration into applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - AWS Secrets Manager

## Overview

Use this skill to manage application secrets with AWS Secrets Manager from Java services.

It focuses on the operational flow that matters in production:
- how to retrieve and deserialize secrets safely
- when to add local caching
- how to integrate secret access into Spring Boot without leaking values into logs or configuration files

Keep large API notes and extended setup details in the bundled references.

## When to Use

Use this skill when:
- replacing hardcoded passwords, API keys, or tokens with managed secrets
- loading database credentials or third-party API credentials at runtime
- adding caching to reduce Secrets Manager latency and API cost
- handling secret version stages such as `AWSCURRENT` and `AWSPENDING`
- wiring secret access into Spring Boot beans or configuration services
- preparing rotation-aware applications or Lambda rotation workflows

Typical trigger phrases include `java secrets manager`, `spring boot secret`, `aws secret cache`, `load db credentials from secrets manager`, and `rotate secret`.

## Instructions

### 1. Model the secret before writing access code

Decide:
- the secret name and path convention
- whether the value is plain text or structured JSON
- which application boundary is allowed to read it
- whether the caller needs the latest value on every request or can tolerate a cache

Prefer JSON secrets for multi-field credentials such as database connection details.

### 2. Create one reusable client per application configuration

Use a single `SecretsManagerClient` with explicit region and the default credential provider chain unless the environment requires something more specific.

Keep client creation in configuration code, not in business services.

### 3. Retrieve and deserialize at the boundary layer

At the integration boundary:
- fetch with `GetSecretValueRequest`
- deserialize JSON into a typed object or validated map
- convert AWS exceptions into application-level errors
- never log `secretString()` or include it in thrown exception messages

### 4. Add caching only where it solves a real problem

Use caching when:
- the secret is read frequently
- latency matters for startup or request handling
- the cost of repeated lookups is material

Document cache TTL expectations clearly, especially if the secret rotates.

### 5. Design for rotation and staged versions

If the secret rotates:
- read through a thin service layer so cache invalidation and retry behavior stay centralized
- understand which callers must tolerate `AWSPENDING` during verification workflows
- test how the application behaves during stale cache windows or partial rotation failures

### 6. Validate end-to-end behavior

Before shipping:
- verify IAM permissions and KMS access
- test missing secret, wrong region, and decryption failure paths
- confirm secrets are not surfaced in logs, metrics, or debug endpoints
- prove database or API clients refresh correctly when credentials rotate

## Examples

### Example 1: Reusable client and typed secret lookup

```java
@Configuration
public class SecretsConfiguration {

    @Bean
    SecretsManagerClient secretsManagerClient() {
        return SecretsManagerClient.builder()
            .region(Region.of("eu-south-2"))
            .credentialsProvider(DefaultCredentialsProvider.create())
            .build();
    }
}

@Service
public class SecretsService {

    private final SecretsManagerClient client;
    private final ObjectMapper objectMapper;

    public SecretsService(SecretsManagerClient client, ObjectMapper objectMapper) {
        this.client = client;
        this.objectMapper = objectMapper;
    }

    public DatabaseSecret loadDatabaseSecret(String secretId) throws JsonProcessingException {
        GetSecretValueResponse response = client.getSecretValue(
            GetSecretValueRequest.builder().secretId(secretId).build()
        );
        return objectMapper.readValue(response.secretString(), DatabaseSecret.class);
    }
}
```

### Example 2: Cache a hot-path secret lookup

```java
public class CachedSecretsService {

    private final SecretCache cache;

    public CachedSecretsService(SecretsManagerClient client) {
        this.cache = new SecretCache(client);
    }

    public String apiToken(String secretId) {
        return cache.getSecretString(secretId);
    }
}
```

Use this pattern only when the application can tolerate the chosen cache refresh behavior.

## Best Practices

- Use hierarchical secret names that match domain and environment boundaries.
- Prefer typed JSON deserialization over string parsing scattered across the codebase.
- Keep secret retrieval in infrastructure services rather than controllers or entities.
- Reuse the SDK client and cache instances.
- Combine least-privilege IAM with KMS permissions and CloudTrail visibility.
- Make rotation behavior explicit in code and operational docs.

## Constraints and Warnings

- Do not log secret values, serialized secret objects, or decrypted payload fragments.
- Cached values may remain stale during or after rotation depending on TTL and refresh behavior.
- Secret access can fail because of IAM policy, KMS policy, region mismatch, or deleted versions; handle these cases explicitly.
- Automatic rotation is not available for every secret shape or integration.
- Large or frequently changing secrets may not be good candidates for aggressive in-memory caching.

## References

- `references/api-reference.md`
- `references/caching-guide.md`
- `references/spring-boot-integration.md`

## Related Skills

- `aws-sdk-java-v2-core`
- `aws-sdk-java-v2-kms`
- `spring-boot-dependency-injection`
