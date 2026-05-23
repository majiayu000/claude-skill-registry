---
name: tenant-data-isolation
description: Data encryption and key management patterns for tenant isolation. Covers encryption at rest, tenant-specific keys, and secure key management.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Tenant Data Isolation Skill

## When to Use This Skill

Use this skill when:

- **Tenant Data Isolation tasks** - Working on data encryption and key management patterns for tenant isolation. covers encryption at rest, tenant-specific keys, and secure key management
- **Planning or design** - Need guidance on Tenant Data Isolation approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for cryptographic isolation of tenant data in multi-tenant systems.

Beyond logical isolation (RLS, schemas), cryptographic isolation ensures that even with database access, tenant data cannot be read without proper keys. This skill covers encryption strategies, key management, and isolation patterns.

## Isolation Levels

```text
+------------------------------------------------------------------+
|                   Data Isolation Spectrum                         |
+------------------------------------------------------------------+
| Level 1: Logical      | TenantId column, RLS policies            |
| Level 2: Schema       | Separate schema per tenant                |
| Level 3: Database     | Separate database per tenant              |
| Level 4: Encrypted    | Per-tenant encryption keys                |
| Level 5: HSM          | Hardware-backed key isolation             |
+------------------------------------------------------------------+
```

## Encryption Strategies

### Encryption Architecture

```text
+------------------------------------------------------------------+
|                  Key Hierarchy                                    |
+------------------------------------------------------------------+
|                                                                   |
|                    +-------------------+                          |
|                    |   Master Key      |  (HSM/Key Vault)         |
|                    |   (KEK)           |                          |
|                    +-------------------+                          |
|                            |                                      |
|            +---------------+---------------+                      |
|            |               |               |                      |
|    +-------v-----+ +-------v-----+ +-------v-----+               |
|    | Tenant A    | | Tenant B    | | Tenant C    |               |
|    | Key (DEK)   | | Key (DEK)   | | Key (DEK)   |               |
|    +-------------+ +-------------+ +-------------+               |
|            |               |               |                      |
|            v               v               v                      |
|    +-------------+ +-------------+ +-------------+               |
|    | Encrypted   | | Encrypted   | | Encrypted   |               |
|    | Data        | | Data        | | Data        |               |
|    +-------------+ +-------------+ +-------------+               |
|                                                                   |
+------------------------------------------------------------------+
```

### Per-Tenant Encryption

```csharp
public sealed class TenantEncryptionService(
    IKeyVaultService keyVault,
    IDbContext db)
{
    public async Task<byte[]> EncryptAsync(
        Guid tenantId,
        byte[] plaintext,
        CancellationToken ct)
    {
        var key = await GetOrCreateTenantKeyAsync(tenantId, ct);

        using var aes = Aes.Create();
        aes.Key = key;
        aes.GenerateIV();

        using var encryptor = aes.CreateEncryptor();
        var ciphertext = encryptor.TransformFinalBlock(plaintext, 0, plaintext.Length);

        // Prepend IV to ciphertext
        var result = new byte[aes.IV.Length + ciphertext.Length];
        Buffer.BlockCopy(aes.IV, 0, result, 0, aes.IV.Length);
        Buffer.BlockCopy(ciphertext, 0, result, aes.IV.Length, ciphertext.Length);

        return result;
    }

    public async Task<byte[]> DecryptAsync(
        Guid tenantId,
        byte[] ciphertext,
        CancellationToken ct)
    {
        var key = await GetTenantKeyAsync(tenantId, ct);

        using var aes = Aes.Create();
        aes.Key = key;

        // Extract IV from ciphertext
        var iv = new byte[16];
        Buffer.BlockCopy(ciphertext, 0, iv, 0, 16);
        aes.IV = iv;

        var encrypted = new byte[ciphertext.Length - 16];
        Buffer.BlockCopy(ciphertext, 16, encrypted, 0, encrypted.Length);

        using var decryptor = aes.CreateDecryptor();
        return decryptor.TransformFinalBlock(encrypted, 0, encrypted.Length);
    }

    private async Task<byte[]> GetOrCreateTenantKeyAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        var keyName = $"tenant-{tenantId}";

        var existingKey = await keyVault.GetKeyAsync(keyName, ct);
        if (existingKey != null)
            return existingKey;

        // Generate new DEK
        using var aes = Aes.Create();
        aes.GenerateKey();

        // Store wrapped key
        await keyVault.CreateKeyAsync(keyName, aes.Key, ct);

        return aes.Key;
    }
}
```

## Key Management

### Azure Key Vault Integration

```csharp
public sealed class AzureKeyVaultService(
    KeyClient keyClient,
    CryptographyClient cryptoClient) : IKeyVaultService
{
    public async Task<string> CreateTenantKeyAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        var keyName = $"tenant-{tenantId}";

        var key = await keyClient.CreateKeyAsync(keyName,
            KeyType.Rsa,
            new CreateRsaKeyOptions(keyName)
            {
                KeySize = 4096,
                KeyOperations = { KeyOperation.WrapKey, KeyOperation.UnwrapKey },
                ExpiresOn = DateTimeOffset.UtcNow.AddYears(2),
                Tags =
                {
                    ["tenant_id"] = tenantId.ToString(),
                    ["created_by"] = "system"
                }
            },
            ct);

        return key.Value.Id.ToString();
    }

    public async Task<byte[]> WrapKeyAsync(
        string keyId,
        byte[] dataKey,
        CancellationToken ct)
    {
        var cryptoClient = new CryptographyClient(new Uri(keyId), _credential);
        var result = await cryptoClient.WrapKeyAsync(
            KeyWrapAlgorithm.RsaOaep256,
            dataKey,
            ct);

        return result.EncryptedKey;
    }

    public async Task<byte[]> UnwrapKeyAsync(
        string keyId,
        byte[] wrappedKey,
        CancellationToken ct)
    {
        var cryptoClient = new CryptographyClient(new Uri(keyId), _credential);
        var result = await cryptoClient.UnwrapKeyAsync(
            KeyWrapAlgorithm.RsaOaep256,
            wrappedKey,
            ct);

        return result.Key;
    }
}
```

### Key Rotation

```csharp
public sealed class KeyRotationService(
    IKeyVaultService keyVault,
    IDbContext db,
    ITenantEncryptionService encryption,
    ILogger<KeyRotationService> logger)
{
    public async Task RotateTenantKeyAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        logger.LogInformation("Starting key rotation for tenant {TenantId}", tenantId);

        // Create new key version
        var newKeyId = await keyVault.CreateKeyVersionAsync(
            $"tenant-{tenantId}",
            ct);

        // Get all encrypted data for tenant
        var encryptedRecords = await db.EncryptedData
            .Where(d => d.TenantId == tenantId)
            .ToListAsync(ct);

        foreach (var record in encryptedRecords)
        {
            // Decrypt with old key
            var plaintext = await encryption.DecryptWithKeyVersionAsync(
                tenantId,
                record.KeyVersion,
                record.CipherText,
                ct);

            // Re-encrypt with new key
            var newCiphertext = await encryption.EncryptAsync(
                tenantId,
                plaintext,
                ct);

            record.CipherText = newCiphertext;
            record.KeyVersion = newKeyId;
        }

        await db.SaveChangesAsync(ct);

        // Mark old key version for deletion (after grace period)
        await keyVault.ScheduleKeyVersionDeletionAsync(
            $"tenant-{tenantId}",
            daysToRetain: 30,
            ct);

        logger.LogInformation(
            "Completed key rotation for tenant {TenantId}, rotated {Count} records",
            tenantId, encryptedRecords.Count);
    }
}
```

## Column-Level Encryption

### EF Core Value Converter

```csharp
public sealed class EncryptedStringConverter(
    ITenantContextAccessor tenantContext,
    ITenantEncryptionService encryption) : ValueConverter<string, byte[]>(
    v => EncryptValue(v, tenantContext, encryption),
    v => DecryptValue(v, tenantContext, encryption))
{
    private static byte[] EncryptValue(
        string value,
        ITenantContextAccessor tenantContext,
        ITenantEncryptionService encryption)
    {
        if (string.IsNullOrEmpty(value))
            return [];

        var plaintext = Encoding.UTF8.GetBytes(value);
        return encryption.EncryptAsync(
            tenantContext.Current!.TenantId,
            plaintext,
            CancellationToken.None).GetAwaiter().GetResult();
    }

    private static string DecryptValue(
        byte[] ciphertext,
        ITenantContextAccessor tenantContext,
        ITenantEncryptionService encryption)
    {
        if (ciphertext.Length == 0)
            return string.Empty;

        var plaintext = encryption.DecryptAsync(
            tenantContext.Current!.TenantId,
            ciphertext,
            CancellationToken.None).GetAwaiter().GetResult();

        return Encoding.UTF8.GetString(plaintext);
    }
}

// Entity configuration
public class CustomerConfiguration : IEntityTypeConfiguration<Customer>
{
    public void Configure(EntityTypeBuilder<Customer> builder)
    {
        builder.Property(c => c.SocialSecurityNumber)
            .HasConversion<EncryptedStringConverter>();

        builder.Property(c => c.BankAccountNumber)
            .HasConversion<EncryptedStringConverter>();
    }
}
```

## Bring Your Own Key (BYOK)

```csharp
public sealed class BYOKService(
    IKeyVaultService keyVault,
    IDbContext db)
{
    public async Task ImportCustomerKeyAsync(
        Guid tenantId,
        byte[] keyMaterial,
        CancellationToken ct)
    {
        // Validate key
        if (keyMaterial.Length != 32) // 256-bit AES
            throw new InvalidKeyException("Key must be 256 bits");

        // Import to Key Vault (wrapped)
        var keyId = await keyVault.ImportKeyAsync(
            $"tenant-{tenantId}-byok",
            keyMaterial,
            ct);

        // Update tenant configuration
        var tenant = await db.Tenants.FindAsync([tenantId], ct);
        if (tenant == null)
            throw new TenantNotFoundException(tenantId);

        tenant.EncryptionKeyId = keyId;
        tenant.KeyType = KeyType.CustomerManaged;
        tenant.KeyImportedAt = DateTimeOffset.UtcNow;

        await db.SaveChangesAsync(ct);
    }

    public async Task RevokeKeyAccessAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        // For BYOK, customer can revoke access
        var tenant = await db.Tenants.FindAsync([tenantId], ct);
        if (tenant?.KeyType != KeyType.CustomerManaged)
            throw new InvalidOperationException("Not a BYOK tenant");

        // Mark tenant as key-revoked
        tenant.KeyRevoked = true;
        tenant.KeyRevokedAt = DateTimeOffset.UtcNow;

        await db.SaveChangesAsync(ct);

        // Data is now inaccessible
    }
}
```

## Security Controls

```text
Key Management Security:
+------------------------------------------------------------------+
| Control                     | Implementation                     |
+-----------------------------+------------------------------------+
| Key access logging          | Azure Key Vault audit logs         |
| Separation of duties        | Key admins != app admins           |
| Key rotation policy         | Annual or on-demand                |
| HSM backing                 | Premium Key Vault / Dedicated HSM  |
| Emergency access            | Break-glass procedure              |
| Key deletion protection     | Soft-delete + purge protection     |
+-----------------------------+------------------------------------+
```

## Best Practices

```text
Tenant Encryption Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Per-tenant keys             | Blast radius limitation            |
| Key hierarchy               | Efficient key management           |
| HSM-backed keys             | Hardware security                  |
| Automatic key rotation      | Reduced exposure window            |
| BYOK option                 | Enterprise control                 |
| Encryption at rest default  | Defense in depth                   |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Shared encryption key | One breach exposes all | Per-tenant keys |
| Keys in code/config | Key exposure risk | Key Vault/HSM |
| No key rotation | Extended exposure | Automatic rotation |
| Keys in same DB | Single point of failure | Separate key storage |
| No key access audit | Can't detect misuse | Enable audit logging |

## Related Skills

- `database-isolation` - Logical isolation
- `saas-compliance-frameworks` - Encryption requirements
- `audit-logging` - Key access auditing

## MCP Research

For current patterns:

```text
perplexity: "multi-tenant encryption key management 2024" "per-tenant encryption SaaS"
microsoft-learn: "Azure Key Vault multi-tenant" "Always Encrypted column"
```
