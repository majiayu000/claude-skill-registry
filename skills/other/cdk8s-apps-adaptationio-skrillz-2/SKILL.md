---
name: cdk8s-apps
description: CDK8s for type-safe Kubernetes manifests using Python. Use when building complex K8s applications programmatically, generating manifests from code, creating reusable infrastructure patterns, or managing multi-environment deployments.
---

# CDK8s Applications

Define Kubernetes applications using Python instead of YAML. cdk8s (Cloud Development Kit for Kubernetes) is a CNCF Sandbox project that provides type-safe, programmable infrastructure for Kubernetes.

## Overview

**What is cdk8s?**
- Define K8s resources using Python, TypeScript, JavaScript, Java, or Go
- Synthesizes to standard Kubernetes YAML manifests
- Works with any Kubernetes cluster (cloud-agnostic)
- Built on the same concepts as AWS CDK
- CNCF Sandbox project (GA since October 2021)

**Key Benefits:**
- **Type Safety**: Catch configuration errors at development time
- **IDE Support**: Autocomplete, inline docs, refactoring
- **Reusability**: Create custom constructs for common patterns
- **Testability**: Unit test infrastructure code
- **Reduced Boilerplate**: Intent-driven APIs vs verbose YAML

**When to Use cdk8s:**
- Complex applications with multiple microservices
- Multi-environment deployments (dev/staging/prod)
- Reusable component libraries
- Teams preferring code over YAML
- EKS deployments integrated with AWS CDK

## Quick Start

### Installation

```bash
# Install cdk8s CLI (requires Node.js 18+)
npm install -g cdk8s-cli

# Initialize Python project
cdk8s init python-app
cd my-cdk8s-app

# Install dependencies
pip install -r requirements.txt
```

### Your First Application

```python
#!/usr/bin/env python3
from constructs import Construct
from cdk8s import App, Chart
from cdk8s_plus_27 import Deployment, ContainerProps

class WebApp(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Create deployment with 3 replicas
        deployment = Deployment(
            self, "web",
            replicas=3,
            containers=[
                ContainerProps(
                    image="nginx:1.21",
                    port=80
                )
            ]
        )

        # Expose as LoadBalancer service
        deployment.expose_via_service(port=80)

# Synthesize to YAML
app = App()
WebApp(app, "my-app")
app.synth()
```

### Synthesize and Deploy

```bash
# Generate Kubernetes manifests
cdk8s synth

# Review generated YAML
cat dist/my-app.k8s.yaml

# Deploy to cluster
kubectl apply -f dist/
```

## Core Concepts

### Constructs Hierarchy

cdk8s uses three levels of constructs:

**L1 Constructs (Low-Level)**
- Auto-generated from Kubernetes API
- Direct mapping to K8s resources
- Full control, verbose syntax

```python
from imports import k8s

k8s.KubeDeployment(
    self, "deployment",
    spec=k8s.DeploymentSpec(
        replicas=3,
        selector=k8s.LabelSelector(match_labels={"app": "web"}),
        template=k8s.PodTemplateSpec(...)
    )
)
```

**L2 Constructs (High-Level - cdk8s-plus)**
- Hand-crafted, intent-driven APIs
- Automatic relationship management
- Reduced boilerplate

```python
from cdk8s_plus_27 import Deployment, ContainerProps

Deployment(
    self, "deployment",
    replicas=3,
    containers=[ContainerProps(image="nginx", port=80)]
)
```

**L3 Constructs (Custom Abstractions)**
- Your own reusable components
- Encapsulate organizational patterns

```python
class WebService(Construct):
    def __init__(self, scope, id, image, replicas=3):
        super().__init__(scope, id)
        # Compose deployment + service + ingress
```

### Apps and Charts

**App**: Root container for all charts
**Chart**: Represents a single Kubernetes manifest file

```python
app = App()

# Each chart → separate YAML file
dev_chart = MyChart(app, "dev", namespace="development")
prod_chart = MyChart(app, "prod", namespace="production")

app.synth()  # Generates dist/dev.k8s.yaml and dist/prod.k8s.yaml
```

### Import Custom Resources

Import CRDs, Helm charts, and external definitions:

```bash
# Import Kubernetes API
cdk8s import k8s

# Import CRD from URL
cdk8s import https://raw.githubusercontent.com/aws-controllers-k8s/s3-controller/main/helm/crds/s3.services.k8s.aws_buckets.yaml

# Import Helm chart
cdk8s import helm:https://charts.bitnami.com/bitnami/redis@18.2.0

# Import from GitHub
cdk8s import github:crossplane/crossplane@0.14.0
```

## Common Workflows

### Workflow 1: Simple Web Application

```python
from cdk8s import App, Chart
from cdk8s_plus_27 import Deployment, ConfigMap, EnvValue, ContainerProps

class WebApp(Chart):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # Configuration
        config = ConfigMap(
            self, "config",
            data={
                "DATABASE_HOST": "postgres.default.svc",
                "LOG_LEVEL": "info"
            }
        )

        # Deployment
        deployment = Deployment(
            self, "web",
            replicas=3,
            containers=[
                ContainerProps(
                    image="myapp:v1.0",
                    port=8080,
                    env_variables={
                        "DATABASE_HOST": EnvValue.from_config_map(
                            config, "DATABASE_HOST"
                        )
                    }
                )
            ]
        )

        # Expose as service
        deployment.expose_via_service(port=80, target_port=8080)

app = App()
WebApp(app, "web-app")
app.synth()
```

### Workflow 2: Multi-Environment Deployment

```python
from cdk8s import App, Chart
from cdk8s_plus_27 import Deployment, ContainerProps

class MyApp(Chart):
    def __init__(self, scope, id, env, replicas, image_tag):
        super().__init__(scope, id, namespace=env)

        Deployment(
            self, "app",
            replicas=replicas,
            containers=[
                ContainerProps(
                    image=f"myapp:{image_tag}",
                    port=8080
                )
            ]
        )

app = App()

# Development
MyApp(app, "dev", env="development", replicas=1, image_tag="dev")

# Staging
MyApp(app, "staging", env="staging", replicas=2, image_tag="v1.2.3-rc")

# Production
MyApp(app, "prod", env="production", replicas=5, image_tag="v1.2.3")

app.synth()
```

### Workflow 3: Custom Reusable Construct

```python
from constructs import Construct
from cdk8s_plus_27 import (
    Deployment, Service, ConfigMap, Secret,
    ContainerProps, EnvValue, ServiceType
)

class MicroserviceApp(Construct):
    """Reusable microservice with deployment, service, and config."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        image: str,
        replicas: int = 3,
        port: int = 8080,
        config: dict = None,
        secrets: dict = None
    ):
        super().__init__(scope, id)

        # ConfigMap
        if config:
            cfg = ConfigMap(self, "config", data=config)

        # Secret
        if secrets:
            sec = Secret(self, "secret", string_data=secrets)

        # Build env vars
        env_vars = {}
        if config:
            for key in config.keys():
                env_vars[key] = EnvValue.from_config_map(cfg, key)
        if secrets:
            for key in secrets.keys():
                env_vars[key] = EnvValue.from_secret_value(key, sec)

        # Deployment
        self.deployment = Deployment(
            self, "deployment",
            replicas=replicas,
            containers=[
                ContainerProps(
                    image=image,
                    port=port,
                    env_variables=env_vars
                )
            ]
        )

        # Service
        self.service = self.deployment.expose_via_service(
            service_type=ServiceType.CLUSTER_IP,
            port=port
        )

# Usage
from cdk8s import App, Chart

class MyChart(Chart):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # Deploy 3 microservices with one construct
        MicroserviceApp(
            self, "frontend",
            image="myapp/frontend:v1",
            replicas=5,
            config={"API_URL": "http://api:8080"}
        )

        MicroserviceApp(
            self, "api",
            image="myapp/api:v1",
            replicas=3,
            secrets={"DATABASE_PASSWORD": "supersecret"}
        )

        MicroserviceApp(
            self, "worker",
            image="myapp/worker:v1",
            replicas=2
        )

app = App()
MyChart(app, "microservices")
app.synth()
```

## Testing

### Unit Tests with pytest

```python
# tests/test_chart.py
import pytest
from cdk8s import Testing
from app import MyChart

def test_deployment_has_correct_replicas():
    chart = Testing.chart()
    MyChart(chart)

    manifests = Testing.synth(chart)
    deployment = [m for m in manifests if m["kind"] == "Deployment"][0]

    assert deployment["spec"]["replicas"] == 3

def test_service_exposes_correct_port():
    chart = Testing.chart()
    MyChart(chart)

    manifests = Testing.synth(chart)
    service = [m for m in manifests if m["kind"] == "Service"][0]

    assert service["spec"]["ports"][0]["port"] == 80
```

### Policy Validation

```python
def test_no_latest_tags():
    """Enforce no :latest image tags"""
    chart = Testing.chart()
    MyChart(chart)

    manifests = Testing.synth(chart)

    for manifest in manifests:
        if manifest["kind"] == "Deployment":
            containers = manifest["spec"]["template"]["spec"]["containers"]
            for container in containers:
                assert not container["image"].endswith(":latest")

def test_all_containers_have_resource_limits():
    """Enforce resource limits"""
    chart = Testing.chart()
    MyChart(chart)

    manifests = Testing.synth(chart)

    for manifest in manifests:
        if manifest["kind"] == "Deployment":
            containers = manifest["spec"]["template"]["spec"]["containers"]
            for container in containers:
                assert "resources" in container
                assert "limits" in container["resources"]
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          npm install -g cdk8s-cli
          pip install -r requirements.txt

      - name: Synthesize manifests
        run: cdk8s synth

      - name: Deploy to EKS
        run: kubectl apply -f dist/
```

## Integration with AWS CDK (EKS)

Deploy cdk8s apps directly to EKS clusters:

```python
from aws_cdk import Stack, aws_eks as eks
from constructs import Construct
import cdk8s
from my_k8s_app import MyK8sChart

class EksStack(Stack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Create EKS cluster with AWS CDK
        cluster = eks.Cluster(
            self, "Cluster",
            version=eks.KubernetesVersion.V1_28
        )

        # Define K8s app with cdk8s
        cdk8s_app = cdk8s.App()
        k8s_chart = MyK8sChart(cdk8s_app, "app")

        # Bridge: Deploy cdk8s chart to EKS
        cluster.add_cdk8s_chart("my-app", k8s_chart)
```

## Best Practices

### 1. Pin Versions

```python
# requirements.txt
cdk8s==2.70.26
cdk8s-plus-27==2.7.84  # Match your K8s version
constructs>=10.0.0
```

### 2. Use Explicit Names

```python
# ❌ Dangerous: Renaming ID recreates resource
Deployment(self, "app-v2", ...)

# ✅ Safe: Use explicit name metadata
from imports import k8s

Deployment(
    self, "app-v2",
    metadata=k8s.ObjectMeta(name="app")  # Stable name
)
```

### 3. Separate Environments

```python
class ProdChart(Chart):
    def __init__(self, scope, id):
        super().__init__(
            scope, id,
            namespace="production",
            labels={"env": "prod"}
        )
```

### 4. Test Before Deploying

```bash
# Dry-run validation
kubectl apply --dry-run=client -f dist/

# Run unit tests
pytest tests/

# GitOps review
git diff dist/
```

## Common Commands

```bash
# Initialize project
cdk8s init python-app

# Import K8s API
cdk8s import k8s

# Import CRD
cdk8s import https://example.com/crd.yaml

# Import Helm chart
cdk8s import helm:https://charts.example.com/chart@1.0.0

# Synthesize manifests
cdk8s synth

# Watch mode (auto-synth)
cdk8s synth --watch

# Deploy
kubectl apply -f dist/

# Validate
kubectl apply --dry-run=client -f dist/
```

## Version Compatibility

| cdk8s-plus | Kubernetes | Python | Node.js |
|------------|------------|--------|---------|
| cdk8s-plus-27 | 1.27+ | 3.7+ | 18+ |
| cdk8s-plus-28 | 1.28+ | 3.7+ | 18+ |
| cdk8s-plus-29 | 1.29+ | 3.7+ | 18+ |

## When to Use cdk8s vs Alternatives

**Use cdk8s when:**
- Complex applications with multiple components
- Development teams prefer code over YAML
- Need reusable component libraries
- Testing infrastructure code is important
- Integrating with AWS CDK for EKS

**Use Helm when:**
- Need existing community charts
- Simple templating is sufficient
- Package distribution required

**Use Kustomize when:**
- Simple overlays needed
- Transparent YAML modifications
- Minimal learning curve important

**Use Raw YAML when:**
- Very simple applications
- One-off deployments
- No reusability needed

## Quick Reference

### Available Constructs (cdk8s-plus)

**Workloads**: `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`, `Pod`

**Services**: `Service`, `Ingress`

**Config**: `ConfigMap`, `Secret`, `EnvValue`

**Storage**: `Volume`, `PersistentVolume`, `PersistentVolumeClaim`

**RBAC**: `ServiceAccount`, `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding`

**Scaling**: `HorizontalPodAutoscaler`

**Networking**: `NetworkPolicy`

## Detailed Guides

For in-depth information, see:

- **[Getting Started Guide](references/getting-started.md)** - Installation, project setup, and basics
- **[Constructs Guide](references/constructs.md)** - L1/L2/L3 constructs, cdk8s-plus, imports
- **[Patterns Guide](references/patterns.md)** - Real-world patterns and best practices

## Resources

**Official Documentation:**
- [cdk8s.io](https://cdk8s.io/) - Official website
- [GitHub](https://github.com/cdk8s-team/cdk8s) - Source code
- [API Reference](https://cdk8s.io/docs/latest/reference/) - API documentation
- [Examples](https://cdk8s.io/docs/latest/examples/) - Code examples

**AWS Resources:**
- [Introducing CDK for Kubernetes](https://aws.amazon.com/blogs/containers/introducing-cdk-for-kubernetes/)
- [cdk8s+ Intent-driven APIs](https://aws.amazon.com/blogs/containers/introducing-cdk8s-intent-driven-apis-for-kubernetes-objects/)

**Community:**
- [CNCF Project Page](https://www.cncf.io/projects/cdk-for-kubernetes-cdk8s/)
- [Slack Channel](https://cdk8s.io/community/)
