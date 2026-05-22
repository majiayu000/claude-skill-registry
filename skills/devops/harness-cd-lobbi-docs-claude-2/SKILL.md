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

Comprehensive Harness CD (Continuous Delivery) for deployments across Kubernetes, Helm, Terraform, ECS, serverless, and traditional platforms with GitOps support.

## When to Use This Skill

Activate this skill when:
- Creating or managing Harness CD pipelines
- Configuring deployment strategies (Canary, Blue-Green, Rolling)
- Setting up environments and infrastructure definitions
- Managing services and artifacts
- Configuring approval gates and governance
- Implementing GitOps workflows
- Setting up deployment verification and rollback
- Managing multi-environment promotion
- Troubleshooting deployment failures

## CD Pipeline Structure

### Basic Deployment Pipeline

```yaml
pipeline:
  name: Deploy Pipeline
  identifier: deploy_pipeline
  projectIdentifier: my_project
  orgIdentifier: default
  stages:
    - stage:
        name: Deploy to Dev
        identifier: deploy_dev
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: my_service
          environment:
            environmentRef: development
            infrastructureDefinitions:
              - identifier: dev_k8s
          execution:
            steps:
              - step:
                  name: Rolling Deployment
                  identifier: rollingDeployment
                  type: K8sRollingDeploy
                  timeout: 10m
                  spec:
                    skipDryRun: false
            rollbackSteps:
              - step:
                  name: Rollback
                  identifier: rollback
                  type: K8sRollingRollback
                  timeout: 10m
```

## Deployment Strategies

### Rolling Deployment

Gradual replacement of instances:

```yaml
- step:
    name: Rolling Deploy
    identifier: rolling
    type: K8sRollingDeploy
    spec:
      skipDryRun: false
      pruningEnabled: false
```

### Canary Deployment

Progressive traffic shifting:

```yaml
- stage:
    name: Canary Deploy
    identifier: canary
    type: Deployment
    spec:
      deploymentType: Kubernetes
      execution:
        steps:
          - stepGroup:
              name: Canary Deployment
              identifier: canaryDeployment
              steps:
                - step:
                    name: Canary Deployment
                    identifier: canaryDeploy
                    type: K8sCanaryDeploy
                    spec:
                      instanceSelection:
                        type: Count
                        spec:
                          count: 1
                      skipDryRun: false
                - step:
                    name: Canary Delete
                    identifier: canaryDelete
                    type: K8sCanaryDelete
                    spec: {}
          - stepGroup:
              name: Primary Deployment
              identifier: primaryDeployment
              steps:
                - step:
                    name: Rolling Deployment
                    identifier: rollingDeploy
                    type: K8sRollingDeploy
                    spec:
                      skipDryRun: false
```

### Blue-Green Deployment

Zero-downtime with instant cutover:

```yaml
- stage:
    name: Blue-Green Deploy
    identifier: blueGreen
    type: Deployment
    spec:
      deploymentType: Kubernetes
      execution:
        steps:
          - step:
              name: Stage Deployment
              identifier: stageDeployment
              type: K8sBGStageDeployment
              spec:
                skipDryRun: false
          - step:
              name: Swap Primary
              identifier: swapPrimary
              type: K8sBGSwapServices
              spec:
                skipDryRun: false
        rollbackSteps:
          - step:
              name: Swap Rollback
              identifier: swapRollback
              type: K8sBGSwapServices
              spec:
                skipDryRun: false
```

## Service Configuration

### Kubernetes Service

```yaml
service:
  name: My Service
  identifier: my_service
  serviceDefinition:
    type: Kubernetes
    spec:
      manifests:
        - manifest:
            identifier: k8s_manifest
            type: K8sManifest
            spec:
              store:
                type: Git
                spec:
                  connectorRef: github_connector
                  gitFetchType: Branch
                  paths:
                    - k8s/
                  branch: main
      artifacts:
        primary:
          primaryArtifactRef: <+input>
          sources:
            - identifier: docker_image
              type: DockerRegistry
              spec:
                connectorRef: docker_connector
                imagePath: myorg/myapp
                tag: <+input>
```

### Helm Service

```yaml
service:
  name: Helm Service
  identifier: helm_service
  serviceDefinition:
    type: NativeHelm
    spec:
      manifests:
        - manifest:
            identifier: helm_chart
            type: HelmChart
            spec:
              store:
                type: Http
                spec:
                  connectorRef: helm_repo
              chartName: my-app
              chartVersion: <+input>
              helmVersion: V3
      artifacts:
        primary:
          primaryArtifactRef: docker_image
          sources:
            - identifier: docker_image
              type: DockerRegistry
              spec:
                connectorRef: docker_connector
                imagePath: myorg/myapp
                tag: <+input>
```

### Terraform Service

```yaml
service:
  name: Terraform Service
  identifier: terraform_service
  serviceDefinition:
    type: CustomDeployment
    spec:
      customDeploymentRef:
        templateRef: terraform_template
        versionLabel: v1
```

## Environment Configuration

### Environment Types

```yaml
# Development
environment:
  name: Development
  identifier: development
  type: PreProduction
  orgIdentifier: default
  projectIdentifier: my_project

# Staging
environment:
  name: Staging
  identifier: staging
  type: PreProduction
  tags:
    tier: staging
    auto_deploy: "true"

# Production
environment:
  name: Production
  identifier: production
  type: Production
  tags:
    tier: production
    requires_approval: "true"
```

### Infrastructure Definition

```yaml
infrastructureDefinition:
  name: K8s Dev Cluster
  identifier: k8s_dev
  type: KubernetesDirect
  orgIdentifier: default
  projectIdentifier: my_project
  environmentRef: development
  spec:
    connectorRef: k8s_connector
    namespace: my-namespace
    releaseName: release-<+INFRA_KEY>
```

## Approval Gates

### Manual Approval

```yaml
- step:
    name: Approval
    identifier: approval
    type: HarnessApproval
    timeout: 1d
    spec:
      approvalMessage: "Please review and approve deployment to production"
      includePipelineExecutionHistory: true
      approvers:
        userGroups:
          - account.ProductionApprovers
        minimumCount: 1
        disallowPipelineExecutor: true
      approverInputs:
        - name: releaseNotes
          defaultValue: ""
```

### Jira Approval

```yaml
- step:
    name: Jira Approval
    identifier: jiraApproval
    type: JiraApproval
    timeout: 1d
    spec:
      connectorRef: jira_connector
      projectKey: DEPLOY
      issueKey: <+pipeline.variables.jiraIssueKey>
      approvalCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Approved
      rejectionCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Rejected
```

### ServiceNow Approval

```yaml
- step:
    name: ServiceNow Approval
    identifier: snowApproval
    type: ServiceNowApproval
    timeout: 1d
    spec:
      connectorRef: servicenow_connector
      ticketNumber: <+pipeline.variables.changeRequest>
      ticketType: CHANGE_REQUEST
      approvalCriteria:
        type: KeyValues
        spec:
          conditions:
            - key: state
              operator: equals
              value: "3"  # Approved state
```

## GitOps Deployments

### Argo CD Integration

```yaml
- stage:
    name: GitOps Deploy
    identifier: gitops_deploy
    type: Deployment
    spec:
      deploymentType: Kubernetes
      gitOpsEnabled: true
      execution:
        steps:
          - step:
              name: Update Release Repo
              identifier: updateReleaseRepo
              type: GitOpsUpdateReleaseRepo
              spec:
                variables:
                  - name: image_tag
                    value: <+artifact.tag>
          - step:
              name: Sync Application
              identifier: syncApp
              type: GitOpsFetchLinkedApps
              spec: {}
          - step:
              name: Sync and Wait
              identifier: syncWait
              type: GitOpsSync
              spec:
                prune: true
                dryRun: false
                applyOnly: false
                forceApply: false
```

### PR-Based GitOps

```yaml
- step:
    name: Create PR
    identifier: createPR
    type: CreatePR
    spec:
      connectorRef: github_connector
      repoName: gitops-config
      sourceBranch: release/<+pipeline.sequenceId>
      targetBranch: main
      title: "Deploy <+service.name> to <+env.name>"
      commitMessage: "Update image tag to <+artifact.tag>"
      updateType: Json
      updates:
        - path: environments/<+env.name>/values.yaml
          key: image.tag
          value: <+artifact.tag>

- step:
    name: Merge PR
    identifier: mergePR
    type: MergePR
    spec:
      connectorRef: github_connector
      prNumber: <+pipeline.stages.Deploy.spec.execution.steps.createPR.output.prNumber>
      deleteSourceBranch: true
```

## Deployment Verification

### Continuous Verification

```yaml
- step:
    name: Verify Deployment
    identifier: verify
    type: Verify
    timeout: 2h
    spec:
      type: Canary
      monitoredService:
        type: Default
        spec: {}
      spec:
        sensitivity: MEDIUM
        duration: 15m
        deploymentTag: <+artifacts.primary.tag>
```

### Health Checks

```yaml
- step:
    name: HTTP Health Check
    identifier: healthCheck
    type: Http
    timeout: 5m
    spec:
      url: <+infra.variables.serviceUrl>/health
      method: GET
      assertion: <+httpResponseCode> == 200
      headers: []
```

## Rollback Strategies

### Automatic Rollback

```yaml
execution:
  steps:
    - step:
        name: Deploy
        identifier: deploy
        type: K8sRollingDeploy
        spec:
          skipDryRun: false
  rollbackSteps:
    - step:
        name: Rollback
        identifier: rollback
        type: K8sRollingRollback
        timeout: 10m
        spec: {}
failureStrategies:
  - onFailure:
      errors:
        - AllErrors
      action:
        type: StageRollback
```

### Manual Rollback

```yaml
- step:
    name: Rollback Confirmation
    identifier: rollbackConfirm
    type: HarnessApproval
    spec:
      approvalMessage: "Approve rollback to previous version?"
      approvers:
        userGroups:
          - account.Deployers
- step:
    name: Execute Rollback
    identifier: executeRollback
    type: K8sRollingRollback
    spec: {}
```

## Multi-Environment Promotion

### Environment Pipeline

```yaml
pipeline:
  name: Multi-Env Deploy
  identifier: multi_env_deploy
  stages:
    - stage:
        name: Deploy to Dev
        identifier: deploy_dev
        type: Deployment
        spec:
          deploymentType: Kubernetes
          environment:
            environmentRef: development

    - stage:
        name: Deploy to Staging
        identifier: deploy_staging
        type: Deployment
        spec:
          deploymentType: Kubernetes
          environment:
            environmentRef: staging
        when:
          pipelineStatus: Success
          condition: <+pipeline.stages.deploy_dev.status> == "SUCCEEDED"

    - stage:
        name: Approval for Production
        identifier: prod_approval
        type: Approval
        spec:
          execution:
            steps:
              - step:
                  type: HarnessApproval
                  spec:
                    approvers:
                      userGroups:
                        - account.ProductionApprovers

    - stage:
        name: Deploy to Production
        identifier: deploy_prod
        type: Deployment
        spec:
          deploymentType: Kubernetes
          environment:
            environmentRef: production
```

## Triggers

### Artifact Trigger

```yaml
trigger:
  name: New Artifact Trigger
  identifier: artifact_trigger
  pipelineIdentifier: deploy_pipeline
  source:
    type: Artifact
    spec:
      type: DockerRegistry
      spec:
        connectorRef: docker_connector
        imagePath: myorg/myapp
        tag: <+trigger.artifact.build>
```

### Webhook Trigger

```yaml
trigger:
  name: GitHub Webhook
  identifier: github_webhook
  pipelineIdentifier: deploy_pipeline
  source:
    type: Webhook
    spec:
      type: Github
      spec:
        type: Push
        spec:
          connectorRef: github_connector
          autoAbortPreviousExecutions: true
          payloadConditions:
            - key: targetBranch
              operator: Equals
              value: main
```

### Scheduled Trigger

```yaml
trigger:
  name: Nightly Deploy
  identifier: nightly_deploy
  pipelineIdentifier: deploy_pipeline
  source:
    type: Scheduled
    spec:
      type: Cron
      spec:
        expression: "0 2 * * *"  # 2 AM daily
        timezone: America/Los_Angeles
```

## CD Expressions

| Expression | Description |
|------------|-------------|
| `<+service.name>` | Service name |
| `<+service.identifier>` | Service identifier |
| `<+env.name>` | Environment name |
| `<+env.identifier>` | Environment identifier |
| `<+env.type>` | Environment type |
| `<+infra.name>` | Infrastructure name |
| `<+infra.connectorRef>` | Infrastructure connector |
| `<+infra.namespace>` | Kubernetes namespace |
| `<+artifact.image>` | Full artifact image |
| `<+artifact.tag>` | Artifact tag |
| `<+artifact.imagePath>` | Artifact image path |
| `<+pipeline.stages.STAGE.output.VAR>` | Stage output variable |

## API Operations

### Execute Deployment

```bash
curl -X POST "https://app.harness.io/pipeline/api/pipeline/execute/${PIPELINE_ID}?accountIdentifier=${ACCOUNT}&orgIdentifier=${ORG}&projectIdentifier=${PROJECT}" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "runtimeInputYaml": "pipeline:\n  stages:\n    - stage:\n        identifier: deploy\n        spec:\n          serviceConfig:\n            serviceRef: my_service\n            artifactSource:\n              image: myorg/myapp:v1.2.3"
  }'
```

### Get Deployment Status

```bash
curl -X GET "https://app.harness.io/pipeline/api/pipelines/execution/v2/${EXECUTION_ID}?accountIdentifier=${ACCOUNT}&orgIdentifier=${ORG}&projectIdentifier=${PROJECT}" \
  -H "x-api-key: ${API_KEY}"
```

### Trigger Rollback

```bash
curl -X PUT "https://app.harness.io/pipeline/api/pipelines/execution/interrupt/${EXECUTION_ID}?accountIdentifier=${ACCOUNT}&orgIdentifier=${ORG}&projectIdentifier=${PROJECT}" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"interruptType": "CUSTOM_FAILURE"}'
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Deployment timeout | Resource limits | Increase step timeout |
| Image pull failed | Auth issue | Verify connector credentials |
| Namespace not found | Infrastructure issue | Check infrastructure definition |
| Manifest error | Invalid YAML | Validate manifests locally |
| Approval timeout | No approver action | Review approval workflow |
| Rollback failed | Missing rollback steps | Add rollback configuration |

### Debug Steps

```yaml
- step:
    name: Debug Info
    identifier: debug
    type: ShellScript
    spec:
      shell: Bash
      source:
        type: Inline
        spec:
          script: |
            echo "=== Deployment Debug ==="
            echo "Service: <+service.name>"
            echo "Environment: <+env.name>"
            echo "Artifact: <+artifact.image>:<+artifact.tag>"
            echo "Namespace: <+infra.namespace>"
            kubectl get pods -n <+infra.namespace>
            kubectl get events -n <+infra.namespace> --sort-by='.lastTimestamp'
```

## Best Practices

1. **Use service overrides** for environment-specific configurations
2. **Implement approval gates** for production deployments
3. **Configure rollback strategies** for all deployment types
4. **Use GitOps** for declarative deployments
5. **Implement deployment verification** with CV or custom health checks
6. **Tag resources** for cost tracking and governance
7. **Use variables** for reusable pipeline configurations
8. **Implement failure strategies** at stage and step levels

## Related Documentation

- [Harness CD Docs](https://developer.harness.io/docs/continuous-delivery)
- [Deployment Strategies](https://developer.harness.io/docs/continuous-delivery/manage-deployments/deployment-concepts)
- [GitOps](https://developer.harness.io/docs/continuous-delivery/gitops)
- [Verification](https://developer.harness.io/docs/continuous-delivery/verify/cv-getstarted)
- [Harness API Reference](../docs/harness/API.md)
- [Harness CI Skill](../harness-ci/SKILL.md)
- [Harness Platform Skill](../harness-platform/SKILL.md)
