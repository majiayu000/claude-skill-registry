---
name: azure-release-pipeline
description: Design Azure release pipelines with deployment strategies and rollback. Use when creating release automation or deployment strategies.
---

# Azure Release Pipeline Skill

Azure Releaseパイプラインを構築するスキルです。

## 主な機能

- **環境管理**: Dev、Staging、Production
- **承認フロー**: 手動承認ゲート
- **デプロイ戦略**: Blue-Green、Rolling
- **ロールバック**: 自動・手動ロールバック

## Classic Release Pipeline (YAML代替)

```yaml
# 環境デプロイ with approvals
stages:
  - stage: Deploy_Staging
    jobs:
      - deployment: DeployStaging
        environment: Staging
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appName: 'myapp-staging'
                    package: '$(Pipeline.Workspace)/drop'

  - stage: Approval
    dependsOn: Deploy_Staging
    jobs:
      - job: WaitForValidation
        pool: server
        steps:
          - task: ManualValidation@0
            timeoutInMinutes: 1440
            inputs:
              notifyUsers: 'approvers@example.com'
              instructions: 'Please validate staging and approve'

  - stage: Deploy_Production
    dependsOn: Approval
    jobs:
      - deployment: DeployProduction
        environment: Production
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appName: 'myapp-prod'
                    package: '$(Pipeline.Workspace)/drop'
```

## デプロイゲート

```yaml
# Time-based gate
gates:
  - task: InvokeRESTAPI@1
    inputs:
      connectionType: 'connectedServiceName'
      method: 'GET'
      urlSuffix: '/health'
      waitForCompletion: 'true'
      successCriteria: 'eq(root.status, "healthy")'
```

## バージョン情報
- Version: 1.0.0
