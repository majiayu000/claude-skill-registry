---
name: kagent
description: Kubernetes-native AI agent framework for building, deploying, and managing AI agents on Kubernetes. This skill should be used when deploying AI agents as Kubernetes resources, analyzing cluster health with AI, and automating complex K8s operations. Use this skill for Phase IV advanced AIOps and agent-based cluster management.
---

# Kagent Skill

## Overview

Kagent is a Kubernetes-native framework for building, deploying, and managing AI agents. It uses Custom Resource Definitions (CRDs) to define agents as Kubernetes resources, enabling declarative AI agent management with full K8s integration.

## Key Concepts

### What Kagent Provides

1. **Kubernetes-Native Agents**: Define AI agents as CRDs
2. **Cluster Analysis**: AI-powered health checks and optimization
3. **Extensibility**: Custom tools and integrations
4. **Observability**: Full visibility into agent operations

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                  │
│  ┌─────────────────┐    ┌─────────────────────────┐ │
│  │ Kagent          │    │ Custom Resources        │ │
│  │ Controller      │───▶│ - Agent                 │ │
│  │                 │    │ - Tool                  │ │
│  │                 │    │ - Model                 │ │
│  └─────────────────┘    └─────────────────────────┘ │
│           │                                          │
│           ▼                                          │
│  ┌─────────────────────────────────────────────────┐ │
│  │              AI Agent Pods                       │ │
│  │  - Execute kubectl commands                      │ │
│  │  - Analyze resources                             │ │
│  │  - Report findings                               │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Kubernetes cluster (Minikube, kind, or cloud)
- kubectl configured
- Go 1.21+ (for building from source)

### Install from Bundle

```bash
# Install CRDs and controller
kubectl apply -f https://raw.githubusercontent.com/kagent-dev/kagent/main/dist/install.yaml
```

### Build from Source

```bash
# Clone repository
git clone https://github.com/kagent-dev/kagent.git
cd kagent/go

# Install CRDs
make install

# Deploy controller
make deploy
```

### Build Installer Bundle

```bash
# Generate consolidated install.yaml
make build-installer
```

## Usage

### Basic Kubernetes Operations

Kagent agents can execute standard kubectl commands:

```bash
# Resource listing
kubectl get pods -n namespace
kubectl get deployments -n namespace
kubectl get services -n namespace

# Detailed listing
kubectl get pods -n namespace -o wide
kubectl get nodes -o wide
```

### Resource Inspection

```bash
# Describe resources
kubectl describe pod podname -n namespace
kubectl describe deployment deployname -n namespace
kubectl describe service servicename -n namespace

# Get full YAML
kubectl get configmap configname -n namespace -o yaml
kubectl get secret secretname -n namespace -o yaml
```

### Health and Status Queries

```bash
# Component health
kubectl get componentstatuses
kubectl get nodes -o wide

# Resource status
kubectl get deployments -n namespace -o wide
kubectl get pods -n namespace -o wide
```

### Advanced Operations

```bash
# Node management
kubectl drain <node>
kubectl cordon/uncordon <node>

# Port forwarding
kubectl port-forward svc/my-service 8080:80

# Authorization checks
kubectl auth can-i create pods

# Debugging
kubectl debug pod/my-pod --image=busybox
```

## Diagnostic Tools

Kagent agents have access to:

| Tool | Purpose |
|------|---------|
| `crictl` | Container runtime interface |
| `kubelet logs` | Node-level logs |
| `journalctl` | System logs |
| `tcpdump` | Network diagnostics |
| `netstat` | Connection status |

## Use Cases for TaskFlow

### 1. Cluster Health Analysis

Use kagent to analyze overall cluster health before deployment:

```bash
kagent "analyze the cluster health and report any issues"
kagent "check if there are sufficient resources for 5 new pods"
```

### 2. Resource Optimization

```bash
kagent "identify pods without resource limits"
kagent "find over-provisioned deployments"
kagent "recommend resource adjustments based on actual usage"
```

### 3. Security Audit

```bash
kagent "find pods running as root"
kagent "identify services exposed without ingress"
kagent "check for secrets mounted as environment variables"
```

### 4. Troubleshooting

```bash
kagent "why are pods in namespace X failing?"
kagent "analyze network connectivity between services"
kagent "find the root cause of OOMKilled pods"
```

## Custom Resource Definitions

### Agent CRD Example

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: cluster-analyzer
  namespace: kagent-system
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
    - helm
  systemPrompt: |
    You are a Kubernetes cluster analyzer.
    Focus on identifying resource issues and optimization opportunities.
```

### Tool CRD Example

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Tool
metadata:
  name: kubectl-tool
spec:
  type: kubectl
  permissions:
    - get
    - list
    - describe
  namespaces:
    - default
    - production
```

## Integration with kubectl-ai

Kagent complements kubectl-ai:

| Tool | Best For |
|------|----------|
| **kubectl-ai** | Ad-hoc commands, quick operations |
| **kagent** | Persistent agents, complex analysis, automation |

### Combined Workflow

```bash
# Use kubectl-ai for immediate operations
kubectl-ai "scale api to 3 replicas"

# Use kagent for analysis and recommendations
kagent "analyze if scaling to 3 replicas is sustainable given current cluster resources"
```

## Best Practices

1. **Start with read-only**: Begin with agents that only read cluster state
2. **Namespace scope**: Limit agent permissions to specific namespaces
3. **Audit trail**: Enable logging for all agent operations
4. **Resource limits**: Set limits on agent pods themselves
5. **Gradual automation**: Start manual, then automate proven workflows

## Resources

Refer to `references/agent-patterns.md` for common agent configurations.
