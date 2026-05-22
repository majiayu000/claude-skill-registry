---
name: infra-change
description: Plan and apply infrastructure code changes safely by reviewing the target manifests or Terraform, presenting the diff or plan, and verifying the result.
---

# Infrastructure Change

## Workflow

1. Read `AGENTS.md`, infrastructure docs, and affected manifests.
2. Identify the exact infrastructure scope.
3. Prepare the code change and the verification path.
4. Present plan or diff before mutation when risk is material.
5. Verify the result with environment-appropriate checks.
