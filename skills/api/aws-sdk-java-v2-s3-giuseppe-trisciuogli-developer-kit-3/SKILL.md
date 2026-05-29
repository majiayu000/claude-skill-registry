---
name: aws-sdk-java-v2-s3
description: Provides Amazon S3 patterns and examples using AWS SDK for Java 2.x. Use when working with S3 buckets, uploading/downloading objects, multipart uploads, presigned URLs, S3 Transfer Manager, object operations, or S3-specific configurations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - Amazon S3

## Overview

Provides patterns for S3 operations: bucket management, object upload/download with multipart support, presigned URLs, S3 Transfer Manager, and S3-specific configurations using AWS SDK for Java 2.x.

## When to Use

- Creating, listing, or deleting S3 buckets with proper configuration
- Uploading or downloading objects from S3 with metadata and encryption
- Working with multipart uploads for large files (>100MB) with error handling
- Generating presigned URLs for temporary access to S3 objects
- Copying or moving objects between S3 buckets with metadata preservation
- Setting object metadata, storage classes, and access controls
- Implementing S3 Transfer Manager for optimized file transfers
- Integrating S3 with Spring Boot applications for cloud storage

## Quick Reference

| Operation | Method | Notes |
|-----------|--------|-------|
| Create bucket | `createBucket()` | Wait with `waiter().waitUntilBucketExists()` |
| Upload object | `putObject()` | Use `RequestBody.fromFile()` |
| Download object | `getObject()` | Streams to file or memory |
| Delete objects | `deleteObjects()` | Batch up to 1000 keys |
| Presigned URL | `presigner.presignGetObject()` | Max 7 days expiration |

### Storage Classes

| Class | Use Case |
|-------|----------|
| `STANDARD` | Frequently accessed data |
| `STANDARD_IA` | Infrequently accessed data |
| `GLACIER` | Long-term archive |
| `INTELLIGENT_TIERING` | Automatic cost optimization |

## Instructions

### 1. Add Dependencies

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
    <version>2.20.0</version>
</dependency>

<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3-transfer-manager</artifactId>
    <version>2.20.0</version>
</dependency>
```

### 2. Create S3 Client

```java
S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .build();

// With retry logic
S3Client s3Client = S3Client.builder()
    .region(Region.US_EAST_1)
    .overrideConfiguration(b -> b
        .retryPolicy(RetryPolicy.builder()
            .numRetries(3)
            .build()))
    .build();
```

### 3. Create Bucket

```java
CreateBucketRequest request = CreateBucketRequest.builder()
    .bucket(bucketName)
    .build();

s3Client.createBucket(request);

// Wait until ready
s3Client.waiter().waitUntilBucketExists(
    HeadBucketRequest.builder().bucket(bucketName).build()
);
```

### 4. Upload Object

```java
PutObjectRequest request = PutObjectRequest.builder()
    .bucket(bucketName)
    .key(key)
    .contentType("application/pdf")
    .serverSideEncryption(ServerSideEncryption.AES256)
    .storageClass(StorageClass.STANDARD_IA)
    .build();

s3Client.putObject(request, RequestBody.fromFile(Paths.get(filePath)));

// Validate upload completion
HeadObjectResponse headResp = s3Client.headObject(HeadObjectRequest.builder()
    .bucket(bucketName)
    .key(key)
    .build());
```

### 5. Download Object

```java
GetObjectRequest request = GetObjectRequest.builder()
    .bucket(bucketName)
    .key(key)
    .build();

s3Client.getObject(request, Paths.get(destPath));
```

### 6. Generate Presigned URL

```java
try (S3Presigner presigner = S3Presigner.create()) {
    GetObjectRequest getRequest = GetObjectRequest.builder()
        .bucket(bucketName)
        .key(key)
        .build();

    GetObjectPresignRequest presignRequest = GetObjectPresignRequest.builder()
        .signatureDuration(Duration.ofMinutes(10))
        .getObjectRequest(getRequest)
        .build();

    String url = presigner.presignGetObject(presignRequest).url().toString();
}
```

### 7. Use Transfer Manager (Large Files)

```java
try (S3TransferManager tm = S3TransferManager.create()) {
    UploadFileRequest request = UploadFileRequest.builder()
        .putObjectRequest(req -> req.bucket(bucketName).key(key))
        .source(Paths.get(filePath))
        .build();

    FileUpload upload = tm.uploadFile(request);
    CompletedFileUpload result = upload.completionFuture().join();
}
```

## Best Practices

### Performance
- **Use S3 Transfer Manager**: Automatic multipart uploads for files >100MB
- **Reuse S3 Client**: Clients are thread-safe; reuse throughout application
- **Enable async operations**: Use `S3AsyncClient` for I/O-bound operations
- **Configure timeouts**: Set appropriate timeouts for large file operations

### Security
- **Use temporary credentials**: IAM roles or AWS STS for short-lived tokens
- **Enable encryption**: Use AES-256 or AWS KMS for sensitive data
- **Use presigned URLs**: Avoid exposing credentials with temporary access
- **Validate metadata**: Sanitize user-provided metadata

### Error Handling
- **Implement retry logic**: Exponential backoff for network operations
- **Handle throttling**: Proper handling of 429 responses
- **Clean up failures**: Abort failed multipart uploads

### Cost Optimization
- **Use appropriate storage classes**: STANDARD, STANDARD_IA, INTELLIGENT_TIERING
- **Implement lifecycle policies**: Automatic transition/expiration
- **Minimize API calls**: Use batch operations when possible

## Constraints and Warnings

- **Object Size**: Single PUT limited to 5GB; use multipart for larger files
- **Bucket Names**: Must be globally unique across all AWS accounts
- **Object Immutability**: Objects cannot be modified; must be replaced entirely
- **Eventual Consistency**: List operations may have slight delays after uploads
- **Presigned URLs**: Maximum expiration time is 7 days
- **Multipart Uploads**: Parts must be at least 5MB except last part

## Examples

### Complete Upload Workflow with Validation

```java
// 1. Upload with validation
PutObjectRequest putRequest = PutObjectRequest.builder()
    .bucket(bucketName)
    .key(key)
    .contentType(contentType)
    .build();

s3Client.putObject(putRequest, RequestBody.fromFile(Paths.get(filePath)));

// 2. Validate with headObject
HeadObjectResponse headResp = s3Client.headObject(HeadObjectRequest.builder()
    .bucket(bucketName)
    .key(key)
    .build());

// 3. Verify metadata
long fileSize = Files.size(Paths.get(filePath));
if (headResp.contentLength() != fileSize) {
    throw new IllegalStateException("Upload size mismatch");
}
```

### Multipart Upload with Abort-on-Failure

```java
// 1. Initiate multipart upload
CreateMultipartUploadRequest createRequest = CreateMultipartUploadRequest.builder()
    .bucket(bucketName)
    .key(key)
    .build();

CreateMultipartUploadResponse multipartUpload = s3Client.createMultipartUpload(createRequest);
String uploadId = multipartUpload.uploadId();

try {
    // 2. Upload parts
    List<CompletedPart> parts = new ArrayList<>();
    int partNumber = 1;
    byte[] fileBytes = Files.readAllBytes(Paths.get(filePath));
    int chunkSize = 5 * 1024 * 1024; // 5MB minimum

    for (int offset = 0; offset < fileBytes.length; offset += chunkSize) {
        int length = Math.min(chunkSize, fileBytes.length - offset);
        UploadPartRequest uploadPartRequest = UploadPartRequest.builder()
            .bucket(bucketName)
            .key(key)
            .uploadId(uploadId)
            .partNumber(partNumber)
            .build();

        UploadPartResponse partResponse = s3Client.uploadPart(uploadPartRequest,
            RequestBody.fromBytes(Arrays.copyOfRange(fileBytes, offset, offset + length)));

        parts.add(CompletedPart.builder()
            .partNumber(partNumber)
            .eTag(partResponse.eTag())
            .build());
        partNumber++;
    }

    // 3. Complete multipart upload
    CompleteMultipartUploadRequest completeRequest = CompleteMultipartUploadRequest.builder()
        .bucket(bucketName)
        .key(key)
        .uploadId(uploadId)
        .multipartUpload(CompletedMultipartUpload.builder().parts(parts).build())
        .build();
    s3Client.completeMultipartUpload(completeRequest);

} catch (Exception e) {
    // 4. Abort on failure
    AbortMultipartUploadRequest abortRequest = AbortMultipartUploadRequest.builder()
        .bucket(bucketName)
        .key(key)
        .uploadId(uploadId)
        .build();
    s3Client.abortMultipartUpload(abortRequest);
    throw new RuntimeException("Upload failed, cleanup performed", e);
}
```

## References

- **[references/s3-client-setup.md](references/s3-client-setup.md)** — Client configuration and basic operations
- **[references/s3-object-operations.md](references/s3-object-operations.md)** — Advanced object operations
- **[references/s3-transfer-patterns.md](references/s3-transfer-patterns.md)** — Transfer Manager and multipart uploads
- **[references/s3-spring-boot-integration.md](references/s3-spring-boot-integration.md)** — Spring Boot integration patterns
- [AWS S3 Developer Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [AWS SDK for Java 2.x S3 API](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/s3/package-summary.html)

## Related Skills

- `aws-sdk-java-v2-core` - Core AWS SDK patterns and configuration
- `spring-boot-dependency-injection` - Spring dependency injection patterns
