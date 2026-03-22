---
name: opa
description: Expert guidance for OPA (Open Policy Agent), the CNCF policy engine for unified authorization across the stack. Helps developers write Rego policies for Kubernetes admission control, API authorization, infrastructure-as-code validation, and data filtering — enforcing security policies as code.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
  - policy
  - authorization
  - kubernetes
  - admission-control
  - rego
---

# OPA — Open Policy Agent


## Overview


OPA (Open Policy Agent), the CNCF policy engine for unified authorization across the stack. Helps developers write Rego policies for Kubernetes admission control, API authorization, infrastructure-as-code validation, and data filtering — enforcing security policies as code.


## Instructions

### Rego Policy Language

```rego
# policy/authz.rego — API authorization policy
package authz

import rego.v1

default allow := false

# Admin users can do anything
allow if {
    input.user.role == "admin"
}

# Users can read their own data
allow if {
    input.method == "GET"
    input.path[0] == "users"
    input.path[1] == input.user.id
}

# Users can update their own profile
allow if {
    input.method in {"PUT", "PATCH"}
    input.path[0] == "users"
    input.path[1] == input.user.id
    not input.body.role                   # Can't change own role
}

# Team members can read team resources
allow if {
    input.method == "GET"
    input.path[0] == "teams"
    team_id := input.path[1]
    team_id in input.user.teams
}

# Managers can approve expenses under $10,000
allow if {
    input.method == "POST"
    input.path == ["expenses", "approve"]
    input.user.role == "manager"
    input.body.amount < 10000
}

# Deny reasons for audit trail
reasons contains msg if {
    not allow
    input.user.role != "admin"
    msg := sprintf("User %s with role %s denied access to %s %s",
        [input.user.id, input.user.role, input.method, concat("/", input.path)])
}
```

### Kubernetes Admission Control (Gatekeeper)

```yaml
# Gatekeeper ConstraintTemplate — define reusable policy templates
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

        import rego.v1

        violation contains {"msg": msg} if {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }

---
# Apply the constraint — all deployments must have these labels
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-labels
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels:
      - "app.kubernetes.io/name"
      - "app.kubernetes.io/managed-by"
      - "team"
```

```yaml
# Block containers running as root
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8snoroot
spec:
  crd:
    spec:
      names:
        kind: K8sNoRoot
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8snoroot

        import rego.v1

        violation contains {"msg": msg} if {
          container := input.review.object.spec.containers[_]
          not container.securityContext.runAsNonRoot
          msg := sprintf("Container %s must set runAsNonRoot: true", [container.name])
        }

        violation contains {"msg": msg} if {
          container := input.review.object.spec.containers[_]
          container.securityContext.runAsUser == 0
          msg := sprintf("Container %s must not run as root (UID 0)", [container.name])
        }

---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sNoRoot
metadata:
  name: no-root-containers
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet"]
```

### API Integration

```typescript
// src/middleware/opa-authz.ts — OPA-backed API authorization
import type { Request, Response, NextFunction } from "express";

const OPA_URL = process.env.OPA_URL ?? "http://opa:8181";

export async function authorize(req: Request, res: Response, next: NextFunction) {
  const input = {
    method: req.method,
    path: req.path.split("/").filter(Boolean),
    user: {
      id: req.user?.id,
      role: req.user?.role,
      teams: req.user?.teams ?? [],
    },
    body: req.body,
  };

  const response = await fetch(`${OPA_URL}/v1/data/authz/allow`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });

  const { result } = await response.json();

  if (result) {
    next();
  } else {
    res.status(403).json({ error: "Forbidden" });
  }
}

// Usage: app.use(authorize);
```

### Terraform Validation

```rego
# policy/terraform.rego — Validate Terraform plans before apply
package terraform

import rego.v1

# Deny public S3 buckets
deny contains msg if {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg := sprintf("S3 bucket %s must not be public", [resource.address])
}

# Require encryption on RDS instances
deny contains msg if {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  not resource.change.after.storage_encrypted
  msg := sprintf("RDS instance %s must have encryption enabled", [resource.address])
}

# Limit instance sizes
deny contains msg if {
  resource := input.resource_changes[_]
  resource.type == "aws_instance"
  not resource.change.after.instance_type in allowed_instance_types
  msg := sprintf("Instance %s uses %s, allowed: %v",
    [resource.address, resource.change.after.instance_type, allowed_instance_types])
}

allowed_instance_types := {"t3.micro", "t3.small", "t3.medium", "m5.large"}
```

```bash
# Validate Terraform plan with OPA
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
opa eval -d policy/ -i plan.json "data.terraform.deny"
```

## Installation

```bash
# CLI
brew install opa

# Docker
docker run -p 8181:8181 openpolicyagent/opa run --server

# Kubernetes (Gatekeeper)
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/v3.15.0/deploy/gatekeeper.yaml
```


## Examples


### Example 1: Setting up Opa for a microservices project

**User request:**

```
I have a Node.js API and a React frontend running in Docker. Set up Opa for monitoring/deployment.
```

The agent creates the necessary configuration files based on patterns like `# Gatekeeper ConstraintTemplate — define reusable policy tem`, sets up the integration with the existing Docker setup, configures appropriate defaults for a Node.js + React stack, and provides verification commands to confirm everything is working.

### Example 2: Troubleshooting kubernetes admission control issues

**User request:**

```
Opa is showing errors in our kubernetes admission control. Here are the logs: [error output]
```

The agent analyzes the error output, identifies the root cause by cross-referencing with common Opa issues, applies the fix (updating configuration, adjusting resource limits, or correcting syntax), and verifies the resolution with appropriate health checks.


## Guidelines

1. **Policy as code** — Store policies in Git alongside application code; review policy changes in PRs
2. **Rego testing** — Write unit tests for policies: `opa test policy/ -v`; catch policy bugs before deployment
3. **Gatekeeper for K8s** — Use OPA Gatekeeper for admission control; enforce policies at deploy time, not just at runtime
4. **Centralize authorization** — Move authorization logic from application code to OPA; one policy engine across all services
5. **Deny by default** — Start with `default allow := false`; explicitly grant access rather than revoking
6. **Bundle for distribution** — Package policies as OPA bundles; deploy to OPA instances via bundle server
7. **Terraform validation** — Validate `terraform plan` output with OPA before `terraform apply`; prevent misconfigurations
8. **Audit logging** — Log OPA decisions for compliance; track who accessed what and which policy allowed/denied it
