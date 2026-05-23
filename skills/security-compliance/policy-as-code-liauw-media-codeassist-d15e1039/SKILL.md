---
name: policy-as-code
description: "Policy as Code with OPA, Kyverno, and Checkov. Use when implementing governance, compliance automation, or security policies for infrastructure and Kubernetes."
---

# Policy as Code

Automated policy enforcement for infrastructure, Kubernetes, and CI/CD pipelines.

## When to Use

- Enforcing security policies in Kubernetes
- Validating Terraform configurations
- Implementing compliance requirements
- Pre-commit infrastructure validation
- Admission control in clusters

## Tools Overview

| Tool | Target | Language | Use Case |
|------|--------|----------|----------|
| OPA/Gatekeeper | K8s, General | Rego | Complex policies |
| Kyverno | Kubernetes | YAML | K8s-native policies |
| Checkov | IaC | Python | Terraform, CloudFormation |
| Sentinel | Terraform | Sentinel | Terraform Enterprise |
| Conftest | Config files | Rego | CI/CD validation |

## OPA Gatekeeper (Kubernetes)

### Installation

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
```

### Constraint Template

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

### Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels:
      - "team"
      - "environment"
```

### Common Policies

```yaml
# Require resource limits
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8scontainerlimits
spec:
  crd:
    spec:
      names:
        kind: K8sContainerLimits
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8scontainerlimits

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.cpu
          msg := sprintf("Container %v has no CPU limit", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.memory
          msg := sprintf("Container %v has no memory limit", [container.name])
        }
---
# Block privileged containers
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8spsprivilegedcontainer
spec:
  crd:
    spec:
      names:
        kind: K8sPSPPrivilegedContainer
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8spsprivilegedcontainer

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged
          msg := sprintf("Privileged container not allowed: %v", [container.name])
        }
```

## Kyverno (Kubernetes)

### Installation

```bash
kubectl create -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml
```

### Policies

```yaml
# Require labels
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-team-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "Label 'team' is required"
        pattern:
          metadata:
            labels:
              team: "?*"
---
# Add default labels (mutating)
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  rules:
    - name: add-managed-by
      match:
        any:
          - resources:
              kinds:
                - Deployment
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              managed-by: kyverno
---
# Block latest tag
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-image-tag
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Using 'latest' tag is not allowed"
        pattern:
          spec:
            containers:
              - image: "!*:latest"
---
# Require resource limits
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-resources
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "CPU and memory limits are required"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
                  requests:
                    memory: "?*"
                    cpu: "?*"
```

## Checkov (Terraform/IaC)

### Installation

```bash
pip install checkov
# or
brew install checkov
```

### Usage

```bash
# Scan Terraform directory
checkov -d ./terraform

# Scan specific file
checkov -f main.tf

# Output formats
checkov -d . -o json
checkov -d . -o sarif

# Skip checks
checkov -d . --skip-check CKV_AWS_1,CKV_AWS_2

# Custom policies
checkov -d . --external-checks-dir ./custom-policies
```

### Custom Policy

```python
# custom-policies/check_s3_versioning.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class S3Versioning(BaseResourceCheck):
    def __init__(self):
        name = "Ensure S3 bucket has versioning enabled"
        id = "CKV_CUSTOM_1"
        supported_resources = ["aws_s3_bucket"]
        categories = [CheckCategories.BACKUP_AND_RECOVERY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        versioning = conf.get("versioning", [{}])
        if versioning and versioning[0].get("enabled", [False])[0]:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = S3Versioning()
```

### .checkov.yaml

```yaml
# .checkov.yaml
soft-fail: false
compact: true
framework:
  - terraform
  - kubernetes
skip-check:
  - CKV_AWS_1  # S3 access logging
  - CKV_K8S_1  # Pod security
check:
  - CKV_AWS_*
  - CKV_K8S_*
```

## Conftest (CI/CD)

### Installation

```bash
brew install conftest
# or
go install github.com/open-policy-agent/conftest@latest
```

### Terraform Policy

```rego
# policy/terraform.rego
package main

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.versioning[0].enabled != true
  msg := sprintf("S3 bucket %v must have versioning enabled", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  resource.change.after.from_port == 22
  msg := sprintf("Security group rule %v allows SSH from 0.0.0.0/0", [resource.address])
}
```

### CI/CD Integration

```yaml
# .github/workflows/policy.yml
name: Policy Check
on: [pull_request]

jobs:
  terraform-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Convert to JSON
        run: terraform show -json tfplan > tfplan.json

      - name: Run Conftest
        uses: instrumenta/conftest-action@master
        with:
          files: tfplan.json
          policy: policy/

  kubernetes-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./kubernetes
          framework: kubernetes
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_checkov
        args:
          - --args=--skip-check CKV_AWS_1

  - repo: https://github.com/open-policy-agent/conftest
    rev: v0.46.0
    hooks:
      - id: conftest
        args: [--policy, policy/]
```

## Best Practices

1. **Start with audit mode** before enforcing
2. **Document exceptions** with rationale
3. **Version policies** in Git
4. **Test policies** before deployment
5. **Monitor policy violations** for trends
6. **Regular policy reviews** for relevance

## Integration

Works with:
- `/k8s` - Kubernetes policies
- `/terraform` - IaC validation
- `/security` - Security policies
- `/devops` - CI/CD integration
