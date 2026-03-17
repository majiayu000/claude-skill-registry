---
name: local-eks-development
description: Local Kubernetes development with EKS parity using Kind, LocalStack for AWS services, and local Keycloak for authentication testing
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
triggers:
  - local dev
  - local kubernetes
  - kind cluster
  - local eks
  - localstack
  - dev environment
  - local keycloak
---

# Local EKS Development Skill

Set up local Kubernetes environment with EKS parity for fast development.

## Use For
- Local K8s with Kind matching EKS, LocalStack for AWS services
- Local Keycloak instance, hot-reload development with Skaffold

## Kind Cluster Configuration (EKS Parity)

```yaml
# kind-config.yaml - Matches EKS 1.28 behavior
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: eks-local
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
      - containerPort: 8080  # Keycloak
        hostPort: 8080
        protocol: TCP
  - role: worker
  - role: worker
networking:
  apiServerAddress: "127.0.0.1"
  apiServerPort: 6443
featureGates:
  # Match EKS feature gates
  EphemeralContainers: true
  ServerSideApply: true
containerdConfigPatches:
  - |-
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:5000"]
      endpoint = ["http://kind-registry:5000"]
```

## Docker Compose for Local Stack

```yaml
# docker-compose.yaml
version: '3.8'

services:
  # LocalStack for AWS services
  localstack:
    image: localstack/localstack:3.0
    container_name: localstack
    ports:
      - "4566:4566"           # LocalStack gateway
      - "4510-4559:4510-4559" # External services
    environment:
      - SERVICES=secretsmanager,ecr,iam,sts,ssm
      - DEBUG=1
      - DATA_DIR=/var/lib/localstack/data
      - DOCKER_HOST=unix:///var/run/docker.sock
      - AWS_DEFAULT_REGION=us-west-2
    volumes:
      - localstack_data:/var/lib/localstack
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - eks-local

  # Local Keycloak
  keycloak:
    image: quay.io/keycloak/keycloak:24.0.1
    container_name: keycloak-local
    ports:
      - "8080:8080"
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
      - KC_HTTP_RELATIVE_PATH=/
      - KC_HEALTH_ENABLED=true
    command: start-dev --import-realm
    volumes:
      - ./keycloak/realm-export.json:/opt/keycloak/data/import/realm.json:ro
    networks:
      - eks-local
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # PostgreSQL for Keycloak (production parity)
  postgres:
    image: postgres:15-alpine
    container_name: postgres-local
    environment:
      - POSTGRES_DB=keycloak
      - POSTGRES_USER=keycloak
      - POSTGRES_PASSWORD=keycloak
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - eks-local

  # Local Docker Registry
  registry:
    image: registry:2
    container_name: kind-registry
    ports:
      - "5000:5000"
    networks:
      - eks-local

volumes:
  localstack_data:
  postgres_data:

networks:
  eks-local:
    driver: bridge
```

## Skaffold Configuration (Hot Reload)

```yaml
# skaffold.yaml
apiVersion: skaffold/v4beta7
kind: Config
metadata:
  name: eks-local-dev

build:
  local:
    push: false
  artifacts:
    - image: localhost:5000/my-service
      context: .
      docker:
        dockerfile: Dockerfile
      sync:
        manual:
          - src: "src/**/*.ts"
            dest: /app/src
          - src: "src/**/*.js"
            dest: /app/src

deploy:
  helm:
    releases:
      - name: my-service
        chartPath: charts/my-service
        valuesFiles:
          - charts/my-service/values-local.yaml
        setValues:
          image.repository: localhost:5000/my-service
          image.tag: "{{.IMAGE_TAG}}"
          keycloak.url: "http://keycloak-local:8080"
          keycloak.realm: "local"

profiles:
  - name: debug
    activation:
      - command: debug
    patches:
      - op: add
        path: /deploy/helm/releases/0/setValues/debug
        value: "true"

portForward:
  - resourceType: service
    resourceName: my-service
    port: 3000
    localPort: 3000
  - resourceType: service
    resourceName: keycloak
    port: 8080
    localPort: 8080
```

## Local Values Override

```yaml
# charts/my-service/values-local.yaml
replicaCount: 1

image:
  repository: localhost:5000/my-service
  pullPolicy: Never
  tag: "latest"

service:
  type: NodePort
  port: 3000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: my-service.localhost
      paths:
        - path: /
          pathType: Prefix

# Local Keycloak config
keycloak:
  enabled: true
  url: "http://keycloak-local:8080"
  realm: "local"
  clientId: "my-service-client"
  clientSecret: "local-dev-secret"

# LocalStack AWS config
aws:
  endpoint: "http://localstack:4566"
  region: "us-west-2"
  accessKeyId: "test"
  secretAccessKey: "test"

# Disable production features locally
autoscaling:
  enabled: false

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

# Enable debug logging
env:
  - name: LOG_LEVEL
    value: "debug"
  - name: NODE_ENV
    value: "development"
```

## Setup Scripts

### Initialize Local Environment
```bash
#!/bin/bash
# scripts/dev-up.sh

set -e

echo "🚀 Starting local EKS development environment..."

# Start Docker Compose services
echo "📦 Starting LocalStack and Keycloak..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
until curl -s http://localhost:4566/_localstack/health | grep -q '"secretsmanager": "running"'; do
  sleep 2
done
until curl -s http://localhost:8080/health | grep -q 'UP'; do
  sleep 2
done

# Create Kind cluster if not exists
if ! kind get clusters | grep -q "eks-local"; then
  echo "🔧 Creating Kind cluster..."
  kind create cluster --config kind-config.yaml

  # Connect to local network
  docker network connect eks-local eks-local-control-plane 2>/dev/null || true
  docker network connect eks-local eks-local-worker 2>/dev/null || true
  docker network connect eks-local eks-local-worker2 2>/dev/null || true
fi

# Install NGINX Ingress
echo "🌐 Installing NGINX Ingress..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Setup local secrets
echo "🔐 Setting up local secrets..."
kubectl create namespace my-service 2>/dev/null || true
kubectl create secret generic my-service-keycloak \
  --namespace my-service \
  --from-literal=client-secret=local-dev-secret \
  --dry-run=client -o yaml | kubectl apply -f -

# Setup LocalStack secrets
aws --endpoint-url=http://localhost:4566 \
  secretsmanager create-secret \
  --name my-service/keycloak-client-secret \
  --secret-string "local-dev-secret" 2>/dev/null || true

echo "✅ Local environment ready!"
echo ""
echo "Services:"
echo "  - Kubernetes API: https://127.0.0.1:6443"
echo "  - Keycloak: http://localhost:8080 (admin/admin)"
echo "  - LocalStack: http://localhost:4566"
echo "  - Registry: http://localhost:5000"
echo ""
echo "Run 'skaffold dev' to start hot-reload development"
```

### Teardown Environment
```bash
#!/bin/bash
# scripts/dev-down.sh

set -e

echo "🛑 Stopping local EKS development environment..."

# Stop Skaffold if running
pkill -f "skaffold dev" 2>/dev/null || true

# Delete Kind cluster
if kind get clusters | grep -q "eks-local"; then
  echo "🗑️ Deleting Kind cluster..."
  kind delete cluster --name eks-local
fi

# Stop Docker Compose
echo "📦 Stopping Docker services..."
docker-compose down -v

echo "✅ Local environment stopped"
```

## Telepresence for Hybrid Development

```bash
# Connect to remote EKS while running local code
telepresence connect

# Intercept traffic to your service
telepresence intercept my-service \
  --namespace my-namespace \
  --port 3000:3000 \
  --env-file my-service.env

# Your local code now receives production traffic
npm run dev

# Clean up
telepresence leave my-service
telepresence quit
```

## Local Keycloak Realm

```json
{
  "realm": "local",
  "enabled": true,
  "sslRequired": "none",
  "registrationAllowed": true,
  "users": [
    {
      "username": "testuser",
      "email": "test@example.com",
      "enabled": true,
      "firstName": "Test",
      "lastName": "User",
      "credentials": [
        {
          "type": "password",
          "value": "testpass",
          "temporary": false
        }
      ],
      "realmRoles": ["user"]
    },
    {
      "username": "admin",
      "email": "admin@example.com",
      "enabled": true,
      "credentials": [
        {
          "type": "password",
          "value": "adminpass",
          "temporary": false
        }
      ],
      "realmRoles": ["admin", "user"]
    }
  ],
  "clients": [
    {
      "clientId": "my-service-client",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "secret": "local-dev-secret",
      "redirectUris": ["http://localhost:*/*", "http://my-service.localhost/*"],
      "webOrigins": ["*"],
      "standardFlowEnabled": true,
      "directAccessGrantsEnabled": true,
      "serviceAccountsEnabled": true,
      "publicClient": false
    }
  ],
  "roles": {
    "realm": [
      {"name": "admin"},
      {"name": "user"}
    ]
  }
}
```

## Environment Parity Checklist

| Feature | EKS Production | Kind Local |
|---------|---------------|------------|
| K8s Version | 1.28 | 1.28 (configurable) |
| Ingress | AWS ALB | NGINX |
| Secrets | Secrets Manager | LocalStack |
| Registry | ECR | Local Registry |
| IAM | IRSA | Mocked |
| Keycloak | Managed | Docker |
| Database | RDS | Docker Postgres |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Kind cluster won't start | Check Docker resources, restart Docker |
| LocalStack not responding | Check container logs, verify ports |
| Keycloak login fails | Verify realm import, check credentials |
| Image pull fails | Ensure registry is connected to Kind network |
| Ingress not working | Check NGINX controller is running |

## References
- [Kind Configuration](https://kind.sigs.k8s.io/docs/user/configuration/)
- [LocalStack AWS Services](https://docs.localstack.cloud/user-guide/aws/)
- [Skaffold Documentation](https://skaffold.dev/docs/)
