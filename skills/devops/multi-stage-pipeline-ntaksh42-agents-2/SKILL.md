---
name: multi-stage-pipeline
description: Create multi-stage Azure Pipelines with deployment gates and approvals. Use when implementing complex deployment pipelines with multiple environments.
---

# Multi-Stage Pipeline Skill

Azure DevOpsマルチステージパイプラインを構築するスキルです。

## 主な機能

- **複数ステージ**: Build → Test → Deploy
- **承認ゲート**: 手動承認
- **並列実行**: 複数環境同時デプロイ
- **条件分岐**: ブランチ、環境による条件
- **デプロイ戦略**: Blue-Green、Canary

## 完全なマルチステージパイプライン

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: Common-Variables

stages:
  # ビルドステージ
  - stage: Build
    displayName: 'Build Application'
    jobs:
      - job: BuildJob
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '18.x'

          - script: |
              npm install
              npm run build
              npm test
            displayName: 'Build and Test'

          - task: PublishBuildArtifacts@1
            inputs:
              PathtoPublish: 'dist'
              ArtifactName: 'app'

  # テストステージ
  - stage: Test
    displayName: 'Run Tests'
    dependsOn: Build
    jobs:
      - job: UnitTests
        displayName: 'Unit Tests'
        steps:
          - script: npm run test:unit
            displayName: 'Run Unit Tests'

      - job: IntegrationTests
        displayName: 'Integration Tests'
        steps:
          - script: npm run test:integration
            displayName: 'Run Integration Tests'

      - job: E2ETests
        displayName: 'E2E Tests'
        steps:
          - script: npm run test:e2e
            displayName: 'Run E2E Tests'

  # セキュリティスキャン
  - stage: Security
    displayName: 'Security Scan'
    dependsOn: Build
    jobs:
      - job: SecurityScan
        steps:
          - task: WhiteSource@21
            inputs:
              cwd: '$(System.DefaultWorkingDirectory)'

  # Dev環境デプロイ
  - stage: Deploy_Dev
    displayName: 'Deploy to Dev'
    dependsOn: 
      - Test
      - Security
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    jobs:
      - deployment: DeployDev
        environment: 'Development'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Dev'
                    appName: 'myapp-dev'
                    package: '$(Pipeline.Workspace)/app'

  # Staging環境デプロイ
  - stage: Deploy_Staging
    displayName: 'Deploy to Staging'
    dependsOn: Deploy_Dev
    condition: succeeded()
    jobs:
      - deployment: DeployStaging
        environment: 'Staging'
        strategy:
          runOnce:
            preDeploy:
              steps:
                - script: echo "Pre-deployment validation"
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Staging'
                    appName: 'myapp-staging'
                    package: '$(Pipeline.Workspace)/app'
            routeTraffic:
              steps:
                - script: echo "Routing traffic"
            postRouteTraffic:
              steps:
                - task: InvokeRESTAPI@1
                  inputs:
                    connectionType: 'connectedServiceName'
                    serviceConnection: 'SmokeTests'
                    method: 'POST'
                    urlSuffix: '/run-smoke-tests'

  # Production環境デプロイ（承認必要）
  - stage: Deploy_Production
    displayName: 'Deploy to Production'
    dependsOn: Deploy_Staging
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProd
        environment: 'Production'  # 承認設定済み
        strategy:
          # Blue-Green デプロイ
          canary:
            increments: [10, 25, 50, 100]
            preDeploy:
              steps:
                - script: echo "Health check"
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Prod'
                    appName: 'myapp-prod'
                    package: '$(Pipeline.Workspace)/app'
                    deploymentMethod: 'zipDeploy'
            on:
              success:
                steps:
                  - script: echo "Deployment successful"
              failure:
                steps:
                  - script: echo "Rolling back"
                  - task: AzureAppServiceManage@0
                    inputs:
                      action: 'Swap Slots'
                      sourceSlot: 'staging'
```

## Canaryデプロイ

```yaml
strategy:
  canary:
    increments: [10, 25, 50, 100]
    deploy:
      steps:
        - script: echo "Deploying $(strategy.increment)%"
        - task: AzureTrafficManager@1
          inputs:
            trafficPercentage: $(strategy.increment)
```

## バージョン情報
- Version: 1.0.0
