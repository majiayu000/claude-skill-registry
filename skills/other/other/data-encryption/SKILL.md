---
name: data-encryption
description: Implement strong encryption using AES, RSA, TLS, and proper key management. Use when securing data at rest, in transit, or implementing end-to-end encryption.
---

# Data Encryption

## Overview

Implement robust encryption strategies for protecting sensitive data at rest and in transit using industry-standard cryptographic algorithms and key management practices.

## When to Use

- Sensitive data storage
- Database encryption
- File encryption
- Communication security
- Compliance requirements (GDPR, HIPAA, PCI-DSS)
- Password storage
- End-to-end encryption

## Implementation Examples

### 1. **Node.js Encryption Library**

```javascript
// encryption-service.js
const crypto = require('crypto');
const fs = require('fs').promises;

class EncryptionService {
  constructor() {
    // AES-256-GCM for symmetric encryption
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32; // 256 bits
    this.ivLength = 16; // 128 bits
    this.saltLength = 64;
    this.tagLength = 16;
  }

  /**
   * Generate a cryptographically secure random key
   */
  generateKey() {
    return crypto.randomBytes(this.keyLength);
  }

  /**
   * Derive a key from a password using PBKDF2
   */
  async deriveKey(password, salt = null) {
    if (!salt) {
      salt = crypto.randomBytes(this.saltLength);
    }

    return new Promise((resolve, reject) => {
      crypto.pbkdf2(
        password,
        salt,
        100000, // iterations
        this.keyLength,
        'sha512',
        (err, derivedKey) => {
          if (err) reject(err);
          else resolve({ key: derivedKey, salt });
        }
      );
    });
  }

  /**
   * Encrypt data using AES-256-GCM
   */
  encrypt(data, key) {
    const iv = crypto.randomBytes(this.ivLength);
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);

    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const tag = cipher.getAuthTag();

    // Return IV + encrypted data + auth tag
    return {
      encrypted: encrypted,
      iv: iv.toString('hex'),
      tag: tag.toString('hex')
    };
  }

  /**
   * Decrypt data using AES-256-GCM
   */
  decrypt(encryptedData, key, iv, tag) {
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      key,
      Buffer.from(iv, 'hex')
    );

    decipher.setAuthTag(Buffer.from(tag, 'hex'));

    let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }

  /**
   * Encrypt file
   */
  async encryptFile(inputPath, outputPath, key) {
    const iv = crypto.randomBytes(this.ivLength);
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);

    const input = await fs.readFile(inputPath);
    const encrypted = Buffer.concat([
      cipher.update(input),
      cipher.final()
    ]);

    const tag = cipher.getAuthTag();

    // Write IV + encrypted data + auth tag
    const output = Buffer.concat([iv, encrypted, tag]);
    await fs.writeFile(outputPath, output);

    return { iv: iv.toString('hex'), tag: tag.toString('hex') };
  }

  /**
   * Decrypt file
   */
  async decryptFile(inputPath, outputPath, key) {
    const data = await fs.readFile(inputPath);

    const iv = data.subarray(0, this.ivLength);
    const tag = data.subarray(data.length - this.tagLength);
    const encrypted = data.subarray(this.ivLength, data.length - this.tagLength);

    const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
    decipher.setAuthTag(tag);

    const decrypted = Buffer.concat([
      decipher.update(encrypted),
      decipher.final()
    ]);

    await fs.writeFile(outputPath, decrypted);
  }

  /**
   * Hash password using bcrypt-style approach
   */
  async hashPassword(password) {
    const salt = crypto.randomBytes(16);

    return new Promise((resolve, reject) => {
      crypto.pbkdf2(
        password,
        salt,
        100000,
        64,
        'sha512',
        (err, hash) => {
          if (err) reject(err);
          else {
            const combined = Buffer.concat([salt, hash]);
            resolve(combined.toString('hex'));
          }
        }
      );
    });
  }

  /**
   * Verify password hash
   */
  async verifyPassword(password, hashedPassword) {
    const combined = Buffer.from(hashedPassword, 'hex');
    const salt = combined.subarray(0, 16);
    const hash = combined.subarray(16);

    return new Promise((resolve, reject) => {
      crypto.pbkdf2(
        password,
        salt,
        100000,
        64,
        'sha512',
        (err, derivedHash) => {
          if (err) reject(err);
          else resolve(crypto.timingSafeEqual(hash, derivedHash));
        }
      );
    });
  }

  /**
   * Generate RSA key pair
   */
  generateKeyPair() {
    return crypto.generateKeyPairSync('rsa', {
      modulusLength: 4096,
      publicKeyEncoding: {
        type: 'spki',
        format: 'pem'
      },
      privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
        cipher: 'aes-256-cbc',
        passphrase: process.env.KEY_PASSPHRASE || 'top-secret'
      }
    });
  }

  /**
   * Encrypt with public key (RSA)
   */
  encryptWithPublicKey(data, publicKey) {
    return crypto.publicEncrypt(
      {
        key: publicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256'
      },
      Buffer.from(data)
    );
  }

  /**
   * Decrypt with private key (RSA)
   */
  decryptWithPrivateKey(encrypted, privateKey) {
    return crypto.privateDecrypt(
      {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256'
      },
      encrypted
    );
  }
}

// Usage examples
async function main() {
  const encryptionService = new EncryptionService();

  // 1. Symmetric encryption
  const key = encryptionService.generateKey();
  const encrypted = encryptionService.encrypt('Secret message', key);
  console.log('Encrypted:', encrypted);

  const decrypted = encryptionService.decrypt(
    encrypted.encrypted,
    key,
    encrypted.iv,
    encrypted.tag
  );
  console.log('Decrypted:', decrypted);

  // 2. Password-based encryption
  const { key: derivedKey, salt } = await encryptionService.deriveKey('myPassword');
  const passwordEncrypted = encryptionService.encrypt('Data', derivedKey);
  console.log('Password encrypted:', passwordEncrypted);

  // 3. Password hashing
  const hashedPassword = await encryptionService.hashPassword('userPassword123');
  const isValid = await encryptionService.verifyPassword('userPassword123', hashedPassword);
  console.log('Password valid:', isValid);

  // 4. RSA encryption
  const { publicKey, privateKey } = encryptionService.generateKeyPair();
  const rsaEncrypted = encryptionService.encryptWithPublicKey('Secret', publicKey);
  const rsaDecrypted = encryptionService.decryptWithPrivateKey(rsaEncrypted, privateKey);
  console.log('RSA decrypted:', rsaDecrypted.toString());
}

main().catch(console.error);

module.exports = EncryptionService;
```

### 2. **Python Cryptography Implementation**

```python
# encryption_service.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os
import base64
from typing import Tuple, Dict

class EncryptionService:
    def __init__(self):
        self.backend = default_backend()

    def generate_key(self) -> bytes:
        """Generate a random 256-bit key"""
        return os.urandom(32)

    def derive_key(self, password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """Derive encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )

        key = kdf.derive(password.encode())
        return key, salt

    def encrypt_aes_gcm(self, plaintext: bytes, key: bytes) -> Dict[str, str]:
        """Encrypt data using AES-256-GCM"""
        iv = os.urandom(12)  # 96-bit IV for GCM

        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=self.backend
        )

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }

    def decrypt_aes_gcm(self, ciphertext: str, key: bytes, iv: str, tag: str) -> bytes:
        """Decrypt data using AES-256-GCM"""
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(
                base64.b64decode(iv),
                base64.b64decode(tag)
            ),
            backend=self.backend
        )

        decryptor = cipher.decryptor()
        plaintext = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()

        return plaintext

    def encrypt_file(self, input_path: str, output_path: str, key: bytes) -> None:
        """Encrypt file using AES-256-GCM"""
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        result = self.encrypt_aes_gcm(plaintext, key)

        # Write IV + ciphertext + tag
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(result['iv']))
            f.write(base64.b64decode(result['ciphertext']))
            f.write(base64.b64decode(result['tag']))

    def decrypt_file(self, input_path: str, output_path: str, key: bytes) -> None:
        """Decrypt file using AES-256-GCM"""
        with open(input_path, 'rb') as f:
            data = f.read()

        iv = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]

        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=self.backend
        )

        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(output_path, 'wb') as f:
            f.write(plaintext)

    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=self.backend
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(b'passphrase')
        )

        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem, public_pem

    def encrypt_rsa(self, plaintext: bytes, public_key_pem: bytes) -> bytes:
        """Encrypt with RSA public key"""
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=self.backend
        )

        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext

    def decrypt_rsa(self, ciphertext: bytes, private_key_pem: bytes, passphrase: bytes) -> bytes:
        """Decrypt with RSA private key"""
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=passphrase,
            backend=self.backend
        )

        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext

# Usage
if __name__ == '__main__':
    service = EncryptionService()

    # AES encryption
    key = service.generate_key()
    encrypted = service.encrypt_aes_gcm(b'Secret data', key)
    print(f"Encrypted: {encrypted['ciphertext']}")

    decrypted = service.decrypt_aes_gcm(
        encrypted['ciphertext'],
        key,
        encrypted['iv'],
        encrypted['tag']
    )
    print(f"Decrypted: {decrypted.decode()}")

    # Password-based encryption
    password = "mySecurePassword"
    key, salt = service.derive_key(password)
    print(f"Derived key: {base64.b64encode(key).decode()}")

    # RSA encryption
    private_key, public_key = service.generate_rsa_keypair()
    rsa_encrypted = service.encrypt_rsa(b'Secret message', public_key)
    rsa_decrypted = service.decrypt_rsa(rsa_encrypted, private_key, b'passphrase')
    print(f"RSA decrypted: {rsa_decrypted.decode()}")
```

### 3. **Database Encryption (PostgreSQL)**

```sql
-- Database-level encryption using pgcrypto

-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create table with encrypted columns
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    -- Encrypted sensitive data
    ssn BYTEA,
    credit_card BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert encrypted data
INSERT INTO users (email, ssn, credit_card)
VALUES (
    'user@example.com',
    pgp_sym_encrypt('123-45-6789', 'encryption-key'),
    pgp_sym_encrypt('4111-1111-1111-1111', 'encryption-key')
);

-- Query encrypted data
SELECT
    email,
    pgp_sym_decrypt(ssn, 'encryption-key') AS ssn,
    pgp_sym_decrypt(credit_card, 'encryption-key') AS credit_card
FROM users
WHERE email = 'user@example.com';

-- Create function for transparent encryption
CREATE OR REPLACE FUNCTION encrypt_sensitive_data()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ssn IS NOT NULL THEN
        NEW.ssn := pgp_sym_encrypt(NEW.ssn::TEXT, current_setting('app.encryption_key'));
    END IF;

    IF NEW.credit_card IS NOT NULL THEN
        NEW.credit_card := pgp_sym_encrypt(NEW.credit_card::TEXT, current_setting('app.encryption_key'));
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger
CREATE TRIGGER encrypt_before_insert
    BEFORE INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION encrypt_sensitive_data();
```

### 4. **TLS/SSL Configuration**

```javascript
// tls-server.js - HTTPS server with strong TLS
const https = require('https');
const fs = require('fs');

const tlsOptions = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem'),
  ca: fs.readFileSync('ca-cert.pem'), // Certificate authority

  // TLS version restrictions
  minVersion: 'TLSv1.2',
  maxVersion: 'TLSv1.3',

  // Strong cipher suites
  ciphers: [
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'TLS_AES_128_GCM_SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES128-GCM-SHA256'
  ].join(':'),

  // Prefer server cipher order
  honorCipherOrder: true,

  // Require client certificate (mutual TLS)
  requestCert: true,
  rejectUnauthorized: true
};

const server = https.createServer(tlsOptions, (req, res) => {
  // Verify client certificate
  const cert = req.socket.getPeerCertificate();

  if (req.client.authorized) {
    res.writeHead(200);
    res.end('Secure connection established');
  } else {
    res.writeHead(401);
    res.end('Unauthorized');
  }
});

server.listen(443, () => {
  console.log('Secure server running on port 443');
});
```

## Best Practices

### ✅ DO
- Use AES-256-GCM for symmetric encryption
- Use RSA-4096 or ECC for asymmetric encryption
- Implement proper key rotation
- Use secure key storage (HSM, KMS)
- Salt and hash passwords
- Use TLS 1.2+ for transit encryption
- Implement key derivation (PBKDF2, Argon2)
- Use authenticated encryption

### ❌ DON'T
- Roll your own crypto
- Store keys in code
- Use ECB mode
- Use MD5 or SHA1
- Reuse IVs/nonces
- Use weak key lengths
- Skip authentication tags

## Encryption Standards

- **AES-256**: Symmetric encryption
- **RSA-4096**: Asymmetric encryption
- **ECDSA/EdDSA**: Digital signatures
- **TLS 1.3**: Transport security
- **PBKDF2/Argon2**: Key derivation
- **HMAC-SHA256**: Message authentication

## Resources

- [NIST Cryptographic Standards](https://csrc.nist.gov/publications/fips)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Node.js Crypto Documentation](https://nodejs.org/api/crypto.html)
- [Python Cryptography Library](https://cryptography.io/)
