---
name: kustomize-generators
description: Use when generating ConfigMaps and Secrets with Kustomize for Kubernetes configuration management.
allowed-tools: [Bash, Read]
---

# Kustomize Generators

Master ConfigMap and Secret generation using Kustomize generators for managing application configuration, credentials, and environment-specific settings without manual YAML creation.

## Overview

Kustomize generators automatically create ConfigMaps and Secrets from literals, files, and environment files. Generated resources include content hashes in their names, enabling automatic rollouts when configuration changes.

## ConfigMap Generator Basics

### Literal Values

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
  - name: app-config
    literals:
      - DATABASE_URL=postgresql://localhost:5432/mydb
      - LOG_LEVEL=info
      - CACHE_ENABLED=true
      - MAX_CONNECTIONS=100
      - TIMEOUT_SECONDS=30
```

Generated ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-8g2h5m9k7t
data:
  DATABASE_URL: postgresql://localhost:5432/mydb
  LOG_LEVEL: info
  CACHE_ENABLED: "true"
  MAX_CONNECTIONS: "100"
  TIMEOUT_SECONDS: "30"
```

### File-Based Generation

```yaml
# kustomization.yaml
configMapGenerator:
  - name: app-config
    files:
      - application.properties
      - config/database.conf
      - config/logging.yml
```

With files:

```properties
# application.properties
server.port=8080
server.host=0.0.0.0
app.name=MyApplication
app.version=1.0.0
```

```conf
# config/database.conf
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

```yaml
# config/logging.yml
level: info
format: json
outputs:
  - stdout
  - file: /var/log/app.log
```

### Named Files

```yaml
configMapGenerator:
  - name: app-config
    files:
      - config.properties=application.properties
      - db.conf=config/database.conf
      - log.yml=config/logging.yml
```

Generated ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-9m4k8h2f6d
data:
  config.properties: |
    server.port=8080
    server.host=0.0.0.0
    app.name=MyApplication
    app.version=1.0.0
  db.conf: |
    max_connections = 100
    shared_buffers = 256MB
    effective_cache_size = 1GB
  log.yml: |
    level: info
    format: json
    outputs:
      - stdout
      - file: /var/log/app.log
```

### Environment Files

```yaml
configMapGenerator:
  - name: app-config
    envs:
      - .env
      - config/.env.production
```

With files:

```bash
# .env
DATABASE_URL=postgresql://localhost:5432/mydb
REDIS_URL=redis://localhost:6379
LOG_LEVEL=info
```

```bash
# config/.env.production
DATABASE_URL=postgresql://prod-db:5432/mydb
REDIS_URL=redis://prod-redis:6379
LOG_LEVEL=warn
MONITORING_ENABLED=true
```

### Mixed Sources

```yaml
configMapGenerator:
  - name: app-config
    literals:
      - APP_NAME=MyApp
      - APP_VERSION=1.0.0
    files:
      - application.properties
    envs:
      - .env
```

## Secret Generator Basics

### Literal Values

```yaml
secretGenerator:
  - name: app-secrets
    type: Opaque
    literals:
      - database-password=super-secret-password
      - api-key=1234567890abcdef
      - jwt-secret=my-jwt-secret-key
```

Generated Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets-2f6h8k9m4t
type: Opaque
data:
  database-password: c3VwZXItc2VjcmV0LXBhc3N3b3Jk
  api-key: MTIzNDU2Nzg5MGFiY2RlZg==
  jwt-secret: bXktand0LXNlY3JldC1rZXk=
```

### File-Based Secrets

```yaml
secretGenerator:
  - name: tls-secret
    type: kubernetes.io/tls
    files:
      - tls.crt=certs/server.crt
      - tls.key=certs/server.key
```

### Docker Registry Secret

```yaml
secretGenerator:
  - name: docker-registry
    type: kubernetes.io/dockerconfigjson
    files:
      - .dockerconfigjson=docker-config.json
```

With docker-config.json:

```json
{
  "auths": {
    "registry.example.com": {
      "username": "myuser",
      "password": "mypassword",
      "email": "myemail@example.com",
      "auth": "bXl1c2VyOm15cGFzc3dvcmQ="
    }
  }
}
```

### SSH Key Secret

```yaml
secretGenerator:
  - name: ssh-keys
    type: Opaque
    files:
      - id_rsa=keys/id_rsa
      - id_rsa.pub=keys/id_rsa.pub
```

## Generator Behaviors

### Create Behavior (Default)

```yaml
configMapGenerator:
  - name: app-config
    behavior: create
    literals:
      - KEY=value
```

Creates a new ConfigMap. Fails if one already exists.

### Replace Behavior

```yaml
configMapGenerator:
  - name: app-config
    behavior: replace
    literals:
      - KEY=new-value
```

Replaces existing ConfigMap entirely. Fails if it doesn't exist.

### Merge Behavior

```yaml
# base/kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info
      - CACHE_ENABLED=true
      - DATABASE_URL=localhost

# overlays/production/kustomization.yaml
configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
      - DATABASE_URL=prod-db.example.com
```

Resulting ConfigMap merges values:

```yaml
data:
  LOG_LEVEL: warn                        # Overridden
  CACHE_ENABLED: "true"                  # From base
  DATABASE_URL: prod-db.example.com      # Overridden
```

## Advanced Generator Patterns

### Multi-Environment Configuration

```yaml
# base/kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - APP_NAME=MyApp
      - CACHE_ENABLED=true
      - TIMEOUT=30
    files:
      - application.properties

# overlays/development/kustomization.yaml
configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=debug
      - DEBUG_MODE=true
      - DATABASE_URL=postgresql://dev-db:5432/mydb

# overlays/production/kustomization.yaml
configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=error
      - DEBUG_MODE=false
      - DATABASE_URL=postgresql://prod-db:5432/mydb
      - RATE_LIMIT_ENABLED=true
```

### Configuration with Multiple Files

```yaml
configMapGenerator:
  - name: nginx-config
    files:
      - nginx.conf
      - mime.types
      - conf.d/default.conf
      - conf.d/ssl.conf
      - conf.d/upstream.conf
```

### Application Configuration Bundle

```yaml
configMapGenerator:
  - name: app-bundle
    literals:
      - APP_NAME=MyApp
      - APP_VERSION=1.0.0
    files:
      - app-config.json
      - feature-flags.yml
      - rate-limits.json
    envs:
      - .env.production
```

With files:

```json
// app-config.json
{
  "server": {
    "port": 8080,
    "host": "0.0.0.0"
  },
  "database": {
    "pool_size": 20,
    "timeout": 5000
  }
}
```

```yaml
# feature-flags.yml
features:
  new_ui: true
  beta_features: false
  metrics: true
```

```json
// rate-limits.json
{
  "global": 1000,
  "per_user": 100,
  "burst": 50
}
```

### Secrets from External Files

```yaml
secretGenerator:
  - name: database-credentials
    files:
      - username=secrets/db-username.txt
      - password=secrets/db-password.txt

  - name: api-keys
    files:
      - stripe-key=secrets/stripe-api-key.txt
      - sendgrid-key=secrets/sendgrid-api-key.txt
      - twilio-key=secrets/twilio-api-key.txt
```

### TLS Certificate Bundle

```yaml
secretGenerator:
  - name: tls-certificates
    type: kubernetes.io/tls
    files:
      - tls.crt=certs/server.crt
      - tls.key=certs/server.key
      - ca.crt=certs/ca-bundle.crt
```

## Generator Options

### Disable Name Suffix Hash

```yaml
configMapGenerator:
  - name: app-config
    options:
      disableNameSuffixHash: true
    literals:
      - KEY=value
```

Generated ConfigMap name: `app-config` (no hash)

Use cases:

- Static references that shouldn't trigger rollouts
- Resources referenced by external systems
- Stable endpoints for debugging

### Immutable ConfigMaps

```yaml
configMapGenerator:
  - name: app-config
    options:
      immutable: true
    literals:
      - KEY=value
```

Generated ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-8g2h5m9k7t
immutable: true
data:
  KEY: value
```

### Labels and Annotations

```yaml
configMapGenerator:
  - name: app-config
    options:
      labels:
        app: myapp
        environment: production
        version: v1.0.0
      annotations:
        config.kubernetes.io/description: "Application configuration"
        config.kubernetes.io/owner: "platform-team"
    literals:
      - KEY=value
```

## Consuming Generated Resources

### Environment Variables from ConfigMap

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        envFrom:
        - configMapRef:
            name: app-config
```

### Specific Keys as Environment Variables

```yaml
env:
- name: DATABASE_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: DATABASE_URL
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: LOG_LEVEL
```

### Volume Mounts from ConfigMap

```yaml
volumes:
- name: config
  configMap:
    name: app-config
    items:
    - key: application.properties
      path: app.properties
    - key: logging.yml
      path: logging.yml

containers:
- name: myapp
  volumeMounts:
  - name: config
    mountPath: /etc/config
    readOnly: true
```

### Secrets as Environment Variables

```yaml
envFrom:
- secretRef:
    name: app-secrets

env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: database-password
```

### Secrets as Volume Mounts

```yaml
volumes:
- name: secrets
  secret:
    secretName: app-secrets
    items:
    - key: database-password
      path: db-password
      mode: 0400

containers:
- name: myapp
  volumeMounts:
  - name: secrets
    mountPath: /etc/secrets
    readOnly: true
```

## Real-World Examples

### Web Application Configuration

```yaml
# base/kustomization.yaml
configMapGenerator:
  - name: webapp-config
    literals:
      - SESSION_TIMEOUT=3600
      - CSRF_ENABLED=true
      - CORS_ENABLED=false
    files:
      - nginx.conf
      - app.properties

secretGenerator:
  - name: webapp-secrets
    literals:
      - session-secret=changeme
      - csrf-token-secret=changeme

resources:
  - deployment.yaml
  - service.yaml
```

```yaml
# overlays/production/kustomization.yaml
resources:
  - ../../base

configMapGenerator:
  - name: webapp-config
    behavior: merge
    literals:
      - SESSION_TIMEOUT=7200
      - CORS_ENABLED=true
      - CORS_ORIGINS=https://example.com,https://www.example.com
      - RATE_LIMIT_ENABLED=true
      - RATE_LIMIT_REQUESTS=1000
    files:
      - nginx.conf=nginx-production.conf

secretGenerator:
  - name: webapp-secrets
    behavior: replace
    files:
      - session-secret=secrets/session-secret.txt
      - csrf-token-secret=secrets/csrf-secret.txt
```

### Microservices Configuration

```yaml
configMapGenerator:
  # User Service Config
  - name: user-service-config
    literals:
      - SERVICE_NAME=user-service
      - PORT=8080
      - METRICS_PORT=9090
    files:
      - config/user-service.yml

  # Order Service Config
  - name: order-service-config
    literals:
      - SERVICE_NAME=order-service
      - PORT=8081
      - METRICS_PORT=9091
    files:
      - config/order-service.yml

  # Payment Service Config
  - name: payment-service-config
    literals:
      - SERVICE_NAME=payment-service
      - PORT=8082
      - METRICS_PORT=9092
    files:
      - config/payment-service.yml

secretGenerator:
  - name: user-service-secrets
    literals:
      - jwt-secret=user-jwt-secret
      - database-password=user-db-password

  - name: payment-service-secrets
    literals:
      - stripe-api-key=sk_test_123
      - webhook-secret=whsec_123
```

### Database Configuration

```yaml
configMapGenerator:
  - name: postgres-config
    files:
      - postgresql.conf
      - pg_hba.conf
    literals:
      - POSTGRES_DB=myapp
      - POSTGRES_MAX_CONNECTIONS=200
      - POSTGRES_SHARED_BUFFERS=256MB

secretGenerator:
  - name: postgres-secrets
    literals:
      - postgres-password=super-secret-password
      - replication-password=repl-password

  - name: postgres-init-scripts
    files:
      - init.sql=scripts/init-db.sql
      - create-tables.sql=scripts/schema.sql
```

### Redis Configuration

```yaml
configMapGenerator:
  - name: redis-config
    files:
      - redis.conf
    literals:
      - REDIS_PORT=6379
      - REDIS_MAXMEMORY=2gb
      - REDIS_MAXMEMORY_POLICY=allkeys-lru

secretGenerator:
  - name: redis-secrets
    literals:
      - redis-password=redis-secure-password
```

### Monitoring Configuration

```yaml
configMapGenerator:
  - name: prometheus-config
    files:
      - prometheus.yml
      - alerts/rules.yml
      - alerts/recording-rules.yml

  - name: grafana-config
    files:
      - grafana.ini
      - datasources/prometheus.yml
      - dashboards/app-dashboard.json

secretGenerator:
  - name: grafana-secrets
    literals:
      - admin-password=grafana-admin-password
      - smtp-password=smtp-password
```

### Application Feature Flags

```yaml
configMapGenerator:
  - name: feature-flags
    files:
      - feature-flags.json
    literals:
      - FEATURE_NEW_UI=true
      - FEATURE_BETA_API=false
      - FEATURE_DARK_MODE=true
      - FEATURE_SOCIAL_LOGIN=true
```

With feature-flags.json:

```json
{
  "features": {
    "new_ui": {
      "enabled": true,
      "rollout_percentage": 100
    },
    "beta_api": {
      "enabled": false,
      "rollout_percentage": 0
    },
    "dark_mode": {
      "enabled": true,
      "rollout_percentage": 100
    },
    "social_login": {
      "enabled": true,
      "providers": ["google", "github"]
    }
  }
}
```

## Generator with Transformers

```yaml
configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info

# Apply transformers
commonLabels:
  app: myapp

namePrefix: prod-

namespace: production
```

Result: ConfigMap named `prod-app-config-8g2h5m9k7t` in namespace `production` with label `app: myapp`

## Testing Generated Resources

```bash
# Build and view generated ConfigMap
kustomize build . | grep -A 20 "kind: ConfigMap"

# Build and save to file
kustomize build . > generated.yaml

# Validate generated resources
kustomize build . | kubectl apply --dry-run=client -f -

# Compare with cluster
kustomize build . | kubectl diff -f -

# Apply generated resources
kubectl apply -k .

# View generated ConfigMap
kubectl get configmap -l app=myapp

# Describe generated ConfigMap
kubectl describe configmap app-config-8g2h5m9k7t

# View ConfigMap data
kubectl get configmap app-config-8g2h5m9k7t -o yaml
```

## When to Use This Skill

Use the kustomize-generators skill when you need to:

1. Generate ConfigMaps from literal values, files, or environment files
2. Generate Secrets for credentials, API keys, or certificates
3. Automatically trigger pod rollouts when configuration changes
4. Manage environment-specific configuration with merge behavior
5. Create immutable ConfigMaps for stable configuration
6. Generate configuration bundles from multiple sources
7. Create TLS secrets from certificate files
8. Generate Docker registry secrets for private registries
9. Manage application feature flags across environments
10. Create database connection configurations
11. Generate monitoring and observability configurations
12. Manage microservices configuration consistently
13. Create SSH key secrets for Git operations
14. Generate application property files dynamically
15. Manage rate limiting and throttling configurations

## Best Practices

1. Use generators instead of static ConfigMap/Secret YAML files
2. Leverage hash suffixes for automatic pod rollouts on config changes
3. Use behavior: merge in overlays to override specific keys
4. Store sensitive files outside version control, reference in generators
5. Use disableNameSuffixHash only when necessary for stability
6. Combine literals, files, and envs in a single generator when logical
7. Use immutable: true for ConfigMaps that shouldn't change
8. Apply labels and annotations to generated resources for tracking
9. Use named files syntax for custom key names in ConfigMaps
10. Generate Secrets from files rather than literals in production
11. Use type: kubernetes.io/tls for TLS certificate secrets
12. Document generator behavior in comments within kustomization.yaml
13. Test generated output with kustomize build before applying
14. Use envFrom for loading entire ConfigMaps as environment variables
15. Mount ConfigMaps as volumes for file-based configuration
16. Use specific key references for sensitive environment variables
17. Apply readOnly: true when mounting secrets as volumes
18. Use mode: 0400 for sensitive files in secret volumes
19. Generate separate ConfigMaps for different configuration concerns
20. Use consistent naming conventions for generated resources
21. Validate generated resources with kubectl apply --dry-run
22. Use kustomize edit add configmap for CLI-based updates
23. Keep generator source files in the same directory as kustomization.yaml
24. Use .gitignore to exclude sensitive generator source files
25. Document required generator source files in README

## Common Pitfalls

1. Hardcoding secrets in literals instead of using external files
2. Not using hash suffixes, missing automatic pod rollouts
3. Committing sensitive generator source files to version control
4. Using behavior: replace when merge would be more appropriate
5. Not testing generated output before applying to clusters
6. Forgetting to update generator source files when changing configuration
7. Using absolute paths in file references instead of relative paths
8. Not documenting which files are needed for generators
9. Mixing configuration concerns in a single generator
10. Not using labels to track generated resources
11. Forgetting to set immutable: true for stable ConfigMaps
12. Using disableNameSuffixHash unnecessarily
13. Not validating generated resource names in referencing resources
14. Hardcoding generated resource names in deployments
15. Not using envFrom for loading entire ConfigMaps
16. Mounting secrets without readOnly: true
17. Not setting restrictive file modes for sensitive volume mounts
18. Using create behavior in overlays, causing conflicts
19. Not using type field for specialized secrets (TLS, Docker)
20. Forgetting to update references when changing generator names
21. Not testing behavior: merge in lower environments first
22. Using literals for large configuration blocks instead of files
23. Not organizing generator source files logically
24. Forgetting to add new generator source files to version control
25. Not using consistent key naming conventions across generators
26. Applying generators without understanding hash suffix implications
27. Not documenting generator behavior for team members
28. Using plain text files for secrets instead of secure storage
29. Not rotating generated secrets regularly
30. Forgetting to clean up old generated ConfigMaps/Secrets

## Resources

- [Kustomize ConfigMap Generator Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/)
- [Kustomize Secret Generator Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/secretgenerator/)
- [Kustomize Generator Options](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/generatoroptions/)
- [Kubernetes ConfigMap Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secret Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Managing ConfigMaps and Secrets](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- [Immutable ConfigMaps and Secrets](https://kubernetes.io/docs/concepts/configuration/configmap/#configmap-immutable)
- [Kustomize Best Practices](https://kubectl.docs.kubernetes.io/guides/config_management/)
