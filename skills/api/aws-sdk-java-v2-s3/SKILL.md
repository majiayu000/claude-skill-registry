---
name: aws-sdk-java-v2-s3
description: Amazon S3 patterns and examples using AWS SDK for Java 2.x. Use when working with S3 buckets, uploading/downloading objects, multipart uploads, presigned URLs, S3 Transfer Manager, object operations, or S3-specific configurations.
category: aws
tags: [aws, s3, java, sdk, storage, objects, transfer-manager, presigned-urls]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS SDK for Java 2.x - Amazon S3

## When to Use

Use this skill when:
- Creating, listing, or deleting S3 buckets with proper configuration
- Uploading or downloading objects from S3 with metadata and encryption
- Working with multipart uploads for large files (>100MB) with error handling
- Generating presigned URLs for temporary access to S3 objects
- Copying or moving objects between S3 buckets with metadata preservation
- Setting object metadata, storage classes, and access controls
- Implementing S3 Transfer Manager for optimized file transfers
- Integrating S3 with Spring Boot applications for cloud storage
- Setting up S3 event notifications for object lifecycle management
- Managing bucket policies, CORS configuration, and access controls
- Implementing retry mechanisms and error handling for S3 operations
- Testing S3 integrations with LocalStack for development environments

## Dependencies

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
    <version>2.20.0</version> // Use the latest stable version
</dependency>

<!-- For S3 Transfer Manager -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3-transfer-manager</artifactId>
    <version>2.20.0</version> // Use the latest stable version
</dependency>

<!-- For async operations -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>netty-nio-client</artifactId>
    <version>2.20.0</version> // Use the latest stable version
</dependency>
```

## Client Setup

### Basic Synchronous Client

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;

S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Basic Asynchronous Client

```java
import software.amazon.awssdk.services.s3.S3AsyncClient;

S3AsyncClient s3AsyncClient = S3AsyncClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Configured Client with Retry Logic

```java
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.core.retry.RetryPolicy;
import software.amazon.awssdk.core.retry.backoff.ExponentialRetryBackoff;
import java.time.Duration;

S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .httpClientBuilder(ApacheHttpClient.builder()
        .maxConnections(200)
        .connectionTimeout(Duration.ofSeconds(5)))
    .overrideConfiguration(b -> b
        .apiCallTimeout(Duration.ofSeconds(60))
        .apiCallAttemptTimeout(Duration.ofSeconds(30))
        .retryPolicy(RetryPolicy.builder()
            .numRetries(3)
            .retryBackoffStrategy(ExponentialRetryBackoff.builder()
                .baseDelay(Duration.ofSeconds(1))
                .maxBackoffTime(Duration.ofSeconds(30))
                .build())
            .build()))
    .build();
```

## Basic Bucket Operations

### Create Bucket

```java
import software.amazon.awssdk.services.s3.model.*;
import java.util.concurrent.CompletableFuture;

public void createBucket(S3Client s3Client, String bucketName) {
    try {
        CreateBucketRequest request = CreateBucketRequest.builder()
            .bucket(bucketName)
            .build();

        s3Client.createBucket(request);

        // Wait until bucket is ready
        HeadBucketRequest waitRequest = HeadBucketRequest.builder()
            .bucket(bucketName)
            .build();

        s3Client.waiter().waitUntilBucketExists(waitRequest);
        System.out.println("Bucket created successfully: " + bucketName);

    } catch (S3Exception e) {
        System.err.println("Error creating bucket: " + e.awsErrorDetails().errorMessage());
        throw e;
    }
}
```

### List All Buckets

```java
public List<String> listAllBuckets(S3Client s3Client) {
    ListBucketsResponse response = s3Client.listBuckets();

    return response.buckets().stream()
        .map(Bucket::name)
        .collect(Collectors.toList());
}
```

### Check if Bucket Exists

```java
public boolean bucketExists(S3Client s3Client, String bucketName) {
    try {
        HeadBucketRequest request = HeadBucketRequest.builder()
            .bucket(bucketName)
            .build();

        s3Client.headBucket(request);
        return true;

    } catch (NoSuchBucketException e) {
        return false;
    }
}
```

## Basic Object Operations

### Upload File to S3

```java
import software.amazon.awssdk.core.sync.RequestBody;
import java.nio.file.Paths;

public void uploadFile(S3Client s3Client, String bucketName, String key, String filePath) {
    PutObjectRequest request = PutObjectRequest.builder()
        .bucket(bucketName)
        .key(key)
        .build();

    s3Client.putObject(request, RequestBody.fromFile(Paths.get(filePath)));
    System.out.println("File uploaded: " + key);
}
```

### Download File from S3

```java
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;
import java.nio.file.Paths;

public void downloadFile(S3Client s3Client, String bucketName, String key, String destPath) {
    GetObjectRequest request = GetObjectRequest.builder()
        .bucket(bucketName)
        .key(key)
        .build();

    s3Client.getObject(request, Paths.get(destPath));
    System.out.println("File downloaded: " + destPath);
}
```

### Get Object Metadata

```java
public Map<String, String> getObjectMetadata(S3Client s3Client, String bucketName, String key) {
    HeadObjectRequest request = HeadObjectRequest.builder()
        .bucket(bucketName)
        .key(key)
        .build();

    HeadObjectResponse response = s3Client.headObject(request);
    return response.metadata();
}
```

## Advanced Object Operations

### Upload with Metadata and Encryption

```java
public void uploadWithMetadata(S3Client s3Client, String bucketName, String key,
                                String filePath, Map<String, String> metadata) {
    PutObjectRequest request = PutObjectRequest.builder()
        .bucket(bucketName)
        .key(key)
        .metadata(metadata)
        .contentType("application/pdf")
        .serverSideEncryption(ServerSideEncryption.AES256)
        .storageClass(StorageClass.STANDARD_IA)
        .build();

    PutObjectResponse response = s3Client.putObject(request,
        RequestBody.fromFile(Paths.get(filePath)));

    System.out.println("Upload completed. ETag: " + response.eTag());
}
```

### Copy Object Between Buckets

```java
public void copyObject(S3Client s3Client, String sourceBucket, String sourceKey,
                       String destBucket, String destKey) {
    CopyObjectRequest request = CopyObjectRequest.builder()
        .sourceBucket(sourceBucket)
        .sourceKey(sourceKey)
        .destinationBucket(destBucket)
        .destinationKey(destKey)
        .build();

    s3Client.copyObject(request);
    System.out.println("Object copied: " + sourceKey + " -> " + destKey);
}
```

### Delete Multiple Objects

```java
public void deleteMultipleObjects(S3Client s3Client, String bucketName, List<String> keys) {
    List<ObjectIdentifier> objectIds = keys.stream()
        .map(key -> ObjectIdentifier.builder().key(key).build())
        .collect(Collectors.toList());

    Delete delete = Delete.builder()
        .objects(objectIds)
        .build();

    DeleteObjectsRequest request = DeleteObjectsRequest.builder()
        .bucket(bucketName)
        .delete(delete)
        .build();

    DeleteObjectsResponse response = s3Client.deleteObjects(request);

    response.deleted().forEach(deleted ->
        System.out.println("Deleted: " + deleted.key()));

    response.errors().forEach(error ->
        System.err.println("Failed to delete " + error.key() + ": " + error.message()));
}
```

## Presigned URLs

### Generate Download URL

```java
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.*;
import java.time.Duration;

public String generateDownloadUrl(String bucketName, String key) {
    try (S3Presigner presigner = S3Presigner.builder()
            .region(Region.US_EAST_1)
            .build()) {

        GetObjectRequest getObjectRequest = GetObjectRequest.builder()
            .bucket(bucketName)
            .key(key)
            .build();

        GetObjectPresignRequest presignRequest = GetObjectPresignRequest.builder()
            .signatureDuration(Duration.ofMinutes(10))
            .getObjectRequest(getObjectRequest)
            .build();

        PresignedGetObjectRequest presignedRequest = presigner.presignGetObject(presignRequest);

        return presignedRequest.url().toString();
    }
}
```

### Generate Upload URL

```java
public String generateUploadUrl(String bucketName, String key) {
    try (S3Presigner presigner = S3Presigner.create()) {

        PutObjectRequest putObjectRequest = PutObjectRequest.builder()
            .bucket(bucketName)
            .key(key)
            .build();

        PutObjectPresignRequest presignRequest = PutObjectPresignRequest.builder()
            .signatureDuration(Duration.ofMinutes(5))
            .putObjectRequest(putObjectRequest)
            .build();

        PresignedPutObjectRequest presignedRequest = presigner.presignPutObject(presignRequest);

        return presignedRequest.url().toString();
    }
}
```

## S3 Transfer Manager

### Upload with Transfer Manager

```java
import software.amazon.awssdk.transfer.s3.*;
import software.amazon.awssdk.transfer.s3.model.*;

public void uploadWithTransferManager(String bucketName, String key, String filePath) {
    try (S3TransferManager transferManager = S3TransferManager.create()) {

        UploadFileRequest uploadRequest = UploadFileRequest.builder()
            .putObjectRequest(req -> req
                .bucket(bucketName)
                .key(key))
            .source(Paths.get(filePath))
            .build();

        FileUpload upload = transferManager.uploadFile(uploadRequest);

        // Monitor progress
        upload.progressFuture().thenAccept(progress -> {
            System.out.println("Upload progress: " + progress.progressPercent() + "%");
        });

        CompletedFileUpload result = upload.completionFuture().join();

        System.out.println("Upload complete. ETag: " + result.response().eTag());
    }
}
```

### Download with Transfer Manager

```java
public void downloadWithTransferManager(String bucketName, String key, String destPath) {
    try (S3TransferManager transferManager = S3TransferManager.create()) {

        DownloadFileRequest downloadRequest = DownloadFileRequest.builder()
            .getObjectRequest(req -> req
                .bucket(bucketName)
                .key(key))
            .destination(Paths.get(destPath))
            .build();

        FileDownload download = transferManager.downloadFile(downloadRequest);

        CompletedFileDownload result = download.completionFuture().join();

        System.out.println("Download complete. Size: " + result.response().contentLength());
    }
}
```

## Spring Boot Integration

### Configuration Properties

```java
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "aws.s3")
public class S3Properties {
    private String accessKey;
    private String secretKey;
    private String region = "us-east-1";
    private String endpoint;
    private String defaultBucket;
    private boolean asyncEnabled = false;
    private boolean transferManagerEnabled = true;

    // Getters and setters
    public String getAccessKey() { return accessKey; }
    public void setAccessKey(String accessKey) { this.accessKey = accessKey; }
    // ... other getters and setters
}
```

### S3 Configuration Class

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.S3AsyncClient;
import software.amazon.awssdk.regions.Region;
import java.net.URI;

@Configuration
public class S3Configuration {

    private final S3Properties properties;

    public S3Configuration(S3Properties properties) {
        this.properties = properties;
    }

    @Bean
    public S3Client s3Client() {
        S3Client.Builder builder = S3Client.builder()
            .region(Region.of(properties.getRegion()));

        if (properties.getAccessKey() != null && properties.getSecretKey() != null) {
            builder.credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create(
                    properties.getAccessKey(),
                    properties.getSecretKey())));
        }

        if (properties.getEndpoint() != null) {
            builder.endpointOverride(URI.create(properties.getEndpoint()));
        }

        return builder.build();
    }

    @Bean
    public S3AsyncClient s3AsyncClient() {
        S3AsyncClient.Builder builder = S3AsyncClient.builder()
            .region(Region.of(properties.getRegion()));

        if (properties.getAccessKey() != null && properties.getSecretKey() != null) {
            builder.credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create(
                    properties.getAccessKey(),
                    properties.getSecretKey())));
        }

        if (properties.getEndpoint() != null) {
            builder.endpointOverride(URI.create(properties.getEndpoint()));
        }

        return builder.build();
    }

    @Bean
    public S3TransferManager s3TransferManager() {
        return S3TransferManager.builder()
            .s3Client(s3Client())
            .build();
    }
}
```

### S3 Service

```java
import org.springframework.stereotype.Service;
import software.amazon.awssdk.transfer.s3.S3TransferManager;
import software.amazon.awssdk.services.s3.model.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
public class S3Service {

    private final S3Client s3Client;
    private final S3AsyncClient s3AsyncClient;
    private final S3TransferManager transferManager;
    private final S3Properties properties;

    public CompletableFuture<Void> uploadFileAsync(String key, Path file) {
        PutObjectRequest request = PutObjectRequest.builder()
            .bucket(properties.getDefaultBucket())
            .key(key)
            .build();

        return CompletableFuture.runAsync(() -> {
            s3Client.putObject(request, RequestBody.fromFile(file));
        });
    }

    public CompletableFuture<byte[]> downloadFileAsync(String key) {
        GetObjectRequest request = GetObjectRequest.builder()
            .bucket(properties.getDefaultBucket())
            .key(key)
            .build();

        return CompletableFuture.supplyAsync(() -> {
            try (ResponseInputStream<GetObjectResponse> response = s3Client.getObject(request)) {
                return response.readAllBytes();
            } catch (IOException e) {
                throw new RuntimeException("Failed to read S3 object", e);
            }
        });
    }

    public CompletableFuture<String> generatePresignedUrl(String key, Duration duration) {
        return CompletableFuture.supplyAsync(() -> {
            try (S3Presigner presigner = S3Presigner.builder()
                    .region(Region.of(properties.getRegion()))
                    .build()) {

                GetObjectRequest getRequest = GetObjectRequest.builder()
                    .bucket(properties.getDefaultBucket())
                    .key(key)
                    .build();

                GetObjectPresignRequest presignRequest = GetObjectPresignRequest.builder()
                    .signatureDuration(duration)
                    .getObjectRequest(getRequest)
                    .build();

                return presigner.presignGetObject(presignRequest).url().toString();
            }
        });
    }

    public Flux<S3Object> listObjects(String prefix) {
        ListObjectsV2Request request = ListObjectsV2Request.builder()
            .bucket(properties.getDefaultBucket())
            .prefix(prefix)
            .build();

        return Flux.create(sink -> {
            s3Client.listObjectsV2Paginator(request)
                .contents()
                .forEach(sink::next);
            sink.complete();
        });
    }
}
```

## Examples

### Basic File Upload Example

```java
public class S3UploadExample {
    public static void main(String[] args) {
        // Initialize client
        S3Client s3Client = S3Client.builder()
            .region(Region.US_EAST_1)
            .build();

        String bucketName = "my-example-bucket";
        String filePath = "document.pdf";
        String key = "uploads/document.pdf";

        // Create bucket if it doesn't exist
        if (!bucketExists(s3Client, bucketName)) {
            createBucket(s3Client, bucketName);
        }

        // Upload file
        Map<String, String> metadata = Map.of(
            "author", "John Doe",
            "content-type", "application/pdf",
            "upload-date", java.time.LocalDate.now().toString()
        );

        uploadWithMetadata(s3Client, bucketName, key, filePath, metadata);

        // Generate presigned URL
        String downloadUrl = generateDownloadUrl(bucketName, key);
        System.out.println("Download URL: " + downloadUrl);

        // Close client
        s3Client.close();
    }
}
```

### Batch File Processing Example

```java
import java.nio.file.*;
import java.util.stream.*;

public class S3BatchProcessing {
    public void processDirectoryUpload(S3Client s3Client, String bucketName, String directoryPath) {
        try (Stream<Path> paths = Files.walk(Paths.get(directoryPath))) {
            List<CompletableFuture<Void>> futures = paths
                .filter(Files::isRegularFile)
                .map(path -> {
                    String key = bucketName + "/" + path.getFileName().toString();
                    return CompletableFuture.runAsync(() -> {
                        uploadFile(s3Client, bucketName, key, path.toString());
                    });
                })
                .collect(Collectors.toList());

            // Wait for all uploads to complete
            CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
            ).join();

            System.out.println("All files uploaded successfully");
        } catch (IOException e) {
            throw new RuntimeException("Failed to process directory", e);
        }
    }
}
```

## Best Practices

### Performance Optimization

1. **Use S3 Transfer Manager**: Automatically handles multipart uploads, parallel transfers, and progress tracking for files >100MB
2. **Reuse S3 Client**: Clients are thread-safe and should be reused throughout the application lifecycle
3. **Enable async operations**: Use S3AsyncClient for I/O-bound operations to improve throughput
4. **Configure proper timeouts**: Set appropriate timeouts for large file operations
5. **Use connection pooling**: Configure HTTP client for optimal connection management

### Security Considerations

1. **Use temporary credentials**: Always use IAM roles or AWS STS for short-lived access tokens
2. **Enable server-side encryption**: Use AES-256 or AWS KMS for sensitive data
3. **Implement access controls**: Use bucket policies and IAM roles instead of access keys in production
4. **Validate object metadata**: Sanitize user-provided metadata to prevent header injection
5. **Use presigned URLs**: Avoid exposing credentials by using temporary access URLs

### Error Handling

1. **Implement retry logic**: Network operations should have exponential backoff retry strategies
2. **Handle throttling**: Implement proper handling of 429 Too Many Requests responses
3. **Validate object existence**: Check if objects exist before operations that require them
4. **Clean up failed operations**: Abort multipart uploads that fail
5. **Log appropriately**: Log successful operations and errors for monitoring

### Cost Optimization

1. **Use appropriate storage classes**: Choose STANDARD, STANDARD_IA, INTELLIGENT_TIERING based on access patterns
2. **Implement lifecycle policies**: Automatically transition or expire objects
3. **Enable object versioning**: For important data that needs retention
4. **Monitor usage**: Track data transfer and storage costs
5. **Minimize API calls**: Use batch operations when possible

## Constraints and Limitations

- **File size limits**: Single PUT operations limited to 5GB; use multipart uploads for larger files
- **Batch operations**: Maximum 1000 objects per DeleteObjects operation
- **Metadata size**: User-defined metadata limited to 2KB
- **Concurrent transfers**: Transfer Manager handles up to 100 concurrent transfers by default
- **Region consistency**: Cross-region operations may incur additional costs and latency
- **S3 eventual consistency**: New objects might not be immediately visible after upload

## References

For more detailed information, see:
- [AWS S3 Object Operations Reference](./references/s3-object-operations.md)
- [S3 Transfer Manager Patterns](./references/s3-transfer-patterns.md)
- [Spring Boot Integration Guide](./references/s3-spring-boot-integration.md)
- [AWS S3 Developer Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [AWS SDK for Java 2.x S3 API](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/s3/package-summary.html)

## Related Skills

- `aws-sdk-java-v2-core` - Core AWS SDK patterns and configuration
- `spring-boot-dependency`-injection - Spring dependency injection patterns
- `unit-test-service-layer` - Testing service layer patterns
- `unit-test-wiremock-rest-api` - Testing external API integrations