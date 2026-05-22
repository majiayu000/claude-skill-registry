---
name: Cosmian KMS
description: Expert guidance for Cosmian Key Management System including key generation, certificate management, encryption operations, access policies, and KMS CLI operations. Use this when working with Cosmian KMS, cryptographic key management, or Cosmian-specific PKI operations.
---

# Cosmian KMS

Expert assistance with Cosmian Key Management System operations and workflows.

## Overview

Cosmian KMS is an open-source Key Management System (KMS) that provides:
- Secure key generation and storage
- Certificate lifecycle management
- Encryption/decryption operations
- Access control policies
- Support for various cryptographic algorithms
- KMIP protocol support
- REST API and CLI interface

## Installation & Setup

### Install Cosmian KMS CLI
```bash
# Install ckms CLI
# Check https://github.com/Cosmian/kms for latest installation instructions

# Configure KMS server connection
ckms config --server-url https://kms.example.com:9998

# With authentication
ckms config --server-url https://kms.example.com:9998 --access-token <token>

# Verify connection
ckms version
```

### Server Configuration
```bash
# Start KMS server (if running locally)
cosmian_kms_server --database-type sqlite --sqlite-path /path/to/kms.db

# With specific port
cosmian_kms_server --port 9998

# Enable HTTPS
cosmian_kms_server --https-p12-file cert.p12 --https-p12-password <password>
```

## Key Management

### Generate Keys

#### Symmetric Keys
```bash
# Generate AES key (256-bit)
ckms sym keys create --algorithm aes --key-size 256 --tag production

# Generate with specific identifier
ckms sym keys create --algorithm aes --key-size 256 --id my-key-id

# Generate ChaCha20 key
ckms sym keys create --algorithm chacha20
```

#### Asymmetric Keys
```bash
# Generate RSA key pair (4096-bit)
ckms rsa keys create --size 4096 --tag production

# Generate EC key pair (P-256)
ckms ec keys create --curve nist-p256

# Generate EC key pair (P-384, more secure)
ckms ec keys create --curve nist-p384

# Generate with tags for organization
ckms rsa keys create --size 4096 --tag "env:prod" --tag "app:api"
```

#### Covercrypt Keys
```bash
# Generate Covercrypt master keys (for policy-based encryption)
ckms cc keys create-master-key-pair --policy policy.json

# Generate user decryption key
ckms cc keys create-user-key --master-private-key-id <id> --access-policy "dept::IT && level::confidential"
```

### List Keys
```bash
# List all keys
ckms keys list

# Filter by tag
ckms keys list --tag production

# Filter by algorithm
ckms keys list --algorithm rsa

# Show detailed information
ckms keys list --detailed
```

### Export Keys
```bash
# Export public key
ckms keys export --key-id <id> --output-file public.pem

# Export private key (requires authorization)
ckms keys export --key-id <id> --output-file private.pem --unwrap

# Export in specific format
ckms keys export --key-id <id> --format pkcs8 --output-file key.p8
```

### Import Keys
```bash
# Import key from file
ckms keys import --key-file key.pem --tag imported

# Import with specific ID
ckms keys import --key-file key.pem --key-id my-imported-key

# Import wrapped key
ckms keys import --key-file wrapped-key.bin --wrapping-key-id <wrap-key-id>
```

### Key Operations
```bash
# Revoke key
ckms keys revoke --key-id <id> --revocation-reason "key-compromise"

# Destroy key (permanent)
ckms keys destroy --key-id <id>

# Rekey (rotate key)
ckms keys rekey --key-id <id>

# Get key attributes
ckms keys get --key-id <id>
```

## Certificate Management

### Generate Certificate
```bash
# Create certificate from existing key
ckms certificates certify --key-id <key-id> \
  --subject "CN=example.com,O=MyOrg,C=US" \
  --days 365

# Generate self-signed certificate
ckms certificates certify --key-id <key-id> \
  --subject "CN=example.com" \
  --self-signed \
  --days 365

# Certificate with SAN
ckms certificates certify --key-id <key-id> \
  --subject "CN=example.com" \
  --san "DNS:example.com" \
  --san "DNS:www.example.com" \
  --san "IP:192.168.1.1" \
  --days 365
```

### Certificate Signing Request (CSR)
```bash
# Generate CSR
ckms certificates request --key-id <key-id> \
  --subject "CN=example.com,O=MyOrg,C=US" \
  --output-file request.csr

# Import and sign CSR
ckms certificates import --certificate-file request.csr --tag csr

# Sign CSR with CA key
ckms certificates sign --csr-id <csr-id> \
  --ca-key-id <ca-key-id> \
  --days 365
```

### Certificate Operations
```bash
# List certificates
ckms certificates list

# Export certificate
ckms certificates export --certificate-id <id> --output-file cert.pem

# Import certificate
ckms certificates import --certificate-file cert.pem --tag imported

# Validate certificate
ckms certificates validate --certificate-id <id>

# Revoke certificate
ckms certificates revoke --certificate-id <id>
```

## Encryption & Decryption

### Symmetric Encryption
```bash
# Encrypt file
ckms sym encrypt --key-id <key-id> --input-file plaintext.txt --output-file encrypted.bin

# Decrypt file
ckms sym decrypt --key-id <key-id> --input-file encrypted.bin --output-file plaintext.txt

# Encrypt with authentication
ckms sym encrypt --key-id <key-id> --input-file data.txt --output-file encrypted.bin --authenticated-data "metadata"
```

### Asymmetric Encryption
```bash
# Encrypt with public key
ckms rsa encrypt --key-id <public-key-id> --input-file plaintext.txt --output-file encrypted.bin

# Decrypt with private key
ckms rsa decrypt --key-id <private-key-id> --input-file encrypted.bin --output-file plaintext.txt
```

### Covercrypt (Policy-Based Encryption)
```bash
# Encrypt with access policy
ckms cc encrypt --key-id <master-public-key-id> \
  --encryption-policy "dept::IT && level::confidential" \
  --input-file sensitive.txt \
  --output-file encrypted.bin

# Decrypt with user key
ckms cc decrypt --key-id <user-key-id> \
  --input-file encrypted.bin \
  --output-file decrypted.txt
```

## Access Control

### Manage Permissions
```bash
# Grant access to key
ckms access grant --key-id <key-id> --user <username> --operations "encrypt,decrypt"

# Revoke access
ckms access revoke --key-id <key-id> --user <username>

# List access permissions
ckms access list --key-id <key-id>

# Grant admin access
ckms access grant --key-id <key-id> --user <username> --operations "*"
```

### Tags & Organization
```bash
# Add tags to key
ckms keys tag --key-id <id> --tag "environment:production" --tag "team:backend"

# Remove tag
ckms keys untag --key-id <id> --tag "environment:production"

# Search by tag
ckms keys list --tag "environment:production"
```

## Advanced Operations

### Key Wrapping
```bash
# Wrap key with another key (for secure export)
ckms keys wrap --key-id <key-to-wrap> --wrapping-key-id <wrapping-key-id> --output-file wrapped.bin

# Unwrap key
ckms keys unwrap --wrapped-key-file wrapped.bin --wrapping-key-id <wrapping-key-id>
```

### Batch Operations
```bash
# Import multiple keys from directory
for key in /path/to/keys/*.pem; do
  ckms keys import --key-file "$key" --tag batch-import
done

# Export multiple keys
ckms keys list --tag production | while read key_id; do
  ckms keys export --key-id "$key_id" --output-file "backup/${key_id}.pem"
done
```

### Audit & Logging
```bash
# View key history
ckms keys history --key-id <id>

# Export audit logs (if supported)
ckms audit export --start-date 2024-01-01 --end-date 2024-12-31
```

## REST API Usage

### API Authentication
```bash
# Set API token
export COSMIAN_KMS_TOKEN="your-api-token"

# Or configure in CLI
ckms config --access-token "your-api-token"
```

### API Examples
```bash
# Create key via API
curl -X POST https://kms.example.com:9998/kmip/2_1 \
  -H "Authorization: Bearer $COSMIAN_KMS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tag": "CreateKeyPair",
    "type": "Request",
    "batch_count": 1,
    "batch_item": [{
      "operation": "CreateKeyPair",
      "request_payload": {
        "common_attributes": {
          "cryptographic_algorithm": "RSA",
          "cryptographic_length": 4096
        }
      }
    }]
  }'

# Get key
curl -X POST https://kms.example.com:9998/kmip/2_1 \
  -H "Authorization: Bearer $COSMIAN_KMS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tag": "Get",
    "type": "Request",
    "batch_item": [{
      "operation": "Get",
      "request_payload": {
        "unique_identifier": "<key-id>"
      }
    }]
  }'
```

## Integration Examples

### Python Integration
```python
from cosmian_kms import KmsClient

# Initialize client
kms = KmsClient("https://kms.example.com:9998", api_key="token")

# Generate key
key_id = kms.create_symmetric_key(algorithm="AES", key_size=256)

# Encrypt data
ciphertext = kms.encrypt(key_id, b"sensitive data")

# Decrypt data
plaintext = kms.decrypt(key_id, ciphertext)
```

### Go Integration
```go
import "github.com/cosmian/kms-go-client"

// Initialize client
client := kms.NewClient("https://kms.example.com:9998", "token")

// Create RSA key pair
privateKeyID, publicKeyID, err := client.CreateRSAKeyPair(4096)

// Encrypt
ciphertext, err := client.Encrypt(publicKeyID, plaintext)

// Decrypt
plaintext, err := client.Decrypt(privateKeyID, ciphertext)
```

## Best Practices

1. **Key Organization**: Use meaningful tags and IDs for keys
2. **Access Control**: Apply principle of least privilege
3. **Key Rotation**: Regularly rotate encryption keys
4. **Backup**: Securely backup master keys and CA certificates
5. **Audit**: Enable and monitor audit logs
6. **HSM Integration**: Use HSM for production CA keys
7. **Policy Management**: Use Covercrypt policies for fine-grained access control
8. **Key Wrapping**: Always wrap keys for export/backup
9. **Revocation**: Revoke compromised keys immediately
10. **Testing**: Test key operations in development before production

## Common Workflows

### Setup Production Environment
```bash
# 1. Generate CA key pair
ckms rsa keys create --size 4096 --tag "ca" --tag "prod" --id prod-ca-key

# 2. Create self-signed CA certificate
ckms certificates certify --key-id prod-ca-key \
  --subject "CN=MyOrg Root CA,O=MyOrg,C=US" \
  --self-signed --days 3650

# 3. Generate server key
ckms rsa keys create --size 4096 --tag "server" --tag "prod"

# 4. Generate server certificate
ckms certificates certify --key-id <server-key-id> \
  --subject "CN=api.example.com,O=MyOrg,C=US" \
  --issuer-certificate-id <ca-cert-id> \
  --san "DNS:api.example.com" \
  --days 365

# 5. Export for deployment
ckms certificates export --certificate-id <server-cert-id> --output-file server.crt
ckms keys export --key-id <server-key-id> --output-file server.key
```

### Key Rotation
```bash
# 1. Generate new key
NEW_KEY=$(ckms sym keys create --algorithm aes --key-size 256 --tag "v2")

# 2. Re-encrypt data with new key
# (Application-specific logic)

# 3. Revoke old key
ckms keys revoke --key-id <old-key-id> --revocation-reason "superseded"

# 4. Archive old key (after grace period)
ckms keys destroy --key-id <old-key-id>
```

## Troubleshooting

### Connection Issues
```bash
# Test connectivity
curl -k https://kms.example.com:9998/version

# Check configuration
ckms config --show

# Verify authentication
ckms version
```

### Key Not Found
```bash
# List all keys with details
ckms keys list --detailed

# Search by tag
ckms keys list --tag <tag-name>

# Check key history
ckms keys history --key-id <id>
```

### Permission Denied
```bash
# Check key permissions
ckms access list --key-id <id>

# Verify your access
ckms keys get --key-id <id>
```

## Security Considerations

- **Network Security**: Always use HTTPS for KMS connections
- **Token Management**: Rotate API tokens regularly
- **Key Lifecycle**: Implement proper key lifecycle policies
- **Separation of Duties**: Different operators for key generation vs. usage
- **Compliance**: Ensure operations meet regulatory requirements (GDPR, HIPAA, etc.)
- **Disaster Recovery**: Have key backup and recovery procedures
- **Monitoring**: Set up alerts for suspicious key operations

## Resources

- Documentation: https://docs.cosmian.com/
- GitHub: https://github.com/Cosmian/kms
- Community: Join Cosmian community for support
