---
name: container-registry-setup
description: Эксперт по container registry. Используй для настройки ECR, Harbor, Docker Hub, image security и CI/CD интеграции.
---

# Container Registry Setup Expert

Эксперт по настройке и управлению container registries.

## Типы Registry

### Cloud-Managed
| Registry | Provider | Features |
|----------|----------|----------|
| ECR | AWS | IAM integration, scanning |
| Artifact Registry | GCP | Multi-format, regional |
| ACR | Azure | AD integration, geo-rep |
| Docker Hub | Docker | Public/private, CI/CD |

### Self-Hosted
| Registry | Best For | Features |
|----------|----------|----------|
| Harbor | Enterprise | RBAC, scanning, replication |
| Nexus | Multi-artifact | Maven, npm, Docker |
| Artifactory | Enterprise | Universal, HA |
| Distribution | Simple | Official Docker registry |

## AWS ECR Setup

### Terraform Configuration

```hcl
resource "aws_ecr_repository" "app" {
  name                 = "my-application"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr.arn
  }

  tags = {
    Environment = "production"
    Team        = "platform"
  }
}

resource "aws_ecr_lifecycle_policy" "cleanup" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Remove untagged after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
```

### ECR Authentication

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Push image
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

## Harbor Self-Hosted

### Docker Compose Setup

```yaml
version: '3'
services:
  harbor-core:
    image: goharbor/harbor-core:v2.9.0
    container_name: harbor-core
    env_file:
      - ./common/config/core/env
    volumes:
      - ./common/config/core/certificates:/etc/core/certificates
      - ./common/config/core/key:/etc/core/key
    depends_on:
      - registry
      - redis
      - postgresql
    networks:
      - harbor

  registry:
    image: goharbor/registry-photon:v2.9.0
    container_name: registry
    volumes:
      - registry_data:/storage
      - ./common/config/registry:/etc/registry
    networks:
      - harbor

  postgresql:
    image: goharbor/harbor-db:v2.9.0
    container_name: harbor-db
    volumes:
      - database:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    networks:
      - harbor

  redis:
    image: goharbor/redis-photon:v2.9.0
    container_name: harbor-redis
    volumes:
      - redis:/var/lib/redis
    networks:
      - harbor

  nginx:
    image: goharbor/nginx-photon:v2.9.0
    container_name: nginx
    ports:
      - "80:8080"
      - "443:8443"
    volumes:
      - ./common/config/nginx:/etc/nginx
    depends_on:
      - harbor-core
    networks:
      - harbor

volumes:
  registry_data:
  database:
  redis:

networks:
  harbor:
    driver: bridge
```

## Image Security

### Vulnerability Scanning

```bash
# Trivy scan
trivy image myapp:latest

# Grype scan
grype myapp:latest

# ECR scan results
aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest
```

### Image Signing with Cosign

```bash
# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myregistry/myapp:latest

# Verify signature
cosign verify --key cosign.pub myregistry/myapp:latest
```

### Content Trust (Docker)

```bash
# Enable content trust
export DOCKER_CONTENT_TRUST=1

# Sign and push
docker push myregistry/myapp:latest

# Verify on pull
docker pull myregistry/myapp:latest
```

## Kubernetes Integration

### Image Pull Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
  namespace: default
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: |
    eyJhdXRocyI6eyJteXJlZ2lzdHJ5LmNvbSI6eyJ1c2VybmFtZSI6InVzZXIi
    LCJwYXNzd29yZCI6InBhc3MiLCJhdXRoIjoiZFhObGNqcHdZWE56In19fQ==
```

### Deployment with Pull Secret

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
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
      containers:
        - name: myapp
          image: myregistry.com/myapp:v1.0.0
          imagePullPolicy: Always
      imagePullSecrets:
        - name: registry-credentials
```

### ServiceAccount Configuration

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: default
imagePullSecrets:
  - name: registry-credentials
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:${{ github.sha }}
            myuser/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitLab CI

```yaml
stages:
  - build
  - push

variables:
  IMAGE_NAME: $CI_REGISTRY_IMAGE

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_NAME:$CI_COMMIT_SHA .
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
  only:
    - main
```

## Cleanup Scripts

### ECR Cleanup

```python
import boto3
from datetime import datetime, timedelta

def cleanup_untagged_images(repository: str, days_old: int = 7):
    """Remove untagged images older than specified days."""
    ecr = boto3.client('ecr')

    response = ecr.describe_images(
        repositoryName=repository,
        filter={'tagStatus': 'UNTAGGED'}
    )

    cutoff = datetime.now() - timedelta(days=days_old)

    images_to_delete = []
    for image in response['imageDetails']:
        if image['imagePushedAt'].replace(tzinfo=None) < cutoff:
            images_to_delete.append({
                'imageDigest': image['imageDigest']
            })

    if images_to_delete:
        ecr.batch_delete_image(
            repositoryName=repository,
            imageIds=images_to_delete
        )
        print(f"Deleted {len(images_to_delete)} images")

# Usage
cleanup_untagged_images('my-app', days_old=7)
```

## Performance Optimization

### Registry Caching

```yaml
# Docker daemon.json
{
  "registry-mirrors": ["https://mirror.gcr.io"],
  "insecure-registries": [],
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 5
}
```

### Pull-Through Cache (Harbor)

```yaml
# Harbor project config
replication:
  - name: docker-hub-proxy
    type: pull-through
    source: https://registry-1.docker.io
    filters:
      - name: library/*
    trigger:
      type: manual
```

## Troubleshooting

```bash
# Test connectivity
curl -v https://myregistry.com/v2/

# Check authentication
docker login myregistry.com

# Verify TLS
openssl s_client -connect myregistry.com:443 -servername myregistry.com

# Clear credentials
docker logout myregistry.com
rm ~/.docker/config.json

# Debug pull issues
docker pull myregistry.com/myapp:latest --debug
```

## Лучшие практики

1. **Image immutability** — используйте immutable tags
2. **Vulnerability scanning** — scan on push обязателен
3. **Lifecycle policies** — автоматическая очистка старых images
4. **Content trust** — подписывайте production images
5. **Geo-replication** — для global deployments
6. **Access control** — минимальные права через RBAC
7. **Monitoring** — алерты на failed pushes и pulls
