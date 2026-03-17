---
name: harness-eks-deployments
description: AWS EKS deployment patterns via Harness CD - Native Helm, Kubernetes manifests, and GitOps strategies with rolling, canary, and blue-green deployments
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
dependencies:
  - harness-code-integration
triggers:
  - eks deploy
  - harness eks
  - kubernetes deployment
  - helm deployment
  - canary deployment
  - blue green deployment
  - rolling deployment
  - eks pipeline
---

# Harness EKS Deployments Skill

Deploy to AWS EKS via Harness CD with Native Helm, Kubernetes manifests, or GitOps.

## Use For
- EKS deployment pipelines, deployment strategies (Rolling/Canary/Blue-Green)
- Native Helm deployments, GitOps with ArgoCD, multi-environment promotion

## Deployment Types

### Native Helm Deployment
```yaml
service:
  name: my-service
  serviceDefinition:
    type: NativeHelm
    spec:
      manifests:
        - manifest:
            identifier: helm_chart
            type: HelmChart
            spec:
              store:
                type: HarnessCode
                spec:
                  repoName: my-app
                  branch: main
                  folderPath: charts/my-service
              chartName: my-service
              chartVersion: <+input>
              helmVersion: V3
      artifacts:
        primary:
          primaryArtifactRef: ecr_image
          sources:
            - identifier: ecr_image
              type: Ecr
              spec:
                connectorRef: aws_connector
                region: us-west-2
                imagePath: my-service
                tag: <+input>
```

### Kubernetes Manifest Deployment
```yaml
service:
  name: my-service
  serviceDefinition:
    type: Kubernetes
    spec:
      manifests:
        - manifest:
            identifier: k8s_manifests
            type: K8sManifest
            spec:
              store:
                type: HarnessCode
                spec:
                  repoName: my-app
                  branch: main
                  paths:
                    - k8s/base
                    - k8s/overlays/<+env.name>
```

## Deployment Strategies

### Rolling (Zero-Downtime Default)
```yaml
execution:
  steps:
    - step:
        type: K8sRollingDeploy
        name: Rolling Deploy
        identifier: rolling_deploy
        spec:
          skipDryRun: false
        timeout: 10m
  rollbackSteps:
    - step:
        type: K8sRollingRollback
        name: Rollback
        identifier: rollback
```

### Canary (Progressive Traffic Shift)
```yaml
execution:
  steps:
    - step:
        type: K8sCanaryDeploy
        name: Canary 10%
        identifier: canary_10
        spec:
          instanceSelection:
            type: Percentage
            spec:
              percentage: 10
    - step:
        type: HarnessApproval
        name: Approve Canary
        spec:
          approvers:
            userGroups:
              - account.DevOpsTeam
    - step:
        type: K8sCanaryDeploy
        name: Canary 50%
        identifier: canary_50
        spec:
          instanceSelection:
            type: Percentage
            spec:
              percentage: 50
    - step:
        type: K8sCanaryDeploy
        name: Full Rollout
        identifier: full_rollout
        spec:
          instanceSelection:
            type: Percentage
            spec:
              percentage: 100
  rollbackSteps:
    - step:
        type: K8sCanaryDelete
        name: Canary Delete
        identifier: canary_delete
```

### Blue-Green (Instant Cutover)
```yaml
execution:
  steps:
    - step:
        type: K8sBGStageDeployment
        name: Stage Deployment
        identifier: stage_deployment
    - step:
        type: HarnessApproval
        name: Approve Switch
        spec:
          approvers:
            userGroups:
              - account.ProductionApprovers
    - step:
        type: K8sBGSwapServices
        name: Swap Services
        identifier: swap_services
  rollbackSteps:
    - step:
        type: K8sBGSwapServices
        name: Rollback Swap
        identifier: rollback_swap
```

## EKS Infrastructure Definition

```yaml
infrastructureDefinition:
  name: EKS Production
  identifier: eks_production
  type: KubernetesDirect
  spec:
    connectorRef: eks_connector
    namespace: <+service.name>-<+env.name>
    releaseName: <+service.name>
  allowSimultaneousDeployments: false
```

## AWS EKS Connector

```yaml
connector:
  name: EKS Production
  identifier: eks_production
  type: K8sCluster
  spec:
    credential:
      type: InheritFromDelegate
    delegateSelectors:
      - eks-delegate
```

## Environment Configuration

### Development
```yaml
environment:
  name: Development
  identifier: development
  type: PreProduction
  overrides:
    manifests:
      - manifest:
          identifier: values_override
          type: Values
          spec:
            store:
              type: HarnessCode
              spec:
                repoName: my-app
                branch: main
                paths:
                  - charts/my-service/values-dev.yaml
```

### Production
```yaml
environment:
  name: Production
  identifier: production
  type: Production
  overrides:
    manifests:
      - manifest:
          identifier: values_override
          type: Values
          spec:
            store:
              type: HarnessCode
              spec:
                repoName: my-app
                branch: main
                paths:
                  - charts/my-service/values-prod.yaml
```

## Verification & Health Checks

```yaml
- step:
    type: Verify
    name: Deployment Verification
    spec:
      type: Canary
      monitoredService:
        type: Default
      spec:
        sensitivity: MEDIUM
        duration: 5m
- step:
    type: Http
    name: Health Check
    spec:
      url: http://<+service.name>.<+infra.namespace>.svc.cluster.local/health
      method: GET
      assertion: <+httpResponseCode> == 200
```

## Multi-Environment Promotion Pipeline

```yaml
pipeline:
  name: EKS Promotion Pipeline
  stages:
    - stage:
        name: Deploy Dev
        type: Deployment
        spec:
          deploymentType: NativeHelm
          environment:
            environmentRef: development
          execution:
            steps:
              - step:
                  type: HelmDeploy
                  name: Helm Deploy
    - stage:
        name: Deploy Staging
        type: Deployment
        spec:
          environment:
            environmentRef: staging
        when:
          pipelineStatus: Success
    - stage:
        name: Deploy Production
        type: Deployment
        spec:
          environment:
            environmentRef: production
        when:
          pipelineStatus: Success
          condition: <+pipeline.stages.deploy_staging.status> == "SUCCEEDED"
```

## Common Expressions

| Expression | Purpose |
|------------|---------|
| `<+service.name>` | Service name |
| `<+env.name>` | Environment name |
| `<+env.type>` | Environment type (Production/PreProduction) |
| `<+infra.namespace>` | Kubernetes namespace |
| `<+infra.releaseName>` | Helm release name |
| `<+artifact.image>` | Full image path |
| `<+artifact.tag>` | Image tag |
| `<+pipeline.executionId>` | Pipeline execution ID |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Helm release failed | Check values file syntax, verify chart dependencies |
| Pod stuck in Pending | Check node resources, PVC availability |
| Image pull error | Verify ECR connector, check image exists |
| Namespace not found | Ensure namespace exists or set createNamespace: true |
| Rollback failed | Check rollback steps, verify previous release exists |
| Verification failed | Adjust sensitivity, extend duration |

## References
- [Harness EKS Tutorial](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/eks-deployments)
- [Native Helm Deployments](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/helm/native-helm-quickstart)
