---
name: aws-sdk-java-v2-core
description: Core patterns and best practices for AWS SDK for Java 2.x. Use when configuring AWS service clients, setting up authentication, managing credentials, configuring timeouts, HTTP clients, or following AWS SDK best practices.
category: aws
tags: [aws, java, sdk, core, authentication, configuration]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS SDK for Java 2.x - Core Patterns

## Overview

Configure AWS service clients, authentication, timeouts, HTTP clients, and implement best practices for AWS SDK for Java 2.x applications. This skill provides essential patterns for building robust, performant, and secure integrations with AWS services.

## When to Use

Use this skill when:
- Setting up AWS SDK for Java 2.x service clients with proper configuration
- Configuring authentication and credential management strategies
- Implementing client lifecycle management and resource cleanup
- Optimizing performance with HTTP client configuration and connection pooling
- Setting up proper timeout configurations for API calls
- Implementing error handling and retry policies
- Enabling monitoring and metrics collection
- Integrating AWS SDK with Spring Boot applications
- Testing AWS integrations with LocalStack and Testcontainers

## Quick Start

### Basic Service Client Setup

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;

// Basic client with region
S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .build();

// Always close clients when done
try (S3Client s3 = S3Client.builder().region(Region.US_EAST_1).build()) {
    // Use client
} // Auto-closed
```

### Basic Authentication

```java
// Uses default credential provider chain
S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .build(); // Automatically detects credentials
```

## Client Configuration

### Service Client Builder Pattern

```java
import software.amazon.awssdk.core.client.config.ClientOverrideConfiguration;
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.http.apache.ProxyConfiguration;
import software.amazon.awssdk.metrics.publishers.cloudwatch.CloudWatchMetricPublisher;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import java.time.Duration;
import java.net.URI;

// Advanced client configuration
S3Client s3Client = S3Client.builder()
    .region(Region.EU_SOUTH_2)
    .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
    .overrideConfiguration(b -> b
        .apiCallTimeout(Duration.ofSeconds(30))
        .apiCallAttemptTimeout(Duration.ofSeconds(10))
        .addMetricPublisher(CloudWatchMetricPublisher.create()))
    .httpClientBuilder(ApacheHttpClient.builder()
        .maxConnections(100)
        .connectionTimeout(Duration.ofSeconds(5))
        .proxyConfiguration(ProxyConfiguration.builder()
            .endpoint(URI.create("http://proxy:8080"))
            .build()))
    .build();
```

### Separate Configuration Objects

```java
ClientOverrideConfiguration clientConfig = ClientOverrideConfiguration.builder()
    .apiCallTimeout(Duration.ofSeconds(30))
    .apiCallAttemptTimeout(Duration.ofSeconds(10))
    .addMetricPublisher(CloudWatchMetricPublisher.create())
    .build();

ApacheHttpClient httpClient = ApacheHttpClient.builder()
    .maxConnections(100)
    .connectionTimeout(Duration.ofSeconds(5))
    .build();

S3Client s3Client = S3Client.builder()
    .region(Region.EU_SOUTH_2)
    .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
    .overrideConfiguration(clientConfig)
    .httpClient(httpClient)
    .build();
```

## Authentication and Credentials

### Default Credentials Provider Chain

```java
// SDK automatically uses default credential provider chain:
// 1. Java system properties (aws.accessKeyId and aws.secretAccessKey)
// 2. Environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
// 3. Web identity token from AWS_WEB_IDENTITY_TOKEN_FILE
// 4. Shared credentials and config files (~/.aws/credentials and ~/.aws/config)
// 5. Amazon ECS container credentials
// 6. Amazon EC2 instance profile credentials

S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .build(); // Uses default credential provider chain
```

### Explicit Credentials Providers

```java
import software.amazon.awssdk.auth.credentials.*;

// Environment variables
CredentialsProvider envCredentials = EnvironmentVariableCredentialsProvider.create();

// Profile from ~/.aws/credentials
CredentialsProvider profileCredentials = ProfileCredentialsProvider.create("myprofile");

// Static credentials (NOT recommended for production)
CredentialsProvider staticCredentials = StaticCredentialsProvider.create(
    AwsBasicCredentials.create("accessKeyId", "secretAccessKey")
);

// Instance profile (for EC2)
CredentialsProvider instanceProfileCredentials = InstanceProfileCredentialsProvider.create();

// Use with client
S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .credentialsProvider(profileCredentials)
    .build();
```

### SSO Authentication Setup

```properties
# ~/.aws/config
[default]
sso_session = my-sso
sso_account_id = 111122223333
sso_role_name = SampleRole
region = us-east-1
output = json

[sso-session my-sso]
sso_region = us-east-1
sso_start_url = https://provided-domain.awsapps.com/start
sso_registration_scopes = sso:account:access
```

```bash
# Login before running application
aws sso login

# Verify active session
aws sts get-caller-identity
```

## HTTP Client Configuration

### Apache HTTP Client (Recommended for Sync)

```java
import software.amazon.awssdk.http.apache.ApacheHttpClient;

ApacheHttpClient httpClient = ApacheHttpClient.builder()
    .maxConnections(100)
    .connectionTimeout(Duration.ofSeconds(5))
    .socketTimeout(Duration.ofSeconds(30))
    .connectionTimeToLive(Duration.ofMinutes(5))
    .expectContinueEnabled(true)
    .build();

S3Client s3Client = S3Client.builder()
    .httpClient(httpClient)
    .build();
```

### Netty HTTP Client (For Async Operations)

```java
import software.amazon.awssdk.http.nio.netty.NettyNioAsyncHttpClient;
import software.amazon.awssdk.http.nio.netty.SslProvider;

NettyNioAsyncHttpClient httpClient = NettyNioAsyncHttpClient.builder()
    .maxConcurrency(100)
    .connectionTimeout(Duration.ofSeconds(5))
    .readTimeout(Duration.ofSeconds(30))
    .writeTimeout(Duration.ofSeconds(30))
    .sslProvider(SslProvider.OPENSSL) // Better performance than JDK
    .build();

S3AsyncClient s3AsyncClient = S3AsyncClient.builder()
    .httpClient(httpClient)
    .build();
```

### URL Connection HTTP Client (Lightweight)

```java
import software.amazon.awssdk.http.urlconnection.UrlConnectionHttpClient;

UrlConnectionHttpClient httpClient = UrlConnectionHttpClient.builder()
    .socketTimeout(Duration.ofSeconds(30))
    .build();
```

## Best Practices

### 1. Reuse Service Clients

**DO:**
```java
@Service
public class S3Service {
    private final S3Client s3Client;

    public S3Service() {
        this.s3Client = S3Client.builder()
            .region(Region.US_EAST_1)
            .build();
    }

    // Reuse s3Client for all operations
}
```

**DON'T:**
```java
public void uploadFile(String bucket, String key) {
    // Creates new client each time - wastes resources!
    S3Client s3 = S3Client.builder().build();
    s3.putObject(...);
    s3.close();
}
```

### 2. Configure API Timeouts

```java
S3Client s3Client = S3Client.builder()
    .overrideConfiguration(b -> b
        .apiCallTimeout(Duration.ofSeconds(30))
        .apiCallAttemptTimeout(Duration.ofMillis(5000)))
    .build();
```

### 3. Close Unused Clients

```java
// Try-with-resources
try (S3Client s3 = S3Client.builder().build()) {
    s3.listBuckets();
}

// Explicit close
S3Client s3Client = S3Client.builder().build();
try {
    s3Client.listBuckets();
} finally {
    s3Client.close();
}
```

### 4. Close Streaming Responses

```java
try (ResponseInputStream<GetObjectResponse> s3Object =
        s3Client.getObject(GetObjectRequest.builder()
            .bucket(bucket)
            .key(key)
            .build())) {

    // Read and process stream immediately
    byte[] data = s3Object.readAllBytes();

} // Stream auto-closed, connection returned to pool
```

### 5. Optimize SSL for Async Clients

**Add dependency:**
```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-tcnative-boringssl-static</artifactId>
    <version>2.0.61.Final</version>
    <scope>runtime</scope>
</dependency>
```

**Configure SSL:**
```java
NettyNioAsyncHttpClient httpClient = NettyNioAsyncHttpClient.builder()
    .sslProvider(SslProvider.OPENSSL)
    .build();

S3AsyncClient s3AsyncClient = S3AsyncClient.builder()
    .httpClient(httpClient)
    .build();
```

## Spring Boot Integration

### Configuration Properties

```java
@ConfigurationProperties(prefix = "aws")
public record AwsProperties(
    String region,
    String accessKeyId,
    String secretAccessKey,
    S3Properties s3,
    DynamoDbProperties dynamoDb
) {
    public record S3Properties(
        Integer maxConnections,
        Integer connectionTimeoutSeconds,
        Integer apiCallTimeoutSeconds
    ) {}

    public record DynamoDbProperties(
        Integer maxConnections,
        Integer readTimeoutSeconds
    ) {}
}
```

### Client Configuration Beans

```java
@Configuration
@EnableConfigurationProperties(AwsProperties.class)
public class AwsClientConfiguration {

    private final AwsProperties awsProperties;

    public AwsClientConfiguration(AwsProperties awsProperties) {
        this.awsProperties = awsProperties;
    }

    @Bean
    public S3Client s3Client() {
        return S3Client.builder()
            .region(Region.of(awsProperties.region()))
            .credentialsProvider(credentialsProvider())
            .overrideConfiguration(clientOverrideConfiguration(
                awsProperties.s3().apiCallTimeoutSeconds()))
            .httpClient(apacheHttpClient(
                awsProperties.s3().maxConnections(),
                awsProperties.s3().connectionTimeoutSeconds()))
            .build();
    }

    private CredentialsProvider credentialsProvider() {
        if (awsProperties.accessKeyId() != null &&
            awsProperties.secretAccessKey() != null) {
            return StaticCredentialsProvider.create(
                AwsBasicCredentials.create(
                    awsProperties.accessKeyId(),
                    awsProperties.secretAccessKey()));
        }
        return DefaultCredentialsProvider.create();
    }

    private ClientOverrideConfiguration clientOverrideConfiguration(
            Integer apiCallTimeoutSeconds) {
        return ClientOverrideConfiguration.builder()
            .apiCallTimeout(Duration.ofSeconds(
                apiCallTimeoutSeconds != null ? apiCallTimeoutSeconds : 30))
            .apiCallAttemptTimeout(Duration.ofSeconds(10))
            .build();
    }

    private ApacheHttpClient apacheHttpClient(
            Integer maxConnections,
            Integer connectionTimeoutSeconds) {
        return ApacheHttpClient.builder()
            .maxConnections(maxConnections != null ? maxConnections : 50)
            .connectionTimeout(Duration.ofSeconds(
                connectionTimeoutSeconds != null ? connectionTimeoutSeconds : 5))
            .socketTimeout(Duration.ofSeconds(30))
            .build();
    }
}
```

### Application Properties

```yaml
aws:
  region: us-east-1
  s3:
    max-connections: 100
    connection-timeout-seconds: 5
    api-call-timeout-seconds: 30
  dynamo-db:
    max-connections: 50
    read-timeout-seconds: 30
```

## Error Handling

```java
import software.amazon.awssdk.services.s3.model.S3Exception;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.core.exception.SdkServiceException;

try {
    s3Client.getObject(request);

} catch (S3Exception e) {
    // Service-specific exception
    System.err.println("S3 Error: " + e.awsErrorDetails().errorMessage());
    System.err.println("Error Code: " + e.awsErrorDetails().errorCode());
    System.err.println("Status Code: " + e.statusCode());
    System.err.println("Request ID: " + e.requestId());

} catch (SdkServiceException e) {
    // Generic service exception
    System.err.println("AWS Service Error: " + e.getMessage());

} catch (SdkClientException e) {
    // Client-side error (network, timeout, etc.)
    System.err.println("Client Error: " + e.getMessage());
}
```

## Testing Patterns

### LocalStack Integration

```java
@TestConfiguration
public class LocalStackAwsConfig {

    @Bean
    public S3Client s3Client() {
        return S3Client.builder()
            .region(Region.US_EAST_1)
            .endpointOverride(URI.create("http://localhost:4566"))
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create("test", "test")))
            .build();
    }
}
```

### Testcontainers with LocalStack

```java
@Testcontainers
@SpringBootTest
class S3IntegrationTest {

    @Container
    static LocalStackContainer localstack = new LocalStackContainer(
        DockerImageName.parse("localstack/localstack:3.0"))
        .withServices(LocalStackContainer.Service.S3);

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        registry.add("aws.s3.endpoint",
            () -> localstack.getEndpointOverride(LocalStackContainer.Service.S3));
        registry.add("aws.region", () -> localstack.getRegion());
        registry.add("aws.access-key-id", localstack::getAccessKey);
        registry.add("aws.secret-access-key", localstack::getSecretKey);
    }
}
```

## Maven Dependencies

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>software.amazon.awssdk</groupId>
            <artifactId>bom</artifactId>
            <version>2.25.0</version> // Use latest stable version
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- Core SDK -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>sdk-core</artifactId>
    </dependency>

    <!-- Apache HTTP Client (recommended for sync) -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>apache-client</artifactId>
    </dependency>

    <!-- Netty HTTP Client (for async) -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>netty-nio-client</artifactId>
    </dependency>

    <!-- URL Connection HTTP Client (lightweight) -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>url-connection-client</artifactId>
    </dependency>

    <!-- CloudWatch Metrics -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>cloudwatch-metric-publisher</artifactId>
    </dependency>

    <!-- OpenSSL for better performance -->
    <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-tcnative-boringssl-static</artifactId>
        <version>2.0.61.Final</version>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

## Gradle Dependencies

```gradle
dependencies {
    implementation platform('software.amazon.awssdk:bom:2.25.0')

    implementation 'software.amazon.awssdk:sdk-core'
    implementation 'software.amazon.awssdk:apache-client'
    implementation 'software.amazon.awssdk:netty-nio-client'
    implementation 'software.amazon.awssdk:cloudwatch-metric-publisher'

    runtimeOnly 'io.netty:netty-tcnative-boringssl-static:2.0.61.Final'
}
```

## Examples

### Basic S3 Upload

```java
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

try (S3Client s3 = S3Client.builder().region(Region.US_EAST_1).build()) {
    PutObjectRequest request = PutObjectRequest.builder()
        .bucket("my-bucket")
        .key("uploads/file.txt")
        .build();

    s3.putObject(request, RequestBody.fromString("Hello, World!"));
}
```

### S3 List Objects with Pagination

```java
import software.amazon.awssdk.services.s3.model.ListObjectsV2Request;
import software.amazon.awssdk.services.s3.model.ListObjectsV2Response;

try (S3Client s3 = S3Client.builder().region(Region.US_EAST_1).build()) {
    ListObjectsV2Request request = ListObjectsV2Request.builder()
        .bucket("my-bucket")
        .build();

    ListObjectsV2Response response = s3.listObjectsV2(request);
    response.contents().forEach(object -> {
        System.out.println("Object key: " + object.key());
    });
}
```

### Async S3 Upload

```java
import software.amazon.awssdk.core.async.AsyncRequestBody;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

S3AsyncClient s3AsyncClient = S3AsyncClient.builder().build();

PutObjectRequest request = PutObjectRequest.builder()
    .bucket("my-bucket")
    .key("async-upload.txt")
    .build();

CompletableFuture<PutObjectResponse> future = s3AsyncClient.putObject(
    request, Async.fromString("Hello, Async World!"));

future.thenAccept(response -> {
    System.out.println("Upload completed: " + response.eTag());
}).exceptionally(error -> {
    System.err.println("Upload failed: " + error.getMessage());
    return null;
});
```

## Performance Considerations

1. **Connection Pooling**: Default max connections is 50. Increase for high-throughput applications.
2. **Timeouts**: Always set both `apiCallTimeout` and `apiCallAttemptTimeout`.
3. **Client Reuse**: Create clients once, reuse throughout application lifecycle.
4. **Stream Handling**: Close streams immediately to prevent connection pool exhaustion.
5. **Async for I/O**: Use async clients for I/O-bound operations.
6. **OpenSSL**: Use OpenSSL with Netty for better SSL performance.
7. **Metrics**: Enable CloudWatch metrics to monitor performance.

## Security Best Practices

1. **Never hardcode credentials**: Use credential providers or environment variables.
2. **Use IAM roles**: Prefer IAM roles over access keys when possible.
3. **Rotate credentials**: Implement credential rotation for long-lived keys.
4. **Least privilege**: Grant minimum required permissions.
5. **Enable SSL**: Always use HTTPS endpoints (default).
6. **Audit logging**: Enable AWS CloudTrail for API call auditing.

## Related Skills

- `aws-sdk-java-v2-s3` - S3-specific patterns and examples
- `aws-sdk-java-v2-dynamodb` - DynamoDB patterns and examples
- `aws-sdk-java-v2-lambda` - Lambda patterns and examples

## References

See [references/](references/) for detailed documentation:

- [Developer Guide](references/developer-guide.md) - Comprehensive guide and architecture overview
- [API Reference](references/api-reference.md) - Complete API documentation for core classes
- [Best Practices](references/best-practices.md) - In-depth best practices and configuration examples

## Additional Resources

- [AWS SDK for Java 2.x Developer Guide](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html)
- [AWS SDK for Java 2.x API Reference](https://sdk.amazonaws.com/java/api/latest/)
- [Best Practices](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/best-practices.html)
- [GitHub Repository](https://github.com/aws/aws-sdk-java-v2)