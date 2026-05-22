---
name: kubectl
description: Kubernetes CLI operations and cluster management
allowed-tools: [Bash, Read]
---

# Kubectl Skill

## Overview

Kubernetes cluster management via kubectl. 90%+ context savings.

## Requirements

- kubectl CLI installed
- KUBECONFIG environment variable or ~/.kube/config

## Tools (Progressive Disclosure)

### Pods

| Tool         | Description   | Confirmation |
| ------------ | ------------- | ------------ |
| get-pods     | List pods     | No           |
| describe-pod | Pod details   | No           |
| logs         | View pod logs | No           |
| delete-pod   | Delete pod    | **REQUIRED** |

### Deployments

| Tool            | Description         | Confirmation |
| --------------- | ------------------- | ------------ |
| get-deployments | List deployments    | No           |
| scale           | Scale deployment    | Yes          |
| rollout         | Rollout status      | No           |
| rollback        | Rollback deployment | Yes          |

### Services

| Tool         | Description     |
| ------------ | --------------- |
| get-services | List services   |
| get-ingress  | List ingresses  |
| port-forward | Port forwarding |

### BLOCKED

| Tool             | Status      |
| ---------------- | ----------- |
| delete namespace | **BLOCKED** |
| delete cluster   | **BLOCKED** |

## Agent Integration

- **devops** (primary): Cluster operations
- **developer** (secondary): App deployment
