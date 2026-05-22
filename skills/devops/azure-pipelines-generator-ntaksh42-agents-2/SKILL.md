---
name: azure-pipelines-generator
description: Generate Azure Pipelines YAML for CI/CD with multi-stage builds and deployments. Use when creating Azure DevOps pipelines or automating builds.
---

# Azure Pipelines Generator Skill

Azure PipelinesのYAML定義を生成するスキルです。

## 概要

CI/CDパイプラインをAzure Pipelines YAML形式で自動生成します。

## 主な機能

- **ビルドパイプライン**: CI設定
- **リリースパイプライン**: CD設定
- **マルチステージ**: ステージ分割
- **テンプレート**: 再利用可能な設定
- **条件付き実行**: ブランチ、タグ条件
- **環境デプロイ**: Dev、Staging、Production

## 基本パイプライン

### Node.js アプリケーション

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*
      - README.md

pool:
  vmImage: 'ubuntu-latest'

variables:
  nodeVersion: '18.x'
  buildConfiguration: 'Release'

stages:
  - stage: Build
    displayName: 'Build and Test'
    jobs:
      - job: BuildJob
        displayName: 'Build Application'
        steps:
          - task: NodeTool@0
            displayName: 'Install Node.js'
            inputs:
              versionSpec: $(nodeVersion)

          - task: Npm@1
            displayName: 'npm install'
            inputs:
              command: 'install'

          - task: Npm@1
            displayName: 'npm run build'
            inputs:
              command: 'custom'
              customCommand: 'run build'

          - task: Npm@1
            displayName: 'npm test'
            inputs:
              command: 'custom'
              customCommand: 'test'

          - task: PublishTestResults@2
            displayName: 'Publish Test Results'
            condition: succeededOrFailed()
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '**/test-results.xml'

          - task: PublishCodeCoverageResults@1
            displayName: 'Publish Code Coverage'
            inputs:
              codeCoverageTool: 'Cobertura'
              summaryFileLocation: '$(System.DefaultWorkingDirectory)/coverage/cobertura-coverage.xml'

          - task: PublishBuildArtifacts@1
            displayName: 'Publish Artifact: dist'
            inputs:
              PathtoPublish: '$(Build.SourcesDirectory)/dist'
              ArtifactName: 'dist'

  - stage: Deploy_Dev
    displayName: 'Deploy to Development'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    jobs:
      - deployment: DeployDev
        displayName: 'Deploy to Dev'
        environment: 'Development'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: DownloadBuildArtifacts@0
                  inputs:
                    artifactName: 'dist'

                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure Web App'
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appType: 'webAppLinux'
                    appName: 'myapp-dev'
                    package: '$(System.ArtifactsDirectory)/dist'

  - stage: Deploy_Prod
    displayName: 'Deploy to Production'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProd
        displayName: 'Deploy to Production'
        environment: 'Production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: DownloadBuildArtifacts@0
                  inputs:
                    artifactName: 'dist'

                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure Web App'
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appType: 'webAppLinux'
                    appName: 'myapp-prod'
                    package: '$(System.ArtifactsDirectory)/dist'
```

### .NET アプリケーション

```yaml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

variables:
  solution: '**/*.sln'
  buildPlatform: 'Any CPU'
  buildConfiguration: 'Release'

stages:
  - stage: Build
    jobs:
      - job: Build
        steps:
          - task: NuGetToolInstaller@1

          - task: NuGetCommand@2
            inputs:
              restoreSolution: '$(solution)'

          - task: VSBuild@1
            inputs:
              solution: '$(solution)'
              msbuildArgs: '/p:DeployOnBuild=true /p:WebPublishMethod=Package /p:PackageAsSingleFile=true /p:SkipInvalidConfigurations=true /p:PackageLocation="$(build.artifactStagingDirectory)"'
              platform: '$(buildPlatform)'
              configuration: '$(buildConfiguration)'

          - task: VSTest@2
            inputs:
              platform: '$(buildPlatform)'
              configuration: '$(buildConfiguration)'

          - task: PublishBuildArtifacts@1
            inputs:
              PathtoPublish: '$(Build.ArtifactStagingDirectory)'
              ArtifactName: 'drop'
```

### Docker ビルド & プッシュ

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  dockerRegistryServiceConnection: 'MyDockerRegistry'
  imageRepository: 'myapp'
  containerRegistry: 'myregistry.azurecr.io'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile'
  tag: '$(Build.BuildId)'

stages:
  - stage: Build
    jobs:
      - job: BuildAndPush
        steps:
          - task: Docker@2
            displayName: 'Build Docker Image'
            inputs:
              command: build
              repository: $(imageRepository)
              dockerfile: $(dockerfilePath)
              containerRegistry: $(dockerRegistryServiceConnection)
              tags: |
                $(tag)
                latest

          - task: Docker@2
            displayName: 'Push Docker Image'
            inputs:
              command: push
              repository: $(imageRepository)
              containerRegistry: $(dockerRegistryServiceConnection)
              tags: |
                $(tag)
                latest

  - stage: Deploy
    dependsOn: Build
    jobs:
      - deployment: DeployToAKS
        environment: 'kubernetes-prod'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: KubernetesManifest@0
                  displayName: 'Deploy to AKS'
                  inputs:
                    action: 'deploy'
                    kubernetesServiceConnection: 'AKS-Connection'
                    namespace: 'production'
                    manifests: |
                      $(Pipeline.Workspace)/manifests/deployment.yml
                      $(Pipeline.Workspace)/manifests/service.yml
                    containers: '$(containerRegistry)/$(imageRepository):$(tag)'
```

## テンプレート使用

### メインパイプライン

```yaml
# azure-pipelines.yml
trigger:
  - main

resources:
  repositories:
    - repository: templates
      type: git
      name: PipelineTemplates
      ref: refs/heads/main

stages:
  - template: templates/build-template.yml@templates
    parameters:
      nodeVersion: '18.x'

  - template: templates/deploy-template.yml@templates
    parameters:
      environment: 'Production'
      appName: 'myapp-prod'
```

### ビルドテンプレート

```yaml
# templates/build-template.yml
parameters:
  - name: nodeVersion
    type: string
    default: '18.x'

jobs:
  - job: Build
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - task: NodeTool@0
        inputs:
          versionSpec: ${{ parameters.nodeVersion }}

      - script: |
          npm install
          npm run build
          npm test
        displayName: 'Build and Test'
```

## PR トリガー

```yaml
# PR validation
pr:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*

trigger: none

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: Npm@1
    displayName: 'npm install'
    inputs:
      command: 'install'

  - task: Npm@1
    displayName: 'Run linter'
    inputs:
      command: 'custom'
      customCommand: 'run lint'

  - task: Npm@1
    displayName: 'Run tests'
    inputs:
      command: 'custom'
      customCommand: 'test'
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
