---
name: secrets-management
description: Implement secrets management with HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets for secure credential storage and rotation.
---

# Secrets Management

## Overview

Deploy and configure secure secrets management systems to store, rotate, and audit access to sensitive credentials, API keys, and certificates across your infrastructure.

## When to Use

- Database credentials management
- API key and token storage
- Certificate management
- SSH key distribution
- Credential rotation automation
- Audit and compliance logging
- Multi-environment secrets
- Encryption key management

## Implementation Examples

### 1. **HashiCorp Vault Setup**

```hcl
# vault-config.hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/vault/config/vault.crt"
  tls_key_file  = "/vault/config/vault.key"
}

api_addr     = "https://0.0.0.0:8200"
cluster_addr = "https://0.0.0.0:8201"

ui = true
```

### 2. **Vault Kubernetes Integration**

```yaml
# vault-kubernetes.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-auth
  namespace: vault

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: vault-auth-delegator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: vault-auth
    namespace: vault

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vault
  namespace: vault
spec:
  replicas: 3
  serviceName: vault
  selector:
    matchLabels:
      app: vault
  template:
    metadata:
      labels:
        app: vault
    spec:
      serviceAccountName: vault-auth
      containers:
        - name: vault
          image: vault:1.15.0
          args:
            - "server"
            - "-config=/vault/config/vault.hcl"
          ports:
            - containerPort: 8200
              name: api
            - containerPort: 8201
              name: cluster
          securityContext:
            runAsNonRoot: true
            runAsUser: 100
            capabilities:
              add:
                - IPC_LOCK
          env:
            - name: VAULT_CLUSTER_ADDR
              value: "https://127.0.0.1:8201"
            - name: VAULT_API_ADDR
              value: "https://127.0.0.1:8200"
            - name: VAULT_SKIP_VERIFY
              value: "false"
          volumeMounts:
            - name: vault-config
              mountPath: /vault/config
            - name: vault-data
              mountPath: /vault/data
            - name: vault-logs
              mountPath: /vault/logs
          livenessProbe:
            httpGet:
              path: /v1/sys/health
              port: 8200
              scheme: HTTPS
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /v1/sys/health
              port: 8200
              scheme: HTTPS
            initialDelaySeconds: 30
            periodSeconds: 5
      volumes:
        - name: vault-config
          configMap:
            name: vault-config
        - name: vault-logs
          emptyDir: {}
  volumeClaimTemplates:
    - metadata:
        name: vault-data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi

---
apiVersion: v1
kind: Service
metadata:
  name: vault
  namespace: vault
spec:
  clusterIP: None
  ports:
    - port: 8200
      targetPort: 8200
      name: api
    - port: 8201
      targetPort: 8201
      name: cluster
  selector:
    app: vault

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: vault-config
  namespace: vault
data:
  vault.hcl: |
    storage "raft" {
      path    = "/vault/data"
      node_id = "node1"
    }

    listener "tcp" {
      address       = "0.0.0.0:8200"
      tls_cert_file = "/vault/config/vault.crt"
      tls_key_file  = "/vault/config/vault.key"
    }

    api_addr     = "https://vault:8200"
    cluster_addr = "https://vault:8201"
    ui = true
```

### 3. **Vault Secret Configuration**

```bash
#!/bin/bash
# vault-setup.sh - Configure Vault for applications

set -euo pipefail

VAULT_ADDR="https://vault:8200"
VAULT_TOKEN="${VAULT_TOKEN}"

export VAULT_ADDR
export VAULT_TOKEN

echo "Setting up Vault secrets..."

# Enable secret engines
vault secrets enable -version=2 kv
vault secrets enable -path=database database

# Create database credentials
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly,readwrite" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
  username="vault_admin" \
  password="vault_password"

# Create database roles
vault write database/roles/readonly \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';" \
  revocation_statements="DROP ROLE IF EXISTS \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Create API secrets
vault kv put secret/api/keys \
  github_token="ghp_xxxxxxxxxxx" \
  aws_access_key="AKIAIOSFODNN7EXAMPLE" \
  aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  slack_webhook="https://hooks.slack.com/services/..."

# Create TLS certificates
vault write -f pki/root/generate/internal \
  common_name="my-root-ca" \
  ttl="87600h"

vault write pki/roles/my-domain \
  allowed_domains="*.myapp.com,myapp.com" \
  allow_subdomains=true \
  max_ttl="720h"

# Setup auto-unseal
vault write sys/seal/migrate/start \
  migrate_from_seal_type="shamir"

echo "Vault setup completed"
```

### 4. **AWS Secrets Manager Configuration**

```python
# aws-secrets-manager.py
import boto3
import json
from datetime import datetime

class SecretsManager:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)

    def create_secret(self, name, secret_value, tags=None):
        """Create a new secret"""
        try:
            response = self.client.create_secret(
                Name=name,
                SecretString=json.dumps(secret_value),
                Tags=tags or []
            )
            return response['ARN']
        except Exception as e:
            print(f"Error creating secret: {e}")
            raise

    def get_secret(self, name):
        """Retrieve a secret"""
        try:
            response = self.client.get_secret_value(SecretId=name)
            return json.loads(response['SecretString'])
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            raise

    def update_secret(self, name, secret_value):
        """Update a secret"""
        try:
            response = self.client.update_secret(
                SecretId=name,
                SecretString=json.dumps(secret_value)
            )
            return response['ARN']
        except Exception as e:
            print(f"Error updating secret: {e}")
            raise

    def rotate_secret(self, name, rotation_rules):
        """Enable automatic rotation"""
        try:
            self.client.rotate_secret(
                SecretId=name,
                RotationRules=rotation_rules
            )
        except Exception as e:
            print(f"Error rotating secret: {e}")
            raise

    def list_secrets(self):
        """List all secrets"""
        try:
            response = self.client.list_secrets()
            return response['SecretList']
        except Exception as e:
            print(f"Error listing secrets: {e}")
            raise

    def delete_secret(self, name, recovery_days=30):
        """Delete a secret with recovery window"""
        try:
            response = self.client.delete_secret(
                SecretId=name,
                RecoveryWindowInDays=recovery_days
            )
            return response
        except Exception as e:
            print(f"Error deleting secret: {e}")
            raise

# Usage
if __name__ == '__main__':
    manager = SecretsManager()

    # Create database credentials secret
    db_creds = {
        'username': 'admin',
        'password': 'SecurePassword123!',
        'host': 'postgres.example.com',
        'port': 5432,
        'dbname': 'myapp'
    }

    secret_arn = manager.create_secret(
        'prod/database/credentials',
        db_creds,
        tags=[
            {'Key': 'Environment', 'Value': 'production'},
            {'Key': 'Service', 'Value': 'myapp'}
        ]
    )

    print(f"Secret created: {secret_arn}")

    # Setup rotation
    manager.rotate_secret(
        'prod/database/credentials',
        {'AutomaticallyAfterDays': 30}
    )

    # Retrieve secret
    retrieved = manager.get_secret('prod/database/credentials')
    print(f"Retrieved secret: {retrieved}")
```

### 5. **Kubernetes Secrets**

```yaml
# kubernetes-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-credentials
  namespace: production
type: Opaque
stringData:
  database_url: "postgresql://user:pass@postgres:5432/myapp"
  api_key: "sk_live_xxxxxxxxxxxxxx"
  jwt_secret: "your-jwt-secret-key"

---
apiVersion: v1
kind: Secret
metadata:
  name: docker-registry
  namespace: production
type: kubernetes.io/dockercfg
data:
  .dockercfg: <base64-encoded-dockerconfig>

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      # Use external secrets operator
      serviceAccountName: myapp
      containers:
        - name: app
          image: myapp:latest
          env:
            # From Kubernetes secret
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-credentials
                  key: database_url
            # From mounted secret
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: app-credentials
                  key: api_key
          volumeMounts:
            - name: secrets
              mountPath: /app/secrets
              readOnly: true
      volumes:
        - name: secrets
          secret:
            secretName: app-credentials
            defaultMode: 0400

---
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secret-store
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secret-store
    kind: SecretStore
  target:
    name: app-external-secret
    creationPolicy: Owner
  data:
    - secretKey: database_url
      remoteRef:
        key: prod/database/url
    - secretKey: api_key
      remoteRef:
        key: prod/api/key
```

## Best Practices

### ✅ DO
- Rotate secrets regularly
- Use strong encryption
- Implement access controls
- Audit secret access
- Use managed services
- Implement secret versioning
- Encrypt secrets in transit
- Use separate secrets per environment

### ❌ DON'T
- Store secrets in code
- Use weak encryption
- Share secrets via email/chat
- Commit secrets to version control
- Use single master password
- Log secret values
- Hardcode credentials
- Disable rotation

## Resources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [External Secrets Operator](https://external-secrets.io/)
- [Kubernetes Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
