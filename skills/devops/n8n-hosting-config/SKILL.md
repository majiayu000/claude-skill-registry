---
name: n8n Hosting & Configuration
description: Self-host n8n - Docker, environment variables, databases, scaling, security, enterprise features
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# n8n Hosting & Configuration

Deploy and configure self-hosted n8n instances.

## Quick Start

### Docker (Recommended)
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=secure-password \
  n8nio/n8n
```

### Docker Compose (Production)
```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=n8n.yourdomain.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.yourdomain.com/
      - GENERIC_TIMEZONE=America/New_York
      - TZ=America/New_York
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - N8N_USER_MANAGEMENT_JWT_SECRET=${JWT_SECRET}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

### NPM Installation
```bash
npm install n8n -g
n8n start
```

## Environment Variables

### Core Settings
```bash
# Instance Configuration
N8N_HOST=localhost              # Hostname
N8N_PORT=5678                   # Port
N8N_PROTOCOL=https              # http or https
WEBHOOK_URL=https://n8n.example.com/  # Public webhook URL

# Timezone
GENERIC_TIMEZONE=America/New_York
TZ=America/New_York

# Encryption (REQUIRED for production)
N8N_ENCRYPTION_KEY=your-32-char-encryption-key

# User Management
N8N_USER_MANAGEMENT_JWT_SECRET=your-jwt-secret
N8N_USER_MANAGEMENT_DISABLED=false
```

### Database Configuration

#### SQLite (Default)
```bash
# Uses ~/.n8n/database.sqlite by default
DB_TYPE=sqlite
DB_SQLITE_DATABASE=/home/node/.n8n/database.sqlite
```

#### PostgreSQL (Recommended for Production)
```bash
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=secure-password
DB_POSTGRESDB_SCHEMA=public

# Connection pooling
DB_POSTGRESDB_POOL_SIZE=10
```

#### MySQL/MariaDB
```bash
DB_TYPE=mysqldb
DB_MYSQLDB_HOST=localhost
DB_MYSQLDB_PORT=3306
DB_MYSQLDB_DATABASE=n8n
DB_MYSQLDB_USER=n8n
DB_MYSQLDB_PASSWORD=secure-password
```

### Execution Settings
```bash
# Execution mode
EXECUTIONS_MODE=queue           # regular or queue

# Process settings
EXECUTIONS_PROCESS=main         # main or own (separate process)
EXECUTIONS_TIMEOUT=3600         # Timeout in seconds
EXECUTIONS_TIMEOUT_MAX=7200     # Max timeout

# Data retention
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none  # Save storage
EXECUTIONS_DATA_SAVE_ON_PROGRESS=false
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=336     # Hours (14 days)
```

### Queue Mode (Redis)
```bash
EXECUTIONS_MODE=queue
QUEUE_BULL_REDIS_HOST=localhost
QUEUE_BULL_REDIS_PORT=6379
QUEUE_BULL_REDIS_PASSWORD=redis-password
QUEUE_BULL_REDIS_DB=0

# Worker settings
QUEUE_BULL_REDIS_TIMEOUT_THRESHOLD=10000
QUEUE_HEALTH_CHECK_ACTIVE=true
```

### Authentication
```bash
# Basic Auth
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure-password

# JWT Auth
N8N_JWT_AUTH_ACTIVE=true
N8N_JWT_AUTH_HEADER=Authorization
N8N_JWKS_URI=https://your-auth-provider/.well-known/jwks.json

# LDAP (Enterprise)
N8N_AUTH_LDAP_ENABLED=true
N8N_AUTH_LDAP_URL=ldap://ldap.example.com:389
N8N_AUTH_LDAP_BIND_DN=cn=admin,dc=example,dc=com
N8N_AUTH_LDAP_BIND_PASSWORD=ldap-password
```

### Security Settings
```bash
# HTTPS
N8N_SSL_KEY=/path/to/private.key
N8N_SSL_CERT=/path/to/certificate.crt

# Security headers
N8N_SECURE_COOKIE=true

# IP restrictions
N8N_EDITOR_BASE_URL=https://n8n.example.com
N8N_BLOCK_ENV_ACCESS_IN_NODE=true

# Endpoint restrictions
N8N_METRICS=true
N8N_METRICS_PREFIX=n8n_
```

### Logging
```bash
# Log level
N8N_LOG_LEVEL=info              # debug, info, warn, error
N8N_LOG_OUTPUT=console          # console or file
N8N_LOG_FILE_LOCATION=/var/log/n8n/

# Log streaming (Enterprise)
N8N_EXTERNAL_STORAGE_ENABLED=true
```

### Email (SMTP)
```bash
N8N_EMAIL_MODE=smtp
N8N_SMTP_HOST=smtp.example.com
N8N_SMTP_PORT=587
N8N_SMTP_USER=n8n@example.com
N8N_SMTP_PASS=smtp-password
N8N_SMTP_SSL=true
N8N_SMTP_SENDER=n8n@example.com
```

## Scaling & High Availability

### Horizontal Scaling with Queue Mode
```yaml
# docker-compose.yml
version: '3.8'

services:
  n8n-main:
    image: n8nio/n8n
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    command: n8n start
    # ... other config

  n8n-worker-1:
    image: n8nio/n8n
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    command: n8n worker
    deploy:
      replicas: 3

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15
    # ... config

volumes:
  redis_data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
spec:
  replicas: 1
  selector:
    matchLabels:
      app: n8n
  template:
    metadata:
      labels:
        app: n8n
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        ports:
        - containerPort: 5678
        env:
        - name: DB_TYPE
          value: postgresdb
        - name: DB_POSTGRESDB_HOST
          valueFrom:
            secretKeyRef:
              name: n8n-secrets
              key: db-host
        envFrom:
        - secretRef:
            name: n8n-secrets
        volumeMounts:
        - name: data
          mountPath: /home/node/.n8n
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: n8n-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: n8n
spec:
  selector:
    app: n8n
  ports:
  - port: 5678
    targetPort: 5678
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: n8n
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
spec:
  tls:
  - hosts:
    - n8n.example.com
    secretName: n8n-tls
  rules:
  - host: n8n.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: n8n
            port:
              number: 5678
```

### Worker Configuration
```bash
# Main instance (editor + webhooks)
n8n start

# Worker instances (execution only)
n8n worker --concurrency=10

# Webhook processor
n8n webhook
```

## Reverse Proxy

### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name n8n.example.com;

    ssl_certificate /etc/letsencrypt/live/n8n.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Increase body size for file uploads
    client_max_body_size 100M;
}
```

### Traefik (Docker)
```yaml
services:
  n8n:
    image: n8nio/n8n
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.n8n.rule=Host(`n8n.example.com`)"
      - "traefik.http.routers.n8n.entrypoints=websecure"
      - "traefik.http.routers.n8n.tls.certresolver=letsencrypt"
      - "traefik.http.services.n8n.loadbalancer.server.port=5678"
```

## External Secrets Management

### HashiCorp Vault
```bash
# Enable external secrets
N8N_EXTERNAL_SECRETS_ENABLED=true
N8N_EXTERNAL_SECRETS_BACKEND=vault

# Vault configuration
VAULT_ADDR=https://vault.example.com
VAULT_TOKEN=your-vault-token
VAULT_MOUNT_PATH=secret
```

### AWS Secrets Manager
```bash
N8N_EXTERNAL_SECRETS_ENABLED=true
N8N_EXTERNAL_SECRETS_BACKEND=aws

AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### Environment-based Secrets
```bash
# Reference in n8n as: {{ $env.MY_SECRET }}
MY_SECRET=secret-value
API_KEY=api-key-value
```

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL backup
pg_dump -h localhost -U n8n -d n8n > backup.sql

# Restore
psql -h localhost -U n8n -d n8n < backup.sql
```

### File System Backup
```bash
# Backup n8n data directory
tar -czf n8n-backup.tar.gz /home/node/.n8n

# Includes:
# - credentials (encrypted)
# - workflows (if file-based)
# - settings
```

### Export/Import Workflows
```bash
# Export all workflows via API
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY" > workflows.json

# Import workflow
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

## Enterprise Features

### Source Control (Git)
```bash
# Enable source control
N8N_SOURCECONTROL_ENABLED=true
N8N_SOURCECONTROL_DEFAULT_BRANCH=main
```

### Environments
```bash
# Development
N8N_ENVIRONMENT=development

# Staging
N8N_ENVIRONMENT=staging

# Production
N8N_ENVIRONMENT=production
```

### Log Streaming
```bash
N8N_LOG_STREAMING_ENABLED=true
N8N_LOG_STREAMING_DESTINATION=https://logs.example.com
```

### RBAC (Role-Based Access Control)
- Owner: Full access
- Admin: Manage users and settings
- Member: Execute and edit workflows
- Viewer: Read-only access

### SSO/SAML
```bash
N8N_AUTH_SAML_ENABLED=true
N8N_AUTH_SAML_METADATA_URL=https://idp.example.com/metadata
```

## Monitoring

### Health Check
```bash
# Liveness
GET /healthz

# Readiness
GET /healthz/readiness
```

### Metrics (Prometheus)
```bash
N8N_METRICS=true
N8N_METRICS_PREFIX=n8n_

# Scrape endpoint
GET /metrics
```

Example metrics:
- `n8n_workflow_executions_total`
- `n8n_workflow_execution_duration_seconds`
- `n8n_active_workflows`

### Grafana Dashboard
```json
{
  "panels": [
    {
      "title": "Executions per minute",
      "targets": [{
        "expr": "rate(n8n_workflow_executions_total[1m])"
      }]
    },
    {
      "title": "Execution duration",
      "targets": [{
        "expr": "histogram_quantile(0.95, n8n_workflow_execution_duration_seconds_bucket)"
      }]
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### Webhook Not Accessible
```bash
# Check WEBHOOK_URL is set correctly
WEBHOOK_URL=https://your-public-url/

# Ensure port is exposed
-p 5678:5678
```

#### Database Connection Failed
```bash
# Test PostgreSQL connection
psql -h $DB_POSTGRESDB_HOST -U $DB_POSTGRESDB_USER -d $DB_POSTGRESDB_DATABASE

# Check credentials and network
```

#### Memory Issues
```bash
# Increase Node.js memory
NODE_OPTIONS=--max-old-space-size=4096
```

#### Execution Timeout
```bash
# Increase timeout
EXECUTIONS_TIMEOUT=7200
EXECUTIONS_TIMEOUT_MAX=14400
```

### Logs
```bash
# Docker logs
docker logs n8n -f

# Increase verbosity
N8N_LOG_LEVEL=debug
```

## Output Format
```
DEPLOYMENT:
  Type: [Docker/K8s/NPM]
  Database: [SQLite/PostgreSQL/MySQL]
  Mode: [Single/Queue]

ENVIRONMENT:
  [Key environment variables]

SCALING:
  Workers: [Number]
  Concurrency: [Per worker]

SECURITY:
  Auth: [Method]
  SSL: [Yes/No]
  Secrets: [Storage method]

MONITORING:
  Metrics: [Endpoint]
  Logs: [Destination]
  Alerts: [Configuration]
```
