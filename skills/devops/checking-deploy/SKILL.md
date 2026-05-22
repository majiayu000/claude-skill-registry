---
name: checking-deploy
description: Validate Kubernetes, Terraform, Helm, GitHub Actions, and Docker configs. Use when user says "deploy check", "validate deployment", "check k8s", "validate infrastructure", "check configs", or wants to verify infrastructure.
user-invocable: true
context: fork
allowed-tools:
  - Task
  - TaskOutput
  - TodoWrite
  - Bash(kubectl:*)
  - Bash(helm:*)
  - Bash(terraform:*)
  - Bash(actionlint:*)
  - Bash(docker:*)
  - Grep
  - Glob
  - mcp__perplexity-ask__perplexity_ask
argument-hint: [--background]
---

# Deployment Validation

Validate Kubernetes, Terraform, Helm, GitHub Actions, and Docker configs.

**Use TodoWrite** to track these 5 phases:

1. Detect infrastructure files
2. Spawn validation agent
3. Collect results
4. Research best practices (if needed)
5. Present summary

---

**Parse $ARGUMENTS:**

- `--background` → Run in background, return immediately with agent ID

---

## Step 1: Detect Infrastructure Files

Use Glob to find infrastructure files (quick scan):

- `**/*.yaml`, `**/*.yml` - K8s, Helm, Kustomize
- `.github/workflows/*.yml` - GitHub Actions
- `**/*.tf` - Terraform
- `**/Dockerfile*`, `**/docker-compose*.yml` - Docker

---

## Step 2: Spawn Validation Agent

Based on detected file types, spawn **infra-engineer** agent:

```
Task(
  subagent_type="infra-engineer",
  run_in_background={true if --background else false},
  description="Infrastructure validation",
  prompt="Validate {detected_types} infrastructure in this repository.

  Run these validations (only for detected file types):

  **Kubernetes:**
  - kubectl apply --dry-run=client -f <files>
  - Check: security contexts, resource limits, non-root users
  - Check: liveness/readiness probes defined
  - Check: no 'latest' image tags

  **Helm:**
  - helm lint <chart>
  - helm template validation
  - Check: values.yaml has sensible defaults

  **GitHub Actions:**
  - actionlint (if available)
  - Check: secrets not hardcoded
  - Check: permissions minimized (not 'write-all')
  - Check: pinned action versions (@vX.Y.Z not @main)

  **Terraform:**
  - terraform fmt -check
  - terraform validate
  - Check: no hardcoded credentials
  - Check: state backend configured

  **Dockerfile:**
  - Multi-stage builds where appropriate
  - Non-root user (USER directive)
  - Pinned base image tags (not :latest)
  - No secrets in build args

  Output format:
  PASS/FAIL per category with file:line for issues.
  Severity: CRITICAL / IMPORTANT / SUGGESTION"
)
```

**If --background:** Return agent ID immediately for later collection.

---

## Step 3: Collect Results (if not background)

```
TaskOutput(task_id=<agent_id>, block=true)
```

---

## Step 4: Research if Needed

For uncertain findings, use Perplexity for current best practices:

```
mcp__perplexity-ask__perplexity_ask with:
"Current best practices for {specific concern} in {technology} 2024-2025"
```

---

## Step 5: Present Summary

```
DEPLOYMENT CHECK
================
Agent ID: {id} (use /agent:resume {id} to continue)

Kubernetes: [PASS/FAIL] - {details}
Helm: [PASS/FAIL] - {details}
GitHub Actions: [PASS/FAIL] - {details}
Terraform: [PASS/FAIL] - {details}
Docker: [PASS/FAIL] - {details}

CRITICAL Issues:
- file:line - issue description

IMPORTANT Issues:
- file:line - issue description

Recommendations:
- [prioritized list]
```

---

**Execute validation now.**
