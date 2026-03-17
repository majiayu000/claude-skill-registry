---
name: harness-cd
description: Harness CD (Continuous Delivery) for Kubernetes, Helm, Terraform, ECS, and serverless deployments with GitOps, approval gates, rollback strategies, and multi-environment promotion
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - harness-platform
  - harness-mcp
triggers:
  - harness cd
  - harness deploy
  - harness deployment
  - harness rollback
  - harness canary
  - harness blue green
  - harness rolling
  - harness gitops
  - harness environment
  - harness infrastructure
  - harness service
  - harness artifact
  - harness approval
  - deployment strategy
  - kubernetes deployment
  - helm deployment
  - terraform deployment
---

# Harness CD Skill

Deployment orchestration for Kubernetes, Helm, Terraform, ECS, serverless with GitOps.

## Use For
- CD pipelines, strategies (Canary/Blue-Green/Rolling), environments
- Approval gates, GitOps, rollback, multi-environment promotion

## Basic Deployment Pipeline

```yaml
pipeline:
  name: Deploy Pipeline
  stages:
    - stage:
        name: Deploy Dev
        type: Deployment
        spec:
          service:
            serviceRef: my_service
          environment:
            environmentRef: development
          execution:
            steps:
              - step:
                  name: Rolling Deploy
                  type: K8sRollingDeploy
                  timeout: 10m
            rollbackSteps:
              - step:
                  name: Rollback
                  type: K8sRollingRollback
```

## Deployment Strategies

### Rolling (gradual replacement)
```yaml
- step:
    type: K8sRollingDeploy
    spec:
      skipDryRun: false
```

### Canary (progressive traffic shift)
```yaml
- step:
    type: K8sCanaryDeploy
    spec:
      instanceSelection:
        type: Count
        spec:
          count: 1
```

### Blue-Green (zero-downtime cutover)
```yaml
- step:
    type: K8sBGStageDeployment
- step:
    type: K8sBGSwapServices
```

## Service Configuration

### Kubernetes
```yaml
serviceDefinition:
  type: Kubernetes
  spec:
    manifests:
      - manifest:
          type: K8sManifest
          spec:
            store:
              type: Git
              spec:
                connectorRef: github_connector
                branch: main
    artifacts:
      primary:
        sources:
          - type: DockerRegistry
            spec:
              imagePath: myorg/myapp
```

### Helm
```yaml
serviceDefinition:
  type: NativeHelm
  spec:
    chartName: my-app
    helmVersion: V3
```

### Terraform
```yaml
serviceDefinition:
  type: CustomDeployment
  spec:
    customDeploymentRef:
      templateRef: terraform_template
```

## Environment & Infrastructure

```yaml
environment:
  name: Production
  type: Production
infrastructureDefinition:
  type: KubernetesDirect
  spec:
    connectorRef: k8s_connector
    namespace: my-namespace
```

## Approval Gates

```yaml
- step:
    type: HarnessApproval
    spec:
      approvers:
        userGroups:
          - account.ProductionApprovers
# Jira: type: JiraApproval, issueKey: <+pipeline.variables.jiraIssueKey>
# ServiceNow: type: ServiceNowApproval, ticketNumber: <+pipeline.variables.changeRequest>
```

## GitOps Deployments

### Argo CD
```yaml
- step:
    type: GitOpsUpdateReleaseRepo
    spec:
      variables:
        - name: image_tag
          value: <+artifact.tag>
- step:
    type: GitOpsSync
    spec:
      prune: true
```

### PR-Based GitOps
```yaml
- step:
    type: CreatePR
    spec:
      updates:
        - path: environments/<+env.name>/values.yaml
          key: image.tag
          value: <+artifact.tag>
```

## Deployment Verification & Rollback

```yaml
- step:
    type: Verify
    spec:
      type: Canary
      sensitivity: MEDIUM
- step:
    type: Http
    spec:
      url: <+infra.variables.serviceUrl>/health
failureStrategies:
  - onFailure:
      errors:
        - AllErrors
      action:
        type: StageRollback
```

## Multi-Environment Promotion

```yaml
pipeline:
  stages:
    - stage:
        name: Deploy Dev
        spec:
          environment:
            environmentRef: development
    - stage:
        name: Deploy Staging
        spec:
          environment:
            environmentRef: staging
        when:
          condition: <+pipeline.stages.deploy_dev.status> == "SUCCEEDED"
    - stage:
        name: Deploy Production
        spec:
          environment:
            environmentRef: production
```

## Triggers

```yaml
# Artifact
trigger:
  source:
    type: Artifact
    spec:
      type: DockerRegistry
      imagePath: myorg/myapp
# Webhook
trigger:
  source:
    type: Webhook
    spec:
      type: Github
# Scheduled
trigger:
  source:
    type: Scheduled
    spec:
      expression: "0 2 * * *"
```

## CD Expressions

| Expression | Purpose |
|----------|---|
| <+service.name> | Service |
| <+env.name> | Environment |
| <+infra.namespace> | Namespace |
| <+artifact.image>:<+artifact.tag> | Image |
| <+pipeline.stages.X.output.VAR> | Output |

## API Operations

```bash
curl -X POST "https://app.harness.io/pipeline/api/pipeline/execute/${PIPELINE_ID}" -H "x-api-key: ${API_KEY}"
curl -X GET "https://app.harness.io/pipeline/api/pipelines/execution/v2/${EXECUTION_ID}" -H "x-api-key: ${API_KEY}"
curl -X PUT "https://app.harness.io/pipeline/api/pipelines/execution/interrupt/${EXECUTION_ID}" -H "x-api-key: ${API_KEY}"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Deployment timeout | Increase step timeout |
| Image pull failed | Verify connector credentials |
| Namespace not found | Check infrastructure definition |
| Manifest error | Validate YAML locally |
| Approval timeout | Review approval workflow |
| Rollback failed | Configure rollback steps |

## References

- [Harness CD Docs](https://developer.harness.io/docs/continuous-delivery)
- [Deployment Strategies](https://developer.harness.io/docs/continuous-delivery/manage-deployments/deployment-concepts)
- [GitOps](https://developer.harness.io/docs/continuous-delivery/gitops)
