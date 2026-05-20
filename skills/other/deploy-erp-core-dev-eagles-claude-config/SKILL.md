---
name: deploy
description: Load deployment strategies with rollout patterns and IaC templates. Supports k8s, docker, sls (serverless), vm.
argument-hint: "<strategy> - Choose: k8s, docker, sls, vm"
---

# Deployment Strategy Loader

When invoked with `/deploy <strategy>`, load the corresponding deployment configuration.

**Configuration File**: `C:\.claude\deployments\deployment-strategies.yaml`

## Supported Strategies

### @deploy:k8s (or /deploy k8s)
**Platform**: Kubernetes / AKS / EKS / GKE

**Includes**:
- Helm chart templates
- Deployment manifests
- Service/Ingress configurations
- HPA (Horizontal Pod Autoscaler)
- ConfigMaps/Secrets management

**Rollout Strategies**:
- Rolling Update (default)
- Blue-Green deployment
- Canary releases
- A/B testing

**IaC**: Terraform, Helm, Kustomize

### @deploy:docker (or /deploy docker)
**Platform**: Docker Compose / Docker Swarm

**Includes**:
- Multi-stage Dockerfile patterns
- docker-compose.yml templates
- Volume/network configuration
- Health checks
- Development vs Production configs

**Rollout Strategies**:
- Recreate (stop old, start new)
- Rolling (for Swarm)

**IaC**: Docker Compose files

### @deploy:sls (or /deploy sls)
**Platform**: AWS Lambda / Azure Functions / Google Cloud Functions

**Includes**:
- Function configuration
- API Gateway setup
- Event triggers (HTTP, Queue, Timer)
- Step Functions / Durable Functions
- Cold start optimization

**Rollout Strategies**:
- Alias-based (weighted traffic)
- Canary with automatic rollback

**IaC**: SAM, Serverless Framework, Terraform

### @deploy:vm (or /deploy vm)
**Platform**: Virtual Machines / Azure VMs / EC2

**Includes**:
- Traditional deployment scripts
- Immutable infrastructure patterns
- Load balancer configuration
- Auto-scaling groups
- Backup/restore procedures

**Rollout Strategies**:
- In-place update
- Rolling (instance by instance)
- Blue-Green (swap IPs)

**IaC**: Terraform, ARM templates, CloudFormation

## Usage
1. Load strategy: `/deploy k8s`
2. Get templates and rollout patterns
3. Combine: `@deploy:k8s @dotnet @arch:ms`
