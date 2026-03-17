---
name: harness-cd
description: Harness NextGen CD for continuous deployment including pipeline YAML structure, deployment strategies (rolling, blue-green, canary), GitOps workflows, approval gates, triggers, environments, services, manifests, Kubernetes deployments, Terraform integration, and secrets management. Activate for Harness pipeline creation, deployment automation, and GitOps configuration.
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
  - terraform-enterprise
  - vault-operations
triggers:
  - harness
  - pipeline
  - deployment
  - cd pipeline
  - gitops
  - continuous deployment
  - rollout
  - canary
  - blue-green
  - deployment strategy
---

# Harness CD Skill

Comprehensive Harness NextGen CD administration for enterprise continuous deployment with GitOps, Kubernetes, Terraform, and multi-cloud support.

## When to Use This Skill

Activate this skill when:
- Creating or managing Harness CD pipelines
- Configuring deployment strategies (rolling, blue-green, canary)
- Setting up GitOps workflows with Harness
- Integrating Kubernetes or Terraform deployments
- Configuring approval workflows and notifications
- Managing environments and infrastructure definitions
- Setting up triggers (webhook, scheduled, manual)
- Troubleshooting deployment failures
- Managing secrets and variables in pipelines

## Harness Pipeline Structure

### Basic Pipeline YAML

```yaml
pipeline:
  name: Example Deployment Pipeline
  identifier: example_deployment
  projectIdentifier: default
  orgIdentifier: default
  tags: {}
  stages:
    - stage:
        name: Deploy to Dev
        identifier: deploy_dev
        description: Deploy to development environment
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: my_service
            serviceInputs:
              serviceDefinition:
                type: Kubernetes
                spec:
                  variables:
                    - name: image_tag
                      type: String
                      value: <+input>
          environment:
            environmentRef: dev
            deployToAll: false
            infrastructureDefinitions:
              - identifier: dev_k8s
          execution:
            steps:
              - step:
                  name: Rollout Deployment
                  identifier: rolloutDeployment
                  type: K8sRollingDeploy
                  timeout: 10m
                  spec:
                    skipDryRun: false
            rollbackSteps:
              - step:
                  name: Rollback Rollout Deployment
                  identifier: rollbackRolloutDeployment
                  type: K8sRollingRollback
                  timeout: 10m
                  spec: {}
        tags: {}
        failureStrategies:
          - onFailure:
              errors:
                - AllErrors
              action:
                type: StageRollback
```

## Deployment Strategies

### Rolling Deployment

Rolling deployments gradually replace instances of the previous version with the new version.

```yaml
execution:
  steps:
    - step:
        name: Rolling Deployment
        identifier: rollingDeployment
        type: K8sRollingDeploy
        timeout: 10m
        spec:
          skipDryRun: false
          pruningEnabled: false
  rollbackSteps:
    - step:
        name: Rolling Rollback
        identifier: rollingRollback
        type: K8sRollingRollback
        timeout: 10m
        spec: {}
```

### Blue-Green Deployment

Blue-green deployments create a new environment (green) alongside the existing one (blue), then switch traffic.

```yaml
execution:
  steps:
    - step:
        name: Stage Deployment
        identifier: stageDeployment
        type: K8sBlueGreenDeploy
        timeout: 10m
        spec:
          skipDryRun: false
    - step:
        name: Swap Primary with Stage
        identifier: bgSwapServices
        type: K8sBlueGreenSwap
        timeout: 10m
        spec:
          skipDryRun: false
  rollbackSteps:
    - step:
        name: Swap Rollback
        identifier: rollbackBgSwap
        type: K8sBlueGreenSwapRollback
        timeout: 10m
        spec: {}
```

### Canary Deployment

Canary deployments gradually roll out changes to a small subset of users before rolling out to the entire infrastructure.

```yaml
execution:
  steps:
    - step:
        name: Canary Deployment
        identifier: canaryDeployment
        type: K8sCanaryDeploy
        timeout: 10m
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
        timeout: 10m
        spec: {}
    - step:
        name: Rolling Deployment
        identifier: rollingDeployment
        type: K8sRollingDeploy
        timeout: 10m
        spec:
          skipDryRun: false
  rollbackSteps:
    - step:
        name: Canary Delete
        identifier: rollbackCanaryDelete
        type: K8sCanaryDelete
        timeout: 10m
        spec: {}
    - step:
        name: Rolling Rollback
        identifier: rollingRollback
        type: K8sRollingRollback
        timeout: 10m
        spec: {}
```

## Services and Manifests

### Service Definition

```yaml
service:
  name: My Application
  identifier: my_application
  tags: {}
  serviceDefinition:
    spec:
      manifests:
        - manifest:
            identifier: k8s_manifests
            type: K8sManifest
            spec:
              store:
                type: Github
                spec:
                  connectorRef: github_connector
                  gitFetchType: Branch
                  branch: main
                  paths:
                    - kubernetes/
              valuesPaths:
                - values.yaml
              skipResourceVersioning: false
      artifacts:
        primary:
          primaryArtifactRef: <+input>
          sources:
            - spec:
                connectorRef: dockerhub_connector
                imagePath: myorg/myapp
                tag: <+input>
              identifier: docker_image
              type: DockerRegistry
      variables:
        - name: namespace
          type: String
          value: <+input>
        - name: replicas
          type: String
          value: "3"
    type: Kubernetes
```

### Helm Chart Service

```yaml
service:
  name: Helm Service
  identifier: helm_service
  serviceDefinition:
    spec:
      manifests:
        - manifest:
            identifier: helm_chart
            type: HelmChart
            spec:
              store:
                type: Http
                spec:
                  connectorRef: helm_connector
              chartName: mychart
              chartVersion: <+input>
              helmVersion: V3
              skipResourceVersioning: false
              valuesPaths:
                - values.yaml
      variables:
        - name: replicas
          type: String
          value: <+input>
    type: Kubernetes
```

## Environments and Infrastructure

### Environment Definition

```yaml
environment:
  name: Production
  identifier: production
  description: Production environment
  tags:
    env: prod
  type: Production
  orgIdentifier: default
  projectIdentifier: default
  variables:
    - name: namespace
      type: String
      value: production
    - name: cluster_name
      type: String
      value: prod-cluster
```

### Infrastructure Definition

```yaml
infrastructureDefinition:
  name: Production K8s
  identifier: prod_k8s
  description: Production Kubernetes cluster
  tags: {}
  orgIdentifier: default
  projectIdentifier: default
  environmentRef: production
  deploymentType: Kubernetes
  type: KubernetesDirect
  spec:
    connectorRef: k8s_connector
    namespace: <+env.variables.namespace>
    releaseName: release-<+INFRA_KEY>
  allowSimultaneousDeployments: false
```

## Triggers

### Webhook Trigger

```yaml
trigger:
  name: GitHub Webhook Trigger
  identifier: github_webhook
  enabled: true
  description: Trigger on GitHub push
  tags: {}
  orgIdentifier: default
  projectIdentifier: default
  pipelineIdentifier: example_deployment
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
          headerConditions: []
  inputYaml: |
    pipeline:
      identifier: example_deployment
      stages:
        - stage:
            identifier: deploy_dev
            type: Deployment
            spec:
              service:
                serviceInputs:
                  serviceDefinition:
                    type: Kubernetes
                    spec:
                      variables:
                        - name: image_tag
                          type: String
                          value: <+trigger.payload.after>
```

### Scheduled Trigger

```yaml
trigger:
  name: Nightly Deployment
  identifier: nightly_deployment
  enabled: true
  tags: {}
  orgIdentifier: default
  projectIdentifier: default
  pipelineIdentifier: example_deployment
  source:
    type: Scheduled
    spec:
      type: Cron
      spec:
        expression: 0 0 * * *  # Daily at midnight
        timezone: America/New_York
  inputYaml: |
    pipeline:
      identifier: example_deployment
      stages:
        - stage:
            identifier: deploy_dev
            type: Deployment
```

## GitOps with Harness

### GitOps Application

```yaml
application:
  name: My Application
  identifier: my_application
  orgIdentifier: default
  projectIdentifier: default
  clusterRef: prod_cluster
  repoURL: https://github.com/myorg/myapp
  path: kubernetes/
  targetRevision: main
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
  destination:
    namespace: production
    name: prod-cluster
```

### GitOps Cluster

```yaml
cluster:
  name: Production Cluster
  identifier: prod_cluster
  orgIdentifier: default
  projectIdentifier: default
  agentIdentifier: gitops_agent
  spec:
    config:
      type: KubernetesDirect
      spec:
        connectorRef: k8s_connector
```

## Approval Workflows

### Manual Approval

```yaml
- step:
    name: Approval
    identifier: approval
    type: HarnessApproval
    timeout: 1d
    spec:
      approvalMessage: Please review and approve deployment
      includePipelineExecutionHistory: true
      approvers:
        minimumCount: 1
        disallowPipelineExecutor: false
        userGroups:
          - account.Engineering_Managers
      approverInputs: []
```

### Jira Approval

```yaml
- step:
    name: Jira Approval
    identifier: jira_approval
    type: JiraApproval
    timeout: 1d
    spec:
      connectorRef: jira_connector
      projectKey: PROJ
      issueKey: <+input>
      approvalCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Done
      rejectionCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Rejected
```

## Variables and Expressions

### Pipeline Variables

```yaml
pipeline:
  variables:
    - name: environment
      type: String
      value: dev
    - name: image_tag
      type: String
      value: <+input>
    - name: replicas
      type: String
      value: <+input>.default(3)
    - name: enable_feature
      type: String
      value: <+input>.allowedValues(true,false)
```

### Common Expressions

| Expression | Description |
|------------|-------------|
| `<+pipeline.name>` | Pipeline name |
| `<+pipeline.sequenceId>` | Pipeline execution ID |
| `<+stage.name>` | Current stage name |
| `<+service.name>` | Service name |
| `<+env.name>` | Environment name |
| `<+artifact.tag>` | Artifact tag |
| `<+artifact.image>` | Full artifact image path |
| `<+secrets.getValue("my_secret")>` | Secret value |
| `<+trigger.payload.branch>` | Git branch from webhook |
| `<+codebase.commitSha>` | Git commit SHA |

## Secrets Management

### Reference Vault Secret

```yaml
- name: API_KEY
  type: String
  value: <+secrets.getValue("vault://path/to/secret#key")>
```

### Reference AWS Secrets Manager

```yaml
- name: DATABASE_PASSWORD
  type: String
  value: <+secrets.getValue("awsSecretsManager://my-secret")>
```

### Connector for HashiCorp Vault

```yaml
connector:
  name: Vault Connector
  identifier: vault_connector
  description: HashiCorp Vault
  orgIdentifier: default
  projectIdentifier: default
  type: Vault
  spec:
    vaultUrl: https://vault.example.com
    basePath: harness
    authToken: <+secrets.getValue("vault_token")>
    renewalIntervalMinutes: 60
    secretEngineManuallyConfigured: true
    secretEngineName: secret
    secretEngineVersion: 2
    readOnly: false
```

## Notifications

### Slack Notification

```yaml
notificationRules:
  - name: Slack Notification
    identifier: slack_notification
    pipelineEvents:
      - type: AllEvents
    notificationMethod:
      type: Slack
      spec:
        userGroups: []
        webhookUrl: <+secrets.getValue("slack_webhook")>
    enabled: true
```

### Email Notification

```yaml
notificationRules:
  - name: Email Notification
    identifier: email_notification
    pipelineEvents:
      - type: PipelineFailed
      - type: PipelineSuccess
    notificationMethod:
      type: Email
      spec:
        userGroups:
          - account.DevOps_Team
        recipients:
          - devops@example.com
    enabled: true
```

## Terraform Integration

### Terraform Plan Step

```yaml
- step:
    name: Terraform Plan
    identifier: terraformPlan
    type: TerraformPlan
    timeout: 10m
    spec:
      provisionerIdentifier: terraform_provisioner
      configuration:
        command: Apply
        configFiles:
          store:
            type: Github
            spec:
              gitFetchType: Branch
              connectorRef: github_connector
              branch: main
              folderPath: terraform/
        secretManagerRef: vault_connector
        varFiles:
          - varFile:
              identifier: tfvars
              spec:
                content: |
                  region = "<+pipeline.variables.region>"
                  environment = "<+pipeline.variables.environment>"
              type: Inline
```

### Terraform Apply Step

```yaml
- step:
    name: Terraform Apply
    identifier: terraformApply
    type: TerraformApply
    timeout: 10m
    spec:
      provisionerIdentifier: terraform_provisioner
      configuration:
        type: InheritFromPlan
```

## Shell Script Steps

```yaml
- step:
    name: Run Script
    identifier: runScript
    type: ShellScript
    timeout: 10m
    spec:
      shell: Bash
      onDelegate: true
      source:
        type: Inline
        spec:
          script: |
            #!/bin/bash
            echo "Deployment started for <+service.name>"
            echo "Environment: <+env.name>"
            echo "Image tag: <+artifact.tag>"

            # Custom validation
            if [ "<+env.name>" == "production" ]; then
              echo "Production deployment requires approval"
              exit 0
            fi
      environmentVariables:
        - name: SERVICE_NAME
          type: String
          value: <+service.name>
        - name: NAMESPACE
          type: String
          value: <+infra.namespace>
      outputVariables:
        - name: deployment_status
          type: String
          value: status
```

## Common Troubleshooting

### Issue: Pipeline Fails to Start

**Checklist:**
1. Verify all required inputs are provided
2. Check service and environment references are valid
3. Ensure connectors are configured and accessible
4. Verify RBAC permissions for the user/service account

### Issue: Manifest Not Found

**Solution:** Verify manifest paths and Git connector configuration

```yaml
manifests:
  - manifest:
      spec:
        store:
          spec:
            paths:
              - kubernetes/deployment.yaml  # Ensure path is correct
              - kubernetes/service.yaml
```

### Issue: Timeout During Deployment

**Solution:** Increase timeout and check Kubernetes cluster health

```yaml
- step:
    timeout: 30m  # Increase timeout
    spec:
      skipDryRun: false
```

### Issue: Secrets Not Resolving

**Solution:** Verify secret manager connector and secret path

```bash
# Test secret resolution
harness secret get vault://path/to/secret#key
```

## Best Practices

1. **Use GitOps** for declarative deployments with version control
2. **Implement approval gates** for production deployments
3. **Use canary or blue-green** for zero-downtime deployments
4. **Store all secrets** in Vault or cloud secret managers
5. **Enable auto-rollback** on deployment failures
6. **Use pipeline templates** for consistency across teams
7. **Implement proper tagging** for resources and pipelines
8. **Monitor pipeline execution** metrics and logs
9. **Use failure strategies** to handle errors gracefully
10. **Version your manifests** and Helm charts in Git

## File References

- See `references/pipeline-structure.md` for complete pipeline YAML reference
- See `references/deployment-strategies.md` for detailed strategy patterns
- See `references/triggers.md` for all trigger configurations
- See `references/gitops.md` for GitOps implementation patterns
- See `examples/` for production-ready pipeline examples
