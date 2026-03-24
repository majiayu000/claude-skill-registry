---
name: aws-sdk-java-v2-core
description: Provides AWS SDK for Java 2.x client configuration, credential resolution, HTTP client tuning, timeout, retry, and testing patterns. Use when creating or hardening AWS service clients, wiring Spring Boot beans, debugging auth or region issues, or choosing sync vs async SDK usage.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x Core Patterns

## Overview

Use this skill to set up AWS SDK for Java 2.x clients with production-safe defaults.

It focuses on the decisions that matter most:
- how credentials and region are resolved
- how to configure sync and async HTTP clients
- how to apply timeouts, retries, lifecycle management, and tests

Keep `SKILL.md` focused on setup and delivery flow. Use the `references/` files for deeper API details and expanded examples.

## When to Use

Use this skill when:
- creating a new AWS SDK for Java 2.x integration in a Java or Spring Boot service
- choosing between sync clients (`S3Client`, `DynamoDbClient`) and async clients (`S3AsyncClient`, `SqsAsyncClient`)
- configuring the default credential provider chain, profiles, IAM roles, or web identity auth
- tuning HTTP connection pooling, timeouts, retries, and observability
- debugging common startup issues such as missing region, invalid credentials, or resource leaks
- preparing integration tests with LocalStack, Testcontainers, or real AWS environments

Typical trigger phrases include `aws sdk java v2`, `configure aws client`, `java aws credentials`, `s3 client bean`, `aws sdk timeout`, and `spring boot aws sdk`.

## Instructions

### 1. Start with the service client and execution model

Choose the smallest client surface that solves the problem:
- use synchronous clients for request/response application flows
- use asynchronous clients when concurrency, streaming, or backpressure matter
- create one reusable client per service and configuration profile instead of rebuilding clients per request

### 2. Prefer the default credential and region resolution flow

Default resolution is usually the right starting point:
- local development: shared AWS config, SSO, or environment variables
- CI/CD: web identity or injected environment variables
- AWS runtime: ECS task roles, EKS IRSA, or EC2 instance profiles

Only hardcode or explicitly override the credential provider when there is a real need such as multi-account access, test isolation, or profile switching.

### 3. Configure HTTP client, timeouts, and retries explicitly

Set these values intentionally for production services:
- API call timeout and attempt timeout
- connection timeout and max connections or concurrency
- retry strategy aligned with service quotas and idempotency
- proxy or TLS settings only when required by the environment

Use Apache for most synchronous clients and Netty for most async clients unless the project already standardizes on something else.

### 4. Wire clients as application-level dependencies

In Spring Boot or modular Java applications:
- expose clients as beans or factory-managed singletons
- inject them through constructors
- keep credential and region selection in configuration, not business services
- close custom HTTP clients and SDK clients during shutdown if the lifecycle is not managed automatically

### 5. Handle failures close to integration boundaries

At the boundary layer:
- catch `SdkException` or service-specific exceptions
- distinguish retryable failures from auth, quota, and validation failures
- log request context, but never secrets or raw credentials
- return application-level errors rather than leaking AWS SDK exceptions through the domain layer

### 6. Validate locally before shipping

Before merging or deploying:
- verify region and caller identity in the target environment
- run integration tests against LocalStack, Testcontainers, or a sandbox AWS account
- confirm timeouts and retry behavior under failure conditions
- check that clients are reused and not created inside hot execution paths

## Examples

### Example 1: Spring Boot sync client with explicit HTTP and timeout settings

```java
@Configuration
public class AwsClientConfiguration {

    @Bean
    S3Client s3Client() {
        return S3Client.builder()
            .region(Region.of("eu-south-2"))
            .credentialsProvider(DefaultCredentialsProvider.create())
            .httpClientBuilder(ApacheHttpClient.builder()
                .maxConnections(100)
                .connectionTimeout(Duration.ofSeconds(3)))
            .overrideConfiguration(ClientOverrideConfiguration.builder()
                .apiCallAttemptTimeout(Duration.ofSeconds(10))
                .apiCallTimeout(Duration.ofSeconds(30))
                .build())
            .build();
    }
}
```

Why this works:
- credentials stay outside application code
- timeouts are explicit
- the client is reusable and easy to test

### Example 2: Async client for high-concurrency workloads

```java
SqsAsyncClient sqsAsyncClient = SqsAsyncClient.builder()
    .region(Region.US_EAST_1)
    .credentialsProvider(DefaultCredentialsProvider.create())
    .httpClientBuilder(NettyNioAsyncHttpClient.builder()
        .maxConcurrency(200)
        .connectionTimeout(Duration.ofSeconds(3))
        .readTimeout(Duration.ofSeconds(20)))
    .overrideConfiguration(ClientOverrideConfiguration.builder()
        .apiCallTimeout(Duration.ofSeconds(30))
        .build())
    .build();
```

Use this pattern when you need non-blocking SDK calls and the rest of the application is prepared to consume futures or reactive wrappers.

## Best Practices

- Default to `DefaultCredentialsProvider` unless a project requirement says otherwise.
- Keep region selection explicit for server-side services.
- Reuse SDK clients instead of constructing them per request.
- Tune retries with service quotas and idempotency in mind.
- Put business mapping on top of the SDK, not inside controllers.
- Keep integration tests close to the configuration that creates the clients.
- Move deep service-specific examples to dedicated skills such as S3, DynamoDB, Bedrock, or Secrets Manager.

## Constraints and Warnings

- Do not embed access keys or session tokens in source code, examples, or configuration files.
- Static credentials are acceptable only for tightly scoped local tests.
- Missing region or invalid credential resolution often fails only at first call, so verify startup assumptions explicitly.
- Async clients require lifecycle management for the underlying HTTP resources.
- Excessive retries can amplify throttling and increase latency.
- Proxy, TLS, and metric publisher APIs can vary by chosen HTTP stack and SDK version; adapt examples to the versions already used by the project.

## References

- `references/api-reference.md`
- `references/best-practices.md`
- `references/developer-guide.md`

## Related Skills

- `aws-sdk-java-v2-secrets-manager`
- `aws-sdk-java-v2-s3`
- `aws-sdk-java-v2-dynamodb`
- `aws-sdk-java-v2-bedrock`
