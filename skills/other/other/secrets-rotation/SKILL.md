---
name: secrets-rotation
description: Implement automated secrets rotation for API keys, credentials, certificates, and encryption keys. Use when managing secrets lifecycle, compliance requirements, or security hardening.
---

# Secrets Rotation

## Overview

Implement automated secrets rotation strategy for credentials, API keys, certificates, and encryption keys with zero-downtime deployment and comprehensive audit logging.

## When to Use

- API key management
- Database credentials
- TLS/SSL certificates
- Encryption key rotation
- Compliance requirements
- Security incident response
- Service account management

## Implementation Examples

### 1. **Node.js Secrets Manager with Rotation**

```javascript
// secrets-manager.js
const AWS = require('aws-sdk');
const crypto = require('crypto');

class SecretsManager {
  constructor() {
    this.secretsManager = new AWS.SecretsManager({
      region: process.env.AWS_REGION
    });

    this.rotationSchedule = new Map();
  }

  /**
   * Generate new secret value
   */
  generateSecret(type = 'api_key', length = 32) {
    switch (type) {
      case 'api_key':
        return crypto.randomBytes(length).toString('hex');

      case 'password':
        // Generate strong password
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
        let password = '';
        for (let i = 0; i < length; i++) {
          password += chars.charAt(crypto.randomInt(chars.length));
        }
        return password;

      case 'jwt_secret':
        return crypto.randomBytes(64).toString('base64');

      default:
        return crypto.randomBytes(length).toString('base64');
    }
  }

  /**
   * Store secret in AWS Secrets Manager
   */
  async createSecret(name, value, description = '') {
    const params = {
      Name: name,
      SecretString: JSON.stringify(value),
      Description: description
    };

    try {
      const result = await this.secretsManager.createSecret(params).promise();
      return result;
    } catch (error) {
      if (error.code === 'ResourceExistsException') {
        // Update existing secret
        return this.updateSecret(name, value);
      }
      throw error;
    }
  }

  /**
   * Retrieve secret
   */
  async getSecret(name) {
    const params = { SecretId: name };

    try {
      const data = await this.secretsManager.getSecretValue(params).promise();

      if ('SecretString' in data) {
        return JSON.parse(data.SecretString);
      }

      // Binary secret
      const buff = Buffer.from(data.SecretBinary, 'base64');
      return buff.toString('ascii');
    } catch (error) {
      console.error(`Error retrieving secret ${name}:`, error);
      throw error;
    }
  }

  /**
   * Update secret value
   */
  async updateSecret(name, value) {
    const params = {
      SecretId: name,
      SecretString: JSON.stringify(value)
    };

    return this.secretsManager.updateSecret(params).promise();
  }

  /**
   * Rotate secret with zero downtime
   */
  async rotateSecret(name, type = 'api_key') {
    console.log(`Starting rotation for secret: ${name}`);

    try {
      // Step 1: Generate new secret
      const newValue = this.generateSecret(type);

      // Step 2: Store new version
      const currentSecret = await this.getSecret(name);

      // Keep old value temporarily for graceful transition
      const secretWithRotation = {
        current: newValue,
        previous: currentSecret.current || currentSecret,
        rotatedAt: new Date().toISOString()
      };

      await this.updateSecret(name, secretWithRotation);

      console.log(`New secret version created for: ${name}`);

      // Step 3: Wait for applications to pick up new secret
      await this.waitForPropagation(5000);

      // Step 4: Verify new secret works
      const verificationPassed = await this.verifySecret(name, newValue);

      if (!verificationPassed) {
        throw new Error('Secret verification failed');
      }

      // Step 5: Remove previous version after grace period
      setTimeout(async () => {
        await this.updateSecret(name, {
          current: newValue,
          rotatedAt: new Date().toISOString()
        });
        console.log(`Rotation completed for: ${name}`);
      }, 300000); // 5 minutes grace period

      return {
        success: true,
        secretName: name,
        rotatedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error(`Rotation failed for ${name}:`, error);

      // Rollback on failure
      await this.rollbackRotation(name);

      throw error;
    }
  }

  /**
   * Schedule automatic rotation
   */
  async scheduleRotation(name, intervalDays = 90) {
    const intervalMs = intervalDays * 24 * 60 * 60 * 1000;

    const rotationJob = setInterval(async () => {
      try {
        await this.rotateSecret(name);
        console.log(`Scheduled rotation completed for: ${name}`);
      } catch (error) {
        console.error(`Scheduled rotation failed for ${name}:`, error);
        // Alert operations team
        this.sendAlert(name, error);
      }
    }, intervalMs);

    this.rotationSchedule.set(name, rotationJob);

    // AWS Secrets Manager automatic rotation
    const params = {
      SecretId: name,
      RotationLambdaARN: process.env.ROTATION_LAMBDA_ARN,
      RotationRules: {
        AutomaticallyAfterDays: intervalDays
      }
    };

    await this.secretsManager.rotateSecret(params).promise();
  }

  /**
   * Rotate database credentials
   */
  async rotateDatabaseCredentials(secretName) {
    const credentials = await this.getSecret(secretName);

    // Generate new password
    const newPassword = this.generateSecret('password', 20);

    // Update database user password
    const connection = await this.connectToDatabase(credentials);

    await connection.query(
      'ALTER USER ? IDENTIFIED BY ?',
      [credentials.username, newPassword]
    );

    // Update secret
    await this.updateSecret(secretName, {
      username: credentials.username,
      password: newPassword,
      host: credentials.host,
      database: credentials.database,
      rotatedAt: new Date().toISOString()
    });

    await connection.end();

    return { success: true };
  }

  /**
   * Rotate TLS certificate
   */
  async rotateTLSCertificate(domain) {
    // Use Let's Encrypt or internal CA
    const certbot = require('certbot');

    try {
      // Request new certificate
      const newCert = await certbot.certonly({
        domains: [domain],
        email: process.env.ADMIN_EMAIL,
        agreeTos: true,
        renewByDefault: true
      });

      // Store in secrets manager
      await this.createSecret(`tls-cert-${domain}`, {
        certificate: newCert.certificate,
        privateKey: newCert.privateKey,
        chain: newCert.chain,
        issuedAt: new Date().toISOString(),
        expiresAt: newCert.expiresAt
      });

      // Update load balancer/web server
      await this.updateServerCertificate(domain, newCert);

      console.log(`TLS certificate rotated for: ${domain}`);

      return { success: true };
    } catch (error) {
      console.error('Certificate rotation failed:', error);
      throw error;
    }
  }

  async waitForPropagation(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async verifySecret(name, value) {
    // Implement verification logic
    // Test API call, database connection, etc.
    return true;
  }

  async rollbackRotation(name) {
    // Restore previous version
    console.log(`Rolling back rotation for: ${name}`);
  }

  async sendAlert(secretName, error) {
    // Send to monitoring system
    console.error(`ALERT: Rotation failed for ${secretName}`, error);
  }

  async connectToDatabase(credentials) {
    // Database connection logic
    return null;
  }

  async updateServerCertificate(domain, cert) {
    // Update server configuration
    return null;
  }
}

// Usage
const secretsManager = new SecretsManager();

// Rotate API key
async function rotateAPIKey() {
  await secretsManager.rotateSecret('api-key-external-service', 'api_key');
}

// Schedule automatic rotation
async function setupRotationSchedule() {
  await secretsManager.scheduleRotation('database-credentials', 90);
  await secretsManager.scheduleRotation('api-keys', 30);
}

// Rotate database credentials
async function rotateDatabaseCreds() {
  await secretsManager.rotateDatabaseCredentials('rds-production');
}

module.exports = SecretsManager;
```

### 2. **Python Secrets Rotation with Vault**

```python
# secrets_rotation.py
import hvac
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Any
import psycopg2
import boto3

class SecretsRotation:
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_client = hvac.Client(url=vault_url, token=vault_token)
        self.ssm = boto3.client('ssm')

    def generate_secret(self, secret_type: str = 'api_key', length: int = 32) -> str:
        """Generate new secret value"""
        if secret_type == 'api_key':
            return secrets.token_urlsafe(length)

        elif secret_type == 'password':
            # Strong password with all character types
            chars = string.ascii_letters + string.digits + string.punctuation
            return ''.join(secrets.choice(chars) for _ in range(length))

        elif secret_type == 'jwt_secret':
            return secrets.token_urlsafe(64)

        else:
            return secrets.token_bytes(length).hex()

    def rotate_secret(self, path: str, secret_type: str = 'api_key') -> Dict[str, Any]:
        """Rotate secret with zero downtime"""
        print(f"Starting rotation for: {path}")

        try:
            # Read current secret
            current_secret = self.vault_client.secrets.kv.v2.read_secret(path=path)
            current_data = current_secret['data']['data']

            # Generate new value
            new_value = self.generate_secret(secret_type)

            # Store with both old and new values
            rotation_data = {
                'current': new_value,
                'previous': current_data.get('current', current_data.get('value')),
                'rotated_at': datetime.utcnow().isoformat()
            }

            self.vault_client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=rotation_data
            )

            print(f"Secret rotated successfully: {path}")

            return {
                'success': True,
                'path': path,
                'rotated_at': rotation_data['rotated_at']
            }

        except Exception as e:
            print(f"Rotation failed for {path}: {e}")
            raise

    def rotate_database_password(self, secret_path: str) -> Dict[str, Any]:
        """Rotate database credentials"""
        # Get current credentials
        secret = self.vault_client.secrets.kv.v2.read_secret(path=secret_path)
        creds = secret['data']['data']

        # Generate new password
        new_password = self.generate_secret('password', 20)

        # Connect to database
        conn = psycopg2.connect(
            host=creds['host'],
            database=creds['database'],
            user=creds['username'],
            password=creds['password']
        )

        cursor = conn.cursor()

        try:
            # Update password in database
            cursor.execute(
                f"ALTER USER {creds['username']} WITH PASSWORD %s",
                (new_password,)
            )
            conn.commit()

            # Update secret in Vault
            updated_creds = {
                **creds,
                'password': new_password,
                'rotated_at': datetime.utcnow().isoformat()
            }

            self.vault_client.secrets.kv.v2.create_or_update_secret(
                path=secret_path,
                secret=updated_creds
            )

            print(f"Database credentials rotated: {secret_path}")

            return {'success': True}

        finally:
            cursor.close()
            conn.close()

    def schedule_rotation(self, path: str, interval_days: int = 90):
        """Schedule automatic rotation using AWS Lambda"""
        # Create rotation schedule in AWS Secrets Manager
        # or use cron job

        schedule_expression = f"rate({interval_days} days)"

        # This would trigger a Lambda function
        print(f"Rotation scheduled for {path}: every {interval_days} days")

    def rotate_encryption_keys(self, key_id: str):
        """Rotate encryption keys"""
        kms = boto3.client('kms')

        # Enable automatic key rotation
        kms.enable_key_rotation(KeyId=key_id)

        print(f"Automatic rotation enabled for KMS key: {key_id}")

    def audit_rotation_history(self, path: str) -> list:
        """Get rotation history"""
        versions = self.vault_client.secrets.kv.v2.read_secret_metadata(path=path)

        history = []
        for version, metadata in versions['data']['versions'].items():
            history.append({
                'version': version,
                'created_time': metadata['created_time'],
                'deleted': metadata.get('deletion_time') is not None
            })

        return sorted(history, key=lambda x: x['created_time'], reverse=True)

# Usage
if __name__ == '__main__':
    rotation = SecretsRotation(
        vault_url='http://localhost:8200',
        vault_token='your-token'
    )

    # Rotate API key
    rotation.rotate_secret('api-keys/external-service', 'api_key')

    # Rotate database credentials
    rotation.rotate_database_password('database/production')

    # Schedule rotations
    rotation.schedule_rotation('api-keys/external-service', 30)
    rotation.schedule_rotation('database/production', 90)

    # View history
    history = rotation.audit_rotation_history('api-keys/external-service')
    print(f"Rotation history: {history}")
```

### 3. **Kubernetes Secrets Rotation**

```yaml
# secrets-rotation-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: secrets-rotation
  namespace: production
spec:
  schedule: "0 2 * * 0"  # Weekly at 2 AM Sunday
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: secrets-rotator
          containers:
          - name: rotate
            image: secrets-rotator:latest
            env:
            - name: VAULT_ADDR
              value: "http://vault:8200"
            - name: VAULT_TOKEN
              valueFrom:
                secretKeyRef:
                  name: vault-token
                  key: token
            command:
            - /bin/sh
            - -c
            - |
              # Rotate secrets
              python /app/rotate_secrets.py \
                --secret database-password \
                --secret api-keys \
                --secret tls-certificates

          restartPolicy: OnFailure
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secrets-rotator
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secrets-rotator
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: secrets-rotator
  namespace: production
subjects:
- kind: ServiceAccount
  name: secrets-rotator
roleRef:
  kind: Role
  name: secrets-rotator
  apiGroup: rbac.authorization.k8s.io
```

## Best Practices

### ✅ DO
- Automate rotation
- Use grace periods
- Verify new secrets
- Maintain rotation audit trail
- Implement rollback procedures
- Monitor rotation failures
- Use managed services (AWS Secrets Manager)
- Test rotation procedures

### ❌ DON'T
- Hardcode secrets
- Share secrets
- Skip verification
- Rotate without grace period
- Ignore rotation failures
- Store secrets in version control

## Rotation Schedule

- **API Keys**: 30-90 days
- **Database Passwords**: 90 days
- **TLS Certificates**: Before expiry
- **Encryption Keys**: 1 year
- **Service Account Tokens**: 90 days

## Zero-Downtime Strategy

1. **Generate new secret**
2. **Store with versioning**
3. **Grace period** (both versions valid)
4. **Verification**
5. **Deprecate old version**
6. **Remove after grace period**

## Resources

- [AWS Secrets Manager Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [NIST Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
