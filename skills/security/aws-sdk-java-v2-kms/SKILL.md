---
name: aws-sdk-java-v2-kms
description: AWS Key Management Service (KMS) patterns using AWS SDK for Java 2.x. Use when creating/managing encryption keys, encrypting/decrypting data, generating data keys, digital signing, key rotation, or integrating encryption into Spring Boot applications.
category: aws
tags: [aws, kms, java, sdk, encryption, security]
version: 1.1.0
allowed-tools: Read, Write, Bash, WebFetch
---

# AWS SDK for Java 2.x - AWS KMS (Key Management Service)

## Overview

This skill provides comprehensive patterns for AWS Key Management Service (KMS) using AWS SDK for Java 2.x. Focus on implementing secure encryption solutions with proper key management, envelope encryption, and Spring Boot integration patterns.

## When to Use

Use this skill when:
- Creating and managing symmetric encryption keys for data protection
- Implementing client-side encryption and envelope encryption patterns
- Generating data keys for local data encryption with KMS-managed keys
- Setting up digital signatures and verification with asymmetric keys
- Integrating encryption capabilities into Spring Boot applications
- Implementing secure key lifecycle management
- Setting up key rotation policies and access controls

## Dependencies

### Maven

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>kms</artifactId>
</dependency>
```

### Gradle

```groovy
implementation 'software.amazon.awssdk:kms:2.x.x'
```

## Client Setup

### Basic Synchronous Client

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.kms.KmsClient;

KmsClient kmsClient = KmsClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Basic Asynchronous Client

```java
import software.amazon.awssdk.services.kms.KmsAsyncClient;

KmsAsyncClient kmsAsyncClient = KmsAsyncClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Advanced Client Configuration

```java
KmsClient kmsClient = KmsClient.builder()
    .region(Region.of(System.getenv("AWS_REGION")))
    .credentialsProvider(DefaultCredentialsProvider.create())
    .overrideConfiguration(c -> c.retryPolicy(RetryPolicy.builder()
        .numRetries(3)
        .build()))
    .build();
```

## Basic Key Management

### Create Encryption Key

```java
public String createEncryptionKey(KmsClient kmsClient, String description) {
    CreateKeyRequest request = CreateKeyRequest.builder()
        .description(description)
        .keyUsage(KeyUsageType.ENCRYPT_DECRYPT)
        .build();

    CreateKeyResponse response = kmsClient.createKey(request);
    return response.keyMetadata().keyId();
}
```

### Describe Key

```java
public KeyMetadata getKeyMetadata(KmsClient kmsClient, String keyId) {
    DescribeKeyRequest request = DescribeKeyRequest.builder()
        .keyId(keyId)
        .build();

    return kmsClient.describeKey(request).keyMetadata();
}
```

### Enable/Disable Key

```java
public void toggleKeyState(KmsClient kmsClient, String keyId, boolean enable) {
    if (enable) {
        kmsClient.enableKey(EnableKeyRequest.builder().keyId(keyId).build());
    } else {
        kmsClient.disableKey(DisableKeyRequest.builder().keyId(keyId).build());
    }
}
```

## Basic Encryption and Decryption

### Encrypt Data

```java
public String encryptData(KmsClient kmsClient, String keyId, String plaintext) {
    SdkBytes plaintextBytes = SdkBytes.fromString(plaintext, StandardCharsets.UTF_8);

    EncryptRequest request = EncryptRequest.builder()
        .keyId(keyId)
        .plaintext(plaintextBytes)
        .build();

    EncryptResponse response = kmsClient.encrypt(request);
    return Base64.getEncoder().encodeToString(
        response.ciphertextBlob().asByteArray());
}
```

### Decrypt Data

```java
public String decryptData(KmsClient kmsClient, String ciphertextBase64) {
    byte[] ciphertext = Base64.getDecoder().decode(ciphertextBase64);
    SdkBytes ciphertextBytes = SdkBytes.fromByteArray(ciphertext);

    DecryptRequest request = DecryptRequest.builder()
        .ciphertextBlob(ciphertextBytes)
        .build();

    DecryptResponse response = kmsClient.decrypt(request);
    return response.plaintext().asString(StandardCharsets.UTF_8);
}
```

## Envelope Encryption Pattern

### Generate and Use Data Key

```java
public DataKeyResult encryptWithEnvelope(KmsClient kmsClient, String masterKeyId, byte[] data) {
    // Generate data key
    GenerateDataKeyRequest keyRequest = GenerateDataKeyRequest.builder()
        .keyId(masterKeyId)
        .keySpec(DataKeySpec.AES_256)
        .build();

    GenerateDataKeyResponse keyResponse = kmsClient.generateDataKey(keyRequest);

    // Encrypt data with data key
    byte[] encryptedData = encryptWithAES(data,
        keyResponse.plaintext().asByteArray());

    // Clear plaintext key from memory
    Arrays.fill(keyResponse.plaintext().asByteArray(), (byte) 0);

    return new DataKeyResult(
        encryptedData,
        keyResponse.ciphertextBlob().asByteArray());
}

public byte[] decryptWithEnvelope(KmsClient kmsClient,
                                  DataKeyResult encryptedEnvelope) {
    // Decrypt data key
    DecryptRequest keyDecryptRequest = DecryptRequest.builder()
        .ciphertextBlob(SdkBytes.fromByteArray(
            encryptedEnvelope.encryptedKey()))
        .build();

    DecryptResponse keyDecryptResponse = kmsClient.decrypt(keyDecryptRequest);

    // Decrypt data with decrypted key
    byte[] decryptedData = decryptWithAES(
        encryptedEnvelope.encryptedData(),
        keyDecryptResponse.plaintext().asByteArray());

    // Clear plaintext key from memory
    Arrays.fill(keyDecryptResponse.plaintext().asByteArray(), (byte) 0);

    return decryptedData;
}
```

## Digital Signatures

### Create Signing Key and Sign Data

```java
public String createAndSignData(KmsClient kmsClient, String description, String message) {
    // Create signing key
    CreateKeyRequest keyRequest = CreateKeyRequest.builder()
        .description(description)
        .keySpec(KeySpec.RSA_2048)
        .keyUsage(KeyUsageType.SIGN_VERIFY)
        .build();

    CreateKeyResponse keyResponse = kmsClient.createKey(keyRequest);
    String keyId = keyResponse.keyMetadata().keyId();

    // Sign data
    SignRequest signRequest = SignRequest.builder()
        .keyId(keyId)
        .message(SdkBytes.fromString(message, StandardCharsets.UTF_8))
        .signingAlgorithm(SigningAlgorithmSpec.RSASSA_PSS_SHA_256)
        .build();

    SignResponse signResponse = kmsClient.sign(signRequest);
    return Base64.getEncoder().encodeToString(
        signResponse.signature().asByteArray());
}
```

### Verify Signature

```java
public boolean verifySignature(KmsClient kmsClient,
                             String keyId,
                             String message,
                             String signatureBase64) {
    byte[] signature = Base64.getDecoder().decode(signatureBase64);

    VerifyRequest verifyRequest = VerifyRequest.builder()
        .keyId(keyId)
        .message(SdkBytes.fromString(message, StandardCharsets.UTF_8))
        .signature(SdkBytes.fromByteArray(signature))
        .signingAlgorithm(SigningAlgorithmSpec.RSASSA_PSS_SHA_256)
        .build();

    VerifyResponse verifyResponse = kmsClient.verify(verifyRequest);
    return verifyResponse.signatureValid();
}
```

## Spring Boot Integration

### Configuration Class

```java
@Configuration
public class KmsConfiguration {

    @Bean
    public KmsClient kmsClient() {
        return KmsClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }

    @Bean
    public KmsAsyncClient kmsAsyncClient() {
        return KmsAsyncClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }
}
```

### Encryption Service

```java
@Service
@RequiredArgsConstructor
public class KmsEncryptionService {

    private final KmsClient kmsClient;

    @Value("${kms.encryption-key-id}")
    private String keyId;

    public String encrypt(String plaintext) {
        try {
            EncryptRequest request = EncryptRequest.builder()
                .keyId(keyId)
                .plaintext(SdkBytes.fromString(plaintext, StandardCharsets.UTF_8))
                .build();

            EncryptResponse response = kmsClient.encrypt(request);
            return Base64.getEncoder().encodeToString(
                response.ciphertextBlob().asByteArray());

        } catch (KmsException e) {
            throw new RuntimeException("Encryption failed", e);
        }
    }

    public String decrypt(String ciphertextBase64) {
        try {
            byte[] ciphertext = Base64.getDecoder().decode(ciphertextBase64);

            DecryptRequest request = DecryptRequest.builder()
                .ciphertextBlob(SdkBytes.fromByteArray(ciphertext))
                .build();

            DecryptResponse response = kmsClient.decrypt(request);
            return response.plaintext().asString(StandardCharsets.UTF_8);

        } catch (KmsException e) {
            throw new RuntimeException("Decryption failed", e);
        }
    }
}
```

## Examples

### Basic Encryption Example

```java
public class BasicEncryptionExample {
    public static void main(String[] args) {
        KmsClient kmsClient = KmsClient.builder()
            .region(Region.US_EAST_1)
            .build();

        // Create key
        String keyId = createEncryptionKey(kmsClient, "Example encryption key");
        System.out.println("Created key: " + keyId);

        // Encrypt and decrypt
        String plaintext = "Hello, World!";
        String encrypted = encryptData(kmsClient, keyId, plaintext);
        String decrypted = decryptData(kmsClient, encrypted);

        System.out.println("Original: " + plaintext);
        System.out.println("Decrypted: " + decrypted);
    }
}
```

### Envelope Encryption Example

```java
public class EnvelopeEncryptionExample {
    public static void main(String[] args) {
        KmsClient kmsClient = KmsClient.builder()
            .region(Region.US_EAST_1)
            .build();

        String masterKeyId = "alias/your-master-key";
        String largeData = "This is a large amount of data that needs encryption...";
        byte[] data = largeData.getBytes(StandardCharsets.UTF_8);

        // Encrypt using envelope pattern
        DataKeyResult encryptedEnvelope = encryptWithEnvelope(
            kmsClient, masterKeyId, data);

        // Decrypt
        byte[] decryptedData = decryptWithEnvelope(
            kmsClient, encryptedEnvelope);

        String result = new String(decryptedData, StandardCharsets.UTF_8);
        System.out.println("Decrypted: " + result);
    }
}
```

## Best Practices

### Security
- **Always use envelope encryption for large data** - Encrypt data locally and only encrypt the data key with KMS
- **Use encryption context** - Add contextual information to track and audit usage
- **Never log sensitive data** - Avoid logging plaintext or encryption keys
- **Implement proper key lifecycle** - Enable automatic rotation and set deletion policies
- **Use separate keys for different purposes** - Don't reuse keys across multiple applications

### Performance
- **Cache encrypted data keys** - Reduce KMS API calls by caching data keys
- **Use async operations** - Leverage async clients for non-blocking I/O
- **Reuse client instances** - Don't create new clients for each operation
- **Implement connection pooling** - Configure proper connection pooling settings

### Error Handling
- **Implement retry logic** - Handle throttling exceptions with exponential backoff
- **Check key states** - Verify key is enabled before performing operations
- **Use circuit breakers** - Prevent cascading failures during KMS outages
- **Log errors comprehensively** - Include KMS error codes and context

## References

For detailed implementation patterns, advanced techniques, and comprehensive examples:

- @references/technical-guide.md - Complete technical implementation patterns
- @references/spring-boot-integration.md - Spring Boot integration patterns
- @references/testing.md - Testing strategies and examples
- @references/best-practices.md - Security and operational best practices

## Related Skills

- @aws-sdk-java-v2-core - Core AWS SDK patterns and configuration
- @aws-sdk-java-v2-dynamodb - DynamoDB integration patterns
- @aws-sdk-java-v2-secrets-manager - Secrets management patterns
- @spring-boot-dependency-injection - Spring dependency injection patterns

## External References

- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [AWS SDK for Java 2.x Documentation](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html)
- [KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)