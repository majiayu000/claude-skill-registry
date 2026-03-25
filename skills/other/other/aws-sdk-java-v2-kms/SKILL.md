---
name: aws-sdk-java-v2-kms
description: Provides AWS Key Management Service (KMS) patterns using AWS SDK for Java 2.x. Use when creating/managing encryption keys, encrypting/decrypting data, generating data keys, digital signing, key rotation, or integrating encryption into Spring Boot applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - AWS KMS (Key Management Service)

## Overview

Provides AWS KMS patterns using AWS SDK for Java 2.x. Covers key management, encryption/decryption, envelope encryption, digital signatures, and Spring Boot integration.

## Instructions

1. **Set Up IAM Permissions** - Grant kms:* actions with least privilege
2. **Create KMS Client** - Instantiate KmsClient with region and credentials
3. **Create Keys** - Use createKey() → **Verify key state is ENABLED before proceeding**
4. **Set Key Policies** - Define key usage permissions → **Test access before production**
5. **Encrypt Data** - Use encrypt() for data <4KB; **Verify ciphertext is not empty**
6. **Envelope Encryption** - For larger data, use generateDataKey() → **Verify data key generation succeeded**
7. **Digital Signatures** - Create signing keys → **Verify signatureValid=true after sign/verify**
8. **Key Rotation** - Enable auto-rotation → **Confirm rotation schedule is active**

## When to Use

- Creating/managing symmetric encryption keys for data protection
- Implementing envelope encryption for large data
- Generating data keys for local encryption with KMS-managed keys
- Setting up digital signatures with asymmetric keys
- Integrating encryption into Spring Boot applications

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
    try {
        GenerateDataKeyRequest keyRequest = GenerateDataKeyRequest.builder()
            .keyId(masterKeyId)
            .keySpec(DataKeySpec.AES_256)
            .build();

        GenerateDataKeyResponse keyResponse = kmsClient.generateDataKey(keyRequest);

        // Validate response
        if (keyResponse.plaintext() == null || keyResponse.ciphertextBlob() == null) {
            throw new IllegalStateException("Data key generation returned null");
        }

        byte[] encryptedData = encryptWithAES(data, keyResponse.plaintext().asByteArray());

        // Clear plaintext key from memory
        Arrays.fill(keyResponse.plaintext().asByteArray(), (byte) 0);

        return new DataKeyResult(encryptedData, keyResponse.ciphertextBlob().asByteArray());

    } catch (KmsException e) {
        throw new RuntimeException("Envelope encryption failed: " + e.awsErrorDetails().errorCode(), e);
    }
}

public byte[] decryptWithEnvelope(KmsClient kmsClient, DataKeyResult encryptedEnvelope) {
    try {
        DecryptRequest keyDecryptRequest = DecryptRequest.builder()
            .ciphertextBlob(SdkBytes.fromByteArray(encryptedEnvelope.encryptedKey()))
            .build();

        DecryptResponse keyDecryptResponse = kmsClient.decrypt(keyDecryptRequest);

        // Validate response
        if (keyDecryptResponse.plaintext() == null) {
            throw new IllegalStateException("Key decryption returned null");
        }

        byte[] decryptedData = decryptWithAES(
            encryptedEnvelope.encryptedData(),
            keyDecryptResponse.plaintext().asByteArray());

        // Clear plaintext key from memory
        Arrays.fill(keyDecryptResponse.plaintext().asByteArray(), (byte) 0);

        return decryptedData;

    } catch (KmsException e) {
        throw new RuntimeException("Envelope decryption failed: " + e.awsErrorDetails().errorCode(), e);
    }
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

- `@`aws-sdk-java-v2-core - Core AWS SDK patterns and configuration
- `@`aws-sdk-java-v2-dynamodb - DynamoDB integration patterns
- `@`aws-sdk-java-v2-secrets-manager - Secrets management patterns
- `@`spring-boot-dependency-injection - Spring dependency injection patterns

## External References

- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [AWS SDK for Java 2.x Documentation](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html)
- [KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)

## Constraints and Warnings

- **Data Size Limit**: Direct encryption limited to 4KB; use envelope encryption for larger data
- **Key Usage Limits**: KMS has quotas on API calls per second
- **Key Material**: Imported key material cannot be managed by AWS for rotation
- **Key Deletion**: Key deletion requires 7-30 day waiting period
- **Regional Boundaries**: KMS keys cannot be used across regions
- **Cost Considerations**: KMS charges per API call and for key storage
- **Asymmetric Keys**: Not all regions support asymmetric key types
- **Key Policies**: Changes to key policies require careful IAM review
- **Envelope Encryption**: Proper implementation required for data key security
- **Logging**: Enable CloudTrail to audit all KMS API usage