---
name: DevOps Practices
description: Expertise in deployment automation, container orchestration, and infrastructure as code. Activates when working with "deploy", "kubernetes", "docker", "terraform", "helm", "k8s", "container", or cloud infrastructure.
version: 1.0.0
---

# DevOps Practices Skill

## Overview

Apply modern DevOps practices for deployment automation, container orchestration, and infrastructure management across multi-cloud environments (Azure, AWS, GCP). This skill encompasses containerization strategies, Kubernetes orchestration, infrastructure as code (IaC), and CI/CD pipeline design using GitHub Actions and Harness.

## Core Competencies

### Container Strategy

**Build Optimized Docker Images:**

Create multi-stage Dockerfiles that minimize image size and maximize build cache efficiency:

```dockerfile
# Development stage with full toolchain
FROM node:20-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Build stage
FROM development AS build
ENV NODE_ENV=production
RUN npm run build && npm prune --production

# Production stage with minimal footprint
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**Implement Security Best Practices:**

- Use specific version tags, never `latest`
- Run containers as non-root user
- Scan images with Trivy or Snyk before deployment
- Minimize attack surface by using distroless or Alpine base images
- Set resource limits (CPU, memory) in all deployment manifests

**Layer Optimization Strategy:**

1. Place frequently changing files (source code) in later layers
2. Place dependency installation early to leverage cache
3. Combine RUN commands to reduce layer count
4. Use `.dockerignore` to exclude unnecessary files

### Kubernetes Orchestration

**Design Deployment Manifests:**

Create production-ready Kubernetes resources with proper resource management:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
  labels:
    app: api-service
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: v1.0.0
    spec:
      containers:
      - name: api
        image: ghcr.io/org/api-service:1.0.0
        ports:
        - containerPort: 3000
          name: http
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: NODE_ENV
          value: "production"
        envFrom:
        - secretRef:
            name: api-secrets
        - configMapRef:
            name: api-config
      serviceAccountName: api-service-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
```

**Implement Service Mesh Patterns:**

Configure Ingress resources with proper routing, TLS, and rate limiting:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

**Configure Horizontal Pod Autoscaling:**

Implement HPA based on CPU, memory, or custom metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Helm Chart Development

**Structure Helm Charts for Reusability:**

Organize Helm charts with proper templating and value management:

```
deployment/helm/api-service/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-staging.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secrets.yaml
    ├── hpa.yaml
    └── _helpers.tpl
```

**Parameterize Configuration:**

Use template functions for flexible deployments:

```yaml
# values.yaml
replicaCount: 3
image:
  repository: ghcr.io/org/api-service
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com
```

**Implement Helm Hooks for Lifecycle Management:**

Use pre-install, post-upgrade hooks for database migrations and testing:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        command: ["npm", "run", "migrate"]
      restartPolicy: OnFailure
```

### Infrastructure as Code

**Terraform Module Design:**

Create reusable Terraform modules for cloud resources:

```hcl
# modules/aks-cluster/main.tf
resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size             = var.vm_size
    enable_auto_scaling = true
    min_count           = var.min_count
    max_count           = var.max_count
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = var.tags
}

# modules/aks-cluster/variables.tf
variable "cluster_name" {
  type        = string
  description = "Name of the AKS cluster"
}

variable "kubernetes_version" {
  type        = string
  description = "Kubernetes version"
  default     = "1.28.0"
}

# modules/aks-cluster/outputs.tf
output "cluster_id" {
  value = azurerm_kubernetes_cluster.main.id
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive = true
}
```

**State Management Best Practices:**

Configure remote state with state locking:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state"
    storage_account_name = "tfstate"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

### CI/CD Pipeline Design

**GitHub Actions Workflow Structure:**

Create comprehensive CI/CD pipelines with testing, building, and deployment stages:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linters
        run: npm run lint

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Setup Helm
        uses: azure/setup-helm@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Get AKS credentials
        run: |
          az aks get-credentials \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --name ${{ secrets.CLUSTER_NAME }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install api-service \
            ./deployment/helm/api-service \
            --namespace production \
            --create-namespace \
            --values ./deployment/helm/api-service/values-prod.yaml \
            --set image.tag=${{ github.sha }} \
            --wait \
            --timeout 5m
```

**Harness Pipeline Configuration:**

Structure Harness pipelines for enterprise-grade deployments:

```yaml
pipeline:
  name: Production Deployment
  identifier: prod_deployment
  projectIdentifier: platform
  orgIdentifier: engineering
  tags: {}
  stages:
    - stage:
        name: Build and Test
        identifier: build_test
        type: CI
        spec:
          cloneCodebase: true
          execution:
            steps:
              - step:
                  type: Run
                  name: Run Tests
                  identifier: run_tests
                  spec:
                    shell: Bash
                    command: |
                      npm ci
                      npm run test
                      npm run lint
              - step:
                  type: BuildAndPushDockerRegistry
                  name: Build and Push
                  identifier: build_push
                  spec:
                    connectorRef: docker_registry
                    repo: <+input>
                    tags:
                      - <+pipeline.sequenceId>
                      - latest
    - stage:
        name: Deploy to Production
        identifier: deploy_prod
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: api_service
          environment:
            environmentRef: production
            infrastructureDefinitions:
              - identifier: prod_k8s
          execution:
            steps:
              - step:
                  type: K8sRollingDeploy
                  name: Rolling Deployment
                  identifier: rolling_deploy
                  spec:
                    skipDryRun: false
                    pruningEnabled: false
              - step:
                  type: K8sBlueGreenDeploy
                  name: Blue Green Deployment
                  identifier: bg_deploy
                  spec:
                    skipDryRun: false
                    pruningEnabled: false
            rollbackSteps:
              - step:
                  type: K8sRollingRollback
                  name: Rollback
                  identifier: rollback
```

## Multi-Cloud Strategies

**Azure-Specific Patterns:**

Leverage Azure-native services for container orchestration:

- Use Azure Container Registry (ACR) with geo-replication
- Implement Azure Key Vault integration for secrets
- Configure Azure Monitor for observability
- Use Azure DevOps or GitHub Actions for CI/CD
- Implement Azure Front Door for global load balancing

**AWS-Specific Patterns:**

Utilize AWS container services:

- Deploy to EKS with Fargate for serverless containers
- Use ECR for container registry
- Implement AWS Secrets Manager integration
- Configure CloudWatch for logging and metrics
- Use AWS Load Balancer Controller for ingress

**GCP-Specific Patterns:**

Leverage Google Cloud Platform capabilities:

- Deploy to GKE with Autopilot mode
- Use Artifact Registry for containers
- Implement Secret Manager integration
- Configure Cloud Monitoring and Logging
- Use Cloud Load Balancing for ingress

## Deployment Best Practices

**Zero-Downtime Deployments:**

Implement rolling updates with proper health checks and graceful shutdown:

1. Configure readiness probes to prevent traffic to unhealthy pods
2. Set `terminationGracePeriodSeconds` to allow in-flight requests to complete
3. Use `preStop` hooks for cleanup operations
4. Implement connection draining in load balancers
5. Use PodDisruptionBudgets to maintain availability during updates

**Blue-Green Deployment Strategy:**

Maintain two identical production environments for instant rollback:

1. Deploy new version to inactive environment (green)
2. Run smoke tests against green environment
3. Switch traffic from blue to green
4. Monitor metrics and error rates
5. Keep blue environment ready for instant rollback if needed

**Canary Deployment Pattern:**

Gradually roll out changes to a subset of users:

1. Deploy new version to canary pods (10% traffic)
2. Monitor key metrics (latency, errors, saturation)
3. Gradually increase traffic to canary (25%, 50%, 75%)
4. Promote to full deployment or rollback based on metrics
5. Automate decision-making with service mesh (Istio, Linkerd)

## Related Resources

- **Workflow Automation Skill** - For pipeline creation and process automation
- **Performance Optimization Skill** - For monitoring and metrics in deployed environments
- **Integration Patterns Skill** - For connecting deployed services
- **GitHub Actions Documentation** - https://docs.github.com/actions
- **Helm Best Practices** - https://helm.sh/docs/chart_best_practices/
- **Kubernetes Production Patterns** - https://kubernetes.io/docs/concepts/
